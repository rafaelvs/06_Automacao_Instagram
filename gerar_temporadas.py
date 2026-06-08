# -*- coding: utf-8 -*-
"""Renderiza TODAS as temporadas serializadas (5 frames/dia) e (re)constroi sequences.json.
Dados em temporadas_data.py (SEASONS). Rode: python gerar_temporadas.py"""
import os, json
from PIL import Image, ImageDraw
from gerar_conteudo import F, wrap, trk, arcs, INK, PAPER, CREAM, GOLD, TXT_L, TXT_D, MUT_L, MUT_D, SB, NR, NB, IMG, ROOT, SIG
from temporadas_data import SEASONS

DISC = "Conteúdo educativo · não substitui avaliação médica."

def seq_story(fn, v, theme, idx, n, segment, title, sub, cue):
    W, H = 1080, 1920; M = 130
    img = Image.new("RGBA", (W, H), (INK if v == "dark" else PAPER) + (255,))
    img = arcs(img, v, W, H); d = ImageDraw.Draw(img)
    tcol = CREAM if v == "dark" else INK
    scol = TXT_L if v == "dark" else TXT_D
    mcol = MUT_L if v == "dark" else MUT_D
    faint = (90, 86, 80) if v == "dark" else (214, 208, 196)
    d.text((M, 150), "RV", font=F(SB, 60), fill=tcol); wf = d.textlength("RV", font=F(SB, 60))
    d.line([(M+wf+24, 162), (M+wf+24, 212)], fill=GOLD, width=2)
    d.text((M+wf+44, 160), "Dr. Rafael Vargas", font=F(NR, 26), fill=tcol)
    d.text((M+wf+44, 194), "Ortopedia · São Paulo", font=F(NR, 22), fill=GOLD)
    trk(d, (W-M, 168), f"{idx}/{n}", F(NB, 34), GOLD, 4, left=False)
    trk(d, (M, 300), theme.upper(), F(NB, 26), GOLD, 5)
    by = 350; bx0 = M; bx1 = W-M; gap = 12; segw = (bx1-bx0-(n-1)*gap)/n
    for i in range(n):
        x = bx0 + i*(segw+gap)
        d.rounded_rectangle([x, by, x+segw, by+10], radius=5, fill=(GOLD if i < idx else faint))
    ky = 640; trk(d, (M, ky), segment.upper(), F(NB, 30), GOLD, 6); d.line([(M, ky+50), (M+70, ky+50)], fill=GOLD, width=3)
    ty = ky+98; tf = F(SB, 88); tl = wrap(d, title, tf, W-2*M)
    if len(tl) > 3: tf = F(SB, 70); tl = wrap(d, title, tf, W-2*M)
    for ln in tl: d.text((M, ty), ln, font=tf, fill=tcol); ty += int(tf.size*1.1)
    by2 = ty+46
    for ln in wrap(d, sub, F(NR, 40), W-2*M): d.text((M, by2), ln, font=F(NR, 40), fill=scol); by2 += 58
    cy = H-360
    for ln in wrap(d, cue, F(NB, 34), W-2*M): d.text((M, cy), ln, font=F(NB, 34), fill=GOLD); cy += 46
    d.text((M, H-210), "@rafaelvargasmd", font=F(NR, 30), fill=mcol)
    d.text((M, H-162), SIG, font=F(NR, 23), fill=mcol)
    d.text((M, H-120), DISC, font=F(NR, 22), fill=mcol)
    img.save(os.path.join(IMG, fn), "JPEG", quality=92)

DOW = ["seg","ter","qua","qui","sex","sab","dom"]
VAR = {"seg":"dark","ter":"light","qua":"dark","qui":"light","sex":"dark","sab":"light","dom":"dark"}

def run():
    seqs = []
    for wk in SEASONS:
        slug = wk["slug"]; theme = wk["theme"]
        for di, day in enumerate(wk["days"]):
            did = DOW[di]; v = VAR[did]; frames = day; n = len(frames)
            imgs = []
            for i, (seg, title, sub, cue) in enumerate(frames, 1):
                fn = f"seq_{slug}_{did}_{i}.jpg"
                seq_story(fn, v, theme, i, n, seg, title, sub, cue)
                imgs.append("images/"+fn)
            seqs.append({"id": f"{slug}-{did}", "theme": theme, "label": frames[0][0], "images": imgs})
        print("ok temporada:", slug, flush=True)
    json.dump(seqs, open(os.path.join(ROOT, "sequences.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print("TEMPORADAS:", len(SEASONS), "| DIAS/SEQUENCIAS:", len(seqs), "| FRAMES:", sum(len(s["images"]) for s in seqs))

if __name__ == "__main__":
    run()
