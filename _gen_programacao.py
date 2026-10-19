# -*- coding: utf-8 -*-
"""Regenera PROGRAMACAO.md a partir da FILA (reels.json / posts.json − state/published.json),
projetando as datas pela agenda do publish.py (reels seg/qua/sex/dom 15h; posts ter/qui/sáb 15h + dom 11h).
Uso: python _gen_programacao.py [AAAA-MM-DD]   (data-base = hoje BRT por padrão)"""
import datetime as dt
import io
import json
import os
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
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
    if os.environ.get("LAMINAS_POR_SEMANA"):
        # a produção não lê variável (regra_reels.py é a fonte única); página gerada com outra cota mentiria
        raise SystemExit("ERRO: LAMINAS_POR_SEMANA está definida no ambiente local — a produção usa "
                         "regra_reels.LAMINAS_POR_SEMANA_PADRAO. Tire a variável e rode de novo.")
    hoje = dt.date.fromisoformat(sys.argv[1]) if len(sys.argv) > 1 else dt.datetime.now(PA.BRT).date()
    st = carrega("state/published.json"); done = {e["id"] for e in st["published"]}
    reels = [x for x in carrega("reels.json") if x["id"] not in done]
    posts = [x for x in carrega("posts.json") if x["id"] not in done]
    seqs = [x for x in carrega("sequences.json") if x["id"] not in done]
    fmt_de = {x["id"]: PA.formato(x) for x in carrega("reels.json")}
    cota = PA.cota_vigente()
    rp = PA.projeta_reels(carrega("reels.json"), st["published"], hoje, st.get("last_reel_date") == hoje.isoformat())
    projetados = {i for _, i in rp}
    fora = [x["id"] for x in reels if x["id"] not in projetados]
    txt_cota = ("sem limite" if cota < 0 else "suspensa (nenhuma lâmina sai)" if cota == 0
                else f"no máximo {cota} vez(es) por semana")
    pp = projeta([x["id"] for x in posts], PA.POST_WEEKDAYS | PA.POST2_WEEKDAYS, hoje, st.get("last_post_date") == hoje.isoformat())
    trial = {x["id"] for x in reels if x.get("trial")}
    L = [f"# PROGRAMAÇÃO — o que vai ao ar e quando\n",
         f"Regenerado em {hoje:%d/%m/%Y} por `_gen_programacao.py`. **Datas são projeção da fila FIFO** a partir do último publicado — job vermelho, alarme de curtidas ou mudança na fila desloca tudo; a fonte de verdade é a fila.\n",
         "**Como revisar/suspender (regra de 30/08):** os itens ficam dias na fila antes de publicar — confira por aqui; para suspender ou editar, avise o chat da auditoria (ou remova a entrada do JSON, com lock `motor-instagram`). Piloto ativo só para formato/estratégia NOVA ou mudança de voz.\n",
         "**Marcações:** `[TRIAL]` = publica só para não-seguidores e fora do grid (B5, 4 peças sorteadas); `[A]`/`[B]` = braço do teste de gancho (B4); `← capa v2` = primeiro reel com o template novo.\n",
         f"**Formatos (18/10/2026):** `[CONVERSA]` e `[COMO FUNCIONA]` são a geração nova (animação, sem rosto) e saem sem limite; a lâmina antiga sai {txt_cota} (regra_reels.py). Dia de reel sem peça permitida fica sem reel.\n",
         "\n## Reels (seg · qua · sex · dom, ~15h BRT)\n", "| Data | Peça | Série | Vídeo |", "|---|---|---|---|"]
    braco = {"fx_sentar_levantar": "A", "fx_roupa": "A", "fx_pino_inflamado": "A", "fx_retirada": "A",
             "fx_kit_casa": "B", "fx_viagem": "B", "fx_curativo_pinos": "B", "fx_dormir": "B"}
    primeiro_v2 = True
    for d, iid in rp:
        tags = []
        if iid in trial: tags.append("**[TRIAL]**")
        if iid in braco: tags.append(f"[{braco[iid]}]")
        f = next((PA.formato(x) for x in reels if x["id"] == iid), "lamina")
        if f != "lamina": tags.append("**[" + f.replace("_", " ").upper() + "]**")
        v = next(x["video"] for x in reels if x["id"] == iid)
        serie = next((x.get("serie") for x in reels if x["id"] == iid and x.get("serie")), None) or serie_de(iid)
        L.append(f"| {DOW[d.weekday()]} {d:%d/%m} | `{iid}` {' '.join(tags)} | {serie} | [▶ assistir]({RAW}{v}) |")
    if not rp:
        L.append("| — | **nenhum reel projetado** | | |")
    if fora:
        L.append(f"\n*{len(fora)} reel(s) da fila FORA desta projeção (cota de lâminas / horizonte de 2 anos): "
                 f"{', '.join('`' + i + '`' for i in fora[:12])}{' …' if len(fora) > 12 else ''}*")
    L += ["\n## Posts de feed (ter · qui · sáb 15h · dom 11h)\n", "| Data | Peça | Nº imagens |", "|---|---|---|"]
    for d, iid in pp:
        n = len(next(x["images"] for x in posts if x["id"] == iid))
        rot = " (verbete)" if iid.startswith("v_") else ""
        L.append(f"| {DOW[d.weekday()]} {d:%d/%m} | `{iid}`{rot} | {n} |")
    L += [f"\n*Sequências de stories: {len(seqs)} restantes, publicadas ter/qui/sáb às 12:30, nos dias do carrossel (cadência reduzida em 12/09; a troca de dias de 13/09 foi revertida em 19/09 — o eixo de dia da semana estava deslocado um dia, ver E7). Quem edita a fila, regenera esta página.*\n"]
    with open(os.path.join(ROOT, "PROGRAMACAO.md"), "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(L))
    novos = sum(1 for _, i in rp if fmt_de.get(i, "lamina") != "lamina")
    ate_r = f"até {rp[-1][0]:%d/%m}" if rp else "(nenhum projetado)"
    ate_p = f"até {pp[-1][0]:%d/%m}" if pp else "(nenhum)"
    print(f"PROGRAMACAO.md: {len(rp)} reels ({novos} de formato novo) {ate_r}, {len(fora)} fora da projeção | {len(pp)} posts {ate_p}")


if __name__ == "__main__":
    main()
