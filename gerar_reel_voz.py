# -*- coding: utf-8 -*-
"""
Reel-episódio FALADO "Pé no Chão" — roda no GitHub Actions (tem rede). Craft 30fps (render_reel) +
locução por cena (durações seguem a voz) + CADEIA DE ÁUDIO DE ESTÚDIO + mix voz/música + loudnorm -14.

VOZ PLUGÁVEL: por padrão usa edge-tts (Antonio). Alterna p/ Piper com VOZ_ENGINE=piper.

Saída: reels/_preview_<ep_id>.mp4 (prefixo _, fora do reels.json -> NÃO publica sozinho).
Uso: python gerar_reel_voz.py <ep_id>
"""
import os, glob, subprocess, sys
import render_reel as R
from episodios_pe_no_chao import get

ROOT=os.path.dirname(os.path.abspath(__file__)); AUD=os.path.join(ROOT,"audio")
# VOZ DO CANAL: motor padrao = edge-tts (vozes neurais Microsoft, gratis, sem chave de API).
# Alterna p/ Piper com VOZ_ENGINE=piper. Botoes de edicao: EDGE_RATE (ritmo) e EDGE_PITCH (tom).
ENGINE=os.environ.get("VOZ_ENGINE","edge")
EDGE_VOICE=os.environ.get("EDGE_VOICE","pt-BR-AntonioNeural")
EDGE_RATE=os.environ.get("EDGE_RATE","+0%")
EDGE_PITCH=os.environ.get("EDGE_PITCH","+0Hz")
VOICE=os.environ.get("PIPER_VOICE", os.path.join(ROOT,"voices","pt_BR-faber-medium.onnx"))
# folgas entre fala e cena (encurtadas p/ a narracao fluir mais natural, menos "robotica"). Tunaveis por env.
LEAD=float(os.environ.get("VOZ_LEAD","0.18")); TAIL=float(os.environ.get("VOZ_TAIL","0.45"))
# RETENCAO-3s (v7): a voz da CENA 0 entra quase no frame 0 (0,05s) — sem "respiro" inicial. O watch
# medio de 2,3s (pulso v7) mostrou que o 1o segundo decide; o lead normal segue nas demais cenas.
LEAD0=float(os.environ.get("VOZ_LEAD0","0.05"))
# apara silencio das pontas de cada trecho de voz (remove os "delays" sinteticos)
TRIM_SIL=("silenceremove=start_periods=1:start_threshold=-50dB:start_silence=0.03,areverse,"
          "silenceremove=start_periods=1:start_threshold=-50dB:start_silence=0.03,areverse,")

VOICE_CHAIN=("highpass=f=85,"
 "equalizer=f=300:t=q:w=1.2:g=-3,equalizer=f=180:t=q:w=1.5:g=2,"
 "equalizer=f=4000:t=q:w=1.6:g=2,equalizer=f=6500:t=q:w=2.0:g=-2,"
 "deesser=i=0.5:m=0.5:f=0.5,"
 "acompressor=threshold=-18dB:ratio=3:attack=15:release=120:makeup=4,"
 "asoftclip=type=tanh,alimiter=limit=-1dB,"
 "loudnorm=I=-16:TP=-1.5:LRA=11,aformat=sample_rates=48000:channel_layouts=stereo")

def synth(text,out_wav):
    raw=out_wav+(".mp3" if ENGINE=="edge" else ".raw.wav")
    if ENGINE=="edge":
        subprocess.run(["edge-tts","--voice",EDGE_VOICE,f"--rate={EDGE_RATE}",f"--pitch={EDGE_PITCH}",
                        "--text",text,"--write-media",raw],check=True,capture_output=True)
    else:
        subprocess.run(["piper","-m",VOICE,"-f",raw],input=text.encode("utf-8"),check=True,capture_output=True)
    subprocess.run(["ffmpeg","-y","-i",raw,"-af",TRIM_SIL+VOICE_CHAIN,out_wav],check=True,capture_output=True)
    os.remove(raw)
def dur_of(w):
    return float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","default=nw=1:nk=1",w],capture_output=True,text=True).stdout.strip())

def main():
    ep_id=sys.argv[1] if len(sys.argv)>1 else "andador"
    epi=get(ep_id); S=epi["scenes"]; TMP="/tmp/_voz"; os.makedirs(TMP,exist_ok=True)
    voices=[]; durs=[]; leads=[]
    for i,s in enumerate(S):
        wv=f"{TMP}/v{i}.wav"; synth(s["vo"],wv); ld=LEAD0 if i==0 else LEAD
        durs.append(round(ld+dur_of(wv)+TAIL,3)); voices.append(wv); leads.append(ld)
    FR="/tmp/_vfr"; total,nf=R.render_frames(epi,durs,FR)
    acc=0.0; offs=[]
    for i,d in enumerate(durs): offs.append(acc+leads[i]); acc+=d
    vin=[]; filt=[]
    for i,wv in enumerate(voices):
        o=int(offs[i]*1000); vin+=["-i",wv]; filt.append(f"[{i}:a]adelay={o}|{o}[d{i}]")
    mixv="".join(f"[d{i}]" for i in range(len(voices)))+f"amix=inputs={len(voices)}:normalize=0[voz]"
    subprocess.run(["ffmpeg","-y"]+vin+["-filter_complex",";".join(filt)+";"+mixv,"-map","[voz]","-t",f"{total:.2f}","-ar","48000",f"{TMP}/voz.wav"],check=True,capture_output=True)
    tracks=sorted(glob.glob(AUD+"/*.mp4")+glob.glob(AUD+"/*.mp3")); music=tracks[epi["ep"]%len(tracks)] if tracks else None
    if music:
        subprocess.run(["ffmpeg","-y","-i",music,"-vn","-map","0:a:0","-af",
            f"highpass=f=120,atrim=0:{total:.2f},loudnorm=I=-40:TP=-2,afade=t=in:d=0.6,afade=t=out:st={total-1.2:.2f}:d=1.2,aformat=sample_rates=48000:channel_layouts=stereo",
            "-t",f"{total:.2f}",f"{TMP}/bed.wav"],check=True,capture_output=True)
        subprocess.run(["ffmpeg","-y","-i",f"{TMP}/voz.wav","-i",f"{TMP}/bed.wav","-filter_complex",
            "[0:a][1:a]amix=inputs=2:duration=first:normalize=0[mx];[mx]loudnorm=I=-14:TP=-1,alimiter=limit=-1dB[o]",
            "-map","[o]","-ar","48000","-c:a","aac","-b:a","192k",f"{TMP}/mix.m4a"],check=True,capture_output=True)
    else:
        subprocess.run(["ffmpeg","-y","-i",f"{TMP}/voz.wav","-af","loudnorm=I=-14:TP=-1","-c:a","aac","-b:a","192k",f"{TMP}/mix.m4a"],check=True,capture_output=True)
    out=os.path.join(ROOT,"reels",f"_preview_{ep_id}.mp4"); os.makedirs(os.path.dirname(out),exist_ok=True)
    R.encode(FR,["-i",f"{TMP}/mix.m4a"],out)
    print("OK",out,round(total,1),"s",nf,"frames | durs",durs)

if __name__=="__main__": main()
