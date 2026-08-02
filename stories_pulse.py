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
import urllib.error
import urllib.parse
import urllib.request

IG_USER = os.environ.get("IG_USER_ID", "").strip()
TOKEN = os.environ.get("IG_ACCESS_TOKEN", "").strip()
VER = os.environ.get("GRAPH_VERSION", "v21.0").strip()
HOST = f"https://graph.instagram.com/{VER}"
SERIE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "state", "stories_serie.json")

if not IG_USER or not TOKEN:
    print("ERRO: defina IG_USER_ID e IG_ACCESS_TOKEN.")
    sys.exit(1)


def get(path, **params):
    """GET na Graph API. Erro NUNCA vaza a query string (o repo e PUBLICO e o log tambem)."""
    params["access_token"] = TOKEN
    url = f"{HOST}/{path}?{urllib.parse.urlencode(params)}"
    try:
        with urllib.request.urlopen(url, timeout=60) as r:
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
