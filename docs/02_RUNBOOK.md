# Runbook Operacional — usar o motor no dia a dia
**Gerado em 23/06/2026.** Tudo roda na nuvem (GitHub Actions). Você não precisa de ffmpeg/Python local.
Pré-requisito: estar logado no `gh` (CLI) **ou** usar a interface web do GitHub (aba **Actions**).

---

## 0. Mapa rápido "quero… → faça…"
| Quero… | Faça |
|---|---|
| Publicar tudo no automático | **Nada.** O `publish.yml` já roda sozinho (ver agenda em `00_ARQUITETURA §4`). |
| Soltar 1 reel novo na fila | **§1** (render) → **§2** (entrar no `reels.json`). |
| Soltar 1 carrossel / story | **§3**. |
| Testar publicação agora | **§4** (FORCE_ID). |
| Renovar o token (a cada ~60d) | **§5**. |
| Algo falhou | **§6** (troubleshooting). |

---

## 1. Render de um Reel novo (na nuvem)
**Web:** aba **Actions → "render-reel-voz" → Run workflow** e preencha:
- `episodio`: id do episódio (ex.: `andador`, `pe_torto`, `displasia_quadril`, `quando_procurar`…).
  Os ids vivem em `episodios_*.py` (função `get(id)` em `episodios_pe_no_chao.py`).
- `rate`: ritmo do Antonio (padrão `-8%`, mais conversacional). `pitch`: tom (padrão `-4Hz`).

**CLI:**
```bash
gh workflow run render-reel-voz.yml -f episodio=pe_torto -f rate=-8% -f pitch=-4Hz
gh run watch   # acompanha; ao fim, o mp4 é commitado em reels/_preview_<id>.mp4
```
O resultado sai como **`reels/_preview_<id>.mp4`** (artefato + commit). O prefixo **`_` = preview**:
fica **fora** do `reels.json`, então **não publica sozinho**. Baixe e revise.

> Para renderizar SEM voz (prova rápida de craft): workflow `render-reel-narrativo`.

---

## 2. Transformar um preview aprovado em Reel publicável
O `publish.py` só publica o que está no **`reels.json`**. Então, depois de aprovar o preview:
1. Renomeie/copie o arquivo tirando o `_` (ex.: `reels/pe_torto.mp4`) **ou** mantenha o nome e só
   aponte para ele no JSON.
2. Adicione um item ao **`reels.json`** (no fim da lista):
```json
{
  "id": "reel_pe_torto",
  "video": "reels/pe_torto.mp4",
  "caption": "Pé torto congênito tem tratamento? Entenda o método de Ponseti...\n\nDr. Rafael Vargas · CRM-SP 226103 · RQE 137901\nConteúdo educativo — não substitui avaliação médica."
}
```
- `id` **único** (nunca reusar — o estado usa id p/ não repetir).
- `caption`: 1ª linha keyword-forward (vira alt/SEO). Sempre com bloco CFM (CRM/RQE/disclaimer).
3. Commit. Na próxima janela de Reels (Seg/Qua/Sex/Dom ~15h BRT) o robô publica **o próximo da fila**.

> A fila respeita a **ordem** do JSON. Para furar fila (publicar já), use **§4 FORCE_ID**.

---

## 3. Adicionar Post (carrossel), Story ou Sequência
Mesma lógica: adicionar item ao JSON certo (as artes já existem em `images/` ou são geradas pelos
geradores 🔵 quando a fila baixar). Formatos:
```json
// posts.json  (carrossel de feed 4:5)
{ "id":"post_xxx", "images":["images/c_on_tema_1.jpg","images/c_on_tema_2.jpg"], "caption":"…", "alt":"…" }

// stories.json (story solto)
{ "id":"story_xxx", "image":"images/s_tema.jpg" }

// sequences.json (story serializado — 5 frames publicados em bloco no mesmo dia)
{ "id":"seq_xxx", "theme":"Semana do Joelho — Dia 2", "images":["images/sq_…_1.jpg", "…_5.jpg"] }
```
Regras: `id` único; caminho da mídia tem que **existir no repo** (a auditoria `_auditoria_motor.py`
checa isso — rode antes de commitar se quiser garantir 0 refs quebradas).

**Para reabastecer em lote** (quando a fila baixar): rodar os geradores 🔵 (`gerar_conteudo.py`,
`carrossel.py`, `gerar_temporadas.py`) — eles produzem as artes e as entradas. Ver `01_INVENTARIO §A`.

---

## 4. Publicar AGORA (teste / furar fila)
**Web:** Actions → "Publicar no Instagram" → Run workflow → campo **force_id** = o `id` do item
(ex.: `reel_pe_torto`, `post01`, `seq_xxx`). Em ~1 min aparece no perfil.
**CLI:** `gh workflow run publish.yml -f force_id=reel_pe_torto`
- `force_id=destaques` → sobe as capas de `destaques.json`.
- Sem `force_id` → modo agendado normal.

---

## 5. Renovar o token da Meta (a cada ~60 dias) — ÚNICA manutenção recorrente
O `IG_ACCESS_TOKEN` expira em ~60 dias. Quando expirar, as publicações falham com erro de token.
1. Gere um token novo de longa duração (passo da Parte A do `README.md` raiz, ou trocar o atual):
   `https://graph.instagram.com/access_token?grant_type=ig_exchange_token&client_secret=APP_SECRET&access_token=TOKEN_ATUAL`
2. GitHub → repo → **Settings → Secrets and variables → Actions → `IG_ACCESS_TOKEN` → Update**.
3. **Anotar a data em `05_MANUTENCAO.md §1`** (só a data — nunca o token; o repo é público).

> 📌 A data real da última troca está na coluna **Updated** do secret, no GitHub. O que estiver
> escrito no repositório é estimativa.
> ✅ Lembrete recorrente (55 dias) já ativo no Google Calendar: *"🔑 Renovar IG_ACCESS_TOKEN"*.
> 📌 A memória [[linkedin-automacao-conteudo]] tem o mesmo padrão de token manual ~60d.

---

## 6. Troubleshooting
| Sintoma | Causa provável | Ação |
|---|---|---|
| Publicação falha com erro de token | Token expirou (~60d) | **§5** renovar o secret |
| `Container … status ERROR/EXPIRED` | Mídia inacessível / formato | Conferir que o repo é **público** e o path existe |
| Reel não publica | Item não está no `reels.json` (ficou como `_preview_`) | **§2** |
| "raw url" 404 | Path no JSON ≠ arquivo no repo | Rodar `python _auditoria_motor.py` (lista refs quebradas) |
| Carrossel recusa `alt_text` nos filhos | Limite da API | Remover `alt_text` dos filhos (deixar só no container) |
| Posta 2x | `id` repetido OU estado não commitado | Garantir `id` único; o `publish.yml` commita `state/published.json` |
| Nada publica há dias | Crons atrasando OU fila esgotada | Ver logs do Actions; conferir runway no `01_INVENTARIO §C` |

---

## 7. Higiene recomendada (rotina leve)
- **Mensal:** rodar `python _auditoria_motor.py` (saúde: refs quebradas, runway, órfãos).
- **Quando a fila de um tipo < ~2 semanas:** reabastecer com os geradores 🔵.
- **A cada ~55 dias:** renovar o token (§5).
- **Trimestral:** revisar `images/_removidos_estetica/` e órfãs (limpeza).
