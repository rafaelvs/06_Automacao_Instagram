# -*- coding: utf-8 -*-
"""
Motor de craft dos reels narrativos "Pé no Chão" (compartilhado preview/voz).
Craft validado: 30fps, easing com OVERSHOOT na entrada do texto, palavra-chave dourada com
pop de escala, motivo de marca (PEGADAS subindo = primeiros passos) preenchendo o meio,
SAFE ZONE corrigida (rodapé CRM/RQE/disclaimer dentro da área visível; base livre p/ UI do IG),
barra de progresso, fundo com leve parallax.
"""
import os, glob, shutil, subprocess, math
from PIL import Image, ImageDraw, ImageFont

W, H, FPS = 1080, 1920, 30
INK=(18,18,24); CREAM=(243,226,200); GOLD=(176,140,79); TXT_L=(206,198,184); MUT_L=(150,144,132); FAINT=(70,66,60); RED=(196,72,60)
FD="/usr/share/fonts/truetype/liberation/"; SB="LiberationSerif-Bold.ttf"; NR="LiberationSans-Regular.ttf"; NB="LiberationSans-Bold.ttf"
M=120
SIG="Dr. Rafael Vargas · CRM-SP 226103 · RQE 137901"
DISC="Conteúdo educativo · não substitui avaliação médica."
SERIE="Pé no Chão"
_FC={}
def F(n,s):
    k=(n,s)
    if k not in _FC: _FC[k]=ImageFont.truetype(FD+n,s)
    return _FC[k]
_m=ImageDraw.Draw(Image.new("RGB",(8,8)))
def eoutc(p): p=0 if p<0 else(1 if p>1 else p); return 1-(1-p)**3
def eback(p):
    p=0 if p<0 else(1 if p>1 else p); c1=1.70158; c3=c1+1; return 1+c3*(p-1)**3+c1*(p-1)**2
def wrap(t,f,mw):
    out=[];cur=""
    for w in t.split():
        s=(cur+" "+w).strip()
        if _m.textlength(s,font=f)<=mw: cur=s
        else:
            if cur: out.append(cur)
            cur=w
    if cur: out.append(cur)
    return out
def trk(d,xy,text,font,fill,tr,left=True):
    x,y=xy
    if not left:
        wt=sum(d.textlength(c,font=font)+tr for c in text)-tr; x=x-wt
    for c in text: d.text((x,y),c,font=font,fill=fill); x+=d.textlength(c,font=font)+tr
def ptxt(base,x,y,text,font,color,alpha,scale=1.0):
    if alpha<=0 or not text: return
    w=int(_m.textlength(text,font=font))+10; h=int(font.size*1.5)+10
    tile=Image.new("RGBA",(max(w,2),max(h,2)),(0,0,0,0)); ImageDraw.Draw(tile).text((5,3),text,font=font,fill=color+(255,))
    if scale!=1.0:
        nw,nh=max(1,int(tile.width*scale)),max(1,int(tile.height*scale)); tile=tile.resize((nw,nh),Image.LANCZOS); x-=(tile.width-w)/2; y-=(tile.height-h)/2
    if alpha<255: tile.putalpha(tile.split()[3].point(lambda v:v*alpha//255))
    base.paste(tile,(int(x-5),int(y-3)),tile)
def _foot(sz,alpha):
    t=Image.new("RGBA",(sz,sz),(0,0,0,0)); d=ImageDraw.Draw(t); c=sz//2; col=GOLD+(alpha,)
    d.ellipse([c-16,int(sz*0.34),c+16,int(sz*0.70)],fill=col); d.ellipse([c-11,int(sz*0.72),c+11,int(sz*0.93)],fill=col)
    for dx in(-15,-6,3,12): d.ellipse([c+dx-4,int(sz*0.26),c+dx+4,int(sz*0.345)],fill=col)
    return t
FPATH=[(M+30,1340,18,-1),(M+170,1300,-10,1),(M+310,1262,16,-1),(W//2,1224,-8,1),
       (W-M-310,1186,16,-1),(W-M-170,1150,-10,1),(W-M-30,1112,14,-1)]
def _feet(img,prog):
    n=len(FPATH)
    for i,(x,y,ang,side) in enumerate(FPATH):
        a=eoutc((prog-i/(n+1))/0.10)
        if a<=0: continue
        ft=_foot(92,int(60*a)).rotate(ang+8*side,expand=True,resample=Image.BICUBIC)
        img.paste(ft,(int(x-ft.width/2+side*14),int(y-ft.height/2)),ft)
def _bone(img,prog):
    """Motivo da série OSSO NOVO: o osso novo preenchendo o vão (linha que cresce das duas
    pontas pro centro) + uma régua de milímetros por baixo. Identidade INK/CREAM/GOLD."""
    ov=Image.new("RGBA",(W,H),(0,0,0,0)); d=ImageDraw.Draw(ov)
    y=1230; x0,x1=M+30,W-M-30; cx=(x0+x1)//2; gap=150  # vão central que o osso novo preenche
    a=int(60); end=GOLD+(a,)
    # duas pontas de osso (segmentos sólidos), com "cabeças" arredondadas
    d.line([(x0,y),(cx-gap,y)],fill=end,width=10); d.line([(cx+gap,y),(x1,y)],fill=end,width=10)
    for ex in (x0,x1):
        d.ellipse([ex-13,y-16,ex+13,y+16],fill=end)
    # osso novo crescendo das duas pontas pro centro conforme prog
    fill=eoutc(min(1.0,prog/0.85)); half=int(gap*fill)
    nb=GOLD+(int(90*fill),)
    if half>0:
        d.line([(cx-gap,y),(cx-gap+half,y)],fill=nb,width=12)
        d.line([(cx+gap,y),(cx+gap-half,y)],fill=nb,width=12)
        # textura de trabéculas (tracinhos diagonais) na zona recém-formada
        for xx in range(cx-gap, cx-gap+half, 18):
            d.line([(xx,y-9),(xx+9,y+9)],fill=GOLD+(int(55*fill),),width=2)
        for xx in range(cx+gap, cx+gap-half, -18):
            d.line([(xx,y-9),(xx-9,y+9)],fill=GOLD+(int(55*fill),),width=2)
    # régua de milímetros (motivo secundário) logo abaixo
    ry=y+70; d.line([(x0,ry),(x1,ry)],fill=GOLD+(34,),width=2)
    for i,xx in enumerate(range(x0,x1+1,26)):
        h=14 if i%5==0 else 7
        d.line([(xx,ry),(xx,ry-h)],fill=GOLD+(34,),width=2)
    img.paste(Image.alpha_composite(img.convert("RGBA"),ov).convert("RGB"),(0,0))
def _bg(drift):
    img=Image.new("RGB",(W,H),INK); ov=Image.new("RGBA",(W,H),(0,0,0,0)); da=ImageDraw.Draw(ov); cy=1720+drift
    for r in(680,580,480,380): da.arc([W//2-r,cy-r,W//2+r,cy+r],204,336,fill=(176,140,79,30),width=2)
    return Image.alpha_composite(img.convert("RGBA"),ov).convert("RGB")
def _no(img,prog,tl):
    a=int(235*eoutc((tl-0.5)/0.6))
    if a<=0: return
    cx,cy,r=W-M-86,470,66; ov=Image.new("RGBA",(W,H),(0,0,0,0)); d=ImageDraw.Draw(ov); col=RED+(a,)
    d.ellipse([cx-r,cy-r,cx+r,cy+r],outline=col,width=13); ang=math.radians(45); dx,dy=math.cos(ang)*r*.74,math.sin(ang)*r*.74
    d.line([(cx-dx,cy+dy),(cx+dx,cy-dy)],fill=col,width=13); img.paste(Image.alpha_composite(img.convert("RGBA"),ov).convert("RGB"),(0,0))
def _header(d,ep,serie=SERIE):
    d.text((M,168),"RV",font=F(SB,54),fill=CREAM); wf=d.textlength("RV",font=F(SB,54))
    d.line([(M+wf+22,178),(M+wf+22,222)],fill=GOLD,width=2)
    d.text((M+wf+40,174),"Dr. Rafael Vargas",font=F(NR,25),fill=CREAM); d.text((M+wf+40,206),"Ortopedia · São Paulo",font=F(NR,21),fill=GOLD)
    trk(d,(W-M,178),f"EP {ep:02d}",F(NB,30),GOLD,3,left=False)
    trk(d,(M,286),serie.upper(),F(NB,25),GOLD,6); d.line([(M,326),(M+62,326)],fill=GOLD,width=3)
def _footer(d,prog):
    fy=1380; d.line([(M,fy),(W-M,fy)],fill=FAINT,width=2)
    d.text((M,fy+22),"@rafaelvargasmd",font=F(NR,26),fill=MUT_L); d.text((M,fy+62),SIG,font=F(NR,21),fill=MUT_L); d.text((M,fy+94),DISC,font=F(NR,20),fill=MUT_L)
    by=fy-14; pw=int(prog*(W-2*M)); d.line([(M,by),(W-M,by)],fill=FAINT,width=4); d.line([(M,by),(M+pw,by)],fill=GOLD,width=4)

def render_frames(episode, durs, frames_dir):
    """Renderiza os JPGs do episódio. durs = lista de durações (s) por cena."""
    shutil.rmtree(frames_dir,ignore_errors=True); os.makedirs(frames_dir)
    S=episode["scenes"]; ep=episode["ep"]
    serie=episode.get("serie",SERIE); motif_fam=episode.get("motif_family","feet")
    bnd=[]; acc=0.0
    for i,dch in enumerate(durs): bnd.append((acc,acc+dch,i)); acc+=dch
    total=acc; nf=int(total*FPS); BIG=F(SB,98); SUB=F(NR,40); T82=F(SB,82)
    for f in range(nf):
        t=f/FPS; cur=bnd[-1]
        for b in bnd:
            if b[0]<=t<b[1]: cur=b; break
        t0,t1,idx=cur; tl=t-t0; s=S[idx]; drift=int(8*math.sin(t*0.5))
        img=_bg(drift)
        if motif_fam=="bone": _bone(img,t/total)
        else: _feet(img,t/total)
        d=ImageDraw.Draw(img)
        if s.get("motif")=="no": _no(img,t/total,tl); d=ImageDraw.Draw(img)
        _header(d,ep,serie)
        trk(d,(M,560),s["k"].upper(),F(NB,28),GOLD,5); d.line([(M,602),(M+56,602)],fill=GOLD,width=3)
        ln=s["sc"]; emph=s.get("e"); tf=BIG
        if any(_m.textlength(x,font=tf)>W-2*M for x in ln): tf=T82
        ty=680
        for li,L in enumerate(ln):
            pr=(tl-0.08-0.16*li)/0.6; yo=(1-eback(pr))*-46; a=int(255*eoutc((tl-0.08-0.16*li)/0.4))
            if emph and emph in L:
                pre,_,post=L.partition(emph); x=M
                if pre: ptxt(img,x,ty+yo,pre,tf,CREAM,a); x+=_m.textlength(pre,font=tf)
                sc=1.0+0.06*(1-eoutc((tl-0.08-0.16*li)/0.5)); ptxt(img,x,ty+yo,emph,tf,GOLD,a,scale=sc); x+=_m.textlength(emph,font=tf)
                if post: ptxt(img,x,ty+yo,post,tf,CREAM,a)
            else: ptxt(img,M,ty+yo,L,tf,CREAM,a)
            ty+=int(tf.size*1.06)
        if s.get("sub"):
            sy=ty+40; pa=int(255*eoutc((tl-0.5)/0.5))
            for sl in wrap(s["sub"],SUB,W-2*M): ptxt(img,M,sy,sl,SUB,TXT_L,pa); sy+=56
        if s.get("cta"):
            pc=eoutc((tl-0.9)/0.6); ptxt(img,M,1330,"Compartilhar = enviar no direct",F(NB,46),GOLD,int(220*pc))
        _footer(d,t/total)
        img.save(f"{frames_dir}/f{f:05d}.jpg","JPEG",quality=92)
    return total, nf

def encode(frames_dir, audio_args, out_mp4):
    cmd=["ffmpeg","-y","-framerate",str(FPS),"-i",f"{frames_dir}/f%05d.jpg"]+audio_args+[
        "-c:v","libx264","-pix_fmt","yuv420p","-profile:v","high","-r","30","-c:a","aac","-b:a","192k",
        "-shortest","-movflags","+faststart",out_mp4]
    subprocess.run(cmd,check=True,capture_output=True)
