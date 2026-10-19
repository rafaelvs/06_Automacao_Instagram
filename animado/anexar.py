# -*- coding: utf-8 -*-
"""Põe um episódio JÁ RENDERIZADO na fila de reels: `python -m animado.anexar <id> [--depois-de <id>]`.

Monta a entrada de reels.json a partir do episódio — vídeo, legenda normalizada (uma CTA = a do
vídeo, menção, assinatura com "Médico", declaração de voz de IA que liga o rótulo da Meta),
`formato` (fora da cota de lâminas), `scenes` com o texto exato do vídeo (o portão CFM do publish
audita isso) e a duração REAL medida no mp4. Recusa se o mp4 não existir: peça sem vídeo na fila
faria o publish falhar ALTO na data.

Posição: por padrão a peça entra na FRENTE dos itens pendentes (a geração nova tem prioridade);
`--depois-de <id>` encaixa logo depois de outra peça pendente.
"""
import argparse
import io
import json
import os
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
TAIL_IA = "Narração com voz digital (IA)."


def entrada(ep):
    import legenda
    from checar_dur import duracao_mp4
    from checar_entretenimento import cenas_de
    video = f"reels/_preview_{ep['id']}.mp4"
    caminho = os.path.join(ROOT, video.replace("/", os.sep))
    if not os.path.exists(caminho):
        raise SystemExit(f"ERRO: {video} não existe — renderize antes (render-animado.yml).")
    legenda.CTA_POR_ID[ep["id"]] = ep["cta"]          # a CTA da legenda é a mesma do vídeo
    cap = legenda.normalizar(f"{ep['legenda']}\n\n{TAIL_IA}", "reel", ep["id"], fam=ep["familia"])
    return {"id": ep["id"], "video": video, "caption": cap, "formato": ep["formato"], "serie": ep["serie"],
            "dur": round(duracao_mp4(caminho), 1), "voz_ia": True, "scenes": cenas_de(ep)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("id")
    ap.add_argument("--depois-de", default="")
    a = ap.parse_args()
    from episodios_entretenimento import EPISODIOS_ENTRETENIMENTO
    ep = next((e for e in EPISODIOS_ENTRETENIMENTO if e["id"] == a.id), None)
    if not ep:
        raise SystemExit(f"ERRO: episódio {a.id!r} não existe.")
    novo = entrada(ep)
    p = os.path.join(ROOT, "reels.json")
    reels = json.load(open(p, encoding="utf-8-sig"))
    done = {e["id"] for e in json.load(open(os.path.join(ROOT, "state", "published.json"), encoding="utf-8"))["published"]}
    if a.id in done:
        raise SystemExit(f"ERRO: {a.id} já foi publicado — não se reanexa.")
    reels = [r for r in reels if r["id"] != a.id]
    if a.depois_de:
        idx = next((i for i, r in enumerate(reels) if r["id"] == a.depois_de), None)
        if idx is None:
            raise SystemExit(f"ERRO: --depois-de {a.depois_de!r} não está na fila.")
        reels.insert(idx + 1, novo)
    else:
        idx = next((i for i, r in enumerate(reels) if r["id"] not in done), len(reels))
        reels.insert(idx, novo)
    with open(p, "w", encoding="utf-8", newline="\n") as f:
        json.dump(reels, f, ensure_ascii=False, indent=1); f.write("\n")
    print(f"anexado: {a.id} ({ep['formato']}, {novo['dur']}s) na posição {reels.index(novo)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
