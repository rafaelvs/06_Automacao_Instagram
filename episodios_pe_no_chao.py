# -*- coding: utf-8 -*-
"""
Biblioteca de EPISÓDIOS da série "Pé no Chão" (reels narrativos faceless).
Formato: cada episódio = história curta (gancho -> tensão -> desenvolvimento -> payoff -> CTA de SEND).
Cada cena: k=kicker, sc=[2 linhas grandes], e=palavra dourada (ou None), sub=apoio, vo=narração (voz),
motif: "no" desenha o símbolo proibido. Última cena cta=True (otimizada p/ compartilhamento no direct).

CFM (Res. 2.336/2023): educativo, sem prometer/insinuar resultado, sem paciente real, com disclaimer.
Guardrail: NUNCA alongamento ósseo sob ângulo estético/altura. Tudo aqui é ortopedia pediátrica de
função / desenvolvimento / sinal de alerta. Temas escolhidos por potencial de SEND (pesquisa de demanda).
"""
SERIE = "Pé no Chão"
SIG = "Dr. Rafael Vargas · CRM-SP 226103 · RQE 137901"
HASH_BASE = "#ortopediapediatrica #ortopediainfantil #saudedacrianca #maternidade #paternidade #ortopediasaopaulo"

def cap(corpo, extra_tags=""):
    return (corpo + "\n\n📤 Manda pra um pai, mãe ou avó que precisa ver. 📌 Salva pra lembrar.\n"
            "💬 Dúvida? Comenta ou chama no direct.\n\n" + HASH_BASE + " " + extra_tags + "\n\n" + SIG)

EPISODES = [
 {"id":"andador","ep":1,"temporada":"quadril",
  "scenes":[
   {"k":"Mito x Verdade","sc":["O andador NÃO","ensina a andar."],"e":"NÃO","sub":"Vou te contar por quê — e o que ajuda de verdade.",
    "vo":"O andador não ensina o bebê a andar. E pode até atrapalhar."},
   {"k":"O que parece","sc":["Parece que ajuda:","a criança se move."],"e":None,"sub":"Mas no andador ela só desliza — empurra com a ponta dos pés.","motif":"no",
    "vo":"Parece que ajuda, porque a criança se move. Mas ali ela só desliza, empurrando com a ponta dos pés."},
   {"k":"O que de fato acontece","sc":["Andar de verdade","é equilíbrio."],"e":"equilíbrio","sub":"Equilíbrio se aprende caindo, levantando e firmando o próprio peso.",
    "vo":"Andar de verdade é equilíbrio. E equilíbrio se aprende caindo, levantando, firmando o próprio peso."},
   {"k":"E tem mais","sc":["Em excesso, está","associado a quedas."],"e":"quedas","sub":"E muda a forma como a criança apoia o quadril enquanto ele se forma.",
    "vo":"Em excesso, o andador está associado a quedas. E muda como a criança apoia o quadril enquanto ele ainda se forma."},
   {"k":"O que ajuda","sc":["Chão livre.","Descalço. Tempo."],"e":"Tempo","sub":"O empurrador entra depois, quando ela já fica de pé sozinha.",
    "vo":"O que ajuda é simples: chão livre, descalço e tempo. O empurrador entra depois, quando ela já fica de pé sozinha."},
   {"k":"Passa adiante","sc":["Manda pra quem","ainda usa andador."],"e":None,"sub":"Um pai, uma mãe, uma avó. Salva pra lembrar.","cta":True,
    "vo":"Manda esse vídeo pra quem ainda usa andador. Um pai, uma mãe, uma avó."},
  ],
  "caption":cap("Mito x Verdade: o andador NÃO ensina o bebê a andar. Parece que ajuda porque a criança se move — mas ali ela só desliza, empurrando com a ponta dos pés. Andar é equilíbrio, e equilíbrio se aprende sustentando o próprio peso. Usado em excesso, está associado a quedas e muda o apoio do quadril enquanto ele se forma. O que ajuda: chão livre, descalço e tempo; o empurrador entra quando o bebê já fica de pé sozinho.","#andador #primeirospassos #desenvolvimentoinfantil")},

 {"id":"pe_chato","ep":2,"temporada":"pernas",
  "scenes":[
   {"k":"Mito x Verdade","sc":["Pé chato nem","sempre é problema."],"e":"nem","sub":"E quase nunca se resolve com aquela palmilha cara.",
    "vo":"Pé chato nem sempre é problema. E quase nunca se resolve com aquela palmilha cara."},
   {"k":"O que quase ninguém conta","sc":["Todo bebê nasce","com pé chato."],"e":None,"sub":"O arco do pé vai se formando sozinho ao longo da infância.",
    "vo":"Quase ninguém conta: todo bebê nasce com o pé chato. O arco vai se formando sozinho ao longo da infância."},
   {"k":"A virada","sc":["Palmilha não","molda o arco."],"e":"não","sub":"Em pé flexível e sem dor, ela costuma ser gasto sem necessidade.","motif":"no",
    "vo":"E a palmilha não molda o arco. No pé flexível e sem dor, costuma ser um gasto sem necessidade."},
   {"k":"Quando acender o alerta","sc":["Dói, é rígido","ou só num pé."],"e":None,"sub":"Pé chato que dói, que é duro ou apareceu de repente merece avaliação.",
    "vo":"O alerta é outro: pé que dói, que é rígido, ou que ficou chato só de um lado. Aí sim vale avaliar."},
   {"k":"Passa adiante","sc":["Antes de comprar","palmilha, avalie."],"e":None,"sub":"Manda pra um pai ou mãe que vai gastar sem precisar.","cta":True,
    "vo":"Antes de comprar palmilha, avalie. Manda isso pra um pai ou mãe que ia gastar sem precisar."},
  ],
  "caption":cap("Mito x Verdade: pé chato na criança quase nunca é problema. Todo bebê nasce com o pé plano e o arco se forma sozinho ao longo da infância — e a palmilha NÃO molda esse arco. Em pé flexível e sem dor, ela costuma ser gasto desnecessário. O que merece avaliação é o pé que dói, que é rígido ou que ficou chato só de um lado.","#pechato #peplano #palmilha")},

 {"id":"dor_crescimento","ep":3,"temporada":"crescimento",
  "scenes":[
   {"k":"Mito x Verdade","sc":["Dor de crescimento","existe — e é real."],"e":"real","sub":"Não é frescura. Mas tem um padrão que tranquiliza.",
    "vo":"Dor de crescimento existe, e é real. Não é frescura. Mas tem um padrão que tranquiliza."},
   {"k":"O padrão que acalma","sc":["Nas duas pernas,","à noite."],"e":None,"sub":"Costuma vir no fim do dia, sem inchaço e sem febre — e some pela manhã.",
    "vo":"O padrão que acalma: dói nas duas pernas, no fim do dia ou à noite, sem inchaço e sem febre. E some pela manhã."},
   {"k":"De manhã","sc":["A criança acorda","e brinca normal."],"e":"normal","sub":"Se à noite doeu mas de dia ela corre e pula, isso fala a favor.",
    "vo":"De manhã, a criança acorda e brinca normal. Se doeu à noite mas de dia ela corre e pula, isso fala a favor."},
   {"k":"Bandeira vermelha","sc":["Só num lugar,","com inchaço."],"e":None,"sub":"Dor numa articulação só, com manqueira, febre ou que persiste: avalie.","motif":"no",
    "vo":"A bandeira vermelha é o contrário: dor num lugar só, com inchaço, manqueira ou febre. Aí precisa avaliar."},
   {"k":"Passa adiante","sc":["Salva pra noite","que bater dúvida."],"e":None,"sub":"E manda pra outra mãe que já passou por essa noite.","cta":True,
    "vo":"Salva pra próxima noite que bater a dúvida. E manda pra outra mãe que já passou por isso."},
  ],
  "caption":cap("Dor de crescimento é real — não é frescura. O padrão que tranquiliza: dói nas DUAS pernas, à noite ou no fim do dia, sem inchaço e sem febre, e some pela manhã, com a criança brincando normal no dia seguinte. A bandeira vermelha é o oposto: dor numa articulação só, com inchaço, febre ou manqueira, ou que persiste — isso merece avaliação.","#dordecrescimento #criancas")},

 {"id":"displasia_quadril","ep":4,"temporada":"quadril",
  "scenes":[
   {"k":"Sinal de alerta","sc":["Um detalhe no","bebê muda tudo."],"e":None,"sub":"O quadril que 'sai do lugar' — e por que achar cedo importa tanto.",
    "vo":"Um detalhe no bebê pode mudar tudo: o quadril que sai do lugar. E achar cedo importa muito."},
   {"k":"O que observar","sc":["Pregas tortas.","Uma perna curta."],"e":None,"sub":"Assimetria nas dobrinhas da coxa ou pernas de tamanhos diferentes.",
    "vo":"O que observar: as dobrinhas da coxa tortas, assimétricas, ou uma perna parecendo mais curta que a outra."},
   {"k":"Mais um sinal","sc":["A perna abre","menos de um lado."],"e":"menos","sub":"Na troca de fralda, um lado abre menos que o outro.",
    "vo":"Mais um sinal: na hora da fralda, um lado do quadril abre menos que o outro."},
   {"k":"Por que correr","sc":["Cedo: uma faixa.","Tarde: cirurgia."],"e":None,"sub":"Diagnóstico precoce costuma se resolver com órtese; tardio, complica.",
    "vo":"Por que correr: cedo, costuma se resolver com uma órtese. Tarde, o caminho fica bem mais difícil."},
   {"k":"Passa adiante","sc":["Manda pra quem","tem bebê em casa."],"e":None,"sub":"Esse é daqueles que vale demais compartilhar.","cta":True,
    "vo":"Manda pra quem tem bebê em casa. Esse vale demais compartilhar."},
  ],
  "caption":cap("Displasia do desenvolvimento do quadril: achar cedo muda o desfecho. Observe assimetria nas pregas (dobrinhas) da coxa, uma perna parecendo mais curta, ou um lado do quadril que abre menos na troca de fralda. Diagnóstico precoce costuma se resolver com órtese; tardio costuma exigir tratamentos mais complexos. Na dúvida, leve ao ortopedista pediátrico.","#displasiadoquadril #ddq #bebe")},

 {"id":"pernas_tortas","ep":5,"temporada":"pernas",
  "scenes":[
   {"k":"Calma, pais","sc":["Perna torta quase","sempre é fase."],"e":"fase","sub":"Tem até um cronograma — e ele costuma terminar bem.",
    "vo":"Perna torta na criança quase sempre é fase. Tem até um cronograma, e ele costuma terminar bem."},
   {"k":"Até os 2 anos","sc":["Arqueada para","fora é comum."],"e":None,"sub":"O famoso 'perninha de cowboy' costuma ser normal nessa idade.",
    "vo":"Até por volta dos 2 anos, a perna arqueada para fora é comum. O famoso jeitinho de cowboy."},
   {"k":"Dos 3 aos 4","sc":["Vira para dentro,","em X."],"e":"X","sub":"Depois ela inverte e fica em X — e isso também é esperado.",
    "vo":"Dos 3 aos 4 anos, ela inverte e fica em X. E isso também é esperado."},
   {"k":"Por volta dos 7","sc":["Costuma alinhar","sozinha."],"e":"sozinha","sub":"O alerta é só se for assimétrico, doloroso ou persistir depois disso.","motif":None,
    "vo":"E por volta dos 7 anos costuma alinhar sozinha. O alerta é só se for assimétrico, doloroso, ou persistir."},
   {"k":"Passa adiante","sc":["Salva esse","cronograma."],"e":None,"sub":"E manda pra mãe que está achando a perna do filho torta.","cta":True,
    "vo":"Salva esse cronograma. E manda pra mãe que está achando a perna do filho torta."},
  ],
  "caption":cap("Pernas tortas na infância quase sempre são FASE, com cronograma: até ~2 anos é comum a perna arqueada para fora (varo); dos 3 aos 4 ela inverte e fica em X (valgo); e por volta dos 6–7 costuma alinhar sozinha. O alerta é quando a curvatura é assimétrica (só um lado), dolorosa, ou persiste depois dessa idade — aí vale avaliar.","#pernastortas #genovaro #genovalgo")},

 {"id":"ponta_dos_pes","ep":6,"temporada":"marcha",
  "scenes":[
   {"k":"Sinal de alerta","sc":["Anda na ponta","dos pés?"],"e":None,"sub":"Tem uma idade que separa o 'normal' do 'vale avaliar'.",
    "vo":"Seu filho anda na ponta dos pés? Tem uma idade que separa o normal do vale avaliar."},
   {"k":"Nos primeiros anos","sc":["É comum e","costuma passar."],"e":"passar","sub":"Muita criança experimenta andar na ponta — e larga sozinha.",
    "vo":"Nos primeiros anos é comum e costuma passar. Muita criança experimenta a ponta do pé e larga sozinha."},
   {"k":"A linha que importa","sc":["Persistiu depois","dos 3 anos?"],"e":None,"sub":"Se anda na ponta o tempo todo após os 3, vale uma avaliação.",
    "vo":"A linha que importa: se persistiu depois dos 3 anos, andando na ponta o tempo todo, vale avaliar."},
   {"k":"Fique de olho se","sc":["Só faz de um","lado, ou enrijece."],"e":None,"sub":"Um lado só, panturrilha dura ou atraso no andar pedem atenção.","motif":None,
    "vo":"Fique de olho também se é só de um lado, se a panturrilha endurece, ou se veio com atraso pra andar."},
   {"k":"Passa adiante","sc":["Guarda a regra","dos 3 anos."],"e":None,"sub":"E manda pra quem vê o filho na pontinha o dia todo.","cta":True,
    "vo":"Guarda a regra dos 3 anos. E manda pra quem vê o filho na pontinha o dia todo."},
  ],
  "caption":cap("Andar na ponta dos pés nos primeiros anos é comum e costuma passar sozinho. A regra prática: se PERSISTE o tempo todo depois dos 3 anos, vale avaliar. Acenda o alerta também se for só de um lado, se a panturrilha endurece, ou se veio junto com atraso para andar.","#andarnapontadope #marcha #desenvolvimento")},

 {"id":"pe_torto","ep":7,"temporada":"reconstrucao",
  "scenes":[
   {"k":"Micro-caso","sc":["Imagine um pé","que nasce virado."],"e":None,"sub":"O pé torto congênito. E a notícia boa que vem com ele.",
    "vo":"Imagine um pé que já nasce virado para dentro. É o pé torto congênito. E vem com uma notícia boa."},
   {"k":"A janela de ouro","sc":["O começo é nas","primeiras semanas."],"e":None,"sub":"Quanto mais cedo, mais o pezinho do bebê coopera.",
    "vo":"A janela de ouro é o começo nas primeiras semanas de vida, quando o pezinho do bebê ainda é bem flexível."},
   {"k":"Como funciona","sc":["Gessos que","corrigem aos poucos."],"e":None,"sub":"O método de Ponseti molda o pé em etapas, com gesso e depois órtese.",
    "vo":"Como funciona: gessos que corrigem aos poucos. É o método de Ponseti, que molda o pé em etapas."},
   {"k":"O desfecho","sc":["Na maioria, sem","grande cirurgia."],"e":None,"sub":"Começando cedo, a maior parte dos casos corrige sem cirurgia grande.",
    "vo":"O desfecho: começando cedo, a maior parte dos casos corrige sem precisar de uma grande cirurgia."},
   {"k":"Passa adiante","sc":["Manda pra quem","espera um bebê."],"e":None,"sub":"Saber disso antes muda a forma de receber o diagnóstico.","cta":True,
    "vo":"Manda pra quem espera um bebê. Saber disso antes muda a forma de receber o diagnóstico."},
  ],
  "caption":cap("Pé torto congênito: o pé já nasce virado para dentro — e a notícia boa é o tratamento. A janela de ouro é começar nas primeiras semanas, com o método de Ponseti: gessos que corrigem o pé aos poucos, depois uma órtese de manutenção. Começando cedo, a maior parte dos casos corrige sem grande cirurgia. Conteúdo educativo; cada caso é avaliado individualmente.","#petorto #ponseti #recemnascido")},

 {"id":"quando_procurar","ep":8,"temporada":"socorros",
  "scenes":[
   {"k":"Salva este","sc":["Quando levar ao","ortopedista infantil?"],"e":None,"sub":"5 sinais que valem uma avaliação — sem pânico, com atenção.",
    "vo":"Quando levar ao ortopedista infantil? Cinco sinais que valem uma avaliação. Sem pânico, com atenção."},
   {"k":"Sinais 1 e 2","sc":["Manca, ou evita","pisar num pé."],"e":None,"sub":"Mancar sem motivo claro, ou proteger sempre o mesmo lado.",
    "vo":"Sinais um e dois: a criança manca, ou evita pisar sempre no mesmo pé."},
   {"k":"Sinais 3 e 4","sc":["Dor que volta,","ou queda fácil."],"e":None,"sub":"Dor frequente no mesmo lugar, ou tropeços e quedas demais.",
    "vo":"Três e quatro: dor que volta sempre no mesmo lugar, ou quedas e tropeços demais."},
   {"k":"Sinal 5","sc":["Um lado diferente","do outro."],"e":"diferente","sub":"Assimetria: um ombro, um quadril ou uma perna fora do par.",
    "vo":"E o quinto: assimetria. Um ombro, um quadril ou uma perna visivelmente diferente do outro lado."},
   {"k":"Passa adiante","sc":["Salva e manda","pra um pai ou mãe."],"e":None,"sub":"Na dúvida, avaliar cedo costuma simplificar tudo.","cta":True,
    "vo":"Salva e manda pra um pai ou mãe. Na dúvida, avaliar cedo costuma simplificar tudo."},
  ],
  "caption":cap("Quando levar ao ortopedista infantil? 5 sinais: 1) manca ou evita pisar num pé; 2) protege sempre o mesmo lado; 3) dor que volta no mesmo lugar; 4) quedas e tropeços demais; 5) assimetria — um ombro, quadril ou perna diferente do outro. Sem pânico: na dúvida, avaliar cedo costuma simplificar tudo.","#ortopediainfantil #sinaisdealerta #quandoprocurar")},
]

def get(ep_id):
    for e in EPISODES:
        if e["id"]==ep_id: return e
    raise KeyError(ep_id)

if __name__=="__main__":
    print(len(EPISODES),"episódios:")
    for e in EPISODES: print(f"  ep{e['ep']:02d} {e['id']:18s} temporada={e['temporada']:12s} cenas={len(e['scenes'])}")
