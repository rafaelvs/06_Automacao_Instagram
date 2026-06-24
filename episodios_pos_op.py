# -*- coding: utf-8 -*-
"""
Série "Recuperação" — vídeos PÓS-OPERATÓRIOS para o PACIENTE (faceless, voz Antonio).
Diferente de "Pé no Chão"/"Osso Novo": registro em 2ª pessoa (fala direta com o paciente),
instrução clínica clara. Saída serve como Short do YouTube + link p/ enviar ao paciente.

═══ CONVENÇÕES DA SÉRIE (aprendizados consolidados — todo episódio novo SEGUE isto) ═══
 1. PAR ADULTO + INFANTIL: todo tema tem 2 episódios — adulto (fala com o paciente) e a "irmã"
    infantil (fala com os PAIS sobre "seu filho"). id infantil = "<tema>_kids".
 2. SINAIS DE ALARME → PRONTO-SOCORRO imediato, avisando a equipe NO CAMINHO (paralelo). NUNCA
    direcionar emergência ao WhatsApp. WhatsApp (11) 3280-1413 só p/ DÚVIDA DE ROTINA (cena de resumo).
 3. ALARME INFANTIL = os "3 A" pediátricos (Analgesia↑ / Ansiedade / Agitação) + dedos roxos/frios /
    não mexe — porque a criança pequena não localiza/descreve a dor (precede sinais clássicos).
 4. EDEMA: elevar o membro SEMPRE que em repouso, durante TODA a recuperação. SEM gelo sobre o gesso.
 5. CARGA: "varia conforme a cirurgia; em geral proibida no início — siga sua equipe" (nunca afirmar regra fixa).
 6. CFM (Res. 2.336/2023): educativo, sem prometer resultado, sem paciente real, rodapé CRM/RQE+disclaimer.
 7. PROCESSO: cada roteiro nasce de revisão de literatura com fontes e é APROVADO pelo Rafael (RQE)
    ANTES do render. Voz: edge Antonio, rate -8%, pitch -4Hz. Roteiros em projeto YouTube/videos_pos_operatorio/.
════════════════════════════════════════════════════════════════════════════════════════

Ep 01  — gesso_pos_op       — Cuidados com o gesso (adulto).
Ep 02  — gesso_pos_op_kids  — Cuidados com o gesso (criança / aos pais).
"""
POS_OP = [
 {"id":"gesso_pos_op","ep":1,"temporada":"pos_operatorio","serie":"Recuperação","motif_family":"bone",
  "scenes":[
   {"k":"Pós-operatório","sc":["Saiu de gesso","depois da cirurgia?"],"e":None,
    "sub":"Os cuidados que protegem o resultado — e os sinais de alarme.",
    "vo":"Você operou e saiu de gesso. Vou te mostrar os cuidados que protegem o resultado da sua cirurgia. E, no final, os sinais que pedem o pronto-socorro."},
   {"k":"Para desinchar","sc":["Em repouso,","mantenha elevado."],"e":"elevado",
    "sub":"Acima do coração — sempre que parar, durante toda a recuperação.",
    "vo":"Sempre que estiver parado, em repouso, deixe o braço ou a perna apoiada em travesseiros, acima da altura do coração. Faça isso durante toda a recuperação: é o que desincha e evita que volte a inchar."},
   {"k":"Circulação","sc":["Mexa sempre","os dedos."],"e":"dedos",
    "sub":"Movimentar os dedos livres ativa a circulação e evita rigidez.",
    "vo":"Movimente sempre os dedos que ficaram de fora do gesso. Isso mantém o sangue circulando e evita que eles enrijeçam."},
   {"k":"No banho","sc":["Mantenha o","gesso seco."],"e":"seco",
    "sub":"Capa impermeável é o mais seguro. Não cutuque por dentro.",
    "vo":"No banho, o jeito mais seguro de não molhar é uma capa impermeável. Saco plástico com toalha, bem vedado, quebra o galho, mas pode vazar. E nunca enfie nada pra coçar, nem tire o enchimento."},
   {"k":"Integridade","sc":["Molhou ou","rachou?"],"e":None,
    "sub":"Seque só com ar frio. Se perdeu a forma: pronto-socorro.",
    "vo":"Se molhar, seque só com ar frio. Ar quente queima a pele, que fica dormente embaixo do gesso. E se o gesso rachar, amolecer ou perder a forma, vá ao pronto-socorro pra trocar ou reforçar. Depois a equipe reavalia na sua consulta."},
   {"k":"Apoio de peso","sc":["Só pise quando","for liberado."],"e":"liberado",
    "sub":"Em geral é proibido no início — varia conforme a sua cirurgia.",
    "vo":"Sobre pisar: na maioria das vezes, o apoio do peso é proibido no começo. Mas isso muda conforme a sua cirurgia. Siga à risca o que a sua equipe orientou."},
   {"k":"Emergência","sc":["Pronto-socorro","se sentir:"],"e":None,"motif":"no",
    "sub":"Dor crescente · dormência · dedos roxos ou frios · gesso apertando.",
    "vo":"Agora, o mais importante. Vá ao pronto-socorro na hora se sentir: dor que aumenta e não passa com o remédio; formigamento ou dormência; dedos roxos, pálidos ou frios; inchaço muito forte; ou o gesso apertando cada vez mais. Avise a sua equipe no caminho, mas não espere: pode ser compressão da circulação, uma emergência."},
   {"k":"Resumo","sc":["Emergência?","Pronto-socorro."],"e":"Pronto-socorro",
    "sub":"Dúvida de rotina: WhatsApp (11) 3280-1413.",
    "vo":"Resumindo: dúvida do dia a dia, fale com a nossa equipe no WhatsApp do consultório. Sinal de alarme, o caminho é o pronto-socorro. A sua recuperação é acompanhada de perto."},
  ],
  "caption":"Saiu de gesso depois da cirurgia? Os cuidados essenciais do pós-operatório — e os sinais que pedem PRONTO-SOCORRO imediato. Dúvidas de rotina fazem parte: fale com nossa equipe.\n\nDr. Rafael Vargas · CRM-SP 226103 · RQE 137901 — Reconstrução e Alongamento Ósseo · Ortopedia Pediátrica.\nConteúdo educativo, não substitui a avaliação do seu médico."},

 {"id":"gesso_pos_op_kids","ep":2,"temporada":"pos_operatorio","serie":"Recuperação","motif_family":"bone",
  "scenes":[
   {"k":"Pós-op infantil","sc":["Seu filho","saiu de gesso?"],"e":None,
    "sub":"Os cuidados — e os sinais que, numa criança, pedem pronto-socorro.",
    "vo":"Seu filho operou e saiu de gesso. Veja como cuidar nesses dias — e, principalmente, os sinais que, numa criança, pedem o pronto-socorro."},
   {"k":"Para desinchar","sc":["Em repouso,","deixe elevado."],"e":"elevado",
    "sub":"Acima do coração, sempre que parar — em toda a recuperação.",
    "vo":"Sempre que ele estiver parado, deitado no sofá ou na cama, apoie o bracinho ou a perna em travesseiros, acima da altura do coração. Faça isso a recuperação toda: desincha e evita que inche de novo."},
   {"k":"Circulação","sc":["Mexa os","dedinhos."],"e":"dedinhos",
    "sub":"Transforme em brincadeira — vira e mexe.",
    "vo":"Incentive a criança a mexer sempre os dedinhos que ficaram de fora. Vira brincadeira: mexe os dedos! Isso mantém o sangue circulando e evita que enrijeçam."},
   {"k":"No banho e no dia a dia","sc":["Nada entra","no gesso."],"e":None,
    "sub":"Capa impermeável · cubra a abertura · coceira: ar frio.",
    "vo":"No banho, proteja com uma capa impermeável e nunca mergulhe o gesso. E criança adora enfiar coisa lá dentro: cubra a abertura pra brinquedo, areia ou migalha não caírem. Se coçar, sopre ar frio com o secador, nunca um objeto."},
   {"k":"Integridade","sc":["Rachou ou","molhou?"],"e":None,
    "sub":"Perdeu a forma: pronto-socorro pra trocar ou reforçar.",
    "vo":"Criança bate o gesso o tempo todo. Se ele rachar, amolecer, molhar e não secar, ou perder a forma, leve ao pronto-socorro pra trocar ou reforçar. Depois a equipe reavalia na consulta."},
   {"k":"Apoio de peso","sc":["Só pisa se","liberado."],"e":"liberado",
    "sub":"Varia conforme a cirurgia — e exige supervisão.",
    "vo":"Sobre pôr o pé no chão: em geral é proibido no começo, mas varia conforme a cirurgia. Siga a orientação da equipe, e fique de olho, porque criança quer sair correndo."},
   {"k":"Emergência","sc":["Pronto-socorro","se notar:"],"e":None,"motif":"no",
    "sub":"Mais dor que antes · agitação · dedos roxos ou frios.",
    "vo":"Numa criança, o alarme mais importante é este: se ela passa a precisar de mais remédio pra dor do que antes, fica muito agitada, ansiosa ou chora sem parar. Some a isso dedos roxos, pálidos ou frios, ou que ela não mexe. Diante disso, pronto-socorro na hora, avisando a equipe no caminho. Pode ser compressão da circulação."},
   {"k":"Resumo","sc":["Emergência?","Pronto-socorro."],"e":"Pronto-socorro",
    "sub":"Dúvida de rotina: WhatsApp (11) 3280-1413.",
    "vo":"Resumindo: dúvida do dia a dia, fale com a nossa equipe no WhatsApp. Sinal de alarme, o caminho é o pronto-socorro. A recuperação do seu filho é acompanhada de perto."},
  ],
  "caption":"Seu filho saiu de gesso depois da cirurgia? Os cuidados no dia a dia — e os sinais de alarme na criança (mais dor que antes, agitação, dedos roxos/frios) que pedem PRONTO-SOCORRO imediato.\n\nDr. Rafael Vargas · CRM-SP 226103 · RQE 137901 — Reconstrução e Alongamento Ósseo · Ortopedia Pediátrica.\nConteúdo educativo, não substitui a avaliação do seu médico."},
]
