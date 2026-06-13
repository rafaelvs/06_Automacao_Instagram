import os, glob, time, threading, subprocess, datetime, traceback
# --- estabilidade: fp16 do kl_loss derrubava no passo 0; sem AMP some o NaN ---
os.environ["TORCH_FORCE_NO_WEIGHTS_ONLY_LOAD"]="1"; os.environ["CUDA_VISIBLE_DEVICES"]="0"
TARGET_STEP=int(os.environ.get("TARGET_STEP","120000"))   # ao atingir, marca DONE e para de religar
print(">> instalando coqui-tts (1-2 min)...", flush=True)
os.system("pip -q install -U coqui-tts huggingface_hub >/dev/null 2>&1")
from huggingface_hub import login, snapshot_download, hf_hub_download, list_repo_files, HfApi
try:
    from kaggle_secrets import UserSecretsClient
    TOK=UserSecretsClient().get_secret("HF_TOKEN")
except Exception:
    TOK=os.environ.get("HF_TOKEN","")
login(TOK)
DS="rafaelvargassilva/tts-ptbr-dados"; CK="rafaelvargassilva/voz-ptbr-ckpt"
api=HfApi(); api.create_repo(CK, private=True, exist_ok=True)

def hb(status, step, extra=""):
    """heartbeat legivel por humano + parseavel pelo vigia (STATUS=/STEP=/TS=)."""
    ts=int(time.time())
    msg=("PROGRESSO voz pt-BR | %s | passo~%d | %s UTC\n"
         "STATUS=%s\nSTEP=%d\nTS=%d\nTARGET=%d\n--- ultimas metricas ---\n%s"
         %(status, step, datetime.datetime.utcnow().strftime("%H:%M"), status, step, ts, TARGET_STEP, extra))
    try:
        open("progress.txt","w").write(msg)
        api.upload_file(path_or_fileobj="progress.txt", path_in_repo="progress.txt", repo_id=CK, repo_type="model")
    except Exception as e: print("[HB] falhou upload:", e, flush=True)

def newest_ckpt_local():
    cks=glob.glob("run/**/*.pth", recursive=True)
    best=None; bstep=-1
    for c in cks:
        d="".join(ch for ch in os.path.basename(c) if ch.isdigit())
        s=int(d) if d else 0
        if s>=bstep: bstep=s; best=c
    return best, max(bstep,0)

# ---------- baixar dataset ----------
print(">> baixando dataset...", flush=True)
snapshot_download(DS, repo_type="dataset", local_dir="data")
os.makedirs("run", exist_ok=True)

# ---------- AUTO-RESUME: pega o checkpoint .pth mais recente no HF ----------
RESTORE=""; START_STEP=0
try:
    files=[f for f in list_repo_files(CK, repo_type="model") if f.endswith(".pth")]
    if files:
        def stepof(f):
            d="".join(ch for ch in os.path.basename(f) if ch.isdigit()); return int(d) if d else 0
        latest=sorted(files, key=stepof)[-1]; START_STEP=stepof(latest)
        local=hf_hub_download(CK, latest, repo_type="model", local_dir="ckpt_in")
        # config.json ajuda mas restore_path so precisa do .pth
        try: hf_hub_download(CK, "config.json", repo_type="model", local_dir="ckpt_in")
        except Exception: pass
        RESTORE=local; print(">> RETOMANDO de", latest, "(passo", START_STEP, ")", flush=True)
    else:
        print(">> 1a sessao: sem checkpoint no HF, treino do zero", flush=True)
except Exception as e:
    print(">> nao deu p/ checar checkpoints (treino do zero):", e, flush=True)

# se ja passamos do alvo, encerra sem religar
if START_STEP>=TARGET_STEP:
    hb("DONE", START_STEP, "alvo de %d passos atingido — nada a fazer."%TARGET_STEP)
    print(">> DONE: alvo atingido. Encerrando.", flush=True); raise SystemExit(0)

os.environ["RESTORE_PATH"]=RESTORE
RECIPE=r'''
import os
os.environ["CUDA_VISIBLE_DEVICES"]="0"
from trainer import Trainer, TrainerArgs
from TTS.tts.configs.shared_configs import BaseDatasetConfig, CharactersConfig
from TTS.tts.configs.vits_config import VitsConfig
from TTS.tts.datasets import load_tts_samples
from TTS.tts.models.vits import Vits, VitsAudioConfig
from TTS.tts.utils.text.tokenizer import TTSTokenizer
from TTS.utils.audio import AudioProcessor
OUT="run"
ds=BaseDatasetConfig(formatter="ljspeech", meta_file_train="metadata.csv", path="data")
audio=VitsAudioConfig(sample_rate=22050)
chars=CharactersConfig(characters_class="TTS.tts.models.vits.VitsCharacters",
  pad="<PAD>", eos="<EOS>", bos="<BOS>", blank="<BLNK>",
  characters="abcdefghijklmnopqrstuvwxyzaaaaeeiooouucABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789áàâãéêíóôõúüçÁÀÂÃÉÊÍÓÔÕÚÜÇ",
  punctuations="!'(),-.:;? ")
cfg=VitsConfig(audio=audio, run_name="voz_ptbr", batch_size=16, eval_batch_size=8,
  num_loader_workers=2, num_eval_loader_workers=2, run_eval=True, test_delay_epochs=-1,
  epochs=10000, use_phonemes=False, characters=chars, text_cleaner="multilingual_cleaners",
  print_step=25, plot_step=200, save_step=500, save_n_checkpoints=3, save_best_after=500,
  mixed_precision=False,                # <- FIX: sem AMP, kl_loss estavel
  grad_clip=[5.0, 5.0],                 # <- FIX: clip evita explosao de gradiente
  lr_gen=2e-4, lr_disc=2e-4, lr_scheduler_gen="ExponentialLR", lr_scheduler_disc="ExponentialLR",
  output_path=OUT, cudnn_benchmark=True, datasets=[ds],
  test_sentences=["O andador nao ensina o bebe a andar.","Equilibrio se aprende firmando o proprio peso."])
ap=AudioProcessor.init_from_config(cfg)
tok,cfg=TTSTokenizer.init_from_config(cfg)
tr,ev=load_tts_samples(ds, eval_split=True, eval_split_size=0.01)
print("AMOSTRAS treino:", len(tr), "| eval:", len(ev), flush=True)
model=Vits(cfg, ap, tok, speaker_manager=None)
rp=os.environ.get("RESTORE_PATH","")
args=TrainerArgs(restore_path=rp) if rp else TrainerArgs()
Trainer(args, cfg, output_path=OUT, model=model, train_samples=tr, eval_samples=ev).fit()
'''
open("train_run.py","w").write(RECIPE)

# ---------- monitor/heartbeat ----------
T0=time.time(); STOP=[False]; LAST=[START_STEP]
def live_step():
    """passo ao vivo: do log (GLOBAL_STEP) ou do checkpoint mais novo."""
    s=0
    try:
        t=os.popen("grep -aoE 'GLOBAL_STEP:[0-9]+' train.log 2>/dev/null | tail -n1").read()
        if t: s=int(t.split(":")[1])
    except Exception: pass
    _, cs=newest_ckpt_local(); return max(s, cs, START_STEP)
def monitor():
    cyc=0
    while not STOP[0]:
        time.sleep(180); cyc+=1
        try:
            step=live_step(); LAST[0]=step
            tail=os.popen("tail -n 80 train.log 2>/dev/null | grep -aE 'GLOBAL_STEP|avg_|loss|EPOCH' | tail -n 6").read()
            hb("RUNNING", step, tail)
            best,_=newest_ckpt_local()
            if best:  # sobe o checkpoint mais novo (e config) toda vez que existe
                for f in [best, os.path.join(os.path.dirname(best),"config.json")]:
                    if os.path.exists(f):
                        try: api.upload_file(path_or_fileobj=f, path_in_repo=os.path.basename(f), repo_id=CK, repo_type="model")
                        except Exception: pass
            print("[MONITOR] passo~%d | %dmin"%(step, int(time.time()-T0)//60), flush=True)
        except Exception as e: print("[MONITOR] erro:", e, flush=True)
threading.Thread(target=monitor, daemon=True).start()

# ---------- roda o treino com upload garantido ao sair ----------
hb("RUNNING", START_STEP, "iniciando...")
print(">> INICIANDO TREINO (primeiras metricas em ~2-3 min)", flush=True)
rc=1
try:
    p=subprocess.Popen(["python","train_run.py"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=1, universal_newlines=True)
    with open("train.log","w") as lg:
        for line in p.stdout:
            print(line, end="", flush=True); lg.write(line); lg.flush()
    rc=p.wait()
except Exception:
    open("train.log","a").write("\n[ORQUESTRADOR] excecao:\n"+traceback.format_exc())
finally:
    STOP[0]=True; time.sleep(1)
    best,bstep=newest_ckpt_local(); step=max(bstep, LAST[0])
    # upload final garantido: checkpoint + config + train.log
    for f in [best, (os.path.join(os.path.dirname(best),"config.json") if best else None), "train.log"]:
        if f and os.path.exists(f):
            try: api.upload_file(path_or_fileobj=f, path_in_repo=os.path.basename(f), repo_id=CK, repo_type="model")
            except Exception as e: print("[FINAL] upload falhou:", f, e, flush=True)
    tail=os.popen("tail -n 40 train.log 2>/dev/null").read()
    if rc==0 and step>=TARGET_STEP:
        hb("DONE", step, "alvo atingido.\n"+tail)
    elif rc==0:
        hb("PAUSED", step, "sessao terminou ok (tempo/cota). Retoma na proxima.\n"+tail)
    else:
        hb("FAILED", step, "rc=%d — TREINO QUEBROU. Ver tail:\n%s"%(rc, tail))
    print(">> encerrado. rc=%d passo~%d (status no progress.txt do HF)"%(rc, step), flush=True)
