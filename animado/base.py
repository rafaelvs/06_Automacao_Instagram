# -*- coding: utf-8 -*-
"""Peças comuns aos formatos animados: paleta, texto, easing, identificação CFM, cartão final e
codificação do vídeo (H.264 + AAC 48 kHz — o Instagram não aceita áudio acima de 48 kHz, e o
`loudnorm` do ffmpeg sobe a taxa se não for forçada)."""
import os
import subprocess

import skia

from . import fontes, voz

W, H, FPS = 1080, 1920, 30
SIG = "Dr. Rafael Vargas · Médico · CRM-SP 226103 · RQE 137901"
DISC = "Conteúdo educativo · não substitui avaliação médica · voz digital (IA)"

BG_IN, BG_OUT = "#17384C", "#0A1520"
OURO, OURO_ESC = "#F5C04A", "#8A5A00"
ACO, ACO_ESC, ACO_HL = "#A9BCCF", "#5E7186", "#E6EEF6"
OSSO_C, OSSO_B, OSSO_L = "#F7EEDD", "#D5C3A2", "#8C7656"
VERMELHO = "#FF5A5F"


def C(hexs, a=255):
    h = hexs.lstrip("#")
    return skia.ColorSetARGB(int(a), int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))


def clamp(x, a=0.0, b=1.0): return max(a, min(b, x))
def prog(t, a, b): return clamp((t - a) / (b - a)) if b > a else float(t >= a)
def e_out(x): return 1 - (1 - x) ** 3
def e_inout(x): return 3 * x * x - 2 * x * x * x
def e_back(x, s=1.7):
    x -= 1
    return x * x * ((s + 1) * x + s) + 1
def e_in_back(x, s=1.7): return x * x * ((s + 1) * x - s)
def lerp(a, b, x): return a + (b - a) * x
def lerpc(c1, c2, x):
    a = [int(c1[i:i + 2], 16) for i in (1, 3, 5)]; b = [int(c2[i:i + 2], 16) for i in (1, 3, 5)]
    return "#" + "".join(f"{int(lerp(a[i], b[i], x)):02X}" for i in range(3))


def paint(cor, a=255, estilo="fill", w=0, blur=0, shader=None):
    p = skia.Paint(AntiAlias=True)
    p.setColor(C(cor, a))
    p.setStyle(skia.Paint.kStroke_Style if estilo == "stroke" else skia.Paint.kFill_Style)
    if w: p.setStrokeWidth(w)
    if estilo == "stroke": p.setStrokeCap(skia.Paint.kRound_Cap)
    if blur: p.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, blur))
    if shader is not None: p.setShader(shader)
    return p


def F(papel):
    return fontes.fonte(papel)


def texto(cv, s, x, y, papel, tam, cor, a=255, centro=True, contorno=0, track=0.0):
    f = skia.Font(F(papel), tam); f.setEdging(skia.Font.Edging.kAntiAlias)
    larg = f.measureText(s) + track * max(0, len(s) - 1)
    x0 = x - larg / 2 if centro else x
    if track:
        cx = x0
        for ch in s:
            if contorno: cv.drawString(ch, cx, y, f, paint("#000000", int(a * 0.85), "stroke", contorno))
            cv.drawString(ch, cx, y, f, paint(cor, a)); cx += f.measureText(ch) + track
    else:
        if contorno: cv.drawString(s, x0, y, f, paint("#000000", int(a * 0.85), "stroke", contorno))
        cv.drawString(s, x0, y, f, paint(cor, a))
    return larg


def larg_texto(s, papel, tam):
    return skia.Font(F(papel), tam).measureText(s)


def quebrar(palavras, papel, tam, larg_max):
    f = skia.Font(F(papel), tam); esp = f.measureText(" ")
    linhas, linha, lw = [], [], 0
    for i, w in enumerate(palavras):
        ww = f.measureText(w)
        if linha and lw + esp + ww > larg_max:
            linhas.append(linha); linha, lw = [], 0
        linha.append((i, w, ww)); lw += (esp if lw else 0) + ww
    if linha: linhas.append(linha)
    return linhas, esp


def fundo_gradiente(cv, cy=None):
    sh = skia.GradientShader.MakeRadial(skia.Point(W / 2, cy if cy is not None else H * 0.45), H * 0.8,
                                        [C(BG_IN), C(BG_OUT)])
    cv.drawRect(skia.Rect(0, 0, W, H), paint(BG_IN, shader=sh))


def rodape_cfm(cv, t, t_fim, y=1585):
    """Identificação na tela a partir de 3 s (decisão D9) até a entrada do cartão final."""
    if 3.0 <= t < t_fim:
        a = prog(t, 3.0, 3.6)
        texto(cv, SIG, W / 2, y, "semi", 27, "#FFFFFF", int(200 * a))
        texto(cv, DISC, W / 2, y + 35, "reg", 23, "#FFFFFF", int(150 * a))


def cartao_id(cv, a, y=1060):
    rr = skia.RRect.MakeRectXY(skia.Rect(150, y, 930, y + 154), 28, 28)
    cv.drawRRect(rr, paint("#0B1824", int(230 * a)))
    cv.drawRRect(rr, paint(OURO, int(255 * a), "stroke", 3))
    texto(cv, "Dr. Rafael Vargas · Médico ortopedista", W / 2, y + 52, "black", 36, "#FFFFFF", int(255 * a))
    texto(cv, "CRM-SP 226103 · RQE 137901 · @rafaelvargasmd", W / 2, y + 94, "semi", 28, OURO, int(255 * a))
    texto(cv, DISC, W / 2, y + 130, "reg", 22, "#FFFFFF", int(170 * a))


def codificar(quadro_fn, total, wav, mp4):
    """Renderiza quadro a quadro (quadro_fn(canvas, t)) direto para o ffmpeg, sem PNG em disco."""
    os.makedirs(os.path.dirname(os.path.abspath(mp4)), exist_ok=True)
    proc = subprocess.Popen([voz.ffmpeg(), "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgba",
                             "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-i", wav,
                             "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-pix_fmt", "yuv420p",
                             "-c:a", "aac", "-b:a", "192k", "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-ar", "48000",
                             "-shortest", "-movflags", "+faststart", mp4], stdin=subprocess.PIPE)
    surf = skia.Surface(W, H); n = int(total * FPS)
    for i in range(n):
        cv = surf.getCanvas(); cv.clear(C(BG_OUT)); quadro_fn(cv, i / FPS)
        proc.stdin.write(surf.makeImageSnapshot().toarray(colorType=skia.kRGBA_8888_ColorType).tobytes())
        if i % 150 == 0:
            print(f"  quadro {i}/{n}", flush=True)
    proc.stdin.close()
    if proc.wait() != 0:
        raise SystemExit(f"ERRO: ffmpeg falhou ao codificar {mp4}")


def previas(quadro_fn, tempos, pasta, prefixo):
    os.makedirs(pasta, exist_ok=True)
    surf = skia.Surface(W, H); saidas = []
    for x in tempos:
        cv = surf.getCanvas(); cv.clear(C(BG_OUT)); quadro_fn(cv, x)
        caminho = os.path.join(pasta, f"{prefixo}_{int(x * FPS):04d}.png")
        surf.makeImageSnapshot().save(caminho, skia.kPNG); saidas.append(caminho)
    return saidas
