# -*- coding: utf-8 -*-
"""Regenera PROGRAMACAO.md a partir da FILA (reels.json / posts.json − state/published.json),
projetando as datas pela agenda do publish.py (reels seg/qua/sex/dom 15h; posts ter/qui/sáb 15h + dom 11h).
Uso: python _gen_programacao.py [AAAA-MM-DD]   (data-base = hoje BRT por padrão)"""
import datetime as dt
import io
import json
import os
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)
import publish_agenda as PA  # noqa: E402

RAW = "https://raw.githubusercontent.com/rafaelvs/06_Automacao_Instagram/main/"
DOW = ["seg", "ter", "qua", "qui", "sex", "sáb", "dom"]


def carrega(n):
    with open(os.path.join(ROOT, n), encoding="utf-8-sig") as f:
        return json.load(f)


def serie_de(iid):
    try:
        from episodios_pe_no_chao import get
        return get(iid).get("serie") or get(iid).get("temporada") or ""
    except Exception:
        return "legado (mudo)" if iid.startswith("reel") else ""


def projeta(ids, weekdays, base, ja_hoje):
    """datas FIFO: 1 item por dia-calendário nos weekdays dados, a partir de base (exclusiva se ja_hoje)."""
    out = []; d = base + dt.timedelta(days=1 if ja_hoje else 0)
    for iid in ids:
        while d.weekday() not in weekdays:
            d += dt.timedelta(days=1)
        out.append((d, iid)); d += dt.timedelta(days=1)
    return out


def main():
    hoje = dt.date.fromisoformat(sys.argv[1]) if len(sys.argv) > 1 else dt.datetime.now(PA.BRT).date()
    st = carrega("state/published.json"); done = {e["id"] for e in st["published"]}
    reels = [x for x in carrega("reels.json") if x["id"] not in done]
    posts = [x for x in carrega("posts.json") if x["id"] not in done]
    seqs = [x for x in carrega("sequences.json") if x["id"] not in done]
    rp = projeta([x["id"] for x in reels], PA.REEL_WEEKDAYS, hoje, st.get("last_reel_date") == hoje.isoformat())
    pp = projeta([x["id"] for x in posts], PA.POST_WEEKDAYS | PA.POST2_WEEKDAYS, hoje, st.get("last_post_date") == hoje.isoformat())
    trial = {x["id"] for x in reels if x.get("trial")}
    L = [f"# PROGRAMAÇÃO — o que vai ao ar e quando\n",
         f"Regenerado em {hoje:%d/%m/%Y} por `_gen_programacao.py`. **Datas são projeção da fila FIFO** a partir do último publicado — job vermelho, alarme de curtidas ou mudança na fila desloca tudo; a fonte de verdade é a fila.\n",
         "**Como revisar/suspender (regra de 30/08):** os itens ficam dias na fila antes de publicar — confira por aqui; para suspender ou editar, avise o chat da auditoria (ou remova a entrada do JSON, com lock `motor-instagram`). Piloto ativo só para formato/estratégia NOVA ou mudança de voz.\n",
         "**Marcações:** `[TRIAL]` = publica só para não-seguidores e fora do grid (B5, 4 peças sorteadas); `[A]`/`[B]` = braço do teste de gancho (B4); `← capa v2` = primeiro reel com o template novo.\n",
         "\n## Reels (seg · qua · sex · dom, ~15h BRT)\n", "| Data | Peça | Série | Vídeo |", "|---|---|---|---|"]
    braco = {"fx_sentar_levantar": "A", "fx_roupa": "A", "fx_pino_inflamado": "A", "fx_retirada": "A",
             "fx_kit_casa": "B", "fx_viagem": "B", "fx_curativo_pinos": "B", "fx_dormir": "B"}
    primeiro_v2 = True
    for d, iid in rp:
        tags = []
        if iid in trial: tags.append("**[TRIAL]**")
        if iid in braco: tags.append(f"[{braco[iid]}]")
        if primeiro_v2 and d >= dt.date(2026, 9, 16) and not iid.startswith("reel"):
            tags.append("**← capa v2**"); primeiro_v2 = False
        v = next(x["video"] for x in reels if x["id"] == iid)
        L.append(f"| {DOW[d.weekday()]} {d:%d/%m} | `{iid}` {' '.join(tags)} | {serie_de(iid)} | [▶ assistir]({RAW}{v}) |")
    L += ["\n## Posts de feed (ter · qui · sáb 15h · dom 11h)\n", "| Data | Peça | Nº imagens |", "|---|---|---|"]
    for d, iid in pp:
        n = len(next(x["images"] for x in posts if x["id"] == iid))
        rot = " (verbete)" if iid.startswith("v_") else ""
        L.append(f"| {DOW[d.weekday()]} {d:%d/%m} | `{iid}`{rot} | {n} |")
    L += [f"\n*Sequências de stories: {len(seqs)} restantes, publicadas seg/ter/sáb às 12:30 (cadência reduzida em 12/09; dias trocados em 13/09 pelos melhores dias medidos). Quem edita a fila, regenera esta página.*\n"]
    with open(os.path.join(ROOT, "PROGRAMACAO.md"), "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(L))
    print(f"PROGRAMACAO.md: {len(rp)} reels ({len(trial)} trial) até {rp[-1][0]:%d/%m} | {len(pp)} posts até {pp[-1][0]:%d/%m}")


if __name__ == "__main__":
    main()
