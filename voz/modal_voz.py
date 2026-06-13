# -*- coding: utf-8 -*-
"""
Treino AUTO-CURÁVEL da voz pt-BR no Modal (fine-tune VITS).

Por que Modal: cron nativo + retries + Volume persistente => "dispara e esquece".
- Fine-tune a partir de tts_models/pt/cv/vits (acaba em ~5-10h GPU em vez de semanas).
- Checkpoints no Modal Volume (durável entre runs) -> retoma com continue_path (correto).
- Se a sessão acabar/cair, o retry do Modal e o modal.Cron de segurança religam sozinhos,
  retomando do checkpoint. Ao atingir o alvo, grava DONE e tudo vira no-op.
- Heartbeat (progress.txt) espelhado no Hugging Face para acompanhar de fora.
- Lease anti-concorrência: nunca dois treinos escrevendo no mesmo Volume.

Bootstrap (uma vez, ver SETUP_MODAL.md):
  pip install modal && modal setup
  modal secret create huggingface HF_TOKEN=<seu_token_hf>
  modal deploy modal_voz.py      # liga o cron de segurança
  modal run modal_voz.py         # dispara o 1o treino agora
"""
import modal, os, time, glob, datetime, traceback

app = modal.App("voz-ptbr")

# imagem com coqui-tts + libs de áudio
image = (
    modal.Image.debian_slim(python_version="3.11")
    .apt_install("ffmpeg", "libsndfile1", "git")
    .pip_install("coqui-tts", "huggingface_hub", "soundfile", "librosa")
    .env({"TORCH_FORCE_NO_WEIGHTS_ONLY_LOAD": "1", "COQUI_TOS_AGREED": "1"})
)

vol = modal.Volume.from_name("voz-ckpt", create_if_missing=True)
CKDIR = "/ckpt"                         # raiz persistente (Volume)
RUNROOT = CKDIR + "/run"               # pasta da run do Coqui (config + checkpoints)
DATADIR = CKDIR + "/data"              # dataset cacheado
DONE = CKDIR + "/DONE"
LEASE = CKDIR + "/RUNNING"             # lease anti-concorrência (timestamp)
PROG = CKDIR + "/progress.txt"

HF_DS = "rafaelvargassilva/tts-ptbr-dados"
HF_CK = "rafaelvargassilva/voz-ptbr-ckpt"
TARGET_STEP = 35000                    # fine-tune: alvo de qualidade (~5-10h em A10G)
BASE_MODEL = "tts_models/pt/cv/vits"   # base portuguesa (mesma arquitetura) p/ fine-tune

LEASE_TTL = 1200                       # 20 min: se o lease não atualiza, considera morto


def _now(): return int(time.time())


def _read_step():
    """passo mais alto a partir dos checkpoints na pasta da run."""
    best = 0
    for c in glob.glob(RUNROOT + "/**/*.pth", recursive=True):
        d = "".join(ch for ch in os.path.basename(c) if ch.isdigit())
        if d:
            best = max(best, int(d))
    return best


def _run_subdir():
    subs = [d for d in glob.glob(RUNROOT + "/*") if os.path.isdir(d) and glob.glob(d + "/*.pth")]
    return sorted(subs)[-1] if subs else None


def _hf_push(local, name, token):
    try:
        from huggingface_hub import HfApi
        HfApi(token=token).upload_file(path_or_fileobj=local, path_in_repo=name,
                                       repo_id=HF_CK, repo_type="model")
    except Exception as e:
        print("[HF] push falhou:", name, e, flush=True)


def _heartbeat(status, step, token, extra=""):
    msg = ("PROGRESSO voz pt-BR (Modal) | %s | passo~%d | %s UTC\n"
           "STATUS=%s\nSTEP=%d\nTS=%d\nTARGET=%d\n--- ultimas metricas ---\n%s"
           % (status, step, datetime.datetime.utcnow().strftime("%H:%M"),
              status, step, _now(), TARGET_STEP, extra))
    try:
        open(PROG, "w").write(msg)
        vol.commit()
    except Exception:
        pass
    _hf_push(PROG, "progress.txt", token)


def _train_once():
    """Um ciclo de treino: resume-ou-fine-tune, treina até alvo/timeout, salva. Idempotente."""
    import threading, subprocess
    from huggingface_hub import login, snapshot_download
    token = os.environ.get("HF_TOKEN", "")
    login(token)

    if os.path.exists(DONE):
        print(">> DONE já existe. Nada a fazer.", flush=True)
        return "DONE"

    # lease anti-concorrência
    if os.path.exists(LEASE):
        try:
            age = _now() - int(open(LEASE).read().strip() or 0)
        except Exception:
            age = 1e9
        if age < LEASE_TTL:
            print(">> outro treino ativo (lease há %ds). Saindo." % age, flush=True)
            return "BUSY"
    open(LEASE, "w").write(str(_now())); vol.commit()

    # dataset cacheado no Volume
    if not os.path.exists(DATADIR + "/metadata.csv"):
        print(">> baixando dataset do HF...", flush=True)
        snapshot_download(HF_DS, repo_type="dataset", local_dir=DATADIR)
        vol.commit()
    os.makedirs(RUNROOT, exist_ok=True)

    # decide RESUME (continue_path) vs FINE-TUNE do zero da base (restore_path)
    sub = _run_subdir()
    CONT = sub or ""
    RESTORE = ""
    if not CONT:
        try:
            from TTS.utils.manage import ModelManager
            mp, cp, _ = ModelManager().download_model(BASE_MODEL)
            RESTORE = mp
            print(">> FINE-TUNE da base:", BASE_MODEL, "->", mp, flush=True)
        except Exception as e:
            print(">> base indisponível, treino do zero:", e, flush=True)

    os.environ["VOZ_CONT"] = CONT
    os.environ["VOZ_RESTORE"] = RESTORE
    os.environ["VOZ_OUT"] = RUNROOT
    os.environ["VOZ_DATA"] = DATADIR
    os.environ["VOZ_TARGET"] = str(TARGET_STEP)

    # escreve o script de treino (inerda config da base se houver; senão char-config pt-BR)
    open("/root/train_run.py", "w").write(RECIPE)

    # monitor: heartbeat + commit do Volume + refresh do lease
    T0 = _now(); STOP = [False]; LAST = [_read_step()]
    def monitor():
        while not STOP[0]:
            time.sleep(180)
            try:
                step = max(_read_step(), LAST[0]); LAST[0] = step
                open(LEASE, "w").write(str(_now()))
                tail = os.popen("tail -n 60 /root/train.log 2>/dev/null | grep -aE 'GLOBAL_STEP|avg_|loss|EPOCH' | tail -n 6").read()
                vol.commit()
                _heartbeat("RUNNING", step, token, tail)
                print("[MON] passo~%d | %dmin" % (step, (_now() - T0) // 60), flush=True)
            except Exception as e:
                print("[MON] erro:", e, flush=True)
    threading.Thread(target=monitor, daemon=True).start()

    _heartbeat("RUNNING", LAST[0], token, "iniciando...")
    rc = 1
    try:
        p = subprocess.Popen(["python", "/root/train_run.py"], stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT, bufsize=1, universal_newlines=True)
        with open("/root/train.log", "w") as lg:
            for line in p.stdout:
                print(line, end="", flush=True); lg.write(line); lg.flush()
        rc = p.wait()
    except Exception:
        open("/root/train.log", "a").write("\n[ORQ] excecao:\n" + traceback.format_exc())
    finally:
        STOP[0] = True; time.sleep(1)
        step = max(_read_step(), LAST[0])
        try:
            if os.path.exists(LEASE): os.remove(LEASE)
        except Exception:
            pass
        # sobe melhor checkpoint + config p/ HF (visibilidade/portabilidade)
        sub = _run_subdir()
        if sub:
            for f in sorted(glob.glob(sub + "/*.pth"))[-1:] + glob.glob(sub + "/config.json"):
                _hf_push(f, os.path.basename(f), token)
        tail = os.popen("tail -n 40 /root/train.log 2>/dev/null").read()
        if rc == 0 and step >= TARGET_STEP:
            open(DONE, "w").write(str(step)); vol.commit()
            _heartbeat("DONE", step, token, "alvo atingido.\n" + tail)
            return "DONE"
        elif rc == 0:
            _heartbeat("PAUSED", step, token, "ciclo ok; retoma no proximo.\n" + tail)
            vol.commit(); return "PAUSED"
        else:
            _heartbeat("FAILED", step, token, "rc=%d\n%s" % (rc, tail))
            vol.commit(); return "FAILED"


RECIPE = r'''
import os, glob
from trainer import Trainer, TrainerArgs
from TTS.tts.configs.vits_config import VitsConfig
from TTS.tts.configs.shared_configs import BaseDatasetConfig, CharactersConfig
from TTS.tts.datasets import load_tts_samples
from TTS.tts.models.vits import Vits, VitsAudioConfig
from TTS.tts.utils.text.tokenizer import TTSTokenizer
from TTS.utils.audio import AudioProcessor

OUT=os.environ["VOZ_OUT"]; DATA=os.environ["VOZ_DATA"]
CONT=os.environ.get("VOZ_CONT",""); RESTORE=os.environ.get("VOZ_RESTORE","")
ds=BaseDatasetConfig(formatter="ljspeech", meta_file_train="metadata.csv", path=DATA)

cfg=VitsConfig()
# Se vamos fazer fine-tune da base, herda a config dela (chars/audio batem com os pesos)
base_cfg=os.path.join(os.path.dirname(RESTORE),"config.json") if RESTORE else ""
inherited=False
if base_cfg and os.path.exists(base_cfg):
    try:
        cfg.load_json(base_cfg); inherited=True
        print(">> config herdada da base:", base_cfg, "| sample_rate=", cfg.audio.sample_rate, flush=True)
    except Exception as e:
        print(">> nao deu p/ herdar config da base:", e, flush=True)
if not inherited:
    cfg.audio=VitsAudioConfig(sample_rate=22050)
    cfg.characters=CharactersConfig(characters_class="TTS.tts.models.vits.VitsCharacters",
      pad="<PAD>",eos="<EOS>",bos="<BOS>",blank="<BLNK>",
      characters="abcdefghijklmnopqrstuvwxyzaaaaeeiooouucABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789áàâãéêíóôõúüçÁÀÂÃÉÊÍÓÔÕÚÜÇ",
      punctuations="!'(),-.:;? ")

# overrides comuns (treino estável + ephemeral-friendly)
cfg.run_name="voz_ptbr"; cfg.output_path=OUT; cfg.datasets=[ds]
cfg.batch_size=16; cfg.eval_batch_size=8
cfg.num_loader_workers=2; cfg.num_eval_loader_workers=2
cfg.run_eval=True; cfg.test_delay_epochs=-1; cfg.epochs=1000
cfg.use_phonemes=False; cfg.text_cleaner="multilingual_cleaners"
cfg.mixed_precision=False               # FIX confirmado: fp16 derrubava o kl_loss no passo 0
cfg.print_step=25; cfg.plot_step=200
cfg.save_step=1000; cfg.save_n_checkpoints=3; cfg.save_best_after=1000
cfg.test_sentences=["O andador nao ensina o bebe a andar.","Equilibrio se aprende firmando o proprio peso."]

ap=AudioProcessor.init_from_config(cfg)
tok,cfg=TTSTokenizer.init_from_config(cfg)
tr,ev=load_tts_samples(ds, eval_split=True, eval_split_size=0.01)
print("AMOSTRAS treino:", len(tr), "| eval:", len(ev), flush=True)
model=Vits(cfg, ap, tok, speaker_manager=None)

if CONT:
    args=TrainerArgs(continue_path=CONT)      # RESUME real (otimizador+scheduler+passo)
    print(">> CONTINUE_PATH:", CONT, flush=True)
elif RESTORE:
    args=TrainerArgs(restore_path=RESTORE)    # FINE-TUNE da base (so pesos, run nova)
    print(">> RESTORE_PATH (fine-tune):", RESTORE, flush=True)
else:
    args=TrainerArgs()
    print(">> treino do zero", flush=True)
Trainer(args, cfg, output_path=OUT, model=model, train_samples=tr, eval_samples=ev).fit()
'''


# ---- Function de treino: GPU, retries (auto-resume em crash), timeout longo ----
@app.function(image=image, gpu="A10G", volumes={CKDIR: vol},
              secrets=[modal.Secret.from_name("huggingface")],
              timeout=12 * 3600, retries=2)
def treinar():
    return _train_once()


# ---- Cron de segurança: a cada 8h religa se não terminou (no-op se DONE/ativo) ----
@app.function(image=image, gpu="A10G", volumes={CKDIR: vol},
              secrets=[modal.Secret.from_name("huggingface")],
              timeout=12 * 3600, retries=2,
              schedule=modal.Cron("0 */8 * * *"))
def treinar_agendado():
    return _train_once()


@app.local_entrypoint()
def main():
    # dispara um ciclo agora (bloqueia até o ciclo retornar status)
    print("status:", treinar.remote())
