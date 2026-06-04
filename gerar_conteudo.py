# -*- coding: utf-8 -*-
"""
Gerador de conteudo (REABASTECIMENTO) para a biblioteca do Instagram do Dr. Rafael Vargas.

Como usar:
1) Preencha as listas POSTS e STORIES abaixo com temas NOVOS (que ainda nao existam
   em posts.json / stories.json). Use ids sequenciais (postNN / storyNN).
2) Rode:  python gerar_conteudo.py
   Ele renderiza as imagens em images/ e ANEXA as entradas em posts.json e stories.json
   (ignora ids que ja existirem).
3) Abra o GitHub Desktop -> commit -> Push. O robo publica em ordem, sem repetir
   (Ter/Qui/Sab posts 19:00, Seg/Qua/Sex stories 12:30, horario de Brasilia).

Padrao da marca: preto #14141A, creme #F3E2C8, dourado #B08C4F, fundo claro #F6F4EF.
Titulos serifados; rotulo dourado com tracking; monograma RV; arcos dourados.
Assinatura obrigatoria (CFM) no slide final / rodape:
  Dr. Rafael Vargas · Médico · CRM-SP 226103 · RQE 137901
Conteudo EDUCATIVO, sem prometer resultado, em conformidade com o CFM.

Specs de slide:
  POST  -> spec dict: {"variant":"dark"/"light","kicker":..,"title":..,
                       "body"(opc):..,"tag"(opc):"arraste →","foot"(opc):SIG,"tsize"(opc):int}
  STORY -> (id, variant, kicker, title, sub)
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
def cap(corpo,tags): return corpo+"\n\n"+SIG+"\n\n"+tags

# ====== PREENCHA COM TEMAS NOVOS (deixe vazio para nao gerar) ======
# POSTS: lista de (id, [slides...], caption)   STORIES: (id, variant, kicker, title, sub)
POSTS = [
]
STORIES = [
]
# ===================================================================

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
