# Manutenção — registro de datas

Único arquivo que precisa ser atualizado à mão. Serve para responder rápido:
**"quando renovei o token pela última vez?"** e **"quando a fila acaba?"**

> 🔒 **Nunca** anote aqui o valor de nenhum token ou secret. Só datas.
> O repositório é **público**.

---

## 1. Renovações do IG_ACCESS_TOKEN

O token da Meta vive **~60 dias**. Quando expira, o `publish.py` falha e a conta para
**em silêncio** — nada avisa. Procedimento de troca: `02_RUNBOOK.md §5`.

| # | Renovado em | Expira (+60d) | Próxima data-alvo (+55d) | Observação |
|---|---|---|---|---|
| 0 | **2026-06-04** | **2026-08-03** | 2026-07-29 | Emissão original, na montagem do repo. **Confirmado em 25/07/2026** pela coluna Updated do secret — nunca foi trocado até então. |
| 1 | `____/____/______` | `____/____/______` | `____/____/______` | ⬅️ **preencher na próxima troca** |

**Fonte de verdade da data:** GitHub → repo → *Settings → Secrets and variables → Actions*
→ coluna **Updated** do secret `IG_ACCESS_TOKEN`. O que está no repositório é só estimativa
até ser conferido lá.

> ⚠️ **Pegadinha:** o §5 do runbook sugere trocar o token atual via `ig_exchange_token`, mas
> isso exige o **valor do token vigente** — e o GitHub **não devolve** um secret depois de
> salvo (são write-only; a tela só mostra a data). Se o token atual não estiver guardado num
> gerenciador de senhas, o caminho é **refazer a Parte A do `README.md`** (gerar token novo no
> painel da Meta e convertê-lo para longa duração). Não crie um app novo — use o existente,
> senão o `IG_USER_ID` muda.

**Como detectar que expirou:** se `state/published.json` ficar **24h sem commit novo**,
algo travou. Verificação rápida:

```
git log -1 --format=%ci -- state/published.json
```

**Lembrete ativo:** Google Calendar → *"🔑 Renovar IG_ACCESS_TOKEN (robô Instagram)"*,
recorrente a cada 55 dias, com alarme 1 dia antes.

---

## 2. Runway das bibliotecas de conteúdo

Contagem em **25/07/2026** (itens pendentes = total no JSON menos os já publicados
em `state/published.json`), na cadência definida em `publish.py:23-30`:

| Fila | Pendentes | Cadência | Acaba por volta de |
|---|---|---|---|
| **REELS** | 55 | 4/sem (Seg/Qua/Sex/Dom) | **~29/10/2026** ⬅️ primeiro a secar |
| SEQUÊNCIAS | 102 | 7/sem (todos os dias) | ~04/11/2026 |
| CARROSSÉIS | 62 | 4/sem (Ter/Qui/Sáb + Dom) | ~10/11/2026 |

Quando uma biblioteca acaba, o robô **não quebra** — apenas deixa de publicar aquele tipo.
Reabastecimento: `02_RUNBOOK.md §1, §2 e §3`.

**Lembrete ativo:** Google Calendar → *"📹 Reabastecer fila de conteúdo do Instagram"*,
**15/09/2026** (~6 semanas de antecedência sobre os reels).

> `stories.json` tem 88 itens pendentes mas está **inerte**: não existe `STORY_WEEKDAYS`
> na agenda atual — stories soltos foram substituídos pelas sequências em jun/2026.
> Último story publicado: 2026-06-07.

---

## 3. Histórico de mudanças de agenda

| Data | Mudança |
|---|---|
| jun/2026 | Posts e reels migram de **19:00 → 15:00**; stories soltos dão lugar a **sequências diárias 12:30** (auditoria de pico de audiência 12h-15h). |
| **2026-07-25** | `GATILHO_cron-job.md` e os comentários de `publish.yml` atualizados para a agenda real — estavam descrevendo a agenda pré-junho. Nenhum agendamento mudou, só a documentação. |

---

## 4. Rotina leve (de `02_RUNBOOK.md §7`)

- **A cada ~55 dias:** renovar o token (§1 acima).
- **Mensal:** `python _auditoria_motor.py` — refs quebradas, runway, órfãos.
- **Quando uma fila < ~2 semanas:** reabastecer com os geradores.
- **Anual:** o PAT do cron-job.org expira — regenerar e atualizar o header `Authorization`
  nos cronjobs (`GATILHO_cron-job.md`).
