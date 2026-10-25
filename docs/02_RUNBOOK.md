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
| Renovar o token | **Nada.** Automático (`refresh-token.yml`). Emergência: **§5**. |
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

## 5. Renovar o token da Meta — AUTOMÁTICO desde 25/07/2026
> ✅ **Não faça isso à mão.** O workflow `refresh-token.yml` renova o `IG_ACCESS_TOKEN`
> sozinho toda segunda (~06:17 BRT) e regrava o próprio secret. Setup único e detalhes em
> **`05_MANUTENCAO.md §0 e §1`**. Confira a última renovação em `state/token_refresh.json`.
>
> O procedimento manual abaixo virou **emergência**: só serve se o token for invalidado de
> fora (senha trocada, app removido) ou se passar 60 dias sem renovar — aí a Meta o mata e
> nem a automação o recupera.

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
| Posta 2x | `id` repetido OU estado não commitado | Garantir `id` único. O `publish.yml` commita `state/published.json` com **retry** (5 tentativas, `pull --rebase`, backoff 10→50s) desde `09da55e` — se esgotar, o job **fica vermelho**; ver o log do step *"Salvar estado"* |
| Nada publica há dias | Crons atrasando OU fila esgotada | Ver logs do Actions; conferir runway no `01_INVENTARIO §C` |
| Job vermelho com `parte INCERTA`, `publicacao INCERTA`, `já expirou` ou `NAO conhece` | Erro da Meta sem confirmação do contêiner, story incompleta de outro dia ou story de hoje fora do estado | **§12** (conferir no app; editar o estado) |

---

## 7. Higiene recomendada (rotina leve)
- **Mensal:** rodar `python _auditoria_motor.py` (saúde: refs quebradas, runway, órfãos).
- **Quando a fila de um tipo < ~2 semanas:** reabastecer com os geradores 🔵.
- ~~**A cada ~55 dias:** renovar o token.~~ → automático; ver `05_MANUTENCAO.md`.
- **Trimestral:** revisar `images/_removidos_estetica/` e órfãs (limpeza).

## 8. Saída da estagnação (12/09/2026) — alarme de curtidas, collab e trial por peça

**Alarme fail-loud de curtidas (B6-iii).** Antes de publicar, `publish.py` lê as 6 últimas peças
do feed (`/media`, reels + carrosséis) e, se a soma de `like_count` for **zero**, NÃO publica:
grava `state.alarme_curtidas`, imprime `::error::ALARME` e sai vermelho — a fila fica pausada até
decisão humana. Publicar no vazio só treina o algoritmo no não-engajamento (plano §4).
- Para **despausar** (decisão declarada, nunca default):
  `gh variable set ALARME_CURTIDAS --body off --repo rafaelvs/06_Automacao_Instagram`
  (ou `ALARME_N_PECAS` para mudar o N; `FORCE_ID` passa direto pelo alarme).
- Leitura da API falhou? O alarme **não** avalia (`::warning::`) e a publicação segue — medidor
  quebrado não para a fila. Token morto na leitura segue o caminho normal (`AUTENTICACAO FALHOU`).

**Collab / audiência emprestada (B3).** `item["collaborators"] = ["usuario1", "usuario2"]` (≤3,
sem `@`) em posts.json/reels.json vira o parâmetro `collaborators` do container (imagem, carrossel
e reel; story não aceita). O parceiro precisa **aceitar o convite no app** para a peça aparecer no
perfil dele. Username inválido → a Meta recusa o container → o item falha ALTO (job vermelho) e
não trava o token. **Antes de usar em peça real, rode o canário:**
`gh workflow run canario-collab.yml --repo rafaelvs/06_Automacao_Instagram` — ele cria um container
com username inválido e **exige que a API recuse** (refutador que nunca falhou não é refutador);
nunca chama `media_publish`. Restrição CFM (Art. 10 §1º): peça em canal de terceiro **não** leva
CTA de contato — a conversão acontece no perfil, que já carrega CRM/RQE.

**Trial por peça (B5).** `item["trial"] = true` em reels.json publica SÓ aquela peça em modo trial
(entrega exclusiva a não-seguidores; a peça sai do grid), sem religar `TRIAL_REELS` global. Uso:
instrumento de diagnóstico com 4 peças sorteadas (ver `PLANO_EXPERIMENTOS.md`), nunca estratégia.
O ramo tomado fica em `state.published[].modo_reel` (trial / fallback_normal / normal).

**Cadência de stories.** Sequências passaram de diárias para **seg/qua/sex** (`SEQ_WEEKDAYS`),
~15 frames/semana — mediana de mercado 8,39/semana; cada seguidor que pula a sequência diária gera
o sinal negativo de ranking de Stories.

## 9. Reordenar filas × `render.yml` (13/09/2026 — plano "núcleo primeiro")

- As três filas (`reels.json`, `posts.json`, `sequences.json`) estão em ORDEM POR FASE do tratamento, não FIFO
  (consulta de controle → gesso em casa → pisar ou não → fixador rotina → …). Quem inserir peça nova, insere na fase
  certa e regenera `PROGRAMACAO.md` (`python _gen_programacao.py`).
- **NUNCA disparar `render.yml` depois da reordenação.** Ele roda `gerar_temporadas.py`, que TRUNCA e reescreve
  `sequences.json` inteiro — desfaz a ordem por fase. Frame de story é JPG pré-renderizado: para trocar UM frame,
  regenerar só aquele JPG (script `rerender_frame.py`, a criar) sem tocar `sequences.json`.
- `reels_legado_mudos.json`: os 27 reels mudos `reel04`–`reel30` retirados da fila em 13/09 (sem voz, sem aprovação
  por peça). Reversível: copiar de volta para o fim de `reels.json`.
- Stories saem seg/ter/sáb 12:30 (`SEQ_WEEKDAYS = {0, 1, 5}`): dias escolhidos pelos views/dia medidos em 83 dias
  (SÁB 102,0 · SEG 100,7 · TER 91,3 · QUI 69,0 = pior). Reverter é 1 linha em `publish.py` + `publish_agenda.py`.
- Plano completo e correções do crítico: oficina, `_GRANDE_REVISAO_2026-08/EVOLUCAO_NUCLEO_PRIMEIRO_2026-09-13.md`.

## 10. Geração nova: rótulo de IA, cota de lâminas e voz (18–19/10/2026)

Decisão do Rafael em 18/10/2026 ("pode seguir com tudo"), depois de ver os dois pilotos de entretenimento.

- **Rótulo "Conteúdo de IA"** — todo reel com voz sintética sai com `is_ai_generated=true` no contêiner. "Voz
  sintética" = campo `voz_ia` verdadeiro OU a legenda contendo "voz digital (IA)". Desde 19/10 o
  `checar_entretenimento.py` (no CI e ANTES de cada publicação) exige em TODO reel pendente `voz_ia` explícito
  (true/false) e coerente com a linha da legenda — 16 lâminas narradas de julho estavam sem nenhum dos dois.
  Imagem, carrossel e story não levam rótulo: a Meta os isenta. Prova de que a API lê o campo:
  `canario_rotulo_ia.py` / `canario-rotulo-ia.yml` (`true` aceito, valor inválido recusado com "Param
  is_ai_generated must be a boolean"). O estado grava `rotulo_ia` em cada reel. Desligar só por decisão humana:
  `gh variable set ROTULO_IA --body off --repo rafaelvs/06_Automacao_Instagram`.
- **Cota de lâminas** — o reel antigo (lâmina de texto lida em voz alta, item sem `formato`) sai no máximo
  `LAMINAS_POR_SEMANA_PADRAO` vezes por semana (`regra_reels.py`, padrão 1, semana de segunda a domingo, horário de
  Brasília). Formato novo (`"formato": "conversa"` ou `"como_funciona"`) sai sem cota. Em dia de reel sem peça
  permitida, não sai reel — o log diz "cota ... cumprida", não "esgotada". `FORCE_ID` passa por cima da cota
  (decisão humana; o reel forçado SOMA ao agendado do dia). **Mudar a cota = editar `regra_reels.py` e commitar**
  (não é variável de repositório desde 19/10: com variável, a página mostrava uma cota e o robô usava outra).
  `-1` = sem cota, `0` = lâminas suspensas. O `publish_agenda.py` projeta o `PROGRAMACAO.md` chamando a MESMA
  função do robô (`regra_reels.proximo_reel`), e o publish grava `formato` em cada reel publicado.
- **Intervalo de conversa** (19/10/2026) — a série CONVERSA ("Se o seu ___ pudesse responder") só sai
  `DIAS_ENTRE_CONVERSAS_PADRAO` dias depois da última (`regra_reels.py`, padrão 10 — "pode deixar a cada 10 dias"; a 1ª versão, 1 por semana,
  punha uma conversa numa segunda e outra na seguinte). Rafael: "é legal, mas tem que ser
  mais espaçada [...] vez ou outra somente, pq é um modelo mais cansativo". COMO FUNCIONA é o formato
  principal, sem cota. Fila com só conversa e lâmina nas cotas = dia sem reel: produzir COMO FUNCIONA.
- **ALL-IN COMO FUNCIONA** (24/10/2026) — depois dos primeiros números (cf_alongamento 2.049 de alcance em 2,8 dias
  e 16 envios; cf_fratura_cola 1.333 em <1 dia; conversa cv_fixador 56; lâminas mediana 32 em 90 dias), o Rafael
  decidiu "dar all-in". Padrões em `regra_reels.py`: `LAMINAS_POR_SEMANA_PADRAO = 0` e `CONVERSAS_ATIVAS_PADRAO =
  False` — só COMO FUNCIONA sai; lâminas e conversas ficam na fila, sem apagar. Dia sem COMO FUNCIONA = dia sem
  reel: a produção tem de manter ~4 por semana na fila (o log do publish avisa).
  Minutos depois, o all-in passou a valer para TODO o conteúdo ("não é só do Reels [...] como se a gente estivesse
  praticamente começando do zero"): `POSTS_ATIVOS_PADRAO = False` (carrossel estático) e `SEQUENCIAS_ATIVAS_PADRAO =
  False` (sequência de stories antiga). O PROGRAMACAO.md mostra o que está parado. A versão nova de carrossel e de
  stories vem do estudo de 24/10 (workflow revisao-modelo-como-funciona).
- **Voz** — a aprovada passou a Antonio **+8% / +0Hz** (era −8%/−4Hz desde 30/08). `checar_voz.py` re-registrado
  com a evidência; o autoteste dele não depende mais de um valor fixo de ritmo.

## 11. Geração nova: render, fila e portões (auditoria adversarial de 19/10/2026)

- **Peça nova** = um dict em `episodios_entretenimento.py` (+ lote em `aprovacoes.json`). Como funciona também
  declara `gancho` e `tela` (TODO rótulo que a cena desenha). Render só na nuvem:
  `gh workflow run render-animado.yml -f episodio=<id> --repo rafaelvs/06_Automacao_Instagram`.
- O render recusa: episódio mal formado ou com violação CFM (antes do 1º quadro); voz cujas palavras não batem
  com o texto (legenda sairia torta); texto desenhado na tela fora do episódio. Grava num `.parcial.mp4` e só
  promove o vídeo no fim, junto com o irmão `reels/_preview_<id>.json` (hash do episódio, hash dos módulos do
  motor, texto desenhado).
- **Fila:** `python -m animado.anexar <id>` — por padrão no FIM do bloco da geração nova (revisão passiva do Rafael
  precisa de janela); `--depois-de <id>` ou `--frente` (só com motivo). Recusa vídeo cujo irmão não bata com o
  episódio e o motor atuais.
- **Portões no caminho da publicação** (publish.yml, antes de qualquer POST): `checar_aprovacoes.py` e
  `checar_entretenimento.py`. Episódio editado ou motor mexido depois do render = publish VERMELHO até re-renderizar
  (de propósito: vídeo velho não sai com legenda nova). Editou o episódio? Re-registre o hash no lote e re-renderize.

## 12. Stories da geração nova: parte INCERTA (`story_nova_incerta`), story incompleta e conferência da conta (24/10/2026)

Regra que vale para tudo abaixo: **HTTP 500 da Meta pode ENTREGAR** (a peça vai ao ar com resposta de erro) e
**duplicar no ar é pior que faltar uma parte**. Por isso o robô pergunta ao contêiner depois de todo erro de
`media_publish` e, quando não consegue saber, PARA e fica vermelho até alguém conferir.

**Quando aparece** (o `publish.yml` fica vermelho com uma destas mensagens):

| Mensagem no log | O que aconteceu | Faça |
|---|---|---|
| `story(ies) com parte INCERTA [...]` | o `media_publish` de uma parte respondeu erro e o contêiner não confirmou (ou a consulta falhou). A parte **pode** estar no ar. Nenhuma story sai até resolver. | conferir e editar o estado (abaixo) |
| `story X com k/3 parte(s) no ar desde dd/mm ... já expirou` | story incompleta de OUTRO dia: completar publicaria o meio da story sem o começo | decidir: abandonar ou republicar inteira (abaixo) |
| `a conta tem N story(ies) de hoje depois das 12:30 que o estado NAO conhece` | outro run publicou com o estado velho (o caso do P0-3), ou houve story postada à mão. Nada saiu neste run. | registrar a story no estado (abaixo) |
| `nao deu para conferir a conta antes da story (GET .../stories ...)` | a leitura da conta falhou; nada saiu | nada, se for pontual: o próximo run tenta de novo |
| `reel_incerto` / `post_incerto` / `seq_incerto` / `story_incerto` + `publicacao INCERTA` | o mesmo para reel, carrossel, sequência antiga ou destaque. O item NÃO volta à fila sozinho; todo run fica vermelho até resolver | conferir e editar o estado (abaixo) |
| `media_publish do conteiner X respondeu erro e ele esta FINISHED ... Write-ahead mantido` (reel/post) | o `media_publish` deu erro e o contêiner ainda não saiu — mas 500 da Meta entrega DEPOIS. Nada a fazer: o próximo run pergunta de novo a ESTE contêiner (abaixo) | nada (o próximo run resolve) |
| `reel/post ... write-ahead ... a consulta ao conteiner falhou` ou `... esta FINISHED, mas a peca saiu da biblioteca` | não dá para saber se o contêiner preparado saiu, ou a peça foi tirada da fila com o contêiner pendente: nada daquele tipo sai | pontual: nada; peça tirada da fila: esperar o contêiner expirar (24 h) |
| `FORCE ...: o reel X tem conteiner preparado (write-ahead FINISHED ...)` | FORCE de OUTRA peça enquanto o contêiner de X espera: gravar o da nova apagaria o rastro de X | esperar o próximo run agendado publicar X, ou forçar o próprio X |
| `aguardando aprovação ... aprovação visual não amarrada aos vídeos` / `lote 'aprovado' sem aprovado_por+evidencia` | o lote da story tem só o hash do texto, ou não tem autor/evidência: NÃO aprova (story fica de fora, job verde com aviso) | registrar a entrada de `--entrada` num lote válido (abaixo) |

**Como conferir, sem tocar no token** (o repo é público; o token nunca vai para terminal, log ou arquivo):
1. **No app:** perfil → toque na foto (stories ativos, últimas 24 h): conte as partes da story e veja a hora de
   cada uma. Story que já expirou: menu → *Arquivo* → *Arquivo de stories*. Reel/carrossel: o grid do perfil.
2. **Pela API, pelo próprio Actions:** `gh workflow run stories.yml --repo rafaelvs/06_Automacao_Instagram` e, no log
   do passo *Pulso de stories*, o bloco `===STORIES_JSON_BEGIN===` lista cada story ativa com `id` e `quando` (UTC,
   BRT = UTC−3). Compare com as entradas `stn_x#0`, `stn_x#1`, `stn_x#2` do `state/published.json` (campos
   `media_id` e `at`; a entrada incerta traz também `container`, `erro` e `status`).

**O que trocar no `state/published.json`** (commit no repo de produção, a partir de clone fresco — a pasta da
oficina não publica nada):
- **Parte INCERTA que ESTÁ no ar:** trocar `"kind": "story_nova_incerta"` por `"kind": "story_nova"` e preencher
  `"media_id"` com o id visto na conferência (a conferência da conta reconhece a story pelo id). Não mexer em `at`.
- **Parte INCERTA que NÃO está no ar:** apagar a entrada inteira. No MESMO dia, o próximo run publica as partes que
  faltam (retomada). Em outro dia, cai no caso "incompleta de outro dia".
- **Nunca apagar a entrada de uma parte que ESTÁ no ar:** o robô a republica.
- **Story incompleta de outro dia** (`... já expirou`): (a) abandonar — tirar a story do `stories_cf.json` (as partes
  ficam no estado como histórico); ou (b) republicar inteira num próximo dia de story — apagar TODAS as entradas
  `stn_x#*` dela (as partes antigas já expiraram no Instagram). Sem uma das duas, todo dia de story fica vermelho.
- **Story de hoje que o estado não conhece:** (a) se é parte de story do robô (run duplicado com estado velho),
  acrescentar a entrada que falta copiando uma parte irmã: `{"id": "stn_x#i", "kind": "story_nova", "story": "stn_x",
  "parte": i, "media_id": "<id>", "at": "<quando>", "temas": [...]}`; (b) se foi postada à mão, registrar
  `{"id": "avulsa:<id>", "kind": "story_avulsa", "media_id": "<id>", "at": "<quando>"}` — o robô passa a conhecê-la.
  A conferência só olha stories a partir das 12:30 de hoje: story manual de manhã não bloqueia nada.
- **`reel_incerto` / `post_incerto` / `seq_incerto` / `story_incerto`:** saiu → trocar o `kind` para `reel` / `post` /
  `seq` / `story` (com o `media_id`, se souber); não saiu → apagar a entrada (o item volta para a fila no próximo dia
  dele). O `last_*_date` do dia da dúvida já foi marcado de propósito: nada mais daquele tipo sai nesse dia.

**Write-ahead (`state.story_nova_publicando`) — não editar à mão.** Antes de cada `media_publish` de story o robô grava
`{story, parte, container, at, sha256}` e salva. Se o job morrer DENTRO da chamada (timeout, cancelamento, runner
perdido), o próximo run pergunta ao contêiner antes de criar outro: PUBLISHED = registra a parte (`confirmado_por`
"write-ahead"); FINISHED no mesmo dia = publica o MESMO contêiner (contêiner só publica uma vez); EXPIRED = nunca
saiu, descarta; qualquer outro status = parte INCERTA (casos acima). Se a própria consulta falhar, o run fica
vermelho sem publicar nada e o seguinte pergunta de novo.

**Write-ahead de REEL e POST (`state.reel_publicando` / `state.post_publicando`) — não editar à mão** (25/10/2026). A
mesma rede, para o feed: antes do `media_publish` o robô grava `{id, container, at, commit, modo_reel, rotulo_ia,
formato}` e salva. Se o `media_publish` responder erro e o contêiner disser FINISHED, o registro FICA (FINISHED um
instante depois do 500 não prova que não saiu: a Meta entrega depois). O run seguinte pergunta a ESTE contêiner antes de
qualquer decisão: PUBLISHED = a peça saiu (registra sem `media_id`, com `confirmado_por` "write-ahead", e marca o dia);
FINISHED = o bloco do tipo publica o MESMO contêiner, antes da fila (contêiner só publica uma vez: a entrega tardia
nunca vira duplicata); EXPIRED/ERROR = nunca saiu, descarta e a peça segue na fila; outro status = `reel_incerto` /
`post_incerto` (casos acima); consulta falhando = nada daquele tipo sai no run. Antes, o reel nesse caso era recriado
num contêiner novo e saía DUAS vezes no feed (permanente).

**Aprovar uma story** (portão `checar_stories.py`, 25/10/2026): no clone com o render do CI em dia, rode
`python checar_stories.py --entrada stn_x` e cole a entrada (hash do texto + sha256 dos 3 vídeos + hash do gerador do
render que o Rafael VIU) em `episodios` de um lote com `"escopo": ["instagram-stories"]`, `"status": "aprovado"` e
`aprovado_por` + `evidencia` não vazios (a mesma regra do portão clínico `checar_aprovacoes`, que roda antes do publish:
lote sem autor/evidência ali derruba o publish INTEIRO). Entrada só com `hash_roteiro` NÃO aprova: um re-render depois
da aprovação (outro recorte, trecho ou fonte) nunca sai com o aval de um vídeo que ele não viu. Re-render = vídeos novos
= re-aprovar (`divergente`).

**Outras duas redes contra duplicar** (não exigem ação): o `publish.yml` faz checkout de `ref: main`, então o run
enfileirado atrás de um run de story lê o estado que o anterior commitou; e a raw URL das mídias vai com o SHA desse
checkout, então a Meta baixa os bytes que os portões conferiram, não o que estiver no main na hora da busca.
