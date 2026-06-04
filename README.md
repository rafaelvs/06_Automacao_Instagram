# Publicação automática no Instagram — Dr. Rafael Vargas

Este pacote publica os posts no perfil **@rafaelvargasmd** sozinho, nas datas
definidas, usando a **API oficial da Meta**. Roda na nuvem do **GitHub Actions**
(grátis). Depois de configurado, você não precisa fazer nada — o robô publica.

- `posts.json` — os 12 posts (data/hora, imagens, legenda). **É aqui que você edita.**
- `images/` — as artes (JPEG, 4:5).
- `publish.py` — o robô que publica via API.
- `.github/workflows/publish.yml` — a agenda automática (verifica a cada 15 min).
- `state/published.json` — controle do que já foi publicado (o robô cuida disso).

> ⚠️ O repositório precisa ser **público** (a Meta busca as imagens por uma URL
> pública). Isso é seguro: só ficam públicas as artes — que vão ao Instagram de
> qualquer forma. **O token NUNCA fica no repositório**; ele vai num cofre (Secrets).

---

## Visão geral do que você faz UMA vez (≈20–30 min)

1. **Na Meta** (developers.facebook.com): criar um app, conectar o Instagram e
   gerar um **token de acesso** + pegar o **ID da conta**.
2. **No GitHub**: criar conta, criar um repositório **público**, subir esta pasta
   e guardar o token e o ID nos **Secrets**.
3. **Testar**: disparar o post 1 manualmente para confirmar que publica.

Depois disso, o robô segue o calendário sozinho. Posso te acompanhar ao vivo em
qualquer passo.

---

## Parte A — Meta (token e ID da conta)

1. Acesse **https://developers.facebook.com/** e entre com sua conta do Facebook
   (se não tiver, crie — é exigência da Meta para usar a API).
2. **Meus Apps → Criar app**. Em "Casos de uso", escolha a opção que menciona
   **Instagram / publicar conteúdo no Instagram**. Dê um nome (ex.: "Posts RV").
3. No painel do app, adicione/abra o produto **Instagram → Configuração da API com
   login do Instagram** ("Instagram API setup with Instagram login").
4. Clique em **Gerar token de acesso** e conecte a conta **@rafaelvargasmd**
   (conta profissional). Autorize as permissões pedidas
   (`instagram_business_basic` e `instagram_business_content_publish`).
5. **Copie o token** que aparece. Esse é o seu `IG_ACCESS_TOKEN`.
6. Ainda nessa tela costuma aparecer o **ID da conta do Instagram**
   (`Instagram user ID`). Copie — é o seu `IG_USER_ID`.
   - Se não aparecer, abra no navegador (trocando o token):
     `https://graph.instagram.com/v21.0/me?fields=user_id,username&access_token=SEU_TOKEN`
     e copie o valor de `user_id`.
7. **Token de longa duração (recomendado):** o token inicial pode durar pouco.
   Para um de ~60 dias, abra no navegador:
   `https://graph.instagram.com/access_token?grant_type=ig_exchange_token&client_secret=SEU_APP_SECRET&access_token=SEU_TOKEN`
   (o `App secret` está em Configurações → Básico do app). Use o token retornado.

> Guarde o **token** e o **IG_USER_ID** num lugar seguro por alguns minutos —
> você vai colá-los no GitHub no passo seguinte. Não compartilhe o token.

---

## Parte B — GitHub (subir e configurar)

1. Crie uma conta em **https://github.com/** (se ainda não tiver).
2. **New repository** → nome ex.: `instagram-rv` → marque **Public** → Create.
3. **Suba os arquivos:** na página do repo, **Add file → Upload files** e
   **arraste TODO o conteúdo desta pasta** (`images/`, `posts.json`,
   `publish.py`, `requirements.txt`, `state/`, e a pasta `.github/`). Confirme com
   **Commit changes**.
   - Importante: a pasta `.github/workflows/publish.yml` precisa ir junto
     (ela é a agenda). Ao arrastar a pasta inteira, o GitHub mantém a estrutura.
4. **Guarde o token e o ID nos Secrets:** no repo, vá em
   **Settings → Secrets and variables → Actions → New repository secret** e crie:
   - `IG_ACCESS_TOKEN` → cole o token da Parte A.
   - `IG_USER_ID` → cole o ID da conta.
5. **Ative os Actions:** abra a aba **Actions** do repo e, se pedir, clique em
   **I understand my workflows, enable them**.

---

## Parte C — Testar agora (publica o Post 1 na hora)

1. No repo, aba **Actions → "Publicar no Instagram" → Run workflow**.
2. No campo **force_id**, digite `post01` e confirme **Run workflow**.
3. Em ~1 minuto o post 1 aparece no perfil. Se der erro, abra o run e me mande a
   mensagem — eu ajusto.

Para o modo automático, não precisa fazer nada: a cada 15 minutos o robô confere
o calendário e publica o que chegou a hora (horário de São Paulo).

---

## Como editar datas, legendas ou trocar arte

Abra **`posts.json`** (botão de lápis no GitHub) e edite:
- `datetime`: data/hora no formato `2026-06-09T19:00:00-03:00` (o `-03:00` é o
  horário de Brasília).
- `caption`: a legenda (use `\n` para quebra de linha).
- `images`: a(s) imagem(ns). Para virar carrossel, adicione mais arquivos em
  `images/` e liste vários caminhos.

Confirme com **Commit changes**. Pronto — o robô passa a usar a versão nova.
Posts que **já foram publicados** não se repetem (controle em `state/published.json`).

---

## Manutenção

- **Token expira em ~60 dias.** Como esta campanha dura ~4 semanas, um token de
  longa duração cobre tudo. Para continuar publicando depois, gere um token novo
  (Parte A) e atualize o secret `IG_ACCESS_TOKEN`.
- **Se uma publicação falhar:** quase sempre é (a) token vencido, (b) repositório
  não-público, ou (c) a conta precisa estar ligada a uma Página do Facebook.
  Nesse último caso, conecte @rafaelvargasmd a uma Página (Configurações do
  Instagram → Conta profissional) e conclua a "Autorização de Publicação na Página".

Documentação oficial: https://developers.facebook.com/docs/instagram-platform/content-publishing/
