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


def fingerprint(gerar_path=None, wf_path=None):
    g = (gerar_path or ROOT / "gerar_reel_voz.py").read_text(encoding="utf-8")
    w = (wf_path or ROOT / ".github" / "workflows" / "render-reel-voz.yml").read_text(encoding="utf-8")
    partes = {
        "engine_default": _extrai(g, r'ENGINE\s*=\s*os\.environ\.get\("VOZ_ENGINE"[^\n]*', "ENGINE"),
        "voz_default": _extrai(g, r'EDGE_VOICE\s*=\s*os\.environ\.get\("EDGE_VOICE"[^\n]*', "EDGE_VOICE"),
        "trim_sil": _extrai(g, r'TRIM_SIL\s*=\s*\(.*?\)\n', "TRIM_SIL"),
        "voice_chain": _extrai(g, r'VOICE_CHAIN\s*=\s*\(.*?\)\n', "VOICE_CHAIN"),
        "synth": _extrai(g, r'def synth\(.*?\n(?=def |\nclass |\Z)', "synth()"),
        "leads": _extrai(g, r'LEAD\s*=.*?\n', "LEAD") + _extrai(g, r'LEAD0\s*=.*?\n', "LEAD0"),
        "workflow_voz_env": _extrai(w, r'env:\s*\n\s*VOZ_ENGINE:.*?run: python gerar_reel_voz\.py[^\n]*', "env do workflow"),
        "workflow_inputs": _extrai(w, r'inputs:\s*\n.*?permissions:', "inputs do workflow"),
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
            # controle POSITIVO 3: mexer no rate default do workflow TEM de mudar
            w = (ROOT / ".github" / "workflows" / "render-reel-voz.yml").read_text(encoding="utf-8")
            (td / "w3.yml").write_text(w.replace('default: "-8%"', 'default: "+4%"'), encoding="utf-8")
            fp3, _ = fingerprint(wf_path=td / "w3.yml")
            r3 = fp3 != fp
            print(f"[{'ok' if r3 else 'FALHOU'}] positivo 3: mudar rate default do workflow muda o fingerprint")
            ok &= r3
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
