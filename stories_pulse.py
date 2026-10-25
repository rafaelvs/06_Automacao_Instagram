# -*- coding: utf-8 -*-
"""
stories_pulse.py — mede os STORIES, que o pulso normal nao enxerga.

Por que existe: `insights_pulse.py` consulta `{IG_USER}/media`, e essa edge — por desenho
da Graph API — NUNCA devolve stories. Resultado medido na auditoria v1 (02/08/2026): as
~150 telas/mes publicadas como sequencia (30 sequencias x 5 frames) eram 100% cegas, e
duas medicoes independentes situam isso em ~72% das views da conta. Ou seja, a maior
parte da atividade nao entrava em nenhuma nota.

A edge `{IG_USER}/stories` so devolve stories ATIVOS (janela de 24 h). Logo isto precisa
rodar TODO DIA e acumular — um pulso mensal nao recupera o que ja expirou.

Uso: workflow `stories.yml` (cron diario), com os MESMOS secrets do publish.
So LEITURA (GET). O token NUNCA e impresso; erro da API sai sem a query string.
Saida: resumo humano + bloco JSON delimitado, e append em state/stories_serie.json.
"""
import datetime
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

IG_USER = os.environ.get("IG_USER_ID", "").strip()
TOKEN = os.environ.get("IG_ACCESS_TOKEN", "").strip()
VER = os.environ.get("GRAPH_VERSION", "v21.0").strip()
HOST = f"https://graph.instagram.com/{VER}"
SERIE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "state", "stories_serie.json")
# v2 (24/10/2026, geração nova): a série diária só guardava a SOMA do dia — não dava para dizer
# qual tela segurou e qual derrubou. Agora cada story medido fica guardado POR PEÇA (media_id),
# com a navegação por tipo e a ligação com a parte da story publicada pelo motor (published.json).
PECAS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "state", "stories_pecas.json")
PUBLICADOS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "state", "published.json")
# Orçamento dos EXTRAS (auditoria 24/10/2026, publicacao#9): a v2 passou de 1 para 4 GETs por story ativo,
# todos com timeout de 60 s, e a série só era gravada DEPOIS deles — com a story de 3 partes no ar, o pior
# caso (13 min) passava dos 10 min do job e a medição do dia se perdia (a edge /stories não devolve ontem).
# Agora a série vai ao disco logo depois da chamada principal; os extras têm timeout curto e um orçamento
# TOTAL — o que não couber vira `erros_extra` ("orçamento"), nunca job morto.
ORCAMENTO_EXTRAS_S = float(os.environ.get("STORIES_ORCAMENTO_EXTRAS_S", "180") or 180)
TIMEOUT_EXTRA_S = float(os.environ.get("STORIES_TIMEOUT_EXTRA_S", "20") or 20)

if not IG_USER or not TOKEN:
    print("ERRO: defina IG_USER_ID e IG_ACCESS_TOKEN.")
    sys.exit(1)


def get(path, _timeout=60, **params):
    """GET na Graph API. Erro NUNCA vaza a query string (o repo e PUBLICO e o log tambem)."""
    params["access_token"] = TOKEN
    url = f"{HOST}/{path}?{urllib.parse.urlencode(params)}"
    try:
        with urllib.request.urlopen(url, timeout=_timeout) as r:
            return json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        try:
            msg = json.loads(e.read().decode("utf-8")).get("error", {}).get("message", str(e))
        except Exception:
            msg = f"HTTP {e.code}"
        return {"_erro": f"{path}: {msg}"}          # sem url, sem token
    except Exception as e:                           # noqa: BLE001
        return {"_erro": f"{path}: {type(e).__name__}"}


hoje = datetime.datetime.now(datetime.timezone.utc)
out = {
    "medido_em": hoje.isoformat(timespec="seconds"),
    "stories_ativos": 0,
    "erros": [],
    "pecas": [],
}

r = get(f"{IG_USER}/stories", fields="id,media_type,media_product_type,timestamp,permalink")
if "_erro" in r:
    out["erros"].append(r["_erro"])
    ativos = []
else:
    ativos = r.get("data", [])

out["stories_ativos"] = len(ativos)

# Metricas de story. `views` substituiu `impressions` nas versoes novas; `reach` e o
# alcance unico; `replies` e o unico sinal de conversa que story oferece.
MET = "views,reach,replies,shares,navigation"
# v2: métricas de conversão (best-effort, chamada própria: uma recusada não leva as outras) e a
# navegação POR TIPO — tap_forward, tap_back, tap_exit, swipe_forward. A Meta recusa breakdown
# misturado com métrica que não o aceita, por isso vai numa chamada só dela.
MET_EXTRA = ("follows", "profile_visits")
for s in ativos:
    linha = {"id": s.get("id"), "quando": (s.get("timestamp") or "")[:16],
             "tipo": s.get("media_type")}
    ins = get(f"{s['id']}/insights", metric=MET)
    if "_erro" in ins:
        # Degrada bem: sem insight ainda registramos que a peca EXISTIU naquele dia —
        # e isso ja e' mais do que se tinha antes.
        linha["erro"] = ins["_erro"][:120]
    else:
        for item in ins.get("data", []):
            vals = item.get("values", [{}])
            linha[item.get("name")] = vals[0].get("value") if vals else None
    out["pecas"].append(linha)

soma = {}
for p in out["pecas"]:
    for k in ("views", "reach", "replies", "shares"):
        if isinstance(p.get(k), (int, float)):
            soma[k] = soma.get(k, 0) + p[k]
out["agregado_do_dia"] = soma

# --- acumula a serie (o dado de ontem nao volta: a edge so tem as ultimas 24 h) -----
# Gravada AQUI, antes dos extras: job que morre (timeout) nos extras não perde a medição do dia.
try:
    serie = json.load(open(SERIE, encoding="utf-8")) if os.path.isfile(SERIE) else {"dias": []}
except Exception:
    serie = {"dias": []}
dia = hoje.date().isoformat()
serie["dias"] = [d for d in serie.get("dias", []) if d.get("dia") != dia]
serie["dias"].append({"dia": dia, "stories_ativos": out["stories_ativos"], **soma})
serie["dias"] = sorted(serie["dias"], key=lambda d: d["dia"])[-400:]
os.makedirs(os.path.dirname(SERIE), exist_ok=True)
with open(SERIE, "w", encoding="utf-8") as fh:
    json.dump(serie, fh, ensure_ascii=False, indent=2)
    fh.write("\n")

# --- v2: guarda POR PEÇA (o mais recente medido de cada media_id) com a parte da story ------
try:
    _pub = json.load(open(PUBLICADOS, encoding="utf-8")).get("published", [])
except Exception:
    _pub = []
_parte = {e.get("media_id"): {"story": e.get("story"), "parte": e.get("parte"), "kind": e.get("kind")}
          for e in _pub if e.get("media_id") and e.get("kind") in ("cfstory", "story_nova")}
try:
    pecas = json.load(open(PECAS, encoding="utf-8")) if os.path.isfile(PECAS) else {"pecas": {}}
except Exception:
    pecas = {"pecas": {}}


def gravar_pecas():
    """Grava as peças medidas até aqui (chamada antes E depois dos extras)."""
    for p in out["pecas"]:
        if not p.get("id"):
            continue
        reg = dict(p); reg["medido_em"] = out["medido_em"]
        _quando = next((a.get("timestamp") for a in ativos if a.get("id") == p["id"]), "") or ""
        try:
            _ts = datetime.datetime.fromisoformat(_quando.replace("+0000", "+00:00"))
            reg["idade_h"] = round((hoje - _ts).total_seconds() / 3600, 1)   # métrica de story depende da idade
        except ValueError:
            reg["idade_h"] = None
        reg.update(_parte.get(p["id"], {}))
        pecas.setdefault("pecas", {})[p["id"]] = reg
    with open(PECAS, "w", encoding="utf-8") as fh:
        json.dump(pecas, fh, ensure_ascii=False, indent=2)
        fh.write("\n")


gravar_pecas()

# --- v2: extras (best-effort, com ORÇAMENTO total): métricas de conversão (chamada própria: uma recusada
# não leva as outras) e a navegação POR TIPO — tap_forward, tap_back, tap_exit, swipe_forward. A Meta recusa
# breakdown misturado com métrica que não o aceita, por isso vai numa chamada só dela.
_fim_extras = time.monotonic() + ORCAMENTO_EXTRAS_S


def get_extra(linha, rotulo, path, **params):
    """GET de um extra dentro do orçamento; sem tempo = `erros_extra` ('orçamento'), sem chamar."""
    resta = _fim_extras - time.monotonic()
    if resta < 1:
        linha.setdefault("erros_extra", []).append(f"{rotulo}: orçamento de {ORCAMENTO_EXTRAS_S:.0f}s dos extras esgotado")
        return None
    r = get(path, _timeout=max(1.0, min(TIMEOUT_EXTRA_S, resta)), **params)
    if "_erro" in r:
        linha.setdefault("erros_extra", []).append(f"{rotulo}: {r['_erro'][:80]}")
        return None
    return r


for linha in out["pecas"]:
    if not linha.get("id"):
        continue
    for _m in MET_EXTRA:
        _r = get_extra(linha, _m, f"{linha['id']}/insights", metric=_m)
        if _r is None:
            continue
        for item in _r.get("data", []):
            vals = item.get("values", [{}])
            linha[item.get("name")] = vals[0].get("value") if vals else None
    _r = get_extra(linha, "navigation+tipo", f"{linha['id']}/insights", metric="navigation",
                   breakdown="story_navigation_action_type")
    if _r is not None:
        try:
            _res = _r["data"][0]["total_value"]["breakdowns"][0]["results"]
            linha["navegacao"] = {str(x.get("dimension_values", ["?"])[0]).lower(): x.get("value") for x in _res}
        except (KeyError, IndexError, TypeError) as _e:
            linha.setdefault("erros_extra", []).append(f"navigation+tipo: formato inesperado ({type(_e).__name__})")

gravar_pecas()

print(f"== STORIES {dia} == ativos: {out['stories_ativos']} | agregado: "
      f"{json.dumps(soma, ensure_ascii=False)}")
if out["erros"]:
    print("erros:", json.dumps(out["erros"], ensure_ascii=False))
print(f"serie acumulada: {len(serie['dias'])} dia(s) em state/stories_serie.json")
print("===STORIES_JSON_BEGIN===")
print(json.dumps(out, ensure_ascii=False))
print("===STORIES_JSON_END===")

# Falha ALTO se a edge inteira quebrou: sem isto o job fica verde medindo nada, que e
# exatamente o modo de falha que a auditoria v1 encontrou espalhado pelos motores.
if out["erros"] and out["stories_ativos"] == 0:
    print("FALHA: a edge /stories nao respondeu — medicao do dia PERDIDA.", file=sys.stderr)
    sys.exit(1)
