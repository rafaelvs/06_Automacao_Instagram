#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Publicador automatico para Instagram (API oficial da Meta / Instagram Login).

Modelo BIBLIOTECA CURADA, sem repetir:
- posts.json, stories.json e reels.json sao LISTAS ORDENADAS (bibliotecas).
- Em cada janela agendada, publica o PROXIMO item ainda nao publicado (em ordem).
- Nada se repete. Quando a biblioteca acaba, o robo simplesmente nao publica
  (hora de reabastecer com conteudo novo).

Agenda (horario de Brasilia, BRT = UTC-3):
- POSTS (feed):  Ter/Qui/Sab, a partir das 19:00  -> 1 post por dia desses.
- STORIES:       TODOS OS DIAS, a partir das 12:30  -> 1 story por dia.
- REELS:         Seg/Qua/Sex/Dom, a partir das 19:00 -> 1 reel por dia desses.

Env: IG_USER_ID, IG_ACCESS_TOKEN, GITHUB_REPOSITORY, GRAPH_VERSION (opc),
     FORCE_ID (opc: publica esse id imediatamente).

NOTA — falha de AUTENTICACAO e' BARULHENTA (mesmo criterio do publish.py):
    Token/permissao vira AuthError, aborta o run, grava o que ja' saiu e sai com
    exit != 0. Este script hoje NAO e' chamado por nenhum workflow (roda a mao),
    mas mantem o mesmo comportamento do publish.py para nao surpreender quem
    recorrer a ele como fallback do fluxo diario de stories.json.

    A tabela de codigos abaixo e' uma COPIA da do publish.py (que e' a canonica e
    tem teste em test_publicacao.py secao F). Mexeu la', sincronize aqui.
"""
import os, sys, json, time, datetime as dt
import requests

POST_WEEKDAYS  = {1, 3, 5}      # Ter, Qui, Sab
POST_MIN       = 19*60          # 19:00
STORY_WEEKDAYS = {0, 1, 2, 3, 4, 5, 6}  # todos os dias
STORY_MIN      = 12*60 + 30     # 12:30
REEL_WEEKDAYS  = {0, 2, 4, 6}      # Seg, Qua, Sex, Dom
REEL_MIN       = 19*60          # 19:00
BRT = dt.timezone(dt.timedelta(hours=-3))

ROOT = os.path.dirname(os.path.abspath(__file__))
POSTS_FILE   = os.path.join(ROOT, "posts.json")
STORIES_FILE = os.path.join(ROOT, "stories.json")
REELS_FILE   = os.path.join(ROOT, "reels.json")
DESTAQUES_FILE = os.path.join(ROOT, "destaques.json")  # stories para os Destaques (FORCE_ID=destaques)
STATE_FILE   = os.path.join(ROOT, "state", "published.json")

IG_USER_ID = os.environ.get("IG_USER_ID", "").strip()
TOKEN      = os.environ.get("IG_ACCESS_TOKEN", "").strip()
REPO       = os.environ.get("GITHUB_REPOSITORY", "").strip()
REF        = os.environ.get("GITHUB_REF_NAME", "main").strip() or "main"
VER        = os.environ.get("GRAPH_VERSION", "v21.0").strip()
FORCE_ID   = os.environ.get("FORCE_ID", "").strip()
HOST       = f"https://graph.instagram.com/{VER}"

if not IG_USER_ID or not TOKEN:
    print("ERRO: defina os secrets IG_USER_ID e IG_ACCESS_TOKEN."); sys.exit(1)

class AuthError(RuntimeError):
    """Token invalido/expirado ou permissao negada. Aborta o run e sai com exit 1."""

# COPIA da tabela do publish.py (canonica, testada em test_publicacao.py secao F).
# Classificar por CODIGO, nao por type: a Meta usa OAuthException tambem em rate
# limit e em erro de midia/parametro.
AUTH_CODES     = {10, 102, 190, 2500}
AUTH_SUBCODES  = {458, 459, 460, 463, 464, 467, 492}
RATE_CODES     = {4, 17, 32, 341, 613}
CONTEUDO_CODES = {100, 352, 2207001, 2207003, 2207004, 2207005, 2207006, 2207020,
                  2207026, 2207032, 2207053}

def _e_falha_de_auth(status, payload):
    err = payload.get("error") if isinstance(payload, dict) else None
    if not isinstance(err, dict): err = {}
    code = err.get("code"); sub = err.get("error_subcode")
    if sub in AUTH_SUBCODES: return True
    if code in AUTH_CODES: return True
    if isinstance(code, int) and 200 <= code <= 299: return True
    if code in RATE_CODES or code in CONTEUDO_CODES: return False
    if isinstance(code, int) and code >= 2207000: return False
    if str(err.get("type", "")) == "OAuthException": return True
    return status in (401, 403)

def _erro_api(r, onde):
    try: payload = r.json()
    except Exception: payload = {}
    detalhe = f"{onde} -> {r.status_code}: {r.text[:300]}"
    if _e_falha_de_auth(r.status_code, payload): raise AuthError(detalhe)
    raise RuntimeError(detalhe)

def _avisar_token_parado(auth_error):
    print(f"::error::AUTENTICACAO FALHOU — token do Instagram invalido ou expirado. {auth_error}")
    print("::error::A fila esta PARADA: nada mais sera publicado ate' renovar. Gere um novo "
          "token e atualize o secret IG_ACCESS_TOKEN em rafaelvs/06_Automacao_Instagram.")
    sys.exit(1)

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
def publish_post(item):
    imgs = item["images"]; cap = item.get("caption", "")
    if len(imgs) == 1:
        cont = api_post(f"{IG_USER_ID}/media", {"image_url": raw_url(imgs[0]), "caption": cap})["id"]
    else:
        kids = [api_post(f"{IG_USER_ID}/media", {"image_url": raw_url(p), "is_carousel_item": "true"})["id"] for p in imgs]
        cont = api_post(f"{IG_USER_ID}/media", {"media_type": "CAROUSEL", "children": ",".join(kids), "caption": cap})["id"]
    wait_finished(cont)
    return api_post(f"{IG_USER_ID}/media_publish", {"creation_id": cont})["id"]
def publish_story(item):
    cont = api_post(f"{IG_USER_ID}/media", {"image_url": raw_url(item["image"]), "media_type": "STORIES"})["id"]
    wait_finished(cont)
    return api_post(f"{IG_USER_ID}/media_publish", {"creation_id": cont})["id"]
def publish_reel(item):
    # Reel: video_url publico (raw do GitHub). share_to_feed mostra tambem no feed.
    cont = api_post(f"{IG_USER_ID}/media", {
        "media_type": "REELS", "video_url": raw_url(item["video"]),
        "caption": item.get("caption", ""), "share_to_feed": "true"})["id"]
    wait_finished(cont, tries=30, delay=10)   # video demora mais p/ processar
    return api_post(f"{IG_USER_ID}/media_publish", {"creation_id": cont})["id"]
def log(state, item, kind, mid, now): state["published"].append({"id": item["id"], "kind": kind, "media_id": mid, "at": now.isoformat()})
def next_item(items, done): return next((x for x in items if x["id"] not in done), None)

def main():
    posts   = load_json(POSTS_FILE, [])
    stories = load_json(STORIES_FILE, [])
    reels   = load_json(REELS_FILE, [])
    state = load_json(STATE_FILE, {"published": [], "last_post_date": "", "last_story_date": "", "last_reel_date": ""})
    state.setdefault("published", []); state.setdefault("last_post_date", ""); state.setdefault("last_story_date", ""); state.setdefault("last_reel_date", "")
    done = {e["id"] for e in state["published"]}
    now = dt.datetime.now(dt.timezone.utc); brt = now.astimezone(BRT); today = brt.date().isoformat()
    mod = brt.hour*60 + brt.minute; changed = False
    auth_error = None   # token morto: para tudo, grava o que saiu e sai com exit 1

    if FORCE_ID == "destaques":
        for it in load_json(DESTAQUES_FILE, []):
            try:
                mid = publish_story(it); log(state, it, "story", mid, now); changed = True
                print(f"Destaque {it['id']} OK -> {mid}")
            except AuthError as e: auth_error = e; break
            except Exception as e: print(f"FALHA destaque {it['id']}: {e}")
        if changed: save_state(state)
        if auth_error: _avisar_token_parado(auth_error)
        return

    if FORCE_ID:
        it = next((x for x in posts if x["id"] == FORCE_ID), None); kind = "post"
        if it is None:
            it = next((x for x in stories if x["id"] == FORCE_ID), None); kind = "story"
        if it is None:
            it = next((x for x in reels if x["id"] == FORCE_ID), None); kind = "reel"
        if it is None: print(f"FORCE_ID={FORCE_ID}: nao encontrado."); return
        try:
            mid = publish_post(it) if kind == "post" else (publish_story(it) if kind == "story" else publish_reel(it))
            log(state, it, kind, mid, now); save_state(state); print(f"FORCE {FORCE_ID} OK -> {mid}")
        except AuthError as e: _avisar_token_parado(e)
        except Exception as e: print(f"FORCE {FORCE_ID} FALHA: {e}")
        return

    # POSTS (feed)
    if brt.weekday() in POST_WEEKDAYS and mod >= POST_MIN and state["last_post_date"] != today:
        it = next_item(posts, done)
        if it:
            try:
                mid = publish_post(it); log(state, it, "post", mid, now)
                done.add(it["id"]); state["last_post_date"] = today; changed = True
                print(f"Post {it['id']} OK -> {mid}")
            except AuthError as e: auth_error = e
            except Exception as e: print(f"FALHA post {it['id']}: {e}")
        else:
            print("Biblioteca de POSTS esgotada — hora de reabastecer.")

    # STORIES
    if not auth_error and brt.weekday() in STORY_WEEKDAYS and mod >= STORY_MIN and state["last_story_date"] != today:
        it = next_item(stories, done)
        if it:
            try:
                mid = publish_story(it); log(state, it, "story", mid, now)
                done.add(it["id"]); state["last_story_date"] = today; changed = True
                print(f"Story {it['id']} OK -> {mid}")
            except AuthError as e: auth_error = e
            except Exception as e: print(f"FALHA story {it['id']}: {e}")
        else:
            print("Biblioteca de STORIES esgotada — hora de reabastecer.")

    # REELS
    if not auth_error and brt.weekday() in REEL_WEEKDAYS and mod >= REEL_MIN and state["last_reel_date"] != today:
        it = next_item(reels, done)
        if it:
            try:
                mid = publish_reel(it); log(state, it, "reel", mid, now)
                done.add(it["id"]); state["last_reel_date"] = today; changed = True
                print(f"Reel {it['id']} OK -> {mid}")
            except AuthError as e: auth_error = e
            except Exception as e: print(f"FALHA reel {it['id']}: {e}")
        else:
            print("Biblioteca de REELS esgotada — hora de reabastecer.")

    # Grava o estado ANTES de sair com erro, para nao reperder o que ja' foi publicado.
    if changed: save_state(state); print("Estado atualizado.")
    elif not auth_error: print("Nada a publicar agora.")

    if auth_error: _avisar_token_parado(auth_error)

if __name__ == "__main__":
    main()
