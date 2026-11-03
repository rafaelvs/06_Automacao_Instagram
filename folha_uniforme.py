# -*- coding: utf-8 -*-
"""Folha de contato UNIFORME do mp4 final: 1 quadro a cada PASSO s (a partir de 0,3 s), em grade de 6 colunas,
quadro a 300 px com o instante escrito. A mesma régua para todos (as folhas dos agentes variavam de 12 a 44
quadros e alguns eram 'momentos-chave' escolhidos). Uso: python folha_uniforme.py <mp4> <saida.jpg> [passo]"""
import os, subprocess, sys, tempfile
from PIL import Image, ImageDraw
import imageio_ffmpeg

FF = imageio_ffmpeg.get_ffmpeg_exe()


def duracao(mp4):
    p = subprocess.run([FF, "-i", mp4], capture_output=True, text=True, errors="replace")
    for l in p.stderr.splitlines():
        if "Duration:" in l:
            h, m, s = l.split("Duration:")[1].split(",")[0].strip().split(":")
            return int(h) * 3600 + int(m) * 60 + float(s)
    raise RuntimeError("sem duração: " + mp4)


def folha(mp4, saida, passo=1.5, cols=6, w=300):
    T = duracao(mp4); ts = []
    t = 0.3
    while t < T - 0.05:
        ts.append(round(t, 2)); t += passo
    tmp = tempfile.mkdtemp(prefix="folha_")
    ims = []
    for k, t in enumerate(ts):
        f = os.path.join(tmp, f"q{k:03d}.png")
        subprocess.run([FF, "-v", "error", "-ss", str(t), "-i", mp4, "-frames:v", "1", "-y", f], check=True)
        im = Image.open(f).convert("RGB"); im = im.resize((w, int(im.height * w / im.width)))
        ImageDraw.Draw(im).text((6, 6), f"{t:.1f}s", fill="white")
        ims.append(im)
    h = ims[0].height; rows = (len(ims) + cols - 1) // cols
    m = Image.new("RGB", (cols * w + (cols - 1) * 6, rows * h + (rows - 1) * 6), "white")
    for k, im in enumerate(ims):
        m.paste(im, ((k % cols) * (w + 6), (k // cols) * (h + 6)))
    m.save(saida, quality=85)
    return len(ims), T


if __name__ == "__main__":
    n, T = folha(sys.argv[1], sys.argv[2], float(sys.argv[3]) if len(sys.argv) > 3 else 1.5)
    print(f"{sys.argv[2]}: {n} quadros de {T:.1f} s")
