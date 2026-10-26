# -*- coding: utf-8 -*-
"""CHAMA O VAR — piloto "O FIXADOR PARECE / UMA ALÇA. PODE?" (rotina com fixador externo), versão 4.

Versão 4 (polimento final, leitor às cegas: "só entendi o que era 'o aparelho' no fim"): o objeto tem UM
nome só, dito e desenhado. A voz diz "fixador" nas 4 vezes (antes, 2 eram "aparelho" — a fonte usa os dois
como sinônimos: "sentar e levantar com o fixador" / "O aparelho não é alça"), e o analista do VAR MARCA o
objeto na tela como no telestrador da TV: em "fixador" (lance 1, ~2 s) um ponto no anel, um fio ciano e a
etiqueta FIXADOR; de novo em "fixador" no lance 3, antes de a capa cobrir. O quadro 0 continua só com o
gancho de texto (que já diz "O FIXADOR").

Série nova (ter/qui/sáb), DIFERENTE do COMO FUNCIONA: em vez de um mecanismo por dentro do corpo, o
VAR julga três LANCES da vida real com fixador. Cada lance segue o mesmo ritual: o lance roda ->
"pode?" (CONGELA, obturador, círculo de telestrador) -> ~0,6 s de CHECANDO com bipes e a câmera
chegando devagar no detalhe que decide -> carimbo (ANULADO âmbar / VALIDADO verde) -> a frase do
porquê, DEMONSTRADA na imagem -> o jeito certo (chip verde JEITO CERTO). O chip do selo VAR segue a
ordem fixa LANCE n -> CHECANDO -> veredito -> JEITO CERTO, então qualquer quadro diz o que se vê.

Lances (fontes conferidas na peça certa: lab/formato_novo/cf_chamaovar_rotina_fixador/storyboard_v3.json):
  1. segurar no fixador pra levantar -> ANULADO (fx_sentar_levantar);
  2. cadeira baixa e fofinha -> ANULADO (fx_sentar_levantar) + replay da cadeira certa, sem fala;
  3. cobrir o fixador com capa de tecido -> VALIDADO (fx_dormir; fx_roupa).
Versão 3 (2ª rodada de revisão): a cadeira fofinha (o lance que mais contraria o palpite) passou para
o meio; a capa vem por último, perguntada como dúvida ("cobrir o fixador"); o porquê do VALIDADO é
mostrado (sem capa o lençol ENGANCHA no anel, com capa DESLIZA; a perna de quem dorme ao lado
encosta na capa); o âmbar acende SÓ o metal (nada de brilho sobre a pele, nenhum halo em articulação); o
quadro 0 é fechado no punho + haste + anéis; a CTA é de jogo ("ia errar o lance da cadeira").

O que a cena mostra (a palavra falada comanda o quadro — ANCORAS):
  * quadro 0: o lance 1 JÁ CONGELADO, bem perto: o PUNHO fechado na haste da frente do fixador
    (dedos e polegar visíveis, a haste acima e abaixo do punho) e os anéis ocupando metade do monitor,
    o metal aceso em âmbar (traço, sem brilho na pele), seta âmbar saindo da haste para cima, círculo
    de telestrador no punho, ícone de pausa; o gancho ACIMA do monitor e nenhum outro texto;
  * "VAR": o selo VAR entra, a imagem REBOBINA 0,5 s como fita e abre o plano; "Segurar": inclina e o
    punho fecha na haste; "fixador": o metal acende; "levantar": o quadril sai do assento puxado pela
    haste; "pode?": congela; "Anulado": carimbo; "alça": o punho ABRE e a mão vai, por cima, direto ao
    braço da cadeira (nunca volta ao aparelho); "Mão"/"cadeira": as mãos nos braços da cadeira (verdes,
    chip JEITO CERTO); "sobe": fica em pé; "perna livre": contorno verde;
  * "Cadeira" (LANCE 2): uma poltrona baixa, de almofada fofa; a pessoa senta e AFUNDA ("fofinha");
    "pode?": congela (círculo na almofada); "Anulado": carimbo; "baixa"/"macia": a almofada cede de
    novo, contorno âmbar NA ALMOFADA; "força": tenta levantar, a seta de esforço sobe e volta, o corpo
    cai de novo no fundo; "joelho": seta-ponteiro âmbar no joelho (sem halo); "aparelho": o metal acende
    e treme; replay (cortina do VAR) da cadeira certa — firme, com braços, mais alta — em verde;
  * "Cobrir" (LANCE 3): na cama, à noite, a pessoa deitada de lado (cabeça lisa, sem rosto), a perna do
    fixador fora do cobertor; "fixador": a câmera chega no aparelho; "com capa": a capa de tecido
    cai e envolve o aparelho; "pode?": congela; "Validado": carimbo; replay SEM capa: o lençol vem e
    ENGANCHA no anel de cima (perto; X âmbar, puxões) -> "não enrosca": COM capa, o lençol desliza liso
    por cima da capa inteira (verde, visto); "protege quem dorme ao lado": a perna de quem dorme junto
    (calça de pijama cor de camelo, meia listrada) sai do cobertor de lá, passa POR CIMA da capa, encosta
    (ondas verdes) e se acomoda;
  * apito final (curto, longo) e o monitor DESLIGA como TV antiga; "No seu caso": a equipe acende;
    "apita": o apito passa para a equipe; "equipe": o selo da série CHAMA O VAR; CTA de jogo.
Guardrails: pele OPACA de desenho, nenhum osso, nenhum exame, nenhum fundo preto, nenhum rosto, nenhum
sangue, nenhuma pele repuxada, nenhum sinal de dor (âmbar só em metal, almofada, setas e carimbo);
cores dos vereditos pela lógica do semáforo (âmbar/verde; vermelho não aparece); ciano = só grafismo do
VAR; dourado = só a legenda. A tela de VAR é desenho próprio (nenhum logo, vinheta ou grafismo de FIFA,
CBF ou emissora). Todo texto desenhado está em ep["tela"] (o render recusa o vídeo se não estiver). Cena
PRESA ao roteiro pelas palavras-âncora: roteiro sem elas = KeyError, não vídeo torto.

Render próprio (cópia do cf_comum.fazer_render) com passos a mais, todos SÓ inserindo silêncio (nada da
fala é cortado): vão fixo entre o fim de cada "pode?" e o veredito (CHECANDO), vão antes de "Cobrir"
(replay da cadeira certa), antes do 2º "não" (replay do lençol enganchando), antes de "No seu caso"
(apito final + TV desligando) e 0,25 s de apito antes da 1ª palavra; uma cópia de som.mixar que conhece
os efeitos novos; e uma cópia da legenda karaokê do cf_comum em que a palavra ativa cresce a partir do
PRÓPRIO CENTRO (no cf_comum ela cresce para a direita e encosta na seguinte — reportado ao dono).
"""
import math
import os

import numpy as np
import skia

from . import som, voz as _voz
from .base import codificar, previas as _previas
from .cf_alongamento import (ACO, ACO_ESC, ACO_HL, BG_OUT, CX, F_BLACK, F_REG, F_SEMI, H, OURO, PELE, W, aviao,
                             clamp, e_back, e_inout, e_out, larg_texto, lerp, lerpc, paint, prog, texto)
from .cf_comum import DISC, SIG
from .cf_fratura_cola import alinhar, comprimir, montar_blocos

# ------------------------------------------------------------------ sincronia com a fala
ANCORAS = {
    # lance 1 — segurar no fixador pra levantar
    "chama": ("chama", 1, False), "var": ("var", 1, False), "segurar": ("segurar", 1, False),
    "fix1": ("fixador", 1, False), "levantar": ("levantar", 1, False), "pode1": ("pode", 1, False),
    "anulado1": ("anulado", 1, False), "ap_alca": ("fixador", 2, False), "alca": ("alça", 1, False),
    "mao": ("mão", 1, False), "cadeira1": ("cadeira", 1, False), "sobe": ("sobe", 1, False),
    "perna": ("perna", 1, False), "livre": ("livre", 1, False),
    # lance 2 — cadeira baixa e fofinha
    "cadeira2": ("cadeira", 2, False), "baixa1": ("baixa", 1, False), "fofinha": ("fofinha", 1, False),
    "pode2": ("pode", 2, False), "anulado2": ("anulado", 2, False), "baixa2": ("baixa", 2, False),
    "macia": ("macia", 1, False), "demais": ("demais", 1, False), "forca": ("força", 1, False),
    "joelho": ("joelho", 1, False), "apf": ("fixador", 3, False),
    # lance 3 — cobrir o fixador com capa de tecido
    "cobrir": ("cobrir", 1, False), "fix2": ("fixador", 4, False), "com": ("com", 1, False),
    "capa": ("capa", 1, False), "pode3": ("pode", 3, False), "validado": ("validado", 1, False),
    "nao2": ("não", 2, False), "enrosca": ("enrosca", 1, False), "lencol": ("lençol", 1, False),
    "protege": ("protege", 1, False), "dorme": ("dorme", 1, False), "lado": ("lado", 1, False),
    # fim
    "no": ("no", 3, False), "caso": ("caso", 1, False), "quem": ("quem", 2, False), "apita": ("apita", 1, False),
    "equipe": ("equipe", 1, False), "manda": ("manda", 1, False),
}
FIM_DE = ("pode1", "pode2", "pode3", "livre", "lado", "apf", "alca", "equipe", "perna", "lencol", "capa")
DESTAQUE = {"var", "fixador", "alça", "livre", "fofinha", "demais", "joelho", "capa", "enrosca", "apita", "equipe"}

# rótulos (todos estão em ep["tela"])
T_VAR = "VAR"
T_LANCE = ("LANCE 1", "LANCE 2", "LANCE 3")
T_CHEC = "CHECANDO"
T_ANUL = "ANULADO"
T_VALID = "VALIDADO"
T_CERTO = "JEITO CERTO"
T_SERIE = "CHAMA O VAR"
T_FIX = "FIXADOR"                 # (v4) a etiqueta do telestrador que dá nome ao objeto

# ------------------------------------------------------------------ paleta (identidade própria da série)
ARD_IN, ARD_OUT = "#22303F", "#121A24"          # ardósia, não o azul-marinho do COMO FUNCIONA
CIANO = "#4FD1FF"                              # só grafismo do VAR
VERDE = "#3DDC84"                              # VALIDADO / jeito certo
AMBAR = "#FFA53A"                              # ANULADO (nunca vermelho)
CARTAO = "#0B1824"
SELO_BG = "#1E2A44"
PELE_CL, PELE_ESC, PELE_LINHA = "#F7CDB8", "#D9937A", "#B9765E"
CAMISA, CAMISA_CL, CAMISA_ESC = "#5B7A99", "#7898B8", "#45607B"
SHORT, SHORT_CL, SHORT_ESC = "#3E5C76", "#557595", "#2C4459"
CABELO = "#4A3426"
CABELO2 = "#2E2A2A"
PAREDE_A, PAREDE_B = "#E2E8EE", "#C8D2DC"
RODAPE = "#A9B5C1"
PISO, PISO_CL, PISO_ESC = "#B9875C", "#CB9A6E", "#93653F"
MAD, MAD_CL, MAD_ESC = "#6E4C33", "#8E6646", "#4F3422"
ESTOFADO, ESTOFADO_CL, ESTOFADO_ESC = "#4F7480", "#6B929E", "#385660"
FOFO, FOFO_CL, FOFO_ESC = "#C9973F", "#E0B866", "#9C7024"     # cadeira baixa e macia (mostarda)
CAPA, CAPA_CL, CAPA_ESC = "#8E7FB8", "#B2A6D6", "#685A92"     # capa de tecido (lilás de malha)
COBERTOR, COBERTOR_CL, COBERTOR_ESC = "#4D78B0", "#6690C6", "#3B5F8E"
LENCOL, LENCOL_ESC = "#F6F9FC", "#D5DFEA"
TEAL = "#5FC4B6"

TONS_PELE = (PELE_ESC, PELE, PELE_CL, PELE, PELE_ESC)
TONS_CAMISA = (CAMISA_ESC, CAMISA, CAMISA_CL, CAMISA, CAMISA_ESC)
TONS_SHORT = (SHORT_ESC, SHORT, SHORT_CL, SHORT, SHORT_ESC)

# ------------------------------------------------------------------ o monitor (janela da cena)
# o gancho fica INTEIRO acima do monitor (linhas em y 168/250); a cena fica acima de y 1230 (karaokê)
JX0, JY0, JX1, JY1 = 28.0, 300.0, 1052.0, 1226.0
JCX, JCY = (JX0 + JX1) / 2, (JY0 + JY1) / 2
JAN = skia.Rect(JX0, JY0, JX1, JY1)
JAN_R = 26


# ------------------------------------------------------------------ utilidades
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
    """Seta reta com contorno escuro (lê sobre parede clara). (cópia adaptada do cf_andador)"""
    if a <= 0 or math.hypot(x1 - x0, y1 - y0) < 2:
        return
    ang = math.atan2(y1 - y0, x1 - x0)
    xb, yb = x1 - tam * 0.55 * math.cos(ang), y1 - tam * 0.55 * math.sin(ang)
    cv.drawLine(x0, y0, xb, yb, paint(CARTAO, int(170 * a), "stroke", larg + 8))
    ponta(cv, x1 + 4 * math.cos(ang), y1 + 4 * math.sin(ang), ang, tam + 10, CARTAO, 0.7 * a)
    cv.drawLine(x0, y0, xb, yb, paint(cor, int(255 * a), "stroke", larg))
    ponta(cv, x1, y1, ang, tam, cor, a)


def _trim(pt, k):
    """Traço desenhado até a fração k (TrimPathEffect devolve None em k = 0). (cópia do cf_crianca_mancando)"""
    if k < 0.999:
        pe = skia.TrimPathEffect.Make(0.0, max(0.002, k))
        if pe is not None:
            pt.setPathEffect(pe)
    return pt


def ik2(a, b, L1, L2, lado):
    """Cinemática inversa de 2 ossos: junta do meio e ponta efetivamente alcançada.
    lado = +1 dobra a junta para a frente/cima (joelho de quem olha para a direita), -1 para trás (cotovelo)."""
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


_CACHE = {}
LINEAR = skia.SamplingOptions(skia.FilterMode.kLinear)


def cacheado(chave, w, h, desenha):
    """Camada estática desenhada uma vez só (o raster do skia aqui é lento para degradês e desfoques)."""
    if chave not in _CACHE:
        sf = skia.Surface(int(w), int(h)); c = sf.getCanvas(); c.clear(skia.ColorTRANSPARENT)
        desenha(c)
        _CACHE[chave] = sf.makeImageSnapshot()
    return _CACHE[chave]


# ------------------------------------------------------------------ câmera (vista de lado)
def aplica(cv, cam):
    s, fx, fy = cam
    cv.translate(JCX, JCY); cv.scale(s, s); cv.translate(-fx, -fy)


def na_tela(cam, x, y):
    s, fx, fy = cam
    return JCX + (x - fx) * s, JCY + (y - fy) * s


# ================================================================== CENÁRIO (lances 1 e 3)
PISO_Y = 1170.0          # onde a sola encosta
PAREDE_Y = 1092.0        # rodapé
SALA_X0, SALA_Y0, SALA_X1, SALA_Y1, SALA_ESC = -60.0, 160.0, 1120.0, 1320.0, 1.6


def sala(cv):
    def _d(c):
        c.scale(SALA_ESC, SALA_ESC); c.translate(-SALA_X0, -SALA_Y0); _sala(c)
    img = cacheado("sala", (SALA_X1 - SALA_X0) * SALA_ESC, (SALA_Y1 - SALA_Y0) * SALA_ESC, _d)
    cv.save(); cv.translate(SALA_X0, SALA_Y0); cv.scale(1 / SALA_ESC, 1 / SALA_ESC)
    cv.drawImage(img, 0, 0, LINEAR)
    cv.restore()


def _sala(cv):
    sh = skia.GradientShader.MakeLinear([skia.Point(0, 150), skia.Point(0, PAREDE_Y)], [_c(PAREDE_A), _c(PAREDE_B)])
    cv.drawRect(skia.Rect(-600, -400, 1700, PAREDE_Y), paint(PAREDE_A, shader=sh))
    # janela da casa (luz do dia) — ajuda a ler "casa", sem texto
    jx0, jy0, jx1, jy1 = 770, 300, 1000, 640
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(jx0 - 14, jy0 - 14, jx1 + 14, jy1 + 14), 8, 8), paint("#F7F9FB"))
    vid = skia.GradientShader.MakeLinear([skia.Point(jx0, jy0), skia.Point(jx1, jy1)], [_c("#BFE3F7"), _c("#E9F6FD")])
    cv.drawRect(skia.Rect(jx0, jy0, jx1, jy1), paint("#CFEAF8", shader=vid))
    cv.drawLine((jx0 + jx1) / 2, jy0, (jx0 + jx1) / 2, jy1, paint("#F7F9FB", 255, "stroke", 12))
    cv.drawLine(jx0, (jy0 + jy1) / 2, jx1, (jy0 + jy1) / 2, paint("#F7F9FB", 255, "stroke", 12))
    cv.drawRect(skia.Rect(jx0 - 24, jy1 + 10, jx1 + 24, jy1 + 26), paint("#E7ECF1"))
    # rodapé e piso de madeira
    cv.drawRect(skia.Rect(-600, PAREDE_Y - 16, 1700, PAREDE_Y), paint(RODAPE))
    shp = skia.GradientShader.MakeLinear([skia.Point(0, PAREDE_Y), skia.Point(0, 1400)], [_c(PISO_ESC), _c(PISO_CL)])
    cv.drawRect(skia.Rect(-600, PAREDE_Y, 1700, 1700), paint(PISO, shader=shp))
    y, k = PAREDE_Y, 0
    while y < 1700:
        cv.drawLine(-600, y, 1700, y, paint(PISO_ESC, 150, "stroke", 2))
        for x0 in range(-600 + (k % 3) * 140, 1700, 420):
            cv.drawLine(x0, y, x0, y + 16 + k * 7, paint(PISO_ESC, 110, "stroke", 2))
        y += 16 + k * 7; k += 1
    cv.drawRect(skia.Rect(-600, PAREDE_Y, 1700, PAREDE_Y + 26), paint("#000000", 40, blur=8))


def cadeira(cv, parte, verde=0.0, verde_assento=0.0):
    """Cadeira firme, com braços e não muito baixa (fx_sentar_levantar), de perfil.
    parte = 'fundo' (encosto, assento, pernas, braço do lado de lá) ou 'frente' (braço do lado de cá)."""
    if parte == "fundo":
        cv.drawRect(skia.Rect(238, PISO_Y - 6, 520, PISO_Y + 10), paint("#000000", 55, blur=10))
        cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(256, 764, 474, 784), 10, 10), paint(esc_cor(MAD, 0.25)))
        cv.drawRect(skia.Rect(440, 780, 454, 940), paint(esc_cor(MAD, 0.25)))
        for x0 in (252, 476):
            cv.drawRect(skia.Rect(x0, 990, x0 + 18, PISO_Y + 2), paint(MAD_ESC))
        cv.drawRect(skia.Rect(246, 540, 268, 990), paint(MAD))
        cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(256, 588, 300, 936), 18, 18), paint(ESTOFADO_ESC))
        cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(262, 596, 292, 926), 14, 14), paint(ESTOFADO))
        cv.drawCircle(257, 540, 13, paint(MAD))
        if verde_assento > 0:
            cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(244, 930, 510, 1000), 18, 18),
                         paint(VERDE, int(140 * verde_assento), blur=12))
        cv.drawRect(skia.Rect(250, 978, 500, 996), paint(MAD))
        cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(250, 936, 504, 982), 16, 16), paint(ESTOFADO))
        cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(256, 938, 500, 952), 7, 7), paint(ESTOFADO_CL, 200))
        if verde_assento > 0:
            cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(250, 936, 504, 996), 16, 16),
                         paint(VERDE, int(255 * verde_assento), "stroke", 5))
            for x0 in (252, 476):
                cv.drawRect(skia.Rect(x0, 996, x0 + 18, PISO_Y + 2), paint(VERDE, int(200 * verde_assento), "stroke", 4))
    else:
        if verde > 0:
            cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(250, 762, 492, 802), 18, 18), paint(VERDE, int(150 * verde), blur=14))
        cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(254, 774, 484, 798), 12, 12), paint(MAD))
        cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(258, 776, 480, 784), 4, 4), paint(MAD_CL, 220))
        cv.drawRect(skia.Rect(452, 796, 468, 938), paint(MAD))
        if verde > 0:
            cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(254, 774, 484, 798), 12, 12), paint(VERDE, int(255 * verde), "stroke", 5))
            cv.drawRect(skia.Rect(452, 796, 468, 938), paint(VERDE, int(220 * verde), "stroke", 4))


# ================================================================== A PESSOA (de perfil, sem rosto)
COXA, CANELA, TRONCO, BRACO, ANTEB = 232.0, 222.0, 245.0, 148.0, 150.0
HR = 50.0
TORN_Y = PISO_Y - 32.0
ANEIS_S = (0.17, 0.48, 0.80)        # posição dos 3 anéis ao longo da canela (joelho = 0, tornozelo = 1)
RA, RB = 70.0, 13.0                 # anel visto quase de lado: elipse estreita perpendicular à canela
S_PEGA = 0.33                       # onde o punho agarra a haste da frente (entre o 1º e o 2º anel)


def shin_frame(knee, ank):
    dx, dy = ank[0] - knee[0], ank[1] - knee[1]; L = math.hypot(dx, dy) or 1.0
    d = (dx / L, dy / L); f = (d[1], -d[0])        # d: ao longo da canela; f: para a frente (dedos)
    return d, f, L


def canela_path(knee, ank):
    """Canela de perfil: frente quase reta (a tíbia), panturrilha abaulada atrás."""
    d, f, L = shin_frame(knee, ank)
    fr, tr = [], []
    for i in range(15):
        s = i / 14
        wf = lerp(29, 19, s)
        wb = 30 + 15 * math.sin(math.pi * clamp(s / 0.7)) ** 1.3 - 9 * s
        c = (knee[0] + d[0] * L * s, knee[1] + d[1] * L * s)
        fr.append((c[0] + f[0] * wf, c[1] + f[1] * wf)); tr.append((c[0] - f[0] * wb, c[1] - f[1] * wb))
    p = poli(fr + tr[::-1])
    k = skia.Path(); k.addCircle(knee[0], knee[1], 30)
    a = skia.Path(); a.addCircle(ank[0], ank[1], 20)
    return uniao(p, k, a)


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


def anel_lado(cv, c, f, metade, a, brilho=-1.0):
    """Anel do fixador visto quase de lado (cópia redesenhada do anel do cf_alongamento, em escala)."""
    if a <= 0:
        return
    ang = math.degrees(math.atan2(f[1], f[0]))
    cv.save(); cv.translate(c[0], c[1]); cv.rotate(ang)
    r = skia.Rect(-RA, -RB, RA, RB)
    if metade == "tras":
        cv.drawArc(r, 180, 180, False, paint(ACO_ESC, int(255 * a), "stroke", 9))
    else:
        cv.drawArc(r, 0, 180, False, paint("#000000", int(70 * a), "stroke", 12, blur=4))
        cv.drawArc(r, 0, 180, False, paint(ACO, int(255 * a), "stroke", 9))
        cv.drawArc(skia.Rect(-RA + 4, -RB + 3, RA - 4, RB - 1), 25, 130, False, paint(ACO_HL, int(170 * a), "stroke", 2.2))
        if 0 < brilho < 1:                       # reflexo de metal correndo pelo arco da frente
            u = brilho; ang0 = lerp(160, 20, u) - 14; aa = math.sin(math.pi * u)
            cv.drawArc(r, ang0, 30, False, paint("#FFFFFF", int(170 * a * aa), "stroke", 18, blur=6))
            cv.drawArc(r, ang0, 26, False, paint("#FFFFFF", int(255 * a * aa), "stroke", 5))
    cv.restore()


def _hastes(knee, ank):
    d, f, L = shin_frame(knee, ank)
    cs = [(knee[0] + d[0] * L * s, knee[1] + d[1] * L * s) for s in ANEIS_S]
    out = []
    for lado in (1, -1):
        p0 = (cs[0][0] + f[0] * lado * (RA - 3) - d[0] * 16, cs[0][1] + f[1] * lado * (RA - 3) - d[1] * 16)
        p1 = (cs[-1][0] + f[0] * lado * (RA - 3) + d[0] * 16, cs[-1][1] + f[1] * lado * (RA - 3) + d[1] * 16)
        out.append((p0, p1))
    return cs, out, d, f


def fixador_lado(cv, knee, ank, a, fase, brilho=-1.0, alerta=0.0):
    """Fixador circular na canela: fase 'tras' (arcos de trás) ou 'frente' (pinos, hastes, arcos da frente).
    `alerta` (0..1): o aparelho inteiro acende em âmbar (o detalhe que o VAR julga)."""
    cs, hastes, d, f = _hastes(knee, ank)
    if fase == "tras":
        for c in cs:
            anel_lado(cv, c, f, "tras", a)
            if alerta > 0:                               # o metal de trás também acende (traço, sem brilho)
                ang = math.degrees(math.atan2(f[1], f[0]))
                cv.save(); cv.translate(c[0], c[1]); cv.rotate(ang)
                cv.drawArc(skia.Rect(-RA, -RB, RA, RB), 180, 180, False, paint(AMBAR, int(230 * alerta * a), "stroke", 6))
                cv.restore()
        return cs
    # (v3) o "aceso" é SÓ no metal: nenhum brilho desfocado por trás do aparelho, que pintava a pele de laranja
    # pinos curtos do anel até a pele, com o pontinho de pele (sem repuxar, sem vermelho)
    for i, c in enumerate(cs):
        s = ANEIS_S[i]
        wf = lerp(29, 19, s); wb = 30 + 15 * math.sin(math.pi * clamp(s / 0.7)) ** 1.3 - 9 * s
        for lado, w in ((1, wf), (-1, wb)):
            p0 = (c[0] + f[0] * lado * (RA - 10), c[1] + f[1] * lado * (RA - 10))
            p1 = (c[0] + f[0] * lado * (w - 3), c[1] + f[1] * lado * (w - 3))
            cv.drawLine(p0[0], p0[1], p1[0], p1[1], paint("#000000", int(70 * a), "stroke", 8, blur=3))
            cv.drawLine(p0[0], p0[1], p1[0], p1[1], paint("#C6D3DF", int(255 * a), "stroke", 6))
            cv.drawCircle(p1[0], p1[1], 6.5, paint("#E7A98D", int(255 * a)))
            cv.drawCircle(p1[0], p1[1], 6.5, paint("#F6C9B4", int(200 * a), "stroke", 1.8))
        cv.drawCircle(c[0] + d[0] * 2, c[1] + d[1] * 2, 7, paint("#E7A98D", int(255 * a)))
        cv.drawCircle(c[0] + d[0] * 2, c[1] + d[1] * 2, 7, paint("#F6C9B4", int(200 * a), "stroke", 1.8))
        cv.drawLine(c[0] + d[0] * 2, c[1] + d[1] * 2, c[0] + d[0] * (RB - 1), c[1] + d[1] * (RB - 1),
                    paint("#C6D3DF", int(255 * a), "stroke", 5))
    # hastes nos dois extremos (frente e trás), com porcas de aço
    for k, (p0, p1) in enumerate(hastes):
        lado = (1, -1)[k]
        cv.drawLine(p0[0], p0[1], p1[0], p1[1], paint("#000000", int(70 * a), "stroke", 10, blur=3))
        cv.drawLine(p0[0], p0[1], p1[0], p1[1], paint("#8FA3B8", int(255 * a), "stroke", 7))
        cv.drawLine(p0[0] - f[0] * 2, p0[1] - f[1] * 2, p1[0] - f[0] * 2, p1[1] - f[1] * 2,
                    paint(ACO_HL, int(140 * a), "stroke", 1.6))
        if alerta > 0:                                   # a haste vira âmbar (traço do tamanho dela)
            cv.drawLine(p0[0], p0[1], p1[0], p1[1], paint(AMBAR, int(255 * alerta * a), "stroke", 7))
            cv.drawLine(p0[0] - f[0] * 1.5, p0[1] - f[1] * 1.5, p1[0] - f[0] * 1.5, p1[1] - f[1] * 1.5,
                        paint("#FFE2B8", int(220 * alerta * a), "stroke", 1.8))
        for c in cs:
            q = (c[0] + f[0] * lado * (RA - 3), c[1] + f[1] * lado * (RA - 3))
            for sgn in (-1, 1):
                qq = (q[0] + d[0] * sgn * 12, q[1] + d[1] * sgn * 12)
                cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(qq[0] - 9, qq[1] - 6, qq[0] + 9, qq[1] + 6), 3, 3),
                             paint(ACO_ESC, int(255 * a)))
    for c in cs:
        anel_lado(cv, c, f, "frente", a, brilho)
        if alerta > 0:                                   # o arco da frente do anel vira âmbar (sem halo)
            ang = math.degrees(math.atan2(f[1], f[0]))
            cv.save(); cv.translate(c[0], c[1]); cv.rotate(ang)
            cv.drawArc(skia.Rect(-RA, -RB, RA, RB), 0, 180, False, paint(AMBAR, int(255 * alerta * a), "stroke", 9))
            cv.drawArc(skia.Rect(-RA + 4, -RB + 3, RA - 4, RB - 1), 25, 130, False,
                       paint("#FFE2B8", int(200 * alerta * a), "stroke", 2.2))
            cv.restore()
    return cs


def ponto_pega(knee, ank):
    """Ponto da haste da frente onde o punho fecha + o referencial da canela."""
    d, f, L = shin_frame(knee, ank)
    c = (knee[0] + d[0] * L * S_PEGA, knee[1] + d[1] * L * S_PEGA)
    return (c[0] + f[0] * (RA - 3), c[1] + f[1] * (RA - 3)), d, f


def punho(cv, p, d, f, tons, a, esc=1.0):
    """Mão FECHADA em volta da haste: dorso, os nós dos 4 dedos para fora da haste, os vincos entre os
    dedos e o polegar cruzando por cima. A haste continua visível acima e abaixo do punho."""
    if a <= 0:
        return
    m = skia.Matrix(); m.setAll(f[0] * esc, d[0] * esc, p[0], f[1] * esc, d[1] * esc, p[1], 0, 0, 1)
    cv.save(); cv.concat(m)
    corpo_p = rr_path(-24, -31, 22, 31, 17)
    for v in (-20, -6.5, 7, 20.5):                       # nós dos dedos (do lado de fora da haste)
        k = skia.Path(); k.addCircle(21, v, 10); corpo_p = uniao(corpo_p, k)
    cv.drawPath(corpo_p, paint("#000000", int(60 * a), blur=6))
    pinta(cv, corpo_p, (0, -31), (0, 31), 56, tons, a, linha=PELE_LINHA, larg_linha=2.6)
    for v in (-13.2, 0.3, 13.8):                        # vincos entre os dedos
        cv.drawLine(31, v, 9, v + 2, paint(PELE_LINHA, int(220 * a), "stroke", 2.6))
    for v in (-20, -6.5, 7, 20.5):                       # brilho nos nós
        cv.drawCircle(24, v - 3, 3.2, paint(PELE_CL, int(200 * a)))
    pol = capsula((-18, -27), (13, -36), 18, 15)          # polegar por cima, cruzando a haste
    pinta(cv, pol, (-18, -27), (13, -36), 18, tons, a, linha=PELE_LINHA, larg_linha=2.4)
    cv.drawOval(skia.Rect(5, -42, 18, -32), paint(PELE_CL, int(220 * a)))
    cv.restore()


def mao(cv, p, dirx, diry, garra, tons, a):
    """Mão: punho fechado e redondo (garra 1) ou mão aberta, espalmada (garra 0). Sem dedos detalhados."""
    L = math.hypot(dirx, diry) or 1.0; ux, uy = dirx / L, diry / L
    comp = lerp(30, 6, garra); larg = lerp(27, 44, garra)
    q0 = (p[0] - ux * comp * 0.5, p[1] - uy * comp * 0.5); q1 = (p[0] + ux * comp * 0.5, p[1] + uy * comp * 0.5)
    pth = capsula(q0, q1, larg, larg * lerp(0.85, 1.0, garra))
    if garra > 0.3:
        nx, ny = -uy, ux
        pol = capsula((p[0] - ux * 6 + nx * 12, p[1] - uy * 6 + ny * 12), (p[0] + ux * 10 + nx * 16, p[1] + uy * 10 + ny * 16), 16, 14)
        pth = uniao(pth, pol)
    pinta(cv, pth, q0, q1, larg, tons, a, linha=PELE_LINHA, larg_linha=2)


def corpo(pose):
    """Esqueleto da pose: quadril, tronco, cabeça, joelhos, cotovelos, mãos (mundo)."""
    hip = pose["hip"]; al = pose["al"]
    up = (math.sin(al), -math.cos(al)); fw = (math.cos(al), math.sin(al))
    sh = (hip[0] + up[0] * TRONCO, hip[1] + up[1] * TRONCO)
    head = (sh[0] + up[0] * 78 + fw[0] * 10, sh[1] + up[1] * 78 + fw[1] * 10)
    ombro = (sh[0] - up[0] * 16 + fw[0] * 4, sh[1] - up[1] * 16 + fw[1] * 4)
    kN, aN = ik2(hip, pose["ankN"], COXA, CANELA, 1)
    kF, aF = ik2(hip, pose["ankF"], COXA, CANELA, 1)
    eN, hN = ik2(ombro, pose["mN"], BRACO, ANTEB, -1)
    eF, hF = ik2((ombro[0] - 6, ombro[1] - 4), pose["mF"], BRACO, ANTEB, -1)
    return dict(hip=hip, al=al, up=up, fw=fw, sh=sh, head=head, ombro=ombro, kN=kN, aN=aN, kF=kF, aF=aF,
                eN=eN, hN=hN, eF=eF, hF=hF)


def perna_desenho(cv, hip, knee, ank, tons, a, short=True, tons_short=TONS_SHORT):
    coxa = capsula(hip, knee, 78, 60)
    pinta(cv, coxa, hip, knee, 78, tons, a, linha=esc_cor(tons[0], 0.25))
    can = canela_path(knee, ank)
    pinta(cv, can, knee, ank, 70, tons, a, linha=esc_cor(tons[0], 0.25))
    pe = pe_path(ank)
    pinta(cv, pe, (ank[0] + 40, ank[1] - 20), (ank[0] + 40, ank[1] + 40), 60, tons, a, linha=esc_cor(tons[0], 0.25))
    if short:
        m = lerp2(hip, knee, 0.5)
        s = capsula(hip, m, 90, 82)
        pinta(cv, s, hip, m, 90, tons_short, a, linha=esc_cor(tons_short[0], 0.3))
    return coxa, can, pe


def braco_desenho(cv, ombro, cot, mao_p, garra, tons_pele, tons_camisa, a, pf=None):
    up = capsula(ombro, cot, 40, 34)
    pinta(cv, up, ombro, cot, 40, tons_pele, a, linha=esc_cor(tons_pele[0], 0.25))
    pulso = lerp2(cot, mao_p, 0.84 if pf is not None and garra > 0.5 else 0.82)
    fo = capsula(cot, pulso, 34, 27)
    pinta(cv, fo, cot, pulso, 34, tons_pele, a, linha=esc_cor(tons_pele[0], 0.25))
    mg = lerp2(ombro, cot, 0.52)
    manga = capsula(ombro, mg, 54, 48)
    pinta(cv, manga, ombro, mg, 54, tons_camisa, a, linha=esc_cor(tons_camisa[0], 0.3))
    if pf is not None and garra > 0.5:
        punho(cv, mao_p, pf[0], pf[1], tons_pele, a, esc=lerp(0.92, 1.0, (garra - 0.5) * 2))
    else:
        mao(cv, mao_p, mao_p[0] - cot[0], mao_p[1] - cot[1], 0.0, tons_pele, a)


def cabeca(cv, head, al, up, fw, a, cabelo=CABELO, tons=None):
    """Cabeça: círculo liso, sem rosto; cabelo atrás e em cima (mostra para onde a pessoa olha)."""
    sh_c = skia.GradientShader.MakeRadial(skia.Point(head[0] + fw[0] * 14 + up[0] * 12, head[1] + fw[1] * 14 + up[1] * 12),
                                          HR * 1.4, [_c(PELE_CL), _c(PELE), _c(PELE_ESC)], [0.0, 0.55, 1.0])
    cv.drawCircle(head[0], head[1], HR, paint(PELE, int(255 * a), shader=sh_c))
    cv.drawCircle(head[0], head[1], HR, paint(PELE_LINHA, int(180 * a), "stroke", 2.5))
    cv.save(); cv.translate(head[0], head[1]); cv.rotate(math.degrees(al))
    cab = skia.Path(); cab.addCircle(0, 0, HR + 3)
    cl = skia.Path(); cl.moveTo(-70, 30); cl.lineTo(-70, -70); cl.lineTo(30, -70); cl.lineTo(22, -24)
    cl.cubicTo(6, -18, -14, -6, -22, 30); cl.close()
    cab = skia.Op(cab, cl, skia.PathOp.kIntersect_PathOp)
    if cab is not None:
        cv.drawPath(cab, paint(cabelo, int(255 * a)))
    cv.restore()


def tronco_cabeca(cv, b, a):
    hip, sh, up, fw, head = b["hip"], b["sh"], b["up"], b["fw"], b["head"]
    pes = (sh[0] + up[0] * 40, sh[1] + up[1] * 40)
    pinta(cv, capsula(sh, pes, 40, 38), sh, pes, 40, TONS_PELE, a)
    tr = capsula((hip[0] + up[0] * 20, hip[1] + up[1] * 20), (sh[0] - up[0] * 12, sh[1] - up[1] * 12), 112, 120)
    pinta(cv, tr, hip, sh, 120, TONS_CAMISA, a, linha=esc_cor(CAMISA_ESC, 0.3))
    q = (hip[0] + up[0] * 46, hip[1] + up[1] * 46)
    sp = capsula(hip, q, 108, 112)
    pinta(cv, sp, hip, q, 112, TONS_SHORT, a, linha=esc_cor(SHORT_ESC, 0.3))
    cabeca(cv, head, b["al"], up, fw, a)


def pessoa(cv, pose, a=1.0, camadas=("fundo", "corpo", "frente"), verde_livre=0.0, brilho=-1.0, bracos=True,
           alerta=0.0, capa_fn=None, treme=(0.0, 0.0)):
    """Desenha a pessoa em camadas (a cadeira entra entre elas). Devolve o esqueleto."""
    b = corpo(pose)
    TP_F = tons_escuros(TONS_PELE, 0.16); TS_F = tons_escuros(TONS_SHORT, 0.15); TC_F = tons_escuros(TONS_CAMISA, 0.16)
    if "fundo" in camadas:
        if verde_livre > 0:                                  # contorno verde na perna livre
            pth = uniao(capsula(b["hip"], b["kF"], 78, 60), canela_path(b["kF"], b["aF"]), pe_path(b["aF"]))
            cv.drawPath(pth, paint(VERDE, int(150 * verde_livre), "stroke", 22, blur=8))
            cv.drawPath(pth, paint(VERDE, int(255 * verde_livre), "stroke", 7))
        perna_desenho(cv, b["hip"], b["kF"], b["aF"], TP_F, a, tons_short=TS_F)
        if bracos:
            braco_desenho(cv, (b["ombro"][0] - 6, b["ombro"][1] - 4), b["eF"], b["hF"], pose["gF"], TP_F, TC_F, a)
    if "corpo" in camadas:
        tronco_cabeca(cv, b, a)
        coxa = capsula(b["hip"], b["kN"], 78, 60)
        pinta(cv, coxa, b["hip"], b["kN"], 78, TONS_PELE, a, linha=esc_cor(PELE_ESC, 0.25))
        m = lerp2(b["hip"], b["kN"], 0.52)
        pinta(cv, capsula(b["hip"], m, 92, 84), b["hip"], m, 92, TONS_SHORT, a, linha=esc_cor(SHORT_ESC, 0.3))
    if "perna" in camadas:
        jx, jy = treme
        cv.save(); cv.translate(jx, jy)
        fixador_lado(cv, b["kN"], b["aN"], a, "tras", alerta=alerta)
        cv.restore()
        pinta(cv, canela_path(b["kN"], b["aN"]), b["kN"], b["aN"], 70, TONS_PELE, a, linha=esc_cor(PELE_ESC, 0.25))
        pinta(cv, pe_path(b["aN"]), (b["aN"][0] + 40, b["aN"][1] - 20), (b["aN"][0] + 40, b["aN"][1] + 40), 60,
              TONS_PELE, a, linha=esc_cor(PELE_ESC, 0.25))
        cv.save(); cv.translate(jx, jy)
        fixador_lado(cv, b["kN"], b["aN"], a, "frente", brilho, alerta)
        cv.restore()
        if capa_fn is not None:
            capa_fn(cv, b["kN"], b["aN"])
    if "braco" in camadas:
        pf = None
        if pose.get("punho"):
            _, d, f = ponto_pega(b["kN"], b["aN"])
            pf = (d, f)
        braco_desenho(cv, b["ombro"], b["eN"], b["hN"], pose["gN"], TONS_PELE, TONS_CAMISA, a, pf)
    return b


def _na_coxa(hip, ank, frac=0.62, alto=36):
    k, _ = ik2(hip, ank, COXA, CANELA, 1)
    dx, dy = k[0] - hip[0], k[1] - hip[1]; L = math.hypot(dx, dy) or 1.0
    nx, ny = dy / L, -dx / L
    return (hip[0] + dx * frac + nx * alto, hip[1] + dy * frac + ny * alto)


# ================================================================== LANCE 1 — segurar no aparelho pra levantar
REST_HIP = (332.0, 912.0)
PUXA_HIP = (398.0, 816.0)      # o quadril SAI do assento, puxado pela haste
ANK_N = (594.0, TORN_Y)        # perna do aparelho à frente, apoiada
ANK_F = (464.0, TORN_Y)        # perna livre, dobrada sob o assento
APOIO_N = (452.0, 770.0)       # mão no braço da cadeira (lado de cá)
APOIO_F = (440.0, 762.0)
EM_PE_HIP = (472.0, 702.0)


def _pega(hip):
    kN, aN = ik2(hip, ANK_N, COXA, CANELA, 1)
    return ponto_pega(kN, aN)[0]


def _pe_l1(t, T, u_ini, h_ini, al_ini):
    """Levantar do jeito certo: inclina, sobe pela perna livre e fica em pé (u 0..1)."""
    ua = e_inout(clamp(u_ini / 0.38)); ub = e_inout(clamp((u_ini - 0.28) / 0.72))
    h1 = (h_ini[0] + 34 * ua, h_ini[1] - 4 * ua)
    return lerp2(h1, EM_PE_HIP, ub), lerp(lerp(al_ini, 0.62, ua), 0.03, ub)


def pose_l1(t, T):
    var, seg, ap1, lev, pode = T["var"], T["segurar"], T["fix1"], T["levantar"], T["pode1"]
    alca, mao_t, cad, sobe = T["alca"], T["mao"], T["cadeira1"], T["sobe"]
    # ---- o lance como ele é (errado): inclinar, agarrar a haste, puxar o corpo pela haste
    if t < var:
        lean = grab = pull = 1.0
    elif t < var + 0.5:                                    # rebobina: desfaz na ordem inversa
        u = 1 - prog(t, var, var + 0.5)
        pull = clamp(u * 3 - 2); grab = clamp(u * 3 - 1); lean = clamp(u * 3)
    else:
        lean = e_inout(prog(t, seg - 0.12, seg + 0.4))
        grab = e_inout(prog(t, seg + 0.02, ap1 + 0.12))
        pull = e_inout(prog(t, lev - 0.08, pode + 0.02))
    hip = lerp2(REST_HIP, PUXA_HIP, pull)
    al = 0.05 + 0.70 * lean + 0.33 * pull          # inclina MUITO: a mão alcança a haste no meio da canela
    m_rest = _na_coxa(hip, ANK_N); m_f_rest = _na_coxa(hip, ANK_F, 0.55, 30)
    pega = _pega(hip)
    arco = math.sin(math.pi * grab) * 40
    mN = (lerp(m_rest[0], pega[0], grab), lerp(m_rest[1], pega[1], grab) - arco)
    gN = clamp((grab - 0.72) / 0.28)
    mF = m_f_rest; gF = 0.0
    punho_on = True
    # ---- o jeito certo: solta ("alça"), volta a sentar, mãos nos braços da cadeira, sobe pela perna livre
    if t >= alca - 0.04:
        solta = prog(t, alca - 0.04, alca + 0.1)
        gN = 1 - solta
        punho_on = solta < 0.5
        volta = e_inout(prog(t, alca + 0.1, mao_t + 0.05))
        hip = lerp2(hip, REST_HIP, volta); al = lerp(al, 0.22, volta)
        # (v3) a mão que soltou vai DIRETO ao braço da cadeira, num arco por cima: nunca volta a pousar
        # no anel nem no joelho (a imagem não pode desdizer "o aparelho não é alça")
        p0 = _pega(hip)
        ctrl = ((p0[0] + APOIO_N[0]) / 2 + 30, (p0[1] + APOIO_N[1]) / 2 - 70)
        u = e_inout(prog(t, alca + 0.02, mao_t + 0.12))
        q = ((1 - u) ** 2 * p0[0] + 2 * (1 - u) * u * ctrl[0] + u * u * APOIO_N[0],
             (1 - u) ** 2 * p0[1] + 2 * (1 - u) * u * ctrl[1] + u * u * APOIO_N[1])
        mN = q
        braco = e_inout(prog(t, mao_t - 0.08, cad + 0.12))
        mF = lerp2(_na_coxa(hip, ANK_F, 0.55, 30), APOIO_F, braco)
    u = prog(t, sobe, sobe + 0.95)
    if u > 0:
        hip, al = _pe_l1(t, T, u, REST_HIP, 0.22)
        b = corpo(dict(hip=hip, al=al, ankN=ANK_N, ankF=ANK_F, mN=(0, 0), mF=(0, 0), gN=0, gF=0))
        pend = (b["ombro"][0] + 22, b["ombro"][1] + (BRACO + ANTEB) * 0.93)
        k = e_inout(clamp((u - 0.5) / 0.4))
        mN = lerp2(APOIO_N, pend, k); mF = lerp2(APOIO_F, (pend[0] - 10, pend[1] - 4), k)
    return dict(hip=hip, al=al, ankN=ANK_N, ankF=ANK_F, mN=mN, mF=mF, gN=gN, gF=gF, pull=pull, pega=pega,
                punho=punho_on and gN > 0.5)


CAM_L1_ABERTA = (1.0, 520.0, 760.0)            # replay do jeito certo: a pessoa inteira, de pé
CAM_L1_JOGO = (1.14, 500.0, 828.0)             # o lance rodando: sentada, maior na tela


CAM_L1_Q0 = (2.45, 622.0, 1012.0)             # quadro 0: punho + haste + anéis ocupando metade do monitor


def cam_l1(t, T, pose):
    pe = pose["pega"]
    perto = (1.5, pe[0] - 84, pe[1] - 110)
    if t < T["var"]:
        return CAM_L1_Q0
    cam = lerp3(CAM_L1_Q0, CAM_L1_JOGO, e_inout(prog(t, T["var"], T["var"] + 0.5)))
    cam = lerp3(cam, perto, e_inout(prog(t, T["pode1"], T["pode1"] + 0.32)))      # congela: chega perto do punho
    cheg = prog(t, T["pode1_fim"], T["anulado1"])                               # CHECANDO: a câmera chega devagar
    cam = (cam[0] * (1 + 0.08 * e_inout(cheg)), cam[1] + 10 * cheg, cam[2] + 6 * cheg)
    cam = lerp3(cam, CAM_L1_JOGO, e_inout(prog(t, T["alca"] + 0.1, T["mao"] + 0.1)))
    return lerp3(cam, CAM_L1_ABERTA, e_inout(prog(t, T["sobe"] - 0.15, T["sobe"] + 0.5)))


def alerta_l1(t, T):
    if t < T["var"]:
        return 1.0
    a = janela(t, T["fix1"], T["alca"], 0.25, 0.3) if t >= T["var"] + 0.5 else 1 - prog(t, T["var"], T["var"] + 0.2)
    return a


def cena_l1(cv, t, T, cam=None):
    pose = pose_l1(t, T)
    cam = cam or cam_l1(t, T, pose)
    cv.save(); aplica(cv, cam)
    sala(cv)
    verde_braco = janela(t, T["mao"] - 0.05, T["livre"] + 0.3, 0.25, 0.3)
    cadeira(cv, "fundo")
    vl = janela(t, T["perna"] - 0.08, T["cadeira2"] - 0.3, 0.2, 0.2)
    vl = vl * (0.75 + 0.25 * math.sin(max(0.0, t - T["livre"]) * 12)) if t > T["livre"] else vl
    br = prog(t, T["ap_alca"] - 0.05, T["ap_alca"] + 0.55)
    b = pessoa(cv, pose, camadas=("fundo",), verde_livre=vl)
    pessoa(cv, pose, camadas=("corpo",))
    cadeira(cv, "frente", verde_braco)
    al1 = min(1.0, alerta_l1(t, T))
    if t >= T["var"]:                                     # o metal pisca forte no carimbo (só o traço)
        al1 = min(1.0, al1 * (0.8 + 0.2 * math.cos(max(0.0, t - T["anulado1"]) * 18)
                              * max(0.0, 1 - abs(t - T["anulado1"] - 0.2) / 0.4)))
    pessoa(cv, pose, camadas=("perna",), brilho=br if 0 < br < 1 else -1, alerta=al1)
    pessoa(cv, pose, camadas=("braco",))
    # seta âmbar saindo da HASTE para cima: o corpo sobe puxando o aparelho
    a_s = janela(t, T["levantar"] - 0.05, T["anulado1"] + 0.1, 0.2, 0.3)
    if t < T["var"]:
        a_s = 1.0
    elif t < T["var"] + 0.5:
        a_s = 1 - prog(t, T["var"], T["var"] + 0.2)
    if a_s > 0:
        kN, aN = ik2(pose["hip"], ANK_N, COXA, CANELA, 1)
        g, d, f = ponto_pega(kN, aN)
        x0, y0 = g[0] + f[0] * 34 - d[0] * 20, g[1] + f[1] * 34 - d[1] * 20
        comp = 118 * e_out(clamp(a_s * 1.4))
        seta(cv, x0, y0, x0 - d[0] * comp, y0 - d[1] * comp, AMBAR, a_s, larg=11, tam=32)
    cv.restore()
    return cam, pose


# ================================================================== LANCE 3 (cama) — cobrir o fixador com capa de tecido
H2 = (430.0, 812.0)            # quadril de quem está deitado (a pessoa é desenhada EM PÉ e girada -90°)
POSE_DEITADA = dict(hip=H2, al=0.0, ankN=(H2[0] + 4, H2[1] + 452), ankF=(H2[0] - 4, H2[1] + 452),
                    mN=(H2[0] + 30, H2[1] + 90), mF=(H2[0] + 20, H2[1] + 90), gN=0, gF=0)
MAT_FUNDO, MAT_FRENTE, MAT_BAIXO = 832.0, 884.0, 948.0     # colchão: tampo (de trás p/ frente) e face da frente
CAMA_X0, CAMA_X1 = 34.0, 1040.0
_GIRO = skia.Matrix(); _GIRO.setRotate(-90, H2[0], H2[1])


def gira(p):
    """Ponto do desenho 'em pé' -> ponto da pessoa deitada (girada -90° em volta do quadril)."""
    return (H2[0] + (p[1] - H2[1]), H2[1] - (p[0] - H2[0]))


def deitar(cv):
    cv.translate(H2[0], H2[1]); cv.rotate(-90); cv.translate(-H2[0], -H2[1])


def quarto(cv):
    def _d(c):
        c.scale(SALA_ESC, SALA_ESC); c.translate(-SALA_X0, -SALA_Y0); _quarto(c)
    img = cacheado("quarto", (SALA_X1 - SALA_X0) * SALA_ESC, (SALA_Y1 - SALA_Y0) * SALA_ESC, _d)
    cv.save(); cv.translate(SALA_X0, SALA_Y0); cv.scale(1 / SALA_ESC, 1 / SALA_ESC)
    cv.drawImage(img, 0, 0, LINEAR)
    cv.restore()


def _quarto(cv):
    """Quarto à noite (azulado, nunca preto): parede, janela com lua, piso, cama de casal vista de lado,
    o travesseiro e a cabeça de quem dorme do lado de lá (sem rosto)."""
    sh = skia.GradientShader.MakeLinear([skia.Point(0, 150), skia.Point(0, 1062)], [_c("#AFC0D8"), _c("#93A6C2")])
    cv.drawRect(skia.Rect(-600, -400, 1700, 1062), paint("#A3B5CF", shader=sh))
    jx0, jy0, jx1, jy1 = 744, 352, 986, 600
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(jx0 - 14, jy0 - 14, jx1 + 14, jy1 + 14), 8, 8), paint("#DCE4EE"))
    vid = skia.GradientShader.MakeLinear([skia.Point(jx0, jy0), skia.Point(jx1, jy1)], [_c("#29406A"), _c("#3E5C8E")])
    cv.drawRect(skia.Rect(jx0, jy0, jx1, jy1), paint("#2F4A78", shader=vid))
    mx, my = jx0 + 70, jy0 + 70
    lua = skia.Path(); lua.addCircle(mx, my, 34)
    corte = skia.Path(); corte.addCircle(mx + 17, my - 11, 31)
    lua = skia.Op(lua, corte, skia.PathOp.kDifference_PathOp)
    cv.drawCircle(mx, my, 56, paint("#E8F0FF", 50, blur=18))
    cv.drawPath(lua, paint("#F2F6FF"))
    for sx, sy in ((jx0 + 170, jy0 + 50), (jx0 + 200, jy0 + 150), (jx0 + 120, jy0 + 190)):
        cv.drawCircle(sx, sy, 3, paint("#F2F6FF", 220))
    cv.drawLine((jx0 + jx1) / 2, jy0, (jx0 + jx1) / 2, jy1, paint("#DCE4EE", 255, "stroke", 12))
    cv.drawLine(jx0, (jy0 + jy1) / 2, jx1, (jy0 + jy1) / 2, paint("#DCE4EE", 255, "stroke", 12))
    # piso
    cv.drawRect(skia.Rect(-600, 1046, 1700, 1062), paint("#8796AE"))
    shp = skia.GradientShader.MakeLinear([skia.Point(0, 1062), skia.Point(0, 1400)], [_c("#6E5640"), _c("#8A6C50")])
    cv.drawRect(skia.Rect(-600, 1062, 1700, 1700), paint("#7A5F46", shader=shp))
    # cabeceira
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(CAMA_X0 - 30, 560, CAMA_X0 + 26, 1062), 18, 18), paint(MAD))
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(CAMA_X0 - 22, 572, CAMA_X0 + 16, 1050), 12, 12), paint(MAD_CL, 120))
    # estrado, pés e sombra
    cv.drawRect(skia.Rect(CAMA_X0, MAT_BAIXO + 50, CAMA_X1, MAT_BAIXO + 62), paint("#000000", 60, blur=10))
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(CAMA_X0, MAT_BAIXO - 4, CAMA_X1, MAT_BAIXO + 44), 8, 8), paint(MAD))
    cv.drawRect(skia.Rect(CAMA_X0, MAT_BAIXO - 4, CAMA_X1, MAT_BAIXO + 6), paint(MAD_CL, 160))
    for x0 in (CAMA_X0 + 30, CAMA_X1 - 50):
        cv.drawRect(skia.Rect(x0, MAT_BAIXO + 44, x0 + 22, 1066), paint(MAD_ESC))
    # colchão: tampo (de leve, visto de cima) e face da frente
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(CAMA_X0 + 4, MAT_FUNDO, CAMA_X1, MAT_FRENTE + 8), 14, 14), paint("#E9EFF5"))
    shf = skia.GradientShader.MakeLinear([skia.Point(0, MAT_FRENTE), skia.Point(0, MAT_BAIXO)], [_c("#DCE4EE"), _c("#C3CFDD")])
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(CAMA_X0 + 4, MAT_FRENTE, CAMA_X1, MAT_BAIXO), 12, 12), paint("#D0DAE5", shader=shf))
    cv.drawLine(CAMA_X0 + 16, MAT_FRENTE + 2, CAMA_X1 - 10, MAT_FRENTE + 2, paint("#FFFFFF", 200, "stroke", 3))
    # travesseiro e cabeça de quem dorme do lado de lá (atrás, mais alto: perspectiva)
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(96, 780, 300, 840), 28, 28), paint("#000000", 40, blur=8))
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(96, 776, 296, 834), 28, 28), paint("#E3E9F1"))
    cabeca(cv, (196, 742), -math.pi / 2 + 0.25, (-1.0, 0.0), (0.0, -1.0), 1.0, cabelo=CABELO2)


def cobertor_fundo(cv, t, mexe=0.0):
    """O cobertor sobre quem dorme do lado de lá (ombro até os pés), atrás da nossa pessoa."""
    resp = 3 * math.sin(t * 2.3)
    pts = [(176, 846), (186, 752), (232, 716 - resp), (320, 708 - resp), (430, 722), (540, 720), (640, 730),
           (712, 730 - 52 * mexe), (770, 736 - 10 * mexe), (850, 740), (884, 712), (912, 706), (934, 736), (944, 846)]
    pth = suave(pts)
    cv.drawPath(pth, paint(esc_cor(COBERTOR, 0.18)))
    cv.save(); cv.clipPath(pth, skia.ClipOp.kIntersect, True)
    for k in range(-2, 16):
        x = 120 + k * 70
        cv.drawLine(x, 660, x + 90, 860, paint(esc_cor(COBERTOR_CL, 0.15), 110, "stroke", 14))
    cv.restore()
    cv.drawPath(pth, paint(esc_cor(COBERTOR_ESC, 0.3), 180, "stroke", 3))


def cobertor_frente(cv):
    """O cobertor da nossa pessoa: do ombro até perto do joelho, caindo pela frente do colchão."""
    topo = [(150, 812), (168, 756), (250, 731), (360, 737), (450, 743), (540, 749), (622, 757), (648, 776)]
    pth = suave(topo, fechar=False)
    pth.lineTo(652, 806); pth.lineTo(646, 984)
    for i in range(1, 9):                                   # barra levemente ondulada
        pth.lineTo(lerp(646, 150, i / 8), 984 + 5 * math.sin(i * 1.7))
    pth.close()
    cv.drawPath(pth, paint("#000000", 60, blur=10))
    sh = skia.GradientShader.MakeLinear([skia.Point(0, 730), skia.Point(0, 970)], [_c(COBERTOR_CL), _c(COBERTOR_ESC)])
    cv.drawPath(pth, paint(COBERTOR, shader=sh))
    cv.save(); cv.clipPath(pth, skia.ClipOp.kIntersect, True)
    for k in range(-3, 14):
        x = 100 + k * 64
        cv.drawLine(x, 700, x + 110, 990, paint(COBERTOR_CL, 120, "stroke", 13))
    cv.drawLine(150, MAT_FRENTE + 10, 660, MAT_FRENTE + 10, paint("#000000", 40, "stroke", 10, blur=6))
    cv.restore()
    dobra = suave([(170, 760), (250, 736), (360, 742), (450, 748), (540, 754), (622, 762), (648, 780)], fechar=False)
    cv.drawPath(dobra, paint("#8FB0DA", 230, "stroke", 9))
    cv.drawPath(pth, paint(COBERTOR_ESC, 200, "stroke", 3))


def travesseiro_frente(cv):
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(52, 846, 268, 900), 26, 26), paint("#000000", 45, blur=8))
    sh = skia.GradientShader.MakeLinear([skia.Point(0, 838), skia.Point(0, 896)], [_c("#FFFFFF"), _c("#DCE4EE")])
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(50, 838, 266, 894), 26, 26), paint("#FFFFFF", shader=sh))
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(50, 838, 266, 894), 26, 26), paint("#B9C6D3", 200, "stroke", 2))


# ---- a capa de tecido (desenhada no referencial da canela, dentro do desenho girado)
def _capa_contorno(knee, ank, n=26):
    d, f, L = shin_frame(knee, ank)
    v0, v1 = L * ANEIS_S[0] - 34, L * ANEIS_S[-1] + 34
    R = RA + 14
    vs = [lerp(v0, v1, i / n) for i in range(n + 1)]

    def larg(v):
        bump = sum(math.exp(-((v - L * s) / 16) ** 2) for s in ANEIS_S)
        return R + 5 * bump - 4 * (1 - min(1.0, bump * 1.3))
    lado_a = [(v, larg(v)) for v in vs]
    lado_b = [(v, -larg(v) * 0.96) for v in vs[::-1]]
    return lado_a + lado_b, (d, f, L, v0, v1, R)


def capa_tecido(cv, knee, ank, veste, a=1.0, verde=0.0, assenta=0.0):
    """Capa de tecido OPACA em volta do aparelho: cai de cima (veste 0..0.45) e envolve (0.45..1)."""
    if veste <= 0 or a <= 0:
        return
    cont, (d, f, L, v0, v1, R) = _capa_contorno(knee, ank)
    cai = e_out(clamp(veste / 0.45)); envolve = e_inout(clamp((veste - 0.45) / 0.55))
    m = skia.Matrix(); m.setAll(f[0], d[0], knee[0], f[1], d[1], knee[1], 0, 0, 1)
    cv.save(); cv.concat(m)
    cv.translate(80 * (1 - cai) + 4 * math.sin(math.pi * assenta), 0)      # cai de "cima" (+f = para cima na cama)
    pth = suave([(w, v) for v, w in cont])
    if envolve < 1:                                         # ainda envolvendo: só a parte de cima, com a borda curvada
        corte = R + 12 - (2 * R + 24) * lerp(0.28, 1.0, envolve)
        cv.clipRect(skia.Rect(corte, v0 - 30, R + 30, v1 + 30), True)
    cv.drawPath(pth, paint("#000000", int(70 * a), blur=10))
    sh = skia.GradientShader.MakeLinear([skia.Point(R, 0), skia.Point(-R, 0)],
                                        [_c(CAPA_CL), _c(CAPA), _c(CAPA), _c(CAPA_ESC)], [0.0, 0.3, 0.7, 1.0])
    cv.drawPath(pth, paint(CAPA, int(255 * a), shader=sh))
    cv.save(); cv.clipPath(pth, skia.ClipOp.kIntersect, True)
    for i in range(int((v1 - v0) / 11) + 1):                 # malha: carreiras finas
        v = v0 + 6 + i * 11
        cv.drawLine(-R - 10, v, R + 10, v, paint(CAPA_ESC, int(55 * a), "stroke", 2))
    for s in ANEIS_S:                                         # o volume dos anéis por baixo do tecido
        v = L * s
        cv.drawLine(-R + 8, v + 5, R - 6, v + 5, paint(CAPA_ESC, int(150 * a), "stroke", 9, blur=3))
        cv.drawLine(-R + 8, v - 2, R - 6, v - 2, paint(CAPA_CL, int(230 * a), "stroke", 7))
    for v in (v0 + 9, v1 - 9):                                # punhos de elástico nas pontas
        cv.drawLine(-R - 10, v, R + 10, v, paint(CAPA_ESC, int(230 * a), "stroke", 15))
        for k in range(-6, 7):
            cv.drawLine(k * 14, v - 6, k * 14, v + 6, paint(esc_cor(CAPA_ESC, 0.25), int(150 * a), "stroke", 2))
    pe_ = paint("#F3EEFF", int(210 * a), "stroke", 2.5)      # costura pespontada no alto da capa
    pe_.setPathEffect(skia.DashPathEffect.Make([9.0, 7.0], 0.0))
    cv.drawLine(R - 16, v0 + 18, R - 16, v1 - 18, pe_)
    cv.restore()
    cv.drawPath(pth, paint(esc_cor(CAPA_ESC, 0.3), int(230 * a), "stroke", 3))
    if envolve < 1:                                         # borda que está dobrando por cima
        corte = R + 12 - (2 * R + 24) * lerp(0.28, 1.0, envolve)
        cv.drawLine(corte, v0 + 4, corte, v1 - 4, paint(CAPA_CL, int(230 * a), "stroke", 8, blur=2))
    if verde > 0:
        cv.drawPath(pth, paint(VERDE, int(150 * verde), "stroke", 22, blur=8))
        cv.drawPath(pth, paint(VERDE, int(255 * verde), "stroke", 7))
    cv.restore()


def cama_estado(t, T):
    """Estado do lance da capa (LANCE 3). Tempos: ver docstring do módulo."""
    V = T["validado"]
    veste = prog(t, T["com"] - 0.05, T["capa_fim"] + 0.12)
    assenta = prog(t, T["capa_fim"] + 0.02, T["capa_fim"] + 0.32)
    # replay SEM capa (o contraexemplo): de pouco depois do carimbo até o 2º "não"
    r0, r1 = V + R0_SEM, T["nao2"] + 0.02
    sem = janela(t, r0, r1, 0.08, 0.1)                     # 1 = capa fora (replay)
    k_sn = prog(t, r0 + 0.05, r0 + 0.42)                   # o lençol vem até o 1º anel...
    tug = max(0.0, t - (r0 + 0.42))                        # ...engancha e dá dois puxões
    puxa = math.sin(min(tug, 0.5) / 0.5 * 2 * math.pi) * (1 - prog(t, r1 - 0.1, r1)) if t < r1 else 0.0
    snag = (t >= r0 + 0.42) and t < r1
    # COM capa: o lençol desliza liso até passar do pé, e volta
    ida = e_inout(prog(t, T["enrosca"] - 0.12, T["lencol_fim"] + 0.05))
    volta = e_inout(prog(t, T["lencol_fim"] + 0.18, T["protege"] + 0.12))
    lencol = ida * (1 - volta) if t >= r1 else 0.0
    passou = janela(t, T["lencol_fim"] - 0.12, T["protege"], 0.12, 0.2)
    # quem dorme ao lado: a perna dela passa por cima, encosta na capa e se acomoda
    pe2 = e_inout(prog(t, T["protege"] - 0.05, T["dorme"] + 0.05))
    acomoda = prog(t, T["dorme"] + 0.05, T["lado_fim"] + 0.2)
    toque = prog(t, T["protege"] + 0.35, T["protege"] + 1.2)
    verde = janela(t, T["enrosca"] - 0.05, T["off"] + 0.4, 0.2, 0.2)
    return dict(veste=veste, assenta=assenta, sem=sem, k_sn=k_sn, puxa=puxa, snag=snag, lencol=lencol,
                indo=volta <= 0, passou=passou, pe2=pe2, acomoda=acomoda, toque=toque, verde=verde)


_TOPO = {}


def _perfil(sil):
    xs = list(range(600, 1012, 6))
    tops = []
    for x in xs:
        r = skia.Path(); r.addRect(skia.Rect(x, 0, x + 6, 2000))
        q = skia.Op(sil, r, skia.PathOp.kIntersect_PathOp)
        bb = q.computeTightBounds() if q is not None else None
        tops.append(bb.top() if bb is not None and not bb.isEmpty() else MAT_FRENTE)
    for i in range(1, len(tops)):                    # o pano cai em rampa depois do pé
        tops[i] = min(tops[i], tops[i - 1] + 9.0)
    for i in range(len(tops) - 2, -1, -1):
        tops[i] = min(tops[i], tops[i + 1] + 9.0)
    return xs, [y - 7 for y in tops]


def topo_perna():
    """Altura do alto da perna deitada, coluna a coluna, COM capa (xs, tops) — e, em _TOPO, a mesma coisa
    SEM capa (o anel e as porcas de fora) e o alto do anel de baixo, onde o lençol engancha."""
    if not _TOPO:
        b = corpo(POSE_DEITADA)
        cont, _ = _capa_contorno(b["kN"], b["aN"])
        d, f, L = shin_frame(b["kN"], b["aN"])
        capa_p = poli([(b["kN"][0] + d[0] * v + f[0] * w, b["kN"][1] + d[1] * v + f[1] * w) for v, w in cont])
        base = uniao(canela_path(b["kN"], b["aN"]), pe_path(b["aN"]), capsula(b["hip"], b["kN"], 78, 60))
        sil = uniao(base, capa_p)
        sil.transform(_GIRO)
        _TOPO["xs"], _TOPO["tops"] = _perfil(sil)
        cs, _, _, _ = _hastes(b["kN"], b["aN"])
        aneis = []
        for c in cs:                                      # cada anel = elipse estreita perpendicular à canela
            o = skia.Path(); o.addOval(skia.Rect(-RA - 4, -RB - 2, RA + 4, RB + 2))
            m = skia.Matrix(); m.setAll(f[0], d[0], c[0], f[1], d[1], c[1], 0, 0, 1)
            o.transform(m); aneis.append(o)
        nua = uniao(base, *aneis)
        nua.transform(_GIRO)
        _TOPO["xs_nu"], _TOPO["tops_nu"] = _perfil(nua)
        c1 = gira(cs[0])                                  # o anel de cima (perto do joelho): o 1º que o lençol encontra
        _TOPO["gancho"] = (c1[0], c1[1] - RA - 2)
    return _TOPO["xs"], _TOPO["tops"]


X_LENCOL0 = 628.0          # o lençol sai de debaixo do cobertor (perto do joelho)...
X_LENCOL1 = 866.0          # ...e vai até passar da capa (para antes do pé: nada de "tenda" nos dedos)


def _pinta_lencol(cv, pth, hem_pts, topo_pts, verde=0.0):
    """Lençol de algodão: SEMI-opaco (o que está embaixo continua visível), barra reta, caimento de pano."""
    cv.drawPath(pth, paint("#000000", 40, blur=9))
    sh = skia.GradientShader.MakeLinear([skia.Point(0, 680), skia.Point(0, MAT_FRENTE + 30)],
                                        [_c(LENCOL, 205), _c(LENCOL_ESC, 185)])
    cv.drawPath(pth, paint(LENCOL, 255, shader=sh))
    cv.drawPath(poli(topo_pts, fechar=False), paint("#FFFFFF", 255, "stroke", 4))
    if len(hem_pts) > 1:
        cv.drawPath(poli(hem_pts, fechar=False), paint("#FFFFFF", 255, "stroke", 6))
        cv.drawPath(poli(hem_pts, fechar=False), paint("#9DB0C6", 210, "stroke", 1.8))
    if verde > 0:
        cv.drawPath(poli(topo_pts, fechar=False), paint(VERDE, int(230 * verde), "stroke", 4))


def _lencol_path(pts, hem, barra):
    """pts: alto do pano, do cobertor (esquerda) até a ponta (direita); hem: barra da ponta, de cima p/ baixo."""
    pth = skia.Path(); pth.moveTo(X_LENCOL0, barra); pth.lineTo(X_LENCOL0, pts[0][1])
    for q in pts:
        pth.lineTo(*q)
    for q in hem[1:]:
        pth.lineTo(*q)
    pth.close()
    return pth


def lencol_desliza(cv, k, indo=True, verde=0.0):
    """COM capa: o lençol sai de debaixo do cobertor e passa por cima da capa inteira SEM parar
    (barra reta, sem zigue-zague; semi-opaco: a capa continua visível)."""
    if k <= 0.005:
        return
    xs, tops = topo_perna()
    xr = lerp(X_LENCOL0 + 14, X_LENCOL1, k)
    pts = [(x, y - 3) for x, y in zip(xs, tops) if X_LENCOL0 <= x <= xr]
    if len(pts) < 2:
        return
    barra = MAT_FRENTE + 30
    x0, y0 = pts[-1]
    recuo = 34 if indo else 16
    hem = [(x0, y0)] + [(x0 - recuo * (i / 8) ** 2, lerp(y0, barra, i / 8)) for i in range(1, 9)]
    _pinta_lencol(cv, _lencol_path(pts, hem, barra), hem, pts, verde)


def lencol_engancha(cv, k, puxa, snag):
    """SEM capa: o lençol sai de debaixo do cobertor e ENGANCHA no anel de cima do aparelho: a ponta fica
    presa num bico no alto do anel e, a cada puxão, o pano repuxa em pregas (não passa)."""
    if k <= 0.005:
        return
    topo_perna()
    xs, tops = _TOPO["xs_nu"], _TOPO["tops_nu"]
    gx, gy = _TOPO["gancho"]
    barra = MAT_FRENTE + 30
    xr = lerp(X_LENCOL0 + 14, gx - 2, e_out(k))
    pts = [(x, y - 3) for x, y in zip(xs, tops) if X_LENCOL0 <= x <= min(xr, gx - 18)]
    if len(pts) < 2:
        pts = [(X_LENCOL0, tops[0] - 3), (xr, tops[0] - 3)]
    if snag:
        bx, by = gx + 8 * abs(puxa), gy - 10 * abs(puxa)          # o bico preso no alto do anel, repuxado
        pts = pts + [(bx, by)]
        hem = [(bx, by)] + [(bx - 64 * (i / 7) - 12 * abs(puxa) * (i / 7), lerp(by, barra, (i / 7) ** 0.75))
                            for i in range(1, 8)]
    else:
        x0, y0 = pts[-1]
        hem = [(x0, y0)] + [(x0 - 26 * (i / 8) ** 2, lerp(y0, barra, i / 8)) for i in range(1, 9)]
    pth = _lencol_path(pts, hem, barra)
    _pinta_lencol(cv, pth, hem, pts)
    if snag:                                                         # pregas de tensão saindo do bico
        bx, by = hem[0]
        cv.save(); cv.clipPath(pth, skia.ClipOp.kIntersect, True)
        for i in range(4):
            cv.drawLine(bx - 2, by + 6, bx - 40 - 34 * i, barra - 4, paint("#93A9C4", 190, "stroke", 4))
        cv.restore()


def perna_ao_lado(cv, k, a=1.0, acomoda=0.0):
    """A perna de quem dorme ao lado (calça de pijama cor de camelo + MEIA listrada: nada de lilás, que é a cor da capa) sai de debaixo do cobertor do lado de
    lá e PASSA POR CIMA da nossa perna, encostando na capa — o jeito mais comum de alguém encostar no aparelho
    dormindo. `k` 0..1 = a perna descendo até a capa; `acomoda` = o assentamento depois do toque."""
    if a <= 0 or k <= 0:
        return
    jx, jy = 690.0, 716.0                                            # joelho dela (sai do cobertor de lá)
    ang = math.radians(lerp(-24, 17, e_out(k)) + 3 * math.sin(math.pi * 2 * acomoda) * (1 - acomoda))
    L = 196.0
    tx, ty = jx + L * math.cos(ang), jy + L * math.sin(ang)          # tornozelo dela
    aa = a * clamp(k * 4)
    cal = capsula((jx - 30, jy - 6), (tx, ty), 64, 50)
    cv.drawPath(cal, paint("#000000", int(70 * aa), blur=10))
    sh = skia.GradientShader.MakeLinear([skia.Point(jx, jy - 30), skia.Point(jx, jy + 30)], [_c("#D2A277"), _c("#9A6A42")])
    cv.drawPath(cal, paint("#B88457", int(255 * aa), shader=sh))
    for i in range(1, 4):                                            # listras do pijama
        u = i / 4
        cx_, cy_ = lerp(jx - 30, tx, u), lerp(jy - 6, ty, u)
        cv.drawLine(cx_ - 10, cy_ - 26, cx_ + 6, cy_ + 26, paint("#E6C49C", int(170 * aa), "stroke", 5))
    cv.drawPath(cal, paint("#6E4A2C", int(200 * aa), "stroke", 2.5))
    # o pé, de meia, caído para a frente (dedos para baixo)
    cv.save(); cv.translate(tx, ty); cv.rotate(math.degrees(ang) + 35); cv.scale(0.9, 0.9)
    pe = pe_path((0.0, 0.0))
    cv.drawPath(pe, paint("#000000", int(60 * aa), blur=5))
    cv.drawPath(pe, paint("#F0C060", int(255 * aa)))
    cv.save(); cv.clipPath(pe, skia.ClipOp.kIntersect, True)
    for xx in (34, 62, 90):
        cv.drawLine(xx, -40, xx - 8, 50, paint("#8A5A2B", int(230 * aa), "stroke", 9))
    cv.drawRect(skia.Rect(-40, -40, 8, 50), paint("#D9A23E", int(255 * aa)))
    cv.restore()
    cv.drawPath(pe, paint("#A87A22", int(230 * aa), "stroke", 2.5))
    cv.restore()
    # a dobra do cobertor de lá por cima da coxa dela (a perna SAI de debaixo do cobertor)
    dob = skia.Path(); dob.addRRect(skia.RRect.MakeRectXY(skia.Rect(jx - 92, jy - 34, jx + 6, jy + 30), 30, 30))
    cv.drawPath(dob, paint("#000000", int(50 * aa), blur=6))
    cv.drawPath(dob, paint(esc_cor(COBERTOR, 0.18), int(255 * aa)))
    cv.drawPath(dob, paint(esc_cor(COBERTOR_ESC, 0.3), int(200 * aa), "stroke", 3))
    return tx, ty


TOQUE_PT = (812.0, 744.0)              # onde a perna dela encosta no alto da capa


CAM_L2_LARGA = (1.0, 545.0, 778.0)
CAM_L2_PERTO = (1.62, 770.0, 800.0)
CAM_L2_MEIO = (1.3, 718.0, 790.0)
CAM_L2_LADO = (1.12, 640.0, 770.0)
CAM_SNAG = (2.3, 700.0, 772.0)         # replay sem capa: perto do anel onde o lençol engancha


def cam_cama(t, T):
    cam = lerp3(CAM_L2_LARGA, CAM_L2_PERTO, e_inout(prog(t, T["fix2"] - 0.05, T["capa"] + 0.2)))
    cheg = prog(t, T["pode3_fim"], T["validado"])
    cam = (cam[0] * (1 + 0.07 * e_inout(cheg)), cam[1], cam[2])
    cam = lerp3(cam, CAM_L2_MEIO, e_inout(prog(t, T["validado"] + 0.2, T["validado"] + 0.5)))
    r0, r1 = T["validado"] + R0_SEM, T["nao2"] + 0.02
    cam = lerp3(cam, CAM_SNAG, e_inout(janela(t, r0 - 0.05, r1 - 0.05, 0.22, 0.18)))
    return lerp3(cam, CAM_L2_LADO, e_inout(prog(t, T["lencol_fim"] + 0.05, T["protege"] + 0.3)))


def cena_cama(cv, t, T):
    cam = cam_cama(t, T)
    e = cama_estado(t, T)
    cv.save(); aplica(cv, cam)
    quarto(cv)
    cobertor_fundo(cv, t, 0.0)
    travesseiro_frente(cv)
    cv.save(); deitar(cv)
    pessoa(cv, POSE_DEITADA, camadas=("corpo",))
    cv.restore()
    cobertor_frente(cv)
    cv.drawOval(skia.Rect(640, MAT_FRENTE - 16, 960, MAT_FRENTE + 12), paint("#000000", 50, blur=10))
    cv.save(); deitar(cv)
    a_capa = 1 - e["sem"]
    capa_fn = (lambda c, k, a_: capa_tecido(c, k, a_, e["veste"], a=a_capa, verde=e["verde"] * a_capa,
                                            assenta=e["assenta"]))
    br = prog(t, T["fix2"] - 0.05, T["fix2"] + 0.55)
    pessoa(cv, POSE_DEITADA, camadas=("perna",), capa_fn=capa_fn, brilho=br if 0 < br < 1 else -1)
    cv.restore()
    if e["sem"] > 0.02:                                     # contraexemplo: sem capa o lençol engancha
        lencol_engancha(cv, e["k_sn"], e["puxa"], e["snag"])
        cobertor_frente(cv)
    elif e["lencol"] > 0.005:
        lencol_desliza(cv, e["lencol"], e["indo"], e["verde"])
        cobertor_frente(cv)                                  # o lençol sai de baixo do cobertor
    perna_ao_lado(cv, e["pe2"], 1.0, e["acomoda"])           # quem dorme ao lado: a perna dela por cima da capa
    if 0 < e["toque"] < 1:                                   # o toque macio: ondas verdes na capa
        for i in range(2):
            u = clamp(e["toque"] * 1.6 - i * 0.35)
            if 0 < u < 1:
                cv.drawArc(skia.Rect(TOQUE_PT[0] - 30 - 70 * u, TOQUE_PT[1] - 20 - 34 * u,
                                     TOQUE_PT[0] + 30 + 70 * u, TOQUE_PT[1] + 20 + 34 * u), 160, 220, False,
                           paint(VERDE, int(230 * (1 - u)), "stroke", 5))
    cv.restore()
    return cam, e


def centro_capa():
    b = corpo(POSE_DEITADA)
    d, f, L = shin_frame(b["kN"], b["aN"])
    c = (b["kN"][0] + d[0] * L * 0.48, b["kN"][1] + d[1] * L * 0.48)
    return gira(c)


def gancho_tela(cam):
    topo_perna()
    return na_tela(cam, *_TOPO["gancho"])


# ================================================================== LANCE 2 (poltrona) — cadeira baixa e fofinha
BAIXA_HIP = (300.0, 1016.0)    # fundo do assento fofo: o joelho fica mais alto que o quadril
ANK_N3 = (600.0, TORN_Y)
ANK_F3 = (476.0, TORN_Y)
PE_HIP3 = (476.0, 702.0)


def cadeira_baixa(cv, parte, afunda=0.0, ambar=0.0):
    """Cadeira baixa, de almofada fofa (mostarda), de perfil; a almofada cede sob o quadril (`afunda`, px)."""
    if parte == "fundo":
        cv.drawRect(skia.Rect(140, PISO_Y - 6, 560, PISO_Y + 12), paint("#000000", 60, blur=12))
        for x0 in (168, 516):                                   # pezinhos curtos
            cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(x0, 1126, x0 + 22, PISO_Y + 2), 5, 5), paint(MAD_ESC))
        cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(150, 1040, 556, 1132), 30, 30), paint(FOFO_ESC))   # base
        cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(176, 916, 352, 980), 30, 30), paint(esc_cor(FOFO, 0.22)))  # braço de lá
        # encosto alto e estufado
        sh = skia.GradientShader.MakeLinear([skia.Point(150, 0), skia.Point(262, 0)], [_c(FOFO_ESC), _c(FOFO), _c(FOFO_CL)])
        cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(146, 690, 266, 1070), 54, 54), paint(FOFO, shader=sh))
        cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(146, 690, 266, 1070), 54, 54), paint(FOFO_ESC, 220, "stroke", 3))
        for y in (800, 900):
            cv.drawCircle(214, y, 6, paint(FOFO_ESC, 230))
        # almofada do assento: o topo cede sob o quadril
        xa, xb, yt = 196.0, 560.0, 1004.0
        p = skia.Path(); p.moveTo(xa, yt + 34)
        p.cubicTo(xa, yt - 4, xa + 30, yt - 8, xa + 60, yt - 6)
        p.cubicTo(250, yt - 4 + afunda * 1.0, 340, yt + afunda, 400, yt - 2 + afunda * 0.4)
        p.cubicTo(470, yt - 8, xb - 30, yt - 10, xb - 6, yt + 8)
        p.cubicTo(xb + 6, yt + 30, xb - 2, yt + 66, xb - 24, yt + 70)
        p.lineTo(xa + 16, yt + 70); p.close()
        if ambar > 0:
            cv.drawPath(p, paint(AMBAR, int(170 * ambar), "stroke", 22, blur=9))
        sh2 = skia.GradientShader.MakeLinear([skia.Point(0, yt - 10), skia.Point(0, yt + 70)], [_c(FOFO_CL), _c(FOFO), _c(FOFO_ESC)])
        cv.drawPath(p, paint(FOFO, shader=sh2))
        cv.drawPath(p, paint(FOFO_ESC, 220, "stroke", 3))
        cv.drawLine(xa + 40, yt + 46, xb - 40, yt + 46, paint(FOFO_ESC, 90, "stroke", 3))
        if ambar > 0:
            cv.drawPath(p, paint(AMBAR, int(255 * ambar), "stroke", 5))
            cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(150, 1040, 556, 1132), 30, 30),
                         paint(AMBAR, int(255 * ambar), "stroke", 6))
    else:
        # braço do lado de cá: baixo e estufado
        sh = skia.GradientShader.MakeLinear([skia.Point(0, 930), skia.Point(0, 1040)], [_c(FOFO_CL), _c(FOFO), _c(FOFO_ESC)])
        cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(166, 938, 346, 1050), 34, 34), paint("#000000", 50, blur=8))
        cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(162, 930, 342, 1044), 34, 34), paint(FOFO, shader=sh))
        cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(162, 930, 342, 1044), 34, 34), paint(FOFO_ESC, 220, "stroke", 3))
        cv.drawLine(180, 952, 324, 952, paint(FOFO_CL, 200, "stroke", 4))


def pose_poltrona(t, T):
    c2, fof, forca, apf = T["cadeira2"], T["fofinha"], T["forca"], T["apf_fim"]
    senta = e_inout(prog(t, c2 + 0.12, fof + 0.1))
    # sentar AFUNDANDO: inclina, desce, e a almofada cede além do esperado ("fofinha")
    ua = e_inout(clamp(senta / 0.45)); ub = e_inout(clamp((senta - 0.3) / 0.7))
    h1 = (PE_HIP3[0] - 30 * ua, PE_HIP3[1] + 140 * ua)
    hip = lerp2(h1, BAIXA_HIP, ub)
    al = lerp(lerp(0.03, 0.6, ua), 0.14, ub)
    over = 14 * math.sin(math.pi * prog(t, fof - 0.05, fof + 0.45))          # afunda mais e volta um pouco
    hip = (hip[0], hip[1] + over * ub)
    # "força": tenta levantar e não sai do fundo (dois balanços)
    u = prog(t, forca - 0.05, apf + 0.05)
    tenta = math.sin(math.pi * u) * (0.6 + 0.4 * abs(math.sin(math.pi * 2 * u)))
    al += 0.55 * tenta
    hip = (hip[0] + 18 * tenta, hip[1] - 22 * tenta * abs(math.sin(math.pi * 2 * u)))
    m_rest = _na_coxa(hip, ANK_N3, 0.7, 34)
    mF = _na_coxa(hip, ANK_F3, 0.6, 30)
    empurra = e_inout(prog(t, T["demais"] - 0.1, forca + 0.05))      # mãos nos braços da cadeira para tentar subir
    m_rest = lerp2(m_rest, (300.0, 928.0 - 6 * tenta), empurra)
    mF = lerp2(mF, (288.0, 914.0 - 6 * tenta), empurra)
    return dict(hip=hip, al=al, ankN=ANK_N3, ankF=ANK_F3, mN=m_rest, mF=mF, gN=0.0, gF=0.0,
                afunda=10 + 12 * ub + over * ub, tenta=tenta, u_forca=u)


CAM_L3 = (1.12, 470.0, 860.0)
CAM_POLT_PERTO = (1.4, 390.0, 960.0)            # congela no ASSENTO (quadril afundado), não no joelho


def cam_poltrona(t, T, pose):
    cam = lerp3((1.0, 500.0, 770.0), CAM_L3, e_inout(prog(t, T["cadeira2"] + 0.1, T["fofinha"] + 0.2)))
    cam = lerp3(cam, CAM_POLT_PERTO, e_inout(prog(t, T["pode2"], T["pode2"] + 0.32)))
    cheg = prog(t, T["pode2_fim"], T["anulado2"])
    cam = (cam[0] * (1 + 0.07 * e_inout(cheg)), cam[1], cam[2])
    return lerp3(cam, CAM_L3, e_inout(prog(t, T["anulado2"] + 0.5, T["baixa2"] + 0.2)))


def cena_poltrona(cv, t, T, cam=None):
    pose = pose_poltrona(t, T)
    cam = cam or cam_poltrona(t, T, pose)
    am_ass = janela(t, T["baixa2"] - 0.05, T["demais"] + 0.35, 0.15, 0.3)
    pulso = 1.0 + 0.3 * max(0.0, 1 - abs(t - T["macia"]) / 0.2)
    afunda = pose["afunda"] + 8 * max(0.0, 1 - abs(t - T["macia"] - 0.1) / 0.3)
    cv.save(); aplica(cv, cam)
    sala(cv)
    cadeira_baixa(cv, "fundo", afunda, min(1.0, am_ass * pulso))
    b = pessoa(cv, pose, camadas=("fundo",))
    pessoa(cv, pose, camadas=("corpo",))
    cadeira_baixa(cv, "frente")
    # "aparelho": o METAL acende em âmbar (traço, sem brilho na pele) e treme — está sendo forçado
    al_fix = janela(t, T["apf"] - 0.05, T["wipe"] + 0.2, 0.15, 0.2)
    tr = janela(t, T["apf"] - 0.02, T["apf_fim"] + 0.15, 0.05, 0.15)
    treme = (2.4 * tr * math.sin(t * 71), 1.8 * tr * math.cos(t * 83))
    pessoa(cv, pose, camadas=("perna",), alerta=al_fix, treme=treme)
    pessoa(cv, pose, camadas=("braco",))
    # "força": seta de ESFORÇO saindo do quadril para cima — cresce, e o corpo cai de volta no fundo
    if 0 < pose["u_forca"] < 1:
        hx, hy = b["hip"]
        k = pose["tenta"]
        a_f = clamp(pose["u_forca"] * 6) * (1 - prog(pose["u_forca"], 0.85, 1.0))
        seta(cv, hx + 30, hy - 40, hx + 30 + 70 * k, hy - 40 - 170 * k, AMBAR, a_f, larg=11, tam=30)
    # "joelho": seta-PONTEIRO âmbar apontando o joelho (nada de anel ou halo em volta da articulação)
    a_j = janela(t, T["joelho"] - 0.06, T["wipe"] + 0.15, 0.15, 0.2)
    if a_j > 0:
        kx, ky = b["kN"]
        ent = e_back(prog(t, T["joelho"] - 0.06, T["joelho"] + 0.22))
        x1, y1 = kx + 30, ky - 46
        x0, y0 = x1 + 150 * clamp(ent, 0, 1.2), y1 - 120 * clamp(ent, 0, 1.2)
        seta(cv, x0, y0, x1, y1, AMBAR, a_j, larg=12, tam=34)
    cv.restore()
    return cam, pose, b


def cena_certa(cv, t, T, cam):
    """Replay do jeito certo depois do lance da poltrona: a cadeira firme, com braços e mais alta, em verde."""
    pose = dict(hip=REST_HIP, al=0.16, ankN=ANK_N, ankF=ANK_F, mN=APOIO_N, mF=APOIO_F, gN=0.0, gF=0.0)
    vv = prog(t, T["wipe"] + 0.2, T["wipe"] + 0.45)
    cv.save(); aplica(cv, cam)
    sala(cv)
    cadeira(cv, "fundo", verde_assento=vv)
    pessoa(cv, pose, camadas=("fundo",))
    pessoa(cv, pose, camadas=("corpo",))
    cadeira(cv, "frente", vv)
    pessoa(cv, pose, camadas=("perna",))
    pessoa(cv, pose, camadas=("braco",))
    cv.restore()


# ================================================================== HUD do VAR (desenho próprio)
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
    if varre > 0:                                   # barra clara que desce durante o CHECANDO
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
        borda = cor_chip if cor_chip != "#FFFFFF" else "#FFFFFF"
        cv.drawRRect(r2, paint(borda, int((230 if cor_chip != "#FFFFFF" else 60) * aa), "stroke", 3 if cor_chip != "#FFFFFF" else 2))
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
    cv.drawPath(p, _trim(paint(CIANO, int(110 * a * (0.6 + 0.4 * pulso)), "stroke", 18, blur=8), k))
    cv.drawPath(p, _trim(paint(CIANO, int(255 * a), "stroke", 8), k))


def etiqueta_tele(cv, t, ax, ay, lx, ly, k, a):
    """(v4) Marcação do analista do VAR (telestrador): ponto no objeto, fio ciano que sai dele e a
    etiqueta com o NOME do objeto. k 0..1: o fio corre do objeto até a etiqueta e a etiqueta abre."""
    if a <= 0 or k <= 0:
        return
    kl = e_out(clamp(k / 0.5))
    kp = e_back(clamp((k - 0.32) / 0.68))
    pul = 0.5 + 0.5 * math.sin(t * 8)
    cv.drawCircle(ax, ay, 15 + 5 * pul, paint(CARTAO, int(120 * a), "stroke", 8))
    cv.drawCircle(ax, ay, 15 + 5 * pul, paint(CIANO, int(255 * a), "stroke", 4))
    cv.drawCircle(ax, ay, 8, paint("#FFFFFF", int(255 * a)))
    ex, ey = lerp(ax, lx, kl), lerp(ay, ly, kl)
    pt = paint(CARTAO, int(170 * a), "stroke", 12); pt.setStrokeCap(skia.Paint.kRound_Cap)
    cv.drawLine(ax, ay, ex, ey, pt)
    pt = paint(CIANO, int(255 * a), "stroke", 5); pt.setStrokeCap(skia.Paint.kRound_Cap)
    cv.drawLine(ax, ay, ex, ey, pt)
    if kp <= 0:
        return
    f = skia.Font(F_BLACK, 44); lw = f.measureText(T_FIX)
    cv.save(); cv.translate(lx, ly); s = clamp(kp, 0.0, 1.15); cv.scale(s, s)
    rr = skia.RRect.MakeRectXY(skia.Rect(-lw / 2 - 26, -36, lw / 2 + 26, 36), 36, 36)
    aa = a * clamp(kp)
    cv.drawRRect(rr, paint("#000000", int(110 * aa), blur=12))
    cv.drawRRect(rr, paint(SELO_BG, int(245 * aa)))
    cv.drawRRect(rr, paint(CIANO, int(255 * aa), "stroke", 4))
    texto(cv, T_FIX, 0, 16, F_BLACK, 44, "#FFFFFF", int(255 * aa))
    cv.restore()


def ponta_anel(knee, ank, i):
    """Ponto da frente do anel i (mundo, desenho 'em pé'): onde o telestrador marca o fixador."""
    cs, _, d, f = _hastes(knee, ank)
    return (cs[i][0] + f[0] * (RA + 2), cs[i][1] + f[1] * (RA + 2))


def carimbo_cor(cv, s, x, y, rot, t0, t, dur, cor, tam=88, esc0=1.9):
    """Carimbo do veredito: OPACO, cor do semáforo, entra batendo e sai encolhendo para o chip do selo."""
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
    """Ícone da equipe: bustos simples, sem mão, sem instrumento (cópia do cf_retirada_fixador)."""
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


# ================================================================== quadro
VEREDITOS = (("pode1", "anulado1", T_ANUL, AMBAR), ("pode2", "anulado2", T_ANUL, AMBAR),
             ("pode3", "validado", T_VALID, VERDE))
DUR_CARIMBOS = (1.35, 1.35, 0.85)     # o do VALIDADO é curto: o replay sem capa entra logo depois
CARIMBO_Y = JY0 + 190
R0_SEM = 0.60                          # replay sem capa: começa 0,6 s depois do VALIDADO
ETQ_L1 = (176.0, -210.0)               # (v4) etiqueta FIXADOR: deslocamento (tela) a partir do anel marcado
ETQ_L3 = (-190.0, -175.0)


def chip_estado(t, T):
    """(texto, alfa, pontos, cor) do chip: LANCE n -> CHECANDO -> (carimbo) -> veredito na cor dele ->
    JEITO CERTO (verde) enquanto a imagem mostra o jeito certo (o ANULADO nunca fica em cima do jeito certo)."""
    cortes = (0.0, T["cadeira2"], T["cobrir"], 1e9)
    certo = (T["mao"] - 0.08, T["wipe"] + 0.12, None)
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
        if k == 2 and t < T["nao2"] + 0.02:            # durante o replay SEM capa o chip não diz VALIDADO
            return None, 0.0, -1, "#FFFFFF"
        if certo[k] is not None and t >= certo[k]:
            return T_CERTO, prog(t, certo[k], certo[k] + 0.18), -1, VERDE
        a = prog(t, T[vd] + dur - 0.1, T[vd] + dur + 0.1)
        if k == 2:
            a = prog(t, T["nao2"] + 0.02, T["nao2"] + 0.25)
        if certo[k] is not None:
            a *= 1 - prog(t, certo[k] - 0.12, certo[k])
        return s, a, -1, cor
    return None, 0.0, -1, "#FFFFFF"


def cena(cv, t, T):
    """O lance da vez (com a cortina do VAR no replay da cadeira certa). Devolve o que o HUD precisa."""
    info = {}
    if t < T["cadeira2"]:
        cam, pose = cena_l1(cv, t, T)
        info.update(lance=1, cam=cam, pose=pose)
    elif t < T["cobrir"]:
        kw = prog(t, T["wipe"], T["wipe"] + 0.36)
        if kw <= 0:
            cam, pose, b = cena_poltrona(cv, t, T)
            info.update(lance=2, cam=cam, pose=pose, b=b)
        else:
            camc = CAM_L3
            xw = lerp(JX0 - 10, JX1 + 10, e_inout(kw))
            if kw < 1:
                cv.save(); cv.clipRect(skia.Rect(xw, 0, W, H), True)
                cena_poltrona(cv, t, T, camc)
                cv.restore()
            cv.save(); cv.clipRect(skia.Rect(0, 0, xw, H), True)
            cena_certa(cv, t, T, camc)
            cv.restore()
            if kw < 1:
                cv.drawLine(xw, JY0, xw, JY1, paint(CIANO, 160, "stroke", 26, blur=10))
                cv.drawLine(xw, JY0, xw, JY1, paint("#FFFFFF", 255, "stroke", 6))
            info.update(lance=2, cam=camc, certa=True)
    else:
        cam, e = cena_cama(cv, t, T)
        info.update(lance=3, cam=cam, e=e)
    return info


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


def legenda_var(cv, blocos, t, destaque, y_base=1395, tam=80):
    """Cópia da legenda karaokê do cf_comum (mesma tipografia, cores e tempos), com UMA diferença: a palavra
    ativa cresce a partir do PRÓPRIO CENTRO. No cf_comum ela cresce a partir da borda esquerda e, numa
    palavra longa, encosta na seguinte ("CADEIRABAIXA") — defeito reportado ao dono do cf_comum."""
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
    """Cópia do cf_comum.interface (rodapé CFM a partir de 3 s, cartão final com a CTA e o aviãozinho),
    usando a legenda_var acima."""
    t_cta = T["manda"] - 0.15
    if t < t_cta:
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


def quadro(cv, t, T, blocos, ep):
    fundo(cv, t)
    t_off = T["off"]
    # ---------- TV desligando: a imagem achata numa linha, vira ponto e some
    k_v = prog(t, t_off, t_off + 0.22) ** 2; k_h = e_inout(prog(t, t_off + 0.2, t_off + 0.36))
    tela_ligada = t < t_off + 0.38
    jan_rr = skia.RRect.MakeRectXY(JAN, JAN_R, JAN_R)
    # depois de desligada, a TV some (a equipe e a CTA ficam sobre o fundo limpo, sem caixa escura)
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
        if lance == 1:                                   # círculo no PUNHO fechado na haste
            pose = info["pose"]
            kN, aN = ik2(pose["hip"], ANK_N, COXA, CANELA, 1)
            g, d, f = ponto_pega(kN, aN)
            hx, hy = na_tela(cam, g[0] + f[0] * 4, g[1] + f[1] * 4)
            s = cam[0]
            k1 = e_out(prog(t, T["pode1"] + 0.12, T["pode1"] + 0.47))
            k0 = 1.0 if t < T["var"] else 0.0
            fora = 1 - prog(t, T["alca"], T["alca"] + 0.25)
            a_c = max(k0 * (1 - prog(t, T["var"], T["var"] + 0.12)), k1 * fora)
            k_tr = 1.0 if t < T["var"] else k1
            pul = 0.5 + 0.5 * math.sin(t * 8) if t < T["var"] or T["pode1_fim"] < t < T["anulado1"] else 0.0
            pul += 1.5 * max(0.0, 1 - abs(t - T["chama"] - 0.1) / 0.18)
            rr_ = 78 * min(s, 1.9)
            circulo_tele(cv, hx, hy, rr_, rr_ * 1.08, k_tr, a_c, 0.7, pul)
            # (v4) em "fixador": o analista marca o objeto e dá o nome dele (sai antes do congelar)
            a_et = janela(t, T["fix1"] - 0.05, T["pode1"] - 0.12, 0.15, 0.18)
            if a_et > 0:
                ax, ay = na_tela(cam, *ponta_anel(kN, aN, 2))
                etiqueta_tele(cv, t, ax, ay, ax + ETQ_L1[0], ay + ETQ_L1[1],
                              prog(t, T["fix1"] - 0.05, T["fix1"] + 0.4), a_et)
        elif lance == 2 and "b" in info:                 # círculo no ASSENTO onde o quadril afundou
            hx_, hy_ = info["pose"]["hip"]
            cx_, cy_ = na_tela(cam, hx_ + 40, hy_ + 6)
            s = cam[0]
            k1 = e_out(prog(t, T["pode2"] + 0.12, T["pode2"] + 0.47))
            fora = 1 - prog(t, T["anulado2"] + 0.3, T["anulado2"] + 0.55)
            pul = 0.5 + 0.5 * math.sin(t * 8) if T["pode2_fim"] < t < T["anulado2"] else 0.0
            circulo_tele(cv, cx_, cy_, 165 * s, 92 * s, k1, k1 * fora, 4.3, pul)
        elif lance == 3:                                 # círculo na capa
            cx_, cy_ = na_tela(cam, *centro_capa())
            s = cam[0]
            k1 = e_out(prog(t, T["pode3"] + 0.12, T["pode3"] + 0.47))
            fora = 1 - prog(t, T["validado"] + 0.25, T["validado"] + 0.45)
            pul = 0.5 + 0.5 * math.sin(t * 8) if T["pode3_fim"] < t < T["validado"] else 0.0
            circulo_tele(cv, cx_, cy_, 150 * s, 112 * s, k1, k1 * fora, 2.1, pul)
            # (v4) em "fixador": a mesma marcação do lance 1, no aparelho deitado (fica enquanto a capa cobre)
            a_et = janela(t, T["fix2"] - 0.05, T["pode3"] - 0.1, 0.15, 0.18)
            if a_et > 0:
                bd = corpo(POSE_DEITADA)
                ax, ay = na_tela(cam, *gira(ponta_anel(bd["kN"], bd["aN"], 1)))
                etiqueta_tele(cv, t, ax, ay, ax + ETQ_L3[0], ay + ETQ_L3[1],
                              prog(t, T["fix2"] - 0.05, T["fix2"] + 0.4), a_et)
            e = info["e"]
            if e["sem"] > 0:                             # replay SEM capa: imagem de "lembrança" (fria)
                cv.drawRect(JAN, paint("#0E2A3A", int(70 * e["sem"])))
            if e["snag"]:                                # o X âmbar no ponto onde o lençol enganchou
                gx, gy = gancho_tela(cam)
                k_x = e_back(prog(t, T["validado"] + R0_SEM + 0.42, T["validado"] + R0_SEM + 0.66))
                cv.save(); cv.translate(gx, gy - 92); cv.scale(clamp(k_x, 0, 1.2), clamp(k_x, 0, 1.2))
                marca_x(cv, 0, 0, 34, AMBAR, e["sem"])
                cv.restore()
                cv.drawCircle(gx, gy, 16, paint(AMBAR, int(255 * e["sem"]), "stroke", 5))
            if e["passou"] > 0:                          # o visto verde quando o lençol passa do pé sem prender
                xs_, ys_ = na_tela(cam, 850, 640)
                k_ok = e_back(prog(t, T["lencol_fim"] - 0.12, T["lencol_fim"] + 0.12))
                cv.save(); cv.translate(xs_, ys_); cv.scale(clamp(k_ok, 0, 1.2), clamp(k_ok, 0, 1.2))
                marca_ok(cv, 0, 0, 34, VERDE, e["passou"])
                cv.restore()
        # flash dos congelamentos e dos cortes de lance
        for t0, forca in ((T["pode1"], 150), (T["pode2"], 150), (T["pode3"], 150), (T["cadeira2"], 190),
                          (T["cobrir"], 190)):
            k = t - t0
            if 0 <= k < 0.16:
                cv.drawRect(JAN, paint("#FFFFFF", int(forca * (1 - k / 0.16))))
        cv.restore()
        # replay sem capa: rebobina na ida e "avança" na volta (faixas de fita)
        if lance == 3:
            r0 = T["validado"] + R0_SEM; r1 = T["nao2"] + 0.02
            ruido_vhs(cv, t, max(janela(t, r0 - 0.06, r0 + 0.1, 0.03, 0.06), janela(t, r1 - 0.08, r1 + 0.06, 0.03, 0.06)))
        varre = 0.0
        for pd, vd, _, _ in VEREDITOS:
            if T[pd + "_fim"] < t < T[vd]:
                varre = prog(t, T[pd + "_fim"], T[vd] - 0.05)
        moldura(cv, t, a_hud, varre)
        congelado = t < T["var"] or any(T[pd] + 0.02 <= t < T[vd] for pd, vd, _, _ in VEREDITOS)
        icone_pausa(cv, JX1 - 70, JY1 - 74, a_hud * (1.0 if congelado else 0.0))
        a_reb = max(janela(t, T["var"], T["var"] + 0.5, 0.03, 0.08),
                    janela(t, T["validado"] + R0_SEM - 0.02, T["nao2"] + 0.02, 0.06, 0.08))
        icone_rebobina(cv, JX1 - 76, JY1 - 74, a_hud * a_reb)
        for (pd, vd, s_, cor), dur in zip(VEREDITOS, DUR_CARIMBOS):
            carimbo_cor(cv, s_, CX, CARIMBO_Y, -5, T[vd] - 0.02, t, dur, cor)
        # rótulo grande do corte de lance (LANCE 2 / LANCE 3)
        for t0, s in ((T["cadeira2"], T_LANCE[1]), (T["cobrir"], T_LANCE[2])):
            k = t - t0
            if -0.02 <= k < 0.6:
                a = prog(k, 0.0, 0.08) * (1 - prog(k, 0.42, 0.6))
                esc = lerp(1.25, 1.0, e_out(prog(k, 0.0, 0.16)))
                cv.save(); cv.translate(JX0 + 210, JY0 + 112); cv.scale(esc, esc)     # canto de cima: não cobre a pessoa
                f = skia.Font(F_BLACK, 70); lw = f.measureText(s)
                rr = skia.RRect.MakeRectXY(skia.Rect(-lw / 2 - 34, -70, lw / 2 + 34, 26), 16, 16)
                cv.drawRRect(rr, paint(CARTAO, int(225 * a))); cv.drawRRect(rr, paint(CIANO, int(255 * a), "stroke", 4))
                texto(cv, s, 0, 0, F_BLACK, 70, "#FFFFFF", int(255 * a))
                cv.restore()

    # ---------- selo VAR + chip: entra em "VAR" (o quadro 0 só tem o gancho de texto), dentro do monitor;
    # sobe para a faixa de cima DEPOIS que o gancho saiu
    t_capa = T["pode1_fim"] + 0.06
    sobe = e_inout(prog(t, t_capa + 0.45, t_capa + 0.85))
    chip, a_chip, pontos, cor_chip = chip_estado(t, T)
    k_s = prog(t, T["var"] - 0.04, T["var"] + 0.14)
    esc_s = lerp(0.92, 1.08, sobe) * (1 + 0.25 * (1 - e_back(k_s))) if k_s < 1 else lerp(0.92, 1.08, sobe)
    selo_var(cv, t, lerp(56, 64, sobe), lerp(JY0 + 24, 146, sobe), esc_s, a_hud * clamp(k_s * 1.5), chip, a_chip,
             pontos, cor_chip)

    # ---------- fim: o VAR saiu; no seu caso, quem apita é a equipe
    a_eq = prog(t, T["no"] - 0.1, T["no"] + 0.1) * (1 - prog(t, T["manda"] - 0.35, T["manda"] - 0.1))
    if a_eq > 0:
        cv.drawCircle(CX, 800, 270, paint(TEAL, int(40 * a_eq), blur=60))
        equipe(cv, CX, 860, t, T["no"] - 0.1, a_eq, esc=1.65)
        pul = 1 + 0.06 * max(0.0, 1 - abs(t - T["equipe"] - 0.1) / 0.2)
        if pul > 1:
            cv.drawCircle(CX, 830, 200 * pul, paint(TEAL, int(70 * (pul - 1) / 0.06), "stroke", 6, blur=4))
        ka = e_out(prog(t, T["quem"] - 0.05, T["apita"] + 0.15))      # o apito passa para a equipe
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


def apito(dur=0.30, seed=11, ganho=0.55, solta=0.04):
    """Apito de árbitro: senoide ~3,2 kHz com o trinado da bolinha (FM e AM a ~40 Hz) + sopro."""
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


def pano(seed=91, dur=0.42):
    """Tecido roçando (capa caindo / lençol deslizando): ruído em banda média, envelope macio."""
    n = int(dur * SR); t = np.arange(n) / SR
    x = _passa_banda(np.random.default_rng(seed).standard_normal(n), 500, 3200)
    return x * np.sin(np.pi * t / dur) ** 2 * 0.9


def pano_longo():
    return pano(92, 0.7)


def fofo(seed=101):
    """Almofada cedendo: 'pfff' grave e abafado + baque mole."""
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


SFX = dict(som.SFX)
SFX.update({"apito": apito, "apito_final": apito_final, "rebobinar": rebobinar, "bipe": bipe, "bipe_alto": bipe_alto,
            "obturador": obturador, "pano": pano, "pano_longo": pano_longo, "fofo": fofo, "tv_desliga": tv_desliga})


def _media_movel(x, w):
    """Igual a np.convolve(x, np.ones(w) / w, 'same'), por soma acumulada (sem o custo O(n·w))."""
    n = len(x)
    c = np.concatenate([[0.0], np.cumsum(x)])
    i = np.arange(n)
    lo = np.clip(i - w // 2, 0, n); hi = np.clip(i + (w - 1) // 2 + 1, 0, n)
    return (c[hi] - c[lo]) / w


def mixar(voz, dur, eventos, ganho_trilha=0.40):
    """Cópia do som.mixar (mesma trilha, mesmo ducking) que conhece os efeitos novos desta série."""
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
    ev = [(0.0, "apito", 0.85), (T["chama"] + 0.02, "pop", 0.25), (T["var"] - 0.02, "rebobinar", 0.7),
          (T["segurar"] - 0.05, "whoosh", 0.28), (T["segurar"] + 0.4, "ping", 0.35), (T["fix1"] + 0.12, "pop", 0.3),
          (T["levantar"] - 0.05, "whoosh", 0.3)]
    for pd, vd, _, _ in VEREDITOS:
        ev.append((T[pd] - 0.01, "obturador", 0.85))
        t0 = T[pd + "_fim"] + 0.07
        ev += [(t0, "bipe", 0.75), (t0 + 0.22, "bipe", 0.75), (t0 + 0.44, "bipe_alto", 0.8)]
        ev.append((T[vd] - 0.02, "thump", 0.9))
    ev += [(T["validado"] - 0.26, "apito", 0.45)]                     # apito curto no silêncio antes do VALIDADO
    # lance 1 — alça
    ev += [(T["ap_alca"] + 0.05 + 0.12 * i, "ping", 0.3 - 0.05 * i) for i in range(3)]
    ev += [(T["alca"] + 0.02, "pop", 0.5), (T["mao"] - 0.05, "whoosh", 0.28), (T["cadeira1"] + 0.05, "tick", 0.45),
           (T["sobe"] - 0.05, "whoosh", 0.42), (T["sobe"] + 0.8, "thump", 0.4)]
    # lance 2 — poltrona fofinha
    ev += [(T["cadeira2"] - 0.03, "tick", 0.55), (T["cadeira2"] + 0.02, "whoosh", 0.45),
           (T["fofinha"] - 0.02, "fofo", 0.45), (T["macia"] + 0.02, "fofo", 0.3), (T["forca"] - 0.02, "whoosh", 0.22),
           (T["joelho"] + 0.02, "pop", 0.3)]
    ev += [(T["apf"] + 0.05 + 0.1 * i, "tick", 0.3 - 0.06 * i) for i in range(3)]     # metal forçado
    ev += [(T["wipe"] - 0.02, "whoosh", 0.42), (T["wipe"] + 0.3, "shimmer", 0.25)]
    # lance 3 — capa
    r0, r1 = T["validado"] + R0_SEM, T["nao2"] + 0.02
    ev += [(T["cobrir"] - 0.03, "tick", 0.55), (T["cobrir"] + 0.02, "whoosh", 0.45), (T["fix2"] + 0.1, "ping", 0.28),
           (T["com"] - 0.02, "pano", 0.55), (T["capa_fim"] + 0.05, "thump", 0.22)]
    ev += [(r0 - 0.06, "rebobinar", 0.35), (r0 + 0.08, "pano", 0.35), (r0 + 0.42, "tick", 0.6),
           (r0 + 0.47, "pano", 0.3), (r0 + 0.72, "pano", 0.25), (r1 - 0.06, "whoosh", 0.35),
           (T["enrosca"] - 0.05, "pano_longo", 0.5), (T["lencol_fim"], "shimmer", 0.25)]
    ev += [(T["protege"] - 0.02, "pano", 0.3), (T["protege"] + 0.35, "fofo", 0.28), (T["protege"] + 0.4, "shimmer", 0.22)]
    # apito final, TV desligando, equipe, apito passando, CTA
    ev += [(T["apito_f"], "apito_final", 0.6), (T["off"] + 0.02, "tv_desliga", 0.75)]
    ev += [(T["no"] - 0.1 + 0.08 * k + 0.2, "pop", 0.28) for k in range(3)]
    ev += [(T["apita"] + 0.1, "pop", 0.32), (T["equipe"], "shimmer", 0.4), (T["manda"] + 0.05, "whoosh", 0.5)]
    return ev


def tempos_previa(T):
    return [0.0, T["var"] + 0.25, T["segurar"] + 0.5, T["fix1"] + 0.45, T["levantar"] + 0.45, T["pode1"] + 0.55,
            T["anulado1"] + 0.3,
            T["alca"] + 0.2, T["alca"] + 0.45, T["mao"] + 0.1, T["livre"] + 0.25,
            T["cadeira2"] + 0.3, T["fofinha"] + 0.3, T["pode2"] + 0.6, T["anulado2"] + 0.4, T["demais"] + 0.1,
            T["forca"] + 0.25, T["joelho"] + 0.2, T["apf"] + 0.3, T["wipe"] + 0.2, T["wipe"] + 0.7,
            T["cobrir"] + 0.3, T["fix2"] + 0.4, T["capa"] + 0.3, T["pode3"] + 0.6, T["validado"] + 0.4,
            T["validado"] + 0.6, T["validado"] + 0.9, T["nao2"] - 0.1, T["enrosca"] + 0.3, T["lencol"] + 0.3,
            T["protege"] + 0.3, T["dorme"] + 0.2, T["off"] + 0.1, T["no"] + 0.3, T["apita"] + 0.3, T["equipe"] + 0.3,
            T["manda"] + 0.5, T["manda"] + 1.6]


# ================================================================== render (cópia do cf_comum.fazer_render + pausas)
VAO_CHECANDO = 0.86                   # fim de "pode?" -> veredito: ~0,3 s de congelar + ~0,55 s de CHECANDO
VAOS_EXTRA = (("cobrir", 1, 0.92),    # replay da cadeira certa (verde, JEITO CERTO), sem fala
              ("não", 2, 0.95),       # replay SEM capa: o lençol engancha no anel, antes de "não enrosca"
              ("no", 3, 1.12))        # apito final + TV desligando, antes de "No seu caso"
PRE_APITO = 0.25                      # o apito do quadro 0 não embola com "Chama"


def pausa_checando(audio, pal, vao=VAO_CHECANDO):
    """Insere silêncio depois de cada 'pode?' até o vão chegar a `vao` (cópia de _trabalho/medir_tempos.py)."""
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
    """Silêncio antes da n-ésima `palavra` até o vão chegar a `vao` (nada da fala é cortado)."""
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
    T["wipe"] = T["apf_fim"] + 0.06              # replay da cadeira certa logo depois de "aparelho."
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
        blocos = montar_blocos(pal)

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
