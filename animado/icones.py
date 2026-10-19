# -*- coding: utf-8 -*-
"""Ícones dos personagens da CONVERSA, desenhados em vetor numa caixa de ~100x120 centrada em
(0, 0). Cada um precisa ser reconhecível pequeno (avatar do cabeçalho) e grande (gancho e CTA)."""
import math

import skia

from .base import ACO, ACO_ESC, OURO, OSSO_C, OSSO_B, OSSO_L, paint


def _abre(cv, x, y, esc, aceno):
    cv.save(); cv.translate(x, y); cv.rotate(aceno); cv.scale(esc, esc)


def fixador(cv, x, y, esc=1.0, alfa=1.0, aceno=0.0):
    A = int(255 * alfa); _abre(cv, x, y, esc, aceno)
    for yy in (-30, 0, 30):
        cv.drawArc(skia.Rect(-40, yy - 9, 40, yy + 9), 180, 180, False, paint(ACO_ESC, A, "stroke", 4.5))
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(-10, -48, 10, 48), 6, 6), paint(OSSO_C, A))
    cv.drawRect(skia.Rect(-15, -50, 15, -40), paint(OSSO_C, A))
    for yy in (-30, 0, 30):
        cv.drawLine(-34, yy - 5, 34, yy + 5, paint("#DDE6EE", A, "stroke", 1.6))
        cv.drawLine(-34, yy + 5, 34, yy - 5, paint("#DDE6EE", A, "stroke", 1.6))
    for sx in (-34, 34):
        cv.drawLine(sx, -30, sx, 30, paint("#8FA3B8", A, "stroke", 3.5))
    for yy in (-30, 0, 30):
        cv.drawArc(skia.Rect(-40, yy - 9, 40, yy + 9), 0, 180, False, paint(ACO, A, "stroke", 4.5))
        cv.drawCircle(-34, yy + 1, 3, paint(OURO, A)); cv.drawCircle(34, yy + 1, 3, paint(OURO, A))
    cv.restore()


def gesso(cv, x, y, esc=1.0, alfa=1.0, aceno=0.0):
    """Gesso de perna (bota) com a trama das faixas e os dedinhos para fora."""
    A = int(255 * alfa); _abre(cv, x, y, esc, aceno)
    p = skia.Path()
    p.moveTo(-22, -52); p.lineTo(22, -52); p.lineTo(20, 18)
    p.cubicTo(22, 30, 40, 34, 46, 44); p.lineTo(46, 54); p.lineTo(-20, 54)
    p.cubicTo(-26, 40, -24, 24, -22, 12); p.close()
    cv.drawPath(p, paint("#000000", int(A * 0.35), blur=5))
    cv.drawPath(p, paint("#F4F6F8", A))
    for k in range(7):                                        # faixas da atadura
        yy = -44 + k * 13
        cv.drawLine(-22, yy, 22, yy + 7, paint("#C9D3DC", A, "stroke", 2))
    cv.drawPath(p, paint("#9AA8B5", A, "stroke", 2.5))
    for k in range(4):                                        # dedos
        cv.drawCircle(48 + (k % 2) * 2, 36 + k * 5, 4.2, paint("#F0B49A", A))
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(-26, -58, 26, -50), 4, 4), paint(OURO, A))   # borda acolchoada
    cv.restore()


def muleta(cv, x, y, esc=1.0, alfa=1.0, aceno=0.0):
    """Muleta axilar: apoio de cima, manopla, hastes que se unem e ponteira."""
    A = int(255 * alfa); _abre(cv, x, y, esc, aceno)
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(-26, -60, 26, -50), 5, 5), paint("#3B4A58", A))   # apoio
    for sx in (-18, 18):
        cv.drawLine(sx, -52, sx * 0.25, 38, paint(ACO, A, "stroke", 5))
    cv.drawLine(-14, -6, 14, -6, paint("#3B4A58", A, "stroke", 7))                 # manopla
    cv.drawLine(0, 36, 0, 54, paint(ACO, A, "stroke", 6))
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(-7, 52, 7, 62), 3, 3), paint("#2A2F35", A))      # ponteira
    cv.restore()


def pinos(cv, x, y, esc=1.0, alfa=1.0, aceno=0.0):
    """Três pinos atravessando a pele (faixa rosada), com a ponta de rosca para fora."""
    A = int(255 * alfa); _abre(cv, x, y, esc, aceno)
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(-50, 8, 50, 40), 12, 12), paint("#F0B49A", A))   # pele
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(-50, 8, 50, 40), 12, 12), paint("#C98A72", A, "stroke", 2))
    for k, sx in enumerate((-28, 0, 28)):
        cv.drawLine(sx, -50, sx, 30, paint("#C4D1DE", A, "stroke", 7))
        for r in range(6):                                    # rosca
            yy = -46 + r * 7
            cv.drawLine(sx - 4, yy, sx + 4, yy + 3, paint(ACO_ESC, A, "stroke", 1.5))
        cv.drawCircle(sx, -52, 6, paint(OURO, A))
        cv.drawCircle(sx, 12, 9, paint("#FFFFFF", int(A * 0.85)))                  # curativo em volta
    cv.restore()


def osso(cv, x, y, esc=1.0, alfa=1.0, aceno=0.0):
    """Osso com um traço de fratura colando (calo dourado no meio)."""
    A = int(255 * alfa); _abre(cv, x, y, esc, aceno)
    p = skia.Path()
    p.moveTo(-12, -40); p.lineTo(12, -40)
    p.cubicTo(30, -40, 30, -62, 14, -58); p.cubicTo(8, -66, -8, -66, -14, -58)
    p.cubicTo(-30, -62, -30, -40, -12, -40); p.close()
    p.addRect(skia.Rect(-12, -42, 12, 42))
    q = skia.Path()
    q.moveTo(-12, 40); q.lineTo(12, 40)
    q.cubicTo(30, 40, 30, 62, 14, 58); q.cubicTo(8, 66, -8, 66, -14, 58)
    q.cubicTo(-30, 62, -30, 40, -12, 40); q.close()
    for pp in (p, q):
        cv.drawPath(pp, paint(OSSO_C, A)); cv.drawPath(pp, paint(OSSO_L, A, "stroke", 2))
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(-16, -6, 16, 8), 6, 6), paint("#F2B544", A))   # calo
    cv.drawLine(-12, 2, 12, -2, paint(OSSO_L, A, "stroke", 2))
    cv.restore()


def tenis(cv, x, y, esc=1.0, alfa=1.0, aceno=0.0):
    """Tênis infantil de lado, sem marca: solado branco, cabedal, cadarço e biqueira."""
    A = int(255 * alfa); _abre(cv, x, y, esc, aceno)
    sola = skia.RRect.MakeRectXY(skia.Rect(-56, 22, 58, 40), 9, 9)
    cv.drawRRect(sola, paint("#000000", int(A * 0.35), blur=5))
    p = skia.Path()                                           # cabedal
    p.moveTo(-50, 24); p.lineTo(-50, -18)
    p.cubicTo(-50, -34, -30, -36, -22, -26)
    p.lineTo(4, 0); p.cubicTo(24, 4, 50, 6, 56, 20); p.lineTo(56, 24); p.close()
    cv.drawPath(p, paint("#3FA7D6", A))
    cv.save(); cv.clipPath(p, skia.ClipOp.kIntersect, True)
    cv.drawCircle(54, 28, 26, paint("#8FD3EE", A))           # biqueira, dentro do cabedal
    cv.restore()
    cv.drawPath(p, paint("#1F5F7E", A, "stroke", 2.5))
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(-54, -40, -18, -28), 6, 6), paint("#1F5F7E", A))  # gola
    for k in range(4):                                        # cadarço cruzado
        xx = -24 + k * 8; yy = -20 + k * 7
        cv.drawLine(xx - 7, yy - 2, xx + 7, yy + 6, paint("#FFFFFF", A, "stroke", 3))
        cv.drawLine(xx - 7, yy + 6, xx + 7, yy - 2, paint("#FFFFFF", A, "stroke", 3))
    cv.drawRRect(sola, paint("#F4F6F8", A))
    cv.drawRRect(sola, paint("#9AA8B5", A, "stroke", 2))
    for k in range(5):                                        # cravos do solado
        cv.drawLine(-44 + k * 22, 36, -36 + k * 22, 36, paint("#C9D3DC", A, "stroke", 2))
    cv.restore()


def pernas(cv, x, y, esc=1.0, alfa=1.0, aceno=0.0):
    """As pernas de uma criança, de frente: bermuda, joelhos, meias e tênis."""
    A = int(255 * alfa); _abre(cv, x, y, esc, aceno)
    bermuda = skia.Path()
    bermuda.moveTo(-36, -60); bermuda.lineTo(36, -60); bermuda.lineTo(40, -22)
    bermuda.lineTo(4, -22); bermuda.lineTo(0, -32); bermuda.lineTo(-4, -22)
    bermuda.lineTo(-40, -22); bermuda.close()
    cv.drawPath(bermuda, paint("#000000", int(A * 0.35), blur=5))
    for sx in (-20, 20):
        cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(sx - 10, -26, sx + 10, 40), 9, 9), paint("#F0B49A", A))
        cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(sx - 10, -26, sx + 10, 40), 9, 9), paint("#C98A72", A, "stroke", 2))
        cv.drawArc(skia.Rect(sx - 6, 2, sx + 6, 12), 200, 140, False, paint("#C98A72", A, "stroke", 2))   # joelho
        cv.drawRect(skia.Rect(sx - 10, 30, sx + 10, 42), paint("#FFFFFF", A))                         # meia
        cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(sx - 14 + (sx > 0) * 4, 40, sx + 14 + (sx > 0) * 4, 56), 7, 7),
                     paint("#3FA7D6", A))                                                               # tênis
    cv.drawPath(bermuda, paint("#E07A5F", A))
    cv.drawPath(bermuda, paint("#9C4A33", A, "stroke", 2.5))
    cv.drawRect(skia.Rect(-36, -60, 36, -53), paint(OURO, A))                                           # cós
    cv.restore()


def fita(cv, x, y, esc=1.0, alfa=1.0, aceno=0.0):
    """Fita métrica de costura enrolada, com a ponta solta e as marcas de centímetro."""
    A = int(255 * alfa); _abre(cv, x, y, esc, aceno)
    cv.drawCircle(-8, -14, 40, paint("#000000", int(A * 0.35), blur=5))
    cv.drawCircle(-8, -14, 40, paint("#F2B544", A))
    for r in (32, 24, 16):                                    # voltas do rolo
        cv.drawCircle(-8, -14, r, paint("#B57F12", A, "stroke", 2))
    cv.drawCircle(-8, -14, 8, paint("#FFF4D6", A))
    tira = skia.Path()                                        # ponta que se desenrola
    tira.moveTo(26, 4); tira.cubicTo(44, 20, 40, 44, 18, 58)
    tira.lineTo(8, 50); tira.cubicTo(26, 40, 30, 24, 16, 12); tira.close()
    cv.drawPath(tira, paint("#F2B544", A))
    cv.drawPath(tira, paint("#B57F12", A, "stroke", 2))
    for k in range(6):                                        # marcas de centímetro
        t = (k + 0.5) / 6
        px = (1 - t) ** 2 * 21 + 2 * (1 - t) * t * 38 + t * t * 13
        py = (1 - t) ** 2 * 8 + 2 * (1 - t) * t * 30 + t * t * 54
        cv.drawLine(px - 4, py, px + (3 if k % 2 else 6), py, paint("#2A2F35", A, "stroke", 1.6))
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(8, 50, 22, 62), 2, 2), paint(ACO, A))      # ponteira de metal
    cv.restore()


ICONES = {"fixador": fixador, "gesso": gesso, "muleta": muleta, "pinos": pinos, "osso": osso,
          "tenis": tenis, "pernas": pernas, "fita": fita}
