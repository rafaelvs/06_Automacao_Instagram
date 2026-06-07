# -*- coding: utf-8 -*-
"""
Gerador de conteudo (REABASTECIMENTO) para a biblioteca do Instagram do Dr. Rafael Vargas.

Como usar:
1) Preencha as listas POSTS e STORIES abaixo com temas NOVOS (postNN / storyNN).
2) Rode:  python gerar_conteudo.py  -> renderiza em images/ e ANEXA a posts.json/stories.json.
3) GitHub Desktop -> commit -> Push. O robo publica em ordem, sem repetir.

Marca: preto #14141A, creme #F3E2C8, dourado #B08C4F, fundo #F6F4EF.
Assinatura CFM: Dr. Rafael Vargas - Medico - CRM-SP 226103 - RQE 137901.
Conteudo EDUCATIVO, sem prometer resultado, conforme o CFM.
"""
import os, json
from PIL import Image, ImageDraw, ImageFont
INK=(20,20,26); PAPER=(246,244,239); CREAM=(243,226,200); GOLD=(176,140,79)
TXT_D=(74,70,64); TXT_L=(206,198,184); MUT_D=(140,134,124); MUT_L=(150,144,132)
FD="/usr/share/fonts/truetype/liberation/"
def F(n,s): return ImageFont.truetype(FD+n,s)
SB="LiberationSerif-Bold.ttf"; NR="LiberationSans-Regular.ttf"; NB="LiberationSans-Bold.ttf"
ROOT=os.path.dirname(os.path.abspath(__file__)); IMG=os.path.join(ROOT,"images")
SIG="Dr. Rafael Vargas · Médico · CRM-SP 226103 · RQE 137901"
def wrap(d,t,f,mw):
    out=[];cur=""
    for w in t.split():
        s=(cur+" "+w).strip()
        if d.textlength(s,font=f)<=mw: cur=s
        else:
            if cur:out.append(cur)
            cur=w
    if cur:out.append(cur)
    return out
def trk(d,xy,text,font,fill,tr,left=True):
    x,y=xy
    if not left:
        tot=sum(d.textlength(c,font=font)+tr for c in text)-tr; x-=tot
    for c in text: d.text((x,y),c,font=font,fill=fill); x+=d.textlength(c,font=font)+tr
def mono(d,v,M):
    col=CREAM if v=="dark" else INK
    d.text((M,108),"RV",font=F(SB,54),fill=col); wf=d.textlength("RV",font=F(SB,54))
    d.line([(M+wf+22,118),(M+wf+22,162)],fill=GOLD,width=2)
    d.text((M+wf+40,116),"Dr. Rafael Vargas",font=F(NR,24),fill=col)
    d.text((M+wf+40,144),"Ortopedia · São Paulo",font=F(NR,20),fill=GOLD)
def arcs(img,v,W,H):
    ov=Image.new("RGBA",(W,H),(0,0,0,0)); da=ImageDraw.Draw(ov)
    col=(176,140,79,68) if v=="dark" else (176,140,79,52)
    for rad in [520,470,420,370,320]: da.arc([W//2-rad,H-150-rad,W//2+rad,H-150+rad],200,340,fill=col,width=2)
    return Image.alpha_composite(img.convert("RGBA"),ov).convert("RGB")
def pslide(spec,fn):
    W,H=1080,1350; M=120
    img=Image.new("RGBA",(W,H),(INK if spec["variant"]=="dark" else PAPER)+(255,)); img=arcs(img,spec["variant"],W,H); d=ImageDraw.Draw(img)
    tcol=CREAM if spec["variant"]=="dark" else INK; bcol=TXT_L if spec["variant"]=="dark" else TXT_D; mcol=MUT_L if spec["variant"]=="dark" else MUT_D
    mono(d,spec["variant"],M)
    ky=470; trk(d,(M,ky),spec["kicker"].upper(),F(NB,26),GOLD,6); d.line([(M,ky+44),(M+64,ky+44)],fill=GOLD,width=3)
    ty=ky+78; tf=F(SB,spec.get("tsize",80))
    for ln in wrap(d,spec["title"],tf,W-2*M): d.text((M,ty),ln,font=tf,fill=tcol); ty+=int(tf.size*1.08)
    if spec.get("body"):
        by=ty+34
        for ln in wrap(d,spec["body"],F(NR,34),W-2*M): d.text((M,by),ln,font=F(NR,34),fill=bcol); by+=46
    d.text((M,H-150),"@rafaelvargasmd",font=F(NR,27),fill=mcol)
    if spec.get("tag"): trk(d,(W-M,H-152),spec["tag"].upper(),F(NB,27),GOLD,3,left=False)
    if spec.get("foot"): d.text((M,H-108),spec["foot"],font=F(NR,24),fill=mcol)
    img.save(os.path.join(IMG,fn),"JPEG",quality=92)
def story(fn,v,k,t,sub):
    W,H=1080,1920; M=130
    img=Image.new("RGBA",(W,H),(INK if v=="dark" else PAPER)+(255,)); img=arcs(img,v,W,H); d=ImageDraw.Draw(img)
    tcol=CREAM if v=="dark" else INK; scol=TXT_L if v=="dark" else TXT_D; mcol=MUT_L if v=="dark" else MUT_D
    d.text((M,150),"RV",font=F(SB,60),fill=tcol); wf=d.textlength("RV",font=F(SB,60))
    d.line([(M+wf+24,162),(M+wf+24,212)],fill=GOLD,width=2)
    d.text((M+wf+44,160),"Dr. Rafael Vargas",font=F(NR,26),fill=tcol); d.text((M+wf+44,194),"Ortopedia · São Paulo",font=F(NR,22),fill=GOLD)
    ky=640; trk(d,(M,ky),k.upper(),F(NB,30),GOLD,6); d.line([(M,ky+50),(M+70,ky+50)],fill=GOLD,width=3)
    ty=ky+98; tf=F(SB,88); tl=wrap(d,t,tf,W-2*M)
    if len(tl)>3: tf=F(SB,70); tl=wrap(d,t,tf,W-2*M)
    for ln in tl: d.text((M,ty),ln,font=tf,fill=tcol); ty+=int(tf.size*1.1)
    by=ty+46
    for ln in wrap(d,sub,F(NR,40),W-2*M): d.text((M,by),ln,font=F(NR,40),fill=scol); by+=58
    d.text((M,H-200),"@rafaelvargasmd",font=F(NR,30),fill=mcol); d.text((M,H-150),SIG,font=F(NR,24),fill=mcol)
    img.save(os.path.join(IMG,fn),"JPEG",quality=92)
def cap(corpo,tags): return corpo+"\n\n""📤 Manda para alguém que precisa ver. 📌 Salve para consultar depois.\n""💬 Dúvida? Comenta ou chama no direct. 📲 Agende pela WhatsApp no link da bio."+"\n\n"+SIG+"\n\n"+tags
NL="\n\n"; A="arraste →"

C19=NL.join(["Pé torto congênito: por que tratar cedo faz diferença.","O pé torto (equinovaro) já nasce com o pé virado para baixo e para dentro. É comum e não tem a ver com algo que se fez na gestação.","O tratamento costuma começar nas primeiras semanas, com gessos que corrigem o pé aos poucos (método de Ponseti) e, depois, uma órtese de manutenção. Começar cedo aproveita a flexibilidade do bebê e costuma evitar cirurgias maiores. O acompanhamento segue ao longo do crescimento.","Quer avaliar o pé do seu bebê? WhatsApp no link da bio."])
C20=NL.join(["Displasia do desenvolvimento do quadril: sinais para observar no bebê.","Na displasia, o quadril não encaixa bem desde cedo. Quando se identifica nos primeiros meses, o tratamento costuma ser mais simples.","Vale avaliar quando há: pregas das coxas assimétricas, uma perna que parece mais curta, dificuldade de abrir uma das pernas na troca de fralda ou um “clique” no quadril. O teste do pezinho não detecta isso — o exame é clínico e, às vezes, com ultrassom.","Na dúvida, avalie. WhatsApp no link da bio."])
C21=NL.join(["Convivendo com o fixador externo: cuidados no dia a dia.","O fixador assusta no começo, mas a rotina de cuidados é simples e faz parte do tratamento. Em geral: manter a região dos pinos limpa e seca conforme a orientação, observar sinais de vermelhidão ou secreção, não apoiar peso além do combinado e comparecer aos retornos.","Cada caso tem orientações próprias — as suas valem mais do que qualquer regra geral. Qualquer dúvida ou sinal diferente, é só avisar.","Fale comigo pelo WhatsApp (link na bio)."])
C22=NL.join(["Como o corpo cria osso novo durante o alongamento.","Parece incrível, mas o próprio corpo regenera osso. Depois de um corte ósseo planejado, o tratamento segue em fases: um tempo de espera (latência), o afastamento gradual milímetro a milímetro (distração) e, por fim, o endurecimento do osso novo (consolidação).","É por isso que o alongamento é um tratamento de etapas, com acompanhamento próximo — cada fase tem o seu tempo e o seu cuidado.","Quer entender como seria no seu caso? WhatsApp no link da bio."])
C23=NL.join(["Deformidades de causa neurológica: a ortopedia também ajuda.","Condições como mielomeningocele e paralisia cerebral podem afetar o equilíbrio muscular e levar a deformidades nos membros, quadris e pés ao longo do crescimento.","O cuidado é em equipe e por etapas: acompanhar o crescimento, prevenir deformidades quando possível e corrigir o que atrapalha o sentar, o ficar de pé ou o andar. O objetivo é função e conforto no dia a dia.","Convive com uma dessas condições? WhatsApp no link da bio."])
C24=NL.join(["Dor de crescimento ou dor que precisa avaliar?","A chamada dor de crescimento é comum, costuma vir no fim do dia ou à noite, nas duas pernas, e melhora pela manhã e com massagem. Não causa mancar nem incha.","Vale procurar avaliação quando a dor é só de um lado, vem com inchaço, vermelhidão ou febre, faz a criança mancar, atrapalha o brincar ou aparece sempre no mesmo ponto.","Na dúvida, observar de perto é o melhor caminho. WhatsApp no link da bio."])

POSTS=[
 ("post19",[
   {"variant":"dark","kicker":"Ortopedia Pediátrica","title":"Pé torto congênito tem tratamento","tag":A,"tsize":72},
   {"variant":"light","kicker":"O que é","title":"Uma curvatura do pé desde o nascimento","body":"O pé torto (equinovaro) faz o pé virar para baixo e para dentro. É comum e não tem relação com algo feito na gestação.","tsize":62},
   {"variant":"dark","kicker":"Como se trata","title":"Gessos que corrigem aos poucos","body":"Costuma começar nas primeiras semanas, com trocas de gesso (método de Ponseti) e, depois, uma órtese de manutenção.","tsize":70},
   {"variant":"light","kicker":"Por que cedo","title":"Quanto antes, mais suave","body":"Começar nos primeiros meses aproveita a flexibilidade do bebê e costuma reduzir cirurgias maiores. O acompanhamento segue no crescimento.","tsize":72},
   {"variant":"dark","kicker":"Converse comigo","title":"Avalie o pé do seu bebê","body":"Tire suas dúvidas pelo WhatsApp — link na bio.","foot":SIG,"tsize":72},
 ],cap(C19,"#petortocongenito #ponseti #ortopediapediatrica #ortopediainfantil #ortopediasaopaulo")),
 ("post20",[
   {"variant":"dark","kicker":"Ortopedia Pediátrica","title":"Displasia do quadril no bebê","tag":A},
   {"variant":"light","kicker":"O que é","title":"O quadril que não encaixa bem","body":"Na displasia do desenvolvimento, o quadril não se encaixa direito desde cedo. Identificar nos primeiros meses costuma tornar o tratamento mais simples.","tsize":70},
   {"variant":"dark","kicker":"Sinais","title":"O que observar","body":"Pregas das coxas assimétricas, uma perna que parece mais curta, dificuldade de abrir uma perna na troca de fralda ou um clique no quadril.","tsize":80},
   {"variant":"light","kicker":"Importante","title":"O teste do pezinho não detecta","body":"A avaliação é clínica e, às vezes, com ultrassom. Por isso o exame do bebê pelo ortopedista faz diferença.","tsize":60},
   {"variant":"dark","kicker":"Converse comigo","title":"Na dúvida, avalie","body":"Fale comigo pelo WhatsApp — link na bio.","foot":SIG,"tsize":80},
 ],cap(C20,"#displasiadoquadril #ddq #ortopediapediatrica #ortopediainfantil #ortopediasaopaulo")),
 ("post21",[
   {"variant":"dark","kicker":"Reconstrução e Alongamento Ósseo","title":"Convivendo com o fixador externo","tag":A,"tsize":68},
   {"variant":"light","kicker":"Calma","title":"Assusta, mas a rotina é simples","body":"O fixador faz parte do tratamento. Com poucos cuidados, a vida segue — escola, trabalho e boa parte das atividades.","tsize":68},
   {"variant":"dark","kicker":"No dia a dia","title":"Cuidados com os pinos","body":"Manter a região limpa e seca conforme a orientação e observar vermelhidão, dor nova ou secreção.","tsize":78},
   {"variant":"light","kicker":"Atenção","title":"Suas orientações valem mais","body":"Cada caso tem cuidados próprios. Não apoie peso além do combinado e compareça aos retornos.","tsize":72},
   {"variant":"dark","kicker":"Converse comigo","title":"Qualquer sinal diferente, avise","body":"Estou por perto pelo WhatsApp — link na bio.","foot":SIG,"tsize":66},
 ],cap(C21,"#fixadorexterno #cuidados #reconstrucaoossea #alongamentoosseo #ortopediasaopaulo")),
 ("post22",[
   {"variant":"dark","kicker":"Alongamento Ósseo","title":"Como o corpo cria osso novo","tag":A},
   {"variant":"light","kicker":"Ponto de partida","title":"O osso se regenera","body":"Depois de um corte ósseo planejado, o próprio corpo forma osso novo no espaço que vai sendo aberto.","tsize":78},
   {"variant":"dark","kicker":"As fases","title":"Espera, distração e consolidação","body":"Primeiro um tempo de latência; depois o afastamento gradual, milímetro a milímetro; por fim, o osso novo endurece.","tsize":60},
   {"variant":"light","kicker":"Por isso","title":"É um tratamento de etapas","body":"Cada fase tem o seu tempo e o seu cuidado, com acompanhamento próximo do começo ao fim.","tsize":72},
   {"variant":"dark","kicker":"Converse comigo","title":"Entenda o seu caso","body":"Tire suas dúvidas pelo WhatsApp — link na bio.","foot":SIG,"tsize":80},
 ],cap(C22,"#alongamentoosseo #osteogenesedistracao #reconstrucaoossea #ortopediasaopaulo #ortopedia")),
 ("post23",[
   {"variant":"dark","kicker":"Ortopedia Pediátrica","title":"Deformidades de causa neurológica","tag":A,"tsize":60},
   {"variant":"light","kicker":"O contexto","title":"Quando o equilíbrio muscular muda","body":"Condições como mielomeningocele e paralisia cerebral podem levar a deformidades nos membros, quadris e pés ao longo do crescimento.","tsize":60},
   {"variant":"dark","kicker":"O cuidado","title":"Em equipe e por etapas","body":"Acompanhar o crescimento, prevenir deformidades quando possível e corrigir o que atrapalha sentar, ficar de pé ou andar.","tsize":74},
   {"variant":"light","kicker":"O objetivo","title":"Função e conforto no dia a dia","body":"Mais do que um ideal, o foco é o que melhora a rotina e a qualidade de vida da criança.","tsize":62},
   {"variant":"dark","kicker":"Converse comigo","title":"Vamos avaliar juntos","body":"Fale comigo pelo WhatsApp — link na bio.","foot":SIG,"tsize":76},
 ],cap(C23,"#mielomeningocele #paralisiacerebral #ortopediapediatrica #deformidadesosseas #ortopediasaopaulo")),
 ("post24",[
   {"variant":"dark","kicker":"Ortopedia Pediátrica","title":"Dor de crescimento ou sinal de alerta?","tag":A,"tsize":60},
   {"variant":"light","kicker":"Costuma ser comum","title":"Como é a dor de crescimento","body":"Geralmente nas duas pernas, no fim do dia ou à noite, melhora pela manhã e com massagem. Não faz mancar nem incha.","tsize":62},
   {"variant":"dark","kicker":"Atenção","title":"Quando avaliar","body":"Dor de um lado só, com inchaço, vermelhidão ou febre, que faz mancar, atrapalha o brincar ou aparece sempre no mesmo ponto.","tsize":78},
   {"variant":"light","kicker":"A conduta","title":"Observar de perto","body":"Na maioria, é só acompanhar. A avaliação serve para tranquilizar e identificar o que precisa de atenção.","tsize":74},
   {"variant":"dark","kicker":"Converse comigo","title":"Na dúvida, avalie","body":"Fale comigo pelo WhatsApp — link na bio.","foot":SIG,"tsize":80},
 ],cap(C24,"#dordecrescimento #ortopediapediatrica #ortopediainfantil #saudedacrianca #ortopediasaopaulo")),
]
STORIES=[
 ("story28","dark","Ortopedia Pediátrica","Pé torto tem tratamento","Começar cedo, com gessos que corrigem aos poucos, costuma evitar cirurgias maiores."),
 ("story29","light","Quadril do bebê","Sinais da displasia","Pregas assimétricas, uma perna mais curta ou dificuldade de abrir a perna merecem avaliação."),
 ("story30","dark","Dúvida comum","Dor de crescimento","Costuma ser nas duas pernas, à noite, e melhora pela manhã. Dor de um lado só, vale avaliar."),
 ("story31","light","Marcha da criança","Pé virado para dentro","Muitas vezes faz parte do desenvolvimento e melhora com o tempo. Se piora ou é assimétrico, avalie."),
 ("story32","dark","Mito","Palmilha corrige tudo?","Nem sempre. A indicação depende do caso — o exame é que diz o que realmente ajuda."),
 ("story33","light","Quando investigar","Pernas de tamanhos diferentes","Diferenças que aumentam, fazem mancar ou vêm de fratura ou infecção merecem avaliação."),
 ("story34","dark","Fixador externo","Cuidando dos pinos","Manter limpo e seco e observar vermelhidão ou secreção faz parte do tratamento."),
 ("story35","light","Como funciona","O corpo cria osso novo","Após um corte planejado, o osso se alonga em fases: espera, distração e consolidação."),
 ("story36","dark","Segunda opinião","Não há mais o que fazer?","Em casos complexos, costuma valer um segundo olhar antes de desistir do tratamento."),
 ("story37","light","Marcha da criança","Andar na ponta dos pés","Comum nos primeiros anos. Se persiste ou é só de um lado, vale uma avaliação."),
 ("story38","dark","Sinal de alerta","Quando a criança manca","Mancar sem melhora, com dor ou febre, não é o esperado — procure avaliação."),
 ("story39","light","Acolhimento","Casos difíceis têm caminho","Avaliação cuidadosa, plano realista e acompanhamento de perto. Agende pelo WhatsApp."),
]

def run():
    posts=json.load(open(os.path.join(ROOT,"posts.json"),encoding="utf-8"))
    stories=json.load(open(os.path.join(ROOT,"stories.json"),encoding="utf-8"))
    pids={p["id"] for p in posts}; sids={s["id"] for s in stories}
    for pid,slides,caption in POSTS:
        if pid in pids: print("pulando (existe):",pid); continue
        imgs=[]
        for i,s in enumerate(slides,1):
            fn=f"{pid}_{i}.jpg"; pslide(s,fn); imgs.append("images/"+fn)
        posts.append({"id":pid,"images":imgs,"caption":caption})
    for sid,v,k,t,sub in STORIES:
        if sid in sids: print("pulando (existe):",sid); continue
        fn=sid+".jpg"; story(fn,v,k,t,sub); stories.append({"id":sid,"image":"images/"+fn})
    json.dump(posts,open(os.path.join(ROOT,"posts.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
    json.dump(stories,open(os.path.join(ROOT,"stories.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
    print("Biblioteca -> posts:",len(posts),"| stories:",len(stories))

if __name__=="__main__":
    run()
