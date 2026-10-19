# -*- coding: utf-8 -*-
"""COMO FUNCIONA — Sever e Osgood-Schlatter ("JOELHO E CALCANHAR / DOENDO NO ESPORTE?").

Mesmo estilo das cenas aprovadas (fundo azul-petróleo, marfim, dourado, rótulos, brilhos, checklist,
cartão de atenção, legenda karaokê, CTA com aviãozinho). Storyboard e correções do verificador
(lote4_cf/cf_osgood_sever_storyboard.json) respeitados aqui:
  * Pernas de DESENHO, de lado, pele lisa e OPACA: nenhum osso, nada translúcido, nenhum tendão,
    nenhuma estrutura interna. A dor é só um brilho vermelho-suave (sem chama, sem sangue).
  * "treina": bola e tênis em contorno flutuam AO LADO, sem encostar no pé (nada de impacto).
  * O balão de lupa é SOLTO (sem seta, sem linha de chamada, sem cabo): dentro, um bloco de osso
    marfim genérico e arredondado (não é o desenho do calcâneo). "crescimento": o contorno do bloco
    INTEIRO vira tracejado dourado e setinhas sobem por dentro (sem faixa em posição específica).
    "inflama": halo vermelho-suave no bloco, pulsando no MESMO ritmo do brilho do calcanhar.
  * Os nomes ("DOENÇA DE SEVER", "OSGOOD-SCHLATTER") entram sóbrios, sem carimbo nem tremor.
  * "estirão": régua SEM números (a do cf_placa_crescimento) com a seta dourada subindo.
  * "equilibrar": balança TREINO / DESCANSO que oscila e assenta NIVELADA (nenhum prato some).
  * "coxa" / "panturrilha": só uma seta dourada de duas pontas que se estica (nada de músculo).
  * "melhorar": as bolsas de gelo saem e os brilhos ficam mais FRACOS, sem sumir; nenhum rótulo,
    nenhum dourado, nenhum check (a fonte diz "tende a melhorar").
  * Cartão de atenção amarelo, sóbrio (sem vermelho de urgência): avaliação, não pronto-socorro.
A cena é PRESA ao roteiro pelas palavras-âncora (ANCORAS): mudar o roteiro sem elas quebra o render
de propósito (KeyError), em vez de sair vídeo dessincronizado. Todo texto desenhado está em
ep["tela"] (o render recusa o vídeo se não estiver).
"""
import math

import skia

from .cf_alongamento import (F_BLACK, OSSO_B, OSSO_C, OSSO_L, OURO, PELE, C, brilhos, clamp, e_back,
                             e_in_back, e_inout, e_out, fundo, lerp, paint, prog, rotulo, texto)
from .cf_comum import capa, fazer_render, interface, selo_como_funciona

# ------------------------------------------------------------------ sincronia com a fala
ANCORAS = {
    "calcanhar": ("calcanhar", 1, False), "treina": ("treina", 1, False), "sever": ("sever", 1, False),
    "osso": ("osso", 1, False), "crescimento": ("crescimento", 1, False), "inflama": ("inflama", 1, False),
    "dor2": ("dor", 2, False), "joelho": ("joelho", 1, False), "estirao": ("estirão", 1, False),
    "osgood": ("osgood-schlatter", 1, False), "ajuda": ("ajuda", 1, False),
    "equilibrar": ("equilibrar", 1, False), "descanso": ("descanso", 1, False), "gelo": ("gelo", 1, False),
    "alongar": ("alongar", 1, False), "coxa": ("coxa", 1, False), "panturrilha": ("panturrilha", 1, False),
    "com": ("com", 1, False), "melhorar": ("melhorar", 1, False), "persiste": ("persiste", 1, False),
    "limita": ("limita", 1, False), "trava": ("trava", 1, False), "avaliar": ("avaliar", 1, False),
    "manda": ("manda", 1, False),
}
DESTAQUE = {"calcanhar", "sever", "crescimento", "inflama", "joelho", "estirão", "osgood-schlatter",
            "equilibrar", "descanso", "gelo", "alongar", "coxa", "panturrilha", "persiste", "esporte",
            "trava", "avaliar"}

# ------------------------------------------------------------------ textos de tela (todos em ep["tela"])
CALCANHAR = "CALCANHAR"
SEVER = "DOENÇA DE SEVER"
AREA = "ÁREA DE CRESCIMENTO"
INFLAM = "INFLAMAÇÃO"
ABAIXO = "ABAIXO DO JOELHO"
ESTIRAO = "ESTIRÃO"
OSGOOD = "OSGOOD-SCHLATTER"
AJUDA = "O QUE AJUDA"
ITENS = ("EQUILIBRAR", "GELO APÓS A ATIVIDADE", "ALONGAR")
TREINO, DESCANSO = "TREINO", "DESCANSO"
COXA, PANTU = "COXA", "PANTURRILHA"
ALERTAS = ("SE A DOR PERSISTE", "LIMITA O ESPORTE", "TRAVA O JOELHO")
AVALIAR, ORTOPED = "VALE AVALIAR", "ORTOPEDIA PEDIÁTRICA"

# ------------------------------------------------------------------ paleta própria
FUNDO_CARTAO = "#0B1824"
AZUL = "#9CC9FF"
PELE_CL, PELE_ESC, PELE_LINHA = "#F7CDB8", "#DA987E", "#B9765E"
SHORT, SHORT_CL, SHORT_ESC = "#4C86C6", "#6FA3DA", "#3A6FA8"
DOR, DOR_TXT = "#FF5A5F", "#FFA3A6"                 # brilho vermelho-suave e o texto dos rótulos de dor
GELO, GELO_MED, GELO_ESC = "#DDF3FF", "#A6DBF7", "#4F97C4"
AMARELO, AMARELO_ESC = "#FFD166", "#8A6A12"
LENTE_IN, LENTE_OUT = "#2B5C7A", "#183B52"          # interior do balão: azul claro, NÃO preto


def _p(cor, a=255, estilo="fill", w=0, blur=0, junta=False, traco=None, fase=0.0):
    p = paint(cor, a, estilo, w, blur)
    if junta:
        p.setStrokeJoin(skia.Paint.kRound_Join)
    if traco:
        p.setPathEffect(skia.DashPathEffect.Make(list(traco), fase))
    return p


def _alfa(a):
    p = skia.Paint()
    p.setAlphaf(clamp(a))
    return p


# ------------------------------------------------------------------ utilidades (copiadas do cf_pe_virado)
def ponta(cv, x, y, ang, tam, cor, a):
    """Cabeça de seta em (x, y) apontando para `ang` (radianos)."""
    p = skia.Path()
    p.moveTo(x + tam * math.cos(ang), y + tam * math.sin(ang))
    p.lineTo(x + tam * 0.75 * math.cos(ang + 2.45), y + tam * 0.75 * math.sin(ang + 2.45))
    p.lineTo(x + tam * 0.75 * math.cos(ang - 2.45), y + tam * 0.75 * math.sin(ang - 2.45))
    p.close()
    cv.drawPath(p, paint(cor, int(255 * a)))


def chip(cv, s, x, y, cor, a, tam=40, borda=None):
    """Rótulo solto (sem ponteiro), centrado em x; y = linha de base do texto."""
    if a <= 0:
        return
    f = skia.Font(F_BLACK, tam); lw = f.measureText(s)
    rr = skia.RRect.MakeRectXY(skia.Rect(x - lw / 2 - 24, y - tam * 1.05, x + lw / 2 + 24, y + tam * 0.34), 16, 16)
    cv.drawRRect(rr, paint(FUNDO_CARTAO, int(225 * a)))
    cv.drawRRect(rr, paint(borda or cor, int(255 * a), "stroke", 3))
    cv.drawString(s, x - lw / 2, y, f, paint(cor, int(255 * a)))


def caixa_check(cv, x0, y, t_ok, t, a, tam=46):
    """Caixinha do checklist (mesmo traço do cf_fratura_cola / cf_quadril_bebe)."""
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


# ------------------------------------------------------------------ as pernas (de lado, olhando para a direita)
# coordenadas locais: chão em y = 0, tornozelo em x = 0; a ponta do pé fica à direita.
def _perna_crianca():
    """Do joelho para baixo: panturrilha arredondada atrás, canela quase reta na frente, pé descalço."""
    p = skia.Path()
    p.moveTo(-58, -445)
    p.cubicTo(-70, -385, -88, -325, -82, -262)
    p.cubicTo(-76, -200, -52, -162, -46, -122)
    p.cubicTo(-42, -92, -50, -72, -60, -52)
    p.cubicTo(-70, -32, -66, -2, -44, 0)
    p.lineTo(150, 0)
    p.cubicTo(178, 0, 190, -6, 186, -16)
    p.cubicTo(182, -30, 150, -40, 110, -56)
    p.cubicTo(80, -68, 52, -82, 40, -104)
    p.cubicTo(36, -140, 44, -250, 50, -330)
    p.cubicTo(52, -380, 54, -410, 56, -445)
    p.close()
    return p


def _perna_ado():
    """Adolescente: coxa (de bermuda) inclinada para a frente, joelho levemente dobrado, canela e pé."""
    p = skia.Path()
    p.moveTo(-118, -850)
    p.cubicTo(-122, -760, -108, -640, -84, -560)
    p.cubicTo(-66, -500, -46, -472, -44, -446)
    p.cubicTo(-62, -410, -86, -350, -84, -290)
    p.cubicTo(-82, -220, -54, -170, -46, -130)
    p.cubicTo(-42, -95, -56, -72, -68, -52)
    p.cubicTo(-80, -30, -74, -2, -50, 0)
    p.lineTo(175, 0)
    p.cubicTo(205, 0, 220, -8, 214, -20)
    p.cubicTo(208, -36, 172, -48, 128, -64)
    p.cubicTo(96, -76, 64, -92, 46, -116)
    p.cubicTo(52, -200, 70, -330, 82, -400)
    p.cubicTo(90, -420, 102, -440, 102, -466)
    p.cubicTo(102, -500, 88, -522, 78, -560)
    p.cubicTo(60, -640, 44, -760, 40, -850)
    p.close()
    return p


def _bermuda():
    p = skia.Path()
    p.moveTo(-132, -862); p.lineTo(52, -862)
    p.cubicTo(58, -780, 70, -690, 84, -620)
    p.lineTo(-100, -596)
    p.cubicTo(-120, -660, -134, -760, -132, -862)
    p.close()
    return p


CRIANCA, ADO, BERMUDA = _perna_crianca(), _perna_ado(), _bermuda()
TOPO = {"crianca": -445, "ado": -850}
GLOW = {"crianca": (-52, -38, 62), "ado": (88, -392, 66)}     # (x, y, raio) locais do brilho de dor
_SH_PELE = skia.GradientShader.MakeLinear([skia.Point(-115, 0), skia.Point(230, 0)],
                                          [C(PELE_ESC), C(PELE), C(PELE_CL), C(PELE), C(PELE)],
                                          [0.0, 0.16, 0.36, 0.55, 1.0])


_MASC_AL = (0, 18, 70, 150, 215, 245, 255)
_MASC_POS = [0.0, 0.18, 0.38, 0.58, 0.76, 0.9, 1.0]


def na_tela(pose, lx, ly):
    x, yf, s = pose
    return x + lx * s, yf + ly * s


def perna(cv, qual, pose, a=1.0):
    """Perna de desenho OPACA (pele lisa); o topo dissolve no fundo por máscara (DstIn), como no piloto."""
    x, yf, s = pose
    if a <= 0 or s <= 0:
        return
    pth = ADO if qual == "ado" else CRIANCA
    top = TOPO[qual]
    cv.save(); cv.translate(x, yf); cv.scale(s, s)
    cv.drawOval(skia.Rect(-95, -10, 220 if qual == "ado" else 195, 16), paint("#000000", int(80 * a), blur=10))
    caixa = skia.Rect(-150, top - 20, 260, 30)
    cv.saveLayer(caixa, _alfa(a)) if a < 1 else cv.saveLayer(caixa, None)
    cv.drawPath(pth, paint(PELE, 255, shader=_SH_PELE))
    if qual == "ado":
        cv.drawArc(skia.Rect(64, -492, 106, -436), -70, 120, False, paint(PELE_LINHA, 110, "stroke", 4))   # joelho
        b = paint(SHORT); b.setPathEffect(skia.CornerPathEffect.Make(16))
        cv.drawPath(BERMUDA, paint("#000000", 60, blur=8))
        cv.drawPath(BERMUDA, b)
        cv.drawLine(-98, -610, 80, -632, paint(SHORT_ESC, 255, "stroke", 5))
        cv.drawLine(-46, -850, -34, -700, paint(SHORT_CL, 140, "stroke", 4))
    cv.drawPath(pth, _p(PELE_LINHA, 230, "stroke", 3.6 / max(s, 0.5), junta=True))
    # rampa de alfa em "S" (várias paradas): a pele opaca dissolve no fundo sem costura horizontal
    masc = skia.Paint(AntiAlias=True)
    masc.setShader(skia.GradientShader.MakeLinear([skia.Point(0, top), skia.Point(0, top + 190)],
                                                  [skia.ColorSetARGB(v, 0, 0, 0) for v in _MASC_AL], _MASC_POS))
    masc.setBlendMode(skia.BlendMode.kDstIn)
    cv.drawRect(caixa, masc)
    cv.restore()
    cv.restore()


def brilho_dor(cv, x, y, r, k):
    """Brilho vermelho-suave sobre a pele (gradiente radial; sem chama, sem sangue)."""
    if k <= 0.005 or r <= 0:
        return
    sh = skia.GradientShader.MakeRadial(skia.Point(x, y), r,
                                        [C(DOR, int(225 * min(1, k))), C(DOR, int(150 * min(1, k))),
                                         C(DOR, int(55 * min(1, k))), C(DOR, 0)], [0.0, 0.35, 0.7, 1.0])
    cv.drawCircle(x, y, r, paint(DOR, 255, shader=sh))
    if k > 1:                                          # lampejo de quando acende
        cv.drawCircle(x, y, r * 0.35, paint("#FFD9DA", int(120 * min(1, k - 1)), blur=10))


# ------------------------------------------------------------------ poses (é a "câmera" da cena)
def _mix(a, b, k):
    return tuple(lerp(u, v, k) for u, v in zip(a, b))


def troca(T):
    """Troca de cena (balão sai, entra o adolescente): 0,3 s depois de "dor" (2ª), para o halo do
    balão completar o pulso de "inflama" antes de sair."""
    return T["dor2"] + 0.3


def poses(t, T):
    """-> (pose da perna da criança, pose da perna do adolescente, alfa do adolescente)."""
    ent = lerp(0.9, 1.0, e_back(prog(t, 0.0, 0.5)))
    # capa: perna centrada; abre espaço para o balão (à esquerda) logo antes de "osso"
    kA = (lerp(560, 720, e_inout(prog(t, T["osso"] - 0.5, T["osso"] + 0.05))), 1075, 1.45 * ent)
    kB, kC, kD, kE = (812, 1000, 0.72), (805, 860, 0.6), (808, 1005, 0.72), (790, 650, 0.40)
    k1, k2, kd, k3 = transicoes(t, T)
    cri = _mix(_mix(_mix(_mix(kA, kB, k1), kC, k2), kD, kd), kE, k3)
    ent_a = e_out(prog(t, troca(T) + 0.05, troca(T) + 0.7))
    aB = (lerp(-320, 270, ent_a), 1000, 0.8)
    ado = _mix(_mix(_mix(aB, (285, 860, 0.68), k2), (275, 1005, 0.8), kd), (300, 650, 0.46), k3)
    return cri, ado, ent_a


def transicoes(t, T):
    """Trocas de enquadramento: A->B ("dor", 2ª), B->C ("ajuda"), C->D ("com": volta às duas pernas
    grandes para o "melhorar"), D->E ("persiste": as pernas sobem para o cartão de atenção)."""
    return (e_inout(prog(t, troca(T) - 0.05, troca(T) + 0.6)),
            e_inout(prog(t, T["ajuda"] - 0.1, T["ajuda"] + 0.5)),
            e_inout(prog(t, T["com"] + 0.05, T["com"] + 0.75)),
            e_inout(prog(t, T["persiste"] - 0.3, T["persiste"] + 0.2)))


def pulso(t, T):
    """Pulso comum aos dois brilhos e ao halo do balão (0..1). Começa perto do PICO logo depois de
    "inflama" e bate a cada 0,8 s enquanto o balão está na tela (2 picos visíveis); depois da troca
    de cena a FASE continua (sem salto) num ritmo mais calmo, de 1,15 s."""
    t0, tr = T["inflama"] + 0.25, troca(T)
    fase = (min(t, tr) - t0) / 0.8 + max(0.0, t - tr) / 1.15
    return 0.5 + 0.5 * math.cos(2 * math.pi * fase)


def intens(t, T, t_on, pre=0.0):
    """Intensidade de um brilho de dor: acende em t_on (com lampejo), pulsa a partir de 'inflama', fica
    mais FRACO (sem sumir) em 'melhorar'. `pre`: brilho fraco antes (a capa já mostra onde dói)."""
    if t < t_on - 0.05:
        return pre * (0.85 + 0.15 * math.sin(t * 5))
    k = max(pre, prog(t, t_on - 0.05, t_on + 0.3))
    flash = clamp(1 - (t - t_on) / 0.6) * 0.5
    amp = 0.32 * prog(t, T["inflama"], T["inflama"] + 0.3) * (1 - 0.75 * prog(t, T["melhorar"], T["melhorar"] + 1.0))
    puls = 1 - amp * (1 - pulso(t, T))
    fraco = lerp(1.0, 0.36, e_inout(prog(t, T["melhorar"], T["melhorar"] + 1.0)))
    return k * puls * fraco + flash * k


# ------------------------------------------------------------------ ícones de "quem treina" (contorno)
def _pent(cx, cy, r, rot):
    p = skia.Path()
    for i in range(5):
        an = rot + i * 2 * math.pi / 5
        (p.moveTo if i == 0 else p.lineTo)(cx + r * math.cos(an), cy + r * math.sin(an))
    p.close()
    return p


def bola(cv, x, y, r, a, giro=0.0, larg=5):
    """Bola de futebol em contorno: gomo central e gomos da borda dourados, costuras brancas."""
    if a <= 0:
        return
    cv.save(); cv.translate(x, y); cv.rotate(giro)
    cv.drawCircle(0, 0, r, paint(FUNDO_CARTAO, int(170 * a)))
    cv.save()
    clip = skia.Path(); clip.addCircle(0, 0, r)
    cv.clipPath(clip, skia.ClipOp.kIntersect, True)
    for i in range(5):
        an = -math.pi / 2 + i * 2 * math.pi / 5
        vx, vy = r * 0.36 * math.cos(an), r * 0.36 * math.sin(an)
        cx, cy = r * 1.02 * math.cos(an + math.pi / 5), r * 1.02 * math.sin(an + math.pi / 5)
        cv.drawPath(_pent(cx, cy, r * 0.36, an + math.pi / 5), paint(OURO, int(255 * a)))
        cv.drawLine(vx, vy, r * 0.74 * math.cos(an), r * 0.74 * math.sin(an), paint("#FFFFFF", int(230 * a), "stroke", larg * 0.6))
    cv.restore()
    cv.drawPath(_pent(0, 0, r * 0.36, -math.pi / 2), paint(OURO, int(255 * a)))
    cv.drawCircle(0, 0, r, paint("#FFFFFF", int(255 * a), "stroke", larg))
    cv.restore()


def tenis(cv, x, y, esc, a):
    """Tênis em contorno, de lado (bico para a direita)."""
    if a <= 0:
        return
    cv.save(); cv.translate(x, y); cv.scale(esc, esc)
    p = skia.Path()
    p.moveTo(-78, 18); p.lineTo(-78, -30)
    p.cubicTo(-78, -48, -64, -54, -50, -50)
    p.lineTo(-30, -46)
    p.cubicTo(-14, -24, 10, -18, 30, -14)
    p.cubicTo(58, -8, 80, 0, 82, 14)
    p.lineTo(82, 18); p.close()
    cv.drawPath(p, paint(FUNDO_CARTAO, int(150 * a)))
    cv.drawPath(p, _p("#FFFFFF", int(255 * a), "stroke", 5, junta=True))
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(-84, 14, 88, 32), 9, 9), paint(OURO, int(255 * a)))
    for k in range(3):                                   # cadarço
        xx = -22 + k * 16
        cv.drawLine(xx, -36 + k * 5, xx + 12, -24 + k * 5, paint(OURO, int(255 * a), "stroke", 4))
    cv.restore()


def treina(cv, t, T):
    sai = 1 - prog(t, T["osso"] - 0.25, T["osso"] + 0.1)
    for i, (x, y) in enumerate(((905, 560), (890, 760))):
        k = prog(t, T["treina"] + 0.12 * i, T["treina"] + 0.12 * i + 0.45)
        a = clamp(k * 2) * sai
        if a <= 0:
            continue
        e = lerp(0.5, 1.0, e_back(k))
        dy = 7 * math.sin(t * 2.1 + i * 1.7)
        if i == 0:
            bola(cv, x, y + dy, 50 * e, a, giro=12 * math.sin(t * 1.3))
        else:
            tenis(cv, x, y + dy, 1.0 * e, a)


# ------------------------------------------------------------------ balão de lupa (solto) com o bloco de osso
BX, BY, BR = 315, 760, 210        # na altura do pé (o balão amplia o calcanhar, não a panturrilha)


def _bloco():
    """Bloco de osso genérico, arredondado (superelipse): não pretende ser a forma do calcâneo."""
    p = skia.Path(); n = 64
    for i in range(n):
        ph = 2 * math.pi * i / n
        c, s = math.cos(ph), math.sin(ph)
        x = 136 * math.copysign(abs(c) ** 0.62, c)
        y = 96 * math.copysign(abs(s) ** 0.62, s)
        (p.moveTo if i == 0 else p.lineTo)(x, y)
    p.close()
    return p


BLOCO = _bloco()
_SH_LENTE = skia.GradientShader.MakeRadial(skia.Point(-40, -50), 260, [C(LENTE_IN), C(LENTE_OUT)])
_SH_BLOCO = skia.GradientShader.MakeLinear([skia.Point(0, -82), skia.Point(0, 82)],
                                           [C(OSSO_C), C(OSSO_C), C(OSSO_B)], [0.0, 0.45, 1.0])


def balao(cv, t, T):
    esc = e_back(prog(t, T["osso"] - 0.1, T["osso"] + 0.35)) * (1 - e_in_back(prog(t, troca(T) - 0.3, troca(T) + 0.1)))
    if esc <= 0.01:
        return
    esc *= 1 + 0.07 * e_inout(prog(t, T["inflama"] - 0.1, T["inflama"] + 0.45))    # o espanto: a lupa chega perto
    k = BR / 210 * esc
    by = BY + 5 * math.sin(t * 1.2)
    cv.save(); cv.translate(BX, by); cv.scale(k, k)
    cv.drawCircle(0, 14, 216, paint("#000000", 110, blur=22))
    cv.save()
    clip = skia.Path(); clip.addCircle(0, 0, 210)
    cv.clipPath(clip, skia.ClipOp.kIntersect, True)
    cv.drawRect(skia.Rect(-210, -210, 210, 210), paint(LENTE_IN, shader=_SH_LENTE))
    # halo de inflamação: pulsa no mesmo ritmo do brilho do calcanhar
    hal = prog(t, T["inflama"], T["inflama"] + 0.35)
    if hal > 0:
        pu = pulso(t, T)
        cv.drawPath(BLOCO, _p(DOR, int(hal * (120 + 110 * pu)), "stroke", 30 + 22 * pu, blur=16, junta=True))
    cv.save(); cv.translate(0, 8)
    cv.drawPath(BLOCO, paint("#000000", 70, blur=12))
    cv.restore()
    cv.drawPath(BLOCO, paint(OSSO_C, shader=_SH_BLOCO))
    cres = prog(t, T["crescimento"] - 0.05, T["crescimento"] + 0.35)
    cv.drawPath(BLOCO, _p(OSSO_L, int(170 * (1 - cres)), "stroke", 3, junta=True))
    if cres > 0:
        # setinhas douradas subindo POR DENTRO do bloco inteiro (símbolo de crescimento)
        cv.save(); cv.clipPath(BLOCO, skia.ClipOp.kIntersect, True)
        vel = 62.0
        for col, x in enumerate((-58, 58)):
            for j in range(4):
                y = 120 - ((t - T["crescimento"]) * vel + j * 62 + col * 31) % 248
                a = cres * clamp((1 - abs(y) / 100) * 2.2)
                if a <= 0:
                    continue
                ch = skia.Path(); ch.moveTo(x - 24, y + 13); ch.lineTo(x, y - 11); ch.lineTo(x + 24, y + 13)
                cv.drawPath(ch, _p("#8A5A00", int(150 * a), "stroke", 15, junta=True))
                cv.drawPath(ch, _p(OURO, int(255 * a), "stroke", 9, junta=True))
        cv.restore()
        if hal > 0:
            cv.drawPath(BLOCO, paint(DOR, int(26 * hal * pulso(t, T))))
        cv.drawPath(BLOCO, _p(OURO, int(255 * cres), "stroke", 7, traco=(22, 13), fase=-(t * 26) % 35))
    cv.restore()
    cv.drawCircle(0, 0, 210, paint("#000000", 90, "stroke", 24, blur=8))
    cv.drawCircle(0, 0, 210, paint(OURO, 255, "stroke", 12))
    cv.drawCircle(0, 0, 200, paint("#FFFFFF", 80, "stroke", 3))
    cv.drawArc(skia.Rect(-150, -150, 150, 150), 200, 50, False, paint("#FFFFFF", 70, "stroke", 6))
    cv.restore()
    brilhos(cv, BX, by, t, T["crescimento"] + 0.1, n=12, raio=200)


# ------------------------------------------------------------------ régua do estirão (sem números)
def regua(cv, x, ytop, ybot, nivel, a):
    """A régua do cf_placa_crescimento (sem números); a barra dourada sobe com uma ponta de seta."""
    if a <= 0:
        return
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(x - 9, ytop, x + 9, ybot), 9, 9), paint("#FFFFFF", int(45 * a)))
    yy, i = ybot, 0
    while yy >= ytop + 6:
        cv.drawLine(x + 15, yy, x + (29 if i % 4 == 0 else 22), yy, paint("#FFFFFF", int(120 * a), "stroke", 2))
        yy -= 34; i += 1
    yn = lerp(ybot, ytop + 34, nivel)
    if nivel > 0.01:
        cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(x - 7, yn, x + 7, ybot), 7, 7), paint(OURO, int(255 * a)))
        cv.drawLine(x, ybot, x, yn, paint("#FFB627", int(90 * a), "stroke", 22, blur=10))
        ponta(cv, x, yn - 4, -math.pi / 2, 30, OURO, a)


# ------------------------------------------------------------------ balança TREINO / DESCANSO
def ang_balanca(t, T):
    k = t - T["equilibrar"]
    if k < 0:
        return 15.0
    return 15.0 * math.exp(-2.3 * k) * math.cos(2 * math.pi * 1.05 * k)


def balanca(cv, x, y, ang, a, esc):
    if a <= 0 or esc <= 0:
        return
    cv.save(); cv.translate(x, y); cv.scale(esc, esc)
    # coluna e pé
    cv.drawLine(0, 6, 0, 168, paint("#000000", int(70 * a), "stroke", 14, blur=4))
    cv.drawLine(0, 6, 0, 168, paint(OSSO_C, int(255 * a), "stroke", 10))
    pe = skia.Path(); pe.moveTo(-46, 186); pe.lineTo(46, 186); pe.lineTo(22, 164); pe.lineTo(-22, 164); pe.close()
    cv.drawPath(pe, paint(OSSO_C, int(255 * a)))
    cv.drawPath(pe, _p(OSSO_L, int(200 * a), "stroke", 2.5, junta=True))
    r = math.radians(ang)
    L = 100
    pts = [(-L * math.cos(r), -L * math.sin(r)), (L * math.cos(r), L * math.sin(r))]
    cv.drawLine(*pts[0], *pts[1], paint("#000000", int(90 * a), "stroke", 15, blur=4))
    cv.drawLine(*pts[0], *pts[1], paint(OURO, int(255 * a), "stroke", 10))
    cv.drawCircle(0, 0, 12, paint(OURO, int(255 * a)))
    cv.drawCircle(0, 0, 12, paint("#8A6512", int(255 * a), "stroke", 3))
    for (px, py), rot in zip(pts, (TREINO, DESCANSO)):
        yb = py + 62
        cv.drawLine(px, py, px - 36, yb, paint("#DDE6EE", int(220 * a), "stroke", 2.5))
        cv.drawLine(px, py, px + 36, yb, paint("#DDE6EE", int(220 * a), "stroke", 2.5))
        prato = skia.Path(); prato.moveTo(px - 44, yb)
        prato.cubicTo(px - 36, yb + 22, px + 36, yb + 22, px + 44, yb); prato.close()
        cv.drawPath(prato, paint(OURO, int(255 * a)))
        cv.drawPath(prato, _p("#8A6512", int(255 * a), "stroke", 2.5, junta=True))
        cv.drawCircle(px, py, 5, paint("#FFFFFF", int(255 * a)))
        texto(cv, rot, px, yb + 54, F_BLACK, 31, "#FFFFFF", int(255 * a), contorno=7)
    cv.restore()


# ------------------------------------------------------------------ gelo e alongamento
def bolsa_gelo(cv, x, y, ang, esc, a):
    """Bolsa de gelo de desenho (azul-clara, com tampa e um floco de neve desenhado)."""
    if a <= 0:
        return
    cv.save(); cv.translate(x, y); cv.rotate(ang); cv.scale(esc, esc)
    corpo = skia.RRect.MakeRectXY(skia.Rect(-34, -50, 34, 54), 26, 26)
    cv.drawRRect(corpo, paint("#000000", int(80 * a), blur=8))
    sh = skia.GradientShader.MakeLinear([skia.Point(-34, 0), skia.Point(34, 0)], [C(GELO_MED), C(GELO), C(GELO_MED)])
    cv.drawRRect(corpo, paint(GELO, int(255 * a), shader=sh))
    cv.drawRRect(corpo, paint(GELO_ESC, int(255 * a), "stroke", 3.5))
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(-15, -66, 15, -46), 6, 6), paint(GELO_ESC, int(255 * a)))
    for k in range(3):                                   # floco de neve (só traços)
        an = math.radians(90 + k * 60)
        dx, dy = 20 * math.cos(an), 20 * math.sin(an)
        cv.drawLine(-dx, 4 - dy, dx, 4 + dy, paint("#FFFFFF", int(255 * a), "stroke", 4.5))
    cv.drawCircle(0, 4, 4, paint(GELO_ESC, int(255 * a)))
    cv.drawLine(-20, -34, -20, 30, paint("#FFFFFF", int(150 * a), "stroke", 4))
    cv.restore()


def seta_dupla(cv, p0, p1, ext, a):
    """Seta dourada de duas pontas que se estica ao longo de p0-p1 (ext 0..1)."""
    if a <= 0 or ext <= 0:
        return
    cx, cy = (p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2
    dx, dy = (p1[0] - p0[0]) / 2 * ext, (p1[1] - p0[1]) / 2 * ext
    ang = math.atan2(dy, dx)
    x0, y0, x1, y1 = cx - dx, cy - dy, cx + dx, cy + dy
    cv.drawLine(x0, y0, x1, y1, paint("#FFB627", int(100 * a), "stroke", 26, blur=10))
    cv.drawLine(x0, y0, x1, y1, paint(FUNDO_CARTAO, int(190 * a), "stroke", 15))
    cv.drawLine(x0, y0, x1, y1, paint(OURO, int(255 * a), "stroke", 8))
    for (x, y, an) in ((x1, y1, ang), (x0, y0, ang + math.pi)):
        ponta(cv, x + 4 * math.cos(an), y + 4 * math.sin(an), an, 34, FUNDO_CARTAO, a * 0.8)
        ponta(cv, x, y, an, 28, OURO, a)


def esticar(t, t0):
    """Extensão da seta: abre de 0,55 a 1 e depois respira de leve (estica / solta)."""
    k = e_out(prog(t, t0, t0 + 0.55))
    resp = 0.05 * math.sin(2 * math.pi * (t - t0) / 1.6) * prog(t, t0 + 0.55, t0 + 0.9)
    return lerp(0.55, 1.0, k) + resp


# ------------------------------------------------------------------ checklist "o que ajuda"
CK_X0, CK_X1, CK_Y0, CK_Y1 = 150, 930, 990, 1212


def checklist(cv, t, T):
    a0 = prog(t, T["ajuda"] + 0.05, T["ajuda"] + 0.4) * (1 - prog(t, T["com"] - 0.05, T["com"] + 0.28))
    if a0 <= 0:
        return
    # entra subindo; sai NO LUGAR, subindo de leve (nunca desce para a faixa da legenda)
    dy = 240 * (1 - e_out(prog(t, T["ajuda"] + 0.05, T["ajuda"] + 0.5))) - 30 * e_out(
        prog(t, T["com"] - 0.05, T["com"] + 0.28))
    rr = skia.RRect.MakeRectXY(skia.Rect(CK_X0, CK_Y0 + dy, CK_X1, CK_Y1 + dy), 26, 26)
    cv.drawRRect(rr, paint("#000000", int(80 * a0), blur=14))
    cv.drawRRect(rr, paint(FUNDO_CARTAO, int(232 * a0)))
    cv.drawRRect(rr, paint(OURO, int(255 * a0), "stroke", 3))
    oks = (T["descanso"] + 0.15, T["gelo"] + 0.5, T["panturrilha"] + 0.5)
    ins = (T["equilibrar"], T["gelo"], T["alongar"])
    for i, (s, t_in, t_ok) in enumerate(zip(ITENS, ins, oks)):
        y = 1054 + i * 66 + dy
        caixa_check(cv, 190, y, t_ok, t, a0, tam=50)
        k = e_out(prog(t, t_in - 0.05, t_in + 0.3))
        if k > 0:
            texto(cv, s, 264 + 30 * (1 - k), y, F_BLACK, 44, "#FFFFFF", int(255 * a0 * k), centro=False)


# ------------------------------------------------------------------ cartão de atenção
CA_X0, CA_X1, CA_Y0, CA_Y1 = 80, 1000, 768, 1226


def relogio(cv, x, y, r, a, t):
    if a <= 0:
        return
    cv.drawCircle(x, y, r, paint(FUNDO_CARTAO, int(255 * a)))
    cv.drawCircle(x, y, r, paint(AMARELO, int(255 * a), "stroke", 5))
    an = t * 2.4
    cv.drawLine(x, y, x + r * 0.7 * math.cos(an), y + r * 0.7 * math.sin(an), paint("#FFFFFF", int(255 * a), "stroke", 4.5))
    cv.drawLine(x, y, x + r * 0.45 * math.cos(an / 12 - 1.2), y + r * 0.45 * math.sin(an / 12 - 1.2),
                paint("#FFFFFF", int(255 * a), "stroke", 5.5))
    cv.drawCircle(x, y, 4, paint(AMARELO, int(255 * a)))


def bola_pausa(cv, x, y, r, a):
    """Bola com um selo de pausa (o esporte parado), sem impacto."""
    if a <= 0:
        return
    bola(cv, x - 5, y - 3, r * 0.78, a, larg=4)
    bx, by = x + r * 0.55, y + r * 0.5
    cv.drawCircle(bx, by, r * 0.5 + 3, paint(FUNDO_CARTAO, int(255 * a)))
    cv.drawCircle(bx, by, r * 0.5, paint(AMARELO, int(255 * a)))
    for dx in (-5.5, 5.5):
        cv.drawLine(bx + dx, by - 8, bx + dx, by + 8, paint(FUNDO_CARTAO, int(255 * a), "stroke", 5))


def cadeado(cv, x, y, a, fecha):
    if a <= 0:
        return
    sobe = 12 * (1 - fecha)
    arco = skia.Path(); arco.moveTo(x - 15, y - 6 - sobe); arco.lineTo(x - 15, y - 18 - sobe)
    arco.cubicTo(x - 15, y - 42 - sobe, x + 15, y - 42 - sobe, x + 15, y - 18 - sobe); arco.lineTo(x + 15, y - 6 - sobe)
    cv.drawPath(arco, _p("#DDE6EE", int(255 * a), "stroke", 6, junta=True))
    corpo = skia.RRect.MakeRectXY(skia.Rect(x - 24, y - 10, x + 24, y + 26), 7, 7)
    cv.drawRRect(corpo, paint(AMARELO, int(255 * a)))
    cv.drawCircle(x, y + 6, 4.5, paint(FUNDO_CARTAO, int(255 * a)))
    cv.drawLine(x, y + 8, x, y + 16, paint(FUNDO_CARTAO, int(255 * a), "stroke", 3.5))


def triangulo_atencao(cv, x, y, a):
    if a <= 0:
        return
    p = skia.Path(); p.moveTo(x, y - 40); p.lineTo(x + 46, y + 36); p.lineTo(x - 46, y + 36); p.close()
    pt = paint(AMARELO, int(255 * a)); pt.setPathEffect(skia.CornerPathEffect.Make(12))
    gl = paint(AMARELO, int(90 * a), blur=14); gl.setPathEffect(skia.CornerPathEffect.Make(12))
    cv.drawPath(p, gl); cv.drawPath(p, pt)
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(x - 5, y - 16, x + 5, y + 14), 5, 5), paint(FUNDO_CARTAO, int(255 * a)))
    cv.drawCircle(x, y + 24, 5.5, paint(FUNDO_CARTAO, int(255 * a)))


def cartao_atencao(cv, t, T):
    # entra depois de as pernas subirem (k3), surgindo no lugar e subindo só 70 px: com alfa alto
    # nunca passa da faixa de cena (base do cartão em 1226 + 70)
    t_in = T["persiste"]
    a_g = prog(t, t_in - 0.05, t_in + 0.3) * (1 - prog(t, T["manda"] - 0.45, T["manda"] - 0.1))
    if a_g <= 0:
        return
    dy = 70 * (1 - e_out(prog(t, t_in, t_in + 0.45)))
    cv.save(); cv.translate(0, dy)
    card = skia.RRect.MakeRectXY(skia.Rect(CA_X0, CA_Y0, CA_X1, CA_Y1), 30, 30)
    cv.drawRRect(card, paint("#000000", int(90 * a_g), blur=16))
    cv.drawRRect(card, paint(FUNDO_CARTAO, int(245 * a_g)))
    cv.drawRRect(card, paint(AMARELO, int(255 * a_g), "stroke", 5))
    cv.drawCircle(CX_A, CA_Y0, 50, paint(FUNDO_CARTAO, int(255 * a_g)))
    cv.drawCircle(CX_A, CA_Y0, 50, paint(AMARELO, int(255 * a_g), "stroke", 5))
    cv.save(); cv.translate(CX_A, CA_Y0 + 2); cv.scale(0.8, 0.8)
    triangulo_atencao(cv, 0, 0, a_g)
    cv.restore()
    for i, (s, chave) in enumerate(zip(ALERTAS, ("persiste", "limita", "trava"))):
        k = prog(t, T[chave] - 0.05, T[chave] + 0.3)
        if k <= 0:
            continue
        a = a_g * k
        y = 888 + i * 92
        xi = 172 + 40 * (1 - e_out(k))
        if i == 0:
            relogio(cv, xi, y - 16, 30, a, t)
        elif i == 1:
            bola_pausa(cv, xi, y - 16, 36, a)
        else:
            cadeado(cv, xi, y - 14, a, e_out(prog(t, T["trava"] + 0.15, T["trava"] + 0.35)))
        texto(cv, s, 240 + 40 * (1 - e_out(k)), y, F_BLACK, 46, "#FFFFFF", int(255 * a), centro=False)
    k = prog(t, T["avaliar"] - 0.05, T["avaliar"] + 0.3)
    if k > 0:
        a = a_g * k
        cv.drawLine(230, 1102, 920, 1102, paint(AMARELO, int(120 * a), "stroke", 2.5))   # divisória (não sublinha)
        esc = lerp(0.85, 1.0, e_back(k))
        cv.save(); cv.translate(CX_A, 1160); cv.scale(esc, esc)
        texto(cv, AVALIAR, 0, 0, F_BLACK, 58, OURO, int(255 * a))
        cv.restore()
        texto(cv, ORTOPED, CX_A, 1206, F_BLACK, 36, AZUL, int(255 * a))
    cv.restore()


CX_A = (CA_X0 + CA_X1) / 2


# ------------------------------------------------------------------ o mundo (pernas, brilhos, mecanismos)
def mundo(cv, t, T):
    cri, ado, ent_a = poses(t, T)
    # chão
    a_chao = 0.6 + 0.4 * ent_a
    yf = cri[1]
    cv.drawLine(40, yf + 2, 1040, yf + 2, paint("#FFFFFF", int(28 * a_chao), "stroke", 3))
    perna(cv, "ado", ado, 1.0 if ent_a > 0 else 0.0)
    perna(cv, "crianca", cri)
    # brilhos de dor
    gx, gy, gr = GLOW["crianca"]
    x, y = na_tela(cri, gx, gy)
    brilho_dor(cv, x, y, gr * cri[2] * (1 + 0.1 * pulso(t, T) * prog(t, T["inflama"], T["inflama"] + 0.3)),
               intens(t, T, T["calcanhar"], pre=0.5))
    if ent_a > 0:
        gx, gy, gr = GLOW["ado"]
        x, y = na_tela(ado, gx, gy)
        brilho_dor(cv, x, y, gr * ado[2] * (1 + 0.1 * pulso(t, T)), intens(t, T, T["joelho"]))
    # alongar: setas de duas pontas (só a seta, nenhum músculo)
    a_set = 1 - prog(t, T["com"] - 0.1, T["com"] + 0.3)
    k = prog(t, T["coxa"] - 0.05, T["coxa"] + 0.15) * a_set
    if k > 0:
        seta_dupla(cv, na_tela(ado, -40, -770), na_tela(ado, 34, -500), esticar(t, T["coxa"] - 0.05), k)
    k = prog(t, T["panturrilha"] - 0.05, T["panturrilha"] + 0.15) * a_set
    if k > 0:
        seta_dupla(cv, na_tela(cri, -34, -395), na_tela(cri, -12, -150), esticar(t, T["panturrilha"] - 0.05), k)
    # gelo após a atividade: pousa sobre os dois brilhos; sai em "melhorar"
    sai = prog(t, T["melhorar"], T["melhorar"] + 0.5)
    # cada bolsa com deslocamento e escala próprios: a da criança fica SOBRE o calcanhar, acima do chão
    for i, (pose, qual, dx, dyl, ang, esc) in enumerate(((ado, "ado", 18, 0, -10, max(0.95, ado[2] * 1.4)),
                                                          (cri, "crianca", 8, -40, 8, max(0.78, cri[2] * 1.15)))):
        t0 = T["gelo"] + 0.1 + 0.12 * i
        k = prog(t, t0, t0 + 0.45)
        if k <= 0 or sai >= 1:
            continue
        gx, gy, _ = GLOW[qual]
        x, y = na_tela(pose, gx + dx, gy + dyl)
        y += -150 * (1 - e_back(k)) - 70 * e_in_back(sai)
        bolsa_gelo(cv, x, y, ang, esc, clamp(k * 2.5) * (1 - sai))


def rotulos(cv, t, T):
    cri, ado, ent_a = poses(t, T)
    # calcanhar (cena 1)
    hx, hy = na_tela(cri, *GLOW["crianca"][:2])
    a = prog(t, T["calcanhar"] + 0.05, T["calcanhar"] + 0.3) * (1 - prog(t, T["osso"] - 0.3, T["osso"]))
    rotulo(cv, CALCANHAR, hx - 110, 1062, hx - 8, hy + 4, DOR_TXT, a, esq=False)
    # nomes (sóbrios, sem carimbo): acompanham a perna
    k1, k2, kd, k3 = transicoes(t, T)
    ks = e_out(prog(t, T["sever"] - 0.05, T["sever"] + 0.35))
    xs = lerp(lerp(lerp(lerp(cri[0] + 40, 830, k1), 815, k2), 830, kd), 812, k3)
    ys = lerp(lerp(lerp(lerp(1150, 1075, k1), 938, k2), 1080, kd), 700, k3) + 16 * (1 - ks)
    chip(cv, SEVER, xs, ys, "#FFFFFF", clamp(ks * 1.4) * fim_cena(t, T), tam=36, borda=OSSO_B)
    ko = e_out(prog(t, T["osgood"] - 0.05, T["osgood"] + 0.35))
    xo = lerp(lerp(lerp(280, 285, k2), 280, kd), 282, k3)
    yo = lerp(lerp(lerp(1075, 938, k2), 1080, kd), 700, k3) + 16 * (1 - ko)
    chip(cv, OSGOOD, xo, yo, "#FFFFFF", clamp(ko * 1.4) * fim_cena(t, T), tam=36, borda=OSSO_B)
    # balão: área de crescimento / inflamação
    a = prog(t, T["crescimento"], T["crescimento"] + 0.25) * (1 - prog(t, troca(T) - 0.3, troca(T)))
    chip(cv, AREA, BX, 1044, OURO, a, tam=38)
    a = prog(t, T["inflama"], T["inflama"] + 0.25) * (1 - prog(t, troca(T) - 0.3, troca(T)))
    chip(cv, INFLAM, BX, 508, DOR_TXT, a, tam=38, borda=DOR)
    # abaixo do joelho; estirão (régua sem números entre as pernas)
    fora = 1 - prog(t, T["ajuda"] - 0.3, T["ajuda"] + 0.05)
    jx, jy = na_tela(ado, *GLOW["ado"][:2])
    a = prog(t, T["joelho"] + 0.05, T["joelho"] + 0.3) * fora
    rotulo(cv, ABAIXO, 450, 424, jx + 6, jy - 4, DOR_TXT, a)
    a = prog(t, T["estirao"] - 0.15, T["estirao"] + 0.1) * fora
    regua(cv, 572, 668, 990, e_inout(prog(t, T["estirao"], T["estirao"] + 0.55)), a)
    chip(cv, ESTIRAO, 572, 612, OURO, prog(t, T["estirao"], T["estirao"] + 0.2) * fora, tam=38)
    brilhos(cv, 572, 712, t, T["estirao"] + 0.5, n=10, raio=80)
    # alongar: nome do que estica, ao lado da seta
    a_set = 1 - prog(t, T["com"] - 0.1, T["com"] + 0.3)
    chip(cv, COXA, 448, 462, OURO, prog(t, T["coxa"], T["coxa"] + 0.2) * a_set, tam=34)
    chip(cv, PANTU, 566, 706, OURO, prog(t, T["panturrilha"], T["panturrilha"] + 0.2) * a_set, tam=34)


def fim_cena(t, T):
    return 1 - prog(t, T["manda"] - 0.45, T["manda"] - 0.1)


# ------------------------------------------------------------------ quadro
def quadro(cv, t, T, blocos, ep):
    fundo(cv, t)
    mundo(cv, t, T)
    treina(cv, t, T)
    balao(cv, t, T)

    # balança entre as pernas: oscila, assenta nivelada e sai inteira (nenhum prato some) antes do gelo
    k = e_back(prog(t, T["equilibrar"] - 0.1, T["equilibrar"] + 0.35))
    a_b = clamp(k * 2) * (1 - prog(t, T["gelo"] - 0.3, T["gelo"] + 0.05))
    esc_b = k * lerp(1.0, 0.85, e_inout(prog(t, T["gelo"] - 0.3, T["gelo"] + 0.05)))
    balanca(cv, 578, 430, ang_balanca(t, T), a_b, esc_b * 1.08)

    rotulos(cv, t, T)

    # título do serviço
    a = prog(t, T["ajuda"], T["ajuda"] + 0.3) * (1 - prog(t, T["com"] - 0.05, T["com"] + 0.3))
    if a > 0:
        dy = -22 * (1 - e_out(prog(t, T["ajuda"], T["ajuda"] + 0.4)))
        texto(cv, AJUDA, 540, 296 + dy, F_BLACK, 56, OURO, int(255 * a), contorno=10)
    checklist(cv, t, T)
    cartao_atencao(cv, t, T)

    capa(cv, t, T["sever"] - 0.35, ep["gancho"][0], ep["gancho"][1])
    selo_como_funciona(cv, prog(t, T["sever"] + 0.1, T["sever"] + 0.5) * (1 - prog(t, T["manda"] - 0.3, T["manda"])))
    interface(cv, t, T, blocos, DESTAQUE)


# ------------------------------------------------------------------ som e prévias
def sons(T):
    ev = [(0.02, "whoosh", 0.35), (0.3, "pop", 0.45),
          (T["calcanhar"] + 0.02, "ping", 0.55),
          (T["treina"] + 0.05, "pop", 0.45), (T["treina"] + 0.17, "pop", 0.4),
          (T["sever"], "tick", 0.45),
          (T["osso"] - 0.12, "whoosh", 0.45), (T["osso"] + 0.12, "pop", 0.6),
          (T["crescimento"], "shimmer", 0.6)]
    ev += [(T["crescimento"] + 0.2 + 0.24 * i, "click", 0.3) for i in range(4)]
    # "inflama": o pulso também se ouve — dois thumps suaves nos dois picos do halo
    ev += [(T["inflama"] + 0.05, "ping", 0.35),
           (T["inflama"] + 0.25, "thump", 0.42), (T["inflama"] + 1.05, "thump", 0.3),
           (troca(T) - 0.05, "whoosh", 0.55), (T["joelho"], "ping", 0.55),
           (T["estirao"], "whoosh", 0.45), (T["estirao"] + 0.5, "ding", 0.45),
           (T["osgood"], "tick", 0.45),
           (T["ajuda"] - 0.05, "whoosh", 0.5), (T["ajuda"] + 0.3, "pop", 0.5),
           (T["equilibrar"], "pop", 0.45)]
    ev += [(T["equilibrar"] + 0.48 * i + 0.1, "click", 0.55 * 0.75 ** i) for i in range(3)]
    ev += [(T["descanso"] + 0.15, "tick", 0.6),
           (T["gelo"] + 0.42, "pop", 0.55), (T["gelo"] + 0.54, "pop", 0.5), (T["gelo"] + 0.5, "tick", 0.55),
           (T["coxa"], "whoosh", 0.4), (T["panturrilha"], "whoosh", 0.4), (T["panturrilha"] + 0.5, "tick", 0.6),
           (T["com"] + 0.05, "whoosh", 0.35), (T["melhorar"], "whoosh", 0.25),
           (T["persiste"] - 0.3, "whoosh", 0.5), (T["persiste"] + 0.15, "pop", 0.5), (T["limita"], "pop", 0.5),
           (T["trava"] + 0.25, "click", 0.75), (T["avaliar"] + 0.05, "ding", 0.5),
           (T["manda"] + 0.05, "whoosh", 0.5)]
    return ev


def tempos_previa(T):
    # inflama+0,3 = 1º pico do halo; dor2+0,15 = chegando ao 2º pico, com o balão ainda inteiro
    # (o "joelho" aparece no quadro do osgood, junto do estirão)
    return [0.0, T["treina"] + 0.6, T["crescimento"] + 0.7, T["inflama"] + 0.3, T["dor2"] + 0.15,
            T["osgood"] + 0.6, T["equilibrar"] + 0.5, T["gelo"] + 0.9, T["panturrilha"] + 0.8,
            T["melhorar"] + 0.8, T["avaliar"] + 0.9, T["manda"] + 1.6]


# respiro antes da CTA: o cartão de atenção completo fica ~2,4 s na tela para ser lido.
render = fazer_render(quadro, ANCORAS, sons, tempos_previa, respiro_cta=2.4)
