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
"""
import os, sys, json, time, datetime as dt
import requests

POST_WEEKDAYS  = {1, 3, 5}
POST_MIN       = 15*60                   # 15:00 BRT (pico de audiencia; era 19:00)
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
TRIAL_GRADUATION = os.environ.get("TRIAL_GRADUATION", "SS_PERFORMANCE").strip()  # SS_PERFORMANCE | MANUAL
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
    r = requests.post(f"{HOST}/{path}", data=data, timeout=120)
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

def publish_post(item):
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
def publish_reel(item):
    # alt_text NAO e' suportado em reels (so imagens); location_id e' suportado.
    base = _loc({"media_type": "REELS", "video_url": raw_url(item["video"]),
                 "caption": item.get("caption", "")})
    cont = None
    if TRIAL_REELS:
        # Trial Reel: so' para nao-seguidores; graduacao automatica (SS_PERFORMANCE) se performar.
        try:
            p = dict(base); p["trial_params"] = json.dumps({"graduation_strategy": TRIAL_GRADUATION})
            cont = api_post(f"{IG_USER_ID}/media", p)["id"]
        except RuntimeError as e:
            # Fallback robusto: se a API recusar trial_params, publica reel normal (nao trava o robo).
            print(f"  ! trial_params recusado ({e}); publicando como reel normal.", file=sys.stderr)
            cont = None
    if cont is None:
        p = dict(base); p["share_to_feed"] = "true"
        cont = api_post(f"{IG_USER_ID}/media", p)["id"]
    wait_finished(cont, tries=30, delay=10)
    return api_post(f"{IG_USER_ID}/media_publish", {"creation_id": cont})["id"]
def log(state, item_id, kind, mid, now): state["published"].append({"id": item_id, "kind": kind, "media_id": mid, "at": now.isoformat()})
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

    if FORCE_ID == "destaques":
        for it in load_json(DESTAQUES_FILE, []):
            try:
                mid = publish_story(it); log(state, it["id"], "story", mid, now); changed = True
                print(f"Destaque {it['id']} OK -> {mid}")
            except Exception as e: print(f"FALHA destaque {it['id']}: {e}")
        if changed: save_state(state)
        return

    if FORCE_ID:
        it = next((x for x in posts if x["id"] == FORCE_ID), None); kind = "post"
        if it is None:
            it = next((x for x in seqs if x["id"] == FORCE_ID), None); kind = "seq"
        if it is None:
            it = next((x for x in stories if x["id"] == FORCE_ID), None); kind = "story"
        if it is None:
            it = next((x for x in reels if x["id"] == FORCE_ID), None); kind = "reel"
        if it is None: print(f"FORCE_ID={FORCE_ID}: nao encontrado."); return
        try:
            if kind == "post": mid = publish_post(it)
            elif kind == "seq": mid = publish_sequence(it)[0]
            elif kind == "story": mid = publish_story(it)
            else: mid = publish_reel(it)
            log(state, it["id"], kind, mid, now); save_state(state); print(f"FORCE {FORCE_ID} OK -> {mid}")
        except Exception as e: print(f"FORCE {FORCE_ID} FALHA: {e}")
        return

    # POSTS (feed)
    if brt.weekday() in POST_WEEKDAYS and mod >= POST_MIN and state["last_post_date"] != today:
        it = next_item(posts, done)
        if it:
            try:
                mid = publish_post(it); log(state, it["id"], "post", mid, now)
                done.add(it["id"]); state["last_post_date"] = today; changed = True
                print(f"Post {it['id']} OK -> {mid}")
            except Exception as e: print(f"FALHA post {it['id']}: {e}")
        else:
            print("Biblioteca de POSTS esgotada — hora de reabastecer.")

    # SEQUENCIA DIARIA (story serializado, 5 frames)
    if brt.weekday() in SEQ_WEEKDAYS and mod >= SEQ_MIN and state["last_seq_date"] != today:
        it = next_item(seqs, done)
        if it:
            try:
                print(f"Sequencia {it['id']} ({it.get('theme','')}) — publicando {len(it['images'])} frames...")
                ids = publish_sequence(it); log(state, it["id"], "seq", ids[0], now)
                done.add(it["id"]); state["last_seq_date"] = today; changed = True
                print(f"Sequencia {it['id']} OK -> {len(ids)} frames")
            except Exception as e: print(f"FALHA sequencia {it['id']}: {e}")
        else:
            print("Biblioteca de SEQUENCIAS esgotada — hora de reabastecer.")

    # REELS
    if brt.weekday() in REEL_WEEKDAYS and mod >= REEL_MIN and state["last_reel_date"] != today:
        it = next_item(reels, done)
        if it:
            try:
                mid = publish_reel(it); log(state, it["id"], "reel", mid, now)
                done.add(it["id"]); state["last_reel_date"] = today; changed = True
                print(f"Reel {it['id']} OK -> {mid}")
            except Exception as e: print(f"FALHA reel {it['id']}: {e}")
        else:
            print("Biblioteca de REELS esgotada — hora de reabastecer.")

    if changed: save_state(state); print("Estado atualizado.")
    else: print("Nada a publicar agora.")

if __name__ == "__main__":
    main()
