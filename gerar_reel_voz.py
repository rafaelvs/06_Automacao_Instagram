# -*- coding: utf-8 -*-
"""
Reel-episodio NARRATIVO com VOZ (serie "Pe no Chao"). Roda no GitHub Actions (tem rede).
Pipeline: Piper (faber pt-BR) sintetiza cada cena -> duracoes seguem a narracao ->
cinetipografia (Pillow) -> mix voz/musica nos niveis estudados (voz -16 LUFS, musica -32,
high-pass 120Hz, limiter) -> mp4 9:16 H.264/AAC faststart.

Saida: reels/_preview_pe_no_chao_ep01.mp4  (NAO entra em reels.json -> nao publica sozinho).

Requer no runner: ffmpeg, fonts-liberation, pip install pillow piper-tts, e a voz faber
em voices/pt_BR-faber-medium.onnx (+ .json). Ver workflow render-reel-voz.yml.
"""
import os, glob, subprocess, math, shutil
from PIL import Image, ImageDraw, ImageFont

W, H, FPS = 1080, 1920, 30
INK=(20,20,26); CREAM=(243,226,200); GOLD=(176,140,79)
TXT_L=(206,198,184); MUT_L=(150,144,132); FAINT=(78,74,68)
FD="/usr/share/fonts/truetype/liberation/"
SB="LiberationSerif-Bold.ttf"; NR="LiberationSans-Regular.ttf"; NB="LiberationSans-Bold.ttf"
M=120
ROOT=os.path.dirname(os.path.abspath(__file__))
AUD=os.path.join(ROOT,"audio")
VOICE=os.environ.get("PIPER_VOICE", os.path.join(ROOT,"voices","pt_BR-faber-medium.onnx"))
OUT=os.path.join(ROOT,"reels","_preview_pe_no_chao_ep01.mp4")
TMP="/tmp/_voz"; FR=TMP+"/frames"
SIG="Dr. Rafael Vargas · CRM-SP 226103 · RQE 137901"
DISC="Conteúdo educativo · não substitui avaliação médica."
SERIE="Pé no Chão"
LEAD=0.30; TAIL=0.80   # respiro antes/depois da fala em cada cena

_FC={}
def F(n,s):
    k=(n,s)
    if k not in _FC: _FC[k]=ImageFont.truetype(FD+n,s)
    return _FC[k]
_m=ImageDraw.Draw(Image.new("RGB",(8,8)))
def ease(p):
    p=0.0 if p<0 else(1.0 if p>1 else p); return 1-(1-p)**3
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
        wt=sum(d.textlength(c,font=font)+tr for c in text)-tr;x=x-wt
    for c in text:d.text((x,y),c,font=font,fill=fill);x+=d.textlength(c,font=font)+tr
def pt(base,x,y,text,font,color,alpha):
    if alpha<=0 or not text:return
    w=int(_m.textlength(text,font=font))+8;h=int(font.size*1.5)+8
    tile=Image.new("RGBA",(max(w,2),max(h,2)),(0,0,0,0));ImageDraw.Draw(tile).text((4,2),text,font=font,fill=color+(255,))
    if alpha<255:tile.putalpha(tile.split()[3].point(lambda v:v*alpha//255))
    base.paste(tile,(int(x-4),int(y-2)),tile)
def sbase(ep,kicker,motif):
    img=Image.new("RGB",(W,H),INK);ov=Image.new("RGBA",(W,H),(0,0,0,0));da=ImageDraw.Draw(ov)
    for r in[560,500,440,380,320]:da.arc([W//2-r,H-120-r,W//2+r,H-120+r],200,340,fill=(176,140,79,55),width=2)
    img=Image.alpha_composite(img.convert("RGBA"),ov).convert("RGB");d=ImageDraw.Draw(img)
    d.text((M,140),"RV",font=F(SB,56),fill=CREAM);wf=d.textlength("RV",font=F(SB,56))
    d.line([(M+wf+22,150),(M+wf+22,196)],fill=GOLD,width=2)
    d.text((M+wf+40,146),"Dr. Rafael Vargas",font=F(NR,25),fill=CREAM);d.text((M+wf+40,178),"Ortopedia · São Paulo",font=F(NR,21),fill=GOLD)
    trk(d,(W-M,150),f"EP {ep:02d}",F(NB,30),GOLD,3,left=False)
    trk(d,(M,250),SERIE.upper(),F(NB,26),GOLD,6);d.line([(M,292),(M+64,292)],fill=GOLD,width=3)
    if kicker:trk(d,(M,560),kicker.upper(),F(NB,28),GOLD,5);d.line([(M,602),(M+58,602)],fill=GOLD,width=3)
    d.text((M,H-176),"@rafaelvargasmd",font=F(NR,27),fill=MUT_L);d.line([(M,H-118),(W-M,H-118)],fill=(70,66,60),width=2)
    d.text((M,H-104),SIG,font=F(NR,21),fill=MUT_L);d.text((M,H-72),DISC,font=F(NR,20),fill=MUT_L)
    d.line([(M,H-128),(W-M,H-128)],fill=FAINT,width=4)
    if motif=="no":
        cx,cy,r=W-M-90,470,70;col=(196,72,60,235);o2=Image.new("RGBA",(W,H),(0,0,0,0));d2=ImageDraw.Draw(o2)
        d2.ellipse([cx-r,cy-r,cx+r,cy+r],outline=col,width=14);a=math.radians(45);dx,dy=math.cos(a)*r*.74,math.sin(a)*r*.74
        d2.line([(cx-dx,cy+dy),(cx+dx,cy-dy)],fill=col,width=14);img=Image.alpha_composite(img.convert("RGBA"),o2).convert("RGB")
    return img

S=[
 {"k":"Mito x Verdade","sc":["O andador NÃO","ensina a andar."],"e":"NÃO","sub":"Vou te contar por quê — e o que ajuda de verdade.",
  "vo":"O andador não ensina o bebê a andar. E pode até atrapalhar."},
 {"k":"O que parece","sc":["Parece que ajuda:","a criança se move."],"e":None,"sub":"Mas no andador ela só desliza — empurra com a ponta dos pés.","motif":"no",
  "vo":"Parece que ajuda, porque a criança se move. Mas ali ela só desliza, empurrando com a ponta dos pés."},
 {"k":"O que de fato acontece","sc":["Andar de verdade","é equilíbrio."],"e":"equilíbrio","sub":"E o equilíbrio se aprende caindo, levantando e sustentando o próprio peso.",
  "vo":"Andar de verdade é equilíbrio. E equilíbrio se aprende caindo, levantando, sustentando o próprio peso."},
 {"k":"E tem mais","sc":["Em excesso, está","associado a quedas."],"e":"quedas","sub":"E muda a forma como a criança apoia o quadril enquanto ele se forma.",
  "vo":"Em excesso, o andador está associado a quedas. E muda a forma como a criança apoia o quadril enquanto ele ainda se forma."},
 {"k":"O que ajuda","sc":["Chão livre.","Descalço. Tempo."],"e":"Tempo","sub":"O empurrador entra depois, quando ela já fica de pé sozinha.",
  "vo":"O que ajuda é simples: chão livre, descalço e tempo. O empurrador entra depois, quando ela já fica de pé sozinha."},
 {"k":"Passa adiante","sc":["Manda pra quem","ainda usa andador."],"e":None,"sub":"Um pai, uma mãe, uma avó. Salva pra lembrar.","cta":True,
  "vo":"Manda esse vídeo pra quem ainda usa andador. Um pai, uma mãe, uma avó."},
]

def synth(text,out_wav):
    # Piper CLI (texto via stdin). Normaliza cada cena a -16 LUFS.
    raw=out_wav+".raw.wav"
    subprocess.run(["piper","-m",VOICE,"-f",raw],input=text.encode("utf-8"),check=True,capture_output=True)
    subprocess.run(["ffmpeg","-y","-i",raw,"-af","loudnorm=I=-16:TP=-1.5:LRA=11,aformat=sample_rates=48000:channel_layouts=stereo",out_wav],check=True,capture_output=True)
    os.remove(raw)
def dur_of(wav):
    r=subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","default=nw=1:nk=1",wav],capture_output=True,text=True)
    return float(r.stdout.strip())

def main():
    shutil.rmtree(TMP,ignore_errors=True); os.makedirs(FR)
    # 1) sintetiza voz por cena e define duracoes
    voices=[]; durs=[]
    for i,s in enumerate(S):
        wv=f"{TMP}/v{i}.wav"; synth(s["vo"],wv); d=dur_of(wv)
        voices.append(wv); durs.append(round(LEAD+d+TAIL,3))
    bnd=[]; acc=0.0
    for i,d in enumerate(durs): bnd.append((acc,acc+d,i)); acc+=d
    total=acc; nframes=int(total*FPS)
    bases=[sbase(1,s["k"],s.get("motif")) for s in S]
    BIG=F(SB,96);SUBF=F(NR,40);CTAF=F(NB,52);T80=F(SB,80)
    # 2) frames
    for f in range(nframes):
        t=f/FPS; cur=bnd[-1]
        for b in bnd:
            if b[0]<=t<b[1]: cur=b; break
        t0,t1,idx=cur; tl=t-t0; s=S[idx]; img=bases[idx].copy(); d=ImageDraw.Draw(img)
        pw=int((t/total)*(W-2*M)); d.line([(M,H-128),(M+pw,H-128)],fill=GOLD,width=4)
        ln=s["sc"]; emph=s["e"]; tf=BIG
        if any(_m.textlength(x,font=tf)>W-2*M for x in ln): tf=T80
        ty=680
        for li,L in enumerate(ln):
            p=ease((tl-0.10-0.18*li)/0.5); dy=(1-p)*34
            if emph and emph in L:
                pre,_,post=L.partition(emph); x=M
                if pre: pt(img,x,ty+dy,pre,tf,CREAM,int(255*p)); x+=_m.textlength(pre,font=tf)
                pt(img,x,ty+dy,emph,tf,GOLD,int(255*p)); x+=_m.textlength(emph,font=tf)
                if post: pt(img,x,ty+dy,post,tf,CREAM,int(255*p))
            else: pt(img,M,ty+dy,L,tf,CREAM,int(255*p))
            ty+=int(tf.size*1.08)
        if s.get("sub"):
            sy=ty+44; ps=ease((tl-0.55)/0.5)
            for sl in wrap(s["sub"],SUBF,W-2*M): pt(img,M,sy,sl,SUBF,TXT_L,int(255*ps)); sy+=56
        if s.get("cta"):
            pc=ease((tl-0.9)/0.6); pt(img,M,H-300,"Compartilhar = enviar no direct",CTAF,GOLD,int(235*pc))
        img.save(f"{FR}/f{f:05d}.jpg","JPEG",quality=91)
    # 3) barramento de voz: cada cena no offset (inicio+LEAD)
    vparts=[]; filt=[]
    for i,wv in enumerate(voices):
        off=int((bnd[i][0]+LEAD)*1000)
        vparts+=["-i",wv]; filt.append(f"[{i}:a]adelay={off}|{off}[d{i}]")
    mixv="".join(f"[d{i}]" for i in range(len(voices)))+f"amix=inputs={len(voices)}:normalize=0[voz]"
    voz=f"{TMP}/voz.wav"
    subprocess.run(["ffmpeg","-y"]+vparts+["-filter_complex",";".join(filt)+";"+mixv,
        "-map","[voz]","-t",f"{total:.2f}","-ar","48000",voz],check=True,capture_output=True)
    # 4) cama musical -32 + high-pass
    tracks=sorted(glob.glob(AUD+"/*.mp4")+glob.glob(AUD+"/*.mp3"))
    music=tracks[1] if len(tracks)>1 else (tracks[0] if tracks else None)
    bed=f"{TMP}/bed.wav"
    if music:
        subprocess.run(["ffmpeg","-y","-i",music,"-vn","-map","0:a:0","-af",
            f"highpass=f=120,atrim=0:{total:.2f},loudnorm=I=-32:TP=-2:LRA=11,afade=t=in:d=0.6,afade=t=out:st={total-1.2:.2f}:d=1.2,aformat=sample_rates=48000:channel_layouts=stereo",
            "-t",f"{total:.2f}",bed],check=True,capture_output=True)
    # 5) mix voz + cama (normalize=0) + limiter
    mix=f"{TMP}/mix.m4a"
    if music:
        subprocess.run(["ffmpeg","-y","-i",voz,"-i",bed,"-filter_complex",
            "[0:a][1:a]amix=inputs=2:duration=first:normalize=0[mx];[mx]alimiter=limit=0.95[out]",
            "-map","[out]","-ar","48000","-c:a","aac","-b:a","192k",mix],check=True,capture_output=True)
    else:
        subprocess.run(["ffmpeg","-y","-i",voz,"-c:a","aac","-b:a","192k",mix],check=True,capture_output=True)
    # 6) encode final
    os.makedirs(os.path.dirname(OUT),exist_ok=True)
    subprocess.run(["ffmpeg","-y","-framerate",str(FPS),"-i",f"{FR}/f%05d.jpg","-i",mix,
        "-c:v","libx264","-pix_fmt","yuv420p","-profile:v","high","-r","30",
        "-c:a","aac","-b:a","192k","-shortest","-movflags","+faststart",OUT],check=True,capture_output=True)
    print("OK",OUT,round(total,1),"s |",nframes,"frames | trilha:",os.path.basename(music) if music else "mudo")
    print("duracoes por cena:",durs)

if __name__=="__main__":
    main()
