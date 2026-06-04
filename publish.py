#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Publicador automatico para Instagram via API oficial da Meta (Instagram Login).

- POSTS (feed): posts.json com datas fixas (imagem unica ou carrossel).
- STORIES: stories.json e' um BANCO ordenado; o robo publica em ROTACAO,
  nos dias/horarios definidos abaixo, indefinidamente (sem input humano).

Env: IG_USER_ID, IG_ACCESS_TOKEN, GITHUB_REPOSITORY (auto no Actions),
     GRAPH_VERSION (opcional, v21.0), FORCE_ID (opcional: publica esse id ja).
"""
import os, sys, json, time, datetime as dt
import requests

# ---- Agenda dos STORIES (horario de Brasilia, BRT = UTC-3) ----
STORY_WEEKDAYS = {0, 2, 4}     # 0=Seg, 2=Qua, 4=Sex
STORY_MINUTE_OF_DAY = 12*60+30 # 12:30
BRT = dt.timezone(dt.timedelta(hours=-3))

ROOT = os.path.dirname(os.path.abspath(__file__))
POSTS_FILE = os.path.join(ROOT, "posts.json")
STORIES_FILE = os.path.join(ROOT, "stories.json")
STATE_FILE = os.path.join(ROOT, "state", "published.json")

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

def load_json(path, default):
    try:
        with open(path, encoding="utf-8") as f: return json.load(f)
    except FileNotFoundError:
        return default

def save_state(state):
    os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)

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
    imgs = item["images"]; caption = item.get("caption", "")
    if len(imgs) == 1:
        cont = api_post(f"{IG_USER_ID}/media", {"image_url": raw_url(imgs[0]), "caption": caption})["id"]
    else:
        kids = [api_post(f"{IG_USER_ID}/media", {"image_url": raw_url(p), "is_carousel_item": "true"})["id"] for p in imgs]
        cont = api_post(f"{IG_USER_ID}/media", {"media_type": "CAROUSEL", "children": ",".join(kids), "caption": caption})["id"]
    wait_finished(cont)
    return api_post(f"{IG_USER_ID}/media_publish", {"creation_id": cont})["id"]

def publish_story(item):
    cont = api_post(f"{IG_USER_ID}/media", {"image_url": raw_url(item["image"]), "media_type": "STORIES"})["id"]
    wait_finished(cont)
    return api_post(f"{IG_USER_ID}/media_publish", {"creation_id": cont})["id"]

def post_due(item, now_utc):
    when = dt.datetime.fromisoformat(item["datetime"])
    if when.tzinfo is None: when = when.replace(tzinfo=dt.timezone.utc)
    return when <= now_utc

def log(state, item, kind, mid, now_utc):
    state["published"].append({"id": item["id"], "kind": kind, "media_id": mid, "at": now_utc.isoformat()})

def main():
    posts = load_json(POSTS_FILE, [])
    stories = load_json(STORIES_FILE, [])
    state = load_json(STATE_FILE, {"published": [], "story_idx": 0, "last_story_date": ""})
    state.setdefault("published", []); state.setdefault("story_idx", 0); state.setdefault("last_story_date", "")
    done = {e["id"] for e in state["published"]}
    now_utc = dt.datetime.now(dt.timezone.utc)
    now_brt = now_utc.astimezone(BRT)
    changed = False

    # ---- FORCE: publica um item especifico (post ou story) ----
    if FORCE_ID:
        p = next((x for x in posts if x["id"] == FORCE_ID), None)
        s = next((x for x in stories if x["id"] == FORCE_ID), None)
        try:
            if p:
                print(f"FORCE post {FORCE_ID}"); mid = publish_post(p); log(state, p, "post", mid, now_utc); changed = True
            elif s:
                print(f"FORCE story {FORCE_ID}"); mid = publish_story(s); log(state, s, "story", mid, now_utc); changed = True
            else:
                print(f"FORCE_ID={FORCE_ID}: id nao encontrado.")
            if changed: print("  OK")
        except Exception as e:
            print(f"  FALHA: {e}")
        if changed: save_state(state)
        return

    # ---- POSTS do feed (datas fixas) ----
    for p in posts:
        if p["id"] in done or not post_due(p, now_utc): continue
        try:
            print(f"Post {p['id']}"); mid = publish_post(p); log(state, p, "post", mid, now_utc)
            done.add(p["id"]); changed = True; print(f"  OK -> {mid}")
        except Exception as e:
            print(f"  FALHA post {p['id']}: {e}")

    # ---- STORIES em ROTACAO (Seg/Qua/Sex >= 12:30 BRT, 1x por dia) ----
    today = now_brt.date().isoformat()
    slot = (now_brt.weekday() in STORY_WEEKDAYS
            and (now_brt.hour*60 + now_brt.minute) >= STORY_MINUTE_OF_DAY
            and state["last_story_date"] != today)
    if slot and stories:
        idx = state["story_idx"] % len(stories)
        s = stories[idx]
        try:
            print(f"Story (rotacao) {s['id']}"); mid = publish_story(s); log(state, s, "story", mid, now_utc)
            state["story_idx"] = idx + 1
            state["last_story_date"] = today
            changed = True; print(f"  OK -> {mid}")
        except Exception as e:
            print(f"  FALHA story {s['id']}: {e}")

    if changed: save_state(state); print("Estado atualizado.")
    else: print("Nada a publicar agora.")

if __name__ == "__main__":
    main()
