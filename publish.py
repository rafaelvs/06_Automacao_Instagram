#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Publicador automatico para Instagram via API oficial da Meta (Instagram Login).
Le posts.json, publica os posts cujo horario ja chegou e que ainda nao foram
publicados, e grava o estado em state/published.json (idempotente).

Variaveis de ambiente esperadas:
  IG_USER_ID        -> ID da conta profissional do Instagram
  IG_ACCESS_TOKEN   -> token de acesso de longa duracao (Instagram User token)
  GITHUB_REPOSITORY -> "usuario/repo" (definido automaticamente pelo GitHub Actions)
  GRAPH_VERSION     -> opcional, padrao v21.0
  FORCE_ID          -> opcional, publica esse post imediatamente (ignora horario)
"""
import os, sys, json, time, datetime as dt
import requests

ROOT = os.path.dirname(os.path.abspath(__file__))
POSTS_FILE = os.path.join(ROOT, "posts.json")
STATE_FILE = os.path.join(ROOT, "state", "published.json")

IG_USER_ID = os.environ.get("IG_USER_ID", "").strip()
TOKEN      = os.environ.get("IG_ACCESS_TOKEN", "").strip()
REPO       = os.environ.get("GITHUB_REPOSITORY", "").strip()
REF        = os.environ.get("GITHUB_REF_NAME", "main").strip() or "main"
VER        = os.environ.get("GRAPH_VERSION", "v21.0").strip()
FORCE_ID   = os.environ.get("FORCE_ID", "").strip()
HOST       = f"https://graph.instagram.com/{VER}"

if not IG_USER_ID or not TOKEN:
    print("ERRO: defina os secrets IG_USER_ID e IG_ACCESS_TOKEN.")
    sys.exit(1)

def raw_url(path):
    # URL publica da imagem dentro do repositorio (repo precisa ser publico)
    if not REPO:
        raise RuntimeError("GITHUB_REPOSITORY nao definido (rode no GitHub Actions).")
    return f"https://raw.githubusercontent.com/{REPO}/{REF}/{path}"

def load_json(path, default):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return default

def save_state(state):
    os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)

def api_post(path, data):
    data = dict(data); data["access_token"] = TOKEN
    r = requests.post(f"{HOST}/{path}", data=data, timeout=60)
    if r.status_code >= 400:
        raise RuntimeError(f"POST {path} -> {r.status_code}: {r.text}")
    return r.json()

def api_get(path, params):
    params = dict(params); params["access_token"] = TOKEN
    r = requests.get(f"{HOST}/{path}", params=params, timeout=60)
    if r.status_code >= 400:
        raise RuntimeError(f"GET {path} -> {r.status_code}: {r.text}")
    return r.json()

def wait_finished(container_id, tries=10, delay=6):
    for _ in range(tries):
        st = api_get(container_id, {"fields": "status_code"}).get("status_code")
        if st == "FINISHED":
            return True
        if st in ("ERROR", "EXPIRED"):
            raise RuntimeError(f"Container {container_id} status {st}")
        time.sleep(delay)
    return True  # segue mesmo assim; media_publish dara erro claro se nao estiver pronto

def publish_post(post):
    imgs = post["images"]
    caption = post.get("caption", "")
    if len(imgs) == 1:
        cont = api_post(f"{IG_USER_ID}/media",
                        {"image_url": raw_url(imgs[0]), "caption": caption})["id"]
    else:
        children = []
        for path in imgs:
            cid = api_post(f"{IG_USER_ID}/media",
                           {"image_url": raw_url(path), "is_carousel_item": "true"})["id"]
            children.append(cid)
        cont = api_post(f"{IG_USER_ID}/media",
                        {"media_type": "CAROUSEL",
                         "children": ",".join(children),
                         "caption": caption})["id"]
    wait_finished(cont)
    media_id = api_post(f"{IG_USER_ID}/media_publish", {"creation_id": cont})["id"]
    return media_id

def main():
    posts = load_json(POSTS_FILE, [])
    state = load_json(STATE_FILE, {"published": []})
    done = {e["id"] for e in state["published"]}
    now = dt.datetime.now(dt.timezone.utc)

    if FORCE_ID:
        targets = [p for p in posts if p["id"] == FORCE_ID and p["id"] not in done]
        if not targets:
            print(f"FORCE_ID={FORCE_ID}: nada a publicar (ja publicado ou inexistente).")
    else:
        targets = []
        for p in posts:
            if p["id"] in done:
                continue
            when = dt.datetime.fromisoformat(p["datetime"])
            if when.tzinfo is None:
                when = when.replace(tzinfo=dt.timezone.utc)
            if when <= now:
                targets.append(p)

    if not targets:
        print("Nenhum post pendente para publicar agora.")
        return

    changed = False
    for p in targets:
        try:
            print(f"Publicando {p['id']} ...")
            mid = publish_post(p)
            state["published"].append({"id": p["id"], "media_id": mid,
                                       "at": now.isoformat()})
            done.add(p["id"]); changed = True
            print(f"  OK -> media_id {mid}")
        except Exception as e:
            print(f"  FALHA em {p['id']}: {e}")

    if changed:
        save_state(state)
        print("Estado atualizado.")

if __name__ == "__main__":
    main()
