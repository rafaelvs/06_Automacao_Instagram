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

**Auditoria reproduzível:** `python _auditoria_motor.py` (na raiz do repo).

---

## TL;DR (estado em 23/06/2026)
- ✅ Sistema **saudável e no ar**: publica sozinho no Instagram via Meta Graph API (GitHub Actions).
- ✅ **0 referências de mídia quebradas**; **runway de meses** (73 reels, 80 posts, 105 sequências, 88 stories na fila).
- 🧭 Render é **na nuvem** (Actions, fontes Linux) — não roda no Windows local.
- ⏰ Única manutenção recorrente: **renovar o token da Meta a cada ~60 dias** (`02_RUNBOOK §5`).
- 🟣 Decisão pendente: manter ou pausar o **treino de voz própria** no Kaggle (`03_AUDITORIA §1`).
- 🧹 Organização de pastas: **opcional**, fazer em fases com teste (`04`) — nunca às cegas (quebra paths).
