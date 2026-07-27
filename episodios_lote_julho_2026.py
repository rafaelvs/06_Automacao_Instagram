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
    "vo":"Joelho em X na criança quase sempre é fase. Dos três aos seis anos, é o desenho normal do crescimento."},
   {"k":"O que acontece","sc":["As perninhas","mudam sozinhas."],"e":None,"sub":"Bebê arqueado, X na pré-escola, alinha perto dos 7.",
    "vo":"As perninhas trocam de forma com a idade e tendem a alinhar perto dos sete."},
   {"k":"O que NÃO ajuda","sc":["Palmilha não","alinha o joelho."],"e":"não","sub":"Em criança saudável, isso não muda o eixo da perna.","motif":"no",
    "vo":"Sapato ou palmilha não endireitam o joelho de criança saudável."},
   {"k":"Quando investigar","sc":["Só um lado,","ou piora."],"e":None,"sub":"X só numa perna, que aumenta, dói ou vem com baixa estatura: avalie.",
    "vo":"Avalie se o X é só de um lado, se piora, dói ou vem com baixa estatura."},
   {"k":"Passa adiante","sc":["Manda pra um pai","preocupado com isso."],"e":None,"sub":"Salva pra lembrar quando bater a dúvida.","cta":True,
    "vo":"Manda pra um pai preocupado com o joelho do filho e salva pra quando a dúvida voltar."},
  ],
  "caption":cap_ped("Joelho em X (geno valgo) na criança quase sempre é fase: entre 3 e 6 anos é o desenho normal do crescimento, e o alinhamento costuma chegar perto dos 7. Sapato e palmilha NÃO endireitam o joelho de uma criança saudável. Merece avaliação na ortopedia pediátrica o X que aparece só num lado, que piora, que dói ou que vem com baixa estatura.","#joelhoemx #genovalgo #desenvolvimentoinfantil")},

 # ───────────── Osso Novo #1 ─────────────
 {"id":"on_consolidacao_viciosa","ep":22,"serie":"Osso Novo","temporada":"refazer-e-realinhar","motif_family":"bone",
  "scenes":[
   {"k":"E quando cola torto?","sc":["O osso colou —","mas entortado."],"e":None,"sub":"Consolidação viciosa. E, na maioria das vezes, tem conserto.",
    "vo":"A fratura colou, mas colou torta. Tem nome, consolidação viciosa, e, na maior parte das vezes, dá pra consertar."},
   {"k":"Por que importa","sc":["Osso torto","sobrecarrega."],"e":"sobrecarrega","sub":"Fora do eixo, o peso vai pro lugar errado e desgasta a junta.",
    "vo":"Não é estética, é mecânica: fora do eixo, o osso sobrecarrega a junta vizinha."},
   {"k":"O conserto","sc":["Cortar e","realinhar."],"e":None,"sub":"A osteotomia corta o osso no ponto certo e devolve o eixo.",
    "vo":"O conserto é a osteotomia: cortar o osso no ponto calculado e girar pro eixo certo."},
   {"k":"Guardrail","sc":["É função,","não estética."],"e":"função","sub":"O objetivo é alinhar a carga e poupar a junta — não embelezar.","motif":"no",
    "vo":"Aqui o objetivo é função: realinhar a carga e proteger a articulação, não a aparência."},
   {"k":"Passa adiante","sc":["Manda pra quem","colou torto."],"e":None,"sub":"Osso novo, de volta ao eixo. Salva pra lembrar.","cta":True,
    "vo":"Se alguém colou torto e acha que não tem jeito, manda o vídeo e salva pra lembrar."},
  ],
  "caption":cap_rec("Osso que colou torto (consolidação viciosa) costuma ter conserto. Não é questão de estética: um eixo errado joga o peso no lugar errado, sobrecarrega a articulação vizinha e acelera o desgaste. O conserto é a osteotomia — cortar o osso no ponto calculado, realinhar e fixar, tudo planejado por imagem (nunca no olhômetro). O objetivo é sempre função: realinhar carga e poupar a junta.","#consolidacaoviciosa #osteotomia #deformidadeossea")},

 # ───────────── Pé no Chão #2 ─────────────
 {"id":"pnc_osgood","ep":23,"serie":"Pé no Chão","temporada":"crescimento",
  "scenes":[
   {"k":"Pais de atleta, atenção","sc":["Caroço dolorido","abaixo do joelho."],"e":None,"sub":"No adolescente que corre e salta, costuma ter nome.",
    "vo":"Carocinho dolorido logo abaixo do joelho, no adolescente que corre e salta, costuma ter nome."},
   {"k":"O que é","sc":["Osgood-","Schlatter."],"e":None,"sub":"A tração do tendão puxa o osso que ainda está crescendo ali.",
    "vo":"Chama Osgood-Schlatter: na fase de estirão, o tendão puxa um osso ainda em formação."},
   {"k":"A boa notícia","sc":["Costuma ser","temporário."],"e":"temporário","sub":"Tende a passar quando o osso amadurece — raramente com cirurgia.",
    "vo":"A boa notícia: costuma ser de fase e passar quando o osso amadurece, raramente com cirurgia."},
   {"k":"O que ajuda","sc":["Dosar o esforço,","gelo, alongar."],"e":None,"sub":"Sem largar o esporte. Se mancar, inchar ou travar: avalie.","motif":"no",
    "vo":"Ajuda dosar o esforço, gelo e alongar, sem largar o esporte. Se mancar, inchar ou travar, avalie."},
   {"k":"Passa adiante","sc":["Manda pro grupo","dos pais do time."],"e":None,"sub":"Salva pra próxima reclamação de joelho.","cta":True,
    "vo":"Manda pro grupo dos pais do time e salva pra próxima reclamação de joelho."},
  ],
  "caption":cap_ped("Caroço dolorido logo abaixo do joelho no adolescente que corre e salta costuma ser Osgood-Schlatter: na fase de estirão, o tendão traciona um ponto de osso ainda em formação. Boa notícia — costuma ser temporário e passar quando o osso amadurece, raramente exigindo cirurgia. Ajuda dosar o esforço (sem largar o esporte), gelo e alongamento orientado. Avalie na ortopedia pediátrica se mancar, inchar muito ou travar.","#osgoodschlatter #dornojoelho #adolescente")},

 # ───────────── Osso Novo #2 ─────────────
 {"id":"on_salvamento_membro","ep":24,"serie":"Osso Novo","temporada":"reconstrucao","motif_family":"bone",
  "scenes":[
   {"k":"A pergunta difícil","sc":["Amputar ou","reconstruir?"],"e":None,"sub":"Em casos graves, essa decisão é real — e é compartilhada.",
    "vo":"Em trauma ou infecção graves, vem uma pergunta dura: salvar o membro ou amputar?"},
   {"k":"Não existe resposta única","sc":["Depende do osso,","do corpo, da vida."],"e":None,"sub":"Extensão da lesão, infecção, circulação e o que a pessoa quer.",
    "vo":"Não existe resposta pronta: pesa a lesão, a infecção, a circulação e a vida da pessoa."},
   {"k":"Reconstruir é possível","sc":["Osso se refaz,","vão se preenche."],"e":"refaz","sub":"Transporte ósseo e fixadores podem reconstruir perdas grandes.",
    "vo":"Reconstruir é possível em muitos casos: transporte ósseo e fixadores refazem grandes perdas de osso, num caminho mais longo, de etapas."},
   {"k":"Amputar não é desistir","sc":["Às vezes é a","melhor função."],"e":None,"sub":"Com prótese, pode devolver autonomia mais rápido e com menos dor.","motif":"no",
    "vo":"E amputar não é desistir: às vezes, com uma boa prótese, devolve autonomia mais rápido."},
   {"k":"Passa adiante","sc":["Manda pra quem","ouviu só amputar."],"e":None,"sub":"Vale uma segunda opinião. Salva pra lembrar.","cta":True,
    "vo":"Se ouviu que só resta amputar, manda o vídeo: uma segunda opinião vale muito. Salva pra lembrar."},
  ],
  "caption":cap_rec("Amputar ou reconstruir? Em casos graves de trauma ou infecção, essa decisão é real — e compartilhada. Não há resposta única: pesa a extensão da lesão, infecção, circulação, saúde geral e o que faz sentido para a vida da pessoa. Reconstruir grandes perdas de osso é possível (transporte ósseo com fixador externo, técnica de Ilizarov), mas costuma ser um caminho de etapas. E amputar não é desistir: às vezes devolve função e autonomia mais rápido. O que guia é a qualidade de vida.","#salvamentodemembro #reconstrucaoossea #segundaopiniao")},

 # ───────────── Pé no Chão #3 ─────────────
 {"id":"pnc_sever","ep":25,"serie":"Pé no Chão","temporada":"crescimento",
  "scenes":[
   {"k":"Dói o calcanhar?","sc":["Criança que joga","bola e reclama."],"e":None,"sub":"Dor no calcanhar no esporte tem uma explicação comum.",
    "vo":"Dor no calcanhar na criança que joga bola, dança ou corre muito tem uma explicação comum."},
   {"k":"O que é","sc":["Doença de","Sever."],"e":None,"sub":"A placa de crescimento do calcanhar inflama com o impacto repetido.",
    "vo":"Chama doença de Sever: o impacto repetido irrita a placa de crescimento do calcanhar."},
   {"k":"Tranquiliza","sc":["Não deixa","sequela."],"e":"Não","sub":"É autolimitada: melhora com o tempo e não estraga o osso.","motif":"no",
    "vo":"O alívio: é dor de fase, não estraga o osso e costuma sumir conforme a criança cresce."},
   {"k":"O que ajuda","sc":["Gelo e calçado","com amortecimento."],"e":None,"sub":"Alongar a panturrilha e dosar o treino. Manca ou dói parado: avalie.",
    "vo":"Ajuda gelo, tênis com amortecimento e alongar a panturrilha. Se mancar, inchar ou doer parado, avalie."},
   {"k":"Passa adiante","sc":["Manda pra outro","pai de atleta."],"e":None,"sub":"Salva pra próxima dor de calcanhar.","cta":True,
    "vo":"Manda pra outro pai de criança no esporte e salva pra próxima dor de calcanhar."},
  ],
  "caption":cap_ped("Dor no calcanhar na criança/pré-adolescente que pratica esporte costuma ser doença de Sever: o impacto repetido irrita a placa de crescimento do calcâneo. Tranquiliza — é autolimitada, melhora com o tempo e não deixa sequela. Ajuda gelo, calçado com amortecimento, calcanheira de silicone, alongar a panturrilha e dosar o treino. Avalie na ortopedia pediátrica se mancar o dia todo, inchar ou doer em repouso.","#doencadesever #dornocalcanhar #esporteinfantil")},

 # ───────────── Osso Novo #3 ─────────────
 {"id":"on_vitamina_d","ep":26,"serie":"Osso Novo","temporada":"viver-o-tratamento","motif_family":"bone",
  "scenes":[
   {"k":"Pergunta comum","sc":["Vitamina ajuda","o osso a colar?"],"e":None,"sub":"Tem papel, sim — mas não do jeito que vendem.",
    "vo":"A vitamina não faz o osso colar feito mágica. Tem papel, mas não é pílula milagrosa."},
   {"k":"O básico que conta","sc":["Cálcio e","vitamina D."],"e":None,"sub":"São a matéria-prima e o pedreiro que coloca o cálcio no osso.",
    "vo":"O que conta é cálcio com vitamina D: o cálcio é o tijolo, a D o coloca no osso."},
   {"k":"Mais não é melhor","sc":["Encher de","cálcio não cola."],"e":"não","sub":"Acima do que o corpo usa, o excesso não acelera — e pode fazer mal.","motif":"no",
    "vo":"Mas mais não é melhor: o excesso não acelera e pode sobrecarregar o rim. Reponha só o que falta, com orientação."},
   {"k":"O que mais pesa","sc":["Não fumar,","comer bem."],"e":None,"sub":"Parar de fumar e ter proteína pesam mais que qualquer cápsula.",
    "vo":"E o que pesa mais que qualquer cápsula: não fumar, controlar diabetes e comer proteína."},
   {"k":"Passa adiante","sc":["Manda pra quem","fraturou agora."],"e":None,"sub":"Salva pra ajustar a dieta da recuperação.","cta":True,
    "vo":"Manda pra quem fraturou agora e salva pra ajustar a alimentação."},
  ],
  "caption":cap_rec("Vitamina ajuda o osso a colar? Tem papel, sim, mas não como pílula mágica. O que conta é o combo cálcio + vitamina D (o tijolo e quem o leva para dentro do osso). Mais NÃO é melhor: acima do que o corpo usa, o excesso não acelera e pode sobrecarregar o rim. O que mais pesa na consolidação — inclusive para evitar a pseudoartrose, a fratura que não cola — é não fumar, controlar o diabetes e ter proteína na dieta. O certo é medir a vitamina D e repor o que falta, com orientação.","#vitaminad #calcio #consolidacaoossea")},

 # ───────────── Pé no Chão #4 ─────────────
 {"id":"pnc_torcicolo","ep":27,"serie":"Pé no Chão","temporada":"sinais-de-alerta",
  "scenes":[
   {"k":"Bebê novinho","sc":["Só olha pra","um lado."],"e":None,"sub":"A cabecinha vive virada sempre pro mesmo lado.",
    "vo":"Bebê que vira a cabeça quase sempre pro mesmo lado merece um olhar cedo."},
   {"k":"O que pode ser","sc":["Torcicolo","do bebê."],"e":None,"sub":"Um músculo do pescoço fica mais encurtado de um lado.",
    "vo":"Pode ser o torcicolo do bebê: um músculo do pescoço fica mais curto de um lado."},
   {"k":"Por que agir cedo","sc":["Quanto antes,","mais simples."],"e":"antes","sub":"Nos primeiros meses costuma resolver só com posição e fisioterapia.",
    "vo":"Quanto mais cedo, mais fácil: nos primeiros meses costuma resolver só com posição e fisioterapia."},
   {"k":"Fique de olho","sc":["Cabeça achatada","de um lado."],"e":None,"sub":"Torcicolo pode vir junto de achatamento do crânio — avalie.","motif":"no",
    "vo":"Fica de olho no crânio: deitar sempre do mesmo lado pode achatar ali. Avalie, não só espere."},
   {"k":"Passa adiante","sc":["Manda pra um pai","ou mãe de recém."],"e":None,"sub":"Quanto antes virem, melhor. Salva pra lembrar.","cta":True,
    "vo":"Manda pra um pai ou mãe de recém-nascido: ver cedo faz diferença. Salva pra lembrar."},
  ],
  "caption":cap_ped("Bebê que vive com a cabeça virada sempre pro mesmo lado pode ter torcicolo congênito: um músculo do pescoço fica encurtado de um lado. Agir cedo é tudo na ortopedia pediátrica — nos primeiros meses costuma resolver só com posição e fisioterapia. Em casa, estimular (com orientação) o lado que ele evita ajuda. Fique de olho no achatamento do crânio, que pode vir junto.","#torcicolo #bebe #desenvolvimentoinfantil")},

 # ───────────── Osso Novo #4 ─────────────
 {"id":"on_diabetes_osso","ep":28,"serie":"Osso Novo","temporada":"quando-o-osso-falha","motif_family":"bone",
  "scenes":[
   {"k":"Pouca gente sabe","sc":["Diabetes mexe","com o osso."],"e":None,"sub":"O açúcar alto atrapalha a fratura colar — e a cirurgia cicatrizar.",
    "vo":"Diabetes mal controlado mexe com o osso: atrapalha a fratura a colar e a ferida a fechar."},
   {"k":"Por quê","sc":["Açúcar alto","trava a obra."],"e":"trava","sub":"Prejudica circulação, defesa e as células que fabricam osso novo.",
    "vo":"O açúcar alto trava a obra: piora a circulação, a defesa e as células que fazem osso."},
   {"k":"O risco extra","sc":["Mais infecção,","cola mais devagar."],"e":None,"sub":"Por isso o controle do açúcar entra no plano cirúrgico.",
    "vo":"Na prática, mais infecção e consolidação lenta. Por isso o controle entra no plano cirúrgico."},
   {"k":"A boa notícia","sc":["Controlado,","o risco cai."],"e":"cai","sub":"Com a glicemia ajustada, a recuperação se aproxima da de qualquer pessoa.","motif":"no",
    "vo":"A boa notícia: controlado, o risco cai muito. Ortopedista e endócrino andam juntos."},
   {"k":"Passa adiante","sc":["Manda pra quem","tem diabetes."],"e":None,"sub":"Vai operar ou fraturou? O controle conta. Salva pra lembrar.","cta":True,
    "vo":"Manda pra alguém com diabetes que vai operar ou fraturou. Salva pra lembrar."},
  ],
  "caption":cap_rec("Pouca gente sabe: o diabetes mal controlado atrapalha a fratura a colar e a cirurgia a cicatrizar. O açúcar alto trava a obra por vários lados — piora circulação, derruba a defesa contra infecção e prejudica as células que fabricam osso novo. Resultado: mais risco de infecção, consolidação mais lenta e até pseudoartrose (a fratura que não cola). A boa notícia: com a glicemia controlada, o risco cai muito. Por isso ortopedista e o cuidado do diabetes caminham juntos.","#diabetes #consolidacaoossea #cicatrizacao")},

 # ───────────── Pé no Chão #5 ─────────────
 {"id":"pnc_engatinhar","ep":29,"serie":"Pé no Chão","temporada":"marcha",
  "scenes":[
   {"k":"Mito x Verdade","sc":["Pular o","engatinhar?"],"e":None,"sub":"Nem todo bebê engatinha — e isso pode ser normal.",
    "vo":"Pular o engatinhar pode ser normal: nem todo bebê engatinha, muitos vão direto pra ficar de pé."},
   {"k":"O que importa","sc":["O que conta é","ele progredir."],"e":"progredir","sub":"Senta, rola, se arrasta, fica de pé — o caminho varia de bebê pra bebê.",
    "vo":"O que conta não é a etapa, é o progresso: sentar, rolar, se arrastar, ficar de pé."},
   {"k":"Engatinhar diferente","sc":["De bumbum","ou de urso."],"e":None,"sub":"Arrastar sentado ou de quatro também conta como locomoção.",
    "vo":"Tem bebê que engatinha de bumbum ou de urso: também vale."},
   {"k":"Quando acender o alerta","sc":["Sempre um lado","do corpo."],"e":None,"sub":"Usar só um lado, rigidez ou perder algo que já fazia: avalie.","motif":"no",
    "vo":"O alerta liga se usa sempre um lado, se as perninhas são muito duras ou molinhas, ou regride."},
   {"k":"Passa adiante","sc":["Manda pra uma","mãe ansiosa."],"e":None,"sub":"Salva pra lembrar nos próximos marcos.","cta":True,
    "vo":"Manda pra aquela mãe ansiosa com os marcos do bebê e salva pra lembrar."},
  ],
  "caption":cap_ped("Pular o engatinhar pode ser normal — nem todo bebê engatinha, e muitos vão direto para o ficar de pé. O que importa não é a etapa exata, é o progresso: sentar, rolar, se arrastar, buscar objetos, ficar de pé. Engatinhar de bumbum ou de urso também conta. Acenda o alerta se usar sempre só um lado do corpo, rigidez/moleza importante, ou perda de habilidades — aí avalie na ortopedia pediátrica.","#engatinhar #marcosdodesenvolvimento #bebe")},

 # ───────────── Osso Novo #5 ─────────────
 {"id":"on_haste_magnetica","ep":30,"serie":"Osso Novo","temporada":"reconstrucao","motif_family":"bone",
  "scenes":[
   {"k":"Tecnologia que impressiona","sc":["Uma haste que","alonga por dentro."],"e":None,"sub":"Sem fixador externo aparente — controlada por ímã.",
    "vo":"Existe uma haste dentro do osso que o alonga aos poucos, sem fixador por fora."},
   {"k":"Como funciona","sc":["Um ímã, fora","do corpo."],"e":None,"sub":"Um controle magnético move a haste milímetros por dia, em casa.",
    "vo":"O controle é magnético: um aparelho na pele move a haste milímetros por dia, em casa."},
   {"k":"Pra quê serve","sc":["Perna mais curta,","falha de osso."],"e":None,"sub":"Discrepância pós-trauma, sequela ou perda óssea — sempre por função.",
    "vo":"Serve pra corrigir uma perna curta e preencher falhas de osso, sempre por função."},
   {"k":"Guardrail, sem rodeio","sc":["Não é sobre","ficar mais alto."],"e":"Não","sub":"Alongar osso é tratamento de discrepância e deformidade — não cosmético.","motif":"no",
    "vo":"Sou direto: não é sobre ficar mais alto. Alongamento ósseo trata discrepância e deformidade, nunca vaidade."},
   {"k":"Passa adiante","sc":["Manda pra quem","tem perna curta."],"e":None,"sub":"Osso novo, de volta ao movimento. Salva pra lembrar.","cta":True,
    "vo":"Manda pra quem convive com uma perna mais curta por trauma. É um tratamento de etapas e paciência, mas existe caminho. Salva pra lembrar."},
  ],
  "caption":cap_rec("Existe uma haste colocada dentro do osso que o alonga aos poucos, controlada por um ímã fora do corpo (sem fixador externo aparente) — milímetros por dia, boa parte em casa. Serve para corrigir uma perna mais curta (encurtamento) pós-trauma/sequela e ajudar a preencher falhas de osso, SEMPRE por função. Deixo claro: alongamento ósseo NÃO é sobre ficar mais alto — é tratamento de discrepância e deformidade, nunca cosmético. E não é mágica: tem fases (alongar, endurecer, reabilitar) e exige paciência.","#alongamentoosseo #discrepancia #reconstrucaoossea")},

 # ───────────── Pé no Chão #6 ─────────────
 {"id":"pnc_calcado_bebe","ep":31,"serie":"Pé no Chão","temporada":"pernas-e-pes",
  "scenes":[
   {"k":"Pergunta de pai","sc":["Bebê precisa","de sapato?"],"e":None,"sub":"Antes de andar, a resposta surpreende.",
    "vo":"Antes de andar, o melhor calçado do bebê é nenhum: o pé descalço fortalece e aprende a equilibrar."},
   {"k":"Quando o sapato entra","sc":["Pra proteger,","ao andar na rua."],"e":None,"sub":"Serve pra proteger do chão da rua — não pra dar suporte.",
    "vo":"O sapato entra quando ela anda na rua, pra proteger, não pra dar suporte."},
   {"k":"Como escolher","sc":["Flexível, leve,","sola fina."],"e":None,"sub":"Que dobre na frente, segure no calcanhar e deixe os dedos livres.",
    "vo":"Escolha flexível, leve, sola fina, firme no calcanhar e com espaço pros dedos."},
   {"k":"O que evitar","sc":["Sapato duro","e ortopédico."],"e":None,"sub":"Em pé saudável, rigidez e bota dura não ajudam — atrapalham.","motif":"no",
    "vo":"E evita o sapato duro e pesado vendido como ortopédico: no pé saudável, só atrapalha."},
   {"k":"Passa adiante","sc":["Manda pra quem","vai montar enxoval."],"e":None,"sub":"Salva antes da próxima compra.","cta":True,
    "vo":"Manda pra aquela amiga grávida montando o enxoval e salva antes da próxima compra de sapatinho."},
  ],
  "caption":cap_ped("Bebê precisa de sapato? Antes de andar, o melhor calçado é o pé descalço — sentir o chão fortalece o pé e treina o equilíbrio (meia antiderrapante resolve o frio). O sapato entra para proteger ao andar na rua, não para dar suporte. Escolha flexível, leve, sola fina, firme no calcanhar e com espaço para os dedos. Evite sapato duro e pesado: no pé saudável, atrapalha — é a orientação atual em ortopedia pediátrica.","#calcadoinfantil #primeirospassos #pedescalco")},

 # ───────────── Osso Novo #6 ─────────────
 {"id":"on_dor_cronica_fratura","ep":32,"serie":"Osso Novo","temporada":"viver-o-tratamento",
  "scenes":[
   {"k":"Já colou, mas dói","sc":["Meses depois,","ainda dói."],"e":None,"sub":"A fratura consolidou e a dor não foi embora. Tem explicações.",
    "vo":"A fratura colou, o exame está bom, mas ainda dói meses depois. Não é frescura: tem causa."},
   {"k":"Vários porquês","sc":["Material, rigidez","ou nervo."],"e":None,"sub":"Pode ser o parafuso incomodando, a junta enrijecida ou um nervo sensível.",
    "vo":"Pode ser uma placa ou parafuso incomodando, a articulação enrijecida ou um nervo sensível na região."},
   {"k":"Investigar, não ignorar","sc":["Dor crônica tem","causa."],"e":"causa","sub":"O caminho é achar de onde vem — avaliação dirigida resolve a maioria.",
    "vo":"O ponto é não ignorar: dor crônica quase sempre tem causa, e a avaliação dirigida costuma encontrar."},
   {"k":"Não normalize a dor","sc":["Conviver nem","sempre é o fim."],"e":None,"sub":"Antes de aceitar a dor pra sempre, vale uma reavaliação.","motif":"no",
    "vo":"E costuma ter o que fazer, conforme a causa: antes de aceitar conviver com dor pra sempre, vale reavaliar."},
   {"k":"Passa adiante","sc":["Manda pra quem","já colou e dói."],"e":None,"sub":"Salva pra levar numa reavaliação.","cta":True,
    "vo":"Manda pra quem colou e segue com dor, e salva pra levar numa reavaliação."},
  ],
  "caption":cap_rec("A fratura colou, o exame está bom, mas meses depois ainda dói — isso não é frescura, costuma ter causa. Pode ser o material (placa/parafuso) incomodando, a articulação enrijecida por imobilidade, ou um nervo mais sensível na região. O caminho é investigar, não ignorar: uma avaliação dirigida encontra a origem na maioria dos casos — e descarta uma pseudoartrose (a fratura que não cola) que tenha passado despercebida. E há tratamento — reabilitação, retirar o implante que incomoda, tratar o ponto sensível. Antes de aceitar conviver com a dor para sempre, reavalie.","#dorcronica #posfratura #reabilitacao")},

 # ───────────── Pé no Chão #7 ─────────────
 {"id":"pnc_hipermobilidade","ep":33,"serie":"Pé no Chão","temporada":"sinais-de-alerta",
  "scenes":[
   {"k":"Criança elástica","sc":["Dobra os dedos","demais?"],"e":None,"sub":"Algumas crianças são naturalmente mais flexíveis. Quase sempre, ok.",
    "vo":"Criança que dobra o dedão até quase encostar no braço quase sempre é só flexibilidade."},
   {"k":"Tem nome","sc":["Hiper-","mobilidade."],"e":None,"sub":"As articulações têm uma amplitude maior que a média.",
    "vo":"Isso tem nome: hipermobilidade. As juntas têm folga maior que a média, e muita gente vive assim."},
   {"k":"Quando é só um charme","sc":["Sem dor, sem","luxação: tranquilo."],"e":"tranquilo","sub":"Flexível, sem dor e sem a junta saindo do lugar costuma ser benigno.",
    "vo":"Quando é só flexibilidade, sem dor e sem a junta sair do lugar, é benigno."},
   {"k":"O que observar","sc":["Dor após brincar","ou cansa fácil."],"e":None,"sub":"Dor recorrente, quedas, cansaço ao andar e mão cansada ao escrever.","motif":"no",
    "vo":"Observe se dói após brincar, se cansa fácil ou a mão cansa ao escrever. Fortalecer ajuda, não frear."},
   {"k":"Passa adiante","sc":["Manda pra um pai","de criança elástica."],"e":None,"sub":"Salva pra lembrar do que observar.","cta":True,
    "vo":"Manda pra um pai de criança elástica e salva pra lembrar do que observar."},
  ],
  "caption":cap_ped("Criança que dobra os dedos e as juntas demais costuma ter hipermobilidade — folga articular maior que a média, e na maioria das vezes é benigna (muitos atletas e bailarinos são assim). Tranquilo quando é só flexibilidade, sem dor e sem a junta sair do lugar. Observe se há dor após brincar, cansaço ao andar, quedas frequentes ou mão cansada ao escrever. O que ajuda é fortalecer, não frear o movimento — com orientação da ortopedia pediátrica.","#hipermobilidade #flexibilidade #ortopediainfantil")},

 # ───────────── Osso Novo #7 ─────────────
 {"id":"on_artrose_osteotomia","ep":34,"serie":"Osso Novo","temporada":"refazer-e-realinhar","motif_family":"bone",
  "scenes":[
   {"k":"Joelho gasto de um lado","sc":["Dói só por","dentro do joelho."],"e":None,"sub":"Quando o desgaste é de um lado só, existe alternativa à prótese.",
    "vo":"Joelho que dói e gastou só de um lado, nem sempre precisa de prótese."},
   {"k":"Por que desgasta de um lado","sc":["A perna pende","pra um lado."],"e":None,"sub":"Um eixo levemente torto concentra todo o peso num compartimento.",
    "vo":"Muitas vezes é o eixo: a perna pende pra dentro e concentra o peso num lado."},
   {"k":"A ideia","sc":["Mudar o eixo,","aliviar o gasto."],"e":None,"sub":"A osteotomia realinha a perna e transfere a carga pro lado saudável.",
    "vo":"A osteotomia corrige o eixo e leva a carga pro lado que ainda está bom."},
   {"k":"Não é pra todo mundo","sc":["Jovem e ativo,","com o eixo torto."],"e":"ativo","sub":"Serve a quem é jovem demais pra prótese; dos dois lados pede outra conduta.","motif":"no",
    "vo":"Serve pra quem é jovem demais pra prótese. Desgaste dos dois lados pede outro caminho."},
   {"k":"Passa adiante","sc":["Manda pra quem","ouviu só prótese."],"e":None,"sub":"Sendo jovem, vale avaliar a osteotomia. Salva pra lembrar.","cta":True,
    "vo":"Se alguém jovem ouviu que só resta prótese, manda o vídeo e salva pra lembrar."},
  ],
  "caption":cap_rec("Joelho que dói e desgastou só de um lado (em geral o de dentro), numa pessoa ainda ativa, nem sempre precisa de prótese. Muitas vezes a causa é o eixo: a perna pende para um lado e concentra o peso num compartimento, que desgasta enquanto o outro está novo. A osteotomia corrige o eixo e realinha a perna, transferindo a carga para o lado saudável — adiando a prótese em quem é jovem demais para ela. Não é para todos: desgaste dos dois lados ou avançado pede outra conduta. A indicação é individual.","#osteotomia #artrosedejoelho #preservacaoarticular")},

 # ───────────── Pé no Chão #8 ─────────────
 {"id":"pnc_cansa_andar","ep":35,"serie":"Pé no Chão","temporada":"marcha",
  "scenes":[
   {"k":"Vive pedindo colo?","sc":["Cansa de andar","mais que os outros."],"e":None,"sub":"Às vezes é só idade — às vezes o corpo está avisando algo.",
    "vo":"Criança que pede colo e cansa de andar antes das outras costuma ser idade, mas às vezes o corpo avisa."},
   {"k":"Quando é normal","sc":["Criança pequena","cansa mesmo."],"e":None,"sub":"Perninha curta, passo curto: distância grande cansa — e é esperado.",
    "vo":"Em criança pequena, cansar é esperado: perna curta dá passo curto, distância vira maratona."},
   {"k":"O que observar","sc":["Sempre o mesmo","jeito de cansar?"],"e":None,"sub":"Manca ao cansar, protege uma perna, ou regrediu no que já fazia?",
    "vo":"Observe o padrão: manca ao cansar? protege sempre a mesma perna? piorou de repente?"},
   {"k":"Bandeiras","sc":["Dor à noite,","febre, emagrecer."],"e":None,"sub":"Dor noturna persistente, febre, perda de peso ou inchaço: avalie logo.","motif":"no",
    "vo":"Bandeiras pra avaliar logo: dor que acorda à noite, febre, emagrecer ou junta inchada."},
   {"k":"Passa adiante","sc":["Manda pra uma mãe","na dúvida do colo."],"e":None,"sub":"Salva pra observar com calma.","cta":True,
    "vo":"Manda pra aquela mãe em dúvida se é manha ou cansaço, salva pra observar."},
  ],
  "caption":cap_ped("Criança que vive pedindo colo e cansa de andar mais que as outras geralmente é só idade — perna curta dá passo curto, e distância grande cansa mesmo. Observe o padrão: manca ao cansar? protege sempre a mesma perna? piorou de repente? Bandeiras que pedem avaliação sem demora: dor noturna persistente, febre, perda de peso ou articulação inchada. Avaliar na ortopedia pediátrica costuma ser simples e tranquilizador.","#desenvolvimentoinfantil #marcha #sinaisdealerta")},

 # ───────────── Osso Novo #8 ─────────────
 {"id":"on_falha_ossea","ep":36,"serie":"Osso Novo","temporada":"quando-o-osso-falha","motif_family":"bone",
  "scenes":[
   {"k":"E quando falta osso?","sc":["Sobrou um vão","sem osso."],"e":None,"sub":"Trauma grave ou infecção podem levar embora um pedaço do osso.",
    "vo":"Nem sempre é só fratura: às vezes falta osso. Um trauma ou infecção leva um pedaço."},
   {"k":"Não dá pra só aproximar","sc":["Encostar as pontas","encurta a perna."],"e":None,"sub":"Juntar o que sobrou fecharia o vão, mas tiraria comprimento.",
    "vo":"Não dá pra só encostar as pontas: fecharia o vão, mas encurtaria a perna."},
   {"k":"A solução elegante","sc":["O osso caminha","e preenche."],"e":"caminha","sub":"No transporte ósseo, um segmento desliza devagar e gera osso atrás de si.",
    "vo":"A solução é o transporte ósseo: um segmento caminha pelo vão e atrás nasce osso novo."},
   {"k":"Leva tempo","sc":["Paciência é","parte do plano."],"e":"Paciência","sub":"É um caminho de etapas e acompanhamento — mas o membro se refaz.","motif":"no",
    "vo":"Não vou romantizar: é um caminho de etapas e paciência, mas devolve membro e função."},
   {"k":"Passa adiante","sc":["Manda pra quem","perdeu osso."],"e":None,"sub":"Osso novo, de volta ao movimento. Salva pra lembrar.","cta":True,
    "vo":"Se alguém perdeu osso e acha que não tem solução, manda esse vídeo. Salva pra lembrar."},
  ],
  "caption":cap_rec("Quando não é só fratura, mas FALTA osso (falha óssea) — um trauma grave ou infecção podem levar um pedaço inteiro. Não dá para só encostar as pontas: fecharia o vão, mas encurtaria a perna. A solução elegante é o transporte ósseo, técnica clássica de Ilizarov: um segmento caminha devagar pelo vão e o corpo gera osso novo atrás dele, preenchendo sem perder comprimento. Há outras rotas (enxerto, técnicas de estrutura) conforme o caso. Leva tempo e etapas — mas devolve membro e função.","#falhaossea #transporteosseo #reconstrucaoossea")},

]

# ── ROLLOUT anti-templatização no feed (18/07/2026): layout + paleta rotacionados por id. ──
# setdefault → opt-in por episódio ainda vence. Já-publicados não mudam (publish.py pula ids
# publicados); vale só p/ reels ainda não renderizados. Ver ganchos_layout / série pós-op.
import ganchos_layout as _gl
_sem_lay = [_e for _e in LOTE_JULHO if "layout" not in _e]
for _e, _lay in zip(_sem_lay, _gl.layout_para_sequencia([_e["id"] for _e in _sem_lay])):
    _e["layout"] = _lay
for _e in LOTE_JULHO:
    _e.setdefault("palette", _gl.palette_para(_e["id"]))
