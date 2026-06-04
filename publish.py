#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Publicador automatico para Instagram (API oficial da Meta / Instagram Login).

Modelo BIBLIOTECA CURADA, sem repetir:
- posts.json e stories.json sao LISTAS ORDENADAS (bibliotecas).
- Em cada janela agendada, publica o PROXIMO item ainda nao publicado (em ordem).
- Nada se repete. Quando a biblioteca acaba, o robo simplesmente nao publica
  (hora de reabastecer com conteudo novo).

Agenda (horario de Brasilia, BRT = UTC-3):
- POSTS (feed):  Ter/Qui/Sab, a partir das 19:00  -> 1 post por dia desses.
- STORIES:       Seg/Qua/Sex, a partir das 12:30  -> 1 story por dia desses.

Env: IG_USER_ID, IG_ACCESS_TOKEN, GITHUB_REPOSITORY, GRAPH_VERSION (opc),
     FORCE_ID (opc: publica esse id imediatamente).
"""
import os, sys, json, time, datetime as dt
import requests

POST_WEEKDAYS  = {1, 3, 5}      # Ter, Qui, Sab
POST_MIN       = 18*60 + 30     # 18:30
STORY_WEEKDAYS = {0, 2, 4}      # Seg, Qua, Sex
STORY_MIN      = 12*60          # 12:00
BRT = dt.timezone(dt.timedelta(hours=-3))

ROOT = os.path.dirname(os.path.abspath(__file__))
POSTS_FILE   = os.path.join(ROOT, "posts.json")
STORIES_FILE = os.path.join(ROOT, "stories.json")
DESTAQUES_FILE = os.path.join(ROOT, "destaques.json")  # stories para os Destaques (publicar com FORCE_ID=destaques)
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
    r = requests.post(f"{HOST}/{path}", data=data, timeout=60)
    if r.status_code >= 400: raise RuntimeError(f"POST {path} -> {r.status_code}: {r.text}")
    return r.json()
def api_get(path, params):
    params = dict(params); params["access_token"] = TOKEN
    r = requests.get(f"{HOST}/{path}", params=params, timeout=60)
    if r.status_code >= 400: raise RuntimeError(f"GET {path} -> {r.status_code}: {r.text}")
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
def log(state, item, kind, mid, now): state["published"].append({"id": item["id"], "kind": kind, "media_id": mid, "at": now.isoformat()})
def next_item(items, done): return next((x for x in items if x["id"] not in done), None)

def main():
    posts   = load_json(POSTS_FILE, [])
    stories = load_json(STORIES_FILE, [])
    state = load_json(STATE_FILE, {"published": [], "last_post_date": "", "last_story_date": ""})
    state.setdefault("published", []); state.setdefault("last_post_date", ""); state.setdefault("last_story_date", "")
    done = {e["id"] for e in state["published"]}
    now = dt.datetime.now(dt.timezone.utc); brt = now.astimezone(BRT); today = brt.date().isoformat()
    mod = brt.hour*60 + brt.minute; changed = False

    if FORCE_ID == "destaques":
        for it in load_json(DESTAQUES_FILE, []):
            try:
                mid = publish_story(it); log(state, it, "story", mid, now); changed = True
                print(f"Destaque {it['id']} OK -> {mid}")
            except Exception as e: print(f"FALHA destaque {it['id']}: {e}")
        if changed: save_state(state)
        return

    if FORCE_ID:
        it = next((x for x in posts if x["id"] == FORCE_ID), None)
        kind = "post"
        if it is None:
            it = next((x for x in stories if x["id"] == FORCE_ID), None); kind = "story"
        if it is None: print(f"FORCE_ID={FORCE_ID}: nao encontrado."); return
        try:
            mid = publish_post(it) if kind == "post" else publish_story(it)
            log(state, it, kind, mid, now); save_state(state); print(f"FORCE {FORCE_ID} OK -> {mid}")
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
            except Exception as e: print(f"FALHA post {it['id']}: {e}")
        else:
            print("Biblioteca de POSTS esgotada — hora de reabastecer.")

    # STORIES
    if brt.weekday() in STORY_WEEKDAYS and mod >= STORY_MIN and state["last_story_date"] != today:
        it = next_item(stories, done)
        if it:
            try:
                mid = publish_story(it); log(state, it, "story", mid, now)
                done.add(it["id"]); state["last_story_date"] = today; changed = True
                print(f"Story {it['id']} OK -> {mid}")
            except Exception as e: print(f"FALHA story {it['id']}: {e}")
        else:
            print("Biblioteca de STORIES esgotada — hora de reabastecer.")

    if changed: save_state(state); print("Estado atualizado.")
    else: print("Nada a publicar agora.")

if __name__ == "__main__":
    main()
