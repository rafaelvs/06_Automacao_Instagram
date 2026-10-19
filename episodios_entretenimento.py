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
  COMO FUNCIONA: id, formato="como_funciona", serie, familia, cena (módulo em animado/), roteiro[frases],
                 cta (= última frase do roteiro), legenda
`familia` escolhe a menção da legenda (reconstrucao | pediatria).
"""

EPISODIOS_ENTRETENIMENTO = [
    # ------------------------------------------------------------ pilotos aprovados em 18/10/2026
    {
        "id": "cf_alongamento",
        "formato": "como_funciona",
        "serie": "Como funciona",
        "familia": "reconstrucao",
        "cena": "cf_alongamento",
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
]
