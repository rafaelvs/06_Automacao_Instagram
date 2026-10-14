# -*- coding: utf-8 -*-
"""
marca.py — KIT DE MARCA dos carrosséis do feed (4:5, 1080x1350).

Por que existe (14/10/2026, pedido do Rafael: "melhorar os slides dentro da minha
personalização"): os carrosséis usavam "RV" digitado em Times Bold, serifa pesada, texturas
genéricas (grade/diagonais/raios) e metade inferior vazia — fora da identidade do cartão, da
pasta e do site. Este módulo concentra a identidade e é a ÚNICA fonte das primitivas visuais:

  • Tipografia DO SITE: Playfair Display (títulos) + Inter (apoio) — arquivos em
    marca/fontes (licença OFL; latin + latin-ext mesclados). Fallback POR CARACTERE para
    Liberation quando um glifo não existe (ex.: "→", "≈") — nunca sai quadradinho.
  • Monograma RV REAL (marca/rv_monograma.png, máscara alfa do logo oficial).
  • Paleta do site/cartão: tinta #14141A · creme #F3E2C8 · dourado #B08C4F · corpo #D9CDB6.
  • Ilustrações em TRAÇO FINO (no espírito do selo do grupo de Reconstrução IOT-HCFMUSP):
      fixador — tíbia/fíbula num fixador circular, com o vão do regenerado (Reconstrução);
      eixo    — fêmur e tíbia com placas de crescimento e o eixo mecânico (Pediatria).
    São esquemas, não exames: nada de raio-X real nem paciente (CFM).

ADITIVO / fail-safe: sem a pasta marca/, as fontes caem para Liberation e o monograma vira
texto — o render nunca quebra por falta de asset. Só Pillow (o runner não tem numpy).
"""
import json
import math
import os

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = os.path.dirname(os.path.abspath(__file__))
DIR_MARCA = os.path.join(ROOT, "marca")
DIR_FONTES = os.path.join(DIR_MARCA, "fontes")
LIB = "/usr/share/fonts/truetype/liberation/"

W, H = 1080, 1350

# ----------------------------------------------------------------------------------------
# Paleta (mesmos valores do CSS do site rafaelvargasmd.com.br)
# ----------------------------------------------------------------------------------------
TINTA = (20, 20, 26)        # #14141A  --preto do site
TINTA_2 = (31, 28, 28)      # brilho quente do fundo (centro de luz)
CREME = (243, 226, 200)     # #F3E2C8
OURO = (176, 140, 79)       # #B08C4F
OURO_CLARO = (201, 168, 108)  # leads de lista sobre fundo escuro (contraste)
CORPO = (217, 205, 182)     # #D9CDB6  texto corrido
CINZA = (146, 137, 121)     # rodapé (legível, discreto)
CINZA_2 = (110, 102, 90)    # #6E665A  disclaimer
FIO = (56, 52, 46)          # filetes sobre o escuro

# ----------------------------------------------------------------------------------------
# Fontes (papéis tipográficos) + fallback por caractere
# ----------------------------------------------------------------------------------------
TITULO, TITULO_IT, TEXTO, TEXTO_MED = "titulo", "titulo_it", "texto", "texto_med"
_ARQ = {
    TITULO: ("PlayfairDisplay-Regular.ttf", "LiberationSerif-Regular.ttf"),
    TITULO_IT: ("PlayfairDisplay-Italic.ttf", "LiberationSerif-Italic.ttf"),
    TEXTO: ("Inter-Regular.ttf", "LiberationSans-Regular.ttf"),
    TEXTO_MED: ("Inter-Medium.ttf", "LiberationSans-Bold.ttf"),
}
# Nomes antigos do carrossel.py (SB/NR/NB) -> papel novo. Quem chama C.F(C.SB, n) ganha a
# tipografia do site sem mudar de código.
PAPEL_DE_ARQUIVO = {
    "LiberationSerif-Bold.ttf": TITULO,
    "LiberationSerif-Regular.ttf": TITULO,
    "LiberationSans-Regular.ttf": TEXTO,
    "LiberationSans-Bold.ttf": TEXTO_MED,
}

try:
    with open(os.path.join(DIR_FONTES, "cobertura.json"), encoding="utf-8") as _f:
        _COB_RAW = json.load(_f)
except Exception:
    _COB_RAW = {}


def _faixas_para_set(faixas):
    s = set()
    for a, b in faixas:
        s.update(range(a, b + 1))
    return s


_COB = {k: _faixas_para_set(v) for k, v in _COB_RAW.items()}
_FC = {}


def _marca_ok(papel):
    return os.path.exists(os.path.join(DIR_FONTES, _ARQ[papel][0]))


def fonte(papel, tam):
    """Fonte do papel tipográfico; cai para Liberation se a fonte da marca faltar."""
    k = (papel, tam)
    if k not in _FC:
        arq, reserva = _ARQ[papel]
        p = os.path.join(DIR_FONTES, arq)
        try:
            _FC[k] = ImageFont.truetype(p, tam)
        except Exception:
            _FC[k] = ImageFont.truetype(LIB + reserva, tam)
    return _FC[k]


def _reserva(papel, tam):
    k = ("_reserva", papel, tam)
    if k not in _FC:
        _FC[k] = ImageFont.truetype(LIB + _ARQ[papel][1], tam)
    return _FC[k]


def _cobre(papel, ch):
    if not _marca_ok(papel):
        return True                      # já está na Liberation
    cob = _COB.get(_ARQ[papel][0])
    return True if cob is None else (ord(ch) in cob or ch in " \n")


def _runs(texto, papel, tam):
    """Quebra o texto em trechos (fonte, string): fallback por caractere."""
    out = []
    for ch in texto:
        f = fonte(papel, tam) if _cobre(papel, ch) else _reserva(papel, tam)
        if out and out[-1][0] is f:
            out[-1][1] += ch
        else:
            out.append([f, ch])
    return out


_MED = ImageDraw.Draw(Image.new("RGB", (8, 8)))


def largura(texto, papel, tam, tr=0):
    if not texto:
        return 0
    if tr:
        return sum(largura(ch, papel, tam) for ch in texto) + tr * (len(texto) - 1)
    return sum(_MED.textlength(s, font=f) for f, s in _runs(texto, papel, tam))


def escreve(d, x, y, texto, papel, tam, cor, tr=0, alinha="esq"):
    """Escreve na LINHA DE BASE y (anchor 'ls'). alinha: esq | centro | dir. Devolve a largura."""
    w = largura(texto, papel, tam, tr)
    if alinha == "centro":
        x -= w / 2
    elif alinha == "dir":
        x -= w
    if tr:
        for ch in texto:
            for f, s in _runs(ch, papel, tam):
                d.text((x, y), s, font=f, fill=cor, anchor="ls")
            x += largura(ch, papel, tam) + tr
        return w
    for f, s in _runs(texto, papel, tam):
        d.text((x, y), s, font=f, fill=cor, anchor="ls")
        x += _MED.textlength(s, font=f)
    return w


def quebra(texto, papel, tam, larg, tr=0, equilibra=False):
    """Quebra gulosa; com equilibra=True reparte as linhas por igual (título não fica com
    uma palavra sozinha embaixo) — busca a menor largura que mantém o nº de linhas."""
    def guloso(lim):
        linhas, cur = [], ""
        for p in texto.split():
            t = (cur + " " + p).strip()
            if largura(t, papel, tam, tr) <= lim or not cur:
                cur = t
            else:
                linhas.append(cur)
                cur = p
        if cur:
            linhas.append(cur)
        return linhas
    base = guloso(larg)
    if not equilibra or len(base) < 2:
        return base
    lo, hi = larg * 0.5, larg
    melhor = base
    for _ in range(14):
        mid = (lo + hi) / 2
        t = guloso(mid)
        if len(t) <= len(base) and all(largura(l, papel, tam, tr) <= larg for l in t):
            melhor, hi = t, mid
        else:
            lo = mid
    return melhor


def ajusta(texto, papel, tam_ini, tam_min, larg, max_linhas, equilibra=True, passo=4):
    """Maior tamanho (até tam_min) em que o texto cabe em max_linhas."""
    tam = tam_ini
    while True:
        linhas = quebra(texto, papel, tam, larg, equilibra=equilibra)
        if len(linhas) <= max_linhas or tam <= tam_min:
            return tam, linhas
        tam -= passo


def metr(papel, tam):
    """(ascendente, descendente) em px — p/ empilhar linhas por linha de base."""
    a, dsc = fonte(papel, tam).getmetrics()
    return a, dsc


# ----------------------------------------------------------------------------------------
# Monograma
# ----------------------------------------------------------------------------------------
_MONO = {}


def _mono_mask():
    if "m" not in _MONO:
        p = os.path.join(DIR_MARCA, "rv_monograma.png")
        _MONO["m"] = Image.open(p).convert("RGBA").getchannel("A") if os.path.exists(p) else None
    return _MONO["m"]


def monograma(img, x, y, alt, cor, ancora="esq-topo"):
    """Cola o monograma RV real (altura `alt`). ancora: esq-topo | centro."""
    m = _mono_mask()
    if m is None:   # fail-safe: monograma tipográfico
        d = ImageDraw.Draw(img)
        f = fonte(TITULO, int(alt * 0.9))
        w = _MED.textlength("RV", font=f)
        if ancora == "centro":
            x, y = x - w / 2, y - alt / 2
        d.text((x, y), "RV", font=f, fill=cor)
        return w
    larg = max(1, round(alt * m.width / m.height))
    mk = m.resize((larg, alt), Image.LANCZOS)
    if ancora == "centro":
        x, y = x - larg / 2, y - alt / 2
    camada = Image.new("RGBA", mk.size, cor + (255,))
    camada.putalpha(mk)
    base = img if img.mode == "RGBA" else None
    if base is not None:
        base.alpha_composite(camada, (round(x), round(y)))
    else:
        img.paste(camada, (round(x), round(y)), camada)
    return larg


# ----------------------------------------------------------------------------------------
# Fundo: tinta + luz quente sutil + (opcional) motivo em traço fino
# ----------------------------------------------------------------------------------------
_GLOW = {}


def _luz(foco):
    k = foco
    if k not in _GLOW:
        pw, ph = 108, 135
        g = Image.new("RGB", (pw, ph), TINTA)
        d = ImageDraw.Draw(g)
        cx, cy = pw * foco[0], ph * foco[1]
        d.ellipse([cx - pw * 0.55, cy - ph * 0.42, cx + pw * 0.55, cy + ph * 0.42], fill=TINTA_2)
        g = g.filter(ImageFilter.GaussianBlur(26)).resize((W, H), Image.BICUBIC)
        _GLOW[k] = g
    return _GLOW[k].copy()


def _bez(p0, p1, p2, p3, t):
    u = 1 - t
    return (u ** 3 * p0[0] + 3 * u * u * t * p1[0] + 3 * u * t * t * p2[0] + t ** 3 * p3[0],
            u ** 3 * p0[1] + 3 * u * u * t * p1[1] + 3 * u * t * t * p2[1] + t ** 3 * p3[1])


def _motivo_curvas(img, cor, espelha=False):
    """Curvas finas douradas que nascem num canto e se dissolvem (mesmo motivo da capa do
    site e do interior da pasta)."""
    S = 2
    ov = Image.new("RGBA", (W * S, H * S), (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    for i in range(5):
        p0 = (-30 * S + i * 26 * S, H * S + 20 * S)
        p1 = (20 * S + i * 22 * S, H * S - (330 + i * 30) * S)
        p2 = ((260 + i * 50) * S, H * S - (560 - i * 22) * S)
        p3 = ((760 + i * 40) * S, H * S - (610 - i * 46) * S)
        prev = _bez(p0, p1, p2, p3, 0)
        N = 90
        for k in range(1, N + 1):
            t = k / N
            pt = _bez(p0, p1, p2, p3, t)
            a = int(70 * (1 - t) ** 1.6)
            if a > 2:
                d.line([prev, pt], fill=cor + (a,), width=2 * S)
            prev = pt
    ov = ov.resize((W, H), Image.LANCZOS)
    if espelha:
        ov = ov.transpose(Image.FLIP_LEFT_RIGHT)
    img.alpha_composite(ov)


def _motivo_anel(img, cor, lado="dir"):
    """Um anel fino em perspectiva saindo da borda — eco do anel do fixador circular."""
    S = 2
    ov = Image.new("RGBA", (W * S, H * S), (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    cx = (W + 120) * S if lado == "dir" else -120 * S
    cy = (H - 250) * S
    for r, a in ((520, 46), (470, 30)):
        d.ellipse([cx - r * S, cy - r * 0.32 * S, cx + r * S, cy + r * 0.32 * S],
                  outline=cor + (a,), width=2 * S)
    img.alpha_composite(ov.resize((W, H), Image.LANCZOS))


# Motivos antigos do estilo_variacao (texturas de grade/raios/diagonais) -> motivos da marca.
# Mantém a VARIAÇÃO determinística por peça (regra 4 v6), trocando só o repertório.
MOTIVO_DA_MARCA = {"arcos": "curvas", "raios": "curvas_esp", "grade": "anel",
                   "cantos": "anel_esq", "diagonais": "liso"}


def fundo(var=None):
    """Imagem RGBA 1080x1350: tinta + luz quente + motivo da peça."""
    mot = MOTIVO_DA_MARCA.get((var or {}).get("motivo", "arcos"), "curvas")
    foco = {"curvas": (0.62, 0.38), "curvas_esp": (0.38, 0.38), "anel": (0.40, 0.45),
            "anel_esq": (0.60, 0.45), "liso": (0.5, 0.40)}[mot]
    img = _luz(foco).convert("RGBA")
    if mot == "curvas":
        _motivo_curvas(img, OURO)
    elif mot == "curvas_esp":
        _motivo_curvas(img, OURO, espelha=True)
    elif mot == "anel":
        _motivo_anel(img, OURO, "dir")
    elif mot == "anel_esq":
        _motivo_anel(img, OURO, "esq")
    return img


# ----------------------------------------------------------------------------------------
# Cabeçalho (mesmo "lockup" da frente do cartão: monograma | nome / especialidade)
# ----------------------------------------------------------------------------------------
def cabecalho(img, x=110, y=88, cor_mono=CREME):
    d = ImageDraw.Draw(img)
    alt = 64
    wl = monograma(img, x, y, alt, cor_mono)
    fx = x + wl + 22
    d.line([(fx, y + 6), (fx, y + alt - 6)], fill=OURO, width=2)
    tx = fx + 22
    escreve(d, tx, y + 30, "Dr. Rafael Vargas", TITULO, 27, CREME)
    escreve(d, tx, y + 58, "Ortopedia e Traumatologia", TEXTO, 17, OURO, tr=0.6)
    return y + alt


# ----------------------------------------------------------------------------------------
# Rodapé CFM + progresso
# ----------------------------------------------------------------------------------------
SIG = "Dr. Rafael Vargas · Médico · CRM-SP 226103 · RQE 137901"
DISC = "Conteúdo educativo — não substitui avaliação médica."


def rodape(d, pagina, n, ac=OURO, x=110, sig=SIG, disc=DISC):
    y0 = H - 152
    d.line([(x, y0), (W - x, y0)], fill=FIO, width=2)
    escreve(d, x, y0 + 44, "@rafaelvargasmd", TEXTO_MED, 21, CORPO)
    escreve(d, x, y0 + 80, sig, TEXTO, 18, CINZA)
    escreve(d, x, y0 + 108, disc, TEXTO, 17, CINZA_2)
    progresso(d, pagina, n, ac, x_dir=W - x, y=y0 + 37)


def progresso(d, pagina, n, ac=OURO, x_dir=970, y=1235):
    """Segmentos finos (o ativo em dourado, mais longo)."""
    seg, ativo, gap = 18, 40, 8
    tot = ativo + (n - 1) * seg + (n - 1) * gap
    x = x_dir - tot
    for i in range(n):
        w = ativo if i == pagina else seg
        d.line([(x, y), (x + w, y)], fill=(ac if i == pagina else FIO), width=3)
        x += w + gap


def seta(d, x, y, comp=64, cor=OURO, larg=2):
    """Seta desenhada em traço fino (não glifo)."""
    d.line([(x, y), (x + comp, y)], fill=cor, width=larg)
    d.line([(x + comp - 11, y - 8), (x + comp, y)], fill=cor, width=larg)
    d.line([(x + comp - 11, y + 8), (x + comp, y)], fill=cor, width=larg)


def arraste(d, x, y, ac=OURO, alinha="esq"):
    t = "Arraste"
    w = largura(t, TEXTO_MED, 24, tr=1.2)
    if alinha == "dir":
        x = x - (w + 18 + 64)
    escreve(d, x, y, t, TEXTO_MED, 24, ac, tr=1.2)
    seta(d, x + w + 18, y - 8, 64, ac)


def filete(d, x, y, comp=72, cor=OURO, larg=2):
    d.line([(x, y), (x + comp, y)], fill=cor, width=larg)


# ----------------------------------------------------------------------------------------
# Ilustrações em traço fino (desenhadas a 3x e reduzidas: traço limpo, sem serrilhado)
# ----------------------------------------------------------------------------------------
def _catmull(pts, fechado=False, n=10):
    if len(pts) < 3:
        return pts
    P = ([pts[-1]] + pts + [pts[0], pts[1]]) if fechado else ([pts[0]] + pts + [pts[-1]])
    out = []
    for i in range(1, len(P) - 2):
        p0, p1, p2, p3 = P[i - 1], P[i], P[i + 1], P[i + 2]
        for k in range(n):
            t = k / n
            t2, t3 = t * t, t * t * t
            out.append(tuple(0.5 * ((2 * p1[j]) + (-p0[j] + p2[j]) * t
                                    + (2 * p0[j] - 5 * p1[j] + 4 * p2[j] - p3[j]) * t2
                                    + (-p0[j] + 3 * p1[j] - 3 * p2[j] + p3[j]) * t3)
                             for j in (0, 1)))
    out.append(pts[0] if fechado else pts[-1])
    return out


def _linha(d, pts, cor, larg):
    if len(pts) >= 2:
        d.line(pts, fill=cor, width=larg, joint="curve")


def _pontilhada(d, pts, cor, larg, traco=10, vazio=9):
    """Polilinha tracejada (comprimentos em px da camada)."""
    acum, on = 0.0, True
    for a, b in zip(pts, pts[1:]):
        seg = math.dist(a, b)
        pos = 0.0
        while pos < seg:
            lim = (traco if on else vazio) - acum
            passo = min(lim, seg - pos)
            if on:
                t0, t1 = pos / seg, (pos + passo) / seg
                d.line([(a[0] + (b[0] - a[0]) * t0, a[1] + (b[1] - a[1]) * t0),
                        (a[0] + (b[0] - a[0]) * t1, a[1] + (b[1] - a[1]) * t1)],
                       fill=cor, width=larg)
            pos += passo
            acum += passo
            if acum >= (traco if on else vazio) - 1e-6:
                acum, on = 0.0, not on


def _tibia_fibula(d, ox, oy, L, cor, larg, vao=None, cor_vao=None, fises=None, cor_fise=None):
    """Tíbia + fíbula em vista frontal (perna direita; medial à esquerda), topo em (ox, oy),
    comprimento L. vao=(y0, y1) frações do comprimento: corticotomia com regenerado.
    fises=[frações y]: placas de crescimento (linha levemente ondulada)."""
    P = lambda x, y: (ox + x * L, oy + y * L)
    med = [(-0.118, 0.036), (-0.110, 0.072), (-0.086, 0.118), (-0.058, 0.168), (-0.045, 0.235),
           (-0.041, 0.40), (-0.041, 0.60), (-0.045, 0.78), (-0.056, 0.875), (-0.068, 0.932),
           (-0.067, 0.986)]
    lat = [(0.112, 0.036), (0.106, 0.072), (0.084, 0.118), (0.056, 0.172), (0.043, 0.240),
           (0.039, 0.40), (0.039, 0.60), (0.043, 0.78), (0.050, 0.875), (0.056, 0.928),
           (0.053, 0.958)]
    topo = [(-0.118, 0.036), (-0.104, 0.014), (-0.056, 0.008), (-0.020, 0.003), (-0.009, 0.009),
            (0.002, 0.003), (0.040, 0.008), (0.098, 0.014), (0.112, 0.036)]
    base_ = [(-0.067, 0.986), (-0.053, 1.0), (-0.041, 0.976), (-0.028, 0.963), (0.0, 0.967),
             (0.030, 0.962), (0.053, 0.958)]

    def contorno(pts):
        return [P(x, y) for x, y in _catmull(pts, n=12)]

    def corta(pts, y0, y1):
        """Divide uma curva (lista de pontos absolutos) removendo o trecho y0<y<y1."""
        a = [p for p in pts if p[1] <= oy + y0 * L]
        b = [p for p in pts if p[1] >= oy + y1 * L]
        return a, b

    cm, cl = contorno(med), contorno(lat)
    if vao:
        y0, y1 = vao
        for c in (cm, cl):
            a, b = corta(c, y0, y1)
            _linha(d, a, cor, larg)
            _linha(d, b, cor, larg)
        # bordas da corticotomia (levemente irregulares) e o regenerado (estrias finas)
        for yy, amp in ((y0, 0.004), (y1, -0.004)):
            xs = [-0.041 + i * 0.0102 for i in range(9)]
            pts = [P(x, yy + amp * 0.35 * math.sin(i * 1.7)) for i, x in enumerate(xs)]
            _linha(d, pts, cor, larg)
        cv = cor_vao or cor
        for i in range(5):
            xx = -0.030 + i * 0.015
            _pontilhada(d, [P(xx, y0 + 0.006), P(xx, y1 - 0.006)], cv, max(1, larg // 2),
                        traco=larg * 2, vazio=int(larg * 1.6))
    else:
        _linha(d, cm, cor, larg)
        _linha(d, cl, cor, larg)
    _linha(d, contorno(topo), cor, larg)
    _linha(d, contorno(base_), cor, larg)
    # fíbula (lateral) — próxima da tíbia, como numa incidência AP real
    fm = [(0.097, 0.108), (0.081, 0.25), (0.069, 0.55), (0.065, 0.82), (0.067, 0.93)]
    fl = [(0.120, 0.094), (0.105, 0.25), (0.089, 0.55), (0.083, 0.82), (0.087, 0.94)]
    fc = [(0.097, 0.108), (0.099, 0.084), (0.109, 0.072), (0.121, 0.078), (0.120, 0.094)]
    fb = [(0.067, 0.93), (0.067, 0.99), (0.076, 1.032), (0.087, 1.0), (0.087, 0.94)]
    for c in (fm, fl, fc, fb):
        _linha(d, contorno(c), cor, max(1, int(larg * 0.85)))
    if fises:
        cf = cor_fise or cor
        for fy in fises:
            if fy < 0.5:
                xa, xb = -0.098, 0.090
            else:
                xa, xb = -0.054, 0.046
            pts = [P(xa + (xb - xa) * i / 10, fy + 0.0035 * math.sin(i * 1.3)) for i in range(11)]
            _linha(d, pts, cf, max(1, int(larg * 0.8)))


def _femur(d, ox, oy, L, cor, larg, fises=None, cor_fise=None):
    """Fêmur em vista frontal (perna direita; cabeça à esquerda/medial). (ox, oy) = centro do
    joelho no topo... aqui: x=0 no centro dos côndilos, y=0 no topo da cabeça. Devolve o centro
    da cabeça (para o eixo mecânico)."""
    P = lambda x, y: (ox + x * L, oy + y * L)
    # cabeça
    hc, hr = (-0.086, 0.070), 0.060
    cab = [(hc[0] + hr * math.cos(a), hc[1] + hr * math.sin(a))
           for a in [math.radians(t) for t in range(50, 331, 8)]]
    _linha(d, [P(x, y) for x, y in cab], cor, larg)
    lateral = [(-0.034, 0.040), (0.008, 0.056), (0.040, 0.052), (0.066, 0.026), (0.090, 0.034),
               (0.104, 0.078), (0.099, 0.132), (0.086, 0.210), (0.072, 0.40), (0.060, 0.60),
               (0.060, 0.760), (0.074, 0.850), (0.096, 0.915), (0.104, 0.958), (0.092, 0.992),
               (0.066, 1.000)]
    medial = [(-0.047, 0.116), (-0.027, 0.140), (-0.022, 0.158), (-0.040, 0.171), (-0.034, 0.190),
              (-0.028, 0.250), (-0.034, 0.45), (-0.046, 0.68), (-0.062, 0.800), (-0.086, 0.885),
              (-0.104, 0.940), (-0.100, 0.982), (-0.076, 1.000)]
    entalhe = [(0.064, 1.000), (0.036, 0.993), (0.016, 0.962), (0.000, 0.956), (-0.018, 0.962),
               (-0.040, 0.993), (-0.074, 1.000)]
    for pts in (lateral, medial, entalhe):
        _linha(d, [P(x, y) for x, y in _catmull(pts, n=12)], cor, larg)
    if fises:
        cf = cor_fise or cor
        for fy in fises:
            if fy > 0.5:   # fise distal do fêmur
                xa, xb = -0.086, 0.094
                pts = [P(xa + (xb - xa) * i / 10, fy + 0.004 * math.sin(i * 1.25)) for i in range(11)]
            else:          # fise da cabeça femoral (arco no colo)
                pts = [P(hc[0] + hr * 0.95 * math.cos(math.radians(a)),
                         hc[1] + hr * 0.95 * math.sin(math.radians(a)) + 0.010)
                       for a in range(-35, 95, 10)]
            _linha(d, pts, cf, max(1, int(larg * 0.8)))
    return P(*hc)


def heroi(img, tipo, caixa, cor=OURO, cor_osso=CREME):
    """Desenha a ilustração `tipo` ('fixador' | 'eixo') centrada na caixa (x0, y0, x1, y1)."""
    x0, y0, x1, y1 = caixa
    S = 3
    bw, bh = (x1 - x0) * S, (y1 - y0) * S
    ov = Image.new("RGBA", (int(bw), int(bh)), (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    if tipo == "fixador":
        _desenha_fixador(d, bw, bh, S, cor, cor_osso)
    else:
        _desenha_eixo(d, bw, bh, S, cor, cor_osso)
    ov = ov.resize((x1 - x0, y1 - y0), Image.LANCZOS)
    img.alpha_composite(ov, (x0, y0))


def _desenha_fixador(d, bw, bh, S, cor, cor_osso):
    L = min(bh * 0.84, bw / 0.58)
    R, ry = 0.27 * L, 0.27 * L * 0.25
    cx = bw / 2
    oy = (bh - L) / 2 + 0.01 * L
    ox = cx + 0.004 * L
    aneis = [oy + 0.17 * L, oy + 0.42 * L, oy + 0.80 * L]
    vao = (0.565, 0.635)
    lw = int(2.7 * S)
    tras = cor + (120,)
    frente = cor + (255,)
    a_tras, a_frente = (206, 334), (64, 116)

    def pt(a, yr, r=R, rr=ry):
        t = math.radians(a)
        return (cx + r * math.cos(t), yr + rr * math.sin(t))

    def anel(yr, a0, a1, c):
        for r, rr in ((R, ry), (R * 0.89, ry * 0.86)):
            d.arc([cx - r, yr - rr, cx + r, yr + rr], a0, a1, fill=c, width=lw)

    # 1) metade de trás dos anéis + hastes de trás
    for yr in aneis:
        anel(yr, 180, 360, tras)
    ext = 0.05 * L
    for a in a_tras:
        x, _ = pt(a, 0)
        d.line([(x, aneis[0] - ext), (x, aneis[-1] + ext)], fill=tras, width=int(1.8 * S))
    # 2) fios transósseos (cruzam o osso) — finos
    for yr in aneis:
        for a, b in ((168, 348), (196, 16)):
            d.line([pt(a, yr, R * 0.89, ry * 0.86), pt(b, yr, R * 0.89, ry * 0.86)],
                   fill=cor + (150,), width=max(1, int(0.9 * S)))
    # 3) osso (tíbia + fíbula) com o vão do regenerado
    _tibia_fibula(d, ox, oy, L, cor_osso + (245,), int(3.4 * S), vao=vao, cor_vao=cor_osso + (180,))
    # 4) hastes da frente + porcas, metade da frente dos anéis
    for a in a_frente:
        x, _ = pt(a, 0)
        d.line([(x, aneis[0] - ext), (x, aneis[-1] + ext)], fill=frente, width=int(2.4 * S))
    for yr in aneis:
        anel(yr, 0, 180, frente)
        for a in a_frente:
            x, y = pt(a, yr)
            for dy in (-0.017 * L, 0.017 * L):
                d.rectangle([x - 0.013 * L, y + dy - 0.005 * L, x + 0.013 * L, y + dy + 0.005 * L],
                            outline=frente, width=int(1.4 * S))


def _desenha_eixo(d, bw, bh, S, cor, cor_osso):
    Lf = min(bh / 1.92, bw / 0.34)
    Lt = 0.80 * Lf
    gap = 0.035 * Lf
    tot = Lf + gap + Lt * 1.03
    ox = bw / 2 + 0.020 * Lf
    oy = (bh - tot) / 2
    lw = int(3.4 * S)
    c_osso = cor_osso + (245,)
    c_fise = cor + (255,)
    cab = _femur(d, ox, oy, Lf, c_osso, lw, fises=[0.895], cor_fise=c_fise)
    ty = oy + Lf + gap
    _tibia_fibula(d, ox, ty, Lt, c_osso, lw, fises=[0.075, 0.935], cor_fise=c_fise)
    tornozelo = (ox - 0.002 * Lt, ty + 0.966 * Lt)
    # eixo mecânico (quadril -> tornozelo), tracejado dourado, passando pelo joelho
    ext = 0.06 * Lf
    vx, vy = tornozelo[0] - cab[0], tornozelo[1] - cab[1]
    n = math.hypot(vx, vy)
    a = (cab[0] - vx / n * ext, cab[1] - vy / n * ext)
    b = (tornozelo[0] + vx / n * ext, tornozelo[1] + vy / n * ext)
    _pontilhada(d, [a, b], cor + (230,), int(1.4 * S), traco=int(9 * S), vazio=int(7 * S))
    # pontos de referência do eixo (quadril, joelho, tornozelo) — pequenos anéis
    joelho_y = oy + Lf + gap / 2
    t = (joelho_y - a[1]) / (b[1] - a[1])
    joelho = (a[0] + (b[0] - a[0]) * t, joelho_y)
    for (px, py), r in ((cab, 0.016), (joelho, 0.013), (tornozelo, 0.013)):
        rr = r * Lf
        d.ellipse([px - rr, py - rr, px + rr, py + rr], outline=cor + (255,), width=int(1.4 * S))
