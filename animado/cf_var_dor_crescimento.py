# -*- coding: utf-8 -*-
"""CHAMA O VAR — "DOR DE CRESCIMENTO / MASSAGEM PODE?" (a crise de dor de crescimento em casa: pode ou não pode?).

v2 (correção pós leitor às cegas + revisor): quadro 0 = as mãos JÁ massageando a panturrilha (sem compressa); a
compressa é um pano dobrado de verdade (ponta dobrada, franjinha, canto caído) e só entra em "compressa"; o carimbo
do LANCE 1 diz a condição ("SE DÓI NAS DUAS PERNAS"); LANCE 2 sem laço no joelho da manhã (o círculo e o X caem na
linha, na divisória) e os vistos ancorados nas pernas; LANCE 3 com a câmera perto da perna que dói (joelho que
incha com setas para fora, termômetro grande, pegadas de passo curto/longo) e, em "Chamar de crescimento", a tela
dividida contra o padrão do LANCE 1 ("SE DÓI NAS DUAS PERNAS") — o X cai na linha, nunca sobre a criança; a porta
leva o estetoscópio (a cruz verde lia como farmácia); a mãozinha sai pela borda de baixo; o fecho sem apito.

v3 (revisão em resolução cheia; só DESENHO — texto, voz e tempos iguais): a compressa vira toalhinha BRANCA (era
pêssego = tom da pele: coxa, canela e pano viravam um bloco bege), cobre só o meio/alto da canela (a canela de baixo
aparece), perde a aba pendente (lia como panturrilha deformada) e o calor "morna" vai para a cama, atrás das pernas;
na MANHÃ do lance 2 o pé de trás sai de cima da divisória (o tênis era cortado na vertical o lance inteiro); no
LANCE 3 o chip "SE DÓI NAS DUAS PERNAS" desce para o chão da metade esquerda e é desenhado depois do carimbo (o
ANULADO ficava colado embaixo dele e, na saída, passava por cima de "DUAS PERNAS").

v4 (2ª revisão em resolução cheia; só DESENHO — texto, voz e tempos iguais; a v3 fica): (1) na MANHÃ do lance 2 os
dois tênis ficam de perfil para a DIREITA (para a bola) e PISAM no chão (antes o de trás apontava ~45° para
baixo-esquerda, solado para fora — o pé lia como torcido — e os dois flutuavam acima do rodapé); o quique é do
quadril, com os pés no chão. (2) Nas cenas de cama a criança aparece INTEIRA: recostada num travesseiro claro na
cabeceira, cabeça com cabelo (sem rosto), ombros de pijama, o corpo sob o cobertor até o peito e o bracinho por
cima dele (antes um volume de bolinhas com dobra de travesseiro: as pernas saíam do nada).

v5 (3ª revisão em resolução cheia; só DESENHO — texto, voz e tempos iguais; v3 e v4 ficam): o carimbo VALIDADO /
SE DÓI NAS DUAS PERNAS do LANCE 1 sai do canto superior esquerdo da cena (420, 470) — onde, desde que a v4 pôs a
cabeça da criança na cabeceira, ele cobria cabeça e rosto de 5,4 a 6,2 s — e pousa na faixa ACIMA do monitor, à
direita do selo VAR, só encostando na borda de cima da janela (sobre o céu/janela da casa, longe da criança e com
os braços adultos entrando livres); a saída encolhendo para o chip do selo fica curta e não cruza a cena.

Série "Chama o VAR" (ter/qui/sáb), construído sobre o piloto cf_chamaovar_rotina_fixador e os episódios do gesso e
dos primeiros socorros: os helpers da série (monitor, selo VAR + chip de estado, telestrador, carimbo com 2ª linha,
rebobinar, TV desligando, apito, sons, legenda karaokê, render com CHECANDO) estão COPIADOS aqui, sem importar
nenhum outro episódio. Contrato de cena do cf_comum (ANCORAS, DESTAQUE, quadro, sons, tempos_previa, render no
nível de cima).

Lances do MESMO quarto, de noite (fontes conferidas na peça certa: lab/formato_novo/cf_var_dor_crescimento/
storyboard.json):
  1. massagem na crise da noite -> VALIDADO / SE DÓI NAS DUAS PERNAS (crescimento-sex: "Compressa morna e massagem
     na perna costumam aliviar bem na hora."; "Ficar perto, conversar e tranquilizar ajuda — a criança sente a sua
     calma."; crescimento-seg: "nas duas pernas, e melhora pela manhã");
  2. chamar de frescura -> ANULADO: é real, e some pela manhã (pnc_dor_crescimento; crescimento-seg);
  3. dor de um lado só, inchaço, febre ou manqueira, chamar de crescimento -> ANULADO: leve para avaliar
     (crescimento-sex "não trate como “crescimento”: avalie."; pnc_dor_crescimento; crescimento-sab; pnc_mancando).
     Fecho: febre + manqueira juntas = atendimento no mesmo dia (pnc_mancar_febre).

O que a cena mostra (a palavra falada comanda o quadro — ANCORAS):
  * quadro 0: o lance 1 JÁ CONGELADO: quarto à noite (parede azul-médio, lua na janela), as DUAS perninhas de pijama
    (calça arregaçada até o joelho, meias) saindo de baixo do cobertor dobrado, risquinhos de dor LILÁS fora da pele
    das duas panturrilhas, ursinho junto dos pés; as duas mãos adultas (manga teal) JÁ massageando a panturrilha
    (dedos abertos); círculo de telestrador e pausa; o gancho é o único texto grande;
  * "VAR": rebobina (as mãos saem) e a câmera abre; "Dor": os risquinhos pulsam; "pernas": colchetes nas DUAS
    panturrilhas; "noite": a lua brilha e o abajur tremula; "massagem": as mãos pousam na perna, de leve; "pode?":
    congela; "Validado": carimbo VALIDADO / SE DÓI NAS DUAS PERNAS; "massagem": círculos lentos (setas circulares);
    "compressa": a mão direita traz o PANO DOBRADO (ponta dobrada, franjinha, aba caída, felpa) e o pousa POR CIMA
    da panturrilha, e sai; "morna": halo pêssego; "costumam": visto verde ancorado na compressa — os risquinhos
    CONTINUAM (sem promessa); "Fica": a câmera abre (o abajur entra) e a mão esquerda fica PARADA no joelho;
    "criança": o pulso dos risquinhos desacelera; "calma": a poça de luz quente sobre as pernas respira;
  * "E chamar de frescura" (LANCE 2): o monitor se divide: NOITE (as perninhas com os risquinhos) | MANHÃ (as
    mesmas perninhas, de tênis, pulando atrás da bola); "frescura": linha TRACEJADA da dor da noite à perna da manhã
    (a ideia, não a pessoa); "pode?": o círculo marca a LIGAÇÃO, na divisória (nunca uma perna); "Anulado": a linha
    se parte e o X cai ali; "dor ... real": visto verde em cima dos risquinhos da noite (a mão adulta pousa ao lado);
    "some": seta da lua ao sol levando três risquinhos que se apagam pelo caminho; "manhã": visto verde junto da
    perna limpa da manhã;
  * "Dor de um lado só" (LANCE 3): a câmera chega PERTO (1,4x) e os risquinhos ficam só embaixo de uma perna;
    "lado": círculo nela, a outra fica translúcida (a pele não muda de cor); "inchaço": o círculo sai, o joelho
    INCHA (o contorno cresce) com setinhas para fora; "febre": termômetro grande, sem número; "manqueira": pegadas
    em pares desiguais (passo longo/curto, a do pé que dói menor e apagada) rumo à porta; "Chamar de crescimento":
    a tela se divide — entra pela esquerda o padrão do LANCE 1 (as duas pernas com dor, chip verde "SE DÓI NAS DUAS
    PERNAS") e uma linha tracejada liga esse padrão à perna que dói (no máximo 2 grafismos ciano); "pode?": círculo
    SÓ em volta da perna que dói; "Anulado": a linha se parte e o X cai na divisória — nunca sobre a criança;
    "Leve": corte para a porta — o braço adulto desce do alto e a mãozinha sobe da borda de baixo (curta e fina),
    seguindo as pegadas; "avaliar": placa com ESTETOSCÓPIO na porta (pictograma, sem texto), contorno verde + visto;
  * apito final e a TV desliga; "Febre e manqueira juntas": a profissional de saúde (sem rosto, de jaleco e
    estetoscópio, sem nada na mão), termômetro + pegadas que se encostam num círculo só; "mesmo": o sol nasce; CTA.
Guardrails: pele OPACA de desenho e sempre cor de pele (nada vermelho, roxo ou âmbar na pele); nenhum osso, exame,
remédio, sangue; nenhum rosto; noite azul-médio (nunca fundo preto); âmbar só em carimbo e X; ciano = só grafismo
do VAR; dourado = só a legenda e o gancho; dor = risquinhos lilás. Todo texto desenhado está em ep["tela"].
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
    # lance 1 — massagem na crise da noite
    "chama": ("chama", 1, False), "var": ("var", 1, False), "dor1": ("dor", 1, False),
    "pernas": ("pernas", 1, False), "noite1": ("noite", 1, False), "massagem1": ("massagem", 1, False),
    "pode1": ("pode", 1, False), "validado": ("validado", 1, False), "massagem2": ("massagem", 2, False),
    "compressa": ("compressa", 1, False), "morna": ("morna", 1, False), "costumam": ("costumam", 1, False),
    "aliviar": ("aliviar", 1, False), "fica": ("fica", 1, False), "perto": ("perto", 1, False),
    "crianca": ("criança", 1, False), "calma": ("calma", 1, False),
    # lance 2 — chamar de frescura
    "e2": ("e", 2, False), "chamar1": ("chamar", 1, False), "frescura": ("frescura", 1, False),
    "pode2": ("pode", 2, False), "anulado1": ("anulado", 1, False), "dor2": ("dor", 2, False),
    "crescimento1": ("crescimento", 1, False), "real": ("real", 1, False), "some": ("some", 1, False),
    "manha": ("manhã", 1, False),
    # lance 3 — um lado só, inchaço, febre ou manqueira
    "dor3": ("dor", 3, False), "lado": ("lado", 1, False), "inchaco": ("inchaço", 1, False),
    "febre1": ("febre", 1, False), "manqueira1": ("manqueira", 1, False), "chamar2": ("chamar", 2, False),
    "crescimento2": ("crescimento", 2, False), "pode3": ("pode", 3, False), "anulado2": ("anulado", 2, False),
    "trate": ("trate", 1, False), "leve": ("leve", 1, False), "avaliar": ("avaliar", 1, False),
    # fecho e CTA
    "febre2": ("febre", 2, False), "manqueira2": ("manqueira", 2, False), "juntas": ("juntas", 1, False),
    "mesmo": ("mesmo", 1, False), "dia": ("dia", 1, False), "manda": ("manda", 1, False),
    "perninha": ("perninha", 1, False),
}
FIM_DE = ("pode1", "pode2", "pode3", "avaliar", "calma", "manha", "aliviar", "frescura")
DESTAQUE = {"var", "massagem", "morna", "calma", "frescura", "real", "manhã", "lado", "febre", "manqueira", "avaliar",
            "juntas", "dia", "perninha"}

# rótulos (todos estão em ep["tela"])
T_VAR = "VAR"
T_LANCE = ("LANCE 1", "LANCE 2", "LANCE 3")
T_CHEC = "CHECANDO"
T_ANUL = "ANULADO"
T_VALID = "VALIDADO"
T_DUAS = "SE DÓI NAS DUAS PERNAS"         # a CONDIÇÃO do VALIDADO (e o padrão que o LANCE 3 contrasta)
T_CERTO = "JEITO CERTO"
T_SERIE = "CHAMA O VAR"

# ------------------------------------------------------------------ paleta (identidade da série + o quarto)
ARD_IN, ARD_OUT = "#22303F", "#121A24"
CIANO = "#4FD1FF"
VERDE = "#3DDC84"
AMBAR = "#FFA53A"
CARTAO = "#0B1824"
SELO_BG = "#1E2A44"
TEAL = "#5FC4B6"
DOR = "#C7A6FF"                                                                       # risquinhos de dor (lilás)
PELE, PELE_CL, PELE_ESC, PELE_LINHA = "#F0B49A", "#F7CDB8", "#D9937A", "#B9765E"     # criança
AD, AD_CL, AD_ESC, AD_LINHA = "#C98D6E", "#DDA98C", "#A56C50", "#7C4C37"             # adulto (outro tom)
MANGA_AD, MANGA_AD_CL, MANGA_AD_ESC = "#5FC4B6", "#84D6CB", "#3E9C90"                # manga teal do adulto
CALCA, CALCA_CL, CALCA_ESC, CALCA_LINHA = "#F2D98A", "#FAEBB5", "#D9BC62", "#A88A3C"  # pijama amarelo-claro
ESTRELA_PIJ = "#5B7BD5"
MEIA, MEIA_CL, MEIA_ESC = "#E3E9F5", "#F4F6FB", "#BAC6DE"
MEIA_FAIXA = "#8EA8E2"
# quarto à noite
PAREDE, PAREDE_ESC = "#3E5590", "#2C3D6E"
CEU_N1, CEU_N2 = "#16224A", "#2B3E7A"
LUA = "#F6F0C8"
LUZ = "#FFD9A0"
COBERTOR, COBERTOR_CL, COBERTOR_ESC, BOLINHA = "#86A9E0", "#9DBCEC", "#6C8FCB", "#BCD1F3"
MADEIRA, MADEIRA_CL, MADEIRA_ESC = "#7A5E57", "#93746A", "#5C4642"
PISO, PISO_ESC = "#4B4568", "#3B3655"
PORTA, PORTA_ESC, PORTA_BATENTE = "#6A6098", "#574E82", "#8494C6"
URSO, URSO_CL, URSO_ESC = "#B98A5E", "#DDB98F", "#8C6340"
# compressa (morna). v3: era pêssego (#FFD2B0), o MESMO tom da pele: coxa, canela e pano viravam um bloco bege só.
# Agora é uma toalhinha BRANCA com contorno marrom-acinzentado (cor própria, longe da pele, do pijama amarelo, do
# cobertor azul e de todas as cores reservadas da série); o "morna" fica no halo pêssego em volta do pano.
COMP, COMP_CL, COMP_ESC, COMP_DOBRA = "#F8F5EF", "#FFFFFF", "#DCD3C4", "#7E6C5A"
COMP_FELPA, COMP_MORNA = "#C9BDAA", "#FFE6D2"
# manhã
PAREDE_M1, PAREDE_M2 = "#E4EEF8", "#D2E1F0"
PISO_M, PISO_M_ESC = "#E3C9A2", "#CDAE82"
SOL = "#FFE07A"
TENIS, TENIS_FAIXA, TENIS_SOLA = "#F7F9FC", "#3D6FD1", "#C5CFDC"
# pictogramas
TERMO_C, TERMO_COL = "#F4F7FB", "#D9C6FF"
PEGADA = "#E2E7F2"

TONS_PELE = (PELE_ESC, PELE, PELE_CL, PELE, PELE_ESC)
TONS_AD = (AD_ESC, AD, AD_CL, AD, AD_ESC)
TONS_MANGA_AD = (MANGA_AD_ESC, MANGA_AD, MANGA_AD_CL, MANGA_AD, MANGA_AD_ESC)
TONS_CALCA = (CALCA_ESC, CALCA, CALCA_CL, CALCA, CALCA_ESC)
TONS_MEIA = (MEIA_ESC, MEIA, MEIA_CL, MEIA, MEIA_ESC)

# ------------------------------------------------------------------ o monitor (janela da cena) — igual ao piloto
JX0, JY0, JX1, JY1 = 28.0, 300.0, 1052.0, 1226.0
JCX, JCY = (JX0 + JX1) / 2, (JY0 + JY1) / 2
JAN = skia.Rect(JX0, JY0, JX1, JY1)
JAN_R = 26
DIV_X = JCX                                     # divisória do LANCE 2 (noite | manhã)


# ------------------------------------------------------------------ utilidades (cópias do piloto)
def _c(h, a=255):
    h = h.lstrip("#")
    return skia.ColorSetARGB(int(a), int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))


def esc_cor(h, k):
    return lerpc(h, "#000000", k)


def tons_esc(tons, k):
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


def oval_path(x0, y0, x1, y1):
    p = skia.Path(); p.addOval(skia.Rect(x0, y0, x1, y1)); return p


def circ_path(x, y, r):
    p = skia.Path(); p.addCircle(x, y, r); return p


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
    return uniao(p, circ_path(p0[0], p0[1], w0 / 2), circ_path(p1[0], p1[1], w1 / 2))


def tubo(p0, p1, rfun, e=1.0, n=16):
    """Tubo de p0 a p1 com raio variável rfun(u) (u = 0 em p0, 1 em p1), pontas redondas."""
    dx, dy = p1[0] - p0[0], p1[1] - p0[1]; L = math.hypot(dx, dy) or 1.0
    nx, ny = -dy / L, dx / L
    top, bot = [], []
    for i in range(n + 1):
        u = i / n; r = rfun(u) * e
        cx_, cy_ = p0[0] + dx * u, p0[1] + dy * u
        top.append((cx_ + nx * r, cy_ + ny * r)); bot.append((cx_ - nx * r, cy_ - ny * r))
    p = poli(top + bot[::-1])
    return uniao(p, circ_path(p0[0], p0[1], rfun(0) * e), circ_path(p1[0], p1[1], rfun(1) * e))


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


def unit(dx, dy):
    L = math.hypot(dx, dy) or 1.0
    return dx / L, dy / L


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
    """cam = (escala, foco x, foco y[, centro x na tela]) — o foco cai no centro (do monitor ou da metade)."""
    s, fx, fy = cam[:3]; cx_ = cam[3] if len(cam) > 3 else JCX
    cv.translate(cx_, JCY); cv.scale(s, s); cv.translate(-fx, -fy)


def na_tela(cam, x, y):
    s, fx, fy = cam[:3]; cx_ = cam[3] if len(cam) > 3 else JCX
    return cx_ + (x - fx) * s, JCY + (y - fy) * s


def cam4(cam):
    return tuple(cam[:3]) + ((cam[3] if len(cam) > 3 else JCX),)


# ================================================================== O QUARTO À NOITE (cenário em cache)
QX0, QY0, QX1, QY1, QESC = -220.0, 250.0, 1720.0, 1520.0, 1.4
PISO_Y = 1075.0                                   # onde a parede encontra o chão
JANELA = (330.0, 420.0, 560.0, 650.0)
LUA_C = (500.0, 512.0)
ABAJUR = (190.0, 760.0)                           # centro da cúpula
POCA = (560.0, 880.0)                             # centro da poça de luz na cama
PORTA_R = (1170.0, 600.0, 1332.0, PISO_Y)
CAMA_X0, CAMA_X1, CAMA_Y_FUNDO, CAMA_Y_FRENTE, CAMA_Y_BAIXO = 285.0, 1060.0, 742.0, 968.0, 1045.0


def _estrela4(cv, x, y, r, cor, a):
    p = poli([(x, y - r), (x + r * 0.28, y - r * 0.28), (x + r, y), (x + r * 0.28, y + r * 0.28), (x, y + r),
              (x - r * 0.28, y + r * 0.28), (x - r, y), (x - r * 0.28, y - r * 0.28)])
    cv.drawPath(p, paint(cor, int(a)))


def _bolinhas(cv, clip, x0, y0, x1, y1, passo, r, cor, a):
    cv.save(); cv.clipPath(clip, skia.ClipOp.kIntersect, True)
    j = 0
    y = y0
    while y < y1:
        x = x0 + (passo / 2 if j % 2 else 0)
        while x < x1:
            cv.drawCircle(x, y, r, paint(cor, a))
            x += passo
        y += passo * 0.62; j += 1
    cv.restore()


def quarto(cv):
    def _d(c):
        c.scale(QESC, QESC); c.translate(-QX0, -QY0); _quarto(c)
    img = cacheado("quarto", (QX1 - QX0) * QESC, (QY1 - QY0) * QESC, _d)
    cv.save(); cv.translate(QX0, QY0); cv.scale(1 / QESC, 1 / QESC)
    cv.drawImage(img, 0, 0, LINEAR)
    cv.restore()


def _quarto(cv):
    # parede: azul-médio, mais escura no alto e nas bordas (nunca preta)
    sh = skia.GradientShader.MakeLinear([skia.Point(0, QY0), skia.Point(0, PISO_Y)],
                                        [_c(PAREDE_ESC), _c(PAREDE), _c("#3A5089")], [0.0, 0.55, 1.0])
    cv.drawRect(skia.Rect(QX0, QY0, QX1, PISO_Y), paint(PAREDE, shader=sh))
    rng = np.random.default_rng(5)                                   # estrelinhas do papel de parede (quarto de criança)
    for gy in range(int(QY0) + 40, int(PISO_Y) - 60, 92):
        for gx in range(int(QX0) + 30, int(QX1), 104):
            x = gx + (52 if (gy // 92) % 2 else 0) + rng.uniform(-8, 8); y = gy + rng.uniform(-8, 8)
            _estrela4(cv, x, y, 7, "#5670AE", 150)
    # rodapé
    cv.drawRect(skia.Rect(QX0, PISO_Y - 18, QX1, PISO_Y), paint("#5A6CA6"))
    cv.drawLine(QX0, PISO_Y - 18, QX1, PISO_Y - 18, paint("#7183BC", 255, "stroke", 3))
    # chão de tábuas
    sh = skia.GradientShader.MakeLinear([skia.Point(0, PISO_Y), skia.Point(0, QY1)], [_c("#56507A"), _c(PISO), _c(PISO_ESC)],
                                        [0.0, 0.35, 1.0])
    cv.drawRect(skia.Rect(QX0, PISO_Y, QX1, QY1), paint(PISO, shader=sh))
    y = PISO_Y; dy = 26.0
    while y < QY1:
        y += dy; dy *= 1.22
        cv.drawLine(QX0, y, QX1, y, paint("#3E3858", 220, "stroke", 3))
    # janela com a lua e 3 estrelinhas (sem texto)
    x0, y0, x1, y1 = JANELA
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(x0 - 16, y0 - 16, x1 + 16, y1 + 16), 8, 8), paint("#000000", 60, blur=10))
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(x0 - 14, y0 - 14, x1 + 14, y1 + 14), 8, 8), paint("#A6B5DA"))
    ceu = skia.GradientShader.MakeLinear([skia.Point(0, y0), skia.Point(0, y1)], [_c(CEU_N1), _c(CEU_N2)])
    cv.drawRect(skia.Rect(x0, y0, x1, y1), paint(CEU_N1, shader=ceu))
    lx, ly = LUA_C
    cv.drawCircle(lx, ly, 62, paint(LUA, 50, blur=18))
    lua = skia.Op(circ_path(lx, ly, 36), circ_path(lx + 17, ly - 11, 31), skia.PathOp.kDifference_PathOp)
    cv.drawPath(lua, paint(LUA))
    for (sx, sy, r) in ((370.0, 470.0, 9.0), (420.0, 600.0, 7.0), (535.0, 612.0, 8.0)):
        _estrela4(cv, sx, sy, r, LUA, 255)
    cv.drawLine((x0 + x1) / 2, y0, (x0 + x1) / 2, y1, paint("#A6B5DA", 255, "stroke", 10))
    cv.drawLine(x0, (y0 + y1) / 2, x1, (y0 + y1) / 2, paint("#A6B5DA", 255, "stroke", 10))
    cv.drawRect(skia.Rect(x0 - 26, y1 + 12, x1 + 26, y1 + 28), paint("#B7C4E4"))
    # porta (sem placa, sem texto)
    px0, py0, px1, py1 = PORTA_R
    cv.drawRect(skia.Rect(px0 - 16, py0 - 16, px1 + 16, py1), paint(PORTA_BATENTE))
    sh = skia.GradientShader.MakeLinear([skia.Point(px0, 0), skia.Point(px1, 0)], [_c(PORTA_ESC), _c(PORTA), _c(PORTA_ESC)])
    cv.drawRect(skia.Rect(px0, py0, px1, py1), paint(PORTA, shader=sh))
    for (a0, b0, a1, b1) in ((px0 + 22, py0 + 26, px1 - 22, py0 + 196), (px0 + 22, py0 + 230, px1 - 22, py1 - 30)):
        cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(a0, b0, a1, b1), 6, 6), paint(PORTA_ESC, 255, "stroke", 5))
    cv.drawCircle(px0 + 26, 858, 10, paint("#D9DEEA")); cv.drawCircle(px0 + 26, 858, 10, paint("#8E99B8", 255, "stroke", 2))
    # criado-mudo e o abajur (cúpula creme acesa)
    cv.drawRect(skia.Rect(108, 862, 272, PISO_Y + 6), paint("#000000", 60, blur=10))
    sh = skia.GradientShader.MakeLinear([skia.Point(110, 0), skia.Point(270, 0)], [_c(MADEIRA_ESC), _c(MADEIRA), _c(MADEIRA_ESC)])
    cv.drawRect(skia.Rect(115, 870, 265, PISO_Y + 4), paint(MADEIRA, shader=sh))
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(106, 856, 274, 876), 6, 6), paint(MADEIRA_CL))
    cv.drawLine(125, 960, 255, 960, paint(MADEIRA_ESC, 255, "stroke", 4))
    cv.drawCircle(190, 922, 6, paint("#D8C7A8"))
    ax, ay = ABAJUR
    cv.drawOval(skia.Rect(ax - 34, 846, ax + 34, 862), paint("#CDBB9C"))
    cv.drawRect(skia.Rect(ax - 5, ay + 30, ax + 5, 852), paint("#BCA98A"))
    cupula = poli([(ax - 32, ay - 40), (ax + 32, ay - 40), (ax + 54, ay + 36), (ax - 54, ay + 36)])
    cv.drawPath(cupula, paint("#FFE3B0", 120, blur=24))
    sh = skia.GradientShader.MakeLinear([skia.Point(0, ay - 40), skia.Point(0, ay + 36)], [_c("#FFF4DC"), _c("#F6DDA8")])
    cv.drawPath(cupula, paint("#F8E6C0", shader=sh))
    cv.drawPath(cupula, paint("#D9B97E", 255, "stroke", 2.5))
    # a cama: cabeceira, colchão com o cobertor azul-claro de bolinhas, a barra caindo na frente, os pés
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(250, 690, 300, 1062), 18, 18), paint("#000000", 60, blur=10))
    sh = skia.GradientShader.MakeLinear([skia.Point(250, 0), skia.Point(300, 0)], [_c(MADEIRA_ESC), _c(MADEIRA_CL), _c(MADEIRA)])
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(252, 690, 300, 1062), 18, 18), paint(MADEIRA, shader=sh))
    for x in (CAMA_X0 + 18, CAMA_X1 - 34):                           # pés da cama
        cv.drawRect(skia.Rect(x, CAMA_Y_BAIXO - 6, x + 18, PISO_Y + 8), paint(MADEIRA_ESC))
    cv.drawOval(skia.Rect(CAMA_X0 - 20, PISO_Y - 4, CAMA_X1 + 30, PISO_Y + 40), paint("#000000", 70, blur=16))
    topo = skia.Path()
    topo.moveTo(CAMA_X0 + 10, CAMA_Y_FUNDO); topo.lineTo(CAMA_X1 - 6, CAMA_Y_FUNDO)
    topo.quadTo(CAMA_X1 + 6, CAMA_Y_FUNDO, CAMA_X1 + 4, CAMA_Y_FUNDO + 30)
    topo.lineTo(CAMA_X1 + 2, CAMA_Y_FRENTE - 18); topo.quadTo(CAMA_X1, CAMA_Y_FRENTE, CAMA_X1 - 24, CAMA_Y_FRENTE)
    topo.lineTo(CAMA_X0 + 20, CAMA_Y_FRENTE); topo.quadTo(CAMA_X0, CAMA_Y_FRENTE, CAMA_X0, CAMA_Y_FRENTE - 20)
    topo.lineTo(CAMA_X0 + 2, CAMA_Y_FUNDO + 20); topo.quadTo(CAMA_X0 + 2, CAMA_Y_FUNDO, CAMA_X0 + 10, CAMA_Y_FUNDO)
    topo.close()
    sh = skia.GradientShader.MakeLinear([skia.Point(0, CAMA_Y_FUNDO), skia.Point(0, CAMA_Y_FRENTE)],
                                        [_c(COBERTOR_ESC), _c(COBERTOR), _c(COBERTOR_CL)])
    cv.drawPath(topo, paint(COBERTOR, shader=sh))
    _bolinhas(cv, topo, CAMA_X0, CAMA_Y_FUNDO + 16, CAMA_X1, CAMA_Y_FRENTE, 46, 5, BOLINHA, 200)
    frente = skia.Path()
    frente.moveTo(CAMA_X0, CAMA_Y_FRENTE - 6); frente.lineTo(CAMA_X1, CAMA_Y_FRENTE - 6)
    frente.lineTo(CAMA_X1 + 2, CAMA_Y_BAIXO)
    n = 14
    for i in range(n + 1):                                          # barra ondulada do cobertor
        x = lerp(CAMA_X1 + 2, CAMA_X0 - 2, i / n)
        frente.lineTo(x, CAMA_Y_BAIXO + (8 if i % 2 else 0))
    frente.close()
    sh = skia.GradientShader.MakeLinear([skia.Point(0, CAMA_Y_FRENTE), skia.Point(0, CAMA_Y_BAIXO)],
                                        [_c("#7B9ED8"), _c("#6585C0")])
    cv.drawPath(frente, paint(COBERTOR, shader=sh))
    _bolinhas(cv, frente, CAMA_X0 + 20, CAMA_Y_FRENTE + 20, CAMA_X1, CAMA_Y_BAIXO + 10, 46, 5, "#A9C2EC", 190)
    cv.drawLine(CAMA_X0 + 6, CAMA_Y_FRENTE - 4, CAMA_X1 - 6, CAMA_Y_FRENTE - 4, paint("#5C7CB6", 200, "stroke", 4))
    # pezeira baixa
    sh = skia.GradientShader.MakeLinear([skia.Point(CAMA_X1 - 10, 0), skia.Point(CAMA_X1 + 23, 0)],
                                        [_c(MADEIRA), _c(MADEIRA_CL), _c(MADEIRA_ESC)])
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(CAMA_X1 - 9, 842, CAMA_X1 + 23, 1062), 14, 14), paint(MADEIRA, shader=sh))
    # luz do abajur: brilho na parede e a poça quente na cama
    cv.drawCircle(ax, ay, 300, paint(LUZ, 255, shader=skia.GradientShader.MakeRadial(
        skia.Point(ax, ay), 300, [_c(LUZ, 120), _c(LUZ, 40), _c(LUZ, 0)], [0.0, 0.45, 1.0])))
    pc = skia.GradientShader.MakeRadial(skia.Point(*POCA), 400, [_c(LUZ, 95), _c(LUZ, 40), _c(LUZ, 0)], [0.0, 0.55, 1.0],
                                        skia.TileMode.kClamp, 0, skia.Matrix.Scale(1.0, 0.36).postTranslate(0, POCA[1] * 0.64))
    cv.save(); cv.clipPath(uniao(topo, frente), skia.ClipOp.kIntersect, True)
    cv.drawRect(skia.Rect(QX0, CAMA_Y_FUNDO - 40, QX1, CAMA_Y_BAIXO + 20), paint(LUZ, shader=pc))
    cv.restore()


DOBRA_X0, DOBRA_Y0, DOBRA_X1, DOBRA_Y1 = 236.0, 548.0, 660.0, 1070.0


def dobra(cv, a=1.0):
    """A criança RECOSTADA no travesseiro e COBERTA até o peito (v4): travesseiro, cabeça com cabelo (sem rosto),
    ombros de pijama, o corpo sob o cobertor e o bracinho por cima dele; só as perninhas ficam de fora."""
    def _d(c):
        c.scale(QESC, QESC); c.translate(-DOBRA_X0, -DOBRA_Y0); _dobra(c)
    img = cacheado("crianca_coberta", (DOBRA_X1 - DOBRA_X0) * QESC, (DOBRA_Y1 - DOBRA_Y0) * QESC, _d)
    cv.save(); cv.translate(DOBRA_X0, DOBRA_Y0); cv.scale(1 / QESC, 1 / QESC)
    if a < 1:
        pt = skia.Paint(); pt.setAlphaf(clamp(a))
        cv.drawImage(img, 0, 0, LINEAR, pt)
    else:
        cv.drawImage(img, 0, 0, LINEAR)
    cv.restore()


# v4 (2ª revisão em resolução cheia): antes o cobertor era um volume azul de bolinhas encostado na cabeceira, com
# uma dobra que lia como TRAVESSEIRO, e a calça saía direto dele (~240 px contra ~370 px das pernas): PERNAS SEM
# CORPO. Agora a criança está RECOSTADA num travesseiro claro apoiado na cabeceira (a cama não comporta o corpo
# deitado reto: quadril em x~474, cabeceira em x~300), coberta até o peito: cabeça com cabelo (sem rosto — o
# estilo da série), pescoço e ombros de pijama (o mesmo amarelo de estrelinhas da calça), o volume do tronco e do
# colo sob o cobertor (dobra do avesso no peito, vincos no quadril e entre as coxas) e o bracinho POR CIMA do
# cobertor, com a mão no colo. As pernas (perna_deitada) e os tempos não mudam; a borda do cobertor continua
# cobrindo a raiz das coxas (x <= ~576).
CR_QUADRIL = (474.0, 902.0)        # quadril (onde as coxas entram sob o cobertor)
CR_OMBRO = (390.0, 732.0)          # meio dos ombros (tronco recostado ~64° no travesseiro)
CR_CABECA = (356.0, 652.0)         # centro da cabeça, apoiada no travesseiro
CR_R_CAB = 52.0
CABELO, CABELO_CL, CABELO_ESC = "#7A5236", "#9A6B48", "#4E3322"
TRAV, TRAV_CL, TRAV_ESC, TRAV_LINHA = "#E4E9F5", "#F4F6FB", "#BFCAE3", "#8A98C2"


def _corpo_cobertor():
    """Contorno do cobertor por cima do corpo recostado: a barra no peito, o tronco e o colo, a borda sobre as coxas
    (por onde as pernas saem) e a beira da cama."""
    m = skia.Path()
    m.moveTo(368, 823)                                   # barra do peito, lado das costas
    m.quadTo(420, 783, 480, 767)                         # barra do peito, lado da frente
    m.cubicTo(508, 776, 530, 794, 552, 799)              # barriga e colo (o cobertor sobe um pouco na coxa de trás)
    m.quadTo(566, 800, 578, 797)
    m.cubicTo(584, 836, 586, 896, 579, 944)              # a borda por cima das coxas
    m.quadTo(576, 972, 566, 990)
    m.lineTo(334, 991)                                   # a beira da cama (o cobertor passa um pouco da borda)
    m.cubicTo(322, 960, 320, 900, 334, 858)              # o lado do travesseiro
    m.quadTo(346, 834, 368, 823)
    m.close()
    return m


def _dobra(cv):
    # ---- travesseiro claro apoiado na cabeceira (atrás da cabeça e dos ombros)
    trav = suave([(300, 600), (360, 576), (428, 584), (452, 650), (444, 760), (430, 868), (370, 934), (306, 930),
                  (296, 800), (292, 680)])
    cv.save(); cv.translate(-4, 10); cv.drawPath(trav, paint("#0E1838", 90, blur=12)); cv.restore()
    sh = skia.GradientShader.MakeLinear([skia.Point(300, 590), skia.Point(450, 760)], [_c(TRAV_CL), _c(TRAV), _c(TRAV_ESC)])
    cv.drawPath(trav, paint(TRAV, shader=sh))
    cv.drawPath(suave([(318, 616), (372, 600), (424, 610)], fechar=False), paint(TRAV_ESC, 200, "stroke", 3))
    cv.drawPath(trav, paint(TRAV_LINHA, 230, "stroke", 2.6))
    # ---- tronco de pijama (só os ombros e o peito aparecem acima do cobertor)
    hx, hy = CR_QUADRIL; sx, sy = CR_OMBRO
    tronco = capsula(CR_QUADRIL, CR_OMBRO, 126, 116)
    cv.save(); cv.translate(-3, 8); cv.drawPath(tronco, paint("#0E1838", 70, blur=10)); cv.restore()
    pijama(cv, tronco, CR_QUADRIL, CR_OMBRO, 0.75, 1.0)
    # ---- pescoço e cabeça (cabelo em cima e atrás; o rosto, sem traços, virado para as pernas)
    cx, cy = CR_CABECA; r = CR_R_CAB
    u = unit(sx - hx, sy - hy)
    pesc0 = (sx + u[0] * 30, sy + u[1] * 30)
    pinta(cv, capsula(pesc0, (cx + 6, cy + 20), 40, 38), pesc0, (cx + 6, cy + 20), 40, TONS_PELE, 1.0,
          linha=PELE_LINHA, larg_linha=2.2)
    fr = (-u[1], u[0]) if -u[1] > 0 else (u[1], -u[0])                  # lado do peito (para a direita)
    ang_f = math.degrees(math.atan2(fr[1], fr[0]))
    gola = skia.Rect(pesc0[0] - 25, pesc0[1] - 25, pesc0[0] + 25, pesc0[1] + 25)   # a gola: só a frente do pescoço
    pt = paint(CALCA_ESC, 255, "stroke", 8); pt.setStrokeCap(skia.Paint.kRound_Cap)
    cv.drawArc(gola, ang_f - 70, 140, False, pt)
    cv.drawCircle(cx - 2, cy + 6, r + 4, paint("#0E1838", 70, blur=10))          # a cabeça afunda no travesseiro
    cabeca = circ_path(cx, cy, r)
    shc = skia.GradientShader.MakeRadial(skia.Point(cx + 22, cy + 18), r * 1.2, [_c(PELE_CL), _c(PELE), _c(PELE_ESC)],
                                         [0.0, 0.6, 1.0])
    cv.drawPath(cabeca, paint(PELE, shader=shc))
    cv.drawPath(cabeca, paint(PELE_LINHA, 200, "stroke", 2.4))
    # o cabelo cobre o alto, a nuca e a lateral; o rosto (sem traços) é só o canto de baixo-direita, virado para as
    # pernas — vista de 3/4 por trás, nada que leia como olho ou boca
    rosto = circ_path(cx + 0.66 * r, cy + 0.54 * r, 0.8 * r)
    cab0 = circ_path(cx - 4, cy - 4, r + 7)
    cabelo = skia.Op(cab0, rosto, skia.PathOp.kDifference_PathOp) or cab0
    shh = skia.GradientShader.MakeLinear([skia.Point(cx - r, cy - r), skia.Point(cx + r, cy + r)],
                                         [_c(CABELO_CL), _c(CABELO), _c(CABELO_ESC)])
    cv.drawPath(cabelo, paint(CABELO, shader=shh))
    cv.drawPath(cabelo, paint(CABELO_ESC, 230, "stroke", 2.4))
    for (a0, a1) in (((cx - 30, cy - 34), (cx + 4, cy - 52)), ((cx - 44, cy - 6), (cx - 18, cy - 38)),
                     ((cx - 34, cy + 26), (cx - 50, cy + 2))):                      # mechas
        cv.drawLine(a0[0], a0[1], a1[0], a1[1], paint(CABELO_CL, 200, "stroke", 3))
    # ---- o cobertor por cima do corpo (o volume do tronco e do colo)
    m = _corpo_cobertor()
    cv.drawPath(m, paint("#000000", 70, blur=14))
    sh = skia.GradientShader.MakeLinear([skia.Point(360, 760), skia.Point(560, 980)], [_c(COBERTOR_CL), _c(COBERTOR), _c(COBERTOR_ESC)])
    cv.drawPath(m, paint(COBERTOR, shader=sh))
    _bolinhas(cv, m, 320, 770, 600, 995, 46, 5, BOLINHA, 210)
    cv.save(); cv.clipPath(m, skia.ClipOp.kIntersect, True)
    # luz no alto do volume (peito e barriga) e sombra embaixo: o cobertor tem um corpo dentro
    cv.drawPath(suave([(392, 812), (470, 786), (548, 812)], fechar=False), paint("#FFFFFF", 70, "stroke", 26, blur=12))
    cv.drawRect(skia.Rect(320, 940, 600, 1000), paint(COBERTOR_ESC, 120, blur=14))
    # vincos: o quadril (onde o tronco dobra para o colo) e entre as coxas
    cv.drawPath(suave([(486, 806), (472, 852), (478, 904), (500, 948)], fechar=False), paint("#5E7FBA", 120, "stroke", 4, blur=2))
    cv.drawPath(suave([(512, 900), (546, 892), (578, 888)], fechar=False), paint("#5E7FBA", 110, "stroke", 3.5, blur=2))
    cv.restore()
    # a barra dobrada (o avesso do cobertor) no peito
    barra_p = skia.Path()
    barra_p.moveTo(368, 823); barra_p.quadTo(420, 783, 480, 767)
    barra_p.quadTo(486, 782, 484, 792); barra_p.quadTo(426, 806, 378, 846); barra_p.quadTo(366, 836, 368, 823)
    barra_p.close()
    cv.drawPath(barra_p, paint("#AFC5EC"))
    _bolinhas(cv, barra_p, 360, 760, 500, 850, 30, 3.5, "#CFDDF5", 220)
    cv.drawPath(barra_p, paint("#7F9BCB", 230, "stroke", 2.4))
    cv.drawPath(m, paint("#5E7FBA", 230, "stroke", 3))
    # ---- o bracinho por cima do cobertor (manga do pijama) com a mão no colo
    omb = (sx + 12, sy + 14); cot = (446, 846); pulso = (524, 846)
    braco = capsula(omb, cot, 40, 34)
    cv.save(); cv.translate(3, 7); cv.drawPath(uniao(braco, capsula(cot, pulso, 32, 28)), paint("#0E1838", 80, blur=8)); cv.restore()
    pijama(cv, braco, omb, cot, 0.5, 1.0)
    ante = capsula(cot, (pulso[0] - 6, pulso[1]), 32, 30)
    pijama(cv, ante, cot, pulso, 0.5, 1.0)
    # a mãozinha pousada no colo, relaxada: palma, dedinhos dobrados para baixo e o polegar por cima
    px_, py_ = pulso
    mao = uniao(oval_path(px_ - 6, py_ - 13, px_ + 24, py_ + 13),
                capsula((px_ + 14, py_ - 8), (px_ + 28, py_ + 4), 12, 11),
                capsula((px_ + 12, py_ + 2), (px_ + 25, py_ + 13), 12, 11),
                capsula((px_ + 2, py_ - 9), (px_ + 16, py_ - 17), 11, 10))
    cv.save(); cv.translate(2, 5); cv.drawPath(mao, paint("#0E1838", 70, blur=5)); cv.restore()
    pinta(cv, mao, (px_ + 8, py_ - 14), (px_ + 8, py_ + 14), 28, TONS_PELE, 1.0, linha=PELE_LINHA, larg_linha=2.0)
    cv.drawLine(px_ + 17, py_ - 3, px_ + 23, py_ + 2, paint(PELE_LINHA, 150, "stroke", 1.6))
    cv.drawLine(px_ - 9, py_ - 15, px_ - 9, py_ + 15, paint(CALCA_ESC, 255, "stroke", 6))                # punho
    # ---- a luz quente do abajur cai no travesseiro, na cabeça e no cobertor (vem da esquerda)
    grupo = uniao(trav, cabeca, m)
    cv.save(); cv.clipPath(grupo, skia.ClipOp.kIntersect, True)
    cv.drawCircle(ABAJUR[0], ABAJUR[1], 520, paint(LUZ, 255, shader=skia.GradientShader.MakeRadial(
        skia.Point(*ABAJUR), 520, [_c(LUZ, 90), _c(LUZ, 30), _c(LUZ, 0)], [0.0, 0.5, 1.0])))
    cv.restore()


def luzes(cv, k_abajur, k_lua):
    """Brilhos vivos por cima do cenário: o abajur respira/tremula (k_abajur) e a lua acende (k_lua)."""
    if k_abajur > 0:
        ax, ay = ABAJUR
        cv.drawCircle(ax, ay, 240, paint(LUZ, 255, shader=skia.GradientShader.MakeRadial(
            skia.Point(ax, ay), 240, [_c(LUZ, int(110 * k_abajur)), _c(LUZ, 0)])))
        pc = skia.GradientShader.MakeRadial(skia.Point(*POCA), 380, [_c(LUZ, int(70 * k_abajur)), _c(LUZ, 0)], [0.0, 1.0],
                                            skia.TileMode.kClamp, 0,
                                            skia.Matrix.Scale(1.0, 0.36).postTranslate(0, POCA[1] * 0.64))
        cv.drawRect(skia.Rect(POCA[0] - 420, POCA[1] - 160, POCA[0] + 420, POCA[1] + 160), paint(LUZ, shader=pc))
    if k_lua > 0:
        lx, ly = LUA_C
        cv.drawCircle(lx, ly, 70, paint(LUA, int(150 * k_lua), blur=22))
        lua = skia.Op(circ_path(lx, ly, 36), circ_path(lx + 17, ly - 11, 31), skia.PathOp.kDifference_PathOp)
        cv.drawPath(lua, paint("#FFFFFF", int(160 * k_lua)))


# ================================================================== AS PERNINHAS (deitadas, de pijama)
PERNA_PERTO = dict(H=(470.0, 930.0), K=(680.0, 906.0), A=(888.0, 932.0))       # esticada
PERNA_LONGE = dict(H=(482.0, 868.0), K=(686.0, 814.0), A=(896.0, 864.0))       # joelho um pouco dobrado
DIR_PE = unit(0.28, -0.96)                         # deitada de barriga para cima: os dedos apontam para o teto
L_PE = 64.0


def r_calca(u):
    return lerp(40.0, 31.0, u)


def r_canela(u):
    return lerp(28.0, 19.0, u) + 6.5 * math.sin(math.pi * clamp(u / 0.82)) ** 1.3


def eixo(P):
    K, A = P["K"], P["A"]
    d = unit(A[0] - K[0], A[1] - K[1])
    return d, (-d[1], d[0])                         # n aponta "para baixo" (para a frente da cama)


def ponto_canela(P, u, off):
    """Ponto da panturrilha em u (0 joelho, 1 tornozelo) deslocado `off` na normal (+ embaixo, - em cima)."""
    K, A = P["K"], P["A"]
    d, n = eixo(P)
    return (K[0] + (A[0] - K[0]) * u + n[0] * off, K[1] + (A[1] - K[1]) * u + n[1] * off)


def _estrela5(r, k=0.46):
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rr = r if i % 2 == 0 else r * k
        pts.append((rr * math.cos(ang), rr * math.sin(ang)))
    return poli(pts)


def pijama(cv, coxa, H, K2, e, a, escuro=0.0):
    pinta(cv, coxa, H, K2, 100 * e, tons_esc(TONS_CALCA, escuro), a, linha=CALCA_LINHA, larg_linha=2.5)
    cv.save(); cv.clipPath(coxa, skia.ClipOp.kIntersect, True)
    d = unit(K2[0] - H[0], K2[1] - H[1]); n = (-d[1], d[0]); L = math.hypot(K2[0] - H[0], K2[1] - H[1])
    for i, (u, v, r) in enumerate(((0.18, -0.45, 9), (0.42, 0.2, 8), (0.66, -0.3, 9), (0.86, 0.45, 7), (0.3, 0.7, 7),
                                   (0.55, -0.75, 7), (0.95, -0.55, 6))):
        x = H[0] + d[0] * L * u + n[0] * v * 44 * e; y = H[1] + d[1] * L * u + n[1] * v * 44 * e
        cv.save(); cv.translate(x, y); cv.rotate(i * 23); cv.scale(e, e)
        cv.drawPath(_estrela5(r), paint(esc_cor(ESTRELA_PIJ, escuro), int(230 * a)))
        cv.restore()
    cv.restore()


def meia_pe(cv, A, d, n, dpe, e, a, escuro=0.0, faixa=MEIA_FAIXA):
    """Pé de meia (deitado: dedos para cima; o calcanhar encosta na cama)."""
    calc = (A[0] - dpe[0] * 10 * e + d[0] * 10 * e, A[1] - dpe[1] * 10 * e + d[1] * 10 * e)
    ponta_ = (A[0] + dpe[0] * L_PE * e + d[0] * 8 * e, A[1] + dpe[1] * L_PE * e + d[1] * 8 * e)
    c_ini = (A[0] - d[0] * 30 * e, A[1] - d[1] * 30 * e)
    cano = tubo(c_ini, A, lambda u: lerp(21.5, 21.0, u), e)
    pe = uniao(capsula(A, ponta_, 44 * e, 37 * e), circ_path(calc[0], calc[1], 22 * e), cano)
    tons = tons_esc(TONS_MEIA, escuro)
    pinta(cv, pe, A, ponta_, 44 * e, tons, a, linha="#7D8BAA", larg_linha=2.4)
    cv.save(); cv.clipPath(pe, skia.ClipOp.kIntersect, True)
    # punho da meia (faixa) e a ponta reforçada
    c0 = (A[0] - d[0] * 20 * e, A[1] - d[1] * 20 * e)
    cv.drawLine(c0[0] - n[0] * 30 * e, c0[1] - n[1] * 30 * e, c0[0] + n[0] * 30 * e, c0[1] + n[1] * 30 * e,
                paint(esc_cor(faixa, escuro), int(255 * a), "stroke", 8 * e))
    cv.drawCircle(ponta_[0], ponta_[1], 20 * e, paint(esc_cor(faixa, escuro), int(255 * a)))
    cv.drawCircle(calc[0], calc[1], 17 * e, paint(esc_cor(faixa, escuro), int(255 * a)))
    cv.restore()
    cv.drawPath(pe, paint("#7D8BAA", int(220 * a), "stroke", 2.4))


def barra(cv, K, dk, e, a, escuro=0.0):
    """A barra da calça arregaçada logo acima do joelho: uma faixa larga, com a dobra mais clara."""
    ang = math.degrees(math.atan2(dk[1], dk[0]))
    r = (r_calca(1.0) + 4) * e
    cv.save(); cv.translate(*K); cv.rotate(ang)
    rr = skia.RRect.MakeRectXY(skia.Rect(-16 * e, -r, 12 * e, r), 9 * e, 9 * e)
    sh = skia.GradientShader.MakeLinear([skia.Point(0, -r), skia.Point(0, r)],
                                        [_c(c) for c in tons_esc((CALCA_ESC, "#F6E3A0", CALCA_CL, "#F6E3A0", CALCA_ESC), escuro)],
                                        [0.0, 0.2, 0.48, 0.8, 1.0])
    cv.drawRRect(rr, paint(CALCA, int(255 * a), shader=sh))
    cv.drawRRect(rr, paint(CALCA_LINHA, int(210 * a), "stroke", 2.4))
    cv.drawLine(-2 * e, -r + 4, -2 * e, r - 4, paint(esc_cor(CALCA_ESC, escuro), int(200 * a), "stroke", 2.6))
    cv.restore()


U_INCH = 0.16                                   # onde o joelho incha (logo abaixo da barra da calça)


def r_canela_inch(inch):
    """Raio da canela com o joelho inchado (`inch` 0..1): o contorno cresce, a pele continua cor de pele."""
    return lambda u: r_canela(u) + 21.0 * inch * math.exp(-((u - U_INCH) / 0.1) ** 2)


def perna_deitada(cv, P, a=1.0, escuro=0.0, inch=0.0):
    H, K, A = P["H"], P["K"], P["A"]
    d, n = eixo(P)
    # sombra na cama
    cv.drawPath(tubo((H[0] + 6, H[1] + 16), (A[0] + 6, A[1] + 16), lambda u: 26), paint("#0E1838", int(70 * a), blur=12))
    canela = tubo(K, A, r_canela_inch(inch) if inch > 0 else r_canela, n=28 if inch > 0 else 16)
    pinta(cv, canela, K, A, 56, tons_esc(TONS_PELE, escuro), a, linha=PELE_LINHA, larg_linha=2.4)
    meia_pe(cv, A, d, n, DIR_PE, 1.0, a, escuro)
    dk = unit(K[0] - H[0], K[1] - H[1])
    K2 = (K[0] + dk[0] * 6, K[1] + dk[1] * 6)
    coxa = tubo(H, K2, r_calca)
    pijama(cv, coxa, H, K2, 0.85, a, escuro)
    barra(cv, (K[0] - dk[0] * 4, K[1] - dk[1] * 4), dk, 1.0, a, escuro)


# ---- os risquinhos de dor (lilás, FORA da pele)
RISCOS_LONGE = ((0.08, -1), (0.42, -1), (0.86, -1))          # (u, lado): -1 = em cima da panturrilha
RISCOS_PERTO = ((0.16, 1), (0.52, 1), (0.9, 1))              # +1 = embaixo


def risco_dor(cv, x, y, ang, s, a):
    """Risquinho de dor em zigue-zague (lilás com contorno escuro): só mostra ONDE dói."""
    a = clamp(a)                                   # e_back passa de 1: alfa > 255 dava a volta (risquinho escuro)
    if a <= 0 or s <= 0:
        return
    cv.save(); cv.translate(x, y); cv.rotate(ang); cv.scale(s, s)
    p = poli([(-26, 7), (-13, -8), (0, 7), (13, -8), (26, 7)], fechar=False)
    pt = paint(CARTAO, int(170 * a), "stroke", 13); pt.setStrokeJoin(skia.Paint.kRound_Join); cv.drawPath(p, pt)
    pt = paint(DOR, int(255 * a), "stroke", 6.5); pt.setStrokeJoin(skia.Paint.kRound_Join); cv.drawPath(p, pt)
    cv.restore()


def riscos_perna(cv, P, lista, ts, a, pulso=0.0, fase=0.0, cor=None, freq=1.1):
    """Os risquinhos em volta de UMA panturrilha, pulsando devagar; `pulso` dá um pulo extra (palavra)."""
    a = clamp(a)
    if a <= 0:
        return
    d, n = eixo(P)
    ang = math.degrees(math.atan2(d[1], d[0]))
    for i, (u, lado) in enumerate(lista):
        off = (r_canela(u) + 34) * lado
        x, y = ponto_canela(P, u, off)
        s = 1.0 + 0.09 * math.sin(ts * 2 * math.pi * freq + i * 1.9 + fase) + 0.35 * pulso
        tilt = (-12 + 12 * i) * lado
        if cor is None:
            risco_dor(cv, x, y, ang + tilt, s, a)
        else:                                                         # versão do molde (contorno ciano)
            cv.save(); cv.translate(x, y); cv.rotate(ang + tilt); cv.scale(s, s)
            p = poli([(-26, 7), (-13, -8), (0, 7), (13, -8), (26, 7)], fechar=False)
            pt = paint(cor, int(255 * a), "stroke", 6); pt.setStrokeJoin(skia.Paint.kRound_Join); cv.drawPath(p, pt)
            cv.restore()


# ================================================================== MÃOS ADULTAS (manga teal), COMPRESSA, URSINHO
ESC_MAO = 0.74                                   # mão adulta do tamanho certo perto da perninha


def mao_adulta(cv, p, ang, a=1.0, lado=1, abre=0.0):
    """Mão adulta pousada vista de cima: palma em p, dedos apontando para `ang` (graus), polegar do `lado`."""
    if a <= 0:
        return
    cv.save(); cv.translate(*p); cv.rotate(ang); cv.scale(ESC_MAO, ESC_MAO * lado)
    palma = rr_path(-50, -38, 22, 38, 30)
    dedos = []
    for (v, comp) in ((-26, 50), (-9, 58), (9, 56), (26, 45)):
        q0 = (8, v); q1 = (8 + comp, v * (1 + 0.15 * abre) + 4)
        dedos.append(capsula(q0, q1, 19, 16))
    pol = capsula((-26, -30), (8, -52 - 8 * abre), 22, 18)
    forma = uniao(palma, pol, *dedos)
    cv.drawPath(forma, paint("#000000", int(70 * a), blur=8))
    pinta(cv, forma, (0, -40), (0, 40), 80, TONS_AD, a, linha=AD_LINHA, larg_linha=2.4)
    for (v, comp) in ((-26, 50), (-9, 58), (9, 56), (26, 45)):     # dobrinhas dos dedos
        cv.drawLine(16 + comp * 0.35, v - 5, 16 + comp * 0.35, v + 5, paint(AD_LINHA, int(150 * a), "stroke", 1.8))
    cv.restore()


def braco_adulto(cv, palma, ang, a=1.0, lado=1, L_ante=200.0, sobe=(130.0, -440.0), abre=0.0):
    """Braço adulto chegando de cima (o adulto sentado na beira da cama): antebraço, manga teal e a mão."""
    if a <= 0:
        return
    e = ESC_MAO
    d = (math.cos(math.radians(ang)), math.sin(math.radians(ang)))
    pulso = (palma[0] - d[0] * 44 * e, palma[1] - d[1] * 44 * e)
    cot = (palma[0] - d[0] * L_ante, palma[1] - d[1] * L_ante)
    omb = (cot[0] + sobe[0], cot[1] + sobe[1])
    pinta(cv, capsula(cot, omb, 104 * e, 116 * e), cot, omb, 110 * e, TONS_MANGA_AD, a, linha=MANGA_AD_ESC, larg_linha=3)
    ante = capsula(pulso, cot, 64 * e, 82 * e)
    pinta(cv, ante, pulso, cot, 74 * e, TONS_AD, a, linha=AD_LINHA)
    m0 = lerp2(pulso, cot, 0.45)
    mg = capsula(m0, cot, 98 * e, 104 * e)
    pinta(cv, mg, m0, cot, 100 * e, TONS_MANGA_AD, a, linha=MANGA_AD_ESC, larg_linha=3)
    n = (-d[1], d[0])
    cv.drawLine(m0[0] - n[0] * 48 * e, m0[1] - n[1] * 48 * e, m0[0] + n[0] * 48 * e, m0[1] + n[1] * 48 * e,
                paint(MANGA_AD_ESC, int(220 * a), "stroke", 4))
    mao_adulta(cv, palma, ang, a, lado, abre)


def compressa(cv, c, ang, a=1.0, halo=0.0):
    """Compressa = TOALHINHA BRANCA dobrada (MORNA) pousada POR CIMA da panturrilha (não enrola a canela): ponta
    dobrada mostrando o avesso, a espessura da dobra na borda de baixo e franjinha nas duas pontas. Sem listras,
    sem vapor. v3 (pós revisão em resolução cheia): (1) cor própria — o pano pêssego era o tom da pele e coxa, canela
    e compressa viravam um bloco bege; (2) o pano cobre só o MEIO da canela e a metade de cima dela: o contorno de
    baixo da panturrilha, o trecho do joelho e o do tornozelo continuam à vista (antes a canela de baixo sumia
    inteira); (3) sem a aba pendente, que lia como panturrilha deformada; (4) o halo morno abraça o pano (brilho no
    contorno) em vez de um disco pêssego quase opaco que lavava a perna. c = centro do pano (a ~8 px acima do eixo
    da canela); ang = o ângulo da canela."""
    if a <= 0:
        return
    cv.save(); cv.translate(*c); cv.rotate(ang)
    corpo = skia.Path()
    corpo.moveTo(-58, -28)
    corpo.quadTo(0, -35, 58, -26)                        # borda de cima, acompanhando o alto da panturrilha
    corpo.quadTo(61, -6, 58, 14)                         # ponta direita
    corpo.quadTo(0, 24, -58, 16)                         # borda de baixo, cedendo um pouco sobre a perna
    corpo.quadTo(-61, -6, -58, -28)                      # ponta esquerda
    corpo.close()
    if halo > 0:                                         # morna: aro quente colado no pano (o calor grande fica na
        cv.drawPath(corpo, paint("#FFC596", int(190 * halo * a), "stroke", 14, blur=8))     # cama: halo_compressa)
    cv.save(); cv.translate(3, 6); cv.drawPath(corpo, paint("#3A2A20", int(80 * a), blur=7)); cv.restore()
    k_m = 0.35 * clamp(halo)                             # o pano esquenta um tico de cor (continua claro, não vira pele)
    tons = [_c(lerpc(c_, COMP_MORNA, k_m)) for c_ in (COMP_CL, COMP, COMP_ESC)]
    sh = skia.GradientShader.MakeLinear([skia.Point(-40, -34), skia.Point(30, 26)], tons)
    cv.drawPath(corpo, paint(COMP, int(255 * a), shader=sh))
    cv.save(); cv.clipPath(corpo, skia.ClipOp.kIntersect, True)
    for yy in range(-26, 16, 8):                                                # felpa do tecido (pontinhos)
        for xx in range(-54 + (yy // 8 % 2) * 5, 58, 10):
            cv.drawCircle(xx, yy, 1.3, paint(COMP_FELPA, int(100 * a)))
    esp = skia.Path(); esp.moveTo(-60, 10); esp.quadTo(0, 18, 60, 8)            # a espessura da dobra (2 camadas)
    cv.drawPath(esp, paint(COMP_ESC, int(255 * a), "stroke", 9))
    cv.restore()
    cv.drawPath(corpo, paint(COMP_DOBRA, int(255 * a), "stroke", 2.6))
    cv.drawPath(esp, paint(COMP_DOBRA, int(150 * a), "stroke", 1.8))
    # ponta dobrada (o avesso) no canto de cima, à direita
    dob = poli([(58, -26), (26, -31), (56, -2)])
    cv.drawPath(poli([(26, -31), (56, -2), (44, -4), (22, -26)]), paint("#000000", int(45 * a), blur=4))
    cv.drawPath(dob, paint("#EDE6DA", int(255 * a)))
    cv.drawPath(dob, paint(COMP_DOBRA, int(255 * a), "stroke", 2.2))
    # franjinha nas duas pontas
    for y in range(-22, 14, 7):
        cv.drawLine(-59, y, -68, y + 2, paint(COMP_DOBRA, int(230 * a), "stroke", 2.2))
    for y in range(2, 14, 7):
        cv.drawLine(59, y, 68, y + 2, paint(COMP_DOBRA, int(230 * a), "stroke", 2.2))
    cv.restore()


def halo_compressa(cv, c, ang, a, halo):
    """O calor da compressa MORNA: brilho pêssego na cama em volta do pano, desenhado ANTES das pernas (v3: o disco
    quase opaco por cima lavava coxa e canela num bloco bege; aqui a perna fica nítida por cima do brilho)."""
    if a <= 0 or halo <= 0:
        return
    cv.save(); cv.translate(*c); cv.rotate(ang)
    cv.drawOval(skia.Rect(-150, -96, 150, 96), paint("#FFC99E", int(190 * halo * a), blur=34))
    cv.drawOval(skia.Rect(-100, -64, 100, 64), paint("#FFDDBF", int(170 * halo * a), blur=18))
    cv.restore()


def ursinho(cv, x, y, a=1.0, inclina=0.0):
    """Ursinho de pelúcia sentado (pista de quarto de criança), sem expressão de dor. (x, y) = base."""
    if a <= 0:
        return
    cv.save(); cv.translate(x, y); cv.rotate(inclina)
    cv.drawOval(skia.Rect(-46, -8, 46, 10), paint("#0E1838", int(80 * a), blur=8))
    corpo = oval_path(-38, -88, 38, 0)
    sh = skia.GradientShader.MakeLinear([skia.Point(-38, 0), skia.Point(38, 0)], [_c(URSO_ESC), _c(URSO), _c(URSO_ESC)])
    for (bx, by) in ((-30, -50), (30, -50)):                                     # bracinhos
        cv.drawOval(skia.Rect(bx - 15, by - 22, bx + 15, by + 22), paint(URSO_ESC, int(255 * a)))
    cv.drawPath(corpo, paint(URSO, int(255 * a), shader=sh))
    cv.drawOval(skia.Rect(-20, -62, 20, -14), paint(URSO_CL, int(255 * a)))
    for bx in (-22, 22):                                                          # perninhas
        cv.drawOval(skia.Rect(bx - 17, -22, bx + 17, 6), paint(URSO, int(255 * a)))
        cv.drawOval(skia.Rect(bx - 9, -12, bx + 9, 2), paint(URSO_CL, int(255 * a)))
    for ex in (-24, 24):                                                          # orelhas
        cv.drawCircle(ex, -136, 13, paint(URSO, int(255 * a))); cv.drawCircle(ex, -136, 6.5, paint(URSO_CL, int(255 * a)))
    cv.drawCircle(0, -112, 33, paint(URSO, int(255 * a), shader=sh))
    cv.drawOval(skia.Rect(-15, -108, 15, -86), paint(URSO_CL, int(255 * a)))
    cv.drawOval(skia.Rect(-6, -104, 6, -96), paint("#3B2A20", int(255 * a)))
    for ex in (-12, 12):
        cv.drawCircle(ex, -118, 3.6, paint("#3B2A20", int(255 * a)))
    cv.drawPath(corpo, paint(URSO_ESC, int(200 * a), "stroke", 2))
    cv.restore()


URSO_POS = (1006.0, 958.0)


# ================================================================== PICTOGRAMAS (sem letra, sem número)
def termometro(cv, x, y, esc, k_col, a):
    """Termômetro de desenho: tubo claro, bulbo e coluna lilás-clara subindo (SEM número e SEM escala)."""
    if a <= 0 or esc <= 0:
        return
    cv.save(); cv.translate(x, y); cv.scale(esc, esc)
    corpo = uniao(rr_path(-17, -92, 17, 40, 17), circ_path(0, 52, 28))
    cv.drawPath(corpo, paint("#000000", int(80 * a), blur=10))
    cv.drawPath(corpo, paint(TERMO_C, int(255 * a)))
    cv.drawPath(corpo, paint(CARTAO, int(220 * a), "stroke", 5))
    topo_col = lerp(30, -78, clamp(k_col))
    cv.drawCircle(0, 52, 19, paint(TERMO_COL, int(255 * a)))
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(-7, topo_col, 7, 50), 7, 7), paint(TERMO_COL, int(255 * a)))
    cv.drawCircle(0, 52, 19, paint("#A88BE0", int(220 * a), "stroke", 3))
    cv.drawLine(-9, -80, -9, 26, paint("#FFFFFF", int(200 * a), "stroke", 3))
    cv.restore()


def pegada(cv, x, y, ang, esc, a, cor=PEGADA, contorno=True):
    """Pegada pequena (sola + 4 dedinhos), apontando para `ang`."""
    if a <= 0:
        return
    cv.save(); cv.translate(x, y); cv.rotate(ang + 90); cv.scale(esc, esc)
    sola = skia.Path()
    sola.moveTo(0, -24); sola.cubicTo(13, -24, 15, -6, 11, 8); sola.cubicTo(8, 20, 9, 30, 0, 31)
    sola.cubicTo(-9, 30, -10, 18, -11, 6); sola.cubicTo(-14, -8, -12, -24, 0, -24); sola.close()
    if contorno:
        cv.drawPath(sola, paint(CARTAO, int(120 * a), "stroke", 5))
    cv.drawPath(sola, paint(cor, int(235 * a)))
    for (dx, dy, r) in ((-9, -33, 5.2), (-1, -37, 4.6), (6, -35, 4.0), (11, -30, 3.4)):
        if contorno:
            cv.drawCircle(dx, dy, r + 2, paint(CARTAO, int(110 * a)))
        cv.drawCircle(dx, dy, r, paint(cor, int(235 * a)))
    cv.restore()


# trilha de pegadas no chão do quarto, em direção à porta: (x, y, lado) — lado 1 = o pé que dói.
# O mancar: passo LONGO até o pé que dói, passo CURTO saindo dele (as pegadas andam em pares desiguais); a pegada
# do pé que dói é menor e mais apagada.
PEGADAS = [(430.0, 1184.0, 0), (584.0, 1158.0, 1), (644.0, 1184.0, 0), (798.0, 1158.0, 1), (858.0, 1184.0, 0),
           (1012.0, 1158.0, 1), (1072.0, 1184.0, 0)]


def trilha(cv, k, a, esc=1.25):
    """Pegadas DESIGUAIS (o mancar): aparecem uma a uma, apontando para a porta (à direita)."""
    n = len(PEGADAS)
    for i, (x, y, lado) in enumerate(PEGADAS):
        ki = clamp(k * n - i)
        if ki <= 0:
            continue
        s = esc * (0.8 if lado else 1.0) * clamp(e_back(ki), 0, 1.15)
        pegada(cv, x, y, 0.0, s, a * (0.45 if lado else 1.0) * clamp(ki * 2))


def sol_icone(cv, x, y, r, a, gira=0.0):
    if a <= 0:
        return
    cv.drawCircle(x, y, r * 1.9, paint(SOL, int(70 * a), blur=22))
    for i in range(10):
        ang = math.radians(gira + i * 36)
        cv.drawLine(x + math.cos(ang) * r * 1.25, y + math.sin(ang) * r * 1.25, x + math.cos(ang) * r * 1.62,
                    y + math.sin(ang) * r * 1.62, paint("#F2C86A", int(255 * a), "stroke", r * 0.16))
    cv.drawCircle(x, y, r, paint(SOL, int(255 * a)))
    cv.drawCircle(x, y, r, paint("#EDB94E", int(255 * a), "stroke", 3))


def placa_estetoscopio(cv, x, y, r, a):
    """Placa redonda da porta com um ESTETOSCÓPIO (pictograma, sem texto): é o médico que avalia. (A cruz verde
    da v1 lia como farmácia.)"""
    if a <= 0:
        return
    cv.drawCircle(x, y, r + 6, paint("#000000", int(80 * a), blur=8))
    cv.drawCircle(x, y, r, paint("#F7FAFD", int(255 * a)))
    cv.drawCircle(x, y, r, paint(TEAL, int(255 * a), "stroke", 5))
    cv.save(); cv.translate(x, y); cv.scale(r / 52.0, r / 52.0)
    tinta = "#34404F"
    u = skia.Path(); u.moveTo(-20, -34); u.lineTo(-20, -12); u.quadTo(-20, 10, 0, 10); u.quadTo(20, 10, 20, -12)
    u.lineTo(20, -34)
    pt = paint(tinta, int(255 * a), "stroke", 6); pt.setStrokeCap(skia.Paint.kRound_Cap); cv.drawPath(u, pt)
    tb = skia.Path(); tb.moveTo(0, 10); tb.quadTo(0, 38, 18, 36); tb.quadTo(32, 34, 30, 18)
    cv.drawPath(tb, pt)
    for ex in (-20, 20):                                           # olivas
        cv.drawCircle(ex, -36, 5.5, paint(tinta, int(255 * a)))
    cv.drawCircle(30, 12, 11, paint("#C6D3DF", int(255 * a)))       # o diafragma
    cv.drawCircle(30, 12, 11, paint(tinta, int(255 * a), "stroke", 3.5))
    cv.restore()


# ================================================================== MÃOS DADAS (o "leve para avaliar") — só mãos e mangas
def maos_dadas(cv, p, a, passo=0.0):
    """A mão adulta (manga teal, vinda de cima) segurando a mãozinha da criança. O bracinho (manga do pijama) sobe
    da borda de BAIXO: curto e fino — menor que o antebraço adulto, sem atravessar a cama. p = as mãos."""
    if a <= 0:
        return
    x, y = p
    bob = 6 * math.sin(passo * 2 * math.pi)
    m_pulso = (x - 12, y + 18 + bob * 0.5)
    m_cot = (x - 34, y + 118); m_omb = (x - 58, y + 360)            # o ombro fica FORA do quadro (embaixo)
    pijama(cv, capsula(m_cot, m_omb, 50, 56), m_cot, m_omb, 0.6, a)
    pinta(cv, capsula(m_pulso, lerp2(m_pulso, m_cot, 0.62), 27, 32), m_pulso, m_cot, 30, TONS_PELE, a, linha=PELE_LINHA)
    mg0 = lerp2(m_pulso, m_cot, 0.58)
    pijama(cv, capsula(mg0, m_cot, 46, 50), mg0, m_cot, 0.6, a)
    cv.drawCircle(x - 4, y + 10 + bob * 0.5, 19, paint(PELE, int(255 * a)))
    cv.drawCircle(x - 4, y + 10 + bob * 0.5, 19, paint(PELE_LINHA, int(200 * a), "stroke", 2.2))
    # braço adulto (de cima): antebraço quase vertical
    e = 0.72                                                         # mais fino: não domina o quadro
    a_pulso = (x - 6, y - 36 + bob); a_cot = (x - 30, y - 270); a_omb = (x - 44, y - 720)
    pinta(cv, capsula(a_cot, a_omb, 104 * e, 116 * e), a_cot, a_omb, 110 * e, TONS_MANGA_AD, a, linha=MANGA_AD_ESC, larg_linha=3)
    pinta(cv, capsula(a_pulso, a_cot, 64 * e, 82 * e), a_pulso, a_cot, 74 * e, TONS_AD, a, linha=AD_LINHA)
    mg = lerp2(a_pulso, a_cot, 0.5)
    pinta(cv, capsula(mg, a_cot, 98 * e, 104 * e), mg, a_cot, 100 * e, TONS_MANGA_AD, a, linha=MANGA_AD_ESC, larg_linha=3)
    # a mão adulta fechada em volta da mãozinha (dedos por cima)
    cv.save(); cv.translate(x, y + bob); cv.scale(e, e)
    palma = rr_path(-40, -46, 30, 16, 26)
    dedos = [capsula((18, -34 + i * 15), (34, -20 + i * 15), 18, 16) for i in range(4)]
    pol = capsula((-30, -6), (-2, 22), 22, 18)
    forma = uniao(palma, pol, *dedos)
    cv.drawPath(forma, paint("#000000", int(60 * a), blur=6))
    pinta(cv, forma, (-40, 0), (34, 0), 76, TONS_AD, a, linha=AD_LINHA, larg_linha=2.4)
    cv.restore()


# ================================================================== A MANHÃ (metade direita do LANCE 2)
MX_LARG = 512.0                                   # largura da metade (coordenadas locais da metade: 0..512 x 0..926)
M_ALT = JY1 - JY0


def manha_fundo(cv):
    def _d(c):
        c.scale(QESC, QESC); _manha(c)
    img = cacheado("manha", MX_LARG * QESC, M_ALT * QESC, _d)
    cv.save(); cv.scale(1 / QESC, 1 / QESC); cv.drawImage(img, 0, 0, LINEAR); cv.restore()


def _manha(cv):
    sh = skia.GradientShader.MakeLinear([skia.Point(0, 0), skia.Point(0, 760)], [_c(PAREDE_M1), _c(PAREDE_M2)])
    cv.drawRect(skia.Rect(0, 0, MX_LARG, 760), paint(PAREDE_M1, shader=sh))
    rng = np.random.default_rng(5)
    for gy in range(30, 740, 92):
        for gx in range(-20, 540, 104):
            _estrela4(cv, gx + (52 if (gy // 92) % 2 else 0) + rng.uniform(-8, 8), gy + rng.uniform(-8, 8), 7, "#C3D3EA", 200)
    # janela de dia (o sol é desenhado vivo, por cima: ele desce quando a metade fecha)
    x0, y0, x1, y1 = 300, 40, 486, 236
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(x0 - 14, y0 - 14, x1 + 14, y1 + 14), 8, 8), paint("#FFFFFF"))
    ceu = skia.GradientShader.MakeLinear([skia.Point(0, y0), skia.Point(0, y1)], [_c("#9ED5F5"), _c("#DDF1FC")])
    cv.drawRect(skia.Rect(x0, y0, x1, y1), paint("#BFE3F7", shader=ceu))
    cv.drawRect(skia.Rect(x0 - 24, y1 + 12, x1 + 24, y1 + 26), paint("#F4F7FB"))
    # rodapé e chão claro
    cv.drawRect(skia.Rect(0, 742, MX_LARG, 760), paint("#F4F7FB"))
    sh = skia.GradientShader.MakeLinear([skia.Point(0, 760), skia.Point(0, M_ALT)], [_c("#EBD4B0"), _c(PISO_M), _c(PISO_M_ESC)])
    cv.drawRect(skia.Rect(0, 760, MX_LARG, M_ALT), paint(PISO_M, shader=sh))
    y = 760.0; dy = 24.0
    while y < M_ALT:
        y += dy; dy *= 1.25
        cv.drawLine(0, y, MX_LARG, y, paint("#D2B48A", 200, "stroke", 3))
    # a beira da cama (de onde a criança pulou), mesmo cobertor
    cv.drawRect(skia.Rect(16, 700, 40, 772), paint(MADEIRA_ESC))
    cv.drawOval(skia.Rect(-60, 752, 200, 790), paint("#000000", 40, blur=14))
    topo = rr_path(-40, 520, 168, 600, 22)
    cv.drawPath(topo, paint("#9DC0F0"))
    _bolinhas(cv, topo, -30, 536, 170, 600, 46, 5, "#CFE0F8", 220)
    frente = rr_path(-40, 586, 172, 706, 10)
    cv.drawPath(frente, paint("#8AAEE6"))
    _bolinhas(cv, frente, -20, 606, 172, 706, 46, 5, "#C3D7F6", 220)
    cv.drawLine(-40, 590, 168, 590, paint("#6F92CC", 200, "stroke", 4))
    # luz do dia entrando
    cv.drawCircle(400, 140, 420, paint("#FFF6D6", 255, shader=skia.GradientShader.MakeRadial(
        skia.Point(400, 140), 420, [_c("#FFF6D6", 110), _c("#FFF6D6", 0)])))


def tenis(cv, A, dpe, e, a):
    """Tênis infantil (branco com faixa azul, solado cinza-claro) no pé de uma perna em pé."""
    ang = math.degrees(math.atan2(dpe[1], dpe[0]))
    cv.save(); cv.translate(*A); cv.rotate(ang); cv.scale(e, e)
    sola = rr_path(-46, 30, 128, 52, 18)
    cabedal = skia.Path()
    cabedal.moveTo(-44, 34); cabedal.lineTo(-40, -38); cabedal.quadTo(-30, -52, -6, -48)
    cabedal.lineTo(30, -36); cabedal.quadTo(70, -24, 108, -4); cabedal.quadTo(132, 8, 128, 34); cabedal.close()
    cv.drawPath(uniao(sola, cabedal), paint("#000000", int(70 * a), blur=8))
    cv.drawPath(sola, paint(TENIS_SOLA, int(255 * a)))
    cv.drawPath(sola, paint("#8E9AAB", int(230 * a), "stroke", 2.4))
    sh = skia.GradientShader.MakeLinear([skia.Point(0, -48), skia.Point(0, 34)], [_c("#FFFFFF"), _c(TENIS), _c("#DCE3EE")])
    cv.drawPath(cabedal, paint(TENIS, int(255 * a), shader=sh))
    cv.save(); cv.clipPath(cabedal, skia.ClipOp.kIntersect, True)
    for k in range(2):
        cv.drawLine(-10 + 26 * k, 30, 30 + 26 * k, -30, paint(TENIS_FAIXA, int(255 * a), "stroke", 9))
    cv.restore()
    cv.drawPath(cabedal, paint("#8E9AAB", int(230 * a), "stroke", 2.4))
    for k in range(3):
        cv.drawLine(44 + k * 16, -28 + k * 6, 54 + k * 16, -14 + k * 6, paint("#9AA6B6", int(230 * a), "stroke", 3))
    cv.restore()


def perna_em_pe(cv, H, K, A, dpe, e, a):
    d, n = unit(A[0] - K[0], A[1] - K[1]), None
    canela = tubo(K, A, r_canela, e)
    pinta(cv, canela, K, A, 70 * e, TONS_PELE, a, linha=PELE_LINHA, larg_linha=2.6)
    meia = tubo((A[0] - d[0] * 40 * e, A[1] - d[1] * 40 * e), A, lambda u: 26.0, e)
    pinta(cv, meia, (A[0] - d[0] * 40 * e, A[1] - d[1] * 40 * e), A, 54 * e, TONS_MEIA, a, linha="#8E9CBA")
    tenis(cv, (A[0] + d[0] * 6 * e, A[1] + d[1] * 6 * e), dpe, E_TENIS, a)
    dk = unit(K[0] - H[0], K[1] - H[1])
    K2 = (K[0] + dk[0] * 6 * e, K[1] + dk[1] * 6 * e)
    coxa = tubo(H, K2, r_calca, e)
    pijama(cv, coxa, H, K2, e * 0.85, a)
    barra(cv, (K[0] - dk[0] * 4 * e, K[1] - dk[1] * 4 * e), dk, e, a)


def bola(cv, x, y, r, gira, a=1.0):
    cv.drawOval(skia.Rect(x - r * 0.95, y + r * 0.82, x + r * 0.95, y + r * 1.12), paint("#000000", int(60 * a), blur=8))
    cv.save(); cv.translate(x, y); cv.rotate(gira)
    cv.drawCircle(0, 0, r, paint("#FFFFFF", int(255 * a)))
    cores = ("#3D7BD9", "#FFFFFF", "#F2C14E", "#FFFFFF", "#F08BB0", "#FFFFFF")
    for i, c in enumerate(cores):
        p = skia.Path(); p.moveTo(0, 0); p.arcTo(skia.Rect(-r, -r, r, r), i * 60, 60, False); p.close()
        cv.drawPath(p, paint(c, int(255 * a)))
    cv.drawCircle(0, 0, r * 0.18, paint("#FFFFFF", int(255 * a)))
    cv.drawCircle(0, 0, r, paint("#8E9AAB", int(255 * a), "stroke", 3))
    cv.restore()
    cv.drawCircle(x - r * 0.35, y - r * 0.4, r * 0.22, paint("#FFFFFF", int(120 * a), blur=4))


# a criança brincando atrás da bola: só as pernas (o quadril fica acima da metade)
M_E = 1.3
# v4 (2ª revisão em resolução cheia): os DOIS tênis de perfil para a DIREITA (para a bola) e APOIADOS no chão.
# Antes o tênis da perna de trás apontava para baixo-esquerda (~45°, solado para fora) enquanto o da frente
# apontava para a direita: o pé de trás lia como TORCIDO no tornozelo; e os dois tênis paravam em y local ~715-730,
# acima do rodapé (742-760) — pés flutuando. Agora cada pé é posto pela ponta do solado num ponto do CHÃO (piso
# começa em y local 760): passada parada em V invertido (a perna de trás inclinada para trás, a da frente sob o
# quadril; joelhos SEPARADOS e um tico para a frente — nunca joelhos juntos com pés afastados, que leria "pernas
# em X"). O "pular" vira quique no lugar: o quadril sobe e desce, os joelhos dobram e esticam, e o calcanhar de
# trás sobe um pouco (impulso, a ponta continua no chão) — nenhum pé sai do chão. O tênis de trás continua longe
# da divisória (x local >= ~60, medido em toda a passada; a correção da v3 fica). A bola fica no chão logo à frente
# da ponta do tênis da frente (antes ela ficava embaixo do pé, mais perto de quem vê).
E_TENIS = M_E * 0.82                            # escala do tênis (cabe a passada inteira na metade de 512 px)
TOE_SOLA = (110.0, 52.0)                        # ponto do solado embaixo da ponta, em coordenadas do tênis
CHAO_TRAS, CHAO_FRENTE = 798.0, 812.0           # onde cada solado encosta no chão (o da frente, mais perto)
PONTA_TRAS_X, PONTA_FRENTE_X = 232.0, 386.0     # x da ponta de cada tênis no chão


def _pe_no_chao(H, ponta_x, chao_y, alfa, fwd):
    """Joelho, tornozelo e direção do pé para um tênis cuja PONTA do solado fica em (ponta_x, chao_y); `alfa`
    (graus) gira o tênis em volta dessa ponta (calcanhar sobe, ponta para baixo-DIREITA); `fwd` = quanto o joelho
    sai da reta quadril-tornozelo para a FRENTE (direita). Devolve (K, A, dpe)."""
    r = math.radians(alfa)
    dpe = (math.cos(r), math.sin(r))
    tx, ty = TOE_SOLA[0] * E_TENIS, TOE_SOLA[1] * E_TENIS
    A2 = (ponta_x - (tx * dpe[0] - ty * dpe[1]), chao_y - (tx * dpe[1] + ty * dpe[0]))
    A = (A2[0], A2[1] - 6 * M_E)
    for _ in range(3):                           # perna_em_pe põe o tênis em A + d*6*e (d = direção da canela)
        K = (lerp(H[0], A[0], 0.54) + fwd, lerp(H[1], A[1], 0.54))
        d = unit(A[0] - K[0], A[1] - K[1])
        A = (A2[0] - d[0] * 6 * M_E, A2[1] - d[1] * 6 * M_E)
    K = (lerp(H[0], A[0], 0.54) + fwd, lerp(H[1], A[1], 0.54))
    return K, A, dpe


def pose_manha(ts):
    pulo = abs(math.sin(ts * 2 * math.pi * 0.9))
    sobe = -14 * pulo                            # o quadril quica (o pé fica no chão)
    flex = 1 - pulo                              # embaixo do quique o joelho dobra mais
    bal = math.sin(ts * 2 * math.pi * 0.45)
    Hf = (262.0 + 3 * bal, 34.0 + sobe)
    Kf, Af, df = _pe_no_chao(Hf, PONTA_FRENTE_X, CHAO_FRENTE, 0.0, 10.0 + 14.0 * flex)
    Hb = (210.0 + 3 * bal, 34.0 + sobe)
    Kb, Ab, db = _pe_no_chao(Hb, PONTA_TRAS_X, CHAO_TRAS, 14.0 * pulo, 6.0 + 8.0 * flex)  # impulso: calcanhar sobe
    return (Hb, Kb, Ab, db), (Hf, Kf, Af, df), pulo


def cena_manha(cv, ts, t_sol=0.0):
    """A metade MANHÃ, em coordenadas locais (0..512 x 0..926). t_sol: o sol desce (0 = no alto)."""
    manha_fundo(cv)
    cv.save(); cv.clipRect(skia.Rect(300, 40, 486, 236), True)
    sol_icone(cv, 420, lerp(118, 330, e_inout(t_sol)), 40, 1.0, ts * 20)
    cv.restore()
    (Hb, Kb, Ab, db), (Hf, Kf, Af, df), pulo = pose_manha(ts)
    # sombra dos pés no chão, embaixo dos solados (v4: os pés agora pisam nela)
    cv.drawOval(skia.Rect(48, 790, 432, 832), paint("#000000", int(58 * (1 - 0.25 * pulo)), blur=12))
    perna_em_pe(cv, Hb, Kb, Ab, db, M_E, 1.0)
    perna_em_pe(cv, Hf, Kf, Af, df, M_E, 1.0)
    # a bola no chão logo à frente da ponta do tênis (mais perto de quem vê: desenhada depois das pernas)
    bx = 454 + 3 * math.sin(ts * 1.4)
    bola(cv, bx, 800, 40, ts * 60)


def manha_canela(ts):
    """Ponto da panturrilha da frente (local), para a linha tracejada."""
    _, (Hf, Kf, Af, _), _ = pose_manha(ts)
    return lerp2(Kf, Af, 0.4)


# ================================================================== A PROFISSIONAL DE SAÚDE + APITO (fecho)
PELE_AD5 = ("#B98163", "#D9A07F", "#E8B998", "#D9A07F", "#B98163"); LINHA_AD5 = "#9A6648"


def profissional(cv, x, y, esc, a, mao_k=1.0, braco=True):
    """Profissional de saúde de frente, sem rosto: jaleco branco, gola em V, estetoscópio e (braco=True) a mão
    erguida. Cópia do fecho do cf_var_primeiros_socorros; aqui o fecho usa braco=False (sem apito na mão)."""
    if a <= 0:
        return None
    cv.save(); cv.translate(x, y); cv.scale(esc, esc)
    om = (70, -6); cot = (128, -40); mao_p = (124, lerp(-60, -132, mao_k))
    jal = ("#C9D3DE", "#EEF2F6", "#FFFFFF", "#EEF2F6", "#C9D3DE")
    if braco:
        pinta(cv, capsula(om, cot, 46, 40), om, cot, 46, jal, a, linha="#9AA8B6")
        pinta(cv, capsula(cot, mao_p, 40, 36), cot, mao_p, 40, jal, a, linha="#9AA8B6")
        mp = capsula((mao_p[0], mao_p[1] + 4), (mao_p[0] + 2, mao_p[1] - 26), 34, 30)
        pinta(cv, mp, (mao_p[0], mao_p[1] + 4), (mao_p[0], mao_p[1] - 26), 34, PELE_AD5, a, linha=LINHA_AD5)
    om_p = skia.Path(); om_p.addRRect(skia.RRect.MakeRectXY(skia.Rect(-96, -20, 96, 140), 70, 70))
    clip = skia.Path(); clip.addRect(skia.Rect(-110, -30, 110, 110))
    om_p = skia.Op(om_p, clip, skia.PathOp.kIntersect_PathOp)
    cv.drawPath(om_p, paint("#000000", int(80 * a), blur=10))
    shj = skia.GradientShader.MakeLinear([skia.Point(-96, 0), skia.Point(96, 0)], [_c("#D5DDE6"), _c("#FFFFFF"), _c("#D5DDE6")])
    cv.drawPath(om_p, paint("#F4F7FA", int(255 * a), shader=shj))
    cv.drawPath(om_p, paint("#9AA8B6", int(220 * a), "stroke", 3))
    cv.drawPath(poli([(-30, -16), (30, -16), (0, 46)]), paint(TEAL, int(255 * a)))
    cv.drawPath(poli([(-34, -18), (-6, 60), (-22, 108)], fechar=False), paint("#B9C6D3", int(255 * a), "stroke", 4))
    cv.drawPath(poli([(34, -18), (6, 60), (22, 108)], fechar=False), paint("#B9C6D3", int(255 * a), "stroke", 4))
    est = suave([(-30, -18), (-44, 30), (-30, 66), (0, 76), (14, 70)], fechar=False)
    cv.drawPath(est, paint("#5B6676", int(255 * a), "stroke", 6))
    cv.drawPath(suave([(30, -18), (40, 20), (34, 50)], fechar=False), paint("#5B6676", int(255 * a), "stroke", 6))
    cv.drawCircle(16, 74, 11, paint("#C6D3DF", int(255 * a))); cv.drawCircle(16, 74, 11, paint("#5B6676", int(255 * a), "stroke", 3))
    cv.drawCircle(0, -58, 40, paint("#000000", int(80 * a), blur=6))
    sh_c = skia.GradientShader.MakeRadial(skia.Point(-10, -70), 56, [_c(PELE_AD5[2]), _c(PELE_AD5[1]), _c(PELE_AD5[0])], [0, 0.55, 1])
    cv.drawCircle(0, -58, 40, paint(PELE_AD5[1], int(255 * a), shader=sh_c))
    cv.drawArc(skia.Rect(-42, -100, 42, -16), 190, 160, False, paint("#3A2A20", int(255 * a), "stroke", 16))
    cv.drawCircle(0, -104, 16, paint("#3A2A20", int(255 * a)))
    cv.restore()
    return (x + mao_p[0] * esc, y + (mao_p[1] - 22) * esc)


# ================================================================== ESTADOS (tempo -> o que a cena mostra)
# poses das mãos adultas: (palma, ângulo dos dedos)
CALF_E, CALF_D = ((726.0, 880.0), 102.0), ((842.0, 900.0), 132.0)      # pousadas na panturrilha (a massagem)
JOELHO_E = ((636.0, 872.0), 98.0)                                      # a esquerda abre espaço: PARADA no joelho
COMP_SEGURA = ((838.0, 884.0), 150.0)                                  # a direita trazendo a compressa
LEITO_E = ((600.0, 766.0), 104.0)                                      # a mão apoiada na cama (noite do LANCE 2)
COMP_CALF = ((772.0, 909.0), 7.0)          # a compressa POR CIMA da panturrilha (meio da canela, u ~0,16..0,72)
FORA = (300.0, -560.0)                                                 # para onde as mãos saem (cima, direita)
RISCOS_L3 = ((0.48, 1), (0.7, 1), (0.92, 1))                           # LANCE 3: só embaixo da perna que dói


def _mix_pose(p, q, k):
    return (lerp2(p[0], q[0], k), lerp(p[1], q[1], k))


def _fora(pose, k):
    (x, y), ang = pose
    return ((x + FORA[0] * k, y + FORA[1] * k), ang)


def ts_l1(t, T):
    if t < T["var"] or T["pode1"] <= t < T["validado"]:
        return T["pode1"]
    if t >= T["crianca"]:                       # 'sente a sua calma': o pulso dos risquinhos desacelera (não somem)
        return T["crianca"] + (t - T["crianca"]) * 0.45
    return t


def estado_l1(t, T):
    """Lance 1. Quadro 0 = as duas mãos JÁ na panturrilha (a massagem congelada), sem compressa."""
    e = {"ts": ts_l1(t, T)}
    V = T["var"]
    # --- mão esquerda
    if t < V:
        pe = CALF_E; ae = 1.0
    elif t < T["massagem1"] - 0.2:
        pe = _fora(CALF_E, e_inout(prog(t, V, V + 0.5))); ae = 1.0 - prog(t, V + 0.4, V + 0.5)
    else:
        k_in = e_out(prog(t, T["massagem1"] - 0.2, T["massagem1"] + 0.3))
        pe = _fora(CALF_E, 1 - k_in); ae = clamp(k_in * 4)
        pe = _mix_pose(pe, JOELHO_E, e_inout(prog(t, T["compressa"] - 0.3, T["compressa"] + 0.15)))
    # --- mão direita
    if t < V:
        pd = CALF_D; ad = 1.0
    elif t < T["massagem1"] - 0.2:
        pd = _fora(CALF_D, e_inout(prog(t, V, V + 0.5))); ad = 1.0 - prog(t, V + 0.4, V + 0.5)
    else:
        k_in = e_out(prog(t, T["massagem1"] - 0.14, T["massagem1"] + 0.36))
        pd = _fora(CALF_D, 1 - k_in); ad = clamp(k_in * 4)
        # vai buscar a compressa (sai rápido), volta com ela, pousa e SAI (a compressa fica à vista)
        t_s0 = T["massagem2"] + 0.24; t_s1 = T["compressa"] - 0.04; t_v1 = T["compressa"] + 0.3
        k_sai = e_inout(prog(t, t_s0, t_s1)) * (1 - e_out(prog(t, t_s1, t_v1)))
        if t >= t_s1:
            pd = COMP_SEGURA
            k_sai = max(k_sai, e_inout(prog(t, t_v1 + 0.1, t_v1 + 0.55)))
            ad = ad * (1 - prog(t, t_v1 + 0.45, t_v1 + 0.55))
        pd = _fora(pd, k_sai)
    # massagem: círculos lentos das duas mãos (do 2º "massagem" até a compressa)
    k_m = janela(t, T["massagem2"] - 0.05, T["compressa"] - 0.1, 0.15, 0.2)
    if k_m > 0:
        ph = (t - T["massagem2"]) * 2 * math.pi * 1.25
        pe = ((pe[0][0] + 11 * k_m * math.cos(ph), pe[0][1] + 6 * k_m * math.sin(ph)), pe[1])
        k_m2 = k_m * (1 - prog(t, T["massagem2"] + 0.18, T["massagem2"] + 0.3))
        pd = ((pd[0][0] + 11 * k_m2 * math.cos(ph + 2.1), pd[0][1] + 6 * k_m2 * math.sin(ph + 2.1)), pd[1])
    e["mao_e"], e["a_e"] = pe, ae
    e["mao_d"], e["a_d"] = pd, ad
    # --- compressa: só a partir de "compressa"
    if t >= T["compressa"] - 0.04:
        k_v = e_out(prog(t, T["compressa"] - 0.04, T["compressa"] + 0.3))
        dest = COMP_CALF[0]
        orig = (dest[0] + FORA[0], dest[1] + FORA[1])
        e["comp"] = (lerp2(orig, dest, k_v), COMP_CALF[1], 1.0)
    else:
        e["comp"] = None
    e["halo"] = prog(t, T["morna"] - 0.05, T["morna"] + 0.3)
    e["urso"] = URSO_POS
    e["urso_inc"] = 0.0
    # --- risquinhos: pulsam em "Dor"
    e["pulso_dor"] = max(0.0, 1 - abs(t - T["dor1"] - 0.12) / 0.22)
    # --- luzes: lua em "noite"; abajur tremula em "noite"; em "calma" a poça de luz quente nas pernas respira
    e["lua"] = janela(t, T["noite1"] - 0.05, T["noite1"] + 0.6, 0.12, 0.4)
    trem = janela(t, T["noite1"], T["noite1"] + 0.5, 0.05, 0.1) * (0.5 + 0.5 * math.sin(t * 47))
    resp = math.sin(math.pi * prog(t, T["calma"] - 0.1, T["calma"] + 1.0))
    e["abajur"] = 0.35 * trem + 1.25 * resp
    return e


def estado_noite_l2(t, T):
    """A metade NOITE do lance 2: as perninhas com dor; em 'dor' a mão adulta pousa ao lado."""
    ts = t
    if T["pode2"] <= t < T["anulado1"]:
        ts = T["pode2"]
    k = e_out(prog(t, T["dor2"] - 0.1, T["dor2"] + 0.4))
    return {"ts": ts, "mao_e": _fora(LEITO_E, 1 - k), "a_e": clamp(k * 4), "mao_d": None, "a_d": 0.0, "comp": None,
            "halo": 0.0, "urso": URSO_POS, "urso_inc": 0.0,
            "pulso_dor": max(0.0, 1 - abs(t - T["dor2"] - 0.15) / 0.25) + max(0.0, 1 - abs(t - T["real"] - 0.1) / 0.25),
            "lua": max(0.0, 1 - abs(t - T["some"]) / 0.35), "abajur": 0.0}


def ts_l3(t, T):
    if T["pode3"] <= t < T["anulado2"]:
        return T["pode3"]
    return t


# ================================================================== câmeras
CAM_Q0 = (1.3, 786.0, 870.0)           # quadro 0: as mãos massageando as duas panturrilhas
CAM_JOGO = (1.06, 720.0, 845.0)
CAM_PERTO1 = (1.22, 786.0, 868.0)      # congela: mãos + panturrilhas
CAM_FICA = (0.95, 660.0, 830.0)        # "Fica perto": a câmera abre (o abajur entra inteiro)
CAM_MEIA = (0.8, 700.0, 830.0, JCX - 256.0)     # metade NOITE do lance 2
CAM_L3 = (0.95, 760.0, 900.0)          # a divisória do lance 2 fecha aqui
CAM_Z3 = (1.4, 720.0, 930.0)           # LANCE 3: perto da perna que dói (pernas em ~60% da largura)
CAM_R3 = (1.0, 800.0, 935.0, JCX + 256.0)       # LANCE 3 dividido: a perna que dói (direita)
CAM_MINI = (0.8, 700.0, 845.0, JCX - 256.0)     # LANCE 3 dividido: o padrão do LANCE 1 (esquerda)
CAM_PORTA = (1.45, 1090.0, 900.0)      # "Leve para avaliar": a porta, as pegadas, as mãos dadas


def cam_l1(t, T):
    V = T["var"]
    if t < V:
        return CAM_Q0
    cam = lerp3(CAM_Q0, CAM_JOGO, e_inout(prog(t, V, V + 0.5)))
    cam = lerp3(cam, CAM_PERTO1, e_inout(prog(t, T["pode1"], T["pode1"] + 0.3)))
    cheg = prog(t, T["pode1_fim"], T["validado"])
    cam = (cam[0] * (1 + 0.05 * e_inout(cheg)),) + tuple(cam[1:])
    cam = lerp3(cam, CAM_JOGO, e_inout(prog(t, T["validado"] + 0.1, T["validado"] + 0.6)))
    return lerp3(cam, CAM_FICA, e_inout(prog(t, T["fica"] - 0.05, T["fica"] + 0.7)))


def cam_l3(t, T):
    return lerp3(CAM_L3, CAM_Z3, e_inout(prog(t, T["dor3"] - 0.15, T["dor3"] + 0.4)))


# ================================================================== cenas
def cena_noite(cv, cam, e, lance3=None):
    """O quarto à noite com as perninhas. `lance3`: dict do lance 3 (dor de um lado só e os sinais)."""
    cv.save(); aplica(cv, cam)
    quarto(cv)
    luzes(cv, e.get("abajur", 0.0), e.get("lua", 0.0))
    if lance3 is not None and lance3.get("trilha_k", 0) > 0:
        trilha(cv, lance3["trilha_k"], 1.0)                 # o mancar: pegadas no chão, rumo à porta
    ux, uy = e["urso"]
    ursinho(cv, ux, uy, 1.0, e.get("urso_inc", 0.0))
    ts = e["ts"]
    esm = lance3.get("esmaece", 0.0) if lance3 is not None else 0.0
    if lance3 is None and e.get("comp") is not None:      # o calor da compressa morna fica ATRÁS das pernas (v3)
        halo_compressa(cv, e["comp"][0], e["comp"][1], e["comp"][2], e.get("halo", 0.0))
    if esm > 0:                                  # "lado": a perna sem dor fica translúcida (a pele não muda de cor)
        cv.saveLayerAlpha(None, int(255 * (1 - 0.62 * esm)))
    perna_deitada(cv, PERNA_LONGE, 1.0, escuro=0.06)
    if esm > 0:
        cv.restore()
    perna_deitada(cv, PERNA_PERTO, 1.0, inch=lance3.get("inch", 0.0) if lance3 is not None else 0.0)
    dobra(cv)
    pul = e.get("pulso_dor", 0.0)
    if lance3 is None:
        riscos_perna(cv, PERNA_LONGE, RISCOS_LONGE, ts, 1.0, pul, 0.0)
        riscos_perna(cv, PERNA_PERTO, RISCOS_PERTO, ts, 1.0, pul, 1.3)
    else:
        L = lance3
        riscos_perna(cv, PERNA_PERTO, RISCOS_L3, ts, L["a_riscos"], L.get("pulso", 0.0), 1.3)
        termometro(cv, 1010.0, 700.0, 0.9 * clamp(L["termo_k"], 0, 1.2), L["termo_col"], clamp(L["termo_k"] * 3))
        cv.restore()
        return
    if e.get("comp") is not None:
        c, ang, ac = e["comp"]
        compressa(cv, c, ang, ac, e.get("halo", 0.0))
    # as mãos adultas (a de trás primeiro)
    if e.get("mao_d") is not None and e.get("a_d", 0) > 0:
        (p, ang) = e["mao_d"]
        braco_adulto(cv, p, ang, e["a_d"], lado=-1, sobe=(190.0, -430.0))
    if e.get("mao_e") is not None and e.get("a_e", 0) > 0:
        (p, ang) = e["mao_e"]
        braco_adulto(cv, p, ang, e["a_e"], lado=1, sobe=(150.0, -440.0))
    cv.restore()


def estado_l3(t, T):
    L = {}
    L["a_riscos"] = clamp(e_back(prog(t, T["dor3"] - 0.05, T["dor3"] + 0.3)))
    L["pulso"] = max(0.0, 1 - abs(t - T["dor3"] - 0.15) / 0.25)
    L["esmaece"] = prog(t, T["lado"] - 0.05, T["lado"] + 0.25)
    L["inch"] = e_out(prog(t, T["inchaco"] - 0.05, T["inchaco"] + 0.4))
    L["termo_k"] = e_back(prog(t, T["febre1"] - 0.06, T["febre1"] + 0.24))
    L["termo_col"] = e_out(prog(t, T["febre1"] + 0.05, T["febre1"] + 0.6))
    L["trilha_k"] = prog(t, T["manqueira1"] - 0.04, T["manqueira1"] + 0.75)
    return L


def cena_porta(cv, t, T, cam):
    """'Leve para avaliar': as mãos dadas seguem as pegadas até a porta (a criança já levantou)."""
    cv.save(); aplica(cv, cam)
    quarto(cv)
    luzes(cv, 0.4, 0.0)
    trilha(cv, 1.0, 1.0)
    ursinho(cv, URSO_POS[0], URSO_POS[1], 1.0)
    k = e_inout(prog(t, T["leve"] - 0.05, T["leve"] + 0.85))
    p = (lerp(850, 1076, k), lerp(1074, 1068, k))
    maos_dadas(cv, p, prog(t, T["leve"] - 0.08, T["leve"] + 0.08), passo=(t - T["leve"]) * 1.6 * (1 - prog(k, 0.9, 1.0)))
    cv.restore()


def cena(cv, t, T):
    """O lance da vez (com as telas divididas do lance 2 e do lance 3). Devolve o que o HUD precisa."""
    info = {}
    t_div0 = T["e2"] - 0.05
    t_div1 = T["noite3"]
    t_div3 = T["chamar2"] - 0.05
    abre = e_inout(prog(t, t_div0, t_div0 + 0.32))
    fecha = e_inout(prog(t, t_div1, t_div1 + 0.3))
    if t < t_div0:
        e = estado_l1(t, T)
        cam = cam_l1(t, T)
        cena_noite(cv, cam, e)
        info.update(lance=1, cam=cam, e=e)
    elif t < t_div1 + 0.3:
        # LANCE 2 (e as transições de abrir e fechar a divisória)
        xd = lerp(JX1 + 4, DIV_X, abre) if t < t_div1 else lerp(DIV_X, JX1 + 4, fecha)
        if t < t_div1:
            cam_n = lerp3(cam4(CAM_FICA), CAM_MEIA, abre)
            en = estado_noite_l2(t, T) if t >= T["e2"] else estado_l1(t, T)
            if t < T["e2"]:
                en = dict(en, comp=None, mao_d=None)
        else:
            cam_n = lerp3(CAM_MEIA, cam4(CAM_L3), fecha)
            en = estado_noite_l2(t, T)
        cv.save(); cv.clipRect(skia.Rect(0, 0, xd, H), True)
        if t < t_div1:
            cena_noite(cv, cam_n, en)
        else:                                                # fechando: já é a noite do lance 3
            cena_noite(cv, cam_n, dict(en, mao_e=None, a_e=0.0), lance3=estado_l3(t, T))
        cv.restore()
        if xd < JX1:
            ts_m = t
            if T["pode2"] <= t < T["anulado1"]:
                ts_m = T["pode2"]
            cv.save(); cv.clipRect(skia.Rect(xd, 0, W, H), True)
            cv.translate(xd, JY0)
            cena_manha(cv, ts_m, fecha)
            cv.restore()
            cv.drawLine(xd, JY0, xd, JY1, paint(CIANO, 150, "stroke", 22, blur=9))
            cv.drawLine(xd, JY0, xd, JY1, paint("#FFFFFF", 255, "stroke", 6))
        info.update(lance=2 if t < t_div1 else 3, cam=cam_n, e=en, xd=xd,
                    ts_m=t if not (T["pode2"] <= t < T["anulado1"]) else T["pode2"])
    elif t < T["leve"] - 0.02:
        L = estado_l3(t, T)
        e = {"ts": ts_l3(t, T), "urso": URSO_POS, "abajur": 0.0, "lua": 0.0}
        if t < t_div3:
            cam = cam_l3(t, T)
            cena_noite(cv, cam, e, lance3=L)
            info.update(lance=3, cam=cam, e=e, L=L)
        else:
            # "Chamar de crescimento": entra pela esquerda o padrão do LANCE 1 (as DUAS pernas com dor)
            abre3 = e_inout(prog(t, t_div3, t_div3 + 0.34))
            xd = lerp(JX0 - 4, DIV_X, abre3)
            cam_r = lerp3(cam4(CAM_Z3), CAM_R3, abre3)
            cv.save(); cv.clipRect(skia.Rect(xd, 0, W, H), True)
            cena_noite(cv, cam_r, e, lance3=L)
            cv.restore()
            cam_l = CAM_MINI[:3] + (CAM_MINI[3] + (xd - DIV_X),)
            if xd > JX0:
                cv.save(); cv.clipRect(skia.Rect(0, 0, xd, H), True)
                cena_noite(cv, cam_l, {"ts": e["ts"], "urso": URSO_POS, "abajur": 0.3, "lua": 0.0})
                cv.restore()
                cv.drawLine(xd, JY0, xd, JY1, paint(CIANO, 150, "stroke", 22, blur=9))
                cv.drawLine(xd, JY0, xd, JY1, paint("#FFFFFF", 255, "stroke", 6))
            info.update(lance=3, cam=cam_r, cam_l=cam_l, e=e, L=L, xd=xd, split=True)
    else:
        cena_porta(cv, t, T, CAM_PORTA)
        info.update(lance=3, cam=CAM_PORTA, porta=True)
    return info


# ================================================================== HUD do VAR (desenho próprio, cópia do piloto)
def fundo(cv, t):
    def _d(c):
        sh = skia.GradientShader.MakeRadial(skia.Point(W / 2, H * 0.42), H * 0.75, [_c(ARD_IN), _c(ARD_OUT)])
        c.drawRect(skia.Rect(0, 0, W, H), paint(ARD_IN, shader=sh))
    cv.drawImage(cacheado("fundo", W, H, _d), 0, 0)


def vinheta(cv):
    def _d(c):
        c.translate(-JX0, -JY0)
        vin = skia.GradientShader.MakeRadial(skia.Point(JCX, JCY), 760, [_c("#000000", 0), _c("#000000", 0), _c("#000000", 80)],
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
        if flash > 0:
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


def colchetes(cv, c, d, meio_l, meio_h, a, cor=CIANO):
    """Cantoneiras de seleção do telestrador em volta de um retângulo girado (centro c, eixo d)."""
    if a <= 0:
        return
    n = (-d[1], d[0])
    for sx in (-1, 1):
        for sy in (-1, 1):
            q = (c[0] + d[0] * meio_l * sx + n[0] * meio_h * sy, c[1] + d[1] * meio_l * sx + n[1] * meio_h * sy)
            q1 = (q[0] - d[0] * 30 * sx, q[1] - d[1] * 30 * sx)
            q2 = (q[0] - n[0] * 26 * sy, q[1] - n[1] * 26 * sy)
            p = poli([q1, q, q2], fechar=False)
            pt = paint(CARTAO, int(160 * a), "stroke", 13); pt.setStrokeJoin(skia.Paint.kRound_Join); cv.drawPath(p, pt)
            pt = paint(cor, int(255 * a), "stroke", 7); pt.setStrokeJoin(skia.Paint.kRound_Join); cv.drawPath(p, pt)


def seta_circular(cv, x, y, r, ang0, a, cor=CIANO):
    """Seta circular do telestrador (o movimento da massagem, devagar)."""
    if a <= 0:
        return
    rect = skia.Rect(x - r, y - r * 0.62, x + r, y + r * 0.62)
    pth = skia.Path(); pth.addArc(rect, ang0, 250)
    cv.drawPath(pth, paint(CARTAO, int(150 * a), "stroke", 12))
    cv.drawPath(pth, paint(cor, int(255 * a), "stroke", 6))
    fim = math.radians(ang0 + 250)
    ex, ey = x + r * math.cos(fim), y + r * 0.62 * math.sin(fim)
    tg = math.atan2(0.62 * math.cos(fim), -math.sin(fim))
    ponta(cv, ex, ey, tg, 20, CARTAO, 0.6 * a)
    ponta(cv, ex, ey, tg, 16, cor, a)


def linha_tracejada(cv, pts_ctrl, k, a, quebra=0.0, cor=CIANO):
    """Linha TRACEJADA do telestrador (curva quadrática), desenhada até k; `quebra` abre um vão no meio."""
    if a <= 0 or k <= 0:
        return
    p0, pc, p1 = pts_ctrl
    pth = skia.Path(); pth.moveTo(*p0); pth.quadTo(pc[0], pc[1], p1[0], p1[1])
    if quebra > 0:                                                    # parte em dois (o vão abre do meio)
        g = 0.5 * quebra * 0.32
        for (u0, u1) in ((0.0, 0.5 - g), (0.5 + g, 1.0)):
            pe = skia.TrimPathEffect.Make(u0, max(u0 + 0.002, min(u1, k)))
            if u0 >= k or pe is None:
                continue
            for cc, w, al in ((CARTAO, 15, 150), (cor, 7, 255)):
                pt = paint(cc, int(al * a), "stroke", w)
                pt.setPathEffect(skia.PathEffect.MakeCompose(skia.DashPathEffect.Make([24.0, 14.0], 0.0), pe))
                cv.drawPath(pth, pt)
    else:
        for cc, w, al in ((CARTAO, 15, 150), (cor, 7, 255)):
            pt = paint(cc, int(al * a), "stroke", w)
            pe = skia.TrimPathEffect.Make(0.0, max(0.002, k)) if k < 0.999 else None
            dash = skia.DashPathEffect.Make([24.0, 14.0], 0.0)
            pt.setPathEffect(skia.PathEffect.MakeCompose(dash, pe) if pe is not None else dash)
            cv.drawPath(pth, pt)
    cv.drawCircle(p0[0], p0[1], 9, paint(cor, int(255 * a)))
    if k >= 0.999:
        cv.drawCircle(p1[0], p1[1], 9, paint(cor, int(255 * a)))


def seta_curva(cv, p0, pc, p1, k, a, cor=CIANO):
    """Seta curva do telestrador (da lua ao sol)."""
    if a <= 0 or k <= 0:
        return
    pth = skia.Path(); pth.moveTo(*p0); pth.quadTo(pc[0], pc[1], p1[0], p1[1])
    cv.drawPath(pth, _trim(paint(CARTAO, int(150 * a), "stroke", 15), k))
    cv.drawPath(pth, _trim(paint(cor, int(255 * a), "stroke", 8), k))
    # ponta no ponto atual
    u = clamp(k)
    x = (1 - u) ** 2 * p0[0] + 2 * (1 - u) * u * pc[0] + u * u * p1[0]
    y = (1 - u) ** 2 * p0[1] + 2 * (1 - u) * u * pc[1] + u * u * p1[1]
    tx = 2 * (1 - u) * (pc[0] - p0[0]) + 2 * u * (p1[0] - pc[0]); ty = 2 * (1 - u) * (pc[1] - p0[1]) + 2 * u * (p1[1] - pc[1])
    ang = math.atan2(ty, tx)
    ponta(cv, x, y, ang, 34, CARTAO, 0.7 * a)
    ponta(cv, x, y, ang, 28, cor, a)


def carimbo_cor(cv, s, x, y, rot, t0, t, dur, cor, tam=88, esc0=1.9, sub=None, tam_sub=44):
    """Carimbo do veredito: OPACO, cor do semáforo, entra batendo e sai encolhendo para o chip do selo.
    `sub`: 2ª linha dentro do mesmo carimbo (a condição: DOR NAS DUAS PERNAS)."""
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


def marca_ok(cv, x, y, r, cor, a, brilho=0.0):
    """Visto desenhado (sem texto) num disco escuro."""
    if a <= 0:
        return
    if brilho > 0:
        cv.drawCircle(x, y, r * 1.7, paint(cor, int(120 * brilho * a), blur=16))
    cv.drawCircle(x, y, r + 6, paint("#000000", int(90 * a), blur=8))
    cv.drawCircle(x, y, r, paint(CARTAO, int(235 * a)))
    cv.drawCircle(x, y, r, paint(cor, int(255 * a), "stroke", 5))
    p = poli([(x - r * 0.45, y + r * 0.02), (x - r * 0.12, y + r * 0.35), (x + r * 0.5, y - r * 0.32)], fechar=False)
    pt = paint(cor, int(255 * a), "stroke", 9); pt.setStrokeCap(skia.Paint.kRound_Cap); pt.setStrokeJoin(skia.Paint.kRound_Join)
    cv.drawPath(p, pt)


def pop_marca(cv, fn, x, y, t, t0, a, r=38, **kw):
    k = e_back(prog(t, t0, t0 + 0.24))
    if k <= 0 or a <= 0:
        return
    cv.save(); cv.translate(x, y); s = clamp(k, 0, 1.2); cv.scale(s, s)
    fn(cv, 0, 0, r, VERDE if fn is marca_ok else AMBAR, a, **kw)
    cv.restore()


# palavras de ligação: nunca terminam um bloco nem uma linha da legenda
LIGACAO = {"a", "o", "as", "os", "e", "de", "da", "do", "das", "dos", "em", "no", "na", "nos", "nas", "um", "uma",
           "pra", "que", "com", "é", "sua", "seu", "lá", "ele", "ou", "como", "pela"}
NAO_ABRE = {"morna"}                     # não abre bloco: 'COMPRESSA' / 'MORNA' separava o pano do 'morna'
ESP_LEG, LARG_LEG = 26, 920


def _base_tok(p):
    import re
    return re.sub(r"[.,:;!?—]", "", p["tok"]).lower()


def partir_linhas(bloco, tam):
    """Linhas da legenda de um bloco (quebra EQUILIBRADA, sem linha terminando em palavra de ligação). (gesso)"""
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
    """Blocos da legenda (cópia do gesso): frase por frase, até 6 palavras e 2 linhas; senão divide no melhor
    ponto — nunca depois de palavra de ligação, de preferência depois da vírgula. A CTA fica inteira."""
    frases = []
    for b in montar_blocos(pal):
        if frases and not frases[-1][-1]["fim_frase"]:
            frases[-1] = frases[-1] + b
        else:
            frases.append(list(b))
    # a pergunta curta fica no MESMO bloco do que ela pergunta ('E CHAMAR DE FRESCURA: PODE?') (socorros)
    juntas = []
    for fr in frases:
        ant = juntas[-1] if juntas else None
        if (ant and len(ant) > 1 and ant[-1]["tok"].endswith(":") and fr[-1]["tok"].endswith("?")
                and len(ant) + len(fr) <= 6):
            juntas[-1] = ant + fr
        else:
            juntas.append(fr)
    frases = juntas

    def dividir(fr):
        if fr[0]["w"].lower() == "manda" or (len(fr) <= 6 and len(partir_linhas(fr, 80)) <= 2):
            return [fr]
        melhor = None
        for i in range(1, len(fr)):
            sc = abs(i - (len(fr) - i))
            if _base_tok(fr[i - 1]) in LIGACAO:
                sc += 100
            if _base_tok(fr[i]) in NAO_ABRE:
                sc += 50
            if fr[i - 1].get("virg"):
                sc -= 3
            if _base_tok(fr[i]) in ("e", "mas"):
                sc -= 2
            if i == 1 or len(fr) - i == 1:
                sc += 3
            if i < len(fr) - i:
                sc += 0.25
            if melhor is None or sc < melhor[0]:
                melhor = (sc, i)
        i = melhor[1]
        return dividir(fr[:i]) + dividir(fr[i:])
    blocos = []
    for fr in frases:
        blocos += dividir(fr)
    return blocos


def legenda_var(cv, blocos, t, destaque, y_base=1395, tam=80, a_extra=1.0):
    """Legenda karaokê do piloto (a palavra ativa cresce do PRÓPRIO CENTRO), quebra equilibrada."""
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
VEREDITOS = (("pode1", "validado", T_VALID, VERDE), ("pode2", "anulado1", T_ANUL, AMBAR),
             ("pode3", "anulado2", T_ANUL, AMBAR))
DUR_CARIMBOS = (1.5, 1.2, 1.3)
# v5: o VALIDADO (LANCE 1) pousa ACIMA do monitor, à direita do selo VAR (x 247-973, y ~100-340 girado a -5°);
# em (420, 470) ele cobria a cabeça da criança recostada na cabeceira (5,4-6,2 s).
POS_CARIMBOS = ((610.0, 222.0), (DIV_X, 470.0), (JCX, 470.0))
SUB_CARIMBOS = (T_DUAS, None, None)


def chip_estado(t, T):
    """(texto, alfa, pontos, cor, flash) do chip: LANCE n -> CHECANDO -> (carimbo) -> veredito -> JEITO CERTO."""
    cortes = (0.0, T["e2"], T["noite3"], 1e9)
    certo = (T["validado"] + DUR_CARIMBOS[0] - 0.05, T["anulado1"] + DUR_CARIMBOS[1] - 0.05, T["leve"] - 0.02)
    for k, (pd, vd, s, cor) in enumerate(VEREDITOS):
        if not (cortes[k] <= t < cortes[k + 1]):
            continue
        flash = 0.0
        if t < T[pd + "_fim"] + 0.04:
            a = 1.0
            if k > 0:
                a = prog(t, cortes[k] + 0.02, cortes[k] + 0.12)
                flash = 1 - prog(t, cortes[k] + 0.06, cortes[k] + 0.3)
            return T_LANCE[k], a, -1, "#FFFFFF", flash
        if t < T[vd] - 0.04:
            t0 = T[pd + "_fim"] + 0.04
            return T_CHEC, 1.0, prog(t, t0, T[vd] - 0.12), "#FFFFFF", 0.0
        dur = DUR_CARIMBOS[k]
        if t < T[vd] + dur - 0.05:
            return None, 0.0, -1, "#FFFFFF", 0.0
        if t >= certo[k]:
            return T_CERTO, prog(t, certo[k], certo[k] + 0.18), -1, VERDE, 0.0
        a = prog(t, T[vd] + dur - 0.1, T[vd] + dur + 0.1) * (1 - prog(t, certo[k] - 0.12, certo[k]))
        return s, a, -1, cor, 0.0
    return None, 0.0, -1, "#FFFFFF", 0.0


# geometria do lance 2 (coordenadas de tela)
LUA_TELA = na_tela(CAM_MEIA, *LUA_C)
SOL_TELA = (DIV_X + 420.0, JY0 + 118.0)


def ponto_quad(p0, pc, p1, u):
    return ((1 - u) ** 2 * p0[0] + 2 * (1 - u) * u * pc[0] + u * u * p1[0],
            (1 - u) ** 2 * p0[1] + 2 * (1 - u) * u * pc[1] + u * u * p1[1])


def meio_curva(p0, pc, p1, n=80):
    """Ponto na METADE DO COMPRIMENTO da curva (onde a linha tracejada se parte e o X cai)."""
    pts = [ponto_quad(p0, pc, p1, i / n) for i in range(n + 1)]
    acc = [0.0]
    for a_, b_ in zip(pts, pts[1:]):
        acc.append(acc[-1] + math.hypot(b_[0] - a_[0], b_[1] - a_[1]))
    meio = acc[-1] / 2
    for i in range(1, n + 1):
        if acc[i] >= meio:
            k = (meio - acc[i - 1]) / ((acc[i] - acc[i - 1]) or 1.0)
            return lerp2(pts[i - 1], pts[i], k)
    return pts[-1]


def pontos_linha(T, t):
    """A linha tracejada 'é frescura': dos risquinhos da noite até a perna que corre de manhã. A curva cruza a
    divisória no alto (parede), e é ali — longe de qualquer perna — que o círculo e o X caem."""
    p0 = na_tela(CAM_MEIA, *ponto_canela(PERNA_LONGE, 0.62, -(r_canela(0.62) + 50)))
    _, (Hf, Kf, Af, _), _ = pose_manha(T["pode2"] if t >= T["pode2"] else t)
    (Hb, Kb, Ab, _), _, _ = pose_manha(T["pode2"] if t >= T["pode2"] else t)
    mb = lerp2(Kb, Ab, 0.42)
    p1 = (DIV_X + mb[0] - 40, JY0 + mb[1])
    pc = (DIV_X - 30, JY0 + 120.0)
    return p0, pc, p1


def setas_incha(cv, cam, a, k, pulso=0.0):
    """'Inchaço': setinhas saindo do joelho para fora (o contorno do joelho cresce; a pele não muda de cor)."""
    if a <= 0 or k <= 0:
        return
    s = cam[0]
    cx, cy = na_tela(cam, *ponto_canela(PERNA_PERTO, U_INCH, 0))
    d, n = eixo(PERNA_PERTO)
    phi = math.degrees(math.atan2(n[1], n[0]))
    vai = 5 * math.sin(pulso * 2 * math.pi)
    for dang in (180 - 42, 180 + 42, 48):
        ang = math.radians(phi + dang)
        ux, uy = math.cos(ang), math.sin(ang)
        r0 = (50 + vai) * s; r1 = r0 + 46 * s * k
        x0, y0 = cx + ux * r0, cy + uy * r0
        x1, y1 = cx + ux * r1, cy + uy * r1
        cv.drawLine(x0, y0, x1, y1, paint(CARTAO, int(160 * a), "stroke", 16))
        cv.drawLine(x0, y0, x1, y1, paint(CIANO, int(255 * a), "stroke", 8))
        ponta(cv, x1, y1, ang, 22 * s, CARTAO, 0.7 * a)
        ponta(cv, x1, y1, ang, 18 * s, CIANO, a)


Y_ROTULO = JY0 + 790.0          # chip do padrão: no chão da metade esquerda (era JY0 + 66, colado no carimbo)


def rotulo_padrao(cv, x, y, a):
    """Chip da metade esquerda do LANCE 3: o padrão que o LANCE 1 validou (visto verde + SE DÓI NAS DUAS PERNAS)."""
    if a <= 0:
        return
    tam = 30
    lw = larg_texto(T_DUAS, F_BLACK, tam)
    w = lw + 82
    rr = skia.RRect.MakeRectXY(skia.Rect(x - w / 2, y - 28, x + w / 2, y + 28), 28, 28)
    cv.drawRRect(rr, paint("#000000", int(100 * a), blur=10))
    cv.drawRRect(rr, paint(CARTAO, int(240 * a)))
    cv.drawRRect(rr, paint(VERDE, int(255 * a), "stroke", 3.5))
    vx = x - w / 2 + 30
    p = poli([(vx - 11, y + 1), (vx - 3, y + 9), (vx + 12, y - 8)], fechar=False)
    pt = paint(VERDE, int(255 * a), "stroke", 6); pt.setStrokeCap(skia.Paint.kRound_Cap); pt.setStrokeJoin(skia.Paint.kRound_Join)
    cv.drawPath(p, pt)
    texto(cv, T_DUAS, x - w / 2 + 56 + lw / 2, y + 11, F_BLACK, tam, "#FFFFFF", int(255 * a))


def hud_lance(cv, t, T, info):
    lance = info.get("lance")
    cam = info.get("cam")
    if lance == 1:
        s = cam[0]
        e = info["e"]
        # quadro 0: círculo em volta das mãos massageando as duas panturrilhas
        if t < T["var"] + 0.12:
            a_c = 1.0 if t < T["var"] else 1 - prog(t, T["var"], T["var"] + 0.12)
            pul = 0.5 + 0.5 * math.sin(t * 8) + 1.5 * max(0.0, 1 - abs(t - T["chama"] - 0.1) / 0.18)
            x, y = na_tela(cam, 792, 878)
            circulo_tele(cv, x, y, 196 * s, 124 * s, 1.0, a_c, 0.7, pul)
        # "pernas": colchetes nas DUAS panturrilhas
        a_b = janela(t, T["pernas"] - 0.04, T["massagem1"] - 0.1, 0.12, 0.2)
        if a_b > 0:
            for P, seed in ((PERNA_LONGE, 0), (PERNA_PERTO, 1)):
                d, n = eixo(P)
                c = na_tela(cam, *ponto_canela(P, 0.48, 0))
                kk = e_back(prog(t, T["pernas"] - 0.04 + 0.06 * seed, T["pernas"] + 0.22 + 0.06 * seed))
                colchetes(cv, c, d, 122 * s * clamp(kk, 0.6, 1.15), 46 * s * clamp(kk, 0.6, 1.15), a_b)
        # "pode?": congela, círculo em volta das mãos + panturrilhas
        k1 = e_out(prog(t, T["pode1"] + 0.12, T["pode1"] + 0.47))
        fora = 1 - prog(t, T["validado"] + 0.3, T["validado"] + 0.55)
        if k1 > 0 and fora > 0:
            pul = 0.5 + 0.5 * math.sin(t * 8) if T["pode1_fim"] < t < T["validado"] else 0.0
            x, y = na_tela(cam, 792, 878)
            circulo_tele(cv, x, y, 196 * s, 124 * s, k1, k1 * fora, 2.3, pul)
        # massagem: setas circulares em volta das mãos
        a_m = janela(t, T["massagem2"] - 0.02, T["compressa"] - 0.1, 0.15, 0.2)
        if a_m > 0:
            for pose, fase, a_k in ((e["mao_e"], 0.0, a_m), (e["mao_d"], 140.0, a_m * (1 - prog(t, T["massagem2"] + 0.12, T["massagem2"] + 0.24)))):
                if pose is None or a_k <= 0:
                    continue
                (px, py), _ = pose
                x, y = na_tela(cam, px - 4, py + 20)
                seta_circular(cv, x, y, 74 * s, (t - T["massagem2"]) * 160 + fase, a_k)
        # "costumam": visto verde ANCORADO na compressa (os risquinhos ficam: sem promessa)
        a_ok = prog(t, T["costumam"] - 0.04, T["costumam"] + 0.1) * (1 - prog(t, T["e2"] - 0.2, T["e2"]))
        if a_ok > 0:
            x, y = na_tela(cam, COMP_CALF[0][0] + 8, COMP_CALF[0][1] - 58)
            pop_marca(cv, marca_ok, x, y, t, T["costumam"] - 0.04, a_ok, 30 * min(1.0, s))
    elif lance == 2:
        xd = info.get("xd", DIV_X)
        a_l2 = 1 - prog(t, T["noite3"], T["noite3"] + 0.25)
        if a_l2 <= 0:
            return
        p0, pc, p1 = pontos_linha(T, t)
        meio = meio_curva(p0, pc, p1)
        k_l = e_inout(prog(t, T["frescura"] - 0.06, T["frescura"] + 0.5))
        quebra = e_out(prog(t, T["anulado1"] - 0.02, T["anulado1"] + 0.3))
        a_lin = a_l2 * (1 - 0.55 * prog(t, T["dor2"] - 0.1, T["dor2"] + 0.2))
        if xd < JX1 - 4:
            linha_tracejada(cv, (p0, pc, p1), k_l, a_lin, quebra)
        # 'pode?': o círculo marca a LIGAÇÃO noite|manhã (na divisória), nunca uma perna
        k1 = e_out(prog(t, T["pode2"] + 0.12, T["pode2"] + 0.47))
        fora = 1 - prog(t, T["anulado1"] + 0.3, T["anulado1"] + 0.55)
        if k1 > 0 and fora > 0:
            pul = 0.5 + 0.5 * math.sin(t * 8) if T["pode2_fim"] < t < T["anulado1"] else 0.0
            circulo_tele(cv, meio[0], meio[1], 96, 74, k1, k1 * fora * a_l2, 4.3, pul)
        # X na linha partida (fica até o fim do lance)
        a_x = prog(t, T["anulado1"] + 0.05, T["anulado1"] + 0.15) * a_l2
        if a_x > 0:
            pop_marca(cv, marca_x, meio[0], meio[1], t, T["anulado1"] + 0.05, a_x, 36)
        # 'dor ... real': visto verde EM CIMA dos risquinhos da noite
        brilho = max(0.0, 1 - abs(t - T["real"] - 0.15) / 0.35)
        vn = na_tela(CAM_MEIA, *ponto_canela(PERNA_LONGE, 0.3, -(r_canela(0.3) + 96)))
        pop_marca(cv, marca_ok, vn[0], vn[1], t, T["dor2"] - 0.04, a_l2, 38, brilho=brilho)
        # 'manhã': visto verde junto da perna LIMPA que corre de manhã
        if xd < JX1 - 100:
            pop_marca(cv, marca_ok, DIV_X + 452, JY0 + 520, t, T["manha"] - 0.04, a_l2, 38,
                      brilho=max(0.0, 1 - abs(t - T["manha"] - 0.2) / 0.35))
        # 'some': seta da lua ao sol, levando os risquinhos que se apagam pelo caminho
        k_s = e_inout(prog(t, T["some"] - 0.06, T["some"] + 0.45))
        if k_s > 0:
            a0 = (LUA_TELA[0] + 46, LUA_TELA[1] - 30); ac = (DIV_X, JY0 + 40); a1 = (SOL_TELA[0] - 66, SOL_TELA[1] + 6)
            seta_curva(cv, a0, ac, a1, k_s, a_l2)
            for i in range(3):
                u = clamp(k_s * 1.15 - 0.13 * (i + 1))
                if u <= 0:
                    continue
                x, y = ponto_quad(a0, ac, a1, u)
                risco_dor(cv, x, y + 34, -8 + 10 * i, 0.85, a_l2 * (1 - u) ** 1.2)
    elif lance == 3 and not info.get("porta"):
        s = cam[0]
        L = info.get("L")
        if L is None:
            return
        a_pre = 1 - prog(t, T["chamar2"] - 0.2, T["chamar2"] + 0.02)    # os sinais saem quando a tela divide
        # 'lado': círculo SÓ na perna que dói
        a_c = prog(t, T["lado"] - 0.04, T["lado"] + 0.08) * (1 - prog(t, T["inchaco"] - 0.12, T["inchaco"] + 0.05))
        if a_c > 0:                                                 # (um sinal por vez: sai quando o inchaço entra)
            x, y = na_tela(cam, *ponto_canela(PERNA_PERTO, 0.5, 6))
            circulo_tele(cv, x, y, 150 * s, 70 * s, e_out(prog(t, T["lado"] - 0.04, T["lado"] + 0.3)), a_c, 1.7, 0.0)
        # 'inchaço': setinhas para fora em volta do joelho (o contorno cresce)
        a_i = prog(t, T["inchaco"] - 0.04, T["inchaco"] + 0.1) * a_pre
        if a_i > 0:
            setas_incha(cv, cam, a_i, e_out(prog(t, T["inchaco"] - 0.04, T["inchaco"] + 0.4)), t * 1.6)
        if not info.get("split"):
            return
        cam_l = info["cam_l"]; xd = info["xd"]
        # (o chip do padrão do LANCE 1 — SE DÓI NAS DUAS PERNAS — é desenhado em quadro(), DEPOIS do carimbo e
        # embaixo da metade esquerda: v3, ver Y_ROTULO)
        # 'Chamar de crescimento': a linha liga as DUAS pernas (esquerda) à perna que dói (direita)
        p0 = na_tela(cam_l, *ponto_canela(PERNA_LONGE, 0.5, -(r_canela(0.5) + 64)))
        p1 = na_tela(cam, *ponto_canela(PERNA_PERTO, 0.42, -(r_canela(0.42) + 6)))
        pc = (DIV_X + 10, JY0 + 170.0)
        meio = meio_curva(p0, pc, p1)
        k_l = e_inout(prog(t, T["crescimento2"] - 0.1, T["crescimento2"] + 0.45))
        quebra = e_out(prog(t, T["anulado2"] - 0.02, T["anulado2"] + 0.3))
        a_lin = 1 - 0.55 * prog(t, T["trate"] + 0.1, T["trate"] + 0.5)
        if xd > DIV_X - 4:
            linha_tracejada(cv, (p0, pc, p1), k_l, a_lin, quebra)
        # 'pode?': círculo SÓ em volta da perna que dói
        k1 = e_out(prog(t, T["pode3"] + 0.12, T["pode3"] + 0.47))
        fora = 1 - prog(t, T["anulado2"] + 0.3, T["anulado2"] + 0.55)
        if k1 > 0 and fora > 0:
            pul = 0.5 + 0.5 * math.sin(t * 8) if T["pode3_fim"] < t < T["anulado2"] else 0.0
            x, y = na_tela(cam, *ponto_canela(PERNA_PERTO, 0.5, 6))
            circulo_tele(cv, x, y, 158 * s, 78 * s, k1, k1 * fora, 3.1, pul)
        # 'Anulado': o X cai na LINHA (o nome), na divisória — nunca sobre a criança
        a_x = prog(t, T["anulado2"] + 0.05, T["anulado2"] + 0.15)
        if a_x > 0:
            pop_marca(cv, marca_x, meio[0], meio[1], t, T["anulado2"] + 0.05, a_x, 36)
    elif info.get("porta"):
        s = cam[0]
        px0, py0, px1, py1 = PORTA_R
        x, y = na_tela(cam, (px0 + px1) / 2, py0 + 120)
        k_c = e_back(prog(t, T["avaliar"] - 0.06, T["avaliar"] + 0.22))
        if k_c > 0:
            cv.save(); cv.translate(x, y); cv.scale(clamp(k_c, 0, 1.2), clamp(k_c, 0, 1.2))
            placa_estetoscopio(cv, 0, 0, 48 * s, 1.0)
            cv.restore()
        a_v = prog(t, T["avaliar"] + 0.2, T["avaliar"] + 0.4)
        if a_v > 0:
            x0, y0 = na_tela(cam, px0 - 10, py0 - 10); x1, y1 = na_tela(cam, px1 + 10, py1)
            rr = skia.RRect.MakeRectXY(skia.Rect(x0, y0, x1, y1), 10, 10)
            cv.drawRRect(rr, paint(VERDE, int(140 * a_v), "stroke", 22, blur=8))
            cv.drawRRect(rr, paint(VERDE, int(255 * a_v), "stroke", 6))
            ox, oy = na_tela(cam, px0 - 54, py0 + 40)
            pop_marca(cv, marca_ok, ox, oy, t, T["avaliar"] + 0.3, 1.0, 40)


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
        ruido_vhs(cv, t, max(rebob, janela(t, T["e2"] - 0.06, T["e2"] + 0.24, 0.03, 0.06),
                             janela(t, T["noite3"] - 0.02, T["noite3"] + 0.3, 0.03, 0.06)))
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
        hud_lance(cv, t, T, info)
        for t0, forca in ((T["pode1"], 150), (T["pode2"], 150), (T["pode3"], 150), (T["e2"] - 0.05, 170),
                          (T["noite3"], 170), (T["leve"] - 0.02, 190)):
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
        a_reb = max(janela(t, T["var"], T["var"] + 0.5, 0.03, 0.08), janela(t, T["e2"] - 0.06, T["e2"] + 0.3, 0.03, 0.08),
                    janela(t, T["noite3"], T["noite3"] + 0.4, 0.03, 0.08))
        icone_rebobina(cv, JX1 - 76, JY1 - 74, a_hud * a_reb * (0.0 if congelado else 1.0))
        for (pd, vd, s_, cor), dur, (px, py), sub in zip(VEREDITOS, DUR_CARIMBOS, POS_CARIMBOS, SUB_CARIMBOS):
            carimbo_cor(cv, s_, px, py, -5, T[vd] - 0.02, t, dur, cor, sub=sub)
        # LANCE 3 dividido: o chip do padrão do LANCE 1 (visto verde + SE DÓI NAS DUAS PERNAS) fica EMBAIXO da metade
        # esquerda (no chão, sob a cama) e é desenhado DEPOIS do carimbo. v3: no alto da metade, ele ficava colado
        # em cima do carimbo ANULADO (lido junto: "SE DÓI NAS DUAS PERNAS / ANULADO", o contrário da mensagem) e, na
        # saída, o carimbo passava por cima de "DUAS PERNAS". Agora ~560 px separam os dois e o carimbo, se cruzar,
        # passa por trás do texto.
        if info.get("split"):
            cv.save(); cv.clipRRect(jan_rr, skia.ClipOp.kIntersect, True)
            rotulo_padrao(cv, info["xd"] - 256.0, Y_ROTULO, prog(t, T["chamar2"] + 0.12, T["chamar2"] + 0.32))
            cv.restore()
        # rótulo grande do corte de lance (LANCE 2 e LANCE 3)
        for t0, s in ((T["e2"] - 0.05, T_LANCE[1]), (T["noite3"], T_LANCE[2])):
            k = t - t0
            if -0.02 <= k < 0.7:
                a = prog(k, 0.0, 0.08) * (1 - prog(k, 0.5, 0.7))
                esc = lerp(1.25, 1.0, e_out(prog(k, 0.0, 0.16)))
                cv.save(); cv.translate(JX0 + 210, JY0 + 112); cv.scale(esc, esc)
                f = skia.Font(F_BLACK, 70); lw = f.measureText(s)
                rr = skia.RRect.MakeRectXY(skia.Rect(-lw / 2 - 34, -70, lw / 2 + 34, 26), 16, 16)
                cv.drawRRect(rr, paint(CARTAO, int(225 * a))); cv.drawRRect(rr, paint(CIANO, int(255 * a), "stroke", 4))
                texto(cv, s, 0, 0, F_BLACK, 70, "#FFFFFF", int(255 * a))
                cv.restore()

    # ---------- selo VAR + chip: entra em "VAR", dentro do monitor; sobe depois que o gancho saiu
    t_capa = T["pode1_fim"] + 0.06
    sobe = e_inout(prog(t, t_capa + 0.45, t_capa + 0.85))
    chip, a_chip, pontos, cor_chip, flash = chip_estado(t, T)
    k_s = prog(t, T["var"] - 0.04, T["var"] + 0.14)
    esc_s = lerp(0.92, 1.08, sobe) * (1 + 0.25 * (1 - e_back(k_s))) if k_s < 1 else lerp(0.92, 1.08, sobe)
    selo_var(cv, t, lerp(56, 64, sobe), lerp(JY0 + 24, 146, sobe), esc_s, a_hud * clamp(k_s * 1.5), chip, a_chip,
             pontos, cor_chip, flash)

    # ---------- fecho: febre + manqueira juntas = atendimento no mesmo dia
    a_f = prog(t, T["febre2"] - 0.1, T["febre2"] + 0.2) * (1 - prog(t, T["manda"] - 0.35, T["manda"] - 0.1))
    if a_f > 0:
        cv.drawCircle(CX, 740, 300, paint(TEAL, int(40 * a_f), blur=60))
        k_sol = e_out(prog(t, T["mesmo"] - 0.08, T["mesmo"] + 0.6))
        if k_sol > 0:
            sol_icone(cv, CX - 200, lerp(860, 520, k_sol), 62, a_f * clamp(k_sol * 2), t * 25)
        ent = e_back(prog(t, T["febre2"] - 0.1, T["febre2"] + 0.3))
        # a profissional de saúde (sem rosto), SEM apito na mão (o leitor via um secador)
        profissional(cv, CX, 770 + 40 * (1 - clamp(ent)), 1.75 * clamp(ent, 0, 1.1), a_f, 1.0, braco=False)
        # termômetro (da esquerda) e pegadas (da direita) que se encostam em 'juntas'
        k_j = e_inout(prog(t, T["juntas"] - 0.05, T["juntas"] + 0.35))
        k_t = e_out(prog(t, T["febre2"] - 0.02, T["febre2"] + 0.35))
        xt = lerp(lerp(-80, 330, k_t), 470, k_j)
        termometro(cv, xt, 1112, 0.9, 1.0, a_f * clamp(k_t * 3))
        k_p = e_out(prog(t, T["manqueira2"] - 0.02, T["manqueira2"] + 0.35))
        xp = lerp(lerp(1160, 760, k_p), 618, k_j)
        if k_p > 0:
            pegada(cv, xp - 26, 1152, -90, 1.5, a_f * clamp(k_p * 3))
            pegada(cv, xp + 28, 1124, -90, 1.5 * 0.78, a_f * clamp(k_p * 3) * 0.62)
        k_c = e_out(prog(t, T["juntas"] + 0.2, T["juntas"] + 0.6))
        circulo_tele(cv, 548, 1126, 190, 112, k_c, a_f, 1.2, max(0.0, 1 - abs(t - T["dia"] - 0.1) / 0.25))
    selo_serie(cv, prog(t, T["febre2"] - 0.1, T["febre2"] + 0.2) * (1 - prog(t, T["manda"] - 0.3, T["manda"])))

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


def rebobinar(seed=31, dur=0.5):
    n = int(dur * SR); t = np.arange(n) / SR
    x = np.random.default_rng(seed).standard_normal(n)
    fc = 600 + 2600 * np.abs(np.sin(np.pi * t / dur * 1.5))
    y = np.zeros(n); acc = 0.0
    for i in range(n):
        a = np.exp(-2 * np.pi * fc[i] / SR); acc = (1 - a) * x[i] + a * acc; y[i] = acc
    f = 900 * np.exp(-t * 3.2) + 200
    saw = 2 * ((np.cumsum(f) / SR) % 1.0) - 1
    env = np.clip(t / 0.02, 0, 1) * np.clip((dur - t) / 0.05, 0, 1)
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
    """Atrito macio (a massagem): 'pfff' grave e abafado. (piloto)"""
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
def grilos(dur, seed=161):
    """Grilos de fundo: chirp de ~4,5 kHz com AM ~30 Hz, 3 pulsos a cada ~1,2 s (bem baixinho)."""
    n = int(dur * SR); y = np.zeros(n)
    rng = np.random.default_rng(seed)
    t0 = rng.uniform(0.05, 0.3)
    while t0 < dur - 0.3:
        f = rng.uniform(4300, 4700)
        for k in range(3):
            p = int((t0 + k * 0.085) * SR); m = int(0.055 * SR)
            if p + m >= n:
                break
            tt = np.arange(m) / SR
            am = 0.5 + 0.5 * np.sin(2 * np.pi * 30 * tt)
            y[p:p + m] += np.sin(2 * np.pi * f * tt) * am * np.sin(np.pi * tt / 0.055)
        t0 += rng.uniform(1.0, 1.4)
    env = np.clip(np.arange(n) / SR / 0.1, 0, 1) * np.clip((dur - np.arange(n) / SR) / 0.08, 0, 1)
    return y * env * 0.5


def passarinho(seed=171):
    """Dois trinados curtos (glissando 3 -> 4,5 kHz, 80 ms) — a manhã."""
    partes = []
    for k in range(2):
        m = int(0.08 * SR); tt = np.arange(m) / SR
        f = 3000 + 1500 * (tt / 0.08) + 120 * np.sin(2 * np.pi * 60 * tt)
        partes += [np.sin(2 * np.pi * np.cumsum(f) / SR) * np.sin(np.pi * tt / 0.08) * 0.5, np.zeros(int(0.06 * SR))]
    return np.concatenate(partes)


def pano(seed=181):
    """A compressa pousando: ruído abafado (passa-baixa 800 Hz), 0,2 s, ataque suave."""
    n = int(0.2 * SR); t = np.arange(n) / SR
    x = som._onepole_lp(som._onepole_lp(np.random.default_rng(seed).standard_normal(n), 800), 800)
    return x * np.sin(np.pi * t / 0.2) ** 1.5 * 2.6


def passos_desiguais(seed=191):
    """Passos de quem manca: forte, (0,18 s) fraco, (0,32 s) forte."""
    a = som.thump(seed); b = som.thump(seed + 1) * 0.5; c = som.thump(seed + 2) * 0.9
    return np.concatenate([a, np.zeros(max(0, int(0.18 * SR) - len(a))), b, np.zeros(max(0, int(0.32 * SR) - len(b))), c])


def porta(seed=201):
    """Clique macio da porta: tick grave + ressonância curta de 300 Hz."""
    n = int(0.22 * SR); t = np.arange(n) / SR
    y = np.sin(2 * np.pi * 300 * t) * np.exp(-t / 0.04) * 0.5
    tk = som.tick(seed) * 0.6
    y[:len(tk)] += tk[:n]
    return som._onepole_lp(y, 2500) * 1.4


def risco(seed=211):
    """Caneta do telestrador riscando (a linha tracejada): ruído 1,5–4 kHz que sobe, 0,35 s."""
    n = int(0.35 * SR); t = np.arange(n) / SR
    x = _banda_fft(np.random.default_rng(seed).standard_normal(n), 1500, 4000)
    return x * np.sin(np.pi * t / 0.35) * (0.4 + 0.6 * t / 0.35) * 0.5


def termo_sobe(seed=221):
    """Tick ascendente (a coluna do termômetro subindo)."""
    n = int(0.3 * SR); t = np.arange(n) / SR
    f = 700 + 1400 * t / 0.3
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.sin(np.pi * t / 0.3) * 0.32


SFX = dict(som.SFX)
SFX.update({"apito": apito, "apito_final": apito_final, "rebobinar": rebobinar,
            "rebobinar_curto": lambda: rebobinar(33, 0.3), "bipe": bipe, "bipe_alto": bipe_alto,
            "obturador": obturador, "fofo": fofo, "tv_desliga": tv_desliga, "passarinho": passarinho, "pano": pano,
            "passos": passos_desiguais, "porta": porta, "risco": risco, "termo": termo_sobe})


def _media_movel(x, w):
    n = len(x)
    c = np.concatenate([[0.0], np.cumsum(x)])
    i = np.arange(n)
    lo = np.clip(i - w // 2, 0, n); hi = np.clip(i + (w - 1) // 2 + 1, 0, n)
    return (c[hi] - c[lo]) / w


def mixar(voz, dur, eventos, ganho_trilha=0.40, baixas=()):
    """Cópia do som.mixar do piloto + `baixas`: janelas em que a trilha cai a ~15% (CHECANDO). (socorros)"""
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


def baixas_trilha(T):
    return [(T[pd + "_fim"] + 0.05, T[vd]) for pd, vd, _, _ in VEREDITOS]


def sons(T):
    # grilos (só nas cenas de noite; param nos congelamentos)
    trechos = ((0.0, T["pode1"]), (T["validado"], T["e2"]), (T["e2"], T["pode2"]), (T["noite3"], T["pode3"]),
               (T["anulado2"], T["leve"]))
    for i, (a, b) in enumerate(trechos):
        SFX["grilos%d" % i] = (lambda d=max(0.2, b - a), s=161 + i: grilos(d, s))
    ev = [(a, "grilos%d" % i, 0.10 if i != 2 else 0.05) for i, (a, b) in enumerate(trechos)]
    ev += [(0.0, "apito", 0.85), (T["chama"] + 0.02, "pop", 0.25), (T["var"] - 0.02, "rebobinar", 0.7)]
    for pd, vd, _, _ in VEREDITOS:
        ev.append((T[pd] - 0.01, "obturador", 0.85))
        t0 = T[pd + "_fim"] + 0.07
        ev += [(t0, "bipe", 0.75), (t0 + 0.22, "bipe", 0.75), (t0 + 0.44, "bipe_alto", 0.8)]
        ev.append((T[vd] - 0.02, "thump", 0.9))
    ev += [(T["validado"] - 0.26, "apito", 0.45)]                     # apito curto no silêncio antes do VALIDADO
    # lance 1 — a crise da noite
    ev += [(T["dor1"] + 0.08, "pop", 0.2), (T["dor1"] + 0.2, "pop", 0.16), (T["pernas"] - 0.02, "tick", 0.45)]
    ev += [(T["noite1"] + 0.02, "grilos0", 0.07), (T["massagem1"] - 0.12, "whoosh", 0.22)]
    ev += [(T["massagem2"] + 0.02, "fofo", 0.32), (T["compressa"] + 0.2, "pano", 0.55)]
    ev += [(T["costumam"] - 0.02, "ping", 0.32), (T["calma"] + 0.05, "shimmer", 0.18)]
    # lance 2 — frescura (noite | manhã)
    ev += [(T["e2"] - 0.06, "rebobinar_curto", 0.4), (T["e2"] + 0.3, "passarinho", 0.18), (T["e2"] + 0.95, "passarinho", 0.13)]
    ev += [(T["frescura"] - 0.04, "risco", 0.5), (T["dor2"] + 0.0, "ping", 0.3), (T["some"] - 0.05, "whoosh", 0.3),
           (T["manha"] + 0.0, "ping", 0.3)]
    # lance 3 — um lado só (sem som cômico)
    ev += [(T["noite3"], "rebobinar_curto", 0.38), (T["noite3"] + 0.02, "whoosh", 0.25)]
    ev += [(T["dor3"] + 0.05, "pop", 0.22), (T["lado"] - 0.02, "tick", 0.45), (T["inchaco"] - 0.02, "tick", 0.42),
           (T["febre1"] - 0.02, "termo", 0.5), (T["manqueira1"] + 0.02, "passos", 0.45),
           (T["chamar2"] - 0.06, "whoosh", 0.32), (T["crescimento2"] - 0.06, "risco", 0.45)]
    ev += [(T["leve"] - 0.03, "whoosh", 0.3), (T["leve"] + 0.12, "passos", 0.32), (T["avaliar"] + 0.05, "porta", 0.5),
           (T["avaliar"] + 0.32, "ping", 0.32)]
    # apito final, TV desligando, fecho, CTA
    ev += [(T["apito_f"], "apito_final", 0.6), (T["off"] + 0.02, "tv_desliga", 0.75)]
    ev += [(T["febre2"] + 0.02, "pop", 0.28), (T["manqueira2"] + 0.02, "passos", 0.35),
           (T["juntas"] + 0.18, "thump", 0.35), (T["mesmo"] - 0.02, "shimmer", 0.35), (T["manda"] + 0.05, "whoosh", 0.5)]
    return ev


def tempos_previa(T):
    return [0.0, T["var"] + 0.25, T["dor1"] + 0.2, T["pernas"] + 0.3, T["noite1"] + 0.2, T["massagem1"] + 0.4,
            T["pode1"] + 0.55, T["validado"] + 0.25, T["massagem2"] + 0.3, T["compressa"] + 0.25,
            T["morna"] + 0.3, T["costumam"] + 0.35, T["fica"] + 0.7, T["crianca"] + 0.6, T["calma"] + 0.3,
            T["e2"] + 0.15, T["e2"] + 0.4, T["frescura"] + 0.5, T["pode2"] + 0.6, T["anulado1"] + 0.3, T["dor2"] + 0.4,
            T["real"] + 0.2, T["some"] + 0.45, T["manha"] + 0.35,
            T["noite3"] + 0.2, T["noite3"] + 0.5, T["lado"] + 0.3, T["inchaco"] + 0.45, T["febre1"] + 0.45,
            T["manqueira1"] + 0.6, T["chamar2"] + 0.3, T["pode3"] + 0.6, T["anulado2"] + 0.3, T["trate"] + 0.35,
            T["leve"] + 0.2, T["avaliar"] + 0.5, T["off"] - 0.05, T["off"] + 0.15,
            T["febre2"] + 0.35, T["manqueira2"] + 0.35, T["juntas"] + 0.6, T["mesmo"] + 0.6,
            T["manda"] + 0.5, T["manda"] + 1.6]


# ================================================================== render (cópia do piloto + os vãos deste episódio)
VAO_CHECANDO = 0.86                   # fim de "pode?" -> veredito: ~0,3 s de congelar + ~0,55 s de CHECANDO
VAOS_EXTRA = (("dor", 3, 0.45),       # a divisória fecha e volta a noite do LANCE 3 (o sol desce)
              ("febre", 2, 1.10))     # o JEITO CERTO (porta com o estetoscópio) respira + apito final + TV desligando
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
    T["noite3"] = T["manha_fim"] + 0.12          # a divisória fecha no vão antes de "Dor" (LANCE 3)
    T["apito_f"] = T["febre2"] - 1.0             # apito final (curto, longo) no silêncio
    T["off"] = T["febre2"] - 0.48                # a TV desliga no sopro longo
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
        som.gravar_wav(wav, mixar(voz_c, T["total"], sons_fn(T), baixas=baixas_trilha(T)))
        codificar(quadro_t, T["total"], wav, mp4)
        return mp4, T["total"]
    return render


render = fazer_render_var(quadro, ANCORAS, sons, tempos_previa, respiro_cta=0.8)
