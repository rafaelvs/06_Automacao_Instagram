# Arquitetura do Motor — Instagram @rafaelvargasmd
**Repositório:** `rafaelvs/06_Automacao_Instagram` (público — a Meta busca a mídia por URL pública).
**Gerado em 23/06/2026** pela organização do motor. Documenta o sistema **como ele é hoje**.

---

## 1. Visão de uma frase
Um **motor de conteúdo faceless** (vídeo + carrossel + stories) gera mídia educativa de ortopedia,
guarda em **bibliotecas curadas** (JSON), e um **robô publica sozinho** no Instagram via **API oficial
da Meta**, rodando 100% de graça no **GitHub Actions**. Sem app aberto, sem celular, sem repetição.

---

## 2. O pipeline (conteúdo → no ar)

```
  [1] DADOS DE EPISÓDIO            [2] MOTOR DE RENDER            [3] BIBLIOTECAS (JSON)
  episodios_*.py  ───────────►  render_reel.py (craft 30fps) ──►  reels.json     (vídeos)
  temporadas_data.py            gerar_reel_voz.py (voz Antonio)    posts.json     (carrosséis)
  (cenas: k, sc, sub, vo)       carrossel.py (feed 4:5)           sequences.json (stories 5-frames)
                                gerar_conteudo/_sequencias        stories.json   (stories soltos)
                                        │                          destaques.json (highlights)
                                        ▼                                  │
                                  mídia em images/ e reels/                │
                                        └──────────────────────────────────┘
                                                       │
                                                       ▼
  [5] AGENDA (GitHub Actions)           [4] PUBLICADOR
  publish.yml (cron */30 + janelas) ──►  publish.py  ──►  Meta Graph API  ──►  Instagram
  render-*.yml (manual, sob demanda)         │                (graph.instagram.com)
                                             ▼
                                     state/published.json  (nada se repete)
```

**Princípio "biblioteca curada":** cada JSON é uma fila. O robô pega **o próximo item ainda não
publicado**, publica e marca em `state/published.json`. Quando a fila acaba, ele para (hora de
reabastecer). **Nada se repete.**

---

## 3. Componentes

### [1] Dados de episódio (o roteiro)
Cada episódio é um dict com `id`, `ep` (nº), `serie`, `motif_family` e uma lista de `scenes`.
Cada cena: `k` (kicker), `sc` (linhas grandes), `e` (palavra dourada de ênfase), `sub` (legenda),
`vo` (locução em **3ª pessoa**). Fontes: `episodios_pe_no_chao.py` (agregador), `episodios_novos_2026.py`,
`episodios_lote_julho_2026.py`, `episodio_apresentacao.py`, `temporadas_data.py`.

### [2] Motor de render — `render_reel.py`
- **1080×1920, 30fps**, desenhado com **Pillow** (sem editor de vídeo).
- Identidade: preto/creme/dourado (`#12121A`/`#F3E2C8`/`#B08C4F`), fontes **Liberation** (Serif p/
  títulos, Sans p/ corpo) — instaladas **só no Linux do Actions** (por isso não renderiza no Windows).
- Craft: easing com **overshoot** na entrada do texto, **palavra-chave dourada** com pop de escala,
  **motivos de marca** (`feet` = pegadas subindo / `bone` = osso novo + régua de mm), barra de
  progresso, **safe-zone** (rodapé CRM/RQE/disclaimer dentro da área visível, base livre p/ UI do IG).
- Rodapé fixo (CFM): `@rafaelvargasmd` · `Dr. Rafael Vargas · CRM-SP 226103 · RQE 137901` ·
  "Conteúdo educativo · não substitui avaliação médica."
- API interna: `render_frames(episode, durs, dir)` → JPGs; `encode(dir, audio_args, out)` → mp4 (ffmpeg).

### [2b] Camada de voz — `gerar_reel_voz.py`
- Sintetiza locução por cena com **edge-tts** (voz neural Microsoft **pt-BR-AntonioNeural**, grátis,
  sem chave). Botões: `EDGE_RATE` (ritmo, padrão −8%), `EDGE_PITCH` (tom, −4Hz). Alterna p/ Piper com
  `VOZ_ENGINE=piper`.
- **Cadeia de áudio de estúdio** (highpass, EQ, de-esser, compressor, limiter, loudnorm −14 LUFS) +
  mix voz/música (trilhas em `audio/`). Durações das cenas **seguem a voz**.
- Saída: `reels/_preview_<id>.mp4` — **o prefixo `_` mantém o preview FORA do `reels.json`** (não
  publica sozinho; é para revisão).

### [3] Bibliotecas de conteúdo (a fila)
| Arquivo | O que guarda | Campos por item |
|---|---|---|
| `reels.json` | vídeos (reels) | `id`, `video`, `caption` |
| `posts.json` | carrosséis do feed | `id`, `images[]`, `caption`, `alt` |
| `sequences.json` | stories serializados (5 frames/dia) | `id`, `theme`, `images[]` |
| `stories.json` | stories soltos | `id`, `image` |
| `destaques.json` | capas de Destaques | `id`, `image` |

### [4] Publicador — `publish.py`
- Publica via **Meta Graph API** (`graph.instagram.com`, Instagram Login). Suporta **post/carrossel**,
  **story**, **sequência** (5 stories em bloco), **reel**.
- **Trial Reels** (alcance de descoberta p/ não-seguidores, graduação automática `SS_PERFORMANCE`),
  **alt-text** (acessibilidade + SEO de imagem), **location_id** (SEO local) — tudo plugável por env.
- Lê a mídia por `raw.githubusercontent.com/<repo>/<ref>/<path>` → **por isso o repo é público**.
- `FORCE_ID=<id>` publica um item na hora (teste). `FORCE_ID=destaques` sobe as capas de Destaques.

### [5] Orquestração — GitHub Actions
- **`publish.yml`** — a agenda. Roda em **UTC** (BRT = UTC−3); o `publish.py` é quem decide se é hora.
  O estado garante **1 item por tipo por dia** mesmo com vários disparos.
- **`render-*.yml`** — rendem mídia sob demanda (manuais). Instalam fontes Liberation + ffmpeg + edge-tts.
- Secrets: `IG_USER_ID`, `IG_ACCESS_TOKEN`. Vars: `LOCATION_ID`, `TRIAL_REELS`, `TRIAL_GRADUATION`.

---

## 4. Agenda de publicação (decodificada — horário de Brasília)
| Tipo | Dias | Janela | Cadência |
|---|---|---|---|
| **Posts (feed)** | Ter / Qui / Sáb | ~15:00 | 3/sem |
| **Carrossel extra** | Dom | ~11:00 | +1/sem (feed 8/sem; dia-duplo com Reel) |
| **Stories (sequência 5-frames)** | todos os dias | ~12:30 | 1 sequência/dia |
| **Reels** | Seg / Qua / Sex / Dom | ~15:00 | 4/sem |
> O cron do GitHub é "melhor esforço" (atrasa); por isso há vários disparos adensados + um catch-all
> `*/30`. O `publish.py` ignora disparos fora da janela.

---

## 5. Guardrails CFM 2.336/2023 (embutidos)
Todo frame leva nome + CRM-SP 226103 + RQE 137901 + disclaimer educativo. Conteúdo **sob função**
(nunca estético/altura). A pasta `images/_removidos_estetica/` é a higiene CFM (artes que enquadravam
estética foram retiradas da fila). Ver guardrail [[guardrail-raio-x-exames-imagem]].

---

## 6. Por que NÃO renderiza no Windows local
`render_reel.py` aponta para `/usr/share/fonts/truetype/liberation/` e usa `ffmpeg`/`edge-tts`/`ffprobe`
no PATH e caminhos `/tmp`. Tudo isso existe **no Ubuntu do GitHub Actions**, não no Windows. Render é,
por design, **na nuvem** (grátis). Ver [[02_RUNBOOK]] para como disparar.
