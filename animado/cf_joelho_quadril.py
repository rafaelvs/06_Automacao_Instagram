# -*- coding: utf-8 -*-
"""COMO FUNCIONA — dor no joelho que vem do quadril ("DÓI O JOELHO. / E É O QUADRIL?").

Mesmo estilo das cenas aprovadas (fundo azul-petróleo com partículas, dourado, rótulos com fio e
ponto, carimbo, checklist, legenda karaokê, CTA com aviãozinho). O mecanismo é o AVISO: uma perna de
desenho, de frente, com o joelho brilhando em vermelho-suave e um "?" em cima; uma seta pontilhada
dourada sobe do joelho por FORA do contorno da coxa até o quadril (o gesto de rastrear), que ganha um
halo dourado. Quando o quadril acende, a seta VIRA: a cabeça passa para a ponta do joelho, o tracejado
corre do quadril para o joelho e, a cada pulso (o MESMO ritmo do halo e do brilho do joelho), uma luz
dourada sai do quadril e chega ao joelho no pico do vermelho — quem avisa é o quadril. A câmera começa
perto do joelho (o espanto) e recua enquanto a seta sobe, revelando o quadril na palavra "quadril".
No pré-adolescente a perna AFINA e ALONGA (a mesma criança, mais velha); no "mancando" ela manca de
verdade (o quadril afunda no passo curto, o pé fica no chão das pegadas); no "exame" a lupa desce ao
joelho e volta ao quadril (o exame olha os dois).

O que o verificador exigiu (lote5_cf/cf_joelho_quadril_storyboard.json) está aqui:
  * Perna de DESENHO, pele lisa e OPACA, shorts: nenhum osso, nada translúcido, nenhuma estrutura
    interna, nenhum fundo preto. O quadril é só um halo sobre o contorno do shorts; a lupa amplia o
    MESMO desenho (barra do shorts, contorno e pele da coxa), com o fundo azul da cena; o halo
    do quadril brilha DENTRO da lente como luz (Screen), sem acinzentar.
  * A seta passa por FORA do contorno (nada de trajeto interno).
  * "Dói no joelho OU na coxa": os brilhos se alternam, nunca os dois fortes juntos.
  * Os lugares da dor do pré-adolescente (virilha, coxa, joelho) são PONTINHOS na perna, acesos um
    de cada vez (o que já passou fica fraco: são alternativas) e todos saem no "mancando"; o
    checklist tem só os DOIS itens que a fonte pede juntos (MANCANDO, SEM TRAUMA CLARO), com tique
    branco. Pegadas do mesmo tamanho, espaçamento desigual, sem rosto.
  * Carimbo VERMELHO só no alarme (AVALIAÇÃO SEM DEMORA); nenhum dourado comemora o alarme.
  * RADIOGRAFIA é só texto num cartão azul-escuro: nenhuma imagem de exame. Nenhum nome de doença,
    nenhum check verde no "esclarecer" (o "?" só encolhe e some devagar).
Desvios do storyboard, por legibilidade no celular (rótulos com folga de ~10% para a Roboto):
  * O cartão do "motivo" e o carimbo saem em DUAS linhas ("DOR NO JOELHO" / "SEM MOTIVO?",
    "AVALIAÇÃO" / "SEM DEMORA"): numa linha só não cabiam ao lado da perna.
  * "TAMBÉM SE OLHA O QUADRIL" fica colado à DIREITA da lupa (não embaixo): sob a lupa ficam a
    coxa, a seta e o rótulo AVISA. Acompanha a lupa na troca de câmera e fica ~1,7 s legível.
  * No pré-adolescente a prancheta entra na metade de BAIXO da coluna direita (o rótulo dos
    pontinhos precisa da faixa ao lado da coxa); no "exame" ela sobe por baixo do carimbo e vira o
    cartão EXAME CLÍNICO no alto, e o carimbo fica onde bateu (recua a 45% no "exame": já cumpriu
    o papel), com AVALIAR CEDO logo abaixo dele. Sob o carimbo, o TEXTO do checklist some.
A cena é PRESA ao roteiro pelas palavras-âncora (ANCORAS): mudar o roteiro sem elas quebra o render
de propósito (KeyError), em vez de sair vídeo dessincronizado. Todo texto desenhado está em
ep["tela"] (o render recusa o vídeo se não estiver).
"""
import math

import skia

from .cf_alongamento import (BG_IN, BG_OUT, F_BLACK, OSSO_B, OSSO_C, OURO, PELE, VERMELHO, H, W, C, clamp,
                             e_back, e_in_back, e_inout, e_out, fundo, lerp, paint, prog, texto)
from .cf_comum import capa, fazer_render, interface, selo_como_funciona

# ------------------------------------------------------------------ sincronia com a fala
ANCORAS = {
    "joelho1": ("joelho", 1, False), "avisando": ("avisando", 1, False), "quadril1": ("quadril", 1, False),
    "crianca": ("criança", 1, False), "doi": ("dói", 1, False), "joelho2": ("joelho", 2, False),
    "coxa1": ("coxa", 1, False), "vir": ("vir", 1, False), "quadril2": ("quadril", 2, False),
    "joelho3": ("joelho", 3, False), "motivo": ("motivo", 1, False), "olha": ("olha", 1, False),
    "quadril3": ("quadril", 3, False), "pre": ("pré-adolescente", 1, False), "virilha": ("virilha", 1, False),
    "coxa2": ("coxa", 2, False), "joelho4": ("joelho", 4, False), "mancando": ("mancando", 1, False),
    "trauma": ("trauma", 1, False), "demora": ("demora", 1, False), "exame": ("exame", 1, False),
    "quando": ("quando", 1, False), "indicado": ("indicado", 1, False), "radiografia": ("radiografia", 1, False),
    "esclarecer": ("esclarecer", 1, False), "cedo": ("cedo", 1, False), "manda": ("manda", 1, False),
}
DESTAQUE = {"joelho", "avisando", "quadril", "criança", "coxa", "motivo", "olha", "pré-adolescente", "virilha",
            "mancando", "trauma", "demora", "exame", "clínico", "radiografia", "esclarecer", "cedo", "diferença"}

# ------------------------------------------------------------------ textos da tela (TODOS estão em ep["tela"])
T_JOELHO, T_INTERROG, T_AVISA, T_QUADRIL = "JOELHO", "?", "AVISA", "QUADRIL"
T_CRIANCA, T_PRE = "NA CRIANÇA", "PRÉ-ADOLESCENTE"
T_COXA, T_VIRILHA = "COXA", "VIRILHA"
T_MOTIVO = ("DOR NO JOELHO", "SEM MOTIVO?")
T_OLHA = "TAMBÉM SE OLHA O QUADRIL"
T_ITENS = ("MANCANDO", "SEM TRAUMA CLARO")
T_CARIMBO = ("AVALIAÇÃO", "SEM DEMORA")
T_EXAME, T_QUANDO, T_RADIO, T_CEDO = "EXAME CLÍNICO", "QUANDO INDICADO", "RADIOGRAFIA", "AVALIAR CEDO"

# ------------------------------------------------------------------ paleta própria (a das pernas do lote 4)
PELE_CL, PELE_ESC, PELE_LINHA = "#F7CDB8", "#DA987E", "#B9765E"
SHORT, SHORT_CL, SHORT_ESC, SHORT_LINHA = "#4C86C6", "#6FA3DA", "#3A6FA8", "#2C5A8E"
FUNDO_CARTAO = "#0B1824"
AZUL = "#9CC9FF"
DOR, DOR_TXT = "#FF5A5F", "#FFA3A6"
MARFIM = OSSO_C
TAM_ROT = 38                                   # rótulos da perna


# ------------------------------------------------------------------ utilidades
def _alfa(a):
    p = skia.Paint()
    p.setAlphaf(clamp(a))
    return p


def _c(h, a=255):
    h = h.lstrip("#")
    return skia.ColorSetARGB(int(a), int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))


def _p(cor, a=255, estilo="fill", w=0, blur=0, junta=False, traco=None, fase=0.0):
    p = paint(cor, a, estilo, w, blur)
    if junta:
        p.setStrokeJoin(skia.Paint.kRound_Join)
    if traco:
        p.setPathEffect(skia.DashPathEffect.Make(list(traco), fase))
    return p


def suave(pts):
    """Contorno fechado e liso passando por todos os pontos (Catmull-Rom -> Bézier)."""
    n = len(pts)
    p = skia.Path(); p.moveTo(*pts[0])
    for i in range(n):
        p0, p1, p2, p3 = pts[(i - 1) % n], pts[i], pts[(i + 1) % n], pts[(i + 2) % n]
        p.cubicTo(p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6,
                  p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6, p2[0], p2[1])
    p.close()
    return p


def ponta(cv, x, y, ang, tam, cor, a):
    """Cabeça de seta em (x, y) apontando para `ang` (radianos). (cópia do cf_pe_virado)"""
    p = skia.Path()
    p.moveTo(x + tam * math.cos(ang), y + tam * math.sin(ang))
    p.lineTo(x + tam * 0.75 * math.cos(ang + 2.45), y + tam * 0.75 * math.sin(ang + 2.45))
    p.lineTo(x + tam * 0.75 * math.cos(ang - 2.45), y + tam * 0.75 * math.sin(ang - 2.45))
    p.close()
    cv.drawPath(p, paint(cor, int(255 * a)))


def etiqueta(cv, s, x, y, cor, a, tam=TAM_ROT, alinh="esq", ancora=None, borda=None, dx=0.0):
    """Rótulo em caixa OPACA. alinh='esq': x = borda esquerda; 'dir': x = borda direita; y = linha de
    base. `ancora` (xa, ya): fio do ponto até a borda da caixa mais perto dele (nunca risca o texto)."""
    if a <= 0:
        return
    f = skia.Font(F_BLACK, tam); lw = f.measureText(s)
    bw = lw + 32
    bx = (x if alinh == "esq" else x - bw) + dx
    y0, y1 = y - tam * 1.06, y + tam * 0.34
    if ancora is not None:
        xa, ya = ancora
        ex = bx if xa < bx else (bx + bw if xa > bx + bw else xa)
        ey = clamp(ya, y0 + 10, y1 - 10) if (xa < bx or xa > bx + bw) else (y0 if ya < y0 else y1)
        cv.drawLine(xa, ya, ex, ey, paint(cor, int(215 * a), "stroke", 2.6))
        cv.drawCircle(xa, ya, 7.5, paint(FUNDO_CARTAO, int(220 * a)))
        cv.drawCircle(xa, ya, 5.5, paint(cor, int(255 * a)))
    rr = skia.RRect.MakeRectXY(skia.Rect(bx, y0, bx + bw, y1), 15, 15)
    cv.drawRRect(rr, paint(FUNDO_CARTAO, int(232 * a)))
    cv.drawRRect(rr, paint(borda or cor, int(255 * a), "stroke", 2.6))
    cv.drawString(s, bx + 16, y, f, paint(cor, int(255 * a)))


# ------------------------------------------------------------------ a perna (de frente; coordenadas locais)
# Perna DIREITA da criança vista de frente: o lado de FORA (onde fica o quadril) é o da esquerda da
# tela; o de DENTRO (virilha) é o da direita. Local: y = 0 no alto do shorts, joelho em y ≈ 445.
# Proporção de criança: coxa roliça e curta, joelho largo, panturrilha redonda, pé curto e gordinho.
_LAT = [(-162, -100), (-162, 30), (-156, 140), (-142, 240), (-122, 330), (-106, 392), (-101, 440), (-108, 492),
        (-113, 560), (-101, 640), (-78, 708), (-64, 748)]
_PE = [(-76, 778), (-84, 808), (-72, 832), (-34, 842), (14, 845), (58, 841), (88, 828), (98, 802), (86, 772)]
_MED = [(54, 748), (60, 708), (78, 640), (88, 560), (88, 500), (81, 450), (85, 398), (104, 328), (122, 240),
        (136, 140), (142, 30), (144, -100)]
PERNA = suave(_LAT + _PE + _MED + [(-8, -106)])
DEDOS = ((74, 826, 19), (46, 836, 15), (19, 840, 14), (-7, 839, 13), (-32, 833, 12))


def _brilho_eixo():
    p = skia.Path(); p.moveTo(24, -60)
    p.cubicTo(30, 160, 10, 360, 12, 450); p.cubicTo(14, 560, 8, 680, 4, 760)
    return p


def _shorts():
    p = skia.Path()
    p.moveTo(-170, -140); p.lineTo(160, -140)
    p.cubicTo(164, -40, 166, 80, 158, 158)
    p.cubicTo(70, 174, -80, 160, -192, 128)
    p.cubicTo(-206, 70, -208, -30, -170, -140)
    p.close()
    return p


def _barra():
    p = skia.Path(); p.moveTo(158, 158); p.cubicTo(70, 174, -80, 160, -192, 128)
    return p


EIXO_BRILHO, SHORTS, BARRA = _brilho_eixo(), _shorts(), _barra()

# pontos do mundo (locais)
P_JOELHO = (-10, 452)
P_COXA = (-14, 262)
P_VIRILHA = (114, 192)                           # alto da coxa, do lado de dentro, logo abaixo do shorts
P_QUADRIL = (-178, 34)                           # halo no contorno do shorts, lado de fora
P_INTERROG = (-8, 388)                           # linha de base do "?" (logo acima da patela)
P_LUPA_JOELHO = (-6, 440)                        # no "exame" a lupa passa pelo joelho
P_LUPA = (-150, 100)                             # onde a lupa para: barra do shorts, contorno e pele da coxa
Y_TOPO_LOCAL = -140
Y_OPACO_LOCAL = 70                               # até aqui o alto do shorts dissolve no fundo


def _seta():
    p = skia.Path(); p.moveTo(-110, 424)
    p.cubicTo(-178, 410, -220, 360, -222, 280)
    p.cubicTo(-224, 200, -226, 140, -212, 88)
    return p


SETA = _seta()


def desenha_perna(cv, cam, dissolve=True):
    """Perna de desenho OPACA (pele lisa) + shorts; o alto do shorts dissolve no fundo e a ponta do pé
    nunca desce para a faixa da legenda (máscara DstIn, como no piloto). A escala (kx, ky) da câmera
    afina e alonga a perna no pré-adolescente (a mesma criança, mais velha)."""
    s, X, Y0, kx, ky = cam
    sx, sy = s * kx, s * ky
    caixa = skia.Rect(max(0.0, X - 230 * sx), max(0.0, Y0 + (Y_TOPO_LOCAL - 10) * sy),
                      min(float(W), X + 200 * sx), min(1240.0, Y0 + 900 * sy))
    if caixa.width() <= 0 or caixa.height() <= 0:
        return
    cv.saveLayer(caixa, None)
    cv.save(); cv.translate(X, Y0); cv.scale(sx, sy)
    k = 1 / s
    cv.drawOval(skia.Rect(-120, 832, 128, 870), paint("#000000", 80, blur=12))            # sombra no chão
    cv.drawPath(PERNA, paint(PELE))
    cv.save(); cv.clipPath(PERNA, skia.ClipOp.kIntersect, True)
    cv.drawPath(PERNA, paint(PELE_ESC, 210, "stroke", 40, blur=16))                      # sombra das bordas
    cv.drawPath(EIXO_BRILHO, paint(PELE_CL, 220, "stroke", 54, blur=20))                  # brilho que segue a perna
    cv.drawOval(skia.Rect(-46, 404, 30, 470), paint(PELE_CL, 150, blur=10))              # patela (só luz)
    cv.drawArc(skia.Rect(-50, 446, 34, 520), 35, 110, False, paint(PELE_ESC, 120, "stroke", 6, blur=3))
    sb = skia.Path(BARRA); sb.offset(0, 16)
    cv.drawPath(sb, paint("#000000", 60, "stroke", 28, blur=10))                          # sombra do shorts
    cv.drawRect(skia.Rect(-120, 742, 110, 860), paint(PELE_ESC, 60, blur=10))            # peito do pé
    cv.restore()
    cv.drawPath(PERNA, _p(PELE_LINHA, 235, "stroke", 3.2 * k, junta=True))
    for dx, dy, r in DEDOS:                       # dedos: a ponta sai do pé, o contorno só embaixo
        cv.drawCircle(dx, dy, r, paint(PELE))
        cv.drawCircle(dx, dy - r * 0.15, r * 0.55, paint(PELE_CL, 200, blur=3))
        cv.drawArc(skia.Rect(dx - r, dy - r, dx + r, dy + r), -15, 210, False, paint(PELE_LINHA, 225, "stroke", 2.6 * k))
    # shorts
    pt = paint(SHORT); pt.setPathEffect(skia.CornerPathEffect.Make(22))
    cv.drawPath(SHORTS, paint("#000000", 70, blur=12))
    cv.drawPath(SHORTS, pt)
    cv.save(); cv.clipPath(SHORTS, skia.ClipOp.kIntersect, True)
    cv.drawPath(SHORTS, paint(SHORT_ESC, 200, "stroke", 44, blur=16))
    cv.drawLine(-14, -140, 4, 150, paint(SHORT_CL, 130, "stroke", 34, blur=14))
    cv.drawPath(BARRA, paint(SHORT_ESC, 255, "stroke", 18))
    cv.restore()
    cv.drawPath(BARRA, paint(SHORT_LINHA, 170, "stroke", 2.6 * k))
    cv.drawLine(-168, 112, -166, 70, paint(SHORT_LINHA, 150, "stroke", 2.6 * k))         # costura lateral
    cv.restore()
    # máscara: o alto dissolve no fundo; o pé some antes da faixa da legenda
    ya, yb = Y0 + Y_TOPO_LOCAL * sy, Y0 + Y_OPACO_LOCAL * sy
    if not dissolve:                              # dentro da lupa: o mesmo desenho, nítido
        ya, yb = ya - 400 * sy, ya - 380 * sy
    yc, yd = 1168.0, 1236.0
    y0, y1 = min(ya, yc), max(yd, yb)
    if y1 > y0:
        def u(y):
            return clamp((y - y0) / (y1 - y0))
        pos = sorted([u(ya), u(yb) + 1e-4, u(yc) + 2e-4, u(yd) + 3e-4])
        masc = skia.Paint(AntiAlias=True)
        masc.setShader(skia.GradientShader.MakeLinear(
            [skia.Point(0, y0), skia.Point(0, y1)],
            [skia.ColorSetARGB(0, 0, 0, 0), skia.ColorSetARGB(255, 0, 0, 0), skia.ColorSetARGB(255, 0, 0, 0),
             skia.ColorSetARGB(0, 0, 0, 0)], [min(1.0, x) for x in pos]))
        masc.setBlendMode(skia.BlendMode.kDstIn)
        cv.drawRect(caixa, masc)
    cv.restore()


# ------------------------------------------------------------------ câmera (local -> tela)
# (escala, X, Y0, kx, ky): kx/ky afinam e alongam a perna (só no pré-adolescente)
CAM_PERTO = (1.40, 554.0, 157.0, 1.0, 1.0)    # o joelho grande no meio da tela (o espanto)
CAM_A = (0.93, 430.0, 365.0, 1.0, 1.0)        # a perna inteira: o quadril aparece
CAM_B = (0.74, 275.0, 290.0, 0.88, 1.12)      # pré-adolescente: perna mais longa e esguia, à esquerda
Y_PE_LOCAL = 845                               # sola do pé (local)


def tremor(t, T):
    k = t - (T["demora"] + 0.02)
    return 9 * math.sin(k * 70) * (1 - k / 0.35) if 0 <= k < 0.35 else 0.0


def manca(t, T):
    """Afundamento do quadril (px) no passo curto: a própria perna manca, em sincronia com as pegadas."""
    d = 0.0
    for dt, _, curto in PEGADAS:
        if not curto:
            continue
        k = t - (T["mancando"] + dt - 0.04)
        if 0 <= k < 0.12:
            d += 20 * e_out(k / 0.12)
        elif 0.12 <= k < 0.42:
            d += 20 * (1 - e_inout((k - 0.12) / 0.30))
    return d


def camera(t, T):
    k1 = e_inout(prog(t, T["joelho1"] + 0.75, T["quadril1"] - 0.05))
    k2 = e_inout(prog(t, T["pre"] - 0.1, T["pre"] + 0.75))
    c = [lerp(a, b, k1) for a, b in zip(CAM_PERTO, CAM_A)]
    s, X, Y0, kx, ky = [lerp(a, b, k2) for a, b in zip(c, CAM_B)]
    d = manca(t, T)
    ky -= d / (s * Y_PE_LOCAL)                    # o pé fica no chão; o quadril é que afunda
    return s, X, Y0 + d + tremor(t, T), kx, ky


def na_tela(cam, lx, ly):
    s, X, Y0, kx, ky = cam
    return X + s * kx * lx, Y0 + s * ky * ly


# ------------------------------------------------------------------ brilhos (vermelho-suave = dor; dourado = o quadril)
def pulso(t, T, fase=0.0):
    """Ritmo comum do brilho do joelho e do halo do quadril (período PERIODO). O halo pulsa na fase
    em que a luz SAI do quadril; o joelho, quando ela CHEGA."""
    return 0.5 + 0.5 * math.cos(2 * math.pi * ((t - T["joelho1"]) / PERIODO - fase))


def _lampejo(t, tempos, ganho=0.55, dur=0.5):
    return sum(clamp(1 - (t - t0) / dur) * ganho for t0 in tempos if t >= t0)


def i_joelho(t, T):
    if t < T["joelho1"] - 0.03:
        return 0.5                                        # a capa já mostra onde dói (parado)
    k = max(0.5, prog(t, T["joelho1"] - 0.03, T["joelho1"] + 0.2))
    apaga = prog(t, T["coxa1"] - 0.05, T["coxa1"] + 0.25) * (1 - prog(t, T["vir"] + 0.1, T["vir"] + 0.5))
    k *= 1 - 0.8 * apaga                                 # "no joelho OU na coxa": um de cada vez
    k *= 1 - prog(t, T["pre"] - 0.1, T["pre"] + 0.5)     # no pré-adolescente entram os pontinhos
    return k * (0.74 + 0.26 * pulso(t, T)) + k * _lampejo(t, (T["joelho1"], T["doi"], T["joelho3"]))


def i_coxa(t, T):
    k = prog(t, T["coxa1"] - 0.05, T["coxa1"] + 0.2) * (1 - prog(t, T["vir"], T["vir"] + 0.45))
    return k * (0.74 + 0.26 * pulso(t, T)) + k * _lampejo(t, (T["coxa1"],))


def i_halo(t, T):
    k = prog(t, T["quadril1"] - 0.1, T["quadril1"] + 0.3)
    return k * (0.62 + 0.38 * pulso(t, T, FASE_SAIDA)) + k * _lampejo(t, (T["quadril1"], T["vir"] + 0.25, T["quadril2"],
                                                               T["quadril3"] + 0.1), 0.45, 0.6)


def brilho_dor(cv, x, y, r, k):
    """Brilho vermelho-suave sobre a pele (gradiente radial; sem chama, sem sangue). (cópia do cf_osgood_sever)"""
    if k <= 0.005 or r <= 0:
        return
    sh = skia.GradientShader.MakeRadial(skia.Point(x, y), r,
                                        [C(DOR, int(225 * min(1, k))), C(DOR, int(150 * min(1, k))),
                                         C(DOR, int(55 * min(1, k))), C(DOR, 0)], [0.0, 0.35, 0.7, 1.0])
    cv.drawCircle(x, y, r, paint(DOR, 255, shader=sh))
    if k > 1:
        cv.drawCircle(x, y, r * 0.35, paint("#FFD9DA", int(120 * min(1, k - 1)), blur=10))


def halo_quadril(cv, x, y, r, k, luz=False):
    """Halo dourado-suave no contorno do quadril (só brilho: nenhuma forma desenhada por dentro).
    `luz`: soma como LUZ (Screen) — dentro da lupa ele brilha quente sobre o azul do shorts."""
    if k <= 0.005:
        return
    a = min(1.0, k)
    sh = skia.GradientShader.MakeRadial(skia.Point(x, y), r,
                                        [C(OURO, int(170 * a)), C(OURO, int(95 * a)), C(OURO, int(30 * a)), C(OURO, 0)],
                                        [0.0, 0.4, 0.75, 1.0])
    ps = [paint(OURO, 255, shader=sh), paint("#FFE8A8", int(110 * a), "stroke", r * 0.1, blur=r * 0.1)]
    if luz:
        for p in ps:
            p.setBlendMode(skia.BlendMode.kScreen)
    cv.drawCircle(x, y, r, ps[0])
    cv.drawCircle(x, y, r * 0.6, ps[1])
    if k > 1:
        cv.drawCircle(x, y, r * 0.4, paint("#FFF4CF", int(110 * min(1, k - 1)), blur=12))


def onda(cv, x, y, t, tempos, cor, r0, r1, s, dur=0.7):
    """Anel fino que se abre e some (marca o instante em que a coisa acende)."""
    for t0 in tempos:
        k = (t - t0) / dur
        if 0 <= k < 1:
            cv.drawCircle(x, y, lerp(r0, r1, e_out(k)), paint(cor, int(200 * (1 - k) ** 1.5), "stroke", 4 / s))


def ponto_dor(cv, x, y, r, k, t, t0):
    """Pontinho vermelho-suave (um lugar possível da dor) com uma onda quando acende."""
    if k <= 0.005:
        return
    brilho_dor(cv, x, y, r * 2.3, 0.9 * k)
    cv.drawCircle(x, y, r * 0.42, paint("#FFE1E2", int(235 * min(1, k))))
    kr = (t - t0) / 0.55
    if 0 <= kr < 1:
        cv.drawCircle(x, y, lerp(r * 0.6, r * 3.4, e_out(kr)), paint(DOR, int(200 * (1 - kr)), "stroke", 3.2))


# ------------------------------------------------------------------ a seta AVISA (por fora da coxa)
def seta_estado(t, T):
    """-> (quanto já cresceu 0..1, intensidade). Apaga no "dói", reacende no "vir" e pisca uma vez."""
    pr = e_inout(prog(t, T["avisando"] - 0.02, T["quadril1"] - 0.02))
    on = 1 - 0.68 * prog(t, T["doi"] - 0.05, T["doi"] + 0.3) * (1 - prog(t, T["vir"] - 0.05, T["vir"] + 0.12))
    k = t - (T["vir"] + 0.2)
    if 0 <= k < 0.42:
        on *= 1 - 0.75 * math.sin(math.pi * k / 0.42)
    return pr, on


PERIODO = 1.05                                   # ritmo comum (pulso do joelho, do quadril e da luz da seta)
FASE_SAIDA = 0.35                                # fração do período em que a luz SAI do quadril


def seta_medida(kx, ky):
    p = skia.Path(SETA); p.transform(skia.Matrix.Scale(kx, ky))
    m = skia.PathMeasure(p, False)
    return m, m.getLength()


def seta_avisa(cv, s, t, T, kx=1.0, ky=1.0):
    """Sobe do joelho ao quadril no "avisando" (o gesto de rastrear). Quando o quadril acende, a seta
    VIRA: a cabeça passa para a ponta do joelho, o tracejado corre do quadril para o joelho e, a cada
    pulso, uma luz dourada sai do quadril e chega ao joelho no pico do brilho vermelho."""
    pr, on = seta_estado(t, T)
    if pr <= 0.002:
        return
    med, L = seta_medida(kx, ky)
    seg = skia.Path(); med.getSegment(0, L * pr, seg, True)
    k = 1 / s
    reac = clamp(1 - (t - T["vir"]) / 0.7) if t >= T["vir"] else 0.0       # reacende: brilho a mais
    cv.drawPath(seg, paint(OURO, int((70 + 90 * reac) * on), "stroke", (22 + 10 * reac) * k, blur=10 * k))
    t1 = T["quadril1"] + 0.35                    # o fluxo inverte (contínuo, sem salto)
    fase = (-t if t < t1 else t - 2 * t1) * 44 * k
    for cor, al, lw in ((FUNDO_CARTAO, 175, 15), (OURO, 255, 9.5)):
        p = paint(cor, int(al * on), "stroke", lw * k)
        p.setPathEffect(skia.DashPathEffect.Make([24 * k, 14 * k], fase % (38 * k)))
        cv.drawPath(seg, p)
    inv = e_inout(prog(t, T["quadril1"] + 0.15, T["quadril1"] + 0.55))
    if inv < 1:                                   # cabeça na ponta que sobe
        pos, tan = med.getPosTan(L * pr)
        ang = math.atan2(tan.y(), tan.x()); e = 1 - inv
        ponta(cv, pos.x() + 5 * k * math.cos(ang), pos.y() + 5 * k * math.sin(ang), ang, 46 * k * e, FUNDO_CARTAO, 0.8 * on)
        ponta(cv, pos.x(), pos.y(), ang, 38 * k * e, OURO, on)
    if inv > 0 and pr >= 0.999:                   # cabeça na ponta do joelho: o aviso CHEGA ao joelho
        pos, tan = med.getPosTan(0.0)
        ang = math.atan2(tan.y(), tan.x()) + math.pi
        e = e_back(inv)
        ponta(cv, pos.x() + 5 * k * math.cos(ang), pos.y() + 5 * k * math.sin(ang), ang, 46 * k * e, FUNDO_CARTAO, 0.8 * on)
        ponta(cv, pos.x(), pos.y(), ang, 38 * k * e, OURO, on)
        ph = ((t - T["joelho1"]) % PERIODO) / PERIODO
        if ph >= FASE_SAIDA:                      # a luz que desce
            q = (ph - FASE_SAIDA) / (1 - FASE_SAIDA)
            al = inv * on * clamp(q * 6) * clamp((1 - q) * 7)
            pos = med.getPosTan(L * (1 - e_inout(q)))[0]
            cv.drawCircle(pos.x(), pos.y(), 22 * k, paint(OURO, int(150 * al), blur=12 * k))
            cv.drawCircle(pos.x(), pos.y(), 9 * k, paint("#FFF4CF", int(255 * al)))


# ------------------------------------------------------------------ o mundo (perna + brilhos + seta + "?")
# pré-adolescente: os lugares possíveis da dor, acesos UM de cada vez (chave, quando apaga, ponto)
LUGARES = (("virilha", "coxa2", P_VIRILHA), ("coxa2", "joelho4", P_COXA), ("joelho4", "mancando", P_JOELHO))


def mundo(cv, t, T, cam, com_interrog=True, lente=False):
    desenha_perna(cv, cam, dissolve=not lente)
    s, X, Y0, kx, ky = cam

    def L(p):                                     # ponto local -> local esticado (a perna alonga no pré-adolescente)
        return p[0] * kx, p[1] * ky
    cv.save(); cv.translate(X, Y0); cv.scale(s, s)
    brilho_dor(cv, *L(P_COXA), 68, i_coxa(t, T))
    brilho_dor(cv, *L(P_JOELHO), 88, i_joelho(t, T))
    # o aceso brilha forte; o que já passou fica como pontinho fraco (são ALTERNATIVAS: virilha, coxa OU
    # joelho) até o checklist começar
    fim_lug = 1 - prog(t, T["mancando"] - 0.08, T["mancando"] + 0.22)
    for chave, prox, p in LUGARES:
        liga = prog(t, T[chave] - 0.05, T[chave] + 0.18)
        forte = 1 - prog(t, T[prox] - 0.08, T[prox] + 0.22)
        k = liga * lerp(0.32, 1.0, forte) * fim_lug
        ponto_dor(cv, *L(p), 22, k * (0.85 + 0.15 * math.sin((t - T[chave]) * 6) * forte), t, T[chave])
    halo_quadril(cv, *L(P_QUADRIL), 125, i_halo(t, T) * (1.25 if lente else 1.0), luz=lente)
    if not lente:                                 # ondas: a dor acende no joelho; o aviso chega no quadril
        onda(cv, *L(P_JOELHO), t, (T["joelho1"], T["doi"]), DOR, 60, 190, s)
        onda(cv, *L(P_QUADRIL), t, (T["quadril1"], T["quadril2"], T["quadril3"] + 0.1), OURO, 70, 210, s)
        seta_avisa(cv, s, t, T, kx, ky)
    if com_interrog:
        interrog(cv, t, T, L)
    cv.restore()


P_INTERROG_B = (-30, 400)                         # pré-adolescente: o "?" menor, no vão entre COXA e JOELHO


def interrog(cv, t, T, L=lambda p: p):
    """O "?" branco acima do joelho: salta no "joelho" (o espanto) e só some, devagar, no "esclarecer"."""
    k = prog(t, T["joelho1"] - 0.04, T["joelho1"] + 0.36)
    if k <= 0:
        return
    sai = e_inout(prog(t, T["esclarecer"], T["esclarecer"] + 1.4))
    if sai >= 1:
        return
    k2 = e_inout(prog(t, T["pre"] - 0.1, T["pre"] + 0.75))
    esc = lerp(0.3, 1.0, e_back(k)) * lerp(1.0, 0.35, sai) * lerp(1.0, 0.76, k2)
    bal = 4 * math.sin((t - T["joelho1"]) * 2.4)
    a = clamp(k * 3) * (1 - sai)
    x, y = L((lerp(P_INTERROG[0], P_INTERROG_B[0], k2), lerp(P_INTERROG[1], P_INTERROG_B[1], k2)))
    cv.save(); cv.translate(x, y - 40 + bal); cv.scale(esc, esc); cv.rotate(6 * math.sin((t - T["joelho1"]) * 1.7))
    texto(cv, T_INTERROG, 0, 40, F_BLACK, 132, "#FFFFFF", int(255 * a), contorno=16)
    cv.restore()


# ------------------------------------------------------------------ lupa (só amplia o MESMO desenho)
def lupa_estado(t, T, cam):
    """-> (x, y, r, alfa) da lupa na tela, ou None. Entra pela direita no "olha" e PARA no quadril."""
    t0 = T["olha"] - 0.08
    if t < t0:
        return None
    s = cam[0]
    alvo = na_tela(cam, *P_LUPA)
    # "o EXAME clínico": a lupa desce ao joelho e volta ao quadril (o exame olha os dois)
    ks = e_inout(prog(t, T["exame"] + 0.05, T["exame"] + 0.7)) * (1 - e_inout(prog(t, T["quando"] - 0.15, T["indicado"] + 0.4)))
    if ks > 0:
        jx, jy = na_tela(cam, *P_LUPA_JOELHO)
        alvo = (lerp(alvo[0], jx, ks), lerp(alvo[1], jy, ks))
    k = e_inout(prog(t, t0, t0 + 0.75))
    x = lerp(1190, alvo[0], k); y = lerp(560, alvo[1], k) - 18 * math.sin(math.pi * k)   # por baixo da faixa
    pousa = e_back(prog(t, t0 + 0.7, t0 + 1.0))
    r = 120 * s / CAM_A[0] * (0.92 + 0.08 * pousa if k >= 1 else 0.92)
    return x, y, r, 1.0


def lupa(cv, t, T, cam):
    st = lupa_estado(t, T, cam)
    if st is None:
        return
    x, y, r, a = st
    m = 1.3
    cv.save()
    clip = skia.Path(); clip.addCircle(x, y, r)
    cv.clipPath(clip, skia.ClipOp.kIntersect, True)
    sh = skia.GradientShader.MakeRadial(skia.Point(W / 2, H * 0.42 + 40 * math.sin(t * 0.3)), H * 0.78,
                                        [_c(BG_IN), _c(BG_OUT)])
    cv.drawCircle(x, y, r + 2, paint(BG_IN, shader=sh))
    cv.drawCircle(x, y, r + 2, paint("#FFFFFF", 8))                           # lente clara, sem fundo escuro
    s, X, Y0, kx, ky = cam
    cam_m = (s * m, x + (X - x) * m, y + (Y0 - y) * m, kx, ky)
    mundo(cv, t, T, cam_m, com_interrog=False, lente=True)
    cv.restore()
    ang = math.radians(225)                                                    # cabo para cima e para fora
    hx, hy = x + r * math.cos(ang), y + r * math.sin(ang)
    L = 74 * r / 120
    ex, ey = hx + L * math.cos(ang), hy + L * math.sin(ang)
    cv.drawLine(hx, hy, ex, ey, paint("#000000", 80, "stroke", 30 * r / 120, blur=6))
    cv.drawLine(hx, hy, ex, ey, paint("#8A6512", 255, "stroke", 26 * r / 120))
    cv.drawLine(hx, hy, ex, ey, paint(OURO, 255, "stroke", 16 * r / 120))
    cv.drawCircle(x, y, r, paint("#000000", 80, "stroke", 20, blur=6))
    cv.drawCircle(x, y, r, paint(OURO, 255, "stroke", 13 * r / 120 + 2))
    cv.drawCircle(x, y, r - 8, paint("#FFF1C2", 120, "stroke", 2.5))
    cv.drawArc(skia.Rect(x - r * 0.72, y - r * 0.72, x + r * 0.72, y + r * 0.72), 290, 50, False,
               paint("#FFFFFF", 150, "stroke", 7))


# ------------------------------------------------------------------ pegadas (cópia do cf_crianca_mancando)
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
DEDOS_PEG = ((15, -67, 10.5), (0, -71, 7.6), (-11, -67, 6.8), (-20, -60, 6.2), (-27, -50, 5.4))


def pegada(cv, x, y, esc, a, direita=False):
    """Pegada de criança vista de cima, apontando para a direita (sentido da marcha), achatada pela
    perspectiva do chão."""
    if a <= 0:
        return
    m = skia.Matrix(); m.setScale(esc, -esc if direita else esc); m.postRotate(90); m.postScale(1, 0.42)
    m.postTranslate(x, y)
    cv.save(); cv.concat(m)
    cv.drawPath(SOLA, paint(MARFIM, int(235 * a)))
    cv.drawPath(SOLA, paint(OSSO_B, int(200 * a), "stroke", 3))
    for dx, dy, r in DEDOS_PEG:
        cv.drawCircle(dx, dy, r, paint(MARFIM, int(235 * a)))
    cv.restore()


# mesmo tamanho, espaçamento desigual (passo curto / passo longo): o mancar
PEGADAS = ((0.10, 104, False), (0.32, 190, True), (0.84, 364, False), (1.06, 450, True))
Y_CHAO = round(CAM_B[2] + CAM_B[0] * CAM_B[4] * Y_PE_LOCAL) + 8      # o chão encosta na sola do pé


def chao(cv, t, T, a0):
    a = prog(t, T["mancando"], T["mancando"] + 0.3) * a0
    if a <= 0:
        return
    sh = skia.GradientShader.MakeLinear([skia.Point(0, Y_CHAO), skia.Point(0, Y_CHAO + 130)],
                                        [_c("#FFFFFF", 30), _c("#FFFFFF", 0)])
    caixa = skia.Rect(30, Y_CHAO - 6, 530, Y_CHAO + 130)
    cv.saveLayer(caixa, None)
    cv.drawRect(skia.Rect(30, Y_CHAO, 530, Y_CHAO + 130), paint("#FFFFFF", int(255 * a), shader=sh))
    cv.drawLine(30, Y_CHAO, 530, Y_CHAO, paint("#CFE3F5", int(110 * a), "stroke", 3))
    for dt, x, dir_ in PEGADAS:
        ts = T["mancando"] + dt
        k = t - ts
        if k < 0:
            continue
        esc = 0.9 * lerp(1.3, 1.0, e_out(clamp(k / 0.18)))
        y = Y_CHAO + (82 if dir_ else 40)
        kr = k / 0.4
        if kr < 1:                                                   # onda no chão a cada pisada
            rx = lerp(20, 70, e_out(kr))
            cv.drawOval(skia.Rect(x - rx, y - rx * 0.16, x + rx, y + rx * 0.16), paint("#FFFFFF", int(140 * (1 - kr) * a), "stroke", 3))
        pegada(cv, x, y, esc, clamp(k / 0.08) * 0.95 * a, direita=dir_)
    masc = skia.Paint(AntiAlias=True)                                # o chão some nas pontas
    masc.setShader(skia.GradientShader.MakeLinear([skia.Point(30, 0), skia.Point(530, 0)],
                                                  [skia.ColorSetARGB(0, 0, 0, 0), skia.ColorSetARGB(255, 0, 0, 0),
                                                   skia.ColorSetARGB(255, 0, 0, 0), skia.ColorSetARGB(0, 0, 0, 0)],
                                                  [0.0, 0.1, 0.88, 1.0]))
    masc.setBlendMode(skia.BlendMode.kDstIn)
    cv.drawRect(caixa, masc)
    cv.restore()


# ------------------------------------------------------------------ coluna da direita: prancheta -> cartões
PR_R = (440, 728, 1032, 1010)                  # prancheta (metade de baixo, no pré-adolescente)
EX_R = (400, 360, 1036, 462)                   # cartão EXAME CLÍNICO
RAD_R = (400, 490, 1036, 652)                  # cartão QUANDO INDICADO / RADIOGRAFIA
CARIMBO_XY = (736, 880)
CK_TAM = 40


def tique(cv, x, y, pr, cor, a, esc=1.0, larg=6):
    if pr <= 0 or a <= 0:
        return
    p = skia.Path(); p.moveTo(x + 10 * esc, y - 17 * esc)
    p.lineTo(x + (10 + 12 * min(1, pr * 2)) * esc, y + (-17 + 12 * min(1, pr * 2)) * esc)
    if pr > 0.5:
        q = (pr - 0.5) * 2
        p.lineTo(x + (22 + 22 * q) * esc, y + (-5 - 30 * q) * esc)
    cv.drawPath(p, _p(cor, int(255 * a), "stroke", larg, junta=True))


def prancheta(cv, t, T, fim):
    ent = e_out(prog(t, T["pre"] + 0.3, T["pre"] + 0.9))
    if ent <= 0 or fim <= 0:
        return
    mor = e_inout(prog(t, T["exame"] - 0.05, T["exame"] + 0.65))
    r = [lerp(a, b, mor) for a, b in zip(PR_R, EX_R)]
    dx = 680 * (1 - ent)
    a = clamp(ent * 2) * fim
    x0, y0, x1, y1 = r[0] + dx, r[1], r[2] + dx, r[3]
    rr = skia.RRect.MakeRectXY(skia.Rect(x0, y0, x1, y1), 24, 24)
    cv.drawRRect(rr, paint("#000000", int(90 * a), blur=14))
    cv.drawRRect(rr, paint(FUNDO_CARTAO, int(238 * a)))
    cv.drawRRect(rr, paint(lerp_cor(MARFIM, OSSO_B, mor), int(235 * a), "stroke", lerp(4, 3, mor)))
    a_cl = a * (1 - prog(mor, 0.0, 0.4))
    if a_cl > 0:                                                         # prendedor dourado
        cm = (x0 + x1) / 2
        cl = skia.RRect.MakeRectXY(skia.Rect(cm - 62, y0 - 22, cm + 62, y0 + 22), 11, 11)
        cv.drawRRect(cl, paint(OURO, int(255 * a_cl)))
        cv.drawRRect(cl, paint("#8A6512", int(255 * a_cl), "stroke", 3))
        cv.drawCircle(cm, y0 - 4, 7, paint("#8A6512", int(255 * a_cl)))
    # itens: aparecem apagados (checklist vazio) e acendem com o tique BRANCO
    a_it = a * (1 - prog(mor, 0.0, 0.35))
    sob = 1 - 0.6 * prog(t, T["demora"], T["demora"] + 0.12)            # sob o carimbo, caixas e tiques esmaecem
    sob_txt = 1 - prog(t, T["demora"] - 0.02, T["demora"] + 0.10)       # e o TEXTO some (nada de texto sob texto)
    f = skia.Font(F_BLACK, CK_TAM)
    for i, (s_, chave) in enumerate(zip(T_ITENS, ("mancando", "trauma"))):
        if a_it <= 0:
            break
        y = y0 + 132 + i * 104
        x = x0 + 40
        on = prog(t, T[chave], T[chave] + 0.2)
        caixa = skia.RRect.MakeRectXY(skia.Rect(x, y - 42, x + 50, y + 8), 10, 10)
        cv.drawRRect(caixa, paint(FUNDO_CARTAO, int(255 * a_it)))
        cv.drawRRect(caixa, paint("#FFFFFF", int(255 * a_it * lerp(0.45, 1.0, on) * sob), "stroke", 3.5))
        tique(cv, x, y, e_out(prog(t, T[chave], T[chave] + 0.3)), "#FFFFFF", a_it * sob)
        if sob_txt > 0:
            cv.drawString(s_, x + 70 + 16 * (1 - e_out(on)), y, f, paint("#FFFFFF", int(a_it * sob_txt * lerp(95, 255, on))))
    # vira o cartão sóbrio EXAME CLÍNICO
    a_ex = a * prog(t, T["exame"] + 0.25, T["exame"] + 0.6)
    if a_ex > 0:
        texto(cv, T_EXAME, (x0 + x1) / 2, y0 + 68, F_BLACK, 48, "#FFFFFF", int(255 * a_ex))


def lerp_cor(c1, c2, x):
    a = [int(c1[i:i + 2], 16) for i in (1, 3, 5)]; b = [int(c2[i:i + 2], 16) for i in (1, 3, 5)]
    return "#" + "".join(f"{int(lerp(a[i], b[i], x)):02X}" for i in range(3))


def cartao_radio(cv, t, T, fim):
    k = prog(t, T["indicado"] - 0.12, T["indicado"] + 0.35)
    if k <= 0 or fim <= 0:
        return
    a = clamp(k * 2) * fim
    dx = 60 * (1 - e_out(k))
    x0, y0, x1, y1 = RAD_R
    rr = skia.RRect.MakeRectXY(skia.Rect(x0 + dx, y0, x1 + dx, y1), 22, 22)
    cv.drawRRect(rr, paint("#000000", int(80 * a), blur=12))
    cv.drawRRect(rr, paint(FUNDO_CARTAO, int(238 * a)))
    cv.drawRRect(rr, paint(AZUL, int(230 * a), "stroke", 3))
    cx = (x0 + x1) / 2 + dx
    texto(cv, T_QUANDO, cx, y0 + 58, F_BLACK, 38, AZUL, int(255 * a))
    kr = prog(t, T["radiografia"] - 0.05, T["radiografia"] + 0.3)
    if kr > 0:
        texto(cv, T_RADIO, cx + 20 * (1 - e_out(kr)), y0 + 128, F_BLACK, 50, "#FFFFFF", int(255 * a * kr))


def carimbo_duplo(cv, linhas, x, y, rot, t0, t, a_fim, tam=54, cor=VERMELHO):
    """Carimbo em duas linhas (mesma batida do cf_comum.carimbo), que FICA na tela."""
    k = t - t0
    if k < 0 or a_fim <= 0:
        return
    esc = lerp(1.9, 1.0, e_out(clamp(k / 0.16))); a = clamp(k / 0.08) * a_fim
    f = skia.Font(F_BLACK, tam)
    ws = [f.measureText(s) for s in linhas]; lw = max(ws)
    cv.save(); cv.translate(x, y); cv.rotate(rot); cv.scale(esc, esc)
    h = tam * 0.92 + 26
    rr = skia.RRect.MakeRectXY(skia.Rect(-lw / 2 - 30, -h - 4, lw / 2 + 30, h + 4), 14, 14)
    cv.drawRRect(rr, paint("#0B1824", int(245 * a)))
    cv.drawRRect(rr, paint(cor, int(255 * a), "stroke", 7))
    rr2 = skia.RRect.MakeRectXY(skia.Rect(-lw / 2 - 18, -h + 8, lw / 2 + 18, h - 8), 9, 9)
    cv.drawRRect(rr2, paint(cor, int(150 * a), "stroke", 2.5))
    for s, w_, yy in zip(linhas, ws, (-tam * 0.2, tam * 0.92)):
        cv.drawString(s, -w_ / 2, yy, f, paint(cor, int(255 * a)))
    cv.restore()


def avaliar_cedo(cv, t, T, fim):
    k = prog(t, T["cedo"] - 0.05, T["cedo"] + 0.3)
    if k <= 0 or fim <= 0:
        return
    a = k * fim
    x, y = CARIMBO_XY[0], 1058
    larg = texto(cv, T_CEDO, x, y + 14 * (1 - e_out(k)), F_BLACK, 50, "#FFFFFF", int(255 * a), contorno=8)
    u = e_inout(prog(t, T["cedo"] + 0.1, T["cedo"] + 0.7))
    if u > 0:
        cv.drawLine(x - larg / 2, y + 20, x - larg / 2 + larg * u, y + 20, paint(OURO, int(255 * a), "stroke", 3))


# ------------------------------------------------------------------ rótulos da perna e cartões da 1ª parte
def faixa(cv, t, T, fim):
    """Faixa discreta no topo: NA CRIANÇA -> PRÉ-ADOLESCENTE (sem rosto, sem corpo)."""
    a1 = prog(t, T["crianca"] - 0.05, T["crianca"] + 0.25) * (1 - prog(t, T["pre"] - 0.1, T["pre"] + 0.15))
    a2 = prog(t, T["pre"] + 0.05, T["pre"] + 0.3) * fim
    for s, a, dy in ((T_CRIANCA, a1, -10 * prog(t, T["pre"] - 0.1, T["pre"] + 0.15)),
                     (T_PRE, a2, 10 * (1 - prog(t, T["pre"] + 0.05, T["pre"] + 0.3)))):
        if a <= 0:
            continue
        f = skia.Font(F_BLACK, 38); lw = f.measureText(s)
        y = 270 + dy
        rr = skia.RRect.MakeRectXY(skia.Rect(540 - lw / 2 - 30, y - 40, 540 + lw / 2 + 30, y + 13), 26, 26)
        cv.drawRRect(rr, paint(FUNDO_CARTAO, int(215 * a)))
        cv.drawRRect(rr, paint(AZUL, int(200 * a), "stroke", 2.5))
        cv.drawString(s, 540 - lw / 2, y, f, paint(AZUL, int(255 * a)))


def rotulos(cv, t, T, cam):
    sai_a = 1 - prog(t, T["pre"] - 0.2, T["pre"] + 0.1)              # a 1ª parte sai no pré-adolescente
    # JOELHO (à direita do joelho) -> sai quando entra o cartão do "motivo"
    xa, ya = na_tela(cam, *P_JOELHO)
    xr = na_tela(cam, 132, 0)[0] + 34
    a = prog(t, T["joelho1"] + 0.45, T["joelho1"] + 0.7) * (1 - prog(t, T["motivo"] - 0.25, T["motivo"])) * sai_a
    a *= 1 - 0.7 * prog(t, T["coxa1"] - 0.05, T["coxa1"] + 0.2) * (1 - prog(t, T["vir"] + 0.1, T["vir"] + 0.4))
    etiqueta(cv, T_JOELHO, xr, ya + 14, DOR_TXT, a, ancora=(xa + 18, ya), borda=DOR)
    # COXA (à direita da coxa), enquanto a coxa brilha
    xa, ya = na_tela(cam, *P_COXA)
    a = prog(t, T["coxa1"], T["coxa1"] + 0.25) * (1 - prog(t, T["vir"], T["vir"] + 0.3))
    etiqueta(cv, T_COXA, na_tela(cam, 148, 0)[0] + 30, ya + 14, DOR_TXT, a, ancora=(xa + 18, ya), borda=DOR)
    # AVISA: à esquerda da seta, no meio dela (sai quando a seta apaga, volta quando reacende)
    xm, ym = na_tela(cam, -222, 280)
    pr, _ = seta_estado(t, T)
    a = (prog(pr, 0.45, 0.7) * (1 - prog(t, T["doi"] - 0.05, T["doi"] + 0.25))
         + prog(t, T["vir"], T["vir"] + 0.25)) * sai_a
    etiqueta(cv, T_AVISA, xm - 16, ym + 13, OURO, clamp(a), tam=36, alinh="dir")
    # QUADRIL: acima do quadril, à esquerda (sai quando a lupa chega)
    xq, yq = na_tela(cam, *P_QUADRIL)
    a = prog(t, T["quadril1"] + 0.12, T["quadril1"] + 0.4) * (1 - prog(t, T["olha"] - 0.15, T["olha"] + 0.15))
    etiqueta(cv, T_QUADRIL, xq + 30, yq - 70, OURO, a, alinh="dir", ancora=(xq - 4, yq - 16))
    # TAMBÉM SE OLHA O QUADRIL: colado à direita da lupa; acompanha a lupa na troca de câmera e fica
    # até o 1º pontinho do pré-adolescente (~1,8 s de leitura)
    st = lupa_estado(t, T, cam)
    if st is not None:
        x, y, r, _ = st
        a = prog(t, T["olha"] + 0.45, T["olha"] + 0.72) * (1 - prog(t, T["virilha"] - 0.35, T["virilha"] - 0.05))
        lw = skia.Font(F_BLACK, 34).measureText(T_OLHA)
        xl = min(x + r + 22, 1036 - (1.1 * lw + 32))          # nunca passa de x=1040 (folga p/ a Roboto)
        etiqueta(cv, T_OLHA, xl, y + 13, "#FFFFFF", a, tam=34, borda=OURO, ancora=(x + r + 4, y),
                 dx=14 * (1 - e_out(prog(t, T["olha"] + 0.45, T["olha"] + 0.85))))
    # pré-adolescente: o rótulo do pontinho aceso (um de cada vez), à direita da perna; o fio sai do
    # próprio ponto (sem "ponto duplo")
    rot = {"virilha": T_VIRILHA, "coxa2": T_COXA, "joelho4": T_JOELHO}
    for chave, prox, p in LUGARES:
        a = prog(t, T[chave], T[chave] + 0.2) * (1 - prog(t, T[prox] - 0.1, T[prox] + 0.12))
        if a <= 0:
            continue
        xa, ya = na_tela(cam, *p)
        etiqueta(cv, rot[chave], 412, ya + 14, DOR_TXT, a, ancora=(xa, ya), borda=DOR,
                 dx=18 * (1 - e_out(prog(t, T[chave], T[chave] + 0.3))))


def cartao_motivo(cv, t, T):
    k = prog(t, T["motivo"] - 0.08, T["motivo"] + 0.3)
    if k <= 0:
        return
    sai = e_in_back(prog(t, T["olha"] - 0.1, T["olha"] + 0.35))
    a = clamp(k * 2) * (1 - prog(t, T["olha"] + 0.05, T["olha"] + 0.35))
    if a <= 0:
        return
    dx = 70 * (1 - e_out(k)) + 520 * sai
    x0, y0, x1, y1 = 568 + dx, 706, 1032 + dx, 864
    rr = skia.RRect.MakeRectXY(skia.Rect(x0, y0, x1, y1), 24, 24)
    cv.drawRRect(rr, paint("#000000", int(90 * a), blur=14))
    cv.drawRRect(rr, paint(FUNDO_CARTAO, int(240 * a)))
    bico = skia.Path(); bico.moveTo(x0 + 2, 768); bico.lineTo(x0 - 24, 785); bico.lineTo(x0 + 2, 802); bico.close()
    cv.drawPath(bico, paint(OURO, int(255 * a)))
    cv.drawRRect(rr, paint(OURO, int(255 * a), "stroke", 4))
    cx = (x0 + x1) / 2
    texto(cv, T_MOTIVO[0], cx, 768, F_BLACK, 46, "#FFFFFF", int(255 * a))
    texto(cv, T_MOTIVO[1], cx, 832, F_BLACK, 46, OURO, int(255 * a))


# ------------------------------------------------------------------ quadro
def quadro(cv, t, T, blocos, ep):
    fundo(cv, t)
    fim = 1 - prog(t, T["manda"] - 0.45, T["manda"] - 0.1)
    cam = camera(t, T)
    tr = tremor(t, T)

    chao(cv, t, T, fim)                           # antes da perna: o pé pisa na linha do chão
    a_mundo = 0.3 + 0.7 * fim                     # na CTA o mundo cai a 30% (antes do véu da interface)
    if a_mundo < 1:
        cv.saveLayerAlpha(None, int(255 * a_mundo))
    mundo(cv, t, T, cam)
    lupa(cv, t, T, cam)
    if a_mundo < 1:
        cv.restore()
    rotulos(cv, t, T, cam)
    cartao_motivo(cv, t, T)
    faixa(cv, t, T, fim)

    cv.save(); cv.translate(tr, 0)
    prancheta(cv, t, T, fim)
    cartao_radio(cv, t, T, fim)
    # o carimbo já cumpriu o papel no "exame": recua a 45% e a hierarquia segue a fala
    a_car = fim * (1 - 0.55 * e_inout(prog(t, T["exame"] - 0.05, T["exame"] + 0.4)))
    carimbo_duplo(cv, T_CARIMBO, CARIMBO_XY[0], CARIMBO_XY[1], -5, T["demora"], t, a_car)
    avaliar_cedo(cv, t, T, fim)
    cv.restore()

    capa(cv, t, T["quadril1"] - 0.25, ep["gancho"][0], ep["gancho"][1])
    selo_como_funciona(cv, prog(t, T["quadril1"] + 0.25, T["quadril1"] + 0.65) * (1 - prog(t, T["manda"] - 0.3, T["manda"])))
    interface(cv, t, T, blocos, DESTAQUE)


# ------------------------------------------------------------------ som e prévias
def sons(T):
    ev = [(T["joelho1"] - 0.02, "pop", 0.65), (T["joelho1"] + 0.04, "ping", 0.5),
          (T["joelho1"] + 0.8, "whoosh", 0.25),                                  # a câmera recua
          (T["avisando"] - 0.02, "whoosh", 0.5)]
    ev += [(T["avisando"] + 0.08 + 0.13 * i, "tick", 0.28) for i in range(4)]       # a seta sobe, pontilhada
    ev += [(T["quadril1"] + 0.0, "ding", 0.55), (T["quadril1"] + 0.06, "shimmer", 0.4),
           (T["crianca"], "tick", 0.45), (T["doi"], "thump", 0.4), (T["coxa1"], "pop", 0.5),
           (T["vir"], "whoosh", 0.35), (T["vir"] + 0.2, "ping", 0.5), (T["quadril2"], "ping", 0.3),
           (T["motivo"] - 0.08, "whoosh", 0.35), (T["motivo"] + 0.15, "pop", 0.55),
           (T["olha"] - 0.1, "whoosh", 0.5), (T["olha"] + 0.66, "click", 0.6), (T["quadril3"] + 0.12, "ding", 0.4),
           (T["pre"] - 0.08, "whoosh", 0.55), (T["pre"] + 0.08, "tick", 0.45), (T["pre"] + 0.65, "pop", 0.5),
           (T["virilha"], "pop", 0.5), (T["coxa2"], "pop", 0.5), (T["joelho4"], "pop", 0.5),
           (T["mancando"] + 0.02, "click", 0.75)]
    ev += [(T["mancando"] + dt, "tick", 0.5 if not d else 0.28) for dt, _, d in PEGADAS]   # passo desigual
    ev += [(T["trauma"] + 0.02, "click", 0.75), (T["demora"] - 0.02, "thump", 0.9),
           (T["exame"] - 0.05, "whoosh", 0.45), (T["exame"] + 0.62, "tick", 0.4),
           (T["indicado"] - 0.12, "whoosh", 0.35), (T["indicado"] + 0.22, "pop", 0.45), (T["radiografia"], "tick", 0.4),
           (T["esclarecer"] + 0.1, "whoosh", 0.22), (T["cedo"], "ding", 0.4), (T["manda"] + 0.05, "whoosh", 0.5)]
    return ev


def tempos_previa(T):
    return [0.0, T["joelho1"] + 0.45, T["avisando"] + 0.35, T["quadril1"] + 0.9, T["coxa1"] + 0.4,
            T["motivo"] + 0.7, T["olha"] + 0.85, T["pre"] + 0.9, T["coxa2"] + 0.3, T["mancando"] + 0.36,
            T["demora"] + 0.3, T["cedo"] + 1.2]


# respiro antes da CTA: o quadro final (carimbo, cartões e AVALIAR CEDO) fica ~2 s para leitura.
render = fazer_render(quadro, ANCORAS, sons, tempos_previa, respiro_cta=2.0)
