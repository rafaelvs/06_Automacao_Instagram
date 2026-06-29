# -*- coding: utf-8 -*-
"""
GATE DE PUBLICAÇÃO — porta única de checagem antes de renderizar/publicar conteúdo.
Roda os lints do projeto e FALHA (exit 1) se houver bloqueio. Idempotente, só leitura.

Rodar:  python gate_publicacao.py   (use PYTHONIOENCODING=utf-8 no Windows)
Plugar (quando quiser): chamar antes do passo de publish/render no workflow, ou como pre-commit.

Bloqueios (FAIL):
  - VIOLACAO de CFM (cfm_guardrails: promessa, estética/altura, raio-X/exame real, termo vetado 'dismetria')
  - FALTA de termo→popular (jargão sem nome popular no gancho/legenda)
Avisos (não bloqueiam): REVISAR (CFM) e SO_CORPO (termo→popular).
"""
import sys

print("######## GATE DE PUBLICACAO ########\n")

print("=== [1/2] Lint CFM ===")
import checar_cfm
violacoes, revisar = checar_cfm.main()

print("\n=== [2/2] Lint termo->popular / termo vetado ===")
import checar_termo_popular
faltas, so_corpo = checar_termo_popular.main()

print("\n=== [3/3] Lint send + hook (advisory — descoberta/SPR) ===")
import checar_send_hook
hook_fraco, send_fraco = checar_send_hook.main()

bloqueios = len(violacoes) + len(faltas)
avisos = len(revisar) + len(so_corpo) + len(hook_fraco) + len(send_fraco)

print("\n################ RESULTADO ################")
print(f"BLOQUEIOS (VIOLACAO CFM + FALTA termo->popular): {bloqueios}")
print(f"avisos (REVISAR + SO_CORPO, nao bloqueiam): {avisos}")
if bloqueios == 0:
    print(">>> PASS — conteudo liberado para render/publicacao.")
    sys.exit(0)
else:
    print(">>> FAIL — corrigir os bloqueios antes de publicar.")
    sys.exit(1)
