import os, glob, time, threading, subprocess, datetime
os.environ["TORCH_FORCE_NO_WEIGHTS_ONLY_LOAD"]="1"; os.environ["CUDA_VISIBLE_DEVICES"]="0"
print(">> instalando coqui-tts (1-2 min)...", flush=True)
os.system("pip -q install -U coqui-tts huggingface_hub >/dev/null 2>&1")
from huggingface_hub import login, snapshot_download, HfApi
from kaggle_secrets import UserSecretsClient
TOK=UserSecretsClient().get_secret("HF_TOKEN"); login(TOK)
DS="rafaelvargassilva/tts-ptbr-dados"; CK="rafaelvargassilva/voz-ptbr-ckpt"
api=HfApi(); api.create_repo(CK, private=True, exist_ok=True)
print(">> baixando dataset...", flush=True); snapshot_download(DS, repo_type="dataset", local_dir="data")
os.makedirs("run", exist_ok=True); CONT=""
try:
    snapshot_download(CK, repo_type="model", local_dir="run")
    subs=[d for d in glob.glob("run/voz_ptbr*") if glob.glob(d+"/*.pth")]
    if subs: CONT=sorted(subs)[-1]; print(">> RETOMANDO de", CONT, flush=True)
except Exception as e: print(">> 1a sessao (sem checkpoint):", e, flush=True)
os.environ["CONT_PATH"]=CONT
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
  print_step=25, plot_step=200, save_step=1000, save_n_checkpoints=2, save_best_after=1000,
  mixed_precision=True, output_path=OUT, cudnn_benchmark=True, datasets=[ds],
  test_sentences=["O andador nao ensina o bebe a andar.","Equilibrio se aprende firmando o proprio peso."])
ap=AudioProcessor.init_from_config(cfg)
tok,cfg=TTSTokenizer.init_from_config(cfg)
tr,ev=load_tts_samples(ds, eval_split=True, eval_split_size=0.01)
print("AMOSTRAS treino:", len(tr), "| eval:", len(ev), flush=True)
model=Vits(cfg, ap, tok, speaker_manager=None)
cont=os.environ.get("CONT_PATH","")
args=TrainerArgs(continue_path=cont) if cont else TrainerArgs()
Trainer(args, cfg, output_path=OUT, model=model, train_samples=tr, eval_samples=ev).fit()
'''
open("train_run.py","w").write(RECIPE)
T0=time.time(); STOP=[False]; CYC=[0]
def monitor():
    while not STOP[0]:
        time.sleep(180); CYC[0]+=1
        try:
            cks=glob.glob("run/**/*.pth", recursive=True); step=0
            for c in cks:
                d="".join(ch for ch in os.path.basename(c) if ch.isdigit())
                if d: step=max(step, int(d))
            tail=os.popen("tail -n 80 train.log 2>/dev/null | grep -E 'GLOBAL_STEP|avg_|loss' | tail -n 5").read()
            el=int(time.time()-T0)
            msg=("PROGRESSO voz pt-BR | passo~%d | %d min rodando | %s UTC\n--- ultimas metricas ---\n%s"
                 %(step, el//60, datetime.datetime.utcnow().strftime("%H:%M"), tail))
            open("progress.txt","w").write(msg)
            api.upload_file(path_or_fileobj="progress.txt", path_in_repo="progress.txt", repo_id=CK, repo_type="model")
            if CYC[0]%6==0 and cks:
                for c in sorted(cks)[-2:]:
                    try: api.upload_file(path_or_fileobj=c, path_in_repo=os.path.basename(c), repo_id=CK, repo_type="model")
                    except Exception: pass
            print("[MONITOR] passo~%d | %dmin"%(step, el//60), flush=True)
        except Exception as e: print("[MONITOR] erro:", e, flush=True)
threading.Thread(target=monitor, daemon=True).start()
print(">> INICIANDO TREINO (as primeiras metricas aparecem em ~2-3 min)", flush=True)
p=subprocess.Popen(["python","train_run.py"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=1, universal_newlines=True)
with open("train.log","w") as lg:
    for line in p.stdout:
        print(line, end="", flush=True); lg.write(line); lg.flush()
STOP[0]=True; print(">> treino encerrou (sessao acabou ou erro). Checkpoint mais recente esta no HF.", flush=True)
