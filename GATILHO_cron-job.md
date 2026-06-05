# Gatilho externo de pontualidade — cron-job.org

Por que: o agendador interno do GitHub é "melhor esforço" e atrasa (buracos de 2h+).
O cron-job.org chama a API do GitHub no horário exato e **força** o workflow a rodar.
O robô (publish.py) continua decidindo o que publicar pela data/hora — o cron-job só dá o "start".

Resultado: post sai Ter/Qui/Sáb 19:00 e story Seg/Qua/Sex 12:30, pontual, de graça.

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

### Cronjob 1 — POSTS
- **Title:** Instagram POSTS
- **Time zone:** America/Sao_Paulo
- **Schedule:** dias **Ter, Qui, Sáb** · hora **19:00**

### Cronjob 2 — STORIES
- **Title:** Instagram STORIES
- **Time zone:** America/Sao_Paulo
- **Schedule:** dias **Seg, Qua, Sex** · hora **12:30**

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
