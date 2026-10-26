# -*- coding: utf-8 -*-
"""CHAMA O VAR — "TORCEU O PÉ: / CORRE QUE PASSA?" (primeiros socorros no jogo), episódio da série.

Mesma linguagem do piloto cf_chamaovar_rotina_fixador (selo VAR + chip, ritual lance -> "pode?"/congela ->
CHECANDO -> carimbo -> porquê mostrado -> JEITO CERTO; paleta ardósia/ciano/âmbar/verde; TV que desliga;
apito que passa adiante; CTA de jogo). Os helpers do piloto foram COPIADOS para cá (o piloto não foi editado).

Três lances do MESMO jogo de criança (storyboard: lab/formato_novo/cf_var_primeiros_socorros/storyboard.json):
  1. "Torceu o pé: corre que passa?" -> ANULADO. Quadro 0 = close de frente das pernas de chuteira, o pé
     que pisou na bola e virou para dentro (só o calçado gira, rígido; nada de pele colorida); em "VAR"
     rebobina; em "Torceu o pé" o replay lento; em "corre" corte para o plano aberto de lado: dois passos
     mancando, congela em "passa?" (só as pernas). Veredito: em "dor que faz parar" a criança para e leva a
     mão ao tornozelo; em "tira do jogo" a placa de substituição (só a seta), o telestrador traça a LINHA
     LATERAL e um adulto (cortado no ombro, sem rosto; a cabeça da criança chega ao peito dele) a leva pela
     mão, pulando num pé só, até cruzar a linha (chip JEITO CERTO); em "Não pisa pra testar" o pé fica no ar,
     com o vão tracejado em verde até a grama.
  2. "Massagem forte pra desinchar: pode?" -> ANULADO. No banco, descalço (pé com calcanhar e dedos), o pé em
     cima da mochila; duas mãos de adulto (mangas com cotovelo) apertam o tornozelo. Replay de perto ("massagem
     forte aumenta o inchaço"): as mãos esfregam, largam, e o tornozelo INTEIRO engrossa por igual (mesma cor de
     pele), com o contorno normal tracejado em ciano por dentro e setas âmbar curtas encostadas no contorno, para
     os lados e para cima. "Gelo com pano": bolsa de gelo no pano listrado; "pé pra cima": o casaco dobrado entra
     e o pé sobe. O contorno não murcha (nada de prometer efeito).
  3. "Caiu e o braço ficou torto. Imobilizar como está: pode?" -> VALIDADO. Outra criança (camisa cinza) tropeça
     e cai sobre a mão; ajoelhada, protege o antebraço torto (dobra de 30° no meio, sem cor, osso ou ferida) com a
     outra mão por baixo; o telestrador marca o ângulo logo acima do braço; a revista (capa com foto e linhas de
     texto) e a toalhinha listrada entram inteiras ao lado. Replay do jeito errado: a mão de um adulto fecha POR
     CIMA do punho, seta âmbar de tração ao longo do antebraço, um contorno-fantasma âmbar mostra o braço
     "endireitado" (a pele não muda), X âmbar, a mão abre e sai (chip só VAR). Cortina: o braço COMO ESTÁ (a mesma
     dobra, em escorço junto à barriga), pano preenchendo o vão sob a dobra, revista reta por baixo, tiras
     frouxas, tipoia; as mesmas linhas do telestrador voltam sobre a tala; a mão do adulto no ombro (contorno
     verde, visto, chip VALIDADO). "e vai pro pronto-socorro": sai andando ao lado do adulto (sem ambulância).
  Fim: apito final, a TV desliga, a profissional de saúde (jaleco e estetoscópio, sem rosto) recebe o apito
  ("Na dúvida, quem apita é o médico."); selo CHAMA O VAR; CTA "Manda pra quem ia errar o lance da massagem.".
Guardrails: pele OPACA de desenho e sempre cor de pele (âmbar só em carimbo, setas, X e contornos); nenhum
osso, exame, sangue, roxo ou ferida; nenhum rosto; nenhum cartão; placa sem número; sem ambulância; vermelho
não aparece. Todo texto desenhado está em ep["tela"] (o render recusa o vídeo se não estiver). Cena PRESA ao
roteiro pelas palavras-âncora (roteiro sem elas = KeyError).

Render próprio (cópia do fazer_render_var do piloto): só INSERE silêncio — vão de CHECANDO depois de cada
"?", vãos antes de "Massagem" e "Caiu" (o visto respira antes do lance seguinte), antes do 3º "e" (o X do
replay + o jeito certo do braço, sem fala) e antes de "Na" (apito final + TV desligando), e 0,25 s de apito
antes da 1ª palavra. Legenda com blocos próprios (montar_blocos_var): a pergunta fica no bloco do que pergunta.
"""
import math
import os

import numpy as np
import skia

from . import som, voz as _voz
from .base import codificar, previas as _previas
from .cf_alongamento import (BG_OUT, CX, F_BLACK, F_REG, F_SEMI, H, OURO, W, aviao, clamp, e_back, e_inout,
                             e_out, larg_texto, lerp, lerpc, paint, prog, texto)
from .cf_comum import DISC, SIG
from .cf_fratura_cola import alinhar, comprimir

# ------------------------------------------------------------------ sincronia com a fala
ANCORAS = {
    # lance 1 — torceu o pé: corre que passa?
    "chama": ("chama", 1, False), "var": ("var", 1, False), "torceu": ("torceu", 1, False),
    "pe1": ("pé", 1, False), "corre": ("corre", 1, False), "passa": ("passa", 1, False),
    "anulado1": ("anulado", 1, False), "dor": ("dor", 1, False), "parar": ("parar", 1, False),
    "tira": ("tira", 1, False), "jogo": ("jogo", 1, False), "nao1": ("não", 1, False),
    "pisa": ("pisa", 1, False), "testar": ("testar", 1, False),
    # lance 2 — massagem forte pra desinchar
    "massagem": ("massagem", 1, False), "forte": ("forte", 1, False), "desinchar": ("desinchar", 1, False),
    "pode1": ("pode", 1, False), "anulado2": ("anulado", 2, False), "logo": ("logo", 1, False),
    "torcao": ("torção", 1, False), "aumenta": ("aumenta", 1, False), "inchaco": ("inchaço", 1, False),
    "gelo": ("gelo", 1, False), "pano": ("pano", 1, False), "pe2": ("pé", 2, False), "cima": ("cima", 1, False),
    # lance 3 — braço torto: imobilizar como está
    "caiu": ("caiu", 1, False), "braco": ("braço", 1, False), "torto1": ("torto", 1, False),
    "imobilizar": ("imobilizar", 1, False), "esta": ("está", 1, False), "pode2": ("pode", 2, False),
    "validado": ("validado", 1, False), "nao2": ("não", 2, False), "puxa": ("puxa", 1, False),
    "endireita": ("endireita", 1, False), "e3": ("e", 3, False), "vai": ("vai", 1, False),
    "pronto": ("pronto-socorro", 1, False),
    # fim
    "na": ("na", 1, False), "quem": ("quem", 1, False), "apita": ("apita", 1, False),
    "medico": ("médico", 1, False), "manda": ("manda", 1, False),
}
FIM_DE = ("passa", "pe1", "parar", "jogo", "testar", "pode1", "pode2", "inchaco", "cima", "torto1", "esta",
          "endireita", "pronto", "medico", "desinchar")
DESTAQUE = {"var", "torceu", "jogo", "testar", "inchaço", "gelo", "cima", "torto", "endireita", "pronto-socorro",
            "apita", "médico"}

# rótulos (todos estão em ep["tela"])
T_VAR = "VAR"
T_LANCE = ("LANCE 1", "LANCE 2", "LANCE 3")
T_CHEC = "CHECANDO"
T_ANUL = "ANULADO"
T_VALID = "VALIDADO"
T_CERTO = "JEITO CERTO"
T_SERIE = "CHAMA O VAR"

# ------------------------------------------------------------------ paleta (a da série)
ARD_IN, ARD_OUT = "#22303F", "#121A24"
CIANO = "#4FD1FF"
VERDE = "#3DDC84"
AMBAR = "#FFA53A"
CARTAO = "#0B1824"
SELO_BG = "#1E2A44"
TEAL = "#5FC4B6"
# peles (desenho, opacas)
PELE1 = ("#D9937A", "#F0B49A", "#F7CDB8", "#F0B49A", "#D9937A"); LINHA1 = "#B9765E"
PELE2 = ("#A0694A", "#C68A62", "#D9A47E", "#C68A62", "#A0694A"); LINHA2 = "#8A5A3E"
PELE_AD = ("#B98163", "#D9A07F", "#E8B998", "#D9A07F", "#B98163"); LINHA_AD = "#9A6648"
# times e roupas
AZUL = ("#2457A8", "#2F6FD0", "#4C8BE6", "#2F6FD0", "#2457A8")
BRANCO = ("#C9D3DE", "#EEF2F6", "#FFFFFF", "#EEF2F6", "#C9D3DE")
CINZA = ("#9CA6B2", "#C3CAD3", "#DCE1E7", "#C3CAD3", "#9CA6B2")
MARINHO = ("#1E2A3A", "#2C3A4E", "#3D4D63", "#2C3A4E", "#1E2A3A")
MEIA_CINZA = ("#B7C0CA", "#E3E8EE", "#F4F7FA", "#E3E8EE", "#B7C0CA")
CAQUI = ("#5E5440", "#7A6E52", "#948766", "#7A6E52", "#5E5440")          # jaqueta do adulto
CALCA = ("#4D5868", "#66748A", "#7E8CA2", "#66748A", "#4D5868")
MANGA_MAOS = ("#5F6874", "#7D8794", "#97A1AD", "#7D8794", "#5F6874")     # mangas das mãos anônimas
CHUTEIRA, CHUTEIRA_CL = "#1F2630", "#343E4C"
SOLA, CRAVO = "#E3E8EE", "#9AA5B1"
CABELO1, CABELO2, CABELO_AD = "#3A2A20", "#1E1A18", "#2B2B2B"
# campo
CEU_A, CEU_B = "#93CDEF", "#DCEFF8"
GRAMA_LONGE, GRAMA_PERTO = "#67AE55", "#3F8D3A"
FAIXA_GRAMA = "#78BE63"
MAD, MAD_CL, MAD_ESC = "#8E6646", "#A97E59", "#6E4C33"
METAL = "#8B97A5"
MOCHILA, MOCHILA_CL, MOCHILA_ESC = "#525C6B", "#6E7888", "#3A4250"     # mochila cinza (neutra: o âmbar fica só nas setas)
CASACO, CASACO_CL, CASACO_ESC = "#3F7F8C", "#5A9AA6", "#2D5F69"
PANO_A, PANO_B = "#F4F1EA", "#7AA6D8"                                   # pano listrado (gelo) e pano da tala
GELO, GELO_CL = "#CFEFFF", "#F2FBFF"
REVISTA = ("#F2C14E", "#5B8DEF", "#EEF2F6")
TIPOIA, TIPOIA_ESC = "#EDE6D6", "#C9BFA8"

# ------------------------------------------------------------------ o monitor (janela da cena)
JX0, JY0, JX1, JY1 = 28.0, 300.0, 1052.0, 1226.0
JCX, JCY = (JX0 + JX1) / 2, (JY0 + JY1) / 2
JAN = skia.Rect(JX0, JY0, JX1, JY1)
JAN_R = 26

G = 1110.0                    # chão (onde as solas encostam) no plano de lado
X_LINHA = 300.0               # a linha lateral cruza a profundidade dos jogadores aqui
VP = (430.0, 640.0)           # ponto de fuga da linha lateral (no horizonte)
HORIZ = 640.0


# ------------------------------------------------------------------ utilidades (cópia do piloto)
def _c(h, a=255):
    h = h.lstrip("#")
    return skia.ColorSetARGB(int(a), int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))


def esc_cor(h, k):
    return lerpc(h, "#000000", k)


def tons_escuros(tons, k):
    return tuple(esc_cor(c, k) for c in tons)


def janela(t, t0, t1, d_in=0.25, d_out=0.3):
    return prog(t, t0, t0 + d_in) * (1 - prog(t, t1, t1 + d_out))


def uniao(*ps):
    out = ps[0]
    for q in ps[1:]:
        out = skia.Op(out, q, skia.PathOp.kUnion_PathOp) or out
    return out


def rr_path(x0, y0, x1, y1, r):
    p = skia.Path(); p.addRRect(skia.RRect.MakeRectXY(skia.Rect(x0, y0, x1, y1), r, r)); return p


def poli(pts, fechar=True):
    p = skia.Path(); p.moveTo(*pts[0])
    for q in pts[1:]:
        p.lineTo(*q)
    if fechar:
        p.close()
    return p


def suave(pts, fechar=True):
    n = len(pts)
    p = skia.Path()
    if fechar:
        m0 = ((pts[-1][0] + pts[0][0]) / 2, (pts[-1][1] + pts[0][1]) / 2)
        p.moveTo(*m0)
        for i in range(n):
            a_, b_ = pts[i], pts[(i + 1) % n]
            p.quadTo(a_[0], a_[1], (a_[0] + b_[0]) / 2, (a_[1] + b_[1]) / 2)
        p.close()
    else:
        p.moveTo(*pts[0])
        for i in range(1, n - 1):
            a_, b_ = pts[i], pts[i + 1]
            p.quadTo(a_[0], a_[1], (a_[0] + b_[0]) / 2, (a_[1] + b_[1]) / 2)
        p.lineTo(*pts[-1])
    return p


def capsula(p0, p1, w0, w1):
    dx, dy = p1[0] - p0[0], p1[1] - p0[1]; L = math.hypot(dx, dy) or 1.0
    nx, ny = -dy / L, dx / L
    p = poli([(p0[0] + nx * w0 / 2, p0[1] + ny * w0 / 2), (p1[0] + nx * w1 / 2, p1[1] + ny * w1 / 2),
              (p1[0] - nx * w1 / 2, p1[1] - ny * w1 / 2), (p0[0] - nx * w0 / 2, p0[1] - ny * w0 / 2)])
    c0 = skia.Path(); c0.addCircle(p0[0], p0[1], w0 / 2)
    c1 = skia.Path(); c1.addCircle(p1[0], p1[1], w1 / 2)
    return uniao(p, c0, c1)


def pinta(cv, path, p0, p1, w, tons, a, linha=None, larg_linha=2.5):
    """Preenche com sombreado cilíndrico perpendicular ao eixo p0->p1 (cópia do piloto)."""
    if a <= 0:
        return
    mx, my = (p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2
    dx, dy = p1[0] - p0[0], p1[1] - p0[1]; L = math.hypot(dx, dy) or 1.0
    nx, ny = -dy / L, dx / L
    g0 = skia.Point(mx - nx * w * 0.62, my - ny * w * 0.62); g1 = skia.Point(mx + nx * w * 0.62, my + ny * w * 0.62)
    sh = skia.GradientShader.MakeLinear([g0, g1], [_c(c) for c in tons], [0.0, 0.2, 0.48, 0.8, 1.0])
    cv.drawPath(path, paint(tons[1], int(255 * a), shader=sh))
    if linha:
        cv.drawPath(path, paint(linha, int(200 * a), "stroke", larg_linha))


def ponta(cv, x, y, ang, tam, cor, a):
    p = skia.Path()
    p.moveTo(x + tam * math.cos(ang), y + tam * math.sin(ang))
    p.lineTo(x + tam * 0.75 * math.cos(ang + 2.45), y + tam * 0.75 * math.sin(ang + 2.45))
    p.lineTo(x + tam * 0.75 * math.cos(ang - 2.45), y + tam * 0.75 * math.sin(ang - 2.45))
    p.close()
    cv.drawPath(p, paint(cor, int(255 * a)))


def seta(cv, x0, y0, x1, y1, cor, a, larg=10, tam=32):
    """Seta reta com contorno escuro (cópia do piloto)."""
    if a <= 0 or math.hypot(x1 - x0, y1 - y0) < 2:
        return
    ang = math.atan2(y1 - y0, x1 - x0)
    xb, yb = x1 - tam * 0.55 * math.cos(ang), y1 - tam * 0.55 * math.sin(ang)
    cv.drawLine(x0, y0, xb, yb, paint(CARTAO, int(170 * a), "stroke", larg + 8))
    ponta(cv, x1 + 4 * math.cos(ang), y1 + 4 * math.sin(ang), ang, tam + 10, CARTAO, 0.7 * a)
    cv.drawLine(x0, y0, xb, yb, paint(cor, int(255 * a), "stroke", larg))
    ponta(cv, x1, y1, ang, tam, cor, a)


def _trim(pt, k):
    if k < 0.999:
        pe = skia.TrimPathEffect.Make(0.0, max(0.002, k))
        if pe is not None:
            pt.setPathEffect(pe)
    return pt


def ik2(a, b, L1, L2, lado):
    dx, dy = b[0] - a[0], b[1] - a[1]
    D = clamp(math.hypot(dx, dy), abs(L1 - L2) + 1.0, L1 + L2 - 0.5)
    cos_a = clamp((L1 * L1 + D * D - L2 * L2) / (2 * L1 * D), -1.0, 1.0)
    ang = math.atan2(dy, dx) - lado * math.acos(cos_a)
    j = (a[0] + L1 * math.cos(ang), a[1] + L1 * math.sin(ang))
    ang2 = math.atan2(b[1] - j[1], b[0] - j[0])
    return j, (j[0] + L2 * math.cos(ang2), j[1] + L2 * math.sin(ang2))


def lerp2(p, q, k):
    return (lerp(p[0], q[0], k), lerp(p[1], q[1], k))


def lerp3(p, q, k):
    return tuple(lerp(p[i], q[i], k) for i in range(len(p)))


def rot2(v, graus):
    r = math.radians(graus); c, s = math.cos(r), math.sin(r)
    return (v[0] * c - v[1] * s, v[0] * s + v[1] * c)


_CACHE = {}
LINEAR = skia.SamplingOptions(skia.FilterMode.kLinear)


def cacheado(chave, w, h, desenha):
    if chave not in _CACHE:
        sf = skia.Surface(int(w), int(h)); c = sf.getCanvas(); c.clear(skia.ColorTRANSPARENT)
        desenha(c)
        _CACHE[chave] = sf.makeImageSnapshot()
    return _CACHE[chave]


def aplica(cv, cam):
    s, fx, fy = cam
    cv.translate(JCX, JCY); cv.scale(s, s); cv.translate(-fx, -fy)


def na_tela(cam, x, y):
    s, fx, fy = cam
    return JCX + (x - fx) * s, JCY + (y - fy) * s


def chaves(t, keys):
    """Interpola dicts de pose entre quadros-chave [(t, dict)] (suave). Tuplas e números."""
    if t <= keys[0][0]:
        return dict(keys[0][1])
    for (t0, p0), (t1, p1) in zip(keys, keys[1:]):
        if t < t1:
            u = e_inout(prog(t, t0, t1))
            out = {}
            for k_, v0 in p0.items():
                v1 = p1.get(k_, v0)
                if isinstance(v0, tuple):
                    out[k_] = lerp2(v0, v1, u) if len(v0) == 2 else lerp3(v0, v1, u)
                elif isinstance(v0, (int, float)) and not isinstance(v0, bool):
                    out[k_] = lerp(v0, v1, u)
                else:
                    out[k_] = v1 if u >= 0.5 else v0
            return out
    return dict(keys[-1][1])


def completa(keys):
    """Cada quadro-chave herda os campos do anterior (só escrevo o que muda)."""
    out, ult = [], {}
    for t, d in keys:
        ult = dict(ult); ult.update(d); out.append((t, ult))
    return out


# ================================================================== CENÁRIO: o campinho (de lado)
CAMPO_X0, CAMPO_Y0, CAMPO_X1, CAMPO_Y1, CAMPO_ESC = -420.0, 150.0, 1460.0, 1520.0, 1.5


def campo(cv):
    def _d(c):
        c.scale(CAMPO_ESC, CAMPO_ESC); c.translate(-CAMPO_X0, -CAMPO_Y0); _campo(c)
    img = cacheado("campo", (CAMPO_X1 - CAMPO_X0) * CAMPO_ESC, (CAMPO_Y1 - CAMPO_Y0) * CAMPO_ESC, _d)
    cv.save(); cv.translate(CAMPO_X0, CAMPO_Y0); cv.scale(1 / CAMPO_ESC, 1 / CAMPO_ESC)
    cv.drawImage(img, 0, 0, LINEAR)
    cv.restore()


def _campo(cv):
    sh = skia.GradientShader.MakeLinear([skia.Point(0, 150), skia.Point(0, HORIZ)], [_c(CEU_A), _c(CEU_B)])
    cv.drawRect(skia.Rect(-600, -200, 1700, HORIZ + 2), paint(CEU_A, shader=sh))
    # nuvens baixas
    for (x, y, r) in ((-120, 330, 60), (-40, 320, 80), (60, 336, 56), (760, 300, 64), (850, 286, 86), (950, 306, 60)):
        cv.drawCircle(x, y, r, paint("#FFFFFF", 150))
    # árvores ao longe
    rng = np.random.default_rng(5)
    for i in range(30):
        x = -500 + i * 75 + rng.uniform(-20, 20); r = rng.uniform(46, 80)
        cv.drawCircle(x, HORIZ - 52 - rng.uniform(0, 26), r, paint(lerpc("#7FAE8A", "#5D8F70", rng.uniform(0, 1))))
    # alambrado: postes, travessa, tela
    cv.save()
    tela = skia.Path(); tela.addRect(skia.Rect(-600, HORIZ - 118, 1700, HORIZ - 4))
    cv.clipPath(tela, skia.ClipOp.kIntersect, True)
    for x in range(-600, 1700, 22):
        cv.drawLine(x, HORIZ - 118, x + 114, HORIZ - 4, paint("#D7E1E8", 120, "stroke", 2))
        cv.drawLine(x + 114, HORIZ - 118, x, HORIZ - 4, paint("#D7E1E8", 120, "stroke", 2))
    cv.restore()
    cv.drawLine(-600, HORIZ - 118, 1700, HORIZ - 118, paint("#AEB9C4", 255, "stroke", 6))
    for x in range(-560, 1700, 190):
        cv.drawRect(skia.Rect(x, HORIZ - 124, x + 9, HORIZ), paint("#97A3AF"))
    # gol pequeno ao longe (à direita)
    gx0, gx1, gy0 = 1010, 1150, HORIZ - 62
    cv.drawRect(skia.Rect(gx0, gy0, gx1, HORIZ), paint("#FFFFFF", 50))
    for x in range(gx0, gx1, 12):
        cv.drawLine(x, gy0, x, HORIZ, paint("#FFFFFF", 70, "stroke", 1.2))
    cv.drawLine(gx0, gy0, gx0, HORIZ + 4, paint("#FFFFFF", 255, "stroke", 6))
    cv.drawLine(gx1, gy0, gx1, HORIZ + 4, paint("#FFFFFF", 255, "stroke", 6))
    cv.drawLine(gx0, gy0, gx1, gy0, paint("#FFFFFF", 255, "stroke", 6))
    # gramado com as faixas do corte (mais largas perto)
    shg = skia.GradientShader.MakeLinear([skia.Point(0, HORIZ), skia.Point(0, 1500)], [_c(GRAMA_LONGE), _c(GRAMA_PERTO)])
    cv.drawRect(skia.Rect(-600, HORIZ, 1700, 1700), paint(GRAMA_LONGE, shader=shg))
    y, k = HORIZ, 0
    while y < 1700:
        hb = 10 + 9 * k ** 1.25
        if k % 2 == 0:
            cv.drawRect(skia.Rect(-600, y, 1700, y + hb), paint(FAIXA_GRAMA, 70))
        y += hb; k += 1
    # tufos de grama
    for i in range(260):
        x = rng.uniform(-600, 1700); yy = rng.uniform(HORIZ + 30, 1500)
        h_ = 4 + 10 * (yy - HORIZ) / 860
        cv.drawLine(x, yy, x - 2, yy - h_, paint("#2F7A2E", 120, "stroke", 1.6 + 1.5 * (yy - HORIZ) / 860))
    cv.drawRect(skia.Rect(-600, HORIZ, 1700, HORIZ + 8), paint("#000000", 30, blur=6))


def linha_lateral_pts(y):
    """x da linha lateral na altura y do gramado (reta que vai ao ponto de fuga)."""
    return X_LINHA + (VP[0] - X_LINHA) * (G - y) / (G - VP[1])


def linha_lateral(cv, a=1.0):
    pts = []
    for y0, y1 in ((HORIZ + 6, 1500),):
        x0, x1 = linha_lateral_pts(y0), linha_lateral_pts(y1)
        w0 = 3.0; w1 = 3.0 + 34 * (y1 - HORIZ) / (1500 - HORIZ)
        pts = [(x0 - w0, y0), (x0 + w0, y0), (x1 + w1, y1), (x1 - w1, y1)]
    cv.drawPath(poli(pts), paint("#FFFFFF", int(225 * a)))


def sombra(cv, x, larg, a=1.0, y=G):
    cv.drawOval(skia.Rect(x - larg / 2, y - 10, x + larg / 2, y + 10), paint("#000000", int(60 * a), blur=8))


# ================================================================== PESSOAS (de perfil, sem rosto)
# Desenho do piloto (proporções de adulto) em coordenadas LOCAIS; cada pessoa é desenhada com escala k e
# espelho em volta do quadril. As poses são dadas no MUNDO (onde as coisas estão de fato).
COXA, CANELA, TRONCO, BRACO, ANTEB = 232.0, 222.0, 245.0, 148.0, 150.0
TORN = 32.0                                         # tornozelo acima da sola (local)

KID1 = dict(k=0.6, hr=64, pele=PELE1, linha=LINHA1, camisa=AZUL, short=BRANCO, meia=AZUL, faixa="#FFFFFF",
            calcado="chuteira", cabelo=CABELO1, gola="#FFFFFF", manga="curta", calca=None)
KID2 = dict(k=0.6, hr=64, pele=PELE2, linha=LINHA2, camisa=CINZA, short=MARINHO, meia=MEIA_CINZA, faixa="#2C3A4E",
            calcado="chuteira", cabelo=CABELO2, gola="#2C3A4E", manga="curta", calca=None)
ADULTO = dict(k=0.95, hr=52, pele=PELE_AD, linha=LINHA_AD, camisa=CAQUI, short=CALCA, meia=None, faixa=None,
              calcado="tenis", cabelo=CABELO_AD, gola=None, manga="longa", calca=CALCA)


def para_local(p, hip, k, mir):
    return (hip[0] + (p[0] - hip[0]) * mir / k, hip[1] + (p[1] - hip[1]) / k)


def para_mundo(q, hip, k, mir):
    return (hip[0] + (q[0] - hip[0]) * k * mir, hip[1] + (q[1] - hip[1]) * k)


def corpo_local(pl, hr):
    hip = pl["hip"]; al = pl["al"]
    up = (math.sin(al), -math.cos(al)); fw = (math.cos(al), math.sin(al))
    sh = (hip[0] + up[0] * TRONCO, hip[1] + up[1] * TRONCO)
    head = (sh[0] + up[0] * (hr + 28) + fw[0] * 10, sh[1] + up[1] * (hr + 28) + fw[1] * 10)
    ombro = (sh[0] - up[0] * 16 + fw[0] * 4, sh[1] - up[1] * 16 + fw[1] * 4)
    kN, aN = ik2(hip, pl["ankN"], COXA, CANELA, 1)
    kF, aF = ik2(hip, pl["ankF"], COXA, CANELA, 1)
    eN, hN = ik2(ombro, pl["mN"], BRACO, ANTEB * pl.get("ante_k", 1.0), pl.get("ladoN", -1))   # ante_k<1: escorço
    eF, hF = ik2((ombro[0] - 6, ombro[1] - 4), pl["mF"], BRACO, ANTEB, -1)
    return dict(hip=hip, al=al, up=up, fw=fw, sh=sh, head=head, ombro=ombro, kN=kN, aN=aN, kF=kF, aF=aF,
                eN=eN, hN=hN, eF=eF, hF=hF)


def pose_local(pose, est):
    k, mir, hip = est["k"], pose.get("mir", 1), pose["hip"]
    pl = dict(pose)
    for ch in ("ankN", "ankF", "mN", "mF"):
        pl[ch] = para_local(pose[ch], hip, k, mir)
    return pl


def juntas(pose, est):
    """Juntas da pessoa no MUNDO (para marcar coisas na tela)."""
    k, mir, hip = est["k"], pose.get("mir", 1), pose["hip"]
    b = corpo_local(pose_local(pose, est), est["hr"])
    out = {}
    for ch, v in b.items():
        out[ch] = para_mundo(v, hip, k, mir) if isinstance(v, tuple) and ch not in ("up", "fw") else v
    if pose.get("kink"):
        out["meio"], out["mao"] = antebraco_pts(b, pose["kink"])
        out["meio"] = para_mundo(out["meio"], hip, k, mir); out["mao"] = para_mundo(out["mao"], hip, k, mir)
    return out


def shin_frame(knee, ank):
    dx, dy = ank[0] - knee[0], ank[1] - knee[1]; L = math.hypot(dx, dy) or 1.0
    d = (dx / L, dy / L); f = (d[1], -d[0])
    return d, f, L


def canela_path(knee, ank, incha=0.0):
    """Canela de perfil (cópia do piloto) + `incha`: o contorno do tornozelo fica mais cheio."""
    d, f, L = shin_frame(knee, ank)
    fr, tr = [], []
    for i in range(15):
        s = i / 14
        wf = lerp(29, 19, s)
        wb = 30 + 15 * math.sin(math.pi * clamp(s / 0.7)) ** 1.3 - 9 * s
        bump = incha * math.exp(-((s - 0.93) / 0.13) ** 2)
        wf += 20 * bump; wb += 24 * bump
        c = (knee[0] + d[0] * L * s, knee[1] + d[1] * L * s)
        fr.append((c[0] + f[0] * wf, c[1] + f[1] * wf)); tr.append((c[0] - f[0] * wb, c[1] - f[1] * wb))
    p = poli(fr + tr[::-1])
    kk = skia.Path(); kk.addCircle(knee[0], knee[1], 30)
    a = skia.Path(); a.addCircle(ank[0], ank[1], 20 + 27 * incha)
    out = uniao(p, kk, a)
    if incha > 0:                                        # o volume desce para o peito do pé e o calcanhar
        o = skia.Path(); o.addOval(skia.Rect(ank[0] - 30 - 22 * incha, ank[1] - 22 - 18 * incha,
                                             ank[0] + 34 + 22 * incha, ank[1] + 22 + 14 * incha))
        if incha > 0.05:
            out = uniao(out, o)
    return out


def pe_path(ank):
    x, y = ank
    p = skia.Path()
    p.moveTo(x - 16, y - 16)
    p.cubicTo(x - 32, y - 2, x - 36, y + 22, x - 26, y + 31)
    p.lineTo(x + 98, y + 32)
    p.cubicTo(x + 124, y + 32, x + 126, y + 16, x + 110, y + 12)
    p.cubicTo(x + 72, y + 2, x + 34, y - 10, x + 18, y - 20)
    p.close()
    return p


def pe_descalco_path(ank):
    """(revisão) Pé DESCALÇO de perfil, apontando para +x: calcanhar redondo, arco da planta, bola do pé,
    dedão com a ponta arredondada e os dedinhos aparecendo embaixo (antes era um cone, 'casco')."""
    x, y = ank
    p = skia.Path()
    p.moveTo(x - 14, y - 22)                                         # atrás do tornozelo (tendão)
    p.cubicTo(x - 20, y - 6, x - 36, y + 4, x - 34, y + 20)          # calcanhar
    p.cubicTo(x - 32, y + 33, x - 14, y + 36, x + 2, y + 32)         # base do calcanhar
    p.cubicTo(x + 20, y + 27, x + 40, y + 27, x + 58, y + 32)        # arco da planta
    p.cubicTo(x + 80, y + 37, x + 100, y + 36, x + 116, y + 31)      # bola do pé até a ponta
    p.cubicTo(x + 129, y + 27, x + 129, y + 12, x + 116, y + 10)     # ponta do dedão
    p.cubicTo(x + 96, y + 7, x + 74, y + 1, x + 46, y - 9)           # peito do pé
    p.cubicTo(x + 30, y - 15, x + 20, y - 22, x + 14, y - 24)        # frente do tornozelo
    p.close()
    dedos = []
    for (dx, dy, r) in ((105, 29, 8.5), (94, 31, 7.5), (84, 32, 6.5)):  # os dedinhos (por baixo do dedão)
        c = skia.Path(); c.addCircle(x + dx, y + dy, r); dedos.append(c)
    return uniao(p, *dedos)


def pe_descalco(cv, ank, tons, linha, a=1.0):
    """(local, já girado) O pé descalço: pele, vinco do dedão, unha e o ossinho do tornozelo."""
    x, y = ank
    p = pe_descalco_path(ank)
    pinta(cv, p, (x + 40, y - 20), (x + 40, y + 40), 60, tons, a, linha=linha)
    cv.drawPath(suave([(x + 103, y + 12), (x + 100, y + 20), (x + 103, y + 27)], fechar=False),
                paint(linha, int(170 * a), "stroke", 2.2))                                     # vinco do dedão
    unha = skia.RRect.MakeRectXY(skia.Rect(x + 110, y + 11, x + 123, y + 19), 4, 4)
    cv.drawRRect(unha, paint("#F8E2D6", int(235 * a))); cv.drawRRect(unha, paint(linha, int(150 * a), "stroke", 1.6))
    cv.drawCircle(x + 2, y - 3, 9, paint(tons[2], int(150 * a)))                                # ossinho do tornozelo
    cv.drawArc(skia.Rect(x - 7, y - 12, x + 11, y + 6), 200, 150, False, paint(linha, int(120 * a), "stroke", 1.8))


def pe_desenho(cv, ank, rot, tons, linha, calcado, a=1.0, longe=False):
    """Pé de perfil, girado `rot` graus em volta do tornozelo (peça rígida: só gira)."""
    cv.save(); cv.translate(ank[0], ank[1]); cv.rotate(rot); cv.translate(-ank[0], -ank[1])
    if calcado not in ("chuteira", "tenis"):
        pe_descalco(cv, ank, tons, linha, a)
        cv.restore()
        return
    p = pe_path(ank); x, y = ank
    if calcado in ("chuteira", "tenis"):
        base = CHUTEIRA if calcado == "chuteira" else "#434A55"
        if longe:
            base = esc_cor(base, 0.15)
        if calcado == "chuteira":                          # cravos por baixo da sola
            for xo in (-14, 12, 54, 86):
                cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(x + xo, y + 28, x + xo + 14, y + 42), 3, 3),
                             paint(CRAVO if not longe else esc_cor(CRAVO, 0.2), int(255 * a)))
        sh = skia.GradientShader.MakeLinear([skia.Point(0, y - 20), skia.Point(0, y + 32)],
                                            [_c(CHUTEIRA_CL if calcado == "chuteira" else "#5A626E"), _c(base)])
        cv.drawPath(p, paint(base, int(255 * a), shader=sh))
        cv.save(); cv.clipPath(p, skia.ClipOp.kIntersect, True)
        cv.drawRect(skia.Rect(x - 50, y + 22, x + 140, y + 40), paint(SOLA if not longe else esc_cor(SOLA, 0.2), int(255 * a)))
        listra = suave([(x - 20, y + 12), (x + 20, y + 6), (x + 64, y + 14)], fechar=False)
        cv.drawPath(listra, paint("#FFFFFF" if not longe else "#C9D2DB", int(230 * a), "stroke", 6))
        cv.restore()
        for u in (0.36, 0.52, 0.68):                       # cadarço
            px_, py_ = lerp(x + 18, x + 110, u), lerp(y - 20, y + 12, u)
            cv.drawLine(px_ - 4, py_ + 2, px_ + 6, py_ + 9, paint("#FFFFFF", int(200 * a), "stroke", 3))
        cv.drawPath(p, paint("#0B0F14", int(160 * a), "stroke", 2.2))
    else:
        pinta(cv, p, (x + 40, y - 20), (x + 40, y + 40), 60, tons, a, linha=linha)
    cv.restore()


def contorno_pe_canela(knee, ank, rot):
    """(local) Canela + pé descalço girado: o contorno NORMAL do tornozelo."""
    pe = pe_descalco_path(ank); m = skia.Matrix(); m.setRotate(rot, ank[0], ank[1]); pe.transform(m)
    return uniao(canela_path(knee, ank, 0.0), pe)


INCHA_G, INCHA_R = 0.95, 48.0                  # quanto o contorno estufa e até onde (local)


def incha_path(knee, ank, rot, incha):
    """(revisão) O tornozelo INTEIRO engrossa por igual: o próprio contorno normal (canela + pé) é empurrado para
    fora a partir do tornozelo, muito perto dele e cada vez menos longe (dedos e joelho não mudam). Mesma cor de pele."""
    base = contorno_pe_canela(knee, ank, rot)
    pm = skia.PathMeasure(base, True)
    melhor, L = None, 0.0
    while True:
        Lc = pm.getLength()
        if Lc > L:
            L = Lc; pts = []
            n = 360
            for i in range(n):
                r = pm.getPosTan(Lc * i / n)
                if r:
                    pts.append((r[0].x(), r[0].y()))
            melhor = pts
        if not pm.nextContour():
            break
    c = (ank[0] + 4, ank[1] - 4)
    out = []
    for (x, y) in melhor:
        dx, dy = x - c[0], y - c[1]; rr = math.hypot(dx, dy)
        g = incha * INCHA_G * math.exp(-(rr / INCHA_R) ** 2)
        out.append((x + dx * g, y + dy * g))
    bola = skia.Path(); bola.addCircle(ank[0] - 6, ank[1] + 2, 39 * incha)                # tapa o vinco do tornozelo
    return uniao(suave(out), bola)


def incha_mundo(pose, est):
    """O contorno inchado no MUNDO (para as setas encostarem nele)."""
    k, mir, hip = est["k"], pose.get("mir", 1), pose["hip"]
    b = corpo_local(pose_local(pose, est), est["hr"])
    p = incha_path(b["kN"], b["aN"], pose.get("rotN", 0.0), pose.get("incha", 0.0))
    m = skia.Matrix(); m.setTranslate(-hip[0], -hip[1]); m.postScale(k * mir, k); m.postTranslate(hip[0], hip[1])
    p.transform(m)
    return p


def meia(cv, knee, ank, tons, faixa, a=1.0):
    """Meião do time sobre a canela (do joelho para baixo), com duas faixas no alto."""
    d, f, L = shin_frame(knee, ank)
    can = canela_path(knee, ank)
    c0 = (knee[0] + d[0] * L * 0.15, knee[1] + d[1] * L * 0.15)
    meio = poli([(c0[0] + f[0] * 200, c0[1] + f[1] * 200), (c0[0] - f[0] * 200, c0[1] - f[1] * 200),
                 (c0[0] - f[0] * 200 + d[0] * 600, c0[1] - f[1] * 200 + d[1] * 600),
                 (c0[0] + f[0] * 200 + d[0] * 600, c0[1] + f[1] * 200 + d[1] * 600)])
    m = skia.Op(can, meio, skia.PathOp.kIntersect_PathOp)
    if m is None:
        return
    pinta(cv, m, knee, ank, 70, tons, a, linha=esc_cor(tons[0], 0.3))
    if faixa:
        cv.save(); cv.clipPath(m, skia.ClipOp.kIntersect, True)
        for s in (0.22, 0.29):
            c = (knee[0] + d[0] * L * s, knee[1] + d[1] * L * s)
            cv.drawLine(c[0] + f[0] * 80, c[1] + f[1] * 80, c[0] - f[0] * 80, c[1] - f[1] * 80, paint(faixa, int(255 * a), "stroke", 12))
        cv.restore()


def perna(cv, hip, knee, ank, est, a, rot=0.0, longe=False, descalco=False, sem_meia=False, incha=0.0, so=None):
    tp = tons_escuros(est["pele"], 0.16) if longe else est["pele"]
    calca = est.get("calca")
    tc = (tons_escuros(calca, 0.16) if longe else calca) if calca else None
    ts = tons_escuros(est["short"], 0.15) if longe else est["short"]
    lin = esc_cor(tp[0], 0.25)
    if so in (None, "coxa"):
        coxa = capsula(hip, knee, 78, 60)
        pinta(cv, coxa, hip, knee, 78, tc or tp, a, linha=esc_cor((tc or tp)[0], 0.25))
        m = lerp2(hip, knee, 0.5 if not calca else 0.3)
        pinta(cv, capsula(hip, m, 90, 82), hip, m, 90, ts, a, linha=esc_cor(ts[0], 0.3))
    if so in (None, "canela"):
        pinta(cv, canela_path(knee, ank, 0.0), knee, ank, 70, tc or tp, a, linha=lin if not tc else esc_cor(tc[0], 0.25))
        if est.get("meia") and not sem_meia:
            tm = tons_escuros(est["meia"], 0.16) if longe else est["meia"]
            meia(cv, knee, ank, tm, est["faixa"], a)
        calc = None if descalco else est["calcado"]
        pe_desenho(cv, ank, rot, tp, lin, calc, a, longe)
        if incha > 0.01:                                  # (revisão) o inchaço cobre o tornozelo por cima do pé
            pinta(cv, incha_path(knee, ank, rot, incha), knee, ank, 70, tp, a * clamp(incha * 5), linha=lin)


def mao(cv, p, dirx, diry, garra, tons, a, linha):
    """Mão: punho fechado (garra 1) ou aberta, espalmada (garra 0) — cópia do piloto."""
    L = math.hypot(dirx, diry) or 1.0; ux, uy = dirx / L, diry / L
    comp = lerp(30, 6, garra); larg = lerp(27, 44, garra)
    q0 = (p[0] - ux * comp * 0.5, p[1] - uy * comp * 0.5); q1 = (p[0] + ux * comp * 0.5, p[1] + uy * comp * 0.5)
    pth = capsula(q0, q1, larg, larg * lerp(0.85, 1.0, garra))
    if garra > 0.3:
        nx, ny = -uy, ux
        pol = capsula((p[0] - ux * 6 + nx * 12, p[1] - uy * 6 + ny * 12), (p[0] + ux * 10 + nx * 16, p[1] + uy * 10 + ny * 16), 16, 14)
        pth = uniao(pth, pol)
    pinta(cv, pth, q0, q1, larg, tons, a, linha=linha, larg_linha=2)


def antebraco_pts(b, kink):
    """Com o antebraço 'torto' (kink graus), o meio fica onde está e a metade da mão gira."""
    cot, hN = b["eN"], b["hN"]
    meio = lerp2(cot, hN, 0.5)
    v = (hN[0] - meio[0], hN[1] - meio[1])
    v = rot2(v, kink)
    return meio, (meio[0] + v[0], meio[1] + v[1])


def braco(cv, ombro, cot, mao_p, garra, est, a, longe=False, kink=0.0, b=None):
    tp = tons_escuros(est["pele"], 0.16) if longe else est["pele"]
    tc = tons_escuros(est["camisa"], 0.16) if longe else est["camisa"]
    lin = esc_cor(tp[0], 0.25)
    longa = est.get("manga") == "longa"
    up = capsula(ombro, cot, 40, 34)
    pinta(cv, up, ombro, cot, 40, tc if longa else tp, a, linha=esc_cor((tc if longa else tp)[0], 0.25))
    if kink:
        meio = lerp2(cot, mao_p, 0.5)
        v = rot2((mao_p[0] - meio[0], mao_p[1] - meio[1]), kink)
        mao_p = (meio[0] + v[0], meio[1] + v[1])
        pulso = lerp2(meio, mao_p, 0.64)
        fo = uniao(capsula(cot, meio, 34, 31), capsula(meio, pulso, 31, 27))
    else:
        pulso = lerp2(cot, mao_p, 0.82)
        fo = capsula(cot, pulso, 34, 27)
    pinta(cv, fo, cot, pulso, 34, tc if longa else tp, a, linha=esc_cor((tc if longa else tp)[0], 0.25))
    if not longa:
        mg = lerp2(ombro, cot, 0.52)
        pinta(cv, capsula(ombro, mg, 54, 48), ombro, mg, 54, tc, a, linha=esc_cor(tc[0], 0.3))
    else:
        cv.drawPath(capsula(lerp2(cot, pulso, 0.86), pulso, 30, 30), paint(esc_cor(tc[0], 0.2), int(255 * a)))
    mao(cv, mao_p, mao_p[0] - pulso[0], mao_p[1] - pulso[1], garra, tp, a, lin)
    return mao_p


def cabeca(cv, head, al, up, fw, a, hr, cabelo, tons):
    sh_c = skia.GradientShader.MakeRadial(skia.Point(head[0] + fw[0] * 14 + up[0] * 12, head[1] + fw[1] * 14 + up[1] * 12),
                                          hr * 1.4, [_c(tons[2]), _c(tons[1]), _c(tons[0])], [0.0, 0.55, 1.0])
    cv.drawCircle(head[0], head[1], hr, paint(tons[1], int(255 * a), shader=sh_c))
    cv.drawCircle(head[0], head[1], hr, paint(esc_cor(tons[0], 0.2), int(180 * a), "stroke", 2.5))
    cv.save(); cv.translate(head[0], head[1]); cv.rotate(math.degrees(al)); cv.scale(hr / 50, hr / 50)
    cab = skia.Path(); cab.addCircle(0, 0, 53)
    cl = skia.Path(); cl.moveTo(-70, 30); cl.lineTo(-70, -70); cl.lineTo(30, -70); cl.lineTo(22, -24)
    cl.cubicTo(6, -18, -14, -6, -22, 30); cl.close()
    cab = skia.Op(cab, cl, skia.PathOp.kIntersect_PathOp)
    if cab is not None:
        cv.drawPath(cab, paint(cabelo, int(255 * a)))
    cv.restore()


def tronco_cabeca(cv, b, est, a):
    hip, sh, up, fw, head = b["hip"], b["sh"], b["up"], b["fw"], b["head"]
    tp, tc, ts = est["pele"], est["camisa"], est["short"]
    pes = (sh[0] + up[0] * 40, sh[1] + up[1] * 40)
    pinta(cv, capsula(sh, pes, 40, 38), sh, pes, 40, tp, a)
    tr = capsula((hip[0] + up[0] * 20, hip[1] + up[1] * 20), (sh[0] - up[0] * 12, sh[1] - up[1] * 12), 112, 120)
    pinta(cv, tr, hip, sh, 120, tc, a, linha=esc_cor(tc[0], 0.3))
    if est.get("gola"):
        g0 = (sh[0] + up[0] * 2 - fw[0] * 18, sh[1] + up[1] * 2 - fw[1] * 18)
        g1 = (sh[0] + up[0] * 2 + fw[0] * 20, sh[1] + up[1] * 2 + fw[1] * 20)
        cv.drawLine(g0[0], g0[1], g1[0], g1[1], paint(est["gola"], int(255 * a), "stroke", 9))
    q = (hip[0] + up[0] * 46, hip[1] + up[1] * 46)
    pinta(cv, capsula(hip, q, 108, 112), hip, q, 112, ts, a, linha=esc_cor(ts[0], 0.3))
    cabeca(cv, head, b["al"], up, fw, a, est["hr"], est["cabelo"], tp)


def pessoa(cv, pose, est, a=1.0, partes="tudo", ganchos=None):
    """Desenha a pessoa (camadas: braço de lá, perna de lá, tronco, coxa de cá, canela de cá, braço de cá).
    `ganchos`: {camada: fn(cv, b)} chamados em coordenadas LOCAIS (dentro da escala da pessoa)."""
    ganchos = ganchos or {}
    k, mir, hip = est["k"], pose.get("mir", 1), pose["hip"]
    pl = pose_local(pose, est)
    b = corpo_local(pl, est["hr"])
    cv.save(); cv.translate(hip[0], hip[1]); cv.scale(k * mir, k); cv.translate(-hip[0], -hip[1])
    if partes in ("tudo", "sem_braco"):
        braco(cv, (b["ombro"][0] - 6, b["ombro"][1] - 4), b["eF"], b["hF"], pose.get("gF", 0.0), est, a, longe=True)
        if "longe" in ganchos:
            ganchos["longe"](cv, b)
        perna(cv, b["hip"], b["kF"], b["aF"], est, a, rot=pose.get("rotF", 0.0), longe=True,
              descalco=pose.get("descalcoF", False))
        tronco_cabeca(cv, b, est, a)
        if "tronco" in ganchos:
            ganchos["tronco"](cv, b)
        perna(cv, b["hip"], b["kN"], b["aN"], est, a, so="coxa")
        if "coxa" in ganchos:
            ganchos["coxa"](cv, b)
        perna(cv, b["hip"], b["kN"], b["aN"], est, a, rot=pose.get("rotN", 0.0), descalco=pose.get("descalcoN", False),
              sem_meia=pose.get("sem_meiaN", False), incha=pose.get("incha", 0.0), so="canela")
        if "perna" in ganchos:
            ganchos["perna"](cv, b)
    if partes in ("tudo", "so_braco"):
        if "antes_braco" in ganchos:
            ganchos["antes_braco"](cv, b)
        braco(cv, b["ombro"], b["eN"], b["hN"], pose.get("gN", 0.0), est, a, kink=pose.get("kink", 0.0), b=b)
        if "braco" in ganchos:
            ganchos["braco"](cv, b)
    cv.restore()
    return b


# ------------------------------------------------------------------ marcha (pés plantados no chão)
def marcha(x_hip, x0, direc, passo, base_y, ank_y, apoio=0.6, lift=60.0, bob=8.0):
    """Pés de quem anda (ou corre) com o quadril em x_hip, saindo de x0 na direção `direc` (+1/-1).
    Fração `apoio` do ciclo com o pé plantado (no mundo). Devolve (hip_y, ankN, ankF, rotN, rotF, fase)."""
    ciclo = passo / apoio
    dist = abs(x_hip - x0)
    out = []
    for desloc in (0.0, 0.5):
        u = (dist / ciclo + desloc) % 1.0
        if u < apoio:
            off = passo / 2 - u * ciclo
            y = ank_y; rot = 0.0
            if u > apoio - 0.12:
                rot = -18 * (u - (apoio - 0.12)) / 0.12            # calcanhar sobe antes de sair
        else:
            w = (u - apoio) / (1 - apoio)
            off = lerp(-passo / 2, passo / 2, e_inout(w))
            y = ank_y - lift * math.sin(math.pi * w)
            rot = lerp(-18, 6, w)
        out.append(((x_hip + direc * off, y), rot))
    fase = (dist / ciclo) % 0.5
    hip_y = base_y - bob * abs(math.sin(2 * math.pi * fase))
    (aN, rN), (aF, rF) = out
    return hip_y, aN, aF, rN, rF, dist / ciclo


# ================================================================== LANCE 1 (close de frente): o pé vira na bola
BOLA_C, BOLA_R = (650.0, 1044.0), 74.0
ANK_FRENTE_L = (372.0, 1006.0)                 # tornozelo da perna de apoio (a da esquerda da tela)
JOELHO_L, JOELHO_R = (382.0, 548.0), (690.0, 540.0)
ANK_ALTO = (662.0, 772.0)                      # pé no ar, antes de pisar
ANK_PISA = (664.0, 862.0)                      # pé pisando em cima da bola
ANK_VIRA = (712.0, 902.0)                      # o tornozelo cai para fora quando o pé vira
GIRO_VIRA = 30.0


def estado_frente(t, T):
    """(tornozelo, giro do calçado em graus, giro da bola) do close."""
    var, tc, pe_f = T["var"], T["torceu"], T["pe1_fim"]
    if t < var:                                        # quadro 0: já virado, congelado
        return ANK_VIRA, GIRO_VIRA, 0.0
    if t < var + 0.5:                                  # rebobina: desvira e sobe
        u = e_inout(prog(t, var, var + 0.5))
        if u < 0.5:
            k = u / 0.5
            return lerp2(ANK_VIRA, ANK_PISA, k), lerp(GIRO_VIRA, 0.0, k), -10 * k
        k = (u - 0.5) / 0.5
        return lerp2(ANK_PISA, ANK_ALTO, k), 0.0, -10 - 8 * k
    # replay lento: desce (torceu) e vira (pé)
    desce = e_inout(prog(t, tc - 0.12, tc + 0.32))
    vira = e_out(prog(t, T["pe1"] - 0.12, pe_f + 0.05))
    ank = lerp2(ANK_ALTO, ANK_PISA, desce)
    ank = lerp2(ank, ANK_VIRA, vira)
    return ank, GIRO_VIRA * vira, -18 + 18 * desce + 12 * vira


def _perna_frente_path(joelho, ank, larg=1.0):
    """Canela de frente (meião): larga em cima, panturrilha, fina no tornozelo."""
    dx, dy = ank[0] - joelho[0], ank[1] - joelho[1]; L = math.hypot(dx, dy) or 1.0
    d = (dx / L, dy / L); n = (-d[1], d[0])
    esq, dir_ = [], []
    for i in range(13):
        s = i / 12
        w = (58 + 12 * math.sin(math.pi * clamp(s / 0.62)) ** 1.2) * (1 - 0.42 * s ** 1.6) * larg
        c = (joelho[0] + dx * s, joelho[1] + dy * s)
        esq.append((c[0] + n[0] * w * 1.04, c[1] + n[1] * w * 1.04)); dir_.append((c[0] - n[0] * w, c[1] - n[1] * w))
    return suave(esq + dir_[::-1])


def _chuteira_frente(cv, ank, giro, a=1.0, esc=1.0):
    """Chuteira vista de frente, peça rígida girando em volta do tornozelo (a sola aparece ao virar)."""
    cv.save(); cv.translate(ank[0], ank[1]); cv.rotate(giro); cv.scale(esc, esc)
    for xo in (-44, -17, 12, 39):                                   # cravos
        cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(xo, 112, xo + 14, 126), 3, 3), paint(CRAVO, int(255 * a)))
    corpo_ = skia.Path(); corpo_.moveTo(-40, -8)
    corpo_.cubicTo(-46, 30, -66, 70, -62, 98); corpo_.lineTo(62, 98)
    corpo_.cubicTo(66, 70, 46, 30, 40, -8); corpo_.close()
    sh = skia.GradientShader.MakeLinear([skia.Point(-60, 0), skia.Point(60, 0)],
                                        [_c("#121821"), _c(CHUTEIRA_CL), _c("#121821")], [0.0, 0.45, 1.0])
    cv.drawPath(corpo_, paint(CHUTEIRA, int(255 * a), shader=sh))
    cv.drawOval(skia.Rect(-46, 46, 46, 100), paint("#3E4958", int(230 * a)))         # bico
    cv.drawOval(skia.Rect(-30, 54, 18, 74), paint("#5A6678", int(160 * a)))          # brilho do bico
    for i in range(3):                                                                 # cadarço
        y = 6 + i * 13
        cv.drawLine(-15, y, 15, y + 4, paint("#FFFFFF", int(225 * a), "stroke", 4))
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(-66, 96, 66, 114), 8, 8), paint(SOLA, int(255 * a)))
    cv.drawPath(corpo_, paint("#0B0F14", int(170 * a), "stroke", 2.5))
    cv.restore()


def _bola(cv, c, r, giro, a=1.0):
    cv.save(); cv.translate(c[0], c[1])
    cv.drawOval(skia.Rect(-r * 1.05, r - 12, r * 1.05, r + 16), paint("#000000", int(70 * a), blur=10))
    circ = skia.Path(); circ.addCircle(0, 0, r)
    sh = skia.GradientShader.MakeRadial(skia.Point(-r * 0.35, -r * 0.4), r * 1.5, [_c("#FFFFFF"), _c("#E6EBF0"), _c("#AEB8C3")],
                                        [0.0, 0.55, 1.0])
    cv.drawPath(circ, paint("#FFFFFF", int(255 * a), shader=sh))
    cv.save(); cv.clipPath(circ, skia.ClipOp.kIntersect, True); cv.rotate(giro)

    def pent(cx, cy, rr, rot0):
        return poli([(cx + rr * math.cos(math.radians(rot0 + 72 * i - 90)), cy + rr * math.sin(math.radians(rot0 + 72 * i - 90)))
                     for i in range(5)])
    cv.drawPath(pent(0, 0, r * 0.3, 0), paint("#1F2630", int(255 * a)))
    for i in range(5):
        ang = math.radians(72 * i - 90 + 36)
        cv.drawPath(pent(math.cos(ang) * r * 0.92, math.sin(ang) * r * 0.92, r * 0.28, 36), paint("#1F2630", int(255 * a)))
        cv.drawLine(math.cos(ang - 0.63) * r * 0.3, math.sin(ang - 0.63) * r * 0.3, math.cos(ang - 0.63) * r * 0.66,
                    math.sin(ang - 0.63) * r * 0.66, paint("#8B96A3", int(200 * a), "stroke", 2))
    cv.restore()
    cv.drawPath(circ, paint("#7C8794", int(200 * a), "stroke", 2.5))
    cv.restore()


def close_frente(cv, t, T):
    """Plano fechado de frente: o short, os joelhos, os meiões, a chuteira de apoio e a que pisa na bola."""
    ank, giro, gb = estado_frente(t, T)
    push = 1.36 * (1.0 + 0.05 * e_inout(prog(t, T["torceu"] - 0.1, T["pe1_fim"] + 0.2)))
    cv.save(); cv.translate(560, 1010); cv.scale(push, push); cv.translate(-560, -1010)
    # gramado de frente (faixas horizontais, mais largas perto) e uma linha do campo ao fundo
    shg = skia.GradientShader.MakeLinear([skia.Point(0, JY0), skia.Point(0, JY1)], [_c("#5FA64F"), _c("#3E8B39")])
    cv.drawRect(skia.Rect(JX0 - 80, JY0 - 80, JX1 + 80, JY1 + 80), paint(GRAMA_LONGE, shader=shg))
    y, k = JY0 - 80, 0
    while y < JY1 + 80:
        hb = 34 + 13 * k
        if k % 2 == 0:
            cv.drawRect(skia.Rect(JX0 - 80, y, JX1 + 80, y + hb), paint(FAIXA_GRAMA, 60))
        y += hb; k += 1
    cv.drawPath(poli([(JX0 - 80, 676), (JX1 + 80, 610), (JX1 + 80, 626), (JX0 - 80, 694)]), paint("#FFFFFF", 200))
    # sombras no chão
    cv.drawOval(skia.Rect(ANK_FRENTE_L[0] - 92, 1112, ANK_FRENTE_L[0] + 92, 1140), paint("#000000", 70, blur=10))
    # short branco (bainha) no alto
    sh_ = skia.Path(); sh_.moveTo(200, JY0 - 60); sh_.lineTo(880, JY0 - 60); sh_.lineTo(866, 392)
    sh_.cubicTo(800, 404, 640, 410, 580, 398); sh_.lineTo(540, 360); sh_.lineTo(500, 398)
    sh_.cubicTo(440, 410, 300, 404, 236, 392); sh_.close()
    # coxas
    for (j, x_top) in ((JOELHO_L, 360), (JOELHO_R, 708)):
        coxa = capsula((x_top, 330), j, 168, 128)
        pinta(cv, coxa, (x_top, 330), j, 168, PELE1, 1.0, linha=LINHA1)
        cv.drawOval(skia.Rect(j[0] - 44, j[1] - 26, j[0] + 44, j[1] + 30), paint(PELE1[2], 120))   # joelho
    shs = skia.GradientShader.MakeLinear([skia.Point(200, 0), skia.Point(880, 0)],
                                         [_c("#C9D3DE"), _c("#FFFFFF"), _c("#EEF2F6"), _c("#C9D3DE")], [0, 0.3, 0.7, 1])
    cv.drawPath(sh_, paint("#FFFFFF", shader=shs))
    cv.drawPath(sh_, paint("#9AA8B6", 220, "stroke", 3))
    cv.drawLine(214, 300, 236, 392, paint(AZUL[1], 255, "stroke", 16))
    cv.drawLine(866, 300, 846, 392, paint(AZUL[1], 255, "stroke", 16))
    # perna de apoio (esquerda da tela)
    for (j, a_, giro_, longe) in ((JOELHO_L, ANK_FRENTE_L, 0.0, True), (JOELHO_R, ank, giro, False)):
        if not longe:
            _bola(cv, BOLA_C, BOLA_R, gb)
        canela = _perna_frente_path((j[0], j[1] + 34), a_)
        joelho_p = skia.Path(); joelho_p.addCircle(j[0], j[1] + 8, 56)
        pinta(cv, joelho_p, (j[0], j[1] - 50), (j[0], j[1] + 60), 112, PELE1, 1.0)
        pinta(cv, canela, (j[0] - 1, j[1]), (j[0] + 1, j[1]), 130, AZUL, 1.0, linha="#1A3F7A")
        cv.save(); cv.clipPath(canela, skia.ClipOp.kIntersect, True)
        dx, dy = a_[0] - j[0], a_[1] - j[1]; L = math.hypot(dx, dy)
        for s in (0.15, 0.21):
            c = (j[0] + dx * s, j[1] + 34 + dy * s); n = (-dy / L, dx / L)
            cv.drawLine(c[0] - n[0] * 120, c[1] - n[1] * 120 - 4, c[0] + n[0] * 120, c[1] + n[1] * 120 + 4,
                        paint("#FFFFFF", 255, "stroke", 16))
        cv.restore()
        _chuteira_frente(cv, (a_[0], a_[1] - 6), giro_)
    cv.restore()
    return ((560 + (ank[0] - 560) * push), (1010 + (ank[1] - 1010) * push)), push


# ================================================================== LANCE 1 (aberto, de lado): corre que passa?
POS_ADULTO0 = 150.0                    # o adulto espera fora do campo (à esquerda da linha lateral)
KID_HIP_Y = G - 286.0
G_FUNDO = G - 36.0                       # o adulto do lance 1 anda um pouco atrás (mais ao fundo)
AD_K = 0.76                              # (revisão) criança de 10-12 anos: a cabeça dela chega ao peito do adulto
ADULTO_L1 = dict(ADULTO, k=AD_K)
AD1_HIP_Y = G_FUNDO - AD_K * 482
AD_TORN = G_FUNDO - TORN * AD_K          # altura do tornozelo do adulto (sola no chão do fundo)
AD_PASSO = 140.0 * AD_K / 0.88


L1_X_INI, L1_X_FIM = 566.0, 112.0       # a criança sai daqui e para fora da linha lateral
L1_AD_DX = 128.0                         # o adulto vai um pouco à frente (à esquerda), sem cobrir a criança
L1_HIP_DOR = (566.0, 880.0)


def _l1_tempos(T):
    t0 = T["tira"] - 0.12
    return t0, t0 + 0.3, T["pisa"] + 0.12             # endireita, vira e anda, chegou


def pose_l1(t, T):
    """Pose da criança (KID1) no plano aberto."""
    t1 = T["corte1"]; tf = T["congela1"]
    D = tf - t1
    keys = completa([
        (t1, dict(hip=(392.0, KID_HIP_Y + 4), al=0.2, ankN=(430.0, G - 34), ankF=(352.0, G - 19), rotN=18.0, rotF=0.0,
                  mN=(350.0, KID_HIP_Y - 40), mF=(460.0, KID_HIP_Y - 110), gN=0.6, gF=0.6, mir=1, incha=0.0)),
        (t1 + 0.28 * D, dict(hip=(442.0, KID_HIP_Y + 14), al=0.12, ankN=(452.0, G - 30), ankF=(400.0, G - 64), rotN=24.0, rotF=-10.0,
                             mN=(500.0, KID_HIP_Y - 150), mF=(400.0, KID_HIP_Y - 60))),
        (t1 + 0.5 * D, dict(hip=(482.0, KID_HIP_Y + 4), al=0.2, ankN=(452.0, G - 30), ankF=(560.0, G - 50), rotN=26.0, rotF=-4.0,
                            mN=(430.0, KID_HIP_Y - 50), mF=(560.0, KID_HIP_Y - 120))),
        (t1 + 0.78 * D, dict(hip=(540.0, KID_HIP_Y + 2), al=0.14, ankN=(500.0, G - 64), ankF=(582.0, G - 19), rotN=20.0, rotF=0.0,
                             mN=(600.0, KID_HIP_Y - 140), mF=(480.0, KID_HIP_Y - 60))),
        (tf, dict(hip=(562.0, KID_HIP_Y + 10), al=0.16, ankN=(560.0, G - 56), ankF=(590.0, G - 19), rotN=22.0,
                  mN=(640.0, KID_HIP_Y - 120), mF=(500.0, KID_HIP_Y - 50))),
        # "dor que faz parar": para, dobra o corpo e leva a mão ao tornozelo (o pé machucado erguido)
        (T["dor"] - 0.05, dict()),
        (T["parar"] + 0.1, dict(hip=L1_HIP_DOR, al=1.05, ankN=(652.0, 1000.0), ankF=(588.0, G - 19), rotN=10.0,
                                mN=(652.0, 986.0), mF=(616.0, 930.0), gN=0.0, gF=0.0)),
    ])
    t0, t_vira, t_cheg = _l1_tempos(T)
    if t < t0:
        return chaves(t, keys)
    # "tira do jogo": vira para a linha lateral e vai pulando num pé só, o adulto ao lado
    u = e_inout(prog(t, t_vira, t_cheg))
    xh = lerp(L1_X_INI, L1_X_FIM, u)
    ergue = e_inout(prog(t, t0, t_vira))
    mir_ = 1 if t < t_vira else -1
    n_pulos = 4
    fase = u * n_pulos
    w = fase % 1.0 if 0 < u < 1 else 0.0
    voo = math.sin(math.pi * clamp((w - 0.45) / 0.55)) if 0 < u < 1 else 0.0
    hip_y = lerp(L1_HIP_DOR[1], KID_HIP_Y + 8, ergue) - 20 * voo
    passo = (L1_X_INI - L1_X_FIM) / n_pulos
    base_i = math.floor(fase) if u < 1 else n_pulos
    desl = passo * e_inout(clamp((w - 0.45) / 0.55)) if 0 < u < 1 else 0.0
    pe_x = L1_X_INI + 22 - passo * base_i - desl
    pe_y = G - 19 - 26 * voo
    atras = (xh - mir_ * 46, G - 100 - 18 * voo)            # o pé machucado no ar, dobrado para trás
    ankN = lerp2((652.0, 1000.0), atras, ergue) if mir_ > 0 else atras
    # depois de virar, a criança dá a mão ao adulto (à frente dela, na altura do peito)
    mao_dada = mao_do_adulto_l1(xh, hip_y)
    mN = lerp2((652.0, 986.0), (xh + mir_ * 22, hip_y + 20), ergue) if mir_ > 0 else         lerp2((xh - 22, hip_y + 20), (mao_dada[0] - 4, mao_dada[1] + 4), e_inout(prog(t, t_vira, t_vira + 0.18)))
    return dict(hip=(xh, hip_y), al=lerp(1.05, 0.14, ergue), ankF=(pe_x, pe_y), ankN=ankN, rotN=28.0, rotF=0.0,
                mN=mN, mF=(xh + mir_ * 34, hip_y + 10), gN=0.0, gF=0.0, mir=mir_, incha=0.0)


def mao_do_adulto_l1(xh, hip_y):
    """Onde as mãos se encontram: à frente da criança (que anda para a esquerda), na altura do peito."""
    return (xh - 96, hip_y - 86)


def pose_adulto_l1(t, T):
    """Adulto (cortado no ombro): espera fora da linha, vem buscar e volta ao lado da criança."""
    t_in0, t_in1 = T["anulado1"] + 0.5, T["tira"] - 0.1
    t0, t_vira, t_cheg = _l1_tempos(T)
    x_ao_lado = L1_X_INI - L1_AD_DX
    if t < t_in0:
        x = POS_ADULTO0; direc = 1; anda = False; x_ref = POS_ADULTO0
    elif t < t_in1:
        x = lerp(POS_ADULTO0, x_ao_lado, e_inout(prog(t, t_in0, t_in1))); direc = 1; anda = True; x_ref = POS_ADULTO0
    elif t < t_vira:
        x = x_ao_lado; direc = 1; anda = False; x_ref = x_ao_lado
    else:
        u = e_inout(prog(t, t_vira, t_cheg))
        x = lerp(x_ao_lado, L1_X_FIM - L1_AD_DX, u); direc = -1; anda = 0 < u < 1; x_ref = x_ao_lado
    if anda:
        hy, aN, aF, rN, rF, _ = marcha(x, x_ref, direc, AD_PASSO, AD1_HIP_Y, AD_TORN, apoio=0.6, lift=36.0, bob=6.0)
    else:
        hy, aN, aF, rN, rF = AD1_HIP_Y, (x + 24 * direc, AD_TORN), (x - 26 * direc, AD_TORN), 0.0, 0.0
    return dict(hip=(x, hy), al=0.06, ankN=aN, ankF=aF, rotN=rN, rotF=rF,
                mN=(x + 40 * direc, hy + 60), mF=(x - 30 * direc, hy + 60), gN=0.0, gF=0.0, mir=direc)


# (revisão) topo da janela em y≈524: o adulto sai cortado no ombro e a cabeça da criança tem folga em cima
CAM_L1_Y = 880.0
CAM_L1 = (1.3, 470.0, CAM_L1_Y)


def cam_l1(t, T, kid):
    j = juntas(kid, KID1)
    perto = (1.75, j["aN"][0] - 10, j["aN"][1] - 40)       # congela: só as pernas (a cabeça fica fora, inteira)
    cam = CAM_L1
    cam = lerp3(cam, perto, e_inout(prog(t, T["congela1"], T["congela1"] + 0.3)))
    cheg = prog(t, T["passa_fim"], T["anulado1"])
    cam = (cam[0] * (1 + 0.07 * e_inout(cheg)), cam[1], cam[2])
    segue = (1.3, clamp(kid["hip"][0] - 20, 300, 500), CAM_L1_Y)
    cam = lerp3(cam, (1.3, 480.0, CAM_L1_Y), e_inout(prog(t, T["anulado1"] + 0.35, T["dor"] + 0.25)))
    cam = lerp3(cam, segue, e_inout(prog(t, T["tira"] - 0.05, T["tira"] + 0.5)))
    jk = juntas(kid, KID1)
    pe = (1.4, jk["aN"][0] + 20, 884.0)                     # "Não pisa pra testar": chega no pé no ar, criança inteira
    return lerp3(cam, pe, e_inout(prog(t, T["pisa"], T["testar"] + 0.1)))


def placa_subst(cv, x, y, a, t):
    """Placa de substituição: só a seta de saída em LEDs verdes (nenhum número)."""
    if a <= 0:
        return
    bal = 3 * math.sin(t * 7)
    cv.save(); cv.translate(x, y + bal); cv.rotate(-3 + 1.5 * math.sin(t * 5))
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(-14, 70, 14, 230), 6, 6), paint("#2A313B", int(255 * a)))
    rr = skia.RRect.MakeRectXY(skia.Rect(-130, -82, 130, 82), 18, 18)
    cv.drawRRect(rr, paint("#000000", int(110 * a), blur=12))
    cv.drawRRect(rr, paint("#11161D", int(250 * a)))
    cv.drawRRect(rr, paint("#5B6676", int(255 * a), "stroke", 6))
    # seta de saída (para a esquerda) em pontinhos de LED
    pts = []
    for i in range(-5, 6):
        pts.append((i * 17 + 20, 0))
    for k_ in range(1, 4):
        pts.append((-65 + k_ * 17, -k_ * 17)); pts.append((-65 + k_ * 17, k_ * 17))
    pts.append((-65, 0))
    pis = 0.75 + 0.25 * math.sin(t * 12)
    for (px_, py_) in pts:
        cv.drawCircle(px_, py_, 9, paint(VERDE, int(90 * a * pis), blur=4))
        cv.drawCircle(px_, py_, 6, paint(VERDE, int(255 * a)))
    cv.restore()


def cena_l1_aberta(cv, t, T):
    kid = pose_l1(t, T)
    ad = pose_adulto_l1(t, T)
    cam = cam_l1(t, T, kid)
    cv.save(); aplica(cv, cam)
    campo(cv)
    linha_lateral(cv)
    # a bola foi embora pela direita
    kb = prog(t, T["corte1"], T["congela1"])
    if t < T["anulado1"] + 1.0:
        bx = lerp(470, 900, e_out(kb))
        _bola(cv, (bx, G - 40), 40, 400 * kb)
    sombra(cv, ad["hip"][0], 120, y=G_FUNDO)
    sombra(cv, kid["hip"][0], 110)
    pessoa(cv, ad, ADULTO_L1, partes="sem_braco")
    pessoa(cv, kid, KID1)
    # o adulto pega a criança pela mão (antes de ela virar, a mão dele espera nas costas dela, sem tocar o rosto)
    k_m = e_inout(prog(t, T["tira"] - 0.25, T["tira"] + 0.05))
    if k_m > 0:
        _, t_vira, _ = _l1_tempos(T)
        xh, hy = kid["hip"]
        costas = (xh - 44, hy - 118)
        alvo = lerp2(costas, mao_do_adulto_l1(xh, hy), e_inout(prog(t, t_vira - 0.05, t_vira + 0.18)))
        ad = dict(ad); ad["mN"] = lerp2(ad["mN"], (alvo[0] + 6, alvo[1] - 2), k_m); ad["gN"] = 0.6
        ad["ladoN"] = 1 if ad.get("mir", 1) < 0 else -1      # (revisão) o cotovelo dobra para trás, longe do rosto da criança
    pessoa(cv, ad, ADULTO_L1, partes="so_braco")
    cv.restore()
    return cam, kid


# ================================================================== LANCE 2 — o banco: massagem forte?
BANCO_Y = 948.0                         # tampo do banco
BANCO_X0, BANCO_X1 = 170.0, 900.0
MOCH = (548.0, 706.0)                   # mochila em cima do banco (x0, x1)
HIP2 = (322.0, BANCO_Y - 20)
ANK2 = (600.0, BANCO_Y - 92)            # calcanhar em cima da mochila
ANK2_ALTO = (600.0, BANCO_Y - 148)      # em cima da mochila + casaco dobrado
ROT_PE2 = -58.0                         # o pé de ponta para cima (deitado no calcanhar)


def banco(cv, parte):
    if parte == "fundo":
        cv.drawOval(skia.Rect(BANCO_X0 - 10, G - 12, BANCO_X1 + 10, G + 14), paint("#000000", 55, blur=12))
        for x0 in (BANCO_X0 + 40, BANCO_X1 - 70):
            cv.drawRect(skia.Rect(x0, BANCO_Y + 20, x0 + 16, G), paint(esc_cor(METAL, 0.3)))
            cv.drawRect(skia.Rect(x0 + 34, BANCO_Y + 20, x0 + 50, G), paint(METAL))
        cv.drawRect(skia.Rect(BANCO_X0 + 40, G - 96, BANCO_X1 - 20, G - 86), paint(esc_cor(METAL, 0.2)))
        sh = skia.GradientShader.MakeLinear([skia.Point(0, BANCO_Y), skia.Point(0, BANCO_Y + 30)], [_c(MAD_CL), _c(MAD_ESC)])
        cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(BANCO_X0, BANCO_Y, BANCO_X1, BANCO_Y + 30), 8, 8), paint(MAD, shader=sh))
        for x in range(int(BANCO_X0) + 90, int(BANCO_X1), 120):
            cv.drawLine(x, BANCO_Y + 4, x, BANCO_Y + 28, paint(MAD_ESC, 160, "stroke", 3))
        cv.drawLine(BANCO_X0 + 8, BANCO_Y + 3, BANCO_X1 - 8, BANCO_Y + 3, paint("#C79B72", 220, "stroke", 4))


def mochila(cv, casaco=0.0, verde=0.0):
    x0, x1 = MOCH
    y1 = BANCO_Y; y0 = BANCO_Y - 70
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(x0 + 6, y0 + 8, x1 + 6, y1 + 4), 26, 26), paint("#000000", 50, blur=8))
    sh = skia.GradientShader.MakeLinear([skia.Point(0, y0), skia.Point(0, y1)], [_c(MOCHILA_CL), _c(MOCHILA_ESC)])
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(x0, y0, x1, y1), 26, 26), paint(MOCHILA, shader=sh))
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(x0 + 34, y0 + 26, x1 - 34, y1 - 8), 14, 14), paint(MOCHILA_ESC, 200))
    cv.drawLine(x0 + 40, y0 + 34, x1 - 40, y0 + 34, paint("#3A3F47", 220, "stroke", 4))
    cv.drawArc(skia.Rect(x0 + 50, y0 - 26, x1 - 50, y0 + 22), 180, 180, False, paint(MOCHILA_ESC, 255, "stroke", 9))
    if casaco > 0:                                    # o casaco dobrado entra por cima (pé pra cima)
        k = e_out(casaco)
        cy = lerp(y0 - 170, y0 - 54, k)
        cx0, cx1 = x0 + 4 + 40 * (1 - k), x1 - 4 - 40 * (1 - k)
        a = clamp(casaco * 3)
        r = skia.RRect.MakeRectXY(skia.Rect(cx0, cy, cx1, cy + 56), 18, 18)
        cv.drawRRect(r, paint("#000000", int(50 * a), blur=6))
        sh2 = skia.GradientShader.MakeLinear([skia.Point(0, cy), skia.Point(0, cy + 56)], [_c(CASACO_CL), _c(CASACO_ESC)])
        cv.drawRRect(r, paint(CASACO, int(255 * a), shader=sh2))
        cv.drawLine(cx0 + 16, cy + 20, cx1 - 16, cy + 20, paint(CASACO_ESC, int(200 * a), "stroke", 3))
        cv.drawLine(cx0 + 16, cy + 38, cx1 - 16, cy + 38, paint(CASACO_ESC, int(150 * a), "stroke", 3))
        cv.drawLine(cx1 - 26, cy + 4, cx1 - 26, cy + 52, paint("#D7DEE5", int(220 * a), "stroke", 4))     # zíper
        if verde > 0:
            cv.drawRRect(r, paint(VERDE, int(255 * verde), "stroke", 5))


def chuteira_no_chao(cv, x, a=1.0):
    pe_desenho(cv, (x, G - 19), 0.0, PELE1, LINHA1, "chuteira", a)


def manga_cor(cv, p0, p1, tons, linha, a=1.0, larg0=33.0, larg1=29.0):
    """Manga de adulto (dobras do tecido e o punho), na cor dada."""
    pinta(cv, capsula(p0, p1, larg0, larg1), p0, p1, larg0, tons, a, linha=linha)
    d = (p1[0] - p0[0], p1[1] - p0[1]); L = math.hypot(*d) or 1.0; u = (d[0] / L, d[1] / L); n = (-u[1], u[0])
    for f, g in ((0.45, 1), (0.62, -1), (0.78, 1)):
        c = lerp2(p0, p1, f)
        cv.drawLine(c[0] - n[0] * 11 * g, c[1] - n[1] * 11 * g, c[0] + u[0] * 9 + n[0] * 4 * g, c[1] + u[1] * 9 + n[1] * 4 * g,
                    paint(esc_cor(tons[0], 0.25), int(160 * a), "stroke", 2.2))
    q = lerp2(p0, p1, 0.9)
    cv.drawPath(capsula(q, p1, larg1 + 2, larg1 + 2), paint(esc_cor(tons[1], 0.18), int(255 * a)))


def braco_adulto(cv, pulso, ang_ante, ang_braco, a=1.0, tons=MANGA_MAOS, linha="#4A525C", L_ante=112.0, L_braco=330.0):
    """(revisão) Braço vestido de um adulto fora do quadro, COM cotovelo: o antebraço sai do punho na direção
    `ang_ante` (graus), dobra no cotovelo e o braço segue em `ang_braco` até a borda (não é mais um tubo reto)."""
    if a <= 0:
        return None
    u1 = (math.cos(math.radians(ang_ante)), math.sin(math.radians(ang_ante)))
    cot = (pulso[0] + u1[0] * L_ante, pulso[1] + u1[1] * L_ante)
    u2 = (math.cos(math.radians(ang_braco)), math.sin(math.radians(ang_braco)))
    om = (cot[0] + u2[0] * L_braco, cot[1] + u2[1] * L_braco)
    pinta(cv, capsula(om, cot, 40, 37), om, cot, 40, tons, a, linha=linha)                  # braço (de cima)
    cv.drawCircle(cot[0], cot[1], 19, paint(esc_cor(tons[1], 0.08), int(255 * a)))          # cotovelo
    manga_cor(cv, cot, pulso, tons, linha, a, 36, 30)                                         # antebraço
    m = lerp2(cot, om, 0.12)                                                                  # vinco da dobra
    cv.drawArc(skia.Rect(m[0] - 16, m[1] - 16, m[0] + 16, m[1] + 16), ang_braco + 120, 110, False,
               paint(esc_cor(tons[0], 0.3), int(170 * a), "stroke", 2.4))
    return cot


def mao_adulto(cv, pulso, ponta_, a=1.0, lado=1):
    """Mão de adulto do punho até a ponta dos dedos: palma, dedos juntos (vincos) e o polegar de um lado."""
    d = (ponta_[0] - pulso[0], ponta_[1] - pulso[1]); L = math.hypot(*d) or 1.0
    u = (d[0] / L, d[1] / L); n = (-u[1] * lado, u[0] * lado)
    q = lambda f, g=0.0: (pulso[0] + u[0] * L * f + n[0] * g, pulso[1] + u[1] * L * f + n[1] * g)   # noqa: E731
    pol = capsula(q(0.18, 13), q(0.62, 20), 15, 12)
    pinta(cv, pol, q(0.18, 13), q(0.62, 20), 15, PELE_AD, a, linha=LINHA_AD, larg_linha=2)
    corpo_ = uniao(capsula(q(0.0), q(0.56), 31, 36), capsula(q(0.5), q(1.0, -2), 35, 28))
    pinta(cv, corpo_, q(0.0), q(1.0), 36, PELE_AD, a, linha=LINHA_AD, larg_linha=2.2)
    for g in (-8.5, 0.0, 8.5):                                          # vincos entre os dedos
        p0_, p1_ = q(0.62, g), q(0.97, g * 0.85)
        cv.drawLine(p0_[0], p0_[1], p1_[0], p1_[1], paint(LINHA_AD, int(190 * a), "stroke", 2.2))
    k0, k1 = q(0.56, -15), q(0.56, 15)
    cv.drawLine(k0[0], k0[1], k1[0], k1[1], paint(LINHA_AD, int(120 * a), "stroke", 2))


def _ponto_canela(jw, s_, lado=1.0, extra=0.0):
    """Ponto na superfície da canela de cá (lado +1 = frente/cima da canela deitada)."""
    kN, aN = jw["kN"], jw["aN"]
    dx, dy = aN[0] - kN[0], aN[1] - kN[1]; L = math.hypot(dx, dy) or 1.0
    d = (dx / L, dy / L); f = (d[1], -d[0])
    w = (lerp(29, 19, s_) if lado > 0 else 30) * KID1["k"] + extra
    c = (kN[0] + dx * s_, kN[1] + dy * s_)
    return (c[0] + f[0] * w * lado, c[1] + f[1] * w * lado)


def _centro_pe(jw, rot):
    v = rot2((48.0 * KID1["k"], 4.0 * KID1["k"]), rot)
    return (jw["aN"][0] + v[0], jw["aN"][1] + v[1])


def maos_anonimas(cv, jw, rot, k, esfrega, t, a=1.0, sai=0.0):
    """Duas mãos de adulto (só as mangas, sem corpo e sem rosto): uma aperta a canela logo acima do tornozelo,
    a outra o pé — o tornozelo fica à vista entre elas."""
    if a <= 0 or k <= 0:
        return
    vai = e_out(k); dx = 7 * esfrega * math.sin(t * 34)
    alvoA = _ponto_canela(jw, 0.62, 1, 4); alvoB = _centro_pe(jw, rot)
    alvoB = (alvoB[0] + 22, alvoB[1] - 14)
    for alvo, ang, lado, ddx, ang_b in ((alvoA, -62.0, 1, dx, -104.0), (alvoB, -30.0, -1, -dx, -72.0)):
        u = (math.cos(math.radians(ang)), math.sin(math.radians(ang)))
        pulso = (alvo[0] + u[0] * 52 + ddx, alvo[1] + u[1] * 52)
        ponta_ = (alvo[0] - u[0] * 8 + ddx, alvo[1] - u[1] * 8)
        sob = 460 * (1 - vai) + 460 * e_inout(sai)
        sh_ = (u[0] * sob, u[1] * sob)
        pulso = (pulso[0] + sh_[0], pulso[1] + sh_[1]); ponta_ = (ponta_[0] + sh_[0], ponta_[1] + sh_[1])
        braco_adulto(cv, pulso, ang, ang_b, a)
        mao_adulto(cv, pulso, ponta_, a, lado)
    if esfrega > 0:                                              # linhas de movimento (esfregar com força)
        for alvo in (alvoA, alvoB):
            for s_ in (-1, 1):
                x = alvo[0] + s_ * 44 + 5 * math.sin(t * 34); y = alvo[1] - 30
                cv.drawArc(skia.Rect(x - 16, y - 8, x + 16, y + 8), 200 if s_ < 0 else -20, 140, False,
                           paint("#FFFFFF", int(230 * a * esfrega), "stroke", 4))


def contorno_normal(cv, b, rot, a):
    """(local) O contorno do tornozelo SEM inchaço, tracejado em ciano (o telestrador guarda o 'antes')."""
    if a <= 0:
        return
    cont = contorno_pe_canela(b["kN"], b["aN"], rot)
    cv.save()
    clip = skia.Path(); clip.addCircle(b["aN"][0] + 6, b["aN"][1] - 10, 84)
    cv.clipPath(clip, skia.ClipOp.kIntersect, True)
    pt = paint(CARTAO, int(120 * a), "stroke", 6); pt.setPathEffect(skia.DashPathEffect.Make([12.0, 9.0], 0.0))
    cv.drawPath(cont, pt)
    pt = paint(CIANO, int(255 * a), "stroke", 3.4); pt.setPathEffect(skia.DashPathEffect.Make([12.0, 9.0], 0.0))
    cv.drawPath(cont, pt)
    cv.restore()


def bolsa_gelo(cv, ank, k, a=1.0, verde=0.0):
    """Bolsa de gelo enrolada num pano listrado, pousando em cima do tornozelo."""
    if k <= 0:
        return
    y = lerp(ank[1] - 260, ank[1] - 36, e_out(k)); x = ank[0] + 6
    aa = a * clamp(k * 4)
    cv.save(); cv.translate(x, y); cv.rotate(-6)
    r = skia.RRect.MakeRectXY(skia.Rect(-70, -30, 70, 30), 26, 26)
    cv.drawRRect(r, paint("#000000", int(60 * aa), blur=8))
    cv.drawRRect(r, paint(PANO_A, int(255 * aa)))
    cv.save(); cv.clipRRect(r, skia.ClipOp.kIntersect, True)
    for xx in range(-70, 80, 22):
        cv.drawRect(skia.Rect(xx, -30, xx + 9, 30), paint(PANO_B, int(220 * aa)))
    cv.restore()
    cv.drawRRect(r, paint("#9FB2C6", int(230 * aa), "stroke", 3))
    for (cx_, cy_) in ((-20, -40), (8, -46), (34, -38)):        # o gelo aparecendo na boca do pano
        q = skia.RRect.MakeRectXY(skia.Rect(cx_ - 15, cy_ - 13, cx_ + 15, cy_ + 15), 6, 6)
        cv.drawRRect(q, paint(GELO, int(240 * aa))); cv.drawRRect(q, paint("#9CCBE6", int(230 * aa), "stroke", 2.5))
        cv.drawLine(cx_ - 8, cy_ - 6, cx_ + 2, cy_ - 8, paint(GELO_CL, int(255 * aa), "stroke", 3))
    if verde > 0:
        cv.drawRRect(r, paint(VERDE, int(255 * verde), "stroke", 6))
    cv.restore()


def pose_l2(t, T):
    pe_sobe = e_inout(prog(t, T["pe2"] - 0.1, T["cima_fim"] + 0.05))
    ank = lerp2(ANK2, ANK2_ALTO, pe_sobe)
    incha = e_inout(prog(t, T["aumenta"] - 0.02, T["inchaco"] + 0.3)) if t >= T["anulado2"] + 0.3 else 0.0
    # a criança se apoia nas mãos para trás; quando o pé sobe ela reclina um pouco
    al = lerp(-0.18, -0.26, pe_sobe)
    return dict(hip=HIP2, al=al, ankN=ank, ankF=(426.0, G - 19), rotN=ROT_PE2, rotF=0.0,
                mN=(HIP2[0] - 40, BANCO_Y - 8), mF=(HIP2[0] - 64, BANCO_Y - 4), gN=0.0, gF=0.0, mir=1,
                descalcoN=True, sem_meiaN=True, incha=incha)


CAM_L2_ABERTA = (1.3, 452.0, 838.0)
CAM_L2_MAOS = (2.0, 590.0, 818.0)
CAM_L2_REPLAY = (2.35, 590.0, 836.0)
CAM_L2_GELO = (1.6, 540.0, 826.0)
CAM_L2_CIMA = (1.36, 470.0, 812.0)


def cam_l2(t, T):
    cam = lerp3((1.18, 470.0, 840.0), CAM_L2_ABERTA, e_inout(prog(t, T["corte2"], T["forte"] + 0.2)))
    cam = lerp3(cam, CAM_L2_MAOS, e_inout(prog(t, T["pode1"], T["pode1"] + 0.32)))
    cheg = prog(t, T["pode1_fim"], T["anulado2"])
    cam = (cam[0] * (1 + 0.07 * e_inout(cheg)), cam[1], cam[2])
    cam = lerp3(cam, CAM_L2_REPLAY, e_inout(prog(t, T["logo"] - 0.3, T["logo"])))
    cam = lerp3(cam, CAM_L2_GELO, e_inout(prog(t, T["gelo"] - 0.12, T["gelo"] + 0.3)))
    return lerp3(cam, CAM_L2_CIMA, e_inout(prog(t, T["pe2"] - 0.1, T["cima_fim"] + 0.1)))


def estado_l2(t, T):
    m0, mp = T["massagem"], T["pode1"]
    r0 = T["logo"] - 0.3                                      # replay: as mãos voltam a apertar de perto
    if t < T["anulado2"] + 0.3:
        k = e_out(prog(t, m0 + 0.05, T["forte"] + 0.1))
        esf = janela(t, T["forte"] - 0.05, mp + 0.02, 0.1, 0.05)
        sai = 0.0
    else:
        k = 1.0
        esf = janela(t, r0 + 0.1, T["aumenta"] - 0.1, 0.1, 0.1)
        sai = prog(t, T["aumenta"] + 0.05, T["aumenta"] + 0.45)          # largam o pé: agora se vê o inchaço
    replay = janela(t, r0 - 0.04, T["gelo"] - 0.12, 0.06, 0.12)
    return dict(k=k, esf=esf, sai=sai, replay=replay)


def cena_l2(cv, t, T):
    cam = cam_l2(t, T)
    kid = pose_l2(t, T)
    e = estado_l2(t, T)
    cv.save(); aplica(cv, cam)
    campo(cv)
    banco(cv, "fundo")
    chuteira_no_chao(cv, 700.0)
    vv = janela(t, T["cima"] - 0.05, T["corte3"], 0.2, 0.1)
    mochila(cv, prog(t, T["pe2"] - 0.25, T["pe2"] + 0.15), verde=vv)
    sombra(cv, 420, 160, 0.6)
    a_cont = janela(t, T["aumenta"] - 0.1, T["gelo"] - 0.1, 0.15, 0.2) if t > T["anulado2"] + 0.3 else 0.0
    pessoa(cv, kid, KID1, ganchos={"perna": lambda c, b: contorno_normal(c, b, ROT_PE2, a_cont)})
    jw = juntas(kid, KID1)
    ank = jw["aN"]
    maos_anonimas(cv, jw, ROT_PE2, e["k"], e["esf"], t, 1.0, e["sai"])
    g = prog(t, T["gelo"] - 0.05, T["pano"] + 0.1)
    bolsa_gelo(cv, ank, g, verde=janela(t, T["pano"], T["corte3"], 0.2, 0.1))
    cv.restore()
    return cam, kid, e


# ================================================================== LANCE 3 — caiu e o braço ficou torto
KID3_X0 = 220.0
AJOELHA_HIP = (552.0, G - 157.0)
KINK = 30.0                      # (revisão) dobra VISÍVEL no meio do antebraço (com 15° parecia só a mão caída)
# (revisão) o braço machucado de lado, na postura de proteção: cotovelo um pouco à frente do ombro, antebraço de
# leve para cima, de modo que a corda cotovelo-mão fica nivelada e a dobra aparece como um bico; a mão de lá,
# em concha, apoia o antebraço por baixo, perto do cotovelo (o docstring antigo dizia isso e o código não fazia).
MAO_L3 = (AJOELHA_HIP[0] + 123, AJOELHA_HIP[1] - 74)        # alvo do IK da mão de cá (antes da dobra)
APOIO_L3 = (AJOELHA_HIP[0] + 70, AJOELHA_HIP[1] - 38)       # a mão de lá, por baixo do antebraço
MAO_L3_CERTO = (AJOELHA_HIP[0] + 83, AJOELHA_HIP[1] - 68)   # na tipoia: cotovelo sob o ombro, antebraço junto à barriga
ANTE_K_CERTO = 0.82                                          # o antebraço cruza a barriga: aparece mais curto (escorço)


def pose_l3(t, T):
    """KID2: corre, tropeça, cai sobre a mão; ajoelha protegendo o antebraço torto com a outra mão."""
    c3, caiu = T["corte3"], T["caiu"]
    if t < caiu - 0.04:                                         # correndo (a criança já entra correndo)
        x = KID3_X0 + 430 * (t - c3)
        hy, aN, aF, rN, rF, _ = marcha(x, KID3_X0, 1, 120.0, KID_HIP_Y + 10, G - 19, apoio=0.42, lift=70.0, bob=14.0)
        sw = math.sin(2 * math.pi * (x - KID3_X0) / (120.0 / 0.42))
        return dict(hip=(x, hy), al=0.3, ankN=aN, ankF=aF, rotN=rN, rotF=rF,
                    mN=(x + 50 * sw, hy - 70), mF=(x - 50 * sw, hy - 70), gN=0.5, gF=0.5, mir=1, kink=0.0)
    x_c = KID3_X0 + 430 * (caiu - 0.04 - c3)
    hy0, aN0, aF0, rN0, rF0, _ = marcha(x_c, KID3_X0, 1, 120.0, KID_HIP_Y + 10, G - 19, apoio=0.42, lift=70.0, bob=14.0)
    keys = completa([
        (caiu - 0.04, dict(hip=(x_c, hy0), al=0.3, ankN=aN0, ankF=aF0, rotN=rN0, rotF=rF0, mN=(x_c + 40, hy0 - 70),
                           mF=(x_c - 30, hy0 - 70), gN=0.5, gF=0.5, mir=1, kink=0.0)),
        # tropeça: o pé de cá fica para trás, o corpo inclina
        (caiu + 0.22, dict(hip=(x_c + 70, KID_HIP_Y + 40), al=0.95, ankN=(x_c - 30, G - 22), ankF=(x_c + 100, G - 60),
                           rotN=30.0, mN=(x_c + 260, G - 150), mF=(x_c + 230, G - 140), gN=0.0, gF=0.0)),
        # chega ao chão sobre a mão estendida (a de cá) e os joelhos
        (caiu + 0.5, dict(hip=(x_c + 120, G - 150), al=1.3, ankN=(x_c - 30, G - 18), ankF=(x_c - 20, G - 18),
                          rotN=60.0, rotF=60.0, mN=(x_c + 330, G - 14), mF=(x_c + 300, G - 22))),
        (T["braco"] - 0.02, dict()),
        # ajoelhada, de tronco erguido, o antebraço de cá dobrado junto ao corpo e a mão de lá por baixo dele
        (T["torto1"] + 0.02, dict(hip=AJOELHA_HIP, al=0.12, ankN=(AJOELHA_HIP[0] - 133, G - 18),
                                  ankF=(AJOELHA_HIP[0] - 125, G - 18), rotN=165.0, rotF=165.0, mN=MAO_L3,
                                  mF=APOIO_L3, gN=0.0, gF=0.45, kink=KINK)),
    ])
    p = chaves(t, keys)
    if t < T["braco"] - 0.02:
        p["kink"] = 0.0
    return p


def pos_l3_certo(t, T):
    """Depois da cortina: o braço COMO ESTÁ (a mesma dobra), na tala de revista com pano, junto ao corpo na tipoia."""
    return dict(hip=AJOELHA_HIP, al=0.06, ankN=(AJOELHA_HIP[0] - 133, G - 18), ankF=(AJOELHA_HIP[0] - 125, G - 18),
                rotN=165.0, rotF=165.0, mN=MAO_L3_CERTO,
                mF=(AJOELHA_HIP[0] + 4, AJOELHA_HIP[1] - 4), gN=0.0, gF=0.0, mir=1, kink=KINK, ante_k=ANTE_K_CERTO)


def revista_pano(cv, x, y, k, a=1.0):
    """A revista dobrada (rígida) e o pano listrado (macio), no chão ao lado da criança. (revisão) Entram INTEIROS,
    dentro do quadro (caem de leve e aparecem), e a revista tem cara de revista: capa com foto, faixa de título,
    linhas de texto e as folhas na borda; o pano é uma toalhinha listrada com franja."""
    if k <= 0 or a <= 0:
        return
    e = e_out(k); aa = a * clamp(k * 2.5)
    cv.save(); cv.translate(x, y - 34 * (1 - e))
    # pano dobrado (toalhinha listrada, com franja nas pontas)
    pn = skia.RRect.MakeRectXY(skia.Rect(0, -30, 128, 0), 9, 9)
    cv.drawRRect(pn, paint("#000000", int(50 * aa), blur=6))
    cv.drawRRect(pn, paint(PANO_A, int(255 * aa)))
    cv.save(); cv.clipRRect(pn, skia.ClipOp.kIntersect, True)
    for xx in range(8, 128, 24):
        cv.drawRect(skia.Rect(xx, -30, xx + 9, 0), paint(PANO_B, int(220 * aa)))
    cv.drawLine(0, -16, 128, -16, paint("#D9D3C6", int(200 * aa), "stroke", 2))         # a dobra
    cv.restore()
    cv.drawRRect(pn, paint("#9FB2C6", int(230 * aa), "stroke", 3))
    for xx in (-1, 129):
        for yy in range(-26, 0, 5):
            d_ = -1 if xx < 0 else 1
            cv.drawLine(xx, yy, xx + 7 * d_, yy + 1, paint("#C9C2B2", int(230 * aa), "stroke", 2))
    # revista dobrada (capa colorida, sem letra), com as folhas aparecendo embaixo
    cv.translate(-176, 0); cv.rotate(-3)
    folhas = poli([(-6, -12), (142, -8), (144, 0), (-8, 0)])
    cv.drawPath(folhas, paint("#000000", int(50 * aa), blur=6))
    cv.drawPath(folhas, paint("#F4F6F8", int(255 * aa)))
    for yy in (-8, -4):
        cv.drawLine(-6, yy, 142, yy + 1, paint("#B8C2CC", int(220 * aa), "stroke", 1.6))
    capa_ = poli([(0, -60), (138, -56), (140, -10), (-4, -12)])
    cv.drawPath(capa_, paint(REVISTA[2], int(255 * aa)))
    cv.drawPath(poli([(4, -57), (134, -53), (134, -45), (4, -48)]), paint("#2C3A4E", int(255 * aa)))    # faixa do título
    foto = poli([(8, -42), (70, -40), (70, -16), (6, -17)])
    cv.drawPath(foto, paint(REVISTA[1], int(255 * aa)))
    cv.drawCircle(50, -33, 7, paint(REVISTA[0], int(255 * aa)))                                        # sol da foto
    cv.drawPath(poli([(6, -17), (30, -30), (46, -22), (58, -28), (70, -16)]), paint("#3F8D3A", int(255 * aa)))
    for i, yy in enumerate((-38, -32, -26, -20)):                                                     # linhas de texto
        cv.drawLine(80, yy, 128 - 8 * (i % 2), yy + 1, paint("#9AA5B1", int(255 * aa), "stroke", 3))
    cv.drawPath(capa_, paint("#7C8794", int(230 * aa), "stroke", 3))
    cv.restore()


def _eixo_antebraco(b):
    """(local) Corda do antebraço torto: do cotovelo até perto da mão; n aponta para baixo."""
    cot = b["eN"]; meio, mao_p = antebraco_pts(b, KINK)
    d = (mao_p[0] - cot[0], mao_p[1] - cot[1]); L = math.hypot(*d) or 1; u = (d[0] / L, d[1] / L); n = (-u[1], u[0])
    if n[1] < 0:
        n = (-n[0], -n[1])
    p0 = (cot[0] - u[0] * 8, cot[1] - u[1] * 8); p1 = (mao_p[0] - u[0] * 26, mao_p[1] - u[1] * 26)
    return p0, p1, u, n


def tipoia(cv, b, a=1.0, verde=0.0):
    """(local, ANTES do braço de cá) Tipoia de pano: do pescoço até debaixo do antebraço."""
    p0, p1, u, n = _eixo_antebraco(b)
    sh_ = b["sh"]; up = b["up"]; fw = b["fw"]
    nuca = (sh_[0] + up[0] * 30 - fw[0] * 4, sh_[1] + up[1] * 30 - fw[1] * 4)
    tip = poli([nuca, (p1[0] + n[0] * 52 + u[0] * 18, p1[1] + n[1] * 52 + u[1] * 18),
                (p0[0] + n[0] * 56 - u[0] * 10, p0[1] + n[1] * 56 - u[1] * 10)])
    cv.drawPath(tip, paint("#000000", int(50 * a), blur=8))
    cv.drawPath(tip, paint(TIPOIA, int(255 * a)))
    cv.drawPath(tip, paint(TIPOIA_ESC, int(230 * a), "stroke", 3.5))
    cv.drawLine(nuca[0], nuca[1], lerp(p0[0], p1[0], 0.45) + n[0] * 50, lerp(p0[1], p1[1], 0.45) + n[1] * 50,
                paint(TIPOIA_ESC, int(150 * a), "stroke", 3))
    if verde > 0:
        cv.drawPath(tip, paint(VERDE, int(220 * verde), "stroke", 6))


def pano_tala(cv, b, a=1.0):
    """(local, ANTES do braço) O pano macio entre o braço e a revista: preenche o vão debaixo da dobra
    (o braço fica COMO ESTÁ, a revista reta por baixo, o pano no meio)."""
    p0, p1, u, n = _eixo_antebraco(b)
    pano_p = poli([(p0[0] - n[0] * 6, p0[1] - n[1] * 6), (p1[0] - n[0] * 6, p1[1] - n[1] * 6),
                   (p1[0] + n[0] * 22, p1[1] + n[1] * 22), (p0[0] + n[0] * 22, p0[1] + n[1] * 22)])
    cv.drawPath(pano_p, paint(PANO_A, int(255 * a)))
    cv.save(); cv.clipPath(pano_p, skia.ClipOp.kIntersect, True)
    for s_ in (0.1, 0.24, 0.38, 0.52, 0.66, 0.8, 0.94):
        c = lerp2(p0, p1, s_)
        cv.drawLine(c[0] - n[0] * 8, c[1] - n[1] * 8, c[0] + n[0] * 24, c[1] + n[1] * 24, paint(PANO_B, int(220 * a), "stroke", 6))
    cv.restore()
    cv.drawPath(pano_p, paint("#9FB2C6", int(200 * a), "stroke", 2.5))


def tala(cv, b, a=1.0, verde=0.0):
    """(local, DEPOIS do braço de cá) A revista dobrada, RETA, por baixo do antebraço (a aba de cá cobre a borda de
    baixo do braço), e duas tiras frouxas em volta — o braço continua com a mesma dobra por cima."""
    p0, p1, u, n = _eixo_antebraco(b)
    aba = poli([(p0[0] + n[0] * 14, p0[1] + n[1] * 14), (p1[0] + n[0] * 14, p1[1] + n[1] * 14),
                (p1[0] + n[0] * 40, p1[1] + n[1] * 40), (p0[0] + n[0] * 40, p0[1] + n[1] * 40)])
    cv.drawPath(aba, paint("#000000", int(60 * a), blur=6))
    cv.drawPath(aba, paint(REVISTA[2], int(255 * a)))
    faixa = poli([(p0[0] + n[0] * 20, p0[1] + n[1] * 20), (p1[0] + n[0] * 20, p1[1] + n[1] * 20),
                  (p1[0] + n[0] * 27, p1[1] + n[1] * 27), (p0[0] + n[0] * 27, p0[1] + n[1] * 27)])
    cv.drawPath(faixa, paint("#2C3A4E", int(255 * a)))
    q0, q1 = lerp2(p0, p1, 0.3), lerp2(p0, p1, 0.62)
    cv.drawPath(poli([(q0[0] + n[0] * 29, q0[1] + n[1] * 29), (q1[0] + n[0] * 29, q1[1] + n[1] * 29),
                      (q1[0] + n[0] * 37, q1[1] + n[1] * 37), (q0[0] + n[0] * 37, q0[1] + n[1] * 37)]), paint(REVISTA[1], int(255 * a)))
    cv.drawPath(aba, paint("#7C8794", int(230 * a), "stroke", 3))
    cot = b["eN"]; meio, mao_p = antebraco_pts(b, KINK)
    for s_ in (0.24, 0.76):
        c = lerp2(p0, p1, s_)
        topo = lerp2(cot, meio, s_ / 0.5) if s_ < 0.5 else lerp2(meio, mao_p, (s_ - 0.5) / 0.5)
        t0 = (topo[0] - n[0] * 19, topo[1] - n[1] * 19); t1 = (c[0] + n[0] * 44, c[1] + n[1] * 44)
        cv.drawLine(t0[0], t0[1], t1[0], t1[1], paint("#F7F3EA", int(255 * a), "stroke", 12))
        cv.drawLine(t0[0], t0[1], t1[0], t1[1], paint("#B9AE95", int(200 * a), "stroke", 2))
    if verde > 0:
        cv.drawPath(aba, paint(VERDE, int(255 * verde), "stroke", 6))


def ganchos_tala(vv):
    return {"antes_braco": lambda c, b: (tipoia(c, b, 1.0, vv), pano_tala(c, b, 1.0)),
            "braco": lambda c, b: tala(c, b, 1.0, vv)}


def no_local(cv, pose, est, fn):
    """Chama fn(cv, b) nas coordenadas LOCAIS da pessoa (como os ganchos do pessoa())."""
    k, mir, hip = est["k"], pose.get("mir", 1), pose["hip"]
    b = corpo_local(pose_local(pose, est), est["hr"])
    cv.save(); cv.translate(hip[0], hip[1]); cv.scale(k * mir, k); cv.translate(-hip[0], -hip[1])
    fn(cv, b)
    cv.restore()


def forma_antebraco(b, kink):
    """(local) O antebraço de cá + a mão com a dobra `kink` (mesma geometria do braco())."""
    cot, mao_p = b["eN"], b["hN"]
    meio = lerp2(cot, mao_p, 0.5)
    if kink:
        v = rot2((mao_p[0] - meio[0], mao_p[1] - meio[1]), kink)
        mao_p = (meio[0] + v[0], meio[1] + v[1])
    pulso = lerp2(meio, mao_p, 0.64)
    d = (mao_p[0] - pulso[0], mao_p[1] - pulso[1]); L = math.hypot(*d) or 1.0; u = (d[0] / L, d[1] / L)
    mao_ = capsula((mao_p[0] - u[0] * 15, mao_p[1] - u[1] * 15), (mao_p[0] + u[0] * 15, mao_p[1] + u[1] * 15), 27, 23)
    return uniao(capsula(cot, meio, 34, 31), capsula(meio, pulso, 31, 27), mao_)


def fantasma(cv, b, kink, a):
    """(local) Replay do jeito errado: o CONTORNO tracejado (âmbar) do antebraço como ficaria se alguém endireitasse —
    só o contorno, a pele não muda e o braço de verdade continua como está."""
    if a <= 0:
        return
    p = forma_antebraco(b, kink)
    pt = paint(CARTAO, int(150 * a), "stroke", 8); pt.setPathEffect(skia.DashPathEffect.Make([14.0, 9.0], 0.0))
    cv.drawPath(p, pt)
    pt = paint(AMBAR, int(255 * a), "stroke", 4.5); pt.setPathEffect(skia.DashPathEffect.Make([14.0, 9.0], 0.0))
    cv.drawPath(p, pt)


def mao_agarra(cv, c, u, n, fecha, a=1.0):
    """(revisão) A mão de um adulto FECHADA POR CIMA do punho da criança, em garra (antes era palma com palma e
    parecia um aperto de mão): o dorso em cima, os quatro dedos dando a volta no punho, do lado de quem vê.
    `c` = centro do punho, `u` = eixo do antebraço (para a mão da criança), `n` = para cima. `fecha`: 0 aberta, 1 fechada."""
    if a <= 0:
        return None
    dc = (c[0] + n[0] * 26 - u[0] * 2, c[1] + n[1] * 26 - u[1] * 2)              # centro do dorso
    dorso = capsula((dc[0] - u[0] * 14, dc[1] - u[1] * 14), (dc[0] + u[0] * 14, dc[1] + u[1] * 14), 34, 32)
    pinta(cv, dorso, (dc[0] - n[0] * 10, dc[1] - n[1] * 10), (dc[0] + n[0] * 10, dc[1] + n[1] * 10), 34, PELE_AD, a,
          linha=LINHA_AD, larg_linha=2.2)
    for i, off in enumerate((-13.5, -4.5, 4.5, 13.5)):
        base = (c[0] + n[0] * 13 + u[0] * off, c[1] + n[1] * 13 + u[1] * off)
        aberta = (base[0] + n[0] * 2 + u[0] * (off * 0.5 + 18), base[1] + n[1] * 2 + u[1] * (off * 0.5 + 18))
        fechada = (c[0] - n[0] * (10 + (1.5 if i in (1, 2) else 0)) + u[0] * (off + 2),
                   c[1] - n[1] * (10 + (1.5 if i in (1, 2) else 0)) + u[1] * (off + 2))
        ponta_ = lerp2(aberta, fechada, e_inout(clamp(fecha)))
        dedo = capsula(base, ponta_, 10.5, 9.5)
        pinta(cv, dedo, base, ponta_, 10.5, PELE_AD, a, linha=LINHA_AD, larg_linha=2)
    k0 = (c[0] + n[0] * 14 - u[0] * 19, c[1] + n[1] * 14 - u[1] * 19)
    k1 = (c[0] + n[0] * 14 + u[0] * 19, c[1] + n[1] * 14 + u[1] * 19)
    cv.drawLine(k0[0], k0[1], k1[0], k1[1], paint(LINHA_AD, int(150 * a), "stroke", 2))   # linha dos nós dos dedos
    return (dc[0] + n[0] * 14, dc[1] + n[1] * 14)                                    # onde o pulso do adulto começa


def replay_puxa(t, T):
    """Tempos do replay do jeito errado (lance 3)."""
    r0 = T["validado"] + DUR_CARIMBOS[2] - 0.1
    solta = T["endireita_fim"] + 0.08
    return dict(
        r0=r0, solta=solta,
        entra=e_out(prog(t, r0, T["nao2"] + 0.1)),
        fecha=e_inout(prog(t, T["nao2"], T["puxa"] + 0.05)) * (1 - e_inout(prog(t, solta, solta + 0.18))),
        sai=e_inout(prog(t, solta + 0.12, T["certo3"])),
        seta=janela(t, T["puxa"] - 0.05, solta, 0.12, 0.15), seta_k=e_out(prog(t, T["puxa"] - 0.05, T["puxa"] + 0.3)),
        fant=janela(t, T["puxa"], solta + 0.05, 0.12, 0.2),
        kink_f=KINK * (1 - e_inout(prog(t, T["endireita"] - 0.12, T["endireita_fim"] - 0.08))),
        x_t0=T["endireita"] + 0.22)


def _eixo_punho(jw):
    """(mundo) Centro do punho, eixo da metade de baixo do antebraço e a normal para cima."""
    meio, mao_p = jw["meio"], jw["mao"]
    d = (mao_p[0] - meio[0], mao_p[1] - meio[1]); L = math.hypot(*d) or 1.0; u = (d[0] / L, d[1] / L)
    n = (u[1], -u[0])
    if n[1] > 0:
        n = (-n[0], -n[1])
    return lerp2(meio, mao_p, 0.5), u, n


def mao_que_puxa(cv, jw, r, a=1.0):
    """Replay do jeito errado: o braço de um adulto (manga cinza, com cotovelo, vindo de cima pela direita) fecha a
    mão por cima do punho para puxar; depois abre e sai."""
    if r["entra"] <= 0 or a <= 0:
        return None
    c, u, n = _eixo_punho(jw)
    ang_ante = math.degrees(math.atan2(n[1], n[0])) + 32
    ua = (math.cos(math.radians(ang_ante)), math.sin(math.radians(ang_ante)))
    sob = 300 * (1 - r["entra"]) + 300 * r["sai"]
    c2 = (c[0] + ua[0] * sob, c[1] + ua[1] * sob)
    pulso = (c2[0] + n[0] * 40 + ua[0] * 6, c2[1] + n[1] * 40 + ua[1] * 6)
    braco_adulto(cv, pulso, ang_ante, -96.0, a, L_ante=104.0, L_braco=300.0)
    mao_agarra(cv, c2, u, n, r["fecha"], a)
    return c


CAM_L3_CORRE = (1.04, 520.0, 872.0)
CAM_L3_CHAO = (1.3, 600.0, 900.0)
CAM_L3_CERTO = (2.15, 612.0, 868.0)
CARIMBO_L3 = (CX + 180, JY0 + 190)       # (revisão) o VALIDADO sai ao lado da cabeça, não em cima dela


def cam_l3(t, T, kid):
    x = kid["hip"][0]
    cam = (1.04, clamp(x + 80, 420, 640), 872.0)
    cam = lerp3(cam, CAM_L3_CHAO, e_inout(prog(t, T["caiu"] + 0.3, T["braco"] + 0.2)))
    jw = juntas(kid, KID2) if kid.get("kink") else None
    if jw:
        meio = jw["meio"]
        perto = (2.05, meio[0] + 24, meio[1] - 16)                 # (revisão) a criança inteira, com folga em cima
        cam = lerp3(cam, perto, e_inout(prog(t, T["torto1"], T["torto1"] + 0.3)))
        mais = (1.7, meio[0] + 70, meio[1] + 40)
        cam = lerp3(cam, mais, e_inout(prog(t, T["imobilizar"] - 0.05, T["imobilizar"] + 0.35)))
        cheg = prog(t, T["pode2_fim"], T["validado"])
        cam = (cam[0] * (1 + 0.07 * e_inout(cheg)), cam[1], cam[2])
        punho = jw["mao"]
        cam = lerp3(cam, (2.05, punho[0] + 36, punho[1] - 30), e_inout(prog(t, T["validado"] + 0.4, T["nao2"] + 0.05)))
    return cam


def cena_l3(cv, t, T):
    kid = pose_l3(t, T)
    cam = cam_l3(t, T, kid)
    r = replay_puxa(t, T)
    rep = janela(t, r["r0"] - 0.05, T["certo3"], 0.1, 0.05)
    cv.save(); aplica(cv, cam)
    campo(cv)
    sombra(cv, kid["hip"][0] + 30, 140)
    # a revista e o pano entram ao lado da criança (inteiros, no quadro); no replay do jeito errado eles somem
    kr = prog(t, T["imobilizar"] + 0.15, T["esta"] + 0.05)
    if kr > 0:
        revista_pano(cv, AJOELHA_HIP[0] + 232, G - 6, kr, 1 - rep)
    pessoa(cv, kid, KID2)
    jw = juntas(kid, KID2)
    info = dict(cam=cam, kid=kid, jw=jw, rep=r)
    if t < T["certo3"]:
        p = mao_que_puxa(cv, jw, r)
        info["mao_puxa"] = p
        if r["fant"] > 0:                    # o contorno-fantasma por cima de tudo (a mão do adulto não o esconde)
            no_local(cv, kid, KID2, lambda c, b: fantasma(c, b, r["kink_f"], r["fant"]))
    cv.restore()
    return info


def cena_l3_certo(cv, t, T, cam):
    """O jeito certo (depois da cortina): tala de revista + pano + tipoia, a mão do adulto no ombro."""
    kid = pos_l3_certo(t, T)
    vv = janela(t, T["certo3"] + 0.55, T["sai3"], 0.2, 0.1)
    cv.save(); aplica(cv, cam)
    campo(cv)
    sombra(cv, AJOELHA_HIP[0], 140)
    pessoa(cv, kid, KID2, ganchos=ganchos_tala(vv))
    jk = juntas(kid, KID2)
    # a mão do adulto (o mesmo da jaqueta cáqui do lance 1, fora do quadro) nas costas do ombro: calma
    om = (jk["ombro"][0] - 20, jk["ombro"][1] + 2)
    u = (math.cos(math.radians(-168)), math.sin(math.radians(-168)))
    pulso = (om[0] + u[0] * 36, om[1] + u[1] * 36)
    braco_adulto(cv, pulso, -168.0, -112.0, 1.0, tons=CAQUI, linha=esc_cor(CAQUI[0], 0.3), L_ante=104.0, L_braco=300.0)
    mao_adulto(cv, pulso, (om[0] + 8, om[1] + 8), 1.0, 1)
    cv.restore()
    return kid, vv


def cena_l3_sai(cv, t, T):
    """'e vai pro pronto-socorro': sai andando, de tipoia, ao lado do adulto (sem ambulância, sem texto)."""
    t0 = T["sai3"]
    x = 600.0 - 250 * (t - t0)
    hy, aN, aF, rN, rF, _ = marcha(x, 600.0, -1, 100.0, KID_HIP_Y + 4, G - 19, apoio=0.6, lift=40.0, bob=6.0)
    dm = (MAO_L3_CERTO[0] - AJOELHA_HIP[0], MAO_L3_CERTO[1] - AJOELHA_HIP[1])
    kid = dict(hip=(x, hy), al=0.06, ankN=aN, ankF=aF, rotN=rN, rotF=rF, mN=(x - dm[0], hy + dm[1]), mF=(x - 4, hy - 4),
               gN=0.0, gF=0.0, mir=-1, kink=KINK, ante_k=ANTE_K_CERTO)
    xa = x + 100
    hya, aNa, aFa, rNa, rFa, _ = marcha(xa, 700.0, -1, AD_PASSO, AD1_HIP_Y, AD_TORN, apoio=0.6, lift=36.0, bob=6.0)
    ad = dict(hip=(xa, hya), al=0.06, ankN=aNa, ankF=aFa, rotN=rNa, rotF=rFa, mN=(xa - 60, hya + 40), mF=(xa + 30, hya + 60),
              gN=0.0, gF=0.0, mir=-1)
    cam = (1.3, 520.0 - 60 * prog(t, t0, t0 + 1.4), CAM_L1_Y)
    cv.save(); aplica(cv, cam)
    campo(cv)
    sombra(cv, xa, 120, y=G_FUNDO); sombra(cv, x, 110)
    pessoa(cv, ad, ADULTO_L1, partes="sem_braco")
    pessoa(cv, kid, KID2, ganchos=ganchos_tala(0.0))
    jk = juntas(kid, KID2)
    ad["mN"] = (jk["ombro"][0] + 22, jk["ombro"][1] + 6)             # (revisão) a mão nas costas, não no pescoço
    pessoa(cv, ad, ADULTO_L1, partes="so_braco")
    cv.restore()
    return cam


# ================================================================== HUD do VAR (cópia do piloto)
def fundo(cv, t):
    def _d(c):
        sh = skia.GradientShader.MakeRadial(skia.Point(W / 2, H * 0.42), H * 0.75, [_c(ARD_IN), _c(ARD_OUT)])
        c.drawRect(skia.Rect(0, 0, W, H), paint(ARD_IN, shader=sh))
    cv.drawImage(cacheado("fundo", W, H, _d), 0, 0)


def vinheta(cv):
    def _d(c):
        c.translate(-JX0, -JY0)
        vin = skia.GradientShader.MakeRadial(skia.Point(JCX, JCY), 760, [_c("#000000", 0), _c("#000000", 0), _c("#000000", 90)],
                                             [0.0, 0.62, 1.0])
        c.drawRect(JAN, paint("#000000", shader=vin))
    cv.drawImage(cacheado("vinheta", JX1 - JX0, JY1 - JY0, _d), JX0, JY0)


def capa(cv, t, t_sai, linha1, linha2):
    sai = e_inout(prog(t, t_sai, t_sai + 0.45))
    if sai >= 1:
        return
    a = 1 - sai
    pulso = 1 + 0.02 * math.sin(t * 5)
    cv.save(); cv.translate(CX, 168 - 50 * sai); cv.scale(pulso, pulso)
    texto(cv, linha1, 0, 0, F_BLACK, 74, "#FFFFFF", int(255 * a), contorno=10)
    texto(cv, linha2, 0, 84, F_BLACK, 74, "#F5C04A", int(255 * a), contorno=10)
    cv.restore()


def moldura(cv, t, a, varre=0.0):
    if a <= 0:
        return
    rr = skia.RRect.MakeRectXY(JAN, JAN_R, JAN_R)
    cv.drawRRect(rr, paint(CIANO, int(70 * a), "stroke", 2))
    cv.save(); cv.clipRRect(rr, skia.ClipOp.kIntersect, True)
    inner = skia.RRect.MakeRectXY(skia.Rect(JX0 + 36, JY0 + 36, JX1 - 36, JY1 - 36), 10, 10)
    cv.clipRRect(inner, skia.ClipOp.kDifference, True)
    off = (t * 24) % 6
    y = JY0 + off
    pl = paint("#FFFFFF", int(26 * a), "stroke", 2)
    while y < JY1:
        cv.drawLine(JX0, y, JX1, y, pl); y += 6
    cv.restore()
    if varre > 0:
        cv.save(); cv.clipRRect(rr, skia.ClipOp.kIntersect, True)
        y = lerp(JY0 - 80, JY1 + 20, varre)
        sh = skia.GradientShader.MakeLinear([skia.Point(0, y - 70), skia.Point(0, y + 10)],
                                            [_c(CIANO, 0), _c(CIANO, int(70 * a)), _c(CIANO, 0)], [0.0, 0.8, 1.0])
        cv.drawRect(skia.Rect(JX0, y - 70, JX1, y + 10), paint(CIANO, shader=sh))
        cv.drawLine(JX0, y, JX1, y, paint(CIANO, int(120 * a), "stroke", 2))
        cv.restore()
    for (x, y, sx, sy) in ((JX0, JY0, 1, 1), (JX1, JY0, -1, 1), (JX0, JY1, 1, -1), (JX1, JY1, -1, -1)):
        p = skia.Path(); p.moveTo(x + 6 * sx, y + 76 * sy); p.lineTo(x + 6 * sx, y + 6 * sy); p.lineTo(x + 76 * sx, y + 6 * sy)
        cv.drawPath(p, paint("#000000", int(110 * a), "stroke", 13, blur=3))
        cv.drawPath(p, paint("#FFFFFF", int(255 * a), "stroke", 7))
        cv.drawPath(p, paint(CIANO, int(255 * a), "stroke", 2))


def selo_var(cv, t, x, y, esc, a, chip=None, a_chip=1.0, pontos=-1.0, cor_chip="#FFFFFF"):
    if a <= 0:
        return
    cv.save(); cv.translate(x, y); cv.scale(esc, esc)
    f = skia.Font(F_BLACK, 52); lw = f.measureText(T_VAR)
    rr = skia.RRect.MakeRectXY(skia.Rect(0, 0, lw + 36, 64), 10, 10)
    cv.drawRRect(rr, paint("#000000", int(100 * a), blur=10))
    cv.drawRRect(rr, paint(SELO_BG, int(250 * a)))
    cv.drawRRect(rr, paint(CIANO, int(255 * a), "stroke", 4))
    texto(cv, T_VAR, 18, 52, F_BLACK, 52, "#FFFFFF", int(255 * a), centro=False)
    if chip and a_chip > 0:
        aa = a * a_chip
        fc = skia.Font(F_BLACK, 34); cw = fc.measureText(chip)
        extra = 70 if pontos >= 0 else 0
        x0 = lw + 50
        r2 = skia.RRect.MakeRectXY(skia.Rect(x0, 8, x0 + cw + 70 + extra, 56), 24, 24)
        cv.drawRRect(r2, paint(CARTAO, int(235 * aa)))
        cv.drawRRect(r2, paint(cor_chip, int((230 if cor_chip != "#FFFFFF" else 60) * aa), "stroke", 3 if cor_chip != "#FFFFFF" else 2))
        pisca = 0.55 + 0.45 * math.sin(t * 9)
        ponto = cor_chip if cor_chip != "#FFFFFF" else CIANO
        cv.drawCircle(x0 + 26, 32, 8, paint(ponto, int(255 * aa * (1.0 if cor_chip != "#FFFFFF" else pisca))))
        texto(cv, chip, x0 + 46, 44, F_BLACK, 34, cor_chip, int(255 * aa), centro=False)
        if pontos >= 0:
            for i in range(3):
                acesa = pontos > i / 3 + 0.02
                cv.drawCircle(x0 + 46 + cw + 22 + i * 22, 33, 7, paint(CIANO if acesa else "#FFFFFF", int(255 * aa) if acesa else int(70 * aa)))
    cv.restore()


def icone_pausa(cv, x, y, a):
    if a <= 0:
        return
    for dx in (-14, 14):
        r = skia.RRect.MakeRectXY(skia.Rect(x + dx - 8, y - 26, x + dx + 8, y + 26), 4, 4)
        cv.drawRRect(r, paint("#000000", int(110 * a), blur=6))
        cv.drawRRect(r, paint(CIANO, int(255 * a)))


def icone_rebobina(cv, x, y, a):
    if a <= 0:
        return
    for dx in (-24, 8):
        p = poli([(x + dx + 26, y - 24), (x + dx + 26, y + 24), (x + dx - 8, y)])
        cv.drawPath(p, paint("#000000", int(110 * a), blur=6))
        cv.drawPath(p, paint(CIANO, int(255 * a)))


def circulo_tele(cv, x, y, rx, ry, k, a, seed=0.0, pulso=0.0):
    if a <= 0 or k <= 0:
        return
    n = 72
    pts = []
    for i in range(n + 10):
        u = i / n
        ang = -math.pi * 0.62 + 2 * math.pi * u
        wob = 1 + 0.035 * math.sin(u * 2 * math.pi * 3 + seed) + 0.018 * math.sin(u * 2 * math.pi * 7 + 2 * seed)
        sp = 1 + 0.07 * u
        esc = (1 + 0.05 * pulso) * wob * sp
        pts.append((x + rx * esc * math.cos(ang), y + ry * esc * math.sin(ang)))
    p = poli(pts, fechar=False)
    cv.drawPath(p, _trim(paint(CARTAO, int(150 * a), "stroke", 15), k))
    cv.drawPath(p, _trim(paint(CIANO, int(110 * a * (0.6 + 0.4 * pulso)), "stroke", 18, blur=8), k))
    cv.drawPath(p, _trim(paint(CIANO, int(255 * a), "stroke", 8), k))


def linha_tele(cv, p0, p1, k, a, cor=CIANO, larg=7, traco=(22.0, 14.0)):
    """Linha TRACEJADA do telestrador, desenhada de p0 até p1 conforme k."""
    if a <= 0 or k <= 0:
        return
    q = lerp2(p0, p1, k)
    pt = paint(CARTAO, int(150 * a), "stroke", larg + 7)
    pt.setPathEffect(skia.DashPathEffect.Make(list(traco), 0.0))
    cv.drawLine(p0[0], p0[1], q[0], q[1], pt)
    pt = paint(cor, int(255 * a), "stroke", larg)
    pt.setPathEffect(skia.DashPathEffect.Make(list(traco), 0.0))
    cv.drawLine(p0[0], p0[1], q[0], q[1], pt)
    cv.drawCircle(p0[0], p0[1], larg * 0.9, paint(cor, int(255 * a)))


def carimbo_cor(cv, s, x, y, rot, t0, t, dur, cor, tam=88, esc0=1.9):
    k = t - t0
    if k < 0 or k > dur:
        return
    esc = lerp(esc0, 1.0, e_out(clamp(k / 0.16)))
    sai = prog(k, dur - 0.28, dur)
    esc *= lerp(1.0, 0.35, e_inout(sai))
    a = clamp(k / 0.06) * (1 - sai)
    xx = lerp(x, 330, e_inout(sai)); yy = lerp(y, 180, e_inout(sai))
    cv.save(); cv.translate(xx, yy); cv.rotate(rot * (1 - sai)); cv.scale(esc, esc)
    f = skia.Font(F_BLACK, tam); lw = f.measureText(s)
    rr = skia.RRect.MakeRectXY(skia.Rect(-lw / 2 - 32, -tam * 1.02, lw / 2 + 32, tam * 0.38), 16, 16)
    cv.drawRRect(rr, paint("#000000", int(110 * a), blur=16))
    cv.drawRRect(rr, paint(CARTAO, int(245 * a)))
    cv.drawRRect(rr, paint(cor, int(255 * a), "stroke", 9))
    rr2 = skia.RRect.MakeRectXY(skia.Rect(-lw / 2 - 20, -tam * 0.9, lw / 2 + 20, tam * 0.26), 10, 10)
    cv.drawRRect(rr2, paint(cor, int(120 * a), "stroke", 2.5))
    cv.drawString(s, -lw / 2, 0, f, paint(cor, int(255 * a)))
    cv.restore()


def ruido_vhs(cv, t, a):
    if a <= 0:
        return
    rng = np.random.default_rng(int(t * 60))
    cv.save(); cv.clipRRect(skia.RRect.MakeRectXY(JAN, JAN_R, JAN_R), skia.ClipOp.kIntersect, True)
    for k in range(3):
        yc = JY0 + ((t * (900 + 300 * k) + k * 330) % (JY1 - JY0))
        hb = 14 + 8 * k
        cv.drawRect(skia.Rect(JX0, yc, JX1, yc + hb), paint("#FFFFFF", int(40 * a)))
        for _ in range(26):
            x = rng.uniform(JX0, JX1); w = rng.uniform(10, 90); yy = yc + rng.uniform(0, hb)
            cv.drawLine(x, yy, x + w, yy, paint("#FFFFFF", int(rng.uniform(80, 200) * a), "stroke", rng.uniform(1, 3)))
    cv.restore()


def apito_icone(cv, x, y, esc, a, rot=-14.0):
    if a <= 0:
        return
    cv.save(); cv.translate(x, y); cv.rotate(rot); cv.scale(esc, esc)
    cv.drawArc(skia.Rect(-96, -40, -24, 40), 60, 240, False, paint(CIANO, int(230 * a), "stroke", 6))
    corpo_ = skia.Path(); corpo_.addCircle(0, 6, 38)
    corpo_ = uniao(corpo_, rr_path(-6, -34, 92, 2, 10))
    cv.drawPath(corpo_, paint("#000000", int(100 * a), blur=10))
    sh = skia.GradientShader.MakeLinear([skia.Point(0, -34), skia.Point(0, 44)], [_c("#F4F8FB"), _c("#B9C6D3")])
    cv.drawPath(corpo_, paint("#DDE6EE", int(255 * a), shader=sh))
    cv.drawPath(corpo_, paint(CIANO, int(255 * a), "stroke", 4))
    cv.drawCircle(-4, 10, 13, paint(SELO_BG, int(255 * a)))
    cv.drawRect(skia.Rect(70, -30, 86, -2), paint(SELO_BG, int(200 * a)))
    cv.drawCircle(-40, 0, 7, paint(CIANO, int(255 * a), "stroke", 4))
    cv.restore()


def profissional(cv, x, y, esc, a, mao_k=1.0):
    """Profissional de saúde de frente, sem rosto: jaleco branco, gola em V do pijama cirúrgico, estetoscópio
    no pescoço e a mão erguida (onde o apito pousa)."""
    if a <= 0:
        return None
    cv.save(); cv.translate(x, y); cv.scale(esc, esc)
    # braço erguido (lado direito da tela), atrás do corpo
    om = (70, -6); cot = (128, -40); mao_p = (124, lerp(-60, -132, mao_k))
    pinta(cv, capsula(om, cot, 46, 40), om, cot, 46, ("#C9D3DE", "#EEF2F6", "#FFFFFF", "#EEF2F6", "#C9D3DE"), a, linha="#9AA8B6")
    pinta(cv, capsula(cot, mao_p, 40, 36), cot, mao_p, 40, ("#C9D3DE", "#EEF2F6", "#FFFFFF", "#EEF2F6", "#C9D3DE"), a, linha="#9AA8B6")
    mp = capsula((mao_p[0], mao_p[1] + 4), (mao_p[0] + 2, mao_p[1] - 26), 34, 30)
    pinta(cv, mp, (mao_p[0], mao_p[1] + 4), (mao_p[0], mao_p[1] - 26), 34, PELE_AD, a, linha=LINHA_AD)
    # tronco (jaleco)
    om_p = skia.Path(); om_p.addRRect(skia.RRect.MakeRectXY(skia.Rect(-96, -20, 96, 140), 70, 70))
    clip = skia.Path(); clip.addRect(skia.Rect(-110, -30, 110, 110))
    om_p = skia.Op(om_p, clip, skia.PathOp.kIntersect_PathOp)
    cv.drawPath(om_p, paint("#000000", int(80 * a), blur=10))
    shj = skia.GradientShader.MakeLinear([skia.Point(-96, 0), skia.Point(96, 0)], [_c("#D5DDE6"), _c("#FFFFFF"), _c("#D5DDE6")])
    cv.drawPath(om_p, paint("#F4F7FA", int(255 * a), shader=shj))
    cv.drawPath(om_p, paint("#9AA8B6", int(220 * a), "stroke", 3))
    cv.drawPath(poli([(-30, -16), (30, -16), (0, 46)]), paint(TEAL, int(255 * a)))                  # gola em V
    cv.drawPath(poli([(-34, -18), (-6, 60), (-22, 108)], fechar=False), paint("#B9C6D3", int(255 * a), "stroke", 4))
    cv.drawPath(poli([(34, -18), (6, 60), (22, 108)], fechar=False), paint("#B9C6D3", int(255 * a), "stroke", 4))
    # estetoscópio
    est = suave([(-30, -18), (-44, 30), (-30, 66), (0, 76), (14, 70)], fechar=False)
    cv.drawPath(est, paint("#5B6676", int(255 * a), "stroke", 6))
    cv.drawPath(suave([(30, -18), (40, 20), (34, 50)], fechar=False), paint("#5B6676", int(255 * a), "stroke", 6))
    cv.drawCircle(16, 74, 11, paint("#C6D3DF", int(255 * a))); cv.drawCircle(16, 74, 11, paint("#5B6676", int(255 * a), "stroke", 3))
    # cabeça sem rosto, cabelo preso
    cv.drawCircle(0, -58, 40, paint("#000000", int(80 * a), blur=6))
    sh_c = skia.GradientShader.MakeRadial(skia.Point(-10, -70), 56, [_c(PELE_AD[2]), _c(PELE_AD[1]), _c(PELE_AD[0])], [0, 0.55, 1])
    cv.drawCircle(0, -58, 40, paint(PELE_AD[1], int(255 * a), shader=sh_c))
    cv.drawArc(skia.Rect(-42, -100, 42, -16), 190, 160, False, paint("#3A2A20", int(255 * a), "stroke", 16))
    cv.drawCircle(0, -104, 16, paint("#3A2A20", int(255 * a)))
    cv.restore()
    return (x + mao_p[0] * esc, y + (mao_p[1] - 22) * esc)


def selo_serie(cv, a):
    if a <= 0:
        return
    lw = larg_texto(T_SERIE, F_BLACK, 36)
    rr = skia.RRect.MakeRectXY(skia.Rect(CX - lw / 2 - 34, 148, CX + lw / 2 + 34, 208), 30, 30)
    cv.drawRRect(rr, paint(SELO_BG, int(235 * a)))
    cv.drawRRect(rr, paint(CIANO, int(255 * a), "stroke", 3))
    texto(cv, T_SERIE, CX, 191, F_BLACK, 36, CIANO, int(255 * a))


def marca_x(cv, x, y, r, cor, a):
    if a <= 0:
        return
    cv.drawCircle(x, y, r + 6, paint("#000000", int(90 * a), blur=8))
    cv.drawCircle(x, y, r, paint(CARTAO, int(235 * a)))
    cv.drawCircle(x, y, r, paint(cor, int(255 * a), "stroke", 5))
    d = r * 0.45
    cv.drawLine(x - d, y - d, x + d, y + d, paint(cor, int(255 * a), "stroke", 9))
    cv.drawLine(x - d, y + d, x + d, y - d, paint(cor, int(255 * a), "stroke", 9))


def marca_ok(cv, x, y, r, cor, a):
    if a <= 0:
        return
    cv.drawCircle(x, y, r + 6, paint("#000000", int(90 * a), blur=8))
    cv.drawCircle(x, y, r, paint(CARTAO, int(235 * a)))
    cv.drawCircle(x, y, r, paint(cor, int(255 * a), "stroke", 5))
    p = poli([(x - r * 0.45, y + r * 0.02), (x - r * 0.12, y + r * 0.35), (x + r * 0.5, y - r * 0.32)], fechar=False)
    pt = paint(cor, int(255 * a), "stroke", 9); pt.setStrokeCap(skia.Paint.kRound_Cap); pt.setStrokeJoin(skia.Paint.kRound_Join)
    cv.drawPath(p, pt)


def pop_marca(cv, fn, x, y, t, t0, a, r=34):
    k = e_back(prog(t, t0, t0 + 0.24))
    if k <= 0 or a <= 0:
        return
    cv.save(); cv.translate(x, y); s = clamp(k, 0, 1.2); cv.scale(s, s)
    fn(cv, 0, 0, r, VERDE if fn is marca_ok else AMBAR, a)
    cv.restore()


def legenda_var(cv, blocos, t, destaque, y_base=1395, tam=80):
    """Cópia da legenda karaokê do piloto (a palavra ativa cresce a partir do próprio centro)."""
    import re
    vivo = None
    for i, b in enumerate(blocos):
        ini = b[0]["t"] - 0.12
        fim = blocos[i + 1][0]["t"] - 0.12 if i + 1 < len(blocos) else b[-1]["t"] + b[-1]["d"] + 2.5
        if ini <= t < fim:
            vivo = b; break
    if not vivo:
        return
    esp = 26; linhas, linha, lw = [], [], 0
    for p in vivo:
        w = larg_texto(p["tok"].upper(), F_BLACK, tam)
        if linha and lw + esp + w > 920:
            linhas.append(linha); linha, lw = [], 0
        linha.append((p, w)); lw += (esp if lw else 0) + w
    if linha:
        linhas.append(linha)
    entrada = e_out(clamp((t - (vivo[0]["t"] - 0.12)) / 0.15))
    alt = tam * 1.18
    y = y_base - (len(linhas) - 1) * alt / 2 + (1 - entrada) * 24
    for ln in linhas:
        total = sum(w for _, w in ln) + esp * (len(ln) - 1); x = CX - total / 2
        for p, w in ln:
            k = t - p["t"]; base = re.sub(r"[.,:;!?—]", "", p["tok"]).lower()
            dita = k >= -0.03; falando = p["t"] - 0.03 <= t <= p["t"] + p["d"] + 0.06
            cor, a = (OURO, 255) if falando else ((OURO if base in destaque else "#FFFFFF"), 255) if dita else ("#FFFFFF", 105)
            esc = 1.0 + (min(0.06, 14.0 / max(w, 1.0)) * (1 - e_out(clamp(k / 0.16))) if dita else 0.0)
            cv.save(); cv.translate(x + w / 2, y); cv.scale(esc, esc)
            texto(cv, p["tok"].upper(), -w / 2, 0, F_BLACK, tam, cor, int(a * entrada), centro=False, contorno=12)
            cv.restore()
            x += w + esp
        y += alt


def interface_var(cv, t, T, blocos, destaque):
    """Cópia do piloto + (storyboard) a legenda some durante os CHECANDO (o rodapé CFM fica)."""
    t_cta = T["manda"] - 0.15
    checando = any(T[pd + "_fim"] + 0.1 < t < T[vd] - 0.12 for pd, vd, _, _ in VEREDITOS)
    if t < t_cta and not checando:
        legenda_var(cv, blocos, t, destaque)
    if 3.0 <= t < t_cta:
        a = prog(t, 3.0, 3.6)
        texto(cv, SIG, CX, 1585, F_SEMI, 27, "#FFFFFF", int(200 * a))
        texto(cv, DISC, CX, 1620, F_REG, 23, "#FFFFFF", int(150 * a))
    if t >= t_cta:
        a = prog(t, t_cta, t_cta + 0.35)
        cv.drawRect(skia.Rect(0, 0, W, H), paint(BG_OUT, int(175 * a)))
        legenda_var(cv, blocos, t, destaque, y_base=700, tam=92)
        aviao(cv, t, T["manda"] + 0.2)
        rr = skia.RRect.MakeRectXY(skia.Rect(150, 1060, 930, 1214), 28, 28)
        cv.drawRRect(rr, paint("#0B1824", int(230 * a))); cv.drawRRect(rr, paint(OURO, int(255 * a), "stroke", 3))
        texto(cv, "Dr. Rafael Vargas · Médico ortopedista", CX, 1112, F_BLACK, 36, "#FFFFFF", int(255 * a))
        texto(cv, "CRM-SP 226103 · RQE 137901 · @rafaelvargasmd", CX, 1154, F_SEMI, 28, OURO, int(255 * a))
        texto(cv, DISC, CX, 1190, F_REG, 22, "#FFFFFF", int(170 * a))


# ================================================================== quadro
VEREDITOS = (("passa", "anulado1", T_ANUL, AMBAR), ("pode1", "anulado2", T_ANUL, AMBAR),
             ("pode2", "validado", T_VALID, VERDE))
DUR_CARIMBOS = (1.25, 1.2, 0.85)
CARIMBO_Y = JY0 + 190


def chip_estado(t, T):
    """(texto, alfa, pontos, cor): LANCE n -> CHECANDO -> (carimbo) -> veredito -> JEITO CERTO (verde) quando
    a imagem mostra o certo. No lance 3, durante o replay do jeito errado o chip some (só o VAR)."""
    cortes = (0.0, T["corte2"], T["corte3"], 1e9)
    certo = (T["cruza"], T["gelo"] - 0.08, None)
    for k, (pd, vd, s, cor) in enumerate(VEREDITOS):
        if not (cortes[k] <= t < cortes[k + 1]):
            continue
        if t < T[pd + "_fim"] + 0.04:
            a = 1.0 if k == 0 else prog(t, cortes[k] + 0.45, cortes[k] + 0.6)
            return T_LANCE[k], a, -1, "#FFFFFF"
        if t < T[vd] - 0.04:
            t0 = T[pd + "_fim"] + 0.04
            return T_CHEC, 1.0, prog(t, t0, T[vd] - 0.12), "#FFFFFF"
        dur = DUR_CARIMBOS[k]
        if t < T[vd] + dur - 0.05:
            return None, 0.0, -1, "#FFFFFF"
        if k == 2:
            if t < T["certo3"] + 0.2:
                return None, 0.0, -1, "#FFFFFF"
            return s, prog(t, T["certo3"] + 0.2, T["certo3"] + 0.4), -1, cor
        if t >= certo[k]:
            return T_CERTO, prog(t, certo[k], certo[k] + 0.18), -1, VERDE
        a = prog(t, T[vd] + dur - 0.1, T[vd] + dur + 0.1) * (1 - prog(t, certo[k] - 0.12, certo[k]))
        return s, a, -1, cor
    return None, 0.0, -1, "#FFFFFF"


def cena(cv, t, T):
    info = {}
    if t < T["corte1"]:
        ank, push = close_frente(cv, t, T)
        info.update(lance=1, close=True, ank=ank, push=push)
    elif t < T["corte2"]:
        cam, kid = cena_l1_aberta(cv, t, T)
        info.update(lance=1, cam=cam, kid=kid)
    elif t < T["corte3"]:
        cam, kid, e = cena_l2(cv, t, T)
        info.update(lance=2, cam=cam, kid=kid, e=e)
    elif t < T["certo3"]:
        info.update(lance=3, **cena_l3(cv, t, T))
    elif t < T["sai3"]:
        kw = prog(t, T["certo3"], T["certo3"] + 0.36)
        cam = CAM_L3_CERTO
        if kw < 1:
            xw = lerp(JX0 - 10, JX1 + 10, e_inout(kw))
            cv.save(); cv.clipRect(skia.Rect(xw, 0, W, H), True)
            cena_l3(cv, t, T)
            cv.restore()
            cv.save(); cv.clipRect(skia.Rect(0, 0, xw, H), True)
            kid, vv = cena_l3_certo(cv, t, T, cam)
            cv.restore()
            cv.drawLine(xw, JY0, xw, JY1, paint(CIANO, 160, "stroke", 26, blur=10))
            cv.drawLine(xw, JY0, xw, JY1, paint("#FFFFFF", 255, "stroke", 6))
        else:
            kid, vv = cena_l3_certo(cv, t, T, cam)
        info.update(lance=3, certo=True, cam=cam, kid=kid, vv=vv)
    else:
        cam = cena_l3_sai(cv, t, T)
        info.update(lance=3, sai=True, cam=cam)
    return info


def hud_lance(cv, t, T, info):
    """Grafismos do VAR sobre a imagem (coordenadas de tela), por lance."""
    lance = info.get("lance")
    cam = info.get("cam")
    if lance == 1 and info.get("close"):
        ax, ay = info["ank"]
        # círculo no tornozelo (quadro 0 e o replay) e a seta âmbar do giro, fora do pé
        if t < T["var"]:
            a0, k0 = 1.0, 1.0
        elif t < T["var"] + 0.5:
            a0, k0 = 1 - prog(t, T["var"], T["var"] + 0.12), 1.0
        else:
            a0, k0 = janela(t, T["pe1"], T["corte1"], 0.15, 0.05), e_out(prog(t, T["pe1"], T["pe1"] + 0.35))
        pul = 1.5 * max(0.0, 1 - abs(t - T["chama"] - 0.1) / 0.18) + (0.5 + 0.5 * math.sin(t * 8))
        ps = info["push"]
        circulo_tele(cv, ax - 10 * ps, ay + 40 * ps, 150 * ps, 140 * ps, k0, a0, 0.7, pul)
        a_s = (1.0 if t < T["var"] else janela(t, T["pe1"] + 0.1, T["corte1"], 0.15, 0.05))
        if t >= T["var"] and t < T["var"] + 0.5:
            a_s = 1 - prog(t, T["var"], T["var"] + 0.15)
        if a_s > 0:
            arco = skia.Path(); r = 96 * ps; cx_, cy_ = ax + 30 * ps, ay + 30 * ps
            arco.addArc(skia.Rect(cx_ - r, cy_ - r, cx_ + r, cy_ + r), -60, 95)
            cv.drawPath(arco, paint(CARTAO, int(170 * a_s), "stroke", 18))
            cv.drawPath(arco, paint(AMBAR, int(255 * a_s), "stroke", 10))
            ang = math.radians(35)
            pxx, pyy = cx_ + r * math.cos(ang), cy_ + r * math.sin(ang)
            ponta(cv, pxx, pyy, ang + math.pi / 2, 32, AMBAR, a_s)
    elif lance == 1:
        kid = info["kid"]
        jk = juntas(kid, KID1)
        hx, hy = na_tela(cam, *jk["aN"])
        s = cam[0]
        k1 = e_out(prog(t, T["congela1"] + 0.05, T["congela1"] + 0.4))
        fora = 1 - prog(t, T["anulado1"] + 0.25, T["anulado1"] + 0.5)
        pul = 0.5 + 0.5 * math.sin(t * 8) if T["passa_fim"] < t < T["anulado1"] else 0.0
        circulo_tele(cv, hx + 14 * s, hy + 4 * s, 64 * s, 60 * s, k1, k1 * fora, 0.7, pul)
        # a linha lateral marcada pelo telestrador (de baixo para o fundo)
        k_l = e_inout(prog(t, T["tira"] + 0.05, T["jogo"] + 0.15))
        a_l = janela(t, T["tira"] + 0.05, T["corte2"] - 0.1, 0.1, 0.1)
        if a_l > 0:
            p0 = na_tela(cam, linha_lateral_pts(1360), 1360); p1 = na_tela(cam, linha_lateral_pts(760), 760)
            linha_tele(cv, p0, p1, k_l, a_l, cor=CIANO, larg=9, traco=(26.0, 16.0))
            cruzou = prog(t, T["cruza"], T["cruza"] + 0.25)
            if cruzou > 0:
                linha_tele(cv, p0, p1, 1.0, a_l * cruzou, cor=VERDE, larg=9, traco=(26.0, 16.0))
        # placa de substituição (só a seta de saída)
        a_p = janela(t, T["tira"] - 0.02, T["pisa"], 0.12, 0.25)
        kp = e_back(prog(t, T["tira"] - 0.02, T["tira"] + 0.26))
        if a_p > 0:
            cv.save(); cv.translate(860, 560); s_ = clamp(kp, 0, 1.15); cv.scale(s_, s_)
            placa_subst(cv, 0, 0, a_p, t)
            cv.restore()
        # "Não força o apoio": o vão tracejado verde entre o pé e a grama
        a_v = janela(t, T["pisa"] - 0.05, T["corte2"] - 0.05, 0.2, 0.1)
        if a_v > 0:
            pe = jk["aN"]
            p0 = na_tela(cam, pe[0], pe[1] + 24); p1 = na_tela(cam, pe[0], G - 2)
            linha_tele(cv, p0, p1, e_out(prog(t, T["pisa"] - 0.05, T["pisa"] + 0.25)), a_v, cor=VERDE, larg=7, traco=(12.0, 9.0))
            cv.drawLine(p1[0] - 34, p1[1], p1[0] + 34, p1[1], paint(VERDE, int(255 * a_v), "stroke", 6))
            pop_marca(cv, marca_ok, p0[0] + 120, p0[1] + 10, t, T["testar"], a_v)
    elif lance == 2:
        e = info["e"]
        kid = info["kid"]
        jk = juntas(kid, KID1)
        ax, ay = na_tela(cam, *jk["aN"])
        s = cam[0]
        k1 = e_out(prog(t, T["pode1"] + 0.12, T["pode1"] + 0.47))
        fora = 1 - prog(t, T["anulado2"] + 0.25, T["anulado2"] + 0.45)
        pul = 0.5 + 0.5 * math.sin(t * 8) if T["pode1_fim"] < t < T["anulado2"] else 0.0
        circulo_tele(cv, ax + 10 * s, ay - 20 * s, 96 * s, 80 * s, k1, k1 * fora, 4.3, pul)
        if e["replay"] > 0:
            cv.drawRect(JAN, paint("#0E2A3A", int(70 * e["replay"])))
        # o inchaço: setas âmbar curtas FORA da pele, apontando para fora
        a_i = janela(t, T["aumenta"] + 0.05, T["gelo"] - 0.15, 0.15, 0.15) if t > T["anulado2"] + 0.3 else 0.0
        if a_i > 0:
            # (revisão) setas curtas ENCOSTADAS no contorno inchado, em leque para os lados e para cima
            # (nunca para baixo nem para a mochila)
            borda = incha_mundo(kid, KID1)
            d, f, _ = shin_frame(jk["kN"], jk["aN"])
            for th in (0.0, 90.0, 140.0):
                r_ = math.radians(th); w_ = (math.cos(r_) * d[0] + math.sin(r_) * f[0], math.cos(r_) * d[1] + math.sin(r_) * f[1])
                rb = 0.0
                while rb < 90 and borda.contains(jk["aN"][0] + w_[0] * rb, jk["aN"][1] + w_[1] * rb):
                    rb += 0.5
                q0 = na_tela(cam, jk["aN"][0] + w_[0] * (rb + 3), jk["aN"][1] + w_[1] * (rb + 3))
                q1 = na_tela(cam, jk["aN"][0] + w_[0] * (rb + 21), jk["aN"][1] + w_[1] * (rb + 21))
                seta(cv, q0[0], q0[1], q1[0], q1[1], AMBAR, a_i, larg=8, tam=24)
        # X âmbar sobre as mãos (no "inchaço"); as mãos saem
        a_x = janela(t, T["aumenta"] - 0.12, T["aumenta"] + 0.4, 0.05, 0.12) if t > T["anulado2"] + 0.3 else 0.0
        if a_x > 0:
            bx, by = na_tela(cam, *_centro_pe(jk, ROT_PE2))
            sob = 180 * e_inout(prog(t, T["aumenta"] + 0.05, T["aumenta"] + 0.45))
            pop_marca(cv, marca_x, bx + 40 * s + 0.6 * sob, by - 70 * s - sob, t, T["aumenta"] - 0.12, a_x, r=36)
        # visto verde no gelo; seta verde do pé subindo
        a_g = janela(t, T["pano"] + 0.05, T["corte3"], 0.15, 0.1)
        if a_g > 0:
            pop_marca(cv, marca_ok, ax + 150 * s, ay - 120 * s, t, T["pano"] + 0.05, a_g, r=34)
        a_c = janela(t, T["pe2"], T["corte3"], 0.15, 0.1)
        if a_c > 0:
            k_c = e_out(prog(t, T["pe2"], T["cima_fim"]))
            x0 = ax + 130 * s
            seta(cv, x0, ay + 30 * s, x0, ay + 30 * s - 120 * s * k_c, VERDE, a_c, larg=10, tam=30)
    elif lance == 3 and not info.get("certo") and not info.get("sai"):
        jw = info["jw"]; kid = info["kid"]
        s = cam[0]
        if kid.get("kink"):
            # o "torto": duas linhas tracejadas ciano ao longo das duas metades do antebraço (ficam até o fim do
            # carimbo VALIDADO — revisão)
            k_t = prog(t, T["torto1"] + 0.05, T["torto1"] + 0.45)
            a_t = janela(t, T["torto1"] + 0.05, T["validado"] + DUR_CARIMBOS[2] - 0.1, 0.1, 0.2)
            linhas_torto(cv, cam, jw, k_t, a_t)
            # círculo no antebraço no "pode?"
            k1 = e_out(prog(t, T["pode2"] + 0.12, T["pode2"] + 0.47))
            fora = 1 - prog(t, T["validado"] + 0.25, T["validado"] + 0.45)
            pul = 0.5 + 0.5 * math.sin(t * 8) if T["pode2_fim"] < t < T["validado"] else 0.0
            mx, my = na_tela(cam, *jw["meio"])
            circulo_tele(cv, mx + 10 * s, my + 2 * s, 110 * s, 70 * s, k1, k1 * fora, 2.1, pul)
        # replay do jeito errado: imagem fria, a seta âmbar de tração ao longo do antebraço e o X
        r = info["rep"]
        rep = janela(t, r["r0"], T["certo3"], 0.08, 0.05)
        if rep > 0:
            cv.drawRect(JAN, paint("#0E2A3A", int(70 * rep)))
            if r["seta"] > 0:
                c, u, n = _eixo_punho(jw)
                q0 = na_tela(cam, c[0] - n[0] * 34 - u[0] * 6, c[1] - n[1] * 34 - u[1] * 6)
                q1 = na_tela(cam, c[0] - n[0] * 34 + u[0] * (6 + 62 * r["seta_k"]), c[1] - n[1] * 34 + u[1] * (6 + 62 * r["seta_k"]))
                seta(cv, q0[0], q0[1], q1[0], q1[1], AMBAR, r["seta"], larg=10, tam=30)
            p = info.get("mao_puxa")
            if p is not None:
                c, u, n = _eixo_punho(jw)
                xx, yy = na_tela(cam, c[0] + u[0] * 64 + n[0] * 36, c[1] + u[1] * 64 + n[1] * 36)
                a_x = janela(t, r["x_t0"], T["certo3"], 0.05, 0.05)
                pop_marca(cv, marca_x, xx, yy, t, r["x_t0"], a_x, r=36)
    elif lance == 3 and info.get("certo"):
        kid = info["kid"]; jk = juntas(kid, KID2)
        # (revisão) logo depois da cortina, as MESMAS linhas do telestrador sobre a tala: o braço ficou como estava
        a_l = janela(t, T["certo3"] + 0.32, T["certo3"] + 1.05, 0.12, 0.25)
        linhas_torto(cv, cam, jk, e_out(prog(t, T["certo3"] + 0.32, T["certo3"] + 0.6)), a_l)
        vv = info.get("vv", 0.0)
        if vv > 0:
            xx, yy = na_tela(cam, *jk["mao"])
            pop_marca(cv, marca_ok, xx + 120, yy - 150, t, T["certo3"] + 0.65, vv, r=36)


def linhas_torto(cv, cam, jw, k_t, a_t, folga=24.0):
    """O telestrador mostra o 'torto' LOGO ACIMA do braço (revisão: em cima dele escondia a dobra): a linha da metade
    de cima do antebraço seguindo reto, a da metade de baixo indo para onde ela vai, e o arco do ângulo (sem número)."""
    if a_t <= 0 or k_t <= 0:
        return
    cot, meio, mao_p = jw["eN"], jw["meio"], jw["mao"]
    d1 = (meio[0] - cot[0], meio[1] - cot[1]); d2 = (mao_p[0] - meio[0], mao_p[1] - meio[1])
    L1 = math.hypot(*d1) or 1.0; L2 = math.hypot(*d2) or 1.0
    n1 = (d1[1] / L1, -d1[0] / L1); n2 = (d2[1] / L2, -d2[0] / L2)
    if n1[1] > 0:
        n1 = (-n1[0], -n1[1])
    if n2[1] > 0:
        n2 = (-n2[0], -n2[1])
    nb = (n1[0] + n2[0], n1[1] + n2[1]); Lb = math.hypot(*nb) or 1.0
    v = (nb[0] / Lb * folga, nb[1] / Lb * folga)
    c0, m0, h0 = (cot[0] + v[0], cot[1] + v[1]), (meio[0] + v[0], meio[1] + v[1]), (mao_p[0] + v[0], mao_p[1] + v[1])
    A = na_tela(cam, c0[0] - d1[0] * 0.2, c0[1] - d1[1] * 0.2); B = na_tela(cam, m0[0] + d1[0] * 1.6, m0[1] + d1[1] * 1.6)
    C = na_tela(cam, *m0); D = na_tela(cam, h0[0] + d2[0] * 0.9, h0[1] + d2[1] * 0.9)
    linha_tele(cv, A, B, e_out(clamp(k_t * 1.8)), a_t, larg=7)
    linha_tele(cv, C, D, e_out(clamp(k_t * 1.8 - 0.8)), a_t, larg=7)
    k_a = e_out(clamp(k_t * 2 - 1.2))
    if k_a > 0:
        M = na_tela(cam, *m0); R = 1.25 * L2 * cam[0]
        a1 = math.degrees(math.atan2(d1[1], d1[0])); a2 = math.degrees(math.atan2(d2[1], d2[0]))
        arco = skia.Path(); arco.addArc(skia.Rect(M[0] - R, M[1] - R, M[0] + R, M[1] + R), a1, (a2 - a1) * k_a)
        cv.drawPath(arco, paint(CARTAO, int(150 * a_t), "stroke", 11))
        cv.drawPath(arco, paint(CIANO, int(255 * a_t), "stroke", 5))


def quadro(cv, t, T, blocos, ep):
    fundo(cv, t)
    t_off = T["off"]
    k_v = prog(t, t_off, t_off + 0.22) ** 2; k_h = e_inout(prog(t, t_off + 0.2, t_off + 0.36))
    tela_ligada = t < t_off + 0.38
    jan_rr = skia.RRect.MakeRectXY(JAN, JAN_R, JAN_R)
    a_tv = 1 - prog(t, t_off + 0.6, t_off + 0.95)
    if a_tv > 0:
        cv.drawRRect(jan_rr, paint("#0E151D", int(255 * a_tv)))
    info = {}
    if tela_ligada:
        cv.save()
        if t >= t_off:
            sy = max(0.006, 1 - clamp(k_v)); sx = max(0.01, 1 - k_h)
            cv.translate(JCX, JCY); cv.scale(sx, sy); cv.translate(-JCX, -JCY)
        cv.clipRRect(jan_rr, skia.ClipOp.kIntersect, True)
        rebob = janela(t, T["var"], T["var"] + 0.5, 0.03, 0.06)
        if rebob > 0:
            cv.translate(6 * math.sin(t * 97) * rebob, 0)
        info = cena(cv, t, T)
        vinheta(cv)
        if t >= t_off:
            cv.drawRect(JAN, paint("#FFFFFF", int(220 * clamp(k_v * 1.2))))
        cv.restore()
        ruido_vhs(cv, t, rebob)
    if t_off <= t < t_off + 0.62:
        k = prog(t, t_off + 0.16, t_off + 0.62)
        a_lin = clamp((0.3 - (1 - k_v)) / 0.25)
        if t < t_off + 0.36 and a_lin > 0:
            w = (JX1 - JX0) / 2 * max(0.02, 1 - k_h)
            cv.drawLine(JCX - w, JCY, JCX + w, JCY, paint("#FFFFFF", int(240 * a_lin), "stroke", 6, blur=3))
            cv.drawLine(JCX - w, JCY, JCX + w, JCY, paint("#DFF6FF", int(255 * a_lin), "stroke", 3))
        r = lerp(10, 2, k)
        a_pt = prog(t, t_off + 0.18, t_off + 0.26) * (1 - k)
        cv.drawCircle(JCX, JCY, r * 3, paint(CIANO, int(120 * a_pt), blur=10))
        cv.drawCircle(JCX, JCY, r, paint("#FFFFFF", int(255 * a_pt)))

    a_hud = 1 - prog(t, t_off + 0.2, t_off + 0.45)
    if tela_ligada and a_hud > 0:
        cv.save(); cv.clipRRect(jan_rr, skia.ClipOp.kIntersect, True)
        hud_lance(cv, t, T, info)
        for t0, forca in ((T["congela1"], 150), (T["pode1"], 150), (T["torto1"], 120), (T["pode2"], 150),
                          (T["corte1"], 210), (T["corte2"], 190), (T["corte3"], 190), (T["sai3"], 120)):
            k = t - t0
            if 0 <= k < 0.16:
                cv.drawRect(JAN, paint("#FFFFFF", int(forca * (1 - k / 0.16))))
        cv.restore()
        r0 = T["validado"] + DUR_CARIMBOS[2] - 0.1
        ruido_vhs(cv, t, max(janela(t, r0 - 0.06, r0 + 0.12, 0.03, 0.06), janela(t, T["logo"] - 0.34, T["logo"] - 0.12, 0.03, 0.06)))
        varre = 0.0
        for pd, vd, _, _ in VEREDITOS:
            if T[pd + "_fim"] < t < T[vd]:
                varre = prog(t, T[pd + "_fim"], T[vd] - 0.05)
        moldura(cv, t, a_hud, varre)
        congelado = t < T["var"] or (T["congela1"] <= t < T["anulado1"] + 0.3) or \
            (T["torto1"] + 0.02 <= t < T["imobilizar"] - 0.05) or \
            any(T[pd] + 0.02 <= t < T[vd] for pd, vd, _, _ in VEREDITOS[1:])
        icone_pausa(cv, JX1 - 70, JY1 - 74, a_hud * (1.0 if congelado else 0.0))
        a_reb = max(janela(t, T["var"], T["var"] + 0.5, 0.03, 0.08),
                    janela(t, T["logo"] - 0.34, T["logo"], 0.03, 0.08),
                    janela(t, r0 - 0.04, T["nao2"] + 0.1, 0.06, 0.08))
        icone_rebobina(cv, JX1 - 76, JY1 - 74, a_hud * a_reb * (0.0 if congelado else 1.0))
        for k_c, ((pd, vd, s_, cor), dur) in enumerate(zip(VEREDITOS, DUR_CARIMBOS)):
            cx_c, cy_c = CARIMBO_L3 if k_c == 2 else (CX, CARIMBO_Y)
            carimbo_cor(cv, s_, cx_c, cy_c, -5, T[vd] - 0.02, t, dur, cor)
        for t0, s in ((T["corte2"], T_LANCE[1]), (T["corte3"], T_LANCE[2])):
            k = t - t0
            if -0.02 <= k < 0.6:
                a = prog(k, 0.0, 0.08) * (1 - prog(k, 0.42, 0.6))
                esc = lerp(1.25, 1.0, e_out(prog(k, 0.0, 0.16)))
                cv.save(); cv.translate(JX0 + 210, JY0 + 112); cv.scale(esc, esc)
                f = skia.Font(F_BLACK, 70); lw = f.measureText(s)
                rr = skia.RRect.MakeRectXY(skia.Rect(-lw / 2 - 34, -70, lw / 2 + 34, 26), 16, 16)
                cv.drawRRect(rr, paint(CARTAO, int(225 * a))); cv.drawRRect(rr, paint(CIANO, int(255 * a), "stroke", 4))
                texto(cv, s, 0, 0, F_BLACK, 70, "#FFFFFF", int(255 * a))
                cv.restore()

    t_capa = T["passa_fim"] + 0.06
    sobe = e_inout(prog(t, t_capa + 0.45, t_capa + 0.85))
    chip, a_chip, pontos, cor_chip = chip_estado(t, T)
    k_s = prog(t, T["var"] - 0.04, T["var"] + 0.14)
    esc_s = lerp(0.92, 1.08, sobe) * (1 + 0.25 * (1 - e_back(k_s))) if k_s < 1 else lerp(0.92, 1.08, sobe)
    selo_var(cv, t, lerp(56, 64, sobe), lerp(JY0 + 24, 146, sobe), esc_s, a_hud * clamp(k_s * 1.5), chip, a_chip,
             pontos, cor_chip)

    # ---------- fim: na dúvida, quem apita é a avaliação (o apito passa para a profissional de saúde)
    a_pr = prog(t, T["na"] - 0.1, T["na"] + 0.2) * (1 - prog(t, T["manda"] - 0.35, T["manda"] - 0.1))
    if a_pr > 0:
        cv.drawCircle(CX, 800, 270, paint(TEAL, int(40 * a_pr), blur=60))
        ent = e_back(prog(t, T["na"] - 0.1, T["na"] + 0.3))
        mk = e_out(prog(t, T["quem"] - 0.2, T["quem"] + 0.15))
        alvo = profissional(cv, CX - 30, 900 + 40 * (1 - clamp(ent)), 2.0 * clamp(ent, 0, 1.1), a_pr, mk)
        ka = e_out(prog(t, T["quem"] - 0.05, T["apita"] + 0.15))
        if ka > 0 and alvo is not None:
            x = lerp(140, alvo[0], ka); y = lerp(330, alvo[1], ka) - 60 * math.sin(math.pi * ka)
            balanco = 10 * math.sin(max(0.0, t - T["apita"]) * 9) * math.exp(-max(0.0, t - T["apita"]) * 3)
            apito_icone(cv, x, y, lerp(0.7, 1.0, ka), a_pr * clamp(ka * 3), -14 + balanco)
        pul = max(0.0, 1 - abs(t - T["apita"] - 0.15) / 0.2)
        if pul > 0:
            cv.drawCircle(CX - 30, 760, 230 * (1 + 0.06 * pul), paint(TEAL, int(70 * pul), "stroke", 6, blur=4))
    selo_serie(cv, prog(t, T["medico"] - 0.1, T["medico"] + 0.2) * (1 - prog(t, T["manda"] - 0.3, T["manda"])))

    capa(cv, t, t_capa, ep["gancho"][0], ep["gancho"][1])
    interface_var(cv, t, T, blocos, DESTAQUE)


# ================================================================== som (sintetizado aqui, sem licença)
SR = som.SR


def _env(n, a=0.005, r=0.2):
    return som._env(n, a, r)


def _passa_banda(x, f_lo, f_hi):
    lp = som._onepole_lp(x, f_hi)
    return lp - som._onepole_lp(lp, f_lo)


def apito(dur=0.30, seed=11, ganho=0.55, solta=0.04):
    n = int(dur * SR); t = np.arange(n) / SR
    fm = 3150 + 130 * np.sin(2 * np.pi * 41 * t)
    ph = 2 * np.pi * np.cumsum(fm) / SR
    am = 1 - 0.55 * (0.5 + 0.5 * np.sin(2 * np.pi * 41 * t + 0.7))
    tom = (np.sin(ph) + 0.22 * np.sin(2 * ph) + 0.08 * np.sin(3 * ph)) * am
    sopro = _passa_banda(np.random.default_rng(seed).standard_normal(n), 2000, 6000) * 0.5
    env = np.clip(t / 0.012, 0, 1) * np.clip((dur - t) / solta, 0, 1)
    return (tom + sopro * 0.6) * env * ganho


def apito_final():
    return np.concatenate([apito(0.14, 21), np.zeros(int(0.07 * SR)), apito(0.42, 23, solta=0.14)])


def rebobinar(seed=31):
    n = int(0.5 * SR); t = np.arange(n) / SR
    x = np.random.default_rng(seed).standard_normal(n)
    fc = 600 + 2600 * np.abs(np.sin(np.pi * t / 0.5 * 1.5))
    y = np.zeros(n); acc = 0.0
    for i in range(n):
        a = np.exp(-2 * np.pi * fc[i] / SR); acc = (1 - a) * x[i] + a * acc; y[i] = acc
    f = 900 * np.exp(-t * 3.2) + 200
    saw = 2 * ((np.cumsum(f) / SR) % 1.0) - 1
    env = np.clip(t / 0.02, 0, 1) * np.clip((0.5 - t) / 0.05, 0, 1)
    return (y * 0.9 + saw * 0.18 + x * 0.04) * env * 0.8


def bipe(f=1600.0, dur=0.075):
    n = int(dur * SR); t = np.arange(n) / SR
    env = np.clip(t / 0.004, 0, 1) * np.clip((dur - t) / 0.02, 0, 1)
    return np.sin(2 * np.pi * f * t) * env * 0.42


def bipe_alto():
    return bipe(2100.0, 0.11)


def obturador(seed=41):
    a = som.tick(seed) * 0.8
    gap = np.zeros(int(0.05 * SR))
    n = int(0.06 * SR)
    ruido = np.random.default_rng(seed).standard_normal(n) * _env(n, 0.001, 0.015) * 0.35
    b = som.tick(seed + 1) * 0.6
    return np.concatenate([a, gap, b + np.pad(ruido, (0, max(0, len(b) - n)))[:len(b)]])


def tv_desliga(seed=71):
    n = int(0.36 * SR); t = np.arange(n) / SR
    f = 1200 * np.exp(-t * 10) + 60
    y = np.sin(2 * np.pi * np.cumsum(f) / SR) * _env(n, 0.002, 0.22) * 0.55
    rng = np.random.default_rng(seed)
    for _ in range(14):
        p = int(rng.uniform(0, n - 600)); m = int(rng.uniform(80, 400))
        y[p:p + m] += rng.standard_normal(m) * _env(m, 0.0002, 0.003) * 0.35
    return y


def ziper(seed=51, dur=0.45):
    """Caneta do telestrador riscando a linha: catraca rápida de cliques em ruído médio."""
    n = int(dur * SR); t = np.arange(n) / SR
    x = _passa_banda(np.random.default_rng(seed).standard_normal(n), 1500, 7000)
    catraca = (0.5 + 0.5 * np.sign(np.sin(2 * np.pi * (60 + 40 * t / dur) * t))) ** 2
    return x * catraca * np.sin(np.pi * t / dur) ** 0.6 * 0.7


def esfrega(seed=61, dur=0.7):
    """Mãos esfregando com força: ruído abafado modulado no vaivém."""
    n = int(dur * SR); t = np.arange(n) / SR
    x = _passa_banda(np.random.default_rng(seed).standard_normal(n), 300, 2500)
    vaivem = 0.35 + 0.65 * np.abs(np.sin(2 * np.pi * 5.4 * t))
    return x * vaivem * np.sin(np.pi * t / dur) ** 0.5 * 1.1


def puf(seed=81):
    """Volume crescendo: 'puf' grave e curto."""
    n = int(0.35 * SR); t = np.arange(n) / SR
    f = 90 + 70 * t / 0.35
    y = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.sin(np.pi * t / 0.35) ** 1.5
    return y * 0.7 + som._onepole_lp(np.random.default_rng(seed).standard_normal(n), 400) * np.sin(np.pi * t / 0.35) * 1.4


def queda(seed=91):
    """Queda abafada na grama (sem estalo de osso)."""
    n = int(0.4 * SR); t = np.arange(n) / SR
    x = som._onepole_lp(np.random.default_rng(seed).standard_normal(n), 300) * np.exp(-t * 14) * 3.0
    return x + np.sin(2 * np.pi * 70 * t) * np.exp(-t * 18) * 0.6


def passo_grama(seed=95):
    n = int(0.09 * SR); t = np.arange(n) / SR
    return som._onepole_lp(np.random.default_rng(seed).standard_normal(n), 900) * np.exp(-t * 40) * 1.6


def tec(seed=97):
    return som.tick(seed) * 0.9


SFX = dict(som.SFX)
SFX.update({"apito": apito, "apito_final": apito_final, "rebobinar": rebobinar, "bipe": bipe, "bipe_alto": bipe_alto,
            "obturador": obturador, "tv_desliga": tv_desliga, "ziper": ziper, "esfrega": esfrega, "puf": puf,
            "queda": queda, "passo": passo_grama, "tec": tec})


def _media_movel(x, w):
    n = len(x)
    c = np.concatenate([[0.0], np.cumsum(x)])
    i = np.arange(n)
    lo = np.clip(i - w // 2, 0, n); hi = np.clip(i + (w - 1) // 2 + 1, 0, n)
    return (c[hi] - c[lo]) / w


def mixar(voz, dur, eventos, ganho_trilha=0.40, baixas=()):
    """Cópia do som.mixar do piloto + `baixas`: janelas em que a trilha cai a ~15% (CHECANDO)."""
    n = int(dur * SR)
    v = np.zeros(n); v[:min(n, len(voz))] = voz[:n]
    musica = som.trilha(dur) * ganho_trilha
    win = int(0.06 * SR)
    envv = np.sqrt(np.maximum(_media_movel(v ** 2, win), 0.0))
    alvo = np.where(envv > 0.02, 0.38, 1.0)
    for t0, t1 in baixas:
        alvo[int(t0 * SR):int(t1 * SR)] = 0.15
    duck = _media_movel(alvo, int(0.25 * SR))
    fx = np.zeros(n)
    cache = {}
    for t0, nome, g in eventos:
        if nome not in cache:
            cache[nome] = SFX[nome]()
        s = cache[nome]
        p = int(t0 * SR)
        if 0 <= p < n:
            m = min(len(s), n - p)
            fx[p:p + m] += s[:m] * g
    mix = v * 1.0 + musica * duck + fx * 0.7
    pico = np.max(np.abs(mix)) or 1.0
    return mix / pico * 0.89


def sons(T):
    ev = [(0.0, "apito", 0.85), (T["chama"] + 0.02, "pop", 0.25), (T["var"] - 0.02, "rebobinar", 0.7),
          (T["torceu"] + 0.25, "passo", 0.5), (T["pe1"] + 0.02, "tec", 0.75), (T["corte1"] - 0.02, "whoosh", 0.35)]
    # os dois passos mancando (o 2º, no pé machucado, mais fraco)
    t1 = T["corte1"]; D = T["congela1"] - t1
    ev += [(t1 + 0.3 * D, "passo", 0.25), (t1 + 0.8 * D, "passo", 0.55)]
    for pd, vd, _, _ in VEREDITOS:
        ev.append((T[pd] - 0.01 if pd != "passa" else T["congela1"] - 0.01, "obturador", 0.85))
        t0 = T[pd + "_fim"] + 0.07
        ev += [(t0, "bipe", 0.75), (t0 + 0.2, "bipe", 0.75), (t0 + 0.4, "bipe_alto", 0.8)]
        ev.append((T[vd] - 0.02, "thump", 0.9))
    ev += [(T["validado"] - 0.24, "apito", 0.45)]
    # lance 1 — tira do jogo
    ev += [(T["dor"] + 0.1, "whoosh", 0.2), (T["tira"] - 0.02, "pop", 0.4), (T["tira"] + 0.05, "ziper", 0.55)]
    _, t0, tc = _l1_tempos(T)
    for i in range(4):
        ev.append((lerp(t0, tc, (i + 0.5) / 4), "passo", 0.4))
    ev += [(T["cruza"], "shimmer", 0.3), (T["testar"] + 0.05, "ping", 0.35)]
    # lance 2 — massagem
    ev += [(T["corte2"] - 0.03, "tick", 0.55), (T["corte2"] + 0.02, "whoosh", 0.4), (T["forte"] - 0.02, "esfrega", 0.55)]
    ev += [(T["logo"] - 0.34, "rebobinar", 0.35), (T["logo"] + 0.05, "esfrega", 0.35), (T["aumenta"] + 0.05, "puf", 0.6),
           (T["inchaco"] + 0.02, "tick", 0.6)]
    ev += [(T["gelo"] + 0.15, "tec", 0.7), (T["pano"] + 0.1, "shimmer", 0.25), (T["pe2"] - 0.2, "whoosh", 0.3),
           (T["cima"] + 0.1, "ping", 0.35)]
    # lance 3 — braço
    ev += [(T["corte3"] - 0.03, "tick", 0.55), (T["corte3"] + 0.12, "passo", 0.35), (T["corte3"] + 0.26, "passo", 0.35),
           (T["caiu"] + 0.45, "queda", 0.75), (T["torto1"] - 0.01, "obturador", 0.6), (T["torto1"] + 0.08, "ziper", 0.45),
           (T["imobilizar"] - 0.02, "whoosh", 0.3)]
    r0 = T["validado"] + DUR_CARIMBOS[2] - 0.1
    ev += [(r0 - 0.06, "rebobinar", 0.35), (T["puxa"], "whoosh", 0.25), (T["endireita"] + 0.2, "tick", 0.6),
           (T["certo3"] - 0.02, "whoosh", 0.42), (T["certo3"] + 0.32, "ziper", 0.35), (T["certo3"] + 0.65, "shimmer", 0.3),
           (T["certo3"] + 0.68, "ping", 0.3)]
    ev += [(T["sai3"] + 0.2 + 0.3 * i, "passo", 0.3) for i in range(4)]
    # apito final, TV desligando, apito passando, CTA
    ev += [(T["apito_f"], "apito_final", 0.6), (T["off"] + 0.02, "tv_desliga", 0.75)]
    ev += [(T["na"] + 0.05, "pop", 0.3), (T["apita"] + 0.1, "pop", 0.32), (T["medico"], "shimmer", 0.4),
           (T["manda"] + 0.05, "whoosh", 0.5)]
    return ev


def baixas_trilha(T):
    return [(T[pd + "_fim"] + 0.05, T[vd]) for pd, vd, _, _ in VEREDITOS]


def tempos_previa(T):
    return [0.0, T["var"] + 0.25, T["torceu"] + 0.2, T["pe1"] + 0.2, T["corte1"] + 0.3, T["congela1"] + 0.1,
            T["passa_fim"] + 0.4, T["anulado1"] + 0.3, T["parar"] + 0.1, T["tira"] + 0.3, T["jogo"] + 0.2,
            T["cruza"] + 0.2, T["testar"] + 0.2,
            T["corte2"] + 0.3, T["forte"] + 0.2, T["pode1"] + 0.5, T["anulado2"] + 0.3, T["aumenta"] + 0.3,
            T["inchaco"] + 0.3, T["inchaco"] + 0.6, T["gelo"] + 0.3, T["pano"] + 0.3, T["cima"] + 0.3,
            T["corte3"] + 0.2, T["caiu"] + 0.25, T["caiu"] + 0.5, T["torto1"] + 0.4, T["esta"] + 0.2, T["pode2"] + 0.5,
            T["validado"] + 0.4, T["puxa"] + 0.1, T["endireita"] + 0.35, T["certo3"] + 0.2, T["certo3"] + 0.6,
            T["certo3"] + 1.2,
            T["sai3"] + 0.4, T["off"] + 0.1, T["na"] + 0.3, T["apita"] + 0.3, T["medico"] + 0.3,
            T["manda"] + 0.5, T["manda"] + 1.6]


# ================================================================== render (cópia do piloto + pausas)
VAO_CHECANDO = 0.80
VAOS_EXTRA = (("massagem", 1, 0.50),  # (revisão) o visto do pé no ar respira antes do LANCE 2
              ("caiu", 1, 0.65),      # o visto do pé elevado respira; a 2ª criança já entra correndo (era 0,45)
              ("e", 3, 1.85),         # (revisão) o X da mão que puxa + o jeito certo do braço, sem fala (era 0,95)
              ("na", 1, 1.05))        # apito final + TV desligando
PRE_APITO = 0.25


def pausa_checando(audio, pal, vao=VAO_CHECANDO):
    """Insere silêncio depois de cada pergunta ('?') até o vão chegar a `vao` (cópia adaptada do piloto)."""
    ins = []
    for i in range(len(pal) - 1):
        if pal[i]["tok"].endswith("?"):
            fim = pal[i]["t"] + pal[i]["d"]; gap = pal[i + 1]["t"] - fim
            if gap < vao:
                ins.append((fim + 0.04, vao - gap))
    if len(ins) != 3:
        raise KeyError(f"esperava 3 perguntas com '?' no roteiro, achei {len(ins)}")
    partes, ult = [], 0
    for t0, extra in ins:
        p = int(t0 * SR); partes += [audio[ult:p], np.zeros(int(extra * SR), dtype=audio.dtype)]; ult = p
    partes.append(audio[ult:])
    novo = np.concatenate(partes)

    def remap(t):
        return t + sum(extra for t0, extra in ins if t > t0)
    return novo, [dict(p, t=remap(p["t"])) for p in pal], ins


def garantir_vao(audio, pal, palavra, n, vao):
    c = 0
    for i, p in enumerate(pal):
        if p["w"].lower() == palavra:
            c += 1
            if c == n:
                break
    else:
        raise KeyError(f"palavra não achada para a pausa: {palavra} #{n}")
    fim = pal[i - 1]["t"] + pal[i - 1]["d"]; gap = p["t"] - fim
    if gap >= vao:
        return audio, pal
    t0 = fim + 0.04; extra = vao - gap; k = int(t0 * SR)
    audio = np.concatenate([audio[:k], np.zeros(int(extra * SR), dtype=audio.dtype), audio[k:]])
    return audio, [dict(q, t=q["t"] + (extra if q["t"] > t0 else 0.0)) for q in pal]


def montar_T(pal, mapa):
    T = {}
    for chave, (palavra, n, prefixo) in mapa.items():
        c = 0
        for p in pal:
            w = p["w"].lower()
            if w == palavra or (prefixo and w.startswith(palavra)):
                c += 1
                if c == n:
                    T[chave] = p["t"]
                    if chave in FIM_DE:
                        T[chave + "_fim"] = p["t"] + p["d"]
                    break
        else:
            raise KeyError(f"palavra-âncora não achada no roteiro: {palavra} #{n}")
    # "nem" (só para o X do replay): a palavra depois de "puxa"
    i = next(i for i, p in enumerate(pal) if p["w"].lower() == "puxa")
    T["nem"] = pal[i + 1]["t"]
    T["fim_fala"] = pal[-1]["t"] + pal[-1]["d"]
    T["total"] = T["fim_fala"] + 2.2
    T["corte1"] = T["corre"] - 0.08                      # close de frente -> plano aberto de lado
    T["congela1"] = T["passa_fim"] - 0.05                # congela no fim de "passa?"
    t0, t_vira, t_cheg = _l1_tempos(T)                   # quando a criança cruza a linha lateral
    alvo = (L1_X_INI - X_LINHA) / (L1_X_INI - L1_X_FIM)
    lo, hi = 0.0, 1.0
    for _ in range(30):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if e_inout(mid) < alvo else (lo, mid)
    T["cruza"] = lerp(t_vira, t_cheg, lo)
    T["corte2"] = T["massagem"] - 0.06
    T["corte3"] = T["caiu"] - 0.36
    T["certo3"] = T["endireita_fim"] + 0.45              # cortina: o jeito certo do braço (depois do X e da soltura)
    T["sai3"] = T["pronto"] - 0.15                       # sai andando para o pronto-socorro
    T["apito_f"] = T["na"] - 1.0
    T["off"] = T["na"] - 0.48
    return T


def calcular_T(ep, tmp, respiro_cta=0.8):
    roteiro = "\n".join(ep["roteiro"])
    voz_bruta, palavras = _voz.narrar(roteiro, _voz.RITMO_COMO_FUNCIONA, os.path.join(tmp, "voz"))
    voz_c, pal, tirado = comprimir(voz_bruta, palavras, respiro_cta=respiro_cta)
    pal = alinhar(pal, roteiro)
    voz_c, pal, ins = pausa_checando(voz_c, pal)
    for palavra, n, vao in VAOS_EXTRA:
        voz_c, pal = garantir_vao(voz_c, pal, palavra, n, vao)
    voz_c = np.concatenate([np.zeros(int(PRE_APITO * SR), dtype=voz_c.dtype), voz_c])
    pal = [dict(p, t=p["t"] + PRE_APITO) for p in pal]
    T = montar_T(pal, ANCORAS)
    return voz_c, pal, T, tirado, ins


def montar_blocos_var(pal):
    """Cópia do montar_blocos (cf_fratura_cola) com duas mudanças da revisão:
    1. a pergunta curta fica no MESMO bloco do que ela pergunta ('MASSAGEM FORTE PRA DESINCHAR: PODE?'); antes o
       'PODE?' saía sozinho, e lida só a legenda a frase de cima parecia recomendar a massagem;
    2. o corte de um bloco longo aceita a vírgula até 2 palavras do meio ('NA DÚVIDA,' / 'QUEM APITA É O MÉDICO.') e
       não deixa o bloco terminar em conjunção ou artigo."""
    frases, atual = [], []
    for p in pal:
        atual.append(p)
        if p["fim_frase"]:
            frases.append(atual); atual = []
    if atual:
        frases.append(atual)
    juntas = []
    for fr in frases:
        ant = juntas[-1] if juntas else None
        if ant and len(ant) > 1 and ant[-1]["tok"].endswith(":") and fr[-1]["tok"].endswith("?") and len(ant) + len(fr) <= 6:
            juntas[-1] = ant + fr
        else:
            juntas.append(fr)
    blocos = []
    for fr in juntas:
        if len(fr) <= 6 or fr[0]["w"].lower() == "manda":
            blocos.append(fr); continue
        n = math.ceil(len(fr) / 5); alvo = len(fr) / n; ini = 0
        for k in range(1, n):
            corte = round(alvo * k)
            virgs = sorted((i + 1 for i in range(ini, len(fr) - 1) if fr[i]["virg"] and abs(i + 1 - corte) <= 2),
                           key=lambda c: abs(c - corte))
            corte = virgs[0] if virgs else corte
            if not virgs and fr[corte - 1]["tok"].lower() in ("e", "o", "a", "de", "da", "do", "pra", "que") and corte - 1 > ini:
                corte -= 1                       # bloco não termina em conjunção/artigo ('GELO COM PANO' / 'E PÉ PRA CIMA.')
            blocos.append(fr[ini:corte]); ini = corte
        blocos.append(fr[ini:])
    return blocos


def fazer_render_var(quadro_fn, sons_fn, tempos_fn, respiro_cta=0.8):
    def render(ep, mp4, tmp, previa=False):
        voz_c, pal, T, tirado, ins = calcular_T(ep, tmp, respiro_cta)
        print(f"{ep['id']}: silêncio cortado {tirado:.2f}s | CHECANDO {[round(x[1], 2) for x in ins]} | "
              f"duração final {T['total']:.2f}s")
        blocos = montar_blocos_var(pal)

        def quadro_t(cv, t):
            quadro_fn(cv, t, T, blocos, ep)

        if previa:
            return _previas(quadro_t, tempos_fn(T), tmp, ep["id"]), T["total"]
        wav = os.path.join(tmp, f"{ep['id']}_mix.wav")
        som.gravar_wav(wav, mixar(voz_c, T["total"], sons_fn(T), baixas=baixas_trilha(T)))
        codificar(quadro_t, T["total"], wav, mp4)
        return mp4, T["total"]
    return render


render = fazer_render_var(quadro, sons, tempos_previa, respiro_cta=0.8)
