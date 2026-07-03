# Inventário Classificado — scripts, workflows e dados
**Gerado em 23/06/2026.** Estado real do repositório, com recomendação de manter/arquivar/remover.
Legenda: 🟢 núcleo ativo · 🔵 gerador (reusável) · 🟡 lote único (já rodou) · 🟣 experimental · ⚪ morto/duplicado.

---

## A. Scripts Python (28)

### 🟢 Núcleo — o motor que você USA sempre
| Arquivo | Papel | Recomendação |
|---|---|---|
| `render_reel.py` | Motor de craft (frames 1080×1920, marca, safe-zone). Compartilhado. | **Manter** (coração) |
| `gerar_reel_voz.py` | Reel falado (edge-tts Antonio + áudio de estúdio). Caminho atual. | **Manter** |
| `publish.py` | Publicador Instagram (Graph API): post/story/seq/reel. | **Manter** (coração) |
| `carrossel.py` | Gera carrossel de feed (4:5, 1080×1350). | **Manter** |

### 🔵 Geradores / reabastecimento (reusáveis quando a fila baixar)
| Arquivo | Papel | Recomendação |
|---|---|---|
| `gerar_conteudo.py` | Renderer base de posts/stories (reabastecimento). | **Manter** |
| `gerar_sequencias.py` | Stories serializados (temporada semanal). | **Manter** |
| `gerar_temporadas.py` | (Re)constrói `sequences.json` de `temporadas_data.py`. | **Manter** |
| `gerar_reel_narrativo.py` | Preview de reel SEM voz (só música). | **Manter** (útil p/ prova rápida) |

### 🟡 Lotes únicos — já rodaram e populizaram os JSON (histórico)
| Arquivo | O que produziu | Recomendação |
|---|---|---|
| `gerar_reels.py` | Reels iniciais (cinetipografia). | **Arquivar** (`scripts_lote/`) |
| `gerar_lote_2026.py` | Posts+stories derivados dos 30 reels 2026. | **Arquivar** |
| `posts_batch1.py` / `posts_batch2.py` | post25–43 / post44–61. | **Arquivar** |
| `stories_batch.py` / `stories_batch2.py` | story40–60 / story61–90. | **Arquivar** |
| `reels_batch.py` | reel04+. | **Arquivar** |
| `anexar_lote_julho.py` | Montou entradas do `reels.json` do lote julho. | **Arquivar** |
| `publicar_narrativos.py` | Prepend dos narrativos no `reels.json`. | **Arquivar** |
> "Arquivar" = mover p/ uma pasta `scripts_lote/` (não apagar — são a memória de como a fila foi feita).
> **Não rodar de novo** sem necessidade: re-executar pode duplicar itens nas bibliotecas.

### 📇 Dados de episódio (conteúdo-fonte, não executável sozinho)
| Arquivo | Conteúdo | Recomendação |
|---|---|---|
| `episodios_pe_no_chao.py` | Agregador `get(id)` de todas as séries. | **Manter** |
| `episodios_novos_2026.py` | 30 episódios narrados 2026. | **Manter** |
| `episodios_lote_julho_2026.py` | 16 episódios julho. | **Manter** |
| `episodio_apresentacao.py` | Vídeo de apresentação (publicado). | **Manter** |
| `temporadas_data.py` | Dados das temporadas (5 frames/dia). | **Manter** |

### 🟣 Experimental — treino de voz própria (ramo separado, inacabado)
| Arquivo | Estado | Recomendação |
|---|---|---|
| `voz/orchestrator.py` | Vigia/treino (roda em Actions, cron). | **Decidir** (ver abaixo) |
| `voz/gcp_train.py` | Treino numa VM GPU do GCP. | **Decidir** |
| `voz/modal_voz.py` | Treino VITS no Modal. | **Decidir** |
| `voz/voz_kernel.py` | **Docstring vazia** — provável stub. | **Revisar/arquivar** |
| `voz_train.py` | **Docstring vazia** — provável stub. | **Revisar/arquivar** |
> ⚠️ Hoje a voz de produção é a **edge-tts (Antonio)** e funciona bem. Este ramo treina uma voz
> **própria/clonada** em **GPU do Kaggle** (orquestrado pelos workflows de voz; o custo no GitHub Actions
> é trivial — segundos). **Não desligar sem decidir** se o treino ainda é desejado (ver `03_AUDITORIA §1`).

### ⚪ Duplicado
| Arquivo | Observação | Recomendação |
|---|---|---|
| `publish_backup_single.py` | Cópia antiga do `publish.py`. | **Remover** (ou `scripts_lote/`) |

---

## B. Workflows do GitHub Actions (10)
| Workflow | Dispara | Gatilho | Recomendação |
|---|---|---|---|
| `publish.yml` | `publish.py` | **cron** (janelas) + manual | 🟢 **Manter** (é a agenda) |
| `render-reel-voz.yml` | `gerar_reel_voz.py` | manual | 🟢 **Manter** (render padrão) |
| `render-todos-reels.yml` | `gerar_reel_voz.py` (vários) | manual | 🔵 Manter |
| `render-reel-narrativo.yml` | `publicar_narrativos.py` | manual | 🔵 Manter |
| `render-conteudo-2026.yml` | `gerar_lote_2026.py` | manual | 🟡 Arquivar (lote feito) |
| `render-lote-2026.yml` | `gerar_reel_voz.py` | manual | 🟡 Arquivar (lote feito) |
| `render-lote-julho-2026.yml` | `anexar_lote_julho.py`+`gerar_reel_voz.py` | manual | 🟡 Arquivar (lote feito) |
| `render.yml` | `gerar_temporadas.py` | manual | 🔵 Manter |
| `voz-train.yml` | `voz/orchestrator.py` | **cron Seg/Qua/Sex 06:00** | 🟣 **Verificar** (treina voz no Kaggle; pausar só se abandonado) |
| `voz-watch.yml` | `voz/orchestrator.py` | **cron a cada 4h** | 🟣 **Verificar** (heartbeat do treino; idem) |

---

## C. Dados / mídia
| Item | Tamanho | Saúde |
|---|---|---|
| `reels.json` | 84 itens (11 publicados, **73 na fila**) | ✅ 0 refs quebradas |
| `posts.json` | 89 itens (9 pub, **80 fila**) | ✅ |
| `sequences.json` | 121 itens (16 pub, **105 fila**) | ✅ |
| `stories.json` | 89 itens (1 pub, fila **CONGELADA** em 88 — **APOSENTADA 03/07/2026**: ~97% dos temas já cobertos pelas sequências; reativação pontual via `FORCE_ID=storyNN`) | ✅ |
| `destaques.json` | 6 itens | ✅ |
| `images/*.jpg` | 1168 (1151 referenciadas, **17 órfãs**) | ⚠️ 17 órfãs (limpeza opcional) |
| `reels/*.mp4` | 85 (84 publicáveis + 55 `_preview_`) | ✅ |
| `state/published.json` | 44 registros | ✅ |

> **Runway:** com a fila atual e a cadência (8 feed/sem + 4 reels/sem + 1 seq/dia), há **meses** de
> conteúdo já pronto. O gargalo NÃO é falta de conteúdo.
