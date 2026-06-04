#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Publicador automatico para Instagram via API oficial da Meta (Instagram Login).
Publica POSTS (feed: imagem unica ou carrossel) e STORIES, conforme posts.json e
stories.json, nos horarios agendados. Grava o estado em state/published.json.

Env: IG_USER_ID, IG_ACCESS_TOKEN, GITHUB_REPOSITORY (auto no Actions),
     GRAPH_VERSION (opcional, v21.0), FORCE_ID (opcional: publica esse id ja).
"""
import os, sys, json, time, datetime as dt
import requests

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
    if not REPO:
        raise RuntimeError("GITHUB_REPOSITORY nao definido (rode no GitHub Actions).")
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
        kids = []
        for p in imgs:
            kids.append(api_post(f"{IG_USER_ID}/media", {"image_url": raw_url(p), "is_carousel_item": "true"})["id"])
        cont = api_post(f"{IG_USER_ID}/media", {"media_type": "CAROUSEL", "children": ",".join(kids), "caption": caption})["id"]
    wait_finished(cont)
    return api_post(f"{IG_USER_ID}/media_publish", {"creation_id": cont})["id"]

def publish_story(item):
    cont = api_post(f"{IG_USER_ID}/media", {"image_url": raw_url(item["image"]), "media_type": "STORIES"})["id"]
    wait_finished(cont)
    return api_post(f"{IG_USER_ID}/media_publish", {"creation_id": cont})["id"]

def due(item, now):
    when = dt.datetime.fromisoformat(item["datetime"])
    if when.tzinfo is None: when = when.replace(tzinfo=dt.timezone.utc)
    return when <= now

def main():
    posts = [dict(p, _kind="post") for p in load_json(POSTS_FILE, [])]
    stories = [dict(s, _kind="story") for s in load_json(STORIES_FILE, [])]
    items = posts + stories
    state = load_json(STATE_FILE, {"published": []})
    done = {e["id"] for e in state["published"]}
    now = dt.datetime.now(dt.timezone.utc)

    if FORCE_ID:
        targets = [it for it in items if it["id"] == FORCE_ID and it["id"] not in done]
        if not targets: print(f"FORCE_ID={FORCE_ID}: nada a publicar.")
    else:
        targets = [it for it in items if it["id"] not in done and due(it, now)]

    if not targets:
        print("Nenhum item pendente para publicar agora."); return

    changed = False
    for it in targets:
        try:
            print(f"Publicando {it['id']} ({it['_kind']}) ...")
            mid = publish_story(it) if it["_kind"] == "story" else publish_post(it)
            state["published"].append({"id": it["id"], "kind": it["_kind"], "media_id": mid, "at": now.isoformat()})
            done.add(it["id"]); changed = True
            print(f"  OK -> media_id {mid}")
        except Exception as e:
            print(f"  FALHA em {it['id']}: {e}")

    if changed:
        save_state(state); print("Estado atualizado.")

if __name__ == "__main__":
    main()
