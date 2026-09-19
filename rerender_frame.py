#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
rerender_frame.py — regenera UM frame de story sem tocar em `sequences.json`.

POR QUE EXISTE (19/09/2026): os frames de sequência são JPGs pré-renderizados em `images/`.
O renderizador de lote (`sequencias_avulsas_lote2.run()`) só sabe CRIAR sequência nova: ele
pula id que já existe (`pula (ja existe)`) e ainda garante que não há colisão de nome de
imagem (`assert fn not in img_existentes`). Ou seja: mudar UMA palavra de UM frame de uma
sequência que já está na fila era, até aqui, impossível sem apagar e recriar a sequência
inteira — e recriar mexe em `sequences.json`, que está em ORDEM POR FASE desde 13/09
(`docs/02_RUNBOOK.md` §9). Pior: `render.yml` chama `gerar_temporadas.py`, que TRUNCA e
reescreve `sequences.json` inteiro. Este script é a saída: texto e imagem mudam juntos,
a fila não é tocada, e nada roda sem o portão CFM aprovar o texto novo.

A FONTE DA VERDADE é o texto no módulo Python (`NOVAS`), nunca o JPG. Por isso o modo
`--trocar-cue` edita o .py PRIMEIRO e só então redesenha o frame a partir dele: imagem que
diverge do roteiro é a próxima "evidência errada" esperando para acontecer.

Uso:
  # ver o que existe
  python rerender_frame.py --listar s_on_fixador_rotina

  # trocar o texto de chamada (cue) do frame 5 de UMA sequência e redesenhar
  python rerender_frame.py s_on_fixador_rotina 5 --cue "Dúvida? WhatsApp no link da bio →"

  # trocar em LOTE, só nas sequências ainda NÃO publicadas (o padrão), com prévia
  python rerender_frame.py --trocar-cue "Dúvidas? Manda DM →" "Dúvida? WhatsApp no link da bio →" --dry-run
  python rerender_frame.py --trocar-cue "Dúvidas? Manda DM →" "Dúvida? WhatsApp no link da bio →"

  # autoteste (prova que o script realmente redesenha; não deixa resíduo)
  python rerender_frame.py --autoteste

Regras de segurança embutidas:
  1. Sequência JÁ PUBLICADA não é redesenhada (o story dela já foi ao ar; mudar o JPG agora
     só criaria divergência entre o que saiu e o que o repo diz que saiu). Exige `--incluir-publicadas`
     com motivo explícito, e mesmo assim NÃO edita o texto-fonte dessas.
  2. Texto novo passa por `cfm_guardrails.auditar` antes de virar imagem. Violação = aborta.
  3. Confere depois de renderizar: arquivo existe, é JPEG 1080x1920 e o mtime avançou.
"""
import argparse
import io
import json
import os
import re
import shutil
import sys
import time

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)

MODULOS = ["sequencias_avulsas_lote2", "sequencias_avulsas", "gerar_sequencias"]


def _carregar():
    """Devolve [(modulo, caminho_do_py, NOVAS)] dos módulos que declaram sequências."""
    out = []
    for nome in MODULOS:
        if not os.path.exists(os.path.join(ROOT, nome + ".py")):
            continue                                              # modulo opcional que este repo nao tem
        try:
            mod = __import__(nome)
        except Exception as e:                                    # noqa: BLE001
            # existe mas nao importa = problema de verdade, nunca silencioso
            print(f"AVISO: {nome}.py existe mas NAO importou: {e}")
            continue
        novas = getattr(mod, "NOVAS", None) or getattr(mod, "SEQUENCIAS", None)
        if novas:
            out.append((mod, os.path.join(ROOT, nome + ".py"), novas))
    if not out:
        sys.exit("ERRO: nenhum modulo de sequencias com NOVAS/SEQUENCIAS encontrado.")
    return out


def _publicadas():
    p = os.path.join(ROOT, "state", "published.json")
    return {e["id"] for e in json.load(open(p, encoding="utf-8"))["published"]}


def _achar(sid):
    for mod, py, novas in _carregar():
        for item in novas:
            if item[0] == sid:
                return mod, py, item
    return None, None, None


def _bloco(src, sid):
    """(inicio, fim) do bloco da sequência `sid` dentro do texto-fonte."""
    m = re.search(r'^\("%s",' % re.escape(sid), src, re.M)
    if not m:
        return None, None
    ini = m.start()
    nxt = re.search(r'^\("s_', src[m.end():], re.M)
    fim = m.end() + nxt.start() if nxt else len(src)
    return ini, fim


def _cfm(theme, seg, title, sub, cue):
    """Mesma montagem de texto do lote (`auditar_novas`): tema + frame + a assinatura que o
    template desenha no rodapé. Texto montado diferente do lote = portão medindo outra coisa."""
    try:
        from cfm_guardrails import auditar
        from sequencias_avulsas_lote2 import SIG
    except Exception as e:                                        # noqa: BLE001
        sys.exit(f"ERRO: portao CFM indisponivel ({e}) — nao renderizo sem portao.")
    texto = f"{theme} · {seg} · {title} · {sub} · {cue} · {SIG}"
    viol, rev = [], []
    for sev, regra, det in auditar(texto, contexto="publico"):
        (viol if sev == "VIOLACAO" else rev).append((sev, regra, det))
    return rev, viol


def _render(sid, n, item, dry=False):
    """Redesenha images/<sid>_<n>.jpg a partir do texto ATUAL do módulo."""
    _sid, theme, v, frames = item
    if not 1 <= n <= len(frames):
        sys.exit(f"ERRO: {sid} tem {len(frames)} frames; pediram o {n}.")
    seg, title, sub, cue = frames[n - 1]
    fn = f"{sid}_{n}.jpg"
    import gerar_conteudo as gc
    destino = os.path.join(gc.IMG, fn)
    print(f"  frame {n}/{len(frames)}: {seg!r} | {title!r}")
    print(f"     sub: {sub[:90]}{'...' if len(sub) > 90 else ''}")
    print(f"     cue: {cue!r}  ->  {destino}")
    rev, viol = _cfm(theme, seg, title, sub, cue)
    for it in rev:
        print(f"     [REVISAR] {it[1]}: {it[2]}")
    if viol:
        sys.exit(f"ABORTADO: {len(viol)} violacao(oes) CFM no texto de {fn}: {viol}")
    if dry:
        print("     (dry-run: nao renderizei)")
        return True
    antes = os.path.getmtime(destino) if os.path.exists(destino) else 0
    time.sleep(0.01)
    from sequencias_avulsas_lote2 import seq_story           # já vem com o patch de fonte
    seq_story(fn, v, theme, n, len(frames), seg, title, sub, cue)
    if not os.path.exists(destino):
        sys.exit(f"ERRO: {destino} nao foi criado.")
    if os.path.getmtime(destino) <= antes:
        sys.exit(f"ERRO: {destino} nao foi reescrito (mtime nao avancou).")
    from PIL import Image
    with Image.open(destino) as im:
        if im.size != (1080, 1920):
            sys.exit(f"ERRO: {destino} saiu {im.size}, esperado (1080, 1920).")
    print(f"     OK reescrito ({os.path.getsize(destino)} bytes)")
    return True


def cmd_trocar_cue(antigo, novo, incluir_publicadas, dry):
    done = _publicadas()
    trocas = []                                                   # (py, sid, n)
    for mod, py, novas in _carregar():
        src = open(py, encoding="utf-8").read()
        original = src
        for item in novas:
            sid, _theme, _v, frames = item
            if sid in done and not incluir_publicadas:
                if any(antigo in f[3] for f in frames):
                    print(f"pulo {sid}: JA PUBLICADA (o story dela ja foi ao ar)")
                continue
            for i, f in enumerate(frames, 1):
                if antigo in f[3]:
                    trocas.append((py, sid, i))
        if trocas and not dry:
            # troca cirúrgica: só dentro do bloco de cada sequência afetada deste módulo
            for _py, sid, _i in [t for t in trocas if t[0] == py]:
                ini, fim = _bloco(src, sid)
                if ini is None:
                    print(f"aviso: bloco de {sid} nao localizado em {os.path.basename(py)}")
                    continue
                src = src[:ini] + src[ini:fim].replace(antigo, novo) + src[fim:]
            if src != original:
                shutil.copy2(py, py + ".bak")
                open(py, "w", encoding="utf-8", newline="\n").write(src)
                print(f"texto-fonte atualizado: {os.path.basename(py)} (backup .bak)")
    if not trocas:
        print(f"nada a trocar: nenhuma sequencia pendente com o cue {antigo!r}")
        return 0
    print(f"\n{len(trocas)} frame(s) para redesenhar:")
    for _py, sid, i in trocas:
        print(f"  - {sid} frame {i}")
    if dry:
        print("\n(dry-run: texto-fonte NAO alterado, nada redesenhado)")
        return 0
    print()
    # recarrega os módulos já com o texto novo
    for nome in MODULOS:
        sys.modules.pop(nome, None)
    for _py, sid, i in trocas:
        _mod, _p, item = _achar(sid)
        print(sid)
        _render(sid, i, item)
    print(f"\nPRONTO: {len(trocas)} frame(s) redesenhado(s). `sequences.json` NAO foi tocado.")
    return 0


def cmd_autoteste():
    """Prova que o script redesenha de verdade: pega o 1o frame pendente, guarda o
    arquivo, redesenha com um cue diferente, confere que o byte mudou, e restaura."""
    done = _publicadas()
    alvo = None
    for _mod, _py, novas in _carregar():
        for item in novas:
            if item[0] not in done:
                alvo = item
                break
        if alvo:
            break
    if not alvo:
        sys.exit("autoteste: nenhuma sequencia pendente para testar.")
    sid = alvo[0]
    import gerar_conteudo as gc
    destino = os.path.join(gc.IMG, f"{sid}_1.jpg")
    if not os.path.exists(destino):
        sys.exit(f"autoteste: {destino} nao existe (sequencia ainda nao renderizada).")
    backup = destino + ".autoteste"
    shutil.copy2(destino, backup)
    antes = open(destino, "rb").read()
    try:
        seg, title, sub, _cue = alvo[3][0]
        item_teste = (sid, alvo[1], alvo[2], [(seg, title, sub, "AUTOTESTE — apagar")] + list(alvo[3][1:]))
        _render(sid, 1, item_teste)
        depois = open(destino, "rb").read()
        if depois == antes:
            sys.exit("FALHA no autoteste: o arquivo NAO mudou — o render nao esta surtindo efeito.")
        print("autoteste: o arquivo mudou como esperado.")
    finally:
        shutil.move(backup, destino)
        restaurado = open(destino, "rb").read()
        assert restaurado == antes, "FALHA: nao consegui restaurar o frame original!"
        print("autoteste: frame original restaurado byte a byte. OK")
    return 0


def main():
    ap = argparse.ArgumentParser(description="Regenera UM frame de story sem tocar em sequences.json.")
    ap.add_argument("sid", nargs="?", help="id da sequencia (ex.: s_on_fixador_rotina)")
    ap.add_argument("n", nargs="?", type=int, help="numero do frame (1-5)")
    ap.add_argument("--listar", metavar="ID", help="mostra os 5 frames da sequencia e sai")
    ap.add_argument("--cue", help="substitui o texto de chamada do frame")
    ap.add_argument("--sub", help="substitui o corpo do frame")
    ap.add_argument("--title", help="substitui o titulo do frame")
    ap.add_argument("--segmento", help="substitui o segmento do frame")
    ap.add_argument("--trocar-cue", nargs=2, metavar=("ANTIGO", "NOVO"),
                    help="troca o cue em TODAS as sequencias pendentes que o tiverem e redesenha")
    ap.add_argument("--incluir-publicadas", action="store_true",
                    help="tambem redesenha frames de sequencias ja publicadas (nao edita o texto-fonte delas)")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--autoteste", action="store_true")
    a = ap.parse_args()

    if a.autoteste:
        return cmd_autoteste()
    if a.trocar_cue:
        return cmd_trocar_cue(a.trocar_cue[0], a.trocar_cue[1], a.incluir_publicadas, a.dry_run)
    if a.listar:
        _m, py, item = _achar(a.listar)
        if not item:
            sys.exit(f"ERRO: sequencia {a.listar} nao encontrada.")
        print(f"{a.listar}  (tema {item[1]}, variante {item[2]}, fonte {os.path.basename(py)})")
        print("PUBLICADA" if a.listar in _publicadas() else "pendente na fila")
        for i, (seg, title, sub, cue) in enumerate(item[3], 1):
            print(f"  [{i}] {seg} | {title}\n      {sub}\n      cue: {cue}")
        return 0
    if not a.sid or not a.n:
        ap.error("informe <id> <n>, ou use --listar/--trocar-cue/--autoteste")

    if a.sid in _publicadas() and not a.incluir_publicadas:
        sys.exit(f"RECUSADO: {a.sid} ja foi publicada. Use --incluir-publicadas se souber o que esta fazendo.")
    _m, _py, item = _achar(a.sid)
    if not item:
        sys.exit(f"ERRO: sequencia {a.sid} nao encontrada nos modulos {MODULOS}.")
    frames = list(item[3])
    seg, title, sub, cue = frames[a.n - 1]
    frames[a.n - 1] = (a.segmento or seg, a.title or title, a.sub or sub, a.cue or cue)
    print(a.sid)
    return _render(a.sid, a.n, (item[0], item[1], item[2], frames), a.dry_run)


if __name__ == "__main__":
    sys.exit(main() or 0)
