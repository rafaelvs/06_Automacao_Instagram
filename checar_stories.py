# -*- coding: utf-8 -*-
"""Portão dos STORIES COMO FUNCIONA com roteiro próprio (Rafael, 24/10/2026).

O Rafael escolheu, para os stories, "story com roteiro próprio": peça NOVA, escrita para story,
com outro ângulo do tema do reel publicado 2-3 dias antes — não é o reel cortado. Formato da geração
nova (processo de 24/10, mesmo do COMO FUNCIONA: diagnóstico, 3 desenhos, crítica, síntese):
"COMO FUNCIONA EM 3 TOQUES" — 3 vídeos curtos sem voz (espanto, mecanismo, o que isso muda), cada um
com um TRECHO em movimento do mp4 aprovado do reel (recorte + zoom) e texto próprio por cima; o
toque do público dispara a mudança. Renderizados por story_cf.py a partir de stories_cf.json.

Este módulo é Python puro (o job de publicação não tem skia) e responde três perguntas:
  1. A story está no formato? (3 telas na ordem, título de 2 linhas de até 20 caracteres, texto
     dentro do limite, chamada de ENVIO sem contato, tema classificável, ilustração no quadro).
  2. Ela pode sair? Aprovada pelo Rafael (lote VÁLIDO em aprovacoes.json — status 'aprovado',
     aprovado_por + evidencia, registro que não é minuta — com a entrada de --entrada: o hash do TEXTO,
     o sha256 dos 3 vídeos e o hash do gerador do render que ele viu; entrada só de texto = pendente),
     vídeos amarrados ao texto, ao
     gerador e aos parâmetros de render atuais pelo arquivo-irmão, render do CI (Roboto), todo texto
     desenhado dentro da story ou do conjunto genérico e todo texto da story desenhado, CFM limpo,
     nenhum chamado a DM/contato, identificação em toda tela.
  3. É o dia dela? O reel de referência tem de ter saído NO GRID (modo trial não conta) há pelo menos
     2 dias (a tela 3 diz "Vídeo completo no perfil": sem o reel no perfil, seria mentira).

API (a MESMA régua para o CI, o publish.py, o story_cf.py e a agenda)
---------------------------------------------------------------------
Problemas são ESTRUTURADOS: lista de (tipo, mensagem), tipo em TIPOS:
  'formato'   estrutura, limites, chamada fora da regra (legenda.cta_de_envio), tema inválido ou
              não classificável;
  'conteudo'  CFM, chamado a DM/contato/agendamento em título/texto/chamada, a lista negra de texto em
              imagem do carrossel (deslize, arraste, salve, antes e depois, cura, altura, '!'...), texto desenhado fora da
              story, texto da story NÃO desenhado (cobertura), identificação ou "Vídeo completo no
              perfil" ausentes;
  'aprovacao' aprovação pendente ou que não vale mais (divergente);
  'render'    irmão ausente ou de outro texto/gerador/parâmetro de render, vídeo trocado/ausente/fora
              do lugar, duração, reel de origem trocado, fonte que não é a do CI (Roboto).

  veredito(st, aprovacoes, reels_por_id, exigir_render=False) -> dict
      {'id', 'situacao' ('aprovada'|'pendente'|'divergente'), 'detalhe', 'problemas', 'erros',
       'avisos', 'pode_sair'}. A ÚNICA função de veredito (main() do CI e publish):
        story APROVADA: todo problema é erro; pode_sair = sem erro.
        story NÃO aprovada: 'aprovacao' e 'render' são AVISO (o texto sobe antes, o render-stories.yml
        roda depois); 'formato' e 'conteudo' são SEMPRE erro; pode_sair = False.
        exigir_render=True (passo do render-stories.yml): 'render' é erro mesmo na pendente.
  incertas(publicados) -> [story_id]   parte INCERTA no estado: o publish não publica nada (erro).
  retomada(fila, publicados, hoje_brt) -> (st, situacao, detalhe)
        situacao 'retomada' (story com 1-2 partes no ar e a 1ª parte do MESMO dia BRT: o publish
        publica só as que faltam, com veredito pode_sair) | 'incompleta_expirada' (1ª parte de outro
        dia, ou render trocado depois dela: no Instagram a parte 1 já expirou — o publish NÃO completa,
        levanta erro e espera decisão humana) | None (nenhuma incompleta). Se o registro da parte no
        estado trouxer 'sha256' (o publish deve gravar o do irmão), a retomada confere que o render
        não mudou entre as partes.
  candidatas(fila, publicados, aprovacoes, hoje_brt, reels_por_id=None, detalhar=True) -> (cands, fora)
        cands = stories sem parte publicada, no calendário (no_calendario) e APROVADAS, na ordem da
        fila; fora = [(id, 'aviso'|'erro', msg)] das NÃO aprovadas no calendário, tiradas ANTES da
        escolha por tema (uma pendente de tema antigo nunca mais trava as aprovadas): 'aviso' para
        aprovação/render, 'erro' para formato/conteúdo (o publish publica a escolhida e fica vermelho).
        Aprovada com render quebrado CONTINUA candidata: escolhida, o veredito barra (vermelho), nunca
        é pulada em silêncio.
  escolher(cands, publicados, hoje_brt, futuras=None, n=None, fila=None) -> (st | None, motivo)
        distância entre temas + tema mais antigo primeiro (temas_conteudo.escolher).
  no_calendario(st, publicados, hoje_brt) / data_do_reel(reel_id, publicados)
        reel de origem publicado fora do modo trial há >= DIAS_DEPOIS_DO_REEL dias; aplicado SEMPRE
        (com qualquer distância de tema, inclusive n < 0).
  entrada_de_aprovacao(id) -> dict   a entrada pronta para o lote do aprovacoes.json: hash do texto,
        sha256 dos 3 vídeos e hash do gerador do render que o Rafael viu (só sai com render coerente).
        É a ÚNICA forma de entrada que aprova (aprovacao_de); o lote precisa de aprovado_por + evidencia.
  Compatibilidade: problemas_de_formato(st) -> [str] (tudo o que se confere só no TEXTO, menos o
  CFM); problemas_de_publicacao(...) -> [str] (= mensagem de aprovação, se não aprovada, + erros do
  veredito); proxima_story(...) (retomada; incompleta_expirada LEVANTA RuntimeError; com `aprovacoes`
  usa candidatas()).
  Ordem esperada no publish (agendado): incertas -> retomada -> candidatas -> escolher -> veredito.
  FORCE_ID=story:<id> (decisão humana): ignora a distância de 2 dias, mas exige o reel no grid e
  veredito pode_sair; pendente ou já completa = erro (pedido humano que não publica não fica verde).

Uso:  python checar_stories.py                       (confere a fila; regra do veredito)
      python checar_stories.py --ids stn_a stn_b     (só esses ids; vírgula também separa)
      python checar_stories.py --ids X --exigir-render   (render-stories.yml: o render TEM de passar)
      python checar_stories.py --entrada stn_x       (imprime a entrada do lote de aprovação)
      python checar_stories.py --autoteste           (controles positivos e negativos de cada guarda)
"""
import datetime as dt
import hashlib
import io
import json
import os
import re
import sys
import unicodedata

ROOT = os.path.dirname(os.path.abspath(__file__))
FILA = os.path.join(ROOT, "stories_cf.json")
PASTA = "stories_cf"                       # relativo ao repo (vai para a raw URL)
GERADOR = os.path.join(ROOT, "story_cf.py")
APROVACOES = os.path.join(ROOT, "aprovacoes.json")
ESCOPO = "instagram-stories"

SIG = "Dr. Rafael Vargas · Médico · CRM-SP 226103 · RQE 137901"
DISC_ST = "Conteúdo educativo · não substitui avaliação médica"   # sem narração: sem "voz digital (IA)"
SELO = "COMO FUNCIONA"
PERFIL = "Vídeo completo no perfil"
TOCA = "toca →"                            # nunca "deslize": no story, deslizar leva para OUTRA conta
NOME = "toque no nome lá em cima ↖"
GENERICO = {SIG, DISC_ST, SELO, PERFIL, TOCA, NOME}
OBRIGATORIOS = {SIG, DISC_ST}             # identificação CFM em TODA tela, desde o quadro 0

TIPOS = ("formato", "conteudo", "aprovacao", "render")
PAPEIS = ("espanto", "mecanismo", "significado")
LIM_TITULO = 20
LIM_TEXTO = {"espanto": 70, "mecanismo": 120, "significado": 120}   # a regra da série é 70; o portão aceita 120
LIM_CTA = 60
DUR_TRECHO_MAX = 8.0                       # segundos de reel por tela
DUR_MIN, DUR_MAX = 3.0, 60.0               # limite de vídeo em story da API
DIAS_DEPOIS_DO_REEL = 2
MODOS_REEL_NO_GRID = (None, "normal", "fallback_normal")   # 'trial' = só não-seguidores, fora do grid
FONTE_DO_CI = "Roboto-"                    # o molde se aprova pelo render do runner (render-stories.yml)
PAPEIS_FONTE = ("black", "bold", "semi", "reg")
# o que muda o vídeo sem mudar o texto (fica fora do hash da aprovação, dentro do hash_render)
CAMPOS_RENDER = ("trecho", "crop", "zoom", "ancora", "foco_x", "esmaecer", "dur",
                 "t_titulo", "t_texto", "t_toca", "t_cartao", "t_perfil", "t_nome")
CAMPOS_CAMERA = ("zoom", "ancora", "foco_x", "esmaecer")
# chamado a contato/DM/agendamento (texto normalizado sem acento, minúsculo) — mesma família do
# checar_carrossel.LEGENDA_DM e da LISTA_NEGRA_IMAGEM; legenda.cta_de_envio sozinha aceita "me escreve no privado"
CONTATO = re.compile(r"\b(dm|direct|inbox|privad[oa]s?|pv|whats ?app|zap|wpp|mensage\w*|me chama|chama no|"
                     r"me (manda|mande|escreve|escreva|envia|envie|liga|ligue)|fala comigo|link (na|da) bio|"
                     r"agend\w*|telefone|celular|contato|"
                     # verificação de 25/10: 'marque uma avaliação', 'fale com a nossa equipe' passavam
                     r"mar(c|q)\w* (uma |sua |a )?(consulta|avaliac\w*)|fal(e|ar|em) com (a gente|a (nossa )?equipe|nossa equipe))\b")
# texto desenhado em imagem: a MESMA lista negra do checar_carrossel.LISTA_NEGRA_IMAGEM (o story era a única
# superfície de texto queimado em imagem sem ela — verificação de 25/10), menos 'nenhuma' (resposta do carrossel) e
# os de DM/agenda (já em CONTATO). Texto normalizado sem acento, minúsculo.
LISTA_NEGRA_STORY = [
    (r"\baltura\b", "'altura'"), (r"estetic", "'estética'"), (r"antes e depois", "'antes e depois'"),
    (r"\bsalv(e|a|ar|em)\b", "'salvar' na imagem"), (r"\bdesliz", "'deslize' (no story, deslizar leva para OUTRA conta)"),
    (r"\barrast", "'arraste'"), (r"garantid", "'garantido'"), (r"\bcura\b", "'cura'"),
    (r"seu filho tem", "'seu filho tem'"), (r"!", "exclamação"),
]
BRT = dt.timezone(dt.timedelta(hours=-3))


def usar_raiz(raiz):
    """Aponta o módulo para outra raiz (testes). Devolve a raiz anterior."""
    global ROOT, FILA, GERADOR, APROVACOES
    velha = ROOT
    ROOT = raiz
    FILA = os.path.join(raiz, "stories_cf.json")
    GERADOR = os.path.join(raiz, "story_cf.py")
    APROVACOES = os.path.join(raiz, "aprovacoes.json")
    return velha


def carregar(caminho, padrao):
    try:
        with io.open(caminho, encoding="utf-8-sig") as f:
            return json.load(f)
    except FileNotFoundError:
        return padrao


def sha256_arquivo(caminho, texto=False):
    """sha256 do arquivo. `texto=True` normaliza CRLF -> LF: o clone do Windows (autocrlf) e o
    runner Linux têm de dar o MESMO hash para o mesmo gerador. Sem memória: o portão lê os bytes
    de hoje, sempre."""
    dados = open(caminho, "rb").read()
    if texto:
        dados = dados.replace(b"\r\n", b"\n")
    return "sha256:" + hashlib.sha256(dados).hexdigest()


def hash_gerador():
    return sha256_arquivo(GERADOR, texto=True)


def _hash_json(obj):
    s = json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return "sha256:" + hashlib.sha256(s.encode("utf-8")).hexdigest()


def texto_aprovavel(st):
    """O que o Rafael aprova pelo hash_roteiro: o TEXTO da story (id, reel, ângulo, títulos e textos).
    A escolha da ilustração (trecho, recorte, câmera, tempos) é parâmetro de render: fica no
    hash_render do irmão e, se o lote trouxer, nos sha256 dos vídeos que ele viu."""
    return {"id": st.get("id"), "reel_ref": st.get("reel_ref"), "angulo": st.get("angulo"),
            "variante": st.get("variante"), "cta": st.get("cta"),
            "telas": [{"papel": t.get("papel"), "titulo": list(t.get("titulo") or []), "texto": t.get("texto")}
                      for t in (st.get("telas") or [])]}


def hash_story(st):
    return _hash_json(texto_aprovavel(st))


def params_render(st):
    """Parâmetros de render de cada tela (o que muda o vídeo sem mudar o texto)."""
    return {"telas": [{k: t.get(k) for k in CAMPOS_RENDER} for t in (st.get("telas") or [])]}


def hash_render(st):
    """Gravado pelo story_cf.py no irmão; correção visual no JSON sem re-render = divergente."""
    return _hash_json(params_render(st))


def camera_de(tela):
    return {k: tela.get(k) for k in CAMPOS_CAMERA}


def _norm_ascii(s):
    return unicodedata.normalize("NFKD", str(s).lower()).encode("ascii", "ignore").decode()


def textos_da_story(st):
    """Títulos, textos e chamada (o texto que vai desenhado)."""
    return [s for _, s in _campos_de_texto(st)]


def contato_em(s):
    """Trecho de chamado a DM/contato/agendamento em `s` (ou None)."""
    m = CONTATO.search(_norm_ascii(s))
    return m.group(0) if m else None


def _formato(st):
    """[(tipo, msg)] do que se confere só no TEXTO da story: estrutura, limites, chamada, tema."""
    p = []

    def f(m):
        p.append(("formato", m))
    sid = st.get("id") or "?"
    if not isinstance(st.get("id"), str) or not re.fullmatch(r"(stn|st)_[a-z0-9_]{1,60}", st["id"]):
        f(f"{sid}: id tem de começar por 'stn_' (geração nova) ou 'st_' e ter só [a-z0-9_] (vai em nome de "
          "arquivo, na raw URL e no render-stories.yml)")
    if not st.get("reel_ref"):
        f(f"{sid}: sem reel_ref")
    telas = [t for t in (st.get("telas") or []) if isinstance(t, dict)]
    if [t.get("papel") for t in telas] != list(PAPEIS) or len(telas) != len(st.get("telas") or []):
        f(f"{sid}: telas têm de ser exatamente {PAPEIS} nessa ordem (veio {[t.get('papel') for t in telas]})")
    for t in telas:
        tit = t.get("titulo") or []
        if not isinstance(tit, list) or len(tit) != 2 or any(not isinstance(x, str) or not x.strip() for x in tit):
            f(f"{sid}/{t.get('papel')}: título tem de ter 2 linhas não vazias")
        for x in tit if isinstance(tit, list) else []:
            if isinstance(x, str) and len(x) > LIM_TITULO:
                f(f"{sid}/{t.get('papel')}: linha de título com {len(x)} > {LIM_TITULO} caracteres: {x!r}")
        tx = t.get("texto") or ""
        if not isinstance(tx, str):
            f(f"{sid}/{t.get('papel')}: texto tem de ser string"); tx = ""
        lim = LIM_TEXTO.get(t.get("papel"), 0)
        if len(tx) > lim:
            f(f"{sid}/{t.get('papel')}: texto com {len(tx)} > {lim} caracteres")
        if t.get("papel") != "espanto" and not tx.strip():
            f(f"{sid}/{t.get('papel')}: texto vazio")
        tr = t.get("trecho")
        if not (isinstance(tr, list) and len(tr) == 2 and all(isinstance(v, (int, float)) for v in tr)
                and 0 <= tr[0] < tr[1] and tr[1] - tr[0] <= DUR_TRECHO_MAX):
            f(f"{sid}/{t.get('papel')}: trecho do reel tem de ser [t0, t1] com 0 ≤ t0 < t1 e até {DUR_TRECHO_MAX}s")
        cr = t.get("crop")
        if not (isinstance(cr, list) and len(cr) == 4 and all(isinstance(v, (int, float)) for v in cr)
                and cr[0] >= 0 and cr[1] >= 0 and cr[2] > 0 and cr[3] > 0 and cr[0] + cr[2] <= 1080 and cr[1] + cr[3] <= 1920):
            f(f"{sid}/{t.get('papel')}: crop tem de ser [x, y, w, h] dentro de 1080x1920")
    cta = st.get("cta") if isinstance(st.get("cta"), str) else ""
    if not cta.lower().startswith("manda pra quem") or len(cta) > LIM_CTA:
        f(f"{sid}: cta tem de começar por 'Manda pra quem' e ter até {LIM_CTA} caracteres (veio {len(cta)})")
    else:
        try:
            import legenda
            if not legenda.cta_de_envio(cta):
                f(f"{sid}: cta não é pedido de ENVIO (legenda.cta_de_envio recusa: contato, agenda ou comentário): {cta!r}")
        except ImportError:
            f(f"{sid}: cta sem conferência (legenda.py ausente: portão da chamada cego — story NÃO sai)")
    if st.get("variante") not in ("A", "B"):
        f(f"{sid}: variante tem de ser 'A' (paradoxo) ou 'B' (sinal reconhecível)")
    try:
        import temas_conteudo
        for m in temas_conteudo.problemas_de_tema(st):
            f(m)
    except ImportError:
        f(f"{sid}: tema sem conferência (temas_conteudo.py ausente — story NÃO sai)")
    return p


def _campos_de_texto(st):
    """[(onde, texto)] de títulos, textos e chamada, com o lugar para a mensagem."""
    out = []
    for t in st.get("telas") or []:
        if isinstance(t, dict):
            out += [(f"{t.get('papel')}/título", x) for x in (t.get("titulo") or []) if isinstance(x, str) and x]
            if isinstance(t.get("texto"), str) and t["texto"]:
                out.append((f"{t.get('papel')}/texto", t["texto"]))
    if isinstance(st.get("cta"), str) and st["cta"]:
        out.append(("cta", st["cta"]))
    return out


def _contato(st):
    sid = st.get("id") or "?"
    return [("conteudo", f"{sid}: {onde} chama para DM/contato/agendamento ({m!r}) em {s!r} — proibido no story")
            for onde, s in _campos_de_texto(st) for m in [contato_em(s)] if m]


def _lista_negra(st):
    sid = st.get("id") or "?"
    return [("conteudo", f"{sid}: {onde} tem {det} — proibido em texto desenhado no story (lista do carrossel): {s!r}")
            for onde, s in _campos_de_texto(st) for rgx, det in LISTA_NEGRA_STORY if re.search(rgx, _norm_ascii(s))]


def cfm(textos):
    """VIOLACAO do guardrail CFM nos textos da story (sem exigir assinatura no texto: a
    identificação vai desenhada em toda tela e o portão confere isso à parte)."""
    try:
        from cfm_guardrails import auditar
    except ImportError:
        return ["cfm_guardrails ausente: portão CFM cego — story NÃO sai"]
    return [f"{r}: {d}" for nivel, r, d in auditar("\n".join(textos), "publico", exigir_assinatura_texto=False)
            if nivel == "VIOLACAO"]


def problemas_do_texto(st):
    """[(tipo, msg)] de tudo o que se confere só no texto: formato + contato/DM + lista negra de imagem + CFM."""
    sid = st.get("id") or "?"
    return (_formato(st) + _contato(st) + _lista_negra(st)
            + [("conteudo", f"{sid}: CFM {v}") for v in cfm(textos_da_story(st) + sorted(GENERICO))])


def problemas_de_formato(st):
    """Compatibilidade: [str] do que se confere só no TEXTO, menos o CFM (formato, chamada, tema,
    contato/DM, lista negra de imagem)."""
    return [m for _, m in _formato(st) + _contato(st) + _lista_negra(st)]


def textos_permitidos(tela, cta=""):
    tit = set(tela.get("titulo") or [])
    corpo = " ".join((tela.get("texto") or "").split())
    if tela.get("papel") == "significado" and cta:
        corpo = corpo + " \n " + " ".join(cta.split())       # a chamada só pode aparecer na tela 3
    return tit, corpo


def texto_fora(tela, desenhados, cta=""):
    """Textos desenhados que não são título, trecho contínuo do texto da tela (ou da chamada, na
    tela 3) ou genéricos. Comparação sem diferenciar caixa: a chamada vai em caixa alta no cartão."""
    tit, corpo = textos_permitidos(tela, cta)
    tit = {x.upper() for x in tit}; corpo_up = corpo.upper()
    fora = []
    for s in desenhados:
        s1 = " ".join(s.split())
        if s1 in GENERICO or s1.upper() in tit or (s1 and s1.upper() in corpo_up):
            continue
        fora.append(s)
    return fora


def cobre(alvo, pecas):
    """O texto `alvo` inteiro é a junção (com um espaço) de pedaços desenhados, em ordem? Sem
    diferenciar caixa (a chamada vai em caixa alta). Texto vazio está coberto."""
    alvo = " ".join(str(alvo or "").split()).upper()
    if not alvo:
        return True
    ps = sorted(x for x in {" ".join(str(p).split()).upper() for p in pecas} if x and x in alvo)
    alcance, pilha = {0}, [0]
    while pilha:
        i = pilha.pop()
        for pc in ps:
            if alvo.startswith(pc, i):
                j = i + len(pc)
                if j == len(alvo):
                    return True
                if alvo[j] == " " and j + 1 not in alcance:
                    alcance.add(j + 1); pilha.append(j + 1)
    return False


def problemas_de_desenho(tela, desenhados, cta=""):
    """[(tipo, msg)] do texto DESENHADO numa tela (o mesmo cheque no story_cf.py e no portão): nada a
    MAIS (texto fora da story), nada a MENOS (as 2 linhas do título, o texto inteiro e, na tela 3, a
    chamada inteira), identificação em toda tela e 'Vídeo completo no perfil' na tela 3."""
    p, nome = [], tela.get("papel")
    fora = texto_fora(tela, desenhados, cta)
    if fora:
        p.append(("conteudo", f"{nome}: texto desenhado fora da story: {fora}"))
    falta = OBRIGATORIOS - set(desenhados)
    if falta:
        p.append(("conteudo", f"{nome}: identificação ausente na tela: {sorted(falta)}"))
    if tela.get("papel") == "significado" and PERFIL not in desenhados:
        p.append(("conteudo", f"significado: falta '{PERFIL}'"))
    des_up = {" ".join(str(s).split()).upper() for s in desenhados}
    faltam = [x for x in (tela.get("titulo") or []) if " ".join(str(x).split()).upper() not in des_up]
    if faltam:
        p.append(("conteudo", f"{nome}: linha de título NÃO desenhada (cobertura): {faltam}"))
    if not cobre(tela.get("texto") or "", desenhados):
        p.append(("conteudo", f"{nome}: o texto da tela não foi desenhado inteiro (cobertura): {tela.get('texto')!r}"))
    if tela.get("papel") == "significado" and not cobre(cta, desenhados):
        p.append(("conteudo", f"{nome}: a chamada não foi desenhada inteira (cobertura): {cta!r}"))
    return p


def _entradas_do_lote(lote, sid):
    return [e for e in (lote.get("episodios") or []) if isinstance(e, dict) and e.get("id") == sid]


def defeito_do_lote(lote, aprovacoes):
    """Motivo pelo qual o lote NÃO autentica aprovação de story (None = lote válido). Fail-closed, a MESMA
    regra de checar_carrossel.defeito_do_lote e do checar_aprovacoes (v1.5/M2) — este último é o passo
    'Portao de aprovacao clinica' do publish.yml, que roda ANTES do publish.py: registro MINUTA, status ≠
    'aprovado' ou lote 'aprovado' sem aprovado_por + evidencia não vazios = não conta. Antes (auditoria de
    fechamento, 25/10/2026) o portão dos stories aprovava esse lote: o CI dos stories e a página diziam
    'aprovada' enquanto o portão clínico derrubava o publish INTEIRO (o reel do dia junto)."""
    if (aprovacoes or {}).get("MINUTA_AGUARDA_AVAL"):
        return "registro é MINUTA (MINUTA_AGUARDA_AVAL=true): minuta nunca aprova"
    if lote.get("status") != "aprovado":
        return f"status {lote.get('status')!r} (só 'aprovado' vale)"
    falta = [c for c in ("aprovado_por", "evidencia") if not str(lote.get(c) or "").strip()]
    if falta:
        return f"lote 'aprovado' sem {'+'.join(falta)} não vazio(s): aprovação sem autor/evidência não autentica"
    return None


def shas_do_irmao(meta):
    """sha256 dos 3 vídeos registrados no irmão, ou None se o irmão não os tem bem formados (ausente, outro
    número de partes, sha256 faltando)."""
    ps = (meta or {}).get("partes")
    if isinstance(ps, list) and len(ps) == len(PAPEIS) and \
            all(isinstance(p, dict) and isinstance(p.get("sha256"), str) and p["sha256"] for p in ps):
        return [p["sha256"] for p in ps]
    return None


def _entrada_amarrada(e):
    v, hg = e.get("videos"), e.get("hash_gerador")
    return isinstance(v, list) and len(v) == len(PAPEIS) and all(isinstance(x, str) and x for x in v) \
        and isinstance(hg, str) and bool(hg)


def aprovacao_de(st, aprovacoes, meta=None):
    """-> (situação, detalhe): 'aprovada' | 'pendente' | 'divergente'.

    Aprova SÓ quando um lote VÁLIDO (escopo LISTA com ESCOPO; defeito_do_lote: status 'aprovado',
    aprovado_por + evidencia, registro que não é minuta) traz, para o id, a entrada de --entrada: o hash
    do TEXTO (hash_roteiro), o sha256 dos 3 vídeos ('videos') e o hash do gerador ('hash_gerador') do
    render que o Rafael VIU — e 'videos'/'hash_gerador' batem com o arquivo-irmão.
      - Entrada só com o texto (sem 'videos' de 3 sha256 + 'hash_gerador') = 'pendente' ('aprovação visual
        não amarrada'), a regra do checar_carrossel: re-render COERENTE depois da aprovação (outro recorte,
        trecho, fonte, com irmão, hash_render e Roboto em dia) nunca sai com o aval de um vídeo que o Rafael
        não viu, e um lote só de texto não anula o amarrar de outro lote (auditoria de fechamento, 25/10).
      - Vídeos ou gerador ≠ irmão, ou texto mudou = 'divergente' (re-aprovar).
      - Irmão ausente ou malformado: não há o que comparar; a aprovação do texto + entrada amarrada vale
        como 'aprovada', e o veredito BARRA pelo 'render' (erro: a aprovada não sai e o job fica vermelho
        — nunca some da escolha em silêncio). Nada sai assim: pode_sair exige render sem problema, e
        irmão ausente/malformado é sempre problema de render.
    Lote com outro status (pendente, substituido...) = 'pendente' (não é divergência: ninguém aprovou)."""
    sid = st.get("id")
    hs = hash_story(st)
    motivos, divergente = [], False
    for lote in (aprovacoes or {}).get("lotes", []):
        if not isinstance(lote, dict):
            continue
        entradas = _entradas_do_lote(lote, sid)
        esc = lote.get("escopo")
        if not entradas or not isinstance(esc, list) or ESCOPO not in esc:
            continue
        nome = lote.get("lote")
        defeito = defeito_do_lote(lote, aprovacoes)
        if defeito:
            motivos.append(f"lote {nome}: {defeito}")
            continue
        for e in entradas:
            if e.get("hash_roteiro") != hs:
                divergente = True
                motivos.append(f"lote {nome}: texto mudou depois da aprovação (hash_roteiro ≠)")
                continue
            if not _entrada_amarrada(e):
                motivos.append(f"lote {nome}: aprovação visual não amarrada aos vídeos (a entrada precisa de 'videos' = "
                               f"sha256 dos {len(PAPEIS)} mp4 e 'hash_gerador' do render que o Rafael viu: gere com "
                               f"`python checar_stories.py --entrada {sid}`)")
                continue
            if meta is None:
                meta = carregar(irmao_de(st), {}) if isinstance(sid, str) else {}
            shas = shas_do_irmao(meta)
            if shas is None:
                return "aprovada", f"{nome} (vídeos não conferíveis: irmão ausente ou malformado — o render barra)"
            if e["videos"] != shas:
                divergente = True
                motivos.append(f"lote {nome}: os vídeos do irmão não são os que o Rafael aprovou (videos ≠)")
                continue
            if isinstance(meta.get("hash_gerador"), str) and e["hash_gerador"] != meta["hash_gerador"]:
                divergente = True
                motivos.append(f"lote {nome}: render de OUTRA versão do story_cf.py que a aprovada (hash_gerador ≠)")
                continue
            return "aprovada", f"{nome} (vídeos amarrados)"
    if not motivos:
        return "pendente", "sem lote de aprovação"
    return ("divergente" if divergente else "pendente"), "; ".join(motivos)


def irmao_de(st):
    return os.path.join(ROOT, PASTA, f"{st['id']}.json")


def arquivo_da_parte(sid, i):
    """O ÚNICO caminho que a parte i (0, 1, 2) pode ter: vai na raw URL que a Meta baixa."""
    return f"{PASTA}/{sid}_{i + 1}.mp4"


def _avaliar(st, aprovacoes, reels_por_id):
    """(situação, detalhe, [(tipo, msg)]) — tudo o que impede a story de sair, menos o calendário."""
    p = problemas_do_texto(st)
    sid = st.get("id") if isinstance(st.get("id"), str) else "?"
    meta = carregar(irmao_de(st), {}) if sid != "?" else {}
    situ, det = aprovacao_de(st, aprovacoes, meta)
    if situ != "aprovada":
        p.insert(0, ("aprovacao", f"{sid}: aprovação pendente ({det})" if situ == "pendente" else
                     f"{sid}: aprovação pendente — a existente não vale mais (divergente: {det})"))
    if any(t == "formato" for t, _ in p) or sid == "?":
        return situ, det, p                    # formato quebrado: o resto não se confere com segurança
    if not os.path.exists(irmao_de(st)):
        return situ, det, p + [("render", f"{sid}: sem arquivo-irmão {PASTA}/{sid}.json (render não feito)")]
    r = []
    if meta.get("hash_story") != hash_story(st):
        r.append(("render", f"{sid}: vídeos feitos de OUTRO texto (hash do irmão ≠ hash da story): re-renderize"))
    if meta.get("hash_gerador") != hash_gerador():
        r.append(("render", f"{sid}: vídeos feitos por OUTRA versão do story_cf.py (re-renderize)"))
    if r:
        return situ, det, p + r                # render velho: o texto desenhado dele não é o de hoje
    if meta.get("hash_render") != hash_render(st):
        r.append(("render", f"{sid}: parâmetros de render (trecho/crop/câmera/tempos) do stories_cf.json ≠ os do "
                            "render (correção visual sem re-render): re-renderize"))
    fontes = meta.get("fontes")
    if not (isinstance(fontes, dict) and all(str(fontes.get(k) or "").startswith(FONTE_DO_CI) for k in PAPEIS_FONTE)):
        r.append(("render", f"{sid}: render com fontes {fontes} — o molde se aprova pelo render do CI ({FONTE_DO_CI}*): "
                            "rode o render-stories.yml"))
    reel = (reels_por_id or {}).get(st["reel_ref"])
    if reel is None:
        r.append(("render", f"{sid}: reel_ref {st['reel_ref']} não está no reels.json"))
    elif reel.get("video") != meta.get("reel_video"):
        r.append(("render", f"{sid}: ilustração tirada de outro vídeo ({meta.get('reel_video')} ≠ {reel.get('video')})"))
    elif not os.path.exists(os.path.join(ROOT, reel["video"])):
        r.append(("render", f"{sid}: mp4 do reel {reel['video']} ausente: não dá para conferir de onde saiu a ilustração"))
    elif sha256_arquivo(os.path.join(ROOT, reel["video"])) != meta.get("reel_sha256"):
        r.append(("render", f"{sid}: o mp4 do reel mudou depois do render da story (re-renderize)"))
    partes = meta.get("partes") or []
    if len(partes) != len(PAPEIS):
        return situ, det, p + r + [("render", f"{sid}: irmão com {len(partes)} partes, esperado {len(PAPEIS)}")]
    for i, (tela, parte) in enumerate(zip(st["telas"], partes)):
        nome = f"{sid}/{tela['papel']}"
        esperado = arquivo_da_parte(sid, i)
        arq = os.path.join(ROOT, esperado)
        if parte.get("arquivo") != esperado or not os.path.exists(arq):
            r.append(("render", f"{nome}: vídeo ausente ou fora do lugar ({parte.get('arquivo')!r}; esperado {esperado!r})"))
            continue
        if sha256_arquivo(arq) != parte.get("sha256"):
            r.append(("render", f"{nome}: vídeo diferente do registrado no irmão"))
        dur = parte.get("dur") if isinstance(parte.get("dur"), (int, float)) else 0
        if not (DUR_MIN <= dur <= DUR_MAX):
            r.append(("render", f"{nome}: duração {parte.get('dur')}s fora de {DUR_MIN}-{DUR_MAX}s"))
        if parte.get("trecho") != tela.get("trecho") or parte.get("crop") != tela.get("crop") \
                or parte.get("camera") != camera_de(tela):
            r.append(("render", f"{nome}: trecho/crop/câmera do irmão ≠ os do stories_cf.json (re-renderize)"))
        p += [(t, f"{sid}/{m}") for t, m in problemas_de_desenho(tela, parte.get("textos_tela") or [], st.get("cta", ""))]
    return situ, det, p + r


def veredito(st, aprovacoes, reels_por_id=None, exigir_render=False):
    """A régua ÚNICA (CI e publish). Ver o topo do módulo."""
    situ, det, probs = _avaliar(st, aprovacoes, reels_por_id)
    if situ == "aprovada":
        erros, avisos = list(probs), []
    else:
        aviso_t = ("aprovacao",) if exigir_render else ("aprovacao", "render")
        erros = [x for x in probs if x[0] not in aviso_t]
        avisos = [x for x in probs if x[0] in aviso_t]
    return {"id": st.get("id"), "situacao": situ, "detalhe": det, "problemas": probs, "erros": erros,
            "avisos": avisos, "pode_sair": situ == "aprovada" and not erros}


def problemas_de_publicacao(st, aprovacoes, reels_por_id=None, exigir_aprovacao=True):
    """Compatibilidade: [str]. Com exigir_aprovacao: a mensagem 'aprovação pendente' (se não aprovada)
    + os ERROS do veredito — render velho de story pendente é aviso e não aparece aqui; formato e
    conteúdo aparecem sempre. Lista vazia = pode sair."""
    v = veredito(st, aprovacoes, reels_por_id)
    if not exigir_aprovacao:
        return [m for t, m in v["problemas"] if t != "aprovacao"]
    return [m for t, m in v["avisos"] if t == "aprovacao"] + [m for _, m in v["erros"]]


def data_do_reel(reel_id, publicados):
    """Data BRT em que o reel saiu NO GRID (a 1ª), ou None. Reel em modo trial (só não-seguidores,
    fora do grid) não conta: a tela 3 diria 'Vídeo completo no perfil' sem o vídeo no perfil."""
    datas = []
    for e in publicados:
        if e.get("id") == reel_id and e.get("kind") == "reel" and e.get("modo_reel") in MODOS_REEL_NO_GRID:
            try:
                datas.append(dt.datetime.fromisoformat(e["at"]).astimezone(BRT).date())
            except (KeyError, ValueError, TypeError):
                continue
    return min(datas) if datas else None


def no_calendario(st, publicados, hoje_brt):
    d = data_do_reel(st.get("reel_ref"), publicados)
    return d is not None and (hoje_brt - d).days >= DIAS_DEPOIS_DO_REEL


def partes_publicadas(publicados):
    """{story_id: {indice_da_parte: media_id}} a partir do estado."""
    out = {}
    for e in publicados:
        if e.get("kind") == "story_nova":
            out.setdefault(e.get("story"), {})[int(e.get("parte", -1))] = e.get("media_id")
    return out


def incertas(publicados):
    return sorted({e.get("story") for e in publicados if e.get("kind") == "story_nova_incerta"})


def retomada(fila, publicados, hoje_brt):
    """(st, situação, detalhe) da story com 1-2 partes no ar. Ver o topo do módulo."""
    feitas = partes_publicadas(publicados)
    for st in fila:
        sid = st.get("id")
        k = len(feitas.get(sid, {}))
        if not 0 < k < len(PAPEIS):
            continue
        regs = [e for e in publicados if e.get("story") == sid and e.get("kind") in ("story_nova", "story_nova_incerta")]
        try:
            d1 = min(dt.datetime.fromisoformat(e["at"]).astimezone(BRT).date() for e in regs)
        except (KeyError, ValueError, TypeError):
            d1 = None
        decidir = (f"decida: abandonar (tire {sid} do stories_cf.json) ou republicar inteira num próximo dia de "
                   f"story (apague as partes {sid}#* do state/published.json)")
        if d1 != hoje_brt:
            quando = f"{d1:%d/%m}" if d1 else "data ilegível"
            return st, "incompleta_expirada", (f"story {sid} com {k}/{len(PAPEIS)} parte(s) no ar desde {quando}: no "
                                               f"Instagram a parte 1 já expirou (24 h) — completar agora publicaria "
                                               f"o meio da story sem o começo; {decidir}")
        meta = carregar(irmao_de(st), {})
        atuais = [pt.get("sha256") for pt in meta.get("partes") or []]
        mudou = [e.get("parte") for e in regs if e.get("sha256") and
                 (not isinstance(e.get("parte"), int) or e["parte"] >= len(atuais) or e["sha256"] != atuais[e["parte"]])]
        if mudou:
            return st, "incompleta_expirada", (f"story {sid}: o render mudou depois das partes {mudou} saírem (sha256 do "
                                               f"registro ≠ irmão) — completar misturaria dois renders; {decidir}")
        return st, "retomada", f"{k}/{len(PAPEIS)} parte(s) no ar desde hoje"
    return None, None, None


def candidatas(fila, publicados, aprovacoes, hoje_brt, reels_por_id=None, detalhar=True):
    """(cands, fora). Ver o topo do módulo. `detalhar=False` (agenda, dia a dia) não roda o veredito
    das não aprovadas: `fora` traz só o aviso de aprovação."""
    feitas = partes_publicadas(publicados)
    com_parte = feitas.keys() | set(incertas(publicados))
    cands, fora = [], []
    for st in fila:
        if st.get("id") in com_parte or not no_calendario(st, publicados, hoje_brt):
            continue
        situ, det = aprovacao_de(st, aprovacoes)
        if situ == "aprovada":
            cands.append(st)
            continue
        fora.append((st.get("id"), "aviso", f"{st.get('id')}: aguardando aprovação do Rafael ({situ}: {det}) — "
                                           "fora da escolha de hoje"))
        if detalhar:
            v = veredito(st, aprovacoes, reels_por_id)
            fora += [(st.get("id"), "aviso", m) for t, m in v["avisos"] if t != "aprovacao"]
            fora += [(st.get("id"), "erro", m) for _, m in v["erros"]]
    return cands, fora


def escolher(cands, publicados, hoje_brt, futuras=None, n=None, fila=None):
    """Entre as candidatas (já no calendário), as liberadas pela DISTÂNCIA ENTRE TEMAS (Rafael, 24/10:
    nada sobre tema que saiu ou vai sair em menos de n dias, em qualquer superfície) e, delas, a do
    tema que apareceu há MAIS tempo. `futuras` = {tema: [datas]} já agendadas (reels da fila).
    -> (story, motivo) e, sem story, (None, 'bloqueios: ...') para o log."""
    import regra_reels
    import temas_conteudo as T
    n = regra_reels.dias_entre_mesmo_tema() if n is None else n
    if not cands:
        return None, "nenhuma story aprovada com o reel de origem no grid há 2+ dias"
    if n < 0:
        return cands[0], "sem distância de tema"
    extra = {s.get("id"): s.get("tema") for s in (fila if fila is not None else cands) if s.get("tema")}
    passadas = T.aparicoes(publicados, BRT, extra)
    st, bloq = T.escolher(cands, hoje_brt, passadas, futuras or {}, n, extra)
    if st is None:
        return None, "bloqueios: " + "; ".join(f"{i}: {m}" for i, m in bloq)
    return st, "tema mais antigo"


def proxima_story(fila, publicados, hoje_brt, futuras=None, n=None, aprovacoes=None):
    """Compatibilidade: retomada do MESMO dia vem primeiro (incompleta de outro dia LEVANTA
    RuntimeError: falha ALTO, nunca completar uma story expirada). Senão, escolher() entre as
    stories sem parte e no calendário — e, com `aprovacoes`, só entre as aprovadas (candidatas)."""
    st, situ, det = retomada(fila, publicados, hoje_brt)
    if situ == "incompleta_expirada":
        raise RuntimeError(det)
    if situ == "retomada":
        return st, "retomada"
    if aprovacoes is not None:
        cands = candidatas(fila, publicados, aprovacoes, hoje_brt)[0]
    else:
        feitas = partes_publicadas(publicados)
        cands = [s for s in fila if not feitas.get(s.get("id")) and no_calendario(s, publicados, hoje_brt)]
    return escolher(cands, publicados, hoje_brt, futuras=futuras, n=n, fila=fila)


def entrada_de_aprovacao(sid):
    """A entrada que o lote do Rafael registra para a story (o que ele viu, byte a byte), ou
    (None, erros) se o render não está coerente com o texto atual (não se aprova render velho)."""
    fila = carregar(FILA, [])
    st = next((s for s in fila if isinstance(s, dict) and s.get("id") == sid), None)
    if st is None:
        return None, [f"{sid}: não está em {os.path.basename(FILA)}"]
    reels = {r["id"]: r for r in carregar(os.path.join(ROOT, "reels.json"), [])}
    v = veredito(st, {"lotes": []}, reels, exigir_render=True)
    if v["erros"]:
        return None, [m for _, m in v["erros"]]
    meta = carregar(irmao_de(st), {})
    return {"id": sid, "hash_roteiro": hash_story(st), "videos": [pt.get("sha256") for pt in meta["partes"]],
            "hash_gerador": meta.get("hash_gerador")}, []


def entrada_hipotetica(st):
    """SÓ para a página (publish_agenda: 'se aprovada hoje'), NUNCA para um lote de verdade: a entrada que
    amarraria o render que está no irmão AGORA (ou marcas 'sem-render' se não há irmão bem formado — aí o
    veredito barra pelo render, como numa aprovação real)."""
    meta = carregar(irmao_de(st), {}) if isinstance(st.get("id"), str) else {}
    hg = meta.get("hash_gerador")
    return {"id": st.get("id"), "hash_roteiro": hash_story(st),
            "videos": shas_do_irmao(meta) or ["sem-render"] * len(PAPEIS),
            "hash_gerador": hg if isinstance(hg, str) and hg else "sem-render"}


def _ids_de(lista):
    out = []
    for x in lista or []:
        out += [i for i in re.split(r"[,\s]+", x) if i]
    return out


def main(argv=None):
    import argparse
    ap = argparse.ArgumentParser(description="Portão dos stories da geração nova (regra única do CI e do publish).")
    ap.add_argument("--autoteste", action="store_true", help="controles positivos e negativos de cada guarda")
    ap.add_argument("--ids", nargs="+", metavar="ID", help="confere só esses ids (espaço ou vírgula)")
    ap.add_argument("--exigir-render", action="store_true", help="render é erro mesmo em story pendente (render-stories.yml)")
    ap.add_argument("--entrada", metavar="ID", help="imprime a entrada pronta para o lote do aprovacoes.json")
    a = ap.parse_args(argv)
    if a.autoteste:
        return _autoteste()
    if a.entrada:
        ent, erros = entrada_de_aprovacao(a.entrada)
        if ent is None:
            for x in erros:
                print(f"::error::{x}")
            print("Entrada NÃO gerada: o render não está coerente com o texto atual (re-renderize no CI).")
            return 1
        print(json.dumps(ent, ensure_ascii=False, indent=1))
        print(f"(vai em 'episodios' de um lote com \"escopo\": [\"{ESCOPO}\"], \"status\": \"aprovado\" e \"aprovado_por\" + "
              "\"evidencia\" não vazios — entrada sem 'videos'/'hash_gerador' ou lote sem autor/evidência NÃO aprova)",
              file=sys.stderr)
        return 0
    fila = carregar(FILA, None)
    if not isinstance(fila, list):
        print(f"::error::{FILA} ausente ou não é uma lista")
        return 1
    aprov = carregar(APROVACOES, {"lotes": []})
    reels = {r["id"]: r for r in carregar(os.path.join(ROOT, "reels.json"), [])}
    publicados = carregar(os.path.join(ROOT, "state", "published.json"), {}).get("published", [])
    feitas = partes_publicadas(publicados)
    erros = 0
    ids = [s.get("id") for s in fila if isinstance(s, dict)]
    dup = sorted({i for i in ids if ids.count(i) > 1})
    if dup or len(ids) != len(fila):
        print(f"::error::fila com id repetido ou item que não é objeto: {dup}")
        erros += 1
    pedidos = _ids_de(a.ids)
    if a.ids is not None:
        falta = [i for i in pedidos if i not in ids]
        if falta or not pedidos:
            print(f"::error::--ids {falta or '(vazio)'} não estão em {os.path.basename(FILA)}")
            return 1
        alvo = [s for s in fila if isinstance(s, dict) and s.get("id") in pedidos]
    else:
        alvo = [s for s in fila if isinstance(s, dict) and len(feitas.get(s.get("id"), {})) != len(PAPEIS)]
    for st in alvo:
        v = veredito(st, aprov, reels, exigir_render=a.exigir_render)
        for _, m in v["avisos"]:
            print(f"::warning::{m}")
        if v["erros"]:
            erros += 1
            for _, m in v["erros"]:
                print(f"::error::{m}")
        else:
            print(f"OK {st['id']} (aprovação: {v['situacao']})")
        if v["situacao"] != "aprovada":
            print(f"::warning::{st['id']}: aguardando aprovação do Rafael — não sai até lá.")
    for sid in incertas(publicados):
        print(f"::warning::story {sid} com parte INCERTA no estado: o publish não publica story nenhuma até a conferência.")
    print(f"{len(alvo)} story(ies) conferida(s) de {len(fila)} na fila; {erros} com problema.")
    return 1 if erros else 0


# ------------------------------------------------------------------ autoteste
def _autoteste():
    """Controle por guarda: a BASE passa e cada mutação reprova com o TIPO certo."""
    import shutil
    import tempfile
    falhas = []

    def checa(nome, ok):
        print(("OK   " if ok else "FALHA"), nome)
        if not ok:
            falhas.append(nome)

    def j(x):
        return json.loads(json.dumps(x))

    cr = [40, 205, 960, 1069]
    base = {"id": "st_x", "reel_ref": "cf_alongamento", "tema": "tempo_tratamento", "angulo": "a", "variante": "A",
            "cta": "Manda pra quem acha devagar.",
            "telas": [{"papel": "espanto", "titulo": ["OSSO CRESCE", "DE NOVO?"], "texto": "", "trecho": [1.0, 3.0], "crop": cr,
                       "dur": 4.5, "t_toca": 2.6},
                      {"papel": "mecanismo", "titulo": ["UM MILÍMETRO", "POR DIA"], "texto": "O corpo preenche o espaço.",
                       "trecho": [9.0, 11.0], "crop": cr, "zoom": [[0.0, 1.0], [6.0, 1.1]], "dur": 6.0},
                      {"papel": "significado", "titulo": ["DEVAGAR", "DE PROPÓSITO"], "texto": "Pele, nervo e vaso esticam junto.",
                       "trecho": [20.0, 22.0], "crop": cr, "dur": 8.0}]}

    def tipos(ps):
        return {t for t, _ in ps}

    # ---------------- formato / texto
    checa("formato válido passa", problemas_do_texto(base) == [])
    for nome, mexe, tipo, trecho in [
        ("id sem prefixo", lambda s: s.update(id="x_1"), "formato", "id tem de"),
        ("id com caractere fora de [a-z0-9_]", lambda s: s.update(id="stn_a b*"), "formato", "id tem de"),
        ("sem reel_ref", lambda s: s.update(reel_ref=""), "formato", "reel_ref"),
        ("2 telas", lambda s: s["telas"].pop(), "formato", "exatamente"),
        ("título de 1 linha", lambda s: s["telas"][0].update(titulo=["SÓ UMA"]), "formato", "2 linhas"),
        ("título com 28 caracteres", lambda s: s["telas"][0].update(titulo=["UMA LINHA GRANDE DEMAIS AQUI", "X"]), "formato", "caracteres"),
        ("texto longo demais", lambda s: s["telas"][1].update(texto="palavra " * 20), "formato", "texto com"),
        ("texto vazio na tela 2", lambda s: s["telas"][1].update(texto=""), "formato", "texto vazio"),
        ("trecho longo demais", lambda s: s["telas"][1].update(trecho=[9.0, 30.0]), "formato", "trecho"),
        ("crop fora do quadro", lambda s: s["telas"][1].update(crop=[100, 0, 1080, 1920]), "formato", "crop"),
        ("chamada que não é de envio", lambda s: s.update(cta="Comenta aqui embaixo"), "formato", "cta"),
        ("chamada de envio fora da série ('Envia pra quem')", lambda s: s.update(cta="Envia pra quem precisa."), "formato", "cta"),
        ("chamada longa demais", lambda s: s.update(cta="Manda pra quem " + "precisa muito " * 5), "formato", "cta"),
        ("chamada de agendamento (legenda.cta_de_envio)", lambda s: s.update(cta="Manda pra quem quer agendar consulta."), "formato", "cta"),
        ("variante inválida", lambda s: s.update(variante="C"), "formato", "variante"),
        ("tema com hífen (inválido)", lambda s: s.update(tema="tempo-tratamento"), "formato", "tema"),
        ("reel de origem sem tema", lambda s: (s.update(reel_ref="cf_zz_novo"), s.pop("tema")), "formato", "tema"),
        ("chamada 'me escreve no privado' (DM)", lambda s: s.update(cta="Manda pra quem quiser: me escreve no privado."), "conteudo", "DM"),
        ("DM no texto da tela 3", lambda s: s["telas"][2].update(texto="Dúvidas sobre o seu caso? Me chama no direct."), "conteudo", "DM"),
        ("WhatsApp no título", lambda s: s["telas"][1].update(titulo=["CHAMA NO", "WHATSAPP"]), "conteudo", "DM"),
        ("promessa (CFM)", lambda s: s["telas"][1].update(texto="Resultado garantido: cura em 30 dias."), "conteudo", "CFM"),
    ]:
        s = j(base); mexe(s); ps = problemas_do_texto(s)
        checa(f"CONTROLE: {nome} reprova ({tipo})", any(t == tipo and trecho in m for t, m in ps))
    for cta in ("Manda pra quem precisa e me chama no direct.", "Manda pra quem precisa. WhatsApp na bio.",
                "Manda um direct pra agendar sua avaliação.", "Manda mensagem que eu te respondo."):
        s = j(base); s["cta"] = cta
        checa(f"CONTROLE: chamada de contato {cta!r} reprova", bool(problemas_do_texto(s)))
    # verificação de 25/10: a família contato/agendamento e a lista negra de texto em imagem do carrossel
    for onde, val, trecho in [
        ("cta", "Manda pra quem precisa entrar em contato.", "DM/contato"),
        ("cta", "Manda pra quem quer marcar uma avaliação.", "DM/contato"),
        ("texto", "Entre em contato pelo site.", "DM/contato"),
        ("texto", "Marque uma avaliação com ortopedista.", "DM/contato"),
        ("texto", "Fale com a nossa equipe.", "DM/contato"),
        ("titulo", ["DESLIZE PRA", "VER O FIM"], "lista do carrossel"),
        ("texto", "Arraste para o lado e veja.", "lista do carrossel"),
        ("texto", "Salve este story para lembrar.", "lista do carrossel"),
        ("texto", "Veja o antes e depois da cirurgia.", "lista do carrossel"),
        ("texto", "Isso cura em 3 meses!", "lista do carrossel"),
        ("texto", "Corrige a altura da criança.", "lista do carrossel"),
        ("texto", "Resultado estético perfeito.", "lista do carrossel"),
        ("titulo", ["SEU FILHO TEM", "PÉ TORTO?"], "lista do carrossel"),
        ("cta", "Manda pra quem precisa! Corre!", "lista do carrossel"),
    ]:
        s = j(base)
        if onde == "cta":
            s["cta"] = val
        else:
            s["telas"][2 if onde == "texto" else 1][onde] = val
        checa(f"CONTROLE: {onde} {val!r} reprova (conteudo: {trecho})",
              any(t == "conteudo" and trecho in m for t, m in problemas_do_texto(s)))
    s = j(base); s["telas"][2]["texto"] = "Assimetria, dor, quedas demais ou piora pedem avaliação."
    checa("o texto real 'piora pedem avaliação' (sinal de alerta, sem marcar consulta) passa", problemas_do_texto(s) == [])
    legenda_real = sys.modules.pop("legenda", None)
    sys.modules["legenda"] = None                       # import legenda -> ImportError
    try:
        checa("CONTROLE: sem legenda.py a chamada fica SEM aval (falha fechada)",
              any("legenda.py ausente" in m for _, m in problemas_do_texto(base)))
    finally:
        del sys.modules["legenda"]
        if legenda_real is not None:
            sys.modules["legenda"] = legenda_real
    checa("compatibilidade: problemas_de_formato devolve str e pega o DM",
          all(isinstance(x, str) for x in problemas_de_formato(dict(j(base), cta="Manda pra quem precisa. WhatsApp na bio.")))
          and problemas_de_formato(dict(j(base), cta="Manda pra quem precisa. WhatsApp na bio.")) != [])

    # ---------------- texto desenhado (mesmo cheque do story_cf.py)
    t2, t3 = base["telas"][1], base["telas"][2]
    d2 = ["UM MILÍMETRO", "POR DIA", "O corpo preenche", "o espaço.", SIG, DISC_ST, SELO, TOCA]
    d3 = ["DEVAGAR", "DE PROPÓSITO", "Pele, nervo e vaso esticam junto.", SIG, DISC_ST, SELO, PERFIL, NOME,
          "MANDA PRA QUEM", "ACHA DEVAGAR."]
    checa("desenho completo passa (linha quebrada e chamada em 2 linhas)",
          problemas_de_desenho(t2, d2) == [] and problemas_de_desenho(t3, d3, base["cta"]) == [])
    for nome, tela, des, trecho in [
        ("texto que não é da story", t2, d2 + ["CURA GARANTIDA"], "fora da story"),
        ("chamada fora da tela 3", t2, d2 + ["MANDA PRA QUEM"], "fora da story"),
        ("tela sem a identificação", t2, [x for x in d2 if x != SIG], "identificação"),
        ("tela 3 sem 'Vídeo completo no perfil'", t3, [x for x in d3 if x != PERFIL], PERFIL),
        ("linha do título não desenhada", t2, [x for x in d2 if x != "POR DIA"], "título NÃO desenhada"),
        ("texto truncado (cobertura)", t2, [x for x in d2 if x != "o espaço."], "texto da tela"),
        ("chamada truncada (cobertura)", t3, [x for x in d3 if x != "ACHA DEVAGAR."], "chamada"),
    ]:
        ps = problemas_de_desenho(tela, des, base["cta"])
        checa(f"CONTROLE: {nome} reprova (conteudo)", any(t == "conteudo" and trecho in m for t, m in ps))

    # ---------------- hashes
    h = hash_story(base); b2 = j(base); b2["telas"][1]["trecho"] = [3.0, 5.0]
    checa("hash da aprovação ignora a escolha da ilustração", hash_story(b2) == h)
    checa("CONTROLE: hash_render muda com o trecho/crop/câmera/tempos", hash_render(b2) != hash_render(base)
          and hash_render(dict(j(base), telas=[dict(t, t_toca=9.9) for t in j(base)["telas"]])) != hash_render(base))
    b2["telas"][1]["texto"] = "O corpo preenche o espaço com osso."
    checa("CONTROLE: hash muda quando o texto muda", hash_story(b2) != h)

    # ---------------- raiz temporária: irmão, vídeos, aprovação, veredito, main()
    tmp = tempfile.mkdtemp(prefix="stchk_")
    raiz_velha = usar_raiz(tmp)
    try:
        open(GERADOR, "w", encoding="utf-8").write("# gerador\n")
        os.makedirs(os.path.join(tmp, PASTA)); os.makedirs(os.path.join(tmp, "reels")); os.makedirs(os.path.join(tmp, "state"))
        open(os.path.join(tmp, "reels", "x.mp4"), "wb").write(b"reel")
        reels = {"cf_alongamento": {"id": "cf_alongamento", "video": "reels/x.mp4"}}
        json.dump(list(reels.values()), open(os.path.join(tmp, "reels.json"), "w", encoding="utf-8"))
        fontes_ci = {"black": "Roboto-Black.ttf", "bold": "Roboto-Bold.ttf", "semi": "Roboto-Medium.ttf", "reg": "Roboto-Regular.ttf"}

        def renderizar(st, bytes_extra=b""):
            """O que o story_cf.py grava (sem desenhar): 3 mp4 + irmão coerentes com `st`."""
            partes = []
            for i, t in enumerate(st["telas"]):
                arq = arquivo_da_parte(st["id"], i)
                open(os.path.join(tmp, arq), "wb").write(b"v%d" % i + bytes_extra)
                des = list(t["titulo"]) + ([t["texto"]] if t["texto"] else []) + [SIG, DISC_ST, SELO] + \
                    ([PERFIL, NOME, st["cta"].upper()] if i == 2 else [TOCA])
                partes.append({"arquivo": arq, "sha256": sha256_arquivo(os.path.join(tmp, arq)), "dur": t.get("dur", 6.0),
                               "textos_tela": des, "trecho": t["trecho"], "crop": t["crop"], "camera": camera_de(t)})
            meta = {"id": st["id"], "hash_story": hash_story(st), "hash_gerador": hash_gerador(), "hash_render": hash_render(st),
                    "reel_video": "reels/x.mp4", "reel_sha256": sha256_arquivo(os.path.join(tmp, "reels", "x.mp4")),
                    "partes": partes, "fontes": dict(fontes_ci)}
            gravar_meta(st["id"], meta)
            return meta

        def gravar_meta(sid, meta):
            json.dump(meta, open(os.path.join(tmp, PASTA, f"{sid}.json"), "w", encoding="utf-8"), ensure_ascii=False)

        aval = {"aprovado_por": "Rafael (autoteste)", "evidencia": "autoteste: aprovação simulada"}

        def lote(eps, status="aprovado", escopo=(ESCOPO,), com_aval=True, nome="L"):
            lt = {"lote": nome, "escopo": list(escopo), "status": status, "episodios": eps}
            if com_aval:
                lt.update(aval)
            return {"lotes": [lt]}
        meta0 = renderizar(base)
        # a entrada que aprova é a de --entrada: hash do texto + sha256 dos 3 vídeos + hash do gerador
        ent = {"id": "st_x", "hash_roteiro": h, "videos": [pt["sha256"] for pt in meta0["partes"]], "hash_gerador": meta0["hash_gerador"]}
        so_texto = {"id": "st_x", "hash_roteiro": h}
        apr = lote([ent])
        v = veredito(base, apr, reels)
        checa("BASE: story completa e aprovada pode sair (sem problema nenhum)", v["pode_sair"] and v["problemas"] == [])
        checa("compatibilidade: problemas_de_publicacao vazio na base", problemas_de_publicacao(base, apr, reels) == [])

        # aprovação
        checa("aprovação com vídeos e gerador amarrados", aprovacao_de(base, lote([ent])) == ("aprovada", "L (vídeos amarrados)"))
        for nome, ap_, esperado in [
            ("sem lote = pendente", {"lotes": []}, "pendente"),
            ("lote de outro escopo não aprova story", lote([ent], escopo=("instagram",)), "pendente"),
            ("escopo que não é lista não aprova", {"lotes": [dict(aval, lote="L", escopo=ESCOPO, status="aprovado", episodios=[ent])]},
             "pendente"),
            ("lote com status 'pendente' e entrada certa = pendente (não divergente)", lote([ent], status="pendente"), "pendente"),
            ("lote 'substituido' com entrada certa = pendente", lote([ent], status="substituido"), "pendente"),
            ("texto mudou depois da aprovação = divergente", lote([dict(ent, hash_roteiro="sha256:outro")]), "divergente"),
            ("vídeos diferentes dos aprovados = divergente", lote([dict(ent, videos=["sha256:a", "sha256:b", "sha256:c"])]), "divergente"),
            ("gerador diferente do aprovado = divergente", lote([dict(ent, hash_gerador="sha256:velho")]), "divergente"),
            ("'videos' malformado = pendente", lote([dict(ent, videos=["sha256:a"])]), "pendente"),
            # auditoria de fechamento (25/10): o amarrar dos vídeos era OPCIONAL — entrada só de texto aprovava
            ("entrada só do texto (sem 'videos'/'hash_gerador') = pendente", lote([so_texto]), "pendente"),
            ("entrada com 'videos' e sem 'hash_gerador' = pendente", lote([{k: x for k, x in ent.items() if k != "hash_gerador"}]), "pendente"),
            ("entrada com 'hash_gerador' e sem 'videos' = pendente", lote([{k: x for k, x in ent.items() if k != "videos"}]), "pendente"),
            # lote válido = o do checar_aprovacoes (portão clínico do publish.yml) e do checar_carrossel
            ("lote 'aprovado' sem aprovado_por = pendente", {"lotes": [dict(lote([ent])["lotes"][0], aprovado_por=" ")]}, "pendente"),
            ("lote 'aprovado' sem evidencia = pendente", {"lotes": [{k: x for k, x in lote([ent])["lotes"][0].items() if k != "evidencia"}]},
             "pendente"),
            ("lote sem aval nenhum = pendente", lote([ent], com_aval=False), "pendente"),
            ("registro MINUTA_AGUARDA_AVAL = pendente", dict(lote([ent]), MINUTA_AGUARDA_AVAL=True), "pendente"),
        ]:
            checa(f"CONTROLE: {nome}", aprovacao_de(base, ap_)[0] == esperado)
        checa("CONTROLE: o motivo da entrada só de texto manda gerar com --entrada",
              "--entrada st_x" in aprovacao_de(base, lote([so_texto]))[1])
        checa("CONTROLE: re-render depois da aprovação com vídeos amarrados = divergente",
              (renderizar(base, b"re-render"), aprovacao_de(base, lote([ent]))[0])[1] == "divergente")
        # o ataque do verificador: lote só de texto + re-render COERENTE (irmão, hash_render e Roboto em dia)
        renderizar(base, b"re-render coerente")
        r = veredito(base, lote([so_texto]), reels)
        checa("CONTROLE: lote só de texto + re-render coerente = pendente e NÃO sai (vídeo que o Rafael não viu)",
              r["situacao"] == "pendente" and not r["pode_sair"] and [t for t, _ in r["problemas"]] == ["aprovacao"])
        dois = [lote([so_texto], nome="L1")["lotes"][0], lote([ent], nome="L2")["lotes"][0]]
        checa("CONTROLE: lote só de texto NÃO anula o amarrar de outro lote (re-render = divergente nas duas ordens)",
              aprovacao_de(base, {"lotes": dois})[0] == "divergente" and aprovacao_de(base, {"lotes": dois[::-1]})[0] == "divergente")
        renderizar(base)
        checa("dois lotes (só texto + amarrado) com o render visto = aprovada pelo amarrado",
              aprovacao_de(base, {"lotes": dois}) == ("aprovada", "L2 (vídeos amarrados)"))

        def mexido(mexe_meta=None, mexe_arq=None, st=None, ap_=None, reels_=None, desfaz=None):
            m = carregar(irmao_de(base), {})
            if mexe_meta:
                mexe_meta(m); gravar_meta("st_x", m)
            if mexe_arq:
                mexe_arq()
            r = veredito(st or base, ap_ or apr, reels if reels_ is None else reels_)
            if desfaz:
                desfaz()
            open(os.path.join(tmp, "reels", "x.mp4"), "wb").write(b"reel")
            renderizar(base)                                  # volta à base
            return r

        def tem(r, tipo, trecho):
            return any(t == tipo and trecho in m for t, m in r["problemas"])
        for nome, kw, tipo, trecho in [
            ("sem irmão", dict(mexe_arq=lambda: os.remove(irmao_de(base))), "render", "sem arquivo-irmão"),
            ("irmão de OUTRO texto", dict(mexe_meta=lambda m: m.update(hash_story="sha256:velho")), "render", "OUTRO texto"),
            # o story_cf.py mudou depois do render aprovado (o irmão segue com o gerador que o Rafael viu: a
            # aprovação vale e o RENDER barra — re-renderizar e re-aprovar)
            ("irmão de outro gerador (story_cf.py mudou)",
             dict(mexe_arq=lambda: open(GERADOR, "w", encoding="utf-8").write("# gerador NOVO\n"),
                  desfaz=lambda: open(GERADOR, "w", encoding="utf-8").write("# gerador\n")), "render", "OUTRA versão"),
            ("parâmetro de render mudou no JSON sem re-render",
             dict(st=dict(j(base), telas=[j(base)["telas"][0], dict(j(base)["telas"][1], crop=[0, 0, 1080, 1920]), j(base)["telas"][2]])),
             "render", "parâmetros de render"),
            ("crop do irmão ≠ JSON (irmão editado)", dict(mexe_meta=lambda m: m["partes"][1].update(crop=[0, 0, 1080, 1920])), "render", "trecho/crop/câmera"),
            ("render com fonte do PC (Segoe)", dict(mexe_meta=lambda m: m.update(fontes=dict(fontes_ci, black="seguibl.ttf"))), "render", "fontes"),
            ("render sem registro de fonte", dict(mexe_meta=lambda m: m.pop("fontes")), "render", "fontes"),
            ("reel_ref fora do reels.json", dict(reels_={}), "render", "não está no reels.json"),
            ("ilustração de outro reel", dict(mexe_meta=lambda m: m.update(reel_video="reels/outro.mp4")), "render", "outro vídeo"),
            ("mp4 do reel trocado", dict(mexe_arq=lambda: open(os.path.join(tmp, "reels", "x.mp4"), "wb").write(b"outro reel")),
             "render", "mp4 do reel mudou"),
            ("mp4 do reel ausente", dict(mexe_arq=lambda: os.remove(os.path.join(tmp, "reels", "x.mp4"))), "render", "ausente"),
            ("irmão com 2 partes", dict(mexe_meta=lambda m: m["partes"].pop()), "render", "2 partes"),
            ("vídeo fora de stories_cf/ ('../x.mp4')", dict(mexe_meta=lambda m: m["partes"][0].update(arquivo="stories_cf/../reels/x.mp4")),
             "render", "fora do lugar"),
            ("vídeo ausente", dict(mexe_arq=lambda: os.remove(os.path.join(tmp, arquivo_da_parte("st_x", 1)))), "render", "ausente"),
            ("vídeo trocado depois do render", dict(mexe_arq=lambda: open(os.path.join(tmp, arquivo_da_parte("st_x", 1)), "wb").write(b"trocado")),
             "render", "diferente do registrado"),
            ("duração 2,0 s", dict(mexe_meta=lambda m: m["partes"][0].update(dur=2.0)), "render", "duração"),
            ("duração 61 s", dict(mexe_meta=lambda m: m["partes"][0].update(dur=61.0)), "render", "duração"),
            ("texto estranho desenhado", dict(mexe_meta=lambda m: m["partes"][1]["textos_tela"].append("CURA GARANTIDA")), "conteudo", "fora da story"),
            ("tela sem a identificação", dict(mexe_meta=lambda m: m["partes"][1]["textos_tela"].remove(SIG)), "conteudo", "identificação"),
            ("tela 3 sem PERFIL", dict(mexe_meta=lambda m: m["partes"][2]["textos_tela"].remove(PERFIL)), "conteudo", PERFIL),
            ("irmão sem a chamada inteira", dict(mexe_meta=lambda m: m["partes"][2]["textos_tela"].remove(base["cta"].upper())), "conteudo", "chamada"),
        ]:
            r = mexido(**kw)
            checa(f"CONTROLE: {nome} reprova ({tipo}) e a aprovada NÃO sai", tem(r, tipo, trecho) and not r["pode_sair"]
                  and any(t == tipo for t, _ in r["erros"]))
        r = mexido(mexe_meta=lambda m: (m.update(hash_story="sha256:velho"), m["partes"][1]["textos_tela"].append("O OSSO AINDA")))
        checa("render velho: só o problema de render (o texto desenhado de outro texto não é conferido)",
              tipos(r["problemas"]) == {"render"})

        # veredito: story pendente
        pend = {"lotes": []}
        r = veredito(base, pend, reels)
        checa("pendente com render em dia: só aviso de aprovação, sem erro, não sai",
              r["erros"] == [] and tipos(r["avisos"]) == {"aprovacao"} and not r["pode_sair"])
        r = mexido(mexe_arq=lambda: os.remove(irmao_de(base)), ap_=pend)
        checa("pendente sem render: aviso (o texto sobe antes do render)", r["erros"] == [] and "render" in tipos(r["avisos"]))
        checa("compatibilidade: pendente sem render = só 'aprovação pendente' (o publish atual avisa, não levanta)",
              (os.remove(irmao_de(base)), problemas_de_publicacao(base, pend, reels))[1] == ["st_x: aprovação pendente (sem lote de aprovação)"])
        renderizar(base)
        r = veredito(dict(j(base), telas=[j(base)["telas"][0], dict(j(base)["telas"][1], titulo=["O OSSO AINDA", "ENDURECE"]),
                                          j(base)["telas"][2]]), pend, reels)
        checa("pendente com texto editado sem re-render: aviso, exit 0 no CI", r["erros"] == [] and "render" in tipos(r["avisos"]))
        r = veredito(dict(j(base), telas=[j(base)["telas"][0], dict(j(base)["telas"][1], texto="Cura garantida em 30 dias."),
                                          j(base)["telas"][2]]), pend, reels)
        checa("CONTROLE: pendente com CFM é ERRO", any(t == "conteudo" for t, _ in r["erros"]))
        r = mexido(mexe_meta=lambda m: m["partes"][1]["textos_tela"].append("veja o vídeo inteiro no link"), ap_=pend)
        checa("CONTROLE: pendente com texto desenhado a mais ('vídeo' na frase) é ERRO", any(t == "conteudo" for t, _ in r["erros"]))
        r = mexido(mexe_meta=lambda m: m.update(fontes={"black": "seguibl.ttf"}), ap_=pend)
        checa("pendente com render do PC: aviso", r["erros"] == [] and "render" in tipos(r["avisos"]))
        r = mexido(mexe_arq=lambda: os.remove(irmao_de(base)), ap_=pend)
        r2 = (os.remove(irmao_de(base)), veredito(base, pend, reels, exigir_render=True))[1]
        renderizar(base)
        checa("CONTROLE: exigir_render (render-stories) faz o render da pendente virar ERRO",
              any(t == "render" for t, _ in r2["erros"]) and r["erros"] == [])

        # calendário, trial, candidatas, retomada
        pub = [{"id": "cf_alongamento", "kind": "reel", "at": "2026-10-21T19:34:00+00:00"}]
        checa("no calendário 2 dias depois do reel", no_calendario(base, pub, dt.date(2026, 10, 23)))
        checa("CONTROLE: 1 dia depois do reel NÃO está no calendário", not no_calendario(base, pub, dt.date(2026, 10, 22)))
        checa("CONTROLE: com distância de tema desligada (n=-1) o reel de ontem continua barrando",
              proxima_story([base], pub, dt.date(2026, 10, 22), n=-1)[0] is None
              and proxima_story([base], pub, dt.date(2026, 10, 23), n=-1)[0] is base)
        pub_trial = [dict(pub[0], modo_reel="trial")]
        checa("CONTROLE: reel em modo TRIAL não conta como 'no perfil'", data_do_reel("cf_alongamento", pub_trial) is None
              and not no_calendario(base, pub_trial, dt.date(2026, 12, 1)))
        checa("reel 'fallback_normal' conta", data_do_reel("cf_alongamento", [dict(pub[0], modo_reel="fallback_normal")]) is not None)
        sa = j(base); sa["id"] = "st_a"; sa["reel_ref"] = "cf_pe_virado"; sa["tema"] = "pe_virado"
        pub_a = pub + [{"id": "cf_pe_virado", "kind": "reel", "at": "2026-09-01T18:00:00+00:00"}]
        cands, fora = candidatas([sa, base], pub_a, apr, dt.date(2026, 11, 20), reels)
        checa("candidatas: a pendente (st_a) sai com aviso e a aprovada fica", cands == [base]
              and any(i == "st_a" and nv == "aviso" and "aguardando aprovação" in m for i, nv, m in fora))
        checa("CONTROLE: sem o filtro, a pendente de tema mais antigo seria a escolhida (fila travada)",
              escolher([sa, base], pub_a, dt.date(2026, 11, 20), n=14, fila=[sa, base])[0] is sa
              and escolher(cands, pub_a, dt.date(2026, 11, 20), n=14, fila=[sa, base])[0] is base)
        checa("proxima_story com aprovações escolhe a aprovada", proxima_story([sa, base], pub_a, dt.date(2026, 11, 20), n=14,
                                                                            aprovacoes=apr)[0] is base)
        sa_cfm = dict(j(sa), telas=[j(sa)["telas"][0], dict(j(sa)["telas"][1], texto="Cura garantida em 30 dias."), j(sa)["telas"][2]])
        checa("CONTROLE: pendente com CFM no calendário volta como ERRO em candidatas",
              any(i == "st_a" and nv == "erro" and "CFM" in m for i, nv, m in candidatas([sa_cfm], pub_a, apr, dt.date(2026, 11, 20), reels)[1]))
        checa("distância de tema: reel de 21/10 libera a story em 04/11 (14 dias)",
              proxima_story([base], pub, dt.date(2026, 11, 4), n=14)[0] is base)
        st0, mot = proxima_story([base], pub, dt.date(2026, 10, 23), n=14)
        checa("CONTROLE: 2 dias depois do reel do mesmo tema NÃO sai", st0 is None and "alongamento" in mot)
        checa("CONTROLE: reel não publicado não vale", proxima_story([base], [], dt.date(2026, 12, 1), n=14)[0] is None)
        sb = dict(j(base), id="st_b", reel_ref="cf_pe_virado", tema="pe_virado")
        pub_b = pub + [{"id": "cf_pe_virado", "kind": "reel", "at": "2026-10-28T19:00:00+00:00"}]
        checa("entre duas liberadas, sai a do tema mais antigo", proxima_story([sb, base], pub_b, dt.date(2026, 11, 20), n=14)[0] is base)
        checa("CONTROLE: tema agendado em menos de 14 dias bloqueia",
              proxima_story([base], pub, dt.date(2026, 11, 10), futuras={"tempo_tratamento": [dt.date(2026, 11, 20)]}, n=14)[0] is None)
        p0 = {"id": "st_x#0", "kind": "story_nova", "story": "st_x", "parte": 0, "media_id": "M1", "at": "2026-11-17T16:00:00+00:00"}
        outra = dict(j(base), id="st_y")
        st_r, situ, _ = retomada([outra, base], pub + [p0], dt.date(2026, 11, 17))
        checa("story incompleta do MESMO dia é retomada antes da próxima", st_r is not None and st_r["id"] == "st_x" and situ == "retomada"
              and proxima_story([outra, base], pub + [p0], dt.date(2026, 11, 17), n=14)[1] == "retomada")
        st_r, situ, det = retomada([outra, base], pub + [p0], dt.date(2026, 11, 19))
        checa("CONTROLE: incompleta de OUTRO dia = 'incompleta_expirada' (não completa)", situ == "incompleta_expirada" and "expirou" in det)
        p0_tarde = dict(p0, at="2026-11-13T02:00:00+00:00")               # qui 12/11 23:00 BRT
        checa("CONTROLE: parte 1 às 23:00 e retomada depois da meia-noite = expirada",
              retomada([base], pub + [p0_tarde], dt.date(2026, 11, 13))[1] == "incompleta_expirada")
        try:
            proxima_story([outra, base], pub + [p0], dt.date(2026, 11, 19), n=14); levantou = False
        except RuntimeError:
            levantou = True
        checa("CONTROLE: proxima_story (compatibilidade) LEVANTA na incompleta expirada", levantou)
        p0_sha = dict(p0, sha256="sha256:render-velho")
        checa("CONTROLE: render trocado depois da parte 1 = expirada (não mistura renders)",
              retomada([base], pub + [p0_sha], dt.date(2026, 11, 17))[1] == "incompleta_expirada"
              and retomada([base], pub + [dict(p0, sha256=carregar(irmao_de(base), {})["partes"][0]["sha256"])],
                           dt.date(2026, 11, 17))[1] == "retomada")
        inc = [{"id": "st_z#1", "kind": "story_nova_incerta", "story": "st_z", "parte": 1}]
        checa("incertas() lista a parte incerta", incertas(pub + inc) == ["st_z"] and incertas(pub) == [])

        # entrada_de_aprovacao
        json.dump([base], open(FILA, "w", encoding="utf-8"), ensure_ascii=False)
        ent2, err = entrada_de_aprovacao("st_x")
        checa("entrada_de_aprovacao: hash do texto + vídeos + gerador; aplicada no lote, aprova",
              ent2 is not None and ent2["videos"] == [pt["sha256"] for pt in carregar(irmao_de(base), {})["partes"]]
              and aprovacao_de(base, lote([ent2]))[0] == "aprovada")
        m = carregar(irmao_de(base), {}); m["hash_story"] = "sha256:velho"; gravar_meta("st_x", m)
        checa("CONTROLE: entrada_de_aprovacao recusa render velho", entrada_de_aprovacao("st_x")[0] is None)
        renderizar(base)

        # main() na raiz temporária (a régua do CI)
        def rodar_main(fila, aprov, argv=(), mexe=None):
            json.dump(fila, open(FILA, "w", encoding="utf-8"), ensure_ascii=False)
            json.dump(aprov, open(APROVACOES, "w", encoding="utf-8"), ensure_ascii=False)
            json.dump({"published": pub_a}, open(os.path.join(tmp, "state", "published.json"), "w", encoding="utf-8"))
            if mexe:
                mexe()
            buf, velho = io.StringIO(), sys.stdout
            sys.stdout = buf
            try:
                rc = main(list(argv))
            finally:
                sys.stdout = velho
            renderizar(base)
            return rc, buf.getvalue()
        quebra_render = lambda: open(os.path.join(tmp, arquivo_da_parte("st_x", 1)), "wb").write(b"trocado")  # noqa: E731
        checa("main(): base aprovada passa (exit 0)", rodar_main([base], apr)[0] == 0)
        checa("CONTROLE main(): aprovada com render quebrado = exit 1", rodar_main([base], apr, mexe=quebra_render)[0] == 1)
        checa("main(): pendente com render quebrado = aviso, exit 0", rodar_main([base], pend, mexe=quebra_render)[0] == 0)
        rc, out = rodar_main([sa_cfm, base], apr)
        checa("CONTROLE main(): pendente com CFM = exit 1", rc == 1 and "::error::" in out)
        rc, _ = rodar_main([base], pend, mexe=lambda: (lambda m: (m["partes"][1]["textos_tela"].append("veja o vídeo inteiro no link"),
                                                               gravar_meta("st_x", m)))(carregar(irmao_de(base), {})))
        checa("CONTROLE main(): pendente com texto fora (com 'vídeo' na frase) = exit 1", rc == 1)
        checa("main(): fila vazia passa", rodar_main([], pend)[0] == 0)
        checa("CONTROLE main(): id repetido na fila = exit 1", rodar_main([base, base], apr)[0] == 1)
        checa("main(): --ids confere só o pedido (outra story quebrada fica de fora)",
              rodar_main([sa_cfm, base], apr, argv=["--ids", "st_x"])[0] == 0)
        checa("CONTROLE main(): --ids de id que não existe = exit 1", rodar_main([base], apr, argv=["--ids", "st_nao_existe"])[0] == 1)
        checa("CONTROLE main(): --exigir-render reprova o render da pendente",
              rodar_main([base], pend, argv=["--ids", "st_x", "--exigir-render"], mexe=quebra_render)[0] == 1
              and rodar_main([base], pend, argv=["--ids", "st_x", "--exigir-render"])[0] == 0)
    finally:
        usar_raiz(raiz_velha)
        shutil.rmtree(tmp, ignore_errors=True)
    print("\n" + ("AUTOTESTE OK" if not falhas else f"AUTOTESTE: {len(falhas)} FALHA(S)"))
    return 1 if falhas else 0


if __name__ == "__main__":
    sys.exit(main())
