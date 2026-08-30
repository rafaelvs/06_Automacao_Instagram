# -*- coding: utf-8 -*-
"""Testa o caminho de ERRO do publish.py sem tocar na rede.

Espelha o test_publicacao.py do repo rafaelvs/linkedin-rv, adaptado a duas
diferencas reais do motor do Instagram:

  1. A Meta devolve HTTP **400** (nao 401) com type=OAuthException / code=190
     quando o token expira. Um teste que so' simulasse 401 passaria verde e
     nao provaria nada.
  2. Codigos de RATE LIMIT (4, 17, 32...) tambem vem com type=OAuthException.
     Eles sao transitorios e NAO podem derrubar o job — cenario E cobre isso.

Relogio congelado em 2026-07-28 18:00 BRT (terca) => a janela abre para
1 POST + 1 SEQUENCIA e nao para reel. Assim da' para testar "token morre no
meio da execucao" com dois itens de tipos diferentes.

Uso, dentro do repo:  python test_publicacao.py      (exit 0 = tudo passou)
"""
import json, os, sys, subprocess, tempfile, shutil
from pathlib import Path

ROOT = Path(__file__).parent

CAP = ("Discrepancia de membro: medir antes de operar. Conteudo educativo.\n\n"
       "Dr. Rafael Vargas · Médico · CRM-SP 226103 · RQE 137901")
# 16/08/2026: assinatura CRM+RQE virou VIOLACAO (nao so REVISAR) na auditoria v1 —
# fixture sem ela travava no _cfm_guard antes mesmo de chegar no cenario de auth
# que este teste quer exercitar. Toda legenda real ja carrega a assinatura.

POSTS = [{"id": "t-post-1", "images": ["media/a.png"], "caption": CAP}]
SEQS = [{"id": "t-seq-1", "theme": "teste",
         "images": [f"media/s{i}.png" for i in range(1, 6)]}]
REELS = [{"id": "t-reel-1", "video": "media/v.mp4", "caption": CAP}]

STUB = r'''
import sys, json, types, datetime as _dt
CENARIO = sys.argv[1]

# 2026-07-28 21:00Z = terca 18:00 BRT -> abre POST (15h) e SEQUENCIA (12:30)
FIXO = _dt.datetime(2026, 7, 28, 21, 0, tzinfo=_dt.timezone.utc)
class FakeDT(_dt.datetime):
    @classmethod
    def now(cls, tz=None):
        return FIXO.astimezone(tz) if tz else FIXO

_n = {"publicados": 0}

class R:
    def __init__(self, code, payload):
        self.status_code = code; self._p = payload; self.text = json.dumps(payload)
    def json(self): return self._p

# Corpo REAL da Meta para token expirado (HTTP 400, nao 401).
ERR_AUTH = {"error": {"message": "Error validating access token: Session has expired",
                      "type": "OAuthException", "code": 190, "error_subcode": 463}}
# Rate limit: TAMBEM OAuthException, porem transitorio -> nao pode virar AuthError.
ERR_RATE = {"error": {"message": "(#4) Application request limit reached",
                      "type": "OAuthException", "code": 4}}
ERR_500 = {"error": {"message": "An unknown error occurred", "type": "Exception", "code": 1}}

def _falha():
    if CENARIO == "auth": return R(400, ERR_AUTH)
    if CENARIO == "rate": return R(400, ERR_RATE)
    if CENARIO == "erro_comum": return R(500, ERR_500)
    if CENARIO == "auth_mid" and _n["publicados"] >= 1: return R(400, ERR_AUTH)
    return None

import requests
def fake_post(url, data=None, timeout=None, **kw):
    r = _falha()
    if r is not None: return r
    if url.endswith("/media_publish"):
        _n["publicados"] += 1
        return R(200, {"id": "MID%03d" % _n["publicados"]})
    return R(200, {"id": "CONT001"})
def fake_get(url, params=None, timeout=None, **kw):
    r = _falha()
    if r is not None: return r
    return R(200, {"status_code": "FINISHED"})
requests.post = fake_post
requests.get = fake_get

import publish
publish.dt = types.SimpleNamespace(datetime=FakeDT, timezone=_dt.timezone,
                                   timedelta=_dt.timedelta)
publish.time.sleep = lambda *a, **k: None
publish.main()
'''


def preparar():
    tmp = Path(tempfile.mkdtemp(prefix="igtest_"))
    for f in ["publish.py", "cfm_guardrails.py"]:
        shutil.copy(ROOT / f, tmp / f)
    (tmp / "posts.json").write_text(json.dumps(POSTS, ensure_ascii=False), encoding="utf-8")
    (tmp / "sequences.json").write_text(json.dumps(SEQS, ensure_ascii=False), encoding="utf-8")
    (tmp / "reels.json").write_text(json.dumps(REELS, ensure_ascii=False), encoding="utf-8")
    (tmp / "stories.json").write_text("[]", encoding="utf-8")
    (tmp / "destaques.json").write_text("[]", encoding="utf-8")
    (tmp / "state").mkdir(exist_ok=True)
    (tmp / "state" / "published.json").write_text(json.dumps(
        {"published": [], "last_post_date": "", "last_seq_date": "", "last_reel_date": ""}),
        encoding="utf-8")
    (tmp / "_stub.py").write_text(STUB, encoding="utf-8")
    return tmp


def rodar(cenario, tmp):
    env = dict(os.environ)
    env.update({"IG_USER_ID": "1784", "IG_ACCESS_TOKEN": "fake",
                "GITHUB_REPOSITORY": "rafaelvs/06_Automacao_Instagram",
                "FORCE_ID": "", "LOCATION_ID": "", "TRIAL_REELS": "false",
                "PYTHONUTF8": "1", "PYTHONIOENCODING": "utf-8"})
    p = subprocess.run([sys.executable, str(tmp / "_stub.py"), cenario],
                       cwd=str(tmp), capture_output=True, text=True, env=env)
    st = json.loads((tmp / "state" / "published.json").read_text(encoding="utf-8"))
    return p.returncode, (p.stdout or "") + (p.stderr or ""), st


falhas = []
def checa(nome, cond, detalhe):
    print(f"  {'PASS' if cond else 'FALHA'}  {nome}: {detalhe}")
    if not cond:
        falhas.append(nome)

def ids(st):
    return [e["id"] for e in st["published"]]


print("=" * 74)
print("A) token EXPIRADO (HTTP 400 / OAuthException 190) — job PRECISA ficar vermelho")
tmp = preparar(); rc, out, st = rodar("auth", tmp)
checa("exit != 0", rc != 0, f"exit={rc}")
checa("nada marcado como publicado", ids(st) == [], f"publicados={ids(st)}")
checa("aviso de fila parada", "PARADA" in out.upper(), "mensagem de erro presente")
checa("nao avancou last_post_date", st["last_post_date"] == "", f"={st['last_post_date']!r}")
shutil.rmtree(tmp, ignore_errors=True)

print("\nB) REGRESSAO — token OK, operacao normal (1 post + 1 sequencia)")
tmp = preparar(); rc, out, st = rodar("ok", tmp)
checa("exit == 0", rc == 0, f"exit={rc}")
checa("publicou post e sequencia", ids(st) == ["t-post-1", "t-seq-1"], f"publicados={ids(st)}")
checa("gravou last_post_date", st["last_post_date"] == "2026-07-28", f"={st['last_post_date']!r}")
checa("gravou last_seq_date", st["last_seq_date"] == "2026-07-28", f"={st['last_seq_date']!r}")
checa("nao publicou reel (fora da janela)", "t-reel-1" not in ids(st), "terca nao tem reel")
shutil.rmtree(tmp, ignore_errors=True)

print("\nC) token morre NO MEIO — o que saiu fica gravado E job fica vermelho")
tmp = preparar(); rc, out, st = rodar("auth_mid", tmp)
checa("exit != 0", rc != 0, f"exit={rc}")
checa("gravou o post que saiu antes da falha", ids(st) == ["t-post-1"], f"publicados={ids(st)}")
checa("nao marcou a sequencia que falhou", "t-seq-1" not in ids(st), "sequencia fora do estado")
shutil.rmtree(tmp, ignore_errors=True)

print("\nD) REGRESSAO — erro COMUM (HTTP 500) segue tolerado, job continua verde")
tmp = preparar(); rc, out, st = rodar("erro_comum", tmp)
checa("exit == 0", rc == 0, f"exit={rc}")
checa("nada publicado", ids(st) == [], f"publicados={ids(st)}")
shutil.rmtree(tmp, ignore_errors=True)

print("\nE) RATE LIMIT (OAuthException code 4) NAO e' falha de auth — job verde")
tmp = preparar(); rc, out, st = rodar("rate", tmp)
checa("exit == 0", rc == 0, f"exit={rc}")
checa("nada publicado", ids(st) == [], f"publicados={ids(st)}")
shutil.rmtree(tmp, ignore_errors=True)

print("\nF) CLASSIFICACAO dos erros da Meta (a parte sutil: quase tudo e' OAuthException)")
os.environ.setdefault("IG_USER_ID", "1784")
os.environ.setdefault("IG_ACCESS_TOKEN", "fake")
sys.path.insert(0, str(ROOT))
import publish as P

TABELA = [
    ("token expirado (caso real: HTTP 400)", 400,
     {"error": {"type": "OAuthException", "code": 190, "error_subcode": 463}}, True),
    ("token revogado (subcode 467)", 400,
     {"error": {"type": "OAuthException", "code": 190, "error_subcode": 467}}, True),
    ("sessao invalida (102)", 400, {"error": {"type": "OAuthException", "code": 102}}, True),
    ("app sem permissao (10)", 400, {"error": {"type": "OAuthException", "code": 10}}, True),
    ("familia de permissao (200)", 403, {"error": {"type": "OAuthException", "code": 200}}, True),
    ("401 sem corpo", 401, {}, True),
    # --- os que NAO podem virar job vermelho ---
    ("rate limit app (4)", 400, {"error": {"type": "OAuthException", "code": 4}}, False),
    ("rate limit user (17)", 400, {"error": {"type": "OAuthException", "code": 17}}, False),
    ("parametro invalido (100)", 400, {"error": {"type": "OAuthException", "code": 100}}, False),
    ("video corrompido (2207026)", 400, {"error": {"type": "OAuthException", "code": 2207026}}, False),
    ("erro de midia novo (2207099)", 400, {"error": {"type": "OAuthException", "code": 2207099}}, False),
    ("erro generico (500)", 500, {"error": {"type": "Exception", "code": 1}}, False),
    ("corpo vazio", 500, {}, False),
    ("corpo HTML/lista (gateway)", 502, ["gateway"], False),
    ("error como string", 400, {"error": "boom"}, False),
]
for nome, st, payload, esperado in TABELA:
    got = P._e_falha_de_auth(st, payload)
    checa(nome, got == esperado, f"auth={got} (esperado {esperado})")

print("=" * 74)
print("RESULTADO:", "TODOS PASSARAM" if not falhas else f"FALHAS -> {falhas}")
sys.exit(1 if falhas else 0)
