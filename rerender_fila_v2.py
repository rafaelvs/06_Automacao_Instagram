# -*- coding: utf-8 -*-
"""
RE-RENDER DA FILA DE CARROSSÉIS no visual v2 da marca (marca.py) — 14/10/2026.

Só refaz a ARTE dos carrosséis AINDA NÃO PUBLICADOS (posts.json menos state/published.json).
Texto, legenda, ordem da fila e aprovações ficam INTOCADOS: os slides saem das mesmas fontes de
conteúdo de sempre e são gravados com os MESMOS nomes de arquivo que o posts.json já aponta —
o robô publica a arte nova sem nenhuma mudança na fila.

Texto CONGELADO (fila_textos_congelados.json): 11 carrosséis pediátricos cuja arte na fila veio de
uma versão anterior do texto-fonte (20/06). Para eles o texto vem do JSON, não do módulo atual —
assim a troca de visual não muda nenhuma palavra do que já estava programado. O 5º slide de
c_pnc_perna_curta_crianca é o card de faixas em cm (gerar_card_resumo_discrepancia.py, 16/08).

Famílias cobertas (todas as da fila em 14/10/2026):
  c_on_* / c_pnc_*  -> gerar_lote_2026.carrossel_de + carrossel.render_post   (images/<id>_N.jpg)
  v_*  (verbetes)   -> gerar_verbetes.renderizar (sem tocar o manifesto)      (verbetes/<id>/sN.jpg)
  postNN do lote 2  -> posts_batch2.POSTS mapeado p/ capa/conteúdo/fecho      (images/<id>_N.jpg)

Fail-loud: se o nº/nome de arquivos gerados não bater com o posts.json, ou se sobrar item da fila
sem gerador conhecido, sai com exit 1 ANTES de qualquer commit (nada meio-feito).

Uso:
  python rerender_fila_v2.py                    # re-renderiza a fila pendente no lugar
  python rerender_fila_v2.py --ids a,b          # só esses ids
  python rerender_fila_v2.py --outdir /tmp/x    # prévia fora do repo (não toca images/ nem verbetes/)
  python rerender_fila_v2.py --listar           # só mostra o que seria refeito
"""
import argparse
import json
import os
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)


def pendentes():
    with open(os.path.join(ROOT, "posts.json"), encoding="utf-8") as f:
        posts = json.load(f)
    with open(os.path.join(ROOT, "state", "published.json"), encoding="utf-8") as f:
        pub = {x["id"] for x in json.load(f)["published"]}
    return [p for p in posts if p["id"] not in pub]


def _lote2026():
    import gerar_lote_2026 as L
    return {"c_" + e["id"]: e for e in L.NEW_EPISODES}, L


def _congelados():
    p = os.path.join(ROOT, "fila_textos_congelados.json")
    if not os.path.exists(p):
        return {}
    with open(p, encoding="utf-8") as f:
        return {k: v["slides"] for k, v in json.load(f).get("itens", {}).items()}


def _substituicoes():
    """Slides trocados de propósito depois do lote (id -> (índice, spec))."""
    out = {}
    try:
        import gerar_card_resumo_discrepancia as G
        out[G.POST_ALVO] = (G.SLIDE_INDEX, G.slide())
    except Exception as e:
        print(f"AVISO: card de faixas indisponível ({e!r})", flush=True)
    return out


def _batch2():
    try:
        import posts_batch2 as B
        return {pid: slides for pid, slides, _cap in B.POSTS}
    except Exception as e:  # gerador antigo ausente: não bloqueia as outras famílias
        print(f"AVISO: posts_batch2 indisponível ({e!r})", flush=True)
        return {}


def _post_do_batch2(pid, slides):
    """Lote 2 (variant/kicker/title/body/tag/foot) -> capa · conteúdo · fecho do template v2.
    Texto palavra por palavra: o fecho usa o próprio corpo do lote 2 ('Fale comigo pelo
    WhatsApp — link na bio') no lugar do bloco de contato padrão."""
    out = []
    for i, s in enumerate(slides):
        if i == 0:
            out.append({"kicker": s.get("kicker", ""), "title": s["title"], "sub": ""})
        elif s.get("foot") or i == len(slides) - 1:
            out.append({"cta": True, "kicker": s.get("kicker", ""), "title": s["title"],
                        "sub": s.get("body", ""), "contato": False})
        else:
            out.append({"kicker": s.get("kicker", ""), "title": s["title"], "body": s.get("body", "")})
    return {"id": pid, "slides": out}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ids", default="")
    ap.add_argument("--outdir", default=None)
    ap.add_argument("--listar", action="store_true")
    a = ap.parse_args()

    import carrossel as C
    import gerar_verbetes as V
    eps, L = _lote2026()
    b2 = _batch2()
    cong = _congelados()
    subs = _substituicoes()
    vids = {V._vid(s) for s in V.CURADORIA}

    fila = pendentes()
    if a.ids:
        quer = {x.strip() for x in a.ids.split(",") if x.strip()}
        fila = [p for p in fila if p["id"] in quer]
    plano, orfaos = [], []
    for p in fila:
        pid = p["id"]
        fam = ("lote2026" if pid in eps else "verbete" if pid in vids else
               "batch2" if pid in b2 else None)
        (plano if fam else orfaos).append((pid, fam, p["images"]))
    for pid, fam, imgs in plano:
        extra = " (texto congelado)" if pid in cong else ""
        print(f"{pid:32} {fam:9} {len(imgs)} slides{extra}", flush=True)
    if orfaos:
        print("SEM GERADOR CONHECIDO (não refeitos):", [o[0] for o in orfaos], flush=True)
    if a.listar:
        return 0

    base = a.outdir or ROOT
    img_dir = os.path.join(base, "images")
    verb_dir = os.path.join(base, "verbetes")
    erros = []
    for pid, fam, esperados in plano:
        if fam == "lote2026":
            post = {"id": pid, "slides": [dict(x) for x in cong[pid]]} if pid in cong else L.carrossel_de(eps[pid])
            if pid in subs:
                i, spec = subs[pid]
                post["slides"][i] = spec
            gerados = C.render_post(post, img_dir)
        elif fam == "batch2":
            gerados = C.render_post(_post_do_batch2(pid, b2[pid]), img_dir)
        else:
            gerados = V.renderizar([pid], outdir=verb_dir, manifesto=False)[0]["slides"]
        if list(gerados) != list(esperados):
            erros.append(f"{pid}: gerados {gerados} != posts.json {esperados}")
        else:
            print(f"ok {pid} ({len(gerados)} slides)", flush=True)
    if erros or orfaos:
        for e in erros:
            print("ERRO:", e, flush=True)
        if orfaos:
            print("ERRO: item(ns) da fila sem gerador no visual v2:", [o[0] for o in orfaos], flush=True)
        return 1
    print(f"FILA RE-RENDERIZADA: {len(plano)} carrossel(éis) no visual v2"
          + (f" em {base}" if a.outdir else ""), flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
