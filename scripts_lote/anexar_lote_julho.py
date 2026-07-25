# -*- coding: utf-8 -*-
"""
Assembler do LOTE JULHO/2026 — monta as entradas do reels.json a partir dos vídeos já renderizados
(reels/_preview_<id>.mp4 pelo gerar_reel_voz). Idempotente: pula quem já está no reels.json.
Roda no GitHub Actions, DEPOIS do passo de render (tem ffprobe + os mp4 commitados na árvore).

Convenção (igual ao LOTE 2026): reels.json id = id do episódio; video = reels/_preview_<id>.mp4.
Os novos são ANEXADOS NO FIM (publicam DEPOIS de toda a fila atual — dá margem de QA visual no
Cowork antes de irem ao ar). Mantém o modelo BIBLIOTECA (sem repetir).
"""
import os, glob, json, subprocess
from episodios_lote_julho_2026 import LOTE_JULHO

ROOT = os.path.dirname(os.path.abspath(__file__))
AUD = os.path.join(ROOT, "audio")
RJ = os.path.join(ROOT, "reels.json")

def dur_of(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                          "-of", "default=nw=1:nk=1", path], capture_output=True, text=True).stdout.strip()
    return round(float(out), 1) if out else None

def music_for(ep):
    # mesma regra do gerar_reel_voz: tracks[ep%len(tracks)]
    tracks = sorted(glob.glob(AUD + "/*.mp4") + glob.glob(AUD + "/*.mp3"))
    return os.path.basename(tracks[ep["ep"] % len(tracks)]) if tracks else None

def main():
    reels = json.load(open(RJ, encoding="utf-8"))
    existing = {r["id"] for r in reels}
    novos = []
    for ep in LOTE_JULHO:
        rid = ep["id"]
        if rid in existing:
            print("pulando (ja no reels.json):", rid); continue
        video = "reels/_preview_" + rid + ".mp4"
        path = os.path.join(ROOT, video)
        if not os.path.exists(path):
            print("SEM VIDEO (render falhou?), pulando:", rid); continue
        novos.append({"id": rid, "video": video, "caption": ep["caption"],
                      "music": music_for(ep), "dur": dur_of(path), "serie": ep["serie"]})
        print("ok", rid, "| dur", novos[-1]["dur"], "| serie", ep["serie"])
    if not novos:
        print("Nada novo a anexar."); return
    reels = reels + novos  # ANEXA NO FIM: novos publicam depois da fila atual (QA-first)
    json.dump(reels, open(RJ, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print("reels.json:", len(reels), "| novos anexados:", len(novos))

if __name__ == "__main__":
    main()
