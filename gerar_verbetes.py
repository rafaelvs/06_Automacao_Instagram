# -*- coding: utf-8 -*-
"""
FÁBRICA DE VERBETES (Aposta 5 do plano de 29/08/2026) — sequências de stories viram
carrosséis-verbete de FEED (4:5, 1080x1350), a única fonte medida de cauda longa da conta
(85% das late-views vêm de posts com keyword leiga declarativa — relatorio_descoberta.md).

O que é um VERBETE (7–8 slides):
  s1  capa-gancho    — keyword leiga GRANDE na 1ª linha, estilo manchete da casa
  s2..s6  conteúdo   — os 5 frames da sequência-fonte RE-RENDERIZADOS em 4:5 a partir do
                       (o frame de abertura é dispensado quando repetiria a capa -> 7 slides)
                       CONTEÚDO-FONTE (temporadas_data / episodios_novos_2026 /
                       sequencias_avulsas_lote2) — nunca crop do frame 9:16 (mataria o rodapé CFM)
  s7  card-resumo    — síntese guardável em bullets (precedente: gerar_card_resumo_discrepancia.py)
  s8  slide-selo     — CRM/RQE + "Conteúdo educativo" + @rafaelvargasmd

PRINCÍPIO EDITORIAL (inegociável): o verbete REORGANIZA o que a sequência já diz — conteúdo
que já passou pelos gates da casa. Toda frase NOVA aqui é de transição/estrutura (capa, fecho
do card, selo); NENHUMA afirmação clínica nova. A limpeza de texto só REMOVE costura serial
de story ("Esta semana...", "Ontem...", "Amanhã...") — não acrescenta clínica.

Saída (compatível com a convenção de paths do publish — repo-root-relativa, como "images/x.jpg"):
  verbetes/<id_verbete>/s1.jpg .. s8.jpg
  verbetes_biblioteca.json  — manifesto {id, tema, keyword, fonte, slides[], caption, alt}
  *** BIBLIOTECA, não fila: NADA entra em posts.json aqui. Publicação liga só no D-day
  (17-18/09), por decisão do Rafael, 2/semana dentro dos 4 slots de post. ***

Uso:
  python gerar_verbetes.py                       -> renderiza os 20 da CURADORIA (ordem do plano)
  python gerar_verbetes.py reconstrucao-ter ...  -> só os ids pedidos (id de sequência-fonte
                                                    ou id de verbete v_*)
  python gerar_verbetes.py --listar              -> imprime a curadoria (fonte -> keyword)
  --outdir DIR / --sem-manifesto                 -> usados pelo harness local de amostras

Guardrails embutidos (falham RUIDOSAMENTE, exit != 0):
  * cfm_guardrails.auditar == 0 VIOLACAO na legenda E no texto de todos os slides;
  * keyword presente nos primeiros 125 caracteres da legenda (1ª linha declarativa);
  * 4–6 hashtags; assinatura CRM+RQE + disclaimer na legenda;
  * todo slide 1080x1350 exato e com rodapé CFM (footer da casa em 8/8 slides);
  * termo vetado ("dismetria"): bloqueado pelo auditar; ângulo estético/estatura
    ("alongamento estético", "ganhar estatura/altura"...): bloqueado AQUI, em
    _checagens — o auditar NÃO cobre isso (verificado 30/08 com controle positivo).
    Menção defensiva ("nunca estética", "baixa estatura" como sinal clínico) passa.
"""
import argparse
import json
import os
import re
import sys
import unicodedata

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import carrossel as C
from cfm_guardrails import auditar
from temporadas_data import SEASONS

ROOT = os.path.dirname(os.path.abspath(__file__))
W, H, M = C.W, C.H, C.M
SIG = C.SIG
DISC = C.DISC
DOW = ["seg", "ter", "qua", "qui", "sex", "sab", "dom"]


def _norm(s):
    return unicodedata.normalize("NFKD", str(s)).encode("ascii", "ignore").decode().lower()


# ---------------------------------------------------------------------------
# 1) FONTES — resolve id de sequência -> {"theme", "frames": [(segmento, título, sub) x5]}
# ---------------------------------------------------------------------------
def carregar_fontes():
    src = {}
    for wk in SEASONS:
        for di, day in enumerate(wk["days"]):
            sid = f"{wk['slug']}-{DOW[di]}"
            src[sid] = {"theme": wk["theme"],
                        "frames": [(seg, tit, sub) for (seg, tit, sub, _cue) in day]}
    # avulsas do lote 2026 (s_on_*/s_pnc_* originais): derivadas dos episódios revisados
    try:
        import episodios_novos_2026 as EN
        for ep in EN.NEW_EPISODES:
            frames = [(sc["k"], " ".join(sc["sc"]).strip(), sc.get("sub", ""))
                      for sc in ep["scenes"]]
            src.setdefault("s_" + ep["id"], {"theme": ep["serie"], "frames": frames})
    except ImportError:
        pass
    # avulsas do lote 2 (fix P0.3 v5): fonte própria
    try:
        import sequencias_avulsas_lote2 as AV
        for (sid, theme, _v, frames5) in AV.NOVAS:
            src.setdefault(sid, {"theme": theme,
                                 "frames": [(seg, tit, sub) for (seg, tit, sub, _cue) in frames5]})
    except ImportError:
        pass
    return src


# ---------------------------------------------------------------------------
# 2) LIMPEZA ESTRUTURAL — remove só a costura serial do formato story.
#    Nunca acrescenta texto clínico; só remove frases de transição e capitaliza.
# ---------------------------------------------------------------------------
_DOW_RE = re.compile(r"^(SEG|TER|QUA|QUI|SEX|SAB|DOM)\s*·\s*", re.I)
_PREFIXOS_SERIAIS = (
    "esta semana", "ontem", "amanha", "semana que vem", "na segunda",
    "fim de semana", "sexta e dia", "sexta de", "vem comigo",
)
_PREFIXOS_COM_MIOLO = ("fechando a",)  # "Fechando a semana: X" -> mantém o X


def limpar_kicker(seg):
    return _DOW_RE.sub("", seg).strip()


def _capitaliza(s):
    s = s.strip()
    return s[:1].upper() + s[1:] if s else s


def limpar_sub(sub):
    frases = re.split(r"(?<=[.!?])\s+", (sub or "").strip())
    mantidas = []
    for f in frases:
        nf = _norm(f)
        if any(nf.startswith(p) for p in _PREFIXOS_SERIAIS):
            continue
        if any(nf.startswith(p) for p in _PREFIXOS_COM_MIOLO):
            if ":" in f:
                mantidas.append(_capitaliza(f.split(":", 1)[1]))
            continue
        if nf.startswith("hoje,") or nf.startswith("hoje "):
            f = re.sub(r"^hoje,?\s*", "", f, flags=re.I)
            mantidas.append(_capitaliza(f))
            continue
        mantidas.append(f)
    return " ".join(mantidas).strip()


# ---------------------------------------------------------------------------
# 3) CURADORIA — os 20 primeiros (ordem do plano: núcleo evaporado -> cauda
#    comprovada -> compilação transversal). fonte -> keyword do verbete.
# ---------------------------------------------------------------------------
KICK_REC = "Reconstrução Óssea"
KICK_PED = "Ortopedia Pediátrica"

CURADORIA = [
 # ---- Núcleo que evaporou sem ativo: SEMANA DA RECONSTRUÇÃO (7) ----
 dict(fonte="reconstrucao-ter", kicker=KICK_REC,
      keyword="uma perna mais curta que a outra",
      titulo="Uma perna mais curta que a outra",
      sub="Quando é só detalhe, quando merece atenção — e as opções que existem. Um guia para salvar.",
      primeira_linha="Uma perna mais curta que a outra (discrepância de membro): quando observar e quando agir.",
      tags="#discrepanciademembro #anisomelia #pernamaiscurta #alongamentoosseo #ortopediasaopaulo"),
 dict(fonte="reconstrucao-qua", kicker=KICK_REC,
      keyword="fixador externo",
      titulo="Fixador externo: última opção?",
      sub="O mito sobre o aparelho que mais assusta as famílias — e o que ele realmente faz.",
      primeira_linha="Fixador externo não é sinal de caso perdido: é uma ferramenta de correção e reconstrução.",
      tags="#fixadorexterno #ilizarov #mitoouverdade #reconstrucaoossea #ortopediasaopaulo"),
 dict(fonte="reconstrucao-qui", kicker=KICK_REC,
      keyword="viver com o fixador externo",
      titulo="Como é viver com o fixador externo",
      sub="Escola, trabalho, banho e o lado emocional — o dia a dia de quem está em tratamento.",
      primeira_linha="Viver com o fixador externo: escola, trabalho, banho e o que esperar da rotina.",
      tags="#fixadorexterno #ilizarov #reconstrucaoossea #reabilitacao #ortopediasaopaulo"),
 dict(fonte="reconstrucao-sex", kicker=KICK_REC,
      keyword="cuidados com os pinos do fixador",
      titulo="Cuidados com os pinos do fixador",
      sub="O básico do dia a dia que faz parte do tratamento. Salve para consultar.",
      primeira_linha="Cuidados com os pinos do fixador externo: o básico diário que faz parte do tratamento.",
      tags="#fixadorexterno #ilizarov #cuidadoscomospinos #reconstrucaoossea #ortopediasaopaulo"),
 dict(fonte="reconstrucao-sab", kicker=KICK_REC,
      keyword="fixador externo: sinais de alerta",
      titulo="Fixador externo: sinais de alerta",
      sub="Quando avisar a equipe sem esperar o próximo retorno.",
      primeira_linha="Fixador externo: sinais de alerta que pedem contato com a equipe sem demora.",
      tags="#fixadorexterno #ilizarov #sinaisdealerta #reconstrucaoossea #ortopediasaopaulo"),
 dict(fonte="reconstrucao-dom", kicker=KICK_REC,
      keyword="alongamento ósseo",
      titulo="Alongamento ósseo: o corpo cria osso novo",
      sub="Como a reconstrução acontece por etapas — e por que função vem sempre em primeiro lugar.",
      primeira_linha="Alongamento ósseo: o próprio corpo cria osso novo, em fases, milímetro a milímetro.",
      tags="#alongamentoosseo #osteogenesedistracao #ilizarov #reconstrucaoossea #ortopediasaopaulo"),
 dict(fonte="reconstrucao-seg", kicker=KICK_REC,
      keyword="reconstrução óssea",
      titulo="Reconstrução óssea: quando pensar nela",
      sub="Os três sinais de que um osso pode precisar de mais do que espera e gesso.",
      primeira_linha="Reconstrução óssea: os três sinais de que um osso pode precisar de correção.",
      tags="#reconstrucaoossea #pseudartrose #fixadorexterno #deformidadeossea #ortopediasaopaulo"),
 # ---- Núcleo que evaporou sem ativo: SEMANA DAS PERNAS TORTAS (7) ----
 dict(fonte="pernas-ter", kicker=KICK_PED,
      keyword="perna arqueada ou em X",
      titulo="Perna arqueada ou em X: é normal?",
      sub="O calendário do alinhamento no crescimento — e o que foge da regra.",
      primeira_linha="Perna arqueada ou em X: o calendário do alinhamento normal — e o que foge da regra.",
      tags="#pernasarqueadas #joelhovalgo #joelhovaro #ortopediapediatrica #ortopediasaopaulo"),
 dict(fonte="pernas-qua", kicker=KICK_PED,
      keyword="perna torta tem que operar",
      titulo="“Perna torta tem que operar logo”?",
      sub="O mito da pressa em corrigir — e quando a correção é real.",
      primeira_linha="Perna torta tem que operar? Na maioria das vezes, não — veja quando a correção é real.",
      tags="#pernastortas #mitoouverdade #joelhovaro #ortopediapediatrica #ortopediasaopaulo"),
 dict(fonte="pernas-sab", kicker=KICK_PED,
      keyword="perna torta: quando avaliar",
      titulo="Perna torta: quando avaliar",
      sub="Três sinais objetivos para separar a fase do crescimento do que pede um olhar.",
      primeira_linha="Perna torta: quando avaliar? Os três sinais de que o desalinhamento da criança pede um olhar.",
      tags="#pernastortas #ortopediapediatrica #ortopediainfantil #saudedacrianca #ortopediasaopaulo"),
 dict(fonte="pernas-dom", kicker=KICK_PED,
      keyword="correção do eixo da perna",
      titulo="Correção do eixo da perna torta",
      sub="Medir, entender a causa e — quando preciso — guiar o próprio crescimento.",
      primeira_linha="Correção do eixo da perna: medir, entender a causa e, quando preciso, guiar o crescimento.",
      tags="#pernastortas #crescimentoguiado #osteotomia #ortopediapediatrica #ortopediasaopaulo"),
 dict(fonte="pernas-seg", kicker=KICK_PED,
      keyword="perna torta: o que observar",
      titulo="Perna torta: o que observar",
      sub="O que acompanhar em casa no crescimento — e o que costuma ser só fase.",
      primeira_linha="Perna torta: o que observar em casa durante o crescimento — e o que costuma ser só fase.",
      tags="#pernastortas #desenvolvimentoinfantil #ortopediapediatrica #saudedacrianca #ortopediasaopaulo"),
 dict(fonte="pernas-qui", kicker=KICK_PED,
      keyword="pernas desalinhadas no esporte",
      titulo="Pernas desalinhadas no esporte",
      sub="Como o eixo torto sobrecarrega o joelho de quem treina — e o que ajuda.",
      primeira_linha="Pernas desalinhadas no esporte: o eixo torto sobrecarrega um lado do joelho de quem treina.",
      tags="#joelhovalgo #esportejovem #dornojoelho #ortopediapediatrica #ortopediasaopaulo"),
 dict(fonte="pernas-sex", kicker=KICK_PED,
      keyword="acompanhar o alinhamento das pernas",
      titulo="Como acompanhar o alinhamento das pernas",
      sub="Observar a evolução da perna que cresce — sem ansiedade e com método.",
      primeira_linha="Como acompanhar o alinhamento das pernas do seu filho — sem ansiedade e com método.",
      tags="#pernastortas #crescimentoinfantil #ortopediapediatrica #saudedacrianca #ortopediasaopaulo"),
 # ---- Temas com cauda comprovada (marcos do andar, joelho, pé) ----
 dict(fonte="s_pnc_marcos_andar", kicker=KICK_PED,
      keyword="com quantos meses o bebê anda",
      titulo="Com quantos meses o bebê anda?",
      sub="A faixa normal, a comparação que não ajuda e a linha do alerta.",
      primeira_linha="Com quantos meses o bebê anda? Entre 9 e 18 meses, em geral — e existe uma linha de alerta.",
      tags="#primeirospassos #desenvolvimentoinfantil #bebe #ortopediapediatrica #ortopediasaopaulo"),
 dict(fonte="marcha-ter", kicker=KICK_PED,
      keyword="pés para dentro",
      titulo="Pés para dentro: precisa corrigir?",
      sub="A queixa clássica dos pais — e o que realmente muda a evolução.",
      primeira_linha="Criança que anda com os pés para dentro: na maioria, melhora sozinho — veja quando avaliar.",
      tags="#pesparadentro #marchainfantil #ortopediapediatrica #ortopediainfantil #ortopediasaopaulo"),
 dict(fonte="joelho-dom", kicker=KICK_PED,
      keyword="joelho torto",
      titulo="O joelho torto que não corrige sozinho",
      sub="Quando o desalinhamento persiste — e como se pensa o tratamento.",
      primeira_linha="Joelho torto que não corrige sozinho: quando o desalinhamento persiste e como se trata.",
      tags="#joelhotorto #joelhovalgo #crescimentoguiado #ortopediapediatrica #ortopediasaopaulo"),
 dict(fonte="marcha-qua", kicker=KICK_PED,
      keyword="bebê precisa de sapato firme",
      titulo="“Bebê precisa de sapato firme”?",
      sub="O mito do calçado — e o que fortalece o pé de verdade.",
      primeira_linha="Bebê precisa de sapato firme? Não — andar descalço em casa, em segurança, fortalece o pé.",
      tags="#andardescalco #calcadoinfantil #mitoouverdade #ortopediapediatrica #ortopediasaopaulo"),
 # ---- Compilações transversais ----
 dict(id="v_mitos_ossos_crianca", kicker=KICK_PED, tema="Mito x Verdade",
      compilacao=[("joelho-qua", "Joelho"), ("quadril-qua", "Quadril"),
                  ("fraturas-qua", "Fraturas"), ("tornozelo-qua", "Tornozelo"),
                  ("esporte-qua", "Esporte")],
      keyword="mito ou verdade",
      titulo="Mito ou verdade: os ossos da criança",
      sub="Frases que todo pai já ouviu — e o que é fato em cada uma.",
      primeira_linha="Mito ou verdade? 5 frases que todo pai já ouviu sobre os ossos da criança — e o que é fato.",
      tags="#mitoouverdade #ortopediapediatrica #ortopediainfantil #saudedacrianca #ortopediasaopaulo"),
 dict(fonte="socorros-sex", kicker=KICK_PED, tema="Primeiros Socorros",
      keyword="primeiros socorros",
      titulo="Primeiros socorros: torção, fratura ou luxação",
      sub="O passo a passo dos primeiros minutos, para salvar e ter à mão na emergência.",
      primeira_linha="Primeiros socorros ortopédicos: o passo a passo para torção, suspeita de fratura e luxação.",
      tags="#primeirossocorros #fraturainfantil #entorse #saudedacrianca #ortopediasaopaulo"),
]


def _vid(spec):
    return spec.get("id") or ("v_" + spec["fonte"].replace("-", "_"))


# ---------------------------------------------------------------------------
# 4) RENDER — primitivas da casa (carrossel.py): base(), footer(), trk(), wrap()
# ---------------------------------------------------------------------------
def _titulo_fit(d, txt, tam_ini, max_linhas, largura):
    tam = tam_ini
    while True:
        tf = C.F(C.SB, tam)
        linhas = C.wrap(txt, tf, largura)
        if len(linhas) <= max_linhas or tam <= 44:
            return tf, linhas
        tam -= 8


def _base(vid):
    var = C._var(vid)
    img, d = C.base(motif=True, var=var)
    ac = var["acento"] if var else C.GOLD
    dy = var["dy"] if var else 0
    he = var["hook_escala"] if var else 1.0
    return img, d, ac, dy, he


def slide_capa(spec, vid, n):
    img, d, ac, dy, he = _base(vid)
    C.trk(d, (M, 300), ("VERBETE · " + spec["kicker"]).upper(), C.F(C.NB, 24), ac, 5)
    d.line([(M, 340), (M + 58, 340)], fill=ac, width=3)
    tf, linhas = _titulo_fit(d, spec["titulo"], int(96 * he), 4, W - 2 * M)
    ty = 380 + dy
    for ln in linhas:
        d.text((M, ty), ln, font=tf, fill=C.CREAM); ty += int(tf.size * 1.08)
    if spec.get("sub"):
        ty += 24
        for ln in C.wrap(spec["sub"], C.F(C.NR, 38), W - 2 * M):
            d.text((M, ty), ln, font=C.F(C.NR, 38), fill=C.TXT); ty += 54
    C.trk(d, (M, H - 210), "ARRASTE →", C.F(C.NB, 30), ac, 4)
    C.footer(d, 0, n, ac=ac)
    return img


def slide_conteudo(kicker, titulo, corpo, vid, page, n):
    img, d, ac, dy, _he = _base(vid)
    C.trk(d, (M, 300), kicker.upper(), C.F(C.NB, 24), ac, 5)
    d.line([(M, 340), (M + 58, 340)], fill=ac, width=3)
    tf, linhas = _titulo_fit(d, titulo, 70, 3, W - 2 * M)
    ty = 400 + dy
    for ln in linhas:
        d.text((M, ty), ln, font=tf, fill=C.CREAM); ty += int(tf.size * 1.12)
    ty += 28
    if corpo:
        tam_corpo = 42
        while True:  # encolhe o corpo se estourar a área útil (rodapé CFM intocável)
            bf = C.F(C.NR, tam_corpo)
            linhas_c = C.wrap(corpo, bf, W - 2 * M)
            alt = len(linhas_c) * int(tam_corpo * 1.42)
            if ty + alt <= H - 180 or tam_corpo <= 32:
                break
            tam_corpo -= 4
        for ln in linhas_c:
            d.text((M, ty), ln, font=bf, fill=C.TXT); ty += int(tam_corpo * 1.42)
    C.footer(d, page, n, ac=ac)
    return img


def slide_card_resumo(spec, bullets, vid, page, n):
    """Card-resumo guardável — padrão do card de 16/08 (lead dourado + corpo)."""
    fecho = "Resumo educativo — cada caso pede avaliação individual."
    img, d, ac, dy, _he = _base(vid)
    C.trk(d, (M, 300), "PARA GUARDAR", C.F(C.NB, 24), ac, 5)
    d.line([(M, 340), (M + 58, 340)], fill=ac, width=3)
    tf, linhas = _titulo_fit(d, spec["titulo"], 62, 2, W - 2 * M)
    corpo_tam = 32
    while True:  # dry-run de altura antes de desenhar; encolhe o corpo se preciso
        lead_f = C.F(C.NB, 30)
        body_f = C.F(C.NR, corpo_tam)
        alt = len(linhas) * int(tf.size * 1.1) + 30
        for lead, corpo in bullets:
            alt += len(C.wrap(lead, lead_f, W - 2 * M - 40)) * int(30 * 1.2)
            if corpo:
                alt += len(C.wrap(corpo, body_f, W - 2 * M - 40)) * int(corpo_tam * 1.3)
            alt += 22
        alt += 44
        if 380 + alt <= H - 175 or corpo_tam <= 24:
            break
        corpo_tam -= 2
    ty = 380
    for ln in linhas:
        d.text((M, ty), ln, font=tf, fill=C.CREAM); ty += int(tf.size * 1.1)
    ty += 30
    for lead, corpo in bullets:
        d.ellipse([M, ty + 11, M + 12, ty + 23], fill=ac)
        for ln in C.wrap(lead, lead_f, W - 2 * M - 40):
            d.text((M + 40, ty), ln, font=lead_f, fill=ac); ty += int(30 * 1.2)
        if corpo:
            for ln in C.wrap(corpo, body_f, W - 2 * M - 40):
                d.text((M + 40, ty), ln, font=body_f, fill=C.TXT); ty += int(corpo_tam * 1.3)
        ty += 22
    ty += 10
    for ln in C.wrap(fecho, C.F(C.NR, 26), W - 2 * M):
        d.text((M, ty), ln, font=C.F(C.NR, 26), fill=C.MUT); ty += 34
    C.footer(d, page, n, ac=ac)
    return img


def slide_selo(vid, page, n):
    img, d, ac, _dy, _he = _base(vid)
    C.trk(d, (M, 340), "QUEM ASSINA ESTE VERBETE", C.F(C.NB, 24), ac, 5)
    d.line([(M, 380), (M + 58, 380)], fill=ac, width=3)
    ty = 430
    for ln in C.wrap("Dr. Rafael Vargas", C.F(C.SB, 84), W - 2 * M):
        d.text((M, ty), ln, font=C.F(C.SB, 84), fill=C.CREAM); ty += 96
    ty += 8
    d.text((M, ty), "Médico · CRM-SP 226103 · RQE 137901", font=C.F(C.NB, 36), fill=C.TXT); ty += 56
    d.text((M, ty), "Ortopedia · São Paulo", font=C.F(C.NR, 34), fill=C.TXT); ty += 76
    d.text((M, ty), "@rafaelvargasmd", font=C.F(C.NB, 44), fill=ac); ty += 84
    for ln in C.wrap("Conteúdo educativo — não substitui avaliação médica.",
                     C.F(C.NR, 32), W - 2 * M):
        d.text((M, ty), ln, font=C.F(C.NR, 32), fill=C.TXT); ty += 46
    ty += 30
    for ln in C.wrap("Salve este verbete e envie para quem precisa.", C.F(C.NB, 32), W - 2 * M):
        d.text((M, ty), ln, font=C.F(C.NB, 32), fill=C.CREAM); ty += 46
    C.footer(d, page, n, ac=ac)
    return img


# ---------------------------------------------------------------------------
# 5) MONTAGEM do verbete (slides de conteúdo a partir da fonte) + legenda
# ---------------------------------------------------------------------------
def _frames_conteudo(spec, fontes):
    """[(kicker, título, corpo)] — 5 slides de conteúdo, fiéis à fonte."""
    if "compilacao" in spec:
        out = []
        for sid, area in spec["compilacao"]:
            fr = fontes[sid]["frames"]
            # frame do mito = capa da sequência (título é a frase-mito);
            # a verdade = frame cujo segmento contém "verdade" (fallback: índice 2)
            titulo_mito = fr[0][1]
            # o frame "A verdade" (nunca o 0 — o segmento da capa é "QUA · Mito x Verdade")
            idx_v = next((i for i, (seg, _t, _s) in enumerate(fr)
                          if i > 0 and _norm(seg).startswith("a verdade")), 2)
            corpo = "A verdade: " + limpar_sub(fr[idx_v][2])
            out.append((area, titulo_mito, corpo))
        return out
    fr = fontes[spec["fonte"]]["frames"]
    return [(limpar_kicker(seg), tit, limpar_sub(sub)) for (seg, tit, sub) in fr]


_CTA_INICIOS = ("salve", "salva", "mande", "manda", "compartilh", "guarde", "envie")


def _eh_cta(frase):
    return any(_norm(frase).startswith(p) for p in _CTA_INICIOS)


def _bullets_resumo(spec, conteudo):
    if "compilacao" in spec:
        return [(titulo, None) for (_k, titulo, _c) in conteudo]
    # frames 2..5 da sequência (pula a capa da fonte): lead = título, corpo = 1ª frase
    # NÃO-CTA (o card é síntese guardável; "salve e mande" vive no slide-selo)
    bullets = []
    for (_k, titulo, corpo) in conteudo[1:]:
        frases = [f for f in re.split(r"(?<=[.!?])\s+", corpo or "") if f and not _eh_cta(f)]
        primeira = frases[0] if frases else None
        if _eh_cta(titulo) and not primeira:
            continue  # bullet 100% CTA não entra no resumo
        bullets.append((titulo, primeira))
    return bullets


def _capa_duplica_frame0(spec, conteudo):
    """True quando o título do frame 1 da fonte repete a capa (mesmo assunto, mesmas
    palavras) — nesse caso o verbete sai com 7 slides (capa já É o frame de abertura)."""
    if "compilacao" in spec:
        return False
    a = set(_norm(re.sub(r"[^\w\s]", " ", conteudo[0][1])).split())
    b = set(_norm(re.sub(r"[^\w\s]", " ", spec["titulo"])).split())
    if not a or not b:
        return False
    return len(a & b) / len(a | b) >= 0.6


def _junta(titulo, corpo):
    t = (titulo or "").rstrip()
    if not corpo:
        return t
    if t[-1:] in ".!?…":
        return f"{t} {corpo}"
    return f"{t}: {corpo}"


def _caption(spec, conteudo):
    corpo_pars = []
    if "compilacao" in spec:
        for (_k, titulo, corpo) in conteudo:
            corpo_pars.append(f"{titulo} — {corpo}")
    else:
        for (_k, titulo, corpo) in conteudo[1:4]:
            corpo_pars.append(_junta(titulo, corpo))
    partes = [spec["primeira_linha"]]
    partes += corpo_pars
    partes.append("📤 Envie este verbete para quem precisa ver. 📌 Salve para consultar depois.\n"
                  "📲 Dúvidas? Fale comigo pelo WhatsApp — link na bio.")
    partes.append(SIG + "\n" + DISC)
    partes.append(spec["tags"])
    return "\n\n".join(partes)


# Ângulo estético/estatura — colocações PROMOCIONAIS vetadas no nicho (o cfm_guardrails
# NÃO as cobre; controle positivo "alongamento estético para ganhar estatura" passou liso
# no auditar em 30/08). Menção defensiva ("nunca estética", "baixa estatura" como sinal
# clínico de raquitismo etc.) NÃO casa com estes padrões — e é conteúdo legítimo da casa.
_ANGULO_VETADO = (
    "alongamento estetico", "cirurgia estetica de alongamento",
    "ganhar estatura", "ganhar altura", "aumentar a estatura", "aumentar a altura",
    "aumentar sua altura", "ficar mais alto",
)


def _checagens(spec, caption, conteudo):
    """Guardrails de saída — falham ruidosamente (lição da casa: gate aprova por omissão)."""
    erros = []
    kw = _norm(spec["keyword"]).replace("?", "").strip()
    if kw not in _norm(spec["titulo"]):
        erros.append(f"keyword fora do título da capa: {spec['keyword']!r}")
    if kw not in _norm(caption[:125]):
        erros.append(f"keyword fora dos primeiros 125 caracteres da legenda: {spec['keyword']!r}")
    ntags = len(re.findall(r"#\S+", spec["tags"]))
    if not (4 <= ntags <= 6):
        erros.append(f"{ntags} hashtags (esperado 4–6)")
    textos = caption + " " + " ".join(f"{k} {t} {c or ''}" for (k, t, c) in conteudo)
    viol = [p for p in auditar(textos, "publico") if p[0] == "VIOLACAO"]
    for _s, regra, det in viol:
        erros.append(f"CFM VIOLACAO [{regra}]: {det}")
    ntxt = _norm(textos)
    for padrao in _ANGULO_VETADO:
        if padrao in ntxt:
            erros.append(f"ângulo estético/estatura vetado: {padrao!r}")
    return erros


def montar_verbete(spec, fontes, outdir):
    vid = _vid(spec)
    conteudo = _frames_conteudo(spec, fontes)
    if len(conteudo) != 5:
        raise RuntimeError(f"{vid}: esperava 5 frames de conteúdo, achei {len(conteudo)}")
    caption = _caption(spec, conteudo)
    erros = _checagens(spec, caption, conteudo)
    if erros:
        raise RuntimeError(f"{vid} REPROVADO: " + " | ".join(erros))
    # 8 slides; ou 7 quando o frame de abertura da fonte repetiria a capa-gancho
    miolo = conteudo[1:] if _capa_duplica_frame0(spec, conteudo) else conteudo
    n = 1 + len(miolo) + 2
    slides_img = [slide_capa(spec, vid, n)]
    for i, (kick, tit, corpo) in enumerate(miolo, 1):
        slides_img.append(slide_conteudo(kick, tit, corpo, vid, i, n))
    slides_img.append(slide_card_resumo(spec, _bullets_resumo(spec, conteudo), vid, n - 2, n))
    slides_img.append(slide_selo(vid, n - 1, n))
    pasta = os.path.join(outdir, vid)
    os.makedirs(pasta, exist_ok=True)
    paths = []
    for i, img in enumerate(slides_img, 1):
        assert img.size == (1080, 1350), f"{vid} s{i}: {img.size} != 1080x1350"
        p = os.path.join(pasta, f"s{i}.jpg")
        img.save(p, "JPEG", quality=92)
        paths.append(f"verbetes/{vid}/s{i}.jpg")
    tema = spec.get("tema") or (fontes[spec["fonte"]]["theme"] if "fonte" in spec else "")
    fonte_ids = ([sid for sid, _a in spec["compilacao"]] if "compilacao" in spec
                 else [spec["fonte"]])
    return {"id": vid, "tema": tema, "keyword": spec["keyword"], "fonte": fonte_ids,
            "slides": paths, "caption": caption,
            "alt": spec["primeira_linha"][:100]}


# ---------------------------------------------------------------------------
# 6) BIBLIOTECA (manifesto) — merge idempotente, NUNCA apaga item alheio
#    (mesma trava do gerar_temporadas.py; e NADA toca posts.json)
# ---------------------------------------------------------------------------
def gravar_manifesto(itens, caminho):
    atuais = []
    try:
        with open(caminho, encoding="utf-8") as f:
            atuais = json.load(f)
    except FileNotFoundError:
        pass
    except (json.JSONDecodeError, OSError) as e:
        print(f"AVISO: manifesto ilegível ({e!r}) — recriando só com os itens desta rodada.",
              flush=True)
    novos = {it["id"]: it for it in itens}
    saida = [novos.pop(it["id"], it) if isinstance(it, dict) else it for it in atuais]
    saida += list(novos.values())
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(saida, f, ensure_ascii=False, indent=2)
    return len(saida)


def renderizar(ids=None, outdir=None, manifesto=True):
    fontes = carregar_fontes()
    outdir = outdir or os.path.join(ROOT, "verbetes")
    por_fonte = {}
    for spec in CURADORIA:
        por_fonte[_vid(spec)] = spec
        if "fonte" in spec:
            por_fonte[spec["fonte"]] = spec
    if ids:
        specs, vistos = [], set()
        for i in ids:
            if i not in por_fonte:
                raise SystemExit(f"id sem curadoria: {i!r} (verbete exige entrada na CURADORIA "
                                 "— keyword/legenda não se inventam)")
            s = por_fonte[i]
            if _vid(s) not in vistos:
                specs.append(s); vistos.add(_vid(s))
    else:
        specs = CURADORIA
    itens = []
    for spec in specs:
        it = montar_verbete(spec, fontes, outdir)
        itens.append(it)
        print(f"ok {it['id']}  ({len(it['slides'])} slides)  kw='{it['keyword']}'", flush=True)
    if manifesto:
        total = gravar_manifesto(itens, os.path.join(os.path.dirname(outdir),
                                                     "verbetes_biblioteca.json"))
        print(f"BIBLIOTECA: {len(itens)} verbete(s) nesta rodada | {total} no manifesto "
              "(fila de posts INTOCADA — publicação só no D-day)")
    return itens


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("ids", nargs="*", help="ids de sequência-fonte ou de verbete (vazio = curadoria dos 20)")
    ap.add_argument("--listar", action="store_true")
    ap.add_argument("--outdir", default=None)
    ap.add_argument("--sem-manifesto", action="store_true")
    args = ap.parse_args()
    if args.listar:
        for i, spec in enumerate(CURADORIA, 1):
            fonte = ",".join(s for s, _a in spec["compilacao"]) if "compilacao" in spec else spec["fonte"]
            print(f"{i:2d}. {fonte:—<46} {spec['keyword']}")
        return
    renderizar(args.ids or None, outdir=args.outdir, manifesto=not args.sem_manifesto)


if __name__ == "__main__":
    main()
