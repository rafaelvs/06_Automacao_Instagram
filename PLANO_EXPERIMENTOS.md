# PLANO DE EXPERIMENTOS — saída da estagnação (congelado em 12/09/2026)

Regra: sorteio **antes** de escrever ou publicar, com semente registrada; a leitura sai na auditoria
v2.1 (15/10) com os comparadores nomeados aqui. Toda aposta de conteúdo vem pareada com uma aposta de
distribuição (regra permanente de auditoria, PLANO_SAIDA_ESTAGNACAO.md §9).

## E1 · Trial Reels por peça (plano B5 / decisão D2) — **ENCERRADO em 13/09/2026, sem resultado, por mecanismo**

- Diretriz do Rafael (13/09): o destinatário é quem saiu da consulta e passou a seguir; crescimento devagar e por dentro. Trial publica SÓ para não-seguidores e fora do grid (`docs/06_TRIAL_REELS.md`) — é o oposto da diretriz, independentemente do resultado.
- Dado da era trial (24/06–31/07, 19 reels, `relatorio_top_bottom.md`): 0 graduaram; alcance por peça mediana 10, 15 de 23 entre 0 e 9, máximo 105. A alavanca já tinha se mostrado fraca antes de ser desligada.
- Ação: `trial: false` nos 4 (`deformidade_angular`, `primeira_consulta`, `qa_dor_crescimento`, `quanto_alongar`); publicam normalmente, para seguidores, no grid. O mecanismo por peça (`item.trial`) fica no motor, desligado.
- Semente e sorteio ficam registrados para a história; nada mais é medido aqui.

## E2 · Teste controlado de gancho (plano B4) — série "Fixador externo por dentro"

- **Semente:** `random.Random("saida-estagnacao-2026-09-12-gancho")`, shuffle dos 8 temas.
- **BRAÇO A — fragmento nominal com número/risco, resolução já no gancho:** `fx_pino_inflamado` (18/09), `fx_sentar_levantar` (27/09), `fx_roupa` (07/10), `fx_retirada` (19/10).
- **BRAÇO B — pergunta do paciente + kicker de série (gancho atual):** `fx_dormir` (21/09), `fx_kit_casa` (30/09), `fx_viagem` (11/10), `fx_curativo_pinos` (23/10).
- **Mesma série, mesmo template (capa v2), mesma voz, mesma legenda-molde; temas pareados por sorteio.**
- **Mede:** alcance e curtidas medianas por braço; retenção nos 3 primeiros segundos (Skip Rate no app — medição do Rafael, A1). Referência externa: na mesma conta faceless do nicho (@the.bone_architect) o fragmento nominal fez 6.712 curtidas contra 45 e 113 nas peças conceituais seguintes.
- **Se empatar:** o gancho não é a variável; o esforço de redação sai da fila.

## E3 · Capa v2 (plano A3 / decisão D9) — todos os reels a partir de 16/09

- **KPI gratuito:** alt text das 12 capas do grid reconhecidas pela Meta como *bone/xray/hospital*. Baseline 1 de 12 (11/09). Meta 30 dias: ≥ 6 de 12. Shares saindo de 0.
- **Métrica secundária (só no app, medida em 13/09 no emulador — `AUDITORIA/evidencias/celular_2026-09-13_curado/`):** skip rate dos 6 reels de 02–11/09 = 61,1 / 71,4 / 75,0 / 85,7 / 67,7 / 78,3% (mediana 73,2%; ~110 de ~150 espectadores agregados); 51–71% saem nos 3 primeiros segundos nas 4 curvas medíveis. **Teste ESTRATIFICADO:** só os reels "capa v2 pura" (excluir os 4 trial de E1, os 8 braços A/B de E2 e os 3 "Anatomia de um Caso", cuja ilustração substitui o herói, e as peças de alarme R1/R2 do plano núcleo-primeiro, formato próprio) — sobram ~5 em 16/09→14/10 — agregando espectadores (não mediana de taxas de n=14–43): **skip agregado < 60%**. Retenção @3 s é a mesma métrica vista do outro lado (≈ 100 − skip + 5 a 11 pp), não um segundo critério.
- **Ressalva registrada pela refutação de 13/09:** a capa v2 ataca o MAIOR degrau da curva (56–79% da perda antes de 3,5 s), não o único (21–44% entre 3,5 e 10 s, trecho que o template não altera); e dentro da amostra o skip não ordena o desempenho contra o "typical reel" — audiência desalinhada é hipótese concorrente que só a distribuição emprestada (B3) testa.
- **Se em 30 dias o alt text não mudar e shares continuarem 0:** o problema não é o template; a capa v2 fica (custo zero) e o esforço de forma sai da fila. (Cláusula "esforço inteiro para H5/distribuição emprestada" removida em 13/09: contradiz a diretriz núcleo-primeiro — distribuição emprestada segue limitada a 1 collab/mês com "sim" do parceiro, E-rede abaixo.)

## E4 · Legenda normalizada (plano A4) — toda a fila desde 13/09

- **Mede:** views/peça e comentários em 30 dias; menções presentes em 100% das peças novas.
- **Se views/peça não subir:** reverter as menções (não as hashtags — o dado contra elas é forte demais).

## E5 · Carrosséis-verbete (plano A7) — 2/semana a partir de 19/09, intercalados 1:1 com os `c_on_`/`c_pnc_`

- **Mede:** saves (hoje 0). Qualquer valor > 0 já é sinal. Limiar único (unificado em 13/09; antes "≥ 15/mês" e "< 5 em 30 d" conviviam): **continua se ≥ 5 saves em 30 dias (13/10) e ≥ 15 em 90 dias (12/12)**; abaixo disso o formato salvável não funciona nesta conta e o esforço vai para as peças por fase (P1–P6 do plano núcleo-primeiro).

## E6 · Alarme fail-loud de curtidas (plano B6-iii)

- **Gatilho:** 6 últimas peças do feed somam 0 curtidas → o motor não publica e o job fica vermelho (`state.alarme_curtidas`).
- **Métrica de dignidade mínima:** peças com ZERO curtidas 5 de 6 (11/09) → 0 de N.

## E7 · Stories por fase (plano núcleo-primeiro, 13/09) — gate assimétrico em 15/10

- **O que ficou de 13/09:** a fila de sequências saiu de FIFO para **ordem por FASE** do tratamento
  (controle → gesso em casa → pisar ou não → fixador rotina → depois do gesso → muletas → dirigir/trabalho …).
  Volume inalterado: 3 sequências de 5 frames por semana.
- **O que foi REVERTIDO em 19/09 (auditoria v2, achado D3):** a troca dos dias (ter/qui/sáb → seg/ter/sáb).
  A decisão saiu de um eixo **deslocado um dia** — `stories_pulse.py` grava o dia em UTC e o workflow roda
  às 23:00 BRT, então a medição do dia D é da sequência publicada em **D−1**, e o relatório agregou como se
  fosse o dia do tema. Prova independente: dias sem sequência = 13, 16, 17, 18/09; dias com `stories_ativos=0`
  = 14, 17, 18, 19/09, exatamente +1. Reatribuindo pelo D−1 sobre os 32 dias limpos disponíveis na decisão:
  DOM 102,2 · SEX 100,7 · SEG 96,3 · QUI 92,0 · SÁB 90,5 · QUA 80,0 · TER 77,8 — os três dias escolhidos eram
  o 3º, o 7º e o 5º. Além disso, "TER 91,3" não se reproduz em nenhuma janela e a série limpa tem **n = 23 dias**
  (2 a 4 por dia da semana), não os "83 dias" que eu havia escrito aqui: com esse n a diferença entre o melhor e
  o pior dia cabe no ruído. Os dias voltaram a **ter/qui/sáb** pelo critério que não depende dessa medição —
  são os dias do carrossel, e a sequência das 12:30 antecipa o post das 15h.
- **Baseline [DADO]:** 27 dias medidos (03–29/08): 2 replies + 1 share em 2.625 views (0,11%); 81% do alcance
  evapora em 24 h; 01–12/09: mediana 84 contas/dia, 0 replies, 2 shares. **Replies = 0 nos 34 dias seguintes**
  (medido na v2) — o único canal onde o perfil tinha conversa secou.
- **Gate 15/10 (assimétrico):** reach mediano/dia < 60 → testar 5/semana com 3 frames; replies = 0 em 12
  sequências → mexer no 5º frame (pergunta em texto), **nunca subir volume**; replies ≥ 6/30 d → manter e
  investir na "pergunta da semana". **Dia da semana só volta à mesa com n ≥ 8 por dia**, medido pelo dia da
  PUBLICAÇÃO, não pelo dia do pulso.
- **CTA do 5º frame corrigida em 19/09:** 16 sequências pendentes terminavam em "Dúvidas? Manda DM →" —
  o DM do Instagram não tem Davi, nem identificação de IA, nem rede de segurança, nem dono (CFM 2.314 Art. 4º §3º).
  Passaram a "Dúvida? WhatsApp no link da bio →" (`rerender_frame.py`). As 2 que já tinham ido ao ar ficaram
  como estavam: o que foi publicado não se reescreve no repo.
- **Limite conhecido:** frames são JPG pré-renderizados. Editar 1 frame = `rerender_frame.py <id> <n>`, que não
  toca `sequences.json`. `render.yml` NÃO pode rodar depois da reordenação (`gerar_temporadas.py` trunca a fila).

## E8 · Rede (P8) — 1 collab/mês, só com "sim" do parceiro

- `@associacaoptc` primeiro (pé torto, `qa_pe_torto_bebe` já publicado); `@atopicosbrasil` só após revisão explícita do ângulo estatura (CFM 2.336 — tabu do perfil). Canário de collab verde em 13/09 (container com convidado inválido é recusado: HTTP 400, code 110/2207018).
- **Mede:** alcance de não-seguidor da peça em collab vs mediana das 4 anteriores; novos seguidores nos 7 dias seguintes.

## Marcos

**16/09** v2 (baseline sob a régua nova) · **30/09** checagem intermediária (alt text, saves, shares) · **15/10** v2.1 (decide E2/E5/E7; E1 já encerrado) · **15/12** v3 (decide lago, D4).
