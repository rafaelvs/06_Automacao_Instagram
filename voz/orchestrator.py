#!/usr/bin/env python3
"""
Orquestrador + vigia do treino da voz pt-BR (roda no GitHub Actions).
Modos:
  launch  -> dispara um run headless no Kaggle (resume do ultimo checkpoint), pacedo pelo cron M/Q/S.
  watch   -> le o heartbeat no HF; se FALHOU, abre issue e re-tenta (crash e' barato); se travado, alerta.
Respeita a cota Kaggle (30h GPU/semana): runs longos saudaveis sao pacedos so pelo schedule;
o watch so re-dispara em caso de FALHA (segundos de GPU), nunca relanca um PAUSED saudavel.
Secrets necessarios no repo: KAGGLE_USERNAME, KAGGLE_KEY, HF_TOKEN. (GITHUB_TOKEN ja vem do Actions.)
"""
import os, sys, time, subprocess, tempfile

KERNEL = "rafaelvargassilva/voz-ptbr-trainer"
CK     = "rafaelvargassilva/voz-ptbr-ckpt"
KDIR   = os.path.join(os.path.dirname(os.path.abspath(__file__)))  # pasta voz/ com kernel-metadata.json
HF_TOKEN = os.environ.get("HF_TOKEN", "")

from huggingface_hub import hf_hub_download, HfApi
api = HfApi(token=HF_TOKEN)

def sh(cmd):
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return r.returncode, (r.stdout or "") + (r.stderr or "")

def read_hb():
    try:
        p = hf_hub_download(CK, "progress.txt", repo_type="model", token=HF_TOKEN,
                            local_dir=tempfile.mkdtemp())
        txt = open(p, encoding="utf-8", errors="ignore").read()
    except Exception as e:
        print(">> sem progress.txt ainda:", e); return None, txt_default()
    d = {"STATUS": "?", "STEP": 0, "TS": 0, "TARGET": 0}
    for ln in txt.splitlines():
        for k in d:
            if ln.startswith(k + "="):
                v = ln.split("=", 1)[1].strip()
                d[k] = v if k == "STATUS" else int(float(v or 0))
    return d, txt

def txt_default(): return ""

def kernel_status():
    rc, out = sh(f'kaggle kernels status {KERNEL}')
    o = out.lower()
    for s in ("queued", "running", "cancelrequested", "complete", "error", "cancelacknowledged"):
        if s in o: return s
    if "404" in o or "not found" in o or "couldn't find" in o.lower(): return "none"
    return "unknown"

def push_run():
    rc, out = sh(f'kaggle kernels push -p "{KDIR}"')
    print(">> push:", out.strip())
    return rc == 0

def read_last_launch():
    try:
        p = hf_hub_download(CK, "last_launch.txt", repo_type="model", token=HF_TOKEN,
                            local_dir=tempfile.mkdtemp())
        return float(open(p).read().strip() or 0)
    except Exception:
        return 0.0

def write_last_launch():
    fn = os.path.join(tempfile.mkdtemp(), "last_launch.txt")
    open(fn, "w").write(str(int(time.time())))
    try: api.upload_file(path_or_fileobj=fn, path_in_repo="last_launch.txt", repo_id=CK, repo_type="model")
    except Exception as e: print(">> nao gravou last_launch:", e)

def gh_issue(title, body):
    # evita duplicar: so cria se nao ha issue aberta com o mesmo titulo
    rc, out = sh(f'gh issue list --state open --search {title!r} --json title')
    if title in out:
        print(">> issue ja aberta, nao duplico"); return
    body = body.replace("'", "")
    rc, out = sh(f'gh issue create --title {title!r} --body {body!r} --label voz')
    print(">> gh issue:", out.strip())

def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "watch"
    hb, raw = read_hb()
    ks = kernel_status()
    st = hb["STATUS"] if hb else "?"
    step = hb["STEP"] if hb else 0
    tgt = hb["TARGET"] if hb else 0
    age = int(time.time()) - (hb["TS"] if hb else 0)
    print(f"== modo={mode} | kernel={ks} | status={st} | passo={step}/{tgt} | heartbeat ha {age//60} min ==")

    if st == "DONE" or (tgt and step >= tgt and tgt > 0):
        print(">> treino concluido (DONE). Nada a fazer."); return

    if mode == "launch":
        if ks in ("running", "queued"):
            print(">> ja ha um run ativo; nao relanco."); return
        if push_run():
            write_last_launch(); print(">> RUN DISPARADO (resume).")
        else:
            gh_issue("voz: falha ao disparar run no Kaggle",
                     "O `kaggle kernels push` falhou no Actions. Checar KAGGLE_USERNAME/KAGGLE_KEY. @rafaelvs")
        return

    # mode == watch
    if ks in ("running", "queued"):
        if age > 1800:
            gh_issue("voz: heartbeat travado durante run",
                     f"Kernel marcado como {ks} mas o heartbeat nao atualiza ha {age//60} min "
                     f"(passo ~{step}). Pode estar travado; vai expirar no limite de tempo. @rafaelvs")
        else:
            print(">> rodando e saudavel.")
        return

    # nao esta rodando
    if st == "FAILED":
        last = read_last_launch()
        gh_issue("voz: treino FALHOU",
                 f"O ultimo run terminou com FAILED no passo ~{step}. Vou re-tentar automaticamente "
                 f"(crash e' barato). Se persistir, ver train.log no HF ({CK}). @rafaelvs")
        if time.time() - last > 3600:   # re-tenta no maximo ~1x/h (crash custa segundos)
            if push_run(): write_last_launch(); print(">> RE-DISPARADO apos falha.")
        else:
            print(">> falhou ha pouco; aguardando antes de re-tentar.")
    else:
        # PAUSED/idle saudavel -> proximo run e' pacedo pelo schedule (cota), nao relanco aqui.
        print(">> ocioso/PAUSED; aguardando proximo horario agendado (cota).")

if __name__ == "__main__":
    main()
