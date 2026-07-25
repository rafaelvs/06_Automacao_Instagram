# Manutenção — registro de datas

Único arquivo que precisa ser atualizado à mão. Serve para responder rápido:
**"quando renovei o token pela última vez?"** e **"quando a fila acaba?"**

> 🔒 **Nunca** anote aqui o valor de nenhum token ou secret. Só datas.
> O repositório é **público**.

---

## 0. Setup único da renovação automática ⚙️

> Faça **uma vez**. Depois disso a seção 1 vira só conferência.

O workflow `refresh-token.yml` renova o token sozinho toda segunda-feira. Para ele poder
reescrever o próprio secret, precisa de um PAT — o `GITHUB_TOKEN` padrão do Actions **não**
tem permissão para gravar secrets.

1. https://github.com/settings/personal-access-tokens/new
   - **Token name:** `refresh-ig-token`
   - **Expiration:** 1 ano
   - **Repository access:** Only select repositories → **06_Automacao_Instagram**
   - **Permissions → Repository permissions → Secrets:** **Read and write**
2. Repo → *Settings → Secrets and variables → Actions → New repository secret*
   - Nome: **`GH_SECRETS_PAT`** · Valor: o PAT gerado.
3. Aba **Actions → "Renovar token do Instagram" → Run workflow**. Verde = funcionando.

> ⚠️ Use um PAT **separado** do que está no cron-job.org. Aquele vive num serviço de
> terceiros; este dá poder de escrever secrets e nunca sai do GitHub.

---

## 1. Renovações do IG_ACCESS_TOKEN

**Automático desde 25/07/2026** — `refresh-token.yml` roda toda segunda ~06:17 BRT e cada
renovação devolve +60 dias. Não há nada a fazer no dia a dia.

**Por que semanal e não a cada 55 dias:** se um run falhar, sobram ~8 tentativas antes de
qualquer prazo apertar. Renovar cedo não custa nada; renovar tarde custa a conta.

**O único jeito de isso quebrar:** o token passar de **60 dias sem renovar** — aí a Meta o
mata de vez e nem a automação o traz de volta (só refaz a Parte A do README). Ou seja: se o
workflow ficar vermelho, você tem semanas de folga para agir, mas **não meses**.

**Como conferir sem abrir o painel:** `state/token_refresh.json` traz `ultima_renovacao`,
`expira_em` e o histórico.

**Se o workflow falhar,** o GitHub manda e-mail para o dono do repo. As duas causas
prováveis, nesta ordem:
1. **`GH_SECRETS_PAT` expirou** (validade de 1 ano) → refazer o passo 0 acima.
2. Token da Meta invalidado (senha trocada, app removido, permissão revogada) → refazer a
   Parte A do `README.md`.

Procedimento manual de emergência: `02_RUNBOOK.md §5`.

### Histórico de origem

| # | Renovado em | Expirava em | Observação |
|---|---|---|---|
| 0 | **2026-06-04** | **2026-08-03** | Emissão original, na montagem do repo. Confirmado em 25/07/2026 pela coluna Updated do secret — nunca foi trocado à mão. |
| 1+ | — | — | A partir daqui é automático: ver `state/token_refresh.json`. |

**Fonte de verdade da data:** `state/token_refresh.json` (ou a coluna **Updated** do secret,
em *Settings → Secrets and variables → Actions*).

> ⚠️ **Pegadinha, se um dia precisar fazer à mão:** o §5 do runbook sugere trocar o token via
> `ig_exchange_token`, mas isso exige o **valor do token vigente** — e o GitHub **não devolve**
> um secret depois de salvo (são write-only; a tela só mostra a data). Sem o token guardado num
> gerenciador de senhas, o caminho é **refazer a Parte A do `README.md`**. Não crie um app novo
> — use o existente, senão o `IG_USER_ID` muda.
>
> É justamente essa armadilha que a automação evita: o workflow **tem** o token vigente (lê do
> secret), então consegue renovar sem passar pelo painel da Meta.

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

- ~~**A cada ~55 dias:** renovar o token.~~ → **automático** desde 25/07/2026 (§1).
- **Mensal:** `python _auditoria_motor.py` — refs quebradas, runway, órfãos.
- **Quando uma fila < ~2 semanas:** reabastecer com os geradores.
- **Anual:** os **dois** PATs expiram — regenerar e atualizar:
  - `GH_SECRETS_PAT` (secret do repo) → §0 acima;
  - o PAT do cron-job.org → header `Authorization` nos cronjobs (`GATILHO_cron-job.md`).

> A manutenção do motor passou de **bimestral** (token, com falha silenciosa) para **anual**
> (PATs, com aviso por e-mail). Não é zero, mas o modo de falha silencioso acabou.
