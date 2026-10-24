# -*- coding: utf-8 -*-
"""COMO FUNCIONA — a retirada do fixador ("COMO SE TIRA / ESSA GAIOLA?").

Mesmo estilo e mesmas peças das cenas aprovadas (cf_alongamento: osso marfim, osso novo dourado,
anel/haste/porca do fixador, brilhos, fundo; cf_fixador_circular: perna com pinos curtos do anel até
o osso; cf_quanto_tempo: os anéis sobem e somem, seta de peso, relógio sem número, ampulheta).
Cada acontecimento é disparado pela palavra falada (ANCORAS):
  * capa (t=0): gancho no alto, a perna com a tíbia marfim e a faixa dourada de osso novo no meio,
    3 anéis com hastes e porcas, 6 pinos curtos do anel até o osso (sem fio cruzando, sem oliva) e
    um pontinho em tom de pele onde cada pino cruza a linha da pele. A 1ª coisa que se mexe é a
    própria gaiola, pulsando em ouro; "gaiola": os anéis brilham em sequência (metal) e a câmera
    abre espaço à direita para o rótulo FIXADOR EXTERNO;
  * "casa": uma casinha de traço simples entra ao lado da perna; "não": o carimbo NÃO SE FAZ EM
    CASA cai SOBRE A CASINHA (nunca sobre a perna); "procedimento": sob o fixador, a pílula
    PROCEDIMENTO DA EQUIPE; "equipe": a casinha sai, entra o ícone da equipe (bustos simples: sem
    mão, sem instrumento, sem mesa, sem paciente deitado) e um reflexo corre pelos 3 anéis;
  * "geral"/"rápido": reloginho sem número; o ponteiro faz um arco curto e para (EM GERAL É
    RÁPIDO) e os anéis dão um pulso dourado no ding; "muitas"/"sedação": a pílula MUITAS VEZES COM
    SEDAÇÃO LEVE (nada de máscara, soro, maca ou centro cirúrgico);
  * "aparelho": os pinos ESMAECEM NO LUGAR (não se movem, não deslizam pela pele); "sai": anéis e
    hastes sobem um pouco e somem (o recurso aprovado no cf_quanto_tempo), carimbo APARELHO SAI.
    Nenhum pino saindo da pele, nenhum close, nenhum sangue, nenhuma desmontagem;
  * "furos": na vista geral (sem zoom) ficam só os pontinhos na linha da pele (FUROS DOS PINOS);
    "cicatrizam": eles encolhem e fecham um a um até virar pele lisa (CICATRIZAM COM O TEMPO) —
    sem contador, sem dia, sem prazo;
  * "osso"/"novo"/"frágil"/"maduro": a câmera chega um pouco mais perto; a faixa dourada (OSSO
    NOVO, MAIS FRÁGIL) tem trama CLARA e RALA, o marfim (OSSO MADURO) é denso; os dois sempre
    opacos, sem rachadura, sem quebra, sem osso translúcido;
  * "ganhando"/"meses": a barra horizontal GANHANDO RESISTÊNCIA enche devagar e, no mesmo passo, a
    trama do dourado adensa e o dourado caminha para o marfim (sem chegar lá — código do piloto);
    POR MESES vai na ponta da barra, que não chega ao fim;
  * "carga"/"poucos": o osso recua; escada em UMA silhueta que sai pela borda direita (sem topo no
    quadro, sem número, sem rótulo de etapa); a seta de peso pousa no 1º degrau e sobe um degrau
    por vez (CARGA VOLTA AOS POUCOS) e PARA antes de "impacto";
  * "impacto"/"torção"/"esperam"/"liberação": cartão de uma linha IMPACTO E TORÇÃO com a bolinha
    quicando e a seta curva de giro; no lugar do check, uma ampulheta; "esperam": abre ESPERAM A
    LIBERAÇÃO e a ampulheta vira; a areia escorre a partir de "liberação";
  * "reta"/"final"/"chegada": corte para uma pista em perspectiva; o marcador (osso marfim com a
    faixa dourada) avança e para ao lado da bandeira RETA FINAL; mais à frente a LINHA DE CHEGADA
    tracejada, não alcançada (sem confete, sem troféu); respiro: a pista recua como resumo, com o
    trecho que falta pulsando; CTA padrão com o aviãozinho.
Nenhum exame de imagem simulado, nenhum implante de modelo comercial, nenhum número na tela. Todo
texto desenhado está em ep["tela"] (o render recusa o vídeo se não estiver). Cena PRESA ao roteiro
pelas palavras-âncora: roteiro sem elas = KeyError, não vídeo torto.
"""
import math

import skia

from .cf_alongamento import (ACO_ESC, ACO_HL, CX, F_BLACK, F_SEMI, HASTE, NOVO_G, OSSO_B, OSSO_C, OSSO_L, OURO,
                             PELE, RX, RY, VERMELHO, W, Y_BASE, Y_TOPO, C, anel, brilhos, clamp, desenha_regenerado,
                             e_back, e_in_back, e_inout, e_out, fundo, haste, larg_texto, lerp, lerpc, paint,
                             path_osso_inf, path_osso_sup, porca, prog, sombra_osso, texto)
from .cf_comum import capa, fazer_render, interface, selo_como_funciona

# ------------------------------------------------------------------ sincronia com a fala
ANCORAS = {
    "gaiola": ("gaiola", 1, False), "casa": ("casa", 1, False), "nao": ("não", 1, False),
    "procedimento": ("procedimento", 1, False), "equipe": ("equipe", 1, False), "geral": ("geral", 1, False),
    "rapido": ("rápido", 1, False), "muitas": ("muitas", 1, False), "sedacao": ("sedação", 1, False),
    "aparelho": ("aparelho", 1, False), "sai": ("sai", 1, False), "furos": ("furos", 1, False),
    "pinos": ("pinos", 1, False), "cicatrizam": ("cicatrizam", 1, False), "tempo": ("tempo", 1, False),
    "mas": ("mas", 1, False), "osso": ("osso", 1, False), "novo": ("novo", 1, False), "fragil": ("frágil", 1, False),
    "maduro": ("maduro", 1, False), "ganhando": ("ganhando", 1, False), "resistencia": ("resistência", 1, False),
    "meses": ("meses", 1, False), "carga": ("carga", 1, False), "poucos": ("poucos", 1, False),
    "impacto": ("impacto", 1, False), "torcao": ("torção", 1, False), "esperam": ("esperam", 1, False),
    "liberacao": ("liberação", 1, False), "reta": ("reta", 1, False), "final": ("final", 1, False),
    "ainda": ("ainda", 1, False), "linha": ("linha", 1, False), "chegada": ("chegada", 1, False),
    "manda": ("manda", 1, False),
}
DESTAQUE = {"gaiola", "casa", "equipe", "rápido", "sedação", "sai", "furos", "cicatrizam", "novo", "frágil",
            "resistência", "meses", "carga", "poucos", "impacto", "torção", "liberação", "final", "chegada",
            "encerra"}

# ------------------------------------------------------------------ textos de tela (todos em ep["tela"])
T_FIX = "FIXADOR EXTERNO"
T_CASA = "NÃO SE FAZ EM CASA"
T_EQUIPE = "PROCEDIMENTO DA EQUIPE"
T_RAPIDO = "EM GERAL É RÁPIDO"
T_SEDACAO = "MUITAS VEZES COM SEDAÇÃO LEVE"
T_SAI = "APARELHO SAI"
T_FUROS = "FUROS DOS PINOS"
T_CICATRIZ = "CICATRIZAM COM O TEMPO"
T_NOVO, T_FRAGIL, T_MADURO = "OSSO NOVO", "MAIS FRÁGIL", "OSSO MADURO"
T_RESIST, T_MESES = "GANHANDO RESISTÊNCIA", "POR MESES"
T_CARGA = "CARGA VOLTA AOS POUCOS"
T_IMPACTO, T_ESPERAM = "IMPACTO E TORÇÃO", "ESPERAM A LIBERAÇÃO"
T_RETA, T_CHEGADA = "RETA FINAL", "LINHA DE CHEGADA"

AZUL = "#9CC9FF"
CARTAO = "#0B1824"
CORAL = "#FFB08A"
TEAL = "#5FC4B6"
PELE_FURO, PELE_ESC = "#E3A186", "#B9735A"

# ------------------------------------------------------------------ geometria (mundo)
Y_AN = (415, 650, 1000)                      # 3 anéis (mesmo anel do piloto: RX x RY)
B0, B1 = 738, 842                            # a faixa de osso novo (regenerado), entre o 2º e o 3º anel
X_HASTE = 204
FOCO = 740


def _perna_path():
    """Contorno de perna do piloto, um pouco mais fino na panturrilha: o anel fica por fora da pele com
    folga e cada pino cruza a linha da pele longe da presilha (o ponto da pele não encosta no anel)."""
    L = Y_BASE - (Y_TOPO - 50)

    def y(f):
        return Y_TOPO - 50 + L * f
    p = skia.Path()
    p.moveTo(CX - 148, y(0.0))
    p.cubicTo(CX - 160, y(0.10), CX - 180, y(0.22), CX - 176, y(0.36))
    p.cubicTo(CX - 172, y(0.52), CX - 134, y(0.66), CX - 110, y(0.80))
    p.cubicTo(CX - 100, y(0.88), CX - 110, y(0.96), CX - 100, y(1.04))
    p.lineTo(CX + 106, y(1.04))
    p.cubicTo(CX + 110, y(0.95), CX + 104, y(0.88), CX + 110, y(0.80))
    p.cubicTo(CX + 128, y(0.64), CX + 162, y(0.50), CX + 158, y(0.34))
    p.cubicTo(CX + 154, y(0.20), CX + 146, y(0.08), CX + 138, y(0.0))
    p.close()
    return p


PERNA = _perna_path()
OSSO = skia.Op(path_osso_sup(Y_TOPO, 800), path_osso_inf(780, Y_BASE), skia.PathOp.kUnion_PathOp)


def _borda(path, y, lado, limite=320):
    """x da borda de `path` na altura y, do lado (-1 esq., +1 dir.), varrendo a partir do eixo.
    (cópia do cf_fixador_circular)"""
    ult = 0
    for d in range(0, limite):
        if path.contains(CX + lado * d, y):
            ult = d
    return CX + lado * ult


def _pinos():
    """6 pinos curtos (2 por anel): do anel (frente, lateral) até a superfície do osso.
    -> [(anel, (x0, y0) no anel, (x1, y1) no osso, (xp, yp) onde cruza a pele)]."""
    out = []
    angs = ((163, 17), (166, 14), (160, 20))
    for r, y in enumerate(Y_AN):
        for k, lado in enumerate((-1, 1)):
            a = math.radians(angs[r][k])
            x0, y0 = CX + RX * math.cos(a) - lado * 6, y + RY * math.sin(a) - 2
            y1 = y + 6 + (3 if lado > 0 else -3)
            x1 = _borda(OSSO, y1, lado) - lado * 2
            u = 0.5
            for j in range(1, 400):
                uu = j / 400
                if PERNA.contains(lerp(x0, x1, uu), lerp(y0, y1, uu)):
                    u = uu; break
            out.append((r, (x0, y0), (x1, y1), (lerp(x0, x1, u), lerp(y0, y1, u))))
    return out


PINOS = _pinos()

# ------------------------------------------------------------------ câmera
K0 = (CX, FOCO, 540, 800, 0.90)              # capa: perna inteira, centrada, abaixo do gancho
K1 = (CX, FOCO, 322, 762, 0.80)              # perna à esquerda: coluna da direita livre
K2 = (CX, 790, 330, 728, 1.50)               # um pouco mais perto do osso novo


def camera(t, T):
    cur = K0
    for t0, t1, k in ((T["gaiola"] - 0.05, T["gaiola"] + 0.75, K1), (T["mas"] - 0.05, T["novo"] + 0.2, K2)):
        a = e_inout(prog(t, t0, t1))
        if a > 0:
            cur = tuple(lerp(c, d, a) for c, d in zip(cur, k))
    tremor = 0.0
    for t0, forca in ((T["nao"] + 0.02, 6),):
        k = t - t0
        if 0 <= k < 0.35:
            tremor += forca * math.sin(k * 70) * (1 - k / 0.35)
    fx, fy, sx, sy, s = cur
    return fx, fy, sx + tremor, sy, s


def na_tela(cam, x, y):
    fx, fy, sx, sy, s = cam
    return sx + (x - fx) * s, sy + (y - fy) * s


# ------------------------------------------------------------------ tempo -> estado
def a_pinos(t, T):
    """Os pinos esmaecem NO LUGAR (sem se mover) logo depois de 'aparelho'."""
    return 1 - prog(t, T["aparelho"] - 0.02, T["aparelho"] + 0.42)


def saida_fix(t, T):
    """Anéis e hastes sobem um pouco e somem (como no cf_quanto_tempo) em 'sai'."""
    k = prog(t, T["sai"] - 0.05, T["sai"] + 0.6)
    return -70 * e_inout(k), 1 - prog(t, T["sai"] + 0.12, T["sai"] + 0.6)


ORDEM_FURO = (0, 1, 2, 3, 4, 5)


def fecha_furo(i, t, T):
    t0 = T["cicatrizam"] + 0.05 + 0.15 * ORDEM_FURO[i]
    return e_inout(prog(t, t0, t0 + 0.55)), t0


def enche_barra(t, T):
    """Barra GANHANDO RESISTÊNCIA: enche devagar e NÃO chega ao fim dentro do vídeo."""
    return 0.62 * prog(t, T["ganhando"] + 0.15, T["carga"] + 0.3) ** 0.85


def densidade_ouro(t, T):
    return clamp(enche_barra(t, T) / 0.55)


def recua(t, T):
    """'carga': o osso recua (encolhe e some, sempre opaco até virar um pontinho)."""
    return prog(t, T["carga"] - 0.3, T["carga"] + 0.12)


def t_corte_pista(T):
    return T["reta"] - 0.28


N_DEG = 8                                    # a escada SAI pela borda direita: nunca há topo no quadro
DEG_X0, DEG_BASE, DEG_RUN, DEG_RISE = 150, 1150, 128, 62
DEG_FADE0, DEG_FADE1, DEG_ALFA_FIM = DEG_X0 + 4 * DEG_RUN, W, 0.4   # do 5º degrau à borda: 1 -> 0,4


def acesos(T):
    """Instante em que cada degrau acende (de baixo para cima). O último acende ANTES de 'impacto':
    durante 'impacto e torção esperam a liberação' a seta fica PARADA."""
    return (T["carga"] + 0.45, T["poucos"] + 0.1, T["poucos"] + 0.6)


# ------------------------------------------------------------------ peças de desenho (utilidades)
def caixa(cv, x0, y0, x1, y1, cor, a, r=16, fundo_a=225, borda=3):
    rr = skia.RRect.MakeRectXY(skia.Rect(x0, y0, x1, y1), r, r)
    cv.drawRRect(rr, paint(CARTAO, int(fundo_a * a)))
    cv.drawRRect(rr, paint(cor, int(255 * a), "stroke", borda))


def pilula(cv, s, x, y, tam, cor, a, esc=1.0, cor_txt=None, dy=0.0):
    """Chip centrado em x; y = linha de base do texto. (cópia do cf_quanto_tempo)"""
    if a <= 0:
        return
    lw = larg_texto(s, F_BLACK, tam)
    cv.save(); cv.translate(x, y + dy); cv.scale(esc, esc)
    caixa(cv, -lw / 2 - 24, -tam * 1.04, lw / 2 + 24, tam * 0.38, cor, a, r=tam * 0.62)
    texto(cv, s, 0, 0, F_BLACK, tam, cor_txt or cor, int(255 * a))
    cv.restore()


def etiqueta(cv, linhas, x, y, ancora, cor, a, cresce=1.0):
    """Caixa com 1 ou 2 linhas (canto sup. esq. em x, y) e linha fina até `ancora` com ponto.
    linhas = [(texto, fonte, tamanho, cor)]; `cresce` abre a 2ª linha. (cópia do cf_fixador_circular)"""
    if a <= 0:
        return
    x += 26 * (1 - e_out(a))
    vis = linhas[:1] + (linhas[1:] if cresce > 0 else [])
    larg = max(larg_texto(s, f, tam) for s, f, tam, _ in vis)
    larg = lerp(larg_texto(*linhas[0][:3]), larg, cresce) if len(vis) > 1 else larg
    alt = linhas[0][2] * 1.22 + sum(tam * 1.22 for _, _, tam, _ in linhas[1:]) * cresce + 22
    xa, ya = ancora
    ym = y + min(alt / 2, linhas[0][2] * 0.8 + 11)
    cv.drawLine(xa, ya, x, ym, paint(CARTAO, int(150 * a), "stroke", 6))
    cv.drawLine(xa, ya, x, ym, paint(cor, int(220 * a), "stroke", 3))
    cv.drawCircle(xa, ya, 8.5, paint(CARTAO, int(200 * a)))
    cv.drawCircle(xa, ya, 7, paint(cor, int(255 * a)))
    rr = skia.RRect.MakeRectXY(skia.Rect(x, y, x + larg + 34, y + alt), 14, 14)
    cv.drawRRect(rr, paint(CARTAO, int(225 * a)))
    cv.drawRRect(rr, paint(cor, int(255 * a), "stroke", 2.5))
    yy = y + 11
    for k, (s, f, tam, c) in enumerate(vis):
        aa = a if k == 0 else a * clamp((cresce - 0.35) / 0.65)
        yy += tam * 1.22 * (1 if k == 0 else cresce)
        if aa > 0:
            texto(cv, s, x + 17, yy - tam * 0.26, f, tam, c, int(255 * aa), centro=False)


def carimbo_cor(cv, s, x, y, rot, t0, t, dur, tam=44, cor=VERMELHO, esc0=1.3, saida=0.3):
    """Carimbo do piloto com cor, tamanho e 'pancada' ajustáveis: entra menor que o do piloto para
    não passar, nem por um quadro, por cima da perna. `saida`: duração do esmaecer final."""
    k = t - t0
    if k < 0 or k > dur:
        return
    esc = lerp(esc0, 1.0, e_out(clamp(k / 0.16))); a = clamp(k / 0.08) * (1 - prog(k, dur - saida, dur))
    cv.save(); cv.translate(x, y); cv.rotate(rot); cv.scale(esc, esc)
    f = skia.Font(F_BLACK, tam); lw = f.measureText(s)
    rr = skia.RRect.MakeRectXY(skia.Rect(-lw / 2 - 22, -tam, lw / 2 + 22, tam * 0.38), 12, 12)
    cv.drawRRect(rr, paint(CARTAO, int(215 * a))); cv.drawRRect(rr, paint(cor, int(255 * a), "stroke", 6))
    cv.drawString(s, -lw / 2, 0, f, paint(cor, int(255 * a)))
    cv.restore()


def hachura(cv, x0, y0, x1, y1, passo, cor, alfa, larg, sentido=1, fase=0.0):
    """Linhas diagonais paralelas dentro do retângulo (o clip fica com quem chama)."""
    if alfa <= 0:
        return
    alt = y1 - y0
    x = x0 - alt + fase
    p = paint(cor, int(alfa), "stroke", larg)
    while x < x1 + alt:
        if sentido > 0:
            cv.drawLine(x, y1, x + alt, y0, p)
        else:
            cv.drawLine(x, y0, x + alt, y1, p)
        x += passo


def tracejado(cv, x0, y0, x1, y1, cor, a, larg=5, traco=18, vazio=12, fase=0.0):
    if a <= 0:
        return
    p = paint(cor, int(255 * a), "stroke", larg)
    p.setPathEffect(skia.DashPathEffect.Make([traco, vazio], fase))
    cv.drawLine(x0, y0, x1, y1, p)


# ------------------------------------------------------------------ mundo: perna, osso, fixador
def desenha_perna(cv, alfa):
    """Pele translúcida com o contorno (mesmo desenho do piloto; topo dissolve no fundo)."""
    if alfa <= 0:
        return
    y0, y1 = Y_TOPO - 50, Y_TOPO - 50 + (Y_BASE - (Y_TOPO - 50)) * 1.04
    sh = skia.GradientShader.MakeLinear([skia.Point(CX - 190, 0), skia.Point(CX + 170, 0)],
                                        [C(PELE, int(85 * alfa)), C(PELE, int(25 * alfa)), C(PELE, int(70 * alfa))],
                                        [0.0, 0.5, 1.0])
    cv.saveLayer(skia.Rect(0, y0 - 40, W, y1 + 40), None)
    cv.drawPath(PERNA, paint(PELE, 255, shader=sh))
    cv.drawPath(PERNA, paint(PELE, int(70 * alfa), "stroke", 14, blur=10))
    cv.drawPath(PERNA, paint(PELE, int(190 * alfa), "stroke", 3))
    masc = skia.Paint(AntiAlias=True)
    L = y1 - y0
    masc.setShader(skia.GradientShader.MakeLinear([skia.Point(0, y0), skia.Point(0, y1)],
                                                  [skia.ColorSetARGB(0, 0, 0, 0), skia.ColorSetARGB(255, 0, 0, 0),
                                                   skia.ColorSetARGB(255, 0, 0, 0), skia.ColorSetARGB(0, 0, 0, 0)],
                                                  [0.0, 120 / L, 1 - 70 / L, 1.0]))
    masc.setBlendMode(skia.BlendMode.kDstIn)
    cv.drawRect(skia.Rect(0, y0 - 40, W, y1 + 40), masc)
    cv.restore()


def osso(cv, t, T):
    """Tíbia marfim (densa) com a faixa dourada de osso novo (hachura rala que adensa); sempre opacos."""
    cv.drawPath(OSSO, paint("#000000", 70, blur=14))
    cv.drawPath(OSSO, paint(OSSO_C, shader=sombra_osso()))
    # o marfim é denso: trama fina e cerrada, no tom do próprio osso (aparece quando a câmera chega perto)
    h_m = prog(t, T["osso"] - 0.1, T["novo"] + 0.4)
    if h_m > 0:
        cv.save(); cv.clipPath(OSSO, skia.ClipOp.kIntersect, True)
        for sentido in (1, -1):
            hachura(cv, CX - 140, Y_TOPO - 20, CX + 140, Y_BASE + 50, 9, OSSO_B, 95 * h_m, 1.6, sentido)
        cv.restore()
    cv.drawPath(OSSO, paint(OSSO_L, 150, "stroke", 2.5))
    cv.drawRect(skia.Rect(CX - 16, Y_TOPO + 250, CX + 16, B0 - 6), paint(OSSO_B, 60, blur=6))
    cv.drawRect(skia.Rect(CX - 16, B1 + 6, CX + 16, Y_BASE - 190), paint(OSSO_B, 60, blur=6))

    # osso novo: o dourado caminha para o marfim no passo da barra (código do piloto: endurecer = ouro
    # virando marfim), sem chegar lá; a trama é CLARA (tom do marfim), nunca risco escuro (não lê como
    # trinca): rala no começo, adensa enquanto ganha resistência
    d = densidade_ouro(t, T)
    brilho = max(0.0, 1 - abs(t - (T["novo"] + 0.25)) / 0.6)
    desenha_regenerado(cv, B0, B1, 1.0, max(0.18, brilho), 0.5 * d, t)
    x0, x1 = CX - HASTE / 2 + 2, CX + HASTE / 2 - 2
    cv.save(); cv.clipRect(skia.Rect(x0, B0, x1, B1))
    cor = OSSO_C
    hachura(cv, x0, B0, x1, B1, 46, cor, 170, 2.4, 1)                         # rala
    hachura(cv, x0, B0, x1, B1, 46, cor, 170 * clamp(d / 0.45), 2.4, -1)      # adensa no passo da barra
    hachura(cv, x0, B0, x1, B1, 46, cor, 170 * clamp((d - 0.45) / 0.45), 2.4, 1, fase=23)
    hachura(cv, x0, B0, x1, B1, 46, cor, 170 * clamp((d - 0.7) / 0.3), 2.4, -1, fase=23)
    cv.restore()
    a_borda = prog(t, T["novo"] - 0.1, T["novo"] + 0.2) * (1 - prog(t, T["carga"] - 0.3, T["carga"]))
    if a_borda > 0:
        for y in (B0, B1):
            cv.drawLine(x0 - 4, y, x1 + 4, y, paint(OURO, int(230 * a_borda), "stroke", 3))


def pino(cv, p0, p1, a):
    """Pino curto do anel até o osso, com a presilha no anel. (cópia do cf_fixador_circular)"""
    if a <= 0:
        return
    cv.drawLine(p0[0], p0[1], p1[0], p1[1], paint("#000000", int(80 * a), "stroke", 13, blur=4))
    cv.drawLine(p0[0], p0[1], p1[0], p1[1], paint("#C6D3DF", int(255 * a), "stroke", 9))
    cv.drawLine(p0[0], p0[1] - 2, p1[0], p1[1] - 2, paint(ACO_HL, int(190 * a), "stroke", 2.5))
    cv.drawCircle(p1[0], p1[1], 5.5, paint(ACO_ESC, int(255 * a)))
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(p0[0] - 12, p0[1] - 11, p0[0] + 12, p0[1] + 11), 5, 5),
                 paint(ACO_ESC, int(255 * a)))
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(p0[0] - 8, p0[1] - 7, p0[0] + 8, p0[1] - 1), 3, 3),
                 paint(ACO_HL, int(160 * a)))


def ponto_pele(cv, x, y, t, T, i):
    """O pontinho em tom de pele onde o pino cruza a linha da pele: com o pino, um anel de pele em volta
    dele; sem o pino, o furo (tom de pele mais escuro, nada de vermelho); 'cicatrizam': encolhe até
    sumir na pele lisa."""
    fecha, t0 = fecha_furo(i, t, T)
    if fecha >= 1:
        return
    r = 11 * (1 - fecha)
    a = 1 - prog(fecha, 0.7, 1.0)
    realce = max(0.0, 1 - abs(t - (T["furos"] + 0.35)) / 0.55)
    if realce > 0:
        cv.drawCircle(x, y, 22, paint(OURO, int(150 * realce), blur=8))
        cv.drawCircle(x, y, 19, paint(OURO, int(230 * realce), "stroke", 3))
    cv.drawCircle(x, y, r + 2, paint("#000000", int(60 * a), blur=3))
    cv.drawCircle(x, y, r, paint(PELE_FURO, int(255 * a)))
    sem_pino = 1 - a_pinos(t, T)
    if sem_pino > 0:
        cv.drawCircle(x, y, r * 0.5, paint(lerpc(PELE_FURO, PELE_ESC, sem_pino), int(255 * a)))
    cv.drawCircle(x, y, r, paint("#F6C9B4", int(200 * a), "stroke", 2))


def reflexo(cv, y, u):
    """Brilho de metal correndo pelo arco da frente do anel (u: 0..1). (cópia do cf_fixador_circular)"""
    if not 0 < u < 1:
        return
    r = skia.Rect(CX - RX, y - RY, CX + RX, y + RY)
    ang = lerp(170, 10, u) - 14; a = math.sin(math.pi * u)
    cv.drawArc(r, ang, 34, False, paint("#FFFFFF", int(170 * a), "stroke", 28, blur=10))
    cv.drawArc(r, ang, 30, False, paint("#FFFFFF", int(255 * a), "stroke", 8))


def mundo(cv, t, T):
    desenha_perna(cv, 1.0)
    dy, a_fix = saida_fix(t, T)
    y_an = [y + dy for y in Y_AN]
    for y in y_an:
        anel(cv, y, 0, a_fix, "tras")
    osso(cv, t, T)
    brilhos(cv, CX, (B0 + B1) / 2, t, T["novo"] + 0.05, n=14, raio=150)

    ap = a_pinos(t, T)
    for i, (r, p0, p1, pp) in enumerate(PINOS):
        pino(cv, p0, p1, ap)
    for i, (r, p0, p1, pp) in enumerate(PINOS):
        ponto_pele(cv, pp[0], pp[1], t, T, i)
        fecha, t0 = fecha_furo(i, t, T)
        brilhos(cv, pp[0], pp[1], t, t0 + 0.4, n=6, raio=34)

    for sx in (-1, 1):
        x = CX + sx * X_HASTE
        haste(cv, x, y_an[0], y_an[1], a_fix)
        haste(cv, x, y_an[1], y_an[2], a_fix, rosca=True, fase=0.0)
        porca(cv, x, y_an[1] + 22, sx * 15, a_fix)
        porca(cv, x, y_an[2] - 22, -10, a_fix)
    pulso = (0.55 + 0.45 * math.sin(t * 6.5)) * (1 - prog(t, T["gaiola"] + 0.3, T["gaiola"] + 0.8))
    pulso = max(pulso, 1 - abs(t - (T["rapido"] + 0.6)) / 0.3)   # "rápido": pulso curto, junto do ding
    for i, y in enumerate(y_an):
        anel(cv, y, 0, a_fix, "frente")
        r = skia.Rect(CX - RX, y - RY, CX + RX, y + RY)
        if pulso > 0:                                      # a gaiola pulsa em ouro desde o quadro 0
            cv.drawArc(r, 0, 180, False, paint(OURO, int(120 * pulso), "stroke", 24, blur=12))
            cv.drawArc(r, 0, 180, False, paint(OURO, int(150 * pulso), "stroke", 4))
        reflexo(cv, y, prog(t, T["gaiola"] + 0.02 + 0.12 * i, T["gaiola"] + 0.5 + 0.12 * i))
        reflexo(cv, y, prog(t, T["equipe"] + 0.12 * i, T["equipe"] + 0.5 + 0.12 * i))   # "equipe"
        k = max(0.0, 1 - abs(t - (T["gaiola"] + 0.25 + 0.12 * i)) / 0.22)
        if k > 0:
            cv.drawArc(r, 0, 180, False, paint(ACO_HL, int(160 * k), "stroke", 22, blur=10))
            cv.drawArc(r, 0, 180, False, paint("#FFFFFF", int(230 * k), "stroke", 5))
    k = t - (T["sai"] + 0.05)                              # rastro curto de subida
    if 0 < k < 0.6 and a_fix > 0:
        for y in y_an:
            for j in range(3):
                yy = y + RY + 18 + j * 16 + 30 * k
                cv.drawLine(CX - 120 + j * 120, yy, CX - 120 + j * 120, yy + 22,
                            paint("#FFFFFF", int(120 * a_fix * (1 - k / 0.6)), "stroke", 3))


JAN0, JAN1 = 214, 1240


def janela_mundo(cv, t, T, cam):
    """O mundo vai numa camada com as bordas de cima e de baixo em degradê: no close, nada do osso
    invade o selo nem a faixa da legenda."""
    r = recua(t, T)
    if r >= 1:
        return
    jan = skia.Rect(0, JAN0, W, JAN1)
    cv.saveLayer(jan, None)
    fx, fy, sx, sy, s = cam
    cv.save()
    if r > 0:                                              # "o osso recua": encolhe e some
        esc = lerp(1.0, 0.1, e_inout(r))
        cv.translate(sx, sy); cv.scale(esc, esc); cv.translate(-sx, -sy)
    cv.translate(sx, sy); cv.scale(s, s); cv.translate(-fx, -fy)
    mundo(cv, t, T)
    cv.restore()
    m = clamp((s - 0.95) / 0.2)                            # a faixa de baixo só morde no close
    for ya, yb, c0, c1 in ((JAN0, JAN0 + 70, 0, 255), (JAN1 - 95, JAN1, 255, int(255 * (1 - m)))):
        masc = skia.Paint(AntiAlias=True)
        masc.setShader(skia.GradientShader.MakeLinear([skia.Point(0, ya), skia.Point(0, yb)],
                                                      [skia.ColorSetARGB(c0, 0, 0, 0), skia.ColorSetARGB(c1, 0, 0, 0)]))
        masc.setBlendMode(skia.BlendMode.kDstIn)
        cv.drawRect(skia.Rect(0, ya, W, yb), masc)
    if r > 0.6:
        p = skia.Paint(); p.setColor(skia.ColorSetARGB(int(255 * prog(r, 0.6, 1.0)), 0, 0, 0))
        p.setBlendMode(skia.BlendMode.kDstOut)
        cv.drawRect(jan, p)
    cv.restore()


# ------------------------------------------------------------------ ato 1: casa, equipe, relógio
def casinha(cv, x, y, a, esc=1.0):
    """Casinha de traço simples (sem texto)."""
    if a <= 0:
        return
    cv.save(); cv.translate(x, y); cv.scale(esc, esc)
    corpo = skia.Path(); corpo.addRect(skia.Rect(-92, -20, 92, 110))
    telhado = skia.Path(); telhado.moveTo(-122, -14); telhado.lineTo(0, -118); telhado.lineTo(122, -14); telhado.close()
    chamine = skia.Path(); chamine.addRect(skia.Rect(52, -112, 80, -58))
    forma = skia.Op(skia.Op(corpo, telhado, skia.PathOp.kUnion_PathOp), chamine, skia.PathOp.kUnion_PathOp)
    cv.drawPath(forma, paint("#000000", int(90 * a), blur=12))
    cv.drawPath(forma, paint("#14324A", int(240 * a)))
    cv.drawPath(forma, paint("#FFFFFF", int(240 * a), "stroke", 6))
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(-26, 40, 26, 110), 6, 6), paint(OURO, int(230 * a)))
    cv.drawCircle(14, 78, 4, paint("#14324A", int(255 * a)))
    for (wx, wy) in ((-72, 6), (40, 6)):
        cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(wx, wy, wx + 34, wy + 30), 4, 4), paint(AZUL, int(200 * a)))
        cv.drawLine(wx + 17, wy, wx + 17, wy + 30, paint("#14324A", int(255 * a), "stroke", 3))
    cv.restore()


def busto(cv, x, y, esc, cor, a):
    """Busto simples (cabeça + ombros), sem mão, sem instrumento."""
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


def equipe(cv, x, y, t, t0, a):
    if a <= 0:
        return
    for k, (dx, dy, esc, cor) in enumerate(((-92, 14, 0.84, "#4E9E94"), (92, 14, 0.84, "#4E9E94"),
                                            (0, 0, 1.0, TEAL))):
        kk = e_back(prog(t, t0 + 0.08 * k, t0 + 0.08 * k + 0.4))
        if kk > 0:
            busto(cv, x + dx, y + dy + 30 * (1 - kk), esc * clamp(kk, 0, 1.2), cor, a * clamp(kk * 2))


def relogio(cv, x, y, r, ang_fim, a, pulso=0.0):
    """Reloginho sem número: 4 marquinhas; o ponteiro (ouro) deixa a fatia do arco que andou."""
    if a <= 0:
        return
    cv.drawCircle(x, y, r + 14, paint(OURO, int(90 * a * pulso), blur=14))
    cv.drawCircle(x, y, r, paint("#000000", int(80 * a), blur=10))
    cv.drawCircle(x, y, r, paint(CARTAO, int(235 * a)))
    cv.drawCircle(x, y, r, paint("#FFFFFF", int(230 * a), "stroke", 6))
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(x - 12, y - r - 18, x + 12, y - r - 4), 4, 4), paint("#FFFFFF", int(230 * a)))
    for i in range(4):
        q = i * math.pi / 2
        cv.drawLine(x + (r - 16) * math.cos(q), y + (r - 16) * math.sin(q), x + (r - 7) * math.cos(q),
                    y + (r - 7) * math.sin(q), paint("#FFFFFF", int(190 * a), "stroke", 4))
    if ang_fim > 0.5:
        fatia = skia.Path(); fatia.moveTo(x, y)
        fatia.arcTo(skia.Rect(x - r + 10, y - r + 10, x + r - 10, y + r - 10), -90, ang_fim, False); fatia.close()
        cv.drawPath(fatia, paint(OURO, int(110 * a)))
    ang = math.radians(ang_fim - 90)
    cv.drawLine(x, y, x + (r - 18) * math.cos(ang), y + (r - 18) * math.sin(ang), paint(OURO, int(255 * a), "stroke", 6))
    cv.drawCircle(x, y, 6, paint(OURO, int(255 * a)))


# ------------------------------------------------------------------ ato 3: barra
BAR_X0, BAR_X1, BAR_Y0, BAR_Y1 = 560, 1010, 990, 1032


def barra(cv, t, T, a):
    if a <= 0:
        return
    cv.save(); cv.translate(24 * (1 - e_out(a)), 0)
    texto(cv, T_RESIST, BAR_X0, BAR_Y0 - 22, F_BLACK, 32, "#FFFFFF", int(255 * a), centro=False, contorno=7)
    tr = skia.RRect.MakeRectXY(skia.Rect(BAR_X0, BAR_Y0, BAR_X1, BAR_Y1), 21, 21)
    cv.drawRRect(tr, paint(CARTAO, int(215 * a)))
    cv.drawRRect(tr, paint("#FFFFFF", int(90 * a), "stroke", 2.5))
    f = enche_barra(t, T)
    xf = lerp(BAR_X0 + 4, BAR_X1 - 4, f)
    if f > 0.005:
        sh = skia.GradientShader.MakeLinear([skia.Point(0, BAR_Y0), skia.Point(0, BAR_Y1)],
                                            [C("#FFD27A"), C(OURO), C("#C98A1E")], [0.0, 0.45, 1.0])
        cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(BAR_X0 + 4, BAR_Y0 + 4, max(BAR_X0 + 30, xf), BAR_Y1 - 4), 17, 17),
                     paint(OURO, int(255 * a), shader=sh))
        cv.drawCircle(xf, (BAR_Y0 + BAR_Y1) / 2, 26, paint(NOVO_G, int(110 * a), blur=12))
    # POR MESES vai na ponta da barra (acompanha o enchimento, que não chega ao fim)
    a2 = a * prog(t, T["meses"] - 0.25, T["meses"])
    if a2 > 0:
        xm = max(xf, BAR_X0 + 120)
        p = skia.Path(); p.moveTo(xm, BAR_Y1 + 6); p.lineTo(xm - 12, BAR_Y1 + 22); p.lineTo(xm + 12, BAR_Y1 + 22); p.close()
        cv.drawPath(p, paint(AZUL, int(255 * a2)))
        lw = larg_texto(T_MESES, F_BLACK, 32)
        xc = clamp(xm, BAR_X0 + lw / 2 + 24, BAR_X1 - lw / 2 - 24)
        pilula(cv, T_MESES, xc, BAR_Y1 + 70, 32, AZUL, a2, esc=lerp(1.25, 1.0, e_out(prog(t, T["meses"], T["meses"] + 0.25))))
    cv.restore()


# ------------------------------------------------------------------ ato 4: escada, seta, cartão
def seta_peso(cv, x, y_ponta, a, esmaga, esc=0.95):
    """Seta grossa para baixo (peso), sem texto. (cópia do cf_quanto_tempo, com escala)"""
    if a <= 0:
        return
    cv.save(); cv.translate(x, y_ponta); cv.scale(esc * (1 + 0.06 * esmaga), esc * (1 - 0.1 * esmaga))
    p = skia.Path()
    p.moveTo(-22, -96); p.lineTo(22, -96); p.lineTo(22, -54); p.lineTo(52, -54); p.lineTo(0, 0)
    p.lineTo(-52, -54); p.lineTo(-22, -54); p.close()
    cv.drawPath(p, paint("#000000", int(90 * a), blur=10))
    sh = skia.GradientShader.MakeLinear([skia.Point(-52, 0), skia.Point(52, 0)],
                                        [C("#FFFFFF", int(255 * a)), C("#C9D6E2", int(255 * a))])
    cv.drawPath(p, paint("#FFFFFF", 255, shader=sh))
    cv.drawPath(p, paint("#5E7186", int(220 * a), "stroke", 3))
    cv.restore()


def degrau(i):
    x0 = DEG_X0 + i * DEG_RUN
    return x0, x0 + DEG_RUN, DEG_BASE - (i + 1) * DEG_RISE


def pos_seta(t, T):
    """(x, y da ponta, esmaga) da seta: pousa no 1º degrau e sobe um degrau por vez."""
    ac = acesos(T)
    t_in = T["carga"] + 0.18
    x0, x1, y = degrau(0)
    if t < ac[0]:
        k = prog(t, t_in, ac[0])
        return (x0 + x1) / 2, lerp(y - 70, y, k * k), 0.0
    i = 0
    for j in range(1, len(ac)):
        if t >= ac[j] - 0.3:
            i = j
    xa0, xa1, ya = degrau(max(0, i - 1)); xb0, xb1, yb = degrau(i)
    if i == 0:
        ki = t - ac[0]
        return (x0 + x1) / 2, y, math.sin(math.pi * clamp(ki / 0.22)) if ki < 0.22 else 0.0
    k = e_inout(prog(t, ac[i] - 0.3, ac[i] + 0.05))
    x = lerp((xa0 + xa1) / 2, (xb0 + xb1) / 2, k)
    yy = lerp(ya, yb, k) - 46 * math.sin(math.pi * k)
    ki = t - (ac[i] + 0.05)
    return x, yy, (math.sin(math.pi * clamp(ki / 0.2)) if 0 < ki < 0.2 else 0.0)


def escada(cv, t, T, a):
    if a <= 0:
        return
    ac = acesos(T)
    # alturas atuais (cada degrau sobe do chão com um pequeno atraso)
    alt = []
    for i in range(N_DEG):
        x0, x1, y = degrau(i)
        k = e_back(prog(t, T["carga"] + 0.05 + 0.06 * i, T["carga"] + 0.45 + 0.06 * i))
        alt.append((x0, x1, lerp(DEG_BASE, y, clamp(k, 0, 1.1)) if k > 0 else DEG_BASE))
    # UMA silhueta em degraus (sem divisórias): lê como escada, não como gráfico de barras; tudo numa
    # camada com a borda direita esmaecendo (a escada continua para fora do quadro, sem topo)
    cv.saveLayer(skia.Rect(0, 560, W, DEG_BASE + 10), None)
    cv.drawLine(60, DEG_BASE + 2, W, DEG_BASE + 2, paint("#FFFFFF", int(60 * a), "stroke", 3))
    sil = skia.Path(); sil.moveTo(alt[0][0], DEG_BASE)
    contorno = skia.Path(); contorno.moveTo(alt[0][0], DEG_BASE)
    for x0, x1, yy in alt:
        sil.lineTo(x0, yy); sil.lineTo(x1, yy)
        contorno.lineTo(x0, yy); contorno.lineTo(x1, yy)
    sil.lineTo(alt[-1][1], DEG_BASE); sil.close()
    topo = min(yy for _, _, yy in alt)
    sh = skia.GradientShader.MakeLinear([skia.Point(0, topo), skia.Point(0, DEG_BASE)],
                                        [C("#2C5B78", int(255 * a)), C("#123045", int(255 * a))])
    cv.drawPath(sil, paint("#2C5B78", 255, shader=sh))
    cv.drawPath(contorno, paint("#6B8296", int(255 * a), "stroke", 7))
    for i, (x0, x1, yy) in enumerate(alt):                 # degraus já pisados: piso dourado
        on = e_out(prog(t, ac[i], ac[i] + 0.3)) if i < len(ac) else 0.0
        if on > 0 and yy < DEG_BASE - 1:
            flash = max(0.0, 1 - (t - ac[i]) / 0.6)
            cv.drawLine(x0 + 4, yy, x1 - 4, yy, paint(NOVO_G, int(a * (90 + 120 * flash) * on), "stroke", 16, blur=10))
            cv.drawLine(x0 + 4, yy, x1 - 4, yy, paint(OURO, int(255 * a * on), "stroke", 7))
    masc = skia.Paint(AntiAlias=True)
    masc.setShader(skia.GradientShader.MakeLinear([skia.Point(DEG_FADE0, 0), skia.Point(DEG_FADE1, 0)],
                                                  [skia.ColorSetARGB(255, 0, 0, 0),
                                                   skia.ColorSetARGB(int(255 * DEG_ALFA_FIM), 0, 0, 0)]))
    masc.setBlendMode(skia.BlendMode.kDstIn)
    cv.drawRect(skia.Rect(0, 560, W, DEG_BASE + 10), masc)
    cv.restore()
    sx, sy, esm = pos_seta(t, T)
    a_s = a * prog(t, T["carga"] + 0.18, T["carga"] + 0.3)
    seta_peso(cv, sx, sy - 4, a_s, esm)


def ampulheta(cv, x, y, s, a, rot, areia_cima):
    """Ampulheta (no lugar do check): vira devagar e a areia escorre. (a partir do ícone do cf_quanto_tempo)"""
    cv.save(); cv.translate(x, y); cv.rotate(rot)
    p = skia.Path()
    p.moveTo(-0.7 * s, -s); p.lineTo(0.7 * s, -s); p.lineTo(0.1 * s, 0)
    p.lineTo(0.7 * s, s); p.lineTo(-0.7 * s, s); p.lineTo(-0.1 * s, 0); p.close()
    cv.drawPath(p, paint(CARTAO, int(200 * a)))
    if areia_cima > 0.02:
        top = skia.Path()
        w = 0.6 * math.sqrt(areia_cima)
        top.moveTo(-w * s, -0.15 * s - 0.65 * s * areia_cima); top.lineTo(w * s, -0.15 * s - 0.65 * s * areia_cima)
        top.lineTo(0, -0.08 * s); top.close()
        cv.drawPath(top, paint(OURO, int(255 * a)))
    baixo = 1 - areia_cima
    if baixo > 0.02:
        w = 0.62 * math.sqrt(baixo)
        bot = skia.Path(); bot.moveTo(-w * s, 0.85 * s); bot.lineTo(w * s, 0.85 * s); bot.lineTo(0, 0.85 * s - 0.6 * s * baixo); bot.close()
        cv.drawPath(bot, paint(OURO, int(255 * a)))
    if 0.02 < areia_cima < 0.98:
        cv.drawLine(0, 0, 0, 0.8 * s, paint(OURO, int(220 * a), "stroke", 2.5))
    cv.drawPath(p, paint("#FFFFFF", int(240 * a), "stroke", 3.5))
    for yy in (-s, s):
        cv.drawLine(-0.92 * s, yy, 0.92 * s, yy, paint("#FFFFFF", int(240 * a), "stroke", 5))
    cv.restore()


def bolinha(cv, x, y, t, a):
    """Bolinha quicando (impacto), sem texto."""
    fase = (t * 2.2) % 1.0
    h = 26 * math.sin(math.pi * fase)
    cv.drawLine(x - 24, y + 22, x + 24, y + 22, paint("#FFFFFF", int(170 * a), "stroke", 3.5))
    cv.drawOval(skia.Rect(x - 14 + h * 0.2, y + 18, x + 14 - h * 0.2, y + 25), paint("#000000", int(90 * a)))
    esm = max(0.0, 1 - h / 6) * 0.22
    cv.save(); cv.translate(x, y + 7 - h); cv.scale(1 + esm, 1 - esm)
    cv.drawCircle(0, 0, 13, paint(CORAL, int(255 * a)))
    cv.drawCircle(-4, -4, 4, paint("#FFFFFF", int(160 * a)))
    cv.restore()
    for k in (-1, 1):
        if h < 6:
            cv.drawLine(x + k * 20, y + 14, x + k * 28, y + 8, paint("#FFFFFF", int(150 * a), "stroke", 3))


def giro(cv, x, y, t, a):
    """Seta curva de giro (torção), sem texto."""
    cv.save(); cv.translate(x, y); cv.rotate(-25 + 18 * math.sin(t * 3.0))
    r = 22
    cv.drawArc(skia.Rect(-r, -r, r, r), 20, 280, False, paint(CORAL, int(255 * a), "stroke", 6))
    ang = math.radians(300)
    px, py = r * math.cos(ang), r * math.sin(ang)
    p = skia.Path(); tx, ty = -math.sin(ang), math.cos(ang)
    p.moveTo(px + 13 * tx, py + 13 * ty); p.lineTo(px - 9 * math.cos(ang) - 4 * tx, py - 9 * math.sin(ang) - 4 * ty)
    p.lineTo(px + 9 * math.cos(ang) - 4 * tx, py + 9 * math.sin(ang) - 4 * ty); p.close()
    cv.drawPath(p, paint(CORAL, int(255 * a)))
    cv.restore()


CARD_Y0 = 380


def cartao_espera(cv, t, T, a):
    """IMPACTO E TORÇÃO (com a bolinha e a seta de giro); no lugar do check, a ampulheta. Em
    'esperam' o cartão abre a 2ª linha ESPERAM A LIBERAÇÃO e a ampulheta vira; a areia começa a
    escorrer em 'liberação'."""
    if a <= 0:
        return
    w1 = larg_texto(T_IMPACTO, F_BLACK, 40)
    larg_lin1 = 70 + 30 + 56 + 28 + 56 + 34 + w1
    g = e_out(prog(t, T["esperam"] - 0.05, T["esperam"] + 0.3))
    larg = max(larg_lin1, larg_texto(T_ESPERAM, F_BLACK, 40) + 96)
    x0 = CX - (larg + 56) / 2; y0 = CARD_Y0 - 18 * (1 - e_out(a))
    h = 108 + 84 * g
    rr = skia.RRect.MakeRectXY(skia.Rect(x0, y0, x0 + larg + 56, y0 + h), 22, 22)
    cv.drawRRect(rr, paint("#000000", int(90 * a), blur=14))
    cv.drawRRect(rr, paint(CARTAO, int(228 * a))); cv.drawRRect(rr, paint(OURO, int(150 * a), "stroke", 2.5))
    xc = x0 + 28
    # a "caixinha do check" com a ampulheta dentro
    bx = skia.RRect.MakeRectXY(skia.Rect(xc, y0 + 19, xc + 70, y0 + 89), 14, 14)
    cv.drawRRect(bx, paint("#14324A", int(235 * a))); cv.drawRRect(bx, paint(OURO, int(255 * a), "stroke", 3.5))
    vira = e_inout(prog(t, T["esperam"] - 0.05, T["esperam"] + 0.5))
    if vira < 1:
        rot, cima = 180 * vira, 0.0
    else:
        rot, cima = 0.0, 1 - 0.75 * prog(t, T["esperam"] + 0.5, t_corte_pista(T))
    ampulheta(cv, xc + 35, y0 + 54, 22, a, rot, cima)
    xi = xc + 70 + 30
    k1 = e_back(prog(t, T["impacto"] - 0.05, T["impacto"] + 0.3)) * 1.35
    if k1 > 0:
        cv.save(); cv.translate(xi + 28, y0 + 54); cv.scale(k1, k1); cv.translate(-(xi + 28), -(y0 + 54))
        bolinha(cv, xi + 28, y0 + 50, t, a)
        cv.restore()
    k2 = e_back(prog(t, T["torcao"] - 0.05, T["torcao"] + 0.3)) * 1.35
    if k2 > 0:
        cv.save(); cv.translate(xi + 112, y0 + 54); cv.scale(k2, k2); cv.translate(-(xi + 112), -(y0 + 54))
        giro(cv, xi + 112, y0 + 54, t, a)
        cv.restore()
    texto(cv, T_IMPACTO, xi + 56 + 28 + 56 + 34, y0 + 70, F_BLACK, 40, "#FFFFFF", int(255 * a), centro=False)
    if g > 0.05:
        cv.save(); cv.clipRRect(rr, True)
        a2 = a * clamp((g - 0.6) / 0.4)
        cv.drawLine(x0 + 24, y0 + 108, x0 + larg + 32, y0 + 108, paint("#FFFFFF", int(40 * a2), "stroke", 2))
        texto(cv, T_ESPERAM, x0 + 28, y0 + 160, F_BLACK, 40, OURO, int(255 * a2), centro=False)
        cv.restore()


# ------------------------------------------------------------------ ato 5: pista
Y_H, Y_N = 318, 1190                          # horizonte e linha de baixo (z = 1)
MEIA = 400                                   # meia largura da pista (mundo)
Z_BAND, Z_CHEG = 1.5, 3.6                   # onde o marcador para (bandeira) e a linha de chegada
Z_INI = 0.97
ALT_M = 262                                  # altura do marcador em z = 1


def proj(xw, z):
    return CX + xw / z, Y_H + (Y_N - Y_H) / z


def z_marcador(t, T):
    return lerp(Z_INI, Z_BAND, e_out(prog(t, t_corte_pista(T) + 0.05, T["final"] + 0.2)))


def pista_resumo(t, T):
    return e_inout(prog(t, T["chegada"] + 0.55, T["chegada"] + 1.5))


def pista(cv, t, T, a):
    """Pista em perspectiva (sem texto): asfalto, bordas, faixa central tracejada."""
    zf = 12.0
    pts = [proj(-MEIA, 0.9), proj(MEIA, 0.9), proj(MEIA, zf), proj(-MEIA, zf)]
    p = skia.Path(); p.moveTo(*pts[0])
    for q in pts[1:]:
        p.lineTo(*q)
    p.close()
    sh = skia.GradientShader.MakeLinear([skia.Point(0, Y_H), skia.Point(0, Y_N)],
                                        [C("#17384C", int(0 * a)), C("#22506B", int(255 * a)), C("#2D6584", int(255 * a))],
                                        [0.0, 0.35, 1.0])
    cv.drawPath(p, paint("#22506B", 255, shader=sh))
    for s in (-1, 1):
        x0, y0 = proj(s * MEIA, 0.9); x1, y1 = proj(s * MEIA, zf)
        sh2 = skia.GradientShader.MakeLinear([skia.Point(0, y1), skia.Point(0, y0)],
                                             [C("#FFFFFF", 0), C("#FFFFFF", int(230 * a))], [0.0, 0.45])
        pp = paint("#FFFFFF", 255, "stroke", 7, shader=sh2)
        cv.drawLine(x0, y0, x1, y1, pp)
    z = 0.95
    while z < 9:
        za, zb = z, z + 0.28 * z
        xa, ya = proj(0, za); xb, yb = proj(0, zb)
        al = a * clamp((9 - z) / 4)
        larg = 10 / za * 1.4
        cv.drawLine(xa, ya, xb, yb, paint("#FFFFFF", int(150 * al), "stroke", max(2.0, larg)))
        z = zb + 0.3 * z


def marcador(cv, x, yb, alt, a, brilho=0.0):
    """O marcador é a própria tíbia da cena em miniatura (marfim, com a faixa dourada), em pé sobre a
    pista — não um 'osso de cachorro' simétrico. Sem texto."""
    if a <= 0:
        return
    esc = alt / (Y_BASE + 40 - Y_TOPO)
    w = 128 * esc
    cv.drawOval(skia.Rect(x - w * 1.3, yb - w * 0.28, x + w * 1.3, yb + w * 0.28), paint("#000000", int(120 * a), blur=6))
    if brilho > 0:
        cv.drawCircle(x, yb - alt / 2, alt * 0.6, paint(NOVO_G, int(110 * brilho * a), blur=18))
    cv.saveLayerAlpha(None, int(255 * a))
    cv.translate(x, yb); cv.scale(esc, esc); cv.translate(-CX, -(Y_BASE + 40))
    cv.drawPath(OSSO, paint("#000000", 90, blur=10))
    cv.drawPath(OSSO, paint(OSSO_C, shader=sombra_osso()))
    cv.drawRect(skia.Rect(CX - HASTE / 2 + 2, B0, CX + HASTE / 2 - 2, B1), paint(OURO))
    cv.drawPath(OSSO, paint(OSSO_L, 220, "stroke", 2.5 / max(esc, 0.15)))
    cv.restore()


def bandeira(cv, x, yb, t, t0, t1, a):
    """Bandeira fincada no acostamento esquerdo; o pano (RETA FINAL) tremula para a direita, por cima
    da pista, e termina ao lado de onde o marcador para."""
    k = t - t0
    if k < 0 or a <= 0:
        return
    cai = e_out(clamp(k / 0.3)); al = a * clamp(k / 0.1)
    dy = -50 * (1 - cai)
    ytop = yb - 170 + dy
    cv.drawLine(x, ytop - 8, x, yb + dy, paint("#000000", int(80 * al), "stroke", 10, blur=4))
    cv.drawLine(x, ytop - 8, x, yb + dy, paint("#DDE6EE", int(255 * al), "stroke", 7))
    cv.drawCircle(x, ytop - 10, 8, paint(OURO, int(255 * al)))
    abre = e_out(prog(t, t1, t1 + 0.4))
    if abre <= 0:
        return
    tam = 34; lw = larg_texto(T_RETA, F_BLACK, tam)
    x0 = x + 4; x1 = x0 + (lw + 56) * abre; hb = 56
    wv = 6 * math.sin(t * 4.5)
    p = skia.Path(); p.moveTo(x0, ytop)
    p.quadTo((x0 + x1) / 2, ytop - wv, x1, ytop + wv * 0.6)
    p.lineTo(x1 - 20 * abre, ytop + hb / 2 + wv * 0.6)
    p.lineTo(x1, ytop + hb + wv * 0.6)
    p.quadTo((x0 + x1) / 2, ytop + hb - wv, x0, ytop + hb); p.close()
    cv.drawPath(p, paint("#000000", int(80 * al), blur=8))
    cv.drawPath(p, paint(OURO, int(255 * al)))
    cv.drawPath(p, paint("#8A6512", int(255 * al), "stroke", 2.5))
    if abre > 0.9:
        texto(cv, T_RETA, (x0 + x1 - 22) / 2, ytop + 40, F_BLACK, tam, CARTAO, int(255 * al * clamp((abre - 0.9) / 0.1)))


def cena_pista(cv, t, T, a):
    if a <= 0:
        return
    r = pista_resumo(t, T)
    esc = lerp(1.0, 0.84, r)
    cx, cy = CX, lerp(700, 640, r)
    cv.save()
    cv.translate(cx, cy); cv.scale(esc, esc); cv.translate(-cx, -cy)

    def T2(x, y):
        return cx + (x - cx) * esc, cy + (y - cy) * esc

    entra = e_out(prog(t, t_corte_pista(T), t_corte_pista(T) + 0.45))
    cv.save(); cv.translate(CX, Y_N); cv.scale(lerp(1.12, 1.0, entra), lerp(1.12, 1.0, entra)); cv.translate(-CX, -Y_N)
    pista(cv, t, T, a)
    zm = z_marcador(t, T)
    # o trecho que falta: pontos dourados do marcador até a linha de chegada (pulsam no respiro)
    a_f = a * prog(t, T["ainda"] - 0.05, T["ainda"] + 0.3)
    if a_f > 0:
        topo = proj(0, zm)[1] - ALT_M / zm - 22          # só à frente do marcador (nada atrás dele)
        z = max(zm + 0.2, (Y_N - Y_H) / max(1.0, topo - Y_H))
        i = 0
        while z < Z_CHEG - 0.12:
            x, y = proj(0, z)
            onda = 0.5 + 0.5 * math.sin(t * 7 - i * 0.9)
            cv.drawCircle(x, y, max(3.0, 9 / z * 1.6), paint(OURO, int(255 * a_f * (0.45 + 0.55 * onda))))
            z += 0.32 * z; i += 1
    # linha de chegada tracejada (não alcançada)
    k = prog(t, T["linha"] - 0.1, T["linha"] + 0.35)
    if k > 0:
        xa, y = proj(-MEIA, Z_CHEG); xb, _ = proj(MEIA, Z_CHEG)
        xe = lerp(xa, xb, e_out(k))
        brilho = max(0.0, 1 - abs(t - (T["chegada"] + 0.25)) / 0.5) + 0.35 * r * (0.5 + 0.5 * math.sin(t * 5))
        if brilho > 0:
            cv.drawLine(xa, y, xe, y, paint(OURO, int(150 * a * min(1.0, brilho)), "stroke", 18, blur=10))
        tracejado(cv, xa, y, xe, y, "#FFFFFF", a, larg=9, traco=16, vazio=11)
        for xx in (xa - 6, xb + 6):
            if xx <= xe + 8:
                cv.drawLine(xx, y + 2, xx, y - 46, paint("#DDE6EE", int(230 * a), "stroke", 5))
    # brilhos centrados no marcador e desenhados ANTES da bandeira: o pano RETA FINAL fica por cima
    # e o texto nunca é coberto
    xbd, ybd = proj(-MEIA - 60, Z_BAND)
    xm, ym = proj(0, zm)
    brilhos(cv, xm, ym - ALT_M / zm * 0.55, t, T["final"] + 0.1, n=10, raio=120)
    # bandeira RETA FINAL no acostamento esquerdo, na altura onde o marcador para
    bandeira(cv, xbd, ybd, t, T["reta"] - 0.05, T["final"] - 0.1, a)
    # marcador
    brilho_m = max(0.0, 1 - abs(t - (T["final"] + 0.25)) / 0.5)
    marcador(cv, xm, ym, ALT_M / zm, a, brilho_m)
    cv.restore()
    cv.restore()
    # rótulo da linha de chegada (fora da escala: fonte sempre legível)
    a_l = a * prog(t, T["linha"] - 0.05, T["linha"] + 0.25)
    if a_l > 0:
        _, y = proj(0, Z_CHEG)
        xs, ys = T2(CX, y)
        pilula(cv, T_CHEGADA, xs, ys - 62, 34, "#FFFFFF", a_l, esc=lerp(1.2, 1.0, e_out(prog(t, T["linha"], T["linha"] + 0.25))))


# ------------------------------------------------------------------ quadro
def quadro(cv, t, T, blocos, ep):
    fundo(cv, t)
    cam = camera(t, T)
    janela_mundo(cv, t, T, cam)
    t_capa = T["casa"] + 0.3

    # ---------- ato 1 (coluna da direita + pílula sob o fixador)
    XC = 800
    a = prog(t, T["gaiola"] + 0.5, T["gaiola"] + 0.75) * (1 - prog(t, T["procedimento"] - 0.2, T["procedimento"] + 0.05))
    etiqueta(cv, [(T_FIX, F_BLACK, 36, "#FFFFFF")], 586, 430,
             na_tela(cam, CX + RX * math.cos(math.radians(30)), Y_AN[0] + RY * math.sin(math.radians(30))), ACO_HL, a)
    k_in = e_back(prog(t, T["casa"] - 0.12, T["casa"] + 0.3))
    t_casa_sai = T["equipe"] - 0.12                        # casinha + carimbo ficam até "equipe"
    k_out = e_in_back(prog(t, t_casa_sai - 0.3, t_casa_sai))
    a_casa = clamp(k_in * 3) * (1 - prog(t, t_casa_sai - 0.12, t_casa_sai))
    casinha(cv, XC + 340 * (1 - clamp(k_in, 0, 1.2)) + 420 * k_out, 700, a_casa)
    # o carimbo está NA casinha: sai com ela, para a direita, sem o recuo inicial (não encosta no anel)
    carimbo_cor(cv, T_CASA, XC - 20 + 420 * max(0.0, k_out), 742, -6, T["nao"] - 0.02, t, t_casa_sai - (T["nao"] - 0.02),
                tam=38, esc0=1.08, saida=0.12)

    t_eq = T["equipe"] - 0.1                               # os bustos entram na palavra "equipe"
    a_eq = prog(t, t_eq, t_eq + 0.15) * (1 - prog(t, T["geral"] - 0.35, T["geral"] - 0.1))
    equipe(cv, XC, 700, t, t_eq, a_eq)

    Y_BAIXO = 1186
    a = prog(t, T["procedimento"], T["procedimento"] + 0.25) * (1 - prog(t, T["muitas"] - 0.25, T["muitas"] - 0.05))
    pilula(cv, T_EQUIPE, CX, Y_BAIXO, 38, OURO, a, cor_txt="#FFFFFF", dy=20 * (1 - e_out(a)))
    a = prog(t, T["muitas"] - 0.05, T["muitas"] + 0.2) * (1 - prog(t, T["aparelho"] - 0.15, T["aparelho"] + 0.05))
    pilula(cv, T_SEDACAO, CX, Y_BAIXO, 38, AZUL, a, cor_txt="#FFFFFF", dy=20 * (1 - e_out(a)))

    k = e_back(prog(t, T["geral"] - 0.2, T["geral"] + 0.2))
    a_rel = clamp(k * 2) * (1 - prog(t, T["aparelho"] - 0.15, T["aparelho"] + 0.05))
    if a_rel > 0:
        giro_rel = 78 * e_inout(prog(t, T["rapido"] - 0.05, T["rapido"] + 0.55))
        pulso = max(0.0, 1 - abs(t - (T["rapido"] + 0.6)) / 0.4)
        cv.save(); cv.translate(XC, 610); cv.scale(clamp(k, 0, 1.2), clamp(k, 0, 1.2)); cv.translate(-XC, -610)
        relogio(cv, XC, 610, 74, giro_rel, a_rel, pulso)
        cv.restore()
        a2 = a_rel * prog(t, T["geral"] - 0.05, T["geral"] + 0.2)
        texto(cv, T_RAPIDO, XC, 760, F_BLACK, 38, "#FFFFFF", int(255 * a2), contorno=8)

    # ---------- ato 2
    # acima da faixa da etiqueta FUROS (y 640-706): pode ficar ~1,6 s
    carimbo_cor(cv, T_SAI, XC, 520, -5, T["sai"] + 0.02, t, T["cicatrizam"] - 0.1 - T["sai"], tam=48, cor=OURO,
                esc0=1.08)
    a = prog(t, T["furos"] - 0.05, T["furos"] + 0.2) * (1 - prog(t, T["mas"] - 0.25, T["mas"]))
    _, _, _, pp = PINOS[3]
    etiqueta(cv, [(T_FUROS, F_BLACK, 36, "#FFFFFF")], 586, 640, na_tela(cam, pp[0] + 12, pp[1]), PELE, a)
    a = prog(t, T["cicatrizam"] - 0.05, T["cicatrizam"] + 0.2) * (1 - prog(t, T["mas"] - 0.2, T["mas"] + 0.05))
    pilula(cv, T_CICATRIZ, CX, Y_BAIXO, 38, PELE, a, cor_txt="#FFFFFF", dy=20 * (1 - e_out(a)))

    # ---------- ato 3 (perto do osso novo)
    some3 = 1 - prog(t, T["carga"] - 0.3, T["carga"] - 0.05)
    a = prog(t, T["novo"] - 0.05, T["novo"] + 0.2) * some3
    etiqueta(cv, [(T_NOVO, F_BLACK, 36, OURO), (T_FRAGIL, F_BLACK, 34, CORAL)], 586, 676,
             na_tela(cam, CX + HASTE / 2 - 4, (B0 + B1) / 2), OURO, a,
             cresce=e_out(prog(t, T["fragil"] - 0.1, T["fragil"] + 0.2)))
    a = prog(t, T["maduro"] - 0.05, T["maduro"] + 0.2) * some3
    etiqueta(cv, [(T_MADURO, F_BLACK, 36, "#FFFFFF")], 586, 430, na_tela(cam, CX + HASTE / 2 - 4, 600), OSSO_C, a)
    # a barra (e POR MESES) some DEPOIS das etiquetas, separada do recuo do osso: ~0,8 s de leitura
    some_barra = 1 - prog(t, T["carga"] - 0.05, T["carga"] + 0.2)
    barra(cv, t, T, prog(t, T["ganhando"] - 0.05, T["ganhando"] + 0.25) * some_barra)

    # ---------- ato 4 (escada, carga, impacto e torção)
    a4 = prog(t, T["carga"] - 0.05, T["carga"] + 0.2) * (1 - prog(t, t_corte_pista(T) - 0.2, t_corte_pista(T)))
    escada(cv, t, T, a4)
    y_carga = lerp(560, 312, e_inout(prog(t, T["impacto"] - 0.45, T["impacto"] - 0.05)))
    pilula(cv, T_CARGA, CX, y_carga, 42, OURO, a4 * prog(t, T["carga"], T["carga"] + 0.25), cor_txt="#FFFFFF",
           esc=lerp(1.25, 1.0, e_out(prog(t, T["carga"], T["carga"] + 0.3))))
    cartao_espera(cv, t, T, prog(t, T["impacto"] - 0.1, T["impacto"] + 0.15) * (1 - prog(t, t_corte_pista(T) - 0.2, t_corte_pista(T))))

    # ---------- ato 5 (pista)
    a5 = prog(t, t_corte_pista(T), t_corte_pista(T) + 0.25) * (1 - prog(t, T["manda"] - 0.45, T["manda"] - 0.1))
    if a5 > 0:
        jan = skia.Rect(0, JAN0, W, JAN1)
        cv.saveLayer(jan, None); cv.clipRect(jan)
        cena_pista(cv, t, T, a5)
        masc = skia.Paint(AntiAlias=True)
        masc.setShader(skia.GradientShader.MakeLinear([skia.Point(0, JAN1 - 110), skia.Point(0, JAN1)],
                                                      [skia.ColorSetARGB(255, 0, 0, 0), skia.ColorSetARGB(0, 0, 0, 0)]))
        masc.setBlendMode(skia.BlendMode.kDstIn)
        cv.drawRect(skia.Rect(0, JAN1 - 110, W, JAN1), masc)
        cv.restore()

    capa(cv, t, t_capa, ep["gancho"][0], ep["gancho"][1])
    selo_como_funciona(cv, prog(t, t_capa + 0.45, t_capa + 0.85) * (1 - prog(t, T["manda"] - 0.3, T["manda"])))
    interface(cv, t, T, blocos, DESTAQUE)


# ------------------------------------------------------------------ som e prévias
def sons(T):
    ev = [(T["gaiola"] + 0.25 + 0.12 * i, "ping", 0.5 - 0.06 * i) for i in range(3)]
    ev += [(T["gaiola"] + 0.05, "whoosh", 0.3), (T["gaiola"] + 0.5, "pop", 0.4),
           (T["casa"] - 0.1, "whoosh", 0.45), (T["casa"] + 0.15, "pop", 0.45), (T["nao"] - 0.02, "thump", 0.9),
           (T["equipe"] - 0.4, "whoosh", 0.4), (T["procedimento"] + 0.05, "pop", 0.4)]
    ev += [(T["equipe"] - 0.1 + 0.08 * k + 0.25, "pop", 0.35) for k in range(3)]
    ev += [(T["geral"] - 0.15, "pop", 0.55), (T["rapido"] - 0.05, "tick", 0.7), (T["rapido"] + 0.2, "tick", 0.6),
           (T["rapido"] + 0.55, "ding", 0.45), (T["muitas"] - 0.05, "whoosh", 0.25), (T["sedacao"], "shimmer", 0.3),
           (T["aparelho"], "whoosh", 0.3)]
    ev += [(T["sai"] + 0.05 + 0.1 * i, "ping", 0.32) for i in range(3)]
    ev += [(T["sai"], "whoosh", 0.55), (T["sai"] + 0.05, "thump", 0.5), (T["furos"] + 0.05, "pop", 0.5)]
    ev += [(T["cicatrizam"] + 0.05 + 0.15 * i + 0.4, "pop", 0.28) for i in range(6)]
    ev += [(T["cicatrizam"] + 1.1, "shimmer", 0.35), (T["mas"] - 0.05, "whoosh", 0.4), (T["novo"] + 0.05, "shimmer", 0.75),
           (T["fragil"], "tick", 0.55), (T["maduro"], "pop", 0.45), (T["ganhando"], "shimmer", 0.5),
           (T["resistencia"] + 0.1, "crackle", 0.4), (T["meses"], "pop", 0.4),
           (T["carga"] - 0.2, "whoosh", 0.55), (T["carga"] + 0.15, "pop", 0.4)]
    ac = acesos(T)
    ev += [(ac[0], "thump", 0.75)] + [(x, "click", 0.85) for x in ac[1:]] + [(x + 0.05, "ding", 0.18) for x in ac]
    ev += [(T["impacto"] - 0.05, "whoosh", 0.3), (T["impacto"] + 0.05, "pop", 0.5), (T["torcao"], "pop", 0.45),
           (T["esperam"], "pop", 0.4), (T["esperam"] + 0.1, "whoosh", 0.2), (T["esperam"] + 0.5, "tick", 0.5),
           (t_corte_pista(T), "whoosh", 0.55), (T["final"] - 0.05, "pop", 0.45), (T["final"] + 0.15, "ding", 0.45),
           (T["ainda"], "shimmer", 0.3), (T["linha"], "whoosh", 0.3), (T["chegada"] + 0.2, "shimmer", 0.5),
           (T["chegada"] + 0.6, "whoosh", 0.3), (T["manda"] + 0.05, "whoosh", 0.5)]
    return ev


def tempos_previa(T):
    return [0.0, T["nao"] + 0.35, T["equipe"] + 0.25, T["rapido"] + 0.7, T["sai"] + 0.3, T["cicatrizam"] + 0.6,
            T["fragil"] + 0.5, T["meses"] + 0.4, T["poucos"] + 0.6, T["liberacao"] + 0.5, T["chegada"] + 0.3,
            T["manda"] + 1.6]


render = fazer_render(quadro, ANCORAS, sons, tempos_previa, respiro_cta=2.2)
