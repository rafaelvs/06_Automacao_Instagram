# -*- coding: utf-8 -*-
"""
Gerador de REELS (cinetipografia) para a biblioteca do Dr. Rafael Vargas.

- Vídeo 1080x1920 (9:16), H.264/AAC, faststart -> pronto p/ API (media_type=REELS).
- Mesma identidade dos posts (INK/CREAM/GOLD, logo RV, fundo de arcos).
- Otimizado p/ assistir SEM som: texto animado (kinetic typography), gancho nos 3s.
- Embute UMA trilha da pasta audio/ por Reel (rotação), em volume de apoio, c/ fades.
  Se não houver trilha, gera mudo (não trava).

Como usar:
1) Coloque os MP3 royalty-free (Meta Sound Collection) em audio/.
2) Preencha REELS abaixo com temas novos (reelNN).
3) python gerar_reels.py  -> renderiza em reels/ e ANEXA a reels.json.
4) GitHub Desktop -> commit -> Push. O robô publica em ordem, sem repetir.

Marca: preto #14141A, creme #F3E2C8, dourado #B08C4F.
Assinatura CFM: Dr. Rafael Vargas · Médico · CRM-SP 226103 · RQE 137901.
Conteúdo EDUCATIVO, sem prometer resultado (CFM).
"""
import os, json, glob, shutil, subprocess
from PIL import Image, ImageDraw, ImageFont

W,H=1080,1920; FPS=15
INK=(20,20,26); CREAM=(243,226,200); GOLD=(176,140,79); TXT_L=(206,198,184); MUT_L=(150,144,132)
FD="/usr/share/fonts/truetype/liberation/"
SB="LiberationSerif-Bold.ttf"; NR="LiberationSans-Regular.ttf"; NB="LiberationSans-Bold.ttf"
M=130
ROOT=os.path.dirname(os.path.abspath(__file__))
REELS_DIR=os.path.join(ROOT,"reels"); AUDIO_DIR=os.path.join(ROOT,"audio")
FRAMES="/tmp/_reelframes"
SIG="Dr. Rafael Vargas · Médico · CRM-SP 226103 · RQE 137901"
_FC={}
def F(n,s):
    k=(n,s)
    if k not in _FC: _FC[k]=ImageFont.truetype(FD+n,s)
    return _FC[k]
_m=ImageDraw.Draw(Image.new("RGB",(8,8)))
def ease(p): p=0.0 if p<0 else (1.0 if p>1 else p); return 1-(1-p)**3
def wrap(t,f,mw):
    out=[];cur=""
    for w in t.split():
        s=(cur+" "+w).strip()
        if _m.textlength(s,font=f)<=mw: cur=s
        else:
            if cur:out.append(cur)
            cur=w
    if cur:out.append(cur)
    return out
def trk(d,xy,text,font,fill,tr):
    x,y=xy
    for c in text: d.text((x,y),c,font=font,fill=fill); x+=d.textlength(c,font=font)+tr
def paste_text(base,x,y,text,font,color,alpha):
    if alpha<=0 or not text: return
    w=int(_m.textlength(text,font=font))+6; h=int(font.size*1.4)+6
    tile=Image.new("RGBA",(max(w,2),max(h,2)),(0,0,0,0)); ImageDraw.Draw(tile).text((0,0),text,font=font,fill=color+(255,))
    if alpha<255: tile.putalpha(tile.split()[3].point(lambda v: v*alpha//255))
    base.paste(tile,(int(x),int(y)),tile)
def static_base(scene):
    img=Image.new("RGB",(W,H),INK)
    ov=Image.new("RGBA",(W,H),(0,0,0,0)); da=ImageDraw.Draw(ov)
    for rad in [560,500,440,380,320]: da.arc([W//2-rad,H-120-rad,W//2+rad,H-120+rad],200,340,fill=(176,140,79,60),width=2)
    img=Image.alpha_composite(img.convert("RGBA"),ov).convert("RGB"); d=ImageDraw.Draw(img)
    d.text((M,150),"RV",font=F(SB,60),fill=CREAM); wf=d.textlength("RV",font=F(SB,60))
    d.line([(M+wf+24,162),(M+wf+24,212)],fill=GOLD,width=2)
    d.text((M+wf+44,160),"Dr. Rafael Vargas",font=F(NR,26),fill=CREAM); d.text((M+wf+44,194),"Ortopedia · São Paulo",font=F(NR,22),fill=GOLD)
    ky=620; trk(d,(M,ky),scene["kicker"].upper(),F(NB,30),GOLD,6); d.line([(M,ky+50),(M+70,ky+50)],fill=GOLD,width=3)
    d.text((M,H-150),"@rafaelvargasmd",font=F(NR,28),fill=MUT_L); d.line([(M,H-92),(W-M,H-92)],fill=(80,76,70),width=3)
    return img
def overlay(img,scene,tl):
    ky=620
    if scene.get("big") or scene.get("cta"):
        tf=scene["_tf"]; ty=ky+110
        for i,ln in enumerate(scene["_lines"]):
            p=ease((tl-0.15*i)/0.5); paste_text(img,M,ty+(1-p)*28,ln,tf,CREAM,int(255*p)); ty+=int(tf.size*1.12)
        if scene.get("cta"):
            p=ease((tl-0.7)/0.5)
            paste_text(img,M,ty+40,"Agende pelo WhatsApp",F(NB,46),GOLD,int(255*p)); paste_text(img,M,ty+104,"link na bio",F(NR,40),TXT_L,int(255*p))
    else:
        ty=ky+118; lf=F(NB,58)
        for i,ln in enumerate(scene["lines"]):
            p=ease((tl-0.4*i)/0.5); paste_text(img,M,ty+(1-p)*30,ln,lf,CREAM,int(255*p)); ty+=92

def build_scenes(spec):
    """spec: {kicker_hook, hook, points:[{kicker, lines}], cta_title}"""
    sc=[{"dur":3.0,"kicker":spec["kicker_hook"],"title":spec["hook"],"big":True}]
    for p in spec["points"]: sc.append({"dur":3.0,"kicker":p["kicker"],"lines":p["lines"]})
    sc.append({"dur":2.8,"kicker":"Converse comigo","title":spec["cta_title"],"cta":True})
    for s in sc:
        if s.get("big") or s.get("cta"):
            tf=F(SB,92); ls=wrap(s["title"],tf,W-2*M)
            if len(ls)>3: tf=F(SB,76); ls=wrap(s["title"],tf,W-2*M)
            s["_tf"]=tf; s["_lines"]=ls
    return sc

def render_reel(scenes, out_mp4, music_path=None):
    if os.path.isdir(FRAMES): shutil.rmtree(FRAMES, ignore_errors=True)
    os.makedirs(FRAMES, exist_ok=True)
    bounds=[]; acc=0.0
    for s in scenes: bounds.append((acc,acc+s["dur"],s,static_base(s))); acc+=s["dur"]
    total=acc; nframes=int(total*FPS)
    for f in range(nframes):
        t=f/FPS; cur=bounds[-1]
        for b in bounds:
            if b[0]<=t<b[1]: cur=b; break
        s0,_,scene,sb=cur; img=sb.copy(); overlay(img,scene,t-s0)
        pw=int((t/total)*(W-2*M)); ImageDraw.Draw(img).line([(M,H-92),(M+pw,H-92)],fill=GOLD,width=4)
        img.save(os.path.join(FRAMES,f"f{f:05d}.jpg"),"JPEG",quality=90)
    # trilha (volume de apoio) ou silencio
    if music_path and os.path.exists(music_path):
        bed="/tmp/_bed.wav"
        subprocess.run(["ffmpeg","-y","-i",music_path,"-vn","-map","0:a:0","-af",
            f"atrim=0:{total:.2f},loudnorm=I=-20:TP=-2:LRA=11,afade=t=in:d=0.5,afade=t=out:st={total-1.2:.2f}:d=1.2,aformat=sample_rates=48000:channel_layouts=stereo",
            "-t",f"{total:.2f}",bed],check=True,capture_output=True)
        ain=["-i",bed]
    else:
        ain=["-f","lavfi","-i","anullsrc=channel_layout=stereo:sample_rate=48000"]
    cmd=["ffmpeg","-y","-framerate",str(FPS),"-i",os.path.join(FRAMES,"f%05d.jpg")]+ain+[
        "-c:v","libx264","-pix_fmt","yuv420p","-profile:v","high","-r","30",
        "-c:a","aac","-b:a","160k","-shortest","-movflags","+faststart",out_mp4]
    subprocess.run(cmd,check=True,capture_output=True)
    return round(total,1)

def cap(corpo,tags): return corpo+"\n\n""📤 Manda para alguém que precisa ver. 📌 Salve para consultar depois.\n""💬 Dúvida? Comenta ou chama no direct. 📲 Agende pela WhatsApp no link da bio."+"\n\n"+SIG+"\n\n"+tags

# ----------------- BIBLIOTECA DE REELS (preencha com temas novos) -----------------
REELS=[
 {"id":"reel01",
  "kicker_hook":"Ortopedia Pediátrica","hook":"Dor de crescimento ou sinal de alerta?",
  "points":[
    {"kicker":"Costuma ser comum","lines":["Dói nas duas pernas","No fim do dia ou à noite","Melhora pela manhã"]},
    {"kicker":"Hora de avaliar","lines":["Dói só de um lado","Vem com inchaço ou febre","Faz a criança mancar"]},
  ],
  "cta_title":"Na dúvida, avalie.",
  "caption":cap("Dor de crescimento é comum e costuma ser nas duas pernas, à noite, melhorando pela manhã. Dor de um lado só, com inchaço, febre ou que faz mancar merece avaliação. Na dúvida, observar de perto é o melhor caminho.","#dordecrescimento #ortopediapediatrica #ortopediainfantil #saudedacrianca #ortopediasaopaulo")},
 {"id":"reel02",
  "kicker_hook":"Ortopedia Pediátrica","hook":"Pé torto congênito tem tratamento.",
  "points":[
    {"kicker":"O que é","lines":["O pé já nasce virado","Para baixo e para dentro","É comum e tem solução"]},
    {"kicker":"Como se trata","lines":["Gessos que corrigem aos poucos","Método de Ponseti","Começar cedo é mais suave"]},
  ],
  "cta_title":"Avalie o pé do seu bebê.",
  "caption":cap("O pé torto (equinovaro) já nasce virado para baixo e para dentro — é comum e não tem relação com algo feito na gestação. O tratamento costuma começar nas primeiras semanas, com gessos que corrigem aos poucos (Ponseti) e depois uma órtese. Começar cedo aproveita a flexibilidade do bebê.","#petortocongenito #ponseti #ortopediapediatrica #ortopediainfantil #ortopediasaopaulo")},
 {"id":"reel03",
  "kicker_hook":"Alongamento Ósseo","hook":"O corpo cria osso novo. Entenda.",
  "points":[
    {"kicker":"Ponto de partida","lines":["Após um corte planejado","O osso se regenera","No espaço que vai abrindo"]},
    {"kicker":"As fases","lines":["Espera (latência)","Distração, milímetro a milímetro","Consolidação do osso novo"]},
  ],
  "cta_title":"Entenda o seu caso.",
  "caption":cap("Parece incrível, mas o próprio corpo regenera osso. Depois de um corte ósseo planejado, o tratamento segue em fases: latência, distração (afastamento gradual, milímetro a milímetro) e consolidação. Por isso é um tratamento de etapas, com acompanhamento próximo.","#alongamentoosseo #reconstrucaoossea #osteogenesedistracao #ortopediasaopaulo #ortopedia")},
]

def run():
    os.makedirs(REELS_DIR, exist_ok=True)
    reels_json=os.path.join(ROOT,"reels.json")
    lib=json.load(open(reels_json,encoding="utf-8")) if os.path.exists(reels_json) else []
    ids={r["id"] for r in lib}
    tracks=sorted(glob.glob(os.path.join(AUDIO_DIR,"*.mp3"))+glob.glob(os.path.join(AUDIO_DIR,"*.m4a"))+glob.glob(os.path.join(AUDIO_DIR,"*.wav"))+glob.glob(os.path.join(AUDIO_DIR,"*.mp4")))
    print("trilhas encontradas:",[os.path.basename(t) for t in tracks] or "(nenhuma -> mudo)")
    made=0
    for i,spec in enumerate(REELS):
        rid=spec["id"]
        if rid in ids: print("pulando (existe):",rid); continue
        scenes=build_scenes(spec)
        out=os.path.join(REELS_DIR,rid+".mp4")
        music=tracks[i % len(tracks)] if tracks else None
        dur=render_reel(scenes,out,music)
        lib.append({"id":rid,"video":"reels/"+rid+".mp4","caption":spec["caption"],
                    "music":os.path.basename(music) if music else None,"dur":dur})
        made+=1; print("ok",rid,dur,"s","| trilha:",os.path.basename(music) if music else "mudo")
    json.dump(lib,open(reels_json,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
    print("Biblioteca -> reels:",len(lib),"| novos:",made)

if __name__=="__main__":
    run()
