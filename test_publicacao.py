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
import json, os, re, sys, subprocess, tempfile, shutil
from pathlib import Path

ROOT = Path(__file__).parent

CAP = ("Discrepancia de membro: medir antes de operar. Conteudo educativo.\n\n"
       "Dr. Rafael Vargas · Médico · CRM-SP 226103 · RQE 137901")
# 16/08/2026: assinatura CRM+RQE virou VIOLACAO (nao so REVISAR) na auditoria v1 —
# fixture sem ela travava no _cfm_guard antes mesmo de chegar no cenario de auth
# que este teste quer exercitar. Toda legenda real ja carrega a assinatura.

# 12/09/2026 (saida da estagnacao): o post leva `collaborators` (B3) e o reel leva `trial`
# por peca (B5) — os stubs abaixo DENUNCIAM esses parametros na saida para os cenarios G/H.
POSTS = [{"id": "t-post-1", "images": ["media/a.png"], "caption": CAP,
          "collaborators": ["parceiro_a"]}]
SEQS = [{"id": "t-seq-1", "theme": "teste",
         "images": [f"media/s{i}.png" for i in range(1, 6)]}]
REELS = [{"id": "t-reel-1", "video": "media/v.mp4", "caption": CAP, "trial": True}]

STUB = r'''
import sys, json, types, datetime as _dt
CENARIO = sys.argv[1]

# 2026-07-28 21:00Z = terca 18:00 BRT -> abre POST (15h) e SEQUENCIA (12:30)
import os as _os
FIXO = _dt.datetime.fromisoformat(_os.environ["FAKE_NOW"]) if _os.environ.get("FAKE_NOW") \
    else _dt.datetime(2026, 7, 28, 21, 0, tzinfo=_dt.timezone.utc)
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
# Corpo REAL do HTTP 500 transitorio da Graph API (auditoria 24/10/2026): OAuthException, code 2,
# is_transient. Ate 24/10 esta fixture era {"type": "Exception", "code": 1} — corpo que a Meta nao manda
# — e nenhum teste via o 500 virar AuthError (parte da story e reel republicados no run seguinte).
ERR_500 = {"error": {"message": "An unexpected error has occurred. Please retry your request later.",
                     "type": "OAuthException", "is_transient": True, "code": 2}}
ERR_500_OAUTH = ERR_500          # nome usado pelos arneses de reproducao da revisao (lab/revisao_infra)

# A CONTA da Meta, persistida entre runs (cada run e' um processo novo): conteineres com status e as
# midias no ar. E' o que prova "nao publicou duas vezes" contando o que FOI AO AR, nao o que o estado diz.
_ARQ_CONTA = "_conta_meta.json"
def _conta():
    try:
        with open(_ARQ_CONTA, encoding="utf-8") as f: return json.load(f)
    except FileNotFoundError:
        return {"n_cont": 0, "n_mid": 0, "conteineres": {}, "midias": []}
def _gravar(c):
    with open(_ARQ_CONTA, "w", encoding="utf-8") as f: json.dump(c, f)
def _ts(t): return t.astimezone(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S+0000")
def _de_ts(s): return _dt.datetime.strptime(s, "%Y-%m-%dT%H:%M:%S%z")
def _ao_ar(c, cid):
    """A Meta poe a peca no ar: conteiner PUBLISHED e midia nova na conta."""
    c["n_mid"] += 1; mid = "MID%03d" % c["n_mid"]
    k = c["conteineres"][cid]; k["status"] = "PUBLISHED"; k["media"] = mid
    c["midias"].append({"id": mid, "timestamp": _ts(FIXO), "media_type": k["media_type"], "container": cid})
    _gravar(c)
    return mid
# story_500_tarde: a Meta respondeu 500 com o conteiner FINISHED e entregou DEPOIS — no run seguinte ja' saiu
_c0 = _conta()
for _cid, _k in list(_c0["conteineres"].items()):
    if _k.pop("tarde", False):
        print("NO_AR_TARDE", _cid, _ao_ar(_c0, _cid))
_gravar(_c0)

# a 2a media_publish do run falha; o efeito diz o que a Meta fez de fato
FALHA_NA_2A = {"story_500_saiu": "saiu", "story_500_oauth": "saiu", "story_500_nao": "nao",
               "story_500_tarde": "tarde", "morre_no_publish": "morre_saiu", "morre_antes_do_publish": "morre",
               "auth_no_publish_saiu": "auth_saiu"}
# o 1o media_publish do run (o do reel/post) falha; o efeito diz o que a Meta fez de fato (write-ahead de reel/post)
FALHA_NA_1A = {"reel_500_tarde": "tarde", "reel_500_nao": "nao", "reel_morre_no_publish": "morre_saiu",
               "post_500_tarde": "tarde"}

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
    data = data or {}
    c = _conta()
    if url.endswith("/media_publish"):
        cid = data.get("creation_id"); k = c["conteineres"].get(cid)
        if k is None:
            return R(400, {"error": {"message": "Media ID is not available", "type": "OAuthException",
                                     "code": 9007, "error_subcode": 2207006}})
        if k["status"] == "PUBLISHED":                  # conteiner so' publica uma vez
            print("REPUBLICAR_RECUSADO", cid)
            return R(400, {"error": {"message": "The media has already been published", "type": "OAuthException",
                                     "code": 100}})
        efeito = None
        if not _n.get("ja_falhou"):
            if CENARIO == "reel_500_oauth":             # o 1o media_publish (o do reel) leva 500 e SAI
                efeito = "saiu"
            elif CENARIO == "publish_500_incerto":      # o 1o media_publish leva 500 e a CONSULTA ao conteiner falha
                efeito = "saiu"; _n["consulta_falha"] = True
            elif CENARIO == "reel_nao_pronto":          # o 1o media_publish: "nao pronto" (9007/2207027), conteiner IN_PROGRESS
                efeito = "nao_pronto"
            elif CENARIO in FALHA_NA_1A:
                efeito = FALHA_NA_1A[CENARIO]
            elif _n["publicados"] == 1:
                efeito = FALHA_NA_2A.get(CENARIO)
        if efeito:
            _n["ja_falhou"] = True
            if efeito in ("saiu", "morre_saiu", "auth_saiu"):
                print("NO_AR_COM_500" if efeito == "saiu" else "NO_AR", cid, _ao_ar(c, cid), flush=True)
            if efeito == "tarde":
                k["tarde"] = True; _gravar(c)
            if efeito in ("morre_saiu", "morre"):       # job morto DENTRO da chamada (timeout/cancelamento)
                print("JOB_MORTO_NO_MEDIA_PUBLISH", cid, flush=True)
                _os._exit(137)
            if efeito == "auth_saiu":
                return R(400, ERR_AUTH)
            if efeito == "nao_pronto":
                k["status"] = "IN_PROGRESS"; _gravar(c)
                return R(400, {"error": {"message": "Media ID is not available", "type": "OAuthException",
                                         "code": 9007, "error_subcode": 2207027}})
            return R(500, ERR_500)
        _n["publicados"] += 1
        mid = _ao_ar(c, cid)
        print("NO_AR", cid, mid)
        return R(200, {"id": mid})
    # denuncia os parametros de audiencia emprestada / trial (cenarios G/H) e o CONTROLE:
    # story NUNCA pode levar collaborators (a API nao aceita).
    if "collaborators" in data:
        print("COLLAB_ENVIADO", data["collaborators"], "media_type=", data.get("media_type", "IMAGE"))
    if "trial_params" in data:
        print("TRIAL_PARAMS", data["trial_params"])
        if CENARIO == "trial_500":                     # 500 transitorio REAL no conteiner trial: nao e' recusa do parametro
            return R(500, ERR_500)
        if CENARIO == "trial_recusado":                # a Meta recusa o PARAMETRO (400, code 100): fallback normal
            return R(400, {"error": {"message": "Invalid parameter", "type": "OAuthException", "code": 100}})
    if "is_ai_generated" in data:
        print("ROTULO_IA", data["is_ai_generated"], "media_type=", data.get("media_type", "IMAGE"))
    print("MIDIA_URL", data.get("video_url") or data.get("image_url") or "-")
    c["n_cont"] += 1; cid = "CONT%03d" % c["n_cont"]
    c["conteineres"][cid] = {"status": "FINISHED", "media_type": data.get("media_type", "IMAGE"), "criado": _ts(FIXO)}
    _gravar(c)
    return R(200, {"id": cid})
def fake_get(url, params=None, timeout=None, **kw):
    r = _falha()
    if r is not None: return r
    params = params or {}
    if url.endswith("/media") and "like_count" in str(params.get("fields", "")):
        # leitura do ALARME de curtidas (B6-iii): 6 pecas do feed
        likes = 0 if CENARIO == "alarme_zero" else 1
        return R(200, {"data": [{"id": "M%d" % i, "like_count": likes, "media_product_type": "FEED"}
                                for i in range(6)]})
    c = _conta()
    if url.endswith("/stories"):                       # so' stories ATIVOS (24 h), como a edge real
        if CENARIO == "stories_falha":
            return R(500, ERR_500)
        vivos = [m for m in c["midias"] if m["media_type"] == "STORIES"
                 and FIXO - _de_ts(m["timestamp"]) < _dt.timedelta(hours=24)]
        return R(200, {"data": [{"id": m["id"], "timestamp": m["timestamp"]} for m in vivos]})
    ult = url.rstrip("/").rsplit("/", 1)[-1]
    if ult.startswith("MID"):                       # conferência de story publicada (GET do media_id)
        m = next((x for x in c["midias"] if x["id"] == ult), None)
        return R(200, {"id": ult, "timestamp": m["timestamp"] if m else _ts(FIXO)})
    if _n.get("consulta_falha") or CENARIO == "consulta_falha":   # consulta ao CONTEINER falhando
        return R(500, ERR_500)
    k = c["conteineres"].get(ult)
    if k is None:
        return R(400, {"error": {"message": "Unsupported get request", "type": "OAuthException", "code": 100,
                                 "error_subcode": 33}})
    st = k["status"]
    if st == "FINISHED" and FIXO - _de_ts(k["criado"]) > _dt.timedelta(hours=24):
        st = "EXPIRED"                              # a Meta expira conteiner NAO publicado em 24 h
    return R(200, {"status_code": st})
requests.post = fake_post
requests.get = fake_get

import publish
publish.dt = types.SimpleNamespace(datetime=FakeDT, timezone=_dt.timezone,
                                   timedelta=_dt.timedelta)
publish.time.sleep = lambda *a, **k: None
# mesmo veredito do __main__ do publish.py: falha registrada por _falhou = exit 1. Antes o stub
# descartava o retorno e todo "exit == 0" era cego a falha (auditoria 19/10).
_falhas = publish.main() or []
if _falhas:
    print("::error::FALHAS " + "; ".join(_falhas))
sys.exit(1 if _falhas else 0)
'''


def preparar(reels=None, publicados=None, last_reel=""):
    tmp = Path(tempfile.mkdtemp(prefix="igtest_"))
    for f in ["publish.py", "cfm_guardrails.py", "regra_reels.py", "checar_stories.py", "publicar_stories.py",
              "temas_conteudo.py", "publish_agenda.py", "legenda.py"]:
        shutil.copy(ROOT / f, tmp / f)
    (tmp / "posts.json").write_text(json.dumps(POSTS, ensure_ascii=False), encoding="utf-8")
    (tmp / "sequences.json").write_text(json.dumps(SEQS, ensure_ascii=False), encoding="utf-8")
    (tmp / "reels.json").write_text(json.dumps(REELS if reels is None else reels, ensure_ascii=False), encoding="utf-8")
    (tmp / "stories.json").write_text("[]", encoding="utf-8")
    (tmp / "destaques.json").write_text("[]", encoding="utf-8")
    (tmp / "state").mkdir(exist_ok=True)
    (tmp / "state" / "published.json").write_text(json.dumps(
        {"published": publicados or [], "last_post_date": "", "last_seq_date": "", "last_reel_date": last_reel}),
        encoding="utf-8")
    (tmp / "_stub.py").write_text(STUB, encoding="utf-8")
    return tmp


def rodar(cenario, tmp, force_id="", agora="", extra=None):
    env = dict(os.environ)
    env.pop("FAKE_NOW", None)
    env.pop("ROTULO_IA", None)
    env.pop("LAMINAS_POR_SEMANA", None)
    env.pop("DIAS_ENTRE_CONVERSAS", None)
    env.pop("CONVERSAS_ATIVAS", None)
    env.pop("POSTS_ATIVOS", None)
    env.pop("SEQUENCIAS_ATIVAS", None)
    # regime de 19/10 (lâmina 1/semana, conversa ligada) como base dos cenários de mecânica; o
    # cenário Q testa o padrão de produção (all-in, 24/10) tirando estas chaves com None
    base = {"LAMINAS_POR_SEMANA": "1", "CONVERSAS_ATIVAS": "on", "POSTS_ATIVOS": "on", "SEQUENCIAS_ATIVAS": "on"}
    for k, v in base.items():
        env[k] = v
    for k, v in (extra or {}).items():
        if v is None:
            env.pop(k, None)
    if agora:
        env["FAKE_NOW"] = agora
    env.update({"IG_USER_ID": "1784", "IG_ACCESS_TOKEN": "fake",
                "GITHUB_REPOSITORY": "rafaelvs/06_Automacao_Instagram",
                "FORCE_ID": force_id, "LOCATION_ID": "", "TRIAL_REELS": "false",
                "ALARME_CURTIDAS": "on", "ALARME_N_PECAS": "6",
                "PYTHONUTF8": "1", "PYTHONIOENCODING": "utf-8"})
    env.update({k: v for k, v in (extra or {}).items() if v is not None})
    # o filho escreve UTF-8 (PYTHONIOENCODING): decodificar pelo locale (cp1252 no Windows) estragava os acentos
    p = subprocess.run([sys.executable, str(tmp / "_stub.py"), cenario],
                       cwd=str(tmp), capture_output=True, text=True, env=env, encoding="utf-8", errors="replace")
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

print("\nD) erro COMUM (HTTP 500): NAO e' falha de auth; item que falha sem publicar deixa o job vermelho")
# Ate 19/10 este cenario afirmava "job verde" porque o stub descartava o retorno de main(); a
# producao sempre saiu com exit 1 aqui (o __main__ do publish.py), e e' o certo: o cron retenta e
# o vermelho avisa. O que este cenario protege: NAO tratar como token morto e nao marcar publicado.
tmp = preparar(); rc, out, st = rodar("erro_comum", tmp)
checa("exit == 1 (falha registrada, nao engolida)", rc == 1, f"exit={rc}")
checa("nao classificou como token morto", "AUTENTICACAO FALHOU" not in out, "sem alarme de token")
checa("nada publicado", ids(st) == [], f"publicados={ids(st)}")
shutil.rmtree(tmp, ignore_errors=True)

print("\nE) RATE LIMIT (OAuthException code 4) NAO e' falha de auth; job vermelho, item fica para o proximo cron")
tmp = preparar(); rc, out, st = rodar("rate", tmp)
checa("exit == 1 (falha registrada; o item fica para o proximo cron)", rc == 1, f"exit={rc}")
checa("nao classificou como token morto", "AUTENTICACAO FALHOU" not in out, "sem alarme de token")
checa("nada publicado", ids(st) == [], f"publicados={ids(st)}")
shutil.rmtree(tmp, ignore_errors=True)

print("\nG) COLLAB (B3, 12/09/2026): post com collaborators ENVIA o parametro; story NAO leva")
tmp = preparar(); rc, out, st = rodar("ok", tmp)
checa("collaborators no container do post", 'COLLAB_ENVIADO ["parceiro_a"] media_type= IMAGE' in out, "parametro JSON com o username")
checa("story sem collaborators (controle)", "media_type= STORIES" not in out, "sequencia publicou sem o parametro")
checa("exit == 0", rc == 0, f"exit={rc}")
shutil.rmtree(tmp, ignore_errors=True)

print("\nH) TRIAL POR PECA (B5): item['trial']=true publica em modo trial com TRIAL_REELS global OFF")
tmp = preparar(); rc, out, st = rodar("ok", tmp, force_id="t-reel-1")
checa("trial_params enviado", "TRIAL_PARAMS" in out and "SS_PERFORMANCE" in out, "graduation_strategy presente")
checa("state registra modo trial", any(e.get("modo_reel") == "trial" for e in st["published"]), f"published={st['published']}")
checa("exit == 0", rc == 0, f"exit={rc}")
shutil.rmtree(tmp, ignore_errors=True)

print("\nI) ALARME DE CURTIDAS (B6-iii): 6 ultimas pecas com ZERO curtidas = NAO publica, job vermelho")
tmp = preparar(); rc, out, st = rodar("alarme_zero", tmp)
checa("exit != 0", rc != 0, f"exit={rc}")
checa("nada publicado", ids(st) == [], f"publicados={ids(st)}")
checa("alarme gravado no state", "alarme_curtidas" in st, f"chaves={sorted(st)}")
checa("mensagem ::error::ALARME", "::error::ALARME" in out, "anotacao visivel no Actions")
shutil.rmtree(tmp, ignore_errors=True)
# controle negativo: com curtidas (cenario 'ok' devolve like_count=1) a publicacao seguiu — ver B/G.
# e o alarme NAO se aplica a FORCE_ID (decisao humana): cenario H publicou com like_count irrelevante.

CAP_IA = CAP + "\nNarração com voz digital (IA)."
R_LAMINA = {"id": "t-lamina-1", "video": "media/l1.mp4", "caption": CAP_IA}
R_LAMINA2 = {"id": "t-lamina-2", "video": "media/l2.mp4", "caption": CAP_IA}
R_CONVERSA = {"id": "t-conversa-1", "video": "media/c1.mp4", "caption": CAP_IA, "formato": "conversa"}
R_MUDO = {"id": "t-mudo-1", "video": "media/m1.mp4", "caption": CAP}          # sem voz sintetica
QUARTA_16H = "2026-07-29T19:00:00+00:00"                                       # qua 16:00 BRT: dia de reel
LAMINA_SEG = {"id": "t-lamina-0", "kind": "reel", "media_id": "M0", "at": "2026-07-27T18:30:00+00:00"}

print("\nJ) ROTULO DE IA (18/10/2026): reel com voz sintetica leva is_ai_generated=true; sem voz, nao")
tmp = preparar(reels=[R_LAMINA, R_MUDO]); rc, out, st = rodar("ok", tmp, force_id="t-lamina-1")
checa("rotulo enviado no conteiner do reel", "ROTULO_IA true media_type= REELS" in out, "is_ai_generated=true")
checa("state registra rotulo_ia=true", any(e.get("rotulo_ia") is True for e in st["published"]), f"published={st['published']}")
checa("exit == 0", rc == 0, f"exit={rc}")
shutil.rmtree(tmp, ignore_errors=True)
tmp = preparar(reels=[R_LAMINA, R_MUDO]); rc, out, st = rodar("ok", tmp, force_id="t-mudo-1")
checa("controle: reel SEM voz sintetica nao leva rotulo", "ROTULO_IA" not in out, "parametro ausente")
checa("controle: state registra rotulo_ia=false", any(e.get("rotulo_ia") is False for e in st["published"]), f"published={st['published']}")
shutil.rmtree(tmp, ignore_errors=True)
tmp = preparar(reels=[R_LAMINA]); rc, out, st = rodar("ok", tmp, force_id="t-lamina-1", extra={"ROTULO_IA": "off"})
checa("ROTULO_IA=off desliga (decisao humana)", "ROTULO_IA" not in out, "parametro ausente com a chave desligada")
shutil.rmtree(tmp, ignore_errors=True)
tmp = preparar(); rc, out, st = rodar("ok", tmp)
checa("controle: post (carrossel/imagem) NUNCA leva rotulo", "ROTULO_IA" not in out, "Meta isenta imagem")
shutil.rmtree(tmp, ignore_errors=True)

print("\nK) COTA DE LAMINAS (18/10/2026): lamina da semana ja saiu -> pula a lamina e publica o formato novo")
tmp = preparar(reels=[R_LAMINA, R_CONVERSA], publicados=[LAMINA_SEG]); rc, out, st = rodar("ok", tmp, agora=QUARTA_16H)
checa("publicou a CONVERSA, nao a lamina", "t-conversa-1" in ids(st) and "t-lamina-1" not in ids(st), f"publicados={ids(st)}")
checa("exit == 0", rc == 0, f"exit={rc}")
shutil.rmtree(tmp, ignore_errors=True)

print("\nL) COTA cumprida e NENHUMA peca nova pronta -> sem reel hoje, sem erro, sem 'esgotada'")
tmp = preparar(reels=[R_LAMINA, R_LAMINA2], publicados=[LAMINA_SEG]); rc, out, st = rodar("ok", tmp, agora=QUARTA_16H)
checa("nenhum reel publicado", "t-lamina-1" not in ids(st) and "t-lamina-2" not in ids(st), f"publicados={ids(st)}")
checa("mensagem de cota (nao 'esgotada')", "lamina: cota 1/semana" in out and "esgotada" not in out.split("REELS")[-1], "texto certo no log")
checa("exit == 0", rc == 0, f"exit={rc}")
checa("last_reel_date NAO avancou", st["last_reel_date"] == "", f"={st['last_reel_date']!r}")
sem_erro = "::error::" not in out
checa("sem ::error:: (dia sem reel nao e falha)", sem_erro, "log limpo")
shutil.rmtree(tmp, ignore_errors=True)

print("\nM) CONTROLE: cota livre (lamina so na semana anterior) -> a lamina da frente sai normalmente")
LAMINA_SEMANA_PASSADA = dict(LAMINA_SEG, at="2026-07-25T18:30:00+00:00")   # sabado da semana anterior
tmp = preparar(reels=[R_LAMINA, R_CONVERSA], publicados=[LAMINA_SEMANA_PASSADA]); rc, out, st = rodar("ok", tmp, agora=QUARTA_16H)
checa("publicou a lamina da frente da fila", "t-lamina-1" in ids(st), f"publicados={ids(st)}")
checa("exit == 0", rc == 0, f"exit={rc}")
shutil.rmtree(tmp, ignore_errors=True)
tmp = preparar(reels=[R_LAMINA, R_CONVERSA], publicados=[LAMINA_SEG]); rc, out, st = rodar("ok", tmp, agora=QUARTA_16H, extra={"LAMINAS_POR_SEMANA": "-1"})
checa("LAMINAS_POR_SEMANA=-1 desliga a cota", "t-lamina-1" in ids(st), f"publicados={ids(st)}")
shutil.rmtree(tmp, ignore_errors=True)

print("\nN) FORMATO NO REGISTRO (auditoria 19/10): a cota conta pelo que SAIU, nao pelo reels.json de hoje")
tmp = preparar(reels=[R_CONVERSA, R_LAMINA]); rc, out, st = rodar("ok", tmp, agora=QUARTA_16H)
reg = next((e for e in st["published"] if e["id"] == "t-conversa-1"), {})
checa("registro do reel grava formato", reg.get("formato") == "conversa", f"registro={reg}")
shutil.rmtree(tmp, ignore_errors=True)
CONVERSA_SEG = {"id": "t-conversa-0", "kind": "reel", "media_id": "M9", "at": "2026-07-27T18:30:00+00:00", "formato": "conversa"}
tmp = preparar(reels=[R_LAMINA], publicados=[CONVERSA_SEG]); rc, out, st = rodar("ok", tmp, agora=QUARTA_16H)
checa("peca nova ja publicada e fora da fila NAO conta como lamina", "t-lamina-1" in ids(st), f"publicados={ids(st)}")
shutil.rmtree(tmp, ignore_errors=True)

print("\nP) INTERVALO DE CONVERSA (19/10/2026, 'a cada 10 dias'): conversa ha menos de 10 dias -> pula, sai o COMO FUNCIONA")
R_CONVERSA2 = {"id": "t-conversa-2", "video": "media/c2.mp4", "caption": CAP_IA, "formato": "conversa"}
R_CF = {"id": "t-cf-1", "video": "media/f1.mp4", "caption": CAP_IA, "formato": "como_funciona"}
CONVERSA_SEG_P = {"id": "t-conversa-0", "kind": "reel", "media_id": "M8", "at": "2026-07-27T18:30:00+00:00", "formato": "conversa"}
tmp = preparar(reels=[R_CONVERSA2, R_CF], publicados=[CONVERSA_SEG_P]); rc, out, st = rodar("ok", tmp, agora=QUARTA_16H)
checa("publicou o COMO FUNCIONA, nao a 2a conversa da semana", "t-cf-1" in ids(st) and "t-conversa-2" not in ids(st), f"publicados={ids(st)}")
checa("exit == 0", rc == 0, f"exit={rc}")
shutil.rmtree(tmp, ignore_errors=True)
tmp = preparar(reels=[R_CONVERSA2], publicados=[CONVERSA_SEG_P]); rc, out, st = rodar("ok", tmp, agora=QUARTA_16H)
checa("so conversa na fila e cota cheia -> sem reel, sem erro", "t-conversa-2" not in ids(st) and rc == 0 and "::error::" not in out, f"exit={rc} publicados={ids(st)}")
checa("mensagem cita o intervalo", "conversa: so a cada 10 dias" in out, "texto no log")
shutil.rmtree(tmp, ignore_errors=True)
CONVERSA_7_DIAS = dict(CONVERSA_SEG_P, at="2026-07-22T18:30:00+00:00")    # quarta anterior: 7 dias
tmp = preparar(reels=[R_CONVERSA2, R_CF], publicados=[CONVERSA_7_DIAS]); rc, out, st = rodar("ok", tmp, agora=QUARTA_16H)
checa("conversa ha 7 dias (semana anterior) AINDA bloqueia", "t-conversa-2" not in ids(st) and "t-cf-1" in ids(st), f"publicados={ids(st)}")
shutil.rmtree(tmp, ignore_errors=True)
CONVERSA_10_DIAS = dict(CONVERSA_SEG_P, at="2026-07-19T18:30:00+00:00")   # domingo, 10 dias antes
tmp = preparar(reels=[R_CONVERSA2, R_CF], publicados=[CONVERSA_10_DIAS]); rc, out, st = rodar("ok", tmp, agora=QUARTA_16H)
checa("controle: conversa ha 10 dias -> a conversa da frente sai", "t-conversa-2" in ids(st), f"publicados={ids(st)}")
shutil.rmtree(tmp, ignore_errors=True)
tmp = preparar(reels=[R_CONVERSA2, R_CF], publicados=[CONVERSA_SEG_P]); rc, out, st = rodar("ok", tmp, agora=QUARTA_16H, extra={"DIAS_ENTRE_CONVERSAS": "-1"})
checa("DIAS_ENTRE_CONVERSAS=-1 desliga o intervalo", "t-conversa-2" in ids(st), f"publicados={ids(st)}")
shutil.rmtree(tmp, ignore_errors=True)

print("\nQ) ALL-IN (24/10/2026): padrao de producao = so COMO FUNCIONA (lamina e conversa suspensas)")
PROD = {"LAMINAS_POR_SEMANA": None, "CONVERSAS_ATIVAS": None}     # tira as chaves: vale o padrao do regra_reels
tmp = preparar(reels=[R_LAMINA, R_CONVERSA, R_CF]); rc, out, st = rodar("ok", tmp, agora=QUARTA_16H, extra=PROD)
checa("publicou o COMO FUNCIONA e nao a lamina nem a conversa da frente", ids(st) == ["t-cf-1"], f"publicados={ids(st)}")
checa("exit == 0", rc == 0, f"exit={rc}")
shutil.rmtree(tmp, ignore_errors=True)
tmp = preparar(reels=[R_LAMINA, R_CONVERSA]); rc, out, st = rodar("ok", tmp, agora=QUARTA_16H, extra=PROD)
checa("fila so com lamina e conversa -> sem reel, sem erro", ids(st) == [] and rc == 0 and "::error::" not in out, f"exit={rc} publicados={ids(st)}")
checa("log pede COMO FUNCIONA", "nenhum COMO FUNCIONA pronto" in out and "conversa: suspensa" in out, "texto no log")
shutil.rmtree(tmp, ignore_errors=True)
tmp = preparar(reels=[R_CONVERSA, R_CF]); rc, out, st = rodar("ok", tmp, agora=QUARTA_16H, extra={"LAMINAS_POR_SEMANA": None, "CONVERSAS_ATIVAS": "on"})
checa("controle: CONVERSAS_ATIVAS=on religa a conversa", ids(st) == ["t-conversa-1"], f"publicados={ids(st)}")
shutil.rmtree(tmp, ignore_errors=True)

print("\nR) ALL-IN EM TUDO (24/10/2026): padrao de producao = carrossel e sequencia antigos suspensos")
TUDO = {"POSTS_ATIVOS": None, "SEQUENCIAS_ATIVAS": None}
tmp = preparar(); rc, out, st = rodar("ok", tmp, extra=TUDO)              # terca 18h: abriria post e sequencia
checa("nada de carrossel nem sequencia antigos com o padrao", ids(st) == [] and rc == 0, f"exit={rc} publicados={ids(st)}")
checa("log diz que estao suspensos", "carrosseis estaticos): SUSPENSOS" in out and "Sequencias de stories antigas: SUSPENSAS" in out, "texto no log")
shutil.rmtree(tmp, ignore_errors=True)
tmp = preparar(); rc, out, st = rodar("ok", tmp, extra={"POSTS_ATIVOS": "on", "SEQUENCIAS_ATIVAS": None})
checa("controle: POSTS_ATIVOS=on religa o carrossel (sequencia segue suspensa)", "t-post-1" in ids(st) and len(ids(st)) == 1, f"publicados={ids(st)}")
shutil.rmtree(tmp, ignore_errors=True)

# ---------------------------------------------------------------- stories da geração nova
import hashlib, importlib.util
_spec = importlib.util.spec_from_file_location("checar_stories_t", ROOT / "checar_stories.py")
CS = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(CS)
TER_17 = "2026-11-17T16:00:00+00:00"                # terca 13:00 BRT (dia de story, sem reel)
SEG_16 = "2026-11-16T16:00:00+00:00"                # segunda (dia de reel, sem story)
ST = {"id": "stn_t", "reel_ref": "cf_pe_virado", "tema": "pe_virado", "angulo": "a", "variante": "B",
      "cta": "Manda pra quem tem filho pequeno.",
      "telas": [{"papel": "espanto", "titulo": ["A CRIANÇA ANDA", "COM O PÉ PRA DENTRO?"], "texto": "", "trecho": [0.6, 2.7], "crop": [0, 310, 645, 950]},
                {"papel": "mecanismo", "titulo": ["LEVES TORÇÕES", "DO CRESCIMENTO"], "texto": "Variações comuns.", "trecho": [4.6, 7.4], "crop": [290, 360, 790, 900]},
                {"papel": "significado", "titulo": ["A ROTAÇÃO COSTUMA", "SE AJUSTAR"], "texto": "Piora pede avaliação.", "trecho": [12.4, 14.6], "crop": [0, 210, 1080, 1055]}]}
STORY_OFF = {"POSTS_ATIVOS": "off", "SEQUENCIAS_ATIVAS": "off"}


def _sha(b):
    return "sha256:" + hashlib.sha256(b).hexdigest()


def preparar_story(aprovado=True, reel_em="2026-11-01T18:00:00+00:00", publicados_extra=None):
    tmp = preparar(reels=[{"id": "cf_pe_virado", "video": "reels/pv.mp4", "caption": CAP, "formato": "como_funciona",
                           "voz_ia": True}],
                   publicados=[{"id": "cf_pe_virado", "kind": "reel", "at": reel_em}] + (publicados_extra or []))
    (tmp / "story_cf.py").write_text("# gerador de teste\n", encoding="utf-8")
    (tmp / "reels").mkdir(exist_ok=True); (tmp / "reels" / "pv.mp4").write_bytes(b"reel")
    (tmp / "stories_cf").mkdir(exist_ok=True)
    partes = []
    for i, t in enumerate(ST["telas"]):
        arq = f"stories_cf/stn_t_{i + 1}.mp4"; (tmp / arq).write_bytes(b"parte%d" % i)
        des = list(t["titulo"]) + ([t["texto"]] if t["texto"] else []) + [CS.SIG, CS.DISC_ST, CS.SELO, CS.TOCA]
        if i == 2:
            des += [CS.PERFIL, CS.NOME, ST["cta"].upper()]
        partes.append({"arquivo": arq, "sha256": _sha(b"parte%d" % i), "dur": 6.0, "textos_tela": des,
                       "trecho": t["trecho"], "crop": t["crop"], "camera": CS.camera_de(t)})
    # o que o story_cf.py grava no irmão e o portão confere: hash_render (trecho/crop/câmera/tempos) e as
    # fontes do render do CI (Roboto)
    meta = {"id": "stn_t", "hash_story": CS.hash_story(ST), "hash_gerador": _sha(b"# gerador de teste\n"),
            "hash_render": CS.hash_render(ST), "reel_video": "reels/pv.mp4", "reel_sha256": _sha(b"reel"),
            "partes": partes, "fontes": {"black": "Roboto-Black.ttf", "bold": "Roboto-Bold.ttf",
                                         "semi": "Roboto-Medium.ttf", "reg": "Roboto-Regular.ttf"}}
    (tmp / "stories_cf" / "stn_t.json").write_text(json.dumps(meta, ensure_ascii=False), encoding="utf-8")
    (tmp / "stories_cf.json").write_text(json.dumps([ST], ensure_ascii=False), encoding="utf-8")
    lotes = [lote_story([entrada(tmp, "stn_t")])] if aprovado else []
    (tmp / "aprovacoes.json").write_text(json.dumps({"lotes": lotes}), encoding="utf-8")
    return tmp


def entrada(tmp, sid):
    """A entrada do lote exatamente como o Rafael a registra: `checar_stories.py --entrada <id>` (hash do texto +
    sha256 dos 3 vídeos + hash do gerador do render que ele viu). Entrada só de texto NÃO aprova (auditoria de
    fechamento, 25/10/2026): o fixture antigo gravava só o hash_roteiro e codificava a régua fraca."""
    velho = CS.usar_raiz(str(tmp))
    # o portão importa legenda/temas_conteudo/cfm_guardrails na hora: arneses que reaproveitam este fixture de OUTRA
    # pasta (lab/revisao_infra) não têm o repo no sys.path — sem isto o portão falha fechado e o fixture não nasce
    sys.path.insert(0, str(tmp))
    try:
        ent, erros = CS.entrada_de_aprovacao(sid)
    finally:
        sys.path.remove(str(tmp))
        CS.usar_raiz(velho)
    assert ent is not None, f"fixture: entrada_de_aprovacao({sid}) recusou o render de teste: {erros}"
    return ent


def lote_story(eps):
    """Lote VÁLIDO (o do portão clínico checar_aprovacoes e do checar_carrossel): status 'aprovado' com autor e evidência."""
    return {"lote": "T", "escopo": ["instagram-stories"], "status": "aprovado", "aprovado_por": "Rafael (fixture do teste)",
            "evidencia": "fixture do test_publicacao — aprovação simulada, nunca publicar", "episodios": eps}


def ids_story(st):
    return [e["id"] for e in st["published"] if e.get("kind", "").startswith("story_nova")]


def conta(tmp):
    """A conta da Meta do STUB (persistida entre runs): o que FOI AO AR, não o que o estado diz."""
    p = tmp / "_conta_meta.json"
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else {"n_cont": 0, "conteineres": {}, "midias": []}


def no_ar(tmp, tipo="STORIES"):
    return [m for m in conta(tmp)["midias"] if m["media_type"] == tipo]


def reg_de(st, rid):
    return next((e for e in st["published"] if e.get("id") == rid), {})


TER_1330 = "2026-11-17T16:30:00+00:00"              # terca 13:30 BRT (cron seguinte)
TRES = ["stn_t#0", "stn_t#1", "stn_t#2"]


print("\nS1) STORY DA GERAÇÃO NOVA aprovada, tema longe: sai inteira (3 partes) e grava a data")
tmp = preparar_story(); rc, out, st = rodar("ok", tmp, agora=TER_17, extra=STORY_OFF)
checa("3 partes publicadas na ordem", ids_story(st) == ["stn_t#0", "stn_t#1", "stn_t#2"], f"{ids_story(st)} | {out[-300:]}")
checa("gravou last_story_nova_date", st.get("last_story_nova_date") == "2026-11-17", f"={st.get('last_story_nova_date')!r}")
checa("exit == 0", rc == 0, f"exit={rc}")
checa("na CONTA: 3 stories", len(no_ar(tmp)) == 3, f"{no_ar(tmp)}")
checa("cada parte registra o sha256 do vídeo (a retomada confere o render)", [reg_de(st, i).get("sha256") for i in TRES]
      == [p["sha256"] for p in json.loads((tmp / "stories_cf" / "stn_t.json").read_text(encoding="utf-8"))["partes"]], "sha256")
checa("CONTROLE da URL: pasta sem git = raw URL pelo nome do branch",
      "MIDIA_URL https://raw.githubusercontent.com/rafaelvs/06_Automacao_Instagram/main/stories_cf/stn_t_1.mp4" in out, out[-400:])
shutil.rmtree(tmp, ignore_errors=True)

print("\nS2) story SEM aprovação do Rafael: não sai, sem erro (aviso)")
tmp = preparar_story(aprovado=False); rc, out, st = rodar("ok", tmp, agora=TER_17, extra=STORY_OFF)
checa("nada publicado", ids_story(st) == [], f"{ids_story(st)}")
checa("exit == 0 e aviso de aprovação", rc == 0 and "aguardando aprova" in out, f"exit={rc}")
shutil.rmtree(tmp, ignore_errors=True)

print("\nS3) DISTÂNCIA DE TEMA (Rafael, 24/10): reel do mesmo tema saiu há 2 dias -> story não sai")
tmp = preparar_story(reel_em="2026-11-15T18:00:00+00:00"); rc, out, st = rodar("ok", tmp, agora=TER_17, extra=STORY_OFF)
checa("nada publicado", ids_story(st) == [], f"{ids_story(st)}")
checa("log explica o bloqueio pelo tema", "bloqueios" in out and "pe_virado" in out, out[-300:])
checa("exit == 0", rc == 0, f"exit={rc}")
shutil.rmtree(tmp, ignore_errors=True)

print("\nS4) 500 REAL da Meta (OAuthException code 2, is_transient) na 2a parte e contêiner NÃO publicado: 1a parte "
      "gravada, job vermelho, retomada sem duplicar e pelo MESMO contêiner")
tmp = preparar_story(); rc, out, st = rodar("story_500_nao", tmp, agora=TER_17, extra=STORY_OFF)
checa("só a 1a parte gravada", ids_story(st) == ["stn_t#0"], f"{ids_story(st)}")
checa("exit == 1", rc == 1, f"exit={rc}")
checa("o 500 transitório NÃO virou 'token morto'", "AUTENTICACAO FALHOU" not in out, out[-300:])
wa = st.get("story_nova_publicando") or {}
checa("write-ahead da parte 2 fica no estado (contêiner FINISHED: o próximo run pergunta de novo)",
      wa.get("parte") == 1 and wa.get("container"), f"{wa}")
rc, out, st = rodar("ok", tmp, agora=TER_1330, extra=STORY_OFF)
checa("retomada publica só as partes 2 e 3", ids_story(st) == TRES, f"{ids_story(st)}")
checa("retomada exit == 0", rc == 0, f"exit={rc} {out[-300:]}")
checa("a parte 2 saiu pelo MESMO contêiner do write-ahead (não se criou outro)",
      reg_de(st, "stn_t#1").get("container") == wa.get("container"), f"{reg_de(st, 'stn_t#1')}")
checa("na CONTA: 3 stories, nenhuma parte 2x", len(no_ar(tmp)) == 3, f"{no_ar(tmp)}")
checa("write-ahead resolvido (sai do estado)", "story_nova_publicando" not in st, f"{st.get('story_nova_publicando')}")
shutil.rmtree(tmp, ignore_errors=True)

print("\nS5) 500 REAL na 2a parte mas o contêiner ficou PUBLISHED (a Meta entregou): conta como saiu")
tmp = preparar_story(); rc, out, st = rodar("story_500_saiu", tmp, agora=TER_17, extra=STORY_OFF)
checa("3 partes gravadas", ids_story(st) == ["stn_t#0", "stn_t#1", "stn_t#2"], f"{ids_story(st)} | {out[-300:]}")
checa("a 2a marcada como confirmada pelo contêiner", any(e.get("confirmado_por") for e in st["published"] if e["id"] == "stn_t#1"), "confirmado_por")
checa("exit == 0", rc == 0, f"exit={rc}")
checa("na CONTA: 3 stories", len(no_ar(tmp)) == 3, f"{no_ar(tmp)}")
shutil.rmtree(tmp, ignore_errors=True)

print("\nS6) vídeo trocado depois do render: portão barra, nada sai, job vermelho")
tmp = preparar_story(); (tmp / "stories_cf" / "stn_t_2.mp4").write_bytes(b"outro")
rc, out, st = rodar("ok", tmp, agora=TER_17, extra=STORY_OFF)
checa("nada publicado", ids_story(st) == [], f"{ids_story(st)}")
checa("exit == 1 com BLOQUEADA", rc == 1 and "BLOQUEADA" in out, f"exit={rc}")
shutil.rmtree(tmp, ignore_errors=True)

print("\nS7) parte INCERTA no estado: nenhuma story sai até conferência humana")
tmp = preparar_story(publicados_extra=[{"id": "stn_z#1", "kind": "story_nova_incerta", "story": "stn_z", "parte": 1,
                                        "media_id": None, "at": "2026-11-14T16:00:00+00:00"}])
rc, out, st = rodar("ok", tmp, agora=TER_17, extra=STORY_OFF)
checa("nada publicado", ids_story(st) == ["stn_z#1"], f"{ids_story(st)}")
checa("exit == 1 com INCERTA", rc == 1 and "INCERTA" in out, f"exit={rc}")
shutil.rmtree(tmp, ignore_errors=True)

print("\nS8) FORCE_ID=story:stn_t numa segunda (decisão humana): publica, portão continua valendo")
tmp = preparar_story(reel_em="2026-11-14T18:00:00+00:00"); rc, out, st = rodar("ok", tmp, force_id="story:stn_t", agora=SEG_16, extra=STORY_OFF)
checa("3 partes publicadas", ids_story(st) == ["stn_t#0", "stn_t#1", "stn_t#2"], f"{ids_story(st)} | {out[-300:]}")
checa("exit == 0", rc == 0, f"exit={rc}")
shutil.rmtree(tmp, ignore_errors=True)

# ---------------------------------------------------------------- publicador (auditoria adversarial de 24/10/2026)
print("\nS9) story_500_oauth: HTTP 500 transitório REAL no media_publish da 2a parte e a Meta PUBLICOU — UMA publicação da parte 2")
tmp = preparar_story(); rc, out, st = rodar("story_500_oauth", tmp, agora=TER_17, extra=STORY_OFF)
c2 = reg_de(st, "stn_t#1").get("container")
checa("sem alarme falso de token", "AUTENTICACAO FALHOU" not in out, out[-300:])
checa("a parte 2 registrada como saiu (confirmada pelo contêiner) e a story completa", rc == 0 and ids_story(st) == TRES
      and reg_de(st, "stn_t#1").get("confirmado_por"), f"exit={rc} {ids_story(st)} {out[-300:]}")
rc, out, st = rodar("ok", tmp, agora=TER_1330, extra=STORY_OFF)
parte2 = [m for m in no_ar(tmp) if m["container"] == c2]
checa("UMA publicação da parte 2 na conta (e 3 stories no total, mesmo com o cron seguinte)",
      c2 and len(parte2) == 1 and len(no_ar(tmp)) == 3 and rc == 0, f"parte2={parte2} conta={no_ar(tmp)}")
shutil.rmtree(tmp, ignore_errors=True)

print("\nS10) REEL com o 500 transitório REAL no media_publish e a Meta PUBLICOU (pré-existente): publicado UMA vez")
tmp = preparar(reels=[R_CF]); rc, out, st = rodar("reel_500_oauth", tmp, agora=QUARTA_16H, extra=STORY_OFF)
checa("sem alarme falso de token", "AUTENTICACAO FALHOU" not in out, out[-300:])
checa("reel registrado como publicado (confirmado pelo contêiner) e o dia marcado",
      reg_de(st, "t-cf-1").get("confirmado_por") and st["last_reel_date"] == "2026-07-29" and rc == 0, f"exit={rc} {st['published']}")
rc, out, st = rodar("ok", tmp, agora="2026-07-29T19:30:00+00:00", extra=STORY_OFF)
checa("o cron seguinte NÃO republica: 1 reel na conta", len(no_ar(tmp, "REELS")) == 1, f"{no_ar(tmp, 'REELS')}")
shutil.rmtree(tmp, ignore_errors=True)

print("\nS11) erro FATAL (token) no media_publish da 2a parte com o contêiner PUBLISHED: a parte é registrada ANTES de subir o erro")
tmp = preparar_story(); rc, out, st = rodar("auth_no_publish_saiu", tmp, agora=TER_17, extra=STORY_OFF)
checa("job vermelho com o alarme de token", rc == 1 and "AUTENTICACAO FALHOU" in out, f"exit={rc}")
checa("partes 1 e 2 registradas (a 2 confirmada pelo contêiner)", ids_story(st) == ["stn_t#0", "stn_t#1"]
      and reg_de(st, "stn_t#1").get("confirmado_por"), f"{ids_story(st)}")
rc, out, st = rodar("ok", tmp, agora=TER_1330, extra=STORY_OFF)
checa("token renovado: retomada publica só a parte 3 (3 stories na conta)", ids_story(st) == TRES and len(no_ar(tmp)) == 3
      and rc == 0, f"exit={rc} {ids_story(st)} {no_ar(tmp)}")
shutil.rmtree(tmp, ignore_errors=True)

print("\nS12) token morre no media_publish da 2a parte e a consulta ao contêiner também falha: INCERTA registrada antes de subir")
tmp = preparar_story(); rc, out, st = rodar("auth_mid", tmp, agora=TER_17, extra=STORY_OFF)
checa("job vermelho com o alarme de token", rc == 1 and "AUTENTICACAO FALHOU" in out, f"exit={rc}")
checa("parte 2 registrada como INCERTA (não como 'não saiu')", [e["kind"] for e in st["published"] if e.get("story") == "stn_t"]
      == ["story_nova", "story_nova_incerta"], f"{st['published']}")
rc, out, st = rodar("ok", tmp, agora=TER_1330, extra=STORY_OFF)
checa("token renovado: nada sai até a conferência humana (1 story na conta)", rc == 1 and "INCERTA" in out
      and len(no_ar(tmp)) == 1, f"exit={rc} {no_ar(tmp)}")
shutil.rmtree(tmp, ignore_errors=True)

print("\nS13) WRITE-AHEAD: job morto DENTRO do media_publish da 2a parte, com a parte no ar: o run seguinte pergunta ao contêiner")
tmp = preparar_story(); rc, out, st = rodar("morre_no_publish", tmp, agora=TER_17, extra=STORY_OFF)
wa = st.get("story_nova_publicando") or {}
checa("job morto com o write-ahead da parte 2 já em disco", rc != 0 and ids_story(st) == ["stn_t#0"] and wa.get("parte") == 1
      and wa.get("container"), f"exit={rc} {ids_story(st)} {wa}")
rc, out, st = rodar("ok", tmp, agora=TER_1330, extra=STORY_OFF)
checa("o run seguinte registra a parte 2 pelo contêiner (PUBLISHED) e publica só a 3", ids_story(st) == TRES
      and "write-ahead" in str(reg_de(st, "stn_t#1").get("confirmado_por")), f"{ids_story(st)} {out[-300:]}")
checa("na CONTA: 3 stories, a parte 2 UMA vez", len(no_ar(tmp)) == 3
      and len([m for m in no_ar(tmp) if m["container"] == wa.get("container")]) == 1, f"{no_ar(tmp)}")
checa("exit == 0 e o dia marcado", rc == 0 and st.get("last_story_nova_date") == "2026-11-17", f"exit={rc}")
shutil.rmtree(tmp, ignore_errors=True)
tmp = preparar_story(); rc, out, st = rodar("morre_antes_do_publish", tmp, agora=TER_17, extra=STORY_OFF)
wa = st.get("story_nova_publicando") or {}; n1 = conta(tmp)["n_cont"]
rc, out, st = rodar("ok", tmp, agora=TER_1330, extra=STORY_OFF)
checa("job morto sem a parte no ar: o contêiner FINISHED do write-ahead é REAPROVEITADO (1 contêiner novo, o da parte 3)",
      rc == 0 and ids_story(st) == TRES and reg_de(st, "stn_t#1").get("container") == wa.get("container")
      and conta(tmp)["n_cont"] - n1 == 1 and len(no_ar(tmp)) == 3, f"exit={rc} {ids_story(st)} n_cont {n1}->{conta(tmp)['n_cont']}")
shutil.rmtree(tmp, ignore_errors=True)

print("\nS14) 500 na 2a parte com o contêiner FINISHED na hora e a Meta ENTREGANDO depois: o cron seguinte não republica")
tmp = preparar_story(); rc, out, st = rodar("story_500_tarde", tmp, agora=TER_17, extra=STORY_OFF)
checa("1a parte gravada e job vermelho", ids_story(st) == ["stn_t#0"] and rc == 1, f"exit={rc} {ids_story(st)}")
rc, out, st = rodar("ok", tmp, agora=TER_1330, extra=STORY_OFF)
checa("o run seguinte vê PUBLISHED pelo write-ahead e publica só a parte 3 (3 stories na conta)",
      "NO_AR_TARDE" in out and ids_story(st) == TRES and len(no_ar(tmp)) == 3 and rc == 0, f"exit={rc} {no_ar(tmp)}")
shutil.rmtree(tmp, ignore_errors=True)

print("\nS15) dois runs a partir da MESMA cópia do estado (checkout de SHA velho, P0-3 da v1.6): o 2º confere a conta e NÃO publica")
tmp = preparar_story()
velho = (tmp / "state" / "published.json").read_text(encoding="utf-8")
rc, out, st = rodar("ok", tmp, agora="2026-11-17T15:30:07+00:00", extra=STORY_OFF)
checa("run A (12:30:07) publica as 3 partes", ids_story(st) == TRES and rc == 0, f"exit={rc} {ids_story(st)}")
(tmp / "state" / "published.json").write_text(velho, encoding="utf-8")
rc, out, st = rodar("ok", tmp, agora="2026-11-17T15:41:00+00:00", extra=STORY_OFF)
checa("run B (12:41, estado de antes do push de A): exit 1 e NADA publicado (3 stories na conta)",
      rc == 1 and ids_story(st) == [] and len(no_ar(tmp)) == 3, f"exit={rc} {no_ar(tmp)}")
checa("  ...e diz por quê (story de hoje que o estado não conhece)", "NAO conhece" in out, out[-400:])
shutil.rmtree(tmp, ignore_errors=True)
tmp = preparar_story()
(tmp / "_conta_meta.json").write_text(json.dumps({"n_cont": 0, "n_mid": 900, "conteineres": {}, "midias": [
    {"id": "MANUAL1", "timestamp": "2026-11-17T13:00:00+0000", "media_type": "STORIES", "container": None}]}), encoding="utf-8")
rc, out, st = rodar("ok", tmp, agora=TER_17, extra=STORY_OFF)
checa("CONTROLE: story manual das 10:00 não bloqueia (a conferência olha a partir das 12:30)", ids_story(st) == TRES and rc == 0,
      f"exit={rc} {out[-300:]}")
shutil.rmtree(tmp, ignore_errors=True)
tmp = preparar_story(); rc, out, st = rodar("stories_falha", tmp, agora=TER_17, extra=STORY_OFF)
checa("GET /stories falhando: nada publicado e job vermelho (guarda cega não libera)", ids_story(st) == [] and rc == 1
      and len(no_ar(tmp)) == 0 and conta(tmp)["n_cont"] == 0, f"exit={rc} {out[-300:]}")
shutil.rmtree(tmp, ignore_errors=True)


def segunda_story(tmp, aprovar_b=True, aprovar_t=False):
    """stn_b (tema alongamento, reel em 02/11) ao lado da stn_t (pe_virado, reel em 01/11: tema MAIS ANTIGO)."""
    B = json.loads(json.dumps(ST)); B["id"] = "stn_b"; B["reel_ref"] = "cf_alongamento"; B["tema"] = "alongamento"
    (tmp / "reels" / "al.mp4").write_bytes(b"reel2")
    rs = json.loads((tmp / "reels.json").read_text(encoding="utf-8"))
    rs.append({"id": "cf_alongamento", "video": "reels/al.mp4", "caption": CAP, "formato": "como_funciona", "voz_ia": True})
    (tmp / "reels.json").write_text(json.dumps(rs, ensure_ascii=False), encoding="utf-8")
    est = json.loads((tmp / "state" / "published.json").read_text(encoding="utf-8"))
    est["published"].append({"id": "cf_alongamento", "kind": "reel", "at": "2026-11-02T18:00:00+00:00"})
    (tmp / "state" / "published.json").write_text(json.dumps(est), encoding="utf-8")
    meta = json.loads((tmp / "stories_cf" / "stn_t.json").read_text(encoding="utf-8"))
    ps = []
    for i, p in enumerate(meta["partes"]):
        arq = f"stories_cf/stn_b_{i + 1}.mp4"; (tmp / arq).write_bytes(b"b%d" % i)
        ps.append(dict(p, arquivo=arq, sha256=_sha(b"b%d" % i)))
    meta.update(id="stn_b", hash_story=CS.hash_story(B), reel_video="reels/al.mp4", reel_sha256=_sha(b"reel2"), partes=ps)
    (tmp / "stories_cf" / "stn_b.json").write_text(json.dumps(meta, ensure_ascii=False), encoding="utf-8")
    (tmp / "stories_cf.json").write_text(json.dumps([ST, B], ensure_ascii=False), encoding="utf-8")
    eps = ([entrada(tmp, "stn_b")] if aprovar_b else []) + ([entrada(tmp, "stn_t")] if aprovar_t else [])
    (tmp / "aprovacoes.json").write_text(json.dumps({"lotes": [lote_story(eps)]}), encoding="utf-8")


PROJ = r'''
import json, sys, datetime as dt, publish_agenda as PA
st = json.load(open("state/published.json", encoding="utf-8"))
fila = json.load(open("stories_cf.json", encoding="utf-8"))
base = dt.date.fromisoformat(sys.argv[1])
r = PA.projeta_stories(fila, st["published"], [], base, st.get("last_story_nova_date") == base.isoformat(),
                       aprovacoes=json.load(open("aprovacoes.json", encoding="utf-8")),
                       reels_por_id={x["id"]: x for x in json.load(open("reels.json", encoding="utf-8"))})
print(json.dumps([[d.isoformat(), i] for d, i in r][:3]))
'''


def pagina(tmp, base):
    env = {k: v for k, v in os.environ.items() if k not in ("DIAS_ENTRE_MESMO_TEMA", "STORIES_NOVOS_ATIVOS")}
    env.update({"PYTHONUTF8": "1", "PYTHONIOENCODING": "utf-8"})
    p = subprocess.run([sys.executable, "-c", PROJ, base], cwd=str(tmp), capture_output=True, text=True, env=env,
                       encoding="utf-8", errors="replace")
    try:
        return json.loads(p.stdout.strip().splitlines()[-1])
    except (ValueError, IndexError):
        return f"ERRO {p.returncode}: {p.stderr[-300:]}"


print("\nS16) FILA: story PENDENTE com o tema mais antigo NÃO trava a APROVADA (e a página diz o mesmo que o robô)")
tmp = preparar_story(aprovado=False); segunda_story(tmp)
proj = pagina(tmp, "2026-11-17")
rc, out, st = rodar("ok", tmp, agora=TER_17, extra=STORY_OFF)
checa("a aprovada (stn_b) sai inteira; a pendente (stn_t) não", ids_story(st) == ["stn_b#0", "stn_b#1", "stn_b#2"] and rc == 0,
      f"exit={rc} {ids_story(st)} {out[-300:]}")
checa("  ...com aviso nomeando a pendente", "::warning::stn_t: aguardando aprovação" in out, out[-500:])
checa("a página (publish_agenda.projeta_stories) projeta o MESMO dia e a MESMA story", isinstance(proj, list) and proj[:1]
      == [["2026-11-17", "stn_b"]], f"{proj}")
shutil.rmtree(tmp, ignore_errors=True)
tmp = preparar_story(aprovado=False); segunda_story(tmp, aprovar_b=True, aprovar_t=True)
rc, out, st = rodar("ok", tmp, agora=TER_17, extra=STORY_OFF)
checa("CONTROLE: as duas aprovadas -> sai a do tema mais antigo (stn_t)", ids_story(st) == TRES, f"{ids_story(st)}")
shutil.rmtree(tmp, ignore_errors=True)

tmp = preparar_story(aprovado=False); segunda_story(tmp)
_fila = json.loads((tmp / "stories_cf.json").read_text(encoding="utf-8"))
_fila[0]["cta"] = "Manda pra quem quer agendar consulta."          # chamada de agendamento: erro de CONTEÚDO (CFM)
(tmp / "stories_cf.json").write_text(json.dumps(_fila, ensure_ascii=False), encoding="utf-8")
rc, out, st = rodar("ok", tmp, agora=TER_17, extra=STORY_OFF)
checa("pendente com erro de CONTEÚDO na fila: a aprovada sai mesmo assim e o job fica VERMELHO nomeando a pendente",
      ids_story(st) == ["stn_b#0", "stn_b#1", "stn_b#2"] and rc == 1 and "FALHA story stn_t (fila, portão)" in out,
      f"exit={rc} {ids_story(st)} {out[-400:]}")
shutil.rmtree(tmp, ignore_errors=True)

print("\nS17) RETOMADA de outro dia: parte 1 na terça, nada na quinta (a parte 1 já expirou no Instagram) — job vermelho")
tmp = preparar_story(); rc, out, st = rodar("story_500_nao", tmp, agora=TER_17, extra=STORY_OFF)
rc, out, st = rodar("ok", tmp, agora="2026-11-19T16:00:00+00:00", extra=STORY_OFF)
checa("partes 2 e 3 NÃO saem 2 dias depois da 1", ids_story(st) == ["stn_t#0"] and rc == 1 and len(no_ar(tmp)) == 1,
      f"exit={rc} {ids_story(st)} {no_ar(tmp)}")
checa("  ...e o log pede decisão (a parte 1 expirou)", "expirou" in out, out[-400:])
checa("  ...e a vaga de quinta NÃO é gasta", st.get("last_story_nova_date") in (None, ""), f"{st.get('last_story_nova_date')}")
shutil.rmtree(tmp, ignore_errors=True)

print("\nS18) FORCE_ID=story:<id> de story JÁ publicada inteira: job vermelho, nada sai, o dia NÃO é marcado")
tmp = preparar_story(); rc, out, st = rodar("ok", tmp, agora=TER_17, extra=STORY_OFF)
rc, out, st = rodar("ok", tmp, force_id="story:stn_t", agora="2026-11-19T14:00:00+00:00", extra=STORY_OFF)
checa("exit 1 com 'já publicada', nada novo na conta", rc == 1 and "já publicada" in out and len(no_ar(tmp)) == 3,
      f"exit={rc} {out[-300:]}")
checa("last_story_nova_date continua o da terça (a story agendada da quinta segue possível)",
      st.get("last_story_nova_date") == "2026-11-17", f"{st.get('last_story_nova_date')}")
shutil.rmtree(tmp, ignore_errors=True)

print("\nS19) FORCE_ID=story:<id> de story NÃO aprovada: job vermelho, nada sai")
tmp = preparar_story(aprovado=False, reel_em="2026-11-14T18:00:00+00:00")
rc, out, st = rodar("ok", tmp, force_id="story:stn_t", agora=SEG_16, extra=STORY_OFF)
checa("exit 1, nada publicado, motivo: aprovação", rc == 1 and ids_story(st) == [] and len(no_ar(tmp)) == 0
      and "story só sai APROVADA" in out, f"exit={rc} {out[-300:]}")
shutil.rmtree(tmp, ignore_errors=True)

print("\nS20) reel de origem ONTEM com a distância de tema desligada: a regra dos 2 dias segura a story")
tmp = preparar_story(reel_em="2026-11-16T18:00:00+00:00")
rc, out, st = rodar("ok", tmp, agora=TER_17, extra=dict(STORY_OFF, DIAS_ENTRE_MESMO_TEMA="off"))
checa("nada publicado 1 dia depois do reel", ids_story(st) == [] and rc == 0, f"exit={rc} {ids_story(st)}")
shutil.rmtree(tmp, ignore_errors=True)
tmp = preparar_story(reel_em="2026-11-15T18:00:00+00:00")
rc, out, st = rodar("ok", tmp, agora=TER_17, extra=dict(STORY_OFF, DIAS_ENTRE_MESMO_TEMA="off"))
checa("CONTROLE: reel há 2 dias -> sai", ids_story(st) == TRES and rc == 0, f"exit={rc} {ids_story(st)}")
shutil.rmtree(tmp, ignore_errors=True)

print("\nS21) RAW URL das mídias (story, post, reel) com o SHA do commit do checkout, não com o nome do branch")
tmp = preparar_story()
def _git(*a):
    return subprocess.run(["git", "-C", str(tmp)] + list(a), capture_output=True, text=True)
_git("init", "-q"); _git("add", "-A"); _git("-c", "user.name=teste", "-c", "user.email=teste@teste", "commit", "-q", "-m", "x")
sha = _git("rev-parse", "HEAD").stdout.strip()
URL = f"https://raw.githubusercontent.com/rafaelvs/06_Automacao_Instagram/{sha}/"
rc, out, st = rodar("ok", tmp, agora=TER_17, extra=STORY_OFF)
urls = [l.split(" ", 1)[1] for l in out.splitlines() if l.startswith("MIDIA_URL ")]
checa("story: as 3 partes pela URL do commit", len(sha) == 40 and urls == [URL + f"stories_cf/stn_t_{i}.mp4" for i in (1, 2, 3)],
      f"sha={sha!r} {urls}")
rc, out, st = rodar("ok", tmp, force_id="t-post-1", agora=TER_17, extra=STORY_OFF)
checa("post: imagem pela URL do commit", "MIDIA_URL " + URL + "media/a.png" in out, out[-300:])
rc, out, st = rodar("ok", tmp, force_id="cf_pe_virado", agora=TER_17, extra=STORY_OFF)
checa("reel: vídeo pela URL do commit", "MIDIA_URL " + URL + "reels/pv.mp4" in out, out[-300:])
shutil.rmtree(tmp, ignore_errors=True)

print("\nS24) REEL e POST com o media_publish em erro e a CONSULTA ao contêiner também falhando: INCERTO, não republica, "
      "vermelho até conferir")
tmp = preparar(reels=[R_CF]); rc, out, st = rodar("publish_500_incerto", tmp, agora=QUARTA_16H, extra=STORY_OFF)
checa("reel registrado como 'reel_incerto' e job vermelho", [e["kind"] for e in st["published"]] == ["reel_incerto"] and rc == 1
      and st["last_reel_date"] == "2026-07-29", f"exit={rc} {st['published']}")
checa("  ...o registro incerto guarda o contêiner e o write-ahead sai do estado", st["published"][0].get("container")
      and "reel_publicando" not in st, f"{st}")
rc, out, st = rodar("ok", tmp, agora="2026-07-31T19:00:00+00:00", extra=STORY_OFF)
checa("próximo dia de reel (sex): o reel incerto NÃO é republicado (1 reel na conta) e o job segue vermelho até a conferência",
      len(no_ar(tmp, "REELS")) == 1 and rc == 1 and "publicacao INCERTA" in out, f"exit={rc} {no_ar(tmp, 'REELS')}")
shutil.rmtree(tmp, ignore_errors=True)
tmp = preparar(reels=[R_CF]); rc, out, st = rodar("reel_nao_pronto", tmp, agora=QUARTA_16H, extra=STORY_OFF)
checa("CONTROLE: recusa 'não pronto' (9007/2207027) com o contêiner IN_PROGRESS = falha comum, NÃO incerto",
      st["published"] == [] and rc == 1 and "publicacao INCERTA" not in out and st["last_reel_date"] == "", f"exit={rc} {st['published']}")
rc, out, st = rodar("ok", tmp, agora="2026-07-31T19:00:00+00:00", extra=STORY_OFF)
checa("  ...e o próximo dia de reel publica a peça (ela continuou na fila)", ids(st) == ["t-cf-1"] and rc == 0
      and len(no_ar(tmp, "REELS")) == 1, f"exit={rc} {ids(st)}")
shutil.rmtree(tmp, ignore_errors=True)
tmp = preparar(); rc, out, st = rodar("publish_500_incerto", tmp, extra={"POSTS_ATIVOS": "on", "SEQUENCIAS_ATIVAS": "off"})
checa("post: registrado como 'post_incerto' (fora da fila) e job vermelho", any(e["kind"] == "post_incerto" for e in st["published"])
      and rc == 1, f"exit={rc} {st['published']}")
rc, out, st = rodar("ok", tmp, agora="2026-07-30T21:00:00+00:00", extra={"POSTS_ATIVOS": "on", "SEQUENCIAS_ATIVAS": "off"})
checa("  ...e não é republicado (1 imagem na conta)", len(no_ar(tmp, "IMAGE")) == 1 and rc == 1, f"exit={rc} {no_ar(tmp, 'IMAGE')}")
shutil.rmtree(tmp, ignore_errors=True)

print("\nS25) SEQUÊNCIA antiga e story nova no mesmo dia: os 5 frames vão ao estado e a conferência da conta os reconhece")
tmp = preparar_story(); rc, out, st = rodar("ok", tmp, agora=TER_17, extra={"POSTS_ATIVOS": "off", "SEQUENCIAS_ATIVAS": "on"})
checa("sequência (5 frames) e as 3 partes da story saem; job verde", "t-seq-1" in ids(st) and ids_story(st) == TRES and rc == 0
      and len(no_ar(tmp)) == 8, f"exit={rc} {ids(st)} {out[-300:]}")
checa("o registro da sequência guarda os 5 media_ids", len(reg_de(st, "t-seq-1").get("media_ids") or []) == 5, f"{reg_de(st, 't-seq-1')}")
shutil.rmtree(tmp, ignore_errors=True)

# ---------------------------------------------------------------- fechamento da auditoria (25/10/2026)
QUARTA_1630 = "2026-07-29T19:30:00+00:00"            # cron seguinte (qua 16:30 BRT)
QUARTA_17H = "2026-07-29T20:00:00+00:00"
SEXTA_16H = "2026-07-31T19:00:00+00:00"              # próximo dia de reel (contêiner de quarta já EXPIRED: 24 h)

print("\nS26) REEL: 500 no media_publish com o contêiner FINISHED e a Meta ENTREGANDO depois — o cron seguinte NÃO cria outro")
tmp = preparar(reels=[R_CF]); rc, out, st = rodar("reel_500_tarde", tmp, agora=QUARTA_16H, extra=STORY_OFF)
wa = st.get("reel_publicando") or {}
checa("run 1: job vermelho, reel fora do registro e o write-ahead (contêiner) no estado", rc == 1 and ids(st) == []
      and wa.get("id") == "t-cf-1" and wa.get("container"), f"exit={rc} {ids(st)} {wa}")
rc, out, st = rodar("ok", tmp, agora=QUARTA_1630, extra=STORY_OFF)
checa("run 2: a Meta entregou depois — o write-ahead registra o reel pelo contêiner e NÃO cria outro (1 reel, 1 contêiner)",
      "NO_AR_TARDE" in out and len(no_ar(tmp, "REELS")) == 1 and conta(tmp)["n_cont"] == 1 and rc == 0
      and "write-ahead" in str(reg_de(st, "t-cf-1").get("confirmado_por")), f"exit={rc} {no_ar(tmp, 'REELS')} {out[-300:]}")
checa("  ...com o dia marcado, formato/modo/rótulo no registro e o write-ahead resolvido", st["last_reel_date"] == "2026-07-29"
      and reg_de(st, "t-cf-1").get("formato") == "como_funciona" and reg_de(st, "t-cf-1").get("modo_reel") == "normal"
      and reg_de(st, "t-cf-1").get("rotulo_ia") is True and "reel_publicando" not in st, f"{st}")
rc, out, st = rodar("ok", tmp, agora=SEXTA_16H, extra=STORY_OFF)
checa("  ...e o próximo dia de reel não o republica (1 reel na conta)", len(no_ar(tmp, "REELS")) == 1 and rc == 0, f"exit={rc}")
shutil.rmtree(tmp, ignore_errors=True)

tmp = preparar(reels=[R_CF]); rc, out, st = rodar("reel_500_nao", tmp, agora=QUARTA_16H, extra=STORY_OFF)
c1 = (st.get("reel_publicando") or {}).get("container")
rc, out, st = rodar("ok", tmp, agora=QUARTA_1630, extra=STORY_OFF)
checa("contêiner FINISHED que a Meta NÃO entregou: o cron seguinte publica o MESMO contêiner (1 contêiner, 1 reel)",
      rc == 0 and c1 and len(no_ar(tmp, "REELS")) == 1 and conta(tmp)["n_cont"] == 1 and no_ar(tmp, "REELS")[0]["container"] == c1
      and reg_de(st, "t-cf-1").get("media_id") and "reel_publicando" not in st, f"exit={rc} {no_ar(tmp, 'REELS')} {out[-300:]}")
shutil.rmtree(tmp, ignore_errors=True)

tmp = preparar(reels=[R_CF]); rc, out, st = rodar("reel_500_nao", tmp, agora=QUARTA_16H, extra=STORY_OFF)
rc, out, st = rodar("ok", tmp, agora=SEXTA_16H, extra=STORY_OFF)
checa("CONTROLE: write-ahead com o contêiner EXPIRED (nunca saiu): descartado e o reel sai com contêiner novo (1 reel)",
      rc == 0 and len(no_ar(tmp, "REELS")) == 1 and conta(tmp)["n_cont"] == 2 and "reel_publicando" not in st,
      f"exit={rc} n_cont={conta(tmp)['n_cont']} {no_ar(tmp, 'REELS')}")
shutil.rmtree(tmp, ignore_errors=True)

tmp = preparar(reels=[R_CF]); rc, out, st = rodar("reel_morre_no_publish", tmp, agora=QUARTA_16H, extra=STORY_OFF)
checa("job morto DENTRO do media_publish do reel (a Meta publicou): o write-ahead já está em disco",
      rc != 0 and (st.get("reel_publicando") or {}).get("container") and ids(st) == [], f"exit={rc} {st}")
rc, out, st = rodar("ok", tmp, agora=QUARTA_1630, extra=STORY_OFF)
checa("  ...o run seguinte registra o reel pelo contêiner (PUBLISHED) e não republica (1 reel)", rc == 0
      and len(no_ar(tmp, "REELS")) == 1 and reg_de(st, "t-cf-1").get("confirmado_por"), f"exit={rc} {no_ar(tmp, 'REELS')}")
shutil.rmtree(tmp, ignore_errors=True)

tmp = preparar(reels=[R_CF]); rodar("reel_500_nao", tmp, agora=QUARTA_16H, extra=STORY_OFF)
rc, out, st = rodar("consulta_falha", tmp, agora=QUARTA_1630, extra=STORY_OFF)
checa("consulta ao contêiner do write-ahead falhando: nada de reel sai, job vermelho, write-ahead mantido", rc == 1
      and len(no_ar(tmp, "REELS")) == 0 and conta(tmp)["n_cont"] == 1 and (st.get("reel_publicando") or {}).get("container"),
      f"exit={rc} n_cont={conta(tmp)['n_cont']} {out[-300:]}")
rc, out, st = rodar("ok", tmp, agora=QUARTA_17H, extra=STORY_OFF)
checa("  ...e o run seguinte publica o MESMO contêiner", rc == 0 and len(no_ar(tmp, "REELS")) == 1 and conta(tmp)["n_cont"] == 1,
      f"exit={rc} n_cont={conta(tmp)['n_cont']}")
shutil.rmtree(tmp, ignore_errors=True)

tmp = preparar(reels=[R_CF]); rodar("ok", tmp, agora=QUARTA_16H, extra=STORY_OFF)
_est = json.loads((tmp / "state" / "published.json").read_text(encoding="utf-8"))
_est["reel_publicando"] = {"id": "t-cf-1", "container": "CONT001", "at": "2026-07-29T19:00:00+00:00"}   # sobra (estado editado)
(tmp / "state" / "published.json").write_text(json.dumps(_est), encoding="utf-8")
rc, out, st = rodar("ok", tmp, agora=QUARTA_1630, extra=STORY_OFF)
checa("write-ahead que sobrou de peça JÁ registrada: descartado, sem 2º registro nem 2º reel", rc == 0
      and [e["id"] for e in st["published"]].count("t-cf-1") == 1 and "reel_publicando" not in st
      and len(no_ar(tmp, "REELS")) == 1, f"exit={rc} {st['published']}")
shutil.rmtree(tmp, ignore_errors=True)

R_CF2 = {"id": "t-cf-2", "video": "media/f2.mp4", "caption": CAP_IA, "formato": "como_funciona"}
tmp = preparar(reels=[R_CF, R_CF2]); rodar("reel_500_nao", tmp, agora=QUARTA_16H, extra=STORY_OFF)
rc, out, st = rodar("consulta_falha", tmp, force_id="t-cf-2", agora=QUARTA_1630, extra=STORY_OFF)
checa("FORCE de outro reel com a consulta ao contêiner preparado FALHANDO: vermelho, nada sai, write-ahead intacto", rc == 1
      and len(no_ar(tmp, "REELS")) == 0 and (st.get("reel_publicando") or {}).get("id") == "t-cf-1", f"exit={rc} {out[-300:]}")
rc, out, st = rodar("ok", tmp, force_id="t-cf-2", agora=QUARTA_1630, extra=STORY_OFF)
checa("FORCE de OUTRO reel com contêiner preparado (write-ahead): vermelho, nada sai, o write-ahead do 1º fica", rc == 1
      and len(no_ar(tmp, "REELS")) == 0 and (st.get("reel_publicando") or {}).get("id") == "t-cf-1", f"exit={rc} {out[-300:]}")
rc, out, st = rodar("ok", tmp, force_id="t-cf-1", agora=QUARTA_17H, extra=STORY_OFF)
checa("CONTROLE: FORCE do MESMO reel publica o contêiner preparado (1 contêiner, 1 reel)", rc == 0
      and len(no_ar(tmp, "REELS")) == 1 and conta(tmp)["n_cont"] == 1, f"exit={rc} n_cont={conta(tmp)['n_cont']}")
shutil.rmtree(tmp, ignore_errors=True)

POST_ON = {"POSTS_ATIVOS": "on", "SEQUENCIAS_ATIVAS": "off"}
tmp = preparar(); rc, out, st = rodar("post_500_tarde", tmp, extra=POST_ON)
checa("POST: 500 com o contêiner FINISHED — vermelho e o write-ahead do post no estado", rc == 1 and ids(st) == []
      and (st.get("post_publicando") or {}).get("id") == "t-post-1", f"exit={rc} {st}")
rc, out, st = rodar("ok", tmp, agora="2026-07-28T21:30:00+00:00", extra=POST_ON)
checa("  ...a Meta entregou depois: registrado pelo write-ahead, 1 imagem na conta, dia marcado", "NO_AR_TARDE" in out
      and len(no_ar(tmp, "IMAGE")) == 1 and reg_de(st, "t-post-1").get("confirmado_por") and st["last_post_date"] == "2026-07-28"
      and rc == 0, f"exit={rc} {no_ar(tmp, 'IMAGE')} {out[-300:]}")
shutil.rmtree(tmp, ignore_errors=True)

print("\nS27) REEL TRIAL: 500 transitório no contêiner trial NÃO é 'trial_params recusado' (a peça do experimento não sai no grid)")
tmp = preparar(); rc, out, st = rodar("trial_500", tmp, force_id="t-reel-1")
checa("trial com 500: job vermelho, nada publicado, sem fallback normal", rc == 1 and ids(st) == [] and len(no_ar(tmp, "REELS")) == 0
      and "trial_params recusado" not in out and "AUTENTICACAO FALHOU" not in out, f"exit={rc} {ids(st)} {out[-300:]}")
shutil.rmtree(tmp, ignore_errors=True)
tmp = preparar(); rc, out, st = rodar("trial_recusado", tmp, force_id="t-reel-1")
checa("CONTROLE: trial_params RECUSADO pela Meta (400, code 100) cai no fallback normal", rc == 0
      and any(e.get("modo_reel") == "fallback_normal" for e in st["published"]), f"exit={rc} {st['published']}")
shutil.rmtree(tmp, ignore_errors=True)

print("\nS28) guardas do caminho da story que a verificação achou sem controle negativo")
tmp = preparar_story(); rc, out, st = rodar("morre_antes_do_publish", tmp, agora=TER_17, extra=STORY_OFF)
wa = st.get("story_nova_publicando") or {}; n1 = conta(tmp)["n_cont"]
_meta = json.loads((tmp / "stories_cf" / "stn_t.json").read_text(encoding="utf-8"))
(tmp / "stories_cf" / "stn_t_2.mp4").write_bytes(b"parte1 RE-RENDER")          # re-render do vídeo 2 (irmão coerente)
_meta["partes"][1]["sha256"] = _sha(b"parte1 RE-RENDER")
(tmp / "stories_cf" / "stn_t.json").write_text(json.dumps(_meta, ensure_ascii=False), encoding="utf-8")
(tmp / "aprovacoes.json").write_text(json.dumps({"lotes": [lote_story([entrada(tmp, "stn_t")])]}), encoding="utf-8")
rc, out, st = rodar("ok", tmp, agora=TER_1330, extra=STORY_OFF)
checa("write-ahead FINISHED de um render ANTIGO: o contêiner velho NÃO é publicado (2 contêineres novos, partes 2 e 3)",
      rc == 0 and ids_story(st) == TRES and wa.get("container") and reg_de(st, "stn_t#1").get("container") != wa.get("container")
      and conta(tmp)["n_cont"] - n1 == 2 and "o render mudou" in out
      and not any(m["container"] == wa.get("container") for m in no_ar(tmp)), f"exit={rc} n_cont {n1}->{conta(tmp)['n_cont']} {out[-300:]}")
shutil.rmtree(tmp, ignore_errors=True)
_ontem = [{"id": f"stn_y#{i}", "kind": "story_nova", "story": "stn_y", "parte": i, "media_id": None,
           "at": "2026-11-16T16:00:00+00:00", "confirmado_por": "status_code PUBLISHED depois de erro"} for i in range(3)]
tmp = preparar_story(publicados_extra=_ontem)
velho = (tmp / "state" / "published.json").read_text(encoding="utf-8")
rc, out, st = rodar("ok", tmp, agora="2026-11-17T15:30:07+00:00", extra=STORY_OFF)
(tmp / "state" / "published.json").write_text(velho, encoding="utf-8")
rc, out, st = rodar("ok", tmp, agora="2026-11-17T15:41:00+00:00", extra=STORY_OFF)
checa("parte sem media_id de ONTEM não desconta story desconhecida de HOJE: o run com estado velho dá exit 1 'NAO conhece'",
      rc == 1 and len(no_ar(tmp)) == 3 and "NAO conhece" in out, f"exit={rc} {no_ar(tmp)} {out[-300:]}")
shutil.rmtree(tmp, ignore_errors=True)
tmp = preparar_story(reel_em="2026-11-14T18:00:00+00:00")
_est = json.loads((tmp / "state" / "published.json").read_text(encoding="utf-8"))
_est["published"] = [e for e in _est["published"] if e.get("id") != "cf_pe_virado"]
(tmp / "state" / "published.json").write_text(json.dumps(_est), encoding="utf-8")
rc, out, st = rodar("ok", tmp, force_id="story:stn_t", agora=SEG_16, extra=STORY_OFF)
checa("FORCE story:<id> com o reel de origem FORA do grid: exit 1 e nada publicado (a tela 3 diria 'no perfil')",
      rc == 1 and ids_story(st) == [] and len(no_ar(tmp)) == 0 and "ainda não saiu no grid" in out, f"exit={rc} {out[-300:]}")
shutil.rmtree(tmp, ignore_errors=True)

print("\nS29) APROVAÇÃO só do TEXTO (fixture antigo) + re-render COERENTE: nada sai (o Rafael não viu o vídeo novo)")
tmp = preparar_story()
_fila = json.loads((tmp / "stories_cf.json").read_text(encoding="utf-8"))
_fila[0]["telas"][1]["crop"] = [0, 0, 1080, 1920]; _fila[0]["telas"][1]["trecho"] = [20.0, 27.5]   # correção visual
(tmp / "stories_cf.json").write_text(json.dumps(_fila, ensure_ascii=False), encoding="utf-8")
_meta = json.loads((tmp / "stories_cf" / "stn_t.json").read_text(encoding="utf-8"))
(tmp / "stories_cf" / "stn_t_2.mp4").write_bytes(b"VIDEO 2 QUE O RAFAEL NUNCA VIU")
_meta["partes"][1].update(sha256=_sha(b"VIDEO 2 QUE O RAFAEL NUNCA VIU"), crop=[0, 0, 1080, 1920], trecho=[20.0, 27.5],
                          camera=CS.camera_de(_fila[0]["telas"][1]))
_meta["hash_render"] = CS.hash_render(_fila[0])
(tmp / "stories_cf" / "stn_t.json").write_text(json.dumps(_meta, ensure_ascii=False), encoding="utf-8")
(tmp / "aprovacoes.json").write_text(json.dumps({"lotes": [lote_story([{"id": "stn_t", "hash_roteiro": CS.hash_story(ST)}])]}),
                                     encoding="utf-8")
rc, out, st = rodar("ok", tmp, agora=TER_17, extra=STORY_OFF)
checa("lote só de texto (com autor e evidência): nada publicado e o aviso diz 'não amarrada'", ids_story(st) == [] and rc == 0
      and len(no_ar(tmp)) == 0 and "não amarrada" in out, f"exit={rc} {ids_story(st)} {out[-400:]}")
(tmp / "aprovacoes.json").write_text(json.dumps({"lotes": [lote_story([entrada(tmp, "stn_t")])]}), encoding="utf-8")
rc, out, st = rodar("ok", tmp, agora=TER_17, extra=STORY_OFF)
checa("CONTROLE: o Rafael aprova o render NOVO (entrada de --entrada) -> sai inteira", ids_story(st) == TRES and rc == 0,
      f"exit={rc} {ids_story(st)} {out[-300:]}")
shutil.rmtree(tmp, ignore_errors=True)
tmp = preparar_story()
(tmp / "aprovacoes.json").write_text(json.dumps({"lotes": [dict(lote_story([entrada(tmp, "stn_t")]), evidencia="")]}),
                                     encoding="utf-8")
rc, out, st = rodar("ok", tmp, agora=TER_17, extra=STORY_OFF)
checa("lote 'aprovado' sem evidência (o portão clínico do publish.yml o recusa): a story não conta como aprovada",
      ids_story(st) == [] and rc == 0 and "evidencia" in out, f"exit={rc} {ids_story(st)} {out[-300:]}")
shutil.rmtree(tmp, ignore_errors=True)

print("\nS22) publish.yml: checkout com ref: main (o run enfileirado lê o estado que o anterior commitou)")
_yml = (ROOT / ".github" / "workflows" / "publish.yml").read_text(encoding="utf-8")
_m = re.search(r"- uses: actions/checkout@v4[ \t]*\r?\n[ \t]+with:[ \t]*\r?\n(?:[ \t]*#[^\n]*\n|[ \t]+[a-z-]+:[^\n]*\n)*?"
               r"[ \t]+ref:[ \t]*main[ \t]*\r?\n", _yml)
checa("o checkout do job de publicação tem ref: main", _m is not None and _yml.count("actions/checkout@") == 1, "publish.yml")

print("\nS23) stories_pulse: a SÉRIE do dia vai ao disco ANTES dos extras, e os extras têm orçamento de tempo")
PULSE = r'''
import sys, json, io, os, time, urllib.parse, urllib.request, runpy
MODO = sys.argv[1]
rel = {"t": 1000.0}
time.monotonic = lambda: rel["t"]
class Resp(io.BytesIO):
    def __enter__(self): return self
    def __exit__(self, *a): return False
def urlopen(url, timeout=None):
    u = urllib.parse.urlsplit(url); q = urllib.parse.parse_qs(u.query); metrica = (q.get("metric") or [""])[0]
    if u.path.endswith("/stories"):
        return Resp(json.dumps({"data": [{"id": "S%d" % i, "media_type": "VIDEO",
                                          "timestamp": "2026-11-17T15:31:00+0000"} for i in (1, 2, 3)]}).encode())
    if not metrica.startswith("views"):                       # extra
        if MODO == "morre_nos_extras":
            print("JOB_MORTO_NOS_EXTRAS", flush=True); os._exit(137)
        if MODO == "extras_pendurados":
            rel["t"] += timeout                               # pendura até o timeout da chamada
            raise TimeoutError("timed out")
    if "breakdown" in q:
        dados = {"data": [{"total_value": {"breakdowns": [{"results": [{"dimension_values": ["TAP_FORWARD"], "value": 3}]}]}}]}
    else:
        dados = {"data": [{"name": m, "values": [{"value": 7}]} for m in metrica.split(",")]}
    return Resp(json.dumps(dados).encode())
urllib.request.urlopen = urlopen
try:
    runpy.run_path("stories_pulse.py", run_name="__main__")
finally:
    json.dump({"gasto_s": rel["t"] - 1000.0}, open("_relogio.json", "w"))
'''


def pulso(modo, extra=None):
    d = Path(tempfile.mkdtemp(prefix="igpulse_")); (d / "state").mkdir()
    shutil.copy(ROOT / "stories_pulse.py", d / "stories_pulse.py"); (d / "_pulse.py").write_text(PULSE, encoding="utf-8")
    env = dict(os.environ, IG_USER_ID="1784", IG_ACCESS_TOKEN="fake", PYTHONUTF8="1", PYTHONIOENCODING="utf-8")
    env.update(extra or {})
    p = subprocess.run([sys.executable, str(d / "_pulse.py"), modo], cwd=str(d), capture_output=True, text=True, env=env,
                       encoding="utf-8", errors="replace")
    ler = lambda n: json.loads((d / n).read_text(encoding="utf-8")) if (d / n).exists() else None
    r = (p.returncode, (p.stdout or "") + (p.stderr or ""), ler("state/stories_serie.json"), ler("state/stories_pecas.json"),
         ler("_relogio.json"))
    shutil.rmtree(d, ignore_errors=True)
    return r


rc, out, serie, pecas, relg = pulso("morre_nos_extras")
checa("job morto nos extras: a série do dia JÁ está gravada (3 ativos, views 21)", rc != 0 and serie and serie["dias"][-1].get("views") == 21
      and serie["dias"][-1].get("stories_ativos") == 3, f"exit={rc} serie={serie} {out[-300:]}")
checa("  ...e as peças da chamada principal também", pecas and sorted(pecas["pecas"]) == ["S1", "S2", "S3"], f"{pecas}")
rc, out, serie, pecas, relg = pulso("extras_pendurados", {"STORIES_ORCAMENTO_EXTRAS_S": "50"})
cortados = [e for p in (pecas or {}).get("pecas", {}).values() for e in p.get("erros_extra", []) if "orçamento" in e]
checa("extras pendurados: o orçamento corta (tempo gasto <= orçamento) e o job termina com a série gravada",
      rc == 0 and relg and relg["gasto_s"] <= 51 and serie and serie["dias"][-1].get("views") == 21 and cortados,
      f"exit={rc} gasto={relg} cortados={len(cortados)} {out[-300:]}")
rc, out, serie, pecas, relg = pulso("ok")
s1 = (pecas or {}).get("pecas", {}).get("S1", {})
checa("CONTROLE: extras respondendo -> follows, profile_visits e navegação por tipo medidos",
      rc == 0 and s1.get("follows") == 7 and s1.get("profile_visits") == 7 and s1.get("navegacao") == {"tap_forward": 3}, f"{s1}")

# ---------------------------------------------------------------- formatos novos (Rafael, 24-26/10/2026)
# "colocar eles, os quatro formatos [...] um cada dia [...] intercalar um formato novo com como funciona": ter/qui/sáb
# (as vagas do carrossel antigo) = um dos 4 formatos novos em rodízio a partir de 03/11/2026; seg/qua/sex/dom = COMO
# FUNCIONA. Padrão de PRODUÇÃO (FN): nenhuma variável de cota/suspensão; stories da geração nova ligados (fila vazia).
# FN1-FN8 testam a MECÂNICA do rodízio simples (pesos iguais); o FN9 testa o padrão de produção com peso (31/10)
FN = {"LAMINAS_POR_SEMANA": None, "CONVERSAS_ATIVAS": None, "POSTS_ATIVOS": None, "SEQUENCIAS_ATIVAS": None,
      "PESOS_FORMATOS_NOVOS": "iguais"}
FN_PROD = dict(FN, PESOS_FORMATOS_NOVOS=None)          # padrão de regra_reels.py (câmera 2 : VAR 1 : reserva 0)
R_QUAL = {"id": "t-qual-1", "video": "media/q1.mp4", "caption": CAP_IA, "formato": "qual_dos_dois", "voz_ia": True}
R_QUAL2 = dict(R_QUAL, id="t-qual-2", video="media/q2.mp4")
R_MITO = dict(R_QUAL, id="t-mito-1", video="media/m1.mp4", formato="mito_na_prova")
R_CAM = dict(R_QUAL, id="t-cam-1", video="media/k1.mp4", formato="camera_lenta")
R_VAR = dict(R_QUAL, id="t-var-1", video="media/v1.mp4", formato="chama_o_var")
R_CF_N = dict(R_QUAL, id="t-cf-n", video="media/fn.mp4", formato="como_funciona")
TER_NOV_16H = "2026-11-17T19:00:00+00:00"           # terça 17/11 16:00 BRT: vaga de formato novo
TER_NOV_1630 = "2026-11-17T19:30:00+00:00"          # o cron seguinte do mesmo dia
TER_OUT_16H = "2026-10-20T19:00:00+00:00"           # terça 20/10 16:00 BRT: ANTES do início (27/10)
SEG_NOV_16H = "2026-11-16T19:00:00+00:00"           # segunda 16/11 16:00 BRT: COMO FUNCIONA


def fmt_reg(st, rid):
    return reg_de(st, rid).get("formato")


print("\nFN1) TERÇA depois de 03/11: publica o FORMATO NOVO (não o COMO FUNCIONA da frente), com rótulo de IA e formato no registro")
tmp = preparar(reels=[R_CF_N, R_QUAL, R_QUAL2]); rc, out, st = rodar("ok", tmp, agora=TER_NOV_16H, extra=FN)
checa("saiu o 1º formato novo da fila, não o COMO FUNCIONA", ids(st) == ["t-qual-1"], f"exit={rc} publicados={ids(st)} {out[-300:]}")
checa("registro: formato, rótulo de IA e modo normal", fmt_reg(st, "t-qual-1") == "qual_dos_dois"
      and reg_de(st, "t-qual-1").get("rotulo_ia") is True and reg_de(st, "t-qual-1").get("modo_reel") == "normal"
      and "ROTULO_IA true media_type= REELS" in out, f"{reg_de(st, 't-qual-1')}")
checa("last_reel_date marcado e exit 0 sem ::error::", st["last_reel_date"] == "2026-11-17" and rc == 0 and "::error::" not in out,
      f"exit={rc} last={st['last_reel_date']!r}")
rc, out, st = rodar("ok", tmp, agora=TER_NOV_1630, extra=FN)
checa("cron seguinte do mesmo dia: 1 reel por dia (t-qual-2 não sai)", ids(st) == ["t-qual-1"] and len(no_ar(tmp, "REELS")) == 1
      and rc == 0, f"exit={rc} publicados={ids(st)} conta={no_ar(tmp, 'REELS')}")
shutil.rmtree(tmp, ignore_errors=True)

print("\nFN2) TERÇA ANTES do início (27/10): nada sai (nem formato novo nem COMO FUNCIONA), exit 0")
tmp = preparar(reels=[R_QUAL, R_CF_N]); rc, out, st = rodar("ok", tmp, agora=TER_OUT_16H, extra=FN)
checa("nada publicado e last_reel_date intacto", ids(st) == [] and st["last_reel_date"] == "", f"publicados={ids(st)}")
checa("exit 0 sem ::error::", rc == 0 and "::error::" not in out, f"exit={rc} {out[-300:]}")
checa("log diz quando começa", "ter/qui/sab sem reel ate 27/10/2026" in out, out[-300:])
shutil.rmtree(tmp, ignore_errors=True)
tmp = preparar(reels=[R_QUAL, R_CF_N]); rc, out, st = rodar("ok", tmp, agora="2026-10-27T19:00:00+00:00", extra=FN)
checa("CONTROLE: terça 27/10 (o início) já publica o formato novo", ids(st) == ["t-qual-1"] and rc == 0, f"exit={rc} {ids(st)}")
shutil.rmtree(tmp, ignore_errors=True)

print("\nFN3) SEGUNDA: publica COMO FUNCIONA e NUNCA formato novo")
tmp = preparar(reels=[R_QUAL, R_MITO, R_CF_N]); rc, out, st = rodar("ok", tmp, agora=SEG_NOV_16H, extra=FN)
checa("saiu o COMO FUNCIONA, mesmo atrás de 2 formatos novos na fila", ids(st) == ["t-cf-n"]
      and fmt_reg(st, "t-cf-n") == "como_funciona" and rc == 0, f"exit={rc} publicados={ids(st)}")
shutil.rmtree(tmp, ignore_errors=True)
tmp = preparar(reels=[R_QUAL, R_MITO, R_CAM, R_VAR]); rc, out, st = rodar("ok", tmp, agora=SEG_NOV_16H, extra=FN)
checa("segunda só com formatos novos na fila: nenhum sai, exit 0, sem ::error::", ids(st) == [] and rc == 0
      and "::error::" not in out and st["last_reel_date"] == "", f"exit={rc} publicados={ids(st)}")
checa("  ...e o log pede COMO FUNCIONA (não 'esgotada')", "nenhum COMO FUNCIONA pronto" in out and "esgotada" not in out, out[-300:])
shutil.rmtree(tmp, ignore_errors=True)
tmp = preparar(reels=[R_CF_N, R_QUAL]); rc, out, st = rodar("ok", tmp, force_id="t-qual-1", agora=SEG_NOV_16H, extra=FN)
checa("CONTROLE: FORCE_ID de formato novo numa segunda (decisão humana) sai e grava o formato (o rodízio lê o registro)",
      ids(st) == ["t-qual-1"] and fmt_reg(st, "t-qual-1") == "qual_dos_dois" and rc == 0, f"exit={rc} {st['published']}")
shutil.rmtree(tmp, ignore_errors=True)

print("\nFN4) RODÍZIO: sai o formato publicado há MAIS tempo; nunca publicado primeiro; empate = ordem da fila")
PUB_ROD = [{"id": "t-qual-0", "kind": "reel", "media_id": "MQ", "at": "2026-11-03T18:05:00+00:00", "formato": "qual_dos_dois"},
           {"id": "t-mito-0", "kind": "reel", "media_id": "MM", "at": "2026-11-05T18:05:00+00:00", "formato": "mito_na_prova"},
           {"id": "t-cam-0", "kind": "reel", "media_id": "MC", "at": "2026-11-07T18:05:00+00:00", "formato": "camera_lenta"},
           {"id": "t-var-0", "kind": "reel", "media_id": "MV", "at": "2026-11-10T18:05:00+00:00", "formato": "chama_o_var"}]
tmp = preparar(reels=[R_VAR, R_CAM, R_MITO, R_QUAL2, R_QUAL], publicados=PUB_ROD)
rc, out, st = rodar("ok", tmp, agora=TER_NOV_16H, extra=FN)
checa("os 4 já saíram: sai o QUAL DOS DOIS (03/11, o mais antigo), mesmo no fim da fila — e o 1º da fila DELE (t-qual-2)",
      ids(st)[len(PUB_ROD):] == ["t-qual-2"] and rc == 0, f"exit={rc} {ids(st)}")
shutil.rmtree(tmp, ignore_errors=True)
tmp = preparar(reels=[R_QUAL, R_MITO, R_CAM, R_VAR], publicados=PUB_ROD[:3])
rc, out, st = rodar("ok", tmp, agora=TER_NOV_16H, extra=FN)
checa("CHAMA O VAR nunca publicado: sai primeiro, mesmo no fim da fila", ids(st)[3:] == ["t-var-1"] and rc == 0, f"{ids(st)}")
shutil.rmtree(tmp, ignore_errors=True)
tmp = preparar(reels=[R_MITO, R_QUAL]); rc, out, st = rodar("ok", tmp, agora=TER_NOV_16H, extra=FN)
checa("empate (nenhum publicado): o da frente da fila (MITO)", ids(st) == ["t-mito-1"], f"{ids(st)}")
shutil.rmtree(tmp, ignore_errors=True)
tmp = preparar(reels=[R_QUAL, R_MITO]); rc, out, st = rodar("ok", tmp, agora=TER_NOV_16H, extra=FN)
checa("CONTROLE do empate: fila invertida -> QUAL", ids(st) == ["t-qual-1"], f"{ids(st)}")
shutil.rmtree(tmp, ignore_errors=True)
# registro antigo SEM 'formato' (t-cam-1 em 07/11): o formato vem do reels.json — sem isso a câmera lenta pareceria
# nunca publicada e passaria à frente
PUB_ANTIGO = dict({k: v for k, v in PUB_ROD[2].items() if k != "formato"}, id="t-cam-1")
tmp = preparar(reels=[R_CAM, dict(R_CAM, id="t-cam-2"), R_QUAL], publicados=[PUB_ANTIGO, PUB_ROD[0]])
rc, out, st = rodar("ok", tmp, agora=TER_NOV_16H, extra=FN)
checa("registro sem 'formato' (antigo) conta pelo reels.json: câmera 07/11 é mais nova que qual 03/11 -> QUAL",
      ids(st)[2:] == ["t-qual-1"], f"{ids(st)}")
shutil.rmtree(tmp, ignore_errors=True)

print("\nFN5) VAGA de ter/qui/sáb SEM formato novo pronto: sem reel, com aviso, exit 0 (o COMO FUNCIONA não ocupa a vaga)")
tmp = preparar(reels=[R_CF_N]); rc, out, st = rodar("ok", tmp, agora=TER_NOV_16H, extra=FN)
checa("nada publicado e last_reel_date intacto", ids(st) == [] and st["last_reel_date"] == "", f"publicados={ids(st)}")
checa("exit 0 e sem ::error::", rc == 0 and "::error::" not in out, f"exit={rc} {out[-300:]}")
checa("aviso (::warning::) da vaga sem peça, sem 'esgotada'", "::warning::Reels: vaga dos FORMATOS NOVOS" in out
      and "esgotada" not in out, out[-400:])
shutil.rmtree(tmp, ignore_errors=True)
tmp = preparar(reels=[R_QUAL], publicados=[{"id": "t-qual-1", "kind": "reel", "media_id": "MQ", "at": "2026-11-03T18:05:00+00:00",
                                            "formato": "qual_dos_dois"}])
rc, out, st = rodar("ok", tmp, agora=TER_NOV_16H, extra=FN)
checa("CONTROLE: biblioteca inteira publicada -> 'esgotada' (não o aviso de vaga)", "esgotada" in out
      and "vaga dos FORMATOS NOVOS" not in out and rc == 0, out[-300:])
shutil.rmtree(tmp, ignore_errors=True)

print("\nFN6) WRITE-AHEAD do formato novo: 500 no media_publish e a Meta entrega depois -> 1 reel, formato no registro")
tmp = preparar(reels=[R_QUAL, R_QUAL2]); rc, out, st = rodar("reel_500_tarde", tmp, agora=TER_NOV_16H, extra=FN)
wa = st.get("reel_publicando") or {}
checa("run 1: vermelho, o contêiner no write-ahead com o formato", rc == 1 and ids(st) == [] and wa.get("id") == "t-qual-1"
      and wa.get("formato") == "qual_dos_dois", f"exit={rc} {wa}")
rc, out, st = rodar("ok", tmp, agora=TER_NOV_1630, extra=FN)
checa("run 2: registrado pelo contêiner, 1 reel na conta, formato no registro, o dia marcado (t-qual-2 não sai)",
      rc == 0 and len(no_ar(tmp, "REELS")) == 1 and ids(st) == ["t-qual-1"] and fmt_reg(st, "t-qual-1") == "qual_dos_dois"
      and st["last_reel_date"] == "2026-11-17" and "reel_publicando" not in st, f"exit={rc} {st['published']} {out[-300:]}")
shutil.rmtree(tmp, ignore_errors=True)

print("\nFN7) WRITE-AHEAD de OUTRO grupo de dias: o contêiner FINISHED que sobrou NÃO sai no dia errado, e nenhum outro reel"
      " sai enquanto ele pode ser entregue (verificação de 26/10/2026)")
R_CF_A = dict(R_CF_N, id="t-cf-a", video="media/fa.mp4")
R_CF_B = dict(R_CF_N, id="t-cf-b", video="media/fb.mp4")
SEG_OUT_2330 = "2026-10-20T02:30:00+00:00"          # segunda 19/10 23:30 BRT (COMO FUNCIONA)
QUA_OUT_16H = "2026-10-21T19:00:00+00:00"           # quarta 21/10 16:00 BRT (o contêiner de segunda já EXPIRED: 24 h)
TER_NOV_2330 = "2026-11-18T02:30:00+00:00"          # terça 17/11 23:30 BRT (formato novo)
QUA_NOV_16H = "2026-11-18T19:00:00+00:00"           # quarta 18/11 16:00 BRT (COMO FUNCIONA)
QUI_NOV_16H = "2026-11-19T19:00:00+00:00"           # quinta 19/11 16:00 BRT (formato novo; o de terça já EXPIRED)
DOM_NOV_2330 = "2026-11-16T02:30:00+00:00"          # domingo 15/11 23:30 BRT (COMO FUNCIONA)
AVISO_WA = "esta FINISHED, mas hoje e' dia"
# (a) COMO FUNCIONA de segunda 23:30 com 500 -> terça 20/10 (antes do início: dia SEM reel)
tmp = preparar(reels=[R_CF_A, R_CF_B]); rc, out, st = rodar("reel_500_nao", tmp, agora=SEG_OUT_2330, extra=FN)
c1 = (st.get("reel_publicando") or {}).get("container")
checa("segunda 23:30: 500 com o contêiner FINISHED — write-ahead do COMO FUNCIONA no estado", rc == 1 and c1
      and (st.get("reel_publicando") or {}).get("formato") == "como_funciona", f"exit={rc} {st.get('reel_publicando')}")
rc, out, st = rodar("ok", tmp, agora=TER_OUT_16H, extra=FN)
checa("terça 20/10 (antes do início): o contêiner do COMO FUNCIONA NÃO sai e nenhum outro reel sai", ids(st) == []
      and len(no_ar(tmp, "REELS")) == 0 and conta(tmp)["n_cont"] == 1 and st["last_reel_date"] == "",
      f"exit={rc} {ids(st)} {no_ar(tmp, 'REELS')} {out[-300:]}")
checa("  ...write-ahead mantido, aviso (::warning::) e job verde", (st.get("reel_publicando") or {}).get("container") == c1
      and AVISO_WA in out and "::warning::" in out and rc == 0 and "::error::" not in out, f"exit={rc} {out[-400:]}")
rc, out, st = rodar("ok", tmp, agora=QUA_OUT_16H, extra=FN)
checa("quarta 21/10: o contêiner expirou (nunca saiu) -> descartado e o COMO FUNCIONA sai no dia DELE (1 reel, sem adiantar a fila)",
      ids(st) == ["t-cf-a"] and st["last_reel_date"] == "2026-10-21" and len(no_ar(tmp, "REELS")) == 1
      and conta(tmp)["n_cont"] == 2 and "reel_publicando" not in st and rc == 0, f"exit={rc} {ids(st)} {out[-300:]}")
shutil.rmtree(tmp, ignore_errors=True)
# (b) o inverso: formato novo de terça 23:30 com 500 -> quarta (dia de COMO FUNCIONA)
tmp = preparar(reels=[R_QUAL, R_CF_N]); rc, out, st = rodar("reel_500_nao", tmp, agora=TER_NOV_2330, extra=FN)
c1 = (st.get("reel_publicando") or {}).get("container")
checa("terça 17/11 23:30: 500 com o contêiner FINISHED — write-ahead do formato novo no estado", rc == 1 and c1
      and (st.get("reel_publicando") or {}).get("formato") == "qual_dos_dois", f"exit={rc} {st.get('reel_publicando')}")
rc, out, st = rodar("ok", tmp, agora=QUA_NOV_16H, extra=FN)
checa("quarta 18/11: o formato novo NÃO sai no dia do COMO FUNCIONA, e o COMO FUNCIONA espera o contêiner (nenhum reel)",
      ids(st) == [] and len(no_ar(tmp, "REELS")) == 0 and conta(tmp)["n_cont"] == 1 and rc == 0 and AVISO_WA in out
      and (st.get("reel_publicando") or {}).get("container") == c1, f"exit={rc} {ids(st)} {out[-400:]}")
rc, out, st = rodar("ok", tmp, agora=QUI_NOV_16H, extra=FN)
checa("quinta 19/11: contêiner expirado -> descartado e o formato novo sai na vaga DELE (contêiner novo, formato no registro)",
      ids(st) == ["t-qual-1"] and fmt_reg(st, "t-qual-1") == "qual_dos_dois" and len(no_ar(tmp, "REELS")) == 1
      and conta(tmp)["n_cont"] == 2 and "reel_publicando" not in st and rc == 0, f"exit={rc} {ids(st)} {out[-300:]}")
rc, out, st = rodar("ok", tmp, agora="2026-11-20T19:00:00+00:00", extra=FN)
checa("  ...e sexta 20/11 o COMO FUNCIONA (a fila dele não perdeu a peça)", ids(st) == ["t-qual-1", "t-cf-n"] and rc == 0,
      f"exit={rc} {ids(st)}")
shutil.rmtree(tmp, ignore_errors=True)
# (c) CONTROLE: mesmo grupo (domingo 23:30 -> segunda, os dois de COMO FUNCIONA) publica o MESMO contêiner, como antes
tmp = preparar(reels=[R_CF_N, R_QUAL]); rc, out, st = rodar("reel_500_nao", tmp, agora=DOM_NOV_2330, extra=FN)
c1 = (st.get("reel_publicando") or {}).get("container")
rc, out, st = rodar("ok", tmp, agora=SEG_NOV_16H, extra=FN)
checa("CONTROLE: domingo 23:30 -> segunda (mesmo grupo): publica o MESMO contêiner (1 contêiner, 1 reel), sem o aviso",
      rc == 0 and c1 and ids(st) == ["t-cf-n"] and len(no_ar(tmp, "REELS")) == 1 and conta(tmp)["n_cont"] == 1
      and no_ar(tmp, "REELS")[0]["container"] == c1 and AVISO_WA not in out and st["last_reel_date"] == "2026-11-16",
      f"exit={rc} {ids(st)} {no_ar(tmp, 'REELS')} {out[-300:]}")
shutil.rmtree(tmp, ignore_errors=True)

print("\nFN8) REEL INCERTO de formato novo: o registro incerto guarda o FORMATO (o rodízio conta o incerto; sem o campo, peça "
      "incerta retirada da fila contava como lâmina)")
tmp = preparar(reels=[R_CAM, R_QUAL]); rc, out, st = rodar("publish_500_incerto", tmp, agora=TER_NOV_16H, extra=FN)
checa("media_publish com erro e consulta falhando: 'reel_incerto' com formato camera_lenta", rc == 1
      and [e["kind"] for e in st["published"]] == ["reel_incerto"] and fmt_reg(st, "t-cam-1") == "camera_lenta",
      f"exit={rc} {st['published']}")
shutil.rmtree(tmp, ignore_errors=True)
tmp = preparar(reels=[R_CAM, R_QUAL]); rodar("reel_500_nao", tmp, agora=TER_NOV_16H, extra=FN)
_c = conta(tmp)
for _k in _c["conteineres"].values():
    _k["status"] = "IN_PROGRESS"                    # o contêiner do write-ahead num status que não decide
(tmp / "_conta_meta.json").write_text(json.dumps(_c), encoding="utf-8")
rc, out, st = rodar("ok", tmp, agora=TER_NOV_1630, extra=FN)
checa("write-ahead com o contêiner num status que não decide: 'reel_incerto' com o formato do write-ahead", rc == 1
      and reg_de(st, "t-cam-1").get("kind") == "reel_incerto" and fmt_reg(st, "t-cam-1") == "camera_lenta",
      f"exit={rc} {st['published']}")
checa("  ...e o dia do write-ahead fica marcado: nenhum 2º reel no MESMO dia (o incerto pode estar no ar)",
      [e["kind"] for e in st["published"]] == ["reel_incerto"] and st["last_reel_date"] == "2026-11-17"
      and len(no_ar(tmp, "REELS")) == 0, f"exit={rc} {st['published']} last={st['last_reel_date']!r}")
shutil.rmtree(tmp, ignore_errors=True)
tmp = preparar(reels=[R_CAM, R_QUAL]); rodar("reel_500_nao", tmp, agora=TER_NOV_16H, extra=FN)
_c = conta(tmp)
for _k in _c["conteineres"].values():
    _k["status"] = "IN_PROGRESS"
(tmp / "_conta_meta.json").write_text(json.dumps(_c), encoding="utf-8")
rc, out, st = rodar("ok", tmp, agora=QUI_NOV_16H, extra=FN)
checa("CONTROLE: o mesmo incerto achado só na QUINTA marca a terça (dia do write-ahead) e a vaga de quinta sai normalmente",
      reg_de(st, "t-cam-1").get("kind") == "reel_incerto"
      and ids(st)[1:] == ["t-qual-1"] and st["last_reel_date"] == "2026-11-19" and rc == 1, f"exit={rc} {st['published']}")
shutil.rmtree(tmp, ignore_errors=True)
# a consequência no rodízio: a câmera lenta incerta de 17/11 SAIU da fila (a conferência a abandonou) e o qual dos dois
# saiu em 10/11 — na quinta 19/11 sai o QUAL (o mais antigo), não a câmera lenta de novo. Sem o formato no registro, o
# incerto contava como lâmina, a câmera lenta parecia nunca publicada e passava à frente.
_inc = [{"id": "t-qual-0", "kind": "reel", "media_id": "MQ", "at": "2026-11-10T18:05:00+00:00", "formato": "qual_dos_dois"},
        {"id": "t-cam-1", "kind": "reel_incerto", "media_id": None, "at": "2026-11-17T19:05:00+00:00", "formato": "camera_lenta"}]
tmp = preparar(reels=[dict(R_CAM, id="t-cam-2"), R_QUAL], publicados=_inc)
rc, out, st = rodar("ok", tmp, agora=QUI_NOV_16H, extra=FN)
checa("  ...e o rodízio conta o incerto pelo formato gravado: quinta sai QUAL DOS DOIS (não a câmera lenta de novo)",
      ids(st)[2:] == ["t-qual-1"], f"exit={rc} {ids(st)}")
shutil.rmtree(tmp, ignore_errors=True)
_inc_sem = [_inc[0], {k: v for k, v in _inc[1].items() if k != "formato"}]
tmp = preparar(reels=[dict(R_CAM, id="t-cam-2"), R_QUAL], publicados=_inc_sem)
rc, out, st = rodar("ok", tmp, agora=QUI_NOV_16H, extra=FN)
checa("  CONTROLE: o mesmo incerto SEM o formato (como era gravado) deixa a câmera lenta repetir — o campo é o que decide",
      ids(st)[2:] == ["t-cam-2"], f"exit={rc} {ids(st)}")
shutil.rmtree(tmp, ignore_errors=True)

print("\nFN9) RODÍZIO COM PESO (Rafael, 31/10): câmera lenta 2 : Chama o VAR 1; Qual dos dois e Mito = reserva")
P4 = [{"id": "p-var", "kind": "reel", "media_id": "PV", "at": "2026-10-27T23:49:00+00:00", "formato": "chama_o_var"},
      {"id": "p-cam", "kind": "reel", "media_id": "PC", "at": "2026-10-29T20:06:00+00:00", "formato": "camera_lenta"},
      {"id": "p-qual", "kind": "reel", "media_id": "PQ", "at": "2026-10-31T18:05:00+00:00", "formato": "qual_dos_dois"},
      {"id": "p-mito", "kind": "reel", "media_id": "PM", "at": "2026-11-03T18:05:00+00:00", "formato": "mito_na_prova"}]
FX = [dict(R_QUAL, id="w-qual", video="media/wq.mp4"), dict(R_MITO, id="w-mito", video="media/wm.mp4"),
      dict(R_CAM, id="w-cam-a", video="media/wca.mp4"), dict(R_VAR, id="w-var-a", video="media/wva.mp4"),
      dict(R_CAM, id="w-cam-b", video="media/wcb.mp4")]
tmp = preparar(reels=FX, publicados=list(P4))
seq = []
for quando in ("2026-11-05T19:00:00+00:00", "2026-11-07T19:00:00+00:00", "2026-11-10T19:00:00+00:00",
               "2026-11-12T19:00:00+00:00", "2026-11-14T19:00:00+00:00"):
    rc, out, st = rodar("ok", tmp, agora=quando, extra=FN_PROD)
    seq.append(ids(st)[-1] if ids(st) else None)
checa("qui VAR (empate 0/2 x 0/1, o mais antigo), sáb e ter CÂMERA (2 para cada VAR), depois a RESERVA mais antiga",
      seq == ["w-var-a", "w-cam-a", "w-cam-b", "w-qual", "w-mito"], f"{seq}")
shutil.rmtree(tmp, ignore_errors=True)
tmp = preparar(reels=[dict(R_CAM, id="e-cam"), dict(R_MITO, id="e-mito")], publicados=P4[:3])
rc, out, st = rodar("ok", tmp, agora="2026-11-03T19:00:00+00:00", extra=FN_PROD)
checa("ESTREIA antes do peso: o Mito (nunca publicado, peso 0) sai antes da câmera lenta", ids(st)[-1:] == ["e-mito"] and rc == 0,
      f"exit={rc} {ids(st)}")
shutil.rmtree(tmp, ignore_errors=True)
tmp = preparar(reels=[dict(R_QUAL, id="v-qual")], publicados=list(P4))
rc, out, st = rodar("ok", tmp, agora="2026-11-05T19:00:00+00:00", extra=FN_PROD)
checa("vaga NUNCA vazia por causa do peso: sem câmera nem VAR, sai a reserva", ids(st)[-1:] == ["v-qual"] and rc == 0,
      f"exit={rc} {ids(st)}")
shutil.rmtree(tmp, ignore_errors=True)
tmp = preparar(reels=FX, publicados=list(P4))
rc, out, st = rodar("ok", tmp, agora="2026-11-05T19:00:00+00:00", extra=dict(FN, PESOS_FORMATOS_NOVOS="iguais"))
checa("CONTROLE: com pesos iguais a vaga de 05/11 é do formato mais antigo (o VAR também), e na de 07/11 a câmera",
      ids(st)[-1:] == ["w-var-a"], f"{ids(st)}")
rc, out, st = rodar("ok", tmp, agora="2026-11-07T19:00:00+00:00", extra=dict(FN, PESOS_FORMATOS_NOVOS="iguais"))
rc, out, st = rodar("ok", tmp, agora="2026-11-10T19:00:00+00:00", extra=dict(FN, PESOS_FORMATOS_NOVOS="iguais"))
checa("CONTROLE: com pesos iguais a 3ª vaga NÃO é câmera de novo (é a reserva mais antiga): o peso é que muda isso",
      ids(st)[-1:] == ["w-qual"], f"{ids(st)}")
shutil.rmtree(tmp, ignore_errors=True)

print("\nO) LAMINAS_POR_SEMANA ilegivel/'off' NAO derruba o motor (posts e stories seguem)")
tmp = preparar(reels=[R_LAMINA, R_CONVERSA], publicados=[LAMINA_SEG]); rc, out, st = rodar("ok", tmp, agora=QUARTA_16H, extra={"LAMINAS_POR_SEMANA": "off"})
checa("'off' = sem cota (a lamina sai)", "t-lamina-1" in ids(st), f"publicados={ids(st)}")
checa("exit == 0 com 'off'", rc == 0, f"exit={rc}")
shutil.rmtree(tmp, ignore_errors=True)
tmp = preparar(); rc, out, st = rodar("ok", tmp, extra={"LAMINAS_POR_SEMANA": "banana"})
checa("valor ilegivel: motor roda (post e sequencia saem)", len(ids(st)) >= 2 and rc == 0, f"exit={rc} publicados={ids(st)}")
checa("valor ilegivel: avisa", "LAMINAS_POR_SEMANA='banana'" in out, "warning no log")
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
    # --- FORMA REAL DA META (auditoria v1.6): a familia 2207xxx chega no error_subcode,
    #     com code generico (24 / 9007 / 9004). Payloads colhidos dos runs vermelhos
    #     33408793664 (31/08), 34042496969 (06/09) e 32043350962 (17/08).
    ("Media Not Found (code 24 / sub 2207006)", 400,
     {"error": {"type": "OAuthException", "code": 24, "error_subcode": 2207006}}, False),
    ("container nao pronto (code 9007 / sub 2207027)", 400,
     {"error": {"type": "OAuthException", "code": 9007, "error_subcode": 2207027}}, False),
    ("midia nao baixavel (code 9004 / sub 2207052)", 400,
     {"error": {"type": "OAuthException", "code": 9004, "error_subcode": 2207052}}, False),
    # --- CONTROLE: token morto continua vermelho MESMO com subcode de midia junto ---
    ("token morto + sub de midia (190 / 2207006)", 400,
     {"error": {"type": "OAuthException", "code": 190, "error_subcode": 2207006}}, True),
    # --- 500 TRANSITORIO no corpo REAL da Graph API (auditoria 24/10/2026): era AuthError pelo catch-all
    #     de OAuthException — a story pulava a consulta ao conteiner e o reel era republicado.
    ("500 transitorio REAL (OAuthException code 2, is_transient)", 500,
     {"error": {"message": "An unexpected error has occurred. Please retry your request later.",
                "type": "OAuthException", "is_transient": True, "code": 2}}, False),
    ("500 'unknown error' (OAuthException code 1)", 500,
     {"error": {"message": "An unknown error occurred", "type": "OAuthException", "code": 1}}, False),
    ("is_transient=true mesmo com HTTP 400", 400, {"error": {"type": "OAuthException", "code": 9999, "is_transient": True}}, False),
    ("code 2 (servico indisponivel) com HTTP 400", 400, {"error": {"type": "OAuthException", "code": 2}}, False),
    ("CONTROLE: token morto com HTTP 500 continua vermelho (190)", 500,
     {"error": {"type": "OAuthException", "code": 190, "error_subcode": 463}}, True),
    ("CONTROLE: 190 com is_transient continua vermelho", 400,
     {"error": {"type": "OAuthException", "code": 190, "is_transient": True}}, True),
    ("CONTROLE: OAuthException de codigo desconhecido (HTTP 400) segue o catch-all = auth", 400,
     {"error": {"type": "OAuthException", "code": 99}}, True),
    ("erro generico (500, type Exception)", 500, {"error": {"type": "Exception", "code": 1}}, False),
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
