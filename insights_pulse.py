# -*- coding: utf-8 -*-
"""
insights_pulse.py — PULSO de metricas do @rafaelvargasmd via Instagram Graph API.

Por que existe: o pulso mensal da auditoria evolutiva rodava pelo app no emulador (VM android-lab);
com a VM indisponivel (billing) e mesmo sem ela, a API da metricas MELHORES: sends (shares) POR PECA,
watch time de Reel, alcance por peca — o que o app so mostra agregado.

Uso: rodado pelo workflow insights.yml (workflow_dispatch) com os MESMOS secrets do publish
(IG_USER_ID, IG_ACCESS_TOKEN). So LEITURA (GET) — nao publica, nao muda nada na conta.
Saida: resumo humano + bloco JSON delimitado (===INSIGHTS_JSON_BEGIN===/END===) p/ parse.
O token NUNCA e impresso; erros da API sao impressos sem a query string.

Escopo necessario do token: instagram_business_manage_insights (se faltar, os GETs de insights
retornam erro de permissao — o script reporta e segue; media basica ainda sai).
"""
import os, sys, json, time, urllib.request, urllib.parse, datetime

IG_USER = os.environ.get("IG_USER_ID", "").strip()
TOKEN = os.environ.get("IG_ACCESS_TOKEN", "").strip()
VER = os.environ.get("GRAPH_VERSION", "v21.0").strip()
DAYS = int(os.environ.get("PULSE_DAYS", "30"))
HOST = f"https://graph.instagram.com/{VER}"
if not IG_USER or not TOKEN:
    print("ERRO: defina IG_USER_ID e IG_ACCESS_TOKEN."); sys.exit(1)

NOW = int(time.time())
SINCE = NOW - DAYS * 86400
JANELA = (datetime.datetime.utcfromtimestamp(SINCE).strftime("%Y-%m-%d"),
          datetime.datetime.utcfromtimestamp(NOW).strftime("%Y-%m-%d"))

def get(path, **params):
    """GET com token; devolve dict ou {'_erro': msg} (nunca vaza token na saida)."""
    params["access_token"] = TOKEN
    url = f"{HOST}/{path}?{urllib.parse.urlencode(params)}"
    try:
        with urllib.request.urlopen(url, timeout=60) as r:
            return json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        try:
            body = json.loads(e.read().decode("utf-8"))
            msg = body.get("error", {}).get("message", str(e))
        except Exception:
            msg = str(e)
        return {"_erro": f"{path}: {msg}"}
    except Exception as e:
        return {"_erro": f"{path}: {e}"}

out = {"janela": f"{JANELA[0]} a {JANELA[1]} (UTC, {DAYS}d)", "conta": {}, "erros": []}

# ── 1) CONTA: metricas de janela (total_value) ────────────────────────────────────────────
# reach: serie diaria somada; demais: total_value no range. Cada metrica isolada em try p/ degradar bem.
def conta_metrica(metric, **extra):
    r = get(f"{IG_USER}/insights", metric=metric, period="day",
            since=SINCE, until=NOW, **extra)
    if "_erro" in r:
        out["erros"].append(r["_erro"]); return None
    return r.get("data", [])

d = conta_metrica("reach")
if d:
    vals = [v.get("value", 0) for v in d[0].get("values", [])]
    # ATENCAO: isto NAO e alcance unico do mes — e a soma dos alcances diarios, entao
    # a mesma pessoa conta de novo a cada dia em que viu algo. Na janela de 03/07-02/08
    # deu 1463 contra 527 de alcance UNICO (breakdown follow_type). A auditoria v1 usou
    # o numero errado como metrica-titulo. O nome ficou explicito para nao enganar de novo.
    out["conta"]["reach_impressoes_soma_diaria"] = sum(vals)

for m in ("views", "profile_views", "website_clicks", "accounts_engaged",
          "total_interactions", "likes", "comments", "shares", "saves", "replies"):
    d = conta_metrica(m, metric_type="total_value")
    if d:
        tv = d[0].get("total_value", {}).get("value")
        if tv is not None:
            out["conta"][m] = tv

# breakdown seguidor/nao-seguidor (a metrica-norte da bolha)
for m in ("views", "reach", "total_interactions"):
    d = conta_metrica(m, metric_type="total_value", breakdown="follow_type")
    if d:
        try:
            bks = d[0]["total_value"]["breakdowns"][0]["results"]
            out["conta"][f"{m}_por_follow_type"] = {
                "/".join(b.get("dimension_values", ["?"])): b.get("value") for b in bks}
        except Exception:
            pass

# TAMANHO DA BASE — sem ele nao da para separar "o Instagram parou de me entregar" de
# "eu tenho poucos seguidores", nem dizer que fracao da base cada peca alcancou.
# A auditoria v1 nao conseguiu responder isso: followers_count nunca era pedido.
r = get(IG_USER, fields="followers_count,follows_count,media_count,username,name,biography,website")
if "_erro" in r:
    out["erros"].append(r["_erro"])
else:
    for campo in ("followers_count", "follows_count", "media_count", "username", "name"):
        if r.get(campo) is not None:
            out["conta"][campo] = r[campo]
    # Superficie de 3 segundos do perfil: a auditoria v1 nao conseguiu auditar bio nem
    # link porque nada disso era versionado. Guardar aqui congela o estado de cada pulso.
    out["perfil"] = {"biography": r.get("biography"), "website": r.get("website")}

# ALCANCE UNICO da janela, derivado do breakdown (a metrica-titulo correta).
try:
    _rb = out["conta"].get("reach_por_follow_type") or {}
    if _rb:
        out["conta"]["reach_unico_janela"] = sum(v for v in _rb.values() if isinstance(v, (int, float)))
except Exception:
    pass

# follower_count diario (crescimento na janela)
d = conta_metrica("follower_count")
if d:
    vals = [v.get("value", 0) for v in d[0].get("values", [])]
    out["conta"]["novos_seguidores_janela"] = sum(vals)

# ── 2) MIDIA: pecas da janela + insights POR PECA (o dado que o app nao da) ───────────────
media = []
r = get(f"{IG_USER}/media", fields="id,media_type,media_product_type,timestamp,like_count,comments_count",
        limit=100)
if "_erro" in r:
    out["erros"].append(r["_erro"])
else:
    media = [m for m in r.get("data", []) if m.get("timestamp", "")[:10] >= JANELA[0]]

MET = {
    "REELS": "views,reach,likes,comments,saved,shares,total_interactions,ig_reels_avg_watch_time",
    "FEED":  "views,reach,likes,comments,saved,shares,total_interactions",
    "STORY": "views,reach,replies,shares",
}
pecas = []
for m in media:
    tipo = m.get("media_product_type", "FEED")
    met = MET.get(tipo, MET["FEED"])
    ins = get(f"{m['id']}/insights", metric=met)
    row = {"id": m["id"], "tipo": tipo, "quando": m.get("timestamp", "")[:16],
           "likes": m.get("like_count"), "comments": m.get("comments_count")}
    if "_erro" in ins:
        row["erro"] = ins["_erro"][:160]
    else:
        for item in ins.get("data", []):
            vals = item.get("values", [{}])
            row[item.get("name")] = vals[0].get("value") if vals else None
    pecas.append(row)

out["pecas_na_janela"] = len(pecas)

# ── 3) AGREGADOS por formato + SPR (sends/reach) por Reel ────────────────────────────────
agg = {}
for p in pecas:
    t = p["tipo"]; a = agg.setdefault(t, {"n": 0, "views": 0, "reach": 0, "shares": 0,
                                          "saved": 0, "likes": 0, "comments": 0})
    a["n"] += 1
    for k in ("views", "reach", "shares", "saved", "likes", "comments"):
        v = p.get(k) or (p.get("replies") if k == "comments" and t == "STORY" else None)
        if isinstance(v, (int, float)):
            a[k] += v
out["agregado_por_formato"] = agg

reels = [p for p in pecas if p["tipo"] == "REELS"]
for p in reels:
    rch = p.get("reach") or 0
    p["spr_pct"] = round(100.0 * (p.get("shares") or 0) / rch, 2) if rch else None
tot_sh = sum(p.get("shares") or 0 for p in reels)
tot_rc = sum(p.get("reach") or 0 for p in reels)
out["reels_janela"] = {
    "n": len(reels), "shares_total": tot_sh, "reach_total": tot_rc,
    "SPR_agregado_pct": round(100.0 * tot_sh / tot_rc, 2) if tot_rc else None,
    # Media SIMPLES: cada reel pesa igual, entao um reel com 1 view distorce tanto quanto
    # um com 111. Mantida so para comparar com as rodadas antigas.
    "watch_time_medio_simples_ms": (lambda ws: round(sum(ws) / len(ws)) if ws else None)(
        [p["ig_reels_avg_watch_time"] for p in reels
         if isinstance(p.get("ig_reels_avg_watch_time"), (int, float))]),
    # Media PONDERADA por views — e esta que descreve o que a audiencia realmente assistiu.
    # Na janela de 03/07-02/08 dava 1891 ms contra 2128 ms da media simples.
    "watch_time_ponderado_ms": (lambda ps: round(
        sum(p["ig_reels_avg_watch_time"] * (p.get("views") or 0) for p in ps)
        / sum((p.get("views") or 0) for p in ps)) if sum((p.get("views") or 0) for p in ps) else None)(
        [p for p in reels if isinstance(p.get("ig_reels_avg_watch_time"), (int, float))]),
    # Mediana de alcance por peca: com n pequeno e cauda longa, a media engana.
    "reach_mediano_por_peca": (lambda xs: sorted(xs)[len(xs) // 2] if xs else None)(
        [p.get("reach") or 0 for p in reels]),
}
out["top_por_shares"] = sorted(pecas, key=lambda p: (p.get("shares") or 0), reverse=True)[:8]
out["top_por_saved"] = sorted(pecas, key=lambda p: (p.get("saved") or 0), reverse=True)[:5]
out["detalhe_pecas"] = pecas

# ── saida ────────────────────────────────────────────────────────────────────────────────
print(f"== PULSO {out['janela']} ==")
print(f"conta: {json.dumps(out['conta'], ensure_ascii=False)}")
print(f"pecas na janela: {len(pecas)} | agregado: {json.dumps(agg, ensure_ascii=False)}")
print(f"reels: {json.dumps(out['reels_janela'], ensure_ascii=False)}")
if out["erros"]:
    print(f"erros ({len(out['erros'])}):")
    for e in out["erros"][:12]:
        print("  -", e[:200])
print("===INSIGHTS_JSON_BEGIN===")
print(json.dumps(out, ensure_ascii=False, default=str))
print("===INSIGHTS_JSON_END===")
