# -*- coding: utf-8 -*-
"""Guarda-freio de VOZ (regra do Rafael, 30/08/2026): qualquer alteração no motor de voz
exige um PILOTO aprovado por ele ANTES de renderizar os próximos episódios.

Como funciona: um fingerprint sha256 cobre tudo que define o SOM da voz publicada —
engine/voz default, cadeia de áudio (VOICE_CHAIN), trim de silêncio, o corpo da função
synth() e o bloco de env/inputs de voz do workflow render-reel-voz.yml. O fingerprint
APROVADO vive em voz_fingerprint.json. Se o atual divergir do aprovado, este script sai
com exit 1 — e o workflow de render fica VERMELHO antes de sintetizar 1 segundo de áudio.

Fluxo para mudar a voz de verdade (ex.: swap edge-tts -> Azure, voz clonada):
  1. Faça a mudança num branch/checkout local.
  2. Renderize UM episódio-piloto e envie ao Rafael.
  3. Com o "está prestando" dele registrado, rode:
       python checar_voz.py --registrar --evidencia "piloto <ep> aprovado pelo Rafael em <data> (<onde>)"
  4. Só então o render em lote volta a passar.

Uso:
  python checar_voz.py               # checa (exit 0 = voz vigente; 1 = mudou sem piloto)
  python checar_voz.py --auto-teste  # prova que o detector detecta (controle positivo + negativo)
  python checar_voz.py --registrar --evidencia "..."   # registra fingerprint novo (pós-piloto)
"""
import argparse
import os
import hashlib
import io
import json
import re
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
ROOT = Path(__file__).resolve().parent
REG = ROOT / "voz_fingerprint.json"


def _extrai(texto, padrao, rotulo, obrigatorio=True):
    m = re.search(padrao, texto, re.S)
    if not m:
        if obrigatorio:
            print(f"REPROVADO: não achei o bloco '{rotulo}' — a estrutura do arquivo mudou; "
                  f"isso TAMBÉM é mudança de voz até prova em contrário.")
            sys.exit(1)
        return ""
    return m.group(0)


def _chamadas_narrar(pasta):
    """Toda chamada narrar(...) do motor novo, por arquivo: é ali que o RITMO é passado. Um
    `voz.narrar(txt, "+25%", tmp)` num chamador trocava o ritmo sem tocar em voz.py."""
    out = []
    for f in sorted(os.listdir(pasta)):
        if f.endswith(".py") and f != "voz.py":
            t = (Path(pasta) / f).read_text(encoding="utf-8")
            out += [f"{f}: {c}" for c in re.findall(r"narrar\([^)\n]*\)", t)]
    return "\n".join(out)


def fingerprint(gerar_path=None, wf_path=None, animado_path=None, animado_dir=None):
    g = (gerar_path or ROOT / "gerar_reel_voz.py").read_text(encoding="utf-8")
    w = (wf_path or ROOT / ".github" / "workflows" / "render-reel-voz.yml").read_text(encoding="utf-8")
    # 18/10/2026: o motor NOVO (animado/, formatos CONVERSA e COMO FUNCIONA) tem a sua própria
    # voz — mesma Antonio, ritmo próprio. A regra do piloto vale para ela também: sem isto,
    # o ritmo da animação poderia mudar sem passar por ninguém.
    pasta = Path(animado_dir) if animado_dir else ROOT / "animado"
    a = (animado_path or pasta / "voz.py").read_text(encoding="utf-8")
    partes = {
        "engine_default": _extrai(g, r'ENGINE\s*=\s*os\.environ\.get\("VOZ_ENGINE"[^\n]*', "ENGINE"),
        "voz_default": _extrai(g, r'EDGE_VOICE\s*=\s*os\.environ\.get\("EDGE_VOICE"[^\n]*', "EDGE_VOICE"),
        "trim_sil": _extrai(g, r'TRIM_SIL\s*=\s*\(.*?\)\n', "TRIM_SIL"),
        "voice_chain": _extrai(g, r'VOICE_CHAIN\s*=\s*\(.*?\)\n', "VOICE_CHAIN"),
        "synth": _extrai(g, r'def synth\(.*?\n(?=def |\nclass |\Z)', "synth()"),
        "leads": _extrai(g, r'LEAD\s*=.*?\n', "LEAD") + _extrai(g, r'LEAD0\s*=.*?\n', "LEAD0"),
        "workflow_voz_env": _extrai(w, r'env:\s*\n\s*VOZ_ENGINE:.*?run: python gerar_reel_voz\.py[^\n]*', "env do workflow"),
        "workflow_inputs": _extrai(w, r'inputs:\s*\n.*?permissions:', "inputs do workflow"),
        "animado_voz": (_extrai(a, r'VOZ\s*=\s*"[^"\n]*"', "animado VOZ")
                        + _extrai(a, r'RITMO_COMO_FUNCIONA\s*=\s*"[^"\n]*"', "animado RITMO_COMO_FUNCIONA")
                        + _extrai(a, r'RITMO_CONVERSA\s*=\s*"[^"\n]*"', "animado RITMO_CONVERSA")
                        + _extrai(a, r'TOM\s*=\s*"[^"\n]*"', "animado TOM")
                        + _extrai(a, r'VOICE_CHAIN\s*=\s*\(.*?\)\n', "animado VOICE_CHAIN")),
        # auditoria 19/10: as constantes sozinhas não bastavam — trocar a voz DENTRO de _tts(),
        # fixar rate/pitch, tirar o "-af VOICE_CHAIN" de narrar() ou passar outro ritmo num
        # chamador davam o MESMO fingerprint. Agora entram os corpos e as chamadas.
        "animado_tts": _extrai(a, r'async def _tts\(.*?\n(?=\n\S|\Z)', "animado _tts()"),
        "animado_narrar": _extrai(a, r'def narrar\(.*?\n(?=\n\S|\Z)', "animado narrar()"),
        "animado_chamadas": _chamadas_narrar(pasta),
    }
    blob = json.dumps(partes, ensure_ascii=False, sort_keys=True)
    return hashlib.sha256(blob.encode("utf-8")).hexdigest(), partes


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--registrar", action="store_true")
    ap.add_argument("--evidencia", default="")
    ap.add_argument("--auto-teste", action="store_true")
    a = ap.parse_args()

    fp, partes = fingerprint()

    if a.auto_teste:
        import tempfile
        ok = True
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            g = (ROOT / "gerar_reel_voz.py").read_text(encoding="utf-8")
            # controle POSITIVO 1: trocar a voz default TEM de mudar o fingerprint
            (td / "g1.py").write_text(g.replace("pt-BR-AntonioNeural", "pt-BR-FranciscaNeural"),
                                      encoding="utf-8")
            fp1, _ = fingerprint(gerar_path=td / "g1.py")
            r1 = fp1 != fp
            print(f"[{'ok' if r1 else 'FALHOU'}] positivo 1: trocar EDGE_VOICE muda o fingerprint")
            ok &= r1
            # controle POSITIVO 2: mexer na cadeia de áudio TEM de mudar
            (td / "g2.py").write_text(g.replace("loudnorm=I=-16", "loudnorm=I=-13"), encoding="utf-8")
            fp2, _ = fingerprint(gerar_path=td / "g2.py")
            r2 = fp2 != fp
            print(f"[{'ok' if r2 else 'FALHOU'}] positivo 2: mexer na VOICE_CHAIN muda o fingerprint")
            ok &= r2
            # controle POSITIVO 3: mexer no rate default do workflow TEM de mudar.
            # 18/10/2026: o controle antigo trocava o texto literal 'default: "-8%"'. Quando a voz
            # aprovada passou a +8%, a troca virou no-op e o controle "falhou" sem o guarda ter
            # mudado — controle preso a um valor fixo apodrece na primeira mudança legítima. Agora
            # troca QUALQUER rate default por outro garantidamente diferente.
            w = (ROOT / ".github" / "workflows" / "render-reel-voz.yml").read_text(encoding="utf-8")
            atual = re.search(r'default: "([+-]\d+%)"', w)
            novo = "+37%" if not atual or atual.group(1) != "+37%" else "-37%"
            w3 = re.sub(r'default: "[+-]\d+%"', f'default: "{novo}"', w, count=1)
            assert w3 != w, "controle 3 nao conseguiu alterar o rate default (estrutura do workflow mudou)"
            (td / "w3.yml").write_text(w3, encoding="utf-8")
            fp3, _ = fingerprint(wf_path=td / "w3.yml")
            r3 = fp3 != fp
            print(f"[{'ok' if r3 else 'FALHOU'}] positivo 3: mudar rate default do workflow muda o fingerprint")
            ok &= r3
            # controle POSITIVO 4 (18/10/2026): mexer no ritmo da voz do motor NOVO TEM de mudar
            av = (ROOT / "animado" / "voz.py").read_text(encoding="utf-8")
            av4 = re.sub(r'RITMO_CONVERSA\s*=\s*"[^"]*"', 'RITMO_CONVERSA = "+37%"', av, count=1)
            if av4 == av:
                av4 = av.replace('RITMO_CONVERSA = "+37%"', 'RITMO_CONVERSA = "-37%"')
            (td / "a4.py").write_text(av4, encoding="utf-8")
            fp4, _ = fingerprint(animado_path=td / "a4.py")
            r4 = fp4 != fp
            print(f"[{'ok' if r4 else 'FALHOU'}] positivo 4: mudar o ritmo da voz do motor novo muda o fingerprint")
            ok &= r4
            # controles POSITIVOS 5-8 (auditoria 19/10): as quatro mutações que passavam batido
            import shutil
            mut = {
                "5: voz trocada dentro de _tts()": ("voz.py", "edge_tts.Communicate(texto, VOZ,",
                                                    'edge_tts.Communicate(texto, "pt-BR-FranciscaNeural",'),
                "6: rate/pitch fixos em _tts()": ("voz.py", "rate=rate, pitch=pitch", 'rate="+40%", pitch="-12Hz"'),
                "7: masterização tirada de narrar()": ("voz.py", '"-af", VOICE_CHAIN, ', ""),
                "8: chamador passa outro ritmo": ("conversa.py", "voz.RITMO_CONVERSA", '"+25%"'),
            }
            for nome, (arq, de, para) in mut.items():
                d = td / f"anim_{nome[0]}"
                shutil.copytree(ROOT / "animado", d, ignore=shutil.ignore_patterns("__pycache__"))
                t = (d / arq).read_text(encoding="utf-8")
                assert de in t, f"controle {nome}: trecho {de!r} sumiu de {arq} — atualize o controle"
                (d / arq).write_text(t.replace(de, para, 1), encoding="utf-8")
                fpm, _ = fingerprint(animado_dir=d)
                r = fpm != fp
                print(f"[{'ok' if r else 'FALHOU'}] positivo {nome} muda o fingerprint")
                ok &= r
            # controle NEGATIVO: comentário fora dos blocos de voz NÃO muda
            (td / "g4.py").write_text(g + "\n# comentário inócuo\n", encoding="utf-8")
            fp4, _ = fingerprint(gerar_path=td / "g4.py")
            r4 = fp4 == fp
            print(f"[{'ok' if r4 else 'FALHOU'}] negativo: comentário fora dos blocos não muda")
            ok &= r4
        print("AUTO-TESTE:", "PASSOU (o detector detecta)" if ok else "REPROVOU — não confiar no guarda")
        sys.exit(0 if ok else 1)

    if a.registrar:
        if not a.evidencia.strip() or "piloto" not in a.evidencia.lower():
            print("REPROVADO: --registrar exige --evidencia citando o PILOTO aprovado pelo Rafael "
                  "(regra de 30/08/2026: mudança de voz sem piloto não sobe).")
            sys.exit(1)
        REG.write_text(json.dumps({"fingerprint": fp, "evidencia": a.evidencia,
                                   "partes_rotulos": sorted(partes.keys())},
                                  ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
        print("registrado:", fp[:16], "…")
        sys.exit(0)

    if not REG.is_file():
        print("REPROVADO: voz_fingerprint.json não existe — registre a voz vigente com --registrar.")
        sys.exit(1)
    reg = json.loads(REG.read_text(encoding="utf-8"))
    if reg.get("fingerprint") != fp:
        print("REPROVADO: a configuração de VOZ mudou sem piloto aprovado registrado.")
        print(f"  aprovado: {reg.get('fingerprint', '?')[:16]}…  atual: {fp[:16]}…")
        print("  Regra (Rafael, 30/08/2026): renderize UM piloto, envie a ele, e registre com "
              "--registrar --evidencia 'piloto ... aprovado ...'. Sem isso, nada de lote.")
        sys.exit(1)
    print(f"ok: voz vigente confere com a aprovada ({fp[:16]}…)")
    sys.exit(0)


if __name__ == "__main__":
    main()
