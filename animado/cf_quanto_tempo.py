# -*- coding: utf-8 -*-
"""COMO FUNCIONA — "Quanto tempo com o fixador?" (o tempo das fases no alongamento ósseo).

Mesmo estilo e mesmas peças do cf_alongamento (osso marfim, osso novo dourado, anel/fio/haste do
fixador, carimbo, brilhos, legenda karaokê, CTA com aviãozinho). Aqui a estrela é a RÉGUA DO TEMPO
(uma barra de progresso, sem número e sem data); o osso com o fixador, menor, fica em cima dela e
reage às mesmas palavras. Cada acontecimento é disparado pela palavra falada:
  * capa (t=0): gancho + "NO ALONGAMENTO" (escopo: a conta das fases vale para o alongamento, não
    para todo fixador — correção do verificador); osso com o corte fino e 3 anéis; trilho vazio com
    o reloginho no começo. "fixador": os anéis brilham (som de metal);
  * "alguns"/"pausa": o 1º trecho enche curto, cinza-azulado, com o ícone de pausa; no osso, o corte
    fica parado (halo azul), nada se mexe;
  * "depois"/"milímetro"/"dia": o 2º trecho avança em tiquinhos iguais, um clique por tique, e no
    osso as partes se afastam no mesmo passo, a fenda enchendo de osso novo dourado; cartão 1 MM;
  * "quanto"/"correção"/"mais": a fita graduada ao lado da fenda se estica e, no mesmo ritmo, o
    trecho do alongamento fica mais comprido (QUANTO MAIOR / A CORREÇÃO -> MAIS DIAS; no "mais" um
    fio dourado sai da base da fita e chega na pílula MAIS DIAS: causa -> efeito);
  * "curta": carimbo A PARTE CURTA, a régua encolhe um pouco;
  * "longa"/"consolidação": a câmera recua e o trecho previsto da consolidação desenrola (contorno
    tracejado, bem mais comprido, mas DENTRO do quadro — correção do verificador); o preenchimento
    dourado->marfim anda nele num passo constante, devagar;
  * "endurece": o osso novo vira marfim e ganha textura; "carga": seta de peso pousa no osso, que
    segura firme;
  * "não"/"apressar": botão de avançar rápido surge sobre a régua, é apertado, fica cinza e treme;
    a régua não acelera;
  * "idade"/"saúde"/"alimentação"/"cigarro": etiquetas entram e a PONTA do trecho previsto dá um
    vaivém simétrico (+meio / -um / +meio, volta ao zero), o MESMO para as quatro (sem direção: a
    fala diz só que muda a velocidade — correção do verificador); "velocidade": a ponta vira
    elástica, sem ponto fixo;
  * "aparelho"/"sai": os anéis sobem e somem; bandeirinha APARELHO SAI fincada no fim da consolidação;
  * "ganhando"/"resistência"/"meses": a régua NÃO termina: um tracejado continua depois da bandeira
    e a hachura do osso novo fica mais densa;
  * "prazo": o fim da régua se dissolve num degradê (sem marca de chegada) + carimbo;
  * "raio": pontos de controle acendem um a um na régua — só acendem, sem check nem selo (correção
    do verificador); uma chave fina embaixo deles com RAIO-X dá nome aos pontos (a frase inteira
    fica só na legenda); NENHUMA imagem de exame;
  * respiro antes da CTA: o osso encolhe e sai (sempre opaco) e a régua sobe como resumo (curta x
    longa, por meses).
Todo texto desenhado está em ep["tela"] (o render recusa o vídeo se não estiver).
"""
import math

import skia

from .cf_comum import capa, carimbo, fazer_render, interface, selo_como_funciona
from .cf_alongamento import (CX, F_BLACK, F_SEMI, HASTE, NOVO, NOVO_G, OSSO_B, OSSO_C, OURO, W,
                             Y_BASE, Y_CORTE, Y_TOPO, C, anel, brilhos, clamp, desenha_osso, desenha_regenerado,
                             e_back, e_in_back, e_inout, e_out, fios, fundo, haste, larg_texto, lerp, lerpc, paint,
                             path_osso_inf, path_osso_sup, porca, prog, texto)

ANCORAS = {
    "quanto": ("quanto", 1, False), "fixador": ("fixador", 1, False), "alongamento": ("alongamento", 1, False),
    "primeiro": ("primeiro", 1, False), "alguns": ("alguns", 1, False), "pausa": ("pausa", 1, False),
    "depois": ("depois", 1, False), "milimetro": ("milímetro", 1, False), "dia": ("dia", 1, False),
    "quanto2": ("quanto", 2, False), "correcao": ("correção", 1, False), "mais": ("mais", 1, False),
    "dias": ("dias", 2, False), "curta": ("curta", 1, False), "longa": ("longa", 1, False),
    "consolidacao": ("consolidação", 1, False), "endurece": ("endurece", 1, False),
    "aguentar": ("aguentar", 1, False), "carga": ("carga", 1, False), "nao": ("não", 1, False),
    "apressar": ("apressar", 1, False), "idade": ("idade", 1, False), "saude": ("saúde", 1, False),
    "alimentacao": ("alimentação", 1, False), "cigarro": ("cigarro", 1, False),
    "velocidade": ("velocidade", 1, False), "aparelho": ("aparelho", 1, False), "sai": ("sai", 1, False),
    "ganhando": ("ganhando", 1, False), "resistencia": ("resistência", 1, False), "meses": ("meses", 1, False),
    "prazo": ("prazo", 1, False), "raio": ("raio", 1, True), "mostra": ("mostra", 1, False),
    "caminho": ("caminho", 1, False), "manda": ("manda", 1, False),
}
DESTAQUE = {"fixador", "alongamento", "pausa", "milímetro", "dia", "correção", "curta", "longa", "consolidação",
            "endurece", "carga", "apressar", "velocidade", "sai", "resistência", "meses", "prazo", "raio-x",
            "caminho"}

# ------------------------------------------------------------------ paleta e textos de tela
AZUL = "#9CC9FF"
CARTAO = "#0B1824"
PAUSA_COR, PAUSA_ESC = "#8AA6C1", "#5F7C98"
CINZA = "#6B7A89"

T_ESCOPO = "NO ALONGAMENTO"
T_PAUSA, T_ALGUNS = "PAUSA", "alguns dias"
T_ALONG = "ALONGAMENTO"
T_1MM, T_POR_DIA = "1 MM", "por dia"
T_QUANTO, T_CORRECAO, T_MAIS = "QUANTO MAIOR", "A CORREÇÃO", "MAIS DIAS"
T_CURTA, T_LONGA, T_CONSOL = "A PARTE CURTA", "A PARTE LONGA", "CONSOLIDAÇÃO"
T_CARGA = "AGUENTAR CARGA"
T_APRESSAR = "NÃO DÁ PRA APRESSAR"
FATORES = (("idade", "IDADE"), ("saude", "SAÚDE"), ("alimentacao", "ALIMENTAÇÃO"), ("cigarro", "CIGARRO"))
T_VELOC = "MUDAM A VELOCIDADE"
T_SAI = "APARELHO SAI"
T_GANHANDO, T_RESIST = "GANHANDO", "RESISTÊNCIA"
T_MESES = "por meses"
T_PRAZO = "PRAZO ÚNICO NÃO EXISTE"
T_RAIO = "RAIO-X"

# ------------------------------------------------------------------ geometria
S_OSSO = 0.53                # o osso é menor que no piloto: a estrela aqui é a régua
BX, BY0, CAPA_DY = 540, 335, 70
GAP_U = 45                   # px de mundo de osso novo por unidade de régua do alongamento
FENDA = 6
RY0, RY_RESUMO, RY_CTA = 1015, 700, 385   # régua: meio da tela, resumo no respiro, acima da CTA
TR_X0, TR_X1 = 122, 1012     # trilho
U0 = TR_X0 + 9               # x da origem do tempo
HH = 20                      # meia-altura do preenchimento
TR_H = 29                    # meia-altura do trilho
TICK = 0.2                   # tamanho de um tique (unidade esquemática: NÃO vai para a tela)
L_A, L_B = 1.6, 4.0          # alongamento antes e depois de "correção"
N_A, N_B = 8, 12
C0 = 1 + L_B                 # onde começa a consolidação
C_FIM, C_PREV = 11.0, 11.2   # fim da consolidação (bandeira) e centro do vaivém da ponta prevista
K_FIM = 38.0                 # escala final (px por unidade): tudo cabe no quadro
MARCOS = (2.5, 5.5, 8.5, 11.5, 14.5, 17.5, 20.5)   # pontos de controle (sem número)


# ------------------------------------------------------------------ tempo -> estado
def t_capa(T):
    return T["primeiro"] + 0.2


def escala(t, T):
    k = 130.0
    k = lerp(k, 112.0, e_inout(prog(t, T["curta"], T["curta"] + 0.45)))
    return lerp(k, K_FIM, recuo(t, T))


def recuo(t, T):
    return e_inout(prog(t, T["longa"] - 0.05, T["consolidacao"] + 0.25))


def abre_prevista(t, T):
    return e_out(prog(t, T["consolidacao"] - 0.05, T["consolidacao"] + 0.95))


def _passos(t, t0, t1, n):
    """Avanço em passinhos (anda e para): um tique por intervalo."""
    p = prog(t, t0, t1) * n
    i = math.floor(p)
    if i >= n:
        return float(n)
    return i + e_out(clamp((p - i) / 0.4))


def janelas(T):
    return (T["depois"] + 0.25, T["quanto2"] - 0.15), (T["correcao"] - 0.05, T["dias"] + 0.35)


def pausa_len(t, T):
    return e_inout(prog(t, T["alguns"], T["pausa"] + 0.25))


def along_len(t, T):
    (a0, a1), (b0, b1) = janelas(T)
    return TICK * (_passos(t, a0, a1, N_A) + _passos(t, b0, b1, N_B))


def prevista(t, T):
    """Comprimento previsto da consolidação (contorno tracejado), com o vaivém da ponta."""
    abre = abre_prevista(t, T)
    assenta = e_inout(prog(t, T["aparelho"], T["sai"]))
    w = 0.0
    for chave, _ in FATORES:                       # o MESMO vaivém para as quatro (sem direção)
        k = t - T[chave]
        # envelope simétrico de meia onda: +0,5 / -1,0 / +0,5 u e volta ao zero; cabe em 0,6 s para
        # não somar com o vaivém do fator seguinte (os quatro vêm a ~0,63-0,85 s um do outro)
        if 0 < k < 0.6:
            w += 1.15 * math.sin(2 * math.pi * k / 0.4) * math.sin(math.pi * k / 0.6)
    amp = 0.6 * prog(t, T["velocidade"], T["velocidade"] + 0.35) * (1 - assenta)
    w += amp * math.sin(2 * math.pi * (t - T["velocidade"]) / 1.0)
    return abre * (lerp(C_PREV, C_FIM, assenta) + w * (1 - assenta))


def consolidado(t, T):
    """Preenchimento da consolidação: passo constante (não acelera no botão)."""
    return C_FIM * prog(t, T["consolidacao"] + 0.3, T["sai"])


def tracejado_len(t, T):
    return (2.5 * e_inout(prog(t, T["resistencia"] - 0.15, T["meses"] + 0.1))
            + 3.5 * e_inout(prog(t, T["meses"] + 0.1, T["prazo"] + 1.0)))


def altura_regua(t, T):
    y = lerp(RY0, RY_RESUMO, e_inout(prog(t, T["caminho"] + 0.35, T["caminho"] + 1.15)))
    return lerp(y, RY_CTA, e_inout(prog(t, T["manda"] - 0.8, T["manda"] - 0.1)))


def tremor(t, T):
    d = 0.0
    for t0, f in ((T["curta"] + 0.02, 7), (T["prazo"] + 0.02, 6)):
        k = t - t0
        if 0 <= k < 0.35:
            d += f * math.sin(k * 70) * (1 - k / 0.35)
    return d


def topo_osso(t, T):
    return BY0 + CAPA_DY * (1 - e_inout(prog(t, t_capa(T), t_capa(T) + 0.8)))


def estado(t, T):
    e = dict(k=escala(t, T), ry=altura_regua(t, T), P=pausa_len(t, T), L=along_len(t, T),
             G=prevista(t, T), F=consolidado(t, T), D=tracejado_len(t, T), by=topo_osso(t, T))
    e["X"] = lambda u, k=e["k"], d=tremor(t, T): U0 + d + u * k
    e["G"] = min(e["G"], (TR_X1 - 16 - U0) / e["k"] - C0)     # nunca passa do fim do trilho
    return e


# ------------------------------------------------------------------ peças de desenho
def caixa(cv, x0, y0, x1, y1, cor, a, r=16, fundo_a=225, borda=3):
    rr = skia.RRect.MakeRectXY(skia.Rect(x0, y0, x1, y1), r, r)
    cv.drawRRect(rr, paint(CARTAO, int(fundo_a * a)))
    cv.drawRRect(rr, paint(cor, int(255 * a), "stroke", borda))


def rotulo_txt(cv, s, x, y, tam, cor, a, fonte=F_BLACK, centro=True, dy=10):
    """Texto solto com contorno escuro, entrando de baixo."""
    if a <= 0:
        return
    texto(cv, s, x, y + dy * (1 - e_out(clamp(a))), fonte, tam, cor, int(255 * clamp(a)), centro=centro, contorno=7)


def pilula(cv, s, x, y, tam, cor, a, esc=1.0, cor_txt=None):
    """Chip centrado em x; y = linha de base do texto."""
    if a <= 0:
        return
    lw = larg_texto(s, F_BLACK, tam)
    cv.save(); cv.translate(x, y); cv.scale(esc, esc)
    caixa(cv, -lw / 2 - 22, -tam * 1.02, lw / 2 + 22, tam * 0.36, cor, a, r=tam * 0.6)
    texto(cv, s, 0, 0, F_BLACK, tam, cor_txt or cor, int(255 * a))
    cv.restore()


def relogio(cv, x, y, ang, a):
    cv.drawCircle(x, y, 27, paint(CARTAO, int(225 * a)))
    cv.drawCircle(x, y, 27, paint("#FFFFFF", int(220 * a), "stroke", 4))
    for i in range(4):
        q = i * math.pi / 2
        cv.drawLine(x + 19 * math.cos(q), y + 19 * math.sin(q), x + 23 * math.cos(q), y + 23 * math.sin(q),
                    paint("#FFFFFF", int(170 * a), "stroke", 2.5))
    cv.drawLine(x, y, x + 9 * math.cos(ang * 0.25 - math.pi / 2), y + 9 * math.sin(ang * 0.25 - math.pi / 2),
                paint("#FFFFFF", int(200 * a), "stroke", 4))
    cv.drawLine(x, y, x + 17 * math.cos(ang - math.pi / 2), y + 17 * math.sin(ang - math.pi / 2),
                paint(OURO, int(255 * a), "stroke", 3.5))
    cv.drawCircle(x, y, 3.5, paint(OURO, int(255 * a)))


def icone_pausa(cv, x, y, esc, a):
    if a <= 0:
        return
    for dx in (-6, 6):
        cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(x + dx * esc - 3.2 * esc, y - 10 * esc, x + dx * esc + 3.2 * esc,
                                                     y + 10 * esc), 2, 2), paint("#FFFFFF", int(240 * a)))


def bloco(cv, x0, x1, y0, y1, cor, a, r=8, shader=None):
    if x1 - x0 < 1:
        return
    rr = skia.RRect.MakeRectXY(skia.Rect(x0, y0, x1, y1), min(r, (x1 - x0) / 2), r)
    cv.drawRRect(rr, paint(cor, int(255 * a), shader=shader))


def botao_ff(cv, x, y, cor, a, esc, dx):
    """Botão de avançar rápido (dois triângulos), sem texto."""
    if a <= 0:
        return
    cv.save(); cv.translate(x + dx, y); cv.scale(esc, esc)
    cv.drawCircle(0, 0, 58, paint(cor, int(70 * a), blur=14))
    cv.drawCircle(0, 0, 46, paint(CARTAO, int(240 * a)))
    cv.drawCircle(0, 0, 46, paint(cor, int(255 * a), "stroke", 5))
    for off in (-11, 10):
        p = skia.Path(); p.moveTo(off - 12, -16); p.lineTo(off + 13, 0); p.lineTo(off - 12, 16); p.close()
        cv.drawPath(p, paint(cor, int(255 * a)))
    cv.restore()


def seta_peso(cv, x, y_ponta, a, esmaga):
    """Seta grossa para baixo (peso), sem texto."""
    if a <= 0:
        return
    cv.save(); cv.translate(x, y_ponta); cv.scale(1 + 0.06 * esmaga, 1 - 0.1 * esmaga)
    p = skia.Path()
    p.moveTo(-22, -96); p.lineTo(22, -96); p.lineTo(22, -54); p.lineTo(52, -54); p.lineTo(0, 0)
    p.lineTo(-52, -54); p.lineTo(-22, -54); p.close()
    cv.drawPath(p, paint("#000000", int(90 * a), blur=10))
    sh = skia.GradientShader.MakeLinear([skia.Point(-52, 0), skia.Point(52, 0)],
                                        [C("#FFFFFF", int(255 * a)), C("#C9D6E2", int(255 * a))])
    cv.drawPath(p, paint("#FFFFFF", 255, shader=sh))
    cv.drawPath(p, paint("#5E7186", int(220 * a), "stroke", 3))
    cv.restore()


# ícones das etiquetas (sem texto)
def ic_ampulheta(cv, x, y, s, a):
    p = skia.Path()
    p.moveTo(x - 0.7 * s, y - s); p.lineTo(x + 0.7 * s, y - s); p.lineTo(x + 0.1 * s, y)
    p.lineTo(x + 0.7 * s, y + s); p.lineTo(x - 0.7 * s, y + s); p.lineTo(x - 0.1 * s, y); p.close()
    areia = skia.Path(); areia.moveTo(x - 0.45 * s, y + 0.82 * s); areia.lineTo(x + 0.45 * s, y + 0.82 * s)
    areia.lineTo(x, y + 0.3 * s); areia.close()
    cv.drawPath(areia, paint(OURO, int(255 * a)))
    cv.drawPath(p, paint("#FFFFFF", int(240 * a), "stroke", 3))
    for yy in (y - s, y + s):
        cv.drawLine(x - 0.9 * s, yy, x + 0.9 * s, yy, paint("#FFFFFF", int(240 * a), "stroke", 4))


def ic_coracao(cv, x, y, s, a):
    p = skia.Path(); p.moveTo(x, y + 0.85 * s)
    p.cubicTo(x - 1.35 * s, y - 0.05 * s, x - 0.75 * s, y - 1.2 * s, x, y - 0.45 * s)
    p.cubicTo(x + 0.75 * s, y - 1.2 * s, x + 1.35 * s, y - 0.05 * s, x, y + 0.85 * s); p.close()
    cv.drawPath(p, paint("#FF8A93", int(255 * a)))


def ic_prato(cv, x, y, s, a):
    cv.drawCircle(x, y, 0.72 * s, paint("#FFFFFF", int(235 * a), "stroke", 3))
    cv.drawCircle(x, y, 0.42 * s, paint("#FFFFFF", int(140 * a), "stroke", 2))
    xf = x - 1.18 * s                                   # garfo
    cv.drawLine(xf, y - 0.2 * s, xf, y + 0.9 * s, paint("#FFFFFF", int(235 * a), "stroke", 3))
    for d in (-0.16, 0, 0.16):
        cv.drawLine(xf + d * s, y - 0.9 * s, xf + d * s, y - 0.3 * s, paint("#FFFFFF", int(235 * a), "stroke", 2))
    cv.drawLine(xf - 0.16 * s, y - 0.3 * s, xf + 0.16 * s, y - 0.3 * s, paint("#FFFFFF", int(235 * a), "stroke", 2))
    xk = x + 1.18 * s                                   # faca
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(xk - 0.13 * s, y - 0.9 * s, xk + 0.13 * s, y + 0.9 * s), 3, 3),
                 paint("#FFFFFF", int(235 * a)))


def ic_cigarro(cv, x, y, s, a):
    """Bastão branco com filtro laranja; sem fumaça, sem brasa, sem marca."""
    cv.save(); cv.translate(x, y); cv.rotate(-18)
    L, R = 2.3 * s, 0.26 * s
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(-L / 2, -R, L / 2, R), 3, 3), paint("#F4F6F8", int(255 * a)))
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(-L / 2, -R, -L / 2 + 0.7 * s, R), 3, 3), paint("#E8913A", int(255 * a)))
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(-L / 2, -R, L / 2, R), 3, 3), paint("#5E7186", int(160 * a), "stroke", 1.5))
    cv.restore()


ICONES = {"idade": ic_ampulheta, "saude": ic_coracao, "alimentacao": ic_prato, "cigarro": ic_cigarro}


def fita(cv, x, y0, y1, a, brilho):
    """Fita de medir graduada (sem número) ao lado da fenda."""
    if a <= 0 or y1 - y0 < 2:
        return
    w = 26
    if brilho > 0:
        cv.drawRect(skia.Rect(x - w, y0 - 10, x + w, y1 + 10), paint(NOVO_G, int(110 * brilho * a), blur=14))
    cv.drawRect(skia.Rect(x - w / 2, y0, x + w / 2, y1), paint("#F3DE9A", int(245 * a)))
    yy, i = y0 + 6, 0
    while yy < y1 - 2:
        cv.drawLine(x - w / 2, yy, x - w / 2 + (11 if i % 2 == 0 else 6), yy, paint("#8A6512", int(230 * a), "stroke", 2))
        yy += 7; i += 1
    cv.drawRect(skia.Rect(x - w / 2, y0, x + w / 2, y1), paint(OURO, int(255 * a), "stroke", 2.5))
    for yv in (y0, y1):
        cv.drawLine(x - 22, yv, x + 22, yv, paint("#FFFFFF", int(240 * a), "stroke", 3.5))


# ------------------------------------------------------------------ osso + fixador (mundo, escala S_OSSO)
def tela_osso(e, x, y):
    return BX + (x - CX) * S_OSSO, e["by"] + (y - Y_TOPO) * S_OSSO


def hachura(cv, y0, y1, h):
    """Textura do osso novo endurecendo: trama clara, no tom do próprio osso (marfim escuro, pouco
    alfa), para o regenerado consolidado ficar quase igual ao osso, como no cf_alongamento — e não
    virar uma tela escura que lembre enxerto ou implante."""
    if h <= 0 or y1 - y0 < 2:
        return
    x0, x1 = CX - HASTE / 2 + 2, CX + HASTE / 2 - 2
    cv.save(); cv.clipRect(skia.Rect(x0, y0, x1, y1))
    alt = y1 - y0
    for fam, lim in enumerate((0.0, 0.45)):
        a = clamp((h - lim) / 0.3)
        if a <= 0:
            continue
        x = x0 - alt
        while x < x1 + alt:
            if fam == 1:
                cv.drawLine(x, y1, x + alt, y0, paint(OSSO_B, int(80 * a), "stroke", 2.5))
            else:
                cv.drawLine(x, y0, x + alt, y1, paint(OSSO_B, int(80 * a), "stroke", 2.5))
            x += 22
    cv.restore()


def osso(cv, t, T, e):
    gap = GAP_U * e["L"]
    yc_inf = Y_CORTE + FENDA + gap; yb = Y_BASE + FENDA + gap
    # saída do osso para o resumo: ele ENCOLHE e some (pop ao contrário), sempre opaco — nada de
    # silhueta translúcida no quadro bem na hora em que se fala "raio-X"; o alfa só cai quando ele
    # já é um pontinho
    s_sai = prog(t, T["caminho"] + 0.2, T["caminho"] + 0.5)
    esc_sai = 1 - e_in_back(s_sai)
    a_osso = 1 - prog(s_sai, 0.8, 1.0)
    if a_osso <= 0 or esc_sai <= 0.01:
        return
    if a_osso < 1:
        cv.saveLayerAlpha(None, int(255 * a_osso))
    cv.save()
    if s_sai > 0:
        cy = e["by"] + (yb - Y_TOPO) / 2 * S_OSSO
        cv.translate(BX, cy); cv.scale(esc_sai, esc_sai); cv.translate(-BX, -cy)
    cv.translate(BX, e["by"]); cv.scale(S_OSSO, S_OSSO); cv.translate(-CX, -Y_TOPO)

    # o fixador sobe e some no "aparelho sai" (sem chegar ao selo COMO FUNCIONA)
    saida = prog(t, T["aparelho"], T["sai"] + 0.35)
    dy_fix = -300 * saida * saida
    a_fix = 1 - prog(t, T["sai"] - 0.2, T["sai"] + 0.2)
    y_an = [Y_TOPO + 95 + dy_fix, Y_CORTE - 78 + dy_fix, yb - 165 + dy_fix]

    for y in y_an:
        anel(cv, y, 0, a_fix, "tras")

    desenha_osso(cv, Y_CORTE, yc_inf, yb)

    # pausa: o corte parado, com halo azul (nada se mexe)
    a_halo = prog(t, T["alguns"], T["alguns"] + 0.3) * (1 - prog(t, T["depois"] + 0.1, T["depois"] + 0.5))
    if a_halo > 0:
        pulso = 0.75 + 0.25 * math.sin(t * 5)
        cv.drawRect(skia.Rect(CX - 90, Y_CORTE - 10, CX + 90, Y_CORTE + FENDA + 10),
                    paint(AZUL, int(170 * a_halo * pulso), blur=12))

    # osso novo na fenda: dourado -> marfim ("endurece") -> hachura mais densa ("resistência")
    if gap > 1.5:
        dens = clamp(gap / 50)
        crescendo = 1.0 if (janelas(T)[0][0] <= t <= janelas(T)[1][1]) else 0.0
        brilho = max(0.35 * dens * crescendo, prog(t, T["milimetro"] - 0.1, T["milimetro"] + 0.3)
                     * (1 - prog(t, T["curta"], T["curta"] + 0.8)))
        duro = e_inout(prog(t, T["endurece"], T["endurece"] + 1.6))
        y0, y1 = Y_CORTE + FENDA * 0.5, yc_inf - FENDA * 0.5
        desenha_regenerado(cv, y0, y1, dens, brilho, duro, t)
        h = 0.4 * e_inout(prog(t, T["endurece"] + 0.3, T["endurece"] + 1.8)) \
            + 0.6 * e_inout(prog(t, T["resistencia"] - 0.2, T["meses"] + 0.9))
        hachura(cv, y0, y1, h)
        if t > T["ganhando"]:                          # contorno firme acendendo devagar
            a = prog(t, T["ganhando"], T["meses"] + 0.6) * (1 - prog(t, T["prazo"], T["prazo"] + 1.0))
            cv.drawRect(skia.Rect(CX - HASTE / 2, y0, CX + HASTE / 2, y1), paint(OURO, int(200 * a), "stroke", 5))

    # carga: o osso segura firme (contorno acende, sem vergar)
    k = t - (T["carga"] + 0.05)
    if 0 <= k < 0.9:
        a = (1 - k / 0.9)
        for pth in (path_osso_sup(Y_TOPO, Y_CORTE), path_osso_inf(yc_inf, yb)):
            cv.drawPath(pth, paint(OURO, int(160 * a), "stroke", 14, blur=8))
            cv.drawPath(pth, paint(OURO, int(255 * a), "stroke", 4))

    # fixador (frente)
    for i, y in enumerate(y_an):
        fios(cv, y, 1.0, a_fix)
    for sx in (-1, 1):
        x = CX + sx * 204
        haste(cv, x, y_an[0], y_an[1], a_fix)
        haste(cv, x, y_an[1], y_an[2], a_fix, rosca=True, fase=e["L"] * 22)
        porca(cv, x, y_an[1] + 22, e["L"] * 450 + sx * 15, a_fix)
        porca(cv, x, y_an[2] - 22, -e["L"] * 450, a_fix)
    for y in y_an:
        anel(cv, y, 0, a_fix, "frente")
    # "fixador": um brilho corre pelos anéis
    for i, y in enumerate(y_an):
        ph = prog(t, T["fixador"] + 0.1 * i, T["fixador"] + 0.1 * i + 0.5)
        if 0 < ph < 1:
            cv.drawArc(skia.Rect(CX - 232, y - 46, CX + 232, y + 46), 180 * ph - 25, 50, False,
                       paint("#FFFFFF", int(255 * math.sin(math.pi * ph)), "stroke", 10))
    cv.restore()
    if a_osso < 1:
        cv.restore()


# ------------------------------------------------------------------ régua do tempo
def regua(cv, t, T, e):
    ry, k, X = e["ry"], e["k"], e["X"]
    cv.saveLayer(skia.Rect(0, ry - 160, W, ry + 70), None)

    tr = skia.RRect.MakeRectXY(skia.Rect(TR_X0, ry - TR_H, TR_X1, ry + TR_H), TR_H, TR_H)
    cv.drawRect(skia.Rect(TR_X0, ry - TR_H, TR_X1, ry + TR_H), paint("#000000", 90, blur=16))
    cv.drawRRect(tr, paint(CARTAO, 190)); cv.drawRRect(tr, paint("#FFFFFF", 75, "stroke", 2.5))
    y0, y1 = ry - HH, ry + HH
    # divisas entre as fases, embaixo do trilho (sem número)
    for u, t_on in ((1, T["depois"] + 0.25), (C0, T["longa"] + 0.3), (C0 + C_FIM, T["sai"] + 0.1)):
        a = prog(t, t_on, t_on + 0.3)
        if a > 0:
            cv.drawLine(X(u), ry + TR_H + 5, X(u), ry + TR_H + 18, paint("#FFFFFF", int(150 * a), "stroke", 3))

    # 1) pausa
    if e["P"] > 0.01:
        sh = skia.GradientShader.MakeLinear([skia.Point(0, y0), skia.Point(0, y1)], [C(PAUSA_COR), C(PAUSA_ESC)])
        bloco(cv, X(0), X(e["P"]) - 1.5, y0, y1, PAUSA_COR, 1, r=12, shader=sh)
        kp = t - T["pausa"]
        if kp > 0:
            icone_pausa(cv, (X(0) + X(1)) / 2, ry, lerp(1.6, 1.0, e_out(clamp(kp / 0.25))) * clamp(k / 70, 0.75, 1),
                        clamp(kp / 0.12))

    # 2) alongamento: tiquinhos iguais
    L = e["L"]
    if L > 0.005:
        larg = TICK * k; folga = clamp(0.12 * larg, 1.5, 3.0)
        n = math.ceil(L / TICK - 1e-6)
        sh = skia.GradientShader.MakeLinear([skia.Point(0, y0), skia.Point(0, y1)], [C("#FFD27A"), C(NOVO), C("#C98A1E")],
                                            [0.0, 0.45, 1.0])
        for i in range(n):
            u0 = 1 + i * TICK; u1 = min(1 + L, u0 + TICK)
            bloco(cv, X(u0) + folga / 2, X(u1) - folga / 2, y0, y1, NOVO, 1, r=4, shader=sh)
        (a0, a1), (b0, b1) = janelas(T)
        if a0 <= t <= a1 + 0.2 or b0 <= t <= b1 + 0.2:
            cv.drawCircle(X(1 + L), ry, 30, paint(NOVO_G, 120, blur=14))

    # 3) consolidação: contorno previsto (tracejado) + preenchimento dourado -> marfim
    G = e["G"]
    if G > 0.02:
        r = skia.RRect.MakeRectXY(skia.Rect(X(C0) + 1.5, y0, X(C0 + G), y1), 8, 8)
        cv.drawRRect(r, paint(OSSO_C, 40))
        borda = paint(OSSO_C, 190, "stroke", 2.5)
        borda.setPathEffect(skia.DashPathEffect.Make([10, 7], 0))
        cv.drawRRect(r, borda)
        F = min(e["F"], G)
        if F > 0.01:
            sh = skia.GradientShader.MakeLinear([skia.Point(X(C0), 0), skia.Point(X(C0 + C_FIM), 0)],
                                                [C(NOVO), C("#F6D58E"), C(OSSO_C)], [0.0, 0.45, 1.0])
            bloco(cv, X(C0) + 1.5, X(C0 + F), y0, y1, NOVO, 1, r=8, shader=sh)
            cv.drawRect(skia.Rect(X(C0) + 2, y0 + 3, X(C0 + F) - 2, y0 + 8), paint("#FFFFFF", 70))
            if T["consolidacao"] + 0.3 < t < T["sai"]:
                cv.drawCircle(X(C0 + F), ry, 26, paint("#FFFFFF", 90, blur=12))
        # a ponta que não para num ponto fixo
        a_el = prog(t, T["idade"] - 0.1, T["idade"] + 0.2) * (1 - prog(t, T["aparelho"], T["sai"]))
        if a_el > 0:
            xe = X(C0 + G)
            cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(xe - 5, y0 - 8, xe + 5, y1 + 8), 4, 4), paint(OURO, int(255 * a_el)))
            cv.drawRect(skia.Rect(xe - 16, y0 - 14, xe + 16, y1 + 14), paint(NOVO_G, int(110 * a_el), blur=12))

    # 4) depois da retirada: tracejado que continua
    D = e["D"]
    if D > 0.05:
        p = paint(OSSO_C, 235, "stroke", 13)
        p.setPathEffect(skia.DashPathEffect.Make([20, 14], 0))
        cv.drawLine(X(C0 + C_FIM) + 14, ry, X(C0 + C_FIM + D), ry, p)

    # 5) raio-X: pontos de controle que só acendem (sem check, sem selo)
    a_m = prog(t, T["raio"] - 0.2, T["raio"]) * (1 - prog(t, T["caminho"] + 0.3, T["caminho"] + 0.7))
    if a_m > 0:
        for i, u in enumerate(MARCOS):
            x = X(u); t_on = T["raio"] + 0.05 + 0.17 * i
            cv.drawCircle(x, ry, 12, paint(CARTAO, int(235 * a_m)))
            cv.drawCircle(x, ry, 12, paint("#FFFFFF", int(150 * a_m), "stroke", 2.5))
            if t >= t_on:
                kk = t - t_on
                cv.drawCircle(x, ry, 34 - 12 * e_out(clamp(kk / 0.4)), paint(OURO, int(150 * a_m), blur=12))
                cv.drawCircle(x, ry, 12 * lerp(1.5, 1.0, e_out(clamp(kk / 0.25))), paint(OURO, int(255 * a_m)))
                cv.drawCircle(x, ry, 5, paint("#FFFFFF", int(255 * a_m)))

    # resumo: um brilho corre a régua inteira
    ks = prog(t, T["caminho"] + 1.3, T["caminho"] + 2.1)
    if 0 < ks < 1:
        xs = lerp(TR_X0 - 90, TR_X1 + 90, e_inout(ks))
        sh = skia.GradientShader.MakeLinear([skia.Point(xs - 80, 0), skia.Point(xs + 80, 0)],
                                            [C("#FFFFFF", 0), C("#FFFFFF", 140), C("#FFFFFF", 0)], [0.0, 0.5, 1.0])
        cv.drawRect(skia.Rect(TR_X0, y0, TR_X1, y1), paint("#FFFFFF", 255, shader=sh))

    # o fim se dissolve ("prazo"): máscara em degradê, nenhuma marca de chegada
    fx = lerp(TR_X1 + 60, 812, e_inout(prog(t, T["prazo"] - 0.1, T["prazo"] + 1.1)))
    masc = skia.Paint(AntiAlias=True)
    masc.setShader(skia.GradientShader.MakeLinear([skia.Point(fx, 0), skia.Point(fx + 200, 0)],
                                                  [skia.ColorSetARGB(255, 0, 0, 0), skia.ColorSetARGB(0, 0, 0, 0)]))
    masc.setBlendMode(skia.BlendMode.kDstIn)
    cv.drawRect(skia.Rect(0, ry - 160, W, ry + 70), masc)
    cv.restore()

    # reloginho no começo: o ponteiro anda com o tempo preenchido (não acelera)
    total = e["P"] + L + e["F"] + e["D"]
    relogio(cv, 70, ry, total * 2 * math.pi / 3.2, 1.0)


def bandeira(cv, t, T, e):
    k = t - (T["sai"] + 0.05)
    if k < 0:
        return
    ry = e["ry"]; x = e["X"](C0 + C_FIM)
    desce = e_back(clamp(k / 0.35))
    topo = ry - 135
    cv.save(); cv.translate(0, -60 * (1 - desce))
    a = clamp(k / 0.12)
    cv.drawLine(x, ry - 24, x, topo, paint("#E6EEF6", int(255 * a), "stroke", 5))
    cv.drawCircle(x, topo, 6, paint(OURO, int(255 * a)))
    abre = e_out(clamp((k - 0.2) / 0.35))
    if abre > 0:
        lw = larg_texto(T_SAI, F_BLACK, 30); w = (lw + 34) * abre
        p = skia.Path(); p.moveTo(x + 3, topo + 2)
        onda = 4 * math.sin(t * 4)
        p.lineTo(x + 3 + w, topo + 2 + onda); p.lineTo(x + 3 + w - 12 * abre, topo + 25 + onda)
        p.lineTo(x + 3 + w, topo + 48 + onda); p.lineTo(x + 3, topo + 48); p.close()
        cv.drawPath(p, paint("#000000", 80, blur=8))
        cv.drawPath(p, paint(OURO, int(255 * a)))
        if abre > 0.95:
            texto(cv, T_SAI, x + 18, topo + 36 + onda * 0.5, F_BLACK, 30, CARTAO, int(255 * a), centro=False)
    cv.restore()


# ------------------------------------------------------------------ rótulos (tela)
def rotulos_regua(cv, t, T, e):
    ry, k, X = e["ry"], e["k"], e["X"]
    rc = recuo(t, T)
    resumo = prog(t, T["caminho"] + 0.8, T["caminho"] + 1.25)
    y_c, y_r1, y_r2, y_r3 = ry - 48, ry + 80, ry + 122, ry + 192

    # pausa
    a = prog(t, T["pausa"] - 0.05, T["pausa"] + 0.25) * (1 - prog(t, T["longa"] - 0.25, T["longa"] + 0.15))
    rotulo_txt(cv, T_PAUSA, X(0.5), y_r1, 30, "#FFFFFF", a)
    a = prog(t, T["alguns"] + 0.1, T["alguns"] + 0.4) * (1 - prog(t, T["longa"] - 0.25, T["longa"] + 0.15))
    rotulo_txt(cv, T_ALGUNS, X(0.5), y_r2, 30, AZUL, a, fonte=F_SEMI)

    # alongamento (à esquerda enquanto cresce; centrado depois do recuo)
    lw = larg_texto(T_ALONG, F_BLACK, 30)
    xa = lerp(max(X(1 + e["L"] / 2), X(1) + lw / 2 + 36), X(1 + L_B / 2) - 10, rc)
    a = prog(t, T["depois"] + 0.25, T["depois"] + 0.55)
    rotulo_txt(cv, T_ALONG, xa, y_r1, 30, "#FFFFFF", a)

    # MAIS DIAS acompanha a frente do alongamento
    a = prog(t, T["mais"] - 0.05, T["mais"] + 0.2) * (1 - prog(t, T["curta"] - 0.25, T["curta"] + 0.05))
    # causa -> efeito: um fio dourado fino sai da base da fita (a correção) e chega na pílula MAIS DIAS
    ap = prog(t, T["mais"] - 0.05, T["mais"] + 0.25)
    a_fio = ap * (1 - prog(t, T["curta"] - 0.25, T["curta"] + 0.05))
    if a_fio > 0:
        _, yf = tela_osso(e, CX, Y_CORTE + FENDA + GAP_U * e["L"])
        xp = X(1 + e["L"]) - larg_texto(T_MAIS, F_BLACK, 34) / 2 - 22
        yp = ry - 57
        pf = skia.Path(); pf.moveTo(398, yf + 8); pf.lineTo(398, yp - 16)
        pf.quadTo(398, yp, 414, yp); pf.lineTo(xp - 6, yp)
        m = skia.PathMeasure(pf, False); seg = skia.Path()
        m.getSegment(0, m.getLength() * e_inout(ap), seg, True)
        cv.drawPath(seg, paint(OURO, int(200 * a_fio), "stroke", 2.5))
        cv.drawCircle(398, yf + 8, 5, paint(OURO, int(255 * a_fio)))
        if ap > 0.9:
            ph = skia.Path(); ph.moveTo(xp, yp); ph.lineTo(xp - 13, yp - 8); ph.lineTo(xp - 13, yp + 8); ph.close()
            cv.drawPath(ph, paint(OURO, int(255 * a_fio)))
    pilula(cv, T_MAIS, X(1 + e["L"]), ry - 46, 34, OURO, a, esc=lerp(1.4, 1.0, e_back(clamp((t - T["mais"] + 0.05) / 0.3))))

    # carimbo da parte curta, em cima do trecho; some ANTES de a câmera recuar (senão ele desliza por
    # cima do reloginho e encavala no rótulo azul A PARTE CURTA, que entra em curta+1.35)
    carimbo(cv, T_CURTA, X(1 + L_B / 2), ry + 4, -5, T["curta"] - 0.02, t, dur=T["longa"] - T["curta"] + 0.05, tam=56)

    # curta x longa, lado a lado (somem para o botão; voltam no resumo)
    some = 1 - prog(t, T["nao"] - 0.35, T["nao"] - 0.05)
    a = max(prog(t, T["curta"] + 1.35, T["curta"] + 1.7) * some, resumo)
    rotulo_txt(cv, T_CURTA, X(1 + L_B / 2) - 10, y_c, 30, AZUL, a)
    x_cons = X(C0 + C_PREV / 2) + 20
    a = max(prog(t, T["consolidacao"] + 0.3, T["consolidacao"] + 0.6) * some, resumo)
    rotulo_txt(cv, T_LONGA, x_cons, y_c, 32, OURO, a)
    a = prog(t, T["consolidacao"] + 0.1, T["consolidacao"] + 0.4)
    rotulo_txt(cv, T_CONSOL, x_cons, y_r1, 30, "#FFFFFF", a)

    # por meses, sob o tracejado
    a = prog(t, T["meses"] - 0.05, T["meses"] + 0.25)
    rotulo_txt(cv, T_MESES, X(C0 + C_FIM + 2.6), y_r1, 30, AZUL, a, fonte=F_SEMI)

    # linha de baixo: um recado por vez, preso à SUA frase (sai antes da frase seguinte, para não
    # formar par falso com a legenda de baixo)
    a = prog(t, T["nao"] - 0.05, T["nao"] + 0.25) * (1 - prog(t, T["idade"] - 0.4, T["idade"] - 0.12))
    rotulo_txt(cv, T_APRESSAR, CX, y_r3, 38, "#FFFFFF", a)
    a = prog(t, T["velocidade"] - 0.05, T["velocidade"] + 0.25) * (1 - prog(t, T["aparelho"] - 0.5, T["aparelho"] - 0.22))
    rotulo_txt(cv, T_VELOC, CX, y_r3, 38, "#FFFFFF", a)
    carimbo(cv, T_PRAZO, CX, ry + 174, -3, T["prazo"] - 0.02, t, dur=1.75, tam=50)   # canto de baixo em y≈1229
    # raio-X: em vez de repetir a frase inteira da legenda, só dá NOME aos pontos — uma chave fina
    # sob os pontos de controle e RAIO-X embaixo dela
    a = prog(t, T["raio"] - 0.05, T["raio"] + 0.25) * (1 - prog(t, T["caminho"] + 0.2, T["caminho"] + 0.5))
    if a > 0:
        xa, xb = X(MARCOS[0]), X(MARCOS[-1])
        abre = e_out(prog(t, T["raio"] - 0.05, T["raio"] + 0.4))
        xm = (xa + xb) / 2; h = (xb - xa) / 2 * abre
        yk = ry + 110
        pk = skia.Path(); pk.moveTo(xm - h, yk - 12); pk.lineTo(xm - h, yk); pk.lineTo(xm + h, yk)
        pk.lineTo(xm + h, yk - 12)
        pk.moveTo(xm, yk); pk.lineTo(xm, yk + 14)
        cv.drawPath(pk, paint(OURO, int(220 * a), "stroke", 3))
        rotulo_txt(cv, T_RAIO, xm, yk + 56, 40, OURO, a)

    # seta dupla sob a ponta elástica
    a = prog(t, T["velocidade"] - 0.05, T["velocidade"] + 0.3) * (1 - prog(t, T["aparelho"], T["sai"]))
    if a > 0:
        xe = X(C0 + e["G"]); y = ry + 50
        cv.drawLine(xe - 40, y, xe + 40, y, paint(OURO, int(255 * a), "stroke", 4))
        for s in (-1, 1):
            p = skia.Path(); p.moveTo(xe + s * 52, y); p.lineTo(xe + s * 36, y - 10); p.lineTo(xe + s * 36, y + 10); p.close()
            cv.drawPath(p, paint(OURO, int(255 * a)))


def botao(cv, t, T, e):
    ra = t - (T["nao"] - 0.1)
    if ra < 0:
        return
    a = clamp(ra / 0.15) * (1 - prog(t, T["idade"] - 0.2, T["idade"] + 0.15))
    if a <= 0:
        return
    esc = lerp(0.4, 1.0, e_back(clamp(ra / 0.35)))
    kp = t - T["apressar"]
    if 0 <= kp < 0.3:
        esc *= 1 - 0.16 * math.sin(math.pi * kp / 0.3)
    cinza = e_inout(prog(t, T["apressar"] + 0.15, T["apressar"] + 0.45))
    cor = lerpc(OURO, CINZA, cinza)
    ks = t - (T["apressar"] + 0.25)
    dx = 10 * math.sin(ks * 48) * math.exp(-ks / 0.2) if ks > 0 else 0.0
    x, y = 680, e["ry"] - 104
    if 0 <= kp < 0.5:                                  # o aperto: anel que se abre
        cv.drawCircle(x, y, 46 + 56 * e_out(kp / 0.5), paint(OURO, int(200 * (1 - kp / 0.5) * a), "stroke", 4))
    botao_ff(cv, x, y, cor, a, esc, dx)


def etiquetas(cv, t, T, e):
    """Idade, saúde, alimentação e cigarro: em coluna à direita, ligadas à ponta da consolidação."""
    a_sai = 1 - prog(t, T["sai"] + 0.3, T["sai"] + 0.7)
    if t < T["idade"] - 0.1 or a_sai <= 0:
        return
    tam = 30
    wmax = max(larg_texto(s, F_BLACK, tam) for _, s in FATORES) * 1.08
    w = 40 + 14 + wmax + 36
    x0 = 1032 - w
    pulso = max(0.0, 1 - abs(t - (T["velocidade"] + 0.15)) / 0.45)
    ys = [600 + 70 * i for i in range(4)]
    # chave + ligação até a ponta
    vis = [prog(t, T[ch] - 0.08, T[ch] + 0.12) for ch, _ in FATORES]
    n = sum(1 for v in vis if v > 0)
    if n:
        xb = x0 - 18; ya = ys[0] + 27; yz = ys[n - 1] + 27
        cor_l = lerpc(AZUL, OURO, pulso)
        cv.drawLine(xb, ya, xb, yz, paint(cor_l, int(200 * a_sai), "stroke", 3))
        for i in range(n):
            cv.drawLine(xb, ys[i] + 27, x0, ys[i] + 27, paint(cor_l, int(200 * a_sai * vis[i]), "stroke", 3))
        xe = e["X"](C0 + e["G"]); ye = e["ry"] - 30
        p = skia.Path(); p.moveTo(xb, yz); p.cubicTo(xb, yz + 60, xe, ye - 70, xe, ye)
        cv.drawPath(p, paint(cor_l, int(200 * a_sai), "stroke", 3))
        cv.drawCircle(xe, ye, 6, paint(cor_l, int(255 * a_sai)))
    for i, (ch, s) in enumerate(FATORES):
        k = t - (T[ch] - 0.08)
        if k < 0:
            continue
        a = clamp(k / 0.12) * a_sai
        esc = lerp(0.5, 1.0, e_back(clamp(k / 0.35)))
        cv.save(); cv.translate(x0 + w / 2, ys[i] + 27); cv.scale(esc, esc)
        cor = lerpc(AZUL, OURO, pulso)
        caixa(cv, -w / 2, -27, w / 2, 27, cor, a, r=14)
        ICONES[ch](cv, -w / 2 + 18 + 20, 0, 17, a)
        texto(cv, s, -w / 2 + 18 + 40 + 14, 11, F_BLACK, tam, "#FFFFFF", int(255 * a), centro=False)
        cv.restore()


def rotulos_osso(cv, t, T, e):
    gap = GAP_U * e["L"]
    xg, yg0 = tela_osso(e, CX + HASTE / 2, Y_CORTE)
    _, yg1 = tela_osso(e, CX, Y_CORTE + FENDA + gap)

    # escopo: logo abaixo do gancho; acende quando a voz diz "alongamento"
    sai = e_inout(prog(t, t_capa(T), t_capa(T) + 0.5))
    if sai < 1:
        k = t - T["alongamento"]
        acende = e_out(clamp(k / 0.25)) if k > 0 else 0.0
        esc = 1 + 0.12 * math.sin(math.pi * clamp(k / 0.35)) if k > 0 else 1.0
        cor = lerpc("#FFFFFF", OURO, acende)
        cv.save(); cv.translate(0, -50 * sai)
        pilula(cv, T_ESCOPO, CX, 362, 36, lerpc(AZUL, OURO, acende), (0.85 + 0.15 * acende) * (1 - sai), esc=esc, cor_txt=cor)
        cv.restore()

    # 1 MM por dia: cartão à direita da fenda
    a = prog(t, T["milimetro"] - 0.05, T["milimetro"] + 0.2) * (1 - prog(t, T["curta"] - 0.2, T["curta"] + 0.15))
    if a > 0:
        x0, y0 = 700, 528
        lw = max(larg_texto(T_1MM, F_BLACK, 72), larg_texto(T_POR_DIA, F_SEMI, 36))
        ym = (yg0 + yg1) / 2
        cv.drawLine(xg + 6, ym, x0, 602, paint(OURO, int(200 * a), "stroke", 2.5))
        cv.drawCircle(xg + 6, ym, 6, paint(OURO, int(255 * a)))
        cv.save(); cv.translate(24 * (1 - e_out(a)), 0)
        caixa(cv, x0, y0, x0 + lw * 1.08 + 52, y0 + 154, OURO, a, r=20, borda=2.5)
        esc = lerp(1.35, 1.0, e_out(clamp((t - T["milimetro"]) / 0.25)))
        cv.save(); cv.translate(x0 + 26, y0 + 80); cv.scale(esc, esc)
        texto(cv, T_1MM, 0, 0, F_BLACK, 72, "#FFFFFF", int(255 * a), centro=False)
        cv.restore()
        a2 = a * prog(t, T["dia"] - 0.05, T["dia"] + 0.2)
        texto(cv, T_POR_DIA, x0 + 30, y0 + 130, F_SEMI, 36, AZUL, int(255 * a2), centro=False)
        cv.restore()

    # fita da correção + QUANTO MAIOR / A CORREÇÃO
    a = prog(t, T["quanto2"] - 0.05, T["quanto2"] + 0.25) * (1 - prog(t, T["curta"] - 0.2, T["curta"] + 0.15))
    if a > 0:
        (_, _), (b0, b1) = janelas(T)
        fita(cv, 398, yg0, yg1, a, prog(t, b0, b0 + 0.2) * (1 - prog(t, b1, b1 + 0.4)))
        rotulo_txt(cv, T_QUANTO, 370 - larg_texto(T_QUANTO, F_BLACK, 34), 604, 34, "#FFFFFF", a, centro=False)
        a2 = a * prog(t, T["correcao"] - 0.05, T["correcao"] + 0.2)
        rotulo_txt(cv, T_CORRECAO, 370 - larg_texto(T_CORRECAO, F_BLACK, 34), 648, 34, OURO, a2, centro=False)

    # carga: seta de peso pousa no topo do osso
    t0 = T["carga"] - 0.3
    k = t - t0
    if k > 0:
        a = clamp(k / 0.12) * (1 - prog(t, T["nao"] - 0.15, T["nao"] + 0.15))
        if a > 0:
            y_pouso = e["by"] - 12
            cai = clamp(k / 0.35)
            y = lerp(y_pouso - 40, y_pouso, cai * cai)
            ki = t - (t0 + 0.35)
            esmaga = math.sin(math.pi * clamp(ki / 0.22)) if ki > 0 else 0.0
            # nenhum pixel da seta acima de y 214 (o selo COMO FUNCIONA mora em 150-204); a borda de
            # cima é um degradê curto, para a cauda "nascer" em vez de aparecer cortada na queda
            cv.saveLayer(skia.Rect(0, 214, W, y_pouso + 30), None)
            cv.clipRect(skia.Rect(0, 214, W, y_pouso + 30))
            seta_peso(cv, CX, y, a, esmaga)
            masc = skia.Paint(AntiAlias=True)
            masc.setShader(skia.GradientShader.MakeLinear([skia.Point(0, 214), skia.Point(0, 225)],
                                                          [skia.ColorSetARGB(0, 0, 0, 0), skia.ColorSetARGB(255, 0, 0, 0)]))
            masc.setBlendMode(skia.BlendMode.kDstIn)
            cv.drawRect(skia.Rect(0, 214, W, y_pouso + 30), masc)
            cv.restore()
            if 0 < ki < 0.45:
                ai = 1 - ki / 0.45
                for s in (-1, 1):
                    for j, dy in enumerate((-14, 0, 14)):
                        x1 = CX + s * (62 + 14 * j); x2 = x1 + s * 30 * e_out(ki / 0.45)
                        cv.drawLine(x1, y_pouso + dy, x2, y_pouso + dy - 6, paint("#FFFFFF", int(230 * ai), "stroke", 4))
            a2 = a * prog(t, T["carga"], T["carga"] + 0.25)
            rotulo_txt(cv, T_CARGA, 620, 296, 38, OURO, a2, centro=False)

    # ganhando resistência: caixa de 2 linhas ao lado do osso novo
    a = prog(t, T["ganhando"] - 0.05, T["ganhando"] + 0.25) * (1 - prog(t, T["caminho"] + 0.1, T["caminho"] + 0.4))
    if a > 0:
        lw = max(larg_texto(T_GANHANDO, F_BLACK, 34), larg_texto(T_RESIST, F_BLACK, 34)) * 1.06
        x0, y0 = 650, 562
        ym = (yg0 + yg1) / 2
        cv.drawLine(xg + 6, ym, x0, ym, paint(OURO, int(200 * a), "stroke", 2.5))
        cv.drawCircle(xg + 6, ym, 6, paint(OURO, int(255 * a)))
        cv.save(); cv.translate(24 * (1 - e_out(a)), 0)
        caixa(cv, x0, y0, x0 + lw + 40, y0 + 112, OURO, a, r=18, borda=2.5)
        texto(cv, T_GANHANDO, x0 + 20, y0 + 46, F_BLACK, 34, "#FFFFFF", int(255 * a), centro=False)
        a2 = a * prog(t, T["resistencia"] - 0.05, T["resistencia"] + 0.2)
        texto(cv, T_RESIST, x0 + 20, y0 + 92, F_BLACK, 34, OURO, int(255 * a2), centro=False)
        cv.restore()


# ------------------------------------------------------------------ quadro
def quadro(cv, t, T, blocos, ep):
    fundo(cv, t)
    e = estado(t, T)

    osso(cv, t, T, e)
    regua(cv, t, T, e)
    bandeira(cv, t, T, e)
    rotulos_regua(cv, t, T, e)
    botao(cv, t, T, e)
    etiquetas(cv, t, T, e)
    rotulos_osso(cv, t, T, e)

    gap = GAP_U * e["L"]
    _, ym = tela_osso(e, CX, Y_CORTE + (FENDA + gap) / 2)
    brilhos(cv, BX, ym, t, T["milimetro"] + 0.05, n=12, raio=120)
    brilhos(cv, BX, ym, t, T["ganhando"] + 0.1, n=12, raio=130)
    brilhos(cv, e["X"](C0 + C_FIM), e["ry"] - 60, t, T["sai"] + 0.35, n=10, raio=110)

    capa(cv, t, t_capa(T), ep["gancho"][0], ep["gancho"][1])
    selo_como_funciona(cv, prog(t, t_capa(T) + 0.2, t_capa(T) + 0.6) * (1 - prog(t, T["manda"] - 0.3, T["manda"])))
    interface(cv, t, T, blocos, DESTAQUE)


# ------------------------------------------------------------------ som e prévias
def sons(T):
    ev = [(T["fixador"] + 0.1 * i + 0.1, "ping", 0.5 - 0.05 * i) for i in range(3)]
    ev += [(T["alongamento"], "pop", 0.5), (t_capa(T), "whoosh", 0.3),
           (T["alguns"], "whoosh", 0.3), (T["pausa"], "pop", 0.65),
           (T["milimetro"], "shimmer", 0.45), (T["dia"], "pop", 0.4),
           (T["quanto2"], "whoosh", 0.25), (T["mais"], "pop", 0.6),
           (T["curta"] - 0.02, "thump", 0.9), (T["longa"], "whoosh", 0.6), (T["consolidacao"], "shimmer", 0.6),
           (T["endurece"], "crackle", 0.8), (T["carga"] + 0.05, "thump", 0.85),
           (T["nao"] - 0.1, "pop", 0.6), (T["apressar"], "tick", 0.9), (T["apressar"] + 0.25, "thump", 0.35)]
    ev += [(T[ch] - 0.08, "pop", 0.6) for ch, _ in FATORES]
    ev += [(T["velocidade"], "whoosh", 0.35), (T["aparelho"], "whoosh", 0.6)]
    ev += [(T["aparelho"] + 0.15 + 0.1 * i, "ping", 0.5 - 0.05 * i) for i in range(3)]
    ev += [(T["sai"] + 0.3, "thump", 0.55), (T["ganhando"], "shimmer", 0.6), (T["meses"], "whoosh", 0.25),
           (T["prazo"] - 0.02, "thump", 0.9)]
    ev += [(T["raio"] + 0.05 + 0.17 * i, "pop", 0.35) for i in range(len(MARCOS))]
    ev += [(T["caminho"] + 0.4, "whoosh", 0.45), (T["caminho"] + 1.35, "ding", 0.35), (T["manda"] + 0.05, "whoosh", 0.5)]
    (a0, a1), (b0, b1) = janelas(T)                     # um clique por tique
    ev += [(lerp(a0, a1, i / N_A), "click", 0.85) for i in range(N_A)]
    ev += [(lerp(b0, b1, i / N_B), "click", 0.85) for i in range(N_B)]
    return ev


def tempos_previa(T):
    return [0.4, T["pausa"] + 0.5, T["dias"] + 0.45, T["curta"] + 0.35, T["consolidacao"] + 1.2,
            T["carga"] + 0.4, T["apressar"] + 0.45, T["velocidade"] + 0.5, T["meses"] + 0.4, T["prazo"] + 0.8,
            T["caminho"] + 0.25, T["caminho"] + 1.75]


render = fazer_render(quadro, ANCORAS, sons, tempos_previa, respiro_cta=3.0)   # ~2 s de resumo antes da CTA
