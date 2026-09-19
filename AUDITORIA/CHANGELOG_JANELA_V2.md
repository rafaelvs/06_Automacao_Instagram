# CHANGELOG DA JANELA v2 — 16/08 → 15/09/2026

**STATUS: ATIVO desde 30/08/2026** (decisões D1-D16 tomadas pelo Rafael; migra para `AUDITORIA/CHANGELOG_JANELA_V2.md` no repo de produção no commit 2). Artefato de 1ª classe da Aposta 2(e): registro canônico de TUDO que muda o sistema durante a janela de medição da v2.

## Regras deste changelog

1. **Toda mudança que toca perfil, fila, motor, template ou coleta entra aqui NO DIA em que acontece**, com: data, o que mudou (com evidência: commit, arquivo, print), o que contamina, e como a v2 deve ler.
2. **Silêncio não é prova de ausência** (lição da casa: inventário afirmado nasce vencido) — a v2 confere este changelog CONTRA o git log do repo de produção e os state files antes de fechar qualquer leitura.
3. Entradas `[PENDENTE Dx]` dependem de decisão do Rafael ainda não tomada; entradas `[PLANEJADO]` têm data prevista mas ainda não aconteceram. Ambas viram entrada datada definitiva quando o fato ocorrer — ou entrada de NÃO-ocorrência se a data passar em branco (escolha por omissão também contamina e também se registra).
4. A janela v2 é **16/08 → 15/09**. O que acontece depois de 15/09 não contamina a janela, mas contamina a CAUDA (dumps v2.1/v3 sobre peças da janela) — por isso também se registra.

---

## Entradas

### 16/08/2026 — Ações da rodada v1 aplicadas em bloco (início da era 3)

- **O que mudou:**
  - **Card-resumo guardável**: **card one-off criado; geradores NÃO alterados** (correção 30/08, auditoria v1.5/A3 — a redação anterior "gerador alterado" era falsa: zero commits em `carrossel.py`/`posts_batch*.py` desde 10/08; a peça única saiu no commit `0dae7b5`). Nenhum card foi publicado até 30/08; pela fila FIFO, o 1º card (c_on_osso_cresce) só sai em **19/09** (fora da janela) e o card da ação de 16/08 (c_pnc_perna_curta_crianca) em **27/10**. A ação 3 da v1 segue substancialmente NÃO FEITA nos geradores.
  - **Ação 14 da v1 (bomba do prepend)**: `publicar_narrativos.py` corrigido no commit `f23b683` (16/08) — `reels = reels + novos` (APPEND, com comentário citando o achado); o workflow segue dispatch-only. Mudança de código do motor dentro da janela; não altera peça publicada.
  - **`perfil.json`**: camada de perfil (bio, nome, categoria, link, destaques) passou a existir como artefato versionado (ação 7 da v1).
  - **Ação 11b**: gate CFM estendido — `_cfm_guard` chamado também em `publish_sequence`/`publish_story` e auditando a concatenação `scenes[].k+sc+sub+vo`; regra `assinatura` promovida de REVISAR para VIOLAÇÃO no contexto público; "antes e depois" reclassificado VIOLAÇÃO→REVISAR (Art. 14, II, b permite conjunto). Cobertura do gate: ~13% → ~100% das superfícies de texto.
- **O que contamina:** a era 3 (16 peças de feed até 29/08) é "pós-ações", mas o efeito esperado da ação mais vendida (saves via card-resumo) é **estruturalmente impossível de aparecer na janela**: zero cards publicados dentro dela. Qualquer leitura "cards não geraram saves" na v2 seria falsa por construção. O gate estendido pode ter alterado texto de peças da era 3 (superfícies antes sem régua) — mudança de conteúdo, não só de medição.
- **Como a v2 deve ler:** era 3 mede consertos de distribuição/gate, NÃO mede cards. A leitura de saves migra formalmente para a **v2.1 de 28/10** (1º card com 5+ semanas de vida); c_pnc fica para a v3. Registrar na ata para não concluir "cards falharam". A queda de reach dos POSTS maduros da era 3 (41,5→28,0, com reels estáveis e stories subindo) segue **sem causa atribuída** — investigar antes de creditar/culpar as ações de 16/08.

### 30/08/2026 — D1/D2/D3 EXECUTADAS: fila intercalada com narrados aprovados (commit `fe3e8ad`)

- **Decisão:** Rafael, 30/08 ~01h, chat auditoria-instagram-v1: "D1 sim, D2 Alongamento adulto, D3 sim,
  demais conforme recomendado".
- **O que mudou (tudo no commit `fe3e8ad` do repo de produção):**
  - 11 reels narrados da série **Alongamento Ósseo (adultos)** inseridos na fila ANTES de reel04 —
    o slot de qua 02/09 passa de reel mudo para `discrepancia_membro` (narrado, preview já renderizado).
  - **12 episódios Q&A lote 2** (`episodios_qa_lote2.py`) commitados e aprovados; renders disparados em
    30/08; a intercalação on/qa aconteceu no **commit 2 = `5ca3e3e` (30/08 01:37)**: 23 narrados aprovados
    na frente de reel04 + este changelog migrado para `AUDITORIA/` no repo (registro 30/08, v1.5/A3).
  - Legendas dos 23 novos: CTA send/save (sem pedido de comentário) + linha "Narração com voz digital
    (IA)." (CFM 2.454, D6) — mudança de padrão de legenda vale só para as peças novas.
  - Gate de aprovação instalado (`aprovacoes.json` + `checar_aprovacoes.py`, hash por episódio; legado
    pendente de ratificação) e **guarda-freio de voz** (`checar_voz.py` no workflow de render: mudança de
    voz sem piloto aprovado pelo Rafael derruba o render — regra dele, 30/08).
  - D7: `voz-train.yml`/`voz-watch.yml` DESATIVADOS (463 runs no-op) — mudança de CI, não contamina medição.
- **O que contamina:** os ~8 slots de reel de 02–15/09 viram peças novas narradas com legenda em padrão
  novo (CTA send/save + disclosure) — incomparáveis com o baseline da era 3.
- **Como a v2 deve ler:** os 8 slots em **estrato separado** rotulado "D1-intercalação"; watch time deles
  comparado ao dos 9 narrados históricos (Q&A lote 1), nunca aos reels mudos; o efeito da linha de
  disclosure na conversão não é isolável (chegou junto com formato novo) — só observar.

### [SUPERSEDIDA 30/08 pela entrada acima] Fila de reels de 02–15/09: intercalação OU regressão a slots mudos

- **O que muda (nas duas hipóteses):**
  - **Se D1 = SIM (recomendado):** Q&A novos/narrados aprovados intercalados na fila a partir de ~02/09 → quebra DELIBERADA e anotada da janela (peças novas com voz, formato diferente do baseline).
  - **Se D1 = NÃO (ou silêncio):** a partir de 02/09 entram reel04…reel11 = **8 slots de reels MUDOS de 11,8s** dentro da janela — que também contaminam, para pior (regressão a formato pré-trial já medido como fraco, desperdiçando watch time, o único sinal top-3 em melhora).
  - Não existe opção neutra. Até 01/09 saem qa_ponta_dos_pes (30/08, com voz) e pnc_mochila (31/08).
- **O que contamina:** os 8 slots de reel de 02–15/09 ficam, em qualquer hipótese, incomparáveis com o resto da era 3.
- **Como a v2 deve ler:** os 8 slots entram em **estrato separado** (rotulado pela decisão tomada); a decisão e a data entram aqui como entrada definitiva; se 02/09 passar sem decisão, registrar "regressão por omissão" — escolha, não acidente.

### 30/08/2026 — D17 EXECUTADA: ângulo estético/estatura promovido a VIOLAÇÃO no guardrail central (commit `33fdb5b`)

- **Decisão:** Rafael, 30/08, chat da auditoria — enquadramento estético/de estatura do alongamento é VIOLAÇÃO (não REVISAR) no `cfm_guardrails.py`.
- **O que mudou:** regra central do gate CFM endurecida DENTRO da janela (commit `33fdb5b`, 30/08 12:51). Re-varredura do acervo publicado e da fila após a mudança: **0 VIOLAÇÃO — contaminação nula no acervo**; o efeito é **prospectivo** (bloqueia peça futura com o enquadramento vetado).
- **O que contamina:** nenhuma peça publicada mudou de texto; a régua de conformidade da era 3 ficou mais dura no meio da janela — comparações de "taxa de bloqueio/REVISAR" antes×depois de 30/08 não são a mesma régua.
- **Como a v2 deve ler:** conformidade auditada com a régua PÓS-D17 (a vigente); qualquer contagem histórica de flags CFM anota a fronteira de 30/08. (Entrada adicionada em 30/08 pela rodada v1.5 — a mudança tinha ficado FORA do changelog, furando a regra 1; achado A3.)

### 30/08/2026 — Fábrica de verbetes criada (commits `6910fa1`, `d5f9900`, `021b2ab`) — biblioteca, NÃO fila

- **O que mudou:** `gerar_verbetes.py` + workflow `render-verbetes.yml` (commit `6910fa1`, 30/08 12:41) e 2 runs verdes de render da biblioteca (`d5f9900`/`021b2ab`, 30/08 15:43–15:45): 20 carrosséis-verbete 4:5 renderizados em `verbetes/` + `verbetes_biblioteca.json`. **`posts.json` intocado** — nada disso entra na fila publicável; publicação só liga no D-day (17–18/09), com lote de aprovação próprio (VERBETES-2026-09).
- **O que contamina:** a janela, nada (nenhuma peça ao ar, nenhum item de fila). Repo ganhou ~20 renders novos (tamanho/histórico).
- **Como a v2 deve ler:** verbetes não existem para a medição da janela; a v2.1 lê o pacote do D-day. (Entrada adicionada em 30/08 pela rodada v1.5 — os commits tinham ficado FORA do changelog; achado A3.)

### 30/08/2026 — Rodada v1.5 da máquina: M1–M5 implementadas na branch `auditoria/v15-provas` (aguarda merge do dono)

- **O que muda (só código/CI/registro — nenhuma peça, fila publicável ou perfil):** M1 freio de voz + fail-loud nos 3 lotes de render e nos pushes de render-reel-voz/stories, ramo Piper morto removido, fingerprint re-registrado (`bed45a4c…`, citando o piloto de 30/08, sem mudança sonora); M2 `gate-aprovacoes.yml` em CI (escopo id-novo, `--isentar-lote LEGADO-PRE-GATE` declarado) + `checar_aprovacoes.py` exigindo `aprovado_por`+`evidencia` e hash de prova com EOL normalizado; M3 este registro corrigido; M4 ferramenta de telemetria copiada p/ pasta durável da oficina; M5 `timeout-minutes: 15` + `checar_cfm.py` advisory no publish.yml + `ci-testes.yml`.
- **Provas (checks novos vistos FALHAR uma vez, protocolo da casa):** gate-aprovacoes VERMELHO run `33336839874` (id semeado `prova_v15_semeado_sem_aval`) → VERDE runs `33336913006`/`33336927027`; ci-testes VERMELHO run `33336839881` (SystemExit semeado) → VERDE runs `33336913008`/`33336927006`. Sementes removidas; branch fecha byte-idêntica à main em `reels.json`/`test_publicacao.py`.
- **O que contamina:** a janela, nada, enquanto na branch (o cron lê só a main). No MERGE, o step advisory e o timeout passam a valer no publish — mudança de CI, não de conteúdo; registrar a data do merge aqui.
- **Como a v2 deve ler:** máquina auditada na v1.5 (baseline 69,0); a v2 (16/09) segue focada em desempenho do perfil.

### [PLANEJADO pós-15/09] Swap edge-tts → Azure Speech (pt-BR-AntonioNeural via endpoint oficial)

- **O que muda:** `synth()` do motor de voz troca o endpoint não-oficial (edge-tts, 503 intermitentes) pelo Azure oficial (free tier). Mesma voz de catálogo; **equivalência sonora ASSUMIDA com base num A/B de 1 cena** — não provada em escala.
- **O que contamina:** a janela em si, nada (swap é pós-15/09). A CAUDA, sim: peças renderizadas pós-swap entram nos dumps da v2.1/v3 misturadas às da janela; se a equivalência A/B for falha (prosódia, loudness, pausas), comparações de watch time cruzando a fronteira do swap ficam sujas — e a hipótese "voz sustenta watch time" é justamente a aposta central.
- **Como a v2 deve ler:** v2 (16/09) não é afetada. A v2.1 estratifica reels por sintetizador (campo no state/manifesto com a data exata do swap — registrar aqui quando acontecer) e só compara watch time DENTRO do mesmo sintetizador até o A/B ser promovido de "assumido" a "provado". O check de equivalência tem de FALHAR uma vez (semeado) antes de merecer confiança.

### [PLANEJADO 17–18/09] D-day de vitrine (pós-fechamento da janela, véspera da cauda)

- **O que muda (em ~24–48h, tudo de uma vez):** 3 posts fixados (post01, post33, reel02); Reorder Grid; 5–6 destaques-menu por queixa; bio nova com disclosure de IA + wa.me com marcador de origem; SEO ligado no template global; toggle de indexação conferido; CTA textual nos frames de story; canário de arquivamento e, se D9 aprovado e canário passar, arquivo seletivo de ~15 peças da era trial (critério reach+views ≤ 17 no snapshot de 29/08). Inclui a **estreia dos verbetes**: cunhar o lote VERBETES-2026-09 (aprovação registrada) e enfileirar 2/semana a partir da biblioteca renderizada em 30/08 (ver entrada da fábrica de verbetes).
- **O que contamina:** (a) séries de CONTA (profile_views, follows, website_clicks, reach) sofrem degrau simultâneo de N intervenções — nenhum efeito é isolável; (b) o arquivo seletivo pode cegar deltas da v3 se a media_id arquivada sumir da edge /media (por isso o canário ANTES, com direito a reprovar); (c) o marcador wa.me muda a semântica do KPI de clique (de "clique" para "clique atribuível") — série antiga e nova não se emendam sem nota.
- **Como a v2 deve ler:** a v2 fecha TODA leitura com dados até 15/09 — nenhum dump pós-17/09 entra na janela. O D-day abre a **era 4**; a v2.1 (28/10) mede o pacote D-day como intervenção ÚNICA composta (sem decompor), sobre as métricas de funil (pv→follows, pv→wa.me por origem). Resultado do canário (passar OU falhar) vira entrada datada aqui.

---

## Registro de coleta na janela (não é contaminação — é a prova de que a leitura é possível)

| Data prevista | Dump | Estado |
|---|---|---|
| 02/09 | pulso 30d (não previsto) | **RECUPERADO em 11/09** do log do run `33649533537` (dispatch avulso de 02/09 que nunca foi salvo). Proveniência diferente das demais — o arquivo carrega bloco `_procedencia`. Janela `2026-08-03 a 2026-09-02`, 36 peças, followers 1309. |
| 05/09 | pulso + insights por peça (1º delta da era 3) | **NÃO OCORREU** (registrado em 11/09). A tarefa `instagram-dumps-janela-v2` está `enabled` e **nunca teve `lastRunAt`**: o cron de dias esparsos (`0 21 5,12,15 9 *`) não recuperou a ocorrência. Perda definitiva do corte temporal daquele dia; as métricas POR PEÇA são cumulativas e sobrevivem nos dumps seguintes. Cron corrigido em 11/09 para `0 21 12,13,14,15 9 *`. |
| 11/09 (≡ 12/09 UTC) | pulso 30d + 90d (mitigação) | **OCORRIDO** — runs `34660456162` (30d) e `34660462168` (90d), salvos como `insights_2026-09-12_30d.json` / `_90d.json`. ⚠️ o `_90d` está **TRUNCADO** em 100 peças (janela declara 14/06; peça mais antiga 19/06) — a era 1/2 não está no arquivo. |
| 12–15/09 | pulso + insights por peça (4 tentativas consecutivas) | [PLANEJADO] — em 15/09, disparar TAMBÉM `-f days=31`, único recorte que fecha exatamente 16/08→15/09. |

Registrar em cada dump: `followers_count` (série de saldo líquido só tem 2 pontos), `reach_por_follow_type` 30d (série de fadiga c1) e os insights por peça da era 3 (hoje 100% sem delta). Dump que não acontecer na data vira entrada de NÃO-ocorrência.

---

### 30/08/2026 — Estreia do formato reel-caso AGENDADA para pós-janela (não contamina a v2)

- **O que muda:** 3 reels do formato novo "Anatomia de um Caso" (ilustração esquemática + caso da literatura) enfileirados para **23/09, 30/09 e 07/10** — todos APÓS o fechamento da janela (15/09). Render do motor: commit `ef150ab` (opt-in, byte-identidade provada — episódios antigos intocados). Piloto de render aprovado pelo Rafael em 30/08.
- **O que contamina:** a janela, nada. A CAUDA sim: a partir de 23/09 o mix de reels ganha um formato novo — a v2.1 (28/10) deve ler os reel-casos em estrato próprio (formato estreia com hipótese de descoberta 10-40× do benchmark; não misturar com Q&A/narrados no watch time).
- **Como ler:** estrato "reel-caso" na v2.1; métrica de prova da Aposta 6: ≥1 piloto ≥150 views em 14d; gate de morte barata: 3 pilotos <150 → revisar formato antes do lote 2.

---

### 11/09/2026 — MERGE da v1.5 (M1–M5) registrado com atraso

- **O que muda:** as melhorias M1–M5 da rodada v1.5 saíram da branch `auditoria/v15-provas` e entraram na main em **`32fd4d9` (30/08/2026 18:43:56 BRT)**, com a rodada publicada em `c140994` (18:44:24). A entrada de 30/08 deste changelog ainda dizia "aguarda merge do dono" e pedia "registrar a data do merge aqui" — fica registrado agora, 12 dias depois. Desde o merge, o `timeout-minutes: 15` e o step advisory do `checar_cfm.py` valem no `publish.yml` em produção (156 execuções no período).
- **O que contamina:** nada de conteúdo. Registro: durante 12 dias o changelog descreveu como "em branch" um estado que já estava em produção — exatamente a doença que ele existe para impedir.
- **Como a v2 deve ler:** M1–M5 valendo em produção desde 30/08 18:43 BRT.

### 11/09/2026 — 4 PUBLICAÇÕES DUPLICADAS na janela (2 no feed, 2 em stories) + 7 dias de stories contaminados

- **O que muda (fato, não plano):** a máquina publicou em duplicidade dentro da janela limpa, por dois defeitos distintos, e o `state/published.json` registra **um** item por par (zero ids duplicados — o instrumento é cego por construção).
  - **FEED/REELS — entram na edge `/media` e portanto na leitura da v2:**
    `18108017225169506` + `18101453204354733` (reel `qa_pe_torto_bebe`, 19/08 18:15 e 18:17) e
    `18037328645821486` + `18581696311066646` (carrossel `post45`, 20/08 18:19 e 18:21).
    Os dois segundos elementos são **órfãos**: não constam do state. Causa: runs `32286338701` e `32402567094` publicaram, perderam o estado no `git pull --rebase` (5 conflitos idênticos em `state/published.json`) e o run seguinte republicou.
  - **STORIES (efêmeros, 24 h — não entram em `/media`):** `stories_ativos` ≠ 5 em **18/08 (6), 24/08 (12), 30/08 (6), 01/09 (7), 03/09 (7), 07/09 (7), 09/09 (10)** — 20 frames a mais do que o desenho. Cada anomalia casa por `media_id` com um run vermelho do dia anterior.
- **Causas, medidas (auditoria v1.6):** (i) `publish.py:_e_falha_de_auth` classificava erro transitório de container da Meta como falha de AUTENTICAÇÃO — a família `2207xxx` chega no `error_subcode` e o código só a procurava no `code`; o run abortava no frame 3/5, os frames 1–2 ficavam no ar sem registro, e o run seguinte republicava a sequência inteira; (ii) `actions/checkout@v4` sem `ref:` fixa o SHA do momento do evento — em 08/09 o run agendado leu um state anterior ao push do run gêmeo e republicou os 5 frames.
- **O que contamina:** a leitura da v2. **Deduplicar os 2 pares de feed/reel antes de qualquer média, mediana ou contagem de peças** (mesma disciplina já aplicada à duplicata `18109531369972268` de 15/07). Nos stories, **excluir os 7 dias acima** ou normalizar por `stories_ativos` — 09/09 é o dia de maior views da janela e tem o dobro de telas no ar.
- **Nota de semântica:** o campo `dia` de `state/stories_serie.json` é o dia da **MEDIÇÃO** (leitura da edge `/stories` ~07h UTC, 24 h para trás). A publicação correspondente é de **D−1**. Vale para a série inteira.

### 11/09/2026 — 4 runs vermelhos desde a v1.5 gritaram "renove o token" com o token vivo

- **O que muda:** runs `33408793664` (31/08), `33648947670` (02/09), `34042496969` (06/09) e `34245242476` (08/09) terminaram em `::error::AUTENTICACAO FALHOU` + "A fila esta PARADA". O token estava íntegro (renovações automáticas em 31/08 `ae8006d` e 07/09 `bde7df6`; `expira_em 2026-11-06`) e a fila NÃO parou. Dentro da janela inteira (16/08→15/09) são **13 runs vermelhos operacionais**, 6 deles com a mesma má classificação (`gh run list --workflow publish.yml --status failure --limit 100`).
- **Efeito colateral medido:** atraso de horário em peças da janela — sequência de 31/08 às 17:26 BRT (alvo 12:30), reel de 06/09 às 16:39 e de 07/09 às 16:18 (alvo 15:00). A hora de publicação é confundidor não declarado na leitura por peça.
- **Como a v2 deve ler:** 3 de 8 reels da janela saíram 1h18 a 2h26 depois do alvo; não ler diferença de reach como efeito de conteúdo sem estratificar por hora (o dado está em `state/published.json`).

### 11/09/2026 — Mudanças de COLETA feitas dentro da janela (regra 1 do changelog cobre coleta)

- Cron da tarefa `instagram-dumps-janela-v2`: `0 21 5,12,15 9 *` → `0 21 12,13,14,15 9 *` (dias consecutivos).
- `SKILL.md` dos dumps: validações novas (e) `erros` só o crônico conhecido, (f) teste de truncamento, (g) nunca sobrescrever; e `-f days=31` no dia 15/09.
- Tarefa `instagram-auditoria-v2`: one-time 16/09 → cron `0 9 16,17,18 9 *` com guarda de idempotência no passo 0 (o agendador tem modo de falha desconhecido: em 01/09 duas one-time a 30 min de distância tiveram destinos opostos).
- 2 pulsos extras de leitura em 11/09 (runs `34660456162` e `34660462168`) — leitura, não publicação.
- Patch proposto (NÃO commitado nesta sessão) em `AUDITORIA/patches/v16_2026-09-11_classificador-lint-pulso.diff`: classificador de erro da Meta, exit real do `checar_cfm.py`, nomeação de métrica + série diária de seguidores + paginação no `insights_pulse.py`, e `schedule` diário em `ci-testes.yml`/`gate-aprovacoes.yml`. Quando for mergeado, **registrar a data aqui** — e desta vez conferir em 24 h.
## 12–13/09/2026 — Plano de saída da estagnação em execução (contaminação DECLARADA dos 3 últimos dias)

Decisão do Rafael em 12/09 ("vamos fazer tudo, prossiga") sobre `PLANO_SAIDA_ESTAGNACAO.md`. Executado na noite de 12/09 (commits `6b289d0`, `94b02e4` e o de render A3 no repo de produção):

| Quando (UTC) | O quê | Afeta a janela 16/08→15/09? |
|---|---|---|
| 13/09 00:10 | Legendas de TODA a fila normalizadas (`legenda.py`): sem hashtags, 1 CTA, 1 menção (`@asami.brasil` / `@sbortopediapediatrica` / `@associacaoptc`), "Médico" na assinatura, 1ª linha na fala do paciente em 12 ids | SIM — pseudartrose (13/09), post59 (13/09), qa_tempo_fixador (14/09), post60 (15/09) saem com legenda nova |
| 13/09 00:17 | `pseudartrose` re-renderizado: locução "Se inscreve" → "Envia para quem precisa." (template de capa ANTIGO) | SIM — 13/09 |
| 13/09 00:20 | `publish.py`: `collaborators` por item; trial por peça (`item.trial`); alarme fail-loud de curtidas; stories DIÁRIOS → ter/qui/sáb | SIM — 14/09 (dom) sem sequência de stories; alarme pode pausar a fila |
| 13/09 00:2x | Render A3 (capa v2): uma frase + herói visual; kicker/sub/CTA/rodapé a partir de 3,5s; header só na última cena | NÃO — 1º reel com capa v2 = `sequela_fratura`, 16/09 |
| 13/09 00:06 | Dumps 30d/90d feitos à mão (a tarefa agendada das 21h de 12/09 NÃO disparou — nenhuma tarefa agendada rodou em 12/09) | — |
| 13/09 ~06:30 | **Núcleo primeiro** (diretriz do Rafael 13/09): `trial: false` nos 4 reels (E1 encerrado por mecanismo); filas reordenadas POR FASE (reels/posts/sequências; pediatria de massa no fim); 27 reels mudos `reel04`–`reel30` fora da fila (`reels_legado_mudos.json`); CTAs por destinatário em `legenda.py`; stories ter/qui/sáb → **seg/ter/sáb** (dias medidos); `PLANO_EXPERIMENTOS.md` E1 encerrado/E3 sem cláusula H5/E5 unificado/E7 gate de stories/E8 rede; runbook §9. Contaminação da janela v2: a fila que a v2 lê em 16/09 já é a nova ordem — comparar por PEÇA, não por posição. Plano: oficina `EVOLUCAO_NUCLEO_PRIMEIRO_2026-09-13.md`. |
| 19/09 | **Auditoria v2 rodada (GLOBAL 50,85; D4 = 22 REPROVOU o portão vinculante de 35).** A tarefa agendada de 16–18/09 **nunca disparou** — três sessões de rotina congeladas desde 18/09 00:45 seguram os 3 slots globais do agendador do Claude, terceira perda de medição desta frente (05/09, 12/09, 16–18/09). Por isso a janela MEDIDA é 20/08–19/09, não a planejada 16/08–15/09: saem 4 dias limpos, entram 4 contaminados; métrica por PEÇA é cumulativa e não sofre, métrica de CONTA sofre. Correções aplicadas no mesmo dia, todas em peça NÃO publicada: (a) a CTA de 16 sequências pendentes saiu do DM do Instagram para o WhatsApp — o DM não tem Davi, identificação de IA nem rede de segurança (CFM 2.314 Art. 4º §3º); (b) endereço errado corrigido em `s_inst_como_e_a_consulta` (frame dizia só Av. Paulista; o consultório principal é Av. Angélica 2491); (c) `cfm_guardrails` passou a exigir a palavra "Médico" na assinatura (3 reels foram ao ar sem ela); (d) `checar_cfm.py` audita toda superfície de texto — cobertura 10,2% → 80,3% —, separa dívida histórica de violação viva e reprova universo vazio; (e) `sincronizar_texto_sequencias.py` grava o texto dos 5 frames dentro de `sequences.json` (29 itens; os outros 24 pendentes não têm módulo-fonte no repo e ficam registrados como ponto cego); (f) step CFM do `publish.yml` promovido de ADVISORY a **BLOQUEIO** (a janela fechou em 15/09 — a promoção estava prevista e registrada como decisão pós-janela); (g) `dur` dos 131 reels trocado pela duração real medida no MP4 (54 de 57 erravam >10%; 47 sem valor) com `checar_dur.py` em CI; (h) `insights.yml` ganhou cron próprio no GitHub e passa a commitar a evidência — a coleta sai do agendador que já a perdeu 3 vezes; (i) **stories voltaram a ter/qui/sáb**: a troca para seg/ter/sáb de 13/09 saiu de um eixo deslocado um dia (o pulso das 23h BRT mede a sequência do dia anterior) e de um n de 23 dias. Nenhuma peça já publicada foi alterada. |

Leitura para a v2: a era 3 limpa termina em **12/09**; 13–15/09 é estrato separado. A tarefa agendada `instagram-auditoria-v2` recebeu o Adendo 4 com a régua nova (Socialinsider 6,65–9,78%, alvo 8%), os denominadores novos e as metas recalibradas.
