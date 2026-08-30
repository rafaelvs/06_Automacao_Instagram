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
| 05/09 | pulso + insights por peça (1º delta da era 3) | [PLANEJADO] |
| 12/09 | pulso + insights por peça | [PLANEJADO] |
| 15/09 | pulso + insights por peça (fechamento da janela) | [PLANEJADO] |

Registrar em cada dump: `followers_count` (série de saldo líquido só tem 2 pontos), `reach_por_follow_type` 30d (série de fadiga c1) e os insights por peça da era 3 (hoje 100% sem delta). Dump que não acontecer na data vira entrada de NÃO-ocorrência.

---

### 30/08/2026 — Estreia do formato reel-caso AGENDADA para pós-janela (não contamina a v2)

- **O que muda:** 3 reels do formato novo "Anatomia de um Caso" (ilustração esquemática + caso da literatura) enfileirados para **23/09, 30/09 e 07/10** — todos APÓS o fechamento da janela (15/09). Render do motor: commit `ef150ab` (opt-in, byte-identidade provada — episódios antigos intocados). Piloto de render aprovado pelo Rafael em 30/08.
- **O que contamina:** a janela, nada. A CAUDA sim: a partir de 23/09 o mix de reels ganha um formato novo — a v2.1 (28/10) deve ler os reel-casos em estrato próprio (formato estreia com hipótese de descoberta 10-40× do benchmark; não misturar com Q&A/narrados no watch time).
- **Como ler:** estrato "reel-caso" na v2.1; métrica de prova da Aposta 6: ≥1 piloto ≥150 views em 14d; gate de morte barata: 3 pilotos <150 → revisar formato antes do lote 2.
