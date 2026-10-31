# -*- coding: utf-8 -*-
"""
legenda.py — normalizador de LEGENDA do motor (plano de saída da estagnação, 12/09/2026, item A4).

Por que existe: a legenda publicada até 11/09 pedia três coisas (📤 manda · 📌 salva · 💬 chama),
trazia 3–9 hashtags e abria com o jargão. Régua adotada (Metricool, 24.364.803 posts de 375.118
contas, jan–fev/2025 × jan–fev/2026, verificada ao dígito em 11/09): post com hashtag tem −31,70%
de views e −33,89% de interações; pedir curtida −4,9%; pedir save +92%; e incluir MENÇÃO vale
+108% de alcance especificamente na faixa abaixo de 2.000 seguidores (a nossa). Mosseri, 07/2026:
"hashtags funcionam, mas nunca foram um bom jeito de aumentar alcance".

Regras aplicadas por normalizar():
  1. ZERO hashtags (linha só de tags some; tag no meio da frase some).
  2. UMA CTA por peça: ENVIAR (reel) ou SALVAR (carrossel). Nunca pedir curtida. Sem o bloco
     triplo 📤/📌/💬/📲 e sem CTA de contato na legenda (o wa.me vive na bio — Art. 10 CFM não é
     tocado: a legenda é do próprio perfil, o que muda é o número de pedidos).
  3. UMA menção pertinente (sociedade da área) — citação, nunca endosso.
  4. Keyword na fala do paciente nos primeiros 125 caracteres: override por id (PRIMEIRA_LINHA),
     porque isso é decisão editorial peça a peça, não regra de regex.
  5. Identificação CFM 2.336 (Arts. 4º/6º): "Médico" + CRM + RQE sempre presentes na assinatura.
  6. Transparência de IA (CFM 2.454): a linha "Narração com voz digital (IA)." dos reels é preservada.

Guardas: a função VALIDA a própria saída (validar()) e levanta ValueError se qualquer regra
ficar violada — normalizador que devolve legenda torta em silêncio é o furo que a casa já pagou.
checar_legenda.py aplica validar() à FILA (reels.json/posts.json − publicados) em CI.
"""
import hashlib
import re
import unicodedata

EMOJI_CTA = ("📤", "📌", "💬", "📲", "🦴")
TAIL_IA = "Narração com voz digital (IA)."
_RE_TAG = re.compile(r"(?<!\S)#[\wÀ-ɏ]+")
_RE_CTA_CORPO = re.compile(r"^(Envia |Manda |Conhece uma família|Salva |Salve |Compartilhe )", re.I)

# Menções pertinentes. Em 11/09/2026 a pesquisa (estag_distribuicao.md) deu "@sbortopediapediatrica,
# 2.465 seguidores" — perfil que NÃO EXISTE (31/10: responde igual a um @ inventado de controle; o
# site oficial sbop.org.br linka @sbopbr). Saiu em 12 peças. Daí a LISTA BRANCA abaixo.
MENCOES = {
    "reconstrucao": "Sociedade da área: @asami.brasil",
    "pediatria":    "Sociedade da área: @sbopbr",
    "pe_torto":     "Associação de famílias: @associacaoptc",
}
HANDLE_PROPRIO = "@rafaelvargasmd"

# LISTA BRANCA de menções (Rafael, 31/10/2026: "não pode colocar um @ numa página inexistente" /
# "tem que ter guardrail"). Todo @ de legenda/texto publicado tem de estar AQUI, com a PROVA de que o
# perfil existe e é de quem dizemos. Entrar na lista exige as duas coisas:
#   1. a fonte oficial (site da entidade) apontando para o perfil — ou, sem site que linke, o nome no
#      próprio perfil batendo com a entidade;
#   2. `python checar_mencoes.py --vivo @handle` com os controles passando (o perfil do Dr. resolve, um @
#      inventado não resolve) e o handle resolvendo.
# Nunca entra @ só porque uma pesquisa (humana ou de IA) disse que existe — foi assim que o erro nasceu.
MENCOES_VERIFICADAS = {
    "@rafaelvargasmd": {"nome": "Dr. Rafael Vargas (o próprio perfil)", "conferido_em": "2026-10-31",
                        "prova": "perfil próprio; título 'Dr. Rafael Vargas · Ortopedia (@rafaelvargasmd)'"},
    "@asami.brasil": {"nome": "ASAMI Brasil", "conferido_em": "2026-10-31",
                      "prova": "link do Instagram no site oficial asami-brasil.com.br; título do perfil "
                               "'ASAMI Brasil (@asami.brasil)'"},
    "@sbopbr": {"nome": "SBOP — Sociedade Brasileira de Ortopedia Pediátrica", "conferido_em": "2026-10-31",
                "prova": "link do Instagram no site oficial sbop.org.br; título do perfil 'Sociedade Brasileira "
                         "de Ortopedia Pediátrica (@sbopbr)'"},
    "@associacaoptc": {"nome": "Associação Primeiro Passo (pais de crianças com pé torto congênito)",
                       "conferido_em": "2026-10-31",
                       "prova": "título do perfil 'Associação Primeiro Passo (@associacaoptc)'; o site "
                                "primeiropasso.org não linka Instagram (só e-mail e grupo do Facebook)"},
}
# Handle do Instagram: letras, números, '.' e '_'; não termina em '.'. O lookbehind tira e-mail
# (contato@site.org) e "@@"; o '.' final de fim de frase sai no rstrip.
_RE_MENCAO = re.compile(r"(?<![\w.@])@([A-Za-z0-9_.]{1,30})")


def mencoes_em(texto):
    """Todos os @handles do texto, em minúsculas, na ordem em que aparecem."""
    return ["@" + m.rstrip(".").lower() for m in _RE_MENCAO.findall(texto or "") if m.rstrip(".")]


def mencoes_nao_verificadas(texto):
    """@handles do texto que NÃO estão em MENCOES_VERIFICADAS (vazio = ok)."""
    return [m for m in mencoes_em(texto) if m not in MENCOES_VERIFICADAS]


# A regra de saída não pode produzir @ fora da lista: falha no import, antes de qualquer legenda.
for _fam, _linha in MENCOES.items():
    _fora = mencoes_nao_verificadas(_linha)
    if _fora:
        raise ImportError(f"legenda.MENCOES[{_fam!r}] usa {_fora} fora de MENCOES_VERIFICADAS")

# "Núcleo primeiro" (13/09/2026): o destinatário da CTA é quem CUIDA do paciente — a rede real por
# onde o perfil cresce aos poucos. Nunca "marque", nunca "conte sua experiência" (CFM Art. 8º §4º).
CTAS = {
    ("reel", "reconstrucao"): ["Envia para quem precisa disso.",
                               "Envia para quem está passando por isso.",
                               "Envia para quem vai cuidar de você em casa.",
                               "Envia para o seu fisioterapeuta.",
                               "Manda para quem está na mesma fase."],
    ("reel", "pediatria"):    ["Envia para um pai ou uma mãe que precisa ver isso.",
                               "Envia para quem tem criança em casa.",
                               "Manda para a escola do seu filho.",
                               "Envia para quem cuida do seu filho quando você não está."],
    ("post", "reconstrucao"): ["Salva para consultar depois.",
                               "Salva para ter à mão quando precisar.",
                               "Salva para a próxima fase."],
    ("post", "pediatria"):    ["Salva para consultar depois.",
                               "Salva para ter à mão quando a dúvida bater.",
                               "Salva para a próxima consulta."],
}
CTAS[("reel", "pe_torto")] = CTAS[("reel", "pediatria")]
CTAS[("post", "pe_torto")] = CTAS[("post", "pediatria")]

# CTA específica por peça (os reels-caso já pediam envio com contexto; UMA cta, com o contexto).
CTA_POR_ID = {
    "caso_transporte_tibia": "Envia para quem precisa entender como o transporte ósseo funciona.",
    "caso_osteomielite_0cm": "Envia para quem convive há anos com uma sequela e acha que não tem mais jeito.",
    "caso_silver_russell":   "Envia para uma família que vive um plano longo desses.",
}

# Primeira linha na FALA DO PACIENTE (B1): (trecho atual, trecho novo). Aplicado uma vez, no início.
# Jargão continua no texto — na 2ª posição. "Alongamento ósseo" sai da 1ª linha (cauda de busca
# dominada por altura/estética/preço — o tabu do perfil; medição de 11/09).
PRIMEIRA_LINHA = {
    "primeira_consulta": ("Vai na primeira consulta sobre alongamento ósseo? Pergunte:",
                          "Vai na primeira consulta por uma perna mais curta ou torta? Pergunte:"),
    "qa_caroco_no_osso": ("Osteocondroma (exostose) é uma das lesões benignas e comuns que aparecem como um 'caroço duro' no osso da criança.",
                          "Um caroço duro no osso do seu filho? O osteocondroma (exostose) é uma das lesões benignas e comuns que aparecem assim na criança."),
    "qa_perna_curta_operar": ("Discrepância de membro (uma perna mais curta): nem sempre precisa operar.",
                              "Uma perna mais curta que a outra (discrepância de membro): nem sempre precisa operar."),
    "qa_ajustar_fixador": ("Método Ilizarov: ajustar o fixador dói? Desconfortos",
                           "Ajustar o fixador externo dói? No método Ilizarov, desconfortos"),
    "qa_banho_fixador": ("Cuidados com o fixador externo: a higiene diária",
                         "Pode tomar banho com o fixador externo? A higiene diária"),
    "c_on_medir_antes": ("Discrepância de membro (uma perna mais curta que a outra): medir antes de corrigir.",
                         "Uma perna mais curta que a outra (discrepância de membro): medir antes de corrigir."),
    "c_on_pseudartrose": ("Pseudartrose: a fratura que não cola.",
                          "A fratura que não cola — isso tem nome: pseudartrose."),
    "c_on_osteomielite": ("Osteomielite: quando a infecção atinge o osso.",
                          "Infecção no osso — a osteomielite — e como ela chega até lá."),
    "c_on_transporte_osseo": ("Transporte ósseo: refazer osso que se perdeu.",
                              "Refazer o osso que se perdeu: o transporte ósseo."),
    "c_on_osteotomia": ("Osteotomia: cortar o osso para realinhar.",
                        "Cortar o osso para realinhar: a osteotomia."),
    "c_on_tres_fases": ("As 3 fases do alongamento ósseo e da reconstrução, inclusive quando o motivo é uma discrepância de membro:",
                        "As 3 fases da reconstrução de um osso — inclusive quando o motivo é uma perna mais curta que a outra (discrepância de membro):"),
    "on_haste_magnetica": ("Para tratar uma discrepância de membro (a perna mais curta),",
                           "Para tratar uma perna mais curta que a outra (discrepância de membro),"),
    # a reescrita de 02/08 tirou o nome popular destes dois (lint termo->popular acusa FALTA)
    "on_salvamento_membro": ("a mesma usada na discrepância de membro)",
                             "a mesma usada quando uma perna fica mais curta que a outra — a discrepância de membro)"),
    "on_falha_ossea": ("encurtaria a perna — uma discrepância de membro.",
                       "encurtaria a perna (uma perna mais curta que a outra — a discrepância de membro)."),
}

_PED_PISTAS = ("criança", "crianca", "bebê", "bebe", "filho", "filha", "adolescente", "pediátric", "pediatric",
               "infantil", "infância", "infancia", "pais ")

# Família fixada por id onde a heurística erra (post60 fala de raquitismo/estatura sem dizer "criança").
FAMILIA_POR_ID = {
    "post60": "pediatria",
    "post61": "reconstrucao",   # institucional (pseudartrose, discrepância, sequelas) — nicho principal
}


def _norm(s):
    return unicodedata.normalize("NFKD", str(s)).encode("ascii", "ignore").decode().lower()


def familia(item_id="", texto="", motif_family=None):
    """reconstrucao | pediatria | pe_torto. Prioridade: pé torto no texto > motif_family do episódio
    > prefixo do id > pistas no texto > reconstrução (nicho principal)."""
    if str(item_id) in FAMILIA_POR_ID:
        return FAMILIA_POR_ID[str(item_id)]
    n = _norm(texto)
    if "pe torto" in n or "ponseti" in n:
        return "pe_torto"
    if motif_family == "bone":
        return "reconstrucao"
    if motif_family == "feet":
        return "pediatria"
    iid = str(item_id)
    if iid.startswith(("pnc_", "c_pnc_", "s_pnc_")):
        return "pediatria"
    if iid.startswith(("on_", "c_on_", "caso_", "s_on_")):
        return "reconstrucao"
    if any(p in n[:400] for p in _PED_PISTAS):
        return "pediatria"
    return "reconstrucao"


def _escolha(lista, chave):
    h = int(hashlib.md5(str(chave).encode("utf-8")).hexdigest(), 16)
    return lista[h % len(lista)]


def _limpa_tags(linha):
    return re.sub(r"\s{2,}", " ", _RE_TAG.sub("", linha)).strip()


def _tail_tipo(s):
    if s.startswith(TAIL_IA) or s.startswith("Narração com voz"):
        return "ia"
    if s.startswith(("Fonte:", "Referência:", "Referencia:")):
        return "fonte"
    if "CRM-SP" in s or s.startswith("Dr. Rafael Vargas"):
        return "sig"
    if s.startswith("Conteúdo educativo") or s.startswith("Conteudo educativo"):
        return "disc"
    return None


def _assinatura(s):
    if "CRM-SP" in s and "Médico" not in s and "Medico" not in s:
        s = s.replace("Dr. Rafael Vargas ·", "Dr. Rafael Vargas · Médico ·", 1)
        if "Médico" not in s:
            s = s.replace("Dr. Rafael Vargas", "Dr. Rafael Vargas · Médico", 1)
    return s


def normalizar(caption, formato, item_id="", fam=None, motif_family=None):
    """Devolve a legenda normalizada (str). formato: 'reel' | 'post'. Levanta ValueError se a
    saída não passar em validar() — nunca devolve legenda torta em silêncio."""
    assert formato in ("reel", "post"), formato
    fam = fam or familia(item_id, caption, motif_family)
    corpo, tail = [], {"ia": [], "fonte": [], "sig": [], "disc": []}
    em_tail = False
    for bruto in str(caption).split("\n"):
        s = bruto.strip()
        if not s:
            if not em_tail:
                corpo.append("")
            continue
        if _RE_TAG.match(s) and not _limpa_tags(s):
            continue                                   # linha só de hashtags
        if s.startswith(EMOJI_CTA):
            continue                                   # bloco triplo de CTA / slogan
        tipo = _tail_tipo(s)
        if tipo:
            em_tail = True
            s = _limpa_tags(s)
            if tipo == "sig":
                s = _assinatura(s)
            tail[tipo].append(s)
            continue
        if em_tail:
            continue                                   # texto solto depois da assinatura: era tag/CTA
        if _RE_CTA_CORPO.match(s):
            continue                                   # CTA em texto puro no corpo (reels-caso)
        if any(s.startswith(m.split(":")[0] + ":") for m in MENCOES.values()):
            continue                                   # menção de uma passada anterior (idempotência)
        corpo.append(_limpa_tags(s))
    texto = "\n".join(corpo)
    texto = re.sub(r"\n{3,}", "\n\n", texto).strip()
    if item_id in PRIMEIRA_LINHA:
        velho, novo = PRIMEIRA_LINHA[item_id]
        if velho in texto:
            texto = texto.replace(velho, novo, 1)
        elif novo not in texto:                        # nem o velho nem o novo: o texto-base mudou
            raise ValueError(f"{item_id}: trecho da PRIMEIRA_LINHA não encontrado: {velho[:60]!r}")
    cta = CTA_POR_ID.get(item_id) or _escolha(CTAS[(formato, fam)], item_id)
    mencao = MENCOES[fam]
    if not tail["sig"]:
        tail["sig"] = ["Dr. Rafael Vargas · Médico · CRM-SP 226103 · RQE 137901"]
    if not tail["disc"]:
        tail["disc"] = ["Conteúdo educativo; não substitui avaliação individual."]
    blocos = [texto, cta, mencao]
    rodape = tail["ia"] + tail["fonte"] + tail["sig"] + tail["disc"]
    blocos.append("\n".join(rodape))
    saida = "\n\n".join(b for b in blocos if b)
    problemas = validar(saida, formato)
    if problemas:
        raise ValueError(f"{item_id}: legenda normalizada ainda viola: {problemas}")
    return saida


_RE_ENVIO = re.compile(r"^(envia|manda)\s+(pra|para)\s+(quem|a|o|as|os|um|uma|alguém|aquele|aquela|seu|sua)\b", re.I)
_RE_CONTATO = re.compile(r"\b(direct|dm|inbox|mensagem|agend\w*|coment\w*|consulta\w*|whats\w*|link|bio)\b", re.I)


def cta_de_envio(cta):
    """CTA de reel = pedido de ENVIO a alguém, nunca de contato/agenda/comentário."""
    c = cta.strip()
    return bool(_RE_ENVIO.match(c)) and not _RE_CONTATO.search(c)


def validar(caption, formato):
    """Lista de violações (vazia = ok). Usada por normalizar() e por checar_legenda.py."""
    p = []
    n = _norm(caption)
    if "#" in caption:
        p.append("hashtag presente")
    # "curta" (adjetivo: perna mais CURTA) NÃO é pedido de curtida — o 1º regex desta função
    # reprovava toda legenda de discrepância de membro (achado no próprio auto-teste, 12/09).
    if re.search(r"\b(curte|curtir|curtiu|curtida|curtidas|deixa (o|um) like|da (o|um) like)\b", n) \
            or re.search(r"\blike\b", n):
        p.append("pede curtida")
    if any(e in caption for e in EMOJI_CTA):
        p.append("bloco de CTA com emoji")
    ctas = [l for l in caption.split("\n") if _RE_CTA_CORPO.match(l.strip())]
    if len(ctas) != 1:
        p.append(f"{len(ctas)} CTA(s) — exigida exatamente 1")
    elif formato == "reel" and not cta_de_envio(ctas[0]):
        # "Manda pra quem..." também é pedido de ENVIO (19/10/2026): os vídeos da geração nova
        # falam "Manda" e a legenda repete a CTA do vídeo. Antes, a variante "Manda para quem está
        # na mesma fase." de CTAS (13/09) quebraria normalizar() no primeiro reel que a sorteasse.
        # Mas o verbo sozinho não basta (auditoria 19/10): "Manda um direct pra agendar" passava.
        # Confere o DESTINO (pra quem / para um... ) e recusa contato, agenda e comentário.
        p.append("CTA de reel tem de pedir ENVIO a alguém (Envia/Manda pra quem…), sem contato")
    elif formato == "post" and not ctas[0].strip().lower().startswith("salva"):
        p.append("CTA de carrossel tem de ser SALVAR")
    mencoes = [m for m in mencoes_em(caption) if m != HANDLE_PROPRIO]
    if len(mencoes) < 1 or len(mencoes) > 2:
        p.append(f"{len(mencoes)} menção(ões) — exigidas 1 a 2")
    fora = mencoes_nao_verificadas(caption)
    if fora:
        p.append(f"menção a perfil NÃO verificado: {', '.join(fora)} (fora de MENCOES_VERIFICADAS)")
    if not ("crm" in n and "rqe" in n and "medico" in n):
        p.append("assinatura sem Médico+CRM+RQE")
    if "whatsapp" in n or "link da bio" in n:
        p.append("CTA de contato na legenda")
    return p


if __name__ == "__main__":
    import io, sys
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    exemplo = ("Joelho em X (geno valgo) na criança quase sempre é fase.\n\n📤 Manda pra um pai.\n"
               "📌 Salva pra lembrar. 💬 Curte e comenta.\n\n#ortopediapediatrica #joelhoemx\n\n"
               "Dr. Rafael Vargas · CRM-SP 226103 · RQE 137901")
    print(normalizar(exemplo, "reel", "pnc_joelho_valgo"))
    print("---")
    print(normalizar(exemplo, "post", "c_pnc_joelho"))
    # controle positivo: legenda com curtida/hashtag TEM de ser reprovada por validar()
    assert validar(exemplo, "reel"), "validar() deixou passar hashtag+curtida — detector morto"
    print("ok: validar() reprova o controle positivo")
