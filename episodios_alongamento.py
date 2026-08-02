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
]
