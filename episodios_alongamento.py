# -*- coding: utf-8 -*-
"""
SÉRIE "ALONGAMENTO ÓSSEO" — lote 1 (31/07/2026).

Nasce já no FORMATO CURTO (<=5 cenas, ~40-45s), o padrão definido pela auditoria v2 do canal:
watch médio de 6,6s contra gancho falado de 11,9s na série antiga. Taxa real do motor = **2,2
palavras/s** (a de 2,6 erra ~15%; medida contra os renders de 31/07).

Cobertura: temas com ZERO sobreposição com a série "Recuperação". Conferido antes de escrever —
`distracao_alongamento` já cobre o princípio do alongamento (cena "SABIA QUE...") e a dor durante a
distração (cenas "Dor esperada"/"Fique de olho"), por isso esses dois temas ficaram de fora.

GUARDRAILS DESTA SÉRIE (inegociáveis):
- Alongamento **sempre funcional** (discrepância, deformidade, sequela). NUNCA estético ou de altura.
- Termo correto: **discrepância de membro / anisomelia**. NUNCA "dismetria".
- Sem promessa de resultado, sem "cura", sem "garante".
- **Encaminhamento proporcional:** esta série é de INDICAÇÃO, não de pós-operatório. Onde não há
  urgência real, a cena 4 é "procure avaliação" — forçar "pronto-socorro" seria alarme falso.
  Onde o paciente já está em tratamento (A3), o pronto-socorro está mantido.
  Desvio da regra da série "Recuperação" aprovado pelo Rafael em 31/07/2026.

ADULTOS (A1/A2/A3): roteiros aprovados pelo Rafael (RQE 137901) em 31/07/2026.
INFANTIS (_kids): derivados do mesmo conteúdo clínico, no padrão irmã do canal —
**AGUARDANDO aval do Rafael**; ver APROVACAO_SERIE_ALONGAMENTO_L1.md.
"""

ALONGAMENTO = [

 # ─────────────────────────── A1 · discrepância de membro ───────────────────────────
 {"id":"discrepancia_membro","ep":201,"temporada":"alongamento","serie":"Alongamento Ósseo",
  "motif_family":"bone","palette":"verde_clinico","layout":"auto",
  "scenes":[
   {"k":"UMA PERNA MAIS CURTA?","sc":["Nem sempre","é cirurgia."],"e":None,
    "sub":"Discrepância de membro: quando tratar e quando só acompanhar.",
    # NAO citar "estetica" aqui: alem de disparar o guardrail CFM, "nem sempre e SO estetica"
    # implica que as vezes e — o oposto do posicionamento funcional da serie.
    "vo":"Uma perna mais curta que a outra nem sempre precisa de cirurgia. O que decide é o quanto ela afeta a sua função."},
   {"k":"Diferenças pequenas","sc":["Comuns.","E sem sintoma."],"e":None,
    "sub":"Muita gente vive sem queixa nenhuma — acompanhar costuma bastar.",
    "vo":"Diferenças pequenas são comuns e muita gente não tem sintoma. A conduta costuma ser acompanhar, às vezes com palmilha."},
   {"k":"O que pesa","sc":["Tamanho, causa","e a marcha."],"e":"marcha",
    "sub":"Em criança, o crescimento que ainda vem entra na conta.",
    "vo":"O que muda a conduta: o tamanho da diferença, a causa e o quanto afeta a marcha. Em criança, pesa o crescimento que ainda vem."},
   {"k":"Quando procurar","sc":["Mancar novo?","Avalie."],"e":None,
    "sub":"Dor no quadril ou na coluna, ou diferença que aumenta rápido.",
    "vo":"Mancar que apareceu ou piorou, dor no quadril ou na coluna, ou diferença que aumenta rápido na criança: procure avaliação."},
   {"k":"Tem tratamento","sc":["E é","funcional."],"e":None,
    "sub":"Dr. Rafael Vargas · CRM-SP 226103 · RQE 137901.",
    "vo":"O tratamento existe e é funcional. Se inscreve para os próximos."},
  ],
  "caption":"Uma perna mais curta que a outra nem sempre precisa de cirurgia — o que decide é o quanto ela afeta a função. Diferenças pequenas são comuns e a conduta costuma ser acompanhar. O que pesa: tamanho, causa e impacto na marcha — em criança, o crescimento que ainda vem. Mancar novo ou dor no quadril: procure avaliação.\n\nDr. Rafael Vargas · CRM-SP 226103 · RQE 137901 — Reconstrução e Alongamento Ósseo · Ortopedia Pediátrica.\nConteúdo educativo, não substitui a avaliação do seu médico."},

 {"id":"discrepancia_membro_kids","ep":202,"temporada":"alongamento","serie":"Alongamento Ósseo",
  "motif_family":"bone","palette":"verde_clinico","layout":"auto",
  "scenes":[
   {"k":"PERNA MAIS CURTA?","sc":["No seu filho,","nem sempre opera."],"e":None,
    "sub":"Guia para os pais: quando tratar e quando acompanhar.",
    "vo":"Uma perna do seu filho mais curta que a outra? Nem sempre é caso de cirurgia."},
   {"k":"É comum","sc":["Diferenças pequenas","são frequentes."],"e":None,
    "sub":"Na infância, muitas não dão sintoma nenhum.",
    "vo":"Diferenças pequenas são comuns na infância e muitas vezes não dão sintoma nenhum. Nesses casos, o tratamento é acompanhar de perto."},
   {"k":"O crescimento manda","sc":["A conta muda","com o tempo."],"e":"tempo",
    "sub":"Pode aumentar ou se acomodar — por isso o acompanhamento É o tratamento.",
    "vo":"Na criança o crescimento muda a conta: a diferença pode aumentar ou se acomodar com o tempo. Por isso as consultas de acompanhamento são o tratamento."},
   {"k":"Quando levar","sc":["Começou a mancar?","Avalie."],"e":None,
    "sub":"Dor no quadril ou nas costas, ou diferença que aumentou rápido.",
    "vo":"Se ele começou a mancar, reclama de dor no quadril ou nas costas, ou a diferença aumentou rápido: leve para avaliação."},
   {"k":"Acompanhar é agir","sc":["Na hora certa.","Sempre."],"e":None,
    "sub":"Dr. Rafael Vargas · CRM-SP 226103 · RQE 137901.",
    "vo":"Acompanhar de perto é o que permite agir na hora certa. Se inscreve."},
  ],
  "caption":"Uma perna do seu filho mais curta que a outra nem sempre é caso de cirurgia. Diferenças pequenas são comuns na infância. Na criança o crescimento muda a conta — por isso o acompanhamento é o tratamento. Mancar novo, dor no quadril ou diferença que aumentou rápido: leve para avaliação.\n\nDr. Rafael Vargas · CRM-SP 226103 · RQE 137901 — Reconstrução e Alongamento Ósseo · Ortopedia Pediátrica.\nConteúdo educativo, não substitui a avaliação do seu médico."},

 # ─────────────────────────── A2 · fixador x haste ───────────────────────────
 {"id":"fixador_ou_haste","ep":203,"temporada":"alongamento","serie":"Alongamento Ósseo",
  "motif_family":"bone","palette":"carvao_quente","layout":"auto",
  "scenes":[
   {"k":"POR FORA OU POR DENTRO?","sc":["A escolha não","é preferência."],"e":None,
    "sub":"Fixador externo ou haste interna: o que decide de verdade.",
    "vo":"Fixador por fora ou haste por dentro? A escolha não é preferência."},
   {"k":"Fixador externo","sc":["Corrige ângulo","e ajusta."],"e":"ajusta",
    "sub":"Em troca: fica visível e exige cuidado diário com os pinos.",
    "vo":"O fixador externo corrige o ângulo do osso junto com o alongamento e dá para ajustar durante o tratamento. Em troca, fica visível e exige cuidado diário com os pinos."},
   {"k":"Haste interna","sc":["Nada para fora.","Mais confortável."],"e":None,
    "sub":"Mas depende do osso comportar o implante.",
    "vo":"A haste interna não deixa nada para fora e costuma ser mais confortável. Mas depende do osso comportar o implante e não resolve toda deformidade."},
   {"k":"O que decide","sc":["É o caso.","Não a moda."],"e":None,
    "sub":"Deformidade, idade, qualidade do osso e infecção prévia.",
    "vo":"Quem decide é o caso: tipo de deformidade, idade, qualidade do osso e infecção prévia. Os dois são bons quando bem indicados."},
   {"k":"Leve à consulta","sc":["Essa pergunta","é sua."],"e":None,
    "sub":"Dr. Rafael Vargas · CRM-SP 226103 · RQE 137901.",
    "vo":"Leve essa pergunta para a consulta. Se inscreve."},
  ],
  "caption":"Fixador por fora ou haste por dentro? A escolha não é preferência. O fixador corrige o ângulo junto e permite ajuste, mas exige cuidado diário com os pinos. A haste não deixa nada para fora, mas depende do osso e não resolve toda deformidade. Quem decide é o caso.\n\nDr. Rafael Vargas · CRM-SP 226103 · RQE 137901 — Reconstrução e Alongamento Ósseo · Ortopedia Pediátrica.\nConteúdo educativo, não substitui a avaliação do seu médico."},

 {"id":"fixador_ou_haste_kids","ep":204,"temporada":"alongamento","serie":"Alongamento Ósseo",
  "motif_family":"bone","palette":"carvao_quente","layout":"auto",
  "scenes":[
   {"k":"POR FORA OU POR DENTRO?","sc":["Depende do osso","do seu filho."],"e":None,
    "sub":"Guia para os pais: o que entra na escolha em uma criança.",
    "vo":"Fixador por fora ou haste por dentro no seu filho? A escolha depende do osso dele."},
   {"k":"Fixador externo","sc":["Vira rotina","da família."],"e":"rotina",
    "sub":"Corrige o ângulo junto e permite ajuste — com cuidado diário nos pinos.",
    "vo":"O fixador externo corrige o ângulo junto com o alongamento e permite ajuste. Em troca, exige o cuidado diário com os pinos, que vira rotina da família."},
   {"k":"Na criança","sc":["As placas de","crescimento."],"e":None,
    "sub":"Elas não podem ser danificadas — e isso limita algumas opções.",
    "vo":"Na criança pesa um fator a mais: as placas de crescimento, que não podem ser danificadas. Isso limita algumas opções por dentro do osso."},
   {"k":"Leve a rotina","sc":["Escola, esporte,","quem cuida."],"e":None,
    "sub":"Isso entra na escolha tanto quanto o exame de imagem.",
    "vo":"Leve à consulta a rotina real do seu filho: escola, esporte, quem cuida dele. Isso entra na escolha tanto quanto o exame."},
   {"k":"Bem indicados","sc":["Os dois","funcionam."],"e":None,
    "sub":"Dr. Rafael Vargas · CRM-SP 226103 · RQE 137901.",
    "vo":"Os dois funcionam quando bem indicados. Se inscreve."},
  ],
  "caption":"Fixador por fora ou haste por dentro no seu filho? Depende do osso dele. O fixador permite ajuste, mas o cuidado com os pinos vira rotina da família. Na criança pesa um fator a mais: as placas de crescimento. Leve a rotina real do seu filho para a consulta.\n\nDr. Rafael Vargas · CRM-SP 226103 · RQE 137901 — Reconstrução e Alongamento Ósseo · Ortopedia Pediátrica.\nConteúdo educativo, não substitui a avaliação do seu médico."},

 # ─────────────────────────── A3 · tempo de tratamento ───────────────────────────
 {"id":"tempo_tratamento","ep":205,"temporada":"alongamento","serie":"Alongamento Ósseo",
  "motif_family":"bone","palette":"noturno_azul","layout":"auto",
  "scenes":[
   {"k":"QUANTO TEMPO?","sc":["Mais do que","a conta sugere."],"e":None,
    "sub":"O alongamento é a parte curta do tratamento.",
    "vo":"Alongar o osso leva bem mais tempo do que a conta de um milímetro por dia sugere."},
   {"k":"A parte curta","sc":["Um milímetro","por dia."],"e":None,
    "sub":"Dividido em pequenos ajustes ao longo do dia.",
    "vo":"A fase de alongamento é a mais rápida: o osso separa cerca de um milímetro por dia, em pequenos ajustes."},
   {"k":"A parte longa","sc":["A consolidação","leva mais."],"e":"consolidação",
    "sub":"É quando o osso novo endurece o suficiente para aguentar carga.",
    "vo":"Depois vem a consolidação, que leva bem mais tempo — é quando o osso novo endurece o suficiente para aguentar carga."},
   {"k":"Sinal de alarme","sc":["Dor em repouso?","Pronto-socorro."],"e":None,"motif":"no",
    "sub":"Dormência que avança ou sinais de infecção nos pinos.",
    "vo":"Durante o tratamento: dor intensa em repouso, dormência que avança ou sinais de infecção nos pinos pedem pronto-socorro, avisando a equipe."},
   {"k":"A disciplina decide","sc":["No meio","do caminho."],"e":None,
    "sub":"Dr. Rafael Vargas · CRM-SP 226103 · RQE 137901.",
    "vo":"É longo, e a disciplina no meio do caminho define o resultado. Se inscreve."},
  ],
  "caption":"Alongar o osso leva mais tempo do que a conta de 1mm por dia sugere. A fase de alongamento é a rápida; a consolidação — quando o osso novo endurece para aguentar carga — leva bem mais. Dor intensa em repouso, dormência que avança ou infecção nos pinos: pronto-socorro.\n\nDr. Rafael Vargas · CRM-SP 226103 · RQE 137901 — Reconstrução e Alongamento Ósseo · Ortopedia Pediátrica.\nConteúdo educativo, não substitui a avaliação do seu médico."},

 {"id":"tempo_tratamento_kids","ep":206,"temporada":"alongamento","serie":"Alongamento Ósseo",
  "motif_family":"bone","palette":"noturno_azul","layout":"auto",
  "scenes":[
   {"k":"QUANTO TEMPO?","sc":["Seu filho com","o fixador."],"e":None,
    "sub":"Guia para os pais: as duas fases e a rotina da escola.",
    "vo":"Quanto tempo seu filho vai ficar com o fixador? Mais do que a conta sugere."},
   {"k":"Duas fases","sc":["Alongar","e consolidar."],"e":None,
    "sub":"A consolidação é a fase mais longa das duas.",
    "vo":"A fase de alongamento é a mais rápida. Depois vem a consolidação, quando o osso novo endurece — e essa parte é a mais longa."},
   {"k":"A boa notícia","sc":["Criança consolida","mais rápido."],"e":"rápido",
    "sub":"Mas o plano segue igual: fisioterapia sem parar e consultas em dia.",
    "vo":"A boa notícia: criança costuma consolidar mais rápido que adulto. Mas o plano segue igual: fisioterapia sem parar e consultas em dia."},
   {"k":"Sinal de alarme","sc":["Criança prostrada?","Pronto-socorro."],"e":None,"motif":"no",
    "sub":"Dor intensa em repouso, dormência, ou secreção nos pinos com febre.",
    "vo":"Durante o tratamento: dor intensa em repouso, criança prostrada, dormência, ou secreção nos pinos com febre — pronto-socorro, avisando a equipe."},
   {"k":"Organize a escola","sc":["Desde o","começo."],"e":None,
    "sub":"Dr. Rafael Vargas · CRM-SP 226103 · RQE 137901.",
    "vo":"Organize a rotina da escola desde o começo. Se inscreve."},
  ],
  "caption":"Quanto tempo seu filho vai ficar com o fixador? São duas fases: o alongamento, mais rápido, e a consolidação, mais longa. A boa notícia é que criança costuma consolidar mais rápido que adulto — mas fisioterapia e consultas seguem iguais. Criança prostrada ou secreção nos pinos com febre: pronto-socorro.\n\nDr. Rafael Vargas · CRM-SP 226103 · RQE 137901 — Reconstrução e Alongamento Ósseo · Ortopedia Pediátrica.\nConteúdo educativo, não substitui a avaliação do seu médico."},

 # ═══════════════════════ LOTE 2 (01/08/2026) ═══════════════════════
 # Temas escolhidos por MEDICAO de sobreposicao contra os 40 episodios no ar (score 0):
 # pseudartrose, sequela de fratura/infeccao e primeira consulta. Os temas "fisioterapia" e
 # "andar/apoiar o pe" foram DESCARTADOS por ja estarem cobertos (carga_fisio, distracao_alongamento).
 # Nenhum destes 6 tem urgencia de pronto-socorro: sao temas de indicacao e preparacao.

 {"id":"pseudartrose","ep":207,"temporada":"alongamento","serie":"Alongamento Ósseo",
  "motif_family":"bone","palette":"noturno_azul","layout":"auto",
  "scenes":[
   {"k":"O OSSO NÃO COLOU?","sc":["Isso tem nome:","pseudartrose."],"e":None,
    "sub":"Fratura que não consolida no tempo esperado — e o que fazer.",
    "vo":"Fraturou, operou, e meses depois o osso ainda não colou? Isso tem nome: pseudartrose."},
   {"k":"O que é","sc":["O foco continua","se mexendo."],"e":None,
    "sub":"Não é falta de cálcio nem de sorte — é falha de consolidação.",
    "vo":"É quando a consolidação não acontece no tempo esperado e o foco da fratura continua se mexendo. Não é falta de cálcio nem de sorte."},
   {"k":"Por que acontece","sc":["Estabilidade,","circulação, cigarro."],"e":"cigarro",
    "sub":"Infecção no local também impede o osso de consolidar.",
    "vo":"Pesa a estabilidade do osso, a circulação no local, infecção — e o cigarro, que atrapalha muito a consolidação."},
   {"k":"Quando procurar","sc":["Dor meses","depois?"],"e":None,
    "sub":"Ou a sensação de que o membro não sustenta o peso.",
    "vo":"Dor que persiste no local da fratura meses depois, ou a sensação de que a perna não sustenta: leve para avaliação com quem trata reconstrução óssea."},
   {"k":"Tem tratamento","sc":["Pseudartrose","se trata."],"e":None,
    "sub":"Dr. Rafael Vargas · CRM-SP 226103 · RQE 137901.",
    "vo":"Pseudartrose tem tratamento. Se inscreve para os próximos."},
  ],
  "caption":"Fraturou, operou, e meses depois o osso não colou? Isso tem nome: pseudartrose — a consolidação não acontece e o foco continua se mexendo. Pesa a estabilidade, a circulação, infecção e o cigarro. Dor que persiste meses depois: procure avaliação com quem trata reconstrução óssea.\n\nDr. Rafael Vargas · CRM-SP 226103 · RQE 137901 — Reconstrução e Alongamento Ósseo · Ortopedia Pediátrica.\nConteúdo educativo, não substitui a avaliação do seu médico."},

 {"id":"pseudartrose_kids","ep":208,"temporada":"alongamento","serie":"Alongamento Ósseo",
  "motif_family":"bone","palette":"noturno_azul","layout":"auto",
  "scenes":[
   {"k":"NÃO COLOU?","sc":["O osso do seu","filho não colou."],"e":None,
    "sub":"Guia para os pais: quando o osso da criança não consolida.",
    "vo":"O osso do seu filho fraturou, tratou, e não colou? Isso tem nome e tem tratamento."},
   {"k":"Na criança","sc":["Criança costuma","consolidar bem."],"e":None,
    "sub":"Quando não cola, vale investigar a causa — não é só esperar mais.",
    "vo":"Criança costuma consolidar bem. Quando não cola, vale investigar a causa — não é só questão de esperar mais."},
   {"k":"Um alerta","sc":["Manchas na pele","junto?"],"e":"manchas",
    "sub":"Existe uma forma que aparece nos primeiros anos. Comente na consulta.",
    "vo":"Existe uma forma que aparece já nos primeiros anos, às vezes ligada a manchas na pele. Se você notou as duas coisas juntas, comente na consulta."},
   {"k":"Quando levar","sc":["Dor que não passa?","Deformidade?"],"e":None,
    "sub":"Ou a criança evitando apoiar o membro.",
    "vo":"Dor que não passa no local, deformidade que apareceu, ou a criança evitando apoiar o membro: leve para avaliação."},
   {"k":"Quanto antes","sc":["Mais opções","existem."],"e":None,
    "sub":"Dr. Rafael Vargas · CRM-SP 226103 · RQE 137901.",
    "vo":"Quanto antes avaliar, mais opções existem. Se inscreve."},
  ],
  "caption":"O osso do seu filho fraturou, tratou e não colou? Criança costuma consolidar bem — quando não cola, vale investigar a causa. Existe uma forma que aparece nos primeiros anos, às vezes ligada a manchas na pele: comente na consulta. Dor que não passa ou deformidade nova: leve para avaliação.\n\nDr. Rafael Vargas · CRM-SP 226103 · RQE 137901 — Reconstrução e Alongamento Ósseo · Ortopedia Pediátrica.\nConteúdo educativo, não substitui a avaliação do seu médico."},

 {"id":"sequela_fratura","ep":209,"temporada":"alongamento","serie":"Alongamento Ósseo",
  "motif_family":"bone","palette":"verde_clinico","layout":"auto",
  "scenes":[
   {"k":"COLOU TORTO?","sc":["Ainda dá","para tratar."],"e":None,
    "sub":"Sequela de fratura: desalinhamento, encurtamento ou infecção.",
    "vo":"Fratura que colou em posição ruim, encurtada, ou que infeccionou: ainda dá para tratar."},
   {"k":"O que é sequela","sc":["O osso colou.","Mas colou mal."],"e":None,
    "sub":"Desalinhado, mais curto, ou com a articulação limitada.",
    "vo":"O osso consolidou, mas ficou desalinhado, mais curto, ou com a articulação limitada. Isso muda a marcha e sobrecarrega o resto."},
   {"k":"Se houve infecção","sc":["Resolver junto","com a reconstrução."],"e":"junto",
    "sub":"É um tratamento mais longo, feito em etapas.",
    "vo":"Se houve infecção no osso, ela precisa ser resolvida junto com a reconstrução. É um tratamento mais longo, com etapas."},
   {"k":"Quando procurar","sc":["Disseram que não","havia o que fazer?"],"e":None,
    "sub":"Se você convive com dor ou manca, vale uma segunda opinião.",
    "vo":"Se você convive com dor, manca, ou foi informado que não havia mais o que fazer: vale uma segunda opinião com quem trata reconstrução óssea."},
   {"k":"Não é caso encerrado","sc":["Sequela antiga","tem opção."],"e":None,
    "sub":"Dr. Rafael Vargas · CRM-SP 226103 · RQE 137901.",
    "vo":"Sequela antiga não quer dizer caso encerrado. Se inscreve."},
  ],
  "caption":"Fratura que colou em posição ruim, encurtada ou que infeccionou ainda dá para tratar. A sequela muda a marcha e sobrecarrega o resto do corpo. Havendo infecção no osso, ela é resolvida junto com a reconstrução, em etapas. Se convive com dor ou manca: vale uma segunda opinião.\n\nDr. Rafael Vargas · CRM-SP 226103 · RQE 137901 — Reconstrução e Alongamento Ósseo · Ortopedia Pediátrica.\nConteúdo educativo, não substitui a avaliação do seu médico."},

 {"id":"sequela_fratura_kids","ep":210,"temporada":"alongamento","serie":"Alongamento Ósseo",
  "motif_family":"bone","palette":"verde_clinico","layout":"auto",
  "scenes":[
   {"k":"COLOU TORTO?","sc":["Em criança,","a conta é outra."],"e":None,
    "sub":"Guia para os pais: sequela de fratura na criança.",
    "vo":"A fratura do seu filho colou torta ou deixou a perna mais curta? Em criança, a conta é diferente."},
   {"k":"O crescimento ajuda","sc":["A criança","remodela o osso."],"e":"remodela",
    "sub":"Parte dos desalinhamentos melhora sozinha com o crescimento.",
    "vo":"A criança tem uma capacidade de remodelar o osso que o adulto não tem. Parte dos desalinhamentos melhora sozinha com o crescimento."},
   {"k":"Mas tem limite","sc":["Depende da idade","e do desvio."],"e":None,
    "sub":"Se a placa de crescimento se machucou, a diferença pode aumentar.",
    "vo":"Isso tem limite: depende da idade, do osso e do tipo de desvio. E quando a placa de crescimento se machuca, a diferença pode aumentar com o tempo."},
   {"k":"Quando acompanhar","sc":["Ele manca?","A diferença cresce?"],"e":None,
    "sub":"Fratura que envolveu a região de crescimento pede acompanhamento.",
    "vo":"Se ele manca, se a diferença está aumentando, ou se a fratura envolveu a região de crescimento: mantenha o acompanhamento de perto."},
   {"k":"Acompanhar é agir","sc":["Na hora","certa."],"e":None,
    "sub":"Dr. Rafael Vargas · CRM-SP 226103 · RQE 137901.",
    "vo":"Acompanhar é o que permite agir na hora certa. Se inscreve."},
  ],
  "caption":"A fratura do seu filho colou torta ou deixou a perna mais curta? Em criança a conta é diferente: ela remodela o osso, e parte dos desalinhamentos melhora com o crescimento. Mas tem limite — e se a placa de crescimento se machucou, a diferença pode aumentar. Mantenha o acompanhamento.\n\nDr. Rafael Vargas · CRM-SP 226103 · RQE 137901 — Reconstrução e Alongamento Ósseo · Ortopedia Pediátrica.\nConteúdo educativo, não substitui a avaliação do seu médico."},

 {"id":"primeira_consulta","ep":211,"temporada":"alongamento","serie":"Alongamento Ósseo",
  "motif_family":"bone","palette":"carvao_quente","layout":"auto",
  "scenes":[
   {"k":"PRIMEIRA CONSULTA?","sc":["Anote estas","perguntas."],"e":None,
    "sub":"O que perguntar numa consulta sobre alongamento ósseo.",
    "vo":"Vai na primeira consulta sobre alongamento ósseo? Anote estas perguntas antes de ir."},
   {"k":"Sobre o objetivo","sc":["O que exatamente","vai corrigir?"],"e":None,
    "sub":"Qual o objetivo funcional do tratamento no seu caso.",
    "vo":"Pergunte qual é o objetivo funcional do tratamento no seu caso, e o que exatamente ele pretende corrigir."},
   {"k":"Sobre a rotina","sc":["Quanto tempo?","E o trabalho?"],"e":None,
    "sub":"Qual método, tempo total, e como fica o deslocamento.",
    "vo":"Pergunte qual método, quanto tempo no total, e como fica sua rotina de trabalho e deslocamento durante o tratamento."},
   {"k":"Sobre o plano B","sc":["E se algo não sair","como esperado?"],"e":"plano",
    "sub":"Um bom plano prevê o que fazer se houver intercorrência.",
    "vo":"E pergunte quais são os riscos e o que se faz se algo não sair como esperado. Um bom plano prevê isso."},
   {"k":"Leve os exames","sc":["E os relatórios","anteriores."],"e":None,
    "sub":"Dr. Rafael Vargas · CRM-SP 226103 · RQE 137901.",
    "vo":"Leve seus exames e os relatórios anteriores. Se inscreve."},
  ],
  "caption":"Vai na primeira consulta sobre alongamento ósseo? Pergunte: qual o objetivo funcional e o que exatamente será corrigido; qual método, quanto tempo no total e como fica sua rotina; e quais os riscos e o plano se algo não sair como esperado. Leve seus exames e relatórios anteriores.\n\nDr. Rafael Vargas · CRM-SP 226103 · RQE 137901 — Reconstrução e Alongamento Ósseo · Ortopedia Pediátrica.\nConteúdo educativo, não substitui a avaliação do seu médico."},

 {"id":"primeira_consulta_kids","ep":212,"temporada":"alongamento","serie":"Alongamento Ósseo",
  "motif_family":"bone","palette":"carvao_quente","layout":"auto",
  "scenes":[
   {"k":"PRIMEIRA CONSULTA?","sc":["Levando seu filho","ao ortopedista."],"e":None,
    "sub":"Guia para os pais: o que levar e o que perguntar.",
    "vo":"Vai levar seu filho na primeira consulta de ortopedia? Anote o que perguntar."},
   {"k":"O que levar","sc":["Exames — e vídeo","de como ele anda."],"e":"anda",
    "sub":"Muita coisa se resolve vendo a marcha ao vivo.",
    "vo":"Leve os exames anteriores e, se tiver, as fotos de como ele anda. Muita coisa se resolve vendo a marcha ao vivo."},
   {"k":"O que perguntar","sc":["Observar","ou tratar agora?"],"e":None,
    "sub":"E de quanto em quanto tempo ele precisa voltar.",
    "vo":"Pergunte o que dá para observar e o que precisa tratar agora, e de quanto em quanto tempo ele precisa voltar."},
   {"k":"Sobre a rotina","sc":["Escola, educação","física, esporte."],"e":None,
    "sub":"Como fica o dia a dia dele durante o acompanhamento.",
    "vo":"Pergunte como fica a escola, a educação física e o esporte durante o acompanhamento."},
   {"k":"Acompanhado de perto","sc":["Mais opções","na hora certa."],"e":None,
    "sub":"Dr. Rafael Vargas · CRM-SP 226103 · RQE 137901.",
    "vo":"Criança acompanhada de perto tem mais opções. Se inscreve."},
  ],
  "caption":"Vai levar seu filho na primeira consulta de ortopedia? Leve os exames anteriores e, se tiver, vídeo de como ele anda. Pergunte o que dá para observar e o que precisa tratar agora, de quanto em quanto tempo voltar, e como fica escola, educação física e esporte.\n\nDr. Rafael Vargas · CRM-SP 226103 · RQE 137901 — Reconstrução e Alongamento Ósseo · Ortopedia Pediátrica.\nConteúdo educativo, não substitui a avaliação do seu médico."},
]
