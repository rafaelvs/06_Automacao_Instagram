# -*- coding: utf-8 -*-
"""
estilo_variacao.py — VARIACAO VISUAL deterministica por peca (regra 4 do template v6).

Motivacao: feedback real de audiencia (08/07, Leonardo Velloso, medico que acompanha o perfil):
"impressao que o assunto ta repetido... parece o mesmo post de antes". A mesmice visual (mesmo
motivo de fundo + mesmo acento + mesma ancoragem) faz TEMAS diferentes parecerem repetidos e casa
com a politica anti-massificacao da Meta. Referencia citada (@endoscopy): "mesmos ossos de layout,
mas imagens e cores diferentes — cada post tem personalidade".

O que este modulo faz: MANTEM a MARCA (paleta preto/creme/dourado, header RV, serifa, rodape CFM) e
rotaciona, por id de peca (DETERMINISTICO — mesmo id => mesmo visual sempre, reproduzivel/idempotente):
  - ACENTO cromatico (sempre DENTRO da paleta quente — dourado/bronze/creme-dourado; nunca cor nova)
  - MOTIVO de fundo (5 familias de textura sutil)
  - ANCORAGEM do bloco de titulo (alto/centro/baixo)
  - ESCALA do hook (titulo da capa)

ADITIVO/fail-safe: o render importa isto em try/except; se sumir, cai no comportamento atual.
So stdlib + Pillow ImageDraw (recebido pronto do render). Nao desenha nada de exame/anatomia real.
"""
import hashlib
import math

# Acentos — TODOS dentro da paleta da marca (quentes: dourado/bronze/creme). Nunca hue novo.
ACENTOS = [
    (188, 150, 84),   # dourado base (leve realce do GOLD atual)
    (214, 182, 116),  # dourado vivo (mais claro — salta no fundo escuro)
    (164, 126, 70),   # bronze (mantido legivel sobre preto)
    (224, 205, 158),  # creme-dourado claro (o mais claro — maior contraste)
]
MOTIVOS = ["arcos", "diagonais", "grade", "raios", "cantos"]
LAYOUTS = ["alto", "centro", "baixo"]
DY_LAYOUT = {"alto": -46, "centro": 0, "baixo": 60}   # deslocamento vertical do bloco de titulo
ESCALAS = [0.92, 1.0, 1.08]                           # escala do hook (titulo capa)


def _idx(post_id, n, salt=""):
    """Indice deterministico e estavel por id (md5 -> mod n). Sem random (reproduzivel)."""
    h = int(hashlib.md5((salt + str(post_id)).encode("utf-8")).hexdigest(), 16)
    return h % n


def variante(post_id):
    """Devolve o estilo desta peca. Mesmo id => mesmo dict sempre."""
    return {
        "acento": ACENTOS[_idx(post_id, len(ACENTOS), "acento")],
        "motivo": MOTIVOS[_idx(post_id, len(MOTIVOS), "motivo")],
        "layout": LAYOUTS[_idx(post_id, len(LAYOUTS), "layout")],
        "dy": DY_LAYOUT[LAYOUTS[_idx(post_id, len(LAYOUTS), "layout")]],
        "hook_escala": ESCALAS[_idx(post_id, len(ESCALAS), "hook")],
    }


def desenha_motivo(da, W, H, motivo, cor, alpha=58):
    """Desenha a textura de fundo (sobre um overlay RGBA ja criado pelo render).
    `da` = ImageDraw do overlay; `cor` = RGB do acento; `alpha` = intensidade base.
    Motivos DENSOS (grade/raios/diagonais) usam menos alpha p/ nao pesar; ESPARSOS (arcos/cantos) mais."""
    dens = {"grade": 0.55, "raios": 0.6, "diagonais": 0.65, "arcos": 1.0, "cantos": 1.0}.get(motivo, 1.0)
    a = max(18, min(90, int(alpha * dens)))
    c = (cor[0], cor[1], cor[2], a)
    if motivo == "arcos":                         # o atual — arcos radiais concentricos (cy relativo p/ carrossel 1350 e reel 1920)
        cy = int(H * 0.87)
        for r in (560, 470, 380, 300):
            da.arc([W // 2 - r, cy - r, W // 2 + r, cy + r], 202, 338, fill=c, width=2)
    elif motivo == "diagonais":                   # feixe de diagonais
        for i in range(-2, 16):
            x = i * 110
            da.line([(x, H), (x + H, 0)], fill=c, width=2)
    elif motivo == "grade":                       # grade tecnica leve
        for x in range(90, W, 130):
            da.line([(x, 0), (x, H)], fill=c, width=1)
        for y in range(90, H, 130):
            da.line([(0, y), (W, y)], fill=c, width=1)
    elif motivo == "raios":                       # raios de um foco inferior
        cx, cy = W // 2, H + 60
        for a in range(198, 343, 9):
            rad = math.radians(a)
            da.line([(cx, cy), (cx + 1700 * math.cos(rad), cy + 1700 * math.sin(rad))], fill=c, width=2)
    elif motivo == "cantos":                      # arcos nos cantos opostos
        for r in (520, 430, 340):
            da.arc([-r, -r, r, r], 0, 90, fill=c, width=2)
            da.arc([W - r, H - r, W + r, H + r], 180, 270, fill=c, width=2)
    else:                                         # fallback = arcos (nunca quebra)
        desenha_motivo(da, W, H, "arcos", cor, alpha)


if __name__ == "__main__":
    for pid in ("post03", "post04", "post05", "post07", "on_pseudartrose"):
        print(f"{pid:20} -> {variante(pid)}")
