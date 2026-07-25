# -*- coding: utf-8 -*-
"""
GATE DE PUBLICAÇÃO — YOUTUBE. Porta única do caminho YouTube (série "Recuperação").
Idempotente, só leitura. FALHA (exit 1) se houver bloqueio.

DECISÃO (25/07/2026, Rafael) — resolve o TODO que estava em checar_cfm.py e gate_publicacao.py:
a auditoria CFM dos metadados públicos do YouTube (seo_episodios.json) É BLOQUEANTE, mas AQUI,
num gate próprio. NÃO foi promovida dentro de gate_publicacao.py de propósito: o gate do
Instagram e o caminho do YouTube seguem DESACOPLADOS — um título de YouTube não pode travar a
publicação do Instagram. Assim o CFM passa a ser exigível nos dois canais sem acoplá-los.
Base da decisão: na data, os 34 episódios davam 0 VIOLACAO (só 4 REVISAR por citarem
"radiografia"), ou seja, tornar bloqueante não custou nada e trava regressões futuras.

Bloqueios (FAIL, exit 1):
  - VIOLACAO de CFM em title / title_alt / description / tags (cfm_guardrails via checar_cfm)
  - Episódio com score SEO < 80 (mesmas regras e pesos de _lint_seo.py --strict)
Avisos (não bloqueiam): REVISAR do CFM; episódios com score 80–99.

Rodar:  python gate_youtube.py                    (todos os 34)
        python gate_youtube.py banho_posop ...    (só esses ids)
        (no Windows use PYTHONIOENCODING=utf-8)

Quando rodar: ANTES de colar metadados no YouTube Studio — inclusive ao editar vídeo já no ar.
O upload em si é MANUAL, por decisão registrada em docs/05_YOUTUBE.md.
"""
import json
import os
import sys

import checar_cfm
import _lint_seo

ROOT = os.path.dirname(os.path.abspath(__file__))
JSON_PATH = os.path.join(ROOT, "seo_episodios.json")


def main():
    filtro = [a for a in sys.argv[1:] if not a.startswith("--")]

    print("######## GATE DE PUBLICACAO — YOUTUBE ########\n")

    with open(JSON_PATH, encoding="utf-8") as f:
        dados = json.load(f)

    if filtro:
        for k in filtro:
            if k not in dados:
                print(f"AVISO: id '{k}' nao existe em seo_episodios.json — ignorado.")
        dados = {k: v for k, v in dados.items() if k in filtro}

    if not dados:
        print(">>> FAIL — nenhum episodio para auditar.")
        sys.exit(1)

    # ── [1/2] CFM sobre os metadados publicos — AQUI E BLOQUEANTE ────────────────────────────
    # Reusa a MESMA funcao que o gate do IG chama como advisory; a diferenca esta no que fazemos
    # com o resultado (aqui VIOLACAO entra em 'bloqueios' e derruba o exit).
    print("=== [1/2] CFM dos metadados publicos (BLOQUEANTE aqui) ===")
    violacoes, revisar = checar_cfm.auditar_seo_youtube()
    # a funcao compartilhada se anuncia como "(advisory)" — verdade no gate do IG, nao aqui.
    print("   ^ o '(advisory)' acima e da funcao compartilhada; NESTE gate VIOLACAO bloqueia.")
    if filtro:
        violacoes = [t for t in violacoes if t[1] in dados]
        revisar = [t for t in revisar if t[1] in dados]

    print(f"VIOLACAO={len(violacoes)}  REVISAR={len(revisar)}")
    for origem, _id, _sev, regra, det in violacoes:
        print(f"   [VIOLACAO] {origem:16s} {str(_id):26s} {regra}: {det}")
    for origem, _id, _sev, regra, det in revisar[:40]:
        print(f"   [revisar ] {origem:16s} {str(_id):26s} {regra}: {det}")

    # ── [2/2] Qualidade SEO — reprovado (<80) BLOQUEIA ───────────────────────────────────────
    print("\n=== [2/2] Qualidade SEO (score < 80 bloqueia) ===")
    reprovados = []
    com_aviso = 0
    n_isentos = 0
    for eid, ent in dados.items():
        # ATENCAO: lint_entry devolve TRES valores desde a isencao TITULO_DO_CANAL (EP07-28) em
        # _lint_seo.py — (score, issues, isentos). Desempacotar em dois quebra este gate.
        score, issues, isentos = _lint_seo.lint_entry(eid, ent)
        if isentos:
            n_isentos += 1
        if not issues:
            continue
        flag = "ERR" if score < 80 else "wrn"
        print(f"{flag}  {eid:<30} {score:3}/100")
        for nome, msg in issues:
            print(f"     [{nome}] {msg}")
        if score < 80:
            reprovados.append(eid)
        else:
            com_aviso += 1
    print(f"auditados: {len(dados)} | reprovados (<80): {len(reprovados)} | com aviso (80-99): {com_aviso}"
          f" | isentos de TITLE_LEN_MIN: {n_isentos}")

    bloqueios = len(violacoes) + len(reprovados)
    avisos = len(revisar) + com_aviso

    print("\n################ RESULTADO ################")
    print(f"BLOQUEIOS (VIOLACAO CFM + SEO < 80): {bloqueios}")
    print(f"avisos (REVISAR CFM + SEO 80-99, nao bloqueiam): {avisos}")
    if bloqueios == 0:
        print(">>> PASS — metadados liberados para publicar/editar no YouTube.")
        sys.exit(0)
    print(">>> FAIL — corrigir os bloqueios antes de publicar no YouTube.")
    sys.exit(1)


if __name__ == "__main__":
    main()
