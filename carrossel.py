# -*- coding: utf-8 -*-
"""
Gerador de CARROSSEL para o feed (4:5, 1080x1350).
Cada post = capa (gancho + ilustração + 'arraste') -> slides de conteúdo (1 ideia cada) -> CTA.

IDENTIDADE (v2, 14/10/2026 — "dentro da personalização" do Rafael): primitivas visuais em
marca.py — tipografia do SITE (Playfair Display + Inter), monograma RV REAL, paleta do site
(#14141A / #F3E2C8 / #B08C4F), cabeçalho igual à frente do cartão, ilustrações em traço fino
(fixador circular / eixo do membro) e rodapé CFM com "Médico". A API pública deste módulo
(W, H, M, F, SB/NR/NB, SIG, DISC, wrap, trk, base, footer, render_post, _var) é a mesma da v1:
gerar_verbetes.py, gerar_lote_2026.py e o lint CFM continuam funcionando sem mudança de chamada.
CFM: educativo, sem prometer resultado, sem paciente real, assinatura + disclaimer em todo
slide. Guardrail: nada de alongamento sob ângulo estético/altura.
"""
import os, json, re
from PIL import Image, ImageDraw, ImageFont
import marca as K

W, H = K.W, K.H; M = 110
INK = K.TINTA; CREAM = K.CREME; GOLD = K.OURO; TXT = K.CORPO; MUT = K.CINZA; FAINT = K.FIO
FD = "/usr/share/fonts/truetype/liberation/"; SB = "LiberationSerif-Bold.ttf"; NR = "LiberationSans-Regular.ttf"; NB = "LiberationSans-Bold.ttf"
SIG = "Dr. Rafael Vargas · Médico · CRM-SP 226103 · RQE 137901"; DISC = "Conteúdo educativo · não substitui avaliação médica."
_FC = {}
def F(n, s):
    """Nomes antigos (SB/NR/NB) -> tipografia da marca (Playfair/Inter), com fallback Liberation."""
    papel = K.PAPEL_DE_ARQUIVO.get(n)
    if papel:
        return K.fonte(papel, s)
    k = (n, s)
    if k not in _FC: _FC[k] = ImageFont.truetype(FD + n, s)
    return _FC[k]
_m = ImageDraw.Draw(Image.new("RGB", (8, 8)))
def wrap(t, f, mw):
    out = []; cur = ""
    for w in t.split():
        s = (cur + " " + w).strip()
        if _m.textlength(s, font=f) <= mw: cur = s
        else:
            if cur: out.append(cur)
            cur = w
    if cur: out.append(cur)
    return out
def trk(d, xy, text, font, fill, tr, left=True):
    x, y = xy
    if not left:
        wt = sum(d.textlength(c, font=font) + tr for c in text) - tr; x -= wt
    for c in text: d.text((x, y), c, font=font, fill=fill); x += d.textlength(c, font=font) + tr
# Variacao visual por peca (regra 4 v6 — feedback Leo 08/07). ADITIVO/fail-safe: sem o modulo, GOLD.
# v2: o repertório de motivos foi trocado por motivos da marca (marca.MOTIVO_DA_MARCA); o acento
# continua dentro da paleta quente e a escolha segue determinística por id.
try:
    import estilo_variacao as _EV
except Exception:
    _EV = None
def _var(post_id):
    return _EV.variante(post_id) if _EV else None

# ------------------------------------------------------------------ primitivas (API v1) -----
def base(motif=True, var=None):
    """Fundo da marca + cabeçalho (monograma | nome). Devolve (img RGB, draw) como na v1."""
    img = K.fundo(var if motif else {"motivo": "diagonais"})
    K.cabecalho(img, x=M)
    img = img.convert("RGB")
    return img, ImageDraw.Draw(img)

def footer(d, page, n, cta=False, ac=GOLD):
    K.rodape(d, page, n, ac=ac, x=M, sig=SIG, disc=DISC)

# ------------------------------------------------------------------ layout v2 ---------------
_HEROI_PED = ("pnc", "pernas", "marcha", "joelho", "ped", "crianc", "pe_", "quadril", "escoliose")
def heroi_de(post_id, pedido=None):
    """Ilustração da capa: 'eixo' (Ortopedia Pediátrica) ou 'fixador' (Reconstrução)."""
    if pedido in ("eixo", "fixador"): return pedido
    pid = post_id.lower()
    return "eixo" if any(t in pid for t in _HEROI_PED) else "fixador"

def _num_e_rotulo(kicker, page):
    """'2 — pouco sangue' -> ('2', 'Pouco sangue'); 'Sinais' -> (str(page), 'Sinais')."""
    k = (kicker or "").strip()
    m = re.match(r"^\s*(\d+)\s*[—–-]\s*(.+)$", k)
    if m:
        n, r = m.group(1), m.group(2).strip()
    else:
        n, r = str(page), k
    return n, (r[:1].upper() + r[1:]) if r else r

def _pilha(blocos):
    """Altura total de uma pilha de blocos [(altura, espaço_depois)]."""
    return sum(h + e for h, e in blocos)

def _texto_bloco(d, x, y_topo, linhas, papel, tam, cor, entrelinha):
    """Escreve linhas a partir do TOPO (y do topo da 1ª linha). Devolve o y do fim do bloco."""
    asc, _ = K.metr(papel, tam)
    y = y_topo + asc
    for ln in linhas:
        K.escreve(d, x, y, ln, papel, tam, cor)
        y += entrelinha
    return y - entrelinha + K.metr(papel, tam)[1]

def slide_capa(img, d, s, post_id, page, n, var, ac, heroi=None, numero_serie=None, rotulo=None):
    """Capa editorial: ilustração em traço fino à direita, gancho em Playfair à esquerda."""
    tipo = heroi_de(post_id, heroi)
    if tipo == "fixador":
        caixa = (590, 190, 1060, 1160); col = 455
    else:
        caixa = (680, 190, 1000, 1165); col = 540
    K.heroi(img, tipo, caixa, cor=ac)
    he = var["hook_escala"] if var else 1.0
    tam, linhas = K.ajusta(s["title"], K.TITULO, int(86 * he), 58, col, 5)
    ent_t = int(tam * 1.13)
    sub = s.get("sub") or ""
    stam = 32
    slinhas = K.quebra(sub, K.TEXTO, stam, col) if sub else []
    blocos = []
    if numero_serie:
        blocos.append((118, 40))
    rot = rotulo if rotulo is not None else (s.get("kicker") or "")
    if rot:
        blocos.append((26, 30))
    blocos.append((len(linhas) * ent_t, 34))
    blocos.append((2, 30 if slinhas else 0))
    if slinhas:
        blocos.append((len(slinhas) * 46, 0))
    alt = _pilha(blocos)
    dy = int((var["dy"] if var else 0) * 0.5)
    y = max(250, int(200 + (1160 - 200 - alt) / 2) - 20 + dy)
    if numero_serie:
        num, tot = numero_serie
        base_n = y + 104          # algarismos de estilo antigo descem abaixo da linha de base
        w = K.escreve(d, M - 6, base_n, num, K.TITULO_IT, 132, ac)
        K.escreve(d, M + w + 8, base_n, "/" + tot, K.TITULO_IT, 46, K.CINZA)
        y += 118 + 40
    if rot:
        K.escreve(d, M, y + 20, rot, K.TEXTO_MED, 22, ac, tr=1.4)
        y += 26 + 30
    y = _texto_bloco(d, M, y, linhas, K.TITULO, tam, CREAM, ent_t)
    y += 34
    K.filete(d, M, y, 72, ac, 2)
    y += 30
    if slinhas:
        _texto_bloco(d, M, y, slinhas, K.TEXTO, stam, TXT, 46)
    K.arraste(d, M, H - 200, ac)

def slide_conteudo(img, d, s, page, n, var, ac, numero=None, rotulo=None):
    """Conteúdo: numeral itálico grande (a sequência) + rótulo, título, filete, corpo.
    O bloco é dimensionado para OCUPAR a área útil (sem metade vazia) e centrado nela."""
    num, rot = _num_e_rotulo(s.get("kicker", ""), page)
    if numero is not None: num = numero
    if rotulo is not None: rot = rotulo
    # "Sinal 2" ao lado do numeral 2 repete o número: fica só "Sinal"
    rot = re.sub(r"\s+" + re.escape(str(num)) + r"$", "", rot or "")
    larg = W - 2 * M
    corpo = s.get("body") or s.get("sub") or ""
    AREA0, AREA1 = 215, 1165
    for tam_ini, ctam_ini in ((96, 42), (88, 40), (80, 38), (72, 36), (64, 34)):
        tam, linhas = K.ajusta(s["title"], K.TITULO, tam_ini, tam_ini - 8, larg, 4)
        ent_t = int(tam * 1.12)
        ctam = ctam_ini
        clinhas = K.quebra(corpo, K.TEXTO, ctam, larg) if corpo else []
        ent_c = int(ctam * 1.46)
        NUM = 172
        alt = NUM + 30 + len(linhas) * ent_t + 38 + 2 + 36 + len(clinhas) * ent_c
        if alt <= (AREA1 - AREA0) - 40:
            break
    dy = int((var["dy"] if var else 0) * 0.4)
    y = int(AREA0 + (AREA1 - AREA0 - alt) / 2) + 18 + dy
    base_num = y + int(NUM * 0.80)
    wn = K.escreve(d, M - 10, base_num, num, K.TITULO_IT, NUM, ac)
    if rot:
        K.escreve(d, M + wn + 28, base_num - 18, rot, K.TEXTO_MED, 27, K.OURO_CLARO, tr=1.2)
    y = y + NUM + 30
    y = _texto_bloco(d, M, y, linhas, K.TITULO, tam, CREAM, ent_t)
    y += 38
    K.filete(d, M, y, 80, ac, 2)
    y += 36
    if clinhas:
        _texto_bloco(d, M, y, clinhas, K.TEXTO, ctam, TXT, ent_c)

def slide_cta(img, d, s, page, n, var, ac):
    """Fecho centrado, como a frente do cartão: monograma, chamada, filete, contato."""
    cx = W // 2
    larg = W - 2 * M - 40
    rot = s.get("kicker") or ""
    tam, linhas = K.ajusta(s["title"], K.TITULO, 90, 62, larg, 3)
    ent_t = int(tam * 1.12)
    sub = s.get("sub") or ""
    stam = 37
    slinhas = K.quebra(sub, K.TEXTO, stam, larg - 60, equilibra=True) if sub else []
    ent_s = int(stam * 1.45)
    MONO = 150
    contato = s.get("contato", True)   # o lote 2 já traz o convite no próprio texto
    alt = (MONO + 56) + (40 if rot else 0) + len(linhas) * ent_t + 40 + 2 + 38 \
        + len(slinhas) * ent_s + (84 + 40 + 40 if contato else 0)
    y = int(215 + (1165 - 215 - alt) / 2) + 10
    K.monograma(img, cx, y + MONO / 2, MONO, CREAM, ancora="centro")
    y += MONO + 56
    if rot:
        K.escreve(d, cx, y + 22, rot, K.TEXTO_MED, 24, ac, tr=1.4, alinha="centro")
        y += 40 + 18
    asc, _ = K.metr(K.TITULO, tam)
    yy = y + asc
    for ln in linhas:
        K.escreve(d, cx, yy, ln, K.TITULO, tam, CREAM, alinha="centro"); yy += ent_t
    y = yy - ent_t + K.metr(K.TITULO, tam)[1] + 40
    d.line([(cx - 40, y), (cx + 40, y)], fill=ac, width=2)
    y += 38
    asc, _ = K.metr(K.TEXTO, stam)
    yy = y + asc
    for ln in slinhas:
        K.escreve(d, cx, yy, ln, K.TEXTO, stam, TXT, alinha="centro"); yy += ent_s
    if contato:
        y = yy - ent_s + 84
        K.escreve(d, cx, y, "Agende pelo WhatsApp", K.TEXTO_MED, 33, ac, alinha="centro")
        K.escreve(d, cx, y + 44, "link na bio", K.TEXTO, 27, TXT, alinha="centro")

def slide_resumo(img, d, titulo, bullets, var, ac, fecho="", rotulo="Para guardar"):
    """Card-resumo guardável: rótulo, título, filete e itens (lead dourado + corpo). Usado no
    último slide dos verbetes e no card de faixas em cm (gerar_card_resumo_discrepancia.py)."""
    larg = W - 2 * M
    tl_tam, tl = K.ajusta(titulo, K.TITULO, 64, 46, larg, 2)
    ent_tl = int(tl_tam * 1.12)
    for lt, bt in ((33, 30), (31, 28), (29, 27), (28, 25), (27, 24), (26, 23)):
        itens = []
        alt = 54 + len(tl) * ent_tl + 40 + 2 + 44
        for lead, corpo in bullets:
            ll = K.quebra(lead, K.TEXTO_MED, lt, larg - 44)
            bl = K.quebra(corpo, K.TEXTO, bt, larg - 44) if corpo else []
            h = len(ll) * int(lt * 1.3) + ((10 + len(bl) * int(bt * 1.42)) if bl else 0)
            itens.append((ll, bl, h))
            alt += h + 30
        fl = K.quebra(fecho, K.TEXTO, 24, larg) if fecho else []
        alt += 14 + len(fl) * 34
        if alt <= 930:
            break
    y = int(215 + (1165 - 215 - alt) / 2) + 10
    if rotulo:
        K.escreve(d, M, y + 22, rotulo, K.TEXTO_MED, 24, ac, tr=1.4)
    y += 54
    y = _texto_bloco(d, M, y, tl, K.TITULO, tl_tam, CREAM, ent_tl) + 40
    K.filete(d, M, y, 80, ac, 2)
    y += 44
    for ll, bl, h in itens:
        a1, _ = K.metr(K.TEXTO_MED, lt)
        ym = y + a1 - int(lt * 0.36)
        d.line([(M, ym), (M + 20, ym)], fill=ac, width=3)
        _texto_bloco(d, M + 44, y, ll, K.TEXTO_MED, lt, K.OURO_CLARO, int(lt * 1.3))
        if bl:
            _texto_bloco(d, M + 44, y + len(ll) * int(lt * 1.3) + 10, bl, K.TEXTO, bt, TXT, int(bt * 1.42))
        y += h + 30
    y += 14
    for ln in fl:
        K.escreve(d, M, y + 24, ln, K.TEXTO, 24, K.CINZA)
        y += 34

def render_post(post, outdir):
    sl = post["slides"]; n = len(sl); paths = []
    os.makedirs(outdir, exist_ok=True)
    pid = post.get("id", "")
    var = _var(pid); AC = var["acento"] if var else GOLD
    for i, s in enumerate(sl):
        capa_ou_cta = (i == 0) or (bool(s.get("cta")) and not s.get("resumo"))
        img = K.fundo(var if capa_ou_cta else {"motivo": "diagonais"})
        K.cabecalho(img, x=M)
        d = ImageDraw.Draw(img)
        if i == 0:
            pedido = post.get("heroi") or ("eixo" if "pediátr" in (s.get("kicker") or "").lower() else None)
            slide_capa(img, d, s, pid, i, n, var, AC, heroi=pedido)
        elif s.get("resumo"):
            slide_resumo(img, d, s["title"], s.get("bullets", []), var, AC, fecho=s.get("fecho", ""),
                         rotulo=s.get("kicker", "Para guardar"))
        elif s.get("cta"):
            slide_cta(img, d, s, i, n, var, AC)
        else:
            slide_conteudo(img, d, s, i, n, var, AC)
        footer(d, i, n, cta=s.get("cta", False), ac=AC)
        p = os.path.join(outdir, f"{post['id']}_{i+1}.jpg")
        img.convert("RGB").save(p, "JPEG", quality=92); paths.append("images/" + os.path.basename(p))
    return paths

# ---- exemplo: refaz o post03 'Fixador externo' como CARROSSEL ----
EXEMPLO={"id":"post03","slides":[
 {"kicker":"Educativo","title":"Fixador externo: pra que serve?","sub":"E por que não é “caso perdido”. Arrasta que eu explico."},
 {"kicker":"O que é","title":"Uma estrutura por fora do corpo","body":"Hastes e pinos seguram o osso por fora da pele, estabilizando enquanto ele cura ou se reconstrói."},
 {"kicker":"Pra que serve","title":"Estabilizar o que é complexo","body":"Fraturas graves, ossos que não colaram e correção de deformidades — situações em que o gesso não basta."},
 {"kicker":"A vantagem","title":"Ajuste fino, sem nova cirurgia","body":"Por ficar por fora, dá pra corrigir aos poucos ao longo do tratamento, sem reabrir a cada etapa."},
 {"kicker":"Mito x Verdade","title":"Não é “gaiola” nem fim de linha","body":"É uma ferramenta precisa e temporária. Na maioria dos casos, sai quando o osso cumpre seu papel."},
 {"kicker":"Passa adiante","cta":True,"title":"Salve e mande pra quem precisa","sub":"Para um familiar que vai passar por isso, ou que ficou assustado com o aparelho."},
]}

if __name__=="__main__":
    ROOT=os.path.dirname(os.path.abspath(__file__))
    paths=render_post(EXEMPLO, os.path.join(ROOT,"images"))
    print("slides gerados:", len(paths)); print(paths)

# ================= BIBLIOTECA DOS 9 (panfletos -> carrosseis) =================
def cta(t,s): return {"cta":True,"kicker":"Passa adiante","title":t,"sub":s}
POSTS=[
 {"id":"post03","slides":[
  {"kicker":"Educativo","title":"Fixador externo: pra que serve?","sub":"E por que não é “caso perdido”. Arrasta que eu explico."},
  {"kicker":"O que é","title":"Uma estrutura por fora do corpo","body":"Hastes e pinos seguram o osso por fora da pele, estabilizando enquanto ele cura ou se reconstrói."},
  {"kicker":"Pra que serve","title":"Estabilizar o que é complexo","body":"Fraturas graves, ossos que não colaram e correção de deformidades — quando o gesso não basta."},
  {"kicker":"A vantagem","title":"Ajuste fino, sem nova cirurgia","body":"Por ficar por fora, dá pra corrigir aos poucos ao longo do tratamento, sem reabrir a cada etapa."},
  {"kicker":"Mito x Verdade","title":"Não é “gaiola” nem fim de linha","body":"É uma ferramenta precisa e temporária. Costuma sair quando o osso cumpre seu papel."},
  cta("Salve e mande pra quem precisa","Para um familiar que vai passar por isso ou que se assustou com o aparelho.")]},
 {"id":"post04","slides":[
  {"kicker":"Educativo","title":"Uma perna mais curta que a outra?","sub":"Quando é só detalhe e quando merece um olhar. Arrasta."},
  {"kicker":"O que é comum","title":"Pequenas diferenças existem","body":"Diferenças de poucos milímetros são frequentes e muitas vezes não causam sintoma algum."},
  {"kicker":"Quando investigar","title":"Quando passa a incomodar","body":"Se aumenta, faz mancar, dói, ou apareceu depois de fratura ou infecção — vale avaliar."},
  {"kicker":"Na criança","title":"O crescimento muda tudo","body":"Acompanhar a evolução ao longo do tempo é parte do diagnóstico, não só uma medida isolada."},
  {"kicker":"O que define","title":"Medir certo guia a conduta","body":"A avaliação clínica somada à imagem diz se é observar, usar palmilha ou tratar."},
  cta("Salve pra lembrar dos sinais","E mande pra um pai ou mãe que está com essa dúvida em casa.")]},
 {"id":"post05","slides":[
  {"kicker":"Educativo","title":"Fratura que não cola?","sub":"Tem nome — pseudartrose — e tem caminho. Arrasta."},
  {"kicker":"O que é","title":"O osso parou de consolidar","body":"Quando a fratura não “fecha” no tempo esperado, chamamos de pseudartrose."},
  {"kicker":"Por que acontece","title":"Quase sempre tem uma causa","body":"Instabilidade, pouca circulação no local, infecção ou perda de osso costumam estar por trás."},
  {"kicker":"O que muda","title":"O tratamento ataca a causa","body":"Estabilizar bem, estimular o osso e, às vezes, enxerto — o plano depende do motivo."},
  {"kicker":"A mensagem","title":"Não é azar, é um problema com plano","body":"Identificada a causa, existe estratégia. O importante é não deixar arrastar."},
  cta("Salve e compartilhe","Com alguém que está há meses com uma fratura que não cola.")]},
 {"id":"post07","slides":[
  {"kicker":"Sinais","title":"Quando procurar um especialista?","sub":"4 situações de caso complexo que pedem avaliação. Arrasta."},
  {"kicker":"Sinal 1","title":"Fratura que não colou","body":"Passou o tempo esperado e o osso não consolidou? Vale uma avaliação dedicada."},
  {"kicker":"Sinal 2","title":"Deformidade ou perna desigual","body":"Quando atrapalha andar ou a função, a correção entra em cena."},
  {"kicker":"Sinal 3","title":"Sequela de infecção ou perda de osso","body":"Depois de trauma ou infecção, existe caminho de reconstrução."},
  {"kicker":"Sinal 4","title":"Já operou e não resolveu","body":"Uma segunda opinião focada em reconstrução pode mudar o rumo."},
  cta("Salve esse checklist","E mande pra quem está nessa encruzilhada agora.")]},
 {"id":"post08","slides":[
  {"kicker":"Educativo","title":"Tratamento guiado e seriado","sub":"Por que fazer em etapas muda o resultado. Arrasta."},
  {"kicker":"O que é","title":"O tratamento acontece em etapas","body":"Em vez de tudo de uma vez, o caminho é dividido em passos com ajustes ao longo dele."},
  {"kicker":"Por que importa","title":"O corpo responde aos poucos","body":"Corrigir em etapas é mais preciso e seguro do que forçar tudo num momento só."},
  {"kicker":"O acompanhamento","title":"Cada retorno afina o plano","body":"Não é “colocar e esperar”: cada consulta ajusta a rota conforme a resposta."},
  {"kicker":"A mensagem","title":"Método costuma vencer pressa","body":"Paciência com direção entrega resultados melhores que a pressa sem plano."},
  cta("Salve e mande adiante","Pra quem está começando um tratamento longo e ansioso por respostas.")]},
 {"id":"post11","slides":[
  {"kicker":"Consultório","title":"Como é a sua consulta","sub":"O que esperar do primeiro encontro. Arrasta."},
  {"kicker":"Antes","title":"Leve seus exames e o histórico","body":"Raio-X, tomografia e o que já foi feito direcionam toda a avaliação."},
  {"kicker":"Na consulta","title":"Conversa, exame e imagens","body":"Entendo a queixa, examino e analiso os exames junto com você."},
  {"kicker":"O plano","title":"Você sai entendendo o caminho","body":"Diagnóstico, opções e próximos passos — claros, no seu tempo."},
  {"kicker":"Onde","title":"Av. Paulista, São Paulo","body":"Atendimento em consultório, com agendamento pelo WhatsApp."},
  cta("Agende a sua avaliação","Manda “consulta” no WhatsApp do link da bio que a gente organiza.")]},
 {"id":"post12","slides":[
  {"kicker":"Dúvidas","title":"Dói? Quanto tempo? Volto a andar?","sub":"As 3 perguntas que todo mundo faz. Arrasta."},
  {"kicker":"Dói?","title":"O controle da dor é parte do plano","body":"Hoje há muitos recursos para manter o conforto durante o tratamento."},
  {"kicker":"Quanto tempo?","title":"Depende do caso","body":"Reconstruções costumam ser por etapas, com acompanhamento — o tempo é individual."},
  {"kicker":"Volto a andar?","title":"O objetivo é sempre função","body":"Andar e usar o membro é a meta. Cada caso é avaliado de forma própria."},
  {"kicker":"A mensagem","title":"Pergunte tudo na consulta","body":"Informação reduz o medo. Não existe pergunta boba sobre o seu tratamento."},
  cta("Salve essas respostas","E mande pra quem vai começar e está cheio de dúvidas.")]},
 {"id":"post14","slides":[
  {"kicker":"Educativo","title":"Sequela de infecção óssea?","sub":"Existe caminho de reconstrução. Arrasta."},
  {"kicker":"O que acontece","title":"A infecção deixa marcas","body":"Pode sobrar perda de osso, deformidade ou uma fratura que não cola."},
  {"kicker":"O primeiro passo","title":"Tratar a infecção é a base","body":"Sem resolver a infecção, qualquer reconstrução não se sustenta."},
  {"kicker":"A reconstrução","title":"Depois, restaura-se o osso","body":"Com a infecção controlada, dá pra recuperar o osso e o alinhamento em etapas."},
  {"kicker":"A mensagem","title":"Complexo, mas não sem saída","body":"É um caminho de etapas, com plano e acompanhamento próximo."},
  cta("Salve e compartilhe","Com alguém que carrega uma sequela e acha que não há mais o que fazer.")]},
 {"id":"post17","slides":[
  {"kicker":"Educativo","title":"Antes de operar, o planejamento muda tudo","sub":"A etapa invisível que mais pesa no resultado. Arrasta."},
  {"kicker":"O que é","title":"Estudar antes de cortar","body":"Analisar imagens, medir, simular e definir cada passo antes da cirurgia."},
  {"kicker":"Por que importa","title":"Decisão no improviso custa caro","body":"O que é resolvido no planejamento não precisa ser improvisado na sala."},
  {"kicker":"O que você ganha","title":"Menos surpresas, mais clareza","body":"Etapas definidas e expectativa realista desde o começo."},
  {"kicker":"A mensagem","title":"A cirurgia começa antes da sala","body":"O tempo investido em planejar é o que faz o resultado ser previsível."},
  cta("Salve e mande adiante","Pra quem vai operar e quer entender o que está por trás da decisão.")]},
]

def atualizar_todos():
    ROOT=os.path.dirname(os.path.abspath(__file__)); IMG=os.path.join(ROOT,"images")
    pj=os.path.join(ROOT,"posts.json"); posts=json.load(open(pj,encoding="utf-8"))
    by={e["id"]:e for e in posts}
    for post in POSTS:
        paths=render_post(post, IMG)
        if post["id"] in by:
            by[post["id"]]["images"]=paths
            # remove a imagem unica antiga (postNN.jpg) se existir
            old=os.path.join(IMG,post["id"]+".jpg")
            try:
                if os.path.exists(old): os.remove(old)
            except Exception: pass
        print("ok", post["id"], "->", len(paths), "slides")
    json.dump(posts, open(pj,"w",encoding="utf-8"), ensure_ascii=False, indent=2)
    print("posts.json atualizado")

if __name__=="__main__":
    atualizar_todos()
