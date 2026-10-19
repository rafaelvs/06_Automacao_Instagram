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
    data = data or {}
    # denuncia os parametros de audiencia emprestada / trial (cenarios G/H) e o CONTROLE:
    # story NUNCA pode levar collaborators (a API nao aceita).
    if "collaborators" in data:
        print("COLLAB_ENVIADO", data["collaborators"], "media_type=", data.get("media_type", "IMAGE"))
    if "trial_params" in data:
        print("TRIAL_PARAMS", data["trial_params"])
    if "is_ai_generated" in data:
        print("ROTULO_IA", data["is_ai_generated"], "media_type=", data.get("media_type", "IMAGE"))
    return R(200, {"id": "CONT001"})
def fake_get(url, params=None, timeout=None, **kw):
    r = _falha()
    if r is not None: return r
    params = params or {}
    if url.endswith("/media") and "like_count" in str(params.get("fields", "")):
        # leitura do ALARME de curtidas (B6-iii): 6 pecas do feed
        likes = 0 if CENARIO == "alarme_zero" else 1
        return R(200, {"data": [{"id": "M%d" % i, "like_count": likes, "media_product_type": "FEED"}
                                for i in range(6)]})
    return R(200, {"status_code": "FINISHED"})
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
    for f in ["publish.py", "cfm_guardrails.py", "regra_reels.py"]:
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
    env.pop("CONVERSAS_POR_SEMANA", None)
    if agora:
        env["FAKE_NOW"] = agora
    env.update({"IG_USER_ID": "1784", "IG_ACCESS_TOKEN": "fake",
                "GITHUB_REPOSITORY": "rafaelvs/06_Automacao_Instagram",
                "FORCE_ID": force_id, "LOCATION_ID": "", "TRIAL_REELS": "false",
                "ALARME_CURTIDAS": "on", "ALARME_N_PECAS": "6",
                "PYTHONUTF8": "1", "PYTHONIOENCODING": "utf-8"})
    env.update(extra or {})
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
checa("mensagem de cota (nao 'esgotada')", "cota de 1 lamina" in out and "esgotada" not in out.split("REELS")[-1], "texto certo no log")
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

print("\nP) COTA DE CONVERSA (19/10/2026, 'vez ou outra'): conversa ja saiu na semana -> pula a conversa, sai o COMO FUNCIONA")
R_CONVERSA2 = {"id": "t-conversa-2", "video": "media/c2.mp4", "caption": CAP_IA, "formato": "conversa"}
R_CF = {"id": "t-cf-1", "video": "media/f1.mp4", "caption": CAP_IA, "formato": "como_funciona"}
CONVERSA_SEG_P = {"id": "t-conversa-0", "kind": "reel", "media_id": "M8", "at": "2026-07-27T18:30:00+00:00", "formato": "conversa"}
tmp = preparar(reels=[R_CONVERSA2, R_CF], publicados=[CONVERSA_SEG_P]); rc, out, st = rodar("ok", tmp, agora=QUARTA_16H)
checa("publicou o COMO FUNCIONA, nao a 2a conversa da semana", "t-cf-1" in ids(st) and "t-conversa-2" not in ids(st), f"publicados={ids(st)}")
checa("exit == 0", rc == 0, f"exit={rc}")
shutil.rmtree(tmp, ignore_errors=True)
tmp = preparar(reels=[R_CONVERSA2], publicados=[CONVERSA_SEG_P]); rc, out, st = rodar("ok", tmp, agora=QUARTA_16H)
checa("so conversa na fila e cota cheia -> sem reel, sem erro", "t-conversa-2" not in ids(st) and rc == 0 and "::error::" not in out, f"exit={rc} publicados={ids(st)}")
checa("mensagem cita as cotas", "conversa(s) por semana cumprida" in out, "texto no log")
shutil.rmtree(tmp, ignore_errors=True)
CONVERSA_SEMANA_PASSADA = dict(CONVERSA_SEG_P, at="2026-07-25T18:30:00+00:00")
tmp = preparar(reels=[R_CONVERSA2, R_CF], publicados=[CONVERSA_SEMANA_PASSADA]); rc, out, st = rodar("ok", tmp, agora=QUARTA_16H)
checa("controle: conversa so na semana anterior -> a conversa da frente sai", "t-conversa-2" in ids(st), f"publicados={ids(st)}")
shutil.rmtree(tmp, ignore_errors=True)
tmp = preparar(reels=[R_CONVERSA2, R_CF], publicados=[CONVERSA_SEG_P]); rc, out, st = rodar("ok", tmp, agora=QUARTA_16H, extra={"CONVERSAS_POR_SEMANA": "-1"})
checa("CONVERSAS_POR_SEMANA=-1 desliga a cota", "t-conversa-2" in ids(st), f"publicados={ids(st)}")
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
