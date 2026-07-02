# -*- coding: utf-8 -*-
"""Lote 1 de posts novos (post25-43). Reaproveita o renderer de gerar_conteudo.py.
python posts_batch1.py -> renderiza em images/ e anexa a posts.json (dedup)."""
import os, json
from gerar_conteudo import pslide, cap, IMG, ROOT, SIG
A="arraste →"; NL="\n\n"

POSTS=[
 ("post25",[
   {"variant":"dark","kicker":"Ortopedia Pediátrica","title":"Pernas em X ou arqueadas","tag":A,"tsize":72},
   {"variant":"light","kicker":"O que é","title":"Quase sempre, parte do crescimento","body":"Joelhos arqueados até cerca dos 2 anos e em X dos 3 aos 6 são comuns e costumam alinhar sozinhos.","tsize":66},
   {"variant":"dark","kicker":"Como acompanhar","title":"Observar a evolução","body":"O importante é ver se melhora com o tempo, comparando os dois lados ao longo do crescimento.","tsize":74},
   {"variant":"light","kicker":"Quando avaliar","title":"Sinais de atenção","body":"Quando é muito acentuado, só de um lado, piora com a idade ou vem com dor e quedas.","tsize":70},
   {"variant":"dark","kicker":"Converse comigo","title":"Na dúvida, avalie","body":"Tire suas dúvidas pelo WhatsApp — link na bio.","foot":SIG,"tsize":76}],
  cap("Joelhos arqueados nos primeiros anos e em X dos 3 aos 6 costumam fazer parte do desenvolvimento e melhoram sozinhos. Vale avaliar na ortopedia pediátrica quando é muito acentuado, assimétrico, piora com a idade ou vem com dor.","#joelhovalgo #joelhovaro #ortopediapediatrica #ortopediainfantil #ortopediasaopaulo")),
 ("post26",[
   {"variant":"dark","kicker":"Ortopedia Pediátrica","title":"Pé chato na criança","tag":A,"tsize":80},
   {"variant":"light","kicker":"O que é","title":"O arco se forma com o tempo","body":"Nos primeiros anos o pé costuma ser plano e flexível. O arco tende a aparecer ao longo do crescimento.","tsize":70},
   {"variant":"dark","kicker":"Mito","title":"Nem todo pé chato pede palmilha","body":"O pé plano flexível e sem dor geralmente não precisa de tratamento — só acompanhamento.","tsize":68},
   {"variant":"light","kicker":"Quando avaliar","title":"Se dói ou é rígido","body":"Dor, cansaço fácil, pé que não se move bem ou assimetria merecem avaliação.","tsize":74},
   {"variant":"dark","kicker":"Converse comigo","title":"Quer avaliar o pezinho?","body":"Fale comigo pelo WhatsApp — link na bio.","foot":SIG,"tsize":76}],
  cap("O pé plano flexível é comum na infância e o arco costuma se formar com o crescimento — geralmente sem necessidade de palmilha. Avalie na ortopedia pediátrica quando há dor, cansaço, rigidez ou assimetria.","#peplano #pechato #ortopediapediatrica #ortopediainfantil #ortopediasaopaulo")),
 ("post27",[
   {"variant":"dark","kicker":"Coluna","title":"Escoliose: perceber cedo","tag":A,"tsize":74},
   {"variant":"light","kicker":"O que observar","title":"Assimetrias na postura","body":"Ombros desnivelados, uma escápula mais saltada ou a cintura torta podem ser sinais.","tsize":74},
   {"variant":"dark","kicker":"Teste simples","title":"Inclinar o tronco à frente","body":"Olhe as costas por trás: se um lado fica mais alto, vale uma avaliação.","tsize":74},
   {"variant":"light","kicker":"Por que cedo","title":"Acompanhar o crescimento","body":"Identificada cedo, a escoliose costuma ter acompanhamento mais simples durante o estirão.","tsize":70},
   {"variant":"dark","kicker":"Converse comigo","title":"Notou algo? Avalie","body":"Agende pelo WhatsApp — link na bio.","foot":SIG,"tsize":76}],
  cap("A escoliose costuma ser indolor no início. Observe ombros e cintura assimétricos e, ao inclinar o tronco à frente, um lado das costas mais alto. Quanto antes a avaliação na ortopedia pediátrica, mais simples o acompanhamento.","#escoliose #colunainfantil #ortopediapediatrica #postura #ortopediasaopaulo")),
 ("post28",[
   {"variant":"dark","kicker":"Adolescente atleta","title":"Dor abaixo do joelho","tag":A,"tsize":78},
   {"variant":"light","kicker":"O que costuma ser","title":"Osgood-Schlatter","body":"Dor logo abaixo da patela em quem treina, no período do estirão. Costuma ser benigna.","tsize":74},
   {"variant":"dark","kicker":"O que ajuda","title":"Ajustar a carga","body":"Equilibrar treino e descanso, gelo após a atividade e alongar a coxa costumam aliviar.","tsize":78},
   {"variant":"light","kicker":"Quando avaliar","title":"Se limita ou persiste","body":"Dor que atrapalha o esporte, não melhora ou trava o joelho merece avaliação.","tsize":74},
   {"variant":"dark","kicker":"Converse comigo","title":"Vamos avaliar?","body":"Fale comigo pelo WhatsApp — link na bio.","foot":SIG,"tsize":80}],
  cap("A doença de Osgood-Schlatter causa dor abaixo da patela em adolescentes que treinam, no estirão. Costuma melhorar ajustando a carga, com gelo e alongamento. Se persiste ou limita, vale avaliar na ortopedia pediátrica.","#osgoodschlatter #joelho #ortopediadoesporte #adolescente #ortopediasaopaulo")),
 ("post29",[
   {"variant":"dark","kicker":"Sinal de alerta","title":"Dor no quadril do pré-adolescente","tag":A,"tsize":58},
   {"variant":"light","kicker":"Atenção","title":"O joelho às vezes avisa o quadril","body":"Dor no joelho ou coxa, com mancar e sem trauma claro, pode ter origem no quadril.","tsize":62},
   {"variant":"dark","kicker":"Por que não esperar","title":"Avaliação precoce importa","body":"Algumas condições do quadril nessa idade pedem diagnóstico rápido para um bom resultado.","tsize":62},
   {"variant":"light","kicker":"A conduta","title":"Exame e, às vezes, raio-X","body":"O exame clínico e, quando indicado, a radiografia ajudam a esclarecer.","tsize":72},
   {"variant":"dark","kicker":"Converse comigo","title":"Procure avaliação","body":"Fale comigo pelo WhatsApp — link na bio.","foot":SIG,"tsize":80}],
  cap("No pré-adolescente, dor no quadril, coxa ou joelho com claudicação e sem trauma claro merece avaliação sem demora na ortopedia pediátrica — o joelho às vezes \"avisa\" um problema do quadril. A avaliação precoce faz diferença.","#quadril #epifisiolise #ortopediapediatrica #sinaldealerta #ortopediasaopaulo")),
 ("post30",[
   {"variant":"dark","kicker":"Bebê","title":"Cabeça sempre para o mesmo lado","tag":A,"tsize":62},
   {"variant":"light","kicker":"O que pode ser","title":"Torcicolo congênito","body":"O bebê prefere virar a cabeça para um lado e às vezes há um nódulo no músculo do pescoço.","tsize":66},
   {"variant":"dark","kicker":"Boa notícia","title":"Cedo, responde bem","body":"Identificado nos primeiros meses, costuma melhorar com alongamentos orientados.","tsize":76},
   {"variant":"light","kicker":"Por que avaliar","title":"Evitar assimetrias","body":"O acompanhamento ajuda a prevenir achatamento da cabeça e preferências posturais.","tsize":70},
   {"variant":"dark","kicker":"Converse comigo","title":"Avalie o pescoço do bebê","body":"Fale comigo pelo WhatsApp — link na bio.","foot":SIG,"tsize":70}],
  cap("O torcicolo muscular congênito faz o bebê preferir um lado, às vezes com um nódulo no pescoço. Identificado cedo na ortopedia pediátrica, costuma responder bem a alongamentos orientados, prevenindo assimetrias.","#torcicolo #bebe #ortopediapediatrica #ortopediainfantil #ortopediasaopaulo")),
 ("post31",[
   {"variant":"dark","kicker":"Primeiros socorros","title":"Não mexe o braço após um puxão","tag":A,"tsize":58},
   {"variant":"light","kicker":"O que costuma ser","title":"\"Cotovelo de babá\"","body":"A pronação dolorosa é comum em crianças pequenas após puxar o bracinho. Ela segura o braço parado.","tsize":70},
   {"variant":"dark","kicker":"O que fazer","title":"Não forçar o movimento","body":"Evite tracionar de novo e procure avaliação. A correção pelo ortopedista costuma ser rápida.","tsize":72},
   {"variant":"light","kicker":"Prevenção","title":"Evitar puxar pelas mãos","body":"Levantar a criança pelas axilas, e não pelas mãos ou pulsos, ajuda a prevenir.","tsize":72},
   {"variant":"dark","kicker":"Converse comigo","title":"Na dúvida, avalie","body":"Fale comigo pelo WhatsApp — link na bio.","foot":SIG,"tsize":80}],
  cap("A pronação dolorosa (\"cotovelo de babá\") ocorre após puxar o bracinho: a criança passa a segurar o braço sem mexer. Não force — a correção na ortopedia pediátrica costuma ser rápida. Levantar pelas axilas ajuda a prevenir.","#cotovelodebaba #pronacaodolorosa #ortopediapediatrica #ortopediainfantil #ortopediasaopaulo")),
 ("post32",[
   {"variant":"dark","kicker":"Entenda","title":"Por que fratura de criança é diferente","tag":A,"tsize":56},
   {"variant":"light","kicker":"A placa de crescimento","title":"Uma região especial do osso","body":"O osso da criança cresce a partir da fise, uma área mais frágil e importante.","tsize":70},
   {"variant":"dark","kicker":"Na prática","title":"Avaliação com cuidado próprio","body":"Fraturas perto da placa pedem atenção especial para não afetar o crescimento.","tsize":70},
   {"variant":"light","kicker":"Do lado bom","title":"Consolidam mais rápido","body":"Em compensação, o osso infantil tem grande capacidade de recuperação.","tsize":74},
   {"variant":"dark","kicker":"Converse comigo","title":"Dúvidas? Fale comigo","body":"WhatsApp no link da bio.","foot":SIG,"tsize":80}],
  cap("O osso da criança cresce pela placa de crescimento (fise), uma região mais frágil e importante. Por isso fraturas infantis têm avaliação própria na ortopedia pediátrica — e costumam consolidar mais rápido que no adulto.","#fratura #placadecrescimento #ortopediapediatrica #ortopediainfantil #ortopediasaopaulo")),
 ("post33",[
   {"variant":"dark","kicker":"Mito x verdade","title":"O bebê precisa de sapato firme?","tag":A,"tsize":62},
   {"variant":"light","kicker":"O que se sabe","title":"Descalço fortalece o pé","body":"Andar descalço em casa estimula a musculatura e o equilíbrio do pé em desenvolvimento.","tsize":74},
   {"variant":"dark","kicker":"O papel do sapato","title":"Proteção, não suporte","body":"O sapato serve para proteger. \"Sapato ortopédico\" sem indicação não é necessário.","tsize":72},
   {"variant":"light","kicker":"Na hora de escolher","title":"Flexível e do tamanho certo","body":"Prefira solado flexível, leve e confortável, com espaço para os dedos.","tsize":72},
   {"variant":"dark","kicker":"Converse comigo","title":"Dúvidas sobre o pezinho?","body":"Fale comigo pelo WhatsApp — link na bio.","foot":SIG,"tsize":68}],
  cap("Para a maioria dos bebês, andar descalço em casa fortalece o pé e o equilíbrio. O sapato é proteção — na ortopedia pediátrica, a recomendação é solado flexível e tamanho confortável, sem necessidade de \"sapato ortopédico\" por rotina.","#primeirospassos #pedobebe #ortopediapediatrica #mitoouverdade #ortopediasaopaulo")),
 ("post34",[
   {"variant":"dark","kicker":"Desenvolvimento","title":"Com que idade a criança anda?","tag":A,"tsize":62},
   {"variant":"light","kicker":"A faixa é ampla","title":"A maioria entre 12 e 15 meses","body":"Mas alguns só andam perto dos 18 meses — e isso também pode ser normal.","tsize":70},
   {"variant":"dark","kicker":"Cada um no seu tempo","title":"Comparar com cuidado","body":"O ritmo varia bastante entre crianças saudáveis. Evite comparações apressadas.","tsize":74},
   {"variant":"light","kicker":"Quando avaliar","title":"Sinais de atenção","body":"Não andar após 18 meses, perder habilidades já conquistadas ou movimento assimétrico.","tsize":68},
   {"variant":"dark","kicker":"Converse comigo","title":"Na dúvida, avalie","body":"Fale comigo pelo WhatsApp — link na bio.","foot":SIG,"tsize":80}],
  cap("Andar entre 12 e 15 meses é o mais comum, mas a faixa normal vai além. Avalie na ortopedia pediátrica quando a criança não anda após 18 meses, perde habilidades já conquistadas ou mostra movimento assimétrico.","#desenvolvimento #marcos #ortopediapediatrica #ortopediainfantil #ortopediasaopaulo")),
 ("post35",[
   {"variant":"dark","kicker":"Emergência","title":"Articulação inchada, quente e com febre","tag":A,"tsize":54},
   {"variant":"light","kicker":"Por que é urgente","title":"Pode ser infecção articular","body":"Dor forte, inchaço, calor, febre e recusa a mexer o membro são sinais de alerta.","tsize":66},
   {"variant":"dark","kicker":"O que fazer","title":"Atendimento imediato","body":"Não espere passar. O diagnóstico e o tratamento precoces protegem a articulação.","tsize":74},
   {"variant":"light","kicker":"Importante","title":"Tempo é fundamental","body":"Quanto antes se trata uma artrite séptica, menor o risco de sequelas.","tsize":74},
   {"variant":"dark","kicker":"Converse comigo","title":"Sinais assim? Procure já","body":"Em emergência, procure o pronto-socorro.","foot":SIG,"tsize":76}],
  cap("Articulação subitamente inchada, quente e dolorosa, com febre e recusa a movimentar o membro, pode ser artrite séptica — uma urgência da ortopedia pediátrica. Procure atendimento imediato: tratar cedo protege a articulação.","#artriteseptica #emergencia #ortopediapediatrica #sinaldealerta #ortopediasaopaulo")),
 ("post36",[
   {"variant":"dark","kicker":"Reconstrução e Alongamento Ósseo","title":"Uma perna mais curta que a outra","tag":A,"tsize":58},
   {"variant":"light","kicker":"Mais comum do que parece","title":"Pequenas diferenças","body":"Diferenças pequenas costumam ser bem toleradas e nem sempre precisam de tratamento.","tsize":72},
   {"variant":"dark","kicker":"Como avaliamos","title":"Medir e acompanhar","body":"Medimos a diferença e, na criança, acompanhamos como ela evolui com o crescimento.","tsize":72},
   {"variant":"light","kicker":"Opções","title":"De palmilha a alongamento","body":"O caminho depende da diferença, da causa, da idade e da expectativa — sempre individual.","tsize":70},
   {"variant":"dark","kicker":"Converse comigo","title":"Quer entender o seu caso?","body":"Fale comigo pelo WhatsApp — link na bio.","foot":SIG,"tsize":68}],
  cap("Uma perna mais curta que a outra — a discrepância de membro — é comum. Diferenças pequenas costumam ser bem toleradas; maiores têm opções que vão de palmilha a alongamento, conforme a diferença, a causa, a idade e a expectativa.","#discrepancia #alongamentoosseo #reconstrucaoossea #ortopediapediatrica #ortopediasaopaulo")),
 ("post37",[
   {"variant":"dark","kicker":"Convivendo com o fixador","title":"Posso tomar banho com o fixador?","tag":A,"tsize":62},
   {"variant":"light","kicker":"Em geral, sim","title":"Seguindo a sua orientação","body":"Na maioria dos casos é possível higienizar a região, mantendo limpo e secando bem os pinos.","tsize":68},
   {"variant":"dark","kicker":"Observe","title":"Sinais na pele","body":"Vermelhidão, dor nova ou secreção ao redor dos pinos devem ser avisados.","tsize":78},
   {"variant":"light","kicker":"Atenção","title":"Sua orientação vale mais","body":"Cada caso tem regras próprias. Na dúvida, siga o que combinamos e me avise.","tsize":74},
   {"variant":"dark","kicker":"Converse comigo","title":"Qualquer dúvida, fale comigo","body":"Estou por perto pelo WhatsApp — link na bio.","foot":SIG,"tsize":66}],
  cap("Na maioria dos casos dá para higienizar a região do fixador externo seguindo a orientação individual: manter limpo, secar bem os pinos e observar vermelhidão ou secreção. Suas orientações valem mais que regras gerais.","#fixadorexterno #cuidados #reconstrucaoossea #alongamentoosseo #ortopediasaopaulo")),
 ("post38",[
   {"variant":"dark","kicker":"Alongamento Ósseo","title":"Dói durante o alongamento?","tag":A,"tsize":74},
   {"variant":"light","kicker":"O que esperar","title":"Desconforto controlável","body":"Algum desconforto pode surgir, sobretudo na fase de afastamento gradual, e costuma ser manejável.","tsize":68},
   {"variant":"dark","kicker":"O que ajuda","title":"Acompanhamento e fisioterapia","body":"Ajustes ao longo do caminho e fisioterapia fazem parte e ajudam bastante.","tsize":74},
   {"variant":"light","kicker":"Importante","title":"Você não fica sozinho","body":"Cada fase tem seu cuidado e o plano é revisto de perto, conforme a sua resposta.","tsize":72},
   {"variant":"dark","kicker":"Converse comigo","title":"Quer entender as etapas?","body":"Fale comigo pelo WhatsApp — link na bio.","foot":SIG,"tsize":70}],
  cap("Algum desconforto pode aparecer no alongamento ósseo, sobretudo na fase de distração, e costuma ser controlável com acompanhamento e fisioterapia. Cada fase tem seu cuidado — o plano é feito para o seu caso.","#alongamentoosseo #reconstrucaoossea #fisioterapia #ortopediasaopaulo #ortopedia")),
 ("post39",[
   {"variant":"dark","kicker":"Reconstrução Óssea","title":"Fratura que não cola","tag":A,"tsize":80},
   {"variant":"light","kicker":"O que é","title":"Pseudoartrose","body":"É quando o osso não consolida no tempo esperado. Tem várias causas — e tem tratamento.","tsize":74},
   {"variant":"dark","kicker":"O caminho","title":"Investigar e estabilizar","body":"Procuramos a causa, garantimos boa estabilidade e estimulamos a formação de osso.","tsize":72},
   {"variant":"light","kicker":"Acompanhamento","title":"De perto, por etapas","body":"O processo é acompanhado passo a passo até o osso consolidar.","tsize":76},
   {"variant":"dark","kicker":"Converse comigo","title":"Convive com isso?","body":"Vamos avaliar pelo WhatsApp — link na bio.","foot":SIG,"tsize":78}],
  cap("Quando uma fratura não consolida (pseudoartrose), há caminho: investigar a causa, estabilizar adequadamente e estimular a formação de osso, com acompanhamento próximo. Cada caso tem seu plano.","#pseudoartrose #reconstrucaoossea #ortopedia #ortopediasaopaulo #fratura")),
 ("post40",[
   {"variant":"dark","kicker":"Reconstrução Óssea","title":"Reconstruir osso após infecção","tag":A,"tsize":64},
   {"variant":"light","kicker":"Primeiro","title":"Tratar a infecção","body":"O controle da infecção vem antes de recompor o osso, em etapas planejadas.","tsize":76},
   {"variant":"dark","kicker":"Transporte ósseo","title":"O osso \"caminha\"","body":"Em falhas ósseas, o próprio osso pode ser conduzido aos poucos para preencher o espaço.","tsize":68},
   {"variant":"light","kicker":"O objetivo","title":"Recuperar função","body":"São casos complexos, com plano individual e acompanhamento próximo do começo ao fim.","tsize":72},
   {"variant":"dark","kicker":"Converse comigo","title":"Casos difíceis têm caminho","body":"Fale comigo pelo WhatsApp — link na bio.","foot":SIG,"tsize":68}],
  cap("Após infecções com perda óssea, a reconstrução é por etapas: controlar a infecção e depois recompor o osso — às vezes com transporte ósseo (técnica de Ilizarov), em que o próprio osso preenche a falha gradualmente.","#transporteosseo #reconstrucaoossea #osteomielite #ortopedia #ortopediasaopaulo")),
 ("post41",[
   {"variant":"dark","kicker":"Adulto","title":"Joelho desalinhado desgasta antes?","tag":A,"tsize":60},
   {"variant":"light","kicker":"Por que o eixo importa","title":"Distribuição de carga","body":"O alinhamento das pernas reparte o peso na cartilagem. Desalinho sobrecarrega um lado.","tsize":70},
   {"variant":"dark","kicker":"A consequência","title":"Pode acelerar o desgaste","body":"A sobrecarga repetida em um compartimento favorece a artrose precoce.","tsize":72},
   {"variant":"light","kicker":"O que dá para fazer","title":"Corrigir o eixo","body":"Em casos selecionados, a osteotomia realinha a perna e protege a articulação.","tsize":74},
   {"variant":"dark","kicker":"Converse comigo","title":"Quer avaliar o seu eixo?","body":"Fale comigo pelo WhatsApp — link na bio.","foot":SIG,"tsize":70}],
  cap("O alinhamento das pernas distribui a carga na cartilagem. Um joelho muito desalinhado pode sobrecarregar um lado e acelerar o desgaste. Avaliar o eixo e, quando indicado, corrigi-lo (osteotomia) ajuda a proteger a articulação.","#osteotomia #joelho #alinhamento #reconstrucaoossea #ortopediasaopaulo")),
 ("post42",[
   {"variant":"dark","kicker":"Ortopedia Pediátrica","title":"Andar com os pés para fora","tag":A,"tsize":72},
   {"variant":"light","kicker":"O que é","title":"Costuma ser do desenvolvimento","body":"A rotação natural dos ossos faz muitos pés virarem para fora (ou para dentro) na infância.","tsize":66},
   {"variant":"dark","kicker":"O que esperar","title":"Melhora com o crescimento","body":"Na maioria, vai se ajustando ao longo dos anos, sem precisar de tratamento.","tsize":76},
   {"variant":"light","kicker":"Quando avaliar","title":"Sinais de atenção","body":"Muito assimétrico, com quedas frequentes ou que piora em vez de melhorar.","tsize":74},
   {"variant":"dark","kicker":"Converse comigo","title":"Na dúvida, avalie","body":"Fale comigo pelo WhatsApp — link na bio.","foot":SIG,"tsize":80}],
  cap("Andar com os pés para fora (ou para dentro) costuma fazer parte do desenvolvimento e melhora com o crescimento, refletindo a rotação dos ossos. Avalie na ortopedia pediátrica quando é muito assimétrico, causa quedas ou piora.","#marcha #rotacao #ortopediapediatrica #ortopediainfantil #ortopediasaopaulo")),
 ("post43",[
   {"variant":"dark","kicker":"Saúde óssea","title":"Vitamina D e ossos na infância","tag":A,"tsize":66},
   {"variant":"light","kicker":"Por que importa","title":"Ajuda a usar o cálcio","body":"A vitamina D participa da fixação do cálcio e sustenta o crescimento ósseo.","tsize":74},
   {"variant":"dark","kicker":"De onde vem","title":"Sol e alimentação","body":"A exposição solar segura e a dieta contribuem para os níveis adequados.","tsize":78},
   {"variant":"light","kicker":"Importante","title":"Suplemento é individual","body":"A necessidade varia. Suplementar por conta própria, sem avaliação, não é recomendado.","tsize":72},
   {"variant":"dark","kicker":"Converse comigo","title":"Dúvidas? Converse comigo","body":"Fale comigo pelo WhatsApp — link na bio.","foot":SIG,"tsize":74}],
  cap("A vitamina D ajuda o corpo a usar o cálcio e sustenta o crescimento ósseo. Sol e alimentação contribuem, mas a necessidade de suplemento é individual — vale avaliar na ortopedia pediátrica antes de iniciar por conta própria.","#vitaminad #saudeossea #ortopediapediatrica #ortopediainfantil #ortopediasaopaulo")),
]

def run():
    posts=json.load(open(os.path.join(ROOT,"posts.json"),encoding="utf-8"))
    pids={p["id"] for p in posts}; made=0
    for pid,slides,caption in POSTS:
        if pid in pids: continue
        imgs=[]
        for i,s in enumerate(slides,1):
            fn=f"{pid}_{i}.jpg"; pslide(s,fn); imgs.append("images/"+fn)
        posts.append({"id":pid,"images":imgs,"caption":caption}); pids.add(pid); made+=1
        json.dump(posts,open(os.path.join(ROOT,"posts.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
        print("ok",pid,flush=True)
    print("posts total:",len(posts),"| novos:",made)

if __name__=="__main__":
    run()
