# -*- coding: utf-8 -*-
"""Episódios da GERAÇÃO NOVA (18/10/2026): formatos CONVERSA e COMO FUNCIONA, renderizados por
`python -m animado.render <id>` (workflow `render-animado.yml`).

Por que um módulo próprio: o portão de aprovação (`checar_aprovacoes.py`) importa todo
`episodios*.py` e confere o hash canônico de cada dict contra `aprovacoes.json`. Mudar uma
vírgula de um episódio já aprovado reprova o portão até nova aprovação — de propósito.

Regras de conteúdo (iguais às do resto do motor): todo fato vem do acervo já aprovado (episódios
anteriores, sequências e carrosséis publicados); CFM 2.336 (sem promessa, sem sensacionalismo,
humor da situação e nunca do paciente, nenhuma complicação vira piada, alongamento NUNCA sob
ângulo de altura/estética); sinal de alarme sempre com a conduta do acervo, nunca o direct.

Campos:
  CONVERSA:      id, formato="conversa", serie, familia, icone, personagem, gancho[2], falas[{quem, texto}],
                 cta, legenda
  COMO FUNCIONA: id, formato="como_funciona", serie, familia, cena (módulo em animado/), gancho[2],
                 roteiro[frases], cta (= última frase do roteiro), legenda,
                 tela[rótulos] = TODO texto que a cena desenha além da legenda karaokê e da identificação
  opcional:      cta_legenda — a CTA da LEGENDA quando a do vídeo usa pronome do personagem ("a gente",
                 "um de nós"): na legenda, assinada pelo médico, o pronome mudaria de dono.
`familia` escolhe a menção da legenda (reconstrucao | pediatria).

`tela` (auditoria 19/10): rótulos como "RAIO-X CONFIRMA" ou um contador "DIA 40" ficavam só no
código da cena, fora do hash de aprovação e do portão CFM. Agora o render anota todo texto
desenhado e RECUSA o vídeo se algo não estiver no episódio; a lista vai para o arquivo-irmão
reels/_preview_<id>.json, que o checar_entretenimento audita.
"""

EPISODIOS_ENTRETENIMENTO = [
    # ------------------------------------------------------------ pilotos aprovados em 18/10/2026
    {
        "id": "cf_alongamento",
        "formato": "como_funciona",
        "serie": "Como funciona",
        "familia": "reconstrucao",
        "cena": "cf_alongamento",
        "gancho": ["CORTAR O OSSO", "DE PROPÓSITO?"],
        # fases: on_tres_fases (latência "alguns dias", distração "o milímetro por dia", consolidação
        # "costuma ser a fase mais longa"); "Z" = o osso dormindo na pausa ("pro osso acordar")
        "tela": ["PELE", "NERVO", "VASO", "DE PROPÓSITO", "Z", "FASE 1", "PAUSA", "alguns dias",
                 "FASE 2", "1 MM", "por dia", "FASE 3", "CONSOLIDAÇÃO", "a fase mais longa"],
        "roteiro": [
            "Pra alongar uma perna mais curta, o primeiro passo é cortar o osso. De propósito.",
            "Um aparelho por fora, o fixador, segura as duas partes.",
            "Alguns dias parado, pro osso acordar. Aí começa a separar: cerca de um milímetro por dia.",
            "E o corpo preenche o espaço com osso novo.",
            "Pele, nervo e vaso esticam junto. Por isso é devagar, de propósito.",
            "Depois, o osso novo endurece. E o aparelho sai.",
            "Manda pra quem não sabia que isso era possível.",
        ],
        "cta": "Manda pra quem não sabia que isso era possível.",
        "legenda": (
            "Pra alongar uma perna mais curta que a outra (discrepância de membro), o primeiro passo é "
            "cortar o osso — de propósito. Depois de alguns dias parado, o fixador externo começa a separar "
            "as partes, cerca de um milímetro por dia, em pequenos ajustes, e o corpo preenche o espaço com "
            "osso novo. Pele, nervo e vaso esticam junto com o osso, e são eles que ditam o limite seguro: por "
            "isso o alongamento ósseo é devagar. Depois vem a consolidação, quando o osso novo endurece o "
            "suficiente para aguentar carga, e o aparelho sai."
        ),
    },
    {
        "id": "cv_fixador",
        "formato": "conversa",
        "serie": "Se pudesse responder",
        "familia": "reconstrucao",
        "icone": "fixador",
        "personagem": "seu fixador",
        "gancho": ["SE O SEU FIXADOR", "PUDESSE RESPONDER…"],
        "falas": [
            {"quem": "P", "texto": "Você engancha em toda calça."},
            {"quem": "F", "texto": "Eu sei. Calça com zíper do lado veste sem esbarrar em mim."},
            {"quem": "P", "texto": "E de noite? Não acho posição."},
            {"quem": "F", "texto": "Travesseiro de apoio embaixo da perna. Ele me protege, e protege a outra perna."},
            {"quem": "P", "texto": "Todo mundo fica olhando."},
            {"quem": "F", "texto": "Deixa olhar. Enquanto isso, eu seguro o seu osso, e ele vai se refazendo."},
            {"quem": "P", "texto": "Quando você vai embora?"},
            {"quem": "F", "texto": "Quem decide quando eu saio é o raio-X. Até lá, limpa meus pinos todo dia, combinado?"},
        ],
        "cta": "Manda pra quem tá convivendo com um de nós.",
        "cta_destaque": ["manda", "nós"],
        "legenda": (
            "Conviver com o fixador externo tem truques: calça com zíper lateral veste sem esbarrar no "
            "aparelho, e um travesseiro de apoio embaixo da perna protege o fixador e a outra perna durante o "
            "sono. A higiene diária dos trajetos dos pinos faz parte da rotina. E quem define quando o fixador "
            "sai é o raio-X, que confirma a fase da consolidação do osso."
        ),
    },
    # ------------------------------------------------------------ lote 1 — 19/10/2026
    # Escrito por roteirista + verificado por refutador adversarial (workflow lote-entretenimento-1):
    # cada fala com fato tem trecho LITERAL do acervo aprovado. cv_gesso_filho: para dedos roxos/frios
    # o acervo tem 3 condutas (PS na hora / retorno imediato / contato no mesmo dia); ficou a MAIS
    # urgente (gesso_pos_op_kids), para não minimizar sinal de alarme. cf_fratura_cola: SEM raio-X
    # simulado (guardrail de exame) e sem formato de calo que o acervo não descreve.
    {
        "id": "cv_gesso_filho",
        "formato": "conversa",
        "serie": "Se pudesse responder",
        "familia": "pediatria",
        "icone": "gesso",
        "personagem": "o gesso do seu filho",
        "gancho": ["SE O GESSO DO SEU", "FILHO RESPONDESSE…"],
        "falas": [
            {"quem": "P", "texto": "Ele quer enfiar a régua em você pra coçar."},
            {"quem": "F", "texto": "Régua não! Arranhão aqui dentro pode infeccionar. Coçou? Ar frio de secador, nunca quente."},
            {"quem": "P", "texto": "Dar banho com você virou uma novela."},
            {"quem": "F", "texto": "Pra mim também. Capa impermeável e nunca me mergulha: molhado, eu perco a função e machuco a pele."},
            {"quem": "P", "texto": "Ele quer guardar carrinho dentro de você."},
            {"quem": "F", "texto": "Não sou garagem! Cobre a minha abertura: brinquedo, areia e migalha não podem cair aqui."},
            {"quem": "P", "texto": "Os dedinhos dele ficaram frios e roxos."},
            {"quem": "F", "texto": "Isso não espera: pronto-socorro na hora, avisando a equipe. Posso estar apertando a circulação."},
        ],
        "cta": "Manda pra quem tem criança engessada em casa.",
        "cta_destaque": ["manda", "engessada"],
        "legenda": (
            "Na ortopedia pediátrica, o gesso protege, mas a rotina da casa muda. Coceira se alivia com "
            "ar frio de secador (nunca quente e nunca com objeto lá dentro), o banho é com capa "
            "impermeável, sem mergulhar o gesso, e a abertura fica coberta para brinquedo, areia ou "
            "migalha não caírem. Dedos roxos, pálidos ou frios, formigamento, inchaço forte, dor que "
            "cresce apesar do remédio, ou a criança muito agitada e chorando sem parar: isso não espera. "
            "Pronto-socorro na hora, avisando a equipe no caminho."
        ),
    },
    {
        "id": "cv_osso",
        "formato": "conversa",
        "serie": "Se pudesse responder",
        "familia": "reconstrucao",
        "icone": "osso",
        "personagem": "seu osso",
        "gancho": ["SE O SEU OSSO", "PUDESSE RESPONDER…"],
        "falas": [
            {"quem": "P", "texto": "Já faz semanas. Por que você não cola logo?"},
            {"quem": "F", "texto": "Calma, cada osso tem seu ritmo. Faço um calo no lugar da fratura, e ele vai ganhando resistência."},
            {"quem": "P", "texto": "E um cigarrinho, atrapalha?"},
            {"quem": "F", "texto": "Pra você, um cigarrinho. Pra mim, vaso apertado e menos sangue e oxigênio. Parar faz diferença."},
            {"quem": "P", "texto": "Como eu sei que você tá colando?"},
            {"quem": "F", "texto": "Pergunta pro raio-X: ele é meu boletim. A cada controle, mostra minha evolução. Não pula nenhum."},
            {"quem": "P", "texto": "Tô me sentindo ótimo. Já posso pisar?"},
            {"quem": "F", "texto": "Pisar conforme a equipe liberar me estimula. O quanto pisar, quem define é o plano, não a coragem."},
        ],
        "cta": "Manda pra quem tá esperando o osso colar.",
        "cta_destaque": ["manda", "colar"],
        "legenda": (
            "Cada osso tem seu ritmo: o tempo de consolidação varia de semanas a meses, sem prazo único. "
            "Na cicatrização, o corpo forma um calo, tecido novo no lugar da fratura, que vai ganhando "
            "resistência com o tempo. O cigarro atrapalha porque a nicotina aperta os vasos e reduz o "
            "sangue e o oxigênio que chegam ao osso; parar durante a recuperação faz diferença. Pisar "
            "conforme a equipe liberar estimula a consolidação, e quem define o quanto pisar é o plano "
            "de tratamento. Quem mostra a evolução são as radiografias seriadas, por isso não pule os "
            "raio-X de controle."
        ),
    },
    {
        "id": "cv_muleta",
        "formato": "conversa",
        "serie": "Se pudesse responder",
        "familia": "reconstrucao",
        "icone": "muleta",
        "personagem": "sua muleta",
        "gancho": ["SE A SUA MULETA", "PUDESSE RESPONDER…"],
        "falas": [
            {"quem": "P", "texto": "Minha axila tá me odiando."},
            {"quem": "F", "texto": "Ela tem razão: o peso vai nas mãos, não nela. Apoiar ali comprime nervo e o braço pode formigar."},
            {"quem": "P", "texto": "Te regulei no olhômetro. Tá bom?"},
            {"quem": "F", "texto": "Tira a prova: em pé, meu topo fica 2 a 3 dedos abaixo da axila, com o cotovelo levemente dobrado."},
            {"quem": "P", "texto": "A escada lá de casa tá me encarando."},
            {"quem": "F", "texto": "Subindo: perna boa primeiro. Descendo: eu e a perna em tratamento primeiro. Corrimão, se tiver."},
            {"quem": "P", "texto": "Hoje bateu coragem. Posso pisar com tudo?"},
            {"quem": "F", "texto": "Adoro a coragem, mas quem decide o quanto você pisa é a sua equipe, não ela. Até lá, conta comigo."},
        ],
        "cta": "Manda pra quem tá de muleta ou cuida de quem tá.",
        "cta_destaque": ["manda", "muleta"],
        "legenda": (
            "Muleta mal ajustada atrapalha. O peso vai nas mãos, não na axila: o apoio axilar comprime "
            "nervos e pode causar formigamento e fraqueza no braço. Em pé, o topo da muleta fica 2 a 3 "
            "dedos abaixo da axila, com o cotovelo levemente dobrado no apoio das mãos. Na escada, a "
            "perna boa sobe primeiro; na descida, vão primeiro as muletas e a perna em tratamento, com "
            "corrimão sempre que existir. E, no pós-operatório ou na reconstrução óssea com fixador "
            "externo, o quanto pisar não é data fixa nem questão de coragem: a liberação de carga é "
            "individual, e quem define é o plano de tratamento, no ritmo da sua equipe."
        ),
    },
    {
        "id": "cv_pinos",
        "formato": "conversa",
        "serie": "Se pudesse responder",
        "familia": "reconstrucao",
        "icone": "pinos",
        "personagem": "seus pinos",
        "gancho": ["SE OS SEUS PINOS", "PUDESSEM RESPONDER…"],
        "falas": [
            {"quem": "P", "texto": "Limpar vocês todo santo dia?"},
            {"quem": "F", "texto": "Todo dia. Mãos lavadas e uma gaze pra cada um: a gente é vizinho, mas não divide gaze."},
            {"quem": "P", "texto": "Um de vocês tá meio vermelhinho."},
            {"quem": "F", "texto": "Calma: reação leve na pele em volta da gente é comum. O que importa é se piora em vez de melhorar."},
            {"quem": "P", "texto": "E se piorar, espero a consulta?"},
            {"quem": "F", "texto": "Não. Pus, mau cheiro, vermelhidão que cresce, dor nova: avisa a equipe cedo. Febre: pronto-socorro."},
            {"quem": "P", "texto": "E se um de vocês parecer frouxo?"},
            {"quem": "F", "texto": "Dá vontade de apertar, a gente sabe. Não aperta por conta própria: avisa logo a equipe."},
        ],
        "cta": "Manda pra quem limpa a gente todo dia.",
        "cta_destaque": ["manda", "gente"],
        "legenda": (
            "Os pinos do fixador externo pedem higiene diária dos trajetos, do jeito que a sua equipe "
            "ensinou: mãos lavadas e um material para cada pino, nunca a mesma gaze de um pino para o "
            "outro. Reação leve na pele ao redor do pino é comum; o que muda a leitura é a evolução. "
            "Secreção com pus ou mau cheiro, vermelhidão que aumenta ou dor nova pedem contato precoce "
            "com a equipe; com febre, pronto-socorro. Pino que parece frouxo: comunique logo a equipe e "
            "não aperte por conta própria."
        ),
    },
    {
        "id": "cf_fratura_cola",
        "formato": "como_funciona",
        "serie": "Como funciona",
        "familia": "reconstrucao",
        "cena": "cf_fratura_cola",
        "gancho": ["QUEM COLA UM", "OSSO QUEBRADO?"],
        "tela": ["COÁGULO", "INFLAMAÇÃO", "ETAPA 1", "EM OBRAS", "CALO ÓSSEO", "OSSO ESTÁVEL", "SANGUE CHEGANDO",
                 "SEM INFECÇÃO", "RESISTÊNCIA", "OSSO MADURO", "1 COÁGULO", "2 CALO", "3 OSSO MADURO",
                 "SEMANAS A MESES", "sem prazo único", "RAIO-X", "RAIO-X CONFIRMA"],
        "roteiro": [
            "Quem cola um osso quebrado? O próprio corpo.",
            "Primeiro, coágulo e inflamação. Faz parte: é a primeira etapa.",
            "Depois, começa a obra: o corpo forma tecido novo, o calo ósseo, uma ponte entre as pontas.",
            "Pra ponte firmar, precisa de osso estável, sangue chegando e nenhuma infecção.",
            "Com o tempo, o calo ganha resistência e vira osso maduro.",
            "Leva semanas a meses. Quem confirma o fim da obra é o raio-X.",
            "Manda pra quem tá esperando o osso colar.",
        ],
        "cta": "Manda pra quem tá esperando o osso colar.",
        "legenda": (
            "Quem cola um osso quebrado é o próprio corpo. A consolidação (o osso colar) vai do coágulo "
            "e da inflamação, que é a primeira etapa, ao calo ósseo, o tecido novo que o corpo forma no "
            "lugar da fratura, e daí ao osso maduro. Para firmar, precisa de um tripé: estabilidade, "
            "sangue chegando e nenhuma infecção. Quando um desses falha, a consolidação emperra. A "
            "estabilidade é o motivo de existirem placas, hastes e fixadores: segurar o osso enquanto "
            "ele cicatriza. Com o tempo, o calo vai ganhando resistência. Leva de semanas a meses, sem "
            "prazo único, e é o raio-X que acompanha e confirma: não pule as consultas de raio-X de "
            "controle.\n\nDor intensa nova, febre, inchaço súbito ou membro que parece estar em ângulo "
            "diferente: pronto-socorro e avise a equipe. Não espere a consulta."
        ),
    },
    # ------------------------------------------------------------ lote 2 — 19/10/2026
    # "temas levemente repetidos, priorizando aqueles que tiveram mais sucesso" (Rafael, 19/10): os
    # temas vêm do ranking refutado (correção de época). Escrito por roteirista + refutado por
    # verificador adversarial (workflow lote-entretenimento-2): cada fala com fato tem trecho LITERAL
    # do acervo aprovado. cv_dor_crescimento: a conduta mais urgente do acervo (febre + manqueira =
    # atendimento no mesmo dia, pnc_mancar_febre) fica para a combinação que a pede.
    {
        "id": "cv_pe_chato",
        "formato": "conversa",
        "serie": "Se pudesse responder",
        "familia": "pediatria",
        "icone": "tenis",
        "personagem": "o tênis do seu filho",
        "gancho": ["SE O TÊNIS DO SEU", "FILHO RESPONDESSE…"],
        "falas": [
            {"quem": "P", "texto": "Paguei caro pra você corrigir o pé chato."},
            {"quem": "F", "texto": "Essa ideia vende muito, mas não corrijo pé: eu protejo. Flexível, leve e no tamanho certo já basta."},
            {"quem": "P", "texto": "E a palmilha que a loja ofereceu?"},
            {"quem": "F", "texto": "Mora aqui dentro e também não esculpe arco. Pé chato flexível e sem dor costuma melhorar crescendo."},
            {"quem": "P", "texto": "Então o que ajuda de verdade?"},
            {"quem": "F", "texto": "Me tirar em casa! É minha folga: tempo descalço, num chão seguro, estimula o pé de verdade."},
            {"quem": "P", "texto": "E quando eu devo me preocupar?"},
            {"quem": "F", "texto": "Se o pé dói, é durinho e travado, ou só um lado é chato: aí vale passar com o ortopedista."},
        ],
        "cta": "Manda pra quem ia gastar achando que corrige.",
        "cta_destaque": ["manda", "corrige"],
        "legenda": (
            "Tênis caro não molda nem corrige o pé da criança: o arco e a musculatura se desenvolvem com o "
            "movimento, andando, correndo, sentindo o chão, e o papel do calçado é proteger: flexível, leve "
            "e no tamanho certo já basta. A palmilha também não molda o arco, e o pé chato (pé plano) "
            "flexível e indolor, na maioria das vezes, melhora com o crescimento, sem tratamento. O que de "
            "fato ajuda não custa nada: tempo descalço em casa, em piso seguro, estimula o pé de verdade. O "
            "que merece avaliação é o pé que dói, que é rígido ou que ficou chato só de um lado."
        ),
    },
    {
        "id": "cv_dor_crescimento",
        "formato": "conversa",
        "serie": "Se pudesse responder",
        "familia": "pediatria",
        "icone": "pernas",
        "personagem": "as pernas do seu filho",
        "gancho": ["SE AS PERNAS DO SEU", "FILHO RESPONDESSEM…"],
        "falas": [
            {"quem": "P", "texto": "Ontem à noite ele chorou de dor nas pernas."},
            {"quem": "F", "texto": "Nas duas, né? No fim do dia ou de noite, sem inchar e sem febre: esse é o nosso jeitão clássico."},
            {"quem": "P", "texto": "E hoje cedo já saiu correndo pela casa."},
            {"quem": "F", "texto": "De noite a gente reclama; de dia, quer pular. É justamente esse contraste que tranquiliza."},
            {"quem": "P", "texto": "Dor de crescimento existe ou é desculpa?"},
            {"quem": "F", "texto": "Existe, e é comum na infância. Não é frescura: nem nossa, nem dele."},
            {"quem": "P", "texto": "E quando não é do crescimento?"},
            {"quem": "F", "texto": "Dor num ponto só, inchaço, manqueira ou febre: não espera, avalia. Mancou com febre? No mesmo dia."},
        ],
        "cta": "Manda pra quem já perdeu o sono com essa dor.",
        "cta_destaque": ["manda", "sono"],
        "legenda": (
            "Dor de crescimento existe, é comum na infância e não é frescura. O padrão que tranquiliza: dói "
            "nas duas pernas, no fim do dia ou à noite, sem inchaço e sem febre, e some pela manhã, com a "
            "criança brincando normal no dia seguinte. Fogem desse padrão e merecem avaliação na ortopedia "
            "pediátrica: dor sempre no mesmo ponto; inchaço, calor ou febre junto; e dor que invade o dia, "
            "fazendo mancar, limitar o brincar ou acordar sempre. Com febre e manqueira juntas, procure "
            "atendimento no mesmo dia."
        ),
    },
    {
        "id": "cv_perna_curta",
        "formato": "conversa",
        "serie": "Se pudesse responder",
        "familia": "reconstrucao",
        "icone": "fita",
        "personagem": "a fita métrica",
        "gancho": ["SE A FITA MÉTRICA", "PUDESSE RESPONDER…"],
        "falas": [
            {"quem": "P", "texto": "Vou medir essa perna mais curta com você."},
            {"quem": "F", "texto": "Comigo? Sou de costura, não de osso! Osso se mede no milímetro: exame de imagem, a escanometria."},
            {"quem": "P", "texto": "Deu diferença. Vai ter que operar?"},
            {"quem": "F", "texto": "Nem sempre. Pequena costuma pedir palmilha e observação. Maior pode ter indicação de correção."},
            {"quem": "P", "texto": "E se for criança, que ainda tá crescendo?"},
            {"quem": "F", "texto": "Aí nem uma medida só basta, imagina eu. Mede e remede, prevendo a diferença no fim do crescimento."},
            {"quem": "P", "texto": "E quando eu me preocupo?"},
            {"quem": "F", "texto": "Mancar novo ou piorando, dor no quadril ou na coluna, diferença crescendo rápido: procure avaliação."},
        ],
        "cta": "Manda pra quem convive com essa diferença.",
        "cta_destaque": ["manda", "diferença"],
        "legenda": (
            "Uma perna mais curta que a outra (discrepância de membro) se mede com exame de imagem, não no "
            "olho nem na fita métrica: a escanometria mostra no milímetro o comprimento real de cada osso. E "
            "nem sempre precisa operar: diferenças pequenas costumam ser conduzidas com palmilha de "
            "compensação e observação, e as maiores podem ter indicação de correção, conforme a magnitude, a "
            "idade e a causa. Na criança, que ainda cresce, mede-se e remede-se ao longo do tempo, prevendo "
            "a diferença no final do crescimento. Mancar que apareceu ou piorou, dor no quadril ou na "
            "coluna, ou diferença que aumenta rápido na criança: procure avaliação."
        ),
    },
    # cf_transporte_osseo: caso da literatura tratado por OUTRA equipe (Pentela et al., J Orthop Case Rep
    # 2023) — atribuição na tela o vídeo inteiro, "ilustração esquemática", desfecho honesto (1,5 cm de
    # encurtamento e rigidez no tornozelo) e a fonte na legenda. cf_osteomielite: tom sóbrio, bactéria não
    # vira personagem; conduta pós-cirurgia = infeccao_ferida_curto (aprovado 30/07). Cenas construídas,
    # revisadas por revisor adversarial e corrigidas (workflow cenas-lote2-como-funciona, 19/10).
    {
        "id": "cf_transporte_osseo",
        "formato": "como_funciona",
        "serie": "Como funciona",
        "familia": "reconstrucao",
        "cena": "cf_transporte_osseo",
        "gancho": ["FALTAVAM 17 CM", "DE OSSO. E AGORA?"],
        "tela": [
            "Caso real da literatura",
            "tratado por outra equipe",
            "ilustração esquemática",
            "17 cm",
            "osso da canela (tíbia)",
            "fixador de Ilizarov",
            "corte no osso saudável",
            "DE PROPÓSITO",
            "UM PEDAÇO VIAJA",
            "osso novo",
            "atrás do segmento",
            "4 MESES",
            "aos poucos",
            "TRANSPORTE ÓSSEO",
            "mesmo princípio do alongamento ósseo",
            "OSSO",
            "COMPRIMENTO",
            "FUNÇÃO",
            "neste caso: ficou 1,5 cm",
            "de encurtamento e rigidez",
            "no tornozelo",
            "cada caso é único",
            "Caso publicado, tratado por outra equipe",
        ],
        "roteiro": [
            "Caso real: ele perdeu dezessete centímetros do osso da canela num acidente.",
            "Com o fixador de Ilizarov segurando a perna, os médicos cortaram o osso saudável. De propósito.",
            "O pedaço cortado foi deslizando, devagarinho, pra dentro da falha.",
            "Atrás dele, no rastro, o corpo fabricava osso novo.",
            "Quatro meses assim. É o transporte ósseo, o mesmo princípio do alongamento.",
            "O objetivo é devolver osso, comprimento e função.",
            "Manda pra quem acha que falta de osso não tem solução.",
        ],
        "cta": "Manda pra quem acha que falta de osso não tem solução.",
        "legenda": (
            "Ele perdeu 17,2 cm do osso da canela (tíbia) num acidente de trânsito. Caso real publicado na "
            "literatura médica, tratado por outra equipe."
            "\n\n"
            "Com o fixador circular de Ilizarov, os médicos cortaram o osso saudável e foram puxando o "
            "segmento aos poucos, por 4 meses, para dentro da falha. Atrás dele, o corpo fabricava osso "
            "novo. É o transporte ósseo: a mesma osteogênese por distração do alongamento ósseo, usada para "
            "vencer perdas grandes de osso depois de trauma ou infecção, num tratamento longo, em etapas. O "
            "objetivo é devolver osso, comprimento e função. Reconstrução de função, nunca estética."
            "\n\n"
            "O desfecho, com a parte honesta: ele voltou ao trabalho andando sem apoio e a perna foi "
            "preservada, mas ficou com 1,5 cm de encurtamento e uma contratura de 10° no tornozelo. Cada "
            "caso é único: este é o relato de um paciente, publicado pelos médicos que o trataram. As "
            "ilustrações são esquemáticas, não são imagens do paciente."
            "\n\n"
            "Fonte: Pentela HK, Harshavardhan JKG, Suriyakumar S. Journal of Orthopaedic Case Reports, "
            "2023;13(5):9-13."
        ),
    },
    {
        "id": "cf_osteomielite",
        "formato": "como_funciona",
        "serie": "Como funciona",
        "familia": "reconstrucao",
        "cena": "cf_osteomielite",
        "gancho": ["OSSO TAMBÉM", "PEGA INFECÇÃO?"],
        "tela": [
            "OSTEOMIELITE",
            "infecção no osso",
            "PORTAS DE ENTRADA",
            "FRATURA EXPOSTA",
            "CIRURGIA",
            "SANGUE",
            "POR DENTRO",
            "DOR QUE NÃO PASSA",
            "INCHAÇO",
            "CALOR",
            "VERMELHIDÃO",
            "ÀS VEZES FEBRE",
            "OU SECREÇÃO",
            "NÃO IGNORE",
            "1 COMBATER A INFECÇÃO",
            "2 REMOVER O OSSO DOENTE",
            "3 RECONSTRUIR, SE SOBRAR VÃO",
            "OSSO DOENTE",
            "VÃO",
            "SEMPRE INDIVIDUALIZADO",
            "DEPOIS DA CIRURGIA",
            "FEBRE",
            "PUS",
            "FERIDA QUE ABRIU",
            "VERMELHIDÃO SE ALASTRANDO",
            "PRONTO-SOCORRO NA HORA",
            "AVISE A EQUIPE",
        ],
        "roteiro": [
            "Osso também pega infecção? Pega. Tem nome: osteomielite.",
            "Pode entrar por fratura exposta, cirurgia ou pelo sangue.",
            "Instalada, pode ir destruindo o osso por dentro.",
            "Dor que não passa, inchaço, calor, vermelhidão, às vezes febre ou secreção: não ignore.",
            "Tem tratamento: combater a infecção, remover o osso doente e, se sobrar um vão, reconstruir.",
            "Operou e veio febre, pus, ferida que abriu ou vermelhidão se alastrando? Pronto-socorro na hora, avisando a equipe.",
            "Manda pra quem operou há pouco.",
        ],
        "cta": "Manda pra quem operou há pouco.",
        "legenda": (
            "O osso também pega infecção: a osteomielite. Ela pode entrar por uma fratura exposta, depois de "
            "uma cirurgia, ou até viajar pelo sangue, vinda de uma infecção em outro lugar do corpo. Quando "
            "se instala, pode ir destruindo o osso por dentro. Sinais comuns: dor que não passa, inchaço, "
            "calor e vermelhidão no local, às vezes febre ou secreção. Não é pra ignorar. Tem tratamento: "
            "combater a infecção, remover o osso doente e, quando sobra um vão, reconstruir o que se perdeu "
            "com as técnicas do alongamento ósseo, sempre de forma individualizada. Sem resolver a infecção, "
            "nenhuma reconstrução se sustenta. Após infecções com perda óssea, a reconstrução é por etapas: "
            "controlar a infecção e depois recompor o osso, às vezes com transporte ósseo."
            "\n\n"
            "Depois de uma cirurgia, se houver febre, pus, ferida que abriu ou vermelhidão se alastrando "
            "pela pele: pronto-socorro na hora, avisando a equipe no caminho."
        ),
    },
    {
        "id": "cf_pe_virado",
        "formato": "como_funciona",
        "serie": "Como funciona",
        "familia": "pediatria",
        "cena": "cf_pe_virado",
        "gancho": ["ANDAR DE POMBINHO?", "PODE SER A COXA."],
        "tela": [
            "PRA DENTRO",
            "?",
            "PÉ",
            "CANELA",
            "COXA",
            "ROTAÇÃO NATURAL",
            "PRA FORA",
            "NA MAIORIA DAS VEZES",
            "SOZINHO",
            "SÓ DE UM LADO",
            "DOR",
            "QUEDAS DEMAIS",
            "PIORA EM VEZ",
            "DE MELHORA",
            "VALE O ORTOPEDISTA OLHAR",
        ],
        "roteiro": [
            "Andar de pombinho: o pé vira pra dentro.",
            "De onde vem? Pode ser um leve giro no pé, na canela ou até na coxa.",
            "Costuma ser a rotação natural dos ossos na infância, pra dentro ou pra fora.",
            "Com o crescimento, na maioria das vezes, o pé alinha sozinho.",
            "O alerta: só de um lado, dor, quedas demais, ou piora em vez de melhora.",
            "Aí vale o ortopedista olhar.",
            "Manda pra quem se preocupa com o andar de pombinho.",
        ],
        "cta": "Manda pra quem se preocupa com o andar de pombinho.",
        "legenda": (
            "Pé pra dentro ao andar, o famoso andar de pombinho. Pode vir de uma leve torção (um giro) do "
            "pé, da canela ou do osso da coxa, todas variações comuns do crescimento, bem conhecidas da "
            "ortopedia pediátrica. Costuma refletir a rotação natural dos ossos, que na infância faz muitos "
            "pés virarem para dentro (ou para fora). A regra é o tempo: conforme a criança cresce, a rotação "
            "costuma se ajustar sozinha, na maioria das vezes sem precisar de tratamento."
            "\n\n"
            "No bebê existe também o metatarso aduto, em que a parte da frente do pé vira para dentro: é "
            "comum, costuma ser flexível e é diferente do pé torto. O acompanhamento define a necessidade de "
            "tratamento."
            "\n\n"
            "O alerta é quando ocorre só de um lado, dói, causa quedas demais, ou piora em vez de melhorar. "
            "Aí vale o ortopedista olhar. Para a consulta, vídeos curtos do andar, de frente e de costas, "
            "ajudam: o celular mostra o que a criança nem sempre repete no consultório."
        ),
    },
    # ------------------------------------------------------------ lote 3 — 19/10/2026 (só COMO FUNCIONA)
    # "você precisa de produzir mais conteudos como o de alongamento para poder deixar essa serie de
    # responder vez ou outra somente" (Rafael, 19/10). Fatos SÓ de fonte publicada ou de lote aprovado
    # (lab/lote3/fontes.json; o lote LEGADO-PRE-GATE pendente de ratificação não vale): 152 fontes
    # conferidas literalmente. Roteirista + verificador adversarial (workflow lote-3-como-funciona) e
    # cena construída, revisada por revisor adversarial e corrigida (cenas-lote3-como-funciona).
    {
        "id": "cf_eixo_perna",
        "formato": "como_funciona",
        "serie": "Como funciona",
        "familia": "reconstrucao",
        "cena": "cf_eixo_perna",
        "gancho": ["TODA PERNA TEM", "UMA LINHA"],
        "tela": [
            "LINHA INVISÍVEL",
            "O EIXO",
            "PESO",
            "REPARTE O PESO",
            "CARGA DEMAIS",
            "UM LADO",
            "ANTES DA HORA",
            "NO ADULTO",
            "NÃO SE AJEITA SOZINHA",
            "OSTEOTOMIA",
            "OSTEO = OSSO",
            "TOMIA = CORTE",
            "CORTE PLANEJADO",
            "MEDE O EIXO",
            "ONDE",
            "QUANTO",
            "EIXO CERTO",
            "FIXA",
            "JÁ ALINHADO",
            "REORGANIZAR",
            "A CARGA",
            "FUNÇÃO, NUNCA ESTÉTICA",
        ],
        "roteiro": [
            "Toda perna tem uma linha invisível: o eixo.",
            "Perna alinhada reparte o peso no joelho.",
            "Torta, joga carga demais num lado. E pode desgastar antes da hora.",
            "No adulto, quando entorta, não se ajeita sozinha.",
            "O caminho costuma ser a osteotomia: um corte planejado no osso.",
            "Antes, mede o eixo e define onde e quanto corrigir.",
            "Corta, reposiciona no eixo certo e fixa, pra cicatrizar já alinhado. É reorganizar a carga.",
            "Manda pra quem convive com uma perna torta.",
        ],
        "cta": "Manda pra quem convive com uma perna torta.",
        "legenda": (
            "Toda perna tem um eixo, e o alinhamento das pernas distribui a carga na cartilagem. Na "
            "deformidade angular, o eixo do osso está desviado: um osso fora de eixo joga carga demais num "
            "canto da articulação, pode sobrecarregar um lado e acelerar o desgaste. No adulto, a perna "
            "torta não se ajeita sozinha e costuma vir de uma fratura que colou torta (a consolidação "
            "viciosa, quando o osso cola, mas torto), de sequelas antigas ou de desgaste. O caminho costuma "
            "ser a osteotomia (osteo = osso, tomia = corte), um corte planejado no osso: antes, mede-se o "
            "eixo e define-se o ponto da osteotomia; depois, o osso é cortado, reposicionado no eixo certo e "
            "fixado para cicatrizar alinhado, e às vezes a correção é gradual, com um aparelho. O objetivo é "
            "um membro alinhado e funcional: função, nunca estética."
            "\n\n"
            "Perna que muda de forma, ou desconforto ao apoiar que não melhora: procure avaliação."
        ),
    },
    {
        "id": "cf_fixador_circular",
        "formato": "como_funciona",
        "serie": "Como funciona",
        "familia": "reconstrucao",
        "cena": "cf_fixador_circular",
        "gancho": ["QUE GAIOLA É ESSA", "NA PERNA?"],
        "tela": [
            "FIXADOR CIRCULAR",
            "DE ILIZAROV",
            "PINOS",
            "ATÉ O OSSO",
            "ANÉIS",
            "SEGURA O OSSO",
            "POR FORA DA PELE",
            "AOS POUQUINHOS",
            "SEM REABRIR A CADA ETAPA",
            "CORTE ÓSSEO",
            "PLANEJADO",
            "ENDIREITA",
            "ALONGA",
            "ALONGAMENTO ÓSSEO",
            "PUXA UM PEDAÇO DE OSSO",
            "TRANSPORTE ÓSSEO",
            "FALHA",
            "O RITMO É DA EQUIPE",
            "NADA DE APERTAR PEÇA",
            "POR CONTA PRÓPRIA",
            "COSTUMA SAIR",
            "QUANDO O OSSO CUMPRE SEU PAPEL",
        ],
        "roteiro": [
            "Essa gaiola tem nome: fixador circular, de Ilizarov.",
            "Pinos atravessam até o osso, presos nos anéis.",
            "Ele segura o osso por fora da pele.",
            "Como fica por fora, ajusta aos pouquinhos, sem reabrir a cada etapa.",
            "Endireita, alonga e até puxa um pedaço de osso pra dentro de uma falha.",
            "O ritmo é da equipe: nada de apertar peça por conta própria.",
            "O aparelho costuma sair quando o osso cumpre seu papel.",
            "Manda pra quem se assustou com esse aparelho.",
        ],
        "cta": "Manda pra quem se assustou com esse aparelho.",
        "legenda": (
            "Aquela “gaiola” de metal na perna é o fixador circular tipo Ilizarov, um fixador externo: pinos "
            "que atravessam até o osso, presos nos anéis, seguram o osso por fora da pele enquanto ele cura "
            "ou se reconstrói. Por ficar por fora, dá para ajustar aos poucos, sem reabrir a cada etapa: a "
            "partir de um corte ósseo planejado, ele permite corrigir o ângulo do osso, fazer o alongamento "
            "ósseo e até o transporte ósseo, puxando um segmento do próprio osso para dentro de uma falha. "
            "Ele trata fraturas complexas, deformidades e a discrepância de membro (uma perna mais curta que "
            "a outra), sempre para devolver função, nunca por estética. O ajuste segue um ritmo programado, "
            "orientado pela equipe: não aperte nem mexa nas peças por conta própria e, se um pino parecer "
            "frouxo, comunique logo a equipe. Nos pinos, o cuidado é diário: reação leve na pele é comum, "
            "mas pus, mau cheiro, vermelhidão que cresce ou dor nova pedem que você avise cedo a equipe; com "
            "febre, pronto-socorro. É uma ferramenta precisa e temporária: costuma sair quando o osso cumpre "
            "seu papel."
        ),
    },
    {
        "id": "cf_gesso_placa",
        "formato": "como_funciona",
        "serie": "Como funciona",
        "familia": "reconstrucao",
        "cena": "cf_gesso_placa",
        "gancho": ["GESSO, PLACA", "OU HASTE?"],
        "tela": [
            "SE MEXE DEMAIS, NÃO COLA",
            "QUEM SEGURA?",
            "?",
            "GESSO",
            "IMOBILIZA",
            "PLACA E PARAFUSOS",
            "HASTE",
            "POR DENTRO DO OSSO",
            "FIXADOR",
            "PINOS ATÉ O OSSO",
            "POR FORA",
            "QUEM DECIDE É O CASO",
            "COLOU?",
            "TIRAR A PLACA?",
            "NEM SEMPRE",
            "a decisão é do cirurgião",
        ],
        "roteiro": [
            "Osso quebrado só cola firme se ficar estável. Se mexe demais, não cola.",
            "Então alguém segura o osso enquanto cicatriza.",
            "Pode ser o gesso, que imobiliza. Ou placa e parafusos.",
            "Ou uma haste, por dentro do osso.",
            "Ou o fixador: pinos atravessam até o osso, presos numa estrutura por fora.",
            "Qual deles? Quem decide é o caso, não a moda.",
            "Colou? Tirar a placa nem sempre é necessário.",
            "Manda pra quem tá com gesso, placa, haste ou fixador.",
        ],
        "cta": "Manda pra quem tá com gesso, placa, haste ou fixador.",
        "legenda": (
            "Quem segura o osso quebrado enquanto ele cicatriza? A consolidação óssea precisa de "
            "estabilidade (osso que se mexe demais não cola), e por isso existem o gesso, que imobiliza, e "
            "as placas, hastes e fixadores: a haste fica por dentro do osso, e no fixador externo os pinos "
            "vão até o osso, presos numa estrutura por fora da pele. A escolha não é preferência: quem "
            "decide é o caso. Depois que o osso colou, a retirada da placa e dos parafusos (o material de "
            "síntese) nem sempre é necessária; quando indicada, tem um tempo próprio, e a decisão é do "
            "cirurgião que acompanha o caso, com apoio das radiografias. Dor intensa nova, febre, inchaço "
            "súbito ou membro que parece estar em ângulo diferente: pronto-socorro e avise a equipe, sem "
            "esperar a consulta. Com gesso, dedos roxos, pálidos ou frios, formigamento, inchaço forte ou "
            "dor que cresce apesar do remédio também não esperam: pronto-socorro na hora, avisando a equipe "
            "no caminho."
        ),
    },
    {
        "id": "cf_pseudartrose",
        "formato": "como_funciona",
        "serie": "Como funciona",
        "familia": "reconstrucao",
        "cena": "cf_pseudartrose",
        "gancho": ["CIGARRO ATRASA", "O OSSO A COLAR?"],
        "tela": [
            "CIGARRO",
            "ATRASA",
            "TRIPÉ",
            "FIRMEZA",
            "SANGUE CHEGANDO",
            "NENHUMA INFECÇÃO",
            "NICOTINA",
            "APERTA OS VASOS",
            "MENOS SANGUE E OXIGÊNIO",
            "CURA LENTA OU NENHUMA",
            "A PONTE NÃO FECHA",
            "PONTO QUE MEXE",
            "FALSA JUNTA",
            "PSEUDARTROSE",
            "a fratura que não cola",
            "RISCO MAIOR",
            "ESTABILIZAR MELHOR",
            "ESTIMULAR O OSSO",
            "CASO A CASO",
            "PARAR DE FUMAR",
            "FAZ DIFERENÇA",
        ],
        "roteiro": [
            "Cigarro atrasa o osso a colar? Atrasa.",
            "Pra colar, precisa de um tripé: firmeza, sangue chegando e nenhuma infecção.",
            "A nicotina aperta os vasos: chega menos sangue e oxigênio.",
            "Pouco sangue, cura lenta ou nenhuma.",
            "Às vezes, a ponte não fecha: fica um ponto que mexe. Uma falsa junta.",
            "É a pseudartrose. Quem fuma tem risco maior.",
            "Tem caminho: estabilizar melhor, estimular o osso. E parar de fumar faz diferença.",
            "Manda pra quem fuma e tá esperando o osso colar.",
        ],
        "cta": "Manda pra quem fuma e tá esperando o osso colar.",
        "legenda": (
            "Cigarro atrasa o osso a colar, sim: o tabagismo está entre os fatores que retardam a "
            "consolidação óssea. Para colar, o osso precisa de um tripé: estabilidade, sangue chegando e "
            "nenhuma infecção. A nicotina aperta os vasos e reduz o oxigênio e o sangue que chegam ao osso. "
            "Quando a consolidação falha, vira pseudartrose, a fratura que não cola: o osso fica com "
            "mobilidade onde deveria estar firme, uma 'falsa junta', e quem fuma tem risco maior. Tem "
            "caminho, sempre caso a caso: estabilizar melhor, estimular o osso e, às vezes, refazer o "
            "trecho; parar de fumar durante a recuperação também faz diferença, e vale conversar com a sua "
            "equipe. Dor que persiste no local da fratura meses depois, ou a sensação de que a perna não "
            "sustenta: leve para avaliação com quem trata reconstrução óssea."
        ),
    },
    {
        "id": "cf_pe_torto",
        "formato": "como_funciona",
        "serie": "Como funciona",
        "familia": "pediatria",
        "cena": "cf_pe_torto",
        "gancho": ["PÉ TORTO SE", "CORRIGE COM GESSO?"],
        "tela": [
            "PÉ TORTO CONGÊNITO",
            "PRA BAIXO",
            "PRA DENTRO",
            "É COMUM",
            "NÃO É CULPA",
            "GESSOS",
            "aos poucos",
            "MANIPULAÇÃO SUAVE",
            "TROCA O GESSO",
            "GESSO APÓS GESSO",
            "COMEÇAR CEDO",
            "FLEXIBILIDADE DO BEBÊ",
            "ÓRTESE",
            "pra manter",
            "ACOMPANHAMENTO",
            "no crescimento",
        ],
        "roteiro": [
            "O pé torto já nasce virado: pra baixo e pra dentro.",
            "É comum, e não é culpa de nada na gravidez.",
            "Quem corrige? Gessos, aos poucos, começando nas primeiras semanas de vida.",
            "Uma manipulação suave, e o gesso. Troca o gesso, e o pé corrige mais um pouco.",
            "Gesso após gesso. Começar cedo aproveita a flexibilidade do bebê.",
            "Depois, uma órtese pra manter. E o acompanhamento segue no crescimento.",
            "Manda pra quem recebeu esse diagnóstico.",
        ],
        "cta": "Manda pra quem recebeu esse diagnóstico.",
        "legenda": (
            "O pé torto congênito (equinovaro) já nasce com o pé virado para baixo e para dentro. É comum e "
            "não tem relação com algo feito na gestação. O tratamento começa nas primeiras semanas de vida, "
            "com manipulação suave e gessos seriados (método de Ponseti): trocas de gesso que corrigem o pé "
            "aos poucos, em etapas. Começar cedo aproveita a flexibilidade do bebê; depois vem uma órtese de "
            "manutenção, e o acompanhamento segue no crescimento. Com o gesso, dedos roxos, pálidos ou "
            "frios, inchaço forte ou a criança muito agitada e chorando sem parar: isso não espera. "
            "Pronto-socorro na hora, avisando a equipe no caminho."
        ),
    },
    {
        "id": "cf_escoliose",
        "formato": "como_funciona",
        "serie": "Como funciona",
        "familia": "pediatria",
        "cena": "cf_escoliose",
        "gancho": ["A COLUNA ENTORTA", "E NÃO DÓI?"],
        "tela": [
            "ESCOLIOSE",
            "COLUNA",
            "COSTUMA NÃO DOER",
            "NO COMEÇO",
            "O SINAL ESTÁ NAS COSTAS",
            "CURVA PRO LADO",
            "E GIRA JUNTO",
            "?",
            "NÃO HÁ PROVA",
            "DE QUE CAUSE ESCOLIOSE",
            "O TESTE",
            "PÉS JUNTOS",
            "JOELHOS ESTICADOS",
            "TRONCO INCLINADO À FRENTE",
            "BRAÇOS SOLTOS",
            "OLHE AS COSTAS POR TRÁS",
            "UM LADO MAIS ALTO",
            "ROTAÇÃO DA COLUNA",
            "SINAL, NÃO DIAGNÓSTICO",
            "LEVE PARA AVALIAÇÃO",
            "COM O ORTOPEDISTA",
            "NO ESTIRÃO",
            "PODE MUDAR MAIS RÁPIDO",
        ],
        "roteiro": [
            "A escoliose costuma não doer no começo. O sinal está nas costas.",
            "A coluna faz uma curva pro lado. E gira junto.",
            "Mochila? Não há prova de que cause escoliose.",
            "O teste: pés juntos, joelhos esticados, tronco inclinado à frente.",
            "Olhe as costas por trás. Um lado mais alto é a rotação da coluna aparecendo.",
            "Sinal, não diagnóstico: leve para avaliação com o ortopedista.",
            "No estirão, a curva pode mudar mais rápido.",
            "Manda pra quem tem filho no estirão.",
        ],
        "cta": "Manda pra quem tem filho no estirão.",
        "legenda": (
            "A escoliose costuma não doer no começo, por isso o sinal é visual: é um desvio em curva da "
            "coluna, visto por trás, e a coluna gira junto. O teste das costas: a criança fica de pé, pés "
            "juntos, e inclina o tronco para a frente com os braços soltos e os joelhos esticados; você olha "
            "as costas por trás. Um lado mais alto que o outro é a rotação da coluna aparecendo, e é sinal, "
            "não diagnóstico. Com o sinal presente, ou na dúvida, leve para avaliação: quem confirma, decide "
            "se pede exame e define a conduta é o ortopedista. No estirão de crescimento, a curva da "
            "escoliose pode mudar mais rápido; em casa, olhe as costas de tempos em tempos. Quanto à "
            "mochila, o peso exagerado causa, sim, dor nas costas e ombros, mas não há prova de que ela "
            "cause escoliose ou deformidade permanente."
        ),
    },
    {
        "id": "cf_quadril_bebe",
        "formato": "como_funciona",
        "serie": "Como funciona",
        "familia": "pediatria",
        "cena": "cf_quadril_bebe",
        "gancho": ["O TESTE DO PEZINHO", "NÃO DETECTA ISSO."],
        "tela": [
            "ENCAIXE",
            "DISPLASIA",
            "CABEÇA DO FÊMUR",
            "NÃO ENCAIXA BEM",
            "TESTE DO PEZINHO",
            "NÃO DETECTA",
            "EXAME DO BEBÊ",
            "ÀS VEZES, COM ULTRASSOM",
            "NA TROCA DE FRALDA",
            "DOBRINHAS DA COXA DIFERENTES",
            "PERNA PARECENDO MAIS CURTA",
            "UM LADO QUE ABRE MENOS",
            "NA DÚVIDA",
            "ORTOPEDISTA PEDIÁTRICO",
            "ACHADO CEDO",
            "SUSPENSÓRIO DE PAVLIK",
            "REPOSICIONA O QUADRIL",
            "AO LONGO DE SEMANAS",
            "com acompanhamento de perto",
        ],
        "roteiro": [
            "O quadril é um encaixe.",
            "Na displasia, a cabeça do fêmur não encaixa bem, desde cedo.",
            "O teste do pezinho não detecta.",
            "A avaliação é no exame do bebê, às vezes com ultrassom.",
            "Na troca de fralda, repare: dobrinhas da coxa diferentes, perna parecendo mais curta, um lado que abre menos.",
            "Na dúvida, leve ao ortopedista pediátrico.",
            "Achado cedo, costuma ser tratado com um suspensório que reposiciona o quadril ao longo de semanas.",
            "Manda pra quem tem bebê em casa.",
        ],
        "cta": "Manda pra quem tem bebê em casa.",
        "legenda": (
            "Na displasia do desenvolvimento do quadril, a cabeça do fêmur não se encaixa bem desde cedo, e "
            "o teste do pezinho não detecta isso. A avaliação é clínica e, às vezes, com ultrassom: por isso "
            "o exame do bebê pelo ortopedista faz diferença. Na troca de fralda, observe assimetria nas "
            "pregas (dobrinhas) da coxa, uma perna parecendo mais curta, um lado do quadril que abre menos "
            "ou um clique no quadril. Identificar nos primeiros meses costuma tornar o tratamento mais "
            "simples: achado cedo, costuma ser tratado com o suspensório de Pavlik, um aparelho que "
            "reposiciona o quadril ao longo de semanas, com acompanhamento de perto. Na dúvida, leve ao "
            "ortopedista pediátrico."
        ),
    },
    {
        "id": "cf_placa_crescimento",
        "formato": "como_funciona",
        "serie": "Como funciona",
        "familia": "pediatria",
        "cena": "cf_placa_crescimento",
        "gancho": ["ONDE O OSSO", "DA CRIANÇA CRESCE?"],
        "tela": [
            "?",
            "ÁREA DE CARTILAGEM",
            "PLACA DE CRESCIMENTO",
            "fise",
            "MAIS FRÁGIL",
            "OSSO JÁ FORMADO",
            "FRATURA",
            "ACIDENTE GRAVE",
            "FIM DO CRESCIMENTO",
            "DO LADO BOM",
        ],
        "roteiro": [
            "Onde o osso da criança cresce? Numa área de cartilagem, a placa de crescimento.",
            "É por ali que o osso aumenta.",
            "Só que ela é mais frágil que o osso já formado.",
            "Fratura ali pede acompanhamento mais cuidadoso, pro osso crescer alinhado.",
            "Num acidente grave, lesão nessa cartilagem pode deixar a perna mais curta.",
            "Por isso: acompanhar até o fim do crescimento.",
            "Do lado bom: osso de criança costuma colar mais rápido.",
            "Manda pra quem tem criança ativa.",
        ],
        "cta": "Manda pra quem tem criança ativa.",
        "legenda": (
            "O osso da criança cresce pela placa de crescimento (fise), uma área de cartilagem por onde o "
            "osso aumenta, mais frágil que o osso já formado. Por isso, fraturas infantis têm avaliação "
            "própria na ortopedia pediátrica: quando a fratura envolve a placa, o acompanhamento é mais "
            "cuidadoso para o osso crescer alinhado. Depois de um acidente grave, a lesão da cartilagem de "
            "crescimento em quem ainda cresce pode levar a uma discrepância de membro (perna mais curta), e "
            "por isso fraturas importantes pedem acompanhamento até o fim do crescimento. Do lado bom, o "
            "osso da criança costuma consolidar mais rápido que no adulto."
            "\n\n"
            "Na criança, o que parece “só torção” às vezes é uma fratura que não aparece fácil; dor "
            "exatamente sobre o osso, não apoiar o pé ou inchaço importante: avalie, pode precisar de "
            "imagem. Deformidade visível, osso exposto, dormência ou pé/mão muito pálido: emergência, vá ao "
            "pronto-socorro."
        ),
    },
]
