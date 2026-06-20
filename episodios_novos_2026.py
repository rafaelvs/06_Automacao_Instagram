# -*- coding: utf-8 -*-
"""
LOTE 2026 — 30 novos episódios narrados (voz), encadeados pela Arquitetura de Ganchos 2026.
  • 18 reels da série "Osso Novo" (reconstrução / alongamento ósseo) — pilar de autoridade.
  • 12 reels novos da série "Pé no Chão" (ortopedia pediátrica) — pilar de alcance.

Mesma engenharia dos pilotos (render_reel + gerar_reel_voz). Cada cena:
  k=kicker, sc=[2 linhas], e=palavra dourada (ou None), sub=apoio na tela, vo=narração (voz complementa),
  motif:"no" desenha o símbolo proibido. Última cena cta=True (otimizada p/ SEND no direct).
Campo novo: "serie" (rótulo no cabeçalho) e "motif_family" ("bone" desenha o vão preenchendo + régua mm).

GUARDRAIL (inegociável): a série Osso Novo trata alongamento/reconstrução SEMPRE sob função, trauma,
deformidade e sequela — NUNCA sob ângulo estético, cosmético ou de altura. Vários reels reafirmam isso.
CFM (Res. 2.336/2023): educativo, sem prometer/insinuar resultado, sem paciente real; rodapé com CRM/RQE
e disclaimer já entram em todo frame pelo render. Cada gancho de saída é pago no gancho de 3s do próximo.
"""
SIG = "Dr. Rafael Vargas · CRM-SP 226103 · RQE 137901"
HASH_PED = "#ortopediapediatrica #ortopediainfantil #saudedacrianca #maternidade #paternidade #ortopediasaopaulo"
HASH_REC = "#reconstrucaoossea #alongamentoosseo #ortopediasaopaulo #pseudartrose #fixadorexterno #traumatortopedico"

def _cap(corpo, hashes, extra_tags, cta_linha):
    return (corpo + "\n\n" + cta_linha + "\n📌 Salva pra lembrar. 💬 Dúvida? Comenta ou chama no direct.\n\n"
            + hashes + " " + extra_tags + "\n\n" + SIG)

def cap_ped(corpo, extra_tags=""):
    return _cap(corpo, HASH_PED, extra_tags, "📤 Manda pra um pai, mãe ou avó que precisa ver.")

def cap_rec(corpo, extra_tags=""):
    # série Osso Novo: público adulto + tagline de marca
    return _cap(corpo, HASH_REC, extra_tags,
                "📤 Manda pra quem está reconstruindo um osso — ou ama alguém que está.\n🦴 Osso novo, de volta ao movimento.")

# ───────────────────────────── SÉRIE "OSSO NOVO" (18) ─────────────────────────────
OSSO_NOVO = [
 {"id":"on_osso_cresce","ep":1,"serie":"Osso Novo","temporada":"o-osso-se-refaz","motif_family":"bone",
  "scenes":[
   {"k":"Como assim?","sc":["O osso cresce","no espaço vazio."],"e":None,"sub":"Parece ficção — mas é biologia, e tem nome.",
    "vo":"Parece difícil de acreditar, mas é pura biologia: o corpo é capaz de fabricar osso novo onde antes não tinha nada."},
   {"k":"A ideia","sc":["Separe o osso","devagarinho."],"e":"devagarinho","sub":"As duas pontas afastam pouquíssimo por dia — e o vão não fica vazio.",
    "vo":"A sacada é separar as duas pontas do osso bem devagar. No vão que se abre, o corpo entende que precisa preencher e começa a produzir osso ali."},
   {"k":"O nome disso","sc":["Osteogênese","por distração."],"e":None,"sub":"Distrair = afastar. A tração lenta acorda a fábrica de osso.",
    "vo":"Esse processo tem nome: osteogênese por distração. Distrair, aqui, quer dizer afastar. É a tração lenta que liga a fábrica de osso."},
   {"k":"Pra que serve","sc":["Reconstruir o que","faltou ou encurtou."],"e":None,"sub":"Trauma, infecção, deformidade — função e movimento, nunca estética.",
    "vo":"E pra que serve? Pra reconstruir osso perdido num trauma, numa infecção, ou corrigir uma diferença entre as pernas. É sobre função e movimento, nunca sobre estética."},
   {"k":"Passa adiante","sc":["Salva: o corpo","refaz osso."],"e":None,"sub":"Manda pra quem acha que osso não se recupera.","cta":True,
    "vo":"Guarda essa: o corpo refaz osso. E no próximo eu te conto por que isso não acontece do nada. Tem um ritmo, a regra do milímetro."},
  ],
  "caption":cap_rec("O osso cresce no espaço vazio. Quando se separam lentamente as duas pontas de um osso, o corpo preenche o vão com osso novo — isso se chama osteogênese por distração. É a base da reconstrução e do alongamento ósseo, usada para refazer o que um trauma, uma infecção ou uma deformidade tiraram. Aqui é sempre sobre função e movimento, nunca estética ou altura. Conteúdo educativo; cada caso é avaliado individualmente.","#osteogeneseporodistração #reconstrucao")},

 {"id":"on_regra_milimetro","ep":2,"serie":"Osso Novo","temporada":"o-osso-se-refaz","motif_family":"bone",
  "scenes":[
   {"k":"O ritmo","sc":["1 milímetro","por dia."],"e":"1 milímetro","sub":"Em geral em 2 a 4 vezes ao dia. É devagar de propósito.",
    "vo":"Tem um ritmo que comanda tudo: mais ou menos um milímetro por dia, normalmente dividido em algumas vezes ao longo do dia. É devagar de propósito."},
   {"k":"Por que não correr","sc":["Rápido demais:","osso não forma."],"e":None,"sub":"A nova ponte óssea precisa de tempo pra se montar.",
    "vo":"Se afasta rápido demais, o osso novo não consegue se formar no vão e o tecido só estica. A pressa, aqui, atrapalha."},
   {"k":"Por que não lento","sc":["Devagar demais:","cola antes da hora."],"e":None,"sub":"Se demora, o osso endurece e trava a correção no meio.",
    "vo":"E se for devagar demais, acontece o contrário: o osso endurece antes da hora e trava a correção lá no meio do caminho."},
   {"k":"Quem ajusta","sc":["Milímetro a","milímetro, com você."],"e":None,"sub":"O ritmo é acompanhado de perto e ajustado caso a caso.",
    "vo":"Por isso é tudo acompanhado de pertinho, ajustando o ritmo conforme o seu osso responde. Não existe piloto automático."},
   {"k":"Passa adiante","sc":["Salva a regra","do milímetro."],"e":None,"sub":"Manda pra quem vai operar e tem essa dúvida.","cta":True,
    "vo":"Guarda a regra do milímetro. E no próximo: por que esse osso novo passa por fases até ficar firme."},
  ],
  "caption":cap_rec("A regra do milímetro. No alongamento e na reconstrução óssea, as pontas do osso são afastadas cerca de 1 mm por dia, em geral em 2 a 4 vezes. Mais rápido, o osso novo não se forma; mais devagar, ele endurece antes da hora e trava a correção. Por isso o ritmo é acompanhado de perto e ajustado para cada pessoa. É sobre devolver função — nunca estética.","#alongamentoosseo #milimetro")},

 {"id":"on_tres_fases","ep":3,"serie":"Osso Novo","temporada":"o-osso-se-refaz","motif_family":"bone",
  "scenes":[
   {"k":"As 3 fases","sc":["Todo osso novo","passa por 3 etapas."],"e":"3 etapas","sub":"Entender as fases tira a ansiedade de quem está no meio.",
    "vo":"Reconstruir osso não é instantâneo: passa por três etapas. Entender cada uma tira muito da ansiedade de quem está no meio do tratamento."},
   {"k":"Fase 1 — latência","sc":["Espera antes","de afastar."],"e":None,"sub":"Alguns dias parados pro osso começar a se reparar.",
    "vo":"A primeira é a latência: alguns dias parados, sem mexer, pro osso começar a acordar e iniciar o reparo."},
   {"k":"Fase 2 — distração","sc":["O milímetro","por dia."],"e":None,"sub":"É aqui que o osso novo vai sendo formado dentro do vão.",
    "vo":"A segunda é a distração: aquele milímetro por dia. É nessa fase que o osso novo vai sendo formado dentro do vão."},
   {"k":"Fase 3 — consolidação","sc":["Parar e deixar","endurecer."],"e":None,"sub":"Costuma ser a fase mais longa — e a que define o resultado.",
    "vo":"E a terceira é a consolidação: para de afastar e dá tempo pro osso amadurecer e endurecer. Costuma ser a fase mais longa, e é a que define o resultado."},
   {"k":"Passa adiante","sc":["Salva as","3 fases."],"e":None,"sub":"Manda pra alguém no meio de uma reconstrução.","cta":True,
    "vo":"Salva as três fases. E se o osso, mesmo assim, simplesmente não cola? É o próximo."},
  ],
  "caption":cap_rec("As 3 fases do alongamento e da reconstrução óssea: latência (alguns dias parado, para o osso iniciar o reparo), distração (o famoso 1 mm por dia, quando o osso novo se forma) e consolidação (parar e deixar o osso amadurecer e endurecer — costuma ser a fase mais longa). Saber em que fase se está tira boa parte da ansiedade do processo.","#consolidacaoossea #reconstrucao")},

 {"id":"on_pseudartrose","ep":4,"serie":"Osso Novo","temporada":"quando-o-osso-falha","motif_family":"bone",
  "scenes":[
   {"k":"Existe isso?","sc":["Fratura que","não cola."],"e":"não","sub":"Quando a consolidação falha, vira o que chamamos de pseudartrose.",
    "vo":"A maioria das fraturas cola sozinha. Mas existe um grupo que, por algum motivo, não cola. E isso tem nome: pseudartrose."},
   {"k":"O que é","sc":["Um osso que","parou de cicatrizar."],"e":None,"sub":"Pseudo + artrose: uma 'falsa junta' onde devia ser osso firme.",
    "vo":"A palavra assusta, mas a ideia é simples: é um osso que parou de cicatrizar e ficou com mobilidade onde deveria estar firme. Uma falsa junta."},
   {"k":"Sinais","sc":["Dor que volta,","meses depois."],"e":None,"sub":"Dor no foco da fratura e sensação de instabilidade além do previsto.",
    "vo":"Os sinais costumam ser dor que insiste no lugar da fratura muito além do esperado, e uma sensação de que ali ainda mexe."},
   {"k":"Tem caminho","sc":["Não cola sozinha,","mas tem caminho."],"e":"caminho","sub":"Estabilizar, estimular e, às vezes, refazer o osso — caso a caso.",
    "vo":"A boa notícia é que pseudartrose costuma ter solução. Geralmente envolve estabilizar melhor, estimular o osso e, em alguns casos, refazer aquele trecho. Sempre avaliado caso a caso."},
   {"k":"Passa adiante","sc":["Salva: osso que","não cola tem saída."],"e":None,"sub":"Manda pra quem está há meses com uma fratura que não fecha.","cta":True,
    "vo":"Manda pra quem está há meses com uma fratura que não fecha. E no próximo: as três coisas que travam um osso. Uma você controla hoje."},
  ],
  "caption":cap_rec("Pseudartrose: a fratura que não cola. Quando a consolidação falha, o osso fica com mobilidade onde deveria estar firme — uma 'falsa junta'. Os sinais costumam ser dor persistente no foco da fratura e sensação de instabilidade muito além do tempo esperado. Costuma ter solução: estabilizar melhor, estimular o osso e, às vezes, refazer o trecho. Sempre individualizado.","#pseudartrose #fratura")},

 {"id":"on_tres_razoes","ep":5,"serie":"Osso Novo","temporada":"quando-o-osso-falha","motif_family":"bone",
  "scenes":[
   {"k":"3 motivos","sc":["3 coisas travam","a cola do osso."],"e":"3 coisas","sub":"Estabilidade, sangue e ausência de infecção — o tripé da consolidação.",
    "vo":"Pra um osso colar, ele precisa de um tripé: firmeza, sangue chegando e nenhuma infecção no caminho. Quando um desses falha, a cicatrização emperra."},
   {"k":"1 — movimento demais","sc":["Se mexe demais,","não cola."],"e":None,"sub":"Osso precisa de estabilidade — daí placas, hastes e fixadores.",
    "vo":"O primeiro é movimento demais. Osso só cola firme se ficar estável. É por isso que existem placas, hastes e fixadores: pra segurar enquanto cicatriza."},
   {"k":"2 — pouco sangue","sc":["Sem irrigação,","sem cura."],"e":None,"sub":"Cicatrização depende de sangue chegando ao osso.",
    "vo":"O segundo é a circulação. Toda cicatrização depende de sangue chegando ali. Pouco sangue, cura lenta ou nenhuma."},
   {"k":"3 — infecção","sc":["Infecção","atrapalha tudo."],"e":None,"sub":"Um osso ocupado se defendendo não se concentra em colar.",
    "vo":"E o terceiro é infecção. Um osso ocupado se defendendo de bactéria não consegue se concentrar em colar."},
   {"k":"Passa adiante","sc":["Salva o tripé","da consolidação."],"e":None,"sub":"Tem um fator desse tripé que está na sua mão hoje.","cta":True,
    "vo":"Salva esse tripé. E tem um item dele que está na sua mão mudar hoje, o que mais surpreende: o cigarro. É o próximo."},
  ],
  "caption":cap_rec("Por que um osso não consolida? Há um tripé: estabilidade (osso que se mexe demais não cola — por isso placas, hastes e fixadores), circulação (sem sangue chegando, não há cicatrização) e ausência de infecção (um osso infectado prioriza se defender). Quando um desses falha, a consolidação emperra. E há um fator desse tripé que está na sua mão mudar.","#consolidacaoossea #ortopedia")},

 {"id":"on_cigarro","ep":6,"serie":"Osso Novo","temporada":"quando-o-osso-falha","motif_family":"bone",
  "scenes":[
   {"k":"O vilão escondido","sc":["O cigarro atrapalha","o osso colar."],"e":"cigarro","sub":"Não é mito: fumar prejudica a consolidação óssea.",
    "vo":"Esse aqui pega muita gente de surpresa. O cigarro está entre as coisas que mais atrapalham um osso a colar. E não é achismo, é bem estabelecido."},
   {"k":"Por quê","sc":["Menos oxigênio","chega no osso."],"e":None,"sub":"A nicotina aperta os vasos e reduz o sangue e o oxigênio que chegam.",
    "vo":"O motivo conversa com o vídeo anterior: a nicotina aperta os vasos e diminui o oxigênio e o sangue que chegam no osso. E sem isso, a cura emperra."},
   {"k":"Quanto pesa","sc":["Mais risco de","não consolidar."],"e":None,"sub":"Fumantes têm risco maior de pseudartrose e cicatrização lenta.",
    "vo":"Na prática, quem fuma tem risco maior de pseudartrose, de infecção e de uma cicatrização mais arrastada. Pesa de verdade no resultado."},
   {"k":"A boa notícia","sc":["Parar antes ajuda,","e muito."],"e":"ajuda","sub":"Reduzir ou parar no período da cirurgia melhora as chances.",
    "vo":"E a parte boa: reduzir ou parar, principalmente em volta da cirurgia, melhora bastante as chances. Vale conversar com a equipe sobre isso antes."},
   {"k":"Passa adiante","sc":["Manda pra quem","vai operar e fuma."],"e":None,"sub":"Esse recado pode mudar um resultado.","cta":True,
    "vo":"Manda pra quem vai operar e ainda fuma. Esse recado pode mudar o resultado. E no próximo: quando quem destrói o osso é uma infecção."},
  ],
  "caption":cap_rec("Cigarro x consolidação óssea. Não é mito: a nicotina aperta os vasos e reduz o oxigênio e o sangue que chegam ao osso — e cicatrização depende disso. Quem fuma tem risco maior de pseudartrose, de infecção e de cura mais lenta. A boa notícia: reduzir ou parar, principalmente em volta da cirurgia, melhora bastante as chances. Vale conversar com sua equipe.","#tabagismo #consolidacaoossea")},

 {"id":"on_osteomielite","ep":7,"serie":"Osso Novo","temporada":"quando-o-osso-falha","motif_family":"bone",
  "scenes":[
   {"k":"Infecção no osso","sc":["O osso também","pega infecção."],"e":None,"sub":"Tem nome: osteomielite. E ela pode destruir osso.",
    "vo":"A gente pensa em infecção na pele, na garganta. Mas o osso também pega. Tem nome: osteomielite. Quando se instala, pode ir destruindo o osso por dentro."},
   {"k":"De onde vem","sc":["Fratura exposta,","cirurgia ou sangue."],"e":None,"sub":"Entra por uma ferida, num pós-operatório, ou pela corrente sanguínea.",
    "vo":"Ela pode entrar por uma fratura exposta, depois de uma cirurgia, ou até viajar pelo sangue de uma infecção em outro lugar do corpo."},
   {"k":"Sinais","sc":["Dor, calor,","vermelhidão, febre."],"e":None,"sub":"Dor persistente, inchaço, calor local, às vezes febre ou secreção.",
    "vo":"Os sinais costumam ser dor que não passa, inchaço, calor e vermelhidão no local, às vezes febre ou uma secreção. Não é pra ignorar."},
   {"k":"Tem tratamento","sc":["Limpar, tratar,","e às vezes refazer."],"e":None,"sub":"Antibiótico, retirada do osso doente e, às vezes, reconstrução.",
    "vo":"E tem caminho: tratar a infecção, remover o osso doente e, quando sobra um vão, reconstruir o que se perdeu. Sempre individualizado."},
   {"k":"Passa adiante","sc":["Salva: osso","infecciona — e trata."],"e":None,"sub":"Manda pra quem convive com uma ferida óssea que não fecha.","cta":True,
    "vo":"Salva e compartilha. E se a infecção levou um pedaço do osso embora, dá pra refazer? Dá. E o nome assusta: transporte ósseo. É o próximo."},
  ],
  "caption":cap_rec("Osteomielite: quando a infecção atinge o osso. Pode entrar por uma fratura exposta, num pós-operatório, ou viajar pelo sangue. Sinais comuns: dor persistente, inchaço, calor, vermelhidão, às vezes febre ou secreção. Tem tratamento: combater a infecção, remover o osso doente e, quando sobra um vão, reconstruir o que se perdeu — sempre individualizado.","#osteomielite #infeccaoossea")},

 {"id":"on_transporte_osseo","ep":8,"serie":"Osso Novo","temporada":"refazer-e-realinhar","motif_family":"bone",
  "scenes":[
   {"k":"Quando falta osso","sc":["Dá pra refazer osso","que se perdeu."],"e":None,"sub":"Faltou um pedaço grande? Há um caminho — longo, mas possível.",
    "vo":"Esse é um dos recursos mais poderosos da reconstrução. Quando falta um pedaço grande de osso, dá pra refazer movendo um segmento de osso vivo, bem devagar, pelo vão. É um processo longo, mas possível."},
   {"k":"Como funciona","sc":["Um pedaço desliza","e deixa osso atrás."],"e":None,"sub":"Atrás do segmento que avança, o corpo forma osso novo.",
    "vo":"Funciona assim: um pedaço do seu próprio osso vai sendo deslizado aos poucos pra dentro da falha. E atrás dele, naquele rastro, o corpo vai formando osso novo."},
   {"k":"De onde vem a ideia","sc":["O mesmo princípio","do milímetro."],"e":None,"sub":"É a osteogênese por distração aplicada a grandes perdas.",
    "vo":"É o mesmo princípio do milímetro por dia que a gente viu lá no começo, agora usado pra vencer perdas grandes de osso, depois de trauma ou infecção."},
   {"k":"Pra quê","sc":["Reconstruir o que","o trauma levou."],"e":None,"sub":"Devolver osso, comprimento e função — nunca estética.",
    "vo":"O objetivo é devolver osso, comprimento e função pra um membro que quase foi perdido. É reconstrução de função, nunca questão estética."},
   {"k":"Passa adiante","sc":["Salva: osso","perdido se refaz."],"e":None,"sub":"Manda pra quem acha que falta de osso não tem solução.","cta":True,
    "vo":"Salva e compartilha — é técnica e tempo, não promessa. E quando o osso não falta, mas está torto? É o próximo."},
  ],
  "caption":cap_rec("Transporte ósseo: refazer osso que se perdeu. Quando um trauma ou uma infecção leva um pedaço grande de osso, um segmento do próprio osso vivo é deslizado lentamente pelo vão — e atrás dele o corpo forma osso novo (a mesma osteogênese por distração). O objetivo é devolver osso, comprimento e função a um membro que quase foi perdido — num tratamento longo, em etapas. Reconstrução de função, nunca estética.","#transporteosseo #reconstrucao")},

 {"id":"on_osteotomia","ep":9,"serie":"Osso Novo","temporada":"refazer-e-realinhar","motif_family":"bone",
  "scenes":[
   {"k":"A palavra do dia","sc":["Osteotomia:","cortar pra alinhar."],"e":None,"sub":"Osteo = osso, tomia = corte. Um corte planejado pra corrigir o eixo.",
    "vo":"Osteotomia parece nome complicado, mas a tradução é direta: osteo é osso, tomia é corte. É um corte planejado no osso pra corrigir um alinhamento torto."},
   {"k":"Por que cortar","sc":["Osso torto","sobrecarrega tudo."],"e":None,"sub":"Um eixo errado joga peso a mais na articulação e desgasta cedo.",
    "vo":"Por que mexer num osso? Porque um osso fora de eixo joga carga demais num canto da articulação, e isso desgasta a cartilagem antes da hora."},
   {"k":"Como corrige","sc":["Corta, realinha","e fixa."],"e":None,"sub":"O osso é reposicionado no eixo certo e fixado pra cicatrizar assim.",
    "vo":"Na osteotomia, a gente corta, reposiciona no eixo certo e fixa pra ele cicatrizar já alinhado. É reorganizar a carga pra proteger a articulação."},
   {"k":"Pra quem","sc":["Sequela, deformidade","ou desgaste inicial."],"e":None,"sub":"Corrigir hoje pode adiar ou evitar problemas maiores depois.",
    "vo":"Costuma ajudar quem tem uma deformidade, uma sequela de fratura ou um desgaste começando. Corrigir o eixo agora pode poupar a articulação lá na frente."},
   {"k":"Passa adiante","sc":["Salva o que é","osteotomia."],"e":None,"sub":"Manda pra quem vive com a perna 'entortando'.","cta":True,
    "vo":"Guarda essa palavra. E no adulto, quando a perna inteira fica torta, também tem conserto? Tem. É o próximo."},
  ],
  "caption":cap_rec("Osteotomia: cortar o osso para realinhar. Osteo = osso, tomia = corte. Um osso fora de eixo joga carga demais num canto da articulação e a desgasta antes da hora. Na osteotomia, o osso é cortado, reposicionado no eixo certo e fixado para cicatrizar alinhado — reorganizando a carga. Costuma ajudar em deformidades, sequelas de fratura e desgaste inicial.","#osteotomia #alinhamento")},

 {"id":"on_perna_torta_adulto","ep":10,"serie":"Osso Novo","temporada":"refazer-e-realinhar","motif_family":"bone",
  "scenes":[
   {"k":"No adulto também","sc":["Perna torta não","é só de criança."],"e":None,"sub":"Sequela, doença ou desgaste — o eixo do adulto também corrige.",
    "vo":"Lá no Pé no Chão a gente falou da perna torta da criança, que costuma alinhar sozinha. No adulto é outra história: quando entorta, não se ajeita sozinho. Mas corrige."},
   {"k":"De onde vem","sc":["Fratura mal","consolidada, doença, desgaste."],"e":None,"sub":"Fratura que colou torta, sequelas antigas ou artrose que desalinha.",
    "vo":"No adulto costuma vir de uma fratura que colou torta, de alguma sequela antiga, ou de um desgaste que vai desalinhando a perna com o tempo."},
   {"k":"Por que tratar","sc":["Joelho e quadril","pagam a conta."],"e":None,"sub":"A perna fora de eixo sobrecarrega articulações e dói.",
    "vo":"E por que corrigir? Porque uma perna fora de prumo sobrecarrega joelho e quadril, dói e desgasta. Endireitar o eixo alivia essa conta."},
   {"k":"Como","sc":["Osteotomia, às vezes","com fixador."],"e":None,"sub":"Realinhar o osso, às vezes de forma gradual, devolvendo o eixo.",
    "vo":"O caminho costuma ser uma osteotomia pra realinhar, às vezes de forma gradual com um aparelho, devolvendo o eixo certo pra perna."},
   {"k":"Passa adiante","sc":["Manda pra quem vive","com a perna torta."],"e":None,"sub":"No adulto, eixo torto tem correção.","cta":True,
    "vo":"Manda pra quem convive com uma perna torta achando que não tem jeito. E quando uma perna fica mais curta que a outra? É o próximo."},
  ],
  "caption":cap_rec("Perna torta no adulto. Diferente da criança (que costuma alinhar sozinha), no adulto a perna torta não se ajeita só — mas corrige. Costuma vir de uma fratura que colou torta, de sequelas antigas ou de desgaste. Importa porque um eixo errado sobrecarrega joelho e quadril, dói e desgasta. O caminho costuma ser a osteotomia para realinhar, às vezes de forma gradual, devolvendo o eixo.","#deformidade #osteotomia")},

 {"id":"on_discrepancia","ep":11,"serie":"Osso Novo","temporada":"refazer-e-realinhar","motif_family":"bone",
  "scenes":[
   {"k":"Recebendo a ponte","sc":["Uma perna mais","curta que a outra."],"e":None,"sub":"Na criança a gente acompanha; no adulto, mede e corrige.",
    "vo":"Essa conversa começou lá na criança, no Pé no Chão. No adulto, quando sobra uma diferença real entre as pernas, a gente não espera crescer: mede e planeja a correção."},
   {"k":"Por que incomoda","sc":["Manca, dói a","coluna e o quadril."],"e":None,"sub":"Diferenças maiores mudam a marcha e sobrecarregam coluna e quadril.",
    "vo":"Diferenças pequenas a gente nem sente. Mas, a partir de certo ponto, começa a mancar, e isso sobrecarrega coluna, quadril e joelho com o tempo."},
   {"k":"De onde vem","sc":["Fratura, infecção","ou de nascença."],"e":None,"sub":"Sequela de fratura, infecção antiga ou diferença congênita.",
    "vo":"Pode vir de uma fratura que afetou o crescimento, de uma infecção antiga, ou ser de nascença que persistiu até a vida adulta."},
   {"k":"Tem correção","sc":["Compensar, frear","ou alongar."],"e":None,"sub":"Da palmilha ao alongamento (casos selecionados) — função e marcha, nunca altura.",
    "vo":"E o leque de soluções é grande: vai de uma palmilha que compensa, até alongar o osso mais curto, em casos selecionados. Sempre pra equilibrar a marcha e a função, nunca uma questão de altura."},
   {"k":"Passa adiante","sc":["Salva: perna curta","tem escada de soluções."],"e":None,"sub":"Manda pra quem manca e nunca mediu.","cta":True,
    "vo":"Salva e compartilha. Mas antes de corrigir qualquer coisa, tem um passo que ninguém pula: medir direito. É o próximo."},
  ],
  "caption":cap_rec("Uma perna mais curta que a outra, no adulto. Diferenças pequenas nem se sentem; a partir de certo ponto, começa a mancar e a sobrecarregar coluna, quadril e joelho. Pode vir de fratura, infecção antiga ou ser congênita. As soluções formam uma escada: da palmilha que compensa até o alongamento do osso mais curto, em casos selecionados — sempre para equilibrar marcha e função, nunca uma questão de altura.","#discrepancia #marcha")},

 {"id":"on_medir_antes","ep":12,"serie":"Osso Novo","temporada":"os-caminhos-do-conserto","motif_family":"bone",
  "scenes":[
   {"k":"O passo que ninguém pula","sc":["Medir vem antes","de corrigir."],"e":"antes","sub":"Sem medida exata, não dá pra escolher o tratamento certo.",
    "vo":"Antes de qualquer correção, vem a medida. Parece óbvio, mas é o passo que decide tudo: sem saber o tamanho exato da diferença, não dá pra escolher o caminho certo."},
   {"k":"Como mede","sc":["Exame de imagem,","no milímetro."],"e":None,"sub":"A escanometria mede o comprimento real de cada osso.",
    "vo":"A medida é feita com exame de imagem, a escanometria, que mostra no milímetro o comprimento real de cada osso. Não é no olho, nem na fita métrica."},
   {"k":"Por que tão exato","sc":["Cada milímetro","muda o plano."],"e":None,"sub":"Compensar, frear o crescimento ou alongar depende da medida.",
    "vo":"Por que tanta exatidão? Porque cada faixa de milímetros aponta pra uma solução diferente. A medida é o mapa do tratamento."},
   {"k":"Na criança muda","sc":["Mede e remede","enquanto cresce."],"e":None,"sub":"Na criança, a previsão considera o quanto ainda vai crescer.",
    "vo":"E na criança tem um detalhe a mais: como ela ainda cresce, a gente mede e remede ao longo do tempo, prevendo a diferença lá no final do crescimento."},
   {"k":"Passa adiante","sc":["Salva: medir","é metade do tratamento."],"e":None,"sub":"Manda pra quem vai investigar uma diferença nas pernas.","cta":True,
    "vo":"Salva isso: medir é metade do tratamento. E com o quê se segura o osso pra corrigir? É o próximo."},
  ],
  "caption":cap_rec("Discrepância: medir antes de corrigir. Sem a medida exata, não há como escolher o tratamento. A escanometria (exame de imagem) mostra no milímetro o comprimento real de cada osso — não é no olho nem na fita métrica. Cada faixa de milímetros aponta para uma solução diferente. Na criança, mede-se e remede-se ao longo do tempo, prevendo a diferença no final do crescimento. Corrigir, aqui, é sempre sobre função e marcha — nunca estética ou altura.","#escanometria #discrepancia")},

 {"id":"on_fixador_vs_haste","ep":13,"serie":"Osso Novo","temporada":"os-caminhos-do-conserto","motif_family":"bone",
  "scenes":[
   {"k":"A ferramenta principal","sc":["O fixador externo,","por fora do osso."],"e":None,"sub":"A estrutura que segura e alonga o osso no ritmo certo — e a mais acessível.",
    "vo":"Pra alongar ou reconstruir um osso, é preciso uma estrutura que o segure no ritmo certo. A principal, e de longe a mais acessível, é o fixador externo."},
   {"k":"Como funciona","sc":["Pinos até o osso,","ajuste por fora."],"e":None,"sub":"Permite corrigir aos poucos, com precisão, ao longo do tratamento.",
    "vo":"São pinos que atravessam até o osso, presos numa estrutura por fora. Isso permite ir ajustando a correção aos pouquinhos, com precisão, ao longo do tratamento."},
   {"k":"E a haste por dentro?","sc":["Existe — mas não é","opção de prateleira."],"e":None,"sub":"Fica dentro do osso; é de custo muito alto e acesso restrito, p/ casos específicos.",
    "vo":"Você talvez tenha ouvido falar das hastes que ficam dentro do osso, algumas até motorizadas. Elas existem, mas são de custo altíssimo e acesso restrito. Não é uma opção de prateleira, e serve pra situações específicas."},
   {"k":"O que decide","sc":["A indicação — e a","realidade de cada um."],"e":None,"sub":"Estado do osso, tipo de correção e a realidade de custo e acesso pesam juntos.",
    "vo":"Por isso não dá pra tratar como uma escolha de menu. O que decide é a indicação pro seu caso, junto com a realidade de custo e de acesso. A equipe pondera o que é seguro e viável pra você."},
   {"k":"Passa adiante","sc":["Salva: a real do","fixador externo."],"e":None,"sub":"O foco é função e o que é viável — nunca vitrine, estética ou altura.","cta":True,
    "vo":"Salva e compartilha. O foco é sempre devolver função, com o que é viável e seguro, nunca estética. E a pergunta número um de quem vai operar: quanto tempo fico com isso? É o próximo."},
  ],
  "caption":cap_rec("Como o osso é segurado para alongar ou reconstruir. A ferramenta principal — e de longe a mais acessível — é o fixador externo: pinos até o osso presos numa estrutura por fora, que permite ajustar a correção aos poucos, com precisão. Existem também hastes internas (algumas motorizadas), mas são de custo muito alto e acesso restrito, para indicações específicas — não são uma opção de prateleira. O que decide não é 'a melhor', e sim a indicação somada à realidade de custo e acesso de cada pessoa. O foco é sempre função e o que é viável — nunca estética ou altura.","#fixadorexterno #reconstrucaoossea")},

 {"id":"on_quanto_tempo","ep":14,"serie":"Osso Novo","temporada":"os-caminhos-do-conserto","motif_family":"bone",
  "scenes":[
   {"k":"A pergunta nº1","sc":["Quanto tempo fico","com o fixador?"],"e":None,"sub":"A resposta honesta começa com: depende do quanto se corrige.",
    "vo":"É quase sempre a primeira pergunta: quanto tempo eu vou ficar com esse aparelho? A resposta honesta começa com depende, mas dá pra entender a lógica."},
   {"k":"A conta básica","sc":["Quanto maior a","correção, mais tempo."],"e":None,"sub":"Lembra do milímetro por dia? O alvo define a fase de distração.",
    "vo":"Lembra do milímetro por dia? Então: quanto maior a diferença a corrigir, mais dias afastando. Essa parte dá pra estimar pela conta."},
   {"k":"O que pesa mais","sc":["A consolidação","leva o maior tempo."],"e":None,"sub":"Depois de afastar, o osso ainda precisa endurecer — e isso não se apressa.",
    "vo":"Mas o que costuma levar mais tempo é a consolidação: depois de afastar, o osso ainda precisa amadurecer e endurecer. E essa parte não dá pra apressar."},
   {"k":"Varia por pessoa","sc":["Cada osso tem","seu ritmo."],"e":None,"sub":"Idade, saúde, tabagismo e nutrição mudam a velocidade.",
    "vo":"E varia de pessoa pra pessoa: idade, saúde, alimentação e o cigarro mudam a velocidade. Por isso o acompanhamento é de perto, com imagem, até liberar."},
   {"k":"Passa adiante","sc":["Salva: o tempo","tem lógica."],"e":None,"sub":"Manda pra quem está nessa contagem.","cta":True,
    "vo":"Salva pra entender a contagem. E no dia a dia com o aparelho, um cuidado decide tudo: os pinos. É o próximo."},
  ],
  "caption":cap_rec("Quanto tempo fico com o fixador? A resposta honesta é 'depende', mas tem lógica. Quanto maior a correção, mais dias na fase de afastamento (o 1 mm por dia). O que costuma levar mais tempo, porém, é a consolidação — o osso ainda precisa amadurecer e endurecer, e isso não se apressa. Idade, saúde, nutrição e tabagismo mudam a velocidade; por isso o acompanhamento é de perto, com imagem. O foco é sempre devolver função — nunca estética ou altura.","#fixadorexterno #recuperacao")},

 {"id":"on_cuidado_pinos","ep":15,"serie":"Osso Novo","temporada":"viver-o-tratamento","motif_family":"bone",
  "scenes":[
   {"k":"O cuidado-chave","sc":["No fixador, tudo","gira nos pinos."],"e":None,"sub":"Onde o pino encontra a pele é o ponto que mais pede atenção.",
    "vo":"Quem usa fixador externo aprende rápido: o cuidado mais importante do dia a dia é com os pinos, ali onde eles encontram a pele."},
   {"k":"Por quê","sc":["É a porta de","entrada da pele."],"e":None,"sub":"Pele e metal convivem ali; a limpeza certa evita irritação e infecção.",
    "vo":"Por quê? Porque ali a pele e o metal convivem o tempo todo. É uma porta que, mal cuidada, pode irritar ou infeccionar. Bem cuidada, passa tranquila."},
   {"k":"A rotina","sc":["Limpeza simples","e constante."],"e":None,"sub":"Higiene orientada pela equipe, sem fórmulas mirabolantes.",
    "vo":"A rotina costuma ser simples: uma limpeza orientada pela equipe, feita com regularidade. Nada de receita caseira mirabolante. O constante é o que protege."},
   {"k":"Sinais de alerta","sc":["Vermelhidão, dor","ou secreção nova."],"e":None,"sub":"Aumento de dor, vermelhidão ou secreção pede contato com a equipe.",
    "vo":"E fica de olho nos sinais: se um pino começa a doer mais, avermelhar ou soltar secreção, é hora de avisar a equipe. Cedo, resolve fácil."},
   {"k":"Passa adiante","sc":["Salva a rotina","dos pinos."],"e":None,"sub":"Manda pra quem está com fixador agora.","cta":True,
    "vo":"Salva e manda pra quem está com fixador agora. Mas quem decide o resultado final não é só o cirurgião. É o próximo."},
  ],
  "caption":cap_rec("Cuidado com os pinos do fixador externo. O ponto mais importante do dia a dia é onde o pino encontra a pele — ali pele e metal convivem, e é a 'porta' que pode irritar ou infeccionar. A rotina costuma ser uma limpeza simples e constante, orientada pela equipe (nada de receita caseira). Fique atento a aumento de dor, vermelhidão ou secreção nova: avisar cedo resolve fácil.","#fixadorexterno #cuidados")},

 {"id":"on_fisioterapia","ep":16,"serie":"Osso Novo","temporada":"viver-o-tratamento","motif_family":"bone",
  "scenes":[
   {"k":"A metade esquecida","sc":["A cirurgia é","metade do caminho."],"e":"metade","sub":"A outra metade do resultado se constrói na reabilitação.",
    "vo":"Tem uma verdade que pouca gente fala: a cirurgia é só metade do caminho. A outra metade, quem constrói é você, na reabilitação."},
   {"k":"Por que tão importante","sc":["Osso novo precisa","de movimento e carga."],"e":None,"sub":"Articulação, músculo e o próprio osso respondem ao estímulo certo.",
    "vo":"Osso novo e articulação não gostam de ficar parados. O movimento e a carga, na dose certa, mantêm a articulação solta e estimulam o osso a ficar forte."},
   {"k":"O risco de pular","sc":["Parar trava","a articulação."],"e":None,"sub":"Sem reabilitação, a rigidez pode roubar o ganho da cirurgia.",
    "vo":"Quem pula essa parte corre o risco da articulação enrijecer e do músculo encolher. Aí a rigidez rouba parte do ganho que a cirurgia deu. Seria uma pena."},
   {"k":"O combinado","sc":["Constância vence","intensidade."],"e":None,"sub":"Pouco e todo dia, guiado pela equipe, supera surtos isolados.",
    "vo":"E o segredo não é treino pesado: é constância. Um pouco todo dia, guiado pela equipe, rende muito mais do que surtos isolados de esforço."},
   {"k":"Passa adiante","sc":["Salva: reabilitar","é metade do resultado."],"e":None,"sub":"Manda pra quem está no pós e desanimou.","cta":True,
    "vo":"Salva e manda pra quem está no pós-operatório e desanimou. E quando tudo isso se junta pra reconstruir uma perna depois de um trauma grave? É o próximo."},
  ],
  "caption":cap_rec("Por que a reabilitação decide o resultado. A cirurgia é metade do caminho; a outra metade se constrói na fisioterapia. Osso novo e articulação não gostam de ficar parados — movimento e carga na dose certa mantêm a articulação solta e fortalecem o osso. Pular essa parte arrisca rigidez e perda de músculo, que roubam o ganho da cirurgia. O segredo não é treino pesado: é constância, guiada pela equipe.","#fisioterapia #reabilitacao")},

 {"id":"on_pos_trauma","ep":17,"serie":"Osso Novo","temporada":"viver-o-tratamento","motif_family":"bone",
  "scenes":[
   {"k":"Tudo junto","sc":["Reconstruir uma","perna inteira."],"e":None,"sub":"Quando o trauma grave leva osso, eixo e comprimento de uma vez.",
    "vo":"Às vezes um acidente grave leva tudo de uma vez: pedaço de osso, alinhamento e comprimento. Reconstruir uma perna assim é juntar tudo o que a gente viu até aqui."},
   {"k":"O quebra-cabeça","sc":["Estabilizar, refazer,","alinhar, igualar."],"e":None,"sub":"Controlar infecção, transportar osso, corrigir eixo e comprimento — por etapas.",
    "vo":"É um quebra-cabeça por etapas: primeiro estabilizar e controlar infecção, depois refazer o osso que faltou, alinhar o eixo e igualar o comprimento. Cada peça no seu tempo."},
   {"k":"Leva tempo","sc":["É uma maratona,","não uma corrida."],"e":None,"sub":"São meses, com altos e baixos — e equipe junto o caminho todo.",
    "vo":"Não é rápido, e não é reto. É uma maratona de meses, com altos e baixos, em que a equipe caminha junto. Saber disso desde o começo ajuda a atravessar."},
   {"k":"O objetivo","sc":["Voltar a apoiar","e andar."],"e":None,"sub":"A meta é função: pisar, sustentar o peso, voltar a viver — não estética.",
    "vo":"E a meta no fim é sempre a mesma: voltar a apoiar o pé, sustentar o peso e retomar a vida. É sobre função e movimento, nunca sobre aparência."},
   {"k":"Passa adiante","sc":["Salva: perna","grave se reconstrói."],"e":None,"sub":"Manda pra quem precisa de esperança baseada em técnica.","cta":True,
    "vo":"Salva e compartilha essa esperança, que é técnica, não promessa. E por que nada disso aqui é sobre estética? É o fecho da série."},
  ],
  "caption":cap_rec("Reconstruir uma perna depois de um trauma grave. Quando um acidente leva osso, alinhamento e comprimento de uma vez, a reconstrução junta tudo: estabilizar e controlar infecção, refazer o osso que faltou, alinhar o eixo e igualar o comprimento — por etapas, cada peça no seu tempo. É uma maratona de meses, com a equipe junto. A meta é sempre função: voltar a apoiar o pé e andar. Nunca estética.","#reconstrucaoossea #trauma")},

 {"id":"on_nao_estetica","ep":18,"serie":"Osso Novo","temporada":"viver-o-tratamento","motif_family":"bone",
  "scenes":[
   {"k":"O fecho da série","sc":["Reconstrução não","é estética."],"e":"não","sub":"Alongar e corrigir osso aqui é sobre função — nunca altura.","motif":"no",
    "vo":"Pra fechar a série, o ponto mais importante de todos. Tudo o que a gente falou, alongar, transportar, corrigir osso, é sobre função. Nunca sobre estética ou altura."},
   {"k":"A diferença","sc":["Devolver o que a","doença levou."],"e":None,"sub":"Trauma, infecção, deformidade e sequela tiraram função; o objetivo é devolver.",
    "vo":"A diferença é o porquê. Aqui a gente parte de um osso que o trauma, a infecção ou uma deformidade machucaram. O objetivo é devolver o que foi perdido, não buscar um padrão."},
   {"k":"Por que isso importa","sc":["É cirurgia séria,","com indicação séria."],"e":None,"sub":"Toda reconstrução tem riscos e tempo; indica-se por necessidade de função.",
    "vo":"Isso importa porque é cirurgia de verdade, com tempo e riscos reais. Ela se justifica por uma necessidade de função: de andar, de apoiar, de viver melhor."},
   {"k":"O nosso compromisso","sc":["Osso novo, de","volta ao movimento."],"e":None,"sub":"O lema da série diz tudo: o foco é o movimento de volta.",
    "vo":"É por isso que o lema da série é esse: osso novo, de volta ao movimento. O movimento de volta é sempre o destino."},
   {"k":"Passa adiante","sc":["Salva e compartilha","a série inteira."],"e":None,"sub":"Manda pra quem precisa entender que reconstrução é função.","cta":True,
    "vo":"Salva e manda pra quem precisa entender isso. É sobre voltar a andar. E se você chegou agora, a série recomeça do começo: o osso cresce no espaço vazio."},
  ],
  "caption":cap_rec("Reconstrução NÃO é estética. Tudo o que esta série mostrou — alongar, transportar e corrigir osso — é sobre função: parte de um osso que o trauma, a infecção ou uma deformidade machucaram, e busca devolver o que foi perdido, nunca um padrão de aparência ou altura. É cirurgia séria, com tempo e riscos reais, indicada por necessidade de função. Por isso o lema: osso novo, de volta ao movimento.","#reconstrucaoossea #funcao")},
]

# ───────────────────────────── SÉRIE "PÉ NO CHÃO" — 12 NOVOS ─────────────────────────────
PE_NO_CHAO_NOVOS = [
 {"id":"pnc_marcos_andar","ep":9,"serie":"Pé no Chão","temporada":"pernas-e-pes",
  "scenes":[
   {"k":"A pergunta de todo pai","sc":["Quando é pra","andar?"],"e":None,"sub":"Existe uma faixa normal — e uma linha que liga o alerta.",
    "vo":"Quando meu filho devia estar andando? Essa angústia é de quase todo pai e mãe. E a boa notícia é que existe uma faixa larga de normal."},
   {"k":"A faixa normal","sc":["Entre 9 e 18","meses, em geral."],"e":None,"sub":"Cada criança tem seu tempo dentro dessa janela.",
    "vo":"A maioria das crianças dá os primeiros passos entre nove e dezoito meses. É uma janela bem ampla, então um pouco antes ou depois costuma estar tudo certo."},
   {"k":"Não compare","sc":["O vizinho andou","antes? Tudo bem."],"e":None,"sub":"Comparar gera ansiedade à toa; o ritmo é individual.",
    "vo":"E aquela comparação com o filho do vizinho que andou cedo? Solta isso. Cada criança tem o seu ritmo, e andar antes não é sinal de nada melhor."},
   {"k":"A linha do alerta","sc":["Sem andar aos","18 meses: avalie."],"e":None,"sub":"Não andar até ~18 meses, ou perder algo já conquistado, pede avaliação.",
    "vo":"A linha que vale guardar: se passou dos dezoito meses e ela ainda não anda, ou se perdeu algo que já fazia, aí vale uma avaliação. Sem pânico, só atenção."},
   {"k":"Passa adiante","sc":["Salva a janela","do primeiro passo."],"e":None,"sub":"Manda pra quem está ansioso esperando o primeiro passo.","cta":True,
    "vo":"Salva essa janela e manda pra quem está no aperto esperando o primeiro passo. E quando ela anda, mas com o pé virado pra dentro? É o próximo."},
  ],
  "caption":cap_ped("Marcos do andar: quando se preocupar. A maioria das crianças dá os primeiros passos entre 9 e 18 meses — janela ampla, então um pouco antes ou depois costuma ser normal. Comparar com outras crianças só gera ansiedade: o ritmo é individual. A linha de alerta: não andar até por volta dos 18 meses, ou perder uma habilidade já conquistada, merece avaliação.","#primeirospassos #desenvolvimentoinfantil")},

 {"id":"pnc_pe_pra_dentro","ep":10,"serie":"Pé no Chão","temporada":"pernas-e-pes",
  "scenes":[
   {"k":"Pé pra dentro","sc":["Anda com o pé","virado pra dentro?"],"e":None,"sub":"Tem nome, tem idade e quase sempre tem final feliz.",
    "vo":"Aquela criança que anda meio de pombinho, com os pés virados pra dentro, assusta os pais. Mas isso tem explicação, tem idade certa e quase sempre se resolve sozinho."},
   {"k":"De onde vem","sc":["Do pé, da canela","ou do quadril."],"e":None,"sub":"Uma leve torção do pé, da perna ou do fêmur — todas comuns.",
    "vo":"Esse jeito de andar pode vir de uma curvinha no pé, de uma leve torção da canela ou do osso da coxa. Todas são variações comuns do crescimento."},
   {"k":"A regra do tempo","sc":["A maioria alinha","com os anos."],"e":None,"sub":"Conforme cresce, a rotação dos ossos costuma se ajustar sozinha.",
    "vo":"E a regra é o tempo: conforme a criança cresce, a rotação desses ossos vai se ajustando naturalmente. A maioria alinha sem precisar de nada."},
   {"k":"Quando avaliar","sc":["Só um lado, dói,","ou piora."],"e":None,"sub":"Assimetria, dor, quedas demais ou piora progressiva pedem avaliação.","motif":None,
    "vo":"O alerta é quando é só de um lado, quando dói, quando ela cai muito mais que o esperado, ou quando piora em vez de melhorar. Aí vale o ortopedista olhar."},
   {"k":"Passa adiante","sc":["Salva: pé pra","dentro costuma alinhar."],"e":None,"sub":"Manda pra mãe preocupada com o 'andar de pombinho'.","cta":True,
    "vo":"Salva e manda pra aquela mãe preocupada com o andar de pombinho. E aquele estalo no joelho da criança, é grave? É o próximo."},
  ],
  "caption":cap_ped("Pé virado para dentro ao andar (o 'andar de pombinho'). Pode vir de uma leve torção do pé, da canela ou do osso da coxa — todas variações comuns do crescimento. A regra é o tempo: conforme a criança cresce, a rotação costuma se ajustar sozinha. O alerta é quando ocorre só de um lado, dói, causa quedas demais, ou piora em vez de melhorar.","#marcha #desenvolvimento")},

 {"id":"pnc_estalo_joelho","ep":11,"serie":"Pé no Chão","temporada":"pernas-e-pes",
  "scenes":[
   {"k":"Aquele 'crec'","sc":["O joelho da criança","estala?"],"e":None,"sub":"Som sem dor quase sempre é inofensivo — eu te explico.",
    "vo":"Sabe aquele crec no joelho quando a criança dobra a perna? Pais ficam aflitos. Mas estalo sem dor, na imensa maioria, é totalmente inofensivo."},
   {"k":"Por que estala","sc":["Tendão, articulação,","bolha de ar."],"e":None,"sub":"Tendões deslizando, gás dentro da articulação — fenômenos normais.",
    "vo":"O barulho costuma ser tendão deslizando sobre o osso ou bolhinhas de gás se formando dentro da articulação. Fenômenos normais, que o corpo todo faz."},
   {"k":"O que tranquiliza","sc":["Sem dor e sem","inchaço: relaxa."],"e":None,"sub":"Se ela brinca, corre e não reclama, o estalo é só som.",
    "vo":"O que tranquiliza é o conjunto: se ela corre, pula e brinca sem reclamar, e não tem inchaço, esse estalo é só barulho. Pode relaxar."},
   {"k":"Quando olhar de perto","sc":["Estala e dói,","trava ou incha."],"e":None,"sub":"Estalo com dor, travamento ou inchaço merece avaliação.","motif":None,
    "vo":"O sinal de atenção é quando o estalo vem junto de dor, de inchaço, ou quando o joelho trava no meio do movimento. Aí, sim, vale investigar."},
   {"k":"Passa adiante","sc":["Salva: estalo sem","dor é normal."],"e":None,"sub":"Manda pra quem se assusta com o joelho que estala.","cta":True,
    "vo":"Salva e manda pra quem se assusta com o joelho que estala. E será que tênis caro corrige o pé da criança? Spoiler: não. É o próximo."},
  ],
  "caption":cap_ped("Estalo no joelho da criança. Estalo SEM dor é, na imensa maioria, inofensivo: costuma ser tendão deslizando sobre o osso ou bolhas de gás dentro da articulação — fenômenos normais. O que tranquiliza é o conjunto: se ela corre, pula e brinca sem reclamar e sem inchaço, é só som. Acenda o alerta quando o estalo vem com dor, inchaço ou travamento do joelho.","#joelho #criancas")},

 {"id":"pnc_tenis_caro","ep":12,"serie":"Pé no Chão","temporada":"pernas-e-pes",
  "scenes":[
   {"k":"Mito caro","sc":["Tênis caro NÃO","corrige o pé."],"e":"NÃO","sub":"O pé da criança não se molda pelo calçado — eu explico.","motif":"no",
    "vo":"Vou economizar seu dinheiro: tênis caro, dito ortopédico, não corrige nem molda o pé da criança. Essa ideia vende muito, mas o pé não funciona assim."},
   {"k":"Como o pé se forma","sc":["Andando, correndo,","sentindo o chão."],"e":None,"sub":"O arco e a musculatura se desenvolvem com movimento, não com solado.",
    "vo":"O pé se forma com o uso: andando, correndo, subindo, sentindo o chão. É o movimento que desenvolve o arco e a musculatura, não um solado especial."},
   {"k":"O que o calçado faz","sc":["Protege. Só isso.","E está ótimo."],"e":None,"sub":"O papel do sapato é proteger; flexível e do tamanho certo basta.",
    "vo":"O papel do sapato é proteger o pé de machucado e do frio. Só isso, e já é muito. Um calçado flexível, leve e no tamanho certo cumpre o trabalho."},
   {"k":"A dica que vale","sc":["Pé no chão,","quando der."],"e":None,"sub":"Tempo descalço em casa, em piso seguro, estimula o pé de verdade.",
    "vo":"E a dica que de fato ajuda não custa nada: deixar a criança um tempo descalça em casa, num chão seguro. Isso, sim, estimula o pé de verdade."},
   {"k":"Passa adiante","sc":["Salva antes de","gastar no tênis."],"e":None,"sub":"Manda pra quem vai gastar caro achando que corrige.","cta":True,
    "vo":"Salva antes de gastar caro com a promessa de corrigir. E se uma perna da criança for mais curta que a outra? É o próximo, e ele faz uma ponte."},
  ],
  "caption":cap_ped("Tênis caro NÃO molda nem corrige o pé da criança. O arco e a musculatura se desenvolvem com o movimento — andando, correndo, sentindo o chão — não com um solado especial. O papel do calçado é proteger: flexível, leve e no tamanho certo já basta. A dica que de fato ajuda não custa nada: tempo descalço em casa, em piso seguro.","#pechato #calcadoinfantil")},

 {"id":"pnc_perna_curta_crianca","ep":13,"serie":"Pé no Chão","temporada":"pernas-e-pes",
  "scenes":[
   {"k":"A ponte","sc":["Uma perna mais","curta que a outra."],"e":None,"sub":"Na criança a história é diferente da do adulto — e se conecta.",
    "vo":"Esse tema costura os dois mundos do perfil. Uma perna mais curta na criança é bem diferente da do adulto, mas conversa com ela."},
   {"k":"Pequena é comum","sc":["Diferença mínima","quase todo mundo tem."],"e":None,"sub":"Diferenças bem pequenas são comuns e não dão sintoma.",
    "vo":"Primeiro, calma: uma diferença pequenininha entre as pernas quase todo mundo tem, e não causa problema nenhum. O corpo lida bem com isso."},
   {"k":"O diferencial da criança","sc":["Ela ainda","está crescendo."],"e":"crescendo","sub":"Como cresce, dá pra prever a diferença final e planejar com tempo.",
    "vo":"O que muda na criança é o trunfo do crescimento. Como ela ainda vai crescer, dá pra prever a diferença lá no final e, se precisar, planejar a correção com calma."},
   {"k":"Quando observar","sc":["Manca, ou a","diferença é visível."],"e":None,"sub":"Mancar, desnível no quadril ou diferença nítida pede avaliação.",
    "vo":"Vale avaliar quando ela manca, quando o quadril fica num desnível, ou quando a diferença é nítida ao olhar. Medir cedo abre as melhores opções."},
   {"k":"Passa adiante","sc":["A versão adulta","está na série Osso Novo."],"e":None,"sub":"Na criança a gente acompanha; no adulto, mede e corrige.","cta":True,
    "vo":"Na criança a gente acompanha o crescimento. No adulto, vira outra história, que eu conto na série Osso Novo. Mas e a dor nas pernas à noite, é sempre crescimento? É o próximo."},
  ],
  "caption":cap_ped("Uma perna mais curta que a outra, na criança. Calma: uma diferença bem pequena quase todo mundo tem, e não dá sintoma. O trunfo da infância é o crescimento — como a criança ainda cresce, dá para prever a diferença no final e planejar com tempo, se preciso. Vale avaliar quando ela manca, quando há desnível no quadril ou a diferença é nítida. (A versão adulta está na série Osso Novo.)","#discrepancia #criancas")},

 {"id":"pnc_nao_dor_crescimento","ep":14,"serie":"Pé no Chão","temporada":"sinais-de-alerta",
  "scenes":[
   {"k":"O outro lado","sc":["Nem toda dor é","de crescimento."],"e":None,"sub":"Já falamos do padrão que acalma; agora, o que NÃO é.",
    "vo":"A gente já falou do padrão tranquilo da dor de crescimento. Agora o complemento importante: os sinais de que aquela dor pode ser outra coisa."},
   {"k":"Sinal 1","sc":["Sempre no","mesmo ponto."],"e":None,"sub":"Dor de crescimento é difusa; dor fixa num lugar pede atenção.",
    "vo":"O primeiro sinal é a localização. Dor de crescimento é espalhada, vaga. Quando a dor mira sempre o mesmo pontinho, isso foge do padrão."},
   {"k":"Sinais 2 e 3","sc":["Inchaço, calor","ou febre junto."],"e":None,"sub":"Articulação inchada, quente, ou febre não combinam com dor de crescimento.",
    "vo":"O segundo e o terceiro: inchaço e calor numa articulação, ou febre junto da dor. Nada disso faz parte da dor de crescimento clássica."},
   {"k":"Sinal 4","sc":["Atrapalha o dia,","não só a noite."],"e":None,"sub":"Dor que faz mancar, acorda toda noite ou limita o brincar: avalie.",
    "vo":"E o quarto: quando a dor sai da noite e invade o dia, fazendo a criança mancar, evitar brincar ou acordar sempre. Aí não é pra esperar, é pra avaliar."},
   {"k":"Passa adiante","sc":["Salva os sinais","que fogem do padrão."],"e":None,"sub":"Manda pra quem fica na dúvida toda noite.","cta":True,
    "vo":"Salva esses sinais de alerta e compartilha. E tem um deles que nunca dá pra ignorar sozinho: mancar. É o próximo."},
  ],
  "caption":cap_ped("Os sinais de que NÃO é dor de crescimento. A dor de crescimento clássica é difusa, nas duas pernas, à noite, sem inchaço, e some pela manhã. Fogem desse padrão e merecem avaliação: dor sempre no MESMO ponto; inchaço, calor ou febre junto; e dor que invade o dia, fazendo mancar, limitar o brincar ou acordar sempre. Na dúvida, avalie.","#dordecrescimento #sinaisdealerta")},

 {"id":"pnc_mancando","ep":15,"serie":"Pé no Chão","temporada":"sinais-de-alerta",
  "scenes":[
   {"k":"Regra de ouro","sc":["Criança mancando","sempre se avalia."],"e":"sempre","sub":"Manqueira não é manha — é um sinal que pede explicação.",
    "vo":"Essa é uma regra de ouro da ortopedia infantil: criança mancando sempre merece ser avaliada. Manqueira não é manha nem birra, é o corpo avisando algo."},
   {"k":"Por que levar a sério","sc":["O corpo está","protegendo algo."],"e":None,"sub":"Mancar é o jeito de fugir de uma dor ou de uma fraqueza.",
    "vo":"A criança manca pra fugir de uma dor ou pra compensar uma fraqueza. Ou seja: por trás da manqueira tem sempre um motivo que vale a pena entender."},
   {"k":"As causas mudam","sc":["Depende muito","da idade."],"e":None,"sub":"De um calçado apertado a quadril ou joelho que pedem mais pressa.",
    "vo":"As causas variam bastante com a idade: pode ser algo bobo, como um sapato apertado ou um machucado no pé, até questões no quadril ou no joelho que pedem mais pressa."},
   {"k":"O que observar","sc":["Há quanto tempo,","e com o quê."],"e":None,"sub":"Tempo de manqueira, dor, febre e o lado ajudam muito o médico.",
    "vo":"O que ajuda o médico: há quanto tempo está mancando, se tem dor, se veio febre junto, e se é sempre do mesmo lado. Repare nisso antes da consulta."},
   {"k":"Passa adiante","sc":["Salva: mancar","sempre se investiga."],"e":None,"sub":"Manda pra quem acha que vai passar sozinho.","cta":True,
    "vo":"Salva essa regra e manda pra quem acha que a manqueira passa sozinha. E quando ela vem junto com febre? Aí o relógio aperta. É o próximo."},
  ],
  "caption":cap_ped("Criança mancando: regra de ouro, sempre se avalia. Manqueira não é manha — é o corpo protegendo algo, fugindo de uma dor ou compensando uma fraqueza. As causas mudam com a idade, de um sapato apertado a questões no quadril ou joelho que pedem mais pressa. Ajuda o médico observar: há quanto tempo, se há dor, se veio febre e se é sempre do mesmo lado.","#manqueira #sinaisdealerta")},

 {"id":"pnc_mancar_febre","ep":16,"serie":"Pé no Chão","temporada":"sinais-de-alerta",
  "scenes":[
   {"k":"Combinação que apressa","sc":["Mancar + febre","pede pressa."],"e":None,"sub":"Juntos, são um sinal de urgência — eu explico sem alarde.",
    "vo":"Tem uma combinação que muda o nível de urgência: criança mancando junto com febre. Separados podem ser bobos. Juntos, pedem atenção rápida, e eu explico por quê."},
   {"k":"Por que correr","sc":["Pode ser infecção","na articulação."],"e":None,"sub":"Uma articulação infectada precisa de avaliação urgente para se proteger.",
    "vo":"Porque uma das causas dessa dupla é uma infecção dentro da articulação. E articulação infectada é das poucas situações na ortopedia infantil que não esperam: quanto antes avaliar, melhor pra protegê-la."},
   {"k":"O que observar","sc":["Não dobra, não","apoia, chora ao mexer."],"e":None,"sub":"Recusa total de mexer ou apoiar a perna reforça a pressa.",
    "vo":"Os sinais que reforçam a pressa: a criança não quer dobrar nem apoiar a perna, chora quando alguém mexe na articulação, e fica quietinha protegendo o membro."},
   {"k":"O que fazer","sc":["Procure atendimento.","Não espere passar."],"e":None,"sub":"Com febre + manqueira, leve para avaliação no mesmo dia.",
    "vo":"E o que fazer é direto: com febre e manqueira juntas, não espere pra ver se melhora. Procure um atendimento no mesmo dia. Melhor avaliar e ser nada do que perder tempo."},
   {"k":"Passa adiante","sc":["Salva: febre +","manca = avaliar já."],"e":None,"sub":"Manda pra todo pai e mãe — esse pode importar muito.","cta":True,
    "vo":"Salva e manda pra todo pai e mãe, porque esse pode fazer diferença de verdade. E nem todo sinal está nas pernas: às vezes está nas costas. É o próximo."},
  ],
  "caption":cap_ped("Mancar + febre na criança: combinação que pede pressa. Uma das causas dessa dupla é uma infecção dentro da articulação — e articulação infectada é das poucas situações que não esperam. Sinais que reforçam a urgência: a criança não quer dobrar nem apoiar a perna, chora ao mexerem na articulação e fica protegendo o membro. Com febre e manqueira juntas, procure atendimento no mesmo dia.","#emergencia #sinaisdealerta")},

 {"id":"pnc_escoliose","ep":17,"serie":"Pé no Chão","temporada":"sinais-de-alerta",
  "scenes":[
   {"k":"Olhe as costas","sc":["Nem todo sinal","está nas pernas."],"e":None,"sub":"A coluna também dá pistas — e dá pra checar em casa.",
    "vo":"A gente fala muito de pé e perna, mas a coluna também manda recados. E a escoliose, aquele desvio da coluna, dá pra começar a checar em casa."},
   {"k":"O que é","sc":["A coluna entorta","para o lado."],"e":None,"sub":"Um desvio em curva, que costuma aparecer no estirão da adolescência.",
    "vo":"Escoliose é quando a coluna, vista por trás, faz uma curva pro lado em vez de ficar reta. Costuma dar as caras no estirão de crescimento, na pré-adolescência."},
   {"k":"O teste de casa","sc":["Peça pra inclinar","o corpo à frente."],"e":None,"sub":"Ao se curvar pra frente, um lado das costas mais alto chama atenção.",
    "vo":"Tem um teste simples: peça pra ela se inclinar pra frente, como quem vai tocar os pés. Aí você olha as costas de cima. Se um lado fica mais alto que o outro, vale mostrar pro médico."},
   {"k":"Por que cedo importa","sc":["Acompanhar cedo","amplia as opções."],"e":None,"sub":"Quanto antes se percebe, mais simples costuma ser o acompanhamento.",
    "vo":"E por que reparar cedo? Porque acompanhar desde o comecinho costuma deixar o manejo mais simples, principalmente enquanto a criança ainda cresce. Sem drama, com atenção."},
   {"k":"Passa adiante","sc":["Salva o teste","da inclinação."],"e":None,"sub":"Manda pra pais de pré-adolescentes.","cta":True,
    "vo":"Salva esse teste das costas e manda pra pais de pré-adolescente. E aqueles medos que viralizam, tipo cair muito? É o próximo."},
  ],
  "caption":cap_ped("Escoliose: o sinal nas costas. É um desvio em curva da coluna (vista por trás), que costuma aparecer no estirão da pré-adolescência. Há um teste simples em casa: peça para a criança inclinar o corpo à frente, como quem vai tocar os pés, e observe as costas de cima — se um lado fica mais alto que o outro, vale mostrar ao médico. Perceber cedo costuma deixar o acompanhamento mais simples.","#escoliose #coluna")},

 {"id":"pnc_cai_muito","ep":18,"serie":"Pé no Chão","temporada":"mito-ou-verdade",
  "scenes":[
   {"k":"Cai toda hora","sc":["Criança que cai","muito: é normal?"],"e":None,"sub":"Tem uma dose de tombo que faz parte — e um ponto que pede olhar.",
    "vo":"Criança nova vive caindo, e isso assusta. Mas existe uma dose de tombo que é parte do aprendizado, e um ponto a partir do qual vale dar uma olhada."},
   {"k":"Por que cai","sc":["Equilíbrio ainda","está em obras."],"e":None,"sub":"Nos primeiros anos, cair é como o corpo calibra o equilíbrio.",
    "vo":"Nos primeiros anos, cair é o jeito do corpo calibrar o equilíbrio. Cada tombo ensina. Então, uma boa quantidade de quedas, sem mais nada, costuma ser normal."},
   {"k":"Quando reparar","sc":["Piora, ou só","tropeça de um lado."],"e":None,"sub":"Cair cada vez mais, tropeçar sempre do mesmo lado ou regredir pede atenção.",
    "vo":"O que muda o jogo é a tendência: se em vez de melhorar com o tempo ela cai cada vez mais, se tropeça sempre do mesmo lado, ou se perdeu uma habilidade que já tinha. Aí vale avaliar."},
   {"k":"O que ajuda em casa","sc":["Chão livre e","pé no chão."],"e":None,"sub":"Espaço seguro pra praticar e tempo descalço ajudam o equilíbrio.",
    "vo":"E o que ajuda em casa é simples: um espaço livre e seguro pra ela praticar, e tempo de pé descalço, que melhora a noção de equilíbrio. Movimento é treino."},
   {"k":"Passa adiante","sc":["Salva: cair faz","parte (até certo ponto)."],"e":None,"sub":"Manda pra quem se preocupa com cada tombo.","cta":True,
    "vo":"Salva e manda pra quem sofre a cada tombo. E o medo que mais viraliza: sentar em W, pode ou não? É o próximo."},
  ],
  "caption":cap_ped("Criança que cai muito: é normal? Nos primeiros anos, cair é como o corpo calibra o equilíbrio — cada tombo ensina, e uma boa quantidade de quedas, sem mais nada, costuma ser normal. O que muda o jogo é a tendência: cair cada vez mais (em vez de melhorar), tropeçar sempre do mesmo lado, ou perder uma habilidade já conquistada. Em casa, ajuda espaço seguro para praticar e tempo descalço.","#desenvolvimento #equilibrio")},

 {"id":"pnc_sentar_w","ep":19,"serie":"Pé no Chão","temporada":"mito-ou-verdade",
  "scenes":[
   {"k":"O medo viral","sc":["Sentar em 'W'","faz mal?"],"e":None,"sub":"Viralizou como vilão — mas a real é mais tranquila.",
    "vo":"Sentar em W, com as perninhas pros lados formando a letra, virou vilão na internet. Mas a real é bem mais tranquila do que os vídeos de susto sugerem."},
   {"k":"Por que fazem","sc":["É a base mais","estável pra brincar."],"e":None,"sub":"O W dá uma base larga; muita criança escolhe pra ter as mãos livres.",
    "vo":"As crianças sentam assim porque é uma base larga e estável, que deixa as mãos livres pra brincar. Faz sentido pra elas, é prático."},
   {"k":"O que se entende hoje","sc":["Na maioria, não","causa deformidade."],"e":None,"sub":"Em criança que cresce bem, alternar posições costuma bastar.",
    "vo":"E o que se entende hoje é que, numa criança que se desenvolve bem, sentar em W de vez em quando não vira deformidade. O exagero do alarme não se sustenta."},
   {"k":"O bom senso","sc":["Variar é melhor","que proibir."],"e":None,"sub":"Se ela só senta em W, ou já tem outro sinal, vale comentar com o médico.",
    "vo":"O bom senso é estimular variar a posição, em vez de proibir e brigar. Agora, se ela só consegue sentar em W, ou já tem outros sinais, aí vale comentar com o ortopedista."},
   {"k":"Passa adiante","sc":["Salva: W não é","o monstro do vídeo."],"e":None,"sub":"Manda pra quem vive corrigindo o filho no chão.","cta":True,
    "vo":"Salva e manda pra quem vive corrigindo o filho no chão por causa disso. E pra fechar a série, a campeã das dúvidas: mochila pesada estraga a coluna? É o próximo."},
  ],
  "caption":cap_ped("Sentar em 'W': pode ou não? Virou vilão na internet, mas a real é mais tranquila. As crianças escolhem essa posição porque é uma base larga e estável, que deixa as mãos livres para brincar. O entendimento atual: numa criança que se desenvolve bem, sentar em W de vez em quando não vira deformidade. O bom senso é estimular variar a posição — e, se ela SÓ senta em W ou já tem outros sinais, comentar com o ortopedista.","#sentaremw #mitoouverdade")},

 {"id":"pnc_mochila","ep":20,"serie":"Pé no Chão","temporada":"mito-ou-verdade",
  "scenes":[
   {"k":"O fecho da série","sc":["Mochila pesada","estraga a coluna?"],"e":None,"sub":"A pergunta que fecha a temporada — com resposta equilibrada.",
    "vo":"Pra fechar essa temporada do Pé no Chão, a campeã das dúvidas escolares: mochila pesada estraga a coluna da criança? Vamos à resposta com equilíbrio."},
   {"k":"O que ela faz","sc":["Causa dor e má","postura no dia."],"e":None,"sub":"Peso excessivo gera dor nas costas e ombros e postura ruim na hora.",
    "vo":"O que o peso exagerado faz, e bem, é causar dor nas costas e nos ombros e uma postura ruim enquanto ela carrega. Desconforto real, no dia a dia."},
   {"k":"O que ela não faz","sc":["Não 'entorta'","a coluna pra sempre."],"e":"não","sub":"Não há prova de que mochila cause escoliose ou deformidade permanente.","motif":"no",
    "vo":"Mas o que ela não faz, ao contrário do mito, é entortar a coluna pra sempre. Não existe prova de que mochila cause escoliose ou deformidade permanente. Alívio pros pais."},
   {"k":"A regra prática","sc":["Até uns 10 a 15%","do peso da criança."],"e":None,"sub":"Mochila leve, duas alças, ajustada às costas, e só o essencial dentro.",
    "vo":"A regra prática que vale guardar: a mochila cheia idealmente não passa de uns dez a quinze por cento do peso da criança. Use as duas alças, ajustada ao corpo, e leve só o necessário."},
   {"k":"Passa adiante","sc":["Salva a regra","da mochila."],"e":None,"sub":"Manda pro grupo da escola. E recomeça a série!","cta":True,
    "vo":"Salva e manda pro grupo da escola. No fim, tudo se resume a saber a hora de procurar, e é isso que o Pé no Chão te ensina. Se quiser, recomeça do primeiro: os marcos do andar."},
  ],
  "caption":cap_ped("Mochila pesada estraga a coluna? Resposta com equilíbrio. O peso excessivo causa, sim, dor nas costas e ombros e má postura na hora de carregar — desconforto real. Mas NÃO há prova de que mochila cause escoliose ou deformidade permanente. A regra prática: a mochila cheia idealmente não passa de ~10–15% do peso da criança; use as duas alças, ajustada ao corpo, e leve só o essencial.","#mochila #postura")},
]

NEW_EPISODES = OSSO_NOVO + PE_NO_CHAO_NOVOS

if __name__ == "__main__":
    print(len(NEW_EPISODES), "novos episódios")
    for e in NEW_EPISODES:
        print(f"  {e['serie']:10s} ep{e['ep']:02d} {e['id']:24s} temporada={e['temporada']:22s} cenas={len(e['scenes'])}")
