# PLANO DE EXPERIMENTOS — saída da estagnação (congelado em 12/09/2026)

Regra: sorteio **antes** de escrever ou publicar, com semente registrada; a leitura sai na auditoria
v2.1 (15/10) com os comparadores nomeados aqui. Toda aposta de conteúdo vem pareada com uma aposta de
distribuição (regra permanente de auditoria, PLANO_SAIDA_ESTAGNACAO.md §9).

## E1 · Trial Reels por peça (plano B5 / decisão D2) — instrumento, não estratégia

- **Semente:** `random.Random("saida-estagnacao-2026-09-12-trial")`, shuffle dos 8 reels narrados de 18/09→05/10 (casos excluídos: estreia do formato).
- **TRIAL (item.trial=true; sai só para não-seguidores e fora do grid):** `deformidade_angular`, `primeira_consulta`, `qa_dor_crescimento`, `quanto_alongar`.
- **NORMAL (comparadores):** `fim_tratamento`, `qa_banho_fixador`, `qa_caroco_no_osso`, `qa_crianca_mancando`.
- **Mede:** alcance, alcance de não-seguidor, retenção (watch time ponderado) e SPR das 4 trial × 4 normal, por TAXA. Ramo tomado fica em `state.published[].modo_reel`.
- **Contraditório honesto:** na era trial (24/06–31/07) o alcance por peça foi 0–9. Se repetir, Trial está morto como alavanca e a decisão fica registrada para não voltar à mesa.

## E2 · Teste controlado de gancho (plano B4) — série "Fixador externo por dentro"

- **Semente:** `random.Random("saida-estagnacao-2026-09-12-gancho")`, shuffle dos 8 temas.
- **BRAÇO A — fragmento nominal com número/risco, resolução já no gancho:** `fx_pino_inflamado` (18/09), `fx_sentar_levantar` (27/09), `fx_roupa` (07/10), `fx_retirada` (19/10).
- **BRAÇO B — pergunta do paciente + kicker de série (gancho atual):** `fx_dormir` (21/09), `fx_kit_casa` (30/09), `fx_viagem` (11/10), `fx_curativo_pinos` (23/10).
- **Mesma série, mesmo template (capa v2), mesma voz, mesma legenda-molde; temas pareados por sorteio.**
- **Mede:** alcance e curtidas medianas por braço; retenção nos 3 primeiros segundos (Skip Rate no app — medição do Rafael, A1). Referência externa: na mesma conta faceless do nicho (@the.bone_architect) o fragmento nominal fez 6.712 curtidas contra 45 e 113 nas peças conceituais seguintes.
- **Se empatar:** o gancho não é a variável; o esforço de redação sai da fila.

## E3 · Capa v2 (plano A3 / decisão D9) — todos os reels a partir de 16/09

- **KPI gratuito:** alt text das 12 capas do grid reconhecidas pela Meta como *bone/xray/hospital*. Baseline 1 de 12 (11/09). Meta 30 dias: ≥ 6 de 12. Shares saindo de 0.
- **Métrica secundária (só no app, medida em 13/09 no emulador — `AUDITORIA/evidencias/celular_2026-09-13_curado/`):** skip rate dos 6 reels de 02–11/09 = 61,1 / 71,4 / 75,0 / 85,7 / 67,7 / 78,3% (mediana 73,2%; ~110 de ~150 espectadores agregados); 51–71% saem nos 3 primeiros segundos nas 4 curvas medíveis. **Teste ESTRATIFICADO:** só os reels "capa v2 pura" (excluir os 4 trial de E1, os 8 braços A/B de E2 e os 3 "Anatomia de um Caso", cuja ilustração substitui o herói) — sobram ~5 em 16/09→14/10 — agregando espectadores (não mediana de taxas de n=14–43): **skip agregado < 60%**. Retenção @3 s é a mesma métrica vista do outro lado (≈ 100 − skip + 5 a 11 pp), não um segundo critério.
- **Ressalva registrada pela refutação de 13/09:** a capa v2 ataca o MAIOR degrau da curva (56–79% da perda antes de 3,5 s), não o único (21–44% entre 3,5 e 10 s, trecho que o template não altera); e dentro da amostra o skip não ordena o desempenho contra o "typical reel" — audiência desalinhada é hipótese concorrente que só a distribuição emprestada (B3) testa.
- **Se em 30 dias o alt text não mudar e shares continuarem 0:** o problema não é o template; o esforço vai inteiro para H5 (distribuição emprestada).

## E4 · Legenda normalizada (plano A4) — toda a fila desde 13/09

- **Mede:** views/peça e comentários em 30 dias; menções presentes em 100% das peças novas.
- **Se views/peça não subir:** reverter as menções (não as hashtags — o dado contra elas é forte demais).

## E5 · Carrosséis-verbete (plano A7) — 2/semana a partir de 19/09, intercalados 1:1 com os `c_on_`/`c_pnc_`

- **Mede:** saves (hoje 0). Qualquer valor > 0 já é sinal; meta 30 dias ≥ 15 saves/mês.
- **Se 20 verbetes renderem < 5 saves em 30 dias:** o formato salvável não funciona nesta conta; esforço vai para reels de caso.

## E6 · Alarme fail-loud de curtidas (plano B6-iii)

- **Gatilho:** 6 últimas peças do feed somam 0 curtidas → o motor não publica e o job fica vermelho (`state.alarme_curtidas`).
- **Métrica de dignidade mínima:** peças com ZERO curtidas 5 de 6 (11/09) → 0 de N.

## Marcos

**16/09** v2 (baseline sob a régua nova) · **30/09** checagem intermediária (alt text, saves, shares) · **15/10** v2.1 (decide E1/E2/E5) · **15/12** v3 (decide lago, D4).
