# REVISÃO DO MOTOR — o que está funcionando (08/11/2026)

Conta: Instagram @rafaelvargasmd. Base: 59 reels de 90 dias (`dataset_reels_90d.json`) e 20 snapshots de insights (`ig/AUDITORIA/evidencias/insights_*.json`, de 24/10 a 08/11). Cada achado passou por um refutador independente. Ficou só o que resistiu, já na versão corrigida.

**Convenções.** FATO = medido nos dados. HIPÓTESE = explicação plausível que ainda não foi testada. "Alcance" = contas únicas alcançadas pela peça. "Skip" = % de quem pula nos primeiros segundos. "Retenção" = tempo médio assistido ÷ duração. "D+3" = 3 dias depois de publicar. "n" = número de peças no grupo. "Mediana" = o valor do meio quando as peças são postas em ordem (não é puxada por um viral, ao contrário da média). "ρ" (correlação de Spearman) vai de −1 a +1: perto de +1, as duas medidas sobem juntas; perto de −1, uma sobe quando a outra desce; perto de 0, não há relação. "p" = chance de a correlação ser acaso (abaixo de 0,05 costuma ser considerado pouco provável). "Shares" = encaminhamentos; "saves" = salvamentos; "CTA" = chamada final ("Manda pra quem...").

**Três correções ao contexto que circulava:**
- A geração animada começou em **21/10** (cf_alongamento), não em 24/10.
- Os formatos novos estrearam **antes de 03/11**: chama_o_var em 27/10 (cf_chamaovar_rotina_fixador) e camera_lenta em 29/10 (cf_cameralenta_ponta_pes). A contagem dos pesos no `regra_reels.py` começa em 01/11.
- O horário real não é "15h fixo": a mediana foi 16:34 BRT, com faixa de 15:13 a 20:50.

---

## 1. Resumo para o Rafael (5 linhas)

1. A mudança grande veio com os vídeos animados, a partir de 21/10. Antes, cada post alcançava umas 35 pessoas. Agora um vídeo comum alcança umas 1.400, e câmera lenta e Chama o VAR passam de 2.500 (mas um Como funciona, o de gesso/placa/haste, também chegou a 2.944; são só 2 vídeos de cada formato novo).
2. Os vídeos que mais rodam são os que quase ninguém pula no começo. Câmera lenta e Chama o VAR perdem só 20 a 24% na abertura; o Como funciona perde de 28 a 56%, conforme a abertura (mediana de 33% nos publicados desde 27/10; 47% contando todos).
3. Esse alcance enorme quase não vira seguidor nem contato. Desde a virada, os cliques no WhatsApp da bio foram quase a zero, e os seguidores continuam entrando no ritmo de antes (cerca de 1 por dia).
4. Um vídeo só (ponta dos pés, 25.903) é quase metade de todo o alcance. Por isso comparamos sempre o vídeo "típico" de cada formato, nunca a soma.
5. Plano até dezembro, sem gravar nada novo: usar a fila que já está pronta até 09/12 para separar o efeito do formato, do dia, da abertura e da chamada final, e medir conversão por vídeo. A decisão do motor de dezembro fica para 01/12.

---

## 2. O que está funcionando

| # | Lição | Números | Tipo | Confiança |
|---|---|---|---|---|
| 2.1 | **A geração animada mudou o patamar de alcance por peça.** | Regime antigo (42 peças, 10/08 a 19/10): mediana 35 (19 a 136); última peça, cv_fixador, 64. cf_alongamento (21/10): 2.049 com 2 a 3 dias, 2.068 no final. Geração nova com ≥ 2 dias: mediana 1.485 (n=15); só como_funciona: 1.361,5 (n=10). Isso dá ~40x a mediana antiga, ou ~20 a 25x as últimas lâminas. | FATO | alta |
| 2.2 | **O salto apareceu só nas peças animadas, não ao lado delas.** | Dois posts FEED de 22/10 e 24/10 ficaram em 21 a 31 de alcance com ~2 dias. Na mesma idade, cf_alongamento tinha 2.049 e cf_fratura_cola 1.333. O acervo antigo ganhou só +6 a +11 desde 24/10 (esc_teste_adams 69→75, caso_silver_russell 51→62, qa_caroco_no_osso 107→117). | FATO (controle parcial: FEED, n=2, não REEL) | média |
| 2.3 | **Hipótese principal: é o formato animado, não um impulso na conta inteira.** | Apoiada em 2.2. Mas nenhum REEL no formato antigo foi publicado depois de 19/10, então formato e data continuam confundidos. | HIPÓTESE | média |
| 2.4 | **Câmera lenta e Chama o VAR formam um segundo nível, acima do como_funciona.** | camera_lenta: 25.903 (ponta_pes) e 5.126 (joelho_estala, só 1,2 dia). chama_o_var: 3.642 e 2.566. Sem o viral, joelho_estala ainda é ~3,8x a mediana do como_funciona com ≥ 2 dias (1.362) e fica acima de todos os como_funciona publicados depois do viral (gesso_placa 2.944, pe_torto 1.485, escoliose 1.102, eixo_perna 1.091, quadril_bebe 248). Mas o "segundo nível" não é limpo: cf_gesso_placa (2.944, como_funciona) supera cf_var_primeiros_socorros (2.566, chama_o_var, ainda com 3,1 dias). É n=2 por formato, e todos saíram em ter/qui/sáb. | FATO (números); a vantagem "do formato" é HIPÓTESE | média |
| 2.5 | **Pouco skip anda junto com alto alcance.** | 15 reels com skip medido: Spearman skip × alcance = −0,75; sem o viral, −0,71; descontando a idade, −0,80. O skip quase não muda com a idade da peça (ρ = 0,07). Os 4 menores skips (19,9 a 24,0; mediana 22,2) são exatamente os 4 de camera_lenta e chama_o_var. Na mesma janela de calendário (de 27/10 em diante), o como_funciona tem mediana 33,1 (n=7). | FATO (associação); causa = HIPÓTESE | média |
| 2.6 | **Retenção alta anda junto com alcance, até dentro de um mesmo formato.** | Geração nova (n=17): ρ = 0,89. Sem o viral: 0,88. Só como_funciona: 0,87 (n=11); com ≥ 3 dias, 0,75 (n=9, p = 0,02). Retenção: chama_o_var 67,0% e 55,1%, camera_lenta 57,6% e 46,7%, mediana do como_funciona 37,1%. A peça de maior retenção é cf_chamaovar_rotina_fixador (3.642), não o viral. | FATO (associação); direção causal = HIPÓTESE | alta para a associação |
| 2.7 | **No como_funciona, abrir com frase leiga parece segurar mais que abrir com rótulo técnico ou aviso.** | "1ª tela" aqui = a primeira tela de texto **depois** da pergunta-título em 2 linhas (todas as peças abrem com uma pergunta). 1ª tela leiga (cf_eixo_perna "LINHA INVISÍVEL", cf_gesso_placa "SE MEXE DEMAIS, NÃO COLA", cf_pe_virado "PRA DENTRO"): skip 30 a 33 (mediana 30,6, n=3). 1ª tela técnica ou com aviso: 5 de 6 ficaram entre 47 e 56. Exceção forte: cf_pe_torto ("PÉ TORTO CONGÊNITO") com 28,5. Confusão de calendário: os 3 leigos saíram entre 28/10 e 04/11; os de skip alto saíram nas pontas (25–26/10 e 06–08/11). | HIPÓTESE (grupos montados depois de ver os números) | média-baixa |
| 2.8 | **O alcance da geração nova se resolve rápido.** | Com ~1 dia, a peça já tem ~90% do alcance atual (n=5). Com 3 dias, mediana de 97% (n=8). Cauda depois do 5º dia: mediana ~+1%; exceções cf_chamaovar_rotina_fixador +4,6% e cf_fratura_cola +6,4 a +9%. Para comparação, o legado tinha 56% no 1º dia (69% contra o horizonte de 7 a 8 dias). | FATO (n pequeno) | alta para a direção |
| 2.9 | **O viral também foi o que mais gerou ação em números absolutos.** | cf_cameralenta_ponta_pes: 27 shares e 18 saves. O máximo de saves de qualquer como_funciona é 5. | FATO | alta |
| 2.10 | **Alguns temas fazem a pessoa encaminhar mais.** | cf_alongamento: 16 shares em 2.068 = 7,7 por mil (as outras 16 peças somadas dão 0,9 por mil). cf_transporte_osseo, de tema parecido, teve 2,0 por mil. | FATO (n=1); a razão é HIPÓTESE | baixa |
| 2.11 | **O melhor como_funciona saiu no dia seguinte ao viral.** | cf_gesso_placa (30/10): 2.944, skip 30,3, retenção 46,2%, 74 curtidas; quase 2x o 2º melhor como_funciona (cf_alongamento, 2.068). Pode ser abertura boa (bate com 2.7) ou "carona" no tráfego do viral de 29/10. n=1, sem como separar. | FATO (número); causa = HIPÓTESE | baixa |
| 2.12 | **A retenção também subiu na virada, não só o alcance.** | Retenção mediana das lâminas/conversas: 20,2% (n=41). Como_funciona: 37,1% (n=11). Retenção é comportamento de quem assiste, o que apoia (sem provar) 2.3; mas o público também mudou (3.3). | FATO; leitura = HIPÓTESE | média |
| 2.13 | **Comentário apareceu onde o tema mexe com uma prática caseira.** | cf_var_primeiros_socorros ("TORCEU O PÉ: CORRE QUE PASSA?") tem 6 dos 17 comentários da geração nova, com 3,1 dias. Nenhuma outra peça passou de 3. | FATO (n=1); a razão é HIPÓTESE | baixa |

---

## 3. O que não está funcionando

| # | Problema | Números | Tipo |
|---|---|---|---|
| 3.1 | **O alcance não vira funil.** Com 99,6% vindo de não seguidores, o alcance subiu ~150x contra a base limpa, mas as visitas ao perfil só dobraram. | Alcance: 46.614 (24/10 a 08/11) contra ~307 por 15 dias antes da virada. Visitas ao perfil: ~107 → 215 por 15 dias; por mil alcançados, de ~350 para 4,6. Cliques no link da bio (WhatsApp): 7 a 14 por mês antes; agora 3, 1, 1, 0 nas janelas de 15 dias sucessivas (contagens pequenas). | FATO |
| 3.2 | **Seguidores no ritmo de antes.** | 0,89 por dia antes (63 em 71 dias); 0,94 por dia depois, tirando um único dia com 8. Esse dia de 8 fechou 13 h **antes** do viral ir ao ar, então não veio dele. No período do viral (dias com fechamento de 30/10 a 08/11): 10 seguidores em 10 dias; só o dia do viral teve 3, e nenhum outro passou de 2. São ~0,5 seguidor por mil alcançados. Na janela de 90 dias, 41 deixaram de seguir. | FATO |
| 3.3 | **O público alcançado ficou jovem e espalhado; a base de seguidores, não.** | Alcançados com menos de 25 anos: 49% (4.448 de 9.054). Entre os seguidores: 1,7%. O salto foi entre 24/10 (12%) e 26/10 (45%), antes do viral e dos formatos novos. A Grande SP é ~8% dos alcançados no Brasil, Alphaville não aparece, e Osasco tem 32. Ressalva grave: essa demografia está congelada desde 31/10 e cobre só ~18% do alcance. | FATO (com ressalva); "jovem demais para o consultório" é HIPÓTESE (18 a 30 anos é faixa típica de alongamento) |
| 3.4 | **Qual dos dois fracassou, e não foi pela retenção.** | cf_qualdosdois_pe_chato: 179 de alcance em 8,2 dias, retenção 36,1% (perto da mediana de 37,1% do como_funciona), skip 38,6%, 0 shares, 0 saves. A causa (formato, tema bebê, sábado, proximidade com o viral) é desconhecida. n=1. | FATO (resultado); causa = HIPÓTESE |
| 3.5 | **Mito na prova ficou no nível de um como_funciona fraco.** | cf_mitonaprova_pinos: 1.019 de alcance, skip 47,3%, retenção 30,6%. n=1. | FATO |
| 3.6 | **Quase não há compartilhamento nem comentário.** | 62 shares em 53.115 de alcance = 1,17 por mil (mediana 0,91). 7 de 17 peças com zero. 17 comentários em 17 peças, mediana 0, e 6 deles numa peça só (2.13); os dois câmera lenta (31.029 de alcance somado) têm 0 comentários. Nenhuma chamada final pede comentário: todas dizem "Manda pra quem...". | FATO |
| 3.7 | **Não dá para avaliar a chamada final (CTA).** | O "Manda pra quem..." está em 100% das peças novas, então não existe grupo de comparação. | FATO |
| 3.8 | **O formato está preso ao dia da semana.** | Ter/qui/sáb só tiveram formatos novos (6 reels); seg/qua/sex/dom só como_funciona (11). Não dá para separar efeito de dia e de formato. | FATO |
| 3.9 | **Alguns como_funciona recentes estão baixos.** | cf_quadril_bebe: 248 com 2,3 dias. cf_fixador_circular: 419 com 0,2 dia, ainda acumulando. Não há queda de patamar mensurável no como_funciona: mediana de 1.500 antes de 27/10 (n=4) contra 1.362 depois, contando só peças com ≥ 5 dias (n=4); incluindo as com ≥ 2 dias, depois de 27/10 a mediana é 1.170 (n=6, de 248 a 2.944). Faixas que se sobrepõem. | FATO; erosão do formato é HIPÓTESE |
| 3.10 | **O agendador não cumpre o horário.** | 6 de 17 peças saíram às 17h ou mais tarde, até 20:50. | FATO |
| 3.11 | **Falta instrumentação.** | Não existe visita ao perfil, follow nem clique por reel. Os snapshots não registram a hora da coleta (a idade de cada leitura tem ±1 dia). Nenhuma peça publicada a partir de 02/11 tem leitura do começo da vida. A demografia está congelada. | FATO |

---

## 4. Lições portáveis para os outros motores

Destinos: YouTube Shorts (que reaproveita esses vídeos), Facebook, Threads, TikTok, Kwai, Pinterest, LinkedIn, Bluesky, X e site.

### 4a. Do formato vídeo vertical (Shorts, TikTok, Kwai, Reels do Facebook)

- **A abertura é o gargalo.** Quanto menos gente pula no início, mais a peça roda (2.5). Meça o skip, ou o equivalente da plataforma ("swiped away" no Shorts), como primeira nota de cada vídeo. HIPÓTESE quanto à causa, mas é o melhor sinal precoce disponível.
- **Retenção é o melhor preditor de alcance disponível (2.6).** Use retenção, não curtidas, como KPI do vídeo.
- **Duração: na faixa de 29 a 36 s, a duração por si só não explica o desempenho.** Fora do Chama o VAR, os vídeos mais longos retiveram menos: sem os VAR e com ≥ 3 dias, ρ = −0,62 (n=12); retenção mediana de 38,6% (< 31 s, n=5) para 30,6% (33 a 36 s, n=3). Indício, não prova. Para reaproveitar, prefira os cortes de ~29 a 31 s.
- **Compare na mesma idade e por mediana, nunca pela soma.** Um viral sozinho foi 47% do alcance de 90 dias.
- **Câmera lenta e Chama o VAR são as peças mais fortes para reaproveitar,** com a maior retenção e o menor skip. Se repetirem o desempenho em outra plataforma, isso é evidência de que o efeito é do formato, não do algoritmo do Instagram (ver teste T5).

### 4b. Do texto e do gancho (vale também para Threads, X, Bluesky, LinkedIn, Pinterest e site)

Todas estas são HIPÓTESES de baixa a média confiança:
- **Primeira linha leiga, não técnica.** Nome técnico ou aviso legal ("caso real da literatura / tratado por outra equipe") sai da abertura e vai para o meio ou para a legenda (2.7).
- **Não responder a pergunta do gancho em seco na primeira frase.** Os 3 casos que fizeram isso ficaram com skip alto (escoliose 47,1, fixador_circular 48,8, osteomielite 49,0). Mas segurar a resposta também não garantiu nada: transporte_osseo teve 51,1.
- **Um sinal visto em casa + uma pergunta de decisão** ("Filho na pontinha: normal até quando?") aparece nas 4 peças de câmera lenta e VAR, mas também no pé chato, que fracassou; e o 4º maior alcance (cf_gesso_placa, "GESSO, PLACA OU HASTE?") não segue esse molde. Sozinho não basta.
- **Destinatário amplo na chamada final** ("Manda pra quem não sabia que isso era possível") pode render mais encaminhamento que destinatário estreito. Base: n=1 (cf_alongamento).

### 4c. Só do Instagram (não transferir sem testar)

- **99% do alcance vem de não seguidores via recomendação.** O mecanismo é do Instagram e pode não existir igual em LinkedIn, Bluesky ou X.
- **O padrão de saturação** (~90% do alcance em 1 dia, ~97% em 3 dias) é do regime atual dos Reels. Outras plataformas e o próprio legado (56% no 1º dia) têm cauda mais longa. Cada motor precisa medir a sua curva.
- **Compartilhamento por DM** como métrica do "Manda pra quem...".
- **Demografia de alcançados** via `reached_audience_demographics`: no Instagram está congelada e cobre ~18%. Não use como verdade em nenhum motor sem verificar o coletor.
- **Alcance alto não é público certo:** o público alcançado no Instagram ficou jovem e nacional (3.3). Os motores de LinkedIn e do site, que buscam paciente e encaminhamento, devem medir conversão (visita, clique, contato), não alcance.

---

## 5. Plano de testes até o motor de dezembro (sem produzir vídeo novo)

Decisão do Rafael: **não fazer vídeos novos agora.** Tudo abaixo usa a fila já pronta até 09/12 e o que já foi publicado.

**Pré-requisito T0 (não é teste, é instrumento). Executa: dono do motor Instagram, junto com quem cuida do coletor de insights. Não precisa de aval.**
- Gravar a **hora** de cada coleta.
- Tirar snapshot por peça em **D+1, D+3 e D+7**.
- Coletar por reel `profile_visits`, `follows`, shares, saves e skip. ⚠️ Verificar antes: a API da Meta documenta `profile_visits` e `follows` para posts de FEED e stories, e pode não entregá-los para REELS. Plano B (sem custo): como sai 1 reel por dia, ler `profile_views`, `website_clicks` e seguidores novos **diários** da conta em D+0 e D+1 e atribuí-los à peça do dia (aproximação; declarar como tal).
- Coletar por dia, na conta, `profile_views` e `website_clicks`.
- Investigar por que a demografia está congelada desde 31/10.
- Registrar no `reels.json`, para cada peça, a **1ª linha da legenda, a capa, a CTA, o horário real e o dia**.

Sem isso, os testes T3 e T4 não têm métrica.

**Janela de medição (pela lente de tempo):**
- Veredito de alcance no **D+3**: captura ~95% do alcance de 2 semanas.
- Leitura de confirmação no **D+7**.
- O skip em D+1 serve só como alerta, com margem de ~±6 pontos. Não é veredito: no pé chato ele subiu de 32,9 para 38,6.
- Diferenças abaixo de ~10–20% entre peças não decidem nada.

**Volume disponível:** de 09/11 a 09/12 são 31 vagas. Na regra atual, 13 em ter/qui/sáb (formatos novos) e 18 em seg/qua/sex/dom (como_funciona). **Fila pronta e ainda não publicada** (`reels.json`): 18 como_funciona, 6 camera_lenta, 4 chama_o_var, 2 mito_na_prova, 1 qual_dos_dois e 7 conversas (cv_*). Os testes T1 a T4 juntos ocupam ~26 das 31 vagas: não dá para somar mais testes neste mês.

| Prioridade | Teste | Hipótese | Variável | Como executar com o que existe | Métrica | Janela | Critério de decisão | Quem executa | Aval do Rafael? |
|---|---|---|---|---|---|---|---|---|---|
| **T1** | Controle de regime | O salto vem do formato animado, não de um impulso na conta inteira (2.3) | Formato antigo × animado, no regime atual | Publicar como REEL **1 peça de conversa que já está pronta e nunca saiu** (há 7 cv_* na fila: cv_pinos, cv_gesso_filho, cv_osso, cv_muleta, cv_pe_chato, cv_dor_crescimento, cv_perna_curta). Hoje não há nenhum reel antigo depois de 19/10. De preferência numa **vaga normal** da grade, no mesmo horário: o "Reel de teste" (trial, só para não seguidores) tem distribuição própria e não se compara direto com um reel comum. Repetir 2 vezes. | Alcance e skip no D+3, contra os como_funciona da mesma semana | D+3 e D+7 | Conversa perto de 35–136 → é o formato (manter all-in animado). Conversa ≥ ~1.000 → é a conta ou o algoritmo, e a vantagem atribuída ao formato precisa ser revista. Entre 136 e 1.000 → inconclusivo; usar a 2ª peça antes de decidir. | Dono do motor Instagram | **Sim**: republica conteúdo antigo e mexe na grade |
| **T2** | Cruzar dia × formato | A força de camera_lenta e chama_o_var é do formato, não de ter/qui/sáb (3.8) | Dia da semana | **Reordenar a fila pronta:** ~3 como_funciona em ter/qui/sáb e ~3 camera_lenta ou chama_o_var em seg/qua/dom. As peças são as mesmas; muda só a regra de dia no `regra_reels.py`. | Alcance D+3, skip, retenção, contra o mesmo formato no seu dia habitual | D+3 de cada uma; avaliar com ≥ 3 pares | Mediana das 3 camera_lenta/VAR fora do seu dia acima da maior como_funciona da mesma semana, e os 3 como_funciona em ter/qui/sáb na faixa habitual (~1.100–1.500) → o peso vem do formato. Se a vantagem some → o dia pesa e entra na regra de dezembro. Com n=3, resultado misto = inconclusivo. | Dono do motor Instagram | **Sim**: muda a regra do rodízio |
| **T3** | Abertura do como_funciona (sem re-render) | Abrir com frase leiga segura mais que rótulo técnico (2.7) | **Capa e 1ª linha da legenda**, que são de graça. Variante opcional: trocar a 1ª tela depois da pergunta-título nas peças prontas que trazem ali rótulo técnico ou aviso (cf_crianca_mancando "CLAUDICAÇÃO", cf_osgood_sever "CALCANHAR" → "DOENÇA DE SEVER", cf_corrigir_e_alongar com o aviso de caso da literatura, cf_retirada_fixador "FIXADOR EXTERNO"). ⚠️ Limite do braço barato: quem não segue (99,6% do alcance) vê o vídeo rodando, não a capa (ela aparece sobretudo na grade do perfil), e a legenda fica cortada embaixo. Esse braço quase não alcança o skip; serve mais para visitas ao perfil. O teste real da abertura é a variante de re-render. | Alternar nos como_funciona da fila: metade com capa e 1ª linha leiga, metade como está. Para a variante da 1ª tela, re-renderizar a peça pronta mudando só o texto da tela (não é episódio novo, mas é vídeo re-renderizado: só com aval). | Skip e retenção (os primeiros sinais), alcance D+3 | D+3; ≥ 4 por braço | Skip mediano do braço leigo ≥ ~10 pontos abaixo → regra de gancho em dezembro. Diferença menor → descartar. | Dono do motor Instagram | Capa e legenda: não. **Re-render da 1ª tela: sim** (mexe na produção) |
| **T4** | CTA e conversão | O "Manda pra quem..." não converte. Uma chamada que leve ao perfil ou WhatsApp, ou que peça para salvar ou comentar, rende mais ação (3.1, 3.6, 3.7) | Texto da CTA na legenda; story apontando para o reel | Alternar a CTA **da legenda** dentro do mesmo formato e do mesmo dia: (a) "Manda pra quem..." atual; (b) "salva para..."; (c) "comenta X"; (d) convite ao perfil ou WhatsApp. Em parte das peças, publicar um **story com link** apontando para o reel no D+0. A CTA falada dentro do vídeo fica como está. | Shares, saves e comentários por mil alcançados; visitas ao perfil, follows e cliques no link (depende de T0) | D+7 (conversão acumula mais devagar) | Variante com ≥ 2x a taxa de ação ou de visitas da atual, somando as ≥ 3 peças de cada braço (não peça a peça: hoje cada peça tem 0 a 3 shares e 0 a 6 comentários, e "2x" de 1 é ruído). Para "comenta X", cuja base é mediana 0, exigir ≥ 3 comentários por peça. Nenhuma diferença → a conversão depende do público, não da CTA. | Dono do motor Instagram | CTA da legenda e story: não. **Mudar a CTA dentro do vídeo: sim** |
| **T5** | Reaproveitar em outra rede | A vantagem de camera_lenta e chama_o_var é do formato, não do algoritmo do Instagram | Plataforma | Republicar **vídeos já publicados**, os 2 câmera lenta, os 2 VAR e 2 a 4 como_funciona, no YouTube Shorts (já reaproveita), TikTok ou Kwai, conforme os motores ativos. | Retenção e swipe-away de cada plataforma, views D+3, ranking relativo entre formatos | D+3 e D+7 | A mesma ordem (camera_lenta e VAR acima do como_funciona) em outra plataforma → efeito do formato, e os pesos de dezembro se sustentam. Ordem diferente → é coisa do Instagram. | Dono de cada motor (Shorts, TikTok, Kwai). Bug em motor alheio: reportar, não consertar. | Não, se o motor já publica reaproveitamento. **Sim** para abrir rede nova |
| **T6** | Horário cumprido | O horário importa (ainda sem sinal: ausência de evidência) | Horário | Primeiro fazer o agendador **cumprir** o horário-alvo; hoje vai de 15:13 a 20:50. Depois alternar 2 horários no como_funciona. | Alcance D+3 | D+3; ≥ 4 por braço | Só muda o horário com diferença > 20% entre as medianas. Caso contrário, mantém e encerra o tema. | Dono do motor Instagram | Não |

**Ressalvas do dono do motor (auditoria-instagram-v1):**
- **T1:** as 7 conversas cv_* têm 4 defeitos de desenho conhecidos (`args_cv.json`, módulo compartilhado). Antes de soltar uma como controle, corrigir e re-renderizar; senão o controle mede o defeito, não o formato.
- **T6:** o atraso de horário provavelmente não é do robô. O GitHub estrangula cron (~6 disparos/dia, memória `gotcha-github-cron-estrangulado-6-por-dia`), e o publish sai no primeiro disparo depois das 15h. Cumprir o horário exige gatilho externo, não ajuste de horário no YAML.
- **T2 e T3 (re-render):** mexem na regra ou no vídeo da produção → só com o aval do Rafael, peça por peça.

Ordem prática:
- T0 já.
- T1 e T2 na primeira semana: são os que separam formato de regime, a maior incerteza de todas.
- T3 e T4 em paralelo, na mesma fila: as variáveis são independentes, mas não variar duas coisas na mesma peça.
- T5 assim que os donos dos motores confirmarem.
- T6 só depois de o agendador estar confiável.

---

## 6. Critérios para gerar o motor de dezembro

**Quando:** ler tudo em **01/12**. Até lá, as peças publicadas até ~28/11 já terão D+3. A decisão vale para a fila a partir de 10/12, depois da fila pronta. Fazer uma leitura parcial em **22/11** só para abortar testes que estejam claramente prejudicando a conta.

**O que decidir:**
1. **Formato ou regime (T1).**
   - Se a lâmina continuar no piso: manter o all-in animado e tratar o como_funciona (~1.300–1.500) como patamar de referência.
   - Se a lâmina subir junto: a vantagem atribuída ao formato precisa ser revista antes de fixar pesos.
2. **Pesos do rodízio.** camera_lenta (2) e chama_o_var (1) só sobem ou se fixam se, com mais peças e fora do seu dia (T2), ficarem acima da faixa do como_funciona do mesmo período, na mesma idade (D+3/D+7). Lembrar que essa faixa já vai até 2.944 (cf_gesso_placa): ficar acima da mediana não basta. qual_dos_dois e mito_na_prova continuam com peso 0. Um caso só (n=1) não condena nem reabilita.
3. **Portão de qualidade por peça (provisório).**
   - Skip ≤ 25% e retenção ≥ 45% = peça "boa".
   - Skip ≥ 45% = revisar o gancho, não abandonar o tema.
   - Esse portão só vira regra se T3 mostrar que mexer na abertura move o skip.
4. **Regra de gancho.** Adotar "1ª tela/1ª linha leiga" e "não responder em seco na 1ª frase" apenas se T3 confirmar.
5. **Métrica-alvo do motor.** Alcance deixa de ser o alvo único. Entram no painel por peça:
   - visitas ao perfil por mil alcançados;
   - follows por mil;
   - shares e saves por mil;
   - cliques no link.

   A CTA de dezembro é a vencedora de T4. Se nenhuma vencer, registrar que a conversão depende do público, não do texto.
6. **Portabilidade.** Se T5 confirmar a ordem dos formatos em outra plataforma, passar os mesmos pesos aos motores de vídeo vertical. Se não confirmar, cada motor fica com sua própria regra.
7. **Produção.** Qualquer mudança no que se renderiza (1ª tela, CTA falada, novos episódios dos formatos) passa por **aval do Rafael** com estes números na mão.

---

## 7. O que NÃO sabemos (limites dos dados)

- **Causa do salto de alcance.** Formato animado, mudança de algoritmo e data começaram juntos em 21/10. Nenhum REEL antigo foi publicado depois disso. O único controle são 2 FEED.
- **n pequeno:** camera_lenta n=2, chama_o_var n=2, qual_dos_dois n=1, mito_na_prova n=1, como_funciona n=11. Nenhuma diferença entre formatos tem força estatística.
- **Outlier.** cf_cameralenta_ponta_pes (25.903) é ~47% do alcance de 90 dias. A segunda câmera lenta (5.126) tinha só 1,2 dia na medição.
- **Idade das peças.** O dataset traz só a foto atual, sem alcance por idade. Peças imaturas: cf_fixador_circular (0,2 dia), cf_cameralenta_joelho_estala (1,2), cf_quadril_bebe (2,3), cf_var_primeiros_socorros (3,1). Os snapshots não têm hora (±1 dia). A cauda além de 16 dias da geração nova nunca foi observada.
- **Skip** só existe a partir de ~25/10. Não há linha de base de antes da mudança, e as lâminas não têm skip.
- **Gancho × formato.** Os 4 menores skips coincidem 100% com camera_lenta e chama_o_var. Não se separa o efeito do texto do efeito do recurso visual ("Volta. Câmera lenta." / "Chama o VAR!").
- **Retenção × alcance.** A correlação é forte, mas a direção é desconhecida: reter pode causar a distribuição, ou ser consequência dela. Retenção e tempo assistido são a mesma medida.
- **Dia, horário e formato** estão confundidos. Sobre o horário há apenas ausência de evidência.
- **Conversão por peça não existe.** Visitas ao perfil (735 em 90 dias), cliques no site (20) e cliques no WhatsApp são só totais da conta. A atribuição de seguidores por dia depende da convenção de `end_time` da Meta (inferida).
- **Público.** Não há demografia por reel nem divisão seguidor/não seguidor por peça. A demografia da conta está congelada desde 31/10 e cobre ~18% do alcance; cidades com menos de 22 alcançados somem da lista. "Público jovem demais para o consultório" e "seguidores são mães" são inferências.
- **CTA.** Ela é a mesma em 100% das peças novas, então seu efeito é desconhecido.
- **Tema (família).** Com ≥ 2 dias, pediatria tem mediana 1.238 (n=7) e reconstrução 1.500 (n=8): sem diferença clara. Mas os 2 câmera lenta são de pediatria, então tema e formato também se confundem ali.
- **Qual dos dois.** A causa do flop é desconhecida: formato, tema bebê, sábado ou proximidade com o viral.
- **Fila futura.** O `reels.json` não traz data de agendamento, então quais peças entram até 09/12 é inferência pela ordem da lista e pelo `regra_reels.py`.
