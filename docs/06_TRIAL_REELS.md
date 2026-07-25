# 06 — Trial Reels: medição, decisão e o que fazer com os 19

**Data da medição:** 25/07/2026 · **Decisão:** desligar por default.

## O que são trial reels

Documentação oficial da Meta, verbatim: *"Trial reels are reels that are only shared to
non-followers."* Graduar é definido como *"convert the trial reel to a reel, sharing it to
followers"*.

Blog oficial (pt-BR): *"Seus seguidores não verão o reel de teste no feed deles nem na aba
Reels"*; *"Ele não será mostrado para outras pessoas no seu perfil"*; e, ao graduar, *"o reel
será exibido na grade do seu perfil"*.

Ou seja: enquanto não gradua, o reel **não vai para seguidores e não entra no grid**.

## A medição

Ligado no commit `8b1bf34` (22/06/2026). Em 25/07/2026:

| fonte | número |
|---|---|
| perfil `@rafaelvargasmd` (meta description do Instagram) | **37 posts**, 1.303 seguidores |
| `state/published.json` — carrosséis | 27 |
| `state/published.json` — reels publicados **antes** de 22/06 | 10 |
| soma | **37** |
| reels publicados **de 22/06 a 24/07** (modo trial) | **19** |

Os 37 posts do perfil são exatamente carrosséis + reels pré-trial. Portanto:

- os 19 reels em modo trial **não estão no grid**;
- **nenhum deles graduou** em até 5 semanas — se algum tivesse graduado, entraria na grade e a
  contagem seria maior que 37.

Mecanismo no código: em `publish.py`, quando `TRIAL_REELS` está ligado o payload leva
`trial_params` e **não leva `share_to_feed: "true"`** — só o fallback (quando a API recusa
`trial_params`) manda `share_to_feed`.

## Por que `SS_PERFORMANCE` não salvou

A referência da API só diz: *"the trial reel will be automatically graduated if the trial reel
performs well"* — sem métrica, limiar ou janela. Fora da API, a Meta declara que decide pelas
**visualizações das primeiras 72h**, com limiar **relativo** (razão views/seguidores), nunca
publicado.

Dois problemas operacionais para um motor automatizado:

1. A Graph API **não expõe** status de graduação nem flag `is_trial`. O robô não tem como saber
   quais reels graduaram — só dá para conferir abrindo o app.
2. `graduation_strategy: MANUAL` **não é acionável pela API** — exige ação humana no app nativo,
   reel a reel. Para um motor 100% automatizado, as saídas reais eram `SS_PERFORMANCE` ou nada.

## Decisão

`TRIAL_REELS` passa a ter **default `false`** em `.github/workflows/publish.yml`.

O recurso continua disponível: para um teste deliberado e pontual (comparar gancho A vs. B),
basta definir a repo variable `TRIAL_REELS=true`. O que muda é que ele deixa de valer para o
fluxo contínuo de 4 reels/semana.

**ATENÇÃO:** mudar o default só resolve se a repo variable `vars.TRIAL_REELS` **não** estiver
definida como `true`. Se estiver, ela vence o default. Conferir em
Settings > Secrets and variables > Actions > Variables e apagar a variável se existir.

## Pendente: o que fazer com os 19

Nenhum graduou, então nenhum está no grid nem chegou aos seguidores. Duas saídas:

- **Graduar manualmente no app** — recupera o item, mas relatos convergentes (fontes
  secundárias) indicam que a graduação herda o timestamp da publicação original, o que limita a
  tração recuperável.
- **Republicar como reel normal** — item novo, timestamp novo, grid preenchido. Custo: o
  `id` já está em `state/published.json`, então exigiria um id novo ou edição do estado.

Decisão ainda não tomada. Os 19 ids estão entre `pnc_quando_procurar` (22/06) e
`on_nao_estetica` (24/07).

## O que foi verificado e está OK

- **CFM art. 4º/6º §1º (identificação em conteúdo temporário):** `gerar_sequencias.py:36` e
  `gerar_temporadas.py:38` já gravam `SIG` ("Dr. Rafael Vargas · Médico · CRM-SP 226103 ·
  RQE 137901") e o disclaimer em todo frame de story. Conforme.

## Fontes

- <https://developers.facebook.com/docs/instagram-platform/content-publishing/>
- <https://developers.facebook.com/docs/instagram-platform/instagram-graph-api/reference/ig-user/media/>
- <https://creators.instagram.com/blog/instagram-trial-reels>
- <https://about.fb.com/news/2024/12/trial-reels-try-content-non-followers-first-see-what-perfoms-best/>
