# -*- coding: utf-8 -*-
"""COMO FUNCIONA — o eixo da perna ("TODA PERNA TEM / UMA LINHA"): perna torta no adulto e a
osteotomia (corte planejado no osso para realinhar).

Mesmo estilo das cenas aprovadas (osso marfim com sombra, osso novo dourado que vira marfim, metal
do fixador, rótulos com ponteiro, carimbos, brilhos, calendário, legenda karaokê, CTA com
aviãozinho). Storyboard e correções do verificador (lote3_cf/cf_eixo_perna_storyboard.json):
  * Dois ossos marfim, "um em cima, outro embaixo", que se encontram no joelho: sem pele, sem
    músculo, sem nome de osso. O de cima se dissolve no fundo (não desenha o quadril).
  * A linha dourada ACOMPANHA os dois ossos, sem âncora anatômica (nenhum "centro do joelho"); em
    "torta" ela dobra junto com o osso de baixo; em "reposiciona" volta a ficar reta e coincide com
    a linha-fantasma (o eixo desejado).
  * Peso: duas setas, uma de cada lado do joelho, sem "partes iguais"; torta = uma seta grande só
    de um lado, que acende em vermelho. O medidor de desgaste é um gráfico (não tecido) e sai na
    troca de assunto ("osteotomia") sem voltar a encher; no fim NÃO há medidor (sem promessa de
    resultado): só o peso se repartindo de novo e o vermelho apagando.
  * "QUANTO" sem número de graus; nenhum exame de imagem (régua-guia reta, SEM marcas, pousada
    sobre o eixo — mede alinhamento, não tamanho); corte limpo, sem sangue; abraçadeiras de aço
    genéricas (sem modelo de implante).
  * Capa: a linha já aparece, fraca (o objeto do gancho). O selo COMO FUNCIONA fica sempre; no zoom
    do corte o mundo se dissolve antes de chegar à faixa dele (vela_topo).
A cena é PRESA ao roteiro pelas palavras-âncora (ANCORAS): roteiro sem elas = KeyError no render,
não vídeo dessincronizado. Todo texto desenhado está em ep["tela"].
"""
import math

import skia

from .cf_alongamento import (ACO, ACO_ESC, ACO_HL, F_BLACK, NOVO, NOVO_G, OSSO_B, OSSO_C, OSSO_L, OURO,
                             VERMELHO, W, H, C, brilhos, clamp, e_back, e_inout, e_out, fundo, larg_texto, lerp,
                             lerpc, paint, prog, texto)
from .cf_comum import capa, carimbo, fazer_render, interface, selo_como_funciona
from .cf_fratura_cola import calendario

ANCORAS = {
    "toda": ("toda", 1, False), "invisivel": ("invisível", 1, False), "eixo": ("eixo", 1, False),
    "reparte": ("reparte", 1, False), "peso": ("peso", 1, False), "joelho": ("joelho", 1, False),
    "torta": ("torta", 1, False), "carga": ("carga", 1, False), "lado": ("lado", 1, False),
    "desgastar": ("desgastar", 1, False), "antes1": ("antes", 1, False), "hora": ("hora", 1, False),
    "adulto": ("adulto", 1, False), "sozinha": ("sozinha", 1, False),
    "caminho": ("caminho", 1, False), "osteotomia": ("osteotomia", 1, False), "corte": ("corte", 1, False),
    "planejado": ("planejado", 1, False), "antes2": ("antes", 2, False), "mede": ("mede", 1, False),
    "onde": ("onde", 1, False), "quanto": ("quanto", 1, False), "corta": ("corta", 1, False),
    "reposiciona": ("reposiciona", 1, False), "certo": ("certo", 1, False), "fixa": ("fixa", 1, False),
    "cicatrizar": ("cicatrizar", 1, False), "alinhado": ("alinhado", 1, False),
    "reorganizar": ("reorganizar", 1, False), "carga2": ("carga", 2, False), "manda": ("manda", 1, False),
}
DESTAQUE = {"invisível", "eixo", "peso", "joelho", "torta", "lado", "desgastar", "hora", "adulto", "sozinha",
            "osteotomia", "planejado", "mede", "onde", "quanto", "corta", "reposiciona", "certo", "fixa",
            "alinhado", "reorganizar", "carga"}

# ------------------------------------------------------------------ geometria (mundo, antes da câmera)
X = 410                         # eixo da perna no mundo (a câmera o leva do centro para a esquerda)
Y_FEM = 360                     # topo do osso de cima (dissolve no fundo até ~550)
Y_JOELHO = 782                  # meio da fresta do joelho
P = 935                         # ponto da dobra no osso de baixo = ponto do corte
HT = 46                         # meia largura da diáfise do osso de baixo
Y_BASE = 1190                   # extremidade do osso de baixo (dobrado, a ponta ainda fica acima da legenda)
Y_L0, Y_L1 = 392, 1222          # a linha dourada passa um pouco das duas pontas
TETA = 16.0                     # dobra (graus) — geometria do desenho, NÃO vai para a tela
FENDA = 8                       # fenda fina do corte
Y_SPLIT = 700                   # onde o bloco PESO se divide nas duas setas
X_COL = 604                     # coluna da direita (rótulos), fora da perna
Y_CAM = 788                     # y na tela do foco: a ponta de baixo do osso fica acima de ~1222 (legenda)
W_RG, Y_RG0, Y_RG1 = 34, 430, 1216   # régua-guia (reta, sem marcas) centrada no eixo
ESCURO = "#0B1824"


# ------------------------------------------------------------------ estado (tudo a partir das palavras)
def angulo(t, T):
    a = TETA * e_inout(prog(t, T["torta"], T["torta"] + 1.0))                       # entorta devagar
    return a * (1 - e_inout(prog(t, T["reposiciona"] + 0.05, T["certo"] + 0.15)))   # volta ao eixo certo


def fenda(t, T):
    return FENDA * e_out(prog(t, T["corta"] + 0.08, T["corta"] + 0.3))


def pouso(T, n):
    """Instante em que o bloco PESO pousa no joelho (1ª vez em "joelho", 2ª antes de "carga")."""
    return T["joelho"] + 0.02 if n == 1 else T["carga2"] - 0.05


def zoom(t, T):
    return e_inout(prog(t, T["corta"] + 0.05, T["corta"] + 0.85)) * (
        1 - e_inout(prog(t, T["alinhado"] + 0.55, T["reorganizar"] + 0.25)))


def camera(t, T):
    """-> (x na tela do eixo, y na tela do foco, escala, y do foco no mundo). Capa: perna centrada; na
    linha invisível desliza para a esquerda (libera a coluna dos rótulos); no corte aproxima."""
    px = lerp(540, X, e_inout(prog(t, T["invisivel"] - 0.2, T["invisivel"] + 0.6)))
    z = zoom(t, T)
    tremor = 0.0
    for t0, forca in ((T["eixo"], 5), (T["sozinha"], 4), (T["corta"] + 0.1, 8), (T["fixa"] + 0.45, 5),
                      (T["carga2"] + 0.45, 4)):
        k = t - t0
        if 0 <= k < 0.35:
            tremor += forca * math.sin(k * 70) * (1 - k / 0.35)
    return px + tremor, Y_CAM, lerp(1.0, 1.28, z), lerp(800, P, z)


def na_tela(cam, x, y):
    px, py, s, fy = cam
    return px + (x - X) * s, py + (y - fy) * s


def aplica(cv, cam):
    px, py, s, fy = cam
    cv.translate(px, py); cv.scale(s, s); cv.translate(-X, -fy)


def girar(ang, f):
    """Rotação do pedaço de baixo em volta da borda côncava (direita) do ponto da dobra."""
    m = skia.Matrix(); m.setRotate(-ang, X + HT, P + f)
    return m


def gira_pt(ang, f, x, y):
    a = math.radians(-ang); cx, cy = X + HT, P + f
    dx, dy = x - cx, y - cy
    return cx + dx * math.cos(a) - dy * math.sin(a), cy + dx * math.sin(a) + dy * math.cos(a)


# ------------------------------------------------------------------ ossos
def path_femur():
    x = X; p = skia.Path()
    p.moveTo(x - 50, Y_FEM)
    p.lineTo(x - 52, 610)
    p.cubicTo(x - 55, 668, x - 100, 690, x - 98, 738)
    p.cubicTo(x - 97, 770, x - 70, 779, x - 48, 777)
    p.cubicTo(x - 26, 775, x - 16, 762, x, 762)
    p.cubicTo(x + 16, 762, x + 26, 775, x + 48, 777)
    p.cubicTo(x + 70, 779, x + 97, 770, x + 98, 738)
    p.cubicTo(x + 100, 690, x + 55, 668, x + 52, 610)
    p.lineTo(x + 50, Y_FEM); p.close()
    return p


def path_tibia_sup():
    x, h = X, HT; p = skia.Path()
    p.moveTo(x - 94, 804)
    p.cubicTo(x - 97, 790, x - 60, 786, x - 20, 790)
    p.cubicTo(x - 8, 792, x + 8, 792, x + 20, 790)
    p.cubicTo(x + 60, 786, x + 97, 790, x + 94, 804)
    p.cubicTo(x + 90, 842, x + h + 6, 858, x + h, 884)
    p.lineTo(x + h, P); p.lineTo(x - h, P); p.lineTo(x - h, 884)
    p.cubicTo(x - h - 6, 858, x - 90, 842, x - 94, 804)
    p.close()
    return p


def path_tibia_inf(y0, yb):
    x, h = X, HT; p = skia.Path()
    p.moveTo(x - h, y0); p.lineTo(x + h, y0); p.lineTo(x + h, yb - 130)
    p.cubicTo(x + h + 3, yb - 82, x + 62, yb - 52, x + 60, yb - 16)
    p.cubicTo(x + 57, yb + 2, x + 22, yb - 3, x - 8, yb - 2)
    p.cubicTo(x - 30, yb, x - 40, yb + 24, x - 54, yb + 26)
    p.cubicTo(x - 70, yb + 26, x - 74, yb - 8, x - 70, yb - 46)
    p.cubicTo(x - 66, yb - 92, x - h - 3, yb - 102, x - h, yb - 130)
    p.close()
    return p


def path_cunha(ang, f):
    """Gomo do lado convexo da dobra (deixa o osso dobrado contínuo, sem degrau)."""
    cx, cy, r = X + HT, P + f, 2 * HT
    p = skia.Path(); p.moveTo(cx, cy)
    p.arcTo(skia.Rect(cx - r, cy - r, cx + r, cy + r), 180 - ang, ang, False)
    p.close()
    return p


def sombra_osso():
    return skia.GradientShader.MakeLinear([skia.Point(X - 86, 0), skia.Point(X + 86, 0)],
                                          [C(OSSO_B), C(OSSO_C), C(OSSO_C), C(OSSO_B)], [0.0, 0.42, 0.58, 1.0])


def uniao(*ps):
    u = skia.Path(ps[0])
    for q in ps[1:]:
        u = skia.Op(u, q, skia.PathOp.kUnion_PathOp)
    return u


def mascara_topo(cv, y0, y1, rect):
    """Dissolve o topo no fundo (curva suave, sem degrau visível onde a máscara termina)."""
    m = skia.Paint(AntiAlias=True)
    alfas = (0, 10, 40, 92, 155, 210, 242, 255)
    m.setShader(skia.GradientShader.MakeLinear([skia.Point(0, y0), skia.Point(0, y1)],
                                               [skia.ColorSetARGB(a, 0, 0, 0) for a in alfas],
                                               [i / (len(alfas) - 1) for i in range(len(alfas))]))
    m.setBlendMode(skia.BlendMode.kDstIn)
    cv.drawRect(rect, m)


def vela_topo(cv, perto):
    """No zoom do corte o osso de cima sobe até a faixa do selo COMO FUNCIONA (y 150-204): o mundo se
    dissolve no fundo antes de chegar lá (máscara na TELA, proporcional ao zoom; o selo fica sempre)."""
    y0, y1, n = 214, 342, 8
    cores = [skia.ColorSetARGB(int(255 * (1 - perto)), 0, 0, 0)]; pos = [0.0]
    for i in range(n + 1):
        k = i / n
        cores.append(skia.ColorSetARGB(int(255 * (1 - perto * (1 - e_inout(k)))), 0, 0, 0))
        pos.append((y0 + (y1 - y0) * k) / y1)
    m = skia.Paint(AntiAlias=True)
    m.setShader(skia.GradientShader.MakeLinear([skia.Point(0, 0), skia.Point(0, y1)], cores, pos))
    m.setBlendMode(skia.BlendMode.kDstIn)
    cv.drawRect(skia.Rect(0, 0, W, y1 + 1), m)


def ossos(cv, t, T, ang, f):
    """Osso de cima (dissolve no topo) + osso de baixo (dobrado / cortado / cicatrizado)."""
    sh = sombra_osso()
    fem = path_femur()
    cam_fem = skia.Rect(X - 220, Y_FEM - 40, X + 220, 800)
    cv.saveLayer(cam_fem, None)
    cv.drawPath(fem, paint("#000000", 70, blur=14))
    cv.drawPath(fem, paint(OSSO_C, shader=sh))
    cv.drawPath(fem, paint(OSSO_L, 150, "stroke", 2.5))
    cv.drawRect(skia.Rect(X - 14, Y_FEM, X + 14, 690), paint(OSSO_B, 55, blur=6))     # canal (profundidade)
    mascara_topo(cv, Y_FEM, Y_FEM + 190, cam_fem)
    cv.restore()

    sup = path_tibia_sup()
    inf = path_tibia_inf(P + f, Y_BASE + f)
    m = girar(ang, f)
    inf_r = skia.Path(inf); inf_r.transform(m)
    baixo = uniao(inf_r, path_cunha(ang, f)) if ang > 0.05 else inf_r
    duro = e_inout(prog(t, T["alinhado"], T["alinhado"] + 1.0))
    dens = e_out(prog(t, T["cicatrizar"] - 0.05, T["cicatrizar"] + 0.4)) if f > 0.5 else 0.0
    banda = skia.Path(); banda.addRect(skia.Rect(X - HT, P - 0.5, X + HT, P + f + 0.5))

    todo = uniao(sup, baixo) if f <= 0.5 else None
    for pth in ((todo,) if todo is not None else (sup, baixo)):
        cv.drawPath(pth, paint("#000000", 70, blur=14))
        cv.drawPath(pth, paint(OSSO_C))          # base lisa: as emendas das peças não vazam o fundo
    cv.drawPath(sup, paint(OSSO_C, shader=sh))
    if ang > 0.05:
        cv.drawPath(path_cunha(ang, f), paint(OSSO_C, shader=sh))
    cv.save(); cv.concat(m); cv.drawPath(inf, paint(OSSO_C, shader=sh)); cv.restore()
    for y0, y1, mm in ((830, P, None), (P + f, Y_BASE + f - 140, m)):                  # canal medular
        cv.save()
        if mm is not None:
            cv.concat(mm)
        cv.drawRect(skia.Rect(X - 12, y0 + 10, X + 12, y1 - 6), paint(OSSO_B, 55, blur=6))
        cv.restore()

    # o vão do corte vira osso: dourado -> marfim
    if dens > 0:
        brilho = prog(t, T["alinhado"] - 0.1, T["alinhado"] + 0.25) * (1 - duro)
        cv.drawRect(skia.Rect(X - HT - 22, P - 16, X + HT + 22, P + f + 16),
                    paint(NOVO_G, int(dens * (60 + 110 * brilho) * (1 - duro)), blur=18))
        if duro > 0:                                             # marfim com a mesma sombra do osso
            cv.drawPath(banda, paint(OSSO_C, int(255 * dens * duro), shader=sh))
        cv.drawPath(banda, paint(NOVO, int(255 * dens * (1 - duro))))
    if todo is not None:
        cv.drawPath(todo, paint(OSSO_L, 150, "stroke", 2.5))
    else:
        if duro < 1:
            for pth in (sup, baixo):
                cv.drawPath(pth, paint(OSSO_L, int(150 * (1 - duro)), "stroke", 2.5))
        if duro > 0:
            cv.drawPath(uniao(sup, banda, baixo), paint(OSSO_L, int(150 * duro), "stroke", 2.5))

    # luz que percorre a perna no "Toda perna"
    k = prog(t, T["toda"], T["toda"] + 1.1)
    if 0 < k < 1:
        cv.save(); cv.clipPath(uniao(fem, sup, baixo), skia.ClipOp.kIntersect, True)
        y = lerp(Y_FEM - 80, Y_BASE + 120, e_inout(k))
        cv.drawRect(skia.Rect(X - 140, y - 70, X + 200, y + 70), paint("#FFFFFF", int(120 * math.sin(math.pi * k)), blur=26))
        cv.restore()
    return sup, baixo


def brilho_cicatriz(cv, t, T):
    """Um brilho dourado percorre a linha do corte (da esquerda para a direita) no "alinhado"."""
    k = prog(t, T["alinhado"] - 0.05, T["alinhado"] + 0.75)
    if not 0 < k < 1:
        return
    x = lerp(X - HT - 10, X + HT + 10, e_inout(k)); a = math.sin(math.pi * k)
    cv.drawCircle(x, P + FENDA / 2, 34, paint(NOVO_G, int(170 * a), blur=16))
    cv.drawCircle(x, P + FENDA / 2, 9, paint("#FFF4CF", int(255 * a), blur=3))


# ------------------------------------------------------------------ linhas: eixo, fantasma, corte
def tracejado_path(cv, pth, cor, alfa, larg, intervalos, fase=0.0, blur=0):
    if alfa <= 0:
        return
    p = paint(cor, int(alfa), "stroke", larg, blur=blur)
    p.setPathEffect(skia.DashPathEffect.Make(intervalos, fase))
    cv.drawPath(pth, p)


def linha_eixo(cv, t, T, ang, f):
    """Na capa a linha já está lá, fraca (a linha "invisível"); em "invisível" um traço aceso desce
    por cima dela; depois acompanha os dois ossos (dobra em "torta", endireita em "reposiciona")."""
    k = e_inout(prog(t, T["invisivel"], T["invisivel"] + 0.75))
    bounds = skia.Rect(X - 200, Y_L0 - 20, X + 260, Y_L1 + 40)
    fase = -t * 26
    cv.saveLayer(bounds, None)
    if k < 1:                                                    # fantasma reta, sem brilho nem ponta
        reta = skia.Path(); reta.moveTo(X, Y_L0); reta.lineTo(X, Y_L1)
        tracejado_path(cv, reta, ESCURO, 70, 10, [26, 14], fase)
        tracejado_path(cv, reta, OURO, 95, 5, [26, 14], fase)
    if t >= T["invisivel"]:
        y_cab = lerp(Y_L0, Y_L1, k)
        pth = skia.Path(); pth.moveTo(X, Y_L0); pth.lineTo(X, P)
        pth.lineTo(*gira_pt(ang, f, X, P + f)); pth.lineTo(*gira_pt(ang, f, X, Y_L1 + f))
        realce = max(prog(t, T["eixo"], T["eixo"] + 0.15) * (1 - prog(t, T["eixo"] + 0.6, T["eixo"] + 1.4)),
                     prog(t, T["certo"] - 0.05, T["certo"] + 0.2) * (1 - prog(t, T["certo"] + 0.6, T["certo"] + 1.4)))
        cv.save(); cv.clipRect(skia.Rect(0, Y_L0 - 20, W, y_cab))
        cv.drawPath(pth, paint(OURO, int(70 + 110 * realce), "stroke", 16 + 10 * realce, blur=10))
        tracejado_path(cv, pth, ESCURO, 190, 12, [26, 14], fase)
        tracejado_path(cv, pth, OURO, 255, 6.5, [26, 14], fase)
        cv.restore()
        if k < 1:                                                # a ponta que desenha a linha
            cv.drawCircle(X, y_cab, 16, paint(OURO, 150, blur=8)); cv.drawCircle(X, y_cab, 6, paint("#FFF4CF"))
    mascara_topo(cv, Y_L0 - 20, Y_L0 + 110, bounds)
    cv.restore()


def janela_medida(T):
    """A régua-guia pousa sobre o eixo e um brilho desce por ela (depois de pousar, antes de "onde")."""
    return T["mede"] + 0.3, T["mede"] + 0.98


def y_varredura(t, T):
    t0, t1 = janela_medida(T)
    return lerp(Y_RG0, Y_RG1, e_inout(prog(t, t0, t1)))


def linha_fantasma(cv, t, T, f):
    """O eixo desejado: linha branca, reta, que a varredura da régua deixa do ponto da dobra para baixo."""
    a = prog(t, T["mede"], T["mede"] + 0.2) * (1 - prog(t, T["alinhado"] - 0.2, T["alinhado"] + 0.4))
    if a <= 0:
        return
    t0, t1 = janela_medida(T)
    y_v = y_varredura(t, T) if t < t1 else Y_L1 + 60
    if y_v <= P:
        return
    cv.save(); cv.clipRect(skia.Rect(0, P - 2, W, y_v))
    cv.drawLine(X, P, X, Y_L1 + f, paint("#FFFFFF", int(80 * a), "stroke", 16, blur=8))
    cv.drawLine(X, P, X, Y_L1 + f, paint(ESCURO, int(170 * a), "stroke", 11))
    cv.drawLine(X, P, X, Y_L1 + f, paint("#FFFFFF", int(240 * a), "stroke", 4.5))
    cv.restore()


def tracejado_corte(cv, t, T):
    if T["corte"] <= t < T["corta"] + 0.1:                    # tracejado do corte planejado
        a = prog(t, T["corte"], T["planejado"])
        pisca = 0.5 + 0.5 * math.sin(t * 9)
        x = X - HT - 14
        while x < X + HT + 14:
            cv.drawLine(x, P, min(x + 15, X + HT + 14), P, paint(ESCURO, int(150 * a), "stroke", 10))
            cv.drawLine(x, P, min(x + 15, X + HT + 14), P, paint(VERMELHO, int(a * (130 + 125 * pisca)), "stroke", 5.5))
            x += 25
    k = t - (T["corta"] + 0.1)
    if 0 <= k < 1.0:
        a = 1 - k
        cv.drawLine(X - 120, P + 3, X + 120, P + 3, paint(VERMELHO, int(200 * a), "stroke", 16, blur=10))
        abre = e_out(clamp(k / 0.12))
        cv.drawLine(X - 100 * abre, P + 4, X + 100 * abre, P + 4, paint("#FFFFFF", int(255 * a), "stroke", 4))
        cv.drawCircle(X, P + 4, 110 * e_out(clamp(k / 0.25)), paint("#FFFFFF", int(130 * (1 - clamp(k / 0.3))), blur=28))


# ------------------------------------------------------------------ peso e setas
def bloco_peso(cv, y, a, sq):
    if a <= 0:
        return
    w, h = 152, 66
    cv.save(); cv.translate(X, y + h / 2); cv.scale(1 + 0.12 * sq, 1 - 0.16 * sq); cv.translate(0, -h / 2)
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(-w / 2 + 4, -h / 2 + 8, w / 2 + 4, h / 2 + 8), 16, 16),
                 paint("#000000", int(90 * a), blur=8))
    rr = skia.RRect.MakeRectXY(skia.Rect(-w / 2, -h / 2, w / 2, h / 2), 16, 16)
    cv.drawRRect(rr, paint(ESCURO, int(235 * a))); cv.drawRRect(rr, paint(OURO, int(255 * a), "stroke", 4))
    texto(cv, "PESO", 0, 14, F_BLACK, 38, "#FFFFFF", int(255 * a))
    cv.restore()


def estado_bloco(t, T, n):
    """-> (y do topo do bloco, alfa, achatamento) da n-ésima descida do bloco PESO."""
    if n == 1:
        t_in, t_cai = T["reparte"], T["peso"]
    else:
        t_in, t_cai = T["reorganizar"] - 0.1, T["reorganizar"] + 0.15
    t_pousa = pouso(T, n)
    if t < t_in or t > t_pousa + 0.45:
        return 0, 0.0, 0.0
    ent = e_out(prog(t, t_in, t_in + 0.3))
    q = prog(t, t_cai, t_pousa)
    y = lerp(418, Y_SPLIT - 68, q * q) - 26 * (1 - ent)
    sq = math.sin(math.pi * prog(t, t_pousa, t_pousa + 0.22)) if t >= t_pousa else 0.0
    a = ent * (1 - prog(t, t_pousa + 0.12, t_pousa + 0.4))
    return y, a, sq


def seta(cv, x, y0, y1, larg, cab, cor, a):
    """Seta reta para baixo, de (x, y0) com a ponta em (x, y1); contorno escuro para ler sobre o marfim."""
    if a <= 0 or y1 - y0 < 6:
        return
    def ponta(yp, L, lw, c, al):
        p = skia.Path(); p.moveTo(x, yp); p.lineTo(x - lw / 2, yp - L); p.lineTo(x + lw / 2, yp - L); p.close()
        cv.drawPath(p, paint(c, int(255 * al)))
    yc = y1 - cab * 0.6
    if yc > y0:
        cv.drawLine(x, y0, x, yc, paint(ESCURO, int(170 * a), "stroke", larg + 8))
    ponta(y1 + 5, cab + 9, cab * 1.15 + 12, ESCURO, a * 0.67)
    if yc > y0:
        cv.drawLine(x, y0, x, yc, paint(cor, int(255 * a), "stroke", larg))
    ponta(y1, cab, cab * 1.15, cor, a)


DX_SETA, Y_PONTA = 54, 770      # cada seta desce num lado do joelho e encosta na fresta


def setas(cv, t, T):
    l1, l2 = pouso(T, 1), pouso(T, 2)
    # 1ª vez: o bloco se divide em duas setas (uma de cada lado); em "carga" elas se fundem numa
    # seta grande só de um lado ("carga demais num lado")
    sep = e_out(prog(t, l1 + 0.08, l1 + 0.42))
    fim1 = 1 - prog(t, T["osteotomia"] - 0.2, T["osteotomia"] + 0.3)
    k = e_inout(prog(t, T["carga"], T["carga"] + 0.55))
    if sep > 0 and fim1 > 0:
        yb = lerp(Y_SPLIT - 10, Y_PONTA, sep)
        seta(cv, X + lerp(-DX_SETA * sep, DX_SETA, k), Y_SPLIT, yb, 10, 26, OURO, fim1 * (1 - k))
        seta(cv, X + DX_SETA * sep, lerp(Y_SPLIT, Y_SPLIT - 80, k), yb, lerp(10, 22, k), lerp(26, 48, k), OURO, fim1)
    # 2ª vez: o peso se reparte de novo, uma seta de cada lado
    sep2 = e_out(prog(t, l2 + 0.08, l2 + 0.42))
    fim2 = 1 - prog(t, T["manda"] - 0.45, T["manda"] - 0.15)
    if sep2 > 0 and fim2 > 0:
        for lado in (-1, 1):
            seta(cv, X + lado * DX_SETA * sep2, Y_SPLIT, lerp(Y_SPLIT - 10, Y_PONTA, sep2), 10, 26, OURO, fim2)


def joelho_vermelho(cv, t, T):
    a = prog(t, T["lado"] - 0.1, T["lado"] + 0.25) * (1 - prog(t, pouso(T, 2) + 0.1, T["carga2"] + 0.6))
    if a <= 0:
        return
    pulso = 0.82 + 0.18 * math.sin((t - T["lado"]) * 6.5)
    cx = X + 52
    cv.drawOval(skia.Rect(cx - 86, Y_JOELHO - 44, cx + 86, Y_JOELHO + 44), paint(VERMELHO, int(120 * a * pulso), blur=26))
    cv.drawOval(skia.Rect(cx - 48, Y_JOELHO - 8, cx + 48, Y_JOELHO + 8), paint(VERMELHO, int(240 * a)))
    cv.drawOval(skia.Rect(cx - 30, Y_JOELHO - 3, cx + 30, Y_JOELHO + 3), paint("#FFD3D4", int(160 * a * pulso)))


# ------------------------------------------------------------------ medir: régua, mira, ângulo
def alfa_regua(t, T):
    return prog(t, T["mede"] - 0.1, T["mede"] + 0.15) * (1 - prog(t, T["onde"] - 0.05, T["onde"] + 0.25))


def regua(cv, t, T):
    """Régua-guia: régua reta de alinhamento, SEM marcas, pousada sobre o eixo (não mede tamanho).
    O trecho de cima da linha corre dentro dela; o de baixo, torto, sai dela."""
    a = alfa_regua(t, T)
    if a <= 0:
        return
    xr = X - 300 * (1 - e_out(prog(t, T["mede"] - 0.1, T["mede"] + 0.3)))
    r = skia.Rect(xr - W_RG / 2, Y_RG0, xr + W_RG / 2, Y_RG1)
    cv.drawRRect(skia.RRect.MakeRectXY(r.makeOffset(5, 8), 9, 9), paint("#000000", int(60 * a), blur=8))
    rr = skia.RRect.MakeRectXY(r, 9, 9)
    cv.drawRRect(rr, paint("#FFFFFF", int(110 * a)))
    cv.drawRRect(rr, paint(ACO_ESC, int(255 * a), "stroke", 3))


def varredura(cv, t, T):
    """Brilho que desce AO LONGO da régua, por cima da linha; ao passar do ponto da dobra deixa a
    linha-fantasma (o eixo desejado)."""
    t0, t1 = janela_medida(T)
    k = prog(t, t0, t1)
    if not 0 < k < 1:
        return
    a = alfa_regua(t, T) * clamp(k * 8) * (1 - prog(k, 0.86, 1.0))
    ys = y_varredura(t, T)
    cv.drawCircle(X, ys, 34, paint(NOVO_G, int(150 * a), blur=14))
    cv.drawRect(skia.Rect(X - W_RG / 2 + 3, ys - 4, X + W_RG / 2 - 3, ys + 4), paint("#FFF4CF", int(235 * a)))
    cv.drawCircle(X, ys, 8, paint("#FFFFFF", int(255 * a), blur=2))


def mira(cv, t, T):
    a = prog(t, T["onde"], T["onde"] + 0.12) * (1 - prog(t, T["corta"] - 0.05, T["corta"] + 0.15))
    if a <= 0:
        return
    pop = e_back(prog(t, T["onde"], T["onde"] + 0.35))
    r = 40 * pop
    cv.save(); cv.translate(X, P); cv.rotate(70 * (1 - e_out(prog(t, T["onde"], T["onde"] + 0.5))))
    cv.drawCircle(0, 0, r, paint(ESCURO, int(170 * a), "stroke", 10))
    cv.drawCircle(0, 0, r, paint("#FFFFFF", int(255 * a), "stroke", 4.5))
    for k in range(4):
        ang = k * math.pi / 2; c, s = math.cos(ang), math.sin(ang)
        cv.drawLine(c * (r - 12), s * (r - 12), c * (r + 16), s * (r + 16), paint(ESCURO, int(170 * a), "stroke", 9))
        cv.drawLine(c * (r - 12), s * (r - 12), c * (r + 16), s * (r + 16), paint("#FFFFFF", int(255 * a), "stroke", 4))
    cv.drawCircle(0, 0, 6, paint(OURO, int(255 * a)))
    cv.restore()


R_ARCO = 250                    # longe do ponto da dobra: as duas linhas já se afastaram


def arco_quanto(cv, t, T, ang):
    a = prog(t, T["quanto"], T["quanto"] + 0.12) * (1 - prog(t, T["corta"] - 0.1, T["corta"] + 0.2))
    if a <= 0 or ang < 0.5:
        return
    var = ang * e_out(prog(t, T["quanto"], T["quanto"] + 0.45))
    r = R_ARCO; rect = skia.Rect(X - r, P - r, X + r, P + r)
    gomo = skia.Path(); gomo.moveTo(X, P); gomo.arcTo(rect, 90, -var, False); gomo.close()
    pulso = math.sin(math.pi * prog(t, T["quanto"], T["quanto"] + 0.6))   # o gomo (o "quanto") pulsa na palavra
    cv.drawPath(gomo, paint(NOVO_G, int((70 + 80 * pulso) * a), blur=10))
    cv.drawPath(gomo, paint(OURO, int((175 + 55 * pulso) * a)))
    arco = skia.Path(); arco.addArc(rect, 90, -var)
    cv.drawPath(arco, paint(ESCURO, int(190 * a), "stroke", 18))
    cv.drawPath(arco, paint(OURO, int(255 * a), "stroke", 10))
    for g in (90, 90 - var):                                   # tracinhos nas duas pontas do arco
        c, s = math.cos(math.radians(g)), math.sin(math.radians(g))
        cv.drawLine(X + c * (r - 22), P + s * (r - 22), X + c * (r + 22), P + s * (r + 22), paint(ESCURO, int(190 * a), "stroke", 11))
        cv.drawLine(X + c * (r - 20), P + s * (r - 20), X + c * (r + 20), P + s * (r + 20), paint(OURO, int(255 * a), "stroke", 5))


# ------------------------------------------------------------------ fixação
def abracadeiras(cv, t, T, f, metade):
    """Duas abraçadeiras de aço genéricas + barrinha que atravessa o corte (sem modelo de implante)."""
    ys = (P - 36, P + f + 40)
    for i, y in enumerate(ys):
        t0 = T["fixa"] + 0.14 * i
        a = clamp(prog(t, t0, t0 + 0.12))
        if a <= 0:
            continue
        k = e_back(prog(t, t0, t0 + 0.45)); dx = 220 * (1 - e_out(prog(t, t0, t0 + 0.4)))
        rx, ry = (HT + 12) * lerp(1.6, 1.0, k), 15
        r = skia.Rect(X + dx - rx, y - ry, X + dx + rx, y + ry)
        if metade == "tras":
            cv.drawArc(r, 180, 180, False, paint(ACO_ESC, int(255 * a), "stroke", 13))
            continue
        cv.drawArc(r, 0, 180, False, paint("#000000", int(80 * a), "stroke", 16, blur=5))
        cv.drawArc(r, 0, 180, False, paint(ACO, int(255 * a), "stroke", 13))
        cv.drawArc(skia.Rect(r.left() + 5, r.top() + 3, r.right() - 5, r.bottom() - 2), 25, 130, False,
                   paint(ACO_HL, int(190 * a), "stroke", 3))
    if metade == "frente":
        t0 = T["fixa"]
        a = clamp(prog(t, t0, t0 + 0.12))
        if a > 0:
            dx = 220 * (1 - e_out(prog(t, t0, t0 + 0.4)))
            xb = X + HT + 16 + dx
            cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(xb - 8 + 3, ys[0] - 26 + 5, xb + 8 + 3, ys[1] + 26 + 5), 7, 7),
                         paint("#000000", int(80 * a), blur=6))
            cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(xb - 8, ys[0] - 26, xb + 8, ys[1] + 26), 7, 7), paint(ACO, int(255 * a)))
            cv.drawLine(xb - 3, ys[0] - 20, xb - 3, ys[1] + 20, paint(ACO_HL, int(170 * a), "stroke", 2.5))
            for y in ys:
                cv.drawCircle(xb, y + 2, 7, paint(ACO_ESC, int(255 * a)))
                cv.drawCircle(xb - 1.5, y + 0.5, 2.5, paint(ACO_HL, int(220 * a)))


# ------------------------------------------------------------------ peças de tela (fora da câmera)
def etiqueta(cv, linhas, x, y, ancora, cor, a, tam=38):
    """Caixa de rótulo com linha fina até `ancora`. linhas = [(texto, cor_texto, k)], k = entrada da linha."""
    if a <= 0:
        return
    x += 24 * (1 - e_out(a))
    vis = [(s, c, k) for s, c, k in linhas if k > 0]
    larg = max(larg_texto(s, F_BLACK, tam) for s, _, _ in vis)
    passo = tam * 1.28
    alt = 18 + sum(passo * e_out(k) for _, _, k in vis)
    xa, ya = ancora
    cv.drawLine(xa, ya, x, y + alt / 2, paint(cor, int(210 * a), "stroke", 3))
    cv.drawCircle(xa, ya, 9, paint(ESCURO, int(200 * a)))
    cv.drawCircle(xa, ya, 6, paint(cor, int(255 * a)))
    rr = skia.RRect.MakeRectXY(skia.Rect(x, y, x + larg + 32, y + alt), 14, 14)
    cv.drawRRect(rr, paint(ESCURO, int(222 * a)))
    cv.drawRRect(rr, paint(cor, int(255 * a), "stroke", 3))
    yy = y + 9
    for s, c, k in vis:
        yy += passo * e_out(k)
        texto(cv, s, x + 16, yy - tam * 0.3, F_BLACK, tam, c, int(255 * a * clamp(k * 1.5)), centro=False)


def chip_topo(cv, s, a, y=300, tam=44, cor=OURO):
    """Título do momento, centrado no topo (área do gancho, depois que ele sai)."""
    if a <= 0:
        return
    lw = larg_texto(s, F_BLACK, tam)
    cv.save(); cv.translate(0, -16 * (1 - e_out(a)))
    rr = skia.RRect.MakeRectXY(skia.Rect(W / 2 - lw / 2 - 28, y - tam * 1.05, W / 2 + lw / 2 + 28, y + tam * 0.4), 18, 18)
    cv.drawRRect(rr, paint(ESCURO, int(225 * a))); cv.drawRRect(rr, paint(cor, int(255 * a), "stroke", 3))
    texto(cv, s, W / 2, y, F_BLACK, tam, cor, int(255 * a))
    cv.restore()


def medidor(cv, t, T):
    """Barrinha que esvazia aos poucos (gráfico, não tecido). Sai na troca de assunto, sem voltar a encher."""
    a = prog(t, T["desgastar"] - 0.05, T["desgastar"] + 0.3) * (1 - prog(t, T["osteotomia"] - 0.1, T["osteotomia"] + 0.35))
    if a <= 0:
        return
    x0, y0, w, h, n = X_COL + 4, 918, 340, 42, 10
    cv.save(); cv.translate(26 * (1 - e_out(a)), 0)
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(x0 - 8, y0 - 8, x0 + w + 8, y0 + h + 8), 14, 14), paint(ESCURO, int(222 * a)))
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(x0 - 8, y0 - 8, x0 + w + 8, y0 + h + 8), 14, 14), paint("#FFFFFF", int(150 * a), "stroke", 3))
    acesos = segmentos_acesos(t, T)
    nivel = acesos / n
    cor = lerpc(OURO, VERMELHO, 1 - nivel)
    sw = (w - (n - 1) * 6) / n
    for i in range(n):
        xs = x0 + i * (sw + 6)
        r = skia.RRect.MakeRectXY(skia.Rect(xs, y0, xs + sw, y0 + h), 6, 6)
        if i < acesos:
            cv.drawRRect(r, paint(cor, int(255 * a)))
        elif i < acesos + 1 and acesos < n:
            frac = segmentos_frac(t, T)
            cv.drawRRect(r, paint(cor, int(255 * a * frac)))
            cv.drawRRect(r, paint("#FFFFFF", int(30 * a)))
        else:
            cv.drawRRect(r, paint("#FFFFFF", int(30 * a)))
    k = prog(t, T["antes1"], T["antes1"] + 0.25)
    if k > 0:
        texto(cv, "ANTES DA HORA", x0 - 6, y0 - 26, F_BLACK, 40, "#FFFFFF", int(255 * a * k), centro=False, contorno=8)
    cv.restore()


def _nivel(t, T):
    """Segmentos acesos (contínuo): de 10 a 4 entre "desgastar" e "osteotomia"."""
    return lerp(10, 4, prog(t, T["desgastar"] + 0.35, T["caminho"]))


def segmentos_acesos(t, T):
    return int(math.floor(_nivel(t, T) + 1e-6))


def segmentos_frac(t, T):
    v = _nivel(t, T)
    return v - math.floor(v + 1e-6)


def titulo_osteotomia(cv, t, T):
    """"OSTEOTOMIA" cai no topo e se parte em duas fichas: cada metade da palavra encolhe e voa para
    a sua ficha (OSTEO = OSSO, TOMIA = CORTE), que acende em volta dela."""
    t0 = T["osteotomia"]
    fim = 1 - prog(t, T["antes2"], T["antes2"] + 0.4)
    if t < t0 - 0.05 or fim <= 0:
        return
    ts = t0 + 0.8                                                # instante em que se parte
    tam, y, tam2, y2 = 80, 318, 40, 316
    s = "OSTEOTOMIA"
    lw = larg_texto(s, F_BLACK, tam); x0 = W / 2 - lw / 2
    xm = x0 + larg_texto("OSTEO", F_BLACK, tam)
    k = e_inout(prog(t, ts, ts + 0.42))                          # viagem das metades
    troca = prog(t, ts + 0.4, ts + 0.52)                          # texto da ficha acende sobre a metade pousada
    some = prog(t, ts + 0.5, ts + 0.62)                           # ... e só então a metade sai
    fichas = ((282, "OSTEO = OSSO", x0, skia.Rect(0, 0, xm, H)), (798, "TOMIA = CORTE", xm, skia.Rect(xm, 0, W, H)))
    kb = prog(t, ts + 0.2, ts + 0.45)
    if kb > 0:                                                   # 1) as fichas (atrás das metades)
        for cxc, s2, _, _ in fichas:
            w2 = larg_texto(s2, F_BLACK, tam2)
            cv.save(); cv.translate(cxc, 301); e = lerp(0.85, 1.0, e_back(kb)); cv.scale(e, e)
            rr = skia.RRect.MakeRectXY(skia.Rect(-w2 / 2 - 24, -35, w2 / 2 + 24, 35), 18, 18)
            cv.drawRRect(rr, paint(ESCURO, int(230 * kb * fim))); cv.drawRRect(rr, paint(OURO, int(255 * kb * fim), "stroke", 3))
            cv.restore()
    if some < 1:                                                 # 2) a palavra / as metades viajando
        queda = e_back(prog(t, t0 - 0.05, t0 + 0.4))
        a = clamp(prog(t, t0 - 0.05, t0 + 0.1)) * (1 - some) * fim
        yy = lerp(y - 120, y, queda)
        cv.save(); cv.clipRect(skia.Rect(0, 214, W, H))             # nasce logo abaixo do selo, sem cruzá-lo
        for cxc, s2, xa, clip in fichas:
            xd = cxc - larg_texto(s2, F_BLACK, tam2) / 2          # onde a metade pousa dentro da ficha
            cv.save()
            cv.translate(lerp(xa, xd, k), lerp(yy, y2, k)); e = lerp(1.0, tam2 / tam, k); cv.scale(e, e)
            cv.translate(-xa, -y)
            cv.clipRect(clip)
            texto(cv, s, W / 2, y, F_BLACK, tam, OURO, int(255 * a), contorno=10)
            cv.restore()
        cv.restore()
        if t >= ts:                                              # o "corte" no meio da palavra
            kc = prog(t, ts, ts + 0.3)
            cv.drawLine(xm, y - tam * 0.9, xm, y + 14, paint("#FFFFFF", int(255 * (1 - kc)), "stroke", 4))
    if troca > 0:                                                # 3) o texto completo de cada ficha
        for cxc, s2, _, _ in fichas:
            texto(cv, s2, cxc, y2, F_BLACK, tam2, OURO, int(255 * troca * fim))


# ------------------------------------------------------------------ quadro
def mundo(cv, t, T):
    ang = angulo(t, T); f = fenda(t, T)
    abracadeiras(cv, t, T, f, "tras")
    ossos(cv, t, T, ang, f)
    brilho_cicatriz(cv, t, T)
    joelho_vermelho(cv, t, T)
    regua(cv, t, T)
    arco_quanto(cv, t, T, ang)
    linha_fantasma(cv, t, T, f)
    linha_eixo(cv, t, T, ang, f)
    varredura(cv, t, T)
    tracejado_corte(cv, t, T)
    abracadeiras(cv, t, T, f, "frente")
    mira(cv, t, T)
    for n in (1, 2):
        y, a, sq = estado_bloco(t, T, n)
        bloco_peso(cv, y, a, sq)
    setas(cv, t, T)
    brilhos(cv, X, P + 160, t, T["certo"] + 0.12, n=12, raio=170)
    brilhos(cv, X, P + 4, t, T["alinhado"] + 0.1, n=14, raio=180)
    brilhos(cv, X, Y_JOELHO, t, pouso(T, 2) + 0.15, n=12, raio=150)
    return ang


def quadro(cv, t, T, blocos, ep):
    fundo(cv, t)
    cam = camera(t, T)
    t_cta = T["manda"] - 0.15

    # ================= mundo (câmera); na CTA fica ao fundo, desfocado; no zoom o topo se dissolve
    desf = 7 * prog(t, t_cta, t_cta + 0.5)
    perto = zoom(t, T)
    if desf > 0.05:
        pb = skia.Paint(); pb.setImageFilter(skia.ImageFilters.Blur(desf, desf))
        cv.saveLayer(None, pb)
    elif perto > 0.001:
        cv.saveLayer(None, None)
    else:
        cv.save()
    cv.save()
    aplica(cv, cam)
    ang = mundo(cv, t, T)
    cv.restore()
    if perto > 0.001:
        vela_topo(cv, perto)
    cv.restore()

    # ================= tela: rótulos com ponteiro (coluna da direita)
    a = prog(t, T["invisivel"] + 0.15, T["invisivel"] + 0.4) * (1 - prog(t, T["reparte"] - 0.25, T["reparte"]))
    etiqueta(cv, [("LINHA INVISÍVEL", OURO, 1.0)], X_COL, 452, na_tela(cam, X, 498), OURO, a)
    # entra na palavra "reparte" e sai em "torta" (não fica escrito "reparte" sobre a perna dobrando)
    a = prog(t, T["reparte"] + 0.05, T["reparte"] + 0.3) * (1 - prog(t, T["torta"] - 0.05, T["torta"] + 0.2))
    etiqueta(cv, [("REPARTE O PESO", "#FFFFFF", 1.0)], X_COL, 636, na_tela(cam, X + 98, 745), OURO, a)
    a = prog(t, T["carga"] + 0.05, T["carga"] + 0.3) * (1 - prog(t, T["adulto"] - 0.1, T["adulto"] + 0.2))
    etiqueta(cv, [("CARGA DEMAIS", "#FFFFFF", 1.0), ("UM LADO", VERMELHO, prog(t, T["lado"], T["lado"] + 0.3))],
             X_COL, 700, na_tela(cam, X + 92, Y_JOELHO), VERMELHO, a)
    medidor(cv, t, T)
    a = prog(t, T["planejado"] - 0.1, T["planejado"] + 0.15) * (1 - prog(t, T["mede"] - 0.1, T["mede"] + 0.15))
    etiqueta(cv, [("CORTE PLANEJADO", "#FFFFFF", 1.0)], X_COL, 846, na_tela(cam, X + HT + 14, P), VERMELHO, a, tam=35)
    a = prog(t, T["onde"] + 0.05, T["onde"] + 0.25) * (1 - prog(t, T["corta"] - 0.1, T["corta"] + 0.15))
    etiqueta(cv, [("ONDE", "#FFFFFF", 1.0)], X_COL, 846, na_tela(cam, X + 28, P - 28), "#FFFFFF", a)
    g = math.radians(90 - ang / 2)                              # meio do gomo dourado (o "quanto")
    a = prog(t, T["quanto"] + 0.1, T["quanto"] + 0.3) * (1 - prog(t, T["corta"] - 0.1, T["corta"] + 0.15))
    etiqueta(cv, [("QUANTO", OURO, 1.0)], X_COL, 1066, na_tela(cam, X + math.cos(g) * R_ARCO * 0.6, P + math.sin(g) * R_ARCO * 0.6),
             OURO, a)
    a = prog(t, T["certo"] + 0.1, T["certo"] + 0.35) * (1 - prog(t, T["alinhado"] - 0.3, T["alinhado"]))
    etiqueta(cv, [("EIXO CERTO", OURO, 1.0)], X_COL, 975, na_tela(cam, X, P + 165), OURO, a)
    a = prog(t, T["alinhado"] + 0.15, T["alinhado"] + 0.4) * (1 - prog(t, T["reorganizar"], T["reorganizar"] + 0.3))
    etiqueta(cv, [("JÁ ALINHADO", OURO, 1.0)], X_COL, 770, na_tela(cam, X + 24, P + FENDA / 2), OURO, a)
    # eco da abertura: mesmo lugar e mesmo ponteiro de "REPARTE O PESO"; fica até a CTA
    a = prog(t, T["reorganizar"] + 0.3, T["reorganizar"] + 0.55) * (1 - prog(t, T["manda"] - 0.4, T["manda"] - 0.15))
    etiqueta(cv, [("REORGANIZAR", "#FFFFFF", 1.0), ("A CARGA", OURO, prog(t, T["carga2"], T["carga2"] + 0.3))],
             X_COL, 636, na_tela(cam, X + 98, 745), OURO, a)

    # ================= tela: calendário, títulos do topo, carimbos
    a = prog(t, T["adulto"], T["adulto"] + 0.3) * (1 - prog(t, T["osteotomia"] - 0.1, T["osteotomia"] + 0.3))
    if a > 0:
        cv.save(); cv.translate(X_COL + 26 + 30 * (1 - e_out(a)), 420); cv.scale(1.45, 1.45)
        calendario(cv, 0, 0, T["adulto"] + (t - T["adulto"]) * 0.55, T["adulto"], a)
        cv.restore()
    chip_topo(cv, "NO ADULTO", prog(t, T["adulto"], T["adulto"] + 0.3) * (1 - prog(t, T["sozinha"] - 0.2, T["sozinha"])))
    titulo_osteotomia(cv, t, T)
    chip_topo(cv, "MEDE O EIXO", prog(t, T["mede"], T["mede"] + 0.3) * (1 - prog(t, T["corta"] - 0.1, T["corta"] + 0.2)))

    carimbo(cv, "O EIXO", na_tela(cam, X + 24, 0)[0], 612, -7, T["eixo"], t, dur=1.6)
    # carimbos do topo entram no lugar do título do momento (a perna fica limpa)
    carimbo(cv, "NÃO SE AJEITA SOZINHA", 540, 312, -4, T["sozinha"] - 0.02, t,
            dur=T["osteotomia"] - T["sozinha"] - 0.15, tam=50)
    carimbo(cv, "FIXA", 664, 694, -6, T["fixa"] + 0.45, t, dur=1.4)
    carimbo(cv, "FUNÇÃO, NUNCA ESTÉTICA", 540, 312, -4, T["carga2"] + 0.43, t,
            dur=T["manda"] - T["carga2"] - 0.65, tam=50)

    # ================= interface
    capa(cv, t, T["eixo"] + 0.2, ep["gancho"][0], ep["gancho"][1])
    selo_como_funciona(cv, prog(t, T["eixo"] + 0.5, T["eixo"] + 0.9) * (1 - prog(t, T["manda"] - 0.3, T["manda"])))
    interface(cv, t, T, blocos, DESTAQUE)


# ------------------------------------------------------------------ som e prévias
def sons(T):
    l1, l2 = pouso(T, 1), pouso(T, 2)
    ev = [(T["toda"], "whoosh", 0.3), (T["invisivel"], "shimmer", 0.6), (T["eixo"] - 0.02, "thump", 0.85),
          (T["reparte"], "pop", 0.4), (T["peso"], "whoosh", 0.4), (l1, "thump", 0.6), (l1 + 0.12, "pop", 0.55),
          (T["torta"], "whoosh", 0.35), (T["carga"], "pop", 0.5), (T["lado"], "thump", 0.55),
          (T["antes1"], "pop", 0.4), (T["adulto"], "whoosh", 0.35), (T["sozinha"] - 0.02, "thump", 0.8),
          (T["osteotomia"], "whoosh", 0.45), (T["osteotomia"] + 0.3, "thump", 0.5), (T["osteotomia"] + 0.8, "tick", 0.7),
          (T["corte"], "tick", 0.5), (T["mede"], "whoosh", 0.4), (T["onde"], "ping", 0.6),
          (T["quanto"], "shimmer", 0.5), (T["corta"] + 0.08, "tick", 1.0), (T["reposiciona"], "whoosh", 0.4),
          (T["certo"] + 0.15, "ding", 0.6), (T["fixa"], "whoosh", 0.35), (T["fixa"] + 0.3, "ping", 0.6),
          (T["fixa"] + 0.44, "ping", 0.6), (T["fixa"] + 0.43, "thump", 0.75), (T["cicatrizar"], "shimmer", 0.45),
          (T["alinhado"] + 0.05, "shimmer", 0.8), (T["alinhado"] + 0.6, "crackle", 0.7),
          (T["reorganizar"], "whoosh", 0.4), (l2, "thump", 0.55), (l2 + 0.12, "pop", 0.5),
          (T["carga2"] + 0.41, "thump", 0.8), (T["manda"] + 0.05, "whoosh", 0.5)]
    # medidor: um clique a cada segmento que apaga
    ev += [(lerp(T["desgastar"] + 0.35, T["caminho"], i / 6), "click", 0.4) for i in range(1, 7)]
    # calendário virando folhas
    ev += [(T["adulto"] + 0.2 + 0.36 * i, "tick", 0.3) for i in range(int((T["osteotomia"] - T["adulto"] - 0.4) / 0.36))]
    # régua medindo; o osso girando de volta ao eixo
    t0, t1 = janela_medida(T)
    ev += [(lerp(t0, t1, i / 5), "click", 0.45) for i in range(6)]
    ev += [(lerp(T["reposiciona"] + 0.1, T["certo"] + 0.1, i / 6), "click", 0.5) for i in range(7)]
    return ev


def tempos_previa(T):
    return [0.0, T["invisivel"] + 0.7, pouso(T, 1) + 0.5, T["hora"] + 0.3, T["sozinha"] + 0.45,
            T["osteotomia"] + 1.3, T["mede"] + 0.8, T["quanto"] + 0.45, T["fixa"] + 0.7, T["alinhado"] + 0.6,
            T["carga2"] + 0.9, T["manda"] + 1.4]


# respiro maior antes da CTA: "FUNÇÃO, NUNCA ESTÉTICA" precisa de ~2 s de leitura depois da última palavra
render = fazer_render(quadro, ANCORAS, sons, tempos_previa, respiro_cta=2.4)
