# -*- coding: utf-8 -*-
"""CHAMA O VAR — "COCEIRA NO GESSO? / SECADOR PODE?" (criança engessada em casa: pode ou não pode?).

Série "Chama o VAR" (ter/qui/sáb), 2º episódio, construído sobre o piloto cf_chamaovar_rotina_fixador:
os helpers do piloto (monitor, selo VAR + chip de estado, telestrador, carimbo, rebobinar, TV desligando,
equipe, apito, sons, legenda karaokê, render com CHECANDO) estão COPIADOS aqui, sem importar o piloto.
Contrato de cena do cf_comum (ANCORAS, DESTAQUE, quadro, sons, tempos_previa, render no nível de cima).

Lances (fontes conferidas na peça certa: lab/formato_novo/cf_var_gesso/storyboard.json):
  1. secador para a coceira -> VALIDADO, SÓ com ar frio (s_pnc_gesso_em_casa: "Ar frio de secador (nunca
     quente) alivia a coceira."; cv_gesso_filho);
  2. régua para coçar -> ANULADO + replay do jeito certo (o secador no frio), sem fala (cv_gesso_filho;
     s_pnc_gesso_em_casa; qa_gesso_molhar);
  3. gesso no chuveiro -> ANULADO; o porquê é MOSTRADO (o gesso escurece e amolece) e o jeito certo resolve:
     capa impermeável, a água escorre e o gesso fica seco (s_pnc_gesso_em_casa; cv_gesso_filho).

O que a cena mostra (a palavra falada comanda o quadro — ANCORAS):
  * quadro 0: o lance 1 JÁ CONGELADO: antebraço de CRIANÇA engessado (dedinhos de fora, polegar livre) numa
    almofada do sofá, a mão adulta segurando um SECADOR apontado para a ABERTURA do gesso, círculo de
    telestrador no bico + abertura, risquinhos de coceira, ícone de pausa; o gancho é o único texto;
  * "VAR": rebobina 0,5 s (o secador sai) e a câmera abre; "Coceira": os dedinhos tamborilam e os
    risquinhos pipocam; "gesso": um brilho corre o gesso; "Secador": o secador volta, desligado; "pode?":
    congela; "Validado": carimbo VALIDADO / SÓ AR FRIO; "ar": o botão desliza para o FLOCO DE NEVE; "frio":
    sai ar AZUL pela abertura; "alivia": os risquinhos somem e os dedos param; "coceira": contorno verde no
    secador (JEITO CERTO); "Quente": o botão pula para a CHAMINHA e o ar fica LARANJA (nada na pele);
    "nunca": X âmbar no ar laranja, o ar corta e o botão volta para o floco;
  * "E a régua": o secador sai; a OUTRA mãozinha da criança entra com uma régua (sem números) e a enfia pela
    abertura ("coçar"; nada do lado de dentro é mostrado); "pode?": congela; "Anulado": carimbo; "arranhão":
    a régua sai e cai fora do quadro; "dentro": círculo âmbar SÓ na abertura; "infeccionar": pulsa e apaga;
    cortina do VAR: o jeito certo volta (secador no frio, ar azul, chip JEITO CERTO);
  * "Gesso no chuveiro" (corte, LANCE 3): banheiro de azulejos, SÓ o antebraço engessado (nenhum corpo, nunca
    criança sem roupa), a ducha abre e as gotas caem no gesso; "pode?": congela com as gotas no ar;
    "Anulado": carimbo; "molhado": manchas cinza-bege; "perde": o contorno amolece e afunda (seta âmbar);
    "machuca": círculo âmbar na borda de cima, onde o gesso encosta na pele (nada desenhado na pele);
    rebobina (gesso seco, ducha fecha); "Capa": UMA mão adulta (de cima, inclinada) puxa o elástico e veste
    a capa plástica transparente, que tem um calombo e ENVOLVE o polegar; "impermeável": a ducha abre, a
    água ESCORRE pela capa e o gesso fica branco; visto verde;
  * apito final e a TV desliga; "No seu caso": a equipe acende; "apita": o apito passa para a equipe;
    "equipe": selo CHAMA O VAR; CTA.
Revisão 2 (leitor às cegas + revisor): estrelas e coração de canetinha no gesso e dedinhos curtos (lê-se
CRIANÇA); ficha grande de floco/chaminha ao lado do jato (quente x frio), com o X do "nunca" no canto
dela; braço da régua curto, com a manga lilás dentro do quadro; legenda com blocos de até 2 linhas, sem
palavra de ligação no fim do bloco/linha (montar_blocos_var, partir_linhas) e apagada no replay sem fala.
Guardrails: pele OPACA de desenho, nenhum osso, nenhum exame, nenhum fundo preto, nenhum rosto, nenhum
sangue; nada desenhado dentro do gesso, nenhuma pele arranhada, vermelha ou queimada, nenhum dedo roxo;
âmbar só em setas, círculos, X e carimbo (vermelho não aparece); ciano = só grafismo do VAR; dourado = só a
legenda. Todo texto desenhado está em ep["tela"]. Cena PRESA ao roteiro pelas palavras-âncora.
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
from .cf_fratura_cola import alinhar, comprimir, montar_blocos

# ------------------------------------------------------------------ sincronia com a fala
ANCORAS = {
    # lance 1 — secador para a coceira
    "chama": ("chama", 1, False), "var": ("var", 1, False), "coceira1": ("coceira", 1, False),
    "gesso1": ("gesso", 1, False), "secador": ("secador", 1, False), "pode1": ("pode", 1, False),
    "validado": ("validado", 1, False), "ar": ("ar", 1, False), "frio": ("frio", 1, False),
    "alivia": ("alivia", 1, False), "coceira2": ("coceira", 2, False), "quente": ("quente", 1, False),
    "nunca": ("nunca", 1, False),
    # lance 2 — régua para coçar
    "e1": ("e", 1, False), "regua": ("régua", 1, False), "cocar": ("coçar", 1, False), "pode2": ("pode", 2, False),
    "anulado1": ("anulado", 1, False), "arranhao": ("arranhão", 1, False), "dentro": ("dentro", 1, False),
    "infeccionar": ("infeccionar", 1, False),
    # lance 3 — gesso no chuveiro ('pode' #3 é o de "pode infeccionar", que não é pergunta)
    "gesso2": ("gesso", 2, False), "chuveiro": ("chuveiro", 1, False), "pode3": ("pode", 4, False),
    "anulado2": ("anulado", 2, False), "molhado": ("molhado", 1, False), "perde": ("perde", 1, False),
    "funcao": ("função", 1, False), "machuca": ("machuca", 1, False), "pele": ("pele", 1, False),
    "capa": ("capa", 1, False), "impermeavel": ("impermeável", 1, False),
    # fim
    "no": ("no", 3, False), "caso": ("caso", 1, False), "quem": ("quem", 1, False), "apita": ("apita", 1, False),
    "equipe": ("equipe", 1, False), "manda": ("manda", 1, False),
}
FIM_DE = ("pode1", "pode2", "pode3", "nunca", "infeccionar", "pele", "impermeavel", "equipe", "capa", "coceira2")
DESTAQUE = {"var", "secador", "frio", "nunca", "régua", "infeccionar", "chuveiro", "função", "capa", "apita",
            "equipe"}

# rótulos (todos estão em ep["tela"])
T_VAR = "VAR"
T_LANCE = ("LANCE 1", "LANCE 2", "LANCE 3")
T_CHEC = "CHECANDO"
T_ANUL = "ANULADO"
T_VALID = "VALIDADO"
T_FRIO = "SÓ AR FRIO"
T_CERTO = "JEITO CERTO"
T_SERIE = "CHAMA O VAR"

# ------------------------------------------------------------------ paleta (identidade da série, do piloto)
ARD_IN, ARD_OUT = "#22303F", "#121A24"
CIANO = "#4FD1FF"
VERDE = "#3DDC84"
AMBAR = "#FFA53A"
CARTAO = "#0B1824"
SELO_BG = "#1E2A44"
TEAL = "#5FC4B6"
PELE, PELE_CL, PELE_ESC, PELE_LINHA = "#F0B49A", "#F7CDB8", "#D9937A", "#B9765E"     # criança
AD, AD_CL, AD_ESC, AD_LINHA = "#C98D6E", "#DDA98C", "#A56C50", "#7C4C37"             # adulto (outro tom)
MANGA_AD, MANGA_AD_CL, MANGA_AD_ESC = "#5FC4B6", "#84D6CB", "#3E9C90"                # manga teal do adulto
CAMISETA, CAMISETA_CL, CAMISETA_ESC = "#9B7ED0", "#B9A2E4", "#7558AC"                # camiseta lilás da criança
PAREDE_A, PAREDE_B = "#E2E8EE", "#C8D2DC"
SOFA, SOFA_CL, SOFA_ESC = "#3F516B", "#566B88", "#2C3A4E"
ALMOF, ALMOF_CL, ALMOF_ESC = "#7EA6CF", "#A3C2E2", "#5A80A8"
GESSO_C = ("#AEB9C4", "#F1F4F7", "#FFFFFF", "#E9EEF2", "#C3CDD6")
MALHA, MALHA_ESC = "#FBF7EE", "#D9D2C4"
INTERIOR = "#3E352E"
MOLHADO, MOLHADO_ESC = "#D2CBBC", "#BDB4A2"
AR_FRIO, AR_QUENTE = "#9FD8FF", "#FF9A4A"
SEC, SEC_CL, SEC_ESC, SEC_BICO = "#9AA9BC", "#C3CEDB", "#6E7E93", "#56667A"
REGUA, REGUA_CL, REGUA_ESC = "#E8C98E", "#F4DDB0", "#B8955A"
AZULEJO, REJUNTE = "#E6EEF2", "#C9D6DD"
GOTA, GOTA_ESC = "#9ED6F5", "#3B6E8F"
CAPA_C, CAPA_BORDA, CAPA_ELAST = "#BFE6FF", "#6FAFD6", "#8FC9EE"

TONS_PELE = (PELE_ESC, PELE, PELE_CL, PELE, PELE_ESC)
TONS_AD = (AD_ESC, AD, AD_CL, AD, AD_ESC)
TONS_MANGA_AD = (MANGA_AD_ESC, MANGA_AD, MANGA_AD_CL, MANGA_AD, MANGA_AD_ESC)
TONS_CAMISETA = (CAMISETA_ESC, CAMISETA, CAMISETA_CL, CAMISETA, CAMISETA_ESC)

# ------------------------------------------------------------------ o monitor (janela da cena) — igual ao piloto
JX0, JY0, JX1, JY1 = 28.0, 300.0, 1052.0, 1226.0
JCX, JCY = (JX0 + JX1) / 2, (JY0 + JY1) / 2
JAN = skia.Rect(JX0, JY0, JX1, JY1)
JAN_R = 26


# ------------------------------------------------------------------ utilidades (cópias do piloto)
def _c(h, a=255):
    h = h.lstrip("#")
    return skia.ColorSetARGB(int(a), int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))


def esc_cor(h, k):
    return lerpc(h, "#000000", k)


def janela(t, t0, t1, d_in=0.25, d_out=0.3):
    return prog(t, t0, t0 + d_in) * (1 - prog(t, t1, t1 + d_out))


def uniao(*ps):
    out = ps[0]
    for q in ps[1:]:
        out = skia.Op(out, q, skia.PathOp.kUnion_PathOp) or out
    return out


def rr_path(x0, y0, x1, y1, r):
    p = skia.Path(); p.addRRect(skia.RRect.MakeRectXY(skia.Rect(x0, y0, x1, y1), r, r)); return p


def oval_path(x0, y0, x1, y1):
    p = skia.Path(); p.addOval(skia.Rect(x0, y0, x1, y1)); return p


def poli(pts, fechar=True):
    p = skia.Path(); p.moveTo(*pts[0])
    for q in pts[1:]:
        p.lineTo(*q)
    if fechar:
        p.close()
    return p


def suave(pts, fechar=True):
    """Contorno suave passando pelo meio dos segmentos (quadráticas)."""
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
    """Tubo afinando de p0 (largura w0) a p1 (w1), pontas redondas."""
    dx, dy = p1[0] - p0[0], p1[1] - p0[1]; L = math.hypot(dx, dy) or 1.0
    nx, ny = -dy / L, dx / L
    p = poli([(p0[0] + nx * w0 / 2, p0[1] + ny * w0 / 2), (p1[0] + nx * w1 / 2, p1[1] + ny * w1 / 2),
              (p1[0] - nx * w1 / 2, p1[1] - ny * w1 / 2), (p0[0] - nx * w0 / 2, p0[1] - ny * w0 / 2)])
    c0 = skia.Path(); c0.addCircle(p0[0], p0[1], w0 / 2)
    c1 = skia.Path(); c1.addCircle(p1[0], p1[1], w1 / 2)
    return uniao(p, c0, c1)


def pinta(cv, path, p0, p1, w, tons, a, linha=None, larg_linha=2.5):
    """Preenche com sombreado cilíndrico perpendicular ao eixo p0->p1 (pele/roupa chapada e opaca)."""
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
    """Seta reta com contorno escuro (lê sobre parede clara). (cópia do piloto)"""
    if a <= 0 or math.hypot(x1 - x0, y1 - y0) < 2:
        return
    ang = math.atan2(y1 - y0, x1 - x0)
    xb, yb = x1 - tam * 0.55 * math.cos(ang), y1 - tam * 0.55 * math.sin(ang)
    cv.drawLine(x0, y0, xb, yb, paint(CARTAO, int(170 * a), "stroke", larg + 8))
    ponta(cv, x1 + 4 * math.cos(ang), y1 + 4 * math.sin(ang), ang, tam + 10, CARTAO, 0.7 * a)
    cv.drawLine(x0, y0, xb, yb, paint(cor, int(255 * a), "stroke", larg))
    ponta(cv, x1, y1, ang, tam, cor, a)


def _trim(pt, k):
    """Traço desenhado até a fração k (TrimPathEffect devolve None em k = 0). (cópia do piloto)"""
    if k < 0.999:
        pe = skia.TrimPathEffect.Make(0.0, max(0.002, k))
        if pe is not None:
            pt.setPathEffect(pe)
    return pt


def lerp2(p, q, k):
    return (lerp(p[0], q[0], k), lerp(p[1], q[1], k))


def lerp3(p, q, k):
    return tuple(lerp(p[i], q[i], k) for i in range(len(p)))


_CACHE = {}
LINEAR = skia.SamplingOptions(skia.FilterMode.kLinear)


def cacheado(chave, w, h, desenha):
    """Camada estática desenhada uma vez só (o raster do skia aqui é lento para degradês e desfoques)."""
    if chave not in _CACHE:
        sf = skia.Surface(int(w), int(h)); c = sf.getCanvas(); c.clear(skia.ColorTRANSPARENT)
        desenha(c)
        _CACHE[chave] = sf.makeImageSnapshot()
    return _CACHE[chave]


# ------------------------------------------------------------------ câmera
def aplica(cv, cam):
    """cam = (escala, foco x, foco y, espelho): espelho -1 = a sala é vista espelhada (o secador entra pela
    direita e não passa por baixo do selo VAR, que fica no canto de cima à esquerda)."""
    s, fx, fy = cam[:3]; m = cam[3] if len(cam) > 3 else 1.0
    cv.translate(JCX, JCY); cv.scale(s * m, s); cv.translate(-fx, -fy)


def na_tela(cam, x, y):
    s, fx, fy = cam[:3]; m = cam[3] if len(cam) > 3 else 1.0
    return JCX + m * (x - fx) * s, JCY + (y - fy) * s


# ================================================================== O BRAÇO ENGESSADO (referencial do braço)
# u = ao longo do antebraço (cotovelo = 0, para a mão = +); v = perpendicular (+ = para baixo)
U_ARO, U_PUNHO, U_ARO2 = 112.0, 405.0, 530.0     # borda de cima do gesso, punho, borda na base dos dedos
R_ARO, R_PUNHO, R_ARO2 = 78.0, 62.0, 58.0
RX_ARO = 30.0                                    # a abertura vista de 3/4 (elipse)
R_PELE = 49.0
V_PELE = 13.0                                    # a pele entra mais baixa: sobra a meia-lua escura em cima
U_POLEGAR = 500.0
GAP = (U_ARO - 9.0, -R_ARO + 19.0)               # a abertura (a meia-lua escura entre a malha e a pele)

ARM_SALA = dict(E=(215.0, 905.0), ang=-4.0, banho=False)
ARM_BANHO = dict(E=(40.0, 880.0), ang=0.0, banho=True)


def l2w(arm, u, v):
    ex, ey = arm["E"]; a = math.radians(arm["ang"])
    return (ex + u * math.cos(a) - v * math.sin(a), ey + u * math.sin(a) + v * math.cos(a))


def w2l(arm, x, y):
    ex, ey = arm["E"]; a = math.radians(arm["ang"])
    dx, dy = x - ex, y - ey
    return (dx * math.cos(a) + dy * math.sin(a), -dx * math.sin(a) + dy * math.cos(a))


def r_gesso(u):
    if u <= U_PUNHO:
        return lerp(R_ARO, R_PUNHO, e_inout(clamp((u - U_ARO) / (U_PUNHO - U_ARO))))
    k = clamp((u - U_PUNHO) / (U_ARO2 - U_PUNHO))
    return lerp(R_PUNHO, R_ARO2, k) + 4 * math.sin(math.pi * k)


U_AFUNDA = 320.0


def _afund(u):
    return math.exp(-((u - U_AFUNDA) / 92.0) ** 2)


def topo_v(u, afunda=0.0):
    """v do alto do gesso em u (com o amolecimento: o meio afunda e ondula)."""
    b = _afund(u)
    return -r_gesso(u) + afunda * (30 * b + 4 * math.sin(u * 0.11) * b)


def gesso_path(afunda=0.0, n=44):
    top, bot = [], []
    for i in range(n + 1):
        u = lerp(U_ARO, U_ARO2, i / n)
        b = _afund(u)
        top.append((u, topo_v(u, afunda)))
        bot.append((u, r_gesso(u) + afunda * (9 * b + 3 * math.sin(u * 0.13 + 1) * b)))
    p = skia.Path()
    p.moveTo(*top[0])
    for q in top[1:]:
        p.lineTo(*q)
    rr = r_gesso(U_ARO2)
    p.arcTo(skia.Rect(U_ARO2 - 15, -rr, U_ARO2 + 15, rr), -90, 180, False)
    for q in reversed(bot):
        p.lineTo(*q)
    p.arcTo(skia.Rect(U_ARO - RX_ARO, -R_ARO, U_ARO + RX_ARO, R_ARO), 90, 180, False)
    p.close()
    return p


ABERTURA = oval_path(U_ARO - RX_ARO, -R_ARO, U_ARO + RX_ARO, R_ARO)


def dedos(cv, amp, ts, a=1.0):
    """Os quatro dedinhos saindo da ponta do gesso, de lado (indicador em cima, mais perto). `amp` faz
    os dedos tamborilarem (coceira). Curtos e gordinhos: mão de CRIANÇA (o leitor às cegas leu adulto)."""
    defs = ((25, 44, 27, 0.0), (8, 54, 30, 1.3), (-10, 60, 31, 2.6), (-28, 57, 31, 3.9))   # (v, comp, larg, fase)
    for k, (v, comp, lg, fase) in enumerate(defs):
        esc = 0.05 * (3 - k)                                        # os de trás um pouco mais escuros
        tons = tuple(esc_cor(c, esc) for c in TONS_PELE)
        sobe = amp * (0.5 + 0.5 * math.sin(ts * 15 + fase)) * 14
        b = (U_ARO2 - 8, v)
        p1 = (U_ARO2 + comp * 0.6, v - 1 - sobe * 0.6)
        p2 = (U_ARO2 + comp, v + 9 - sobe)
        dp = uniao(capsula(b, p1, lg, lg * 0.97), capsula(p1, p2, lg * 0.97, lg * 0.88))
        pinta(cv, dp, b, p2, lg, tons, a, linha=PELE_LINHA, larg_linha=2.0)
        cv.drawOval(skia.Rect(p2[0] - 9, p2[1] - lg * 0.36, p2[0] + 3, p2[1] - lg * 0.06), paint(PELE_CL, int(210 * a)))


POL_DU, POL_DV, POL_W0, POL_W1 = 36.0, -36.0, 36.0, 33.0     # polegar curto e gordinho (criança)


def polegar(cv, r_top, a=1.0):
    """Polegar livre saindo por cima do gesso (com a malha dobrada em volta)."""
    u = U_POLEGAR
    b = (u, r_top + 10); q = (u + POL_DU, r_top + 10 + POL_DV)
    pth = capsula(b, q, POL_W0, POL_W1)
    pinta(cv, pth, b, q, POL_W0, TONS_PELE, a, linha=PELE_LINHA, larg_linha=2.2)
    cv.drawOval(skia.Rect(q[0] - 8, q[1] - 12, q[0] + 8, q[1] - 2), paint(PELE_CL, int(210 * a)))
    cv.drawOval(skia.Rect(u - 26, r_top - 7, u + 26, r_top + 11), paint(MALHA, int(255 * a)))
    cv.drawOval(skia.Rect(u - 26, r_top - 7, u + 26, r_top + 11), paint(MALHA_ESC, int(220 * a), "stroke", 2.2))
    pinta(cv, capsula((u - 2, r_top + 4), (u + 10, r_top - 10), 34, 33), (u - 2, r_top + 4), (u + 10, r_top - 10), 34,
          TONS_PELE, a)


RABISCO_ROXO, RABISCO_ROSA, RABISCO_AZUL = "#8E5CD9", "#E86AA6", "#4A7FD8"


def _estrela(r, n=5, k=0.46):
    pts = []
    for i in range(2 * n):
        ang = -math.pi / 2 + i * math.pi / n
        rr = r if i % 2 == 0 else r * k
        pts.append((rr * math.cos(ang), rr * math.sin(ang)))
    return poli(pts)


def _coracao(r):
    p = skia.Path()
    p.moveTo(0, r * 0.9)
    p.cubicTo(-r * 1.25, r * 0.05, -r * 0.85, -r * 0.95, 0, -r * 0.38)
    p.cubicTo(r * 0.85, -r * 0.95, r * 1.25, r * 0.05, 0, r * 0.9)
    p.close()
    return p


def rabiscos(cv, a=1.0):
    """Desenhos de canetinha no gesso (estrelas e coração): o gesso é de CRIANÇA. Só na superfície de fora,
    sem letra nem rosto, cores fora das reservadas (âmbar/ciano/verde/dourado). Referencial do braço."""
    for (u, v, r, rot, cor, forma) in ((222, -24, 25, -12, RABISCO_ROXO, "e"), (306, 16, 22, 0, RABISCO_ROSA, "c"),
                                       (392, -20, 20, 14, RABISCO_AZUL, "e"), (458, 20, 13, -8, RABISCO_ROXO, "e")):
        pth = _estrela(r) if forma == "e" else _coracao(r)
        cv.save(); cv.translate(u, v); cv.rotate(rot)
        cv.drawPath(pth, paint(cor, int(70 * a)))
        pt = paint(cor, int(235 * a), "stroke", 4.2); pt.setStrokeJoin(skia.Paint.kRound_Join)
        cv.drawPath(pth, pt)
        cv.restore()


def coceira_risco(cv, x, y, k, a):
    """Risquinho de coça-coça (zigue-zague claro com contorno), pipocando."""
    if a <= 0 or k <= 0:
        return
    s = clamp(k, 0, 1.2)
    cv.save(); cv.translate(x, y); cv.scale(s, s)
    pts = [(-24, 6), (-12, -8), (0, 6), (12, -8), (24, 6)]
    p = poli(pts, fechar=False)
    pt = paint(CARTAO, int(170 * a), "stroke", 12); pt.setStrokeJoin(skia.Paint.kRound_Join); cv.drawPath(p, pt)
    pt = paint("#FFE08A", int(255 * a), "stroke", 6); pt.setStrokeJoin(skia.Paint.kRound_Join); cv.drawPath(p, pt)
    cv.restore()


def braco(cv, arm, e, t):
    """O antebraço da criança com o gesso, no referencial do braço. `e`: estado do quadro."""
    banho = arm["banho"]
    af = e.get("afunda", 0.0)
    cv.save(); cv.translate(*arm["E"]); cv.rotate(arm["ang"])
    # sombra no apoio
    if not banho:
        cv.drawOval(skia.Rect(-70, 30, U_ARO2 + 110, 104), paint("#000000", 55, blur=16))
    # dedinhos (a base fica escondida pela ponta do gesso)
    dedos(cv, e.get("tamb", 0.0), e.get("ts", t))
    # o gesso
    gp = gesso_path(af)
    cv.drawPath(gp, paint("#000000", 50, blur=10))
    wet = e.get("molhado", 0.0)
    tons = [lerpc(c, MOLHADO, 0.35 * wet) for c in GESSO_C]
    rmax = R_ARO + 10
    sh = skia.GradientShader.MakeLinear([skia.Point(0, -rmax), skia.Point(0, rmax)], [_c(c) for c in tons][::-1],
                                        [0.0, 0.22, 0.42, 0.7, 1.0])
    cv.drawPath(gp, paint("#FFFFFF", shader=sh))
    cv.save(); cv.clipPath(gp, skia.ClipOp.kIntersect, True)
    for k in range(15):                                    # as voltas da atadura
        u0 = U_ARO + 18 + k * 31
        cv.drawLine(u0 + 12, -rmax, u0 - 12, rmax, paint("#C2CCD6", 190, "stroke", 2.6))
        cv.drawLine(u0 + 16, -rmax, u0 - 8, rmax, paint("#FFFFFF", 150, "stroke", 2))
    rabiscos(cv)
    if wet > 0:                                          # manchas de gesso molhado (só a superfície)
        for (u, v, rx, ry, s) in ((240, -36, 64, 30, 0.0), (322, -12, 60, 40, 0.15), (405, -30, 58, 28, 0.3),
                                  (290, 26, 46, 24, 0.45), (448, 4, 40, 26, 0.6)):
            k = clamp((wet - s * 0.5) / 0.5)
            if k <= 0:
                continue
            cv.drawOval(skia.Rect(u - rx * k, v - ry * k, u + rx * k, v + ry * k), paint(MOLHADO, int(200 * k), blur=9))
            cv.drawOval(skia.Rect(u - rx * k * 0.7, v - ry * k * 0.6, u + rx * k * 0.5, v + ry * k * 0.6),
                        paint(MOLHADO_ESC, int(90 * k), blur=8))
    if 0 < e.get("brilho", -1) < 1:                        # brilho correndo pelo gesso (dá nome ao objeto)
        x = lerp(U_ARO - 40, U_ARO2 + 40, e["brilho"])
        g = skia.GradientShader.MakeLinear([skia.Point(x - 70, 0), skia.Point(x + 70, 0)],
                                           [_c("#FFFFFF", 0), _c("#FFFFFF", 230), _c("#FFFFFF", 0)])
        cv.drawRect(skia.Rect(x - 70, -rmax, x + 70, rmax), paint("#FFFFFF", shader=g))
    cv.restore()
    cv.drawPath(gp, paint("#8E9BA8", 255, "stroke", 2.5))
    # malha dobrada na ponta dos dedos
    rr = r_gesso(U_ARO2)
    cv.drawArc(skia.Rect(U_ARO2 - 15, -rr, U_ARO2 + 15, rr), -90, 180, False, paint(MALHA, 255, "stroke", 11))
    cv.drawArc(skia.Rect(U_ARO2 - 15, -rr, U_ARO2 + 15, rr), -80, 160, False, paint(MALHA_ESC, 200, "stroke", 2))
    # a abertura de cima: o fundo escuro, a metade de trás da malha
    cv.drawPath(ABERTURA, paint(INTERIOR))
    cv.drawArc(skia.Rect(U_ARO - RX_ARO, -R_ARO, U_ARO + RX_ARO, R_ARO), -90, 180, False, paint(MALHA_ESC, 255, "stroke", 8))
    # a pele (braço + antebraço num contorno só) entrando pela abertura
    cv.save()
    clip = uniao(rr_path(-900, -900, U_ARO, 900, 0), ABERTURA)
    cv.clipPath(clip, skia.ClipOp.kIntersect, True)
    ante = capsula((-20 if not banho else -700, 4), (U_ARO + 30, V_PELE), 2 * R_PELE + 6, 2 * R_PELE)
    if not banho:
        d = (-0.62, 0.785)                                 # o braço desce para a esquerda (a criança reclinada)
        ombro = (d[0] * 470, d[1] * 470)
        cot = skia.Path(); cot.addCircle(-2, 4, R_PELE + 4)
        pele = uniao(ante, capsula((0, 0), ombro, 2 * R_PELE + 6, 2 * R_PELE + 16), cot)
    else:
        pele = ante
    cv.drawPath(pele, paint("#000000", 50, blur=10))
    pinta(cv, pele, (0, V_PELE * 0.5), (U_ARO, V_PELE * 0.5), 2 * R_PELE, TONS_PELE, 1.0, linha=PELE_LINHA,
          larg_linha=2.6)
    if not banho:                                          # manga curta da camiseta no braço
        m0 = (d[0] * 250, d[1] * 250); m1 = (d[0] * 520, d[1] * 520)
        mg = capsula(m0, m1, 2 * R_PELE + 44, 2 * R_PELE + 50)
        pinta(cv, mg, (m0[0] - 60, m0[1] - 40), (m0[0] + 60, m0[1] + 40), 140, TONS_CAMISETA, 1.0,
              linha=esc_cor(CAMISETA_ESC, 0.3), larg_linha=3)
        n = (-d[1], d[0])
        cv.drawLine(m0[0] + d[0] * 22 + n[0] * 66, m0[1] + d[1] * 22 + n[1] * 66,
                    m0[0] + d[0] * 22 - n[0] * 66, m0[1] + d[1] * 22 - n[1] * 66, paint(CAMISETA_ESC, 180, "stroke", 4))
    cv.restore()
    # a metade da frente da malha (passa na frente da pele)
    if e.get("regua_fn") is not None:
        e["regua_fn"](cv)
    cv.drawArc(skia.Rect(U_ARO - RX_ARO, -R_ARO, U_ARO + RX_ARO, R_ARO), 90, 180, False, paint("#000000", 60, "stroke", 16, blur=4))
    cv.drawArc(skia.Rect(U_ARO - RX_ARO, -R_ARO, U_ARO + RX_ARO, R_ARO), 90, 180, False, paint(MALHA, 255, "stroke", 13))
    cv.drawArc(skia.Rect(U_ARO - RX_ARO + 5, -R_ARO + 5, U_ARO + RX_ARO - 5, R_ARO - 5), 100, 160, False,
               paint(MALHA_ESC, 220, "stroke", 2.2))
    # polegar livre
    polegar(cv, topo_v(U_POLEGAR, af))
    # risquinhos de coceira junto da borda do gesso
    for i, (u, v) in enumerate(((168, -112), (300, -100), (408, -94))):
        coceira_risco(cv, u, v, e.get("coc", (0, 0, 0))[i], 1.0 if e.get("coc", (0, 0, 0))[i] > 0 else 0)
    if e.get("capa_fn") is not None:
        e["capa_fn"](cv)
    cv.restore()


# ================================================================== O SECADOR (de perfil)
D_SEC = (0.28, 0.96)                      # para onde o bico aponta (para a abertura, de cima)
_L = math.hypot(*D_SEC); D_SEC = (D_SEC[0] / _L, D_SEC[1] / _L)
DIST_SEC = 150.0                          # do bico à abertura


def secador_pos(arm, sec):
    """Bico do secador: apontado para a abertura (sec = 1) ou recuando para fora do quadro (sec -> 0)."""
    gx, gy = l2w(arm, *GAP)
    k = DIST_SEC + (1 - sec) * 760
    return (gx - D_SEC[0] * k, gy - D_SEC[1] * k)


def _icone_floco(cv, x, y, r, cor, a):
    for i in range(3):
        ang = math.radians(90 + 60 * i)
        dx, dy = r * math.cos(ang), r * math.sin(ang)
        cv.drawLine(x - dx, y - dy, x + dx, y + dy, paint(cor, int(255 * a), "stroke", 3.4))
        for s in (-1, 1):
            bx, by = x + s * dx * 0.62, y + s * dy * 0.62
            for t_ in (-1, 1):
                a2 = ang + (math.pi if s < 0 else 0) + t_ * 2.5
                cv.drawLine(bx, by, bx + 0.42 * r * math.cos(a2), by + 0.42 * r * math.sin(a2), paint(cor, int(255 * a), "stroke", 2.6))


def _icone_chama(cv, x, y, r, cor, a):
    p = skia.Path()
    p.moveTo(x, y - r * 1.15)
    p.cubicTo(x + r * 0.95, y - r * 0.2, x + r * 0.95, y + r * 0.95, x, y + r * 0.95)
    p.cubicTo(x - r * 0.95, y + r * 0.95, x - r * 0.95, y - r * 0.1, x - r * 0.25, y - r * 0.45)
    p.cubicTo(x - r * 0.15, y - r * 0.05, x + r * 0.05, y - r * 0.4, x, y - r * 1.15)
    p.close()
    cv.drawPath(p, paint(cor, int(255 * a)))
    inner = skia.Path(); inner.addOval(skia.Rect(x - r * 0.38, y + r * 0.05, x + r * 0.38, y + r * 0.85))
    cv.drawPath(inner, paint("#FFE2B8" if cor != "#7F8B99" else "#9AA5B1", int(230 * a)))


def punho(cv, p, d, f, tons, a, esc=1.0, linha=AD_LINHA):
    """Mão FECHADA em volta de uma barra (cópia do piloto, com a cor da pele como parâmetro)."""
    if a <= 0:
        return
    m = skia.Matrix(); m.setAll(f[0] * esc, d[0] * esc, p[0], f[1] * esc, d[1] * esc, p[1], 0, 0, 1)
    cv.save(); cv.concat(m)
    corpo_p = rr_path(-24, -31, 22, 31, 17)
    for v in (-20, -6.5, 7, 20.5):
        k = skia.Path(); k.addCircle(21, v, 10); corpo_p = uniao(corpo_p, k)
    cv.drawPath(corpo_p, paint("#000000", int(60 * a), blur=6))
    pinta(cv, corpo_p, (0, -31), (0, 31), 56, tons, a, linha=linha, larg_linha=2.6)
    for v in (-13.2, 0.3, 13.8):
        cv.drawLine(31, v, 9, v + 2, paint(linha, int(220 * a), "stroke", 2.6))
    for v in (-20, -6.5, 7, 20.5):
        cv.drawCircle(24, v - 3, 3.2, paint(tons[2], int(200 * a)))
    pol = capsula((-18, -27), (13, -36), 18, 15)
    pinta(cv, pol, (-18, -27), (13, -36), 18, tons, a, linha=linha, larg_linha=2.4)
    cv.restore()


def secador(cv, tip, bot, a, verde=0.0):
    """Secador de cabelo de perfil + a mão adulta no cabo (manga teal). Referencial: x = para trás a partir
    do bico, y = lado do cabo. `bot`: botão deslizante (-1 floco de neve, 0 desligado, +1 chaminha)."""
    if a <= 0:
        return
    d = D_SEC
    ang = math.degrees(math.atan2(-d[1], -d[0]))
    ar = math.radians(ang)

    def w(x, y):
        return (tip[0] + x * math.cos(ar) - y * math.sin(ar), tip[1] + x * math.sin(ar) + y * math.cos(ar))
    # antebraço adulto (no mundo, atrás do secador): do punho no cabo para cima, para fora do quadro
    pu = w(214, 206)
    sobe = (pu[0] + 150, pu[1] - 560)
    ante = capsula(pu, sobe, 78, 92)
    pinta(cv, ante, pu, sobe, 84, TONS_AD, a, linha=AD_LINHA)
    m0 = lerp2(pu, sobe, 0.36)
    mg = capsula(m0, (sobe[0] + 40, sobe[1] - 160), 108, 116)
    pinta(cv, mg, m0, sobe, 112, TONS_MANGA_AD, a, linha=MANGA_AD_ESC, larg_linha=3)
    # fio
    c0 = w(220, 252)
    fio = skia.Path(); fio.moveTo(*c0)
    fio.cubicTo(c0[0] + 40, c0[1] + 30, c0[0] + 160, c0[1] - 10, c0[0] + 220, c0[1] - 300)
    cv.drawPath(fio, paint("#3A4452", int(255 * a), "stroke", 9))
    cv.save(); cv.translate(*tip); cv.rotate(ang)
    cabo = capsula((198, 30), (216, 224), 70, 62)
    tambor = rr_path(64, -58, 304, 58, 56)
    bico = poli([(0, -25), (72, -40), (72, 40), (0, 25)])
    corpo = uniao(cabo, tambor, bico)
    cv.drawPath(corpo, paint("#000000", int(80 * a), blur=12))
    if verde > 0:
        cv.drawPath(corpo, paint(VERDE, int(150 * verde * a), "stroke", 24, blur=8))
    pinta(cv, cabo, (198, 30), (214, 214), 70, (SEC_ESC, SEC, SEC_CL, SEC, SEC_ESC), a, linha=esc_cor(SEC_ESC, 0.3))
    sh = skia.GradientShader.MakeLinear([skia.Point(0, -58), skia.Point(0, 58)],
                                        [_c(SEC_ESC), _c(SEC_CL), _c(SEC), _c(SEC_ESC)], [0.0, 0.3, 0.65, 1.0])
    cv.drawPath(tambor, paint(SEC, int(255 * a), shader=sh))
    cv.drawPath(tambor, paint(esc_cor(SEC_ESC, 0.3), int(220 * a), "stroke", 2.5))
    cv.drawOval(skia.Rect(284, -48, 310, 48), paint("#566476", int(255 * a)))
    for yy in (-30, -12, 6, 24):
        cv.drawLine(290, yy, 304, yy + 4, paint("#2F3A47", int(220 * a), "stroke", 3))
    cv.drawRect(skia.Rect(64, -50, 82, 50), paint("#8796A8", int(255 * a)))
    sh2 = skia.GradientShader.MakeLinear([skia.Point(0, -40), skia.Point(0, 40)], [_c("#6C7C90"), _c(SEC_BICO), _c("#3E4B5B")])
    cv.drawPath(bico, paint(SEC_BICO, int(255 * a), shader=sh2))
    cv.drawPath(bico, paint("#2F3A47", int(220 * a), "stroke", 2.5))
    cv.drawLine(4, -16, 66, -28, paint("#9FB0C3", int(170 * a), "stroke", 3))
    if verde > 0:
        cv.drawPath(corpo, paint(VERDE, int(255 * verde * a), "stroke", 6))
    # botão deslizante no cabo: floco de neve num lado, chaminha no outro (sem letras)
    placa = rr_path(176, 34, 236, 148, 26)
    cv.drawPath(placa, paint("#2F3A47", int(255 * a)))
    cv.drawPath(placa, paint("#5E6C7E", int(255 * a), "stroke", 2.5))
    yk = 91 + 22 * bot
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(186, yk - 12, 226, yk + 12), 10, 10), paint("#E6EEF6", int(255 * a)))
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(186, yk - 12, 226, yk + 12), 10, 10), paint("#5E6C7E", int(255 * a), "stroke", 2))
    frio_on = clamp(-bot); quente_on = clamp(bot)
    for (yy, fn, on, cor) in ((50, _icone_floco, frio_on, AR_FRIO), (132, _icone_chama, quente_on, AR_QUENTE)):
        cv.save(); cv.translate(206, yy); cv.rotate(-ang)
        if on > 0:
            cv.drawCircle(0, 0, 22, paint(cor, int(120 * on * a), blur=8))
        fn(cv, 0, 0, 14, lerpc("#7F8B99", cor, on) if on > 0 else "#7F8B99", a)
        cv.restore()
    # a mão adulta fechada no cabo
    punho(cv, (214, 206), (0.09, 0.996), (1.0, 0.0), TONS_AD, a, esc=1.45)
    cv.restore()


def ar_secador(cv, tip, cor, a, ts, alcance):
    """3 linhas de ar onduladas saindo do bico até a abertura (contorno escuro: lê sobre parede clara)."""
    if a <= 0:
        return
    d = D_SEC; n = (-d[1], d[0])
    for k, off in enumerate((-17, 0, 17)):
        pts = []
        for i in range(26):
            s = lerp(10, alcance, i / 25)
            o = off * lerp(0.7, 0.35, i / 25) + 6.5 * math.sin((s - ts * 260) / 34 * 2 * math.pi + k * 1.7)
            pts.append((tip[0] + d[0] * s + n[0] * o, tip[1] + d[1] * s + n[1] * o))
        p = poli(pts, fechar=False)
        cv.drawPath(p, paint("#1E3550", int(150 * a), "stroke", 12))
        cv.drawPath(p, paint(cor, int(255 * a), "stroke", 6))


# ================================================================== CENÁRIO: a sala (lances 1 e 2)
SALA_X0, SALA_Y0, SALA_X1, SALA_Y1, SALA_ESC = -260.0, 120.0, 1300.0, 1500.0, 1.5


def sala(cv):
    def _d(c):
        c.scale(SALA_ESC, SALA_ESC); c.translate(-SALA_X0, -SALA_Y0); _sala(c)
    img = cacheado("sala", (SALA_X1 - SALA_X0) * SALA_ESC, (SALA_Y1 - SALA_Y0) * SALA_ESC, _d)
    cv.save(); cv.translate(SALA_X0, SALA_Y0); cv.scale(1 / SALA_ESC, 1 / SALA_ESC)
    cv.drawImage(img, 0, 0, LINEAR)
    cv.restore()


def _sala(cv):
    sh = skia.GradientShader.MakeLinear([skia.Point(0, 150), skia.Point(0, 1040)], [_c(PAREDE_A), _c(PAREDE_B)])
    cv.drawRect(skia.Rect(-600, -400, 1700, 1100), paint(PAREDE_A, shader=sh))
    # janela da casa (luz do dia), sem texto
    jx0, jy0, jx1, jy1 = 690, 330, 980, 650
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(jx0 - 14, jy0 - 14, jx1 + 14, jy1 + 14), 8, 8), paint("#F7F9FB"))
    vid = skia.GradientShader.MakeLinear([skia.Point(jx0, jy0), skia.Point(jx1, jy1)], [_c("#BFE3F7"), _c("#E9F6FD")])
    cv.drawRect(skia.Rect(jx0, jy0, jx1, jy1), paint("#CFEAF8", shader=vid))
    cv.drawLine((jx0 + jx1) / 2, jy0, (jx0 + jx1) / 2, jy1, paint("#F7F9FB", 255, "stroke", 12))
    cv.drawLine(jx0, (jy0 + jy1) / 2, jx1, (jy0 + jy1) / 2, paint("#F7F9FB", 255, "stroke", 12))
    cv.drawRect(skia.Rect(jx0 - 24, jy1 + 10, jx1 + 24, jy1 + 26), paint("#E7ECF1"))
    # o braço do sofá (encosto de lado) e o assento ao fundo
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(-600, 1006, 1800, 1700), 60, 60), paint("#000000", 60, blur=18))
    sh = skia.GradientShader.MakeLinear([skia.Point(0, 1000), skia.Point(0, 1300)], [_c(SOFA_CL), _c(SOFA), _c(SOFA_ESC)])
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(-600, 996, 1800, 1700), 56, 56), paint(SOFA, shader=sh))
    cv.drawLine(-600, 1060, 1800, 1060, paint(SOFA_ESC, 160, "stroke", 4))
    for x in range(-560, 1800, 160):
        cv.drawCircle(x, 1130, 6, paint(SOFA_ESC, 200))
    # a almofada debaixo do braço (membro apoiado)
    alm = skia.Path()
    alm.moveTo(70, 1010)
    alm.cubicTo(60, 960, 90, 938, 170, 940)
    alm.cubicTo(420, 948, 700, 946, 980, 938)
    alm.cubicTo(1050, 936, 1070, 970, 1060, 1010)
    alm.cubicTo(1056, 1060, 1030, 1072, 980, 1070)
    alm.cubicTo(700, 1062, 420, 1062, 170, 1070)
    alm.cubicTo(96, 1072, 74, 1050, 70, 1010)
    alm.close()
    cv.drawPath(alm, paint("#000000", 70, blur=14))
    sh = skia.GradientShader.MakeLinear([skia.Point(0, 938), skia.Point(0, 1070)], [_c(ALMOF_CL), _c(ALMOF), _c(ALMOF_ESC)])
    cv.drawPath(alm, paint(ALMOF, shader=sh))
    cv.save(); cv.clipPath(alm, skia.ClipOp.kIntersect, True)
    for i, x in enumerate(range(110, 1060, 56)):
        for j, y in enumerate((968, 1004, 1040)):
            cv.drawCircle(x + (28 if j % 2 else 0), y, 5, paint("#E3EEF8", 180))
    cv.restore()
    cv.drawPath(alm, paint(ALMOF_ESC, 220, "stroke", 3))
    # carrinho de brinquedo na frente da almofada (pista de criança em casa), sem marca
    carrinho(cv, 690, 1034)


def carrinho(cv, x, y):
    cv.drawOval(skia.Rect(x - 60, y + 14, x + 64, y + 30), paint("#000000", 60, blur=6))
    corpo = skia.Path()
    corpo.moveTo(x - 58, y + 12); corpo.lineTo(x - 56, y - 8); corpo.cubicTo(x - 40, y - 14, x - 30, y - 16, x - 22, y - 16)
    corpo.lineTo(x - 10, y - 38); corpo.lineTo(x + 30, y - 38); corpo.lineTo(x + 44, y - 16)
    corpo.cubicTo(x + 58, y - 14, x + 62, y - 6, x + 62, y + 12); corpo.close()
    cv.drawPath(corpo, paint("#F2C14E"))
    cv.drawPath(corpo, paint("#B88A1E", 230, "stroke", 2.5))
    jan = poli([(x - 6, y - 33), (x + 12, y - 33), (x + 12, y - 18), (x - 16, y - 18)])
    cv.drawPath(jan, paint("#BFE3F7"))
    jan2 = poli([(x + 18, y - 33), (x + 27, y - 33), (x + 36, y - 18), (x + 18, y - 18)])
    cv.drawPath(jan2, paint("#BFE3F7"))
    for wx in (x - 34, x + 38):
        cv.drawCircle(wx, y + 14, 13, paint("#2F3A47"))
        cv.drawCircle(wx, y + 14, 5, paint("#C8D2DC"))


# ---- a régua (lance 2) e a mãozinha que segura
D_REG = (math.cos(math.radians(45)), math.sin(math.radians(45)))    # direção da régua (referencial do braço)
L_REG = 250.0


def regua_desenho(cv, tip, ang_extra=0.0, a=1.0):
    """Régua escolar de madeira clara com marquinhas de medida e SEM números. `tip` = ponta da frente
    (referencial do braço); o corpo vai para trás (para cima-esquerda)."""
    if a <= 0:
        return
    ang = math.degrees(math.atan2(D_REG[1], D_REG[0])) + ang_extra
    cv.save(); cv.translate(*tip); cv.rotate(ang)
    r = skia.Rect(-L_REG, -17, 0, 17)
    cv.drawRect(skia.Rect(-L_REG + 4, -13, 4, 21), paint("#000000", int(60 * a), blur=6))
    sh = skia.GradientShader.MakeLinear([skia.Point(0, -17), skia.Point(0, 17)], [_c(REGUA_CL), _c(REGUA), _c(REGUA_ESC)])
    cv.drawRect(r, paint(REGUA, int(255 * a), shader=sh))
    cv.drawRect(r, paint("#8C6A33", int(220 * a), "stroke", 2.4))
    for i in range(int(L_REG / 12)):
        x = -L_REG + 10 + i * 12
        h = 12 if i % 5 == 0 else 6
        cv.drawLine(x, -17, x, -17 + h, paint("#6B4E22", int(220 * a), "stroke", 2))
    cv.restore()


def regua_mao(cv, end, a=1.0, aberta=0.0):
    """A OUTRA mãozinha da criança segurando a ponta de trás da régua; o antebraço sai do quadro pelo alto
    à esquerda (referencial do braço)."""
    if a <= 0:
        return
    # antebraço CURTO e fino (pulso de criança) e a manga lilás logo ali, DENTRO do quadro: lê-se o braço
    # da própria criança (o leitor às cegas achou o braço longo e nu "enorme, na diagonal")
    sai = (end[0] - 290, end[1] - 310)
    m0 = lerp2(end, sai, 0.36)                             # a manga lilás da mesma camiseta: é a criança
    ante = capsula(end, lerp2(end, sai, 0.42), 60, 66)
    pinta(cv, ante, end, sai, 64, TONS_PELE, a, linha=PELE_LINHA)
    pinta(cv, capsula(m0, (sai[0] - 200, sai[1] - 160), 100, 112), m0, sai, 106, TONS_CAMISETA, a,
          linha=esc_cor(CAMISETA_ESC, 0.3), larg_linha=3)
    nn = (-(sai[1] - end[1]), sai[0] - end[0]); L = math.hypot(*nn) or 1.0; nn = (nn[0] / L, nn[1] / L)
    m1 = lerp2(end, sai, 0.41)                             # a bainha da manga
    cv.drawLine(m1[0] - nn[0] * 48, m1[1] - nn[1] * 48, m1[0] + nn[0] * 48, m1[1] + nn[1] * 48,
                paint(CAMISETA_ESC, int(200 * a), "stroke", 4))
    d = (D_REG[0], D_REG[1]); f = (D_REG[1], -D_REG[0])
    if aberta < 0.5:
        punho(cv, (end[0] + d[0] * 6, end[1] + d[1] * 6), d, f, TONS_PELE, a, esc=0.95, linha=PELE_LINHA)
    else:                                                  # a mão abre (soltou a régua)
        p = (end[0] + d[0] * 10, end[1] + d[1] * 10)
        palma = capsula((p[0] - 10, p[1] - 6), (p[0] + 22, p[1] + 10), 52, 44)
        pinta(cv, palma, (p[0], p[1] - 26), (p[0], p[1] + 26), 52, TONS_PELE, a, linha=PELE_LINHA)
        for k in range(4):
            q0 = (p[0] + 26, p[1] - 12 + k * 9); q1 = (q0[0] + 34, q0[1] + 6 + k * 3)
            pinta(cv, capsula(q0, q1, 14, 12), q0, q1, 14, TONS_PELE, a, linha=PELE_LINHA, larg_linha=1.8)


# ================================================================== CENÁRIO: o banheiro (lance 3)
DUCHA = (575.0, 430.0)                      # centro da ducha (mundo)


def banheiro(cv):
    def _d(c):
        c.scale(SALA_ESC, SALA_ESC); c.translate(-SALA_X0, -SALA_Y0); _banheiro(c)
    img = cacheado("banheiro", (SALA_X1 - SALA_X0) * SALA_ESC, (SALA_Y1 - SALA_Y0) * SALA_ESC, _d)
    cv.save(); cv.translate(SALA_X0, SALA_Y0); cv.scale(1 / SALA_ESC, 1 / SALA_ESC)
    cv.drawImage(img, 0, 0, LINEAR)
    cv.restore()


def _banheiro(cv):
    """Azulejos claros com rejunte e a ducha redonda cromada no alto."""
    sh = skia.GradientShader.MakeLinear([skia.Point(0, 150), skia.Point(0, 1400)], [_c("#EEF4F7"), _c("#D9E4EA")])
    cv.drawRect(skia.Rect(-600, -400, 1800, 1800), paint(AZULEJO, shader=sh))
    L = 128
    for k, y in enumerate(range(-384, 1800, L)):
        if k % 6 == 4:
            cv.drawRect(skia.Rect(-600, y, 1800, y + L), paint("#CFE3EE", 200))
    for x in range(-640, 1800, L):
        cv.drawLine(x, -400, x, 1800, paint(REJUNTE, 255, "stroke", 5))
    for y in range(-384, 1800, L):
        cv.drawLine(-600, y, 1800, y, paint(REJUNTE, 255, "stroke", 5))
    for x in range(-640, 1800, L):
        for y in range(-384, 1800, L):
            cv.drawLine(x + 12, y + 14, x + 40, y + 14, paint("#FFFFFF", 150, "stroke", 3))
    # o cano e a ducha
    hx, hy = DUCHA
    cano = skia.Path(); cano.moveTo(hx + 250, 120); cano.lineTo(hx + 250, 250)
    cano.quadTo(hx + 250, hy - 70, hx + 120, hy - 70); cano.lineTo(hx + 50, hy - 52)
    cv.drawPath(cano, paint("#000000", 60, "stroke", 30, blur=8))
    cv.drawPath(cano, paint("#9BA9B8", 255, "stroke", 24))
    cv.drawPath(cano, paint("#E6EEF6", 220, "stroke", 6))
    cv.save(); cv.translate(hx, hy); cv.rotate(-14)
    cv.drawOval(skia.Rect(-120, -40, 120, 40), paint("#000000", 70, blur=12))
    sh = skia.GradientShader.MakeLinear([skia.Point(0, -46), skia.Point(0, 30)], [_c("#F2F6FA"), _c("#AAB7C5"), _c("#7D8B9B")])
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(-120, -50, 120, 10), 30, 30), paint("#AAB7C5", shader=sh))
    cv.drawOval(skia.Rect(-120, -10, 120, 30), paint("#8796A8"))
    cv.drawOval(skia.Rect(-112, -6, 112, 26), paint("#B9C6D3"))
    for i in range(-4, 5):
        for j in (0, 1):
            cv.drawCircle(i * 22 + (11 if j else 0), 6 + j * 10, 3.2, paint("#55657A"))
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(-120, -50, 120, 10), 30, 30), paint("#6E7E93", 220, "stroke", 2.5))
    cv.restore()


# gotas: deterministicas (saem da face da ducha e caem no gesso)
_RNG = np.random.default_rng(7)
GOTAS = [(float(_RNG.uniform(0, 1)), float(_RNG.uniform(0, 1)), float(_RNG.uniform(0.85, 1.15))) for _ in range(30)]
U_AGUA0, U_AGUA1 = 175.0, 470.0             # trecho do gesso onde a água bate (referencial do braço)


def _gota(cv, x, y, a, esc=1.0):
    p = skia.Path()
    p.moveTo(x, y - 17 * esc)
    p.cubicTo(x + 7 * esc, y - 4 * esc, x + 9 * esc, y + 4 * esc, x, y + 9 * esc)
    p.cubicTo(x - 9 * esc, y + 4 * esc, x - 7 * esc, y - 4 * esc, x, y - 17 * esc)
    p.close()
    cv.drawPath(p, paint(GOTA_ESC, int(170 * a), "stroke", 4))
    cv.drawPath(p, paint(GOTA, int(255 * a)))
    cv.drawCircle(x - 2.5 * esc, y + 1 * esc, 2.4 * esc, paint("#FFFFFF", int(230 * a)))


def gotas(cv, arm, ts, t_on, a, capa_on=0.0, afunda=0.0, adiantada=False):
    """A água da ducha. Cada gota sai da face da ducha e cai num ponto do gesso (ou da capa)."""
    if a <= 0:
        return
    hx, hy = DUCHA
    for i, (f_lane, fase, vel) in enumerate(GOTAS):
        k = (ts - t_on) * 2.0 * vel - fase
        if adiantada:
            k += 1.0
        if k < 0:
            continue
        k = k % 1.0
        u = lerp(U_AGUA0, U_AGUA1, f_lane)
        topo = topo_v(u, afunda) - (16 if capa_on > 0.5 else 0)
        ex, ey = l2w(arm, u, topo)
        sx, sy = hx - 90 + 180 * f_lane, hy + 18 + 6 * f_lane
        kk = k / 0.9
        if kk < 1:
            x, y = lerp(sx, ex, kk), lerp(sy, ey - 10, kk ** 1.25)
            _gota(cv, x, y, a * clamp(kk * 6), 1.0)
        else:                                              # respingo ao bater
            s = (k - 0.9) / 0.1
            for sg in (-1, 1):
                cv.drawArc(skia.Rect(ex - 10 - 22 * s, ey - 16 - 10 * s, ex + 10 + 22 * s, ey + 6),
                           200 if sg < 0 else 290, 50, False, paint(GOTA_ESC, int(200 * a * (1 - s)), "stroke", 4))
                cv.drawArc(skia.Rect(ex - 10 - 22 * s, ey - 16 - 10 * s, ex + 10 + 22 * s, ey + 6),
                           200 if sg < 0 else 290, 50, False, paint(GOTA, int(255 * a * (1 - s)), "stroke", 2.5))


def _r_capa(u):
    if u < U_ARO - 8:
        return R_PELE + 12
    if u > U_ARO2 + 4:
        return R_ARO2 + 12
    return r_gesso(u) + 13


U_CAPA_FIM = U_ARO2 + 104
# a capa ENVOLVE o polegar (revisor: a ponta do polegar furava o contorno da capa no "jeito certo").
# O calombo cobre a ponta do polegar com folga (ponta em v ~ -104 em u ~ 536; capa sobe a ~ -114).
U_CALOMBO, A_CALOMBO, S_CALOMBO = U_POLEGAR + 34.0, 46.0, 34.0


def _r_capa_topo(u):
    """Raio da capa do lado de CIMA (onde está o polegar): o contorno do gesso + o calombo do polegar."""
    return _r_capa(u) + A_CALOMBO * math.exp(-((u - U_CALOMBO) / S_CALOMBO) ** 2)


def capa_impermeavel(cv, u_esq, a=1.0, verde=0.0):
    """Capa plástica transparente (azul-claro translúcido, reflexo branco), fechada na ponta dos dedos e com
    o elástico na borda aberta (u_esq); o lado de cima tem o calombo que envolve o polegar. Referencial do
    braço."""
    if a <= 0 or u_esq >= U_CAPA_FIM - 20:
        return
    n = 48
    us = [lerp(u_esq, U_CAPA_FIM - 34, i / n) for i in range(n + 1)]
    top = [(u, -_r_capa_topo(u)) for u in us]
    bot = [(u, _r_capa(u)) for u in reversed(us)]
    p = suave(top, fechar=False)
    rr = _r_capa(U_CAPA_FIM - 34)
    p.lineTo(U_CAPA_FIM - 34, -rr)
    p.arcTo(skia.Rect(U_CAPA_FIM - 34 - 40, -rr, U_CAPA_FIM - 34 + 40, rr), -90, 180, False)
    for q in bot:
        p.lineTo(*q)
    p.close()
    cv.drawPath(p, paint(CAPA_C, int(95 * a)))
    cv.save(); cv.clipPath(p, skia.ClipOp.kIntersect, True)
    for vv, lg, al in ((-0.62, 9, 200), (-0.42, 4, 150), (0.58, 5, 110)):
        pts = [(u, vv * (_r_capa_topo(u) if vv < 0 else _r_capa(u))) for u in us]
        cv.drawPath(suave(pts, fechar=False), paint("#FFFFFF", int(al * a), "stroke", lg))
    cv.restore()
    cv.drawPath(p, paint(CAPA_BORDA, int(230 * a), "stroke", 3.2))
    if verde > 0:
        cv.drawPath(p, paint(VERDE, int(140 * verde * a), "stroke", 20, blur=8))
        cv.drawPath(p, paint(VERDE, int(255 * verde * a), "stroke", 5))
    # o elástico na borda aberta (em cima acompanha o calombo enquanto a capa passa pelo polegar)
    re_t, re_b = _r_capa_topo(u_esq) + 2, _r_capa(u_esq) + 2
    anel = skia.Rect(u_esq - 11, -re_t, u_esq + 11, re_b)
    cv.drawOval(anel, paint("#000000", int(60 * a), "stroke", 14, blur=4))
    cv.drawOval(anel, paint(CAPA_ELAST, int(255 * a), "stroke", 11))
    cv.drawOval(anel, paint("#4F8DB5", int(230 * a), "stroke", 2))


def contas_agua(cv, ts, t0, a):
    """Gotas que batem na capa viram contas e ESCORREM pela frente dela até pingar (referencial do braço)."""
    if a <= 0:
        return
    for i in range(12):
        u = lerp(U_AGUA0 + 10, U_AGUA1, ((i * 0.618) % 1.0))
        k = ((ts - t0) * 1.6 - i * 0.083)
        if k < 0:
            continue
        k = k % 1.0
        rc = _r_capa(u) + 2
        if k < 0.75:
            v = lerp(-(_r_capa_topo(u) + 2) * 0.55, rc, e_inout(k / 0.75))
            cv.drawCircle(u, v, 10, paint(GOTA_ESC, int(190 * a), "stroke", 4))
            cv.drawCircle(u, v, 10, paint("#DFF4FF", int(245 * a)))
            cv.drawCircle(u - 2, v - 2, 2.2, paint("#FFFFFF", int(255 * a)))
        else:                                              # pinga da parte de baixo
            s = (k - 0.75) / 0.25
            _gota(cv, u, rc + 10 + 90 * s * s, a * (1 - s), 0.8)


def mao_capa(cv, p, a, lado=-1):
    """Mão adulta puxando o elástico da capa por CIMA; o antebraço sobe inclinado para fora do quadro (um
    adulto debruçado, uma pessoa só). O grupo inteiro aparece/some junto (camada com alfa: sem 'raio-X' do
    punho da manga, do antebraço e dos dedos uns através dos outros)."""
    if a <= 0:
        return
    x, y = p
    cv.saveLayerAlpha(skia.Rect(x - 120, y - 900, x + 900, y + 120), int(255 * clamp(a)))
    _mao_capa(cv, x, y, lado, 1.0)
    cv.restore()


def _mao_capa(cv, x, y, lado, a):
    sai = (x + 300, y + lado * 470)
    p0 = (x + 14, y + lado * 34)
    ante = capsula(p0, lerp2(p0, sai, 0.3), 82, 88)
    pinta(cv, ante, p0, sai, 86, TONS_AD, a, linha=AD_LINHA)
    m0 = lerp2(p0, sai, 0.17)
    pinta(cv, capsula(m0, (sai[0] + 60, sai[1] + lado * 140), 112, 122), m0, sai, 118,
          TONS_MANGA_AD, a, linha=MANGA_AD_ESC, larg_linha=3)
    nx, ny = -(sai[1] - p0[1]), sai[0] - p0[0]; L = math.hypot(nx, ny) or 1.0; nx, ny = nx / L, ny / L
    m1 = lerp2(p0, sai, 0.22)
    cv.drawLine(m1[0] - nx * 54, m1[1] - ny * 54, m1[0] + nx * 54, m1[1] + ny * 54, paint(MANGA_AD_ESC, int(200 * a), "stroke", 4))
    palma = capsula((x + 4, y + lado * 30), (x + 24, y + lado * 4), 62, 54)
    pinta(cv, palma, (x - 28, y), (x + 34, y), 62, TONS_AD, a, linha=AD_LINHA)
    pol = capsula((x - 16, y + lado * 14), (x - 22, y - lado * 10), 22, 18)
    pinta(cv, pol, (x - 28, y), (x - 8, y), 22, TONS_AD, a, linha=AD_LINHA, larg_linha=2.2)
    for k in range(3):
        q0 = (x + 14 + k * 12, y + lado * 6); q1 = (x + 6 + k * 12, y - lado * 16)
        pinta(cv, capsula(q0, q1, 18, 16), (q0[0] - 9, q0[1]), (q0[0] + 9, q0[1]), 18, TONS_AD, a, linha=AD_LINHA,
              larg_linha=2)


# ================================================================== ESTADOS (tempo -> o que a cena mostra)
def estado_sala(t, T):
    V = T["var"]
    e = {}
    # relógio da cena: congela do "pode?" ao veredito (e o quadro 0 = o lance 1 congelado)
    ts = t
    if t < V or T["pode1"] <= t < T["validado"]:
        ts = T["pode1"]
    elif T["pode2"] <= t < T["anulado1"]:
        ts = T["pode2"]
    e["ts"] = ts
    # secador: aponta (1) ou fora do quadro (0)
    if t < V:
        sec = 1.0
    elif t < V + 0.5:
        sec = 1 - e_inout(prog(t, V, V + 0.5))
    else:
        sec = e_out(prog(t, T["secador"] - 0.14, T["secador"] + 0.36)) * (1 - e_inout(prog(t, T["e1"] - 0.06, T["e1"] + 0.36)))
    e["sec"] = sec
    bot = 0.0
    bot = lerp(bot, -1.0, e_out(prog(t, T["ar"] - 0.05, T["ar"] + 0.12)))
    bot = lerp(bot, 1.0, e_out(prog(t, T["quente"] - 0.05, T["quente"] + 0.1)))
    bot = lerp(bot, -1.0, e_out(prog(t, T["nunca_fim"] - 0.06, T["nunca_fim"] + 0.08)))
    e["bot"] = bot
    e["ar_frio"] = (prog(t, T["frio"] - 0.03, T["frio"] + 0.18) * (1 - prog(t, T["quente"] - 0.02, T["quente"] + 0.06))
                    + prog(t, T["nunca_fim"] + 0.06, T["nunca_fim"] + 0.2))
    e["ar_quente"] = prog(t, T["quente"] + 0.02, T["quente"] + 0.12) * (1 - prog(t, T["nunca_fim"] - 0.08, T["nunca_fim"]))
    e["verde"] = max(janela(t, T["coceira2"] - 0.05, T["quente"] - 0.12, 0.2, 0.1),
                     janela(t, T["nunca_fim"] + 0.1, T["e1"] - 0.1, 0.15, 0.15))
    e["x_quente"] = janela(t, T["nunca"] - 0.04, T["nunca_fim"] + 0.05, 0.1, 0.15)
    # coceira: 3 risquinhos e os dedinhos tamborilando
    coc = []
    for i in range(3):
        if t < V:
            k = 1.0
        elif t < V + 0.5:
            k = 1 - prog(t, V, V + 0.3)
        else:
            k = e_back(prog(t, T["coceira1"] + 0.04 + 0.13 * i, T["coceira1"] + 0.34 + 0.13 * i))
            k *= 1 - prog(t, T["alivia"] + 0.06 + 0.12 * i, T["alivia"] + 0.2 + 0.12 * i)
        coc.append(k)
    e["coc"] = tuple(coc)
    if t < V:
        e["tamb"] = 1.0
    else:
        e["tamb"] = max(1 - prog(t, V, V + 0.3), janela(t, T["coceira1"] - 0.04, T["alivia"] + 0.15, 0.12, 0.35))
    e["brilho"] = prog(t, T["gesso1"] - 0.04, T["gesso1"] + 0.55)
    # régua
    ent = e_out(prog(t, T["regua"] - 0.14, T["regua"] + 0.34))
    ins = 62 * e_inout(prog(t, T["cocar"] - 0.04, T["pode2"] - 0.06))
    if T["cocar"] < ts < T["pode2"]:
        ins += 9 * math.sin((ts - T["cocar"]) * 2 * math.pi * 4.2) * prog(ts, T["cocar"], T["cocar"] + 0.15)
    sai = e_inout(prog(t, T["arranhao"] - 0.08, T["arranhao"] + 0.26))
    ins = lerp(ins, -96, sai)
    cai = prog(t, T["arranhao"] + 0.3, T["arranhao"] + 0.84)
    e.update(reg_ent=ent, reg_ins=ins, reg_cai=cai, reg_sai=sai)
    e["reg_on"] = T["e1"] <= t < T["wipe"] + 0.4
    return e


ESTADO_CERTO = dict(ts=0.0, sec=1.0, bot=-1.0, ar_frio=1.0, ar_quente=0.0, verde=1.0, x_quente=0.0,
                    coc=(0.0, 0.0, 0.0), tamb=0.0, brilho=-1.0, reg_on=False)


def regua_fn_de(e, t):
    """A régua e a mãozinha (no referencial do braço), desenhadas entre a pele e a malha da frente."""
    if not e.get("reg_on") or e["reg_ent"] <= 0:
        return None

    def fn(cv):
        fora = (1 - e["reg_ent"]) * 520
        tip = (GAP[0] + D_REG[0] * (e["reg_ins"] - fora) + 4, GAP[1] + D_REG[1] * (e["reg_ins"] - fora))
        end = (tip[0] - D_REG[0] * L_REG, tip[1] - D_REG[1] * L_REG)
        cai = e["reg_cai"]
        cv.save()
        # o que já entrou na abertura fica escondido (corta no plano da borda, fora da meia-lua)
        corte = skia.Path(); corte.addRect(skia.Rect(-900, -900, U_ARO - 2, 900))
        corte = uniao(corte, ABERTURA)
        cv.clipPath(corte, skia.ClipOp.kIntersect, True)
        if cai <= 0:
            regua_desenho(cv, tip)
        cv.restore()
        if cai > 0:                                        # soltou: a régua cai para fora do quadro
            k = e_inout(cai) if cai < 1 else 1.0
            cx_, cy_ = lerp2(tip, end, 0.5)
            cv.save(); cv.translate(-30 * k, 620 * k * k); cv.rotate(-38 * k)
            regua_desenho(cv, tip, a=1 - prog(cai, 0.8, 1.0))
            cv.restore()
        # a mãozinha (some para fora pelo alto à esquerda depois de soltar)
        rec = e_inout(prog(cai, 0.1, 0.8))
        regua_mao(cv, (end[0] - 260 * rec, end[1] - 200 * rec), 1.0, aberta=1.0 if cai > 0.05 else 0.0)
    return fn


def estado_banho(t, T):
    e = {}
    ts = t
    if T["pode3"] <= t < T["anulado2"]:
        ts = T["pode3"]
    e["ts"] = ts
    r0, r1 = T["rebob3"], T["capa"]
    volta = e_inout(prog(t, r0, r1 - 0.05))                # rebobina: tudo volta ao gesso seco
    e["molhado"] = prog(t, T["molhado"] - 0.05, T["molhado"] + 0.75) * (1 - volta)
    e["afunda"] = e_inout(prog(t, T["perde"] - 0.04, T["perde"] + 0.5)) * (1 - volta)
    e["agua1"] = (1 - prog(t, r0, r0 + 0.3)) if t >= T["chuveiro"] - 0.08 else 0.0
    e["capa_u"] = lerp(U_CAPA_FIM + 10, U_ARO - 52, e_inout(prog(t, T["capa"] - 0.04, T["capa"] + 0.3)))
    e["capa_on"] = 1.0 if t >= T["capa"] - 0.04 else 0.0
    e["maos"] = janela(t, T["capa"] - 0.1, T["capa"] + 0.36, 0.1, 0.25)
    e["maos_sai"] = prog(t, T["capa"] + 0.3, T["capa"] + 0.62)
    e["agua2"] = prog(t, T["impermeavel"] - 0.02, T["impermeavel"] + 0.14)
    e["contas"] = prog(t, T["impermeavel"] + 0.22, T["impermeavel"] + 0.4)
    e["ok"] = prog(t, T["impermeavel"] + 0.32, T["impermeavel"] + 0.5)
    e["verde_capa"] = janela(t, T["impermeavel"] + 0.3, T["off"], 0.2, 0.1)
    return e


# ================================================================== câmeras
CAM_Q0 = (1.36, 500.0, 728.0, -1.0)    # quadro 0: secador + abertura + o braço com os dedinhos
CAM_JOGO = (1.28, 472.0, 738.0, -1.0)
CAM_L1_PERTO = (1.5, 322.0, 742.0, -1.0)    # congela: chega no bico + abertura
CAM_L2_PERTO = (1.5, 270.0, 790.0, -1.0)    # congela: a régua entrando na abertura
CAM_BANHO = (1.25, 372.0, 772.0)
CAM_BANHO_PERTO = (1.42, 340.0, 800.0)


def cam_sala(t, T):
    V = T["var"]
    if t < V:
        return CAM_Q0
    cam = lerp3(CAM_Q0, CAM_JOGO, e_inout(prog(t, V, V + 0.5)))
    cam = lerp3(cam, CAM_L1_PERTO, e_inout(prog(t, T["pode1"], T["pode1"] + 0.3)))
    cheg = prog(t, T["pode1_fim"], T["validado"])
    cam = (cam[0] * (1 + 0.05 * e_inout(cheg)),) + tuple(cam[1:])
    cam = lerp3(cam, CAM_JOGO, e_inout(prog(t, T["validado"] + 0.1, T["validado"] + 0.5)))
    cam = lerp3(cam, CAM_L2_PERTO, e_inout(prog(t, T["pode2"], T["pode2"] + 0.3)))
    cheg = prog(t, T["pode2_fim"], T["anulado1"])
    cam = (cam[0] * (1 + 0.05 * e_inout(cheg)),) + tuple(cam[1:])
    return lerp3(cam, CAM_JOGO, e_inout(prog(t, T["anulado1"] + 0.5, T["arranhao"] + 0.2)))


def cam_banho(t, T):
    cam = lerp3(CAM_BANHO, CAM_BANHO_PERTO, e_inout(prog(t, T["pode3"], T["pode3"] + 0.3)))
    cheg = prog(t, T["pode3_fim"], T["anulado2"])
    cam = (cam[0] * (1 + 0.05 * e_inout(cheg)),) + tuple(cam[1:])
    return lerp3(cam, CAM_BANHO, e_inout(prog(t, T["anulado2"] + 0.4, T["molhado"] + 0.2)))


# ================================================================== cenas
def cena_sala(cv, t, T, cam, e):
    cv.save(); aplica(cv, cam)
    sala(cv)
    e = dict(e)
    e["regua_fn"] = regua_fn_de(e, t)
    braco(cv, ARM_SALA, e, t)
    tip = secador_pos(ARM_SALA, e["sec"])
    if e["sec"] > 0.01:
        alc = DIST_SEC + 6
        ar_secador(cv, tip, AR_FRIO, min(1.0, e["ar_frio"]) * (1 if e["sec"] > 0.98 else 0), e["ts"] if e["ts"] else t, alc)
        ar_secador(cv, tip, AR_QUENTE, e["ar_quente"] * (1 if e["sec"] > 0.98 else 0), e["ts"] if e["ts"] else t, alc)
        secador(cv, tip, e["bot"], 1.0, e["verde"])
    cv.restore()
    return tip


def cena_banho(cv, t, T, cam, e):
    cv.save(); aplica(cv, cam)
    banheiro(cv)
    arm = ARM_BANHO
    ee = dict(e)
    if e["capa_on"] > 0:
        ee["capa_fn"] = lambda c: capa_impermeavel(c, e["capa_u"], 1.0, e["verde_capa"])
    braco(cv, arm, ee, t)
    gotas(cv, arm, e["ts"], T["chuveiro"] - 0.06, e["agua1"], 0.0, e["afunda"])
    if e["agua2"] > 0:
        gotas(cv, arm, t, T["impermeavel"], e["agua2"], 1.0, 0.0, adiantada=True)
        cv.save(); cv.translate(*arm["E"]); cv.rotate(arm["ang"])
        contas_agua(cv, t, T["impermeavel"] + 0.22, e["contas"])
        cv.restore()
    if e["maos"] > 0:                                     # a mão adulta vestindo a capa (puxa o elástico)
        sx = e["maos_sai"]
        u = e["capa_u"]
        px, py = l2w(arm, u + 6, -(_r_capa_topo(u) + 6))
        mao_capa(cv, (px + 170 * sx, py - 270 * sx), e["maos"])
    cv.restore()


# ================================================================== HUD do VAR (desenho próprio, cópia do piloto)
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
    """Gancho de 2 linhas ACIMA do monitor (não encosta na janela da cena)."""
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
    """Cantoneiras em L nos cantos da janela, fio ciano e varredura SÓ nas bordas."""
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


def selo_var(cv, t, x, y, esc, a, chip=None, a_chip=1.0, pontos=-1.0, cor_chip="#FFFFFF", flash=0.0):
    """Caixa VAR + chip de estado à direita (x, y = canto sup. esq.)."""
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
        if flash > 0:                                      # o chip troca de lance com um flash curto
            cv.drawRRect(r2, paint("#FFFFFF", int(200 * flash * aa)))
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


def circulo_tele(cv, x, y, rx, ry, k, a, seed=0.0, pulso=0.0, cor=CIANO):
    """Círculo de caneta do telestrador: traço com tremor, desenhado em `k` (0..1)."""
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
    cv.drawPath(p, _trim(paint(cor, int(110 * a * (0.6 + 0.4 * pulso)), "stroke", 18, blur=8), k))
    cv.drawPath(p, _trim(paint(cor, int(255 * a), "stroke", 8), k))


def carimbo_cor(cv, s, x, y, rot, t0, t, dur, cor, tam=88, esc0=1.9, sub=None, tam_sub=44):
    """Carimbo do veredito: OPACO, cor do semáforo, entra batendo e sai encolhendo para o chip do selo.
    `sub`: 2ª linha dentro do mesmo carimbo (a condição: SÓ AR FRIO)."""
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
    baixo = tam * 0.38 + (tam_sub * 1.25 if sub else 0)
    lw2 = skia.Font(F_BLACK, tam_sub).measureText(sub) if sub else 0
    meia = max(lw, lw2) / 2
    rr = skia.RRect.MakeRectXY(skia.Rect(-meia - 32, -tam * 1.02, meia + 32, baixo), 16, 16)
    cv.drawRRect(rr, paint("#000000", int(110 * a), blur=16))
    cv.drawRRect(rr, paint(CARTAO, int(245 * a)))
    cv.drawRRect(rr, paint(cor, int(255 * a), "stroke", 9))
    rr2 = skia.RRect.MakeRectXY(skia.Rect(-meia - 20, -tam * 0.9, meia + 20, baixo - tam * 0.12), 10, 10)
    cv.drawRRect(rr2, paint(cor, int(120 * a), "stroke", 2.5))
    cv.drawString(s, -lw / 2, 0, f, paint(cor, int(255 * a)))
    if sub:
        cv.drawLine(-meia + 6, tam * 0.2, meia - 6, tam * 0.2, paint(cor, int(150 * a), "stroke", 2.5))
        texto(cv, sub, 0, tam * 0.2 + tam_sub * 1.02, F_BLACK, tam_sub, "#FFFFFF", int(255 * a))
    cv.restore()


def ruido_vhs(cv, t, a):
    """Faixas de ruído correndo (fita rebobinando)."""
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


def equipe(cv, x, y, t, t0, a, esc=1.0):
    """Ícone da equipe: bustos simples, sem mão, sem instrumento (cópia do piloto)."""
    if a <= 0:
        return
    for k, (dx, dy, e_, cor) in enumerate(((-110, 16, 0.84, "#4E9E94"), (110, 16, 0.84, "#4E9E94"), (0, 0, 1.0, TEAL))):
        kk = e_back(prog(t, t0 + 0.08 * k, t0 + 0.08 * k + 0.4))
        if kk > 0:
            busto(cv, x + dx * esc, y + (dy + 30 * (1 - kk)) * esc, e_ * esc * clamp(kk, 0, 1.2), cor, a * clamp(kk * 2))


def busto(cv, x, y, esc, cor, a):
    cv.save(); cv.translate(x, y); cv.scale(esc, esc)
    om = skia.Path(); om.addRRect(skia.RRect.MakeRectXY(skia.Rect(-56, -6, 56, 74), 46, 46))
    clip = skia.Path(); clip.addRect(skia.Rect(-60, -10, 60, 58))
    om = skia.Op(om, clip, skia.PathOp.kIntersect_PathOp)
    cv.drawPath(om, paint("#000000", int(80 * a), blur=8))
    cv.drawPath(om, paint(cor, int(255 * a)))
    gola = skia.Path(); gola.moveTo(-16, -4); gola.lineTo(0, 18); gola.lineTo(16, -4)
    cv.drawPath(gola, paint(CARTAO, int(150 * a), "stroke", 4))
    cv.drawCircle(0, -40, 30, paint("#000000", int(80 * a), blur=6))
    cv.drawCircle(0, -40, 30, paint("#EEF3F8", int(255 * a)))
    cv.drawArc(skia.Rect(-30, -70, 30, -10), 200, 140, False, paint(cor, int(255 * a), "stroke", 10))
    cv.restore()


def apito_icone(cv, x, y, esc, a, rot=-14.0):
    """Apito de árbitro (desenho, sem texto): corpo redondo, bocal e cordão ciano."""
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


def selo_serie(cv, a):
    if a <= 0:
        return
    lw = larg_texto(T_SERIE, F_BLACK, 36)
    rr = skia.RRect.MakeRectXY(skia.Rect(CX - lw / 2 - 34, 148, CX + lw / 2 + 34, 208), 30, 30)
    cv.drawRRect(rr, paint(SELO_BG, int(235 * a)))
    cv.drawRRect(rr, paint(CIANO, int(255 * a), "stroke", 3))
    texto(cv, T_SERIE, CX, 191, F_BLACK, 36, CIANO, int(255 * a))


def marca_x(cv, x, y, r, cor, a):
    """X desenhado (sem texto) num disco escuro: o contraexemplo."""
    if a <= 0:
        return
    cv.drawCircle(x, y, r + 6, paint("#000000", int(90 * a), blur=8))
    cv.drawCircle(x, y, r, paint(CARTAO, int(235 * a)))
    cv.drawCircle(x, y, r, paint(cor, int(255 * a), "stroke", 5))
    d = r * 0.45
    cv.drawLine(x - d, y - d, x + d, y + d, paint(cor, int(255 * a), "stroke", 9))
    cv.drawLine(x - d, y + d, x + d, y - d, paint(cor, int(255 * a), "stroke", 9))


def marca_ok(cv, x, y, r, cor, a):
    """Visto desenhado (sem texto) num disco escuro."""
    if a <= 0:
        return
    cv.drawCircle(x, y, r + 6, paint("#000000", int(90 * a), blur=8))
    cv.drawCircle(x, y, r, paint(CARTAO, int(235 * a)))
    cv.drawCircle(x, y, r, paint(cor, int(255 * a), "stroke", 5))
    p = poli([(x - r * 0.45, y + r * 0.02), (x - r * 0.12, y + r * 0.35), (x + r * 0.5, y - r * 0.32)], fechar=False)
    pt = paint(cor, int(255 * a), "stroke", 9); pt.setStrokeCap(skia.Paint.kRound_Cap); pt.setStrokeJoin(skia.Paint.kRound_Join)
    cv.drawPath(p, pt)


FLOCO_HUD, CHAMA_HUD = "#2F86D9", "#F07A22"
ICO_DX, ICO_DY, ICO_ESC = -40.0, -36.0, 1.1      # a ficha fica acima e à esquerda do X (o X não a apaga)


def icone_ar(cv, x, y, tipo, a, esc=1.0):
    """Ficha GRANDE do tipo de ar ao lado do jato (o leitor às cegas quase não viu a diferença quente/frio):
    disco claro com contorno escuro e o floco de neve azul ou a chaminha laranja (sem letra)."""
    if a <= 0 or esc <= 0:
        return
    cor = FLOCO_HUD if tipo == "frio" else CHAMA_HUD
    cv.save(); cv.translate(x, y); cv.scale(esc, esc)
    cv.drawCircle(0, 4, 50, paint("#000000", int(70 * a), blur=8))
    cv.drawCircle(0, 0, 48, paint("#F7FAFD", int(250 * a)))
    cv.drawCircle(0, 0, 48, paint(CARTAO, int(200 * a), "stroke", 5))
    cv.drawCircle(0, 0, 41, paint(cor, int(255 * a), "stroke", 4))
    if tipo == "frio":
        for i in range(3):                                   # floco de neve grosso (lê no celular)
            ang = math.radians(90 + 60 * i)
            dx, dy = 27 * math.cos(ang), 27 * math.sin(ang)
            cv.drawLine(-dx, -dy, dx, dy, paint(cor, int(255 * a), "stroke", 6.5))
            for s in (-1, 1):
                bx, by = s * dx * 0.6, s * dy * 0.6
                for t_ in (-1, 1):
                    a2 = ang + (math.pi if s < 0 else 0) + t_ * 2.45
                    cv.drawLine(bx, by, bx + 12 * math.cos(a2), by + 12 * math.sin(a2), paint(cor, int(255 * a), "stroke", 5))
    else:
        _icone_chama(cv, 0, 4, 26, cor, a)
    cv.restore()


# palavras de ligação: nunca terminam um bloco nem uma linha da legenda (revisor: "PERDE / A" órfão)
LIGACAO = {"a", "o", "as", "os", "e", "de", "da", "do", "das", "dos", "em", "no", "na", "nos", "nas", "um", "uma",
           "pra", "que", "com", "é", "sua", "seu", "lá", "ele"}
ESP_LEG, LARG_LEG = 26, 920


def _base_tok(p):
    import re
    return re.sub(r"[.,:;!?—]", "", p["tok"]).lower()


def partir_linhas(bloco, tam):
    """Linhas da legenda de um bloco: [(palavra, largura), ...] por linha. Usa o MESMO número de linhas da
    quebra gulosa do piloto, mas escolhe a quebra EQUILIBRADA (menor linha mais longa), sem linha
    terminando em palavra de ligação, sem palavra sozinha na última linha e preferindo quebrar depois da
    vírgula."""
    from itertools import combinations
    ws = [(p, larg_texto(p["tok"].upper(), F_BLACK, tam)) for p in bloco]

    def larg(seg):
        return sum(w for _, w in seg) + ESP_LEG * (len(seg) - 1)
    gul, linha, lw = [], [], 0
    for p, w in ws:
        if linha and lw + ESP_LEG + w > LARG_LEG:
            gul.append(linha); linha, lw = [], 0
        linha.append((p, w)); lw += (ESP_LEG if lw else 0) + w
    if linha:
        gul.append(linha)
    k = len(gul)
    if k <= 1 or len(ws) > 12:
        return gul
    melhor = None
    for cortes in combinations(range(1, len(ws)), k - 1):
        lims = (0,) + cortes + (len(ws),)
        lns = [ws[lims[j]:lims[j + 1]] for j in range(k)]
        if any(larg(ln) > LARG_LEG for ln in lns):
            continue
        sc = max(larg(ln) for ln in lns)
        for ln in lns[:-1]:
            if _base_tok(ln[-1][0]) in LIGACAO:
                sc += 400
            if ln[-1][0].get("virg"):
                sc -= 60
        if len(lns[-1]) == 1 and len(ws) > k:
            sc += 150
        if melhor is None or sc < melhor[0]:
            melhor = (sc, lns)
    return melhor[1] if melhor else gul


def montar_blocos_var(pal):
    """Blocos da legenda deste episódio (embrulha o montar_blocos do cf_fratura_cola SEM mexer nele):
    frase por frase, um bloco só se tiver até 6 palavras E couber em 2 linhas no rodapé; senão divide no
    melhor ponto — nunca depois de palavra de ligação, de preferência depois da vírgula ou antes do 'e',
    equilibrado. Corrige o bloco de 3 linhas que subia até a moldura ('ARRANHÃO LÁ / DENTRO PODE /
    INFECCIONAR.') e o 'A' órfão ('MOLHADO, ELE PERDE / A' + 'FUNÇÃO E MACHUCA A PELE.'). A frase da CTA
    ('Manda...') fica inteira, como no piloto (vai para o cartão final)."""
    frases = []
    for b in montar_blocos(pal):                          # reagrupa por frase (montar_blocos só divide frases)
        if frases and not frases[-1][-1]["fim_frase"]:
            frases[-1] = frases[-1] + b
        else:
            frases.append(list(b))

    def dividir(fr):
        if fr[0]["w"].lower() == "manda" or (len(fr) <= 6 and len(partir_linhas(fr, 80)) <= 2):
            return [fr]
        melhor = None
        for i in range(1, len(fr)):
            sc = abs(i - (len(fr) - i))
            if _base_tok(fr[i - 1]) in LIGACAO:
                sc += 100
            if fr[i - 1].get("virg"):
                sc -= 3
            if _base_tok(fr[i]) in ("e", "mas"):
                sc -= 2
            if i == 1 or len(fr) - i == 1:
                sc += 3
            if i < len(fr) - i:
                sc += 0.25                                   # empate: a primeira parte mais longa
            if melhor is None or sc < melhor[0]:
                melhor = (sc, i)
        i = melhor[1]
        return dividir(fr[:i]) + dividir(fr[i:])
    blocos = []
    for fr in frases:
        blocos += dividir(fr)
    return blocos


def legenda_var(cv, blocos, t, destaque, y_base=1395, tam=80, a_extra=1.0):
    """Cópia da legenda karaokê do piloto (a palavra ativa cresce a partir do PRÓPRIO CENTRO), com a quebra
    de linha equilibrada (partir_linhas) e um alfa extra (a legenda sai no replay sem fala)."""
    import re
    if a_extra <= 0:
        return
    vivo = None
    for i, b in enumerate(blocos):
        ini = b[0]["t"] - 0.12
        fim = blocos[i + 1][0]["t"] - 0.12 if i + 1 < len(blocos) else b[-1]["t"] + b[-1]["d"] + 2.5
        if ini <= t < fim:
            vivo = b; break
    if not vivo:
        return
    esp = ESP_LEG
    linhas = partir_linhas(vivo, tam)
    entrada = e_out(clamp((t - (vivo[0]["t"] - 0.12)) / 0.15))
    a_x = clamp(a_extra)
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
            texto(cv, p["tok"].upper(), -w / 2, 0, F_BLACK, tam, cor, int(a * entrada * a_x), centro=False, contorno=12)
            cv.restore()
            x += w + esp
        y += alt


def interface_var(cv, t, T, blocos, destaque):
    """Cópia do cf_comum.interface (rodapé CFM a partir de 3 s, cartão final com a CTA e o aviãozinho)."""
    t_cta = T["manda"] - 0.15
    if t < t_cta:
        # o replay do JEITO CERTO (cortina do VAR) não tem fala: a legenda "PODE INFECCIONAR." sai antes dele,
        # para não juntar "infeccionar" com o secador brilhando em verde (revisor)
        a_leg = 1.0
        if T["infeccionar_fim"] <= t < T["gesso2"] - 0.12:
            a_leg = 1 - prog(t, T["infeccionar_fim"] + 0.02, T["infeccionar_fim"] + 0.2)
        legenda_var(cv, blocos, t, destaque, a_extra=a_leg)
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
VEREDITOS = (("pode1", "validado", T_VALID, VERDE), ("pode2", "anulado1", T_ANUL, AMBAR),
             ("pode3", "anulado2", T_ANUL, AMBAR))
DUR_CARIMBOS = (1.5, 1.35, 1.35)
POS_CARIMBOS = ((330.0, 530.0), (330.0, 500.0), (330.0, 500.0))
SUB_CARIMBOS = (T_FRIO, None, None)


def chip_estado(t, T):
    """(texto, alfa, pontos, cor, flash) do chip: LANCE n -> CHECANDO -> (carimbo) -> veredito -> JEITO CERTO."""
    cortes = (0.0, T["e1"], T["gesso2"], 1e9)
    certo = ((T["validado"] + DUR_CARIMBOS[0] - 0.05), T["wipe"] + 0.14, T["capa"] - 0.02)
    for k, (pd, vd, s, cor) in enumerate(VEREDITOS):
        if not (cortes[k] <= t < cortes[k + 1]):
            continue
        flash = 0.0
        if t < T[pd + "_fim"] + 0.04:
            a = 1.0
            if k == 1:
                a = prog(t, cortes[k] + 0.02, cortes[k] + 0.12)
                flash = 1 - prog(t, cortes[k] + 0.06, cortes[k] + 0.3)
            elif k == 2:
                a = prog(t, cortes[k] + 0.45, cortes[k] + 0.6)
            return T_LANCE[k], a, -1, "#FFFFFF", flash
        if t < T[vd] - 0.04:
            t0 = T[pd + "_fim"] + 0.04
            return T_CHEC, 1.0, prog(t, t0, T[vd] - 0.12), "#FFFFFF", 0.0
        dur = DUR_CARIMBOS[k]
        if t < T[vd] + dur - 0.05:
            return None, 0.0, -1, "#FFFFFF", 0.0
        if k == 0 and T["quente"] - 0.1 <= t < T["nunca_fim"] + 0.12:     # contraexemplo: o chip apaga
            return None, 0.0, -1, "#FFFFFF", 0.0
        if t >= certo[k]:
            a0 = certo[k] if k != 0 or t < T["quente"] else T["nunca_fim"] + 0.12
            return T_CERTO, prog(t, a0, a0 + 0.18), -1, VERDE, 0.0
        a = prog(t, T[vd] + dur - 0.1, T[vd] + dur + 0.1) * (1 - prog(t, certo[k] - 0.12, certo[k]))
        return s, a, -1, cor, 0.0
    return None, 0.0, -1, "#FFFFFF", 0.0


def cena(cv, t, T):
    """O lance da vez (com a cortina do VAR no replay do jeito certo). Devolve o que o HUD precisa."""
    info = {}
    if t < T["gesso2"]:
        e = estado_sala(t, T)
        cam = cam_sala(t, T)
        kw = prog(t, T["wipe"], T["wipe"] + 0.36)
        if kw <= 0:
            tip = cena_sala(cv, t, T, cam, e)
            info.update(lance=1 if t < T["e1"] else 2, cam=cam, e=e, tip=tip)
        else:
            camc = CAM_JOGO
            xw = lerp(JX0 - 10, JX1 + 10, e_inout(kw))
            if kw < 1:
                cv.save(); cv.clipRect(skia.Rect(xw, 0, W, H), True)
                cena_sala(cv, t, T, cam, e)
                cv.restore()
            cv.save(); cv.clipRect(skia.Rect(0, 0, xw, H), True)
            ec = dict(ESTADO_CERTO, ts=t)
            cena_sala(cv, t, T, camc, ec)
            cv.restore()
            if kw < 1:
                cv.drawLine(xw, JY0, xw, JY1, paint(CIANO, 160, "stroke", 26, blur=10))
                cv.drawLine(xw, JY0, xw, JY1, paint("#FFFFFF", 255, "stroke", 6))
            info.update(lance=2, cam=cam if kw < 1 else camc, e=e, certa=True, xw=xw if kw < 1 else W + 10)
    else:
        e = estado_banho(t, T)
        cam = cam_banho(t, T)
        cena_banho(cv, t, T, cam, e)
        info.update(lance=3, cam=cam, e=e)
    return info


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
        ruido_vhs(cv, t, max(rebob, janela(t, T["rebob3"], T["capa"] - 0.04, 0.04, 0.06)))
    if t_off <= t < t_off + 0.62:                       # a linha e o ponto de luz
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

    # ---------- grafismo sobre a imagem (coordenadas de tela)
    if tela_ligada and a_hud > 0:
        cv.save(); cv.clipRRect(jan_rr, skia.ClipOp.kIntersect, True)
        lance = info.get("lance")
        cam = info.get("cam")
        if lance in (1, 2) and not info.get("certa"):
            s = cam[0]
            gx, gy = na_tela(cam, *l2w(ARM_SALA, *GAP))
            if lance == 1:                               # círculo no bico + abertura
                tip = secador_pos(ARM_SALA, 1.0)
                tx, ty = na_tela(cam, *tip)
                cx_, cy_ = (gx + tx) / 2 + 6 * s, (gy + ty) / 2 + 4 * s
                k1 = e_out(prog(t, T["pode1"] + 0.12, T["pode1"] + 0.47))
                k0 = 1.0 if t < T["var"] else 0.0
                fora = 1 - prog(t, T["validado"] + 0.3, T["validado"] + 0.55)
                a_c = max(k0 * (1 - prog(t, T["var"], T["var"] + 0.12)), k1 * fora)
                k_tr = 1.0 if t < T["var"] else k1
                pul = 0.5 + 0.5 * math.sin(t * 8) if t < T["var"] or T["pode1_fim"] < t < T["validado"] else 0.0
                pul += 1.5 * max(0.0, 1 - abs(t - T["chama"] - 0.1) / 0.18)
                circulo_tele(cv, cx_, cy_, 128 * s, 124 * s, k_tr, a_c, 0.7, pul)
                e = info["e"]
                # ficha GRANDE do tipo de ar ao lado do jato: floco (frio) / chaminha (quente, que leva o X)
                if e["sec"] > 0.98:
                    mx, my = na_tela(cam, tip[0] + D_SEC[0] * 62, tip[1] + D_SEC[1] * 62)
                    ix, iy = mx - 112 * s + ICO_DX, my - 70 * s + ICO_DY      # o X do 'nunca' cai no canto da ficha
                    sai_ = 1 - prog(t, T["e1"] - 0.12, T["e1"] + 0.06)
                    t_f1, t_f2 = T["frio"] - 0.03, T["nunca_fim"] + 0.06
                    a_fr = (prog(t, t_f1, t_f1 + 0.12) * (1 - prog(t, T["quente"] - 0.06, T["quente"] + 0.02))
                            + prog(t, t_f2, t_f2 + 0.12)) * sai_
                    k_fr = e_back(prog(t, t_f2 if t >= t_f2 else t_f1, (t_f2 if t >= t_f2 else t_f1) + 0.24))
                    icone_ar(cv, ix, iy, "frio", clamp(a_fr), ICO_ESC * clamp(k_fr, 0, 1.2))
                    t_q = T["quente"] + 0.02
                    a_q = prog(t, t_q, t_q + 0.1) * (1 - prog(t, T["nunca_fim"] - 0.04, T["nunca_fim"] + 0.08))
                    icone_ar(cv, ix, iy, "quente", a_q, ICO_ESC * clamp(e_back(prog(t, t_q, t_q + 0.24)), 0, 1.2))
                if e["x_quente"] > 0:                    # contraexemplo: o ar quente leva X âmbar
                    mx, my = na_tela(cam, tip[0] + D_SEC[0] * 62, tip[1] + D_SEC[1] * 62)
                    k_x = e_back(prog(t, T["nunca"] - 0.04, T["nunca"] + 0.2))
                    circulo_tele(cv, mx, my, 92 * s, 92 * s, prog(t, T["nunca"] - 0.06, T["nunca"] + 0.2),
                                 e["x_quente"], 3.1, 0.0, AMBAR)
                    cv.save(); cv.translate(mx - 112 * s, my - 70 * s); cv.scale(clamp(k_x, 0, 1.2), clamp(k_x, 0, 1.2))
                    marca_x(cv, 0, 0, 36, AMBAR, e["x_quente"])
                    cv.restore()
            else:                                        # lance 2: a régua entrando / a abertura
                d = (D_REG[0], D_REG[1])
                k1 = e_out(prog(t, T["pode2"] + 0.12, T["pode2"] + 0.47))
                fora = 1 - prog(t, T["anulado1"] + 0.3, T["anulado1"] + 0.55)
                pul = 0.5 + 0.5 * math.sin(t * 8) if T["pode2_fim"] < t < T["anulado1"] else 0.0
                rx_, ry_ = na_tela(cam, *l2w(ARM_SALA, GAP[0] - d[0] * 60, GAP[1] - d[1] * 60))
                circulo_tele(cv, rx_, ry_ + 6 * s, 126 * s, 100 * s, k1, k1 * fora, 4.3, pul)
                # "dentro": círculo âmbar SÓ na abertura (o lá dentro é apontado, nunca mostrado)
                a_d = janela(t, T["dentro"] - 0.06, T["infeccionar"] + 0.22, 0.1, 0.3)
                if a_d > 0:
                    ox, oy = na_tela(cam, *l2w(ARM_SALA, U_ARO, 0))
                    pulA = 1.4 * max(0.0, 1 - abs(t - T["infeccionar"] - 0.08) / 0.22)
                    circulo_tele(cv, ox, oy, (RX_ARO + 52) * s, (R_ARO + 30) * s,
                                 e_out(prog(t, T["dentro"] - 0.06, T["dentro"] + 0.3)), a_d, 5.2, pulA, AMBAR)
        elif lance == 3:
            s = cam[0]
            e = info["e"]
            k1 = e_out(prog(t, T["pode3"] + 0.12, T["pode3"] + 0.47))
            fora = 1 - prog(t, T["anulado2"] + 0.3, T["anulado2"] + 0.55)
            pul = 0.5 + 0.5 * math.sin(t * 8) if T["pode3_fim"] < t < T["anulado2"] else 0.0
            cx_, cy_ = na_tela(cam, *l2w(ARM_BANHO, (U_AGUA0 + U_AGUA1) / 2, -R_ARO - 20))
            circulo_tele(cv, cx_, cy_, 200 * s, 118 * s, k1, k1 * fora, 2.1, pul)
            # "perde": seta âmbar curta mostrando o afundamento
            a_s = janela(t, T["perde"] - 0.02, T["machuca"] - 0.05, 0.15, 0.25) * (1 - prog(t, T["rebob3"], T["rebob3"] + 0.2))
            if a_s > 0:
                x0, y0 = na_tela(cam, *l2w(ARM_BANHO, U_AFUNDA, topo_v(U_AFUNDA, e["afunda"]) - 120))
                x1, y1 = na_tela(cam, *l2w(ARM_BANHO, U_AFUNDA, topo_v(U_AFUNDA, e["afunda"]) - 22))
                kk = e_out(prog(t, T["perde"] - 0.02, T["perde"] + 0.3))
                seta(cv, x0, y0, x0, lerp(y0, y1, kk), AMBAR, a_s, larg=11, tam=30)
            # "machuca": círculo âmbar na borda de cima, onde o gesso encosta na pele
            a_m = janela(t, T["machuca"] - 0.04, T["rebob3"], 0.12, 0.2)
            if a_m > 0:
                ox, oy = na_tela(cam, *l2w(ARM_BANHO, U_ARO, -R_ARO * 0.35))
                circulo_tele(cv, ox, oy, 82 * s, 104 * s, e_out(prog(t, T["machuca"] - 0.04, T["machuca"] + 0.3)), a_m,
                             1.4, 0.0, AMBAR)
            if e["ok"] > 0:                              # visto verde: a capa segura a água, o gesso fica seco
                ox, oy = na_tela(cam, *l2w(ARM_BANHO, U_ARO2 - 30, -R_ARO - 120))
                k_ok = e_back(prog(t, T["impermeavel"] + 0.32, T["impermeavel"] + 0.56))
                cv.save(); cv.translate(ox + 120 * s, oy); cv.scale(clamp(k_ok, 0, 1.2), clamp(k_ok, 0, 1.2))
                marca_ok(cv, 0, 0, 38, VERDE, e["ok"])
                cv.restore()
        if info.get("certa"):                            # replay do JEITO CERTO: a ficha do floco volta
            tip = secador_pos(ARM_SALA, 1.0)
            mx, my = na_tela(CAM_JOGO, tip[0] + D_SEC[0] * 62, tip[1] + D_SEC[1] * 62)
            s = CAM_JOGO[0]
            cv.save(); cv.clipRect(skia.Rect(0, 0, info["xw"], H), True)
            icone_ar(cv, mx - 112 * s + ICO_DX, my - 70 * s + ICO_DY, "frio", 1 - prog(t, T["gesso2"] - 0.12, T["gesso2"]),
                     ICO_ESC)
            cv.restore()
        # flash dos congelamentos e do corte de lance
        for t0, forca in ((T["pode1"], 150), (T["pode2"], 150), (T["pode3"], 150), (T["gesso2"], 190)):
            k = t - t0
            if 0 <= k < 0.16:
                cv.drawRect(JAN, paint("#FFFFFF", int(forca * (1 - k / 0.16))))
        cv.restore()
        varre = 0.0
        for pd, vd, _, _ in VEREDITOS:
            if T[pd + "_fim"] < t < T[vd]:
                varre = prog(t, T[pd + "_fim"], T[vd] - 0.05)
        moldura(cv, t, a_hud, varre)
        congelado = t < T["var"] or any(T[pd] + 0.02 <= t < T[vd] for pd, vd, _, _ in VEREDITOS)
        icone_pausa(cv, JX1 - 70, JY1 - 74, a_hud * (1.0 if congelado else 0.0))
        a_reb = max(janela(t, T["var"], T["var"] + 0.5, 0.03, 0.08), janela(t, T["rebob3"], T["capa"] - 0.04, 0.06, 0.08))
        icone_rebobina(cv, JX1 - 76, JY1 - 74, a_hud * a_reb)
        for (pd, vd, s_, cor), dur, (px, py), sub in zip(VEREDITOS, DUR_CARIMBOS, POS_CARIMBOS, SUB_CARIMBOS):
            carimbo_cor(cv, s_, px, py, -5, T[vd] - 0.02, t, dur, cor, sub=sub)
        # rótulo grande do corte de lance (LANCE 3)
        k = t - T["gesso2"]
        if -0.02 <= k < 0.6:
            a = prog(k, 0.0, 0.08) * (1 - prog(k, 0.42, 0.6))
            esc = lerp(1.25, 1.0, e_out(prog(k, 0.0, 0.16)))
            cv.save(); cv.translate(JX0 + 210, JY0 + 112); cv.scale(esc, esc)
            f = skia.Font(F_BLACK, 70); lw = f.measureText(T_LANCE[2])
            rr = skia.RRect.MakeRectXY(skia.Rect(-lw / 2 - 34, -70, lw / 2 + 34, 26), 16, 16)
            cv.drawRRect(rr, paint(CARTAO, int(225 * a))); cv.drawRRect(rr, paint(CIANO, int(255 * a), "stroke", 4))
            texto(cv, T_LANCE[2], 0, 0, F_BLACK, 70, "#FFFFFF", int(255 * a))
            cv.restore()

    # ---------- selo VAR + chip: entra em "VAR", dentro do monitor; sobe depois que o gancho saiu
    t_capa = T["pode1_fim"] + 0.06
    sobe = e_inout(prog(t, t_capa + 0.45, t_capa + 0.85))
    chip, a_chip, pontos, cor_chip, flash = chip_estado(t, T)
    k_s = prog(t, T["var"] - 0.04, T["var"] + 0.14)
    esc_s = lerp(0.92, 1.08, sobe) * (1 + 0.25 * (1 - e_back(k_s))) if k_s < 1 else lerp(0.92, 1.08, sobe)
    selo_var(cv, t, lerp(56, 64, sobe), lerp(JY0 + 24, 146, sobe), esc_s, a_hud * clamp(k_s * 1.5), chip, a_chip,
             pontos, cor_chip, flash)

    # ---------- fim: o VAR saiu; no seu caso, quem apita é a equipe
    a_eq = prog(t, T["no"] - 0.1, T["no"] + 0.1) * (1 - prog(t, T["manda"] - 0.35, T["manda"] - 0.1))
    if a_eq > 0:
        cv.drawCircle(CX, 800, 270, paint(TEAL, int(40 * a_eq), blur=60))
        equipe(cv, CX, 860, t, T["no"] - 0.1, a_eq, esc=1.65)
        pul = 1 + 0.06 * max(0.0, 1 - abs(t - T["equipe"] - 0.1) / 0.2)
        if pul > 1:
            cv.drawCircle(CX, 830, 200 * pul, paint(TEAL, int(70 * (pul - 1) / 0.06), "stroke", 6, blur=4))
        ka = e_out(prog(t, T["quem"] - 0.05, T["apita"] + 0.15))
        if ka > 0:
            x = lerp(140, CX + 12, ka); y = lerp(330, 600, ka) - 60 * math.sin(math.pi * ka)
            balanco = 10 * math.sin(max(0.0, t - T["apita"]) * 9) * math.exp(-max(0.0, t - T["apita"]) * 3)
            apito_icone(cv, x, y, lerp(0.7, 1.15, ka), a_eq * clamp(ka * 3), -14 + balanco)
    selo_serie(cv, prog(t, T["equipe"] - 0.1, T["equipe"] + 0.2) * (1 - prog(t, T["manda"] - 0.3, T["manda"])))

    capa(cv, t, t_capa, ep["gancho"][0], ep["gancho"][1])
    interface_var(cv, t, T, blocos, DESTAQUE)


# ================================================================== som (sintetizado aqui, sem licença)
SR = som.SR


def _env(n, a=0.005, r=0.2):
    return som._env(n, a, r)


def _passa_banda(x, f_lo, f_hi):
    lp = som._onepole_lp(x, f_hi)
    return lp - som._onepole_lp(lp, f_lo)


def _banda_fft(x, f_lo, f_hi):
    """Passa-banda por FFT (rápido para ruídos longos: chuveiro, secador)."""
    X = np.fft.rfft(x)
    f = np.fft.rfftfreq(len(x), 1 / SR)
    X[(f < f_lo) | (f > f_hi)] = 0
    y = np.fft.irfft(X, len(x))
    return y / (np.max(np.abs(y)) or 1.0)


def apito(dur=0.30, seed=11, ganho=0.55, solta=0.04):
    """Apito de árbitro: senoide ~3,2 kHz com o trinado da bolinha (FM e AM a ~40 Hz) + sopro. (piloto)"""
    n = int(dur * SR); t = np.arange(n) / SR
    fm = 3150 + 130 * np.sin(2 * np.pi * 41 * t)
    ph = 2 * np.pi * np.cumsum(fm) / SR
    am = 1 - 0.55 * (0.5 + 0.5 * np.sin(2 * np.pi * 41 * t + 0.7))
    tom = (np.sin(ph) + 0.22 * np.sin(2 * ph) + 0.08 * np.sin(3 * ph)) * am
    sopro = _passa_banda(np.random.default_rng(seed).standard_normal(n), 2000, 6000) * 0.5
    env = np.clip(t / 0.012, 0, 1) * np.clip((dur - t) / solta, 0, 1)
    return (tom + sopro * 0.6) * env * ganho


def apito_final():
    """Curto, longo (fim de jogo)."""
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


def fofo(seed=101):
    """Coisa mole cedendo: 'pfff' grave e abafado + baque mole. (piloto)"""
    n = int(0.42 * SR); t = np.arange(n) / SR
    x = som._onepole_lp(np.random.default_rng(seed).standard_normal(n), 600)
    y = x * np.sin(np.pi * t / 0.42) ** 1.2 * 3.0
    return y + np.pad(som.thump(seed) * 0.35, (0, max(0, n - len(som.thump(seed)))))[:n]


def tv_desliga(seed=71):
    n = int(0.36 * SR); t = np.arange(n) / SR
    f = 1200 * np.exp(-t * 10) + 60
    y = np.sin(2 * np.pi * np.cumsum(f) / SR) * _env(n, 0.002, 0.22) * 0.55
    rng = np.random.default_rng(seed)
    for _ in range(14):
        p = int(rng.uniform(0, n - 600)); m = int(rng.uniform(80, 400))
        y[p:p + m] += rng.standard_normal(m) * _env(m, 0.0002, 0.003) * 0.35
    return y


# ---- efeitos novos deste episódio
def secador_som(dur, grave=1.0, seed=111):
    """Secador ligado: ruído em banda 300–3000 Hz + zumbido de motor 120 Hz; entra em 0,15 s."""
    n = int(dur * SR); t = np.arange(n) / SR
    x = _banda_fft(np.random.default_rng(seed).standard_normal(n), 300 * grave, 3000 * grave)
    hum = 0.35 * np.sin(2 * np.pi * 120 * grave * t) + 0.12 * np.sin(2 * np.pi * 240 * grave * t)
    env = np.clip(t / 0.15, 0, 1) * np.clip((dur - t) / 0.1, 0, 1)
    return (x * 0.7 + hum) * env * 0.7


def raspa_regua(seed=121):
    """Raspadinha curta (régua coçando): ruído 2–4 kHz com AM ~60 Hz, 0,25 s."""
    n = int(0.25 * SR); t = np.arange(n) / SR
    x = _banda_fft(np.random.default_rng(seed).standard_normal(n), 2000, 4000)
    am = 0.5 + 0.5 * np.sin(2 * np.pi * 60 * t)
    return x * am * np.sin(np.pi * t / 0.25) * 0.8


def chuveiro_som(dur, seed=131):
    """Chiado de chuveiro (ruído 3–8 kHz) + gotinhas (ticks aleatórios 1,5–3 kHz)."""
    n = int(dur * SR); t = np.arange(n) / SR
    x = _banda_fft(np.random.default_rng(seed).standard_normal(n), 3000, 8000) * 0.55
    rng = np.random.default_rng(seed + 1)
    for _ in range(int(dur * 10)):
        p = int(rng.uniform(0, max(1, n - 2000))); f = rng.uniform(1500, 3000); m = 1600
        tt = np.arange(m) / SR
        x[p:p + m] += np.sin(2 * np.pi * f * tt) * np.exp(-tt / 0.006) * 0.35
    env = np.clip(t / 0.12, 0, 1) * np.clip((dur - t) / 0.05, 0, 1)
    return x * env


def plastico(seed=141):
    """Plástico amassando (crinkle): ruído com AM irregular, 0,4 s."""
    n = int(0.4 * SR); t = np.arange(n) / SR
    rng = np.random.default_rng(seed)
    x = _banda_fft(rng.standard_normal(n), 1500, 9000)
    am = np.repeat(rng.uniform(0, 1, n // 240 + 1) ** 3, 240)[:n]
    return x * am * np.sin(np.pi * t / 0.4) * 1.2


def elastico(seed=151):
    """'Snap' do elástico: ataque seco + ressonância curta de 900 Hz."""
    n = int(0.16 * SR); t = np.arange(n) / SR
    y = np.sin(2 * np.pi * 900 * t) * np.exp(-t / 0.03) * 0.6
    y[:int(0.003 * SR)] += np.random.default_rng(seed).standard_normal(int(0.003 * SR)) * 0.8
    return y


SFX = dict(som.SFX)
SFX.update({"apito": apito, "apito_final": apito_final, "rebobinar": rebobinar, "bipe": bipe, "bipe_alto": bipe_alto,
            "obturador": obturador, "fofo": fofo, "tv_desliga": tv_desliga, "raspa": raspa_regua,
            "plastico": plastico, "elastico": elastico})


def _media_movel(x, w):
    n = len(x)
    c = np.concatenate([[0.0], np.cumsum(x)])
    i = np.arange(n)
    lo = np.clip(i - w // 2, 0, n); hi = np.clip(i + (w - 1) // 2 + 1, 0, n)
    return (c[hi] - c[lo]) / w


def mixar(voz, dur, eventos, ganho_trilha=0.40):
    """Cópia do som.mixar do piloto (mesma trilha, mesmo ducking) que conhece os efeitos desta série."""
    n = int(dur * SR)
    v = np.zeros(n); v[:min(n, len(voz))] = voz[:n]
    musica = som.trilha(dur) * ganho_trilha
    win = int(0.06 * SR)
    envv = np.sqrt(np.maximum(_media_movel(v ** 2, win), 0.0))
    alvo = np.where(envv > 0.02, 0.38, 1.0)
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
    # sons de duração variável (dependem dos tempos da fala): registrados aqui
    d_frio = T["quente"] - T["frio"] + 0.03
    d_quente = T["nunca_fim"] - T["quente"]
    d_frio2 = max(0.2, T["e1"] - T["nunca_fim"] - 0.1)
    d_replay = T["gesso2"] - T["wipe"] - 0.2
    d_ch1 = T["pode3"] - T["chuveiro"] + 0.1
    d_ch2 = T["rebob3"] - T["anulado2"] + 0.1
    d_ch3 = T["off"] - T["impermeavel"] + 0.1
    SFX.update({"sec_frio": lambda: secador_som(d_frio), "sec_quente": lambda: secador_som(d_quente, 0.82, 112),
                "sec_frio2": lambda: secador_som(d_frio2, 1.0, 113), "sec_replay": lambda: secador_som(d_replay, 1.0, 114),
                "chuv1": lambda: chuveiro_som(d_ch1), "chuv2": lambda: chuveiro_som(d_ch2, 132),
                "chuv3": lambda: chuveiro_som(d_ch3, 133)})
    ev = [(0.0, "apito", 0.85), (T["chama"] + 0.02, "pop", 0.25), (T["var"] - 0.02, "rebobinar", 0.7)]
    for pd, vd, _, _ in VEREDITOS:
        ev.append((T[pd] - 0.01, "obturador", 0.85))
        t0 = T[pd + "_fim"] + 0.07
        ev += [(t0, "bipe", 0.75), (t0 + 0.22, "bipe", 0.75), (t0 + 0.44, "bipe_alto", 0.8)]
        ev.append((T[vd] - 0.02, "thump", 0.9))
    ev += [(T["validado"] - 0.26, "apito", 0.45)]                     # apito curto no silêncio antes do VALIDADO
    # lance 1 — secador
    ev += [(T["coceira1"] + 0.06 + 0.13 * i, "pop", 0.24) for i in range(3)]
    ev += [(T["gesso1"], "shimmer", 0.25), (T["secador"] - 0.1, "whoosh", 0.35)]
    ev += [(T["ar"] - 0.02, "tick", 0.5), (T["frio"] - 0.03, "sec_frio", 0.32)]
    ev += [(T["alivia"] + 0.08 + 0.12 * i, "pop", 0.22 - 0.05 * i) for i in range(3)]
    ev += [(T["coceira2"] + 0.05, "shimmer", 0.22)]
    ev += [(T["quente"] - 0.03, "tick", 0.5), (T["quente"] + 0.02, "sec_quente", 0.32), (T["nunca"], "thump", 0.5)]
    ev += [(T["nunca_fim"] + 0.06, "sec_frio2", 0.28)]
    # lance 2 — régua
    ev += [(T["e1"] - 0.04, "whoosh", 0.3), (T["e1"] + 0.02, "tick", 0.4), (T["regua"] - 0.1, "whoosh", 0.25)]
    ev += [(T["cocar"] + 0.04, "raspa", 0.42), (T["cocar"] + 0.32, "raspa", 0.34)]
    ev += [(T["arranhao"] - 0.06, "whoosh", 0.3), (T["arranhao"] + 0.36, "pop", 0.3)]
    ev += [(T["wipe"] - 0.02, "whoosh", 0.42), (T["wipe"] + 0.3, "shimmer", 0.25), (T["wipe"] + 0.12, "sec_replay", 0.26)]
    # lance 3 — chuveiro
    ev += [(T["gesso2"] - 0.03, "tick", 0.55), (T["gesso2"] + 0.02, "whoosh", 0.45)]
    ev += [(T["chuveiro"] - 0.08, "chuv1", 0.34), (T["anulado2"] + 0.04, "chuv2", 0.2)]
    ev += [(T["perde"] - 0.02, "fofo", 0.4)]
    ev += [(T["rebob3"] - 0.04, "rebobinar", 0.35)]
    ev += [(T["capa"] - 0.06, "plastico", 0.5), (T["capa"] + 0.3, "elastico", 0.55)]
    ev += [(T["impermeavel"] - 0.02, "chuv3", 0.26), (T["impermeavel"] + 0.34, "shimmer", 0.3)]
    # apito final, TV desligando, equipe, apito passando, CTA
    ev += [(T["apito_f"], "apito_final", 0.6), (T["off"] + 0.02, "tv_desliga", 0.75)]
    ev += [(T["no"] - 0.1 + 0.08 * k + 0.2, "pop", 0.28) for k in range(3)]
    ev += [(T["apita"] + 0.1, "pop", 0.32), (T["equipe"], "shimmer", 0.4), (T["manda"] + 0.05, "whoosh", 0.5)]
    return ev


def tempos_previa(T):
    return [0.0, T["var"] + 0.25, T["coceira1"] + 0.4, T["gesso1"] + 0.3, T["secador"] + 0.4, T["pode1"] + 0.55,
            T["validado"] + 0.3, T["frio"] + 0.25, T["alivia"] + 0.3, T["coceira2"] + 0.3, T["quente"] + 0.3,
            T["nunca"] + 0.25, T["nunca_fim"] + 0.25,
            T["regua"] + 0.3, T["cocar"] + 0.4, T["pode2"] + 0.6, T["anulado1"] + 0.3, T["arranhao"] + 0.3,
            T["arranhao"] + 0.6, T["dentro"] + 0.3, T["infeccionar"] + 0.2, T["wipe"] + 0.2, T["wipe"] + 0.6,
            T["gesso2"] + 0.3, T["chuveiro"] + 0.5, T["pode3"] + 0.6, T["anulado2"] + 0.3, T["molhado"] + 0.5,
            T["perde"] + 0.5, T["machuca"] + 0.4, T["rebob3"] + 0.25, T["capa"] + 0.15, T["capa"] + 0.35,
            T["impermeavel"] + 0.5, T["impermeavel"] + 1.1, T["off"] - 0.1, T["off"] + 0.1, T["no"] + 0.3, T["apita"] + 0.3,
            T["equipe"] + 0.3, T["manda"] + 0.5, T["manda"] + 1.6]


# ================================================================== render (cópia do piloto + os vãos deste episódio)
VAO_CHECANDO = 0.86                   # fim de "pode?" -> veredito: ~0,3 s de congelar + ~0,55 s de CHECANDO
VAOS_EXTRA = (("gesso", 2, 0.85),     # replay do JEITO CERTO (secador no frio) depois de "infeccionar."
              ("capa", 1, 0.60),      # rebobina para o gesso seco antes da capa entrar
              ("no", 3, 1.12))        # apito final + TV desligando, antes de "No seu caso"
PRE_APITO = 0.25                      # o apito do quadro 0 não embola com "Chama"


def pausa_checando(audio, pal, vao=VAO_CHECANDO):
    """Insere silêncio depois de cada 'pode?' até o vão chegar a `vao` (cópia do piloto)."""
    ins = []
    for i in range(len(pal) - 1):
        if pal[i]["tok"].lower() == "pode?":
            fim = pal[i]["t"] + pal[i]["d"]; gap = pal[i + 1]["t"] - fim
            if gap < vao:
                ins.append((fim + 0.04, vao - gap))
    partes, ult = [], 0
    for t0, extra in ins:
        p = int(t0 * SR); partes += [audio[ult:p], np.zeros(int(extra * SR), dtype=audio.dtype)]; ult = p
    partes.append(audio[ult:])
    novo = np.concatenate(partes)

    def remap(t):
        return t + sum(extra for t0, extra in ins if t > t0)
    return novo, [dict(p, t=remap(p["t"])) for p in pal], ins


def garantir_vao(audio, pal, palavra, n, vao):
    """Silêncio antes da n-ésima `palavra` até o vão chegar a `vao` (nada da fala é cortado). (piloto)"""
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
    T["fim_fala"] = pal[-1]["t"] + pal[-1]["d"]
    T["total"] = T["fim_fala"] + 2.2
    T["wipe"] = T["infeccionar"] + 0.40          # replay do jeito certo (secador no frio) no vão antes de "Gesso"
    T["rebob3"] = T["pele_fim"] + 0.04           # rebobina para o gesso seco no vão antes de "Capa"
    T["apito_f"] = T["no"] - 1.0                 # apito final (curto, longo) no silêncio
    T["off"] = T["no"] - 0.48                    # a TV desliga no sopro longo
    return T


def fazer_render_var(quadro_fn, mapa, sons_fn, tempos_fn, respiro_cta=0.8):
    def render(ep, mp4, tmp, previa=False):
        roteiro = "\n".join(ep["roteiro"])
        voz_bruta, palavras = _voz.narrar(roteiro, _voz.RITMO_COMO_FUNCIONA, os.path.join(tmp, "voz"))
        voz_c, pal, tirado = comprimir(voz_bruta, palavras, respiro_cta=respiro_cta)
        pal = alinhar(pal, roteiro)
        voz_c, pal, ins = pausa_checando(voz_c, pal)
        for palavra, n, vao in VAOS_EXTRA:
            voz_c, pal = garantir_vao(voz_c, pal, palavra, n, vao)
        voz_c = np.concatenate([np.zeros(int(PRE_APITO * SR), dtype=voz_c.dtype), voz_c])
        pal = [dict(p, t=p["t"] + PRE_APITO) for p in pal]
        T = montar_T(pal, mapa)
        print(f"{ep['id']}: silêncio cortado {tirado:.2f}s | CHECANDO {[round(x[1], 2) for x in ins]} | "
              f"duração final {T['total']:.2f}s")
        blocos = montar_blocos_var(pal)

        def quadro_t(cv, t):
            quadro_fn(cv, t, T, blocos, ep)

        if previa:
            return _previas(quadro_t, tempos_fn(T), tmp, ep["id"]), T["total"]
        wav = os.path.join(tmp, f"{ep['id']}_mix.wav")
        som.gravar_wav(wav, mixar(voz_c, T["total"], sons_fn(T)))
        codificar(quadro_t, T["total"], wav, mp4)
        return mp4, T["total"]
    return render


render = fazer_render_var(quadro, ANCORAS, sons, tempos_previa, respiro_cta=0.8)
