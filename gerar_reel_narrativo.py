# -*- coding: utf-8 -*-
"""
PREVIEW de reel-episódio "Pé no Chão" (craft 30fps, SEM voz — só música de apoio).
Para conferir craft/ritmo/layout localmente. A versão FALADA é gerar_reel_voz.py (roda no CI).
Uso: python gerar_reel_narrativo.py <ep_id> [saida.mp4]    (ex.: andador, pe_chato, dor_crescimento...)
"""
import os, glob, subprocess, sys
import render_reel as R
from episodios_pe_no_chao import get

ROOT=os.path.dirname(os.path.abspath(__file__)); AUD=os.path.join(ROOT,"audio")
DUR_HOOK=3.4; DUR_SCENE=3.8; DUR_CTA=3.6

def main():
    ep_id=sys.argv[1] if len(sys.argv)>1 else "andador"
    out=sys.argv[2] if len(sys.argv)>2 else f"/tmp/preview_{ep_id}.mp4"
    epi=get(ep_id); n=len(epi["scenes"])
    durs=[]
    for i,s in enumerate(epi["scenes"]):
        durs.append(DUR_CTA if s.get("cta") else (DUR_HOOK if i==0 else DUR_SCENE))
    FR="/tmp/_narr"; total,nf=R.render_frames(epi,durs,FR)
    tracks=sorted(glob.glob(AUD+"/*.mp4")+glob.glob(AUD+"/*.mp3"))
    music=tracks[epi["ep"]%len(tracks)] if tracks else None
    if music:
        subprocess.run(["ffmpeg","-y","-i",music,"-vn","-map","0:a:0","-af",
            f"highpass=f=120,atrim=0:{total:.2f},loudnorm=I=-28:TP=-2,afade=t=in:d=0.5,"
            f"afade=t=out:st={total-1:.2f}:d=1,aformat=sample_rates=48000:channel_layouts=stereo",
            "-t",f"{total:.2f}","/tmp/_nbed.wav"],check=True,capture_output=True)
        ain=["-i","/tmp/_nbed.wav"]
    else:
        ain=["-f","lavfi","-i","anullsrc=channel_layout=stereo:sample_rate=48000"]
    R.encode(FR,ain,out)
    print("OK",out,round(total,1),"s",nf,"frames |",os.path.basename(music) if music else "mudo")

if __name__=="__main__": main()
