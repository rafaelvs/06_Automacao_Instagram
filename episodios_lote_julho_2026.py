# -*- coding: utf-8 -*-
"""
LOTE JULHO/2026 — 16 novos episódios narrados (voz), para reabastecer a fila de Reels (o gargalo).
  • 8 "Pé no Chão" (ortopedia pediátrica) — pilar de alcance/afinidade.
  • 8 "Osso Novo" (reconstrução / alongamento ósseo) — pilar de autoridade.

Tópicos escolhidos por alto potencial de SEND e SEM sobreposição com os 38 episódios já gerados.
Mesma engenharia (render_reel + gerar_reel_voz). Cada cena:
  k=kicker, sc=[2 linhas grandes], e=palavra dourada (ou None), sub=apoio na tela,
  vo=narração (a VOZ complementa a tela, não repete), motif:"no" desenha o símbolo proibido,
  última cena cta=True (otimizada p/ compartilhamento no direct). motif_family:"bone" nos de osso.

GUARDRAIL (inegociável): "Osso Novo" trata alongamento/reconstrução SEMPRE sob função, trauma,
deformidade e sequela — NUNCA sob ângulo estético/cosmético/altura (o ep on_haste_magnetica reafirma
isso na tela). Nenhum frame usa raio-X/exame real ou falso — só esquema/ilustração didática.
CFM (Res. 2.336/2023): educativo, sem prometer/insinuar resultado, sem paciente real; rodapé com
CRM-SP 226103 · RQE 137901 e disclaimer entram em todo frame pelo render.
"""
from episodios_novos_2026 import cap_ped, cap_rec

LOTE_JULHO = [

 # ───────────── Pé no Chão #1 ─────────────
 {"id":"pnc_joelho_valgo","ep":21,"serie":"Pé no Chão","temporada":"pernas",
  "scenes":[
   {"k":"Mito x Verdade","sc":["Joelho em X","quase sempre é fase."],"e":"fase","sub":"Entre 3 e 6 anos, é o desenho normal do crescimento.",
    "vo":"Se você olhou de frente e os joelhos do seu filho quase se encostam enquanto os pés ficam afastados, calma. Dos três aos seis anos, isso costuma ser só uma fase do crescimento."},
   {"k":"O que acontece","sc":["As perninhas","mudam sozinhas."],"e":None,"sub":"Bebê nasce mais arqueado, vira X na pré-escola e alinha perto dos 7.",
    "vo":"As pernas trocam de forma com a idade: o bebê é mais arqueadinho, vira esse X na pré-escola e tende a alinhar lá pros sete anos. É um vaivém normal."},
   {"k":"O que NÃO ajuda","sc":["Palmilha não","alinha o joelho."],"e":"não","sub":"Em criança saudável, isso não muda o eixo da perna.","motif":"no",
    "vo":"E aquela ideia de sapato ortopédico ou palmilha pra endireitar? Em criança saudável, não muda o eixo do joelho. Pode poupar esse dinheiro."},
   {"k":"Quando investigar","sc":["Só um lado,","ou piora."],"e":None,"sub":"X só numa perna, que aumenta, dói ou vem com baixa estatura: avalie.",
    "vo":"O alerta liga quando foge do padrão: o X só de um lado, que piora em vez de melhorar, que dói, ou numa criança muito baixinha. Aí vale avaliar."},
   {"k":"O que de fato importa","sc":["Tempo, eixo","e simetria."],"e":"simetria","sub":"Acompanhar a evolução vale mais que qualquer correção precoce.",
    "vo":"No fim, o que conta é observar a evolução: se os dois lados são parecidos e caminham pro alinhamento, o tempo costuma resolver melhor que qualquer correção apressada."},
   {"k":"Passa adiante","sc":["Manda pra um pai","preocupado com isso."],"e":None,"sub":"Salva pra lembrar quando bater a dúvida.","cta":True,
    "vo":"Manda esse vídeo pra aquele pai ou mãe que vive preocupado com o joelho do filho. E salva pra quando a dúvida voltar."},
  ],
  "caption":cap_ped("Joelho em X (geno valgo) na criança quase sempre é fase: entre 3 e 6 anos é o desenho normal do crescimento, e o alinhamento costuma chegar perto dos 7. Sapato e palmilha NÃO endireitam o joelho de uma criança saudável. Merece avaliação o X que aparece só num lado, que piora, que dói ou que vem com baixa estatura.","#joelhoemx #genovalgo #desenvolvimentoinfantil")},

 # ───────────── Osso Novo #1 ─────────────
 {"id":"on_consolidacao_viciosa","ep":22,"serie":"Osso Novo","temporada":"refazer-e-realinhar","motif_family":"bone",
  "scenes":[
   {"k":"E quando cola torto?","sc":["O osso colou —","mas entortado."],"e":None,"sub":"Acontece. E, na maioria das vezes, tem conserto.",
    "vo":"Tem uma situação que assusta muita gente: a fratura até colou, mas colou torta. Isso tem nome, consolidação viciosa, e, na maior parte das vezes, dá pra consertar."},
   {"k":"Por que importa","sc":["Osso torto","sobrecarrega."],"e":"sobrecarrega","sub":"Um eixo errado joga o peso pro lugar errado e desgasta a junta.",
    "vo":"E não é só estética, é mecânica: um osso fora do eixo joga o peso no lugar errado, força a articulação vizinha e, com o tempo, acelera o desgaste dela."},
   {"k":"O conserto","sc":["Cortar e","realinhar."],"e":None,"sub":"A osteotomia corta o osso no ponto certo e devolve o eixo.",
    "vo":"O conserto é uma osteotomia: a gente corta o osso no ponto calculado, gira pro eixo certo e fixa. É como reabrir um nó mal feito e amarrar do jeito correto."},
   {"k":"Planejado no milímetro","sc":["Mede antes,","corta depois."],"e":None,"sub":"O ângulo é calculado por imagem — nada é no olhômetro.",
    "vo":"E nada disso é no olho: o ângulo e o ponto do corte são calculados antes, na imagem. Medir com precisão é o que separa um bom resultado de um remendo."},
   {"k":"Guardrail","sc":["É função,","não estética."],"e":"função","sub":"O objetivo é alinhar a carga e poupar a junta — não embelezar.","motif":"no",
    "vo":"Importante deixar claro: aqui o objetivo é função. Realinhar a carga, proteger a articulação e devolver movimento. Não é sobre aparência."},
   {"k":"Passa adiante","sc":["Manda pra quem","colou torto."],"e":None,"sub":"Osso novo, de volta ao eixo. Salva pra lembrar.","cta":True,
    "vo":"Se você conhece alguém que ficou com um osso colado torto e acha que não tem mais jeito, manda esse vídeo. Quase sempre tem caminho."},
  ],
  "caption":cap_rec("Osso que colou torto (consolidação viciosa) costuma ter conserto. Não é questão de estética: um eixo errado joga o peso no lugar errado, sobrecarrega a articulação vizinha e acelera o desgaste. O conserto é a osteotomia — cortar o osso no ponto calculado, realinhar e fixar, tudo planejado por imagem (nunca no olhômetro). O objetivo é sempre função: realinhar carga e poupar a junta.","#consolidacaoviciosa #osteotomia #deformidadeossea")},

 # ───────────── Pé no Chão #2 ─────────────
 {"id":"pnc_osgood","ep":23,"serie":"Pé no Chão","temporada":"crescimento",
  "scenes":[
   {"k":"Pais de atleta, atenção","sc":["Caroço dolorido","abaixo do joelho."],"e":None,"sub":"No adolescente que corre e salta, costuma ter nome.",
    "vo":"Se seu filho adolescente reclama de um carocinho dolorido logo abaixo do joelho, ainda mais se ele corre, joga ou salta muito, presta atenção: isso tem nome."},
   {"k":"O que é","sc":["Osgood-","Schlatter."],"e":None,"sub":"A tração do tendão puxa o osso que ainda está crescendo ali.",
    "vo":"Chama Osgood-Schlatter. Naquela fase de estirão, o tendão forte do joelho fica puxando um ponto de osso que ainda está se formando. Daí a dor e o caroço."},
   {"k":"A boa notícia","sc":["Costuma ser","temporário."],"e":"temporário","sub":"Tende a passar quando o osso amadurece — sem cirurgia, na maioria.",
    "vo":"A boa notícia: na maioria das vezes é coisa de fase. Quando aquele osso termina de amadurecer, costuma passar, e quase nunca precisa de cirurgia."},
   {"k":"O que ajuda","sc":["Dosar o esforço,","gelo, alongar."],"e":None,"sub":"Não é parar tudo — é ajustar a carga e fortalecer com orientação.",
    "vo":"O que ajuda não é largar o esporte, é dosar: ajustar a carga nos picos de dor, gelo depois do treino e fortalecer com orientação. Equilíbrio, não proibição."},
   {"k":"Quando avaliar","sc":["Manca, incha","ou trava."],"e":None,"sub":"Dor que faz mancar, inchaço importante ou joelho que trava: avalie.","motif":"no",
    "vo":"Agora, se a dor faz mancar, se incha de verdade ou o joelho trava, não empurra com a barriga: vale uma avaliação pra descartar outras coisas."},
   {"k":"Passa adiante","sc":["Manda pro grupo","dos pais do time."],"e":None,"sub":"Salva pra próxima reclamação de joelho.","cta":True,
    "vo":"Manda esse vídeo pro grupo dos pais do time, que sempre tem alguém passando por isso. E salva pra próxima reclamação de joelho."},
  ],
  "caption":cap_ped("Caroço dolorido logo abaixo do joelho no adolescente que corre e salta costuma ser Osgood-Schlatter: na fase de estirão, o tendão traciona um ponto de osso ainda em formação. Boa notícia — costuma ser temporário e passar quando o osso amadurece, raramente exigindo cirurgia. Ajuda dosar o esforço (sem largar o esporte), gelo e alongamento orientado. Avalie se mancar, inchar muito ou travar.","#osgoodschlatter #dornojoelho #adolescente")},

 # ───────────── Osso Novo #2 ─────────────
 {"id":"on_salvamento_membro","ep":24,"serie":"Osso Novo","temporada":"reconstrucao","motif_family":"bone",
  "scenes":[
   {"k":"A pergunta difícil","sc":["Amputar ou","reconstruir?"],"e":None,"sub":"Em casos graves, essa decisão é real — e é compartilhada.",
    "vo":"Tem uma pergunta dura que aparece em casos graves de trauma ou infecção: dá pra salvar o membro, ou o melhor caminho é amputar? É uma decisão séria, e ela é tomada junto."},
   {"k":"Não existe resposta única","sc":["Depende do osso,","do corpo, da vida."],"e":None,"sub":"Extensão da lesão, infecção, circulação, idade e o que a pessoa quer.",
    "vo":"Não existe uma resposta pronta. Pesa o tamanho da lesão, se tem infecção, como está a circulação e o nervo, a saúde geral e, principalmente, o que faz sentido pra vida daquela pessoa."},
   {"k":"Reconstruir é possível","sc":["Osso se refaz,","vão se preenche."],"e":"refaz","sub":"Transporte ósseo e fixadores podem reconstruir perdas grandes.",
    "vo":"Reconstruir é, sim, possível em muitos casos: com transporte ósseo e fixadores, dá pra refazer perdas grandes de osso. Mas costuma ser um caminho mais longo, de etapas."},
   {"k":"Amputar não é desistir","sc":["Às vezes é a","melhor função."],"e":None,"sub":"Com prótese, pode devolver autonomia mais rápido e com menos dor.","motif":"no",
    "vo":"E aqui um ponto honesto: amputar não é desistir. Em algumas situações, com uma boa prótese, é o caminho que devolve autonomia mais rápido e com menos sofrimento."},
   {"k":"O que guia","sc":["Função e","qualidade de vida."],"e":"qualidade","sub":"A melhor escolha é a que devolve mais vida — não a mais heroica.",
    "vo":"O que guia a decisão não é qual cirurgia é mais impressionante, e sim qual devolve mais função e qualidade de vida pra aquela pessoa específica. Isso muda de gente pra gente."},
   {"k":"Passa adiante","sc":["Manda pra quem","ouviu só amputar."],"e":None,"sub":"Vale uma segunda opinião. Salva pra lembrar.","cta":True,
    "vo":"Se alguém ouviu que só resta amputar e ficou na dúvida, manda esse vídeo. Uma segunda opinião, nessas horas, vale muito."},
  ],
  "caption":cap_rec("Amputar ou reconstruir? Em casos graves de trauma ou infecção, essa decisão é real — e compartilhada. Não há resposta única: pesa a extensão da lesão, infecção, circulação, saúde geral e o que faz sentido para a vida da pessoa. Reconstruir grandes perdas de osso é possível (transporte ósseo, fixadores), mas costuma ser um caminho de etapas. E amputar não é desistir: às vezes devolve função e autonomia mais rápido. O que guia é a qualidade de vida.","#salvamentodemembro #reconstrucaoossea #segundaopiniao")},

 # ───────────── Pé no Chão #3 ─────────────
 {"id":"pnc_sever","ep":25,"serie":"Pé no Chão","temporada":"crescimento",
  "scenes":[
   {"k":"Dói o calcanhar?","sc":["Criança que joga","bola e reclama."],"e":None,"sub":"Dor no calcanhar no esporte tem uma explicação comum.",
    "vo":"Criança ou pré-adolescente que joga bola, faz dança ou corre muito e vive reclamando do calcanhar? Tem uma explicação bem comum pra isso."},
   {"k":"O que é","sc":["Doença de","Sever."],"e":None,"sub":"A placa de crescimento do calcanhar inflama com o impacto repetido.",
    "vo":"Chama doença de Sever. No calcanhar da criança ainda tem uma placa de crescimento, e o impacto repetido do esporte irrita justamente esse ponto."},
   {"k":"Tranquiliza","sc":["Não deixa","sequela."],"e":"Não","sub":"É autolimitada: melhora com o tempo e não estraga o osso.","motif":"no",
    "vo":"E aqui vai o alívio: é uma dor de fase, que não deixa sequela e não estraga o osso. Some sozinha conforme a criança cresce."},
   {"k":"O que ajuda","sc":["Gelo e calçado","com amortecimento."],"e":None,"sub":"Calcanheira de silicone, dosar treino e alongar a panturrilha.",
    "vo":"Pra aliviar: gelo depois do esforço, um tênis com bom amortecimento, às vezes uma calcanheira de silicone, e alongar a panturrilha. E dosar os treinos nos dias de pico."},
   {"k":"Quando avaliar","sc":["Manca, incha","ou dói parado."],"e":None,"sub":"Se atrapalha o dia, incha ou dói até em repouso: avalie.",
    "vo":"Se a dor faz mancar o dia todo, se incha, ou se dói até parado, sem esforço, aí vale passar no ortopedista pra confirmar e descartar outras causas."},
   {"k":"Passa adiante","sc":["Manda pra outro","pai de atleta."],"e":None,"sub":"Salva pra próxima dor de calcanhar.","cta":True,
    "vo":"Manda pra outro pai ou mãe de criança que vive no esporte. E salva pra próxima vez que o calcanhar reclamar."},
  ],
  "caption":cap_ped("Dor no calcanhar na criança/pré-adolescente que pratica esporte costuma ser doença de Sever: o impacto repetido irrita a placa de crescimento do calcâneo. Tranquiliza — é autolimitada, melhora com o tempo e não deixa sequela. Ajuda gelo, calçado com amortecimento, calcanheira de silicone, alongar a panturrilha e dosar o treino. Avalie se mancar o dia todo, inchar ou doer em repouso.","#doencadesever #dornocalcanhar #esporteinfantil")},

 # ───────────── Osso Novo #3 ─────────────
 {"id":"on_vitamina_d","ep":26,"serie":"Osso Novo","temporada":"viver-o-tratamento","motif_family":"bone",
  "scenes":[
   {"k":"Pergunta comum","sc":["Vitamina ajuda","o osso a colar?"],"e":None,"sub":"Tem papel, sim — mas não do jeito que vendem.",
    "vo":"Quem está com uma fratura sempre pergunta: tomar vitamina faz o osso colar mais rápido? Tem papel, sim, mas não é a pílula mágica que costumam vender."},
   {"k":"O básico que conta","sc":["Cálcio e","vitamina D."],"e":None,"sub":"São a matéria-prima e o pedreiro que coloca o cálcio no osso.",
    "vo":"O combo que importa de verdade é cálcio e vitamina D. O cálcio é o tijolo, e a vitamina D é quem leva esse tijolo pra dentro do osso. Faltando um, a obra atrasa."},
   {"k":"Mais não é melhor","sc":["Encher de","cálcio não cola."],"e":"não","sub":"Acima do que o corpo usa, o excesso não acelera — e pode fazer mal.","motif":"no",
    "vo":"Mas atenção: mais não é melhor. Passar do que o corpo usa não acelera a consolidação e ainda pode sobrecarregar o rim. O alvo é repor o que falta, não empilhar."},
   {"k":"O que mais pesa","sc":["Não fumar,","comer bem."],"e":None,"sub":"Parar de fumar e ter proteína pesam mais que qualquer cápsula.",
    "vo":"E o que pesa mais que qualquer suplemento: não fumar, controlar diabetes e comer proteína. Esses fatores movem a agulha bem mais que uma cápsula extra."},
   {"k":"O caminho certo","sc":["Repor o que","falta, medindo."],"e":"medindo","sub":"Dosar a vitamina D e repor o necessário, com orientação.",
    "vo":"O caminho certo é simples: medir a vitamina D, repor o que estiver baixo e ajustar a alimentação, com orientação. Personalizado, não no chute."},
   {"k":"Passa adiante","sc":["Manda pra quem","fraturou agora."],"e":None,"sub":"Salva pra ajustar a dieta da recuperação.","cta":True,
    "vo":"Manda pra alguém que acabou de fraturar e quer ajudar o osso. E salva pra ajustar a alimentação da recuperação."},
  ],
  "caption":cap_rec("Vitamina ajuda o osso a colar? Tem papel, sim, mas não como pílula mágica. O que conta é o combo cálcio + vitamina D (o tijolo e quem o leva para dentro do osso). Mais NÃO é melhor: acima do que o corpo usa, o excesso não acelera e pode sobrecarregar o rim. O que mais pesa na consolidação é não fumar, controlar o diabetes e ter proteína na dieta. O certo é medir a vitamina D e repor o que falta, com orientação.","#vitaminad #calcio #consolidacaoossea")},

 # ───────────── Pé no Chão #4 ─────────────
 {"id":"pnc_torcicolo","ep":27,"serie":"Pé no Chão","temporada":"sinais-de-alerta",
  "scenes":[
   {"k":"Bebê novinho","sc":["Só olha pra","um lado."],"e":None,"sub":"A cabecinha vive virada sempre pro mesmo lado.",
    "vo":"Reparou que o seu bebê quase sempre vira a cabeça pro mesmo lado e custa a olhar pro outro? Isso merece um olhar com carinho, e cedo."},
   {"k":"O que pode ser","sc":["Torcicolo","do bebê."],"e":None,"sub":"Um músculo do pescoço fica mais encurtado de um lado.",
    "vo":"Pode ser o torcicolo congênito: um músculo do pescoço, de um lado, fica mais curtinho e tenso, e por isso a cabeça prefere aquele lado."},
   {"k":"Por que agir cedo","sc":["Quanto antes,","mais simples."],"e":"antes","sub":"Nos primeiros meses costuma resolver só com posição e fisioterapia.",
    "vo":"E aqui o tempo joga a favor: quanto mais cedo, mais fácil. Nos primeiros meses, costuma resolver com mudança de posição e fisioterapia, sem nada invasivo."},
   {"k":"O que ajuda em casa","sc":["Estimular o","lado difícil."],"e":None,"sub":"Chamar a atenção pelo lado que ele evita — com orientação.",
    "vo":"Em casa ajuda estimular o lado que ele evita: conversar, oferecer o brinquedo e posicionar o berço pra ele querer virar pra lá. Mas sempre com orientação de quem acompanha."},
   {"k":"Fique de olho","sc":["Cabeça achatada","de um lado."],"e":None,"sub":"Torcicolo pode vir junto de achatamento do crânio — avalie.","motif":"no",
    "vo":"Fica de olho também na cabecinha: como ele deita sempre do mesmo lado, o crânio pode achatar ali. Por isso vale avaliar e não só esperar."},
   {"k":"Passa adiante","sc":["Manda pra um pai","ou mãe de recém."],"e":None,"sub":"Quanto antes virem, melhor. Salva pra lembrar.","cta":True,
    "vo":"Manda pra um pai ou mãe de bebê recém-nascido. Nisso, ver cedo faz toda a diferença. Salva pra lembrar."},
  ],
  "caption":cap_ped("Bebê que vive com a cabeça virada sempre pro mesmo lado pode ter torcicolo congênito: um músculo do pescoço fica encurtado de um lado. Agir cedo é tudo — nos primeiros meses costuma resolver só com posição e fisioterapia. Em casa, estimular (com orientação) o lado que ele evita ajuda. Fique de olho no achatamento do crânio, que pode vir junto.","#torcicolo #bebe #desenvolvimentoinfantil")},

 # ───────────── Osso Novo #4 ─────────────
 {"id":"on_diabetes_osso","ep":28,"serie":"Osso Novo","temporada":"quando-o-osso-falha","motif_family":"bone",
  "scenes":[
   {"k":"Pouca gente sabe","sc":["Diabetes mexe","com o osso."],"e":None,"sub":"O açúcar alto atrapalha a fratura colar — e a cirurgia cicatrizar.",
    "vo":"Pouca gente liga uma coisa à outra, mas o diabetes mal controlado mexe diretamente com o osso: atrapalha a fratura a colar e a ferida a fechar."},
   {"k":"Por quê","sc":["Açúcar alto","trava a obra."],"e":"trava","sub":"Prejudica circulação, defesa e as células que fabricam osso novo.",
    "vo":"O motivo é que o açúcar alto trava a obra por vários lados: piora a circulação, derruba a defesa contra infecção e atrapalha as células que fabricam osso novo."},
   {"k":"O risco extra","sc":["Mais infecção,","cola mais devagar."],"e":None,"sub":"Por isso o controle do açúcar entra no plano cirúrgico.",
    "vo":"Na prática, isso significa mais risco de infecção e uma consolidação mais lenta. Por isso, controlar o açúcar não é detalhe: faz parte do plano cirúrgico, tanto quanto o parafuso."},
   {"k":"A boa notícia","sc":["Controlado,","o risco cai."],"e":"cai","sub":"Com a glicemia ajustada, a recuperação se aproxima da de qualquer pessoa.",
    "vo":"E a boa notícia é direta: com o diabetes bem controlado, esse risco cai bastante e a recuperação se aproxima da de qualquer outra pessoa. O controle muda o jogo."},
   {"k":"Time junto","sc":["Ortopedista e","endócrino."],"e":None,"sub":"Cirurgia e controle do açúcar caminham lado a lado.","motif":"no",
    "vo":"Por isso a gente não trabalha sozinho: ortopedista e quem cuida do diabetes andam juntos. Não dá pra cuidar do osso ignorando o açúcar."},
   {"k":"Passa adiante","sc":["Manda pra quem","tem diabetes."],"e":None,"sub":"Vai operar ou fraturou? O controle conta. Salva pra lembrar.","cta":True,
    "vo":"Manda pra alguém com diabetes que vai operar ou fraturou. Saber disso muda a preparação. E salva pra lembrar."},
  ],
  "caption":cap_rec("Pouca gente sabe: o diabetes mal controlado atrapalha a fratura a colar e a cirurgia a cicatrizar. O açúcar alto trava a obra por vários lados — piora circulação, derruba a defesa contra infecção e prejudica as células que fabricam osso novo. Resultado: mais risco de infecção e consolidação mais lenta. A boa notícia: com a glicemia controlada, o risco cai muito. Por isso ortopedista e o cuidado do diabetes caminham juntos.","#diabetes #consolidacaoossea #cicatrizacao")},

 # ───────────── Pé no Chão #5 ─────────────
 {"id":"pnc_engatinhar","ep":29,"serie":"Pé no Chão","temporada":"marcha",
  "scenes":[
   {"k":"Mito x Verdade","sc":["Pular o","engatinhar?"],"e":None,"sub":"Nem todo bebê engatinha — e isso pode ser normal.",
    "vo":"O seu bebê foi direto pra de pé e nunca engatinhou direito? Antes de se preocupar: nem todo bebê engatinha, e muitos pulam essa etapa sem nenhum problema."},
   {"k":"O que importa","sc":["O que conta é","ele progredir."],"e":"progredir","sub":"Senta, rola, se arrasta, fica de pé — o caminho varia de bebê pra bebê.",
    "vo":"O que importa não é a etapa exata, é o progresso: ele senta, rola, se arrasta, busca os objetos, fica de pé. Cada bebê faz esse caminho do seu jeito."},
   {"k":"Engatinhar diferente","sc":["De bumbum","ou de urso."],"e":None,"sub":"Arrastar sentado ou de quatro também conta como locomoção.",
    "vo":"E tem bebê que engatinha torto: arrastando o bumbum sentado, ou de ursinho, com as mãos e os pés. Isso também vale, é só um estilo de se locomover."},
   {"k":"Quando acender o alerta","sc":["Sempre um lado","do corpo."],"e":None,"sub":"Usar só um lado, rigidez ou perder algo que já fazia: avalie.","motif":"no",
    "vo":"O alerta liga se ele usa sempre só um lado do corpo, se as perninhas são muito duras ou molinhas, ou se ele perde algo que já fazia. Aí vale avaliar."},
   {"k":"Sem corrida","sc":["Comparar não","ajuda."],"e":"não","sub":"A janela do desenvolvimento é ampla; o pediatra acompanha a curva.",
    "vo":"E evita comparar com o filho do vizinho: a janela do normal é larga. Quem acompanha a curva de cada criança é o pediatra, com calma."},
   {"k":"Passa adiante","sc":["Manda pra uma","mãe ansiosa."],"e":None,"sub":"Salva pra lembrar nos próximos marcos.","cta":True,
    "vo":"Manda pra aquela mãe ou pai ansioso com os marcos do bebê. E salva pra lembrar nos próximos."},
  ],
  "caption":cap_ped("Pular o engatinhar pode ser normal — nem todo bebê engatinha, e muitos vão direto para o ficar de pé. O que importa não é a etapa exata, é o progresso: sentar, rolar, se arrastar, buscar objetos, ficar de pé. Engatinhar de bumbum ou de urso também conta. Acenda o alerta se usar sempre só um lado do corpo, rigidez/moleza importante, ou perda de habilidades — aí avalie.","#engatinhar #marcosdodesenvolvimento #bebe")},

 # ───────────── Osso Novo #5 ─────────────
 {"id":"on_haste_magnetica","ep":30,"serie":"Osso Novo","temporada":"reconstrucao","motif_family":"bone",
  "scenes":[
   {"k":"Tecnologia que impressiona","sc":["Uma haste que","alonga por dentro."],"e":None,"sub":"Sem fixador externo aparente — controlada por ímã.",
    "vo":"Tem uma tecnologia que parece coisa de filme: uma haste colocada dentro do osso que vai alongando aos poucos, sem aquele fixador externo todo aparente por fora."},
   {"k":"Como funciona","sc":["Um ímã, fora","do corpo."],"e":None,"sub":"Um controle magnético move a haste milímetros por dia, em casa.",
    "vo":"O controle é magnético: um aparelhinho encostado na pele, fora do corpo, move a haste pouquíssimos milímetros por dia. Boa parte do ajuste acontece em casa, sem agulha."},
   {"k":"Pra quê serve","sc":["Perna mais curta,","falha de osso."],"e":None,"sub":"Discrepância pós-trauma, sequela ou perda óssea — sempre por função.",
    "vo":"E pra que serve: corrigir uma perna que ficou mais curta depois de trauma, doença ou sequela, e ajudar a preencher falhas de osso. Sempre por função, nunca por estética."},
   {"k":"Guardrail, sem rodeio","sc":["Não é sobre","ficar mais alto."],"e":"Não","sub":"Alongar osso é tratamento de discrepância e deformidade — não cosmético.","motif":"no",
    "vo":"E aqui eu sou direto: isso não é sobre ficar mais alto. Alongamento ósseo é tratamento de diferença de comprimento e de deformidade. Usar por vaidade não é o caminho, e eu não trato assim."},
   {"k":"Tem preço","sc":["Exige etapas","e paciência."],"e":"paciência","sub":"Não é mágica: tem fase de alongar, fase de endurecer e reabilitação.",
    "vo":"E nada é mágica: tem a fase de alongar, depois a fase em que o osso novo endurece, e a reabilitação no meio. Exige etapas e paciência, com acompanhamento de perto."},
   {"k":"Passa adiante","sc":["Manda pra quem","tem perna curta."],"e":None,"sub":"Osso novo, de volta ao movimento. Salva pra lembrar.","cta":True,
    "vo":"Manda pra alguém que convive com uma perna mais curta por trauma ou sequela. Existe caminho. E salva pra lembrar."},
  ],
  "caption":cap_rec("Existe uma haste colocada dentro do osso que o alonga aos poucos, controlada por um ímã fora do corpo (sem fixador externo aparente) — milímetros por dia, boa parte em casa. Serve para corrigir encurtamento pós-trauma/sequela e ajudar a preencher falhas de osso, SEMPRE por função. Deixo claro: alongamento ósseo NÃO é sobre ficar mais alto — é tratamento de discrepância e deformidade, nunca cosmético. E não é mágica: tem fases (alongar, endurecer, reabilitar) e exige paciência.","#alongamentoosseo #discrepancia #reconstrucaoossea")},

 # ───────────── Pé no Chão #6 ─────────────
 {"id":"pnc_calcado_bebe","ep":31,"serie":"Pé no Chão","temporada":"pernas-e-pes",
  "scenes":[
   {"k":"Pergunta de pai","sc":["Bebê precisa","de sapato?"],"e":None,"sub":"Antes de andar, a resposta surpreende.",
    "vo":"Aquela dúvida na hora de montar o enxoval: bebê precisa mesmo de sapato? A resposta, antes de ele andar, costuma surpreender."},
   {"k":"Verdade","sc":["Descalço é o","melhor tênis."],"e":"melhor","sub":"Sentir o chão ajuda o pé a se desenvolver e a equilibrar.",
    "vo":"Pra quem ainda não anda, o melhor calçado é nenhum: o pé descalço sente o chão, fortalece e aprende a equilibrar. Meia antiderrapante resolve o frio."},
   {"k":"Quando o sapato entra","sc":["Pra proteger,","ao andar na rua."],"e":None,"sub":"Serve pra proteger do chão da rua — não pra dar suporte.",
    "vo":"O sapato entra quando ela começa a andar na rua, e o papel dele é proteger de pedra, frio e sujeira. Não é dar suporte mágico nem corrigir nada."},
   {"k":"Como escolher","sc":["Flexível, leve,","sola fina."],"e":None,"sub":"Que dobre na frente, segure no calcanhar e deixe os dedos livres.",
    "vo":"Na hora de escolher: que seja flexível, dobre na ponta, tenha sola fina e firme no calcanhar, com espaço pros dedos. Quanto mais perto do descalço, melhor."},
   {"k":"O que evitar","sc":["Sapato duro","e ortopédico."],"e":None,"sub":"Em pé saudável, rigidez e bota dura não ajudam — atrapalham.","motif":"no",
    "vo":"E o que evitar: aquele sapato durão, pesado, vendido como ortopédico. No pé saudável, isso não ajuda, só engessa um pé que precisa se mexer."},
   {"k":"Passa adiante","sc":["Manda pra quem","vai montar enxoval."],"e":None,"sub":"Salva antes da próxima compra.","cta":True,
    "vo":"Manda pra aquela amiga grávida montando o enxoval. E salva antes da próxima compra de sapatinho."},
  ],
  "caption":cap_ped("Bebê precisa de sapato? Antes de andar, o melhor calçado é o pé descalço — sentir o chão fortalece o pé e treina o equilíbrio (meia antiderrapante resolve o frio). O sapato entra para proteger ao andar na rua, não para dar suporte. Escolha flexível, leve, sola fina, firme no calcanhar e com espaço para os dedos. Evite sapato duro e pesado: no pé saudável, atrapalha.","#calcadoinfantil #primeirospassos #pedescalco")},

 # ───────────── Osso Novo #6 ─────────────
 {"id":"on_dor_cronica_fratura","ep":32,"serie":"Osso Novo","temporada":"viver-o-tratamento",
  "scenes":[
   {"k":"Já colou, mas dói","sc":["Meses depois,","ainda dói."],"e":None,"sub":"A fratura consolidou e a dor não foi embora. Tem explicações.",
    "vo":"Tem uma queixa que angustia: a fratura já colou, o exame tá bom, mas meses depois ainda dói. Isso não é frescura nem está na cabeça: costuma ter explicação."},
   {"k":"Vários porquês","sc":["Material, rigidez","ou nervo."],"e":None,"sub":"Pode ser o parafuso incomodando, a junta enrijecida ou um nervo sensível.",
    "vo":"E os motivos são vários: às vezes é uma placa ou parafuso incomodando por baixo da pele, às vezes a articulação que enrijeceu parada, ou um nervo que ficou mais sensível na região."},
   {"k":"Investigar, não ignorar","sc":["Dor crônica tem","causa."],"e":"causa","sub":"O caminho é achar de onde vem — avaliação dirigida resolve a maioria.",
    "vo":"O ponto-chave é não ignorar: dor crônica quase sempre tem uma causa achável. Uma boa avaliação dirigida identifica de onde ela vem na maioria dos casos."},
   {"k":"Tem tratamento","sc":["Reabilitar, tirar","material, ajustar."],"e":None,"sub":"De fisioterapia a retirar o implante que incomoda — depende da causa.",
    "vo":"E tem o que fazer: pode ser reabilitação pra soltar a junta, retirar o material que está incomodando, ou tratar o ponto sensível. O tratamento segue a causa, não o palpite."},
   {"k":"Não normalize a dor","sc":["Conviver nem","sempre é o fim."],"e":None,"sub":"Antes de aceitar a dor pra sempre, vale uma reavaliação.","motif":"no",
    "vo":"Então não normalize: antes de aceitar conviver com dor pra sempre, vale uma reavaliação. Muita gente melhora quando a causa certa finalmente é tratada."},
   {"k":"Passa adiante","sc":["Manda pra quem","já colou e dói."],"e":None,"sub":"Salva pra levar numa reavaliação.","cta":True,
    "vo":"Manda pra alguém que fraturou, já colou e segue com dor. E salva pra levar numa reavaliação."},
  ],
  "caption":cap_rec("A fratura colou, o exame está bom, mas meses depois ainda dói — isso não é frescura, costuma ter causa. Pode ser o material (placa/parafuso) incomodando, a articulação enrijecida por imobilidade, ou um nervo mais sensível na região. O caminho é investigar, não ignorar: uma avaliação dirigida encontra a origem na maioria dos casos. E há tratamento — reabilitação, retirar o implante que incomoda, tratar o ponto sensível. Antes de aceitar conviver com a dor para sempre, reavalie.","#dorcronica #posfratura #reabilitacao")},

 # ───────────── Pé no Chão #7 ─────────────
 {"id":"pnc_hipermobilidade","ep":33,"serie":"Pé no Chão","temporada":"sinais-de-alerta",
  "scenes":[
   {"k":"Criança elástica","sc":["Dobra os dedos","demais?"],"e":None,"sub":"Algumas crianças são naturalmente mais flexíveis. Quase sempre, ok.",
    "vo":"Tem criança que dobra o dedão até quase encostar no braço, estica o cotovelo além da conta e impressiona todo mundo. Na maioria das vezes, é só flexibilidade, e tá tudo bem."},
   {"k":"Tem nome","sc":["Hiper-","mobilidade."],"e":None,"sub":"As articulações têm uma amplitude maior que a média.",
    "vo":"Isso tem nome: hipermobilidade. As juntas têm uma folga maior que a média. Muita gente vive a vida toda assim, inclusive bailarinos e ginastas, sem problema nenhum."},
   {"k":"Quando é só um charme","sc":["Sem dor, sem","luxação: tranquilo."],"e":"tranquilo","sub":"Flexível, sem dor e sem a junta saindo do lugar costuma ser benigno.",
    "vo":"Quando é só flexibilidade, não dói, a junta não sai do lugar e a criança brinca normal, é benigno. Pode ser até um talento pra alguns esportes."},
   {"k":"Quando observar","sc":["Dor após brincar","ou cansa fácil."],"e":None,"sub":"Dor recorrente, quedas, cansaço ao andar e mão cansada ao escrever.",
    "vo":"Vale observar se aparece dor depois de brincar, se ela cansa fácil de andar, cai muito, ou reclama que a mão cansa ao escrever. Aí a folga pode estar cobrando um preço."},
   {"k":"O que ajuda","sc":["Fortalecer,","não frear."],"e":None,"sub":"Músculo forte é a cinta que estabiliza a junta frouxa.","motif":"no",
    "vo":"E a solução não é proibir movimento, é fortalecer: músculo forte funciona como uma cinta que segura a junta mais frouxa. Atividade orientada ajuda muito."},
   {"k":"Passa adiante","sc":["Manda pra um pai","de criança elástica."],"e":None,"sub":"Salva pra lembrar do que observar.","cta":True,
    "vo":"Manda pra aquele pai ou mãe que tem uma criança elástica em casa. E salva pra lembrar do que vale observar."},
  ],
  "caption":cap_ped("Criança que dobra os dedos e as juntas demais costuma ter hipermobilidade — folga articular maior que a média, e na maioria das vezes é benigna (muitos atletas e bailarinos são assim). Tranquilo quando é só flexibilidade, sem dor e sem a junta sair do lugar. Observe se há dor após brincar, cansaço ao andar, quedas frequentes ou mão cansada ao escrever. O que ajuda é fortalecer, não frear o movimento.","#hipermobilidade #flexibilidade #ortopediainfantil")},

 # ───────────── Osso Novo #7 ─────────────
 {"id":"on_artrose_osteotomia","ep":34,"serie":"Osso Novo","temporada":"refazer-e-realinhar","motif_family":"bone",
  "scenes":[
   {"k":"Joelho gasto de um lado","sc":["Dói só por","dentro do joelho."],"e":None,"sub":"Quando o desgaste é de um lado só, existe alternativa à prótese.",
    "vo":"Tem um tipo de dor de joelho bem específica: gasta só de um lado, geralmente o de dentro, na pessoa ainda ativa. Pra essa, nem sempre a resposta é prótese."},
   {"k":"Por que desgasta de um lado","sc":["A perna pende","pra um lado."],"e":None,"sub":"Um eixo levemente torto concentra todo o peso num compartimento.",
    "vo":"Muitas vezes o motivo é o eixo: a perna pende um pouquinho pra dentro, e isso joga quase todo o peso num lado só do joelho. Aquele lado desgasta enquanto o outro está novo."},
   {"k":"A ideia","sc":["Mudar o eixo,","aliviar o gasto."],"e":None,"sub":"A osteotomia realinha a perna e transfere a carga pro lado saudável.",
    "vo":"A osteotomia faz algo elegante: corrige o eixo da perna pra transferir a carga do lado gasto pro lado que ainda está bom. Alivia onde dói usando o que está preservado."},
   {"k":"Pra quem serve","sc":["Mais jovem","e ativo."],"e":"ativo","sub":"Adia a prótese em quem é novo demais pra ela — ganha anos de joelho.",
    "vo":"Serve principalmente pra quem é jovem e ativo demais pra uma prótese. É uma forma de ganhar anos com o próprio joelho, adiando a troca pra mais tarde."},
   {"k":"Não é pra todo mundo","sc":["Depende do eixo","e do desgaste."],"e":None,"sub":"Desgaste dos dois lados ou muito avançado pede outra conduta.","motif":"no",
    "vo":"Mas não é solução universal: se o desgaste já é dos dois lados ou muito avançado, o caminho é outro. Por isso a indicação é individual, medida caso a caso."},
   {"k":"Passa adiante","sc":["Manda pra quem","ouviu só prótese."],"e":None,"sub":"Sendo jovem, vale avaliar a osteotomia. Salva pra lembrar.","cta":True,
    "vo":"Se alguém jovem ouviu que só resta prótese no joelho, manda esse vídeo. Pode valer avaliar a osteotomia antes. E salva pra lembrar."},
  ],
  "caption":cap_rec("Joelho que dói e desgastou só de um lado (em geral o de dentro), numa pessoa ainda ativa, nem sempre precisa de prótese. Muitas vezes a causa é o eixo: a perna pende para um lado e concentra o peso num compartimento, que desgasta enquanto o outro está novo. A osteotomia realinha a perna e transfere a carga para o lado saudável — adiando a prótese em quem é jovem demais para ela. Não é para todos: desgaste dos dois lados ou avançado pede outra conduta. A indicação é individual.","#osteotomia #artrosedejoelho #preservacaoarticular")},

 # ───────────── Pé no Chão #8 ─────────────
 {"id":"pnc_cansa_andar","ep":35,"serie":"Pé no Chão","temporada":"marcha",
  "scenes":[
   {"k":"Vive pedindo colo?","sc":["Cansa de andar","mais que os outros."],"e":None,"sub":"Às vezes é só idade — às vezes o corpo está avisando algo.",
    "vo":"Tem criança que pede colo o tempo todo e cansa de andar bem antes das outras. Quase sempre é coisa de idade, mas de vez em quando o corpo está dando um recado."},
   {"k":"Quando é normal","sc":["Criança pequena","cansa mesmo."],"e":None,"sub":"Perninha curta, passo curto: distância grande cansa — e é esperado.",
    "vo":"Pra criança pequena, cansar é esperado: perna curta dá passo curto, então um passeio que pra você é tranquilo, pra ela é uma maratona. Isso por si só não preocupa."},
   {"k":"O que observar","sc":["Sempre o mesmo","jeito de cansar?"],"e":None,"sub":"Manca ao cansar, protege uma perna, ou regrediu no que já fazia?",
    "vo":"O que vale observar é o padrão: ela manca quando cansa? Protege sempre a mesma perna? Andava bem e de repente piorou? Esses detalhes mudam a conversa."},
   {"k":"Bandeiras","sc":["Dor à noite,","febre, emagrecer."],"e":None,"sub":"Dor noturna persistente, febre, perda de peso ou inchaço: avalie logo.","motif":"no",
    "vo":"Algumas bandeiras pedem avaliação sem demora: dor que acorda à noite toda noite, febre junto, emagrecimento ou uma junta inchada. Aí não é só cansaço."},
   {"k":"O caminho","sc":["Avaliar é","simples."],"e":"simples","sub":"Conversa, exame e, se preciso, um exame dirigido — costuma tranquilizar.",
    "vo":"E a boa notícia: avaliar costuma ser simples. Uma boa conversa, o exame da criança e, se necessário, um exame dirigido. Na maioria das vezes, sai de lá tranquilo."},
   {"k":"Passa adiante","sc":["Manda pra uma mãe","na dúvida do colo."],"e":None,"sub":"Salva pra observar com calma.","cta":True,
    "vo":"Manda pra aquela mãe que não sabe se é manha ou cansaço de verdade. E salva pra observar com calma."},
  ],
  "caption":cap_ped("Criança que vive pedindo colo e cansa de andar mais que as outras geralmente é só idade — perna curta dá passo curto, e distância grande cansa mesmo. Observe o padrão: manca ao cansar? protege sempre a mesma perna? piorou de repente? Bandeiras que pedem avaliação sem demora: dor noturna persistente, febre, perda de peso ou articulação inchada. Avaliar costuma ser simples e tranquilizador.","#desenvolvimentoinfantil #marcha #sinaisdealerta")},

 # ───────────── Osso Novo #8 ─────────────
 {"id":"on_falha_ossea","ep":36,"serie":"Osso Novo","temporada":"quando-o-osso-falha","motif_family":"bone",
  "scenes":[
   {"k":"E quando falta osso?","sc":["Sobrou um vão","sem osso."],"e":None,"sub":"Trauma grave ou infecção podem levar embora um pedaço do osso.",
    "vo":"Tem situações em que não é só uma fratura: falta osso de verdade. Um trauma grave ou uma infecção podem levar embora um pedaço inteiro, deixando um vão. Isso tem nome: falha óssea."},
   {"k":"Não dá pra só aproximar","sc":["Encostar as pontas","encurta a perna."],"e":None,"sub":"Juntar o que sobrou fecharia o vão, mas tiraria comprimento.",
    "vo":"E não dá pra simplesmente encostar as duas pontas: até fecharia o vão, mas a perna ficaria mais curta. Então o desafio é preencher o espaço sem perder comprimento."},
   {"k":"A solução elegante","sc":["O osso caminha","e preenche."],"e":"caminha","sub":"No transporte ósseo, um segmento desliza devagar e gera osso atrás de si.",
    "vo":"A solução é engenhosa: o transporte ósseo. A gente faz um segmento do osso caminhar devagar pelo vão, e atrás dele vai nascendo osso novo. O corpo preenche o buraco sozinho."},
   {"k":"Outras rotas","sc":["Enxerto ou","reforço de estrutura."],"e":None,"sub":"Conforme o caso: enxerto do próprio corpo ou técnicas de reforço.",
    "vo":"Existem outras rotas conforme o tamanho da falha: enxerto de osso do próprio paciente, ou técnicas que dão uma estrutura pra ele crescer. A escolha depende do vão e da pessoa."},
   {"k":"Leva tempo","sc":["Paciência é","parte do plano."],"e":"Paciência","sub":"É um caminho de etapas e acompanhamento — mas o membro se refaz.","motif":"no",
    "vo":"Não vou romantizar: é um caminho de etapas, que pede paciência e acompanhamento de perto. Mas é real, e devolve membro e função onde parecia não ter mais saída."},
   {"k":"Passa adiante","sc":["Manda pra quem","perdeu osso."],"e":None,"sub":"Osso novo, de volta ao movimento. Salva pra lembrar.","cta":True,
    "vo":"Se você conhece alguém que perdeu osso num acidente ou infecção e acha que não tem solução, manda esse vídeo. Existe caminho. E salva pra lembrar."},
  ],
  "caption":cap_rec("Quando não é só fratura, mas FALTA osso (falha óssea) — um trauma grave ou infecção podem levar um pedaço inteiro. Não dá para só encostar as pontas: fecharia o vão, mas encurtaria a perna. A solução elegante é o transporte ósseo: um segmento caminha devagar pelo vão e o corpo gera osso novo atrás dele, preenchendo sem perder comprimento. Há outras rotas (enxerto, técnicas de estrutura) conforme o caso. Leva tempo e etapas — mas devolve membro e função.","#falhaossea #transporteosseo #reconstrucaoossea")},

]
