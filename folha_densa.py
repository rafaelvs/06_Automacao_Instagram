# -*- coding: utf-8 -*-
"""Folhas DENSAS para inspeção de anatomia: 1 quadro a cada PASSO s, recorte da área de cena, em folhas de 24 quadros
(6x4) com o instante escrito. Uso: python folha_densa.py <mp4> <pasta_saida> [passo=0.3]"""
import glob, os, subprocess, sys, tempfile
from PIL import Image, ImageDraw
import imageio_ffmpeg
FF = imageio_ffmpeg.get_ffmpeg_exe()


def folhas(mp4, out, passo=0.3, w=300, por=24, cols=6):
    os.makedirs(out, exist_ok=True)
    tmp = tempfile.mkdtemp(prefix="dens_")
    subprocess.run([FF, "-v", "error", "-i", mp4, "-vf", f"fps=1/{passo},scale={w}:-1", os.path.join(tmp, "q%04d.png")], check=True)
    qs = sorted(glob.glob(os.path.join(tmp, "q*.png")))
    feitas = []
    for k in range(0, len(qs), por):
        ims = []
        for j, q in enumerate(qs[k:k + por]):
            im = Image.open(q).convert("RGB")
            t = (k + j) * passo
            d = ImageDraw.Draw(im); d.rectangle((0, 0, 58, 16), fill="black"); d.text((3, 2), f"{t:5.1f}s", fill="white")
            ims.append(im)
        h = ims[0].height; rows = (len(ims) + cols - 1) // cols
        m = Image.new("RGB", (cols * w + (cols - 1) * 4, rows * h + (rows - 1) * 4), "white")
        for j, im in enumerate(ims):
            m.paste(im, ((j % cols) * (w + 4), (j // cols) * (h + 4)))
        p = os.path.join(out, f"folha_{k // por + 1:02d}.jpg"); m.save(p, quality=86); feitas.append(p)
    return feitas


if __name__ == "__main__":
    fs = folhas(sys.argv[1], sys.argv[2], float(sys.argv[3]) if len(sys.argv) > 3 else 0.3)
    print(len(fs), "folhas em", sys.argv[2])
