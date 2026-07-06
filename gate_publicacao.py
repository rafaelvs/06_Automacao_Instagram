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
# seo_advisory_inline=False: o advisory do SEO YouTube e impresso mais abaixo no bloco [extra]
# do gate (para nao duplicar). A semantica de VIOLACOES/BLOQUEIOS/EXIT do IG NAO muda.
violacoes, revisar = checar_cfm.main(seo_advisory_inline=False)

print("\n=== [2/2] Lint termo->popular / termo vetado ===")
import checar_termo_popular
faltas, so_corpo = checar_termo_popular.main()

print("\n=== [3/3] Lint send + hook (advisory — descoberta/SPR) ===")
import checar_send_hook
hook_fraco, send_fraco = checar_send_hook.main()

# ADITIVO/ADVISORY: cobertura extra de send-ask nas bibliotecas (reels.json/posts.json).
# Só conta como AVISO (send fraco/ausente); JAMAIS entra em 'bloqueios'/exit=1.
print("\n=== [3b] Send-ask bibliotecas (reels/posts) — advisory ===")
try:
    _caps = checar_send_hook.relatorio_captions()
    send_libs_fraco = _caps["fraco"] + _caps["ausente"]
except Exception as e:
    print("AVISO: auditoria de captions falhou (fail-open — nao bloqueia):", e)
    send_libs_fraco = 0

# --- COBERTURA ADITIVA (ADVISORY): CFM sobre metadados publicos do YouTube (seo_episodios.json) ---
# Fecha a brecha em que title/title_alt/description/tags do motor SEO v2 nao passavam pelos
# guardrails CFM. E AVISO: NAO entra em BLOQUEIOS nem no exit — o gate do IG e a pipeline do
# YouTube sao desacoplados por design do Rafael (um titulo de YT nao pode travar a publicacao do IG).
# Promover isto a blocking, ou plugar o guardrail DENTRO da publicacao do YouTube (_cfm_guard),
# e decisao do Rafael.
print("\n=== [extra] CFM advisory — SEO YouTube (seo_episodios.json) ===")
try:
    seo_yt_viol, seo_yt_rev = checar_cfm.auditar_seo_youtube()
    checar_cfm.imprimir_seo_advisory(seo_yt_viol, seo_yt_rev)
    print(f"\n>>> SEO YouTube (CFM advisory): VIOLACAO={len(seo_yt_viol)} REVISAR={len(seo_yt_rev)} "
          f"(AVISO — nao afeta BLOQUEIOS/EXIT)")
except Exception as _e:
    print(f"AVISO: SEO YouTube advisory falhou: {_e} (fail-open — nao afeta o gate).")

bloqueios = len(violacoes) + len(faltas)
avisos = len(revisar) + len(so_corpo) + len(hook_fraco) + len(send_fraco) + send_libs_fraco

print("\n################ RESULTADO ################")
print(f"BLOQUEIOS (VIOLACAO CFM + FALTA termo->popular): {bloqueios}")
print(f"avisos (REVISAR + SO_CORPO, nao bloqueiam): {avisos}")
if bloqueios == 0:
    print(">>> PASS — conteudo liberado para render/publicacao.")
    sys.exit(0)
else:
    print(">>> FAIL — corrigir os bloqueios antes de publicar.")
    sys.exit(1)
