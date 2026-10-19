# -*- coding: utf-8 -*-
"""COMO FUNCIONA — criança mancando ("CRIANÇA MANCANDO? / NÃO É MANHA.").

Mesmo estilo das cenas aprovadas (fundo azul-petróleo, marfim, dourado, rótulos, carimbo, checklist,
calendário sem número, legenda karaokê, CTA com aviãozinho). O mecanismo é o PASSO: duas pernas de
desenho, de perfil, andam no lugar sobre uma esteira; a da frente (a que manca) fica pouco tempo no
chão e a outra muito, e o quadril CAI no apoio curto — o ritmo desigual se ouve (clique a cada passo)
e se vê nas pegadas, do MESMO tamanho, com espaçamento desigual (a do lado que manca mais clara).
Depois, um semáforo de pressa SEM luz verde (de propósito) sobe de âmbar a vermelho conforme a fala.

O que o verificador exigiu está aqui:
  * Pernas de desenho (contorno arredondado, pele lisa, shorts): nenhum osso, nada translúcido,
    nenhum exame, nenhum fundo preto; a faísca de dor e o círculo do inchaço flutuam SOLTOS, sem marcar
    ponto anatômico; a "articulação" é uma dobradiça esquemática (um bastão fixo, outro que dobra e
    volta, um pino) no vazio à direita, LONGE do joelho — não aponta qual articulação.
  * "NÃO É MANHA" é o carimbo DOURADO (desfaz o mito, não repreende ninguém); vermelho só na pressa
    (PEDE PRESSA, NO MESMO DIA), nas faíscas do encaixe MANCAR + FEBRE e no contorno das fichas no
    "juntas". Dourado nunca comemora o alarme.
  * No "apoia" o pé que manca para no ar: a última pisada dele não deixa pegada e, no lugar, pulsa
    uma pegada VAZIA tracejada em branco (as outras pegadas baixam à metade).
  * "No mesmo dia": um calendário grande entra no "procure" virando folhas sem parar, freia no
    "mesmo" até PARAR numa folha inteira e ganha um círculo vermelho feito à mão.
  * Saídas definidas para o quadro não lotar: escudo, faísca e bateria saem no "sempre"; a prancheta
    recolhe no 1º "febre" e só o termômetro fica guardado no canto; a lua some no "apressam"; a
    dobradiça esmaece no "apoia"; os rótulos da perna saem no "juntas".
  * Nenhum rosto chorando; nenhuma bactéria-personagem; nada de pus ou sangue.
Desvio consciente do storyboard: as etiquetas recolhem para dentro da luz laranja no "Mancar" da
frase 5 (0,6 s antes do "febre"), para a ficha MANCAR — que nasce das pernas nessa palavra — ter
lugar livre; a ficha FEBRE nasce do termômetro no "febre" e as duas se encaixam com clique metálico.
A cena é PRESA ao roteiro pelas palavras-âncora (ANCORAS): mudar o roteiro sem elas quebra o render
de propósito (KeyError), em vez de sair vídeo dessincronizado.
"""
import math

import skia

from .cf_alongamento import (ACO, ACO_ESC, ACO_HL, F_BLACK, OSSO_B, OSSO_C, OSSO_L, OURO, PELE, VERMELHO, H, W,
                             clamp, e_back, e_inout, e_out, fundo, lerp, paint, prog)
from .cf_comum import capa, fazer_render, interface, selo_como_funciona
from .cf_fratura_cola import calendario, carimbo_ouro

# ------------------------------------------------------------------ sincronia com a fala
ANCORAS = {
    "mancar1": ("mancar", 1, False), "manha": ("manha", 1, False), "protegendo": ("protegendo", 1, False),
    "foge": ("foge", 1, False), "fraqueza": ("fraqueza", 1, False), "sempre": ("sempre", 1, False),
    "repare": ("repare", 1, False), "quando": ("quando", 1, False), "doi": ("dói", 1, False),
    "febre1": ("febre", 1, False), "mancar2": ("mancar", 2, False), "melhora": ("melhora", 1, False),
    "noite": ("noite", 1, False), "inchaco": ("inchaço", 1, False), "apressam": ("apressam", 1, False),
    "mancar3": ("mancar", 3, False), "febre2": ("febre", 2, False), "pede": ("pede", 1, False),
    "pode": ("pode", 1, False), "articulacao": ("articulação", 1, False), "apoia": ("apoia", 1, False),
    "chora": ("chora", 1, False), "aumenta": ("aumenta", 1, False), "juntas": ("juntas", 1, False),
    "procure": ("procure", 1, False), "mesmo": ("mesmo", 1, False), "manda": ("manda", 1, False),
}
DESTAQUE = {"manha", "protegendo", "dor", "fraqueza", "sempre", "avalia", "febre", "melhora", "noite", "inchaço",
            "apressam", "pressa", "infecção", "articulação", "apoia", "chora", "aumenta", "juntas", "mesmo", "dia"}

PELE_CL, PELE_ESC, PELE_LINHA = "#F7CDB8", "#DA987E", "#B9765E"
SHORT, SHORT_CL, SHORT_ESC, SHORT_LINHA = "#4C86C6", "#6FA3DA", "#3A6FA8", "#2C5A8E"
FUNDO_CARTAO = "#0B1824"
LARANJA = "#FF8A3D"
AZUL_CL = "#9CC9FF"
INCHA = "#FF9F7A"
MARFIM = OSSO_C


# ------------------------------------------------------------------ utilidades
def _c(h, a=255):
    h = h.lstrip("#")
    return skia.ColorSetARGB(int(a), int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))


def _alfa(a):
    p = skia.Paint()
    p.setAlphaf(clamp(a))
    return p


def _uniao(a, b):
    return skia.Op(a, b, skia.PathOp.kUnion_PathOp) or a


def _trim(pt, k):
    """Traço desenhado até a fração k (TrimPathEffect devolve None em k = 0)."""
    if k < 0.999:
        pe = skia.TrimPathEffect.Make(0.0, max(0.002, k))
        if pe is not None:
            pt.setPathEffect(pe)
    return pt


def ponta(cv, x, y, ang, tam, cor, a):
    """Cabeça de seta em (x, y) apontando para `ang` (radianos). (cópia do cf_pe_virado)"""
    p = skia.Path()
    p.moveTo(x + tam * math.cos(ang), y + tam * math.sin(ang))
    p.lineTo(x + tam * 0.75 * math.cos(ang + 2.45), y + tam * 0.75 * math.sin(ang + 2.45))
    p.lineTo(x + tam * 0.75 * math.cos(ang - 2.45), y + tam * 0.75 * math.sin(ang - 2.45))
    p.close()
    cv.drawPath(p, paint(cor, int(255 * a)))


def chip(cv, s, x, y, cor, a, tam=40, borda=None, dim=1.0):
    """Rótulo solto centrado em x (y = linha de base). `dim` esmaece texto e borda; o fundo fica opaco."""
    if a <= 0:
        return
    f = skia.Font(F_BLACK, tam); lw = f.measureText(s)
    rr = skia.RRect.MakeRectXY(skia.Rect(x - lw / 2 - 24, y - tam * 1.05, x + lw / 2 + 24, y + tam * 0.34), 16, 16)
    cv.drawRRect(rr, paint(FUNDO_CARTAO, int(225 * a)))
    cv.drawRRect(rr, paint(borda or cor, int(255 * a * dim), "stroke", 3))
    cv.drawString(s, x - lw / 2, y, f, paint(cor, int(255 * a * dim)))


def placa(cv, s, x1, y, cor, a, tam=40, texto_cor="#FFFFFF", larg_borda=3.0):
    """Rótulo alinhado à DIREITA em x1 (as placas do semáforo e as da perna)."""
    if a <= 0:
        return
    f = skia.Font(F_BLACK, tam); lw = f.measureText(s)
    x0 = x1 - lw - 48
    rr = skia.RRect.MakeRectXY(skia.Rect(x0, y - tam * 1.05, x1, y + tam * 0.34), 16, 16)
    cv.drawRRect(rr, paint(FUNDO_CARTAO, int(230 * a)))
    cv.drawRRect(rr, paint(cor, int(255 * a), "stroke", larg_borda))
    cv.drawString(s, x0 + 24, y, f, paint(texto_cor, int(255 * a)))


def carimbo_cor(cv, s, x, y, rot, t0, t, dur=1.9, tam=58, cor=VERMELHO):
    """Carimbo (mesma batida do cf_comum.carimbo) em outra cor e tamanho."""
    k = t - t0
    if k < 0 or k > dur:
        return
    esc = lerp(1.9, 1.0, e_out(clamp(k / 0.16))); a = clamp(k / 0.08) * (1 - prog(k, dur - 0.35, dur))
    cv.save(); cv.translate(x, y); cv.rotate(rot); cv.scale(esc, esc)
    f = skia.Font(F_BLACK, tam); lw = f.measureText(s)
    rr = skia.RRect.MakeRectXY(skia.Rect(-lw / 2 - 24, -tam, lw / 2 + 24, tam * 0.36), 12, 12)
    cv.drawRRect(rr, paint("#0B1824", int(175 * a))); cv.drawRRect(rr, paint(cor, int(255 * a), "stroke", 7))
    cv.drawString(s, -lw / 2, 0, f, paint(cor, int(255 * a)))
    cv.restore()


def brilhos_cor(cv, x, y, t, t0, n=14, raio=190, cor=VERMELHO):
    """(cópia do cf_alongamento.brilhos com a cor como parâmetro) — o dourado é a cor do que é BOM;
    no encaixe MANCAR + FEBRE (alarme) as faíscas são vermelhas."""
    k = t - t0
    if k < 0 or k > 0.9:
        return
    for i in range(n):
        ang = i * 2 * math.pi / n + 0.3
        d = raio * e_out(k / 0.9) * (0.6 + 0.4 * ((i * 37) % 10) / 10)
        a = int(255 * (1 - k / 0.9))
        px, py = x + d * math.cos(ang), y + d * math.sin(ang) * 0.8
        s = 9 * (1 - k / 0.9) + 3
        p = skia.Path(); p.moveTo(px, py - s * 2); p.lineTo(px + s * 0.5, py - s * 0.5); p.lineTo(px + s * 2, py)
        p.lineTo(px + s * 0.5, py + s * 0.5); p.lineTo(px, py + s * 2); p.lineTo(px - s * 0.5, py + s * 0.5)
        p.lineTo(px - s * 2, py); p.lineTo(px - s * 0.5, py - s * 0.5); p.close()
        cv.drawPath(p, paint(cor, a))


# ------------------------------------------------------------------ pegada (cópia do cf_pe_virado)
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


def pegada(cv, x, y, esc, a, direita=False, vazia=False, fase=0.0):
    """Pegada de criança vista de cima, apontando para a direita (sentido da marcha), achatada pela
    perspectiva do chão. `vazia`: só o contorno tracejado (o pé que não desce) — o contorno é
    transformado ANTES de traçar, para o traço ter a mesma espessura em toda a volta."""
    if a <= 0:
        return
    m = skia.Matrix(); m.setScale(esc, -esc if direita else esc); m.postRotate(90); m.postScale(1, 0.42)
    m.postTranslate(x, y)
    if vazia:
        sola = skia.Path(SOLA); sola.transform(m)
        cv.drawPath(sola, paint("#FFFFFF", int(110 * a), "stroke", 12, blur=7))
        cv.drawPath(sola, paint("#FFFFFF", int(36 * a)))
        pt = paint("#FFFFFF", int(255 * a), "stroke", 6)
        pt.setPathEffect(skia.DashPathEffect.Make([14, 9], fase))
        cv.drawPath(sola, pt)
        for dx, dy, r in DEDOS:
            d = skia.Path(); d.addCircle(dx, dy, r); d.transform(m)
            cv.drawPath(d, paint("#FFFFFF", int(255 * a), "stroke", 3.5))
        return
    cv.save(); cv.concat(m)
    cv.drawPath(SOLA, paint(MARFIM, int(235 * a)))
    cv.drawPath(SOLA, paint(OSSO_B, int(200 * a), "stroke", 3))
    for dx, dy, r in DEDOS:
        cv.drawCircle(dx, dy, r, paint(MARFIM, int(235 * a)))
    cv.restore()


# ------------------------------------------------------------------ marcha (mundo: quadril em repouso em (HX0, HY0))
Y_CHAO = 930                       # linha da sola
GY = Y_CHAO - 30                   # tornozelo apoiado
HX0, HY0 = 540, GY - 352            # perna quase reta no apoio (contato: d ≈ 361 < L1 + L2)
L1, L2 = 182, 182                  # coxa, perna (de criança: curtas e roliças)
F_FRENTE = 80                      # onde o calcanhar toca, à frente do quadril
LIFT = 58
P_CICLO = 1.16                     # um ciclo = dois passos
SD_SAO = 0.70                      # a perna boa fica MUITO tempo no chão...
S0_MAN, SD_MAN = 0.66, 0.36        # ...a que manca, POUCO (toca em 0,66 do ciclo: ritmo longo-curto)
VEL = 2 * F_FRENTE / (SD_SAO * P_CICLO)
TAU = 0.18
LANE_SAO, LANE_MAN = Y_CHAO + 30, Y_CHAO + 68
FUNDO_CHAO = 96
PEG_VAZIA_X = HX0 + 78                # onde o pé suspenso desceria


def avanco(t, T):
    """Quanto a esteira já andou (px do mundo): constante até 'apoia', depois freia."""
    ta = T["apoia"]
    if t <= ta:
        return VEL * t
    return VEL * (ta + TAU * (1 - math.exp(-(t - ta) / TAU)))


def pe_no_ciclo(fi, s0, sd):
    """-> (x do tornozelo em relação ao quadril, altura, inclinação do pé, no chão?, fração da fase)."""
    u = (fi - s0) % 1.0
    if u < sd:
        return F_FRENTE - VEL * P_CICLO * u, 0.0, 0.0, True, u / sd
    w = (u - sd) / (1 - sd)
    xb = F_FRENTE - VEL * P_CICLO * sd
    return lerp(xb, F_FRENTE, e_inout(w)), LIFT * math.sin(math.pi * w), 22 * (1 - 2 * w) * math.sin(math.pi * w), False, w


def vaivem(t, T):
    """O 'mexer' do 'chora ao mexer': a perna suspensa balança de leve junto com a seta."""
    env = prog(t, T["chora"], T["chora"] + 0.25) * (1 - prog(t, T["juntas"] - 0.2, T["juntas"] + 0.2))
    return 14 * env * math.sin(2 * math.pi * 1.5 * (t - T["chora"]))


def pose(t, T):
    """(quadril, tornozelo da perna boa, tornozelo da que manca), cada tornozelo = (x, y, inclinação)."""
    fi = avanco(t, T) / (VEL * P_CICLO)
    xs, ys, ps, ch_s, fs = pe_no_ciclo(fi, 0.0, SD_SAO)
    xm, ym, pm, ch_m, fm = pe_no_ciclo(fi, S0_MAN, SD_MAN)
    # o quadril sobe um pouco no apoio da perna boa e CAI no apoio curto da que manca (o mancar se vê)
    dy = (-6 * math.sin(math.pi * fs) if ch_s else 0.0) + (18 * math.sin(math.pi * fm) if ch_m else 0.0)
    hip = (HX0, HY0 + dy)
    sao = (HX0 + xs, GY - ys, ps)
    man = (HX0 + xm, GY - ym, pm)
    k = e_inout(prog(t, T["apoia"] - 0.05, T["apoia"] + 0.5))         # a que manca fica no ar
    if k > 0:
        mx = vaivem(t, T)
        hip = (HX0, lerp(hip[1], HY0 - 4, k))
        sao = (lerp(sao[0], HX0 + 4, k), lerp(sao[1], GY, k), lerp(sao[2], 0.0, k))
        man = (lerp(man[0], HX0 + 52 + mx, k), lerp(man[1], GY - 88, k), lerp(man[2], 12.0, k))
    return hip, sao, man


def joelho(hx, hy, ax, ay):
    """Cinemática inversa de dois segmentos; o joelho dobra para a frente (+x)."""
    dx, dy = ax - hx, ay - hy
    d = max(1.0, min(math.hypot(dx, dy), L1 + L2 - 0.5))
    fi = math.atan2(dy, dx)
    al = math.acos(clamp((L1 * L1 + d * d - L2 * L2) / (2 * L1 * d), -1.0, 1.0))
    return hx + L1 * math.cos(fi - al), hy + L1 * math.sin(fi - al)


def tubo(x0, y0, r0, x1, y1, r1):
    L = math.hypot(x1 - x0, y1 - y0) or 1.0
    nx, ny = -(y1 - y0) / L, (x1 - x0) / L
    p = skia.Path()
    p.moveTo(x0 + nx * r0, y0 + ny * r0); p.lineTo(x1 + nx * r1, y1 + ny * r1)
    p.lineTo(x1 - nx * r1, y1 - ny * r1); p.lineTo(x0 - nx * r0, y0 - ny * r0); p.close()
    c0 = skia.Path(); c0.addCircle(x0, y0, r0)
    c1 = skia.Path(); c1.addCircle(x1, y1, r1)
    return _uniao(_uniao(p, c0), c1)


def pe_path(ax, ay, inc):
    """Pé de desenho (gordinho), saindo do tornozelo, apontando para a frente; sola em y + 30."""
    p = skia.Path()
    p.moveTo(-17, -16)
    p.cubicTo(-30, -8, -33, 22, -16, 29)
    p.cubicTo(-4, 31, 30, 31, 56, 30)
    p.cubicTo(78, 29, 82, 10, 66, 5)
    p.cubicTo(46, -1, 27, -6, 18, -16)
    p.close()
    m = skia.Matrix(); m.setScale(1.12, 1.12); m.postRotate(inc); m.postTranslate(ax, ay)
    p.transform(m)
    return p


R_QUAD, R_JOE, R_TOR = 37, 30, 20


def perna(cv, hip, ank, longe=False, aro=0.0):
    """Perna de desenho (coxa + perna + pé num contorno só), sempre opaca. Devolve o joelho."""
    hx, hy = hip; ax, ay, inc = ank
    kx, ky = joelho(hx, hy, ax, ay)
    corpo = _uniao(_uniao(tubo(hx, hy, R_QUAD, kx, ky, R_JOE), tubo(kx, ky, R_JOE, ax, ay, R_TOR)), pe_path(ax, ay, inc))
    if aro > 0:                                                   # "o corpo protegendo": brilho dourado
        cv.drawPath(corpo, paint(OURO, int(150 * aro), "stroke", 18, blur=10))
    cv.save(); cv.clipPath(corpo, skia.ClipOp.kIntersect, True)
    cv.drawPath(corpo, paint(PELE))
    for x0, y0, r0, x1, y1, r1 in ((ax, ay, R_TOR, kx, ky, R_JOE), (kx, ky, R_JOE, hx, hy, R_QUAD)):
        L = math.hypot(x1 - x0, y1 - y0) or 1.0
        nx, ny = -(y1 - y0) / L, (x1 - x0) / L
        mx, my = (x0 + x1) / 2, (y0 + y1) / 2
        r = (r0 + r1) / 2
        sh = skia.GradientShader.MakeLinear([skia.Point(mx - nx * r, my - ny * r), skia.Point(mx + nx * r, my + ny * r)],
                                            [_c(PELE_ESC), _c(PELE), _c(PELE_CL), _c(PELE), _c(PELE_ESC)],
                                            [0.0, 0.22, 0.5, 0.78, 1.0])
        cv.drawPath(tubo(x0, y0, r0, x1, y1, r1), paint(PELE, shader=sh))
    if longe:                                                     # perna de trás um tom mais escura
        cv.drawPath(corpo, paint("#3A2620", 70))
    cv.restore()
    cv.drawPath(corpo, paint(PELE_LINHA, 230, "stroke", 3.2))
    return kx, ky


def manga_short(hip, joe):
    """Barra do shorts (reta) no referencial da coxa -> (contorno, linha da bainha)."""
    hx, hy = hip; kx, ky = joe
    L = math.hypot(kx - hx, ky - hy) or 1.0
    ux, uy = (kx - hx) / L, (ky - hy) / L; nx, ny = -uy, ux
    ex, ey = hx + ux * 78, hy + uy * 78
    p = skia.Path()
    p.moveTo(hx + nx * 45, hy + ny * 45); p.lineTo(ex + nx * 42, ey + ny * 42)
    p.lineTo(ex - nx * 42, ey - ny * 42); p.lineTo(hx - nx * 45, hy - ny * 45); p.close()
    c = skia.Path(); c.addCircle(hx, hy, 45)
    bainha = ((ex + nx * 38 - ux * 10, ey + ny * 38 - uy * 10), (ex - nx * 38 - ux * 10, ey - ny * 38 - uy * 10))
    return _uniao(p, c), bainha


def path_cintura(hip):
    hx, hy = hip
    p = skia.Path()
    p.moveTo(hx - 58, hy - 86)
    p.lineTo(hx + 54, hy - 86)
    p.cubicTo(hx + 62, hy - 40, hx + 62, hy - 6, hx + 50, hy + 22)
    p.lineTo(hx - 38, hy + 26)
    p.cubicTo(hx - 70, hy + 16, hx - 76, hy - 34, hx - 58, hy - 86)
    p.close()
    return p


def pernas(cv, hip, sao, man, aro):
    """Perna boa (de trás), perna que manca (da frente) e o shorts por cima, num contorno só.
    Devolve o joelho da perna que manca."""
    ks = perna(cv, hip, sao, longe=True)
    m_s, b_s = manga_short(hip, ks)
    cv.drawPath(m_s, paint(SHORT_ESC)); cv.drawPath(m_s, paint(SHORT_LINHA, 220, "stroke", 2.6))
    cv.drawLine(b_s[0][0], b_s[0][1], b_s[1][0], b_s[1][1], paint(SHORT_LINHA, 150, "stroke", 2.6))
    km = perna(cv, hip, man, aro=aro)
    m_m, b_m = manga_short(hip, km)
    sh = _uniao(path_cintura(hip), m_m)
    cv.drawPath(sh, paint("#000000", 50, blur=8))
    cv.drawPath(sh, paint(SHORT))
    hx, hy = hip
    cv.save(); cv.clipPath(sh, skia.ClipOp.kIntersect, True)
    cv.drawRect(skia.Rect(hx - 90, hy - 90, hx + 90, hy - 62), paint(SHORT_CL))              # cós
    cv.drawLine(hx - 90, hy - 62, hx + 90, hy - 62, paint(SHORT_LINHA, 120, "stroke", 2))
    cv.restore()
    cv.drawPath(sh, paint(SHORT_LINHA, 230, "stroke", 2.8))
    cv.drawLine(b_m[0][0], b_m[0][1], b_m[1][0], b_m[1][1], paint(SHORT_LINHA, 150, "stroke", 2.6))
    return km


def batidas(T):
    """Instantes em que cada calcanhar toca o chão (só antes do 'apoia'): [(t, é_a_que_manca)]."""
    out = []
    for n in range(-8, 40):
        for fr, man in ((0.0, False), (S0_MAN, True)):
            ts = (n + fr) * P_CICLO
            if ts < T["apoia"]:
                out.append((ts, man))
    return out


def chao(cv, t, T):
    """Esteira: faixa do chão, risquinhos que correm e as pegadas (iguais no tamanho, desiguais no
    espaçamento; a da perna que manca mais clara). Some nas bordas por máscara."""
    G = avanco(t, T)
    x0, x1 = HX0 - 520, HX0 + 520
    cv.saveLayer(skia.Rect(x0 - 10, Y_CHAO - 20, x1 + 10, Y_CHAO + FUNDO_CHAO + 20), None)
    sh = skia.GradientShader.MakeLinear([skia.Point(0, Y_CHAO), skia.Point(0, Y_CHAO + FUNDO_CHAO)],
                                        [_c("#FFFFFF", 40), _c("#FFFFFF", 8)])
    cv.drawRect(skia.Rect(x0, Y_CHAO, x1, Y_CHAO + FUNDO_CHAO), paint("#FFFFFF", 255, shader=sh))
    cv.drawLine(x0, Y_CHAO, x1, Y_CHAO, paint("#CFE3F5", 170, "stroke", 3))
    passo = 64; off = G % passo
    x = x0 - off
    while x < x1:
        cv.drawLine(x, Y_CHAO + FUNDO_CHAO - 4, x + 24, Y_CHAO + FUNDO_CHAO - 4, paint("#FFFFFF", 46, "stroke", 3))
        x += passo
    apaga = lerp(1.0, 0.5, prog(t, T["apoia"] + 0.2, T["apoia"] + 0.6))   # a vazia é que tem de saltar aos olhos
    for ts, man in batidas(T):
        if ts > t:
            continue
        if man and ts > T["apoia"] - 0.5:                               # o pé que manca já não desce: nada no chão
            continue
        kr = (t - ts) / 0.4
        if kr < 1:                                                      # onda no chão a cada pisada
            rx = lerp(26, 92, e_out(kr)); xr = HX0 + F_FRENTE + 22 - (G - VEL * ts)
            cv.drawOval(skia.Rect(xr - rx, Y_CHAO - rx * 0.16, xr + rx, Y_CHAO + rx * 0.16),
                        paint("#FFFFFF" if not man else "#FF8A8D", int(150 * (1 - kr)), "stroke", 3))
        xp = HX0 + F_FRENTE + 24 - (G - VEL * ts)
        if xp < x0 - 60 or xp > x1 + 60:
            continue
        k = t - ts
        esc = 0.72 * lerp(1.3, 1.0, e_out(clamp(k / 0.18)))
        pegada(cv, xp, LANE_MAN if man else LANE_SAO, esc, clamp(k / 0.08) * (0.42 if man else 0.95) * apaga, direita=man)
    k = prog(t, T["apoia"] + 0.25, T["apoia"] + 0.55)              # o pé que não desce: pegada vazia
    if k > 0:
        pul = 0.8 + 0.2 * math.cos((t - T["apoia"]) * 4.2)             # pulsa entre 0,6 e 1,0
        pegada(cv, PEG_VAZIA_X, LANE_MAN, 1.0, k * pul * (1 - prog(t, T["manda"] - 0.4, T["manda"] - 0.1)),
               direita=True, vazia=True, fase=-t * 18)
    masc = skia.Paint(AntiAlias=True)
    masc.setShader(skia.GradientShader.MakeLinear([skia.Point(x0, 0), skia.Point(x1, 0)],
                                                  [skia.ColorSetARGB(0, 0, 0, 0), skia.ColorSetARGB(255, 0, 0, 0),
                                                   skia.ColorSetARGB(255, 0, 0, 0), skia.ColorSetARGB(0, 0, 0, 0)],
                                                  [0.0, 0.2, 0.8, 1.0]))
    masc.setBlendMode(skia.BlendMode.kDstIn)
    cv.drawRect(skia.Rect(x0 - 10, Y_CHAO - 20, x1 + 10, Y_CHAO + FUNDO_CHAO + 20), masc)
    cv.restore()


# ------------------------------------------------------------------ câmera (mundo -> tela)
def camera(t, T):
    """Perto na 1ª parte; no 'sempre' as pernas descem para o terço de baixo (centro); no 'pode'
    vão para a esquerda, abrindo lugar para a dobradiça e os rótulos da perna."""
    k1 = e_inout(prog(t, T["sempre"] - 0.05, T["sempre"] + 0.8))
    k2 = e_inout(prog(t, T["pode"] - 0.1, T["articulacao"]))
    return lerp(1.1, 0.8, k1), lerp(540, 330, k2), lerp(579, 840, k1)   # chão no mesmo lugar da tela


def aplica(cv, cam):
    s, cx, cy = cam
    cv.translate(cx, cy); cv.scale(s, s); cv.translate(-HX0, -HY0)


def na_tela(cam, x, y):
    s, cx, cy = cam
    return cx + s * (x - HX0), cy + s * (y - HY0)


# ------------------------------------------------------------------ 1ª parte: escudo, faísca, bateria
def path_escudo():
    p = skia.Path()
    p.moveTo(540, 428)
    p.cubicTo(606, 446, 662, 448, 704, 438)
    p.cubicTo(716, 590, 712, 790, 540, 1012)
    p.cubicTo(368, 790, 364, 590, 376, 438)
    p.cubicTo(418, 448, 474, 446, 540, 428)
    p.close()
    p.offset(0, HY0 - 560)                     # acompanha o quadril (desenhado para HY0 = 560)
    return p


ESCUDO = path_escudo()


def escudo(cv, t, T, a):
    k = prog(t, T["protegendo"] - 0.05, T["protegendo"] + 0.6)
    if k <= 0 or a <= 0:
        return
    pulso = 0.8 + 0.2 * math.sin((t - T["protegendo"]) * 3.2)
    cv.drawPath(ESCUDO, paint(OURO, int(26 * a * k)))
    for larg, al, bl in ((20, 110, 12), (6, 255, 0)):
        cv.drawPath(ESCUDO, _trim(paint(OURO, int(al * a * pulso), "stroke", larg, blur=bl), e_inout(k)))


def faisca(cv, x, y, r, a):
    """Faísca de dor: estrela de 4 pontas (lados côncavos), vermelha, com halo."""
    if a <= 0:
        return
    p = skia.Path()
    pts = [(x + r * math.cos(-math.pi / 2 + i * math.pi / 2), y + r * math.sin(-math.pi / 2 + i * math.pi / 2)) for i in range(4)]
    p.moveTo(*pts[0])
    for i in range(1, 5):
        p.quadTo(x, y, *pts[i % 4])
    p.close()
    cv.drawCircle(x, y, r * 0.9, paint(VERMELHO, int(90 * a), blur=18))
    cv.drawPath(p, paint(VERMELHO, int(255 * a)))
    cv.drawCircle(x, y, r * 0.16, paint("#FFE1E2", int(230 * a)))


def bateria(cv, x, y, a, t, t0):
    if a <= 0:
        return
    w, h = 118, 60
    rr = skia.RRect.MakeRectXY(skia.Rect(x - w / 2, y - h / 2, x + w / 2, y + h / 2), 13, 13)
    cv.drawRRect(rr, paint(FUNDO_CARTAO, int(210 * a)))
    cv.drawRRect(rr, paint(AZUL_CL, int(255 * a), "stroke", 5))
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(x + w / 2 + 3, y - 13, x + w / 2 + 13, y + 13), 4, 4), paint(AZUL_CL, int(255 * a)))
    sw = (w - 22 - 3 * 6) / 4
    for i in range(4):
        r = skia.RRect.MakeRectXY(skia.Rect(x - w / 2 + 11 + i * (sw + 6), y - h / 2 + 11,
                                            x - w / 2 + 11 + i * (sw + 6) + sw, y + h / 2 - 11), 4, 4)
        if i == 0:                                                 # quase vazia: o último gomo pisca devagar
            pis = 0.35 + 0.65 * (0.5 + 0.5 * math.cos(2 * math.pi * (t - t0) / 1.4))
            cv.drawRRect(r, paint("#FF6A4D", int(255 * a * pis)))
        else:
            cv.drawRRect(r, paint(AZUL_CL, int(45 * a), "stroke", 2))


# ------------------------------------------------------------------ semáforo de pressa (sem verde, de propósito)
SX0, SX1, SY0, SY1 = 846, 1016, 262, 646
SXC = (SX0 + SX1) / 2
LUZ_Y = {"verm": 333, "lar": 454, "amb": 575}
RL = 54
COR_ON = {"verm": VERMELHO, "lar": LARANJA, "amb": OURO}
COR_OFF = {"verm": "#3B1D23", "lar": "#3D2819", "amb": "#3B3319"}
PLACA_X1, PLACA_Y = 1014, 716
CAL_X, CAL_Y = 690, 760                # calendário do 'mesmo dia' (163 px)
MUNDO_RET = skia.Rect(0, 200, W, 1240)                     # camadas limitadas: o render não paga a tela inteira
SEMAFORO_RET = skia.Rect(740, 180, W, 740)
DOB_X, DOB_Y = 790, 990                # a dobradiça: no vazio à direita, longe do joelho


def luzes(t, T):
    amb = prog(t, T["sempre"] + 0.25, T["sempre"] + 0.45)
    lar = prog(t, T["apressam"], T["apressam"] + 0.2)
    v = 0.0
    if t >= T["pede"]:
        k = t - T["pede"]
        if k < 0.55:                                               # a primeira piscada
            v = math.sin(math.pi * k / 0.55)
        elif t < T["aumenta"]:
            v = (0.5 - 0.5 * math.cos(2 * math.pi * (k - 0.55) / 1.3)) ** 1.6
        else:                                                      # pisca mais rápido
            v = (0.5 - 0.5 * math.cos(2 * math.pi * (t - T["aumenta"]) / 0.42)) ** 1.3
        v = max(v, prog(t, T["mesmo"], T["mesmo"] + 0.12))         # no "mesmo dia": fixa e cheia
    return {"amb": amb, "lar": lar, "verm": v}


def semaforo(cv, t, T, dx, a):
    if a <= 0:
        return
    lz = luzes(t, T)
    cv.save(); cv.translate(dx, 0)
    cv.drawRect(skia.Rect(SXC - 8, SY1 - 4, SXC + 8, PLACA_Y - 40), paint("#41566B", int(255 * a)))   # haste
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(SXC - 16, SY0 - 18, SXC + 16, SY0 + 4), 6, 6), paint("#41566B", int(255 * a)))
    caixa = skia.RRect.MakeRectXY(skia.Rect(SX0, SY0, SX1, SY1), 34, 34)
    cv.drawRRect(caixa, paint("#000000", int(90 * a), blur=14))
    cv.drawRRect(caixa, paint("#16222D", int(255 * a)))
    cv.drawRRect(caixa, paint("#41566B", int(255 * a), "stroke", 4))
    for nome, y in LUZ_Y.items():
        i = lz[nome]
        cv.drawArc(skia.Rect(SXC - RL - 12, y - RL - 12, SXC + RL + 12, y + RL + 12), 198, 144, False,
                   paint("#0C141B", int(255 * a), "stroke", 12))
        cv.drawCircle(SXC, y, RL, paint(COR_OFF[nome], int(255 * a)))
        if i > 0.01:
            cor = COR_ON[nome]
            cv.drawCircle(SXC, y, RL + 22, paint(cor, int(120 * a * i), blur=26))
            sh = skia.GradientShader.MakeRadial(skia.Point(SXC - 15, y - 16), RL * 1.25,
                                                [_c("#FFFFFF", int(235 * a * i)), _c(cor, int(255 * a * i)), _c(cor, int(200 * a * i))],
                                                [0.0, 0.42, 1.0])
            cv.drawCircle(SXC, y, RL, paint(cor, 255, shader=sh))
        cv.drawCircle(SXC, y, RL, paint("#0C141B", int(255 * a), "stroke", 4))
    cv.restore()


def barra_pressa(cv, t, T, a0):
    a = prog(t, T["apoia"], T["apoia"] + 0.3) * a0
    if a <= 0:
        return
    nivel = lerp(0.0, 0.45, e_out(prog(t, T["apoia"], T["apoia"] + 0.6)))
    nivel = lerp(nivel, 0.72, e_out(prog(t, T["chora"], T["chora"] + 0.5)))
    nivel = lerp(nivel, 1.0, e_out(prog(t, T["aumenta"], T["aumenta"] + 0.6)))
    x0, x1, y0, y1 = 798, 828, SY0 + 10, SY1 - 6
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(x0, y0, x1, y1), 15, 15), paint("#FFFFFF", int(40 * a)))
    alt = (y1 - y0 - 8) * nivel
    if alt > 1:
        sh = skia.GradientShader.MakeLinear([skia.Point(0, y1), skia.Point(0, y0)], [_c(OURO), _c(LARANJA), _c(VERMELHO)],
                                            [0.0, 0.5, 1.0])
        cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(x0 + 4, y1 - 4 - alt, x1 - 4, y1 - 4), 11, 11),
                     paint(OURO, int(255 * a), shader=sh))
        if nivel > 0.98:
            pul = 0.6 + 0.4 * math.sin((t - T["aumenta"]) * 9)
            cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(x0 - 6, y0 - 6, x1 + 6, y1 + 6), 20, 20),
                         paint(VERMELHO, int(90 * a * pul), blur=14))


# ------------------------------------------------------------------ prancheta (repare)
PR_X0, PR_Y0, PR_X1, PR_Y1 = 60, 292, 590, 610
ITENS = (("DESDE QUANDO?", "quando", 410), ("DÓI?", "doi", 494), ("FEBRE?", "febre1", 578))
CK_TAM = 42
PRANCHETA_RET = skia.Rect(0, 236, 650, 660)                # a camada cobre só a prancheta (com a sombra)


def prancheta(cv, t, T, a0):
    ent = prog(t, T["repare"] - 0.05, T["repare"] + 0.45)
    enc = e_inout(prog(t, T["febre1"] + 0.8, T["febre1"] + 1.4))       # recolhe para o canto
    a = clamp(ent * 3) * (1 - enc) * a0
    if a <= 0:
        return
    dx = -620 * (1 - e_out(ent))
    s = lerp(1.0, 0.22, enc)
    cv.saveLayer(PRANCHETA_RET, _alfa(a)) if a < 1 else cv.save()
    cv.translate(lerp(PR_X0 + dx, 52, enc), lerp(PR_Y0, 262, enc)); cv.scale(s, s); cv.translate(-PR_X0, -PR_Y0)
    rr = skia.RRect.MakeRectXY(skia.Rect(PR_X0, PR_Y0, PR_X1, PR_Y1), 24, 24)
    cv.drawRRect(rr, paint("#000000", 90, blur=12))
    cv.drawRRect(rr, paint(FUNDO_CARTAO, 235))
    cv.drawRRect(rr, paint(MARFIM, 230, "stroke", 4))
    cm = (PR_X0 + PR_X1) / 2                                           # prendedor dourado
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(cm - 62, PR_Y0 - 22, cm + 62, PR_Y0 + 22), 11, 11), paint(OURO))
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(cm - 62, PR_Y0 - 22, cm + 62, PR_Y0 + 22), 11, 11), paint("#8A6512", 255, "stroke", 3))
    cv.drawCircle(cm, PR_Y0 - 4, 7, paint("#8A6512"))
    f = skia.Font(F_BLACK, CK_TAM)
    for s_, ch, y in ITENS:
        on = t >= T[ch]
        x = PR_X0 + 34
        caixa = skia.RRect.MakeRectXY(skia.Rect(x, y - 40, x + 48, y + 8), 10, 10)
        febre = ch == "febre1"
        cor_cx = (VERMELHO if febre else OURO) if on else "#8FA3B8"
        cv.drawRRect(caixa, paint(FUNDO_CARTAO, 255))
        cv.drawRRect(caixa, paint(cor_cx, 255, "stroke", 3.5))
        if on and not febre:
            pr = e_out(clamp((t - T[ch]) / 0.3))
            p = skia.Path(); p.moveTo(x + 10, y - 17)
            p.lineTo(x + 10 + 12 * min(1, pr * 2), y - 17 + 12 * min(1, pr * 2))
            if pr > 0.5:
                q = (pr - 0.5) * 2
                p.lineTo(x + 22 + 22 * q, y - 5 - 30 * q)
            cv.drawPath(p, paint(OURO, 255, "stroke", 6))
        if on and febre:                                               # FEBRE? acende
            k = e_back(clamp((t - T[ch]) / 0.3))
            cv.drawCircle(x + 24, y - 16, 13 * k, paint(VERMELHO, 255))
            pul = 0.5 + 0.5 * math.sin((t - T[ch]) * 8)
            lw = f.measureText(s_)
            cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(x + 62, y - 44, x + 86 + lw, y + 12), 12, 12),
                         paint(VERMELHO, int(70 * pul), blur=10))
        cor_t = ("#FF8A8D" if febre else "#FFFFFF") if on else "#FFFFFF"
        cv.drawString(s_, x + 74, y, f, paint(cor_t, 255 if on else 105))
    cv.restore()


def termometro(cv, x, y, nivel, a, esc=1.0):
    """(cópia do cf_osteomielite) bulbo e coluna vermelha, SEM número."""
    if a <= 0:
        return
    cv.save(); cv.translate(x, y); cv.scale(esc, esc)
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(-14, -50, 14, 26), 14, 14), paint("#000000", int(70 * a), blur=6))
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(-12, -48, 12, 24), 12, 12), paint("#EEF3F8", int(255 * a)))
    cv.drawCircle(0, 32, 19, paint("#EEF3F8", int(255 * a)))
    cv.drawCircle(0, 32, 13, paint(VERMELHO, int(255 * a)))
    h = lerp(6, 64, clamp(nivel))
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(-5, 26 - h, 5, 32), 5, 5), paint(VERMELHO, int(255 * a)))
    for k in range(4):
        cv.drawLine(5, -30 + k * 14, 11, -30 + k * 14, paint("#8FA3B8", int(220 * a), "stroke", 2))
    cv.restore()


GUARDA = (84, 318)                                                     # o canto onde o termômetro espera


def termo_estado(t, T, cam):
    """-> (x, y, escala, alfa, nível). Nasce ao lado de FEBRE?, vai para o canto, voa até a perna."""
    t0 = T["febre1"] + 0.05
    if t < t0:
        return None
    f = skia.Font(F_BLACK, CK_TAM)
    p0 = (PR_X0 + 34 + 74 + f.measureText("FEBRE?") + 46, ITENS[2][2] - 18)
    k1 = e_inout(prog(t, T["febre1"] + 0.8, T["febre1"] + 1.4))
    x, y = lerp(p0[0], GUARDA[0], k1), lerp(p0[1], GUARDA[1], k1)
    esc = lerp(0.82, 0.78, k1) * lerp(0.4, 1.0, e_back(prog(t, t0, t0 + 0.35)))
    k2 = e_inout(prog(t, T["febre2"], T["febre2"] + 0.65))
    if k2 > 0:                                  # desce pela borda esquerda (não cruza as fichas) até a perna
        dst = na_tela(cam, HX0 - 170, HY0 + 120)
        cx_, cy_ = 36, 820
        x = (1 - k2) ** 2 * x + 2 * k2 * (1 - k2) * cx_ + k2 ** 2 * dst[0]
        y = (1 - k2) ** 2 * y + 2 * k2 * (1 - k2) * cy_ + k2 ** 2 * dst[1]
        esc = lerp(esc, 1.3, k2)                   # grande o bastante para ler "febre" no celular
    if k1 >= 1 and t < T["febre2"]:                                     # guardado: pulsa de leve
        esc *= 1 + 0.06 * math.sin((t - T["febre1"]) * 5)
    nivel = lerp(0.15, 0.85, e_out(prog(t, t0, t0 + 0.9)))
    return x, y, esc, 1.0, nivel


# ------------------------------------------------------------------ etiquetas penduradas no semáforo
ETQ = (("melhora", "NÃO MELHORA", 374), ("noite", "DOR QUE ACORDA À NOITE", 460), ("inchaco", "INCHAÇO", 546))
ETQ_X1, ETQ_TAM = 786, 38


def lua(cv, x, y, r, a, cor=MARFIM):
    if a <= 0:
        return
    p = skia.Path(); p.addCircle(x, y, r)
    q = skia.Path(); q.addCircle(x + r * 0.48, y - r * 0.26, r * 0.86)
    c = skia.Op(p, q, skia.PathOp.kDifference_PathOp) or p
    cv.drawPath(c, paint(cor, int(110 * a), blur=12))
    cv.drawPath(c, paint(cor, int(255 * a)))


def etiquetas(cv, t, T, a0):
    rec = prog(t, T["mancar3"] - 0.05, T["mancar3"] + 0.4)              # recolhem para dentro da luz laranja
    if rec >= 1 or a0 <= 0:
        return
    jun = e_inout(prog(t, T["apressam"], T["apressam"] + 0.45))          # agrupam junto da luz laranja
    lx, ly = SXC, LUZ_Y["lar"]
    f = skia.Font(F_BLACK, ETQ_TAM)
    for i, (ch, s, y) in enumerate(ETQ):
        k = prog(t, T[ch] - 0.02, T[ch] + 0.3)
        if k <= 0:
            continue
        esc = lerp(1.0, 0.8, jun)                                        # 38 px x 0,8 = 30 px: ainda legível
        x1 = lerp(ETQ_X1, SX0 - 16, jun)
        yy = lerp(y, LUZ_Y["lar"] - 50 + i * 54, jun)
        if rec > 0:
            r = e_inout(rec)
            x1, yy = lerp(x1, lx + 40, r), lerp(yy, ly + 20, r)
            esc *= 1 - r
        a = clamp(k * 2) * a0 * (1 - rec) ** 2
        balanco = 9 * math.exp(-4 * (t - T[ch])) * math.sin((t - T[ch]) * 13) if t >= T[ch] else 0.0
        # cordão até a caixa do semáforo
        if esc > 0.05:
            cv.drawLine(x1 - 4, yy - 26 * esc, SX0 + 2, yy - 26 * esc - 10, paint("#8FA3B8", int(220 * a), "stroke", 2.5))
        cv.save(); cv.translate(x1, yy - 26 * esc); cv.rotate(balanco); cv.scale(esc, esc); cv.translate(0, 26)
        lw = f.measureText(s)
        x0 = -(lw + 16 + 58 + 10 + 24)
        rr = skia.RRect.MakeRectXY(skia.Rect(x0, -44, 0, 18), 14, 14)
        cv.drawRRect(rr, paint(FUNDO_CARTAO, int(235 * a)))
        cv.drawRRect(rr, paint(LARANJA, int(255 * a), "stroke", 3))
        cv.drawCircle(-12, -26, 5, paint(LARANJA, int(255 * a)))         # furo da etiqueta
        ix, iy = x0 + 16 + 29, -13
        if ch == "melhora":                                              # calendário sem número, folhas virando
            cv.save(); cv.translate(ix - 24, iy - 23); cv.scale(0.5, 0.5)
            calendario(cv, 0, 0, t, T[ch], a)
            cv.restore()
        elif ch == "noite":
            lua(cv, ix, iy, 20, a)
        else:                                                            # inchaço: círculo que infla devagar
            r = lerp(7, 21, e_inout(prog(t, T[ch], T[ch] + 1.4))) * (1 + 0.05 * math.sin(t * 4))
            cv.drawCircle(ix, iy, r, paint(INCHA, int(140 * a)))
            cv.drawCircle(ix, iy, r, paint(INCHA, int(255 * a), "stroke", 3))
        cv.drawString(s, x0 + 16 + 58 + 10, 0, f, paint("#FFFFFF", int(255 * a)))
        cv.restore()


# ------------------------------------------------------------------ fichas MANCAR + FEBRE (quebra-cabeça)
FY0, FY1 = 404, 506
FYM = (FY0 + FY1) / 2
FXA, FXJ, FXB = 108, 380, 606
F_TAM = 46


def _peca_mancar():
    p = skia.Path(); p.addRRect(skia.RRect.MakeRectXY(skia.Rect(FXA, FY0, FXJ, FY1), 12, 12))
    c = skia.Path(); c.addCircle(FXJ + 12, FYM, 20)
    return _uniao(p, c)


def _peca_febre():
    p = skia.Path(); p.addRRect(skia.RRect.MakeRectXY(skia.Rect(FXJ + 3, FY0, FXB, FY1), 12, 12))
    c = skia.Path(); c.addCircle(FXJ + 12, FYM, 23)
    return skia.Op(p, c, skia.PathOp.kDifference_PathOp) or p


PECA_M, PECA_F = _peca_mancar(), _peca_febre()
CM = ((FXA + FXJ) / 2, FYM)
CF = ((FXJ + 35 + FXB) / 2, FYM)


def fichas(cv, t, T, cam, a0):
    km = prog(t, T["mancar3"], T["mancar3"] + 0.5)
    if km <= 0 or a0 <= 0:
        return
    t_lock = T["febre2"] + 0.3
    verm = prog(t, T["juntas"], T["juntas"] + 0.3)
    borda = VERMELHO if verm > 0.5 else "#E6EEF6"
    trem = 0.0
    if 0 <= t - t_lock < 0.3:
        trem = 5 * math.sin((t - t_lock) * 60) * (1 - (t - t_lock) / 0.3)
    f = skia.Font(F_BLACK, F_TAM)
    for peca, cen, s, t0, src in ((PECA_M, CM, "MANCAR", T["mancar3"], na_tela(cam, HX0 + 20, HY0 + 200)),
                                  (PECA_F, CF, "FEBRE", T["febre2"], GUARDA)):
        k = prog(t, t0, t0 + (0.5 if s == "MANCAR" else 0.3))
        if k <= 0:
            continue
        e = e_out(k)
        x, y = lerp(src[0], cen[0], e) + trem, lerp(src[1], cen[1], e)
        if s == "FEBRE":                       # chega por cima e desce no encaixe (não passa sobre a MANCAR)
            x = lerp(src[0], cen[0], e_out(clamp(k / 0.7))) + trem
            y = lerp(src[1], cen[1], e_inout(k)) - 110 * math.sin(math.pi * k)
        esc = lerp(0.25, 1.0, e_back(k) if s == "MANCAR" else e)
        a = clamp(k * 3) * a0
        cv.save(); cv.translate(x, y); cv.scale(esc, esc); cv.translate(-cen[0], -cen[1])
        cv.drawPath(peca, paint("#000000", int(90 * a), blur=10))
        if verm > 0:
            cv.drawPath(peca, paint(VERMELHO, int(110 * a * verm), "stroke", 16, blur=10))
        cv.drawPath(peca, paint(FUNDO_CARTAO, int(240 * a)))
        cv.drawPath(peca, paint(borda, int(255 * a), "stroke", lerp(3.5, 5.5, verm)))
        lw = f.measureText(s)
        cv.drawString(s, cen[0] - lw / 2 + (4 if s == "FEBRE" else -6), FYM + F_TAM * 0.36, f, paint("#FFFFFF", int(255 * a)))
        cv.restore()
    brilhos_cor(cv, FXJ + 12, FYM, t, t_lock, n=10, raio=120, cor="#FF8A8D")


# ------------------------------------------------------------------ articulação: dobradiça esquemática
def dobradica(cv, x, y, a, t, t0, esc0=1.55):
    """Articulação ESQUEMÁTICA (sem indicar qual): um bastão fixo na horizontal e outro que dobra e
    volta 40° em torno do pino, dentro de um anel vermelho que pulsa. Fica longe da perna."""
    if a <= 0:
        return
    esc = esc0 * lerp(0.5, 1.0, e_back(prog(t, t0, t0 + 0.4)))
    dobra = 320 - 20 * math.cos(2 * math.pi * (t - t0) / 1.2)          # 300° <-> 340°, ida e volta em 1,2 s
    cv.save(); cv.translate(x, y); cv.scale(esc, esc)
    pul = 0.5 + 0.5 * math.sin((t - t0) * 7)
    r = 64 + 6 * pul
    cv.drawCircle(0, 0, r, paint(FUNDO_CARTAO, int(150 * a)))
    cv.drawCircle(0, 0, r, paint(VERMELHO, int(110 * a * (0.5 + 0.5 * pul)), "stroke", 16, blur=10))
    cv.drawCircle(0, 0, r, paint(VERMELHO, int(255 * a), "stroke", 6))
    for ang in (180, dobra):
        cv.save(); cv.rotate(ang)
        rr = skia.RRect.MakeRectXY(skia.Rect(-4, -11, 52, 11), 11, 11)
        cv.drawRRect(rr, paint(ACO, int(255 * a)))
        cv.drawRRect(rr, paint(ACO_ESC, int(255 * a), "stroke", 3))
        cv.restore()
    cv.drawCircle(0, 0, 13, paint(ACO_ESC, int(255 * a)))
    cv.drawCircle(-3, -3, 4.5, paint(ACO_HL, int(220 * a)))
    cv.restore()


SETA_RECUO, SETA_A0, SETA_A1 = 60, -112, -52                    # raio e arco da seta de vaivém


def seta_vaivem(cv, kx, ky, ax, ay, t, T, a):
    """Seta curva de vaivém (duas pontas) em volta da perna suspensa, presa ao joelho (mundo)."""
    if a <= 0:
        return
    R = math.hypot(ax - kx, ay - ky) - SETA_RECUO                   # à frente da canela, sem tocar o pé
    base = math.degrees(math.atan2(ay - ky, ax - kx))
    osc = 8 * math.sin(2 * math.pi * 1.5 * (t - T["chora"]))
    a0, a1 = base + SETA_A0 + osc, base + SETA_A1 + osc
    n = 20
    pts = [(kx + R * math.cos(math.radians(lerp(a0, a1, i / n))), ky + R * math.sin(math.radians(lerp(a0, a1, i / n))))
           for i in range(n + 1)]
    p = skia.Path(); p.moveTo(*pts[0])
    for q in pts[1:]:
        p.lineTo(*q)
    cor = "#FF8A8D"
    cv.drawPath(p, paint(cor, int(90 * a), "stroke", 22, blur=6))
    cv.drawPath(p, paint(cor, int(255 * a), "stroke", 11))
    for (x0, y0), (x1, y1) in ((pts[-2], pts[-1]), (pts[1], pts[0])):
        ponta(cv, x1, y1, math.atan2(y1 - y0, x1 - x0), 38, cor, a)


# ------------------------------------------------------------------ calendário que PARA (no mesmo dia)
CAL_V = 5.0                                                             # folhas por segundo (como o calendario())


def freio_cal(t_in, t_para):
    """-> (fase em que começa a frear, duração do freio). O freio desacelera até uma folha INTEIRA."""
    fm = CAL_V * (t_para - t_in)
    r = math.ceil(fm) - fm
    if r < 0.75:
        r += 1.0
    return fm, 2 * r / CAL_V


def fase_cal(t, t_in, t_para):
    """-> (fase das folhas, parado?). Vira a 5 folhas/s de `t_in` a `t_para`; aí freia e PARA."""
    fm, d = freio_cal(t_in, t_para)
    if t < t_para:
        return CAL_V * (t - t_in), False
    u = min(t - t_para, d)
    return fm + CAL_V * u - CAL_V * u * u / (2 * d), t >= t_para + d


def calendario_parado(cv, x, y, t, t_in, t_para, a, esc=1.5):
    """Folha sem número; vira sem parar desde o 'procure' (o tempo passando), freia no 'mesmo' e
    PARA; um círculo vermelho é desenhado à mão na folha parada."""
    if a <= 0:
        return
    ent = lerp(0.6, 1.0, e_back(prog(t, t_in, t_in + 0.3)))
    cv.save(); cv.translate(x + 48 * esc, y + 46 * esc); cv.scale(esc * ent, esc * ent); cv.translate(-48, -46)
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(3, 5, 99, 97), 12, 12), paint("#000000", int(80 * a), blur=8))
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(0, 0, 96, 92), 12, 12), paint("#EEF3F8", int(255 * a)))
    cv.drawRect(skia.Rect(0, 0, 96, 24), paint(VERMELHO, int(255 * a)))
    for xx in (24, 72):
        cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(xx - 4, -8, xx + 4, 10), 3, 3), paint("#5E7186", int(255 * a)))
    for i in range(3):
        cv.drawLine(14, 42 + i * 16, 82, 42 + i * 16, paint("#9AA8B5", int(200 * a), "stroke", 4))
    fase, parado = fase_cal(t, t_in, t_para)
    if not parado:                                                      # a folha de cima virando
        f = fase - math.floor(fase)
        cv.save(); cv.translate(0, 24); cv.scale(1, 1 - f)
        cv.drawRect(skia.Rect(0, 0, 96, 68), paint("#FFFFFF", int(170 * a * (1 - f))))
        cv.restore()
    _, d = freio_cal(t_in, t_para)
    kc = prog(t, t_para + d + 0.05, t_para + d + 0.55)
    if kc > 0:                                                          # círculo "à mão" (traço irregular)
        p = skia.Path(); n = 40
        for i in range(n + 1):
            u = i / n
            ang = -2.2 + u * 2 * math.pi * 1.08
            rr = 1 + 0.06 * math.sin(u * 11) + 0.05 * u
            px, py = 48 + 46 * rr * math.cos(ang), 58 + 30 * rr * math.sin(ang)
            (p.moveTo if i == 0 else p.lineTo)(px, py)
        cv.drawPath(p, _trim(paint(VERMELHO, int(255 * a), "stroke", 5.5), e_out(kc)))
    cv.restore()


def viradas_cal(t_in, t_para):
    """Instantes em que uma folha nova começa a virar (para o 'tick') e o instante em que PARA."""
    fm, d = freio_cal(t_in, t_para)
    fim = fm + CAL_V * d / 2                                           # fase final (folha inteira)
    out, u, ult = [], 0.0, 0
    while True:
        tt = t_in + u
        f = fase_cal(tt, t_in, t_para)[0]
        if f >= fim - 1e-6 or tt > t_para + d:
            break
        if math.floor(f) > ult:
            out.append(tt); ult = math.floor(f)
        u += 0.005
    return out, t_para + d


# ------------------------------------------------------------------ quadro
def quadro(cv, t, T, blocos, ep):
    fundo(cv, t)
    noite = prog(t, T["noite"] - 0.05, T["noite"] + 0.3) * (1 - prog(t, T["apressam"], T["apressam"] + 0.45))
    if noite > 0:                                                       # dor que acorda à noite: o fundo escurece
        cv.drawRect(skia.Rect(0, 0, W, H), paint("#03070C", int(135 * noite)))
    fim = 1 - prog(t, T["manda"] - 0.45, T["manda"] - 0.1)              # a CTA fica limpa (só o semáforo)
    w1 = 1 - prog(t, T["sempre"] - 0.05, T["sempre"] + 0.35)            # 1ª parte (escudo, faísca, bateria)
    cam = camera(t, T)
    hip, sao, man = pose(t, T)

    # ---------------- mundo: esteira e pernas (câmera)
    if fim > 0:
        cv.saveLayer(MUNDO_RET, _alfa(fim)) if fim < 1 else cv.save()
        aplica(cv, cam)
        escudo(cv, t, T, w1)
        chao(cv, t, T)
        cv.drawOval(skia.Rect(HX0 - 150, Y_CHAO - 10, HX0 + 170, Y_CHAO + 18), paint("#000000", 70, blur=10))
        aro = prog(t, T["protegendo"], T["protegendo"] + 0.4) * w1 * (0.7 + 0.3 * math.sin(t * 3.2))
        kx, ky = pernas(cv, hip, sao, man, aro)
        # faísca (foge de uma dor) e bateria (compensa uma fraqueza): possibilidades, uma OU outra
        a_f = prog(t, T["foge"] - 0.03, T["foge"] + 0.12) * w1
        if a_f > 0:
            dim = lerp(1.0, 0.38, prog(t, T["fraqueza"], T["fraqueza"] + 0.35))
            pis = 0.72 + 0.28 * math.cos((t - T["foge"]) * 15) if t < T["foge"] + 1.0 else 1.0
            r = 48 * lerp(0.4, 1.0, e_back(prog(t, T["foge"], T["foge"] + 0.3))) * (0.92 + 0.08 * pis)
            faisca(cv, 792, 720 + 8 * math.sin(t * 2.3), r, a_f * pis * dim)
        a_b = prog(t, T["fraqueza"] - 0.03, T["fraqueza"] + 0.15) * w1
        if a_b > 0:
            esc = 1.15 * lerp(0.5, 1.0, e_back(prog(t, T["fraqueza"], T["fraqueza"] + 0.35)))
            cv.save(); cv.translate(284, 722 + 6 * math.sin(t * 1.9 + 1)); cv.scale(esc, esc)
            bateria(cv, 0, 0, a_b, t, T["fraqueza"])
            cv.restore()
        a_s = prog(t, T["chora"] - 0.05, T["chora"] + 0.25) * (1 - prog(t, T["juntas"] - 0.1, T["juntas"] + 0.25))
        seta_vaivem(cv, kx, ky, man[0], man[1], t, T, a_s)
        cv.restore()

    # ---------------- 1ª parte: rótulos
    chip(cv, "CLAUDICAÇÃO", 540, 1150, OURO,
         prog(t, T["mancar1"], T["mancar1"] + 0.25) * (1 - prog(t, T["foge"] - 0.12, T["foge"] + 0.1)))
    chip(cv, "O CORPO PROTEGENDO ALGO", 540, 322, OURO, prog(t, T["protegendo"], T["protegendo"] + 0.3) * w1, tam=42)
    chip(cv, "FOGE DE UMA DOR", 540, 1150, VERMELHO, prog(t, T["foge"], T["foge"] + 0.25) * w1,
         dim=lerp(1.0, 0.55, prog(t, T["fraqueza"], T["fraqueza"] + 0.35)))
    chip(cv, "COMPENSA UMA FRAQUEZA", 540, 1216, AZUL_CL, prog(t, T["fraqueza"], T["fraqueza"] + 0.25) * w1, tam=38)

    # ---------------- semáforo de pressa + barra (desfocado ao fundo na CTA)
    ent = e_out(prog(t, T["sempre"], T["sempre"] + 0.6))
    if ent > 0:
        desf = 9 * prog(t, T["manda"] - 0.3, T["manda"] + 0.3)
        if desf > 0.3:
            pb = skia.Paint(); pb.setImageFilter(skia.ImageFilters.Blur(desf, desf))
            cv.saveLayer(SEMAFORO_RET, pb)                              # camada só do semáforo (render leve)
        semaforo(cv, t, T, 440 * (1 - ent), 1.0)
        barra_pressa(cv, t, T, fim)
        if desf > 0.3:
            cv.restore()

    # ---------------- checklist, etiquetas, lua
    prancheta(cv, t, T, fim)
    etiquetas(cv, t, T, fim)
    lua(cv, 996, 212, 28, prog(t, T["noite"], T["noite"] + 0.3) * (1 - prog(t, T["apressam"], T["apressam"] + 0.4)))

    # ---------------- placas do semáforo (à direita, debaixo dele)
    placa(cv, "SEMPRE SE AVALIA", PLACA_X1, PLACA_Y, OURO,
          prog(t, T["sempre"] + 0.6, T["sempre"] + 0.85) * (1 - prog(t, T["mancar2"] - 0.1, T["mancar2"] + 0.2)))
    placa(cv, "APRESSAM A CONSULTA", PLACA_X1, PLACA_Y, LARANJA,
          prog(t, T["apressam"], T["apressam"] + 0.25) * (1 - prog(t, T["mancar3"] - 0.1, T["mancar3"] + 0.2)))
    placa(cv, "PODE SER INFECÇÃO NA ARTICULAÇÃO", PLACA_X1, PLACA_Y, VERMELHO,
          prog(t, T["pode"], T["pode"] + 0.25) * (1 - prog(t, T["apoia"] + 0.2, T["apoia"] + 0.5)))
    placa(cv, "A PRESSA AUMENTA", PLACA_X1, PLACA_Y, VERMELHO,
          prog(t, T["aumenta"], T["aumenta"] + 0.25) * (1 - prog(t, T["juntas"] - 0.1, T["juntas"] + 0.2)))

    # ---------------- fichas, termômetro, dobradiça, rótulos da perna
    fichas(cv, t, T, cam, fim)
    chip(cv, "FEBRE E MANQUEIRA JUNTAS", 386, 596, "#FFFFFF", prog(t, T["juntas"], T["juntas"] + 0.3) * fim, tam=38,
         borda=VERMELHO)
    te = termo_estado(t, T, cam)
    if te:
        x, y, esc, a, nivel = te
        termometro(cv, x, y, nivel, a * fim, esc)
    dobradica(cv, DOB_X, DOB_Y, prog(t, T["articulacao"] - 0.05, T["articulacao"] + 0.2) *
              (1 - prog(t, T["apoia"] - 0.05, T["apoia"] + 0.35)), t, T["articulacao"])
    placa(cv, "NÃO APOIA A PERNA", PLACA_X1, 850, "#FF8A8D",
          prog(t, T["apoia"] + 0.1, T["apoia"] + 0.35) * (1 - prog(t, T["juntas"] - 0.1, T["juntas"] + 0.2)), tam=38)
    placa(cv, "CHORA AO MEXER", PLACA_X1, 934, "#FF8A8D",
          prog(t, T["chora"], T["chora"] + 0.25) * (1 - prog(t, T["juntas"] - 0.1, T["juntas"] + 0.2)), tam=38)

    # ---------------- no mesmo dia: calendário que para + carimbo
    a_cal = prog(t, T["procure"], T["procure"] + 0.2) * fim
    calendario_parado(cv, CAL_X, CAL_Y, t, T["procure"], T["mesmo"], a_cal, esc=1.7)
    carimbo_cor(cv, "NO MESMO DIA", 775, 1034, -5, T["mesmo"], t, dur=T["manda"] - T["mesmo"] - 0.1, tam=52)

    # ---------------- carimbos
    carimbo_ouro(cv, "NÃO É MANHA", 540, 742, -8, T["manha"], t, dur=T["protegendo"] - T["manha"] + 0.25)
    carimbo_cor(cv, "PEDE PRESSA", 360, 610, -6, T["pede"] + 0.08, t, dur=1.8, tam=58)

    capa(cv, t, T["manha"] + 0.2, ep["gancho"][0], ep["gancho"][1])
    selo_como_funciona(cv, prog(t, T["manha"] + 0.55, T["manha"] + 0.95) * (1 - prog(t, T["manda"] - 0.3, T["manda"])))
    interface(cv, t, T, blocos, DESTAQUE)


def sons(T):
    ev = []
    for n in range(0, 12):                                  # passos: o ouvido pega o ritmo curto-longo
        for fr, g in ((0.0, 0.42), (S0_MAN, 0.24)):
            ts = (n + fr) * P_CICLO
            if 0.05 < ts < T["sempre"] - 0.1:
                ev.append((ts, "click", g))
    ev += [(T["manha"], "thump", 0.85), (T["protegendo"], "shimmer", 0.6), (T["foge"], "pop", 0.55),
           (T["fraqueza"], "ping", 0.4), (T["sempre"], "whoosh", 0.55), (T["sempre"] + 0.27, "ding", 0.45),
           (T["repare"], "whoosh", 0.3), (T["quando"], "click", 0.75), (T["doi"], "click", 0.75),
           (T["febre1"], "pop", 0.6), (T["febre1"] + 0.8, "whoosh", 0.25)]
    ev += [(T["melhora"] + 0.2 * i, "tick", 0.22) for i in range(5)]           # folhinhas virando
    ev += [(T["noite"], "whoosh", 0.3), (T["noite"] + 0.08, "shimmer", 0.4), (T["inchaco"], "pop", 0.45),
           (T["apressam"], "ding", 0.55), (T["mancar3"], "whoosh", 0.4), (T["mancar3"] + 0.35, "pop", 0.4),
           (T["febre2"], "whoosh", 0.4), (T["febre2"] + 0.3, "click", 1.0), (T["febre2"] + 0.31, "ping", 0.5),
           (T["pede"] + 0.08, "thump", 0.85), (T["articulacao"], "pop", 0.5), (T["apoia"], "whoosh", 0.35),
           (T["chora"], "tick", 0.4), (T["chora"] + 0.33, "tick", 0.3), (T["aumenta"], "shimmer", 0.45),
           (T["aumenta"] + 0.55, "ping", 0.45), (T["juntas"], "thump", 0.55)]
    viradas, parou = viradas_cal(T["procure"], T["mesmo"])
    ev += [(T["procure"], "whoosh", 0.3)] + [(tv, "tick", 0.22) for tv in viradas]   # folhas virando
    ev += [(T["mesmo"], "thump", 0.9), (T["mesmo"] + 0.05, "ding", 0.55), (parou, "tick", 0.45),
           (parou + 0.05, "click", 0.5), (T["manda"] + 0.05, "whoosh", 0.5)]
    return ev


def tempos_previa(T):
    return (0.0, T["manha"] + 0.45, T["fraqueza"] + 0.6, T["sempre"] + 1.0, T["febre1"] + 0.5, T["inchaco"] + 0.3,
            T["pede"] + 0.45, T["articulacao"] + 0.6, T["aumenta"] + 0.5, T["procure"] + 0.5, T["mesmo"] + 1.3,
            T["manda"] + 1.0)


# respiro antes da CTA: o quadro final (semáforo vermelho fixo, calendário parado, NO MESMO DIA) fica ~2 s.
render = fazer_render(quadro, ANCORAS, sons, tempos_previa, respiro_cta=2.0)
