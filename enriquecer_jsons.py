# -*- coding: utf-8 -*-
"""
BACKFILL — grava o TEXTO DE TELA dentro de sequences.json / stories.json / destaques.json.

POR QUE
-------
publish.py roda no publish.yml, que instala SO requirements.txt (requests). Se o
_cfm_guard tentasse resolver o texto importando checar_frames, puxaria gerar_conteudo ->
carrossel -> PIL, ausente naquele runner: o import falharia e cairia no fail-open, ou
seja, um guardrail que se desliga sozinho todo dia. Materializar o texto no JSON deixa
publish.py auditar com ZERO import novo alem de stdlib.

O QUE GRAVA
-----------
  sequences.json : "frames": [{"seg","title","sub","cue"} x5]
  stories.json   : "kicker","title","sub"
  destaques.json : "kicker","title","sub"
Itens cujo texto veio de transcricao de imagem levam tambem:
  "texto_origem": "transcricao"  e  "texto_revisado": false
Itens com fonte viva em codigo levam "texto_origem": "codigo".

TRAVAS
------
- FAIL-CLOSED de cobertura: se QUALQUER item nao resolver texto, ou se qualquer fonte
  falhar ao importar, NAO escreve nada. Backfill parcial e pior que nenhum: daria
  falsa sensacao de cobertura, que e exatamente o furo que este trabalho fecha.
- IDEMPOTENTE: reprocessar produz o mesmo arquivo. Nao duplica nem reordena campos.
- DRY-RUN por padrao. So escreve com --aplicar.

ATENCAO — este backfill sozinho NAO basta: gerar_temporadas.py reescreve
sequences.json inteiro a cada rodada e apagaria os frames. Os geradores precisam
passar a gravar o texto que renderizam (patch separado).

Rodar:  python enriquecer_jsons.py            (dry-run, so relatorio)
        python enriquecer_jsons.py --aplicar  (escreve)
"""
import json
import os
import sys

from checar_frames import frames_sequencias, textos_stories, textos_transcritos

ROOT = os.path.dirname(os.path.abspath(__file__))


def _carrega(arq):
    with open(os.path.join(ROOT, arq), encoding="utf-8") as fh:
        return json.load(fh)


def _grava(arq, dados):
    with open(os.path.join(ROOT, arq), "w", encoding="utf-8") as fh:
        json.dump(dados, fh, ensure_ascii=False, indent=2)
        fh.write("\n")


def construir():
    """Retorna (saidas, faltando, falhas). saidas: {arquivo: lista_enriquecida}."""
    seq_txt, f1 = frames_sequencias()
    sto_txt, f2 = textos_stories()
    tra_txt, _meta, f3 = textos_transcritos()
    falhas = f1 + f2 + f3
    faltando = []
    saidas = {}

    # --- sequences.json ---
    seqs = _carrega("sequences.json")
    for it in seqs:
        src = seq_txt.get(it.get("id"))
        if not src:
            faltando.append(("sequences.json", it.get("id")))
            continue
        it["frames"] = [
            {"seg": f[0], "title": f[1], "sub": f[2], "cue": f[3]}
            for f in (tuple(list(fr) + ["", "", "", ""])[:4] for fr in src["frames"])
        ]
        it["texto_origem"] = "codigo"
    saidas["sequences.json"] = seqs

    # --- stories.json e destaques.json ---
    for arq in ("stories.json", "destaques.json"):
        itens = _carrega(arq)
        for it in itens:
            _id = it.get("id")
            if _id in sto_txt:
                k, t, s = sto_txt[_id]
                it["kicker"], it["title"], it["sub"] = k, t, s
                it["texto_origem"] = "codigo"
            elif _id in tra_txt:
                r = tra_txt[_id]
                it["kicker"] = r.get("kicker", "")
                it["title"] = r.get("title", "")
                it["sub"] = r.get("sub", "")
                it["texto_origem"] = "transcricao"
                it["texto_revisado"] = bool(r.get("revisado", False))
            else:
                faltando.append((arq, _id))
        saidas[arq] = itens

    return saidas, faltando, falhas


def main(aplicar=False):
    saidas, faltando, falhas = construir()

    print("=== BACKFILL DE TEXTO DE TELA ===")
    for arq, itens in saidas.items():
        com = sum(1 for it in itens if "frames" in it or "title" in it)
        transcritos = sum(1 for it in itens if it.get("texto_origem") == "transcricao")
        print(f"{arq:18s} {len(itens):4d} itens | {com:4d} com texto | {transcritos:3d} de transcricao")

    if falhas:
        print(f"\n!!! {len(falhas)} fonte(s) nao carregaram:")
        for fonte, err in falhas:
            print(f"   [FALHA] {fonte}: {err}")
    if faltando:
        print(f"\n!!! {len(faltando)} item(ns) sem texto resolvivel:")
        for arq, _id in faltando[:30]:
            print(f"   [SEM TEXTO] {arq}: {_id}")

    if falhas or faltando:
        print("\nABORTADO — cobertura incompleta. Backfill parcial daria falsa cobertura,")
        print("que e exatamente o furo que este trabalho fecha. Nada foi escrito.")
        return 1

    nao_revisados = sum(1 for itens in saidas.values() for it in itens
                        if it.get("texto_revisado") is False)
    print(f"\nCobertura COMPLETA. {nao_revisados} itens com texto_revisado=false "
          f"(transcricao pendente de conferencia medica).")

    if not aplicar:
        print("\nDRY-RUN — nada escrito. Rode com --aplicar para gravar.")
        return 0

    for arq, itens in saidas.items():
        _grava(arq, itens)
        print(f"gravado: {arq}")
    return 0


if __name__ == "__main__":
    sys.exit(main(aplicar="--aplicar" in sys.argv))
