# -*- coding: utf-8 -*-
"""Põe um episódio JÁ RENDERIZADO na fila de reels: `python -m animado.anexar <id> [--depois-de <id> | --frente]`.

Monta a entrada de reels.json a partir do episódio — vídeo, legenda (a MESMA função que o portão
usa para conferir: `checar_entretenimento.legenda_de`), `formato` (fora da cota de lâminas),
`scenes` com o texto exato do vídeo (o portão CFM do publish audita isso) e a duração REAL medida no
mp4. Recusa se o mp4 não existir ou se o arquivo-irmão do render (reels/_preview_<id>.json) não
bater com o episódio e o motor atuais: vídeo de outro texto não entra na fila.

Posição (auditoria 19/10): por padrão a peça entra no FIM do bloco da geração nova pendente — a
revisão do Rafael é passiva (ele olha a fila antes da data), e pôr cada peça nova na FRENTE fazia
a peça recém-feita sair no mesmo dia, sem janela. `--depois-de <id>` encaixa logo depois de outra
peça pendente; `--frente` põe na frente de tudo (só com motivo).
"""
import argparse
import json
import os
import sys

# reconfigure (e nao um TextIOWrapper novo): quem importa este modulo ja pode ter
# embrulhado o stdout, e o embrulho antigo, ao ser coletado, FECHA o buffer — o
# render de 19/10 perdeu 3 videos prontos com "I/O operation on closed file".
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)


def entrada(ep):
    import checar_entretenimento as ce
    from checar_dur import duracao_mp4
    video = ce.video_de(ep)
    caminho = os.path.join(ROOT, video.replace("/", os.sep))
    if not os.path.exists(caminho):
        raise SystemExit(f"ERRO: {video} não existe — renderize antes (render-animado.yml).")
    irmao = os.path.join(ROOT, ce.sidecar_de(ep).replace("/", os.sep))
    if not os.path.exists(irmao):
        raise SystemExit(f"ERRO: {ce.sidecar_de(ep)} não existe — o vídeo não prova de qual texto veio. Re-renderize.")
    sc = json.load(open(irmao, encoding="utf-8"))
    if sc.get("hash_episodio") != ce.hash_episodio(ep) or sc.get("hash_motor") != ce.hash_motor(ep):
        raise SystemExit(f"ERRO: {video} foi renderizado de outro texto ou de outro motor. Re-renderize.")
    return {"id": ep["id"], "video": video, "caption": ce.legenda_de(ep), "formato": ep["formato"],
            "serie": ep["serie"], "dur": round(duracao_mp4(caminho), 1), "voz_ia": True, "scenes": ce.cenas_de(ep)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("id")
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--depois-de", default="")
    g.add_argument("--frente", action="store_true")
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
    pend = [i for i, r in enumerate(reels) if r["id"] not in done]
    if a.depois_de:
        idx = next((i for i, r in enumerate(reels) if r["id"] == a.depois_de), None)
        if idx is None:
            raise SystemExit(f"ERRO: --depois-de {a.depois_de!r} não está na fila.")
        reels.insert(idx + 1, novo)
    elif a.frente:
        reels.insert(pend[0] if pend else len(reels), novo)
    else:
        novos = [i for i in pend if reels[i].get("formato")]
        reels.insert(novos[-1] + 1 if novos else (pend[0] if pend else len(reels)), novo)
    with open(p, "w", encoding="utf-8", newline="\n") as f:
        json.dump(reels, f, ensure_ascii=False, indent=1); f.write("\n")
    print(f"anexado: {a.id} ({ep['formato']}, {novo['dur']}s) na posição {reels.index(novo)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
