# -*- coding: utf-8 -*-
"""
Gerador de REEL-EPISODIO NARRATIVO (serie "Pe no Chao") — modelo faceless.
PREVIEW LOCAL renderiza so o VISUAL (cinetipografia narrativa + motivo + musica).
A VOZ (Piper faber) + legenda karaoke entram no GitHub Actions (rede). vo=narracao.
"""
import os, json, glob, shutil, subprocess, math
from PIL import Image, ImageDraw, ImageFont

W, H, FPS = 1080, 1920, 30
INK=(20,20,26); CREAM=(243,226,200); GOLD=(176,140,79)
TXT_L=(206,198,184); MUT_L=(150,144,132); FAINT=(78,74,68)
FD="/usr/share/fonts/truetype/liberation/"
SB="LiberationSerif-Bold.ttf"; NR="LiberationSans-Regular.ttf"; NB="LiberationSans-Bold.ttf"
M=120
ROOT=os.path.dirname(os.path.abspath(__file__))
AUDIO_DIR=os.path.join(ROOT,"audio")
FRAMES="/tmp/_reelnarr"
SIG="Dr. Rafael Vargas · CRM-SP 226103 · RQE 137901"
DISC="Conteúdo educativo · não substitui avaliação médica."
SERIE="Pé no Chão"

_FC={}
def F(n,s):
    k=(n,s)
    if k not in _FC: _FC[k]=ImageFont.truetype(FD+n,s)
    return _FC[k]
_m=ImageDraw.Draw(Image.new("RGB",(8,8)))
def ease(p):
    p=0.0 if p<0 else (1.0 if p>1 else p); return 1-(1-p)**3
def wrap(t,f,mw):
    out=[]; cur=""
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
        wtot=sum(d.textlength(c,font=font)+tr for c in text)-tr; x=x-wtot
    for c in text:
        d.text((x,y),c,font=font,fill=fill); x+=d.textlength(c,font=font)+tr
def paste_text(base,x,y,text,font,color,alpha):
    if alpha<=0 or not text: return
    w=int(_m.textlength(text,font=font))+8; h=int(font.size*1.5)+8
    tile=Image.new("RGBA",(max(w,2),max(h,2)),(0,0,0,0))
    ImageDraw.Draw(tile).text((4,2),text,font=font,fill=color+(255,))
    if alpha<255: tile.putalpha(tile.split()[3].point(lambda v: v*alpha//255))
    base.paste(tile,(int(x-4),int(y-2)),tile)

def base_frame(ep, idx, n, kicker, t_global, total):
    img=Image.new("RGB",(W,H),INK)
    ov=Image.new("RGBA",(W,H),(0,0,0,0)); da=ImageDraw.Draw(ov)
    for rad in [560,500,440,380,320]:
        da.arc([W//2-rad,H-120-rad,W//2+rad,H-120+rad],200,340,fill=(176,140,79,55),width=2)
    img=Image.alpha_composite(img.convert("RGBA"),ov).convert("RGB"); d=ImageDraw.Draw(img)
    d.text((M,140),"RV",font=F(SB,56),fill=CREAM); wf=d.textlength("RV",font=F(SB,56))
    d.line([(M+wf+22,150),(M+wf+22,196)],fill=GOLD,width=2)
    d.text((M+wf+40,146),"Dr. Rafael Vargas",font=F(NR,25),fill=CREAM)
    d.text((M+wf+40,178),"Ortopedia · São Paulo",font=F(NR,21),fill=GOLD)
    trk(d,(W-M,150),f"EP {ep:02d}",F(NB,30),GOLD,3,left=False)
    trk(d,(M,250),SERIE.upper(),F(NB,26),GOLD,6)
    d.line([(M,292),(M+64,292)],fill=GOLD,width=3)
    if kicker:
        trk(d,(M,560),kicker.upper(),F(NB,28),GOLD,5)
        d.line([(M,602),(M+58,602)],fill=GOLD,width=3)
    d.text((M,H-176),"@rafaelvargasmd",font=F(NR,27),fill=MUT_L)
    d.line([(M,H-118),(W-M,H-118)],fill=(70,66,60),width=2)
    d.text((M,H-104),SIG,font=F(NR,21),fill=MUT_L)
    d.text((M,H-72),DISC,font=F(NR,20),fill=MUT_L)
    pw=int((t_global/total)*(W-2*M))
    d.line([(M,H-128),(W-M,H-128)],fill=FAINT,width=4)
    d.line([(M,H-128),(M+pw,H-128)],fill=GOLD,width=4)
    return img

def draw_no(img, cx, cy, r, alpha):
    if alpha<=0: return
    ov=Image.new("RGBA",(W,H),(0,0,0,0)); d=ImageDraw.Draw(ov)
    col=(196,72,60,alpha)
    d.ellipse([cx-r,cy-r,cx+r,cy+r],outline=col,width=14)
    a=math.radians(45); dx,dy=math.cos(a)*r*0.74,math.sin(a)*r*0.74
    d.line([(cx-dx,cy+dy),(cx+dx,cy-dy)],fill=col,width=14)
    img.paste(Image.alpha_composite(img.convert("RGBA"),ov).convert("RGB"),(0,0))

EP01 = {
 "ep":1, "slug":"andador",
 "scenes":[
  {"dur":3.6,"kicker":"Mito x Verdade","screen":["O andador NÃO","ensina a andar."],
   "emph":"NÃO","sub":"Vou te contar por quê — e o que ajuda de verdade.",
   "vo":"O andador não ensina o bebê a andar. E pode até atrapalhar."},
  {"dur":4.0,"kicker":"O que parece","screen":["Parece que ajuda:","a criança se move."],
   "emph":None,"sub":"Mas no andador ela só desliza — empurra com a ponta dos pés.",
   "vo":"Parece que ajuda, porque a criança se move. Mas ali ela só desliza, empurrando com a ponta dos pés.","motif":"no"},
  {"dur":4.2,"kicker":"O que de fato acontece","screen":["Andar de verdade","é equilíbrio."],
   "emph":"equilíbrio","sub":"E o equilíbrio se aprende caindo, levantando e sustentando o próprio peso.",
   "vo":"Andar de verdade é equilíbrio. E equilíbrio se aprende caindo, levantando, sustentando o próprio peso."},
  {"dur":4.2,"kicker":"E tem mais","screen":["Em excesso, está","associado a quedas."],
   "emph":"quedas","sub":"E muda a forma como a criança apoia o quadril enquanto ele se forma.",
   "vo":"Em excesso, o andador está associado a quedas — e muda a forma como a criança apoia o quadril enquanto ele ainda se forma."},
  {"dur":4.2,"kicker":"O que ajuda","screen":["Chão livre.","Descalço. Tempo."],
   "emph":"Tempo","sub":"O empurrador entra depois, quando ela já fica de pé sozinha.",
   "vo":"O que ajuda é simples: chão livre, descalço e tempo. O empurrador entra depois, quando ela já fica de pé sozinha."},
  {"dur":3.6,"kicker":"Passa adiante","screen":["Manda pra quem","ainda usa andador."],
   "emph":None,"sub":"Um pai, uma mãe, uma avó. Salva pra lembrar.",
   "vo":"Manda esse vídeo pra quem ainda usa andador. Um pai, uma mãe, uma avó.","cta":True},
 ],
 "caption":("Mito x Verdade: o andador NÃO ensina o bebê a andar.\n\n"
   "Parece que ajuda porque a criança se move — mas no andador ela só desliza, "
   "empurrando com a ponta dos pés. Andar de verdade é equilíbrio, e equilíbrio se "
   "aprende sustentando o próprio peso: caindo, levantando, firmando. Usado em excesso, "
   "o andador está associado a quedas e muda o apoio do quadril enquanto ele se forma.\n\n"
   "O que ajuda é simples: chão livre, descalço e tempo. O empurrador (aquele de empurrar "
   "em pé) entra depois, quando o bebê já fica de pé sozinho.\n\n"
   "Manda pra um pai, mãe ou avó que ainda usa andador. Salva pra lembrar.\n\n"
   "#ortopediapediatrica #ortopediainfantil #desenvolvimentoinfantil #primeirospassos "
   "#maternidade #andador #saudedacrianca #ortopediasaopaulo\n\n"+SIG)
}

def render(ep_data, out_mp4, music_path=None):
    scenes=ep_data["scenes"]; ep=ep_data["ep"]; n=len(scenes)
    if os.path.isdir(FRAMES): shutil.rmtree(FRAMES,ignore_errors=True)
    os.makedirs(FRAMES,exist_ok=True)
    bounds=[]; acc=0.0
    for i,s in enumerate(scenes): bounds.append((acc,acc+s["dur"],i,s)); acc+=s["dur"]
    total=acc; nframes=int(total*FPS)
    BIG=F(SB,96); SUBF=F(NR,40); CTAF=F(NB,52)
    for f in range(nframes):
        t=f/FPS; cur=bounds[-1]
        for b in bounds:
            if b[0]<=t<b[1]: cur=b; break
        t0,t1,idx,scene=cur; tl=t-t0
        img=base_frame(ep,idx+1,n,scene["kicker"],t,total)
        if scene.get("motif")=="no":
            a=int(255*ease((tl-0.5)/0.6)); draw_no(img,W-M-90,470,70,min(a,235))
        lines=scene["screen"]; emph=scene.get("emph")
        tf=BIG
        if any(_m.textlength(ln,font=tf)>W-2*M for ln in lines): tf=F(SB,80)
        ty=680
        for li,ln in enumerate(lines):
            p=ease((tl-0.10-0.18*li)/0.5); dy=(1-p)*34
            if emph and emph in ln:
                pre,_,post=ln.partition(emph); x=M
                if pre: paste_text(img,x,ty+dy,pre,tf,CREAM,int(255*p)); x+=_m.textlength(pre,font=tf)
                paste_text(img,x,ty+dy,emph,tf,GOLD,int(255*p)); x+=_m.textlength(emph,font=tf)
                if post: paste_text(img,x,ty+dy,post,tf,CREAM,int(255*p))
            else:
                paste_text(img,M,ty+dy,ln,tf,CREAM,int(255*p))
            ty+=int(tf.size*1.08)
        sub=scene.get("sub")
        if sub:
            sy=ty+44; ps=ease((tl-0.55)/0.5)
            for sl in wrap(sub,SUBF,W-2*M):
                paste_text(img,M,sy,sl,SUBF,TXT_L,int(255*ps)); sy+=56
        if scene.get("cta"):
            pc=ease((tl-0.9)/0.6)
            paste_text(img,M,H-300,"Compartilhar = enviar no direct",CTAF,GOLD,int(235*pc))
        img.save(os.path.join(FRAMES,f"f{f:05d}.jpg"),"JPEG",quality=91)
    if music_path and os.path.exists(music_path):
        bed="/tmp/_bedn.wav"
        subprocess.run(["ffmpeg","-y","-i",music_path,"-vn","-map","0:a:0","-af",
          f"atrim=0:{total:.2f},loudnorm=I=-22:TP=-2:LRA=11,afade=t=in:d=0.5,"
          f"afade=t=out:st={total-1.2:.2f}:d=1.2,aformat=sample_rates=48000:channel_layouts=stereo",
          "-t",f"{total:.2f}",bed],check=True,capture_output=True)
        ain=["-i",bed]
    else:
        ain=["-f","lavfi","-i","anullsrc=channel_layout=stereo:sample_rate=48000"]
    cmd=["ffmpeg","-y","-framerate",str(FPS),"-i",os.path.join(FRAMES,"f%05d.jpg")]+ain+[
      "-c:v","libx264","-pix_fmt","yuv420p","-profile:v","high","-r","30",
      "-c:a","aac","-b:a","160k","-shortest","-movflags","+faststart",out_mp4]
    subprocess.run(cmd,check=True,capture_output=True)
    return round(total,1)

if __name__=="__main__":
    import sys
    out=sys.argv[1] if len(sys.argv)>1 else "/tmp/preview_andador.mp4"
    tracks=sorted(glob.glob(os.path.join(AUDIO_DIR,"*.mp4"))+glob.glob(os.path.join(AUDIO_DIR,"*.mp3")))
    music=tracks[1] if len(tracks)>1 else (tracks[0] if tracks else None)
    dur=render(EP01,out,music)
    print("OK",out,dur,"s","| trilha:",os.path.basename(music) if music else "mudo")
