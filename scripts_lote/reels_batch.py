# -*- coding: utf-8 -*-
"""Lote de Reels novos (reel04+). Reaproveita o gerador principal e as trilhas em rotacao.
Roda quantas vezes precisar (dedup pula os ja feitos). python reels_batch.py"""
import os, json, glob
from gerar_reels import build_scenes, render_reel, cap, REELS_DIR, AUDIO_DIR, ROOT

REELS=[
 {"id":"reel04","kicker_hook":"Ortopedia Pediátrica","hook":"Pernas em X ou arqueadas: é normal?",
  "points":[
   {"kicker":"Faz parte do crescimento","lines":["Arqueadas até ~2 anos","Em X dos 3 aos 6","Costuma alinhar sozinho"]},
   {"kicker":"Hora de avaliar","lines":["Só de um lado","Piora com a idade","Atrapalha o andar"]}],
  "cta_title":"Na dúvida, avalie.",
  "caption":cap("Joelhos arqueados nos primeiros 2 anos e em X dos 3 aos 6 costumam fazer parte do desenvolvimento e melhoram sozinhos. Vale avaliar na ortopedia pediátrica quando é só de um lado, piora com a idade ou é muito acentuado.","#joelhovalgo #ortopediapediatrica #ortopediainfantil #saudedacrianca #ortopediasaopaulo")},
 {"id":"reel05","kicker_hook":"Ortopedia Pediátrica","hook":"Pé chato na criança preocupa?",
  "points":[
   {"kicker":"Quase sempre não","lines":["Comum nos primeiros anos","O arco se forma com o tempo","Flexível é o esperado"]},
   {"kicker":"Quando olhar de perto","lines":["Dói ou cansa rápido","Pé rígido","Só de um lado"]}],
  "cta_title":"Quer avaliar? Fale comigo.",
  "caption":cap("O pé plano flexível é comum na infância e o arco costuma se formar ao longo do crescimento — geralmente não precisa de palmilha. Vale avaliar na ortopedia pediátrica quando há dor, cansaço fácil, rigidez ou assimetria.","#peplano #pechato #ortopediapediatrica #ortopediainfantil #ortopediasaopaulo")},
 {"id":"reel06","kicker_hook":"Coluna","hook":"Escoliose: como perceber cedo.",
  "points":[
   {"kicker":"Sinais para observar","lines":["Ombros desnivelados","Uma escápula saltada","Cintura assimétrica"]},
   {"kicker":"Teste simples em casa","lines":["A criança inclina à frente","Olhe as costas por trás","Um lado mais alto? Avalie"]}],
  "cta_title":"Notou algo? Avalie.",
  "caption":cap("A escoliose costuma ser indolor no começo — por isso observar a postura ajuda. Ombros ou cintura assimétricos e, ao inclinar o tronco à frente, um lado das costas mais alto merecem avaliação na ortopedia pediátrica. Quanto antes, mais simples o acompanhamento.","#escoliose #colunainfantil #ortopediapediatrica #postura #ortopediasaopaulo")},
 {"id":"reel07","kicker_hook":"Adolescente atleta","hook":"Dor abaixo do joelho que treina muito?",
  "points":[
   {"kicker":"Pode ser Osgood-Schlatter","lines":["Dor logo abaixo da patela","Piora ao correr e saltar","Comum no estirão"]},
   {"kicker":"O que costuma ajudar","lines":["Ajustar a carga de treino","Gelo após atividade","Alongar a coxa"]}],
  "cta_title":"Persistiu? Vamos avaliar.",
  "caption":cap("A doença de Osgood-Schlatter causa dor logo abaixo da patela em adolescentes que treinam, no período do estirão. Costuma melhorar ajustando a carga, com gelo e alongamento. Se a dor persiste ou limita, vale avaliar na ortopedia pediátrica.","#osgoodschlatter #joelho #ortopediadoesporte #adolescente #ortopediasaopaulo")},
 {"id":"reel08","kicker_hook":"Sinal de alerta","hook":"Dor no quadril ou joelho no pré-adolescente.",
  "points":[
   {"kicker":"Por que olhar com atenção","lines":["Dor no joelho pode vir do quadril","Mancar sem trauma claro","Mais comum no estirão"]},
   {"kicker":"Não deixe para depois","lines":["Avaliação precoce importa","Às vezes pede raio-X","Quanto antes, melhor"]}],
  "cta_title":"Procure avaliação.",
  "caption":cap("No pré-adolescente, dor no quadril ou no joelho com claudicação, sem trauma claro, merece avaliação sem demora na ortopedia pediátrica — o joelho às vezes \"avisa\" um problema do quadril. A avaliação precoce faz diferença no resultado.","#quadril #epifisiolise #ortopediapediatrica #sinaldealerta #ortopediasaopaulo")},
 {"id":"reel09","kicker_hook":"Bebê","hook":"Cabecinha sempre virada para o mesmo lado?",
  "points":[
   {"kicker":"Pode ser torcicolo congênito","lines":["Preferência por um lado","Dificuldade de virar","Às vezes um caroço no pescoço"]},
   {"kicker":"Boa notícia","lines":["Tratado cedo responde bem","Alongamentos orientados","Acompanhamento simples"]}],
  "cta_title":"Avalie o pescoço do bebê.",
  "caption":cap("O torcicolo muscular congênito faz o bebê preferir virar a cabeça para um lado, às vezes com um nódulo no pescoço. Identificado cedo, costuma responder bem a alongamentos orientados e acompanhamento na ortopedia pediátrica.","#torcicolo #bebe #ortopediapediatrica #ortopediainfantil #ortopediasaopaulo")},
 {"id":"reel10","kicker_hook":"Primeiros socorros","hook":"Criança não mexe o braço após puxão?",
  "points":[
   {"kicker":"Pode ser \"cotovelo de babá\"","lines":["Comum até ~5 anos","Após puxar o bracinho","A criança segura o braço parado"]},
   {"kicker":"O que fazer","lines":["Não force o movimento","Procure avaliação","A redução é rápida"]}],
  "cta_title":"Na dúvida, avalie.",
  "caption":cap("A pronação dolorosa (\"cotovelo de babá\") acontece quando o bracinho é puxado, comum em crianças pequenas: ela passa a segurar o braço sem mexer. Não force — a correção pelo especialista em ortopedia pediátrica costuma ser rápida.","#cotovelodebaba #pronacaodolorosa #ortopediapediatrica #ortopediainfantil #ortopediasaopaulo")},
 {"id":"reel11","kicker_hook":"Entenda","hook":"Por que fratura de criança é diferente?",
  "points":[
   {"kicker":"A placa de crescimento","lines":["O osso ainda está crescendo","Tem áreas mais frágeis","Consolida mais rápido"]},
   {"kicker":"Por isso","lines":["Avaliação tem cuidado próprio","Acompanhar o crescimento","Cada idade, uma conduta"]}],
  "cta_title":"Dúvidas? Fale comigo.",
  "caption":cap("O osso da criança tem a placa de crescimento (fise), uma região mais frágil e importante. Por isso fraturas infantis têm avaliação e acompanhamento próprios na ortopedia pediátrica — e costumam consolidar mais rápido que no adulto.","#fratura #placadecrescimento #ortopediapediatrica #ortopediainfantil #ortopediasaopaulo")},
 {"id":"reel12","kicker_hook":"Mito x verdade","hook":"Sapato firme ajuda o bebê a andar?",
  "points":[
   {"kicker":"O que a evidência diz","lines":["Descalço fortalece o pé","Andar sente o chão","Sapato é proteção, não suporte"]},
   {"kicker":"Na prática","lines":["Solado flexível","Tamanho confortável","Pé livre em casa"]}],
  "cta_title":"Dúvidas sobre o pezinho? Fale comigo.",
  "caption":cap("Para a maioria dos bebês, andar descalço em casa ajuda a fortalecer o pé e o equilíbrio — algo bem estabelecido na ortopedia pediátrica. O sapato serve de proteção — prefira solado flexível e tamanho confortável, não \"sapato ortopédico\" sem indicação.","#primeirospassos #pedobebe #ortopediapediatrica #mitoouverdade #ortopediasaopaulo")},
 {"id":"reel13","kicker_hook":"Desenvolvimento","hook":"Com que idade a criança anda?",
  "points":[
   {"kicker":"A janela é ampla","lines":["A maioria entre 12 e 15 meses","Alguns só perto dos 18","Cada um no seu tempo"]},
   {"kicker":"Quando avaliar","lines":["Não anda após 18 meses","Perdeu habilidades","Assimetria de movimento"]}],
  "cta_title":"Na dúvida, avalie.",
  "caption":cap("Andar entre 12 e 15 meses é o mais comum, mas a faixa normal vai além. Vale avaliar na ortopedia pediátrica quando a criança não anda após 18 meses, perde habilidades já conquistadas ou mostra assimetria de movimento.","#desenvolvimento #marcos #ortopediapediatrica #ortopediainfantil #ortopediasaopaulo")},
 {"id":"reel14","kicker_hook":"Emergência","hook":"Articulação inchada, quente e com febre?",
  "points":[
   {"kicker":"Não espere","lines":["Pode ser infecção articular","Dor forte e febre","Recusa a mexer o membro"]},
   {"kicker":"O que fazer","lines":["Procure atendimento já","Diagnóstico rápido é crucial","Tratar cedo protege a articulação"]}],
  "cta_title":"Sinais assim? Atendimento imediato.",
  "caption":cap("Articulação subitamente inchada, quente e dolorosa, com febre e recusa a movimentar o membro, pode ser artrite séptica — uma urgência da ortopedia pediátrica. Procure atendimento imediato: o diagnóstico e o tratamento precoces protegem a articulação.","#artriteseptica #emergencia #ortopediapediatrica #sinaldealerta #ortopediasaopaulo")},
 {"id":"reel15","kicker_hook":"Reconstrução e Alongamento Ósseo","hook":"Uma perna mais curta que a outra?",
  "points":[
   {"kicker":"Tem avaliação e caminho","lines":["Pequenas diferenças são comuns","Medimos e acompanhamos","Várias opções de tratamento"]},
   {"kicker":"Depende do caso","lines":["Da diferença e da causa","Da idade e do crescimento","Plano individual"]}],
  "cta_title":"Quer entender o seu caso?",
  "caption":cap("Uma perna mais curta que a outra — a discrepância de membro — é mais comum do que parece. Diferenças pequenas costumam ser bem toleradas; maiores têm opções que vão de palmilha a alongamento, conforme a diferença, a causa, a idade e o crescimento.","#discrepancia #alongamentoosseo #reconstrucaoossea #ortopediapediatrica #ortopediasaopaulo")},
 {"id":"reel16","kicker_hook":"Convivendo com o fixador","hook":"Posso tomar banho com o fixador externo?",
  "points":[
   {"kicker":"Em geral, sim","lines":["Seguindo sua orientação","Secar bem a região dos pinos","Observar vermelhidão"]},
   {"kicker":"Atenção","lines":["Cada caso tem sua regra","Sinal diferente, avise","Mantenha os retornos"]}],
  "cta_title":"Qualquer dúvida, fale comigo.",
  "caption":cap("Na maioria dos casos é possível higienizar a região do fixador externo seguindo a orientação individual: manter limpo, secar bem os pinos e observar vermelhidão ou secreção. Suas orientações valem mais que qualquer regra geral — qualquer sinal diferente, avise.","#fixadorexterno #cuidados #reconstrucaoossea #alongamentoosseo #ortopediasaopaulo")},
 {"id":"reel17","kicker_hook":"Alongamento Ósseo","hook":"Dói durante o alongamento ósseo?",
  "points":[
   {"kicker":"O que esperar","lines":["Desconforto leve é comum","Controlável com a equipe","Cada fase é diferente"]},
   {"kicker":"O acompanhamento ajuda","lines":["Ajustes ao longo do caminho","Fisioterapia junto","Você não fica sozinho"]}],
  "cta_title":"Quer entender as etapas?",
  "caption":cap("Algum desconforto pode aparecer no alongamento ósseo, sobretudo na fase de distração, e costuma ser controlável com o acompanhamento da equipe e fisioterapia. Cada fase tem seu cuidado — o plano é feito para o seu caso.","#alongamentoosseo #reconstrucaoossea #fisioterapia #ortopediasaopaulo #ortopedia")},
 {"id":"reel18","kicker_hook":"Reconstrução Óssea","hook":"Fratura que não cola tem solução?",
  "points":[
   {"kicker":"Chama-se pseudoartrose","lines":["O osso não consolidou","Várias causas possíveis","Tem tratamento"]},
   {"kicker":"O caminho","lines":["Investigar a causa","Estabilizar e estimular o osso","Acompanhar de perto"]}],
  "cta_title":"Convive com isso? Vamos avaliar.",
  "caption":cap("Quando uma fratura não consolida (pseudoartrose), existe caminho: investigar a causa, estabilizar adequadamente e estimular a formação de osso, com acompanhamento próximo. Cada caso tem seu plano.","#pseudoartrose #reconstrucaoossea #ortopedia #ortopediasaopaulo #fratura")},
 {"id":"reel19","kicker_hook":"Reconstrução Óssea","hook":"Como se reconstrói osso após infecção?",
  "points":[
   {"kicker":"Quando há perda óssea","lines":["Primeiro, tratar a infecção","Depois, recompor o osso","Em etapas planejadas"]},
   {"kicker":"Transporte ósseo","lines":["O próprio osso \"caminha\"","Preenche a falha aos poucos","Acompanhamento de perto"]}],
  "cta_title":"Casos complexos têm caminho.",
  "caption":cap("Após infecções com perda óssea, a reconstrução é por etapas: controlar a infecção e, depois, recompor o osso — às vezes com transporte ósseo (técnica de Ilizarov), em que o próprio osso preenche a falha gradualmente. São casos complexos, com plano individual.","#transporteosseo #reconstrucaoossea #osteomielite #ortopedia #ortopediasaopaulo")},
 {"id":"reel20","kicker_hook":"Adulto","hook":"Joelho desalinhado pode desgastar antes?",
  "points":[
   {"kicker":"Por que o eixo importa","lines":["Distribui a carga na cartilagem","Desalinho sobrecarrega um lado","Acelera o desgaste"]},
   {"kicker":"Há o que fazer","lines":["Avaliar o alinhamento","Às vezes corrigir o eixo","Proteger a articulação"]}],
  "cta_title":"Quer avaliar o seu eixo?",
  "caption":cap("O alinhamento das pernas distribui a carga na cartilagem. Um joelho muito desalinhado pode sobrecarregar um lado e acelerar o desgaste. Avaliar o eixo e, em casos selecionados, corrigi-lo (osteotomia) ajuda a proteger a articulação.","#osteotomia #joelho #alinhamento #reconstrucaoossea #ortopediasaopaulo")},
 {"id":"reel21","kicker_hook":"Ortopedia Pediátrica","hook":"Andar com os pés para fora: é problema?",
  "points":[
   {"kicker":"Geralmente não","lines":["Comum no desenvolvimento","Costuma melhorar","Vem da rotação dos ossos"]},
   {"kicker":"Quando avaliar","lines":["Muito assimétrico","Quedas frequentes","Piora com o tempo"]}],
  "cta_title":"Na dúvida, avalie.",
  "caption":cap("Andar com os pés para fora (ou para dentro) costuma fazer parte do desenvolvimento e melhora com o crescimento, refletindo a rotação natural dos ossos. Avalie na ortopedia pediátrica quando é muito assimétrico, causa quedas ou piora.","#marcha #rotacao #ortopediapediatrica #ortopediainfantil #ortopediasaopaulo")},
 {"id":"reel22","kicker_hook":"Saúde óssea","hook":"Vitamina D e ossos fortes na infância.",
  "points":[
   {"kicker":"Por que importa","lines":["Ajuda a fixar o cálcio","Sustenta o crescimento ósseo","Sol e dieta contribuem"]},
   {"kicker":"Na prática","lines":["Avaliação individual","Suplemento só se indicado","Nada de exageros"]}],
  "cta_title":"Dúvidas? Converse comigo.",
  "caption":cap("A vitamina D ajuda o corpo a usar o cálcio e sustenta o crescimento ósseo. Sol e alimentação contribuem, mas a necessidade de suplemento é individual — vale avaliar na ortopedia pediátrica antes de iniciar por conta própria.","#vitaminad #saudeossea #ortopediapediatrica #ortopediainfantil #ortopediasaopaulo")},
 {"id":"reel23","kicker_hook":"Mito x verdade","hook":"Mochila pesada causa escoliose?",
  "points":[
   {"kicker":"O que se sabe","lines":["Não causa escoliose","Pode causar dor e má postura","Peso e uso importam"]},
   {"kicker":"Boas práticas","lines":["Use as duas alças","Ajuste junto às costas","Leve só o necessário"]}],
  "cta_title":"Dúvidas de postura? Fale comigo.",
  "caption":cap("Mochila pesada não causa escoliose, mas pode gerar dor e estimular má postura. Prefira mochila com as duas alças, bem ajustada às costas, levando só o necessário — a regra prática da ortopedia pediátrica é até cerca de 10 a 15% do peso da criança.","#mochila #postura #ortopediapediatrica #mitoouverdade #ortopediasaopaulo")},
 {"id":"reel24","kicker_hook":"Ortopedia Pediátrica","hook":"Pezinho curvo no recém-nascido.",
  "points":[
   {"kicker":"Metatarso aduto","lines":["A parte da frente vira para dentro","Comum e geralmente flexível","Diferente do pé torto"]},
   {"kicker":"O que costuma acontecer","lines":["Muitos melhoram sozinhos","Acompanhar o formato","Tratar se for rígido"]}],
  "cta_title":"Quer avaliar o pé do bebê?",
  "caption":cap("No metatarso aduto, a parte da frente do pé do bebê vira para dentro — é comum, costuma ser flexível e melhora sozinho na maioria. É diferente do pé torto. O acompanhamento define se há necessidade de tratamento.","#metatarsoaduto #pedobebe #ortopediapediatrica #ortopediainfantil #ortopediasaopaulo")},
 {"id":"reel25","kicker_hook":"Acolhimento","hook":"Disseram que não há mais o que fazer?",
  "points":[
   {"kicker":"Vale um segundo olhar","lines":["Casos complexos exigem tempo","Nem sempre é o fim do caminho","Reavaliar pode abrir opções"]},
   {"kicker":"Como trabalho","lines":["Avaliação cuidadosa","Plano realista e honesto","Acompanhamento de perto"]}],
  "cta_title":"Vamos reavaliar juntos.",
  "caption":cap("Em casos complexos de deformidade e reconstrução — pseudoartrose, discrepância de membro, sequelas —, um segundo olhar cuidadoso às vezes revela opções que não pareciam existir. Não prometo milagre — proponho avaliação honesta, plano realista e acompanhamento próximo.","#segundaopiniao #casoscomplexos #reconstrucaoossea #deformidades #ortopediasaopaulo")},
 {"id":"reel26","kicker_hook":"Primeira consulta","hook":"Como é a primeira consulta comigo.",
  "points":[
   {"kicker":"O que acontece","lines":["Escuto a sua história","Examino com calma","Explico em linguagem clara"]},
   {"kicker":"Você sai com","lines":["Entendimento do problema","Plano de próximos passos","Espaço para perguntar"]}],
  "cta_title":"Agende pelo WhatsApp.",
  "caption":cap("Na primeira consulta — seja de reconstrução, alongamento ósseo ou ortopedia pediátrica —, escuto a história, examino com calma e explico o que está acontecendo em linguagem clara. A ideia é você sair entendendo o problema e os próximos passos, com espaço para todas as suas perguntas.","#primeiraconsulta #ortopedia #ortopediapediatrica #reconstrucaoossea #ortopediasaopaulo")},
 {"id":"reel27","kicker_hook":"Ortopedia Pediátrica","hook":"Criança que cansa para andar e sente dor.",
  "points":[
   {"kicker":"Vale investigar quando","lines":["Cansa muito mais que os colegas","Dor que limita o brincar","Mudança no jeito de andar"]},
   {"kicker":"O objetivo","lines":["Entender a causa","Tranquilizar quando é leve","Tratar o que precisa"]}],
  "cta_title":"Na dúvida, avalie.",
  "caption":cap("Criança que cansa muito mais que os colegas, sente dor que limita o brincar ou muda o jeito de andar merece avaliação na ortopedia pediátrica. Muitas vezes é leve e tranquilizamos; quando há algo a tratar, quanto antes melhor.","#dor #marcha #ortopediapediatrica #saudedacrianca #ortopediasaopaulo")},
 {"id":"reel28","kicker_hook":"Deformidades complexas","hook":"Deformidade nas pernas tem correção?",
  "points":[
   {"kicker":"Sim, com planejamento","lines":["Medimos o eixo com precisão","Definimos onde corrigir","Corrigir devagar é mais seguro"]},
   {"kicker":"Guiado e seriado","lines":["Acompanhamento em etapas","Ajustes ao longo do caminho","Foco em função"]}],
  "cta_title":"Quer entender o seu caso?",
  "caption":cap("Deformidades angulares das pernas podem ser corrigidas com planejamento: medir o eixo com precisão, definir o ponto da osteotomia e, muitas vezes, corrigir de forma gradual e acompanhada. O foco é segurança e função.","#deformidades #reconstrucaoossea #alongamentoosseo #ortopedia #ortopediasaopaulo")},
 {"id":"reel29","kicker_hook":"Ossos frágeis","hook":"Criança que fratura com facilidade.",
  "points":[
   {"kicker":"Vale investigar","lines":["Fraturas repetidas sem grande trauma","Histórico na família","Pode haver causa óssea"]},
   {"kicker":"O cuidado","lines":["Avaliação especializada","Acompanhamento ao longo do crescimento","Proteger e fortalecer"]}],
  "cta_title":"Convive com isso? Vamos avaliar.",
  "caption":cap("Fraturas repetidas com pequenos traumas, às vezes com histórico familiar, merecem investigação — pode haver uma condição óssea, como a osteogênese imperfeita. O cuidado é especializado, na ortopedia pediátrica, e acompanha o crescimento.","#osteogeneseimperfeita #ossosfrageis #ortopediapediatrica #ortopediainfantil #ortopediasaopaulo")},
 {"id":"reel30","kicker_hook":"Reconstrução e Alongamento Ósseo","hook":"Quando indicar alongamento ósseo?",
  "points":[
   {"kicker":"Avalia-se caso a caso","lines":["Diferença que incomoda a função","Deformidade associada","Expectativa realista"]},
   {"kicker":"Decisão conjunta","lines":["Conversamos sobre opções","Riscos e benefícios","Plano feito com você"]}],
  "cta_title":"Vamos conversar sobre o seu caso?",
  "caption":cap("A indicação de alongamento ósseo é individual: pesa-se a diferença ou deformidade, o impacto na função e a expectativa realista. É uma decisão conjunta, conversando opções, riscos e benefícios — sem promessas, com plano feito para você.","#alongamentoosseo #reconstrucaoossea #deformidades #ortopedia #ortopediasaopaulo")},
]

def run():
    os.makedirs(REELS_DIR, exist_ok=True)
    rj=os.path.join(ROOT,"reels.json")
    lib=json.load(open(rj,encoding="utf-8")) if os.path.exists(rj) else []
    ids={r["id"] for r in lib}
    tracks=sorted(glob.glob(os.path.join(AUDIO_DIR,"*.mp3"))+glob.glob(os.path.join(AUDIO_DIR,"*.m4a"))+glob.glob(os.path.join(AUDIO_DIR,"*.wav"))+glob.glob(os.path.join(AUDIO_DIR,"*.mp4")))
    made=0
    # indice de rotacao continua a partir do tamanho atual da biblioteca
    for spec in REELS:
        rid=spec["id"]
        if rid in ids: continue
        scenes=build_scenes(spec)
        out=os.path.join(REELS_DIR,rid+".mp4")
        music=tracks[len(lib) % len(tracks)] if tracks else None
        dur=render_reel(scenes,out,music)
        lib.append({"id":rid,"video":"reels/"+rid+".mp4","caption":spec["caption"],
                    "music":os.path.basename(music) if music else None,"dur":dur})
        ids.add(rid); made+=1
        json.dump(lib,open(rj,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
        print("ok",rid,dur,"s |",os.path.basename(music) if music else "mudo",flush=True)
    print("reels total:",len(lib),"| novos nesta rodada:",made)

if __name__=="__main__":
    run()
