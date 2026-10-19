# -*- coding: utf-8 -*-
"""COMO FUNCIONA — displasia do quadril do bebê ("O teste do pezinho não detecta isso.").

Mesmo estilo das cenas aprovadas (fundo azul-petróleo, marfim, dourado, rótulos com fio, carimbo,
checklist, calendário, legenda karaokê, CTA com aviãozinho). Storyboard e correções do verificador
(lote3_cf/cf_quadril_bebe_storyboard.json) respeitados aqui:
  * O encaixe é ESQUEMÁTICO: uma concha marfim em arco e uma haste com uma bola na ponta. A bola
    assenta SEM som de clique (clique no quadril é sinal de alerta na legenda) — a peça não usa
    "click" nem "tick", e sons() recusa tick/click/pop/ping enquanto a bola volta ao centro.
  * "DISPLASIA" entra como rótulo sóbrio, sem carimbo e sem tremor; o único carimbo é o espanto
    factual "NÃO DETECTA".
  * "Não encaixa bem" = a bola desce um pouco do centro e fica PARADA, com folga tingida de
    vermelho suave. Não oscila, não passa da borda, a concha não fica rasa.
  * Ultrassom = ícone do transdutor (ponteira e cabo), contorno de aço. Nenhuma tela, nenhuma
    imagem de exame, nenhum fundo preto.
  * Pernas de DESENHO (pele lisa, sem osso, nada translúcido), deitadas no trocador, de fralda.
    O "abre menos" é um arco tracejado menor, sem manobra de exame e sem estalo.
  * Suspensório = ícone de roupa (alças azul-claras e fivela) AO LADO do encaixe: não toca na haste
    nem na bola, e o bebê não é desenhado. A bola começa a voltar no "reposiciona" e só chega ao
    centro durante o calendário; o contorno se apaga para o marfim neutro (sem dourado, sem
    brilho, sem carimbo de resultado).
A cena é PRESA ao roteiro pelas palavras-âncora (ANCORAS): roteiro sem elas = KeyError no render,
em vez de vídeo dessincronizado.
"""
import math

import skia

from .cf_alongamento import (ACO, ACO_ESC, ACO_HL, F_BLACK, F_SEMI, OSSO_B, OSSO_C, OSSO_L, OURO, PELE, W, C,
                             brilhos, clamp, e_back, e_inout, e_out, fundo, lerp, lerpc, paint, prog, texto)
from .cf_alongamento import carimbo as carimbo_vermelho
from .cf_comum import capa, fazer_render, interface, selo_como_funciona
from .cf_fratura_cola import calendario

# ------------------------------------------------------------------ sincronia com a fala
ANCORAS = {
    "encaixe": ("encaixe", 1, False), "displasia": ("displasia", 1, False), "cabeca": ("cabeça", 1, False),
    "bem": ("bem", 1, False), "teste": ("teste", 1, False), "pezinho": ("pezinho", 1, False),
    "detecta": ("detecta", 1, False), "exame": ("exame", 1, False), "as": ("às", 1, False),
    "ultrassom": ("ultrassom", 1, False), "fralda": ("fralda", 1, False), "repare": ("repare", 1, False),
    "dobrinhas": ("dobrinhas", 1, False), "perna": ("perna", 1, False), "lado": ("lado", 1, False),
    "duvida": ("dúvida", 1, False), "ortopedista": ("ortopedista", 1, False), "achado": ("achado", 1, False),
    "suspensorio": ("suspensório", 1, False), "reposiciona": ("reposiciona", 1, False),
    "semanas": ("semanas", 1, False), "manda": ("manda", 1, False),
}
DESTAQUE = {"encaixe", "displasia", "fêmur", "pezinho", "detecta", "exame", "ultrassom", "fralda", "dobrinhas",
            "curta", "menos", "dúvida", "ortopedista", "pediátrico", "cedo", "suspensório", "reposiciona",
            "semanas"}

FUNDO_CARTAO = "#0B1824"
VERM_SUAVE = "#F08487"
MARFIM_NEUTRO = "#E2D3B6"
AZUL_CLARO = "#9CC9FF"
PELE_CL, PELE_ESC, PELE_LINHA = "#F7CDB8", "#DA987E", "#B9765E"
FRALDA, FRALDA_SOMBRA, FRALDA_LINHA = "#F4F7FB", "#CBD7E4", "#97AABE"
SUSP, SUSP_ESC = "#8FC3EA", "#4D83B0"
TAPETE, TAPETE_BORDA = "#21506A", "#4A7E9C"


# ------------------------------------------------------------------ utilidades
def _alfa(a):
    p = skia.Paint()
    p.setAlphaf(clamp(a))
    return p


def janela(t, t0, t1, d_in=0.25, d_out=0.3):
    return prog(t, t0, t0 + d_in) * (1 - prog(t, t1, t1 + d_out))


def ponta(cv, x, y, ang, tam, cor, a):
    p = skia.Path()
    p.moveTo(x + tam * math.cos(ang), y + tam * math.sin(ang))
    p.lineTo(x + tam * 0.75 * math.cos(ang + 2.45), y + tam * 0.75 * math.sin(ang + 2.45))
    p.lineTo(x + tam * 0.75 * math.cos(ang - 2.45), y + tam * 0.75 * math.sin(ang - 2.45))
    p.close()
    cv.drawPath(p, paint(cor, int(255 * a)))


def seta_pts(cv, pts, cor, a, larg=7, tam=22):
    if a <= 0 or len(pts) < 2:
        return
    p = skia.Path(); p.moveTo(*pts[0])
    for q in pts[1:]:
        p.lineTo(*q)
    cv.drawPath(p, paint(cor, int(90 * a), "stroke", larg + 8, blur=6))
    cv.drawPath(p, paint(cor, int(255 * a), "stroke", larg))
    (x0, y0), (x1, y1) = pts[-2], pts[-1]
    ponta(cv, x1, y1, math.atan2(y1 - y0, x1 - x0), tam, cor, a)


def arco_pts(cx, cy, r, a0, a1, n=24):
    return [(cx + r * math.cos(math.radians(lerp(a0, a1, k / n))), cy + r * math.sin(math.radians(lerp(a0, a1, k / n))))
            for k in range(n + 1)]


def curva(p0, p1, p2, n=16):
    return [((1 - u) ** 2 * p0[0] + 2 * (1 - u) * u * p1[0] + u * u * p2[0],
             (1 - u) ** 2 * p0[1] + 2 * (1 - u) * u * p1[1] + u * u * p2[1]) for u in (k / n for k in range(n + 1))]


def chip(cv, s, x, y, cor, a, tam=40, borda=None, alinh="c"):
    """Rótulo solto em caixa opaca. alinh 'c': x = centro; 'e': x = borda esquerda da caixa.
    y = linha de base do texto."""
    if a <= 0:
        return
    f = skia.Font(F_BLACK, tam); lw = f.measureText(s)
    x0 = x - lw / 2 if alinh == "c" else x + 24
    rr = skia.RRect.MakeRectXY(skia.Rect(x0 - 24, y - tam * 1.05, x0 + lw + 24, y + tam * 0.34), 16, 16)
    cv.drawRRect(rr, paint(FUNDO_CARTAO, int(225 * a)))
    cv.drawRRect(rr, paint(borda or cor, int(255 * a), "stroke", 3))
    cv.drawString(s, x0, y, f, paint(cor, int(255 * a)))


def rotulo_fio(cv, s, bx, y, xa, ya, cor, a, tam=40):
    """Caixa opaca com fio que sai do ponto (xa, ya) e termina na borda ESQUERDA da caixa."""
    if a <= 0:
        return
    f = skia.Font(F_BLACK, tam); lw = f.measureText(s)
    yc = y - tam * 0.42
    cv.drawLine(xa, ya, bx, yc, paint(cor, int(210 * a), "stroke", 2.5))
    cv.drawCircle(xa, ya, 6, paint(cor, int(255 * a)))
    rr = skia.RRect.MakeRectXY(skia.Rect(bx, y - tam * 1.1, bx + lw + 30, y + tam * 0.25), 14, 14)
    cv.drawRRect(rr, paint(FUNDO_CARTAO, int(230 * a)))
    cv.drawRRect(rr, paint(cor, int(255 * a), "stroke", 2.5))
    cv.drawString(s, bx + 15, y - tam * 0.075, f, paint(cor, int(255 * a)))


def caixa_check(cv, x0, y, t_ok, t, a, tam=50):
    """Caixinha do checklist (mesmo traço do cf_fratura_cola); o check se desenha em `t_ok`."""
    if a <= 0:
        return
    rr = skia.RRect.MakeRectXY(skia.Rect(x0, y - tam * 0.84, x0 + tam, y + tam * 0.16), 10, 10)
    cv.drawRRect(rr, paint(FUNDO_CARTAO, int(220 * a)))
    cv.drawRRect(rr, paint(OURO, int(255 * a), "stroke", 3.5))
    if t >= t_ok:
        k = tam / 50
        pr = e_out(clamp((t - t_ok) / 0.3))
        p = skia.Path(); p.moveTo(x0 + 10 * k, y - 18 * k)
        p.lineTo(x0 + (10 + 12 * min(1, pr * 2)) * k, y + (-18 + 12 * min(1, pr * 2)) * k)
        if pr > 0.5:
            q = (pr - 0.5) * 2
            p.lineTo(x0 + (22 + 22 * q) * k, y + (-6 - 30 * q) * k)
        cv.drawPath(p, paint(OURO, int(255 * a), "stroke", 6))


# ------------------------------------------------------------------ o encaixe (coordenadas locais)
R_BOLA, R_IN, CORTE = 95, 103, 18
INCL = 16                         # a haste desce inclinada para a esquerda (não vira um cogumelo)


def _concha():
    ext = skia.Path(); ext.addCircle(0, -4, 162)
    faixa = skia.Path(); faixa.addRect(skia.Rect(-400, -400, 400, CORTE))
    p = skia.Op(ext, faixa, skia.PathOp.kIntersect_PathOp)
    oco = skia.Path(); oco.addCircle(0, 0, R_IN)
    return skia.Op(p, oco, skia.PathOp.kDifference_PathOp)


def _boca():
    oco = skia.Path(); oco.addCircle(0, 0, R_IN)
    faixa = skia.Path(); faixa.addRect(skia.Rect(-400, -400, 400, CORTE))
    return skia.Op(oco, faixa, skia.PathOp.kIntersect_PathOp)


def _haste():
    p = skia.Path()
    p.moveTo(-40, 30)
    p.cubicTo(-46, 120, -66, 200, -64, 300)
    p.lineTo(-64, 470); p.lineTo(64, 470); p.lineTo(64, 300)
    p.cubicTo(66, 200, 46, 120, 40, 30)
    p.close()
    return p


CONCHA, BOCA, HASTE_P = _concha(), _boca(), _haste()


def _femur(cv):
    """Haste marfim com a bola na ponta (o 'fêmur' esquemático); a haste dissolve no fundo."""
    cv.saveLayer(skia.Rect(-140, -20, 140, 490), None)
    sh = skia.GradientShader.MakeLinear([skia.Point(-70, 0), skia.Point(70, 0)],
                                        [C(OSSO_B), C(OSSO_C), C(OSSO_C), C(OSSO_B)], [0.0, 0.42, 0.58, 1.0])
    cv.drawPath(HASTE_P, paint(OSSO_C, shader=sh))
    cv.drawPath(HASTE_P, paint(OSSO_L, 150, "stroke", 2.5))
    m = skia.Paint(AntiAlias=True)
    m.setShader(skia.GradientShader.MakeLinear([skia.Point(0, 220), skia.Point(0, 440)],
                                               [skia.ColorSetARGB(255, 0, 0, 0), skia.ColorSetARGB(0, 0, 0, 0)]))
    m.setBlendMode(skia.BlendMode.kDstIn)
    cv.drawRect(skia.Rect(-140, -20, 140, 490), m)
    cv.restore()
    cv.drawCircle(0, 8, R_BOLA, paint("#000000", 60, blur=14))
    rad = skia.GradientShader.MakeRadial(skia.Point(-34, -36), 160, [C(OSSO_C), C(OSSO_C), C(OSSO_B)], [0.0, 0.45, 1.0])
    cv.drawCircle(0, 0, R_BOLA, paint(OSSO_C, shader=rad))
    cv.drawCircle(0, 0, R_BOLA, paint(OSSO_L, 150, "stroke", 2.5))


def estado_junta(t, T):
    """(dx, dy) da bola, cor e alfa do contorno, folga (0-1) e alfa do alvo pontilhado."""
    sobe = 1 - e_inout(prog(t, 0.0, T["encaixe"] + 0.12))           # a haste sobe e assenta, suave
    desl = e_inout(prog(t, T["bem"], T["bem"] + 0.7))                 # sai do centro e PARA
    volta = e_inout(prog(t, T["reposiciona"], T["semanas"] + 1.5))     # devagar; termina DURANTE o calendário
    frac = desl * (1 - volta)
    # Folga pequena: o centro da bola fica no máximo ~6 px abaixo da boca (CORTE) — a bola NÃO passa da
    # borda (lê "não encaixa bem", não "saiu"). A capa mostra exatamente o mesmo estado do "bem".
    g = frac + sobe                                                   # nunca os dois > 0 ao mesmo tempo
    dx, dy = -8 * g, 24 * g
    cor = lerpc(OURO, VERM_SUAVE, prog(t, T["bem"], T["bem"] + 0.6))
    neutro = e_inout(prog(t, T["semanas"], T["semanas"] + 1.5))
    cor = lerpc(cor, MARFIM_NEUTRO, neutro)
    a_cont = prog(t, T["encaixe"] - 0.05, T["encaixe"] + 0.3) * (1 - 0.1 * neutro)   # marfim cheio: a bola ASSENTA
    alvo = prog(t, T["reposiciona"], T["reposiciona"] + 0.4) * (1 - prog(t, T["semanas"] + 1.1, T["semanas"] + 1.7))
    return dx, dy, cor, a_cont, frac, alvo


def junta(cv, t, T, pose):
    x, y, s, a = pose
    if a <= 0:
        return
    dx, dy, cor, a_cont, folga, alvo = estado_junta(t, T)
    cv.saveLayer(None, _alfa(a)) if a < 1 else cv.save()
    cv.translate(x, y); cv.scale(s, s)
    if folga > 0.01:                                                  # a folga, tingida de vermelho suave
        cv.save(); cv.clipPath(BOCA, skia.ClipOp.kIntersect, True)
        cv.drawRect(skia.Rect(-130, -130, 130, 40), paint(cor, int(80 * folga)))
        cv.restore()
    if alvo > 0:                    # onde a bola deve ficar: ANTES da bola, só aparece o trecho na folga
        pd = paint(MARFIM_NEUTRO, int(210 * alvo), "stroke", 4)
        pd.setPathEffect(skia.DashPathEffect.Make([16, 12], 0))
        cv.drawCircle(0, 0, R_BOLA, pd)
    cv.save(); cv.translate(dx, dy); cv.rotate(INCL); _femur(cv); cv.restore()
    cv.drawPath(CONCHA, paint("#000000", 70, blur=14))
    sh = skia.GradientShader.MakeLinear([skia.Point(0, -166), skia.Point(0, CORTE)], [C(OSSO_C), C(OSSO_B)])
    pf = paint(OSSO_C, shader=sh); pf.setPathEffect(skia.CornerPathEffect.Make(22))
    cv.drawPath(CONCHA, pf)
    po = paint(OSSO_L, 160, "stroke", 2.5); po.setPathEffect(skia.CornerPathEffect.Make(22))
    cv.drawPath(CONCHA, po)
    if a_cont > 0:
        r = skia.Rect(-100, -100, 100, 100)
        cv.drawArc(r, 172, 196, False, paint(cor, int(120 * a_cont), "stroke", 20, blur=10))
        cv.drawArc(r, 172, 196, False, paint(cor, int(255 * a_cont), "stroke", 6))
    brilhos(cv, 0, -40, t, T["encaixe"] + 0.12, n=12, raio=170)       # só no encaixe normal
    cv.restore()


def pose_junta(t, T):
    """(x, y, escala, alfa) do encaixe na tela: centro -> canto (teste do pezinho) -> some na fralda
    -> volta no 'achado' -> esmaece sob a CTA."""
    x, y, s = 440.0, 770.0, 1.0
    s = lerp(s, 1.06, e_inout(prog(t, T["cabeca"], T["cabeca"] + 0.7)))
    k = e_inout(prog(t, T["teste"] - 0.05, T["teste"] + 0.6))
    x, y, s = lerp(x, 175, k), lerp(y, 420, k), lerp(s, 0.45, k)   # a haste some antes do cartão (y 640)
    a = 1 - prog(t, T["fralda"] - 0.45, T["fralda"] - 0.1)
    if t >= T["achado"] - 0.15:
        k = e_out(prog(t, T["achado"] - 0.15, T["achado"] + 0.55))
        x, y, s, a = 370.0, lerp(720, 640, k), lerp(0.66, 0.82, k), k
    a *= 1 - prog(t, T["manda"] - 0.45, T["manda"] - 0.05)
    return x, y, s, a


def l2w(pose, lx, ly):
    x, y, s, _ = pose
    return x + s * lx, y + s * ly


def polar(r, ang):
    return r * math.cos(math.radians(ang)), r * math.sin(math.radians(ang))


# ------------------------------------------------------------------ ato 1: o encaixe e a displasia
def rotulos_abertura(cv, t, T, pose):
    sai = 1 - prog(t, T["teste"] - 0.2, T["teste"] + 0.1)
    xa, ya = l2w(pose, *polar(100, -55))
    rotulo_fio(cv, "ENCAIXE", 700, 600, xa, ya, OURO,
               prog(t, T["encaixe"] + 0.05, T["encaixe"] + 0.3) * (1 - prog(t, T["cabeca"] - 0.25, T["cabeca"] + 0.05)))
    k = e_out(prog(t, T["displasia"], T["displasia"] + 0.45))         # rótulo sóbrio: só desliza
    chip(cv, "DISPLASIA", lerp(-360, 56, k), 488, "#FFFFFF", k * sai, tam=44, borda=AZUL_CLARO, alinh="e")
    a = janela(t, T["cabeca"], T["bem"] - 0.05, 0.25, 0.3)
    if a > 0:
        dx, dy, *_ = estado_junta(t, T)
        bx, by = l2w(pose, *(v + d for v, d in zip(polar(R_BOLA + 14, 38), (dx, dy))))
        cresce = e_out(prog(t, T["cabeca"], T["cabeca"] + 0.35))
        pts = curva((625, 915), (588, 852), (bx, by))
        seta_pts(cv, pts[:max(2, int(len(pts) * cresce))], OURO, a, larg=6, tam=22)
        chip(cv, "CABEÇA DO FÊMUR", 558, 985, OURO, a, tam=40, alinh="e")
    xa, ya = l2w(pose, *polar(99, -55))
    rotulo_fio(cv, "NÃO ENCAIXA BEM", 572, 600, xa, ya, VERM_SUAVE,
               prog(t, T["bem"] + 0.15, T["bem"] + 0.45) * sai)


# ------------------------------------------------------------------ ato 2: o teste do pezinho
def _sola():
    p = skia.Path()
    p.moveTo(2, 58)
    p.cubicTo(-16, 58, -24, 44, -24, 26)
    p.cubicTo(-24, 8, -28, -10, -27, -26)
    p.cubicTo(-26, -44, -12, -52, 3, -52)
    p.cubicTo(19, -52, 28, -42, 26, -26)
    p.cubicTo(24, -12, 11, -3, 12, 14)
    p.cubicTo(13, 30, 21, 40, 18, 50)
    p.cubicTo(15, 56, 8, 58, 2, 58)
    p.close()
    return p


SOLA = _sola()
DEDOS = ((15, -67, 10.5), (0, -71, 7.6), (-11, -67, 6.8), (-20, -60, 6.2), (-27, -50, 5.4))


def pegadinha_contorno(cv, x, y, esc, cor, a):
    """Pegadinha de bebê só no contorno (sem gota, sem agulha, sem sangue)."""
    cv.save(); cv.translate(x, y); cv.scale(esc, esc)
    cv.drawPath(SOLA, paint(cor, int(255 * a), "stroke", 4.5))
    for dx, dy, r in DEDOS:
        cv.drawCircle(dx, dy, r, paint(cor, int(255 * a), "stroke", 3.5))
    cv.restore()


def cartao_pezinho(cv, t, T):
    t_in, t_out = T["pezinho"] - 0.08, T["exame"] - 0.22
    if t < t_in or t > t_out + 0.45:
        return
    k_in = e_out(prog(t, t_in, t_in + 0.45)); k_out = e_inout(prog(t, t_out, t_out + 0.3))
    k = t - T["detecta"]
    trem = 11 * math.sin(k * 70) * (1 - k / 0.35) if 0 <= k < 0.35 else 0.0
    dx = 780 * (1 - k_in) + 320 * k_out + trem
    a = clamp(k_in * 2) * (1 - k_out)
    cv.save(); cv.translate(dx, 0)
    cv.saveLayer(None, _alfa(a)) if a < 1 else cv.save()
    # cartão largo: a pegadinha à esquerda fica LIVRE; o carimbo cai na metade direita, acima do título
    rr = skia.RRect.MakeRectXY(skia.Rect(170, 600, 1010, 930), 30, 30)
    cv.drawRRect(rr, paint("#000000", 90, blur=18))
    cv.drawRRect(rr, paint("#F3F7FB"))
    cv.drawRRect(rr, paint("#C9D6E2", 255, "stroke", 3))
    pegadinha_contorno(cv, 292, 752, 1.35, "#2B4A66", 1.0)
    texto(cv, "TESTE DO PEZINHO", 590, 884, F_BLACK, 50, "#16324A")
    cv.restore(); cv.restore()
    carimbo_vermelho(cv, "NÃO DETECTA", 652 + dx - trem * 0.3, 762, -7, T["detecta"], t,
                     dur=T["exame"] - T["detecta"] - 0.1)


# ------------------------------------------------------------------ ato 3: exame do bebê, às vezes ultrassom
def sonda(cv, x, y, a):
    """Transdutor de ultrassom: ponteira arredondada com cabo, contorno de aço. Sem tela, sem imagem."""
    if a <= 0:
        return
    cv.save(); cv.translate(x, y); cv.rotate(-16)
    cabo = skia.Path(); cabo.moveTo(0, -112)
    cabo.cubicTo(6, -170, 70, -170, 64, -230); cabo.cubicTo(58, -280, 10, -280, 18, -330)
    cv.drawPath(cabo, paint("#000000", int(70 * a), "stroke", 14, blur=5))
    cv.drawPath(cabo, paint(ACO_ESC, int(255 * a), "stroke", 10))
    cv.drawPath(cabo, paint(ACO, int(200 * a), "stroke", 3))
    corpo = skia.Path()
    corpo.moveTo(-24, -118); corpo.lineTo(24, -118)
    corpo.cubicTo(30, -60, 30, 0, 34, 30)
    corpo.cubicTo(52, 46, 58, 62, 56, 76)
    corpo.cubicTo(30, 100, -30, 100, -56, 76)
    corpo.cubicTo(-58, 62, -52, 46, -34, 30)
    corpo.cubicTo(-30, 0, -30, -60, -24, -118)
    corpo.close()
    cv.drawPath(corpo, paint("#000000", int(80 * a), blur=10))
    sh = skia.GradientShader.MakeLinear([skia.Point(-50, 0), skia.Point(50, 0)],     # corpo CLARO sobre o cartão
                                        [C("#8FA6B8"), C("#C9D6E2"), C("#8FA6B8")])
    cv.drawPath(corpo, paint("#C9D6E2", int(255 * a), shader=sh))
    cv.drawPath(corpo, paint(ACO_ESC, int(255 * a), "stroke", 4))
    ponteira = skia.Path(); ponteira.moveTo(-50, 80); ponteira.cubicTo(-26, 98, 26, 98, 50, 80)
    cv.drawPath(ponteira, paint(ACO_ESC, int(255 * a), "stroke", 9))
    cv.drawPath(ponteira, paint(ACO_HL, int(255 * a), "stroke", 4))
    cv.drawLine(-14, -96, -16, 20, paint("#FFFFFF", int(170 * a), "stroke", 4))
    cv.restore()


def avaliacao(cv, t, T):
    a = prog(t, T["exame"] + 0.02, T["exame"] + 0.3) * (1 - prog(t, T["fralda"] - 0.3, T["fralda"]))
    if a <= 0:
        return
    rr = skia.RRect.MakeRectXY(skia.Rect(110, 640, 970, 965), 26, 26)
    cv.drawRRect(rr, paint(FUNDO_CARTAO, int(200 * a)))
    cv.drawRRect(rr, paint("#2C4E66", int(255 * a), "stroke", 2.5))
    caixa_check(cv, 150, 735, T["exame"] + 0.25, t, a)
    texto(cv, "EXAME DO BEBÊ", 226, 735, F_BLACK, 46, "#FFFFFF", int(255 * a * prog(t, T["exame"] + 0.15, T["exame"] + 0.4)),
          centro=False)
    k2 = e_out(prog(t, T["as"], T["as"] + 0.35))
    if k2 > 0:
        cv.drawCircle(175, 873, 11, paint(ACO, int(255 * a * k2)))
        texto(cv, "ÀS VEZES, COM ULTRASSOM", 226 - 40 * (1 - k2), 887, F_BLACK, 40, "#D6E4F0", int(255 * a * k2),
              centro=False)
    kp = e_out(prog(t, T["ultrassom"] - 0.05, T["ultrassom"] + 0.5))
    if kp > 0:
        sonda(cv, lerp(1300, 880, kp), 790, a)


# ------------------------------------------------------------------ ato 4: na troca de fralda
HQ, HY = (455, 625), 480          # quadris (x da perna da esquerda e da direita da tela) e altura
K_CURTA = 0.88                    # a perna da direita da tela parece mais curta
PE_Y0 = 322                       # início do pé (unidades da perna, antes do fator de comprimento)


def _perna_path(k):
    def Y(v):
        return v * k
    p = skia.Path()
    p.moveTo(-66, -30)
    p.cubicTo(-76, Y(40), -78, Y(120), -62, Y(178))
    p.cubicTo(-54, Y(206), -52, Y(226), -55, Y(254))
    p.cubicTo(-57, Y(292), -44, Y(318), -36, Y(336))
    p.lineTo(36, Y(336))
    p.cubicTo(44, Y(318), 57, Y(292), 55, Y(254))
    p.cubicTo(52, Y(226), 54, Y(206), 62, Y(178))
    p.cubicTo(78, Y(120), 76, Y(40), 66, -30)
    p.close()
    return p


def pe_fundo(k):
    """Ponta dos dedos (unidades locais, a partir do quadril)."""
    return PE_Y0 * k + 84


def perna_bebe(cv, hx, ang, k, dentro, dobras, glow):
    """Perna de desenho (pele lisa, sem osso), presa no quadril (hx, HY), girada `ang` graus.
    `dentro` = +1 se o lado de dentro (dedão, dobrinhas) fica à direita na perna sem giro."""
    cv.save(); cv.translate(hx, HY); cv.rotate(ang)
    sh = skia.GradientShader.MakeLinear([skia.Point(-80, 0), skia.Point(80, 0)],
                                        [C(PELE_ESC), C(PELE), C(PELE_CL), C(PELE), C(PELE_ESC)],
                                        [0.0, 0.22, 0.5, 0.78, 1.0])
    pe_top = PE_Y0 * k
    pe = skia.RRect.MakeRectXY(skia.Rect(-44, pe_top, 44, pe_top + 80), 40, 40)
    perna = _perna_path(k)
    cv.drawPath(perna, paint("#000000", 60, blur=12))
    cv.drawRRect(pe, paint(PELE, shader=sh))
    cv.drawRRect(pe, paint(PELE_LINHA, 230, "stroke", 3.2))
    for i, (fx, r) in enumerate(((-29, 9), (-15, 9.5), (-1, 10), (14, 11), (30, 13))):
        xx = fx * dentro
        cv.drawCircle(xx, pe_top + 74 - (2 if i == 4 else 0), r, paint(PELE_CL))
        cv.drawCircle(xx, pe_top + 74 - (2 if i == 4 else 0), r, paint(PELE_LINHA, 230, "stroke", 2.6))
    cv.drawPath(perna, paint(PELE, shader=sh))
    cv.drawPath(perna, paint(PELE_LINHA, 230, "stroke", 3.2))
    cv.drawArc(skia.Rect(-22, 200 * k - 12, 22, 200 * k + 12), 25, 130, False, paint(PELE_LINHA, 140, "stroke", 3))
    for y in dobras:                                                  # dobrinhas da coxa (do lado de dentro)
        p = skia.Path(); p.moveTo(72 * dentro, y - 6)
        p.quadTo(36 * dentro, y + 14, -14 * dentro, y + 4)
        if glow > 0:
            cv.drawPath(p, paint(OURO, int(150 * glow), "stroke", 18, blur=8))
            cv.drawPath(p, paint(lerpc(PELE_LINHA, OURO, glow), 255, "stroke", 4 + 2 * glow))
        else:
            cv.drawPath(p, paint(PELE_LINHA, 200, "stroke", 4))
    cv.restore()


def _fralda():
    p = skia.Path()
    p.moveTo(342, 400); p.lineTo(738, 400)
    p.cubicTo(748, 450, 742, 500, 716, 528)
    p.cubicTo(680, 540, 640, 555, 600, 592)
    p.cubicTo(575, 612, 505, 612, 480, 592)
    p.cubicTo(440, 555, 400, 540, 364, 528)
    p.cubicTo(338, 500, 332, 450, 342, 400)
    p.close()
    return p


FRALDA_P = _fralda()


def fralda(cv):
    cv.save(); cv.translate(0, -28)
    sh = skia.GradientShader.MakeLinear([skia.Point(0, 400), skia.Point(0, 610)], [C(FRALDA), C(FRALDA_SOMBRA)])
    pf = paint(FRALDA, shader=sh); pf.setPathEffect(skia.CornerPathEffect.Make(18))
    sombra = paint("#000000", 80, blur=12); sombra.setPathEffect(skia.CornerPathEffect.Make(18))
    cv.drawPath(FRALDA_P, sombra)
    cv.drawPath(FRALDA_P, pf)
    po = paint(FRALDA_LINHA, 255, "stroke", 3); po.setPathEffect(skia.CornerPathEffect.Make(18))
    cv.drawPath(FRALDA_P, po)
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(346, 404, 734, 432), 10, 10), paint("#DDE7F1"))
    for x0 in (330, 708):                                             # abas
        cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(x0, 444, x0 + 42, 490), 10, 10), paint(AZUL_CLARO))
        cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(x0, 444, x0 + 42, 490), 10, 10), paint("#6E9CC9", 255, "stroke", 2.5))
    for x, y in ((470, 470), (540, 505), (610, 470), (505, 545), (575, 545)):   # estampa de bolinhas
        cv.drawCircle(x, y, 7, paint(AZUL_CLARO, 170))
    cv.restore()


def troca_fralda(cv, t, T):
    t_in = T["fralda"] - 0.1
    if t < t_in or t > T["duvida"] + 0.6:
        return
    ent = e_out(prog(t, t_in, t_in + 0.5)); sai = e_inout(prog(t, T["duvida"] - 0.3, T["duvida"] + 0.1))
    a = clamp(ent * 1.5) * (1 - sai)
    if a <= 0:
        return
    cv.saveLayer(None, _alfa(a)) if a < 1 else cv.save()
    cv.translate(0, 140 * (1 - ent) - 60 * sai)
    # trocador
    mat = skia.RRect.MakeRectXY(skia.Rect(150, 342, 930, 950), 46, 46)
    cv.drawRRect(mat, paint(TAPETE, 235))
    cv.drawRRect(mat, paint(TAPETE_BORDA, 200, "stroke", 3))
    ps = paint(TAPETE_BORDA, 150, "stroke", 2.5); ps.setPathEffect(skia.DashPathEffect.Make([14, 10], 0))
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(172, 364, 908, 928), 32, 32), ps)
    # abrir: um lado para antes (arco menor, tracejado em vermelho suave)
    th_n = 40 * e_inout(prog(t, T["lado"], T["lado"] + 0.9))
    th_c = 20 * e_inout(prog(t, T["lado"], T["lado"] + 0.55))
    glow = prog(t, T["dobrinhas"], T["dobrinhas"] + 0.3) * (1 - 0.4 * prog(t, T["perna"], T["perna"] + 0.4))
    perna_bebe(cv, HQ[0], th_n, 1.0, 1, (116, 166), glow)
    perna_bebe(cv, HQ[1], -th_c, K_CURTA, -1, (96, 124, 152), glow)
    fralda(cv)
    # régua tracejada nos pés
    a_r = prog(t, T["perna"], T["perna"] + 0.2) * (1 - prog(t, T["lado"] - 0.1, T["lado"] + 0.2))
    if a_r > 0:
        y_l = HY + pe_fundo(1.0); y_c = HY + pe_fundo(K_CURTA)
        x1 = lerp(330, 760, e_out(prog(t, T["perna"], T["perna"] + 0.45)))
        pr = paint(OURO, int(255 * a_r), "stroke", 5); pr.setPathEffect(skia.DashPathEffect.Make([22, 14], 0))
        cv.drawLine(330, y_l + 6, x1, y_l + 6, pr)
        k = prog(t, T["perna"] + 0.35, T["perna"] + 0.6)
        if k > 0:
            pc = paint(VERM_SUAVE, int(230 * a_r * k), "stroke", 3.5); pc.setPathEffect(skia.DashPathEffect.Make([10, 8], 0))
            cv.drawLine(575, y_c + 6, 715, y_c + 6, pc)
            xm = 728
            cv.drawLine(xm, y_c + 10, xm, y_l + 2, paint(VERM_SUAVE, int(255 * a_r * k), "stroke", 4))
            ponta(cv, xm, y_c + 6, -math.pi / 2, 12, VERM_SUAVE, a_r * k)
            ponta(cv, xm, y_l + 6, math.pi / 2, 12, VERM_SUAVE, a_r * k)
    # arcos de abertura
    a_arc = prog(t, T["lado"], T["lado"] + 0.15)
    if a_arc > 0 and th_n > 2:
        seta_pts(cv, arco_pts(HQ[0], HY, 450, 90, 90 + th_n), OURO, a_arc, larg=6, tam=22)
    if a_arc > 0 and th_c > 1:
        pts = arco_pts(HQ[1], HY, 450, 90, 90 - th_c)
        p = skia.Path(); p.moveTo(*pts[0])
        for q in pts[1:]:
            p.lineTo(*q)
        pd = paint(VERM_SUAVE, int(255 * a_arc), "stroke", 6); pd.setPathEffect(skia.DashPathEffect.Make([18, 12], 0))
        cv.drawPath(p, pd)
        if th_c > 19.5:                                               # o ponto onde para
            ang = math.radians(90 - th_c)
            c, s = math.cos(ang), math.sin(ang)
            cv.drawLine(HQ[1] + 428 * c, HY + 428 * s, HQ[1] + 472 * c, HY + 472 * s,
                        paint(VERM_SUAVE, int(255 * a_arc), "stroke", 7))
    cv.restore()


SINAIS = (("dobrinhas", "DOBRINHAS DA COXA DIFERENTES"), ("perna", "PERNA PARECENDO MAIS CURTA"),
          ("lado", "UM LADO QUE ABRE MENOS"))
CHECK_ATRASO = {"lado": 0.6}      # o 3º check só depois que a perna afetada PARA (som suave, sem estalo)


def checklist_sinais(cv, t, T):
    a0 = prog(t, T["repare"] - 0.1, T["repare"] + 0.25) * (1 - prog(t, T["duvida"] - 0.3, T["duvida"] + 0.05))
    if a0 <= 0:
        return
    dy = -50 * e_inout(prog(t, T["duvida"] - 0.3, T["duvida"] + 0.1))
    rr = skia.RRect.MakeRectXY(skia.Rect(140, 968 + dy, 940, 1206 + dy), 24, 24)
    cv.drawRRect(rr, paint(FUNDO_CARTAO, int(205 * a0)))
    cv.drawRRect(rr, paint("#2C4E66", int(255 * a0), "stroke", 2.5))
    for i, (chave, s) in enumerate(SINAIS):
        y = 1030 + i * 78 + dy
        a = a0 * prog(t, T["repare"] + 0.08 * i, T["repare"] + 0.08 * i + 0.25)
        caixa_check(cv, 172, y, T[chave] + CHECK_ATRASO.get(chave, 0.1), t, a, tam=46)
        k = e_out(prog(t, T[chave] + 0.05, T[chave] + 0.35))
        if k > 0:
            texto(cv, s, 238 + 30 * (1 - k), y, F_BLACK, 38, "#FFFFFF", int(255 * a0 * k), centro=False)


# ------------------------------------------------------------------ ato 5: na dúvida
def na_duvida(cv, t, T):
    sai = 1 - prog(t, T["achado"] - 0.4, T["achado"] - 0.15)          # some ANTES de o encaixe voltar
    k = e_back(prog(t, T["duvida"] + 0.05, T["duvida"] + 0.45))
    a = clamp(k * 1.5) * sai
    if a <= 0:
        return
    cv.save(); cv.translate(540, 650); cv.scale(lerp(0.7, 1.0, k), lerp(0.7, 1.0, k))
    chip(cv, "NA DÚVIDA", 0, 0, "#FFFFFF", a, tam=52, borda=OURO)
    cv.restore()
    ka = prog(t, T["ortopedista"] - 0.15, T["ortopedista"] + 0.25)
    if ka > 0:
        seta_pts(cv, [(540, 690), (540, lerp(690, 768, e_out(ka)))], OURO, ka * sai, larg=6, tam=20)
    kc = e_out(prog(t, T["ortopedista"], T["ortopedista"] + 0.45))
    if kc > 0:
        ac = clamp(kc * 1.6) * sai
        cv.save(); cv.translate(700 * (1 - kc), 0)
        rr = skia.RRect.MakeRectXY(skia.Rect(140, 792, 940, 928), 28, 28)
        cv.drawRRect(rr, paint("#000000", int(80 * ac), blur=14))
        cv.drawRRect(rr, paint(FUNDO_CARTAO, int(235 * ac)))
        cv.drawRRect(rr, paint(OURO, int(255 * ac), "stroke", 3))
        cx, cy = 210, 860
        cv.drawCircle(cx, cy, 38, paint(OURO, int(255 * ac), "stroke", 4.5))
        pr = e_out(prog(t, T["ortopedista"] + 0.45, T["ortopedista"] + 0.8))
        if pr > 0:
            cv.drawCircle(cx, cy, 38, paint(OURO, int(60 * ac * pr)))
            p = skia.Path(); p.moveTo(cx - 17, cy + 1)
            p.lineTo(cx - 17 + 12 * min(1, pr * 2), cy + 1 + 13 * min(1, pr * 2))
            if pr > 0.5:
                q = (pr - 0.5) * 2
                p.lineTo(cx - 5 + 25 * q, cy + 14 - 30 * q)
            cv.drawPath(p, paint(OURO, int(255 * ac), "stroke", 7))
        texto(cv, "ORTOPEDISTA PEDIÁTRICO", 272, 878, F_BLACK, 46, "#FFFFFF", int(255 * ac), centro=False)
        cv.restore()


# ------------------------------------------------------------------ ato 6: achado cedo, suspensório, semanas
def suspensorio(cv, x, y, a):
    """Ícone de suspensório de roupa: duas alças azul-claras e uma fivela simples (sem bebê)."""
    if a <= 0:
        return
    cv.save(); cv.translate(x, y)
    for sx in (-1, 1):
        p = skia.Path()
        p.moveTo(sx * 44, -176); p.cubicTo(sx * 56, -80, sx * 62, 60, sx * 72, 170)
        cv.drawPath(p, paint("#000000", int(70 * a), "stroke", 40, blur=8))
        cv.drawPath(p, paint(SUSP_ESC, int(255 * a), "stroke", 38))
        cv.drawPath(p, paint(SUSP, int(255 * a), "stroke", 30))
        pc = paint("#FFFFFF", int(150 * a), "stroke", 2.5); pc.setPathEffect(skia.DashPathEffect.Make([10, 8], 0))
        cv.drawPath(p, pc)
        cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(sx * 72 - 22, 164, sx * 72 + 22, 196), 6, 6), paint(ACO, int(255 * a)))
        cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(sx * 72 - 22, 164, sx * 72 + 22, 196), 6, 6),
                     paint(ACO_ESC, int(255 * a), "stroke", 2.5))
    faixa = skia.Path(); faixa.moveTo(-62, -30); faixa.lineTo(62, -30)
    cv.drawPath(faixa, paint(SUSP_ESC, int(255 * a), "stroke", 34))
    cv.drawPath(faixa, paint(SUSP, int(255 * a), "stroke", 26))
    fiv = skia.RRect.MakeRectXY(skia.Rect(-30, -56, 30, -4), 9, 9)
    cv.drawRRect(fiv, paint(FUNDO_CARTAO, int(120 * a)))
    cv.drawRRect(fiv, paint(ACO_HL, int(255 * a), "stroke", 6))
    cv.drawLine(0, -52, 0, -8, paint(ACO_HL, int(255 * a), "stroke", 5))
    cv.restore()


def tratamento(cv, t, T):
    fim = 1 - prog(t, T["manda"] - 0.45, T["manda"] - 0.1)
    if t < T["achado"] - 0.1 or fim <= 0:
        return
    k = e_back(prog(t, T["achado"], T["achado"] + 0.4))
    chip(cv, "ACHADO CEDO", 540, 330, OURO, clamp(k * 1.5) * (1 - prog(t, T["semanas"] - 0.6, T["semanas"] - 0.3)) * fim,
         tam=44)                                                     # sai antes de o calendário entrar
    ks = e_out(prog(t, T["suspensorio"] - 0.05, T["suspensorio"] + 0.5))
    if ks > 0:
        suspensorio(cv, lerp(1260, 800, ks), 660, clamp(ks * 1.5) * fim)
        chip(cv, "SUSPENSÓRIO DE PAVLIK", 540, 1040, "#D7ECFF", clamp(ks * 1.5) * fim, tam=40, borda=SUSP)
    kr = e_out(prog(t, T["reposiciona"], T["reposiciona"] + 0.35))
    if kr > 0:
        chip(cv, "REPOSICIONA O QUADRIL", 540 + 40 * (1 - kr), 1130, "#FFFFFF", kr * fim, tam=40, borda=AZUL_CLARO)
    a_cal = prog(t, T["semanas"] - 0.25, T["semanas"] + 0.15) * fim
    if a_cal > 0:
        devagar = T["semanas"] + (t - T["semanas"]) * 0.42                 # folhas virando devagar
        calendario(cv, 70, 236, devagar, T["semanas"], a_cal)
        texto(cv, "AO LONGO DE SEMANAS", 186, 288, F_BLACK, 40, "#FFFFFF", int(255 * a_cal), centro=False, contorno=6)
        texto(cv, "com acompanhamento de perto", 188, 332, F_SEMI, 32, AZUL_CLARO, int(255 * a_cal), centro=False)


# ------------------------------------------------------------------ quadro
def quadro(cv, t, T, blocos, ep):
    fundo(cv, t)
    pose = pose_junta(t, T)
    junta(cv, t, T, pose)
    rotulos_abertura(cv, t, T, pose)
    cartao_pezinho(cv, t, T)
    avaliacao(cv, t, T)
    troca_fralda(cv, t, T)
    chip(cv, "NA TROCA DE FRALDA", 540, 312, "#FFFFFF",
         janela(t, T["fralda"], T["duvida"] - 0.35, 0.3, 0.3), tam=44, borda=OURO)
    checklist_sinais(cv, t, T)
    na_duvida(cv, t, T)
    tratamento(cv, t, T)

    capa(cv, t, T["teste"] - 0.1, ep["gancho"][0], ep["gancho"][1])
    selo_como_funciona(cv, prog(t, T["teste"] + 0.3, T["teste"] + 0.7) * (1 - prog(t, T["manda"] - 0.3, T["manda"])))
    interface(cv, t, T, blocos, DESTAQUE)


def sons(T):
    ev = [(0.05, "whoosh", 0.35), (T["encaixe"] + 0.1, "shimmer", 0.6),       # assenta SEM clique
          (T["displasia"], "whoosh", 0.3), (T["cabeca"], "pop", 0.45), (T["bem"] + 0.05, "whoosh", 0.3),
          (T["teste"], "whoosh", 0.45), (T["pezinho"], "whoosh", 0.5), (T["detecta"] - 0.02, "thump", 0.85),
          (T["exame"] - 0.05, "whoosh", 0.35), (T["exame"] + 0.25, "ping", 0.55), (T["as"], "pop", 0.35),
          (T["ultrassom"], "whoosh", 0.4), (T["fralda"] - 0.1, "whoosh", 0.5), (T["repare"], "pop", 0.35),
          (T["dobrinhas"] + 0.1, "ping", 0.5),                                # sinal de alerta: sem shimmer
          (T["perna"] + 0.1, "ping", 0.5), (T["perna"], "whoosh", 0.25),
          (T["lado"], "whoosh", 0.4), (T["lado"] + 0.6, "pop", 0.35),        # nada metálico ao abrir as pernas
          (T["duvida"] + 0.08, "pop", 0.55), (T["ortopedista"], "whoosh", 0.4), (T["ortopedista"] + 0.5, "ding", 0.55),
          (T["achado"] - 0.1, "whoosh", 0.45), (T["achado"] + 0.1, "pop", 0.4),
          (T["suspensorio"], "whoosh", 0.45), (T["suspensorio"] + 0.35, "pop", 0.4),
          (T["reposiciona"], "whoosh", 0.25), (T["semanas"], "whoosh", 0.25), (T["manda"] + 0.05, "whoosh", 0.5)]
    # Nenhum tick/click/pop/ping enquanto a bola volta e assenta (clique no quadril é sinal de alerta).
    assert not [e for e in ev if T["semanas"] + 0.8 <= e[0] < T["manda"] and e[1] in ("tick", "click", "pop", "ping")]
    return ev


def tempos_previa(T):
    return (0.0, T["encaixe"] + 0.5, T["cabeca"] + 0.7, T["bem"] + 0.9, T["detecta"] + 0.45,
            T["ultrassom"] + 0.7, T["perna"] + 0.9, T["lado"] + 1.2, T["ortopedista"] + 0.9,
            T["reposiciona"] + 0.5, T["semanas"] + 1.9, T["manda"] + 1.6)


# respiro maior antes da CTA: a bola termina de voltar ao centro enquanto o calendário vira devagar.
render = fazer_render(quadro, ANCORAS, sons, tempos_previa, respiro_cta=2.4)
