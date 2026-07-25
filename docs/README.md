# 📂 docs/ — Documentação do Motor (Instagram @rafaelvargasmd)
Organização criada em **23/06/2026**. Comece por aqui.

| Doc | Para quê |
|---|---|
| [00_ARQUITETURA.md](00_ARQUITETURA.md) | Como o sistema funciona ponta a ponta (pipeline, componentes, agenda, CFM). |
| [01_INVENTARIO.md](01_INVENTARIO.md) | Cada script/workflow/dado classificado (manter/arquivar/verificar). |
| [02_RUNBOOK.md](02_RUNBOOK.md) | **Como usar no dia a dia**: render, publicar, token, troubleshooting. |
| [03_AUDITORIA.md](03_AUDITORIA.md) | Saúde do motor (runway, refs quebradas, pontos de atenção). |
| [04_ORGANIZACAO_PROPOSTA.md](04_ORGANIZACAO_PROPOSTA.md) | Estrutura-alvo + plano de migração seguro (em fases). |
| [05_YOUTUBE.md](05_YOUTUBE.md) | **Série "Recuperação" no YouTube**: o que está no ar, decisões (upload manual, gate CFM) e runbook. |
| [05a_YOUTUBE_COLAR.md](05a_YOUTUBE_COLAR.md) | Título/descrição/tags prontos para colar no YouTube Studio (gerado de `seo_episodios.json`). |
| [05_MANUTENCAO.md](05_MANUTENCAO.md) | Manutenção recorrente do motor (token, agenda, checagens). |
| [ESTRATEGIA_YOUTUBE_2026.md](ESTRATEGIA_YOUTUBE_2026.md) | 📺 Ganchos, título, descrição, tags e gate de SEO. Fonte de `seo_youtube.py` e `ganchos.py`. |
| [GUIA_PRODUCAO_RECUPERACAO.md](GUIA_PRODUCAO_RECUPERACAO.md) | 🩺 Convenções da série "Recuperação" + regras R1-R7. Fonte de `_lint_recuperacao.py`. |
| [SETUP_MODAL.md](SETUP_MODAL.md) | 🎙️ Bootstrap e operação do treino da voz pt-BR. Fonte de `voz/modal_voz.py`. |

> ⚠️ Os três docs normativos acima foram **reconstruídos em 25/07/2026** a partir do que já estava
> codificado nos scripts que os citam — os originais viviam fora do Git e se perderam na troca de máquina.

**Auditoria reproduzível:** `python _auditoria_motor.py` (na raiz do repo).

---

## TL;DR (estado em 23/06/2026)
- ✅ Sistema **saudável e no ar**: publica sozinho no Instagram via Meta Graph API (GitHub Actions).
- ✅ **0 referências de mídia quebradas**; **runway de meses** (73 reels, 80 posts, 105 sequências, 88 stories na fila).
- 🧭 Render é **na nuvem** (Actions, fontes Linux) — não roda no Windows local.
- ⏰ Única manutenção recorrente: **renovar o token da Meta a cada ~60 dias** (`02_RUNBOOK §5`).
- 🟣 Decisão pendente: manter ou pausar o **treino de voz própria** no Kaggle (`03_AUDITORIA §1`).
- 🧹 Organização de pastas: **opcional**, fazer em fases com teste (`04`) — nunca às cegas (quebra paths).
