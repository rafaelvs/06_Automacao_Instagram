#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Guarda o contrato de EXIT CODE do publish.py.   Rodar:  python teste_publish_exit.py

Por que este teste existe
-------------------------
Ate 07/2026 toda falha NAO-auth do publish.py saia por `print` puro: o job do Actions
terminava VERDE. Como o item que falha nao entra em `done` nem avanca `last_*_date`, o
cron (*/30) repetia o MESMO item para sempre — inclusive o `BLOQUEADO CFM` do guardrail,
que e' permanente. A fila ficava parada com o painel todo verde. (Varredura de 30/07/2026;
ver a licao "except: pass desliga o alarme".)

O contrato que este arquivo protege:
  - falha de item          -> ::error:: e exit 1   (job VERMELHO = notificacao do GitHub)
  - publicacao bem-sucedida-> exit 0               (nao pode virar alarme falso)
  - aviso de expiracao     -> ::warning:: e exit 0 (avisa, nunca bloqueia)

Nao toca a rede: `requests` e' stubado dentro de um sandbox temporario.
"""
import json, os, shutil, subprocess, sys, tempfile, datetime as dt

REPO = os.path.dirname(os.path.abspath(__file__))

STUB_REQUESTS = '''
class _R:
    status_code = 200
    text = "{}"
    def json(self): return {"id": "FAKE_MEDIA_ID", "status_code": "FINISHED"}
class RequestException(Exception): pass
def post(*a, **k): return _R()
def get(*a, **k): return _R()
'''

ASSINATURA = "\nDr. Rafael Vargas - CRM-SP 226103 / RQE 137.901 - Medico"
CAPTION_LIMPA = "Como a consulta de ortopedia pediatrica funciona." + ASSINATURA
# "dismetria" e' TERMO VETADO no cfm_guardrails (o correto e' "discrepancia de membro").
CAPTION_VIOLACAO = "Tratamento de dismetria dos membros." + ASSINATURA


def montar(caption, token_state=None):
    d = tempfile.mkdtemp(prefix="ig_teste_")
    for f in ("publish.py", "cfm_guardrails.py"):
        shutil.copy(os.path.join(REPO, f), d)
    json.dump([{"id": "post01", "images": ["images/p1.jpg"], "caption": caption}],
              open(os.path.join(d, "posts.json"), "w", encoding="utf-8"))
    for nome in ("stories.json", "sequences.json", "reels.json", "destaques.json"):
        json.dump([], open(os.path.join(d, nome), "w", encoding="utf-8"))
    os.makedirs(os.path.join(d, "state"), exist_ok=True)
    if token_state is not None:
        json.dump(token_state, open(os.path.join(d, "state", "token_refresh.json"), "w", encoding="utf-8"))
    open(os.path.join(d, "requests.py"), "w", encoding="utf-8").write(STUB_REQUESTS)
    return d


def rodar(d, force_id="post01"):
    env = dict(os.environ)
    env.update({"IG_USER_ID": "123", "IG_ACCESS_TOKEN": "tok",
                "GITHUB_REPOSITORY": "rafaelvs/06_Automacao_Instagram",
                "FORCE_ID": force_id, "PYTHONPATH": d, "PYTHONIOENCODING": "utf-8"})
    p = subprocess.run([sys.executable, os.path.join(d, "publish.py")],
                       capture_output=True, text=True, env=env, cwd=d, timeout=120)
    return p.returncode, (p.stdout or "") + (p.stderr or "")


falhas = []
def checar(nome, cond, detalhe=""):
    print(f"  {'OK  ' if cond else 'FALHOU'}  {nome}" + (f"  <- {detalhe}" if not cond and detalhe else ""))
    if not cond: falhas.append(nome)


print("1) Bloqueio CFM tem de deixar o job VERMELHO")
rc, out = rodar(montar(CAPTION_VIOLACAO))
checar("exit 1", rc == 1, f"exit={rc}")
checar("emite ::error::", "::error::" in out)
checar("cita BLOQUEADO CFM", "BLOQUEADO CFM" in out)
checar("avisa da retentativa infinita", "RETENTAR" in out)

print("2) Publicacao OK continua VERDE (sem alarme falso)")
d = montar(CAPTION_LIMPA)
rc, out = rodar(d)
checar("exit 0", rc == 0, f"exit={rc}\n{out[-600:]}")
checar("sem ::error::", "::error::" not in out)
estado = json.load(open(os.path.join(d, "state", "published.json"), encoding="utf-8"))
checar("estado gravado", any(e["id"] == "post01" for e in estado.get("published", [])))

print("3) FORCE_ID inexistente e' falha, nao 'nada a fazer'")
rc, _ = rodar(montar(CAPTION_LIMPA), force_id="naoexiste99")
checar("exit 1", rc == 1, f"exit={rc}")

print("4) Aviso de expiracao avisa, mas NUNCA bloqueia")
hoje = dt.date.today()
rc, out = rodar(montar(CAPTION_LIMPA))                       # sem token_refresh.json
checar("sem registro: ::warning:: + exit 0", "::warning::" in out and rc == 0)
rc, out = rodar(montar(CAPTION_LIMPA, {"expira_em": (hoje + dt.timedelta(days=5)).isoformat()}))
checar("5 dias: avisa + exit 0", "::warning::" in out and "expira em" in out and rc == 0)
rc, out = rodar(montar(CAPTION_LIMPA, {"expira_em": (hoje + dt.timedelta(days=100)).isoformat()}))
checar("100 dias: silencio", "::warning::" not in out, out[-300:])
d = montar(CAPTION_LIMPA)
open(os.path.join(d, "state", "token_refresh.json"), "w").write("{lixo,,,")
rc, out = rodar(d)
checar("JSON corrompido: fail-open", rc == 0 and "FORCE post01 OK" in out, f"exit={rc}")

print()
if falhas:
    print(f"FALHOU: {len(falhas)} check(s) -> {falhas}")
    sys.exit(1)
print("TODOS OS CHECKS PASSARAM")
