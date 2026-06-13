# -*- coding: utf-8 -*-
"""
Treino da voz pt-BR numa VM GPU do GCP — autônomo, sem token (usa só fontes públicas + GCS).

- Dados: reconstrói do corpus PÚBLICO TTS-Portuguese (CC-BY) -> sem Hugging Face privado.
- Storage: checkpoints/progresso num bucket GCS via a service account da VM (auth nativa).
- Fine-tune VITS de tts_models/pt/cv/vits (acaba em ~5-10h); resume real com continue_path.
- Self-healing: roda dentro de um MIG Spot (recria sozinho se preemptado, retoma do checkpoint).
- Self-terminate: ao atingir o alvo, grava DONE e zera o MIG (a VM se desliga -> custo para).
"""
import os, glob, time, threading, subprocess, datetime, traceback, urllib.request, zipfile, csv

os.environ["TORCH_FORCE_NO_WEIGHTS_ONLY_LOAD"] = "1"
os.environ["COQUI_TOS_AGREED"] = "1"
os.environ["CUDA_VISIBLE_DEVICES"] = "0"

BUCKET = os.environ.get("VOZ_BUCKET", "").rstrip("/")     # gs://projeto-voz-ckpt
MIG = os.environ.get("VOZ_MIG", "")
TARGET_STEP = 35000
BASE_MODEL = "tts_models/pt/cv/vits"
WORK = "/opt/voz"; RUN = WORK + "/run"; DATA = WORK + "/data"


def md(path):
    try:
        r = urllib.request.Request("http://metadata.google.internal/computeMetadata/v1/" + path,
                                   headers={"Metadata-Flavor": "Google"})
        return urllib.request.urlopen(r, timeout=5).read().decode()
    except Exception:
        return ""


ZONE = md("instance/zone").split("/")[-1]
NAME = md("instance/name")


def sh(c):
    return subprocess.run(c, shell=True, capture_output=True, text=True)


def gcs_up():
    if BUCKET:
        sh(f"gsutil -m rsync -d -r {RUN} {BUCKET}/run")


def gcs_down():
    if BUCKET:
        os.makedirs(RUN, exist_ok=True)
        sh(f"gsutil -m rsync -r {BUCKET}/run {RUN}")


def gcs_put(local, name):
    if BUCKET and os.path.exists(local):
        sh(f"gsutil cp {local} {BUCKET}/{name}")


def gcs_exists(name):
    return BUCKET and sh(f"gsutil -q stat {BUCKET}/{name}").returncode == 0


def progress(status, step, extra=""):
    msg = (f"PROGRESSO voz pt-BR (GCP) | {status} | passo~{step} | "
           f"{datetime.datetime.utcnow():%H:%M} UTC\n"
           f"STATUS={status}\nSTEP={step}\nTS={int(time.time())}\nTARGET={TARGET_STEP}\n"
           f"--- ultimas metricas ---\n{extra}")
    try:
        open(WORK + "/progress.txt", "w").write(msg)
        gcs_put(WORK + "/progress.txt", "progress.txt")
    except Exception as e:
        print("[PROG]", e, flush=True)


def stop_mig():
    """Zera o MIG -> a VM se autodestrói (custo para)."""
    if MIG and ZONE:
        print(">> alvo atingido: zerando MIG (autodesliga)", flush=True)
        sh(f"gcloud compute instance-groups managed resize {MIG} --size 0 --zone {ZONE} -q")


def newest_ckpt():
    best, bstep = None, -1
    for c in glob.glob(RUN + "/**/*.pth", recursive=True):
        d = "".join(ch for ch in os.path.basename(c) if ch.isdigit())
        s = int(d) if d else 0
        if s >= bstep:
            bstep, best = s, c
    return best, max(bstep, 0)


def run_subdir():
    subs = [d for d in glob.glob(RUN + "/*") if os.path.isdir(d) and glob.glob(d + "/*.pth")]
    return sorted(subs)[-1] if subs else None


# ---------------- prep de dados do corpus PÚBLICO ----------------
def prep():
    if os.path.exists(DATA + "/metadata.csv"):
        print(">> dataset já preparado", flush=True); return
    os.makedirs(WORK, exist_ok=True); os.chdir(WORK)
    import soundfile as sf, librosa, numpy as np
    if not os.path.isdir("corpus"):
        ok = False
        for url in ["https://huggingface.co/datasets/Edresson/TTS-Portuguese-Corpus/resolve/main/TTS-Portuguese-Corpus.zip",
                    "https://www.dropbox.com/s/ohpc7epowv9ct7o/TTS-Portuguese-Corpus.zip?dl=1"]:
            try:
                print(">> baixando corpus:", url[:60], flush=True)
                urllib.request.urlretrieve(url, "c.zip")
                zipfile.ZipFile("c.zip").extractall("corpus"); os.remove("c.zip"); ok = True; break
            except Exception as e:
                print(">> falhou:", e, flush=True)
        assert ok, "download do corpus falhou"
    metas = [f for f in glob.glob("corpus/**/*", recursive=True)
             if f.lower().endswith((".csv", ".txt"))]
    texts = {}
    for m in metas:
        try:
            lines = open(m, encoding="utf-8", errors="ignore").read().splitlines()
        except Exception:
            continue
        for ln in lines:
            for sep in ["==", "|", "\t", ","]:
                if sep in ln:
                    k, v = ln.split(sep, 1)
                    k = os.path.splitext(os.path.basename(k.strip()))[0]
                    if k and v.strip():
                        texts[k] = v.strip().strip('"')
                    break
    print(">> transcricoes:", len(texts), flush=True)
    os.makedirs(DATA + "/wavs", exist_ok=True); rows = []; SR = 22050
    wavs = glob.glob("corpus/**/*.wav", recursive=True)
    print(">> wavs no corpus:", len(wavs), flush=True)
    for i, w in enumerate(wavs):
        wid = os.path.splitext(os.path.basename(w))[0]; t = texts.get(wid)
        if not t:
            continue
        try:
            y, _ = librosa.load(w, sr=SR, mono=True)
            y, _ = librosa.effects.trim(y, top_db=30)
            y = np.concatenate([y, np.zeros(int(0.08 * SR))])
            if len(y) < int(0.4 * SR):
                continue
            sf.write(f"{DATA}/wavs/{wid}.wav", (y * 32767).astype("int16"), SR, subtype="PCM_16")
            rows.append((wid, t, t))
        except Exception:
            pass
        if i % 500 == 0:
            print("  processados", i, flush=True)
    csv.writer(open(DATA + "/metadata.csv", "w", encoding="utf-8", newline=""),
               delimiter="|").writerows(rows)
    print(">> clipes válidos:", len(rows), flush=True)


# ---------------- recipe de treino ----------------
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
base_cfg=os.path.join(os.path.dirname(RESTORE),"config.json") if RESTORE else ""
inherited=False
if base_cfg and os.path.exists(base_cfg):
    try:
        cfg.load_json(base_cfg); inherited=True
        print(">> config herdada da base | sr=", cfg.audio.sample_rate, flush=True)
    except Exception as e:
        print(">> nao herdou config:", e, flush=True)
if not inherited:
    cfg.audio=VitsAudioConfig(sample_rate=22050)
    cfg.characters=CharactersConfig(characters_class="TTS.tts.models.vits.VitsCharacters",
      pad="<PAD>",eos="<EOS>",bos="<BOS>",blank="<BLNK>",
      characters="abcdefghijklmnopqrstuvwxyzaaaaeeiooouucABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789áàâãéêíóôõúüçÁÀÂÃÉÊÍÓÔÕÚÜÇ",
      punctuations="!'(),-.:;? ")
cfg.run_name="voz_ptbr"; cfg.output_path=OUT; cfg.datasets=[ds]
cfg.batch_size=16; cfg.eval_batch_size=8
cfg.num_loader_workers=3; cfg.num_eval_loader_workers=2
cfg.run_eval=True; cfg.test_delay_epochs=-1; cfg.epochs=1000
cfg.use_phonemes=False; cfg.text_cleaner="multilingual_cleaners"
cfg.mixed_precision=False                # FIX: fp16 derrubava o kl_loss no passo 0
cfg.print_step=25; cfg.plot_step=200
cfg.save_step=1000; cfg.save_n_checkpoints=3; cfg.save_best_after=1000
cfg.test_sentences=["O andador nao ensina o bebe a andar.","Equilibrio se aprende firmando o proprio peso."]
ap=AudioProcessor.init_from_config(cfg)
tok,cfg=TTSTokenizer.init_from_config(cfg)
tr,ev=load_tts_samples(ds, eval_split=True, eval_split_size=0.01)
print("AMOSTRAS treino:", len(tr), "| eval:", len(ev), flush=True)
model=Vits(cfg, ap, tok, speaker_manager=None)
if CONT:
    args=TrainerArgs(continue_path=CONT); print(">> CONTINUE_PATH:", CONT, flush=True)
elif RESTORE:
    args=TrainerArgs(restore_path=RESTORE); print(">> RESTORE (fine-tune):", RESTORE, flush=True)
else:
    args=TrainerArgs(); print(">> do zero", flush=True)
Trainer(args, cfg, output_path=OUT, model=model, train_samples=tr, eval_samples=ev).fit()
'''


def main():
    os.makedirs(WORK, exist_ok=True)
    # já concluído?
    if gcs_exists("DONE"):
        print(">> DONE no bucket. Nada a fazer; zerando MIG.", flush=True); stop_mig(); return
    prep()
    gcs_down()                       # retoma estado anterior, se houver
    os.makedirs(RUN, exist_ok=True)

    sub = run_subdir(); CONT = sub or ""; RESTORE = ""
    if not CONT:
        try:
            from TTS.utils.manage import ModelManager
            mp, cp, _ = ModelManager().download_model(BASE_MODEL)
            RESTORE = mp; print(">> base p/ fine-tune:", mp, flush=True)
        except Exception as e:
            print(">> base indisponível, treino do zero:", e, flush=True)
    os.environ["VOZ_OUT"] = RUN; os.environ["VOZ_DATA"] = DATA
    os.environ["VOZ_CONT"] = CONT; os.environ["VOZ_RESTORE"] = RESTORE
    open(WORK + "/train_run.py", "w").write(RECIPE)

    T0 = time.time(); STOP = [False]; LAST = [newest_ckpt()[1]]

    def monitor():
        while not STOP[0]:
            time.sleep(180)
            try:
                step = max(newest_ckpt()[1], LAST[0]); LAST[0] = step
                tail = os.popen("tail -n 60 " + WORK + "/train.log 2>/dev/null | grep -aE 'GLOBAL_STEP|avg_|loss|EPOCH' | tail -n 6").read()
                gcs_up(); progress("RUNNING", step, tail)
                print(f"[MON] passo~{step} | {int(time.time()-T0)//60}min", flush=True)
            except Exception as e:
                print("[MON]", e, flush=True)
    threading.Thread(target=monitor, daemon=True).start()

    progress("RUNNING", LAST[0], "iniciando...")
    rc = 1
    try:
        p = subprocess.Popen(["python3", WORK + "/train_run.py"], stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT, bufsize=1, universal_newlines=True)
        with open(WORK + "/train.log", "w") as lg:
            for line in p.stdout:
                print(line, end="", flush=True); lg.write(line); lg.flush()
        rc = p.wait()
    except Exception:
        open(WORK + "/train.log", "a").write("\n[ORQ]\n" + traceback.format_exc())
    finally:
        STOP[0] = True; time.sleep(1)
        gcs_up()
        sub = run_subdir()
        if sub:
            for f in sorted(glob.glob(sub + "/*.pth"))[-1:] + glob.glob(sub + "/config.json"):
                gcs_put(f, "latest/" + os.path.basename(f))
        step = max(newest_ckpt()[1], LAST[0])
        tail = os.popen("tail -n 40 " + WORK + "/train.log 2>/dev/null").read()
        gcs_put(WORK + "/train.log", "train.log")
        if rc == 0 and step >= TARGET_STEP:
            open(WORK + "/DONE", "w").write(str(step)); gcs_put(WORK + "/DONE", "DONE")
            progress("DONE", step, "alvo atingido.\n" + tail); stop_mig()
        elif rc == 0:
            progress("PAUSED", step, "ciclo ok; retoma no proximo boot.\n" + tail)
        else:
            progress("FAILED", step, f"rc={rc}\n{tail}")
        print(f">> fim rc={rc} passo~{step}", flush=True)


if __name__ == "__main__":
    main()
