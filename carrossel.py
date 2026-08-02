# -*- coding: utf-8 -*-
"""
Gerador de CARROSSEL para o feed (4:5, 1080x1350) — substitui os 'panfletos' de imagem unica.
Cada post = capa (gancho + 'arraste') -> slides de conteudo (1 ideia cada) -> CTA (salve/manda/WhatsApp).
Mesma identidade dos reels (INK/CREAM/GOLD, arcos, serifa). CFM: educativo, sem prometer resultado,
sem paciente real, assinatura + disclaimer. Guardrail: nada de alongamento sob angulo estetico/altura.
"""
import os, json
from PIL import Image, ImageDraw, ImageFont
W,H = 1080,1350; M=110
INK=(18,18,24); CREAM=(243,226,200); GOLD=(176,140,79); TXT=(206,198,184); MUT=(150,144,132); FAINT=(70,66,60)
FD="/usr/share/fonts/truetype/liberation/"; SB="LiberationSerif-Bold.ttf"; NR="LiberationSans-Regular.ttf"; NB="LiberationSans-Bold.ttf"
SIG="Dr. Rafael Vargas · Médico · CRM-SP 226103 · RQE 137901"; DISC="Conteúdo educativo · não substitui avaliação médica."
_FC={}
def F(n,s):
    k=(n,s)
    if k not in _FC: _FC[k]=ImageFont.truetype(FD+n,s)
    return _FC[k]
_m=ImageDraw.Draw(Image.new("RGB",(8,8)))
def wrap(t,f,mw):
    out=[];cur=""
    for w in t.split():
        s=(cur+" "+w).strip()
        if _m.textlength(s,font=f)<=mw:cur=s
        else:
            if cur:out.append(cur)
            cur=w
    if cur:out.append(cur)
    return out
def trk(d,xy,text,font,fill,tr,left=True):
    x,y=xy
    if not left:
        wt=sum(d.textlength(c,font=font)+tr for c in text)-tr;x-=wt
    for c in text:d.text((x,y),c,font=font,fill=fill);x+=d.textlength(c,font=font)+tr
# Variacao visual por peca (regra 4 v6 — feedback Leo 08/07). ADITIVO/fail-safe: sem o modulo, GOLD.
try:
    import estilo_variacao as _EV
except Exception:
    _EV=None
def _var(post_id):
    return _EV.variante(post_id) if _EV else None
def base(motif=True, var=None):
    img=Image.new("RGB",(W,H),INK); ov=Image.new("RGBA",(W,H),(0,0,0,0)); da=ImageDraw.Draw(ov)
    if motif:
        if var and _EV: _EV.desenha_motivo(da,W,H,var["motivo"],var["acento"],alpha=58)
        else:
            cy=1180
            for r in(560,470,380,300): da.arc([W//2-r,cy-r,W//2+r,cy+r],202,338,fill=(176,140,79,34),width=2)
    img=Image.alpha_composite(img.convert("RGBA"),ov).convert("RGB"); d=ImageDraw.Draw(img)
    d.text((M,86),"RV",font=F(SB,46),fill=CREAM); wf=d.textlength("RV",font=F(SB,46))
    d.line([(M+wf+20,94),(M+wf+20,132)],fill=GOLD,width=2)
    d.text((M+wf+36,90),"Dr. Rafael Vargas",font=F(NR,23),fill=CREAM); d.text((M+wf+36,120),"Ortopedia · São Paulo",font=F(NR,19),fill=GOLD)
    return img,d
def footer(d,page,n,cta=False,ac=GOLD):
    d.line([(M,H-150),(W-M,H-150)],fill=FAINT,width=2)
    d.text((M,H-128),"@rafaelvargasmd",font=F(NR,24),fill=MUT)
    d.text((M,H-94),SIG,font=F(NR,19),fill=MUT); d.text((M,H-64),DISC,font=F(NR,18),fill=MUT)
    # indicador de paginas (bolinhas) — usa o acento da peca
    bx=W-M-(n*22);
    for i in range(n):
        c=ac if i==page else FAINT
        d.ellipse([bx+i*22, H-126, bx+i*22+10, H-116], fill=c)

def render_post(post, outdir):
    sl=post["slides"]; n=len(sl); paths=[]
    os.makedirs(outdir, exist_ok=True)
    var=_var(post.get("id","")); AC=var["acento"] if var else GOLD; DY=var["dy"] if var else 0
    HE=var["hook_escala"] if var else 1.0
    for i,s in enumerate(sl):
        img,d=base(motif=True,var=var)
        trk(d,(M,300),s.get("kicker",("EDUCATIVO" if i==0 else "")).upper(),F(NB,24),AC,5)
        d.line([(M,340),(M+58,340)],fill=AC,width=3)
        if i==0:  # CAPA
            tf=F(SB,int(92*HE)); tl=wrap(s["title"],tf,W-2*M)
            if len(tl)>3: tf=F(SB,int(76*HE)); tl=wrap(s["title"],tf,W-2*M)
            ty=380+DY
            for ln in tl: d.text((M,ty),ln,font=tf,fill=CREAM); ty+=int(tf.size*1.08)
            if s.get("sub"):
                ty+=24
                for ln in wrap(s["sub"],F(NR,38),W-2*M): d.text((M,ty),ln,font=F(NR,38),fill=TXT); ty+=54
            trk(d,(M,H-210),"ARRASTE →",F(NB,30),AC,4)
        elif s.get("cta"):
            tf=F(SB,80); ty=400+DY
            for ln in wrap(s["title"],tf,W-2*M): d.text((M,ty),ln,font=tf,fill=CREAM); ty+=int(tf.size*1.1)
            ty+=20
            for ln in wrap(s.get("sub",""),F(NR,38),W-2*M): d.text((M,ty),ln,font=F(NR,38),fill=TXT); ty+=54
            d.text((M,H-250),"Agende pelo WhatsApp",font=F(NB,42),fill=AC); d.text((M,H-198),"link na bio",font=F(NR,34),fill=TXT)
        else:  # CONTEUDO
            tf=F(SB,70); ty=400+DY
            for ln in wrap(s["title"],tf,W-2*M): d.text((M,ty),ln,font=tf,fill=CREAM); ty+=int(tf.size*1.12)
            ty+=28
            for ln in wrap(s["body"],F(NR,42),W-2*M): d.text((M,ty),ln,font=F(NR,42),fill=TXT); ty+=60
        footer(d,i,n,cta=s.get("cta",False),ac=AC)
        p=os.path.join(outdir,f"{post['id']}_{i+1}.jpg"); img.save(p,"JPEG",quality=92); paths.append("images/"+os.path.basename(p))
    return paths

# ---- exemplo: refaz o post03 'Fixador externo' como CARROSSEL ----
EXEMPLO={"id":"post03","slides":[
 {"kicker":"Educativo","title":"Fixador externo: pra que serve?","sub":"E por que não é “caso perdido”. Arrasta que eu explico."},
 {"kicker":"O que é","title":"Uma estrutura por fora do corpo","body":"Hastes e pinos seguram o osso por fora da pele, estabilizando enquanto ele cura ou se reconstrói."},
 {"kicker":"Pra que serve","title":"Estabilizar o que é complexo","body":"Fraturas graves, ossos que não colaram e correção de deformidades — situações em que o gesso não basta."},
 {"kicker":"A vantagem","title":"Ajuste fino, sem nova cirurgia","body":"Por ficar por fora, dá pra corrigir aos poucos ao longo do tratamento, sem reabrir a cada etapa."},
 {"kicker":"Mito x Verdade","title":"Não é “gaiola” nem fim de linha","body":"É uma ferramenta precisa e temporária. Na maioria dos casos, sai quando o osso cumpre seu papel."},
 {"kicker":"Passa adiante","cta":True,"title":"Salve e mande pra quem precisa","sub":"Para um familiar que vai passar por isso, ou que ficou assustado com o aparelho."},
]}

if __name__=="__main__":
    ROOT=os.path.dirname(os.path.abspath(__file__))
    paths=render_post(EXEMPLO, os.path.join(ROOT,"images"))
    print("slides gerados:", len(paths)); print(paths)

# ================= BIBLIOTECA DOS 9 (panfletos -> carrosseis) =================
def cta(t,s): return {"cta":True,"kicker":"Passa adiante","title":t,"sub":s}
POSTS=[
 {"id":"post03","slides":[
  {"kicker":"Educativo","title":"Fixador externo: pra que serve?","sub":"E por que não é “caso perdido”. Arrasta que eu explico."},
  {"kicker":"O que é","title":"Uma estrutura por fora do corpo","body":"Hastes e pinos seguram o osso por fora da pele, estabilizando enquanto ele cura ou se reconstrói."},
  {"kicker":"Pra que serve","title":"Estabilizar o que é complexo","body":"Fraturas graves, ossos que não colaram e correção de deformidades — quando o gesso não basta."},
  {"kicker":"A vantagem","title":"Ajuste fino, sem nova cirurgia","body":"Por ficar por fora, dá pra corrigir aos poucos ao longo do tratamento, sem reabrir a cada etapa."},
  {"kicker":"Mito x Verdade","title":"Não é “gaiola” nem fim de linha","body":"É uma ferramenta precisa e temporária. Costuma sair quando o osso cumpre seu papel."},
  cta("Salve e mande pra quem precisa","Para um familiar que vai passar por isso ou que se assustou com o aparelho.")]},
 {"id":"post04","slides":[
  {"kicker":"Educativo","title":"Uma perna mais curta que a outra?","sub":"Quando é só detalhe e quando merece um olhar. Arrasta."},
  {"kicker":"O que é comum","title":"Pequenas diferenças existem","body":"Diferenças de poucos milímetros são frequentes e muitas vezes não causam sintoma algum."},
  {"kicker":"Quando investigar","title":"Quando passa a incomodar","body":"Se aumenta, faz mancar, dói, ou apareceu depois de fratura ou infecção — vale avaliar."},
  {"kicker":"Na criança","title":"O crescimento muda tudo","body":"Acompanhar a evolução ao longo do tempo é parte do diagnóstico, não só uma medida isolada."},
  {"kicker":"O que define","title":"Medir certo guia a conduta","body":"A avaliação clínica somada à imagem diz se é observar, usar palmilha ou tratar."},
  cta("Salve pra lembrar dos sinais","E mande pra um pai ou mãe que está com essa dúvida em casa.")]},
 {"id":"post05","slides":[
  {"kicker":"Educativo","title":"Fratura que não cola?","sub":"Tem nome — pseudartrose — e tem caminho. Arrasta."},
  {"kicker":"O que é","title":"O osso parou de consolidar","body":"Quando a fratura não “fecha” no tempo esperado, chamamos de pseudartrose."},
  {"kicker":"Por que acontece","title":"Quase sempre tem uma causa","body":"Instabilidade, pouca circulação no local, infecção ou perda de osso costumam estar por trás."},
  {"kicker":"O que muda","title":"O tratamento ataca a causa","body":"Estabilizar bem, estimular o osso e, às vezes, enxerto — o plano depende do motivo."},
  {"kicker":"A mensagem","title":"Não é azar, é um problema com plano","body":"Identificada a causa, existe estratégia. O importante é não deixar arrastar."},
  cta("Salve e compartilhe","Com alguém que está há meses com uma fratura que não cola.")]},
 {"id":"post07","slides":[
  {"kicker":"Sinais","title":"Quando procurar um especialista?","sub":"4 situações de caso complexo que pedem avaliação. Arrasta."},
  {"kicker":"Sinal 1","title":"Fratura que não colou","body":"Passou o tempo esperado e o osso não consolidou? Vale uma avaliação dedicada."},
  {"kicker":"Sinal 2","title":"Deformidade ou perna desigual","body":"Quando atrapalha andar ou a função, a correção entra em cena."},
  {"kicker":"Sinal 3","title":"Sequela de infecção ou perda de osso","body":"Depois de trauma ou infecção, existe caminho de reconstrução."},
  {"kicker":"Sinal 4","title":"Já operou e não resolveu","body":"Uma segunda opinião focada em reconstrução pode mudar o rumo."},
  cta("Salve esse checklist","E mande pra quem está nessa encruzilhada agora.")]},
 {"id":"post08","slides":[
  {"kicker":"Educativo","title":"Tratamento guiado e seriado","sub":"Por que fazer em etapas muda o resultado. Arrasta."},
  {"kicker":"O que é","title":"O tratamento acontece em etapas","body":"Em vez de tudo de uma vez, o caminho é dividido em passos com ajustes ao longo dele."},
  {"kicker":"Por que importa","title":"O corpo responde aos poucos","body":"Corrigir em etapas é mais preciso e seguro do que forçar tudo num momento só."},
  {"kicker":"O acompanhamento","title":"Cada retorno afina o plano","body":"Não é “colocar e esperar”: cada consulta ajusta a rota conforme a resposta."},
  {"kicker":"A mensagem","title":"Método costuma vencer pressa","body":"Paciência com direção entrega resultados melhores que a pressa sem plano."},
  cta("Salve e mande adiante","Pra quem está começando um tratamento longo e ansioso por respostas.")]},
 {"id":"post11","slides":[
  {"kicker":"Consultório","title":"Como é a sua consulta","sub":"O que esperar do primeiro encontro. Arrasta."},
  {"kicker":"Antes","title":"Leve seus exames e o histórico","body":"Raio-X, tomografia e o que já foi feito direcionam toda a avaliação."},
  {"kicker":"Na consulta","title":"Conversa, exame e imagens","body":"Entendo a queixa, examino e analiso os exames junto com você."},
  {"kicker":"O plano","title":"Você sai entendendo o caminho","body":"Diagnóstico, opções e próximos passos — claros, no seu tempo."},
  {"kicker":"Onde","title":"Av. Paulista, São Paulo","body":"Atendimento em consultório, com agendamento pelo WhatsApp."},
  cta("Agende a sua avaliação","Manda “consulta” no WhatsApp do link da bio que a gente organiza.")]},
 {"id":"post12","slides":[
  {"kicker":"Dúvidas","title":"Dói? Quanto tempo? Volto a andar?","sub":"As 3 perguntas que todo mundo faz. Arrasta."},
  {"kicker":"Dói?","title":"O controle da dor é parte do plano","body":"Hoje há muitos recursos para manter o conforto durante o tratamento."},
  {"kicker":"Quanto tempo?","title":"Depende do caso","body":"Reconstruções costumam ser por etapas, com acompanhamento — o tempo é individual."},
  {"kicker":"Volto a andar?","title":"O objetivo é sempre função","body":"Andar e usar o membro é a meta. Cada caso é avaliado de forma própria."},
  {"kicker":"A mensagem","title":"Pergunte tudo na consulta","body":"Informação reduz o medo. Não existe pergunta boba sobre o seu tratamento."},
  cta("Salve essas respostas","E mande pra quem vai começar e está cheio de dúvidas.")]},
 {"id":"post14","slides":[
  {"kicker":"Educativo","title":"Sequela de infecção óssea?","sub":"Existe caminho de reconstrução. Arrasta."},
  {"kicker":"O que acontece","title":"A infecção deixa marcas","body":"Pode sobrar perda de osso, deformidade ou uma fratura que não cola."},
  {"kicker":"O primeiro passo","title":"Tratar a infecção é a base","body":"Sem resolver a infecção, qualquer reconstrução não se sustenta."},
  {"kicker":"A reconstrução","title":"Depois, restaura-se o osso","body":"Com a infecção controlada, dá pra recuperar o osso e o alinhamento em etapas."},
  {"kicker":"A mensagem","title":"Complexo, mas não sem saída","body":"É um caminho de etapas, com plano e acompanhamento próximo."},
  cta("Salve e compartilhe","Com alguém que carrega uma sequela e acha que não há mais o que fazer.")]},
 {"id":"post17","slides":[
  {"kicker":"Educativo","title":"Antes de operar, o planejamento muda tudo","sub":"A etapa invisível que mais pesa no resultado. Arrasta."},
  {"kicker":"O que é","title":"Estudar antes de cortar","body":"Analisar imagens, medir, simular e definir cada passo antes da cirurgia."},
  {"kicker":"Por que importa","title":"Decisão no improviso custa caro","body":"O que é resolvido no planejamento não precisa ser improvisado na sala."},
  {"kicker":"O que você ganha","title":"Menos surpresas, mais clareza","body":"Etapas definidas e expectativa realista desde o começo."},
  {"kicker":"A mensagem","title":"A cirurgia começa antes da sala","body":"O tempo investido em planejar é o que faz o resultado ser previsível."},
  cta("Salve e mande adiante","Pra quem vai operar e quer entender o que está por trás da decisão.")]},
]

def atualizar_todos():
    ROOT=os.path.dirname(os.path.abspath(__file__)); IMG=os.path.join(ROOT,"images")
    pj=os.path.join(ROOT,"posts.json"); posts=json.load(open(pj,encoding="utf-8"))
    by={e["id"]:e for e in posts}
    for post in POSTS:
        paths=render_post(post, IMG)
        if post["id"] in by:
            by[post["id"]]["images"]=paths
            # remove a imagem unica antiga (postNN.jpg) se existir
            old=os.path.join(IMG,post["id"]+".jpg")
            try:
                if os.path.exists(old): os.remove(old)
            except Exception: pass
        print("ok", post["id"], "->", len(paths), "slides")
    json.dump(posts, open(pj,"w",encoding="utf-8"), ensure_ascii=False, indent=2)
    print("posts.json atualizado")

if __name__=="__main__":
    atualizar_todos()
