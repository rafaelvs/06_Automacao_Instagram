# Gatilho externo de pontualidade — cron-job.org

Por que: o agendador interno do GitHub é "melhor esforço" e atrasa (buracos de 2h+).
O cron-job.org chama a API do GitHub no horário exato e **força** o workflow a rodar.
O robô (publish.py) continua decidindo o que publicar pela data/hora — o cron-job só dá o "start".

Resultado: as publicações saem no horário-alvo, pontuais, de graça.

## Agenda real (fonte da verdade: `publish.py` linhas 23-30)

| O quê | Dias | Hora (BRT) |
|---|---|---|
| **POSTS** (carrossel de feed) | Ter / Qui / Sáb | 15:00 |
| **CARROSSEL EXTRA** (4º da semana) | Dom | 11:00 |
| **SEQUÊNCIAS** (story serializado, 5 frames em bloco) | **todos os dias** | 12:30 |
| **REELS** | Seg / Qua / Sex / **Dom** | 15:00 |

> ⚠️ Agenda **atualizada em 25/07/2026**. A anterior (posts 19:00, stories 12:30 em Seg/Qua/Sex)
> está obsoleta — os horários migraram para o pico de audiência de 12h-15h (auditoria jun/2026).
> O `publish.py` é quem decide o que publicar; o cron-job só dá o "start" pontual.

---

## Passo 1 — Criar o token do GitHub (PAT fine-grained)

Página: https://github.com/settings/personal-access-tokens/new

- **Token name:** cron-job-instagram
- **Expiration:** 1 ano (ou personalizado)
- **Repository access:** Only select repositories → **06_Automacao_Instagram**
- **Permissions → Repository permissions → Actions:** **Read and write**
  (o "Metadata: Read" entra sozinho — ok)
- Clicar **Generate token** e **copiar** o código (começa com `github_pat_...`).

> ⚠️ Esse token é uma SENHA. Não cola no repositório nem manda no chat.
> Só vai colado dentro do cron-job.org (campo Authorization). Se vazar, é só revogar e gerar outro.

---

## Passo 2 — Conta no cron-job.org

https://cron-job.org → Sign up (grátis). Confirmar e-mail.

---

## Passo 3 — Criar 2 cronjobs

Em "Cronjobs" → "Create cronjob". Os DOIS usam exatamente os mesmos dados de request,
mudando só a agenda.

### Dados comuns (aba Common / Advanced)

- **URL:**
  ```
  https://api.github.com/repos/rafaelvs/06_Automacao_Instagram/actions/workflows/publish.yml/dispatches
  ```
- **Request method:** POST
- **Headers** (adicionar uma a uma):
  | Key | Value |
  |-----|-------|
  | Accept | application/vnd.github+json |
  | Authorization | Bearer COLE_AQUI_O_TOKEN |
  | X-GitHub-Api-Version | 2022-11-28 |
  | Content-Type | application/json |
  | User-Agent | cron-job-rafael |
- **Request body:**
  ```
  {"ref":"main"}
  ```

> O cabeçalho **User-Agent** é obrigatório na API do GitHub — sem ele dá erro 403.

Como POSTS (Ter/Qui/Sáb 15:00) e REELS (Seg/Qua/Sex/Dom 15:00) juntos cobrem **os 7 dias
às 15:00**, dois cronjobs bastam para a janela principal:

### Cronjob 1 — JANELA DAS 15h (posts + reels)
- **Title:** Instagram 15h (posts + reels)
- **Time zone:** America/Sao_Paulo
- **Schedule:** **todos os dias** · hora **15:00**
- Cobre: POSTS Ter/Qui/Sáb **e** REELS Seg/Qua/Sex/Dom.

### Cronjob 2 — JANELA DAS 12h30 (sequências)
- **Title:** Instagram 12h30 (sequências)
- **Time zone:** America/Sao_Paulo
- **Schedule:** **todos os dias** · hora **12:30**
- Cobre: a sequência diária (5 frames em bloco).

### Cronjob 3 — CARROSSEL EXTRA de domingo *(opcional)*
- **Title:** Instagram 11h domingo (carrossel extra)
- **Time zone:** America/Sao_Paulo
- **Schedule:** dia **Dom** · hora **11:00**
- Sem ele, o carrossel de domingo ainda sai — mas depende do catch-all `*/30` do GitHub,
  que é "melhor esforço" e pode atrasar 1-2h. É o único item da agenda sem gatilho pontual.

> Disparar o workflow fora da janela é inofensivo: o `publish.py` confere data/hora e o
> `state/published.json` impede repetição. Disparo a mais nunca duplica publicação.

---

## Passo 4 — Testar

No cronjob, botão **"Run now"** (ou "TEST RUN").
- Resposta esperada da API: **204 No Content** = deu certo (workflow disparado).
- 401/403 = token errado ou faltou User-Agent.
Depois confere em github.com/rafaelvs/06_Automacao_Instagram/actions se nasceu um run novo.

---

## Manutenção
- Token expira em 1 ano → quando expirar, gerar outro e atualizar o header Authorization nos 2 cronjobs.
- Para pausar tudo: desligar os 2 cronjobs no painel.
