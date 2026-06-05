# -*- coding: utf-8 -*-
"""Lote 2 de posts novos (post44-61). python posts_batch2.py"""
import os, json
from gerar_conteudo import pslide, cap, IMG, ROOT, SIG
A="arraste →"

POSTS=[
 ("post44",[
   {"variant":"dark","kicker":"Ortopedia Pediátrica","title":"Pezinho curvo no recém-nascido","tag":A,"tsize":62},
   {"variant":"light","kicker":"O que é","title":"Metatarso aduto","body":"A parte da frente do pé vira para dentro. É comum, costuma ser flexível e é diferente do pé torto.","tsize":68},
   {"variant":"dark","kicker":"O que esperar","title":"Muitos melhoram sozinhos","body":"Boa parte se ajusta com o crescimento. O acompanhamento observa o formato ao longo do tempo.","tsize":68},
   {"variant":"light","kicker":"Quando tratar","title":"Se for mais rígido","body":"Pés mais rígidos podem precisar de gesso ou órtese — sempre conforme a avaliação.","tsize":74},
   {"variant":"dark","kicker":"Converse comigo","title":"Quer avaliar o pé do bebê?","body":"Fale comigo pelo WhatsApp — link na bio.","foot":SIG,"tsize":66}],
  cap("No metatarso aduto, a frente do pé do bebê vira para dentro — é comum, costuma ser flexível e melhora na maioria. É diferente do pé torto. O acompanhamento define a necessidade de tratamento.","#metatarsoaduto #pedobebe #ortopediapediatrica #ortopediainfantil #ortopediasaopaulo")),
 ("post45",[
   {"variant":"dark","kicker":"Acolhimento","title":"Disseram que não há mais o que fazer?","tag":A,"tsize":56},
   {"variant":"light","kicker":"Vale um segundo olhar","title":"Casos complexos pedem tempo","body":"Reavaliar com calma às vezes revela opções que não pareciam existir.","tsize":72},
   {"variant":"dark","kicker":"Sem promessas","title":"Honestidade em primeiro lugar","body":"Não prometo milagre. Proponho uma avaliação cuidadosa e um plano realista.","tsize":72},
   {"variant":"light","kicker":"Como trabalho","title":"Acompanhamento de perto","body":"Quando há caminho, seguimos juntos, etapa por etapa.","tsize":78},
   {"variant":"dark","kicker":"Converse comigo","title":"Vamos reavaliar juntos","body":"Fale comigo pelo WhatsApp — link na bio.","foot":SIG,"tsize":78}],
  cap("Em casos complexos de deformidade e reconstrução, um segundo olhar cuidadoso às vezes revela opções. Não prometo milagre — proponho avaliação honesta, plano realista e acompanhamento próximo.","#segundaopiniao #casoscomplexos #reconstrucaoossea #deformidades #ortopediasaopaulo")),
 ("post46",[
   {"variant":"dark","kicker":"Primeira consulta","title":"Como é a primeira consulta comigo","tag":A,"tsize":60},
   {"variant":"light","kicker":"Escuto","title":"A sua história","body":"Começamos entendendo a queixa, o tempo de evolução e o que mais te preocupa.","tsize":76},
   {"variant":"dark","kicker":"Examino","title":"Com calma","body":"O exame físico cuidadoso, e os exames quando necessários, orientam o diagnóstico.","tsize":78},
   {"variant":"light","kicker":"Explico","title":"Em linguagem clara","body":"Você sai entendendo o problema, as opções e os próximos passos.","tsize":78},
   {"variant":"dark","kicker":"Converse comigo","title":"Agende pelo WhatsApp","body":"Link na bio para marcar.","foot":SIG,"tsize":80}],
  cap("Na primeira consulta, escuto a história, examino com calma e explico em linguagem clara. A ideia é você sair entendendo o problema e os próximos passos, com espaço para todas as perguntas.","#primeiraconsulta #ortopedia #ortopediapediatrica #reconstrucaoossea #ortopediasaopaulo")),
 ("post47",[
   {"variant":"dark","kicker":"Ortopedia Pediátrica","title":"Criança que cansa e sente dor para andar","tag":A,"tsize":54},
   {"variant":"light","kicker":"Quando investigar","title":"Sinais que chamam atenção","body":"Cansaço muito acima dos colegas, dor que limita o brincar ou mudança no jeito de andar.","tsize":66},
   {"variant":"dark","kicker":"O objetivo","title":"Entender a causa","body":"Muitas vezes é leve e tranquilizamos; quando há algo a tratar, quanto antes melhor.","tsize":74},
   {"variant":"light","kicker":"Como avaliamos","title":"História e exame","body":"O relato dos pais e o exame da criança guiam o que pode precisar de investigação.","tsize":74},
   {"variant":"dark","kicker":"Converse comigo","title":"Na dúvida, avalie","body":"Fale comigo pelo WhatsApp — link na bio.","foot":SIG,"tsize":80}],
  cap("Criança que cansa muito mais que os colegas, sente dor que limita o brincar ou muda o jeito de andar merece avaliação. Muitas vezes é leve; quando há algo a tratar, quanto antes melhor.","#dor #marcha #ortopediapediatrica #saudedacrianca #ortopediasaopaulo")),
 ("post48",[
   {"variant":"dark","kicker":"Deformidades complexas","title":"Deformidade nas pernas tem correção?","tag":A,"tsize":56},
   {"variant":"light","kicker":"Sim, com planejamento","title":"Medir o eixo com precisão","body":"Definimos exatamente onde e quanto corrigir antes de qualquer passo.","tsize":74},
   {"variant":"dark","kicker":"Como se corrige","title":"Devagar é mais seguro","body":"Muitas vezes a correção é gradual e guiada, respeitando os tecidos ao redor.","tsize":74},
   {"variant":"light","kicker":"O foco","title":"Função e alinhamento","body":"O objetivo é um membro alinhado e funcional, com acompanhamento por etapas.","tsize":74},
   {"variant":"dark","kicker":"Converse comigo","title":"Quer entender o seu caso?","body":"Fale comigo pelo WhatsApp — link na bio.","foot":SIG,"tsize":66}],
  cap("Deformidades angulares das pernas podem ser corrigidas com planejamento: medir o eixo, definir o ponto de correção e, muitas vezes, corrigir de forma gradual e acompanhada. O foco é segurança e função.","#deformidades #reconstrucaoossea #alongamentoosseo #ortopedia #ortopediasaopaulo")),
 ("post49",[
   {"variant":"dark","kicker":"Ossos frágeis","title":"Criança que fratura com facilidade","tag":A,"tsize":62},
   {"variant":"light","kicker":"Quando investigar","title":"Fraturas repetidas","body":"Várias fraturas com pequenos traumas, às vezes com histórico familiar, merecem atenção.","tsize":72},
   {"variant":"dark","kicker":"Uma possibilidade","title":"Osteogênese imperfeita","body":"É a condição dos \"ossos de vidro\", de gravidade variável e com acompanhamento próprio.","tsize":68},
   {"variant":"light","kicker":"O cuidado","title":"Especializado e contínuo","body":"O objetivo é proteger, fortalecer e acompanhar ao longo do crescimento.","tsize":74},
   {"variant":"dark","kicker":"Converse comigo","title":"Convive com isso?","body":"Vamos avaliar pelo WhatsApp — link na bio.","foot":SIG,"tsize":78}],
  cap("Fraturas repetidas com pequenos traumas, às vezes com histórico familiar, merecem investigação — pode haver uma condição óssea, como a osteogênese imperfeita. O cuidado é especializado e acompanha o crescimento.","#osteogeneseimperfeita #ossosfrageis #ortopediapediatrica #ortopediainfantil #ortopediasaopaulo")),
 ("post50",[
   {"variant":"dark","kicker":"Reconstrução e Alongamento Ósseo","title":"Quando indicar alongamento ósseo","tag":A,"tsize":56},
   {"variant":"light","kicker":"Avalia-se caso a caso","title":"O que pesa na decisão","body":"A diferença ou deformidade, o impacto na função e uma expectativa realista.","tsize":74},
   {"variant":"dark","kicker":"Decisão conjunta","title":"Conversando opções","body":"Falamos com transparência sobre riscos, benefícios e alternativas.","tsize":76},
   {"variant":"light","kicker":"O compromisso","title":"Plano feito com você","body":"Sem promessas — um plano honesto, do seu jeito e com acompanhamento próximo.","tsize":74},
   {"variant":"dark","kicker":"Converse comigo","title":"Vamos conversar sobre o seu caso?","body":"Fale comigo pelo WhatsApp — link na bio.","foot":SIG,"tsize":58}],
  cap("A indicação de alongamento ósseo é individual: pesa-se a diferença ou deformidade, o impacto na função e a expectativa realista. É uma decisão conjunta, com transparência sobre riscos e benefícios.","#alongamentoosseo #reconstrucaoossea #deformidades #ortopedia #ortopediasaopaulo")),
 ("post51",[
   {"variant":"dark","kicker":"Ortopedia Pediátrica","title":"Pé cavo: o arco muito alto","tag":A,"tsize":66},
   {"variant":"light","kicker":"O que é","title":"O oposto do pé chato","body":"No pé cavo o arco é mais alto que o habitual, e o peso se concentra em poucos pontos.","tsize":72},
   {"variant":"dark","kicker":"Por que avaliar","title":"Pode ter causa a investigar","body":"Quando é acentuado ou progride, vale procurar uma causa, às vezes neurológica.","tsize":70},
   {"variant":"light","kicker":"O que ajuda","title":"Depende do caso","body":"De adaptações simples a tratamentos específicos — definidos pela avaliação.","tsize":76},
   {"variant":"dark","kicker":"Converse comigo","title":"Quer avaliar o seu pé?","body":"Fale comigo pelo WhatsApp — link na bio.","foot":SIG,"tsize":72}],
  cap("No pé cavo, o arco é mais alto que o habitual e o peso se concentra em poucos pontos. Quando é acentuado ou progride, vale investigar a causa. O tratamento depende da avaliação de cada caso.","#pecavo #ortopediapediatrica #ortopediainfantil #pe #ortopediasaopaulo")),
 ("post52",[
   {"variant":"dark","kicker":"Jovem atleta","title":"Dor no calcanhar de quem treina","tag":A,"tsize":62},
   {"variant":"light","kicker":"O que costuma ser","title":"Doença de Sever","body":"Inflamação na região de crescimento do calcâneo, comum em crianças e adolescentes ativos.","tsize":70},
   {"variant":"dark","kicker":"O que ajuda","title":"Carga, gelo e alongamento","body":"Equilibrar treino e descanso, gelo após a atividade e alongar a panturrilha costumam aliviar.","tsize":70},
   {"variant":"light","kicker":"Boa notícia","title":"Costuma ser autolimitada","body":"Com os cuidados, tende a melhorar. Se persiste, vale avaliar.","tsize":76},
   {"variant":"dark","kicker":"Converse comigo","title":"Dor que não passa?","body":"Fale comigo pelo WhatsApp — link na bio.","foot":SIG,"tsize":76}],
  cap("A doença de Sever causa dor no calcanhar em crianças e adolescentes ativos, na área de crescimento do osso. Costuma melhorar com ajuste de carga, gelo e alongamento. Se persiste, vale avaliar.","#doencadesever #calcanhar #ortopediadoesporte #ortopediapediatrica #ortopediasaopaulo")),
 ("post53",[
   {"variant":"dark","kicker":"Dúvida comum","title":"Estalos nas articulações: é grave?","tag":A,"tsize":64},
   {"variant":"light","kicker":"Na maioria","title":"Estalo sem dor é benigno","body":"Articulações que estalam sem dor, inchaço ou travamento costumam não preocupar.","tsize":72},
   {"variant":"dark","kicker":"Quando avaliar","title":"Se vem com sintomas","body":"Estalo acompanhado de dor, inchaço, travamento ou sensação de falseio merece avaliação.","tsize":72},
   {"variant":"light","kicker":"Em resumo","title":"O sintoma é que guia","body":"O estalo isolado importa menos que a dor ou a limitação associada.","tsize":74},
   {"variant":"dark","kicker":"Converse comigo","title":"Na dúvida, avalie","body":"Fale comigo pelo WhatsApp — link na bio.","foot":SIG,"tsize":80}],
  cap("Articulações que estalam sem dor, inchaço ou travamento costumam ser benignas. O estalo acompanhado de dor, inchaço, travamento ou falseio é que merece avaliação — o sintoma guia, não o barulho.","#estalos #articulacoes #ortopedia #ortopediapediatrica #ortopediasaopaulo")),
 ("post54",[
   {"variant":"dark","kicker":"Ortopedia Pediátrica","title":"Frouxidão dos ligamentos","tag":A,"tsize":70},
   {"variant":"light","kicker":"O que é","title":"Articulações mais \"soltas\"","body":"A hipermobilidade é comum e, em muitos, é só uma característica, sem doença.","tsize":74},
   {"variant":"dark","kicker":"Quando dá sintoma","title":"Dores após esforço","body":"Algumas crianças sentem dores nas pernas após muita atividade.","tsize":78},
   {"variant":"light","kicker":"O que ajuda","title":"Fortalecimento","body":"Atividade física e fortalecimento muscular costumam ajudar bastante.","tsize":78},
   {"variant":"dark","kicker":"Converse comigo","title":"Quer entender melhor?","body":"Fale comigo pelo WhatsApp — link na bio.","foot":SIG,"tsize":74}],
  cap("A hipermobilidade (frouxidão ligamentar) é comum e, em muitos, é só uma característica. Algumas crianças têm dores após esforço; atividade física e fortalecimento muscular costumam ajudar.","#hipermobilidade #frouxidaoligamentar #ortopediapediatrica #ortopediainfantil #ortopediasaopaulo")),
 ("post55",[
   {"variant":"dark","kicker":"Coluna","title":"Dor nas costas na criança","tag":A,"tsize":76},
   {"variant":"light","kicker":"Menos comum que no adulto","title":"Por isso merece atenção","body":"Dor nas costas persistente na criança nem sempre deve ser ignorada.","tsize":70},
   {"variant":"dark","kicker":"Sinais de alerta","title":"Quando investigar","body":"Dor que acorda à noite, febre, perda de peso, ou que piora e limita as atividades.","tsize":70},
   {"variant":"light","kicker":"A conduta","title":"Avaliar com cuidado","body":"A avaliação define se é algo simples ou se precisa de investigação.","tsize":76},
   {"variant":"dark","kicker":"Converse comigo","title":"Dor que não passa?","body":"Fale comigo pelo WhatsApp — link na bio.","foot":SIG,"tsize":76}],
  cap("Dor nas costas persistente na criança merece atenção. Sinais como dor noturna, febre, perda de peso ou que limita as atividades pedem avaliação. Na maioria é simples, mas vale investigar quando há alerta.","#dornascostas #colunainfantil #ortopediapediatrica #sinaldealerta #ortopediasaopaulo")),
 ("post56",[
   {"variant":"dark","kicker":"Esporte na infância","title":"Prevenir lesões na criança atleta","tag":A,"tsize":60},
   {"variant":"light","kicker":"Equilíbrio","title":"Treino e descanso","body":"Variar atividades e respeitar o descanso reduz lesões por excesso de uso.","tsize":78},
   {"variant":"dark","kicker":"Base","title":"Aquecer e fortalecer","body":"Aquecimento e fortalecimento adequados à idade protegem articulações e músculos.","tsize":74},
   {"variant":"light","kicker":"Atenção","title":"Dor não é normal","body":"Dor que persiste ou limita o esporte deve ser avaliada, não \"empurrada com a barriga\".","tsize":72},
   {"variant":"dark","kicker":"Converse comigo","title":"Dúvidas? Fale comigo","body":"WhatsApp no link da bio.","foot":SIG,"tsize":80}],
  cap("Para a criança atleta, variar atividades, respeitar o descanso, aquecer e fortalecer reduzem lesões por excesso de uso. Dor que persiste ou limita o esporte deve ser avaliada — não é normal.","#esporteinfantil #prevencao #ortopediadoesporte #ortopediapediatrica #ortopediasaopaulo")),
 ("post57",[
   {"variant":"dark","kicker":"Adolescente","title":"Tornozelo torcido: e agora?","tag":A,"tsize":72},
   {"variant":"light","kicker":"No começo","title":"Repouso, gelo e elevação","body":"Nas primeiras horas, proteger, aplicar gelo e elevar o tornozelo ajuda a controlar o inchaço.","tsize":68},
   {"variant":"dark","kicker":"Quando avaliar","title":"Sinais de atenção","body":"Não conseguir apoiar o pé, inchaço importante ou dor que não melhora merecem avaliação.","tsize":68},
   {"variant":"light","kicker":"Reabilitação","title":"Voltar com segurança","body":"Fortalecer e treinar o equilíbrio reduz o risco de torcer de novo.","tsize":76},
   {"variant":"dark","kicker":"Converse comigo","title":"Torceu e não melhora?","body":"Fale comigo pelo WhatsApp — link na bio.","foot":SIG,"tsize":74}],
  cap("Na torção de tornozelo, proteger, aplicar gelo e elevar ajuda no início. Não apoiar o pé, inchaço importante ou dor que não melhora merecem avaliação. Fortalecer e treinar equilíbrio evita novas torções.","#entorse #tornozelo #ortopediadoesporte #adolescente #ortopediasaopaulo")),
 ("post58",[
   {"variant":"dark","kicker":"Antes da consulta","title":"O que levar à consulta de ortopedia","tag":A,"tsize":56},
   {"variant":"light","kicker":"Histórico","title":"A linha do tempo","body":"Quando começou, o que melhora ou piora, e tratamentos já tentados.","tsize":78},
   {"variant":"dark","kicker":"Exames","title":"Os que você já tem","body":"Leve raios-X, ressonâncias e laudos anteriores, mesmo antigos.","tsize":80},
   {"variant":"light","kicker":"Dúvidas","title":"Anote suas perguntas","body":"Uma listinha ajuda a não esquecer nada de importante no dia.","tsize":78},
   {"variant":"dark","kicker":"Converse comigo","title":"Vamos marcar?","body":"Agende pelo WhatsApp — link na bio.","foot":SIG,"tsize":80}],
  cap("Para aproveitar a consulta, leve a história do problema (quando começou, o que melhora/piora, tratamentos já feitos), os exames que já tem (mesmo antigos) e uma lista das suas dúvidas.","#consulta #ortopedia #ortopediapediatrica #reconstrucaoossea #ortopediasaopaulo")),
 ("post59",[
   {"variant":"dark","kicker":"Ortopedia Pediátrica","title":"Joelho que falseia no adolescente","tag":A,"tsize":58},
   {"variant":"light","kicker":"O que pode ser","title":"Instabilidade da patela","body":"A patela pode \"escapar\" para o lado, causando a sensação de que o joelho vai ceder.","tsize":70},
   {"variant":"dark","kicker":"Sinais","title":"Falseio e dor anterior","body":"Sensação de insegurança, dor na frente do joelho e episódios de \"saída\" da patela.","tsize":72},
   {"variant":"light","kicker":"O que ajuda","title":"Fortalecer primeiro","body":"O fortalecimento costuma ser a base; alguns casos pedem avaliação mais detalhada.","tsize":74},
   {"variant":"dark","kicker":"Converse comigo","title":"Joelho inseguro?","body":"Fale comigo pelo WhatsApp — link na bio.","foot":SIG,"tsize":78}],
  cap("A sensação de joelho que \"falseia\" no adolescente pode ser instabilidade da patela, que escapa para o lado. Fortalecimento costuma ser a base; alguns casos pedem avaliação mais detalhada.","#instabilidadepatelar #joelho #ortopediapediatrica #adolescente #ortopediasaopaulo")),
 ("post60",[
   {"variant":"dark","kicker":"Saúde óssea","title":"Pernas que arqueiam e pioram","tag":A,"tsize":70},
   {"variant":"light","kicker":"Quando não é só do crescimento","title":"Pode haver causa","body":"Arqueamento que piora, é assimétrico ou vem com baixa estatura merece investigação.","tsize":66},
   {"variant":"dark","kicker":"Uma possibilidade","title":"Raquitismo","body":"Alterações no metabolismo ósseo podem deformar os ossos em crescimento.","tsize":74},
   {"variant":"light","kicker":"O caminho","title":"Avaliar e tratar a causa","body":"Tratar a origem e, quando preciso, corrigir a deformidade restabelece o alinhamento.","tsize":70},
   {"variant":"dark","kicker":"Converse comigo","title":"As pernas pioraram?","body":"Fale comigo pelo WhatsApp — link na bio.","foot":SIG,"tsize":74}],
  cap("Arqueamento das pernas que piora, é assimétrico ou vem com baixa estatura pode não ser só do crescimento — às vezes há causa, como o raquitismo. Avaliar e tratar a origem ajuda a restabelecer o alinhamento.","#raquitismo #deformidades #ortopediapediatrica #saudeossea #ortopediasaopaulo")),
 ("post61",[
   {"variant":"dark","kicker":"Reconstrução e Alongamento Ósseo","title":"Casos difíceis têm caminho","tag":A,"tsize":58},
   {"variant":"light","kicker":"A proposta","title":"Tratamento guiado e seriado","body":"Avaliação cuidadosa, plano realista e correção em etapas, acompanhando de perto.","tsize":70},
   {"variant":"dark","kicker":"Quem cuido","title":"Crianças e adultos","body":"Deformidades e problemas ósseos de difícil solução, em diferentes idades.","tsize":74},
   {"variant":"light","kicker":"O foco","title":"Função e qualidade de vida","body":"Mais do que um ideal, o que melhora o dia a dia de quem busca ajuda.","tsize":72},
   {"variant":"dark","kicker":"Converse comigo","title":"Vamos avaliar o seu caso?","body":"Fale comigo pelo WhatsApp — link na bio.","foot":SIG,"tsize":66}],
  cap("Para deformidades e problemas ósseos de difícil solução, em crianças e adultos, a proposta é um tratamento guiado e seriado: avaliação cuidadosa, plano realista e correção em etapas, com foco em função e qualidade de vida.","#reconstrucaoossea #alongamentoosseo #deformidades #casoscomplexos #ortopediasaopaulo")),
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
