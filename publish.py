#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Publicador automatico para Instagram (API oficial da Meta / Instagram Login).

Modelo BIBLIOTECA CURADA, sem repetir:
- posts.json e reels.json sao listas (bibliotecas) — 1 item por janela.
- sequences.json e a nova STORY SERIALIZADA: cada item e 1 DIA = sequencia de 5 frames,
  publicados EM BLOCO (um story atras do outro) na janela diaria.
- Nada se repete. Quando a biblioteca acaba, o robo nao publica (hora de reabastecer).

Agenda (horario de Brasilia, BRT = UTC-3):
- POSTS (feed):  Ter/Qui/Sab, a partir das 15:00.  (pico de audiencia 12h-15h; ver auditoria jun/2026)
- STORIES (seq): TODOS OS DIAS, a partir das 12:30  -> 1 sequencia (5 frames) por dia.
- REELS:         Seg/Qua/Sex/Dom, a partir das 15:00.  (pico de audiencia; antes era 19:00, na descida)

Env: IG_USER_ID, IG_ACCESS_TOKEN, GITHUB_REPOSITORY, GRAPH_VERSION (opc),
     FORCE_ID (opc: publica esse id imediatamente - post, story, reel ou sequencia).

NOTA — falha de AUTENTICACAO e' BARULHENTA (nao silenciosa):
    O token da Meta (renovado a cada ~60 dias) e' o ponto unico de falha do motor.
    Ate 07/2026 um `except Exception` engolia o erro, o main() retornava normal e o
    job do Actions terminava VERDE — a fila pararia sem ninguem perceber. Agora um
    erro de auth vira `AuthError`, o robo para de tentar (o token vale para todos os
    itens), grava o que ja' saiu e sai com exit != 0, deixando o job VERMELHO — que
    e' o que dispara a notificacao do GitHub.

    CUIDADO ao mexer aqui: a Meta devolve HTTP **400** (nao 401) com
    type=OAuthException / code=190 quando o token expira, entao NAO da' para decidir
    so' pelo status HTTP. E os codigos de rate limit (4, 17, 32...) tambem vem como
    OAuthException — esses sao transitorios e NAO podem derrubar o job.

NOTA — por que NAO existe um limite de itens por execucao aqui:
    O robo do LinkedIn tem LINKEDIN_MAX_PER_RUN porque la' os posts tem horario
    marcado e se acumulam como "vencidos" enquanto a publicacao esta travada. Aqui a
    fila e' uma BIBLIOTECA e cada bloco publica no maximo 1 item por dia-calendario
    (guarda `last_*_date != today`). Se o token ficar morto 10 dias, a volta publica
    1 post, nao 10 — a recuperacao ja' e' gradual por construcao. Um limite global
    de 1/execucao seria ate' NOCIVO: no domingo saem legitimamente carrossel + reel.
"""
import os, sys, json, time, datetime as dt
import requests

POST_WEEKDAYS  = {1, 3, 5}
POST_MIN       = 15*60                   # 15:00 BRT (pico de audiencia; era 19:00)
POST2_WEEKDAYS = {6}                     # 4o carrossel/sem (feed 8/sem) — dia-duplo c/ Reel no domingo
POST2_MIN      = 11*60                   # 11:00 BRT — escalonado p/ nao colidir com o Reel das 15h
SEQ_WEEKDAYS   = {0, 1, 2, 3, 4, 5, 6}   # sequencia diaria
SEQ_MIN        = 12*60 + 30              # 12:30
REEL_WEEKDAYS  = {0, 2, 4, 6}
REEL_MIN       = 15*60                   # 15:00 BRT (pico de audiencia; era 19:00)
BRT = dt.timezone(dt.timedelta(hours=-3))

ROOT = os.path.dirname(os.path.abspath(__file__))
POSTS_FILE   = os.path.join(ROOT, "posts.json")
STORIES_FILE = os.path.join(ROOT, "stories.json")
SEQ_FILE     = os.path.join(ROOT, "sequences.json")
REELS_FILE   = os.path.join(ROOT, "reels.json")
DESTAQUES_FILE = os.path.join(ROOT, "destaques.json")
STATE_FILE   = os.path.join(ROOT, "state", "published.json")
TOKEN_STATE_FILE = os.path.join(ROOT, "state", "token_refresh.json")  # escrito por refresh_token.py
AVISO_EXPIRACAO_DIAS = 14   # a renovacao roda toda segunda: 14 dias = ~2 tentativas de folga

IG_USER_ID = os.environ.get("IG_USER_ID", "").strip()
TOKEN      = os.environ.get("IG_ACCESS_TOKEN", "").strip()
REPO       = os.environ.get("GITHUB_REPOSITORY", "").strip()
REF        = os.environ.get("GITHUB_REF_NAME", "main").strip() or "main"
VER        = os.environ.get("GRAPH_VERSION", "v21.0").strip()
FORCE_ID   = os.environ.get("FORCE_ID", "").strip()
LOCATION_ID = os.environ.get("LOCATION_ID", "").strip()   # SEO local: place id (SP). Inerte se vazio.
# Trial Reels: publica o reel so' para NAO-seguidores (alcance de descoberta); graduacao
# SS_PERFORMANCE promove sozinho aos seguidores se performar (sem passo manual). Default OFF.
TRIAL_REELS = os.environ.get("TRIAL_REELS", "false").strip().lower() in ("1", "true", "yes", "sim")
TRIAL_GRADUATION = os.environ.get("TRIAL_GRADUATION", "").strip() or "SS_PERFORMANCE"  # vazio -> default; SS_PERFORMANCE | MANUAL
HOST       = f"https://graph.instagram.com/{VER}"

if not IG_USER_ID or not TOKEN:
    print("ERRO: defina os secrets IG_USER_ID e IG_ACCESS_TOKEN."); sys.exit(1)

class AuthError(RuntimeError):
    """Token invalido/expirado ou permissao negada. Aborta o run e faz o job ficar
    VERMELHO, em vez de sair verde com a fila parada."""

# Quase TUDO na Meta chega com type=OAuthException — inclusive rate limit e erro de
# midia. Por isso a classificacao e' por CODIGO, nao pelo type.
# 1) Token/permissao: nao adianta tentar de novo, precisa de humano.
AUTH_CODES     = {10, 102, 190, 2500}
AUTH_SUBCODES  = {458, 459, 460, 463, 464, 467, 492}
# 2) Throttling: transitorio, o proximo disparo do cron resolve sozinho.
RATE_CODES     = {4, 17, 32, 341, 613}
# 3) Parametro/midia invalida: problema DAQUELE item, nao do token. O robo loga e
#    segue para os outros blocos (um reel corrompido nao pode travar a sequencia do dia).
CONTEUDO_CODES = {100, 352, 2207001, 2207003, 2207004, 2207005, 2207006, 2207020,
                  2207026, 2207032, 2207053}

def _e_falha_de_auth(status, payload):
    # corpo pode vir vazio/HTML/lista (erro de gateway): nunca confiar no formato
    err = payload.get("error") if isinstance(payload, dict) else None
    if not isinstance(err, dict): err = {}
    code = err.get("code"); sub = err.get("error_subcode")
    if sub in AUTH_SUBCODES: return True
    if code in AUTH_CODES: return True
    if isinstance(code, int) and 200 <= code <= 299: return True    # familia de permissao
    if code in RATE_CODES or code in CONTEUDO_CODES: return False
    if isinstance(code, int) and code >= 2207000: return False      # erros de container/midia
    if str(err.get("type", "")) == "OAuthException": return True
    return status in (401, 403)

def _erro_api(r, onde):
    """Resposta >=400 vira excecao: AuthError se for token/permissao (aborta tudo),
    RuntimeError no resto (o robo tolera e tenta o proximo bloco)."""
    try: payload = r.json()
    except Exception: payload = {}
    detalhe = f"{onde} -> {r.status_code}: {r.text[:300]}"
    if _e_falha_de_auth(r.status_code, payload): raise AuthError(detalhe)
    raise RuntimeError(detalhe)

def _avisar_token_parado(auth_error):
    """Mensagem unica de encerramento quando o token morre. Sai com exit 1 para o
    job ficar vermelho (o estado ja' foi gravado pelo chamador)."""
    print(f"::error::AUTENTICACAO FALHOU — token do Instagram invalido ou expirado. {auth_error}")
    print("::error::A fila esta PARADA: nada mais sera publicado ate' renovar. Gere um novo "
          "token e atualize o secret IG_ACCESS_TOKEN em rafaelvs/06_Automacao_Instagram.")
    sys.exit(1)

def _falhou(falhas, rotulo, erro):
    """Registra falha NAO-auth de um item, de forma BARULHENTA.

    Ate 07/2026 estas falhas saiam por `print` puro: o main() retornava normal e o job
    ficava VERDE. Como o item que falha NAO entra em `done` nem avanca `last_*_date`, o
    cron (*/30) repetia o MESMO item para sempre — inclusive o `RuntimeError` do
    guardrail CFM (`BLOQUEADO CFM`), que e' permanente por definicao e NUNCA se resolve
    sozinho. Resultado: fila parada em silencio, com o painel todo verde.

    Agora cada falha sai como `::error::` (anotacao visivel no Actions) e o main()
    devolve a lista para o processo sair com exit 1 — espelhando o caminho do AuthError.
    O passo "Salvar estado" do publish.yml tem `if: always()`, entao o que JA' foi ao ar
    continua sendo commitado normalmente: ficar vermelho nao faz republicar."""
    print(f"::error::FALHA {rotulo}: {erro}")
    falhas.append(f"{rotulo} ({type(erro).__name__})")

def _avisar_validade_do_token():
    """Aviso preventivo de expiracao DENTRO do motor.

    Ate 07/2026 o unico alarme de expiracao vivia fora do repo (uma tarefa agendada no
    PC do Rafael). Se o refresh-token.yml falha — como falhou desde sempre, por falta do
    secret GH_SECRETS_PAT — nada aqui dentro reclamava ate' o token simplesmente morrer.
    Isto le' o rastro deixado por refresh_token.py e avisa ANTES. Nunca bloqueia: e' so'
    um ::warning:: (o job segue verde), porque publicar ainda funciona ate' a expiracao."""
    # Leitura propria (nao load_json): um JSON corrompido aqui levantaria ValueError e
    # derrubaria a publicacao inteira por causa de um aviso COSMETICO. Fail-open sempre.
    try:
        with open(TOKEN_STATE_FILE, encoding="utf-8") as fh:
            estado = json.load(fh)
    except (OSError, ValueError):
        estado = None
    if not isinstance(estado, dict) or not estado.get("expira_em"):
        print("::warning::Sem registro de renovacao do token (state/token_refresh.json ausente). "
              "A renovacao automatica pode nunca ter rodado — confira o workflow refresh-token.yml.")
        return
    try:
        expira = dt.date.fromisoformat(estado["expira_em"])
    except (TypeError, ValueError):
        print("::warning::state/token_refresh.json tem 'expira_em' ilegivel — nao da' para conferir a validade.")
        return
    dias = (expira - dt.datetime.now(BRT).date()).days
    if dias <= AVISO_EXPIRACAO_DIAS:
        print(f"::warning::Token do Instagram expira em {dias} dia(s) ({expira:%d/%m/%Y}). "
              "Se o refresh-token.yml nao voltar a rodar verde, a fila para nessa data.")

def raw_url(path):
    if not REPO: raise RuntimeError("GITHUB_REPOSITORY nao definido (rode no GitHub Actions).")
    return f"https://raw.githubusercontent.com/{REPO}/{REF}/{path}"
def load_json(p, d):
    try:
        with open(p, encoding="utf-8") as f: return json.load(f)
    except FileNotFoundError: return d
def save_state(s):
    os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
    with open(STATE_FILE, "w", encoding="utf-8") as f: json.dump(s, f, ensure_ascii=False, indent=2)
def api_post(path, data):
    data = dict(data); data["access_token"] = TOKEN
    r = requests.post(f"{HOST}/{path}", data=data, timeout=120)
    if r.status_code >= 400: _erro_api(r, f"POST {path}")
    return r.json()
def api_get(path, params):
    params = dict(params); params["access_token"] = TOKEN
    r = requests.get(f"{HOST}/{path}", params=params, timeout=60)
    if r.status_code >= 400: _erro_api(r, f"GET {path}")
    return r.json()
def wait_finished(cid, tries=10, delay=6):
    for _ in range(tries):
        st = api_get(cid, {"fields": "status_code"}).get("status_code")
        if st == "FINISHED": return True
        if st in ("ERROR", "EXPIRED"): raise RuntimeError(f"Container {cid} status {st}")
        time.sleep(delay)
    return True
def _alt(item):
    """Alt-text (acessibilidade + SEO de imagem): usa item['alt'] ou a 1a linha da legenda
    (que e' keyword-forward). API suporta alt_text em imagens desde mar/2025."""
    a = (item.get("alt") or "").strip()
    if not a:
        a = (item.get("caption", "") or "").strip().split("\n", 1)[0].strip()
    return a[:100]

def _loc(d):
    """Adiciona location_id (SEO local) ao payload se LOCATION_ID estiver definido. No-op se vazio."""
    if LOCATION_ID:
        d = dict(d); d["location_id"] = LOCATION_ID
    return d

def _cfm_guard(item):
    """Backstop CFM antes de publicar. Se o MODULO estiver ausente: avisa ALTO e nao bloqueia
    (fail-open RUIDOSO — nao quebra o robo). Se o modulo existir mas tiver bug (SyntaxError/re.error):
    a excecao propaga -> o try/except do chamador trata como FALHA (fail-CLOSED: nao publica, nao marca
    done). Se houver VIOLACAO de CFM: loga marcador distinto 'BLOQUEADO CFM' e levanta RuntimeError
    (o chamador pula o item e NAO avanca, forcando revisao humana). Conteudo limpo passa direto."""
    try:
        from cfm_guardrails import auditar
    except (ImportError, ModuleNotFoundError):
        print("!!! ALERTA: cfm_guardrails ausente — guardrail CFM DESLIGADO neste run.", file=sys.stderr)
        return
    viol = [p for p in auditar(item.get("caption", ""), "publico") if p[0] == "VIOLACAO"]
    if viol:
        msg = "BLOQUEADO CFM: " + "; ".join(f"{r}:{d}" for _, r, d in viol)
        print(f"!!! {msg} (item={item.get('id', '?')}) — NAO publicado, revisar.", file=sys.stderr)
        raise RuntimeError(msg)

def publish_post(item):
    _cfm_guard(item)
    imgs = item["images"]; cap = item.get("caption", ""); alt = _alt(item)
    if len(imgs) == 1:
        cont = api_post(f"{IG_USER_ID}/media", _loc({"image_url": raw_url(imgs[0]), "caption": cap, "alt_text": alt}))["id"]
    else:
        # alt_text por filho do carrossel (verificar no 1o publish real; se a API recusar, remover dos filhos).
        kids = [api_post(f"{IG_USER_ID}/media", {"image_url": raw_url(p), "is_carousel_item": "true", "alt_text": alt})["id"] for p in imgs]
        cont = api_post(f"{IG_USER_ID}/media", _loc({"media_type": "CAROUSEL", "children": ",".join(kids), "caption": cap}))["id"]
    wait_finished(cont)
    return api_post(f"{IG_USER_ID}/media_publish", {"creation_id": cont})["id"]
def publish_story_img(image_path):
    cont = api_post(f"{IG_USER_ID}/media", {"image_url": raw_url(image_path), "media_type": "STORIES"})["id"]
    wait_finished(cont)
    return api_post(f"{IG_USER_ID}/media_publish", {"creation_id": cont})["id"]
def publish_story(item):
    return publish_story_img(item["image"])
def publish_sequence(seq):
    # publica os 5 frames em ordem, um atras do outro (story serializado)
    ids = []
    for i, img in enumerate(seq["images"], 1):
        mid = publish_story_img(img); ids.append(mid)
        print(f"  frame {i}/{len(seq['images'])} -> {mid}", flush=True)
        time.sleep(2)
    return ids
# Ramo que a ultima publicacao de reel tomou. Vai para o state (ver log()).
# Sem isto ninguem consegue provar POR DADO se um reel saiu em modo trial: o fallback
# abaixo e' silencioso e a Graph API nao expoe o status de trial na leitura da midia.
# Foi essa cegueira que deixou 19 reels publicados fora do grid de 22/06 a 24/07/2026
# sem que nenhuma auditoria conseguisse confirmar a causa. Ver docs/06_TRIAL_REELS.md.
_MODO_REEL = None   # "trial" | "fallback_normal" | "normal"


def publish_reel(item):
    global _MODO_REEL
    _cfm_guard(item)
    # alt_text NAO e' suportado em reels (so imagens); location_id e' suportado.
    base = _loc({"media_type": "REELS", "video_url": raw_url(item["video"]),
                 "caption": item.get("caption", "")})
    cont = None
    _MODO_REEL = "normal"
    if TRIAL_REELS:
        # Trial Reel: so' para nao-seguidores; graduacao automatica (SS_PERFORMANCE) se performar.
        try:
            p = dict(base); p["trial_params"] = json.dumps({"graduation_strategy": TRIAL_GRADUATION})
            cont = api_post(f"{IG_USER_ID}/media", p)["id"]
            _MODO_REEL = "trial"
        except AuthError:
            # Token morto nao e' "trial_params recusado": propaga, senao este except
            # engoliria a falha de auth e o robo tentaria de novo a' toa.
            raise
        except RuntimeError as e:
            # Fallback robusto: se a API recusar trial_params, publica reel normal (nao trava o robo).
            print(f"  ! trial_params recusado ({e}); publicando como reel normal.", file=sys.stderr)
            cont = None
            _MODO_REEL = "fallback_normal"
    if cont is None:
        p = dict(base); p["share_to_feed"] = "true"
        cont = api_post(f"{IG_USER_ID}/media", p)["id"]
    wait_finished(cont, tries=30, delay=10)
    return api_post(f"{IG_USER_ID}/media_publish", {"creation_id": cont})["id"]
def log(state, item_id, kind, mid, now):
    reg = {"id": item_id, "kind": kind, "media_id": mid, "at": now.isoformat()}
    if kind == "reel" and _MODO_REEL:
        # Prova por dado de qual ramo publicou (trial / fallback / normal). A auditoria v1
        # nao conseguiu confirmar isso em 18 reels de julho porque nada era gravado.
        reg["modo_reel"] = _MODO_REEL
        print(f"  modo do reel: {_MODO_REEL}", flush=True)
    state["published"].append(reg)
def next_item(items, done): return next((x for x in items if x["id"] not in done), None)

def main():
    posts   = load_json(POSTS_FILE, [])
    stories = load_json(STORIES_FILE, [])
    seqs    = load_json(SEQ_FILE, [])
    reels   = load_json(REELS_FILE, [])
    state = load_json(STATE_FILE, {"published": [], "last_post_date": "", "last_seq_date": "", "last_reel_date": ""})
    state.setdefault("published", []); state.setdefault("last_post_date", ""); state.setdefault("last_seq_date", ""); state.setdefault("last_reel_date", "")
    done = {e["id"] for e in state["published"]}
    now = dt.datetime.now(dt.timezone.utc); brt = now.astimezone(BRT); today = brt.date().isoformat()
    mod = brt.hour*60 + brt.minute; changed = False
    auth_error = None   # token morto: para tudo, grava o que saiu e sai com exit 1
    falhas = []         # falhas NAO-auth: o run termina VERMELHO (ver _falhou)

    _avisar_validade_do_token()

    if FORCE_ID == "destaques":
        for it in load_json(DESTAQUES_FILE, []):
            try:
                mid = publish_story(it); log(state, it["id"], "story", mid, now); changed = True
                print(f"Destaque {it['id']} OK -> {mid}")
            except AuthError as e: auth_error = e; break
            except Exception as e: _falhou(falhas, f"destaque {it['id']}", e)
        if changed: save_state(state)
        if auth_error: _avisar_token_parado(auth_error)
        return falhas

    if FORCE_ID:
        it = next((x for x in posts if x["id"] == FORCE_ID), None); kind = "post"
        if it is None:
            it = next((x for x in seqs if x["id"] == FORCE_ID), None); kind = "seq"
        if it is None:
            it = next((x for x in stories if x["id"] == FORCE_ID), None); kind = "story"
        if it is None:
            it = next((x for x in reels if x["id"] == FORCE_ID), None); kind = "reel"
        if it is None:
            # FORCE_ID digitado errado tambem e' falha: antes saia verde sem publicar nada.
            _falhou(falhas, f"FORCE_ID={FORCE_ID}", ValueError("id nao encontrado em nenhuma biblioteca"))
            return falhas
        try:
            if kind == "post": mid = publish_post(it)
            elif kind == "seq": mid = publish_sequence(it)[0]
            elif kind == "story": mid = publish_story(it)
            else: mid = publish_reel(it)
            log(state, it["id"], kind, mid, now); save_state(state); print(f"FORCE {FORCE_ID} OK -> {mid}")
        except AuthError as e: _avisar_token_parado(e)
        except Exception as e: _falhou(falhas, f"FORCE {FORCE_ID}", e)
        return falhas

    # POSTS (feed)
    if brt.weekday() in POST_WEEKDAYS and mod >= POST_MIN and state["last_post_date"] != today:
        it = next_item(posts, done)
        if it:
            try:
                mid = publish_post(it); log(state, it["id"], "post", mid, now)
                done.add(it["id"]); state["last_post_date"] = today; changed = True
                print(f"Post {it['id']} OK -> {mid}")
            except AuthError as e: auth_error = e
            except Exception as e: _falhou(falhas, f"post {it['id']}", e)
        else:
            print("Biblioteca de POSTS esgotada — hora de reabastecer.")

    # CARROSSEL EXTRA (4o/sem) — dia-duplo com o Reel; horario escalonado (11h) p/ nao colidir
    if not auth_error and brt.weekday() in POST2_WEEKDAYS and mod >= POST2_MIN and state["last_post_date"] != today:
        it = next_item(posts, done)
        if it:
            try:
                mid = publish_post(it); log(state, it["id"], "post", mid, now)
                done.add(it["id"]); state["last_post_date"] = today; changed = True
                print(f"Post extra {it['id']} OK -> {mid}")
            except AuthError as e: auth_error = e
            except Exception as e: _falhou(falhas, f"post extra {it['id']}", e)
        else:
            print("Biblioteca de POSTS esgotada (extra) — hora de reabastecer.")

    # SEQUENCIA DIARIA (story serializado, 5 frames)
    if not auth_error and brt.weekday() in SEQ_WEEKDAYS and mod >= SEQ_MIN and state["last_seq_date"] != today:
        it = next_item(seqs, done)
        if it:
            try:
                print(f"Sequencia {it['id']} ({it.get('theme','')}) — publicando {len(it['images'])} frames...")
                ids = publish_sequence(it); log(state, it["id"], "seq", ids[0], now)
                done.add(it["id"]); state["last_seq_date"] = today; changed = True
                print(f"Sequencia {it['id']} OK -> {len(ids)} frames")
            except AuthError as e: auth_error = e
            except Exception as e: _falhou(falhas, f"sequencia {it['id']}", e)
        else:
            print("Biblioteca de SEQUENCIAS esgotada — hora de reabastecer.")

    # REELS
    if not auth_error and brt.weekday() in REEL_WEEKDAYS and mod >= REEL_MIN and state["last_reel_date"] != today:
        it = next_item(reels, done)
        if it:
            try:
                mid = publish_reel(it); log(state, it["id"], "reel", mid, now)
                done.add(it["id"]); state["last_reel_date"] = today; changed = True
                print(f"Reel {it['id']} OK -> {mid}")
            except AuthError as e: auth_error = e
            except Exception as e: _falhou(falhas, f"reel {it['id']}", e)
        else:
            print("Biblioteca de REELS esgotada — hora de reabastecer.")

    # Grava o estado ANTES de sair com erro, para nao reperder o que ja' foi publicado
    # quando o token morre no meio da execucao.
    if changed: save_state(state); print("Estado atualizado.")
    elif not auth_error and not falhas: print("Nada a publicar agora.")

    if auth_error: _avisar_token_parado(auth_error)
    return falhas

if __name__ == "__main__":
    # O exit code vive AQUI, nao dentro do main(), para que todo caminho de saida
    # (inclusive os `return` antecipados do FORCE_ID) passe pelo mesmo veredito.
    _falhas = main() or []
    if _falhas:
        print(f"::error::{len(_falhas)} item(ns) falharam SEM publicar: {'; '.join(_falhas)}")
        print("::error::Item que falha nao entra em `done`: o cron (*/30) vai RETENTAR o mesmo "
              "item indefinidamente. Se for 'BLOQUEADO CFM', a fila NAO anda sozinha — "
              "corrija ou remova o item (docs/02_RUNBOOK.md).")
        sys.exit(1)
