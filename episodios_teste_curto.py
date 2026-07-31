# -*- coding: utf-8 -*-
"""
TESTE DE RETENÇÃO — versões CURTAS de 3 episódios da série "Recuperação" (30/07/2026).

Por quê: a auditoria v2 do canal mediu **watch médio de 6,6 s** contra um **gancho falado de 11,9 s** —
o espectador sai antes de a promessa terminar. O motor do Instagram já tinha resolvido o mesmo problema
em 26/07 (commit 5e006c7: 74 s -> 38 s, <=5 cenas), mas a série do YouTube ficou de fora ("pos-op
intactos"). Estes 3 são o teste controlado (opção B, aprovada pelo Rafael em 30/07).

Alvo do formato: **<=5 cenas · ~100 palavras · ~38-43 s**, gancho resolvido em <=7 s com a keyword
falada na 1a frase (sem "vou te mostrar" — anunciar o que vem custa a sessão inteira em Shorts).

VARIÁVEL ISOLADA: palette, motif_family e layout são os MESMOS do original de cada episódio, para que a
única diferença medida seja a DURAÇÃO/estrutura. Não mexer nisso sem refazer o desenho do teste.

GUARDRAIL CFM (conferido 3/3 antes de renderizar): a cena de sinal de alarme -> pronto-socorro é
INTOCÁVEL. Condensar é exatamente onde a conduta se perde. WhatsApp só para dúvida de rotina.

Roteiros aprovados pelo Rafael (RQE 137901) em 30/07/2026 —
ver Projeto_YouTube_Dr_Rafael_Vargas\APROVACAO_FORMATO_CURTO_2026-07-30.md
"""

TESTE_CURTO = [

 {"id":"infeccao_ferida_curto","ep":101,"temporada":"pos_operatorio","serie":"Recuperação",
  "motif_family":"bone","palette":"verde_clinico","layout":"auto",
  "scenes":[
   {"k":"PUS NA FERIDA?","sc":["Não espere","passar."],"e":None,
    "sub":"Pus, febre ou vermelhidão que avança: isso pede avaliação hoje.",
    "vo":"Pus, febre ou vermelhidão que avança na ferida da cirurgia: não espere passar."},
   {"k":"Sinais precoces","sc":["Vermelhidão","que cresce."],"e":"cresce",
    "sub":"Passa das bordas, aumenta a cada dia, com calor e dor que voltou.",
    "vo":"Comece pelo que aparece antes: vermelhidão que passa das bordas e cresce a cada dia, calor no local, e dor que voltou a aumentar."},
   {"k":"Não faça","sc":["Não esprema.","Não passe pomada."],"e":None,
    "sub":"Nada de antibiótico por conta própria — e não espere melhorar sozinho.",
    "vo":"Não esprema, não passe pomada ou antibiótico por conta própria, e não espere para ver se melhora sozinho."},
   {"k":"Sinal de alarme","sc":["Febre ou pus?","Pronto-socorro."],"e":None,"motif":"no",
    "sub":"Ferida aberta ou vermelhidão se alastrando: pronto-socorro na hora.",
    "vo":"Febre, pus, ferida que abriu ou vermelhidão se alastrando pela pele: pronto-socorro na hora, avisando a equipe no caminho. Infecção tratada cedo é bem mais simples."},
   {"k":"Todo dia","sc":["Olhe a ferida.","Todo dia."],"e":None,
    "sub":"Dúvida de rotina: WhatsApp (11) 3280-1413.",
    "vo":"Olhe a ferida todos os dias. Dúvida de rotina, WhatsApp. Se este vídeo te ajudou, se inscreve."},
  ],
  "caption":"Pus, febre ou vermelhidão que avança na ferida da cirurgia: não espere passar. Sinais precoces: vermelhidão além das bordas, calor, dor que voltou. Não esprema nem passe pomada por conta própria. Febre, pus ou ferida aberta: pronto-socorro.\n\nDr. Rafael Vargas · CRM-SP 226103 · RQE 137901 — Reconstrução e Alongamento Ósseo · Ortopedia Pediátrica.\nConteúdo educativo, não substitui a avaliação do seu médico."},

 {"id":"retorno_atividades_curto","ep":102,"temporada":"pos_operatorio","serie":"Recuperação",
  "motif_family":"bone","palette":"verde_clinico","layout":"auto",
  "scenes":[
   {"k":"QUANDO DIRIGIR?","sc":["Depende da","sua cirurgia."],"e":None,
    "sub":"Não do prazo do vizinho nem do que você leu na internet.",
    "vo":"Quando você pode voltar a dirigir, trabalhar e jogar bola depende da sua cirurgia — não do prazo do vizinho."},
   {"k":"A ordem das coisas","sc":["Escritório cedo.","Volante, não."],"e":None,
    "sub":"Dirigir exige reflexo total — nada de volante com analgésico forte.",
    "vo":"Trabalho de escritório costuma liberar cedo. Dirigir exige reflexo total: nada de volante usando analgésico forte ou com cirurgia no membro inferior."},
   {"k":"Esporte é o último","sc":["O tecido ainda","está remodelando."],"e":"remodelando",
    "sub":"Exige força e resistência — quem antecipa costuma recuar.",
    "vo":"O esporte volta por último, porque exige força e resistência de um tecido que ainda está se remodelando. Quem antecipa costuma recuar."},
   {"k":"Sinal de alarme","sc":["Dor aguda?","Pronto-socorro."],"e":None,"motif":"no",
    "sub":"Inchaço súbito ou trauma no retorno: pronto-socorro, avisando a equipe.",
    "vo":"Dor aguda intensa, inchaço súbito ou qualquer trauma durante o retorno: pronto-socorro, avisando a equipe. Dor nova ao retomar uma atividade é sinal de que foi cedo demais."},
   {"k":"Quem dá o prazo","sc":["É a sua equipe.","Não a internet."],"e":None,
    "sub":"Dúvida de rotina: WhatsApp (11) 3280-1413.",
    "vo":"Quem dá o prazo é a sua equipe, não a internet. Dúvida de rotina, WhatsApp. Se ajudou, se inscreve."},
  ],
  "caption":"Quando voltar a dirigir, trabalhar e jogar bola depende da SUA cirurgia — não do prazo do vizinho. Escritório libera cedo; dirigir exige reflexo total; esporte é o último. Dor aguda, inchaço súbito ou trauma no retorno: pronto-socorro.\n\nDr. Rafael Vargas · CRM-SP 226103 · RQE 137901 — Reconstrução e Alongamento Ósseo · Ortopedia Pediátrica.\nConteúdo educativo, não substitui a avaliação do seu médico."},

 {"id":"edema_curto","ep":103,"temporada":"pos_operatorio","serie":"Recuperação",
  "motif_family":"bone","palette":"carvao_quente","layout":"auto",
  "scenes":[
   {"k":"INCHOU MUITO?","sc":["Inchar é","esperado."],"e":None,
    "sub":"O que não é esperado: inchar de repente, só de um lado.",
    "vo":"Inchaço depois da cirurgia é esperado. O que não é esperado: inchar de repente, só de um lado."},
   {"k":"Por que incha","sc":["Sangue e líquido","para cicatrizar."],"e":None,
    "sub":"Por isso incha mais nos primeiros dias — faz parte do processo.",
    "vo":"O corpo manda sangue e líquido extra para a área operada para cicatrizar. Por isso incha mais nos primeiros dias."},
   {"k":"O que resolve","sc":["Eleve acima","do coração."],"e":"eleve",
    "sub":"Sempre que estiver parado. Pode levar semanas até sumir de vez.",
    "vo":"Elevar acima do coração sempre que estiver parado é o principal tratamento. Pode levar semanas até sumir de vez — e isso é normal."},
   {"k":"Sinal de alarme","sc":["Panturrilha dura?","Pronto-socorro."],"e":None,"motif":"no",
    "sub":"Inchaço súbito, vermelhidão, calor ou falta de ar: pode ser trombose.",
    "vo":"Inchaço que aumenta de repente, panturrilha dolorida e inchada mesmo em repouso, vermelhidão, calor ou falta de ar: pronto-socorro. Pode ser trombose."},
   {"k":"O esperado","sc":["Diminui","aos poucos."],"e":None,
    "sub":"Dúvida de rotina: WhatsApp (11) 3280-1413.",
    "vo":"Inchaço que diminui aos poucos é o esperado. Dúvida de rotina, WhatsApp. Se inscreve para os próximos."},
  ],
  "caption":"Inchaço depois da cirurgia é esperado — inchar de repente e só de um lado, não. Elevar acima do coração sempre que estiver parado é o principal tratamento. Inchaço súbito, panturrilha dolorida, vermelhidão ou falta de ar: pronto-socorro, pode ser trombose.\n\nDr. Rafael Vargas · CRM-SP 226103 · RQE 137901 — Reconstrução e Alongamento Ósseo · Ortopedia Pediátrica.\nConteúdo educativo, não substitui a avaliação do seu médico."},
]
