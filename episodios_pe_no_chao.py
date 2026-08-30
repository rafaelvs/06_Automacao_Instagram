# -*- coding: utf-8 -*-
"""
Biblioteca de EPISÓDIOS da série "Pé no Chão" (reels narrativos faceless).
Formato: cada episódio = história curta (gancho -> tensão -> desenvolvimento -> payoff -> CTA de SEND).
Cada cena: k=kicker, sc=[2 linhas grandes], e=palavra dourada (ou None), sub=apoio, vo=narração (voz),
motif: "no" desenha o símbolo proibido. Última cena cta=True (otimizada p/ compartilhamento no direct).

MODELO DE VOZ (3 camadas): a TELA mostra a manchete (sc) + apoio (sub); a VOZ (vo) COMPLEMENTA —
acrescenta o porquê, o acolhimento e o tom de conversa, sem repetir o texto. (Decidido 14/06/2026.)

CFM (Res. 2.336/2023): educativo, sem prometer/insinuar resultado, sem paciente real, com disclaimer.
Guardrail: NUNCA alongamento ósseo sob ângulo estético/altura. Tudo aqui é ortopedia pediátrica de
função / desenvolvimento / sinal de alerta. Temas escolhidos por potencial de SEND (pesquisa de demanda).
"""
SERIE = "Pé no Chão"
SIG = "Dr. Rafael Vargas · Médico · CRM-SP 226103 · RQE 137901"
HASH_BASE = "#ortopediapediatrica #ortopediainfantil #saudedacrianca #maternidade #paternidade #ortopediasaopaulo"

def cap(corpo, extra_tags=""):
    return (corpo + "\n\n📤 Manda pra um pai, mãe ou avó que precisa ver. 📌 Salva pra lembrar.\n"
            "💬 Dúvida? Comenta ou chama no direct.\n\n" + HASH_BASE + " " + extra_tags + "\n\n" + SIG)

EPISODES = [
 {"id":"andador","ep":1,"temporada":"quadril",
  "scenes":[
   {"k":"Mito x Verdade","sc":["O andador NÃO","ensina a andar."],"e":"NÃO","sub":"Vou te contar por quê — e o que ajuda de verdade.",
    "vo":"Essa é daquelas que surpreende quase todo mundo. E quando você entende o porquê, não olha mais pro andador do mesmo jeito."},
   {"k":"O que parece","sc":["Parece que ajuda:","a criança se move."],"e":None,"sub":"Mas no andador ela só desliza — empurra com a ponta dos pés.","motif":"no",
    "vo":"Bate aquela sensação de que está ajudando, né? Mas repara: ali ela não anda de verdade, só empurra na ponta do pé e escorrega pra todo lado."},
   {"k":"O que de fato acontece","sc":["Andar de verdade","é equilíbrio."],"e":"equilíbrio","sub":"Equilíbrio se aprende caindo, levantando e firmando o próprio peso.",
    "vo":"Andar mesmo é outra coisa: é equilíbrio. E equilíbrio ninguém ensina. A criança conquista caindo, levantando e segurando o próprio corpo."},
   {"k":"E tem mais","sc":["Em excesso, está","associado a quedas."],"e":"quedas","sub":"E muda a forma como a criança apoia o quadril enquanto ele se forma.",
    "vo":"E tem o outro lado: usado demais, ele aparece ligado a mais quedas. Sem contar que muda o apoio do quadril bem na fase em que ele está se formando."},
   {"k":"O que ajuda","sc":["Chão livre.","Descalço. Tempo."],"e":"Tempo","sub":"O empurrador entra depois, quando ela já fica de pé sozinha.",
    "vo":"O que faz diferença de verdade é o básico: chão livre, pezinho descalço e tempo pra explorar. O empurrador entra mais pra frente, quando ela já fica de pé sozinha."},
   {"k":"Passa adiante","sc":["Manda pra quem","ainda usa andador."],"e":None,"sub":"Um pai, uma mãe, uma avó. Salva pra lembrar.","cta":True,
    "vo":"Se você conhece alguém que ainda usa andador, manda esse vídeo. Um pai, uma mãe ou uma avó vão agradecer."},
  ],
  "caption":cap("Mito x Verdade: o andador NÃO ensina o bebê a andar. Parece que ajuda porque a criança se move — mas ali ela só desliza, empurrando com a ponta dos pés. Andar é equilíbrio, e equilíbrio se aprende sustentando o próprio peso. Usado em excesso, está associado a quedas e muda o apoio do quadril enquanto ele se forma. O que ajuda: chão livre, descalço e tempo; o empurrador entra quando o bebê já fica de pé sozinho.","#andador #primeirospassos #desenvolvimentoinfantil")},

 {"id":"pe_chato","ep":2,"temporada":"pernas",
  "scenes":[
   {"k":"Mito x Verdade","sc":["Pé chato nem","sempre é problema."],"e":"nem","sub":"E quase nunca se resolve com aquela palmilha cara.",
    "vo":"Se você olhou pra sola do pé do seu filho toda encostada no chão e se assustou... respira. Na maior parte das vezes, isso é normal."},
   {"k":"O que quase ninguém conta","sc":["Todo bebê nasce","com pé chato."],"e":None,"sub":"O arco do pé vai se formando sozinho ao longo da infância.",
    "vo":"Todo mundo nasce com o pé assim, planinho. O arco, aquela curvinha embaixo, vai surgindo sozinho com os anos, conforme a criança anda e corre."},
   {"k":"A virada","sc":["Palmilha não","molda o arco."],"e":"não","sub":"Em pé flexível e sem dor, ela costuma ser gasto sem necessidade.","motif":"no",
    "vo":"E o que raramente te contam na loja: a palmilha não esculpe esse arco. Num pé que dobra normal e não dói, ela costuma ser dinheiro jogado fora."},
   {"k":"Quando acender o alerta","sc":["Dói, é rígido","ou só num pé."],"e":None,"sub":"Pé chato que dói, que é duro ou apareceu de repente merece avaliação.",
    "vo":"Existe, sim, a hora de ligar o alerta: se esse pé dói, se é durinho e travado, ou se só um lado é chato. Aí vale passar com o ortopedista."},
   {"k":"Passa adiante","sc":["Antes de comprar","palmilha, avalie."],"e":None,"sub":"Manda pra um pai ou mãe que vai gastar sem precisar.","cta":True,
    "vo":"Então, antes de gastar com palmilha, vale ouvir um especialista. E manda esse vídeo pra aquele pai ou mãe que já tá quase comprando uma."},
  ],
  "caption":cap("Mito x Verdade: pé chato na criança quase nunca é problema. Todo bebê nasce com o pé plano e o arco se forma sozinho ao longo da infância — e a palmilha NÃO molda esse arco. Em pé flexível e sem dor, ela costuma ser gasto desnecessário. O que merece avaliação é o pé que dói, que é rígido ou que ficou chato só de um lado.","#pechato #peplano #palmilha")},

 {"id":"dor_crescimento","ep":3,"temporada":"crescimento",
  "scenes":[
   {"k":"Mito x Verdade","sc":["Dor de crescimento","existe — e é real."],"e":"real","sub":"Não é frescura. Mas tem um padrão que tranquiliza.",
    "vo":"Quem nunca ouviu aquele é só dor de crescimento? Pois é: ela existe mesmo, não é frescura. E o melhor, tem um padrão que dá pra reconhecer e ficar tranquilo."},
   {"k":"O padrão que acalma","sc":["Nas duas pernas,","à noite."],"e":None,"sub":"Costuma vir no fim do dia, sem inchaço e sem febre — e some pela manhã.",
    "vo":"O jeitão clássico é esse: incomoda nas duas perninhas, mais no fim do dia ou de noite, sem inchar e sem febre. E de manhã, já sumiu."},
   {"k":"De manhã","sc":["A criança acorda","e brinca normal."],"e":"normal","sub":"Se à noite doeu mas de dia ela corre e pula, isso fala a favor.",
    "vo":"Aí no dia seguinte ela acorda e sai correndo, brincando normal. Esse contraste, chorou de noite mas pula de dia, é justamente o que tranquiliza."},
   {"k":"Bandeira vermelha","sc":["Só num lugar,","com inchaço."],"e":None,"sub":"Dor numa articulação só, com manqueira, febre ou que persiste: avalie.","motif":"no",
    "vo":"Agora, o sinal de atenção é o oposto: quando dói sempre num ponto só, com inchaço, manqueira ou febre. Aí não é pra esperar, vale avaliar."},
   {"k":"Passa adiante","sc":["Salva pra noite","que bater dúvida."],"e":None,"sub":"E manda pra outra mãe que já passou por essa noite.","cta":True,
    "vo":"Salva isso pra próxima noite de dúvida. E manda pra outra mãe que já perdeu o sono com essa mesma situação."},
  ],
  "caption":cap("Dor de crescimento é real — não é frescura. O padrão que tranquiliza: dói nas DUAS pernas, à noite ou no fim do dia, sem inchaço e sem febre, e some pela manhã, com a criança brincando normal no dia seguinte. A bandeira vermelha é o oposto: dor numa articulação só, com inchaço, febre ou manqueira, ou que persiste — isso merece avaliação.","#dordecrescimento #criancas")},

 {"id":"displasia_quadril","ep":4,"temporada":"quadril",
  "scenes":[
   {"k":"Sinal de alerta","sc":["Um detalhe no","bebê muda tudo."],"e":None,"sub":"O quadril que 'sai do lugar' — e por que achar cedo importa tanto.",
    "vo":"Tem um detalhe no bebê que, se a gente percebe cedo, muda completamente a história. É o quadril que pode sair do lugar."},
   {"k":"O que observar","sc":["Pregas tortas.","Uma perna curta."],"e":None,"sub":"Assimetria nas dobrinhas da coxa ou pernas de tamanhos diferentes.",
    "vo":"Dá pra desconfiar olhando: aquelas dobrinhas da coxa que ficam tortas, diferentes de um lado pro outro, ou uma perna parecendo um tiquinho mais curta."},
   {"k":"Mais um sinal","sc":["A perna abre","menos de um lado."],"e":"menos","sub":"Na troca de fralda, um lado abre menos que o outro.",
    "vo":"E na troca de fralda, presta atenção: se um lado do quadril abre menos que o outro, é um sinal que pede um olhar com calma."},
   {"k":"Por que correr","sc":["Cedo: o suspensório.","Tarde: cirurgia."],"e":None,"sub":"Achado cedo, costuma ser tratado com o suspensório de Pavlik; tardio, complica.",
    "vo":"Por que a pressa? Achado cedo, costuma ser tratado com um suspensório, que vai reposicionando o quadril ao longo de semanas, com acompanhamento de perto. Descoberto tarde, o caminho fica bem mais difícil, às vezes cirúrgico."},
   {"k":"Passa adiante","sc":["Manda pra quem","tem bebê em casa."],"e":None,"sub":"Esse é daqueles que vale demais compartilhar.","cta":True,
    "vo":"Esse aqui vale demais compartilhar. Manda pra quem tem bebê em casa."},
  ],
  "caption":cap("Displasia do desenvolvimento do quadril: achar cedo muda o desfecho. Observe assimetria nas pregas (dobrinhas) da coxa, uma perna parecendo mais curta, ou um lado do quadril que abre menos na troca de fralda. Diagnóstico precoce costuma se resolver com órtese; tardio costuma exigir tratamentos mais complexos. Na dúvida, leve ao ortopedista pediátrico.","#displasiadoquadril #ddq #bebe")},

 {"id":"pernas_tortas","ep":5,"temporada":"pernas",
  "scenes":[
   {"k":"Calma, pais","sc":["Perna torta quase","sempre é fase."],"e":"fase","sub":"Tem até um cronograma — e ele costuma terminar bem.",
    "vo":"Se você acha a perninha do seu filho torta, calma. Quase sempre é fase. E olha que curioso: tem até um cronograma, e ele costuma terminar bem."},
   {"k":"Até os 2 anos","sc":["Arqueada para","fora é comum."],"e":None,"sub":"O famoso 'perninha de cowboy' costuma ser normal nessa idade.",
    "vo":"Até por volta dos 2 anos, é comum a perna arquear pra fora. O famoso jeitinho de cowboy. Pode respirar, faz parte do caminho."},
   {"k":"Dos 3 aos 4","sc":["Vira para dentro,","em X."],"e":"X","sub":"Depois ela inverte e fica em X — e isso também é esperado.",
    "vo":"Depois acontece o contrário: dos 3 aos 4 anos ela costuma virar pra dentro, num formato de X. E isso também é esperado, viu?"},
   {"k":"Por volta dos 7","sc":["Costuma alinhar","sozinha."],"e":"sozinha","sub":"O alerta é só se for assimétrico, doloroso ou persistir depois disso.","motif":None,
    "vo":"Lá pelos 7 anos, costuma alinhar sozinha, sem ninguém fazer nada. O sinal de atenção é só se for diferente de um lado, doer, ou insistir depois dessa idade."},
   {"k":"Passa adiante","sc":["Salva esse","cronograma."],"e":None,"sub":"E manda pra mãe que está achando a perna do filho torta.","cta":True,
    "vo":"Salva esse cronograma pra consultar depois. E manda pra aquela mãe que está achando a perna do filho torta."},
  ],
  "caption":cap("Pernas tortas na infância quase sempre são FASE, com cronograma: até ~2 anos é comum a perna arqueada para fora (varo); dos 3 aos 4 ela inverte e fica em X (valgo); e por volta dos 6–7 costuma alinhar sozinha. O alerta é quando a curvatura é assimétrica (só um lado), dolorosa, ou persiste depois dessa idade — aí vale avaliar.","#pernastortas #genovaro #genovalgo")},

 {"id":"ponta_dos_pes","ep":6,"temporada":"marcha",
  "scenes":[
   {"k":"Sinal de alerta","sc":["Anda na ponta","dos pés?"],"e":None,"sub":"Tem uma idade que separa o 'normal' do 'vale avaliar'.",
    "vo":"Seu filho vive andando na pontinha do pé? Existe uma idade que separa o é normal do vale dar uma olhada. E é isso que muda tudo."},
   {"k":"Nos primeiros anos","sc":["É comum e","costuma passar."],"e":"passar","sub":"Muita criança experimenta andar na ponta — e larga sozinha.",
    "vo":"Nos primeiros anos, isso é super comum e costuma passar sozinho. Um monte de criança experimenta a ponta do pé e larga sem ninguém pedir."},
   {"k":"A linha que importa","sc":["Persistiu depois","dos 3 anos?"],"e":None,"sub":"Se anda na ponta o tempo todo após os 3, vale uma avaliação.",
    "vo":"A linha que importa é essa: se depois dos 3 anos ela ainda anda na ponta o tempo todo, aí sim vale uma avaliação."},
   {"k":"Fique de olho se","sc":["Só faz de um","lado, ou enrijece."],"e":None,"sub":"Um lado só, panturrilha dura ou atraso no andar pedem atenção.","motif":None,
    "vo":"E fica de olho também se é só de um lado, se a panturrilha fica durinha, ou se veio junto com uma demora pra começar a andar."},
   {"k":"Passa adiante","sc":["Guarda a regra","dos 3 anos."],"e":None,"sub":"E manda pra quem vê o filho na pontinha o dia todo.","cta":True,
    "vo":"Guarda a regra dos 3 anos. E manda pra quem vê o filho na pontinha o dia inteiro."},
  ],
  "caption":cap("Andar na ponta dos pés nos primeiros anos é comum e costuma passar sozinho. A regra prática: se PERSISTE o tempo todo depois dos 3 anos, vale avaliar. Acenda o alerta também se for só de um lado, se a panturrilha endurece, ou se veio junto com atraso para andar.","#andarnapontadope #marcha #desenvolvimento")},

 {"id":"pe_torto","ep":7,"temporada":"reconstrucao",
  "scenes":[
   {"k":"Micro-caso","sc":["Imagine um pé","que nasce virado."],"e":None,"sub":"O pé torto congênito — e por que começar cedo muda o desfecho.",
    "vo":"Imagina um pezinho que já nasce virado pra dentro. É o pé torto congênito. Não é frescura, nem culpa de nada na gravidez — e tem um caminho de tratamento que funciona, principalmente quando começa cedo."},
   {"k":"A janela de ouro","sc":["O começo é nas","primeiras semanas."],"e":None,"sub":"Quanto mais cedo, mais o pezinho do bebê coopera.",
    "vo":"A janela de ouro é começar nas primeiras semanas de vida, quando o pé do bebê ainda é molinho e coopera com a gente."},
   {"k":"Como funciona","sc":["Gessos que","corrigem aos poucos."],"e":None,"sub":"O método de Ponseti molda o pé em etapas, com gesso e depois órtese.",
    "vo":"E como corrige? Com gessos que vão moldando o pé aos pouquinhos, em etapas, e depois uma órtese de manutenção pra segurar a correção."},
   {"k":"O desfecho","sc":["Na maioria, sem","grande cirurgia."],"e":None,"sub":"Começando cedo, a maior parte dos casos corrige sem cirurgia grande.",
    "vo":"E começando cedo, a maior parte dos casos corrige sem precisar de uma cirurgia grande."},
   {"k":"Passa adiante","sc":["Manda pra quem","espera um bebê."],"e":None,"sub":"Saber disso antes muda a forma de receber o diagnóstico.","cta":True,
    "vo":"Manda pra quem está esperando um bebê. Saber que existe tratamento desde cedo muda a forma de receber esse diagnóstico."},
  ],
  "caption":cap("Pé torto congênito: o pé já nasce virado para dentro — e a notícia boa é o tratamento. A janela de ouro é começar nas primeiras semanas, com o método de Ponseti: gessos que corrigem o pé aos poucos, depois uma órtese de manutenção. Começando cedo, a maior parte dos casos corrige sem grande cirurgia. Conteúdo educativo; cada caso é avaliado individualmente.","#petorto #ponseti #recemnascido")},

 {"id":"quando_procurar","ep":8,"temporada":"socorros",
  "scenes":[
   {"k":"Salva este","sc":["Quando levar ao","ortopedista infantil?"],"e":None,"sub":"5 sinais que valem uma avaliação — sem pânico, com atenção.",
    "vo":"Quando é hora de levar a criança no ortopedista? Separei cinco sinais que valem uma avaliação. Sem pânico, só atenção."},
   {"k":"Sinais 1 e 2","sc":["Manca, ou evita","pisar num pé."],"e":None,"sub":"Mancar sem motivo claro, ou proteger sempre o mesmo lado.",
    "vo":"Os dois primeiros: quando ela manca sem um motivo claro, ou quando vive protegendo sempre o mesmo pezinho."},
   {"k":"Sinais 3 e 4","sc":["Dor que volta,","ou queda fácil."],"e":None,"sub":"Dor frequente no mesmo lugar, ou tropeços e quedas demais.",
    "vo":"O terceiro e o quarto: dor que insiste em voltar no mesmo lugar, ou tropeços e quedas muito além do esperado pra idade."},
   {"k":"Sinal 5","sc":["Um lado diferente","do outro."],"e":"diferente","sub":"Assimetria: um ombro, um quadril ou uma perna fora do par.",
    "vo":"E o quinto é a assimetria: um ombro, um quadril ou uma perna visivelmente diferente do outro lado."},
   {"k":"Passa adiante","sc":["Salva e manda","pra um pai ou mãe."],"e":None,"sub":"Na dúvida, avaliar cedo costuma simplificar tudo.","cta":True,
    "vo":"Salva e manda pra um pai ou mãe. Na dúvida, avaliar cedo quase sempre simplifica tudo."},
  ],
  "caption":cap("Quando levar ao ortopedista infantil? 5 sinais: 1) manca ou evita pisar num pé; 2) protege sempre o mesmo lado; 3) dor que volta no mesmo lugar; 4) quedas e tropeços demais; 5) assimetria — um ombro, quadril ou perna diferente do outro. Sem pânico: na dúvida, avaliar cedo costuma simplificar tudo.","#ortopediainfantil #sinaisdealerta #quandoprocurar")},
]

# ── ROLLOUT anti-templatização no feed (18/07/2026): layout + paleta rotacionados por id. ──
# Aplica-se SÓ aos episódios PRÓPRIOS do Pé no Chão — roda ANTES dos merges abaixo, então os assets
# mesclados depois ficam FORA: novos/lote já vêm rolados dos próprios módulos; a APRESENTAÇÃO
# (vídeo institucional) e a série PÓS-OP permanecem INTOCADAS (classico). setdefault → opt-in
# explícito por episódio ainda vence. Ver ganchos_layout (layout_para_sequencia / palette_para).
import ganchos_layout as _gl
_sem_lay = [_e for _e in EPISODES if "layout" not in _e]
for _e, _lay in zip(_sem_lay, _gl.layout_para_sequencia([_e["id"] for _e in _sem_lay])):
    _e["layout"] = _lay
for _e in EPISODES:
    _e.setdefault("palette", _gl.palette_para(_e["id"]))

# LOTE 2026: 30 novos episódios narrados (18 "Osso Novo" + 12 "Pé no Chão") encadeados pela
# Arquitetura de Ganchos 2026. Mantidos em módulo próprio p/ diff limpo; aqui só estendemos a lista.
try:
    from episodios_novos_2026 import NEW_EPISODES
    EPISODES = EPISODES + NEW_EPISODES
except Exception as _e:  # nunca quebrar o render dos pilotos se o módulo novo faltar
    print("AVISO: episodios_novos_2026 não carregado:", _e)

# LOTE JULHO/2026: +16 episódios (8 Pé no Chão + 8 Osso Novo) p/ reabastecer a fila de Reels.
try:
    from episodios_lote_julho_2026 import LOTE_JULHO
    EPISODES = EPISODES + LOTE_JULHO
except Exception as _e:
    print("AVISO: episodios_lote_julho_2026 não carregado:", _e)

# SÉRIE "Respondendo" (temporada "Você Perguntou"): +10 reels curtos de P&R intercalados no feed.
try:
    from episodios_qa_respondendo import QA_EPISODES
    EPISODES = EPISODES + QA_EPISODES
except Exception as _e:
    print("AVISO: episodios_qa_respondendo não carregado:", _e)

# VÍDEO DE APRESENTAÇÃO do perfil (Doctoralia) — módulo próprio, mesmo motor.
try:
    from episodio_apresentacao import APRESENTACAO
    EPISODES = EPISODES + APRESENTACAO
except Exception as _e:
    print("AVISO: episodio_apresentacao não carregado:", _e)

# SÉRIE "RECUPERAÇÃO": vídeos pós-operatórios p/ o paciente (YouTube Short + link). Mesmo motor.
try:
    from episodios_pos_op import POS_OP
    EPISODES = EPISODES + POS_OP
except Exception as _e:
    print("AVISO: episodios_pos_op não carregado:", _e)

# TESTE DE RETENÇÃO (30/07/2026): versões curtas (~40s, <=5 cenas) de 3 episódios da "Recuperação".
# Módulo separado de propósito — o POS_OP tem 34 ids e gates que contam esse número.
try:
    from episodios_teste_curto import TESTE_CURTO
    EPISODES = EPISODES + TESTE_CURTO
except Exception as _e:
    print("AVISO: episodios_teste_curto não carregado:", _e)

# SÉRIE "ALONGAMENTO ÓSSEO" (31/07/2026): o nicho core, já no formato curto. Mesmo motor.
try:
    from episodios_alongamento import ALONGAMENTO
    EPISODES = EPISODES + ALONGAMENTO
except Exception as _e:
    print("AVISO: episodios_alongamento não carregado:", _e)

# SÉRIE "Respondendo" LOTE 2 (30/08/2026): +12 episódios de perguntas reais (Doctoralia).
# Aprovado D3 30/08/2026; registro em aprovacoes.json. Mesmo motor.
try:
    from episodios_qa_lote2 import QA_LOTE2
    EPISODES = EPISODES + QA_LOTE2
except Exception as _e:
    print("AVISO: episodios_qa_lote2 não carregado:", _e)

# SÉRIE "Anatomia de um Caso" (30/08/2026): 3 pilotos caso-da-literatura com ilustrações
# esquemáticas por cena (ilustracoes_caso.py). Formato aprovado pelo Rafael 30/08 ("pode
# seguir"); troca "sem amputação"→"a perna foi preservada" registrada no módulo. Mesmo motor.
try:
    from episodios_anatomia_caso import ANATOMIA_CASO
    EPISODES = EPISODES + ANATOMIA_CASO
except Exception as _e:
    print("AVISO: episodios_anatomia_caso não carregado:", _e)

def get(ep_id):
    for e in EPISODES:
        if e["id"]==ep_id: return e
    raise KeyError(ep_id)

if __name__=="__main__":
    print(len(EPISODES),"episódios:")
    for e in EPISODES: print(f"  ep{e['ep']:02d} {e['id']:18s} temporada={e['temporada']:12s} cenas={len(e['scenes'])}")
