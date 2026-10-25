# -*- coding: utf-8 -*-
"""STORY "COMO FUNCIONA EM 3 TOQUES" — gerador movido a DADOS (geração nova, 24/10/2026).

Cada story de `stories_cf.json` vira 3 vídeos curtos SEM VOZ (espanto, mecanismo, significado).
O desenho não é refeito: é um TRECHO em movimento do mp4 JÁ APROVADO do reel COMO FUNCIONA de
origem (sha256 conferido), recortado acima do karaokê e abaixo do gancho do reel, com câmera
(zoom de no máximo 1,25×). Por cima, a moldura fixa da série:
  * fundo azul-petróleo = o MESMO gradiente do reel (cf_alongamento.fundo), calibrado pelo próprio
    mp4 (desloc_do_fundo: o fundo decodificado fica 1–2 níveis abaixo do analítico), sob a mesma
    transformação do recorte (a emenda do recorte com o fundo não aparece);
  * selo COMO FUNCIONA; título de 2 linhas (branca + ouro, contorno); linha de texto curta;
    "toca →" nas telas 1 e 2; na tela 3, corte seco para um cartão limpo com a chamada de envio,
    "Vídeo completo no perfil" e "toque no nome lá em cima ↖";
  * identificação CFM (SIG + aviso) em TODO quadro, desde o quadro 0, tudo dentro de y 270–1580.
Fundo e trecho são compostos com numpy/Pillow (o raster do skia leva ~0,3 s por quadro só no
gradiente); o texto vai em skia, com a tipografia da série (fontes de animado/fontes.py), direto no
mesmo array. As setas → e ↖ são desenhadas como vetor (nem o Segoe UI Bold tem o ↖; o skia não troca
de fonte glifo a glifo). Som: só efeitos e vinheta sintetizados com animado.som, sem voz, ~ -19 LUFS.
Dependências: skia-python, numpy, Pillow, edge-tts (importado por animado.voz) e ffmpeg ≥ 5.1.

Regras que o gerador cobra ANTES de desenhar (falha ALTO, nada é gravado):
  formato, chamada de envio, DM/contato, tema e CFM pelo próprio checar_stories (problemas_do_texto);
  limites da série (texto ≤ 70, chamada ≤ 60, tela 1 sem linha); trecho da tela 1 terminando ≥ 0,2 s
  antes de `resposta_no_reel_em`; zoom em [1, 1,25]; âncora e `foco_x` dentro do recorte; linha na
  tela ≥ 1 s + 0,35 s por palavra antes de sair e a chamada idem no cartão;
  rótulos queimados do reel que entram no recorte ⊆ textos_tela do irmão do reel;
  sha256 do mp4 do reel (o de reels.json) igual ao fixado em `reel_sha256`;
  com STORY_FONTES_EXIGIDAS=<prefixo> (o render-stories.yml usa 'Roboto-'), toda fonte escolhida
  começa pelo prefixo — runner sem Roboto não cai calado na reserva DejaVu.
E DEPOIS de desenhar: o MESMO cheque do portão (checar_stories.problemas_de_desenho: nada A MAIS,
nada A MENOS — as 2 linhas do título, o texto inteiro e a chamada inteira na tela 3 —, identificação
em toda tela, "Vídeo completo no perfil" na tela 3) mais a quebra exata do desenho (esperados) e o
vídeo com a duração certa.
Só então os 3 mp4 e o irmão `stories_cf/<id>.json` (o que checar_stories.py confere) são gravados;
o irmão leva hash_story, hash_gerador, hash_render (trecho/crop/câmera/tempos), as fontes e o
sha256 de cada vídeo.

Uso:
  python story_cf.py <id> [<id> ...]           renderiza stories_cf/<id>_{1,2,3}.mp4 + stories_cf/<id>.json
  python story_cf.py --todos                   as stories da fila que PRECISAM de render: pula as já
                                               publicadas inteiras e as de render em dia (--forcar
                                               re-renderiza essas também). Uma recusa não aborta as
                                               outras: renderiza as válidas, lista as recusadas e sai ≠ 0
  python story_cf.py ... --lista-ok ARQ        grava em ARQ os ids renderizados com sucesso (um por linha)
  python story_cf.py <id> --previa [--pasta D] só PNGs de conferência (quadro 0, meio e fim de cada
                                               tela + tela 2 SEM TEXTO) e o mosaico; não grava vídeo
  python story_cf.py --folha <reel_id> [--pasta D]   folha de contato do reel a cada 1 s
"""
import argparse
import datetime as dt
import hashlib
import json
import math
import os
import subprocess
import sys
import tempfile

sys.dont_write_bytecode = True                 # não deixar .pyc dentro de animado/ (motor aprovado)
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)

import numpy as np  # noqa: E402
import skia  # noqa: E402
from PIL import Image  # noqa: E402

import checar_stories as CS  # noqa: E402
from animado import fontes, som  # noqa: E402
from animado.base import FPS, H, W, CanvasRegistrador  # noqa: E402
from animado.cf_alongamento import BG_IN, BG_OUT, OURO, C, clamp, e_back, e_inout, e_out, lerp, prog  # noqa: E402
from animado.voz import ffmpeg  # noqa: E402

PASTA_SAIDA = os.path.join(ROOT, CS.PASTA)
PREVIA_PADRAO = os.path.join(ROOT, ".animado_tmp", "story_cf_previa")

# ------------------------------------------------------------------ geometria (1080 x 1920)
ZONA_UTIL = (270, 1580)                        # nada essencial fora daqui (interface do Instagram)
LARG_MAX = 864                                 # 960 úteis − 10% de folga (Segoe aqui, Roboto no runner)
SELO_Y0, SELO_Y1 = 286, 338
TIT_Y1 = 428                                   # linha de base da 1ª linha do título
TIT_TAM_MAX, TIT_TAM_MIN = 84, 60
CAIXA = (40, 550, 1040, 1366)                  # onde o trecho do reel é encaixado (x0, y0, x1, y1)
TXT_TAM, TXT_Y1, TXT_Y2 = 40, 1416, 1464       # linha de texto: 1 linha em TXT_Y1+18, 2 linhas em Y1/Y2
TOCA_TAM, TOCA_X1, TOCA_Y = 40, 990, 1340      # "toca →": canto inferior direito da caixa (pílula até
                                               # x ~1008: longe da borda que some em tela que corta as laterais)
ROD_Y1, ROD_Y2 = 1530, 1564                    # identificação CFM (≥ 22 px; dentro da zona útil)
CTA_TAM_MAX, CTA_TAM_MIN = 86, 60
LIM_TEXTO_SERIE, LIM_CTA_SERIE = 70, 60        # a regra da série (o portão aceita mais)
ZOOM_MAX = 1.25                                # acima disso o mp4 borra
FOLGA_RESPOSTA = 0.2
SEG_POR_PALAVRA = 0.35                         # a linha fica na tela ≥ 1 s + 0,35 s por palavra antes de
SEG_LEITURA_BASE = 1.0                         # sair (tela 3: até o cartão; tela 2: até o fim); o cartão
                                               # fica o mesmo tempo para a chamada. Leitor frio (24/10):
                                               # o aviso de 8 palavras em 2,4 s "quase passa batido".

TF = {p: fontes.fonte(p) for p in ("black", "bold", "semi", "reg")}


def fonte_arquivo(papel):
    """Arquivo de fonte que animado.fontes escolheu para o papel (vai para o irmão: Segoe = PC)."""
    for nome in fontes.CANDIDATOS[papel]:
        caminho = fontes._achar(nome)
        if caminho and skia.Typeface.MakeFromFile(caminho) is not None:
            return os.path.basename(caminho)
    return None


# ------------------------------------------------------------------ desenho: utilidades
def tinta(cor, a=255, estilo="fill", w=0):
    p = skia.Paint(AntiAlias=True)
    p.setColor(C(cor, max(0, min(255, int(a)))))
    if estilo == "stroke":
        p.setStyle(skia.Paint.kStroke_Style); p.setStrokeWidth(w)
        p.setStrokeCap(skia.Paint.kRound_Cap); p.setStrokeJoin(skia.Paint.kRound_Join)
    return p


def _fonte(papel, tam):
    f = skia.Font(TF[papel], tam); f.setEdging(skia.Font.Edging.kAntiAlias); f.setSubpixel(True)
    return f


_GLIFOS_OK = set()


def conferir_glifos(s, papel):
    """Falha ALTO se a fonte não tem glifo para algum caractere (sairia quadradinho no ar)."""
    if (papel, s) in _GLIFOS_OK:
        return
    ids = _fonte(papel, 40).textToGlyphs(s)
    faltam = [ch for ch, g in zip(s, ids) if g == 0 and not ch.isspace()]
    if faltam:
        raise SystemExit(f"ERRO: a fonte '{papel}' ({TF[papel].getFamilyName()}) não tem glifo para {faltam} "
                         f"em {s!r} — o vídeo sairia com quadradinho.")
    _GLIFOS_OK.add((papel, s))


def larg(s, papel, tam):
    return _fonte(papel, tam).measureText(s)


def escrever(cv, s, x, y, papel, tam, cor, a=255, alinhar="c", contorno=0):
    """Texto da série (o canvas registrador anota a string). alinhar: c | e | d."""
    conferir_glifos(s, papel)
    f = _fonte(papel, tam); w = f.measureText(s)
    x0 = x - w / 2 if alinhar == "c" else (x - w if alinhar == "d" else x)
    if a > 0:
        if contorno:
            cv.drawString(s, x0, y, f, tinta("#000000", a * 0.85, "stroke", contorno))
        cv.drawString(s, x0, y, f, tinta(cor, a))
    return w


def seta(cv, x, y, tam, cor, a, direcao):
    """Seta vetorial do tamanho de um glifo: '→' a partir de (x, linha de base) ou '↖'."""
    p = tinta(cor, a, "stroke", max(3.0, tam * 0.11))
    meio = y - tam * 0.34; L = tam * 0.78; c = tam * 0.30
    if direcao == "→":
        cv.drawLine(x, meio, x + L, meio, p)
        cv.drawLine(x + L, meio, x + L - c, meio - c, p); cv.drawLine(x + L, meio, x + L - c, meio + c, p)
        return L
    # '↖': ponta em cima à esquerda
    x0, y0, x1, y1 = x + tam * 0.08, meio - L / 2, x + tam * 0.08 + L * 0.8, meio + L / 2 * 0.8
    cv.drawLine(x1, y1, x0, y0, p)
    cv.drawLine(x0, y0, x0 + c * 1.15, y0, p); cv.drawLine(x0, y0, x0, y0 + c * 1.15, p)
    return L * 0.8 + tam * 0.08


def generico_com_seta(cv, rotulo, x, y, papel, tam, cor, a=255, alinhar="c"):
    """Texto genérico terminado em seta (TOCA, NOME): o texto vai em glifos e a seta em vetor; o
    registrador anota a string INTEIRA do portão (é ela que o público lê)."""
    assert rotulo in (CS.TOCA, CS.NOME), rotulo
    corpo, direcao = rotulo[:-2], rotulo[-1]
    conferir_glifos(corpo, papel)
    esp = larg(" ", papel, tam); wt = larg(corpo, papel, tam); ws = tam * 0.86
    total = wt + esp + ws
    x0 = x - total / 2 if alinhar == "c" else (x - total if alinhar == "d" else x)
    if a <= 0:
        return total, x0
    getattr(cv, "registra", lambda _s: None)(rotulo)
    real = getattr(cv, "real", cv)
    real.drawString(corpo, x0, y, _fonte(papel, tam), tinta(cor, a))
    seta(real, x0 + wt + esp, y, tam, cor, a, direcao)
    return total, x0


def quebrar(texto, papel, tam, larg_max, max_linhas):
    """Quebra em até max_linhas trechos CONTÍNUOS do texto (o portão aceita linha quebrada)."""
    pal = texto.split()
    if larg(texto, papel, tam) <= larg_max or len(pal) == 1:
        return [" ".join(pal)]
    melhor = None
    if max_linhas >= 2:
        for i in range(1, len(pal)):
            ls = [" ".join(pal[:i]), " ".join(pal[i:])]
            m = max(larg(x, papel, tam) for x in ls)
            if melhor is None or m < melhor[0]:
                melhor = (m, ls)
    if max_linhas >= 3 and (melhor is None or melhor[0] > larg_max):
        for i in range(1, len(pal)):
            for j in range(i + 1, len(pal)):
                ls = [" ".join(pal[:i]), " ".join(pal[i:j]), " ".join(pal[j:])]
                m = max(larg(x, papel, tam) for x in ls)
                if m < melhor[0]:
                    melhor = (m, ls)
    return melhor[1]


# ------------------------------------------------------------------ o reel: trecho decodificado
class Trecho:
    """Só o trecho [t0, t1) do mp4 do reel, já recortado, lido do ffmpeg quadro a quadro (RGB)."""

    def __init__(self, mp4, t0, t1, crop):
        self.mp4, self.t0 = mp4, t0
        self.x, self.y, self.w, self.h = (int(round(v)) for v in crop)
        self.n = int(round((t1 - t0) * FPS))
        self.proc = None; self.err = None; self.k = -1; self.buf = None; self.img = None; self.img_k = None
        self.desloc = None                         # desloc_do_fundo (medido uma vez por tela)

    def _abrir(self):
        self.fechar()
        # -ss no instante EXATO do quadro (k/30 s) e -fps_mode passthrough: com o -ss fora da grade
        # (ou sem passthrough) o ffmpeg DUPLICA o 1º quadro e o trecho inteiro sai 1 quadro atrasado.
        # format=rgb24 ANTES do crop: em yuv420p o crop arredonda y/altura ímpares para par e o
        # quadro sai com 1 linha a menos (leitura desalinhada).
        cmd = [ffmpeg(), "-v", "error", "-ss", f"{round(self.t0 * FPS) / FPS:.6f}", "-i", self.mp4,
               "-frames:v", str(self.n), "-fps_mode", "passthrough",
               "-vf", f"format=rgb24,crop={self.w}:{self.h}:{self.x}:{self.y}",
               "-f", "rawvideo", "-pix_fmt", "rgb24", "-"]
        self.err = tempfile.TemporaryFile()
        self.proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=self.err)
        self.k = -1

    def quadro(self, k):
        """Quadro k do trecho (k além do fim = o último quadro, segurado). -> PIL RGB."""
        k = max(0, min(self.n - 1, k))
        if self.proc is None or k < self.k:
            self._abrir()
        tam = self.w * self.h * 3
        while self.k < k:
            b = self.proc.stdout.read(tam)
            if len(b) < tam:
                self.proc.wait(); self.err.seek(0)
                msg = self.err.read().decode("utf-8", "replace").strip()[-400:]
                raise SystemExit(f"ERRO: {self.mp4} acabou no quadro {self.k + 1} de {self.n} do trecho "
                                 f"(t0={self.t0}) — trecho fora do vídeo? {msg}")
            self.buf = b; self.k += 1
        if self.img_k != self.k:
            self.img = Image.frombuffer("RGB", (self.w, self.h), self.buf, "raw", "RGB", 0, 1)
            self.img_k = self.k
        return self.img

    def fechar(self):
        if self.proc is not None:
            try:
                self.proc.stdout.close()
            except OSError:
                pass
            if self.proc.poll() is None:
                self.proc.kill()
            self.proc.wait(); self.proc = None
        if self.err is not None:
            self.err.close(); self.err = None


def zoom_em(tela, tau):
    kf = tela.get("zoom", 1.0)
    if isinstance(kf, (int, float)):
        return float(kf)
    if tau <= kf[0][0]:
        return float(kf[0][1])
    for (ta, za), (tb, zb) in zip(kf, kf[1:]):
        if tau <= tb:
            return lerp(za, zb, e_inout(prog(tau, ta, tb)))
    return float(kf[-1][1])


def saida_do_recorte(tela):
    """(x, y, w, h) inteiros da story onde o recorte inteiro (zoom 1) é encaixado, centrado na CAIXA.
    A caixa não se move: o zoom acontece DENTRO dela (câmera). Com `foco_x` (um x do REEL), o
    recorte desliza na horizontal para esse x cair no meio da story (W/2), sem sair da CAIXA: serve
    quando o recorte tira um rótulo de um lado e o objeto que muda ficaria encostado na borda."""
    bx, by, bw, bh = tela["crop"]
    cx0, cy0, cx1, cy1 = CAIXA
    s0 = min((cx1 - cx0) / bw, (cy1 - cy0) / bh)
    ow, oh = int(round(bw * s0)), int(round(bh * s0))
    dx = int(round((cx0 + cx1) / 2 - ow / 2))
    if tela.get("foco_x") is not None:
        dx = max(cx0, min(cx1 - ow, int(round(W / 2 - (tela["foco_x"] - bx) * s0))))
    return dx, int(round(cy0 + (cy1 - cy0 - oh) / 2)), ow, oh


def janela(tela, tau):
    """Janela do quadro do reel vista no instante tau: o recorte dividido pelo zoom, com a âncora
    parada no mesmo lugar da tela (zoom em torno da âncora)."""
    bx, by, bw, bh = tela["crop"]
    z = zoom_em(tela, tau)
    ax, ay = tela.get("ancora") or (bx + bw / 2, by + bh / 2)
    return ax - (ax - bx) / z, ay - (ay - by) / z, bw / z, bh / z


def _rgb(h):
    return np.array([int(h[i:i + 2], 16) for i in (1, 3, 5)], np.float32)


_C_IN, _C_OUT = _rgb(BG_IN), _rgb(BG_OUT)
_GRAD, _MASC = {}, {}


def gradiente(cx, cy, raio, desloc=(0.0, 0.0, 0.0)):
    """O fundo azul-petróleo do COMO FUNCIONA (gradiente radial BG_IN -> BG_OUT de
    cf_alongamento.fundo), com centro e raio já na story. Liso: calculado a 1/4 e ampliado.
    `desloc` = o quanto o mp4 do reel, decodificado, fica abaixo/acima do gradiente analítico
    (medido por desloc_do_fundo); somado aqui, a emenda do recorte com o fundo some."""
    chave = (round(cx * 2) / 2, round(cy * 2) / 2, round(raio * 2) / 2, tuple(desloc))
    img = _GRAD.get(chave)
    if img is None:
        if len(_GRAD) > 16:
            _GRAD.clear()
        q = 4
        xs = (np.arange(W // q, dtype=np.float32) + 0.5) * q - 0.5
        ys = (np.arange(H // q, dtype=np.float32) + 0.5) * q - 0.5
        d = np.sqrt((ys[:, None] - chave[1]) ** 2 + (xs[None, :] - chave[0]) ** 2) / chave[2]
        np.clip(d, 0, 1, out=d)
        rgb = _C_IN + (_C_OUT - _C_IN) * d[..., None] + np.asarray(desloc, np.float32)
        img = Image.fromarray(np.clip(rgb + 0.5, 0, 255).astype(np.uint8), "RGB").resize((W, H), Image.BILINEAR)
        _GRAD[chave] = img
    return img


def desloc_do_fundo(tela, trecho):
    """Diferença (R, G, B) entre o fundo do mp4 do reel decodificado e o gradiente analítico do
    cf_alongamento.fundo: o raster do skia + o yuv420p do reel deixam o fundo ~1–2 níveis abaixo
    (medido: −1, −2, 0 nos dois reels), e um degrau desses desenha o retângulo do recorte num
    quadro escuro. Medida no anel de 8 px da borda do recorte (só pixels de fundo: |dif| < 6) em 3
    quadros do trecho; mediana, em passos de 0,5, limitada a ±4. Constante por tela (sem tremular)."""
    if trecho.desloc is not None:
        return trecho.desloc
    bx, by = tela["crop"][0], tela["crop"][1]
    amostras = []
    for k in sorted({0, trecho.n // 2, trecho.n - 1}):
        a = np.asarray(trecho.quadro(k), np.float32); h, w = a.shape[:2]; b = 8
        anel = np.zeros((h, w), bool); anel[:b] = anel[-b:] = True; anel[:, :b] = anel[:, -b:] = True
        yy, xx = np.nonzero(anel)
        cy = H * 0.42 + 40 * math.sin((tela["trecho"][0] + k / FPS) * 0.3)
        d = np.clip(np.hypot(xx + bx - W / 2, yy + by - cy) / (H * 0.78), 0, 1)
        res = a[yy, xx] - (_C_IN + (_C_OUT - _C_IN) * d[:, None])
        amostras.append(res[np.abs(res).max(1) < 6])
    res = np.concatenate(amostras)
    trecho.desloc = ((0.0, 0.0, 0.0) if len(res) < 500 else
                     tuple(float(v) for v in np.clip(np.round(np.median(res, 0) * 2) / 2, -4, 4)))
    return trecho.desloc


def mascara(ow, oh, esmaecer):
    """Bordas do recorte que esmaecem no fundo ([topo, direita, base, esquerda] em px da story)."""
    esm = tuple(int(v) for v in (esmaecer or (0, 0, 0, 0)))
    if not any(esm):
        return None
    chave = (ow, oh, esm)
    if chave not in _MASC:
        topo, dir_, base, esq = esm
        a = np.ones((oh, ow), np.float32)
        yy = np.arange(oh, dtype=np.float32)[:, None] + 0.5
        xx = np.arange(ow, dtype=np.float32)[None, :] + 0.5
        if topo:
            a = np.minimum(a, np.clip(yy / topo, 0, 1))
        if base:
            a = np.minimum(a, np.clip((oh - yy) / base, 0, 1))
        if esq:
            a = np.minimum(a, np.clip(xx / esq, 0, 1))
        if dir_:
            a = np.minimum(a, np.clip((ow - xx) / dir_, 0, 1))
        a = a * a * (3 - 2 * a)                                  # rampa suave
        _MASC[chave] = Image.fromarray((a * 255 + 0.5).astype(np.uint8), "L")
    return _MASC[chave]


def fundo_com_trecho(tela, tau, trecho):
    """PIL RGB 1080x1920: o fundo do reel estendido à story inteira, sob a MESMA transformação do
    recorte (a emenda não aparece), e o quadro do trecho na janela da câmera."""
    k = int(math.floor(tau * FPS + 1e-6))
    desloc = desloc_do_fundo(tela, trecho)
    img = trecho.quadro(k)
    t_reel = tela["trecho"][0] + min(k, trecho.n - 1) / FPS
    dx, dy, ow, oh = saida_do_recorte(tela)
    vx, vy, vw, vh = janela(tela, tau)
    s = ow / vw
    # cf_alongamento.fundo: centro (W/2, 0,42 H + 40 sen(0,3 t)), raio 0,78 H — no tempo do REEL
    cx = dx + (W / 2 - vx) * s
    cy = dy + (H * 0.42 + 40 * math.sin(t_reel * 0.3) - vy) * s
    bg = gradiente(cx, cy, H * 0.78 * s, desloc).copy()
    bx, by = tela["crop"][0], tela["crop"][1]
    caixa = (max(0.0, vx - bx), max(0.0, vy - by), min(float(trecho.w), vx - bx + vw), min(float(trecho.h), vy - by + vh))
    bg.paste(img.resize((ow, oh), Image.BICUBIC, box=caixa), (dx, dy), mascara(ow, oh, tela.get("esmaecer")))
    return bg


# ------------------------------------------------------------------ moldura da série
def selo(cv):
    tam = 34; trk = 4
    w = larg(CS.SELO, "black", tam) + trk * (len(CS.SELO) - 1)
    rr = skia.RRect.MakeRectXY(skia.Rect(W / 2 - w / 2 - 30, SELO_Y0, W / 2 + w / 2 + 30, SELO_Y1), 26, 26)
    cv.drawRRect(rr, tinta("#FFFFFF", 28))
    conferir_glifos(CS.SELO, "black")
    getattr(cv, "registra", lambda _s: None)(CS.SELO)
    real = getattr(cv, "real", cv); f = _fonte("black", tam); x = W / 2 - w / 2
    for ch in CS.SELO:                                   # espaçamento de letra do selo do reel
        real.drawString(ch, x, SELO_Y1 - 13, f, tinta(OURO, 255)); x += f.measureText(ch) + trk


def rodape(cv):
    escrever(cv, CS.SIG, W / 2, ROD_Y1, "semi", 28, "#FFFFFF", 220)
    escrever(cv, CS.DISC_ST, W / 2, ROD_Y2, "reg", 24, "#FFFFFF", 185)


def tam_titulo(st):
    """Um tamanho só para os títulos da story (série), cabendo com folga."""
    tam = TIT_TAM_MAX
    for t in st["telas"]:
        for s in t["titulo"]:
            tam = min(tam, LARG_MAX * 100 / larg(s, "black", 100))
    return math.floor(tam)


def titulo(cv, linhas, tam, esc=1.0, a=255):
    if a <= 0:
        return
    y2 = TIT_Y1 + tam * 1.08
    cy = (TIT_Y1 + y2) / 2 - tam * 0.35
    cv.save(); cv.translate(W / 2, cy); cv.scale(esc, esc); cv.translate(-W / 2, -cy)
    escrever(cv, linhas[0], W / 2, TIT_Y1, "black", tam, "#FFFFFF", a, contorno=10)
    escrever(cv, linhas[1], W / 2, y2, "black", tam, OURO, a, contorno=10)
    cv.restore()


def linha_texto(cv, texto, a=255, dy=0.0):
    if not texto or a <= 0:
        return
    ls = quebrar(texto, "bold", TXT_TAM, LARG_MAX, 2)
    ys = [TXT_Y1 + 18] if len(ls) == 1 else [TXT_Y1, TXT_Y2]
    for s, y in zip(ls, ys):
        escrever(cv, s, W / 2, y + dy, "bold", TXT_TAM, "#FFFFFF", a, contorno=6)


def toca(cv, tau, t0):
    a = 255 * e_out(prog(tau, t0, t0 + 0.3))
    if a <= 0:
        return
    total = larg("toca", "bold", TOCA_TAM) + larg(" ", "bold", TOCA_TAM) + TOCA_TAM * 0.86
    x0 = TOCA_X1 - total
    rr = skia.RRect.MakeRectXY(skia.Rect(x0 - 20, TOCA_Y - 40, TOCA_X1 + 18, TOCA_Y + 15), 27, 27)
    cv.drawRRect(rr, tinta("#0B1824", a * 0.78))
    empurra = 5 * (0.5 - 0.5 * math.cos(2 * math.pi * max(0.0, tau - t0) / 1.1))
    generico_com_seta(cv, CS.TOCA, x0 + empurra, TOCA_Y, "bold", TOCA_TAM, "#FFFFFF", a, alinhar="e")


def tam_cta(cta):
    """(tamanho, linhas) da chamada em caixa alta: 2 linhas equilibradas; 3 se ficar pequena."""
    cta = cta.upper()
    ls = quebrar(cta, "black", CTA_TAM_MAX, LARG_MAX, 2)
    tam = min(CTA_TAM_MAX, LARG_MAX * CTA_TAM_MAX / max(larg(s, "black", CTA_TAM_MAX) for s in ls))
    if tam < CTA_TAM_MIN:
        ls = quebrar(cta, "black", CTA_TAM_MIN, LARG_MAX, 3)
        tam = min(CTA_TAM_MAX, LARG_MAX * CTA_TAM_MIN / max(larg(s, "black", CTA_TAM_MIN) for s in ls))
    return math.floor(tam), ls


def cartao(cv, st, tela, tau):
    """Cartão final da tela 3: limpo e opaco, a chamada de envio em letras grandes e o caminho
    real até o perfil no story. Sem caixa com cara de botão, nada perto do botão nativo."""
    tam, ls = tam_cta(st["cta"])
    k = tau - tela["t_cartao"]
    esc = lerp(1.12, 1.0, e_out(clamp(k / 0.18)))
    passo = tam * 1.12
    y0 = 860 - (len(ls) - 1) * passo / 2
    cy = y0 + (len(ls) - 1) * passo / 2 - tam * 0.35
    cv.save(); cv.translate(W / 2, cy); cv.scale(esc, esc); cv.translate(-W / 2, -cy)
    for i, s in enumerate(ls):
        escrever(cv, s, W / 2, y0 + i * passo, "black", tam, "#FFFFFF" if i % 2 == 0 else OURO,
                 255 * clamp((k + 1 / FPS) / 0.1), contorno=10)
    cv.restore()
    yb = y0 + (len(ls) - 1) * passo + 150
    a1 = 255 * e_out(prog(tau, tela["t_perfil"], tela["t_perfil"] + 0.3))
    a2 = 255 * e_out(prog(tau, tela["t_nome"], tela["t_nome"] + 0.3))
    escrever(cv, CS.PERFIL, W / 2, yb, "bold", 48, "#FFFFFF", a1)
    generico_com_seta(cv, CS.NOME, W / 2, yb + 64, "semi", 40, "#C9D6E2", a2)


# ------------------------------------------------------------------ uma tela = um vídeo
def moldura(cv, st, tela, tau, tam_tit, no_cartao, sem_texto=False):
    """Todo o texto da story (o canvas registrador anota cada string) + a identificação CFM."""
    papel = tela["papel"]
    if no_cartao:
        cartao(cv, st, tela, tau)
        selo(cv)
        rodape(cv)
        return
    if not sem_texto:
        selo(cv)
        if papel == "espanto":
            titulo(cv, tela["titulo"], tam_tit)
        elif papel == "mecanismo":                      # a resposta CARIMBA no lugar da pergunta
            kk = tau - tela["t_titulo"]
            if kk >= 0:
                titulo(cv, tela["titulo"], tam_tit, lerp(1.15, 1.0, e_out(clamp(kk / 0.16))),
                       255 * clamp((kk + 1 / FPS) / 0.1))
        else:                                           # significado: o sentido na vida real
            kk = tau - tela["t_titulo"]
            if kk >= 0:
                titulo(cv, tela["titulo"], tam_tit, lerp(0.9, 1.0, e_back(clamp(kk / 0.28))),
                       255 * clamp((kk + 1 / FPS) / 0.14))
        if tela.get("texto") and "t_texto" in tela:
            kt = prog(tau, tela["t_texto"], tela["t_texto"] + 0.25)
            linha_texto(cv, tela["texto"], 255 * e_out(kt), 14 * (1 - e_out(kt)))
        if "t_toca" in tela:
            toca(cv, tau, tela["t_toca"])
    rodape(cv)


class Quadro:
    """Quadro da story sobre um array numpy RGBA. O fundo e o trecho do reel entram por
    numpy/Pillow (o raster do skia leva ~0,3 s só para preencher 1080x1920 com o gradiente) e o
    texto por skia, desenhado direto no mesmo array."""

    def __init__(self):
        self.buf = np.empty((H, W, 4), np.uint8); self.buf[..., 3] = 255
        self.surf = skia.Surface(self.buf, colorType=skia.ColorType.kRGBA_8888_ColorType,
                                 alphaType=skia.AlphaType.kPremul_AlphaType)

    def desenhar(self, st, tela, tau, trecho, tam_tit, registro=None, sem_texto=False):
        no_cartao = tela["papel"] == "significado" and tau >= tela["t_cartao"]
        bg = gradiente(W / 2, H * 0.42, H * 0.78) if no_cartao else fundo_com_trecho(tela, tau, trecho)
        self.buf[..., :3] = np.asarray(bg)
        cv = self.surf.getCanvas()
        moldura(CanvasRegistrador(cv, registro) if registro is not None else cv, st, tela, tau, tam_tit,
                no_cartao, sem_texto)
        return self.buf


def eventos_de_som(tela):
    p = tela["papel"]
    if p == "espanto":
        return [(0.0, "vinheta", 1.0)]
    ev = [(0.0, "whoosh", 0.55)]
    if p == "mecanismo":
        ev += [(tela["t_titulo"], "thump", 0.9), (tela["t_texto"], "ping", 0.45)]
    else:
        ev += [(tela["t_titulo"], "pop", 0.9), (tela["t_texto"], "ping", 0.45), (tela["t_cartao"], "ding", 0.65)]
    return ev


def vinheta():
    """Assinatura sonora da série: 3 notas (dó–mi–sol), igual em toda edição, no timbre do ding
    de animado.som (mesmo envelope, mesmas parciais)."""
    sr = som.SR; n = int(1.3 * sr); y = np.zeros(n)
    for k, f in enumerate((1046.5, 1318.5, 1568.0)):
        ini = int(k * 0.12 * sr); m = n - ini; t = np.arange(m) / sr
        y[ini:] += sum(np.sin(2 * np.pi * ff * t) * g for ff, g in ((f, .5), (2 * f, .18), (3 * f, .07))) * som._env(m, 0.002, 0.30)
    return y * 0.55


# Volume moderado: ~ -19 LUFS (o reel narrado vai a -14) e pico ~ -1 dBFS, medidos com ebur128.
G_TRILHA, G_FX, GANHO, TETO = 0.50, 0.55, 1.4, 0.89


def mixar(dur, eventos):
    """Trilha baixa + efeitos, SEM voz. Sem loudnorm (num clipe curto e esparso ele bombeia a
    trilha): ganho fixo e limitador suave (tanh), igual em toda edição."""
    n = int(round(dur * som.SR))
    mus = np.zeros(n); tr = som.trilha(dur); mus[:min(n, len(tr))] = tr[:n]
    fx = np.zeros(n)
    for t0, nome, g in eventos:
        s = vinheta() if nome == "vinheta" else som.SFX[nome]()
        p = int(t0 * som.SR)
        if 0 <= p < n:
            m = min(len(s), n - p); fx[p:p + m] += s[:m] * g
    x = (mus * G_TRILHA + fx * G_FX) * GANHO
    return np.tanh(x / TETO) * TETO


def codificar(st, tela, mp4, wav, tam_tit, registro):
    dur = float(tela["dur"]); n = int(round(dur * FPS))
    cmd = [ffmpeg(), "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgba", "-s", f"{W}x{H}", "-r", str(FPS),
           "-i", "-", "-i", wav, "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-pix_fmt", "yuv420p",
           "-profile:v", "high", "-c:a", "aac", "-b:a", "128k", "-ar", "48000", "-ac", "2", "-shortest",
           "-movflags", "+faststart", mp4]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    trecho = Trecho(reel_mp4(st), tela["trecho"][0], tela["trecho"][1], tela["crop"])
    q = Quadro()
    try:
        for i in range(n):
            proc.stdin.write(q.desenhar(st, tela, i / FPS, trecho, tam_tit, registro).tobytes())
    finally:
        trecho.fechar()
        proc.stdin.close()
    if proc.wait() != 0:
        raise SystemExit(f"ERRO: ffmpeg falhou ao codificar {mp4}")
    return trecho.desloc or (0.0, 0.0, 0.0)


# ------------------------------------------------------------------ dados e conferências
def carregar_fila():
    fila = CS.carregar(CS.FILA, None)
    if not isinstance(fila, list):
        raise SystemExit(f"ERRO: {CS.FILA} ausente ou não é uma lista")
    return fila


def reels_por_id():
    return {r["id"]: r for r in CS.carregar(os.path.join(ROOT, "reels.json"), [])}


def reel_de(st):
    r = reels_por_id().get(st["reel_ref"])
    if r is None or not r.get("video"):
        raise SystemExit(f"ERRO: {st['id']}: reel_ref {st['reel_ref']!r} não está no reels.json (ou sem vídeo)")
    return r


def reel_mp4(st):
    return os.path.join(ROOT, reel_de(st)["video"].replace("/", os.sep))


def _sha(h):
    return h if str(h).startswith("sha256:") else f"sha256:{h}"


def conferir(st):
    """Tudo o que impede o render, ANTES do primeiro quadro. Lista vazia = pode desenhar."""
    texto = CS.problemas_do_texto(st)                  # formato, chamada, tema, DM/contato, CFM
    p = [m for _, m in texto]
    if any(t == "formato" for t, _ in texto):
        return p
    sid = st["id"]
    if len(st["cta"]) > LIM_CTA_SERIE:
        p.append(f"{sid}: chamada com {len(st['cta'])} > {LIM_CTA_SERIE} caracteres (regra da série)")
    for t in st["telas"]:
        nome = f"{sid}/{t['papel']}"
        if len(t.get("texto") or "") > LIM_TEXTO_SERIE:
            p.append(f"{nome}: texto com {len(t['texto'])} > {LIM_TEXTO_SERIE} caracteres (regra da série)")
        if t["papel"] == "espanto" and (t.get("texto") or "").strip():
            p.append(f"{nome}: a tela 1 não leva linha de texto (só a pergunta)")
        if not (CS.DUR_MIN <= float(t.get("dur") or 0) <= CS.DUR_MAX):
            p.append(f"{nome}: dur {t.get('dur')} fora de {CS.DUR_MIN}-{CS.DUR_MAX}s")
        obrig = {"espanto": ["t_toca"], "mecanismo": ["t_titulo", "t_texto", "t_toca"],
                 "significado": ["t_titulo", "t_texto", "t_cartao", "t_perfil", "t_nome"]}[t["papel"]]
        for chave in obrig:
            if not isinstance(t.get(chave), (int, float)) or not 0 <= t[chave] < float(t.get("dur") or 0):
                p.append(f"{nome}: {chave} ausente ou fora da duração da tela")
        kf = t.get("zoom", 1.0)
        zs = [kf] if isinstance(kf, (int, float)) else [z for _, z in kf]
        if any(not (1.0 <= z <= ZOOM_MAX) for z in zs):
            p.append(f"{nome}: zoom {zs} fora de [1, {ZOOM_MAX}] (acima borra; abaixo mostraria fora do recorte)")
        if not isinstance(kf, (int, float)) and [x for x, _ in kf] != sorted(x for x, _ in kf):
            p.append(f"{nome}: chaves de zoom fora de ordem")
        cr = t["crop"]; ax, ay = t.get("ancora") or (cr[0] + cr[2] / 2, cr[1] + cr[3] / 2)
        if not (cr[0] <= ax <= cr[0] + cr[2] and cr[1] <= ay <= cr[1] + cr[3]):
            p.append(f"{nome}: âncora {t.get('ancora')} fora do recorte")
        fx = t.get("foco_x")
        if fx is not None and not (isinstance(fx, (int, float)) and cr[0] <= fx <= cr[0] + cr[2]):
            p.append(f"{nome}: foco_x {fx} fora do recorte (x {cr[0]}–{cr[0] + cr[2]} do reel)")
        # a linha tem de ficar na tela tempo de ser lida: ≥ SEG_LEITURA_BASE + SEG_POR_PALAVRA por
        # palavra até sair (tela 3: o cartão corta; tela 2: o fim do vídeo); a chamada, idem no cartão;
        # e os tempos da tela em ordem
        if t.get("texto") and isinstance(t.get("t_texto"), (int, float)):
            sai = t.get("t_cartao") if t["papel"] == "significado" else t.get("dur")
            precisa = SEG_LEITURA_BASE + SEG_POR_PALAVRA * len(t["texto"].split())
            if isinstance(sai, (int, float)) and sai - t["t_texto"] < precisa - 1e-6:
                p.append(f"{nome}: a linha fica {sai - t['t_texto']:.2f}s na tela, precisa de ≥ {precisa:.2f}s "
                         f"({SEG_LEITURA_BASE}s + {SEG_POR_PALAVRA}s × {len(t['texto'].split())} palavras)")
        if t["papel"] == "significado" and isinstance(t.get("t_cartao"), (int, float)) and st.get("cta"):
            precisa = SEG_LEITURA_BASE + SEG_POR_PALAVRA * len(st["cta"].split())
            fica = float(t.get("dur") or 0) - t["t_cartao"]
            if fica < precisa - 1e-6:
                p.append(f"{nome}: a chamada fica {fica:.2f}s no cartão, precisa de ≥ {precisa:.2f}s "
                         f"({SEG_LEITURA_BASE}s + {SEG_POR_PALAVRA}s × {len(st['cta'].split())} palavras)")
        ordem = [k for k in ("t_titulo", "t_texto", "t_cartao", "t_perfil", "t_nome") if isinstance(t.get(k), (int, float))]
        if [t[k] for k in ordem] != sorted(t[k] for k in ordem):
            p.append(f"{nome}: tempos fora de ordem ({', '.join(f'{k}={t[k]}' for k in ordem)})")
    # nada cortado: título, linha (até 2 linhas) e chamada cabem na largura útil com a folga
    if tam_titulo(st) < TIT_TAM_MIN:
        p.append(f"{sid}: título só caberia com {tam_titulo(st)} px (< {TIT_TAM_MIN}): encurte a linha mais larga")
    for t in st["telas"]:
        if t.get("texto"):
            ls = quebrar(t["texto"], "bold", TXT_TAM, LARG_MAX, 2)
            if len(ls) > 2 or max(larg(x, "bold", TXT_TAM) for x in ls) > LARG_MAX:
                p.append(f"{sid}/{t['papel']}: a linha de texto não cabe em 2 linhas de {LARG_MAX} px")
    if tam_cta(st["cta"])[0] < CTA_TAM_MIN:
        p.append(f"{sid}: a chamada não cabe no cartão com {CTA_TAM_MIN} px")
    t1 = st["telas"][0]["trecho"][1]; resp = st.get("resposta_no_reel_em")
    if not isinstance(resp, (int, float)):
        p.append(f"{sid}: sem resposta_no_reel_em (o segundo em que o reel mostra a resposta)")
    elif t1 > resp - FOLGA_RESPOSTA:
        p.append(f"{sid}: o trecho da tela 1 termina em {t1}s, depois de resposta_no_reel_em − {FOLGA_RESPOSTA}s")
    # o reel: vídeo do reels.json, sha256 fixado na story, rótulos queimados do irmão do reel
    try:
        r = reel_de(st)
    except SystemExit as e:
        return p + [str(e)]
    mp4 = reel_mp4(st)
    if not os.path.exists(mp4):
        return p + [f"{sid}: vídeo do reel ausente: {r['video']}"]
    if not st.get("reel_sha256"):
        p.append(f"{sid}: sem reel_sha256 (o mp4 aprovado do reel tem de ser fixado na story)")
    elif CS.sha256_arquivo(mp4) != _sha(st["reel_sha256"]):
        p.append(f"{sid}: o mp4 do reel ({r['video']}) não é o fixado em reel_sha256 — trecho de outro vídeo")
    irmao_reel = os.path.splitext(mp4)[0] + ".json"
    rot_ok = set(CS.carregar(irmao_reel, {}).get("textos_tela") or [])
    dur_reel = r.get("dur")
    for t in st["telas"]:
        fora = [x for x in t.get("rotulos_reel") or [] if x not in rot_ok]
        if fora:
            p.append(f"{sid}/{t['papel']}: rótulos do reel {fora} não estão em textos_tela de {os.path.basename(irmao_reel)}")
        if isinstance(dur_reel, (int, float)) and t["trecho"][1] > dur_reel:
            p.append(f"{sid}/{t['papel']}: trecho termina em {t['trecho'][1]}s, depois do fim do reel ({dur_reel}s)")
    return p


def esperados(st, tela):
    """Strings que a tela TEM de desenhar, exatamente como o desenho as quebra: as 2 linhas do
    título, os pedaços da linha de texto, o selo e, conforme a tela, 'toca →' ou a chamada (em
    caixa alta, nas linhas do cartão) + 'Vídeo completo no perfil' + 'toque no nome lá em cima ↖'.
    -> (lista, problemas da quebra)."""
    nome = f"{st['id']}/{tela['papel']}"
    out, p = list(tela["titulo"]) + [CS.SELO], []
    if tela.get("texto"):
        ls = quebrar(tela["texto"], "bold", TXT_TAM, LARG_MAX, 2)
        if " ".join(ls) != " ".join(tela["texto"].split()):
            p.append(f"{nome}: a quebra da linha perde texto: {ls!r} ≠ {tela['texto']!r}")
        out += ls
    if tela["papel"] == "significado":
        ls = tam_cta(st["cta"])[1]
        if " ".join(ls) != " ".join(st["cta"].upper().split()):
            p.append(f"{nome}: a quebra da chamada perde texto: {ls!r}")
        out += ls + [CS.PERFIL, CS.NOME]
    else:
        out.append(CS.TOCA)
    return out, p


def conferir_desenhado(st, tela, desenhados):
    """Depois do render: nada A MAIS (texto fora da story) e nada A MENOS (cobertura). Sem a
    cobertura, uma linha truncada — 'Assimetria, dor, quedas demais' sem 'ou piora pedem
    avaliação.' — passaria, e é justamente a conduta do sinal de alerta (o contrapeso CFM).
    A primeira parte é o MESMO cheque do portão (checar_stories.problemas_de_desenho); a segunda,
    a quebra exata deste desenho (esperados)."""
    p = []
    nome = f"{st['id']}/{tela['papel']}"
    if not desenhados:
        p.append(f"{nome}: nenhum texto registrado (registrador desligado?)")
    p += [f"{st['id']}/{m}" for _, m in CS.problemas_de_desenho(tela, desenhados, st.get("cta", ""))]
    esp, p_quebra = esperados(st, tela)
    p += p_quebra
    faltam = [s for s in esp if s not in set(desenhados)]
    if faltam:
        p.append(f"{nome}: texto da story que NÃO foi desenhado (cobertura): {faltam}")
    if tela["papel"] != "significado" and (CS.PERFIL in desenhados or CS.NOME in desenhados):
        p.append(f"{nome}: '{CS.PERFIL}'/'{CS.NOME}' só podem aparecer na tela 3")
    if tela["papel"] == "significado" and CS.TOCA in desenhados:
        p.append(f"{nome}: '{CS.TOCA}' não vai na tela 3 (é a última)")
    return p


def hash_modulos():
    out = {}
    for m in ("base", "cf_alongamento", "fontes", "som", "voz"):
        caminho = os.path.join(ROOT, "animado", f"{m}.py")
        out[m] = "sha256:" + hashlib.sha256(open(caminho, "rb").read().replace(b"\r\n", b"\n")).hexdigest()
    return out


# ------------------------------------------------------------------ render de uma story
def fontes_fora_da_exigencia():
    """{papel: arquivo} das fontes escolhidas que não começam por STORY_FONTES_EXIGIDAS (vazio = ok
    ou exigência desligada). O render-stories.yml exige 'Roboto-': sem isso, um runner sem Roboto
    cairia calado na reserva Liberation/DejaVu."""
    exig = os.environ.get("STORY_FONTES_EXIGIDAS", "").strip()
    if not exig:
        return {}
    return {p: fonte_arquivo(p) for p in TF if not str(fonte_arquivo(p) or "").startswith(exig)}


def renderizar(st):
    probs = conferir(st)
    ruins = fontes_fora_da_exigencia()
    if ruins:
        probs.append(f"{st['id']}: fontes {ruins} não começam por {os.environ['STORY_FONTES_EXIGIDAS']!r} "
                     "(STORY_FONTES_EXIGIDAS): render com a fonte errada não sai")
    if probs:
        for x in probs:
            print(f"  [PORTÃO] {x}")
        raise SystemExit(f"ABORTADO: {len(probs)} problema(s) em {st['id']} — nada foi renderizado.")
    from checar_dur import duracao_mp4
    os.makedirs(PASTA_SAIDA, exist_ok=True)
    tmp = os.path.join(ROOT, ".animado_tmp", "story_cf", st["id"]); os.makedirs(tmp, exist_ok=True)
    tam_tit = tam_titulo(st)
    partes, parciais = [], []
    try:
        for i, tela in enumerate(st["telas"]):
            final = os.path.join(PASTA_SAIDA, f"{st['id']}_{i + 1}.mp4")
            parcial = final + ".parcial.mp4"; parciais.append((parcial, final))
            wav = os.path.join(tmp, f"tela{i + 1}.wav")
            som.gravar_wav(wav, mixar(float(tela["dur"]), eventos_de_som(tela)))
            registro = set()
            print(f"{st['id']} tela {i + 1}/3 ({tela['papel']}): trecho {tela['trecho']} s do {st['reel_ref']}, {tela['dur']} s")
            desloc_medido = codificar(st, tela, parcial, wav, tam_tit, registro)
            real = duracao_mp4(parcial)
            if not real or abs(real - float(tela["dur"])) > 0.15:
                raise SystemExit(f"ERRO: {os.path.basename(final)} saiu com {real}s, esperado {tela['dur']}s")
            desenhados = sorted(registro)
            p = conferir_desenhado(st, tela, desenhados)
            if p:
                raise SystemExit("ERRO: " + "; ".join(p))
            partes.append({"arquivo": f"{CS.PASTA}/{st['id']}_{i + 1}.mp4", "dur": round(real, 2),
                           "textos_tela": desenhados, "rotulos_reel": list(tela.get("rotulos_reel") or []),
                           "trecho": tela["trecho"], "crop": tela["crop"],
                           "camera": {k: tela.get(k) for k in ("zoom", "ancora", "foco_x", "esmaecer")},
                           "desloc_fundo": list(desloc_medido)})
    except BaseException:
        for parcial, _ in parciais:
            if os.path.exists(parcial):
                os.remove(parcial)
        print(f"render de {st['id']} FALHOU — vídeos e irmão anteriores ficaram intocados")
        raise
    for (parcial, final), parte in zip(parciais, partes):
        os.replace(parcial, final)
        parte["sha256"] = CS.sha256_arquivo(final)
    meta = {"id": st["id"], "hash_story": CS.hash_story(st), "hash_gerador": CS.hash_gerador(),
            "hash_render": CS.hash_render(st),
            "reel_video": reel_de(st)["video"], "reel_sha256": CS.sha256_arquivo(reel_mp4(st)),
            "partes": [{k: p[k] for k in ("arquivo", "sha256", "dur", "textos_tela", "rotulos_reel", "trecho", "crop",
                                          "camera", "desloc_fundo")}
                       for p in partes],
            "fontes": {p: fonte_arquivo(p) for p in TF}, "motor": hash_modulos(),
            "renderizado_em": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")}
    with open(CS.irmao_de(st), "w", encoding="utf-8", newline="\n") as f:
        json.dump(meta, f, ensure_ascii=False, indent=1); f.write("\n")
    print(f"OK {st['id']}: {', '.join(p['arquivo'] + ' (' + str(p['dur']) + 's)' for p in partes)} | irmão {CS.PASTA}/{st['id']}.json")


# ------------------------------------------------------------------ prévia, mosaico e folha
def _grade(imagens, legendas, ncol, tw, th, faixa=40, gap=8):
    """Mosaico (Pillow) com legenda de conferência em cada quadro (legenda fora do vídeo)."""
    nlin = math.ceil(len(imagens) / ncol)
    out = np.empty((gap + nlin * (th + faixa + gap), gap + ncol * (tw + gap), 4), np.uint8)
    out[...] = (32, 32, 32, 255)
    base = Image.fromarray(out, "RGBA")
    for k, im in enumerate(imagens):
        if im is None:
            continue
        x = gap + (k % ncol) * (tw + gap); y = gap + (k // ncol) * (th + faixa + gap)
        base.paste(im.convert("RGB").resize((tw, th), Image.LANCZOS), (x, y + faixa))
    out = np.array(base)
    surf = skia.Surface(out, colorType=skia.ColorType.kRGBA_8888_ColorType, alphaType=skia.AlphaType.kPremul_AlphaType)
    cv = surf.getCanvas(); f = skia.Font(TF["semi"], 24)
    for k, leg in enumerate(legendas):
        if leg:
            x = gap + (k % ncol) * (tw + gap); y = gap + (k // ncol) * (th + faixa + gap)
            cv.drawString(leg, x + 4, y + 28, f, tinta("#FFE14D"))
    return Image.fromarray(out[..., :3], "RGB")


def faixa_fontes(st, largura, tam=22, margem=12):
    """Faixa de CONFERÊNCIA sob o mosaico (fora do vídeo): de onde saiu cada texto (campo → id da
    fonte → trecho literal) e a revisão registrada, para quem aprova o molde olhar junto dos quadros."""
    f = skia.Font(TF["semi"], tam); fb = skia.Font(TF["black"], tam)
    linhas = [("FONTES (campo → id → trecho literal) — conferência, fora do vídeo", True)]
    for fo in st.get("fontes") or []:
        s = f"{fo.get('campo')} → {fo.get('id_fonte') or 'sem fonte (pergunta nova)'} → “{fo.get('trecho_literal') or ''}”"
        if fo.get("nota"):
            s += f"  [{fo['nota']}]"
        linhas.append((s, False))
    rev = st.get("revisao") or {}
    if rev:
        linhas.append(("REVISÃO", True))
        linhas += [(f"{k}: {v}", False) for k, v in rev.items()]
    quebradas = []
    for s, negrito in linhas:                     # quebra por largura, palavra a palavra
        fonte, atual = (fb if negrito else f), ""
        for pal in s.split(" "):
            prova = pal if not atual else atual + " " + pal
            if atual and fonte.measureText(prova) > largura - 2 * margem:
                quebradas.append((atual, negrito)); atual = "    " + pal
            else:
                atual = prova
        quebradas.append((atual, negrito))
    alt = margem * 2 + len(quebradas) * int(tam * 1.35)
    buf = np.empty((alt, largura, 4), np.uint8); buf[...] = (24, 24, 24, 255)
    cv = skia.Surface(buf, colorType=skia.ColorType.kRGBA_8888_ColorType, alphaType=skia.AlphaType.kPremul_AlphaType).getCanvas()
    for k, (s, negrito) in enumerate(quebradas):
        cv.drawString(s, margem, margem + tam + k * int(tam * 1.35), fb if negrito else f,
                      tinta("#FFE14D" if negrito else "#E8E8E8"))
    return Image.fromarray(buf[..., :3].copy(), "RGB")


def previa(st, pasta):
    """PNGs de conferência (quadro 0, meio e fim de cada tela; tela 2 também SEM o texto do story;
    tela 3 também o último quadro antes do cartão) e o mosaico. Mesmo código do vídeo."""
    probs = conferir(st)
    for x in probs:
        print(f"  [PORTÃO] {x}")
    os.makedirs(pasta, exist_ok=True)
    tam_tit = tam_titulo(st)
    imagens, legendas, ncol = [], [], 4
    q = Quadro()
    for i, tela in enumerate(st["telas"]):
        dur = float(tela["dur"]); ult = (round(dur * FPS) - 1) / FPS
        tempos = [(0.0, False), (round(dur / 2 * FPS) / FPS, False), (ult, False)]
        if tela["papel"] == "mecanismo":
            tempos.append((ult, True))
        if tela["papel"] == "significado":
            tempos.insert(2, ((round(tela["t_cartao"] * FPS) - 1) / FPS, False))
        tempos.sort(key=lambda x: x[0])
        trecho = Trecho(reel_mp4(st), tela["trecho"][0], tela["trecho"][1], tela["crop"])
        linha_im, linha_leg = [], []
        try:
            for tau, sem in tempos:
                im = Image.fromarray(q.desenhar(st, tela, tau, trecho, tam_tit, sem_texto=sem)[..., :3].copy(), "RGB")
                nome = os.path.join(pasta, f"{st['id']}_t{i + 1}_{tau:05.2f}{'_sem_texto' if sem else ''}.png")
                im.save(nome)
                linha_im.append(im); linha_leg.append(f"T{i + 1} {tela['papel']} · {tau:.2f}s{' · SEM TEXTO' if sem else ''}")
        finally:
            trecho.fechar()
        imagens += linha_im + [None] * (ncol - len(linha_im)); legendas += linha_leg + [""] * (ncol - len(linha_leg))
    saida = os.path.join(pasta, f"mosaico_{st['id']}.jpg")
    grade = _grade(imagens, legendas, ncol, 360, 640)
    faixa = faixa_fontes(st, grade.width)
    junto = Image.new("RGB", (grade.width, grade.height + faixa.height), (32, 32, 32))
    junto.paste(grade, (0, 0)); junto.paste(faixa, (0, grade.height))
    junto.save(saida, quality=88)
    print(f"prévia {st['id']}: {sum(1 for x in imagens if x is not None)} quadros + {saida}")
    return saida


def folha(reel_id, pasta):
    r = reels_por_id().get(reel_id)
    if not r:
        raise SystemExit(f"ERRO: {reel_id} não está no reels.json")
    mp4 = os.path.join(ROOT, r["video"].replace("/", os.sep))
    tw, th = 216, 384
    proc = subprocess.run([ffmpeg(), "-v", "error", "-i", mp4, "-vf", f"fps=1,scale={tw}:{th}", "-f", "rawvideo",
                           "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE, check=True)
    n = len(proc.stdout) // (tw * th * 3)
    ims = [Image.frombuffer("RGB", (tw, th), proc.stdout[k * tw * th * 3:(k + 1) * tw * th * 3], "raw", "RGB", 0, 1)
           for k in range(n)]
    os.makedirs(pasta, exist_ok=True)
    saida = os.path.join(pasta, f"folha_{reel_id}.jpg")
    _grade(ims, [f"{k} s" for k in range(n)], 8, tw, th, faixa=30, gap=4).save(saida, quality=88)
    print(f"folha: {saida} ({n} quadros, 1 por segundo)")


def precisa_de_render(st, publicados, reels, aprov):
    """(precisa, motivo) para o --todos: story publicada inteira não se re-renderiza (o vídeo dela já
    saiu; o reel pode ter mudado depois e ela seria recusada à toa); story com render em dia também
    não (re-render troca os bytes e derruba a aprovação amarrada aos vídeos)."""
    if len(CS.partes_publicadas(publicados).get(st.get("id"), {})) == len(CS.PAPEIS):
        return False, "já publicada inteira"
    v = CS.veredito(st, aprov, reels, exigir_render=True)
    render = [m for t, m in v["problemas"] if t == "render"]
    if not render:
        return False, "render em dia"
    return True, render[0]


def main(argv=None):
    ap = argparse.ArgumentParser(description="Renderiza os stories COMO FUNCIONA EM 3 TOQUES de stories_cf.json.")
    ap.add_argument("ids", nargs="*", help="ids das stories (stn_...)")
    ap.add_argument("--todos", action="store_true", help="as stories da fila que precisam de render")
    ap.add_argument("--forcar", action="store_true", help="com --todos: re-renderiza também as de render em dia")
    ap.add_argument("--lista-ok", metavar="ARQ", help="grava os ids renderizados com sucesso (um por linha)")
    ap.add_argument("--previa", action="store_true", help="só PNGs de conferência e mosaico, sem vídeo")
    ap.add_argument("--folha", metavar="REEL_ID", help="folha de contato do reel (1 quadro por segundo)")
    ap.add_argument("--pasta", default=PREVIA_PADRAO, help="pasta da prévia/folha (padrão .animado_tmp/story_cf_previa)")
    a = ap.parse_args(argv)
    if a.folha:
        folha(a.folha, a.pasta)
        return 0
    fila = carregar_fila()
    if a.todos:
        publicados = CS.carregar(os.path.join(ROOT, "state", "published.json"), {}).get("published", [])
        reels = reels_por_id(); aprov = CS.carregar(CS.APROVACOES, {"lotes": []})
        alvo = []
        for st in fila:
            precisa, motivo = precisa_de_render(st, publicados, reels, aprov)
            if precisa or (a.forcar and motivo == "render em dia"):
                alvo.append(st)
            else:
                print(f"{st.get('id')}: pulada ({motivo})")
    else:
        if not a.ids:
            ap.error("diga o id da story (ou --todos)")
        por_id = {s.get("id"): s for s in fila}
        falta = [i for i in a.ids if i not in por_id]
        if falta:
            raise SystemExit(f"ERRO: {falta} não estão em stories_cf.json")
        alvo = [por_id[i] for i in a.ids]
    ok, recusadas = [], []
    for st in alvo:
        try:
            if a.previa:
                previa(st, a.pasta)
            else:
                renderizar(st)
            ok.append(st["id"])
        except (SystemExit, Exception) as e:        # recusa do portão ou erro do render: segue com as outras
            if not isinstance(e, SystemExit):
                import traceback
                traceback.print_exc()
            recusadas.append((st.get("id"), str(e)))
            print(f"::error::{st.get('id')}: {e}")
    if a.lista_ok:
        with open(a.lista_ok, "w", encoding="utf-8", newline="\n") as f:
            f.write("".join(i + "\n" for i in ok))
    print(f"{len(ok)} story(ies) {'com prévia' if a.previa else 'renderizada(s)'}: {ok or '—'}"
          + (f" | {len(recusadas)} RECUSADA(S): {[i for i, _ in recusadas]}" if recusadas else ""))
    return 1 if recusadas else 0


if __name__ == "__main__":
    sys.exit(main())
