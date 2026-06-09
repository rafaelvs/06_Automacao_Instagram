# -*- coding: utf-8 -*-
"""
Renderiza os episódios narrativos "Pé no Chão" (30fps, SEM voz — só música) e os PREPENDA
no reels.json, pra o robô publicar o formato novo a partir do próximo reel.
Roda no GitHub Actions (workflow render-reel-narrativo). Base 'sem voz' p/ comparar com a falada depois.
"""
import os, glob, json, subprocess
import render_reel as R
from episodios_pe_no_chao import EPISODES, SIG

ROOT=os.path.dirname(os.path.abspath(__file__)); AUD=os.path.join(ROOT,"audio"); REELS=os.path.join(ROOT,"reels")
DUR_HOOK=3.4; DUR_SCENE=3.8; DUR_CTA=3.6

def render_ep(epi):
    durs=[]
    for i,s in enumerate(epi["scenes"]):
        durs.append(DUR_CTA if s.get("cta") else (DUR_HOOK if i==0 else DUR_SCENE))
    FR="/tmp/_pncfr"; total,nf=R.render_frames(epi,durs,FR)
    tracks=sorted(glob.glob(AUD+"/*.mp4")+glob.glob(AUD+"/*.mp3"))
    music=tracks[epi["ep"]%len(tracks)] if tracks else None
    if music:
        subprocess.run(["ffmpeg","-y","-i",music,"-vn","-map","0:a:0","-af",
          f"highpass=f=120,atrim=0:{total:.2f},loudnorm=I=-16:TP=-1.5,afade=t=in:d=0.5,"
          f"afade=t=out:st={total-1:.2f}:d=1,aformat=sample_rates=48000:channel_layouts=stereo",
          "-t",f"{total:.2f}","/tmp/_pncbed.wav"],check=True,capture_output=True)
        ain=["-i","/tmp/_pncbed.wav"]
    else:
        ain=["-f","lavfi","-i","anullsrc=channel_layout=stereo:sample_rate=48000"]
    os.makedirs(REELS,exist_ok=True)
    out=os.path.join(REELS,f"pnc_{epi['id']}.mp4")
    R.encode(FR,ain,out)
    return "reels/"+os.path.basename(out), round(total,1), os.path.basename(music) if music else None

def main():
    rj=os.path.join(ROOT,"reels.json"); reels=json.load(open(rj,encoding="utf-8"))
    existing={r["id"] for r in reels}
    novos=[]
    for epi in EPISODES:
        rid="pnc_"+epi["id"]
        if rid in existing: print("pulando (existe):",rid); continue
        video,dur,music=render_ep(epi)
        novos.append({"id":rid,"video":video,"caption":epi["caption"],"music":music,"dur":dur,"serie":"Pé no Chão"})
        print("ok",rid,dur,"s |",music)
    # PREPENDA os novos (publicam antes dos reels antigos)
    reels=novos+reels
    json.dump(reels,open(rj,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
    print("reels.json:",len(reels),"| novos narrativos:",len(novos))

if __name__=="__main__": main()
