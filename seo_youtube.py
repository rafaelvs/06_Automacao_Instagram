# -*- coding: utf-8 -*-
"""
Motor de SEO/metadados do YouTube — série "Recuperação".
Gera TÍTULO (padrão variado por episódio → anti-templatização), DESCRIÇÃO (com E-E-A-T + disclaimer
CFM + WhatsApp + hashtags) e TAGS (semânticas por episódio). Fundamentado em ESTRATEGIA_YOUTUBE_2026.md:
 - CTR importa mas é "gated" pela retenção → título promete e o vídeo entrega (sem clickbait vazio).
 - Busca é SEMÂNTICA → título/descrição cobrem o TÓPICO e a INTENÇÃO (como o paciente pesquisa).
 - E-E-A-T (autoridade do cirurgião) é o FOSSO contra o "AI slop" + confiança do paciente (YMYL).
 - Variação: o PADRÃO do título alterna por episódio, então os títulos do canal não têm a mesma cara.

Versão 2 (03/07/2026): + 3 padrões de título (8 no total); + _EPISODE_TAGS (long-tail semânticos
por episódio, baseados em linguagem de paciente); + _SEARCH_INTENT (intenções de busca por episódio,
para guiar refinamento manual); + titulo_alt() para A/B; + score_seo() como gate de qualidade.
"""
SIG = ("Dr. Rafael Vargas · CRM-SP 226103 · RQE 137901 — "
       "Reconstrução e Alongamento Ósseo · Ortopedia Pediátrica.")
DISC = "Conteúdo educativo, não substitui a avaliação do seu médico."
WPP = "Dúvidas de rotina: WhatsApp (11) 3280-1413."

# ── PADRÕES DE TÍTULO (8 padrões, variam por episódio → anti-templatização) ──────────────────
# {foco} = tema do episódio (ex.: "Gesso no pós-operatório").
# {pais} = "" para adulto; " (guia para os pais)" para _kids.
# P0-P4: originais. P5-P7: novos (busca semântica + E-E-A-T).
TITLE_PATTERNS = [
    "{foco}: cuidados e sinais de alarme{pais}",                         # P0 - classic alarm
    "Saiu de cirurgia? {foco}{pais}",                                     # P1 - post-op hook
    "{foco} no pós-operatório — o que fazer{pais}",                       # P2 - how-to
    "Pós-operatório: {foco}{pais}",                                       # P3 - label (fraco, mas varia)
    "{foco}: o essencial e quando ir ao pronto-socorro{pais}",            # P4 - decision
    "O que é normal com {foco}? Quando é sinal de alarme{pais}",          # P5 - reassurance arc
    "{foco}: quando chamar o médico — e quando não precisa{pais}",        # P6 - decision tree
    "Cirurgião explica: {foco}{pais}",                                    # P7 - E-E-A-T / autoridade
]

# ── TAGS SEMÂNTICAS POR EPISÓDIO ────────────────────────────────────────────────────────────
# Long-tail + linguagem de paciente (o que o paciente realmente digita no YouTube).
# Merge com a base genérica em tags().
_EPISODE_TAGS = {
    "gesso_pos_op": [
        "gesso ortopédico", "cuidado com gesso", "gesso molhou", "gesso pós-operatório",
        "gesso apertando", "dedos roxos gesso", "molhar gesso", "banho com gesso",
        "gesso impermeável", "quanto tempo de gesso", "pronto-socorro gesso",
    ],
    "gesso_pos_op_kids": [
        "gesso criança", "filho de gesso", "gesso infantil", "cuidar criança com gesso",
        "banho criança com gesso", "filho operado gesso", "gesso criança molhou",
        "sinais de alarme gesso criança", "criança agitada gesso",
    ],
    "fixador_externo": [
        "fixador externo", "cuidado com pinos fixador", "infecção pino fixador",
        "como limpar pinos fixador", "fixador ilizarov", "ilizarov cuidados",
        "pinos no osso", "banho com fixador externo", "pino vermelho infecção",
        "fixador externo pós-operatório", "pino frouxo fixador",
    ],
    "fixador_externo_kids": [
        "fixador externo criança", "filho com fixador", "pino fixador criança",
        "cuidar criança fixador externo", "ilizarov infantil",
        "ortopedia pediátrica fixador", "infecção pino criança",
    ],
    "carga_fisio": [
        "quando pisar depois da cirurgia", "carga após cirurgia ortopédica",
        "medo de mexer depois da cirurgia", "fisioterapia ortopédica pós-operatório",
        "reabilitação ortopédica", "quando voltar a andar após cirurgia",
        "mobilização precoce cirurgia", "repouso pós-cirurgia",
        "apoio de peso pós-cirurgia", "fisioterapia quando começar",
    ],
    "carga_fisio_kids": [
        "fisioterapia criança operada", "filho com medo de mexer após cirurgia",
        "reabilitação criança cirurgia", "quando filho pode brincar após cirurgia",
        "criança fisioterapia pós-operatório", "movimento após cirurgia criança",
    ],
    "artrorrise": [
        "artrorrise", "pé plano cirurgia", "pé plano implante", "pé plano pós-operatório",
        "pé chato cirurgia", "pé plano adulto cirurgia", "bota pé plano",
        "cirurgia pé plano recuperação", "implante calcanhar pé plano",
        "pé plano corrigido cirurgia",
    ],
    "artrorrise_kids": [
        "artrorrise criança", "pé plano criança cirurgia", "pé plano infantil operado",
        "filho pé plano operado", "cirurgia pé chato criança",
        "implante pé plano criança", "pé plano pediátrico",
    ],
    "growth_guided": [
        "epifisiodese", "guia de crescimento ósseo", "placa de crescimento cirurgia",
        "cirurgia crescimento joelho", "diferença comprimento pernas cirurgia",
        "deformidade joelho cirurgia", "epifisiodese pós-operatório",
        "varo valgo cirurgia joelho", "implante joelho crescimento",
    ],
    "growth_guided_kids": [
        "epifisiodese criança", "guia de crescimento filho", "cirurgia crescimento criança",
        "placa crescimento joelho criança", "filho operou o joelho crescimento",
        "epifisiodese pediátrica", "implante crescimento osso criança",
    ],
    "ferida_cirurgica": [
        "ferida cirúrgica cuidado", "curativo pós-operatório", "quando molhar a ferida",
        "pontos cirurgia ortopédica", "sinais infecção ferida", "secar ferida cirurgica",
        "vermelhidão na ferida", "quanto tempo para fechar ferida cirúrgica",
    ],
    "ferida_cirurgica_kids": [
        "ferida cirúrgica criança", "curativo criança operada", "filho operou ferida",
        "criança coçou a ferida", "pontos criança cirurgia", "ferida criança pós-op",
    ],
    "dor_posop": [
        "dor após cirurgia", "dor pós-operatório ortopédico", "dor normal pós-operatório",
        "analgésico pós-operatório", "dor que não passa cirurgia",
        "síndrome compartimental sinais", "dor crescente cirurgia",
        "quanto dói depois da cirurgia ortopédica",
    ],
    "dor_posop_kids": [
        "dor criança operada", "filho chora depois da cirurgia",
        "analgésico criança pós-operatório", "criança agitada dor cirurgia",
        "criança inconsolável após cirurgia",
    ],
    "edema": [
        "inchaço após cirurgia ortopédica", "edema pós-operatório",
        "perna inchada cirurgia", "como desinchar depois da cirurgia",
        "elevação do membro pós-operatório", "inchaço normal cirurgia",
        "gelo inchaço cirurgia perigo",
    ],
    "edema_kids": [
        "inchaço criança operada", "filho inchado após cirurgia",
        "como desinchar criança operada", "edema infantil pós-cirurgia",
        "criança perna inchada cirurgia",
    ],
    "infeccao_ferida": [
        "infecção na ferida cirúrgica", "ferida infectada ortopedia",
        "febre após cirurgia ortopédica", "pus na ferida cirúrgica",
        "vermelhidão ferida cirurgia alastra", "secreção ferida cirúrgica",
        "infecção pós-operatória ortopédica",
    ],
    "infeccao_ferida_kids": [
        "infecção ferida criança", "filho com infecção após cirurgia",
        "ferida infectada criança ortopedia", "febre criança depois da cirurgia",
    ],
    "tvp": [
        "trombose após cirurgia", "TVP trombose venosa profunda",
        "coágulo após cirurgia ortopédica", "perna inchada trombose",
        "anticoagulante pós-operatório", "panturrilha dor cirurgia trombose",
        "falta de ar após cirurgia", "embolia pulmonar ortopedia",
    ],
    "tvp_kids": [
        "trombose criança", "TVP pediátrica", "criança trombose após cirurgia",
        "perna inchada criança operada trombose",
    ],
    "fisioterapia": [
        "fisioterapia pós-operatório ortopédico", "quando começar fisioterapia",
        "fisioterapia precoce ortopedia", "reabilitação ortopédica cirurgia",
        "exercício pós-cirurgia ortopédica", "rigidez após cirurgia como tratar",
        "fisioterapia obrigatória cirurgia",
    ],
    "fisioterapia_kids": [
        "fisioterapia criança operada", "reabilitação infantil ortopédica",
        "criança fisioterapia cirurgia", "fisioterapia lúdica criança",
        "quando iniciar fisioterapia criança operada",
    ],
    "retorno_atividades": [
        "quando voltar a trabalhar cirurgia ortopédica", "quando dirigir após cirurgia",
        "retorno atividades pós-operatório", "quando caminhar após cirurgia",
        "retorno esporte após cirurgia", "volta ao trabalho cirurgia ortopédica",
        "quando voltar a fazer esporte após cirurgia",
    ],
    "retorno_atividades_kids": [
        "quando filho volta à escola após cirurgia", "criança volta esporte cirurgia",
        "retorno atividades criança operada", "quando filho pode brincar cirurgia",
        "criança educação física após cirurgia",
    ],
    "ortese_bota": [
        "bota ortopédica pós-operatório", "órtese imobilizadora", "bota imobilizadora",
        "como usar bota ortopédica", "bota ortopédica pode dormir",
        "quando tirar bota ortopédica", "bota ortopédica pressão",
    ],
    "ortese_bota_kids": [
        "bota ortopédica criança", "filho com bota ortopédica",
        "criança tira bota escondido", "órtese infantil ortopedia",
        "bota criança cirurgia",
    ],
    "distracao_alongamento": [
        "alongamento ósseo ilizarov", "distração óssea pós-operatório",
        "ativação do fixador em casa", "ilizarov em casa cuidados",
        "pinos alongamento ósseo", "quanto tempo fixador externo ilizarov",
        "cuidado fixador ilizarov", "voltas do fixador",
    ],
    "distracao_alongamento_kids": [
        "alongamento ósseo criança", "ilizarov infantil em casa",
        "distração óssea criança", "filho alongamento ósseo fixador",
        "criança fixador ilizarov rotina",
    ],
    "consolidacao": [
        "consolidação óssea pós-operatório", "osso fechando radiografia",
        "quando o osso consolida", "calo ósseo formação",
        "retirada de carga pós-cirurgia", "tabagismo consolidação óssea",
        "quanto tempo para consolidar osso",
    ],
    "consolidacao_kids": [
        "consolidação óssea criança", "criança osso fechando",
        "filho consolidação após cirurgia", "osso criança consolida mais rápido",
    ],
    "retirada_fixador": [
        "retirada do fixador externo", "retirar fixador ortopédico",
        "pós-retirada fixador cuidados", "quando retirar fixador externo",
        "buracos dos pinos após retirada", "osso após retirada do fixador",
        "cicatrização pinos fixador",
    ],
    "retirada_fixador_kids": [
        "retirada fixador criança", "filho retirando fixador externo",
        "tirar pinos criança cirurgia", "fixador externo criança retirada",
    ],
    "banho_posop": [
        "banho após cirurgia ortopédica", "quando posso molhar a ferida",
        "banho com gesso impermeável", "banho com curativo cirúrgico",
        "como tomar banho com fixador externo", "molhar ferida cirurgia risco",
        "banho pós-operatório seguro",
    ],
    "banho_posop_kids": [
        "banho criança com gesso", "como dar banho filho operado",
        "banho com fixador criança", "criança banho pós-operatório seguro",
        "banho esponja criança gesso ortopedia",
    ],
}

# ── INTENÇÕES DE BUSCA (top 3-5 queries do paciente por episódio) ────────────────────────────
# Referência para refinamento manual de título/descrição e para futura análise de performance.
_SEARCH_INTENT = {
    "gesso_pos_op":       ["cuidado com gesso ortopédico", "gesso molhou o que fazer",
                           "gesso apertando o que fazer", "dedos roxos no gesso"],
    "gesso_pos_op_kids":  ["filho com gesso cuidados", "gesso criança banho",
                           "criança agitada com gesso quando ir ao pronto-socorro"],
    "fixador_externo":    ["cuidado com pinos do fixador", "infecção pino fixador",
                           "como limpar pinos fixador externo", "pino vermelho o que fazer"],
    "fixador_externo_kids": ["fixador externo criança cuidados", "infecção pino criança"],
    "carga_fisio":        ["quando posso pisar após cirurgia", "fisioterapia pós-operatório quando",
                           "medo de mexer depois da cirurgia"],
    "carga_fisio_kids":   ["quando filho pode mexer após cirurgia", "fisioterapia criança cirurgia"],
    "artrorrise":         ["artrorrise pós-operatório", "pé plano cirurgia recuperação",
                           "bota após artrorrise"],
    "artrorrise_kids":    ["artrorrise criança cuidados", "pé plano infantil cirurgia"],
    "growth_guided":      ["epifisiodese pós-operatório", "cirurgia de crescimento joelho",
                           "diferença de perna cirurgia"],
    "growth_guided_kids": ["epifisiodese criança", "cirurgia crescimento filho cuidados"],
    "ferida_cirurgica":   ["cuidado com ferida cirúrgica", "quando molhar ferida após cirurgia",
                           "ferida vermelha ortopedia"],
    "ferida_cirurgica_kids": ["ferida cirúrgica criança", "criança coçou a ferida"],
    "dor_posop":          ["dor após cirurgia ortopédica", "dor que não passa cirurgia",
                           "dor pós-operatória normal"],
    "dor_posop_kids":     ["filho chora muito após cirurgia", "criança com dor ortopedia"],
    "edema":              ["inchaço após cirurgia ortopédica", "como desinchar",
                           "edema pós-operatório"],
    "edema_kids":         ["filho inchado após cirurgia", "edema criança operada"],
    "infeccao_ferida":    ["infecção ferida cirúrgica", "febre após cirurgia",
                           "pus na ferida ortopedia"],
    "infeccao_ferida_kids": ["infecção ferida criança", "febre criança cirurgia"],
    "tvp":                ["trombose após cirurgia ortopédica", "perna inchada trombose",
                           "coágulo após cirurgia"],
    "tvp_kids":           ["trombose criança cirurgia", "TVP pediátrica"],
    "fisioterapia":       ["fisioterapia pós-operatório obrigatória", "quando começar fisioterapia",
                           "reabilitação ortopédica"],
    "fisioterapia_kids":  ["fisioterapia criança operada", "reabilitação infantil cirurgia"],
    "retorno_atividades": ["quando voltar trabalhar após cirurgia", "quando dirigir após cirurgia",
                           "retorno esporte ortopedia"],
    "retorno_atividades_kids": ["quando filho volta escola após cirurgia",
                                "criança volta brincar após cirurgia"],
    "ortese_bota":        ["bota ortopédica como usar", "posso dormir com bota ortopédica",
                           "quando tirar bota ortopédica"],
    "ortese_bota_kids":   ["bota ortopédica criança", "filho tira bota escondido"],
    "distracao_alongamento": ["ativação do fixador em casa", "ilizarov em casa",
                              "quanto voltas no fixador", "alongamento ósseo cuidados"],
    "distracao_alongamento_kids": ["ilizarov criança em casa", "alongamento ósseo filho"],
    "consolidacao":       ["quando o osso consolida após cirurgia", "calo ósseo quanto tempo",
                           "radiografia consolidação"],
    "consolidacao_kids":  ["consolidação óssea criança", "osso filho fechando"],
    "retirada_fixador":   ["retirada do fixador externo", "depois de retirar o fixador",
                           "cuidado após retirar fixador"],
    "retirada_fixador_kids": ["retirada fixador criança", "tirar pinos filho"],
    "banho_posop":        ["quando posso molhar a ferida", "como tomar banho com gesso",
                           "banho após cirurgia ortopédica"],
    "banho_posop_kids":   ["banho filho com gesso", "como dar banho criança com fixador"],
}


def _is_kids(eid): return str(eid).endswith("_kids")


def titulo(episode, foco, idx=None):
    """Título variado e dentro do limite (100 chars). foco = tema curto (ex.: 'Gesso no pós-operatório')."""
    eid = episode["id"]; pais = " (guia para os pais)" if _is_kids(eid) else ""
    i = (idx if idx is not None else sum(map(ord, eid))) % len(TITLE_PATTERNS)
    t = TITLE_PATTERNS[i].format(foco=foco, pais=pais)
    if "#shorts" not in t.lower():
        t = (t[:100 - len(" #Shorts")]).rstrip() + " #Shorts"
    return t[:100]


def titulo_alt(episode, foco, avoid=None):
    """Título alternativo para A/B (padrão seguinte na roleta).
    avoid: string a evitar (ex.: título original já publicado) — avança +1 até diferir."""
    eid = episode["id"]; pais = " (guia para os pais)" if _is_kids(eid) else ""
    base = sum(map(ord, eid))
    n = len(TITLE_PATTERNS)
    for offset in range(1, n):
        i = (base + offset) % n
        t = TITLE_PATTERNS[i].format(foco=foco, pais=pais)
        if "#shorts" not in t.lower():
            t = (t[:100 - len(" #Shorts")]).rstrip() + " #Shorts"
        t = t[:100]
        if avoid is None or t != avoid:
            return t
    return t  # fallback: retorna o último (não deve ocorrer)


def descricao(hook, pontos, hashtags="", fontes=None):
    """Descrição com E-E-A-T + CFM. hook=1ª linha forte; pontos=lista; fontes=lista de URLs."""
    corpo = hook.strip() + "\n\n" + "\n".join("• " + p for p in pontos)
    bloco_fontes = ("\n\nReferências: " + " · ".join(fontes)) if fontes else ""
    tags_line = ("\n\n" + hashtags.strip()) if hashtags else ""
    return f"{corpo}\n\n{WPP}\n\n{SIG}\n{DISC}{bloco_fontes}{tags_line}"


def tags(foco, kids=False, episode_id=None):
    """Tags semânticas: base genérica + episode-specific long-tail + foco.
    episode_id ativa as tags de linguagem-de-paciente mapeadas em _EPISODE_TAGS."""
    base = [
        "ortopedia", "pós-operatório", "recuperação", "Dr. Rafael Vargas",
        "alongamento ósseo", "reconstrução óssea", "ortopedia São Paulo",
        "cirurgia ortopédica",
    ]
    if kids:
        base += ["ortopedia pediátrica", "ortopedia infantil", "pais", "criança"]
    specific = _EPISODE_TAGS.get(episode_id, []) if episode_id else []
    f = foco.lower().strip()
    all_tags = base + specific + ([f] if f not in base and f not in specific else [])
    seen = set()
    return [t for t in all_tags if not (t in seen or seen.add(t))]


def search_intent(episode_id):
    """Top queries do paciente para o episódio — guia para refinamento manual do título."""
    return _SEARCH_INTENT.get(episode_id, [])


def score_seo(title, description, tags_list):
    """Gate de qualidade SEO. Retorna (score 0-100, lista de issues)."""
    issues = []
    score = 100
    if len(title) < 45:
        issues.append(f"título curto ({len(title)} chars; ideal ≥ 45)")
        score -= 15
    if len(title) > 100:
        issues.append(f"título longo ({len(title)} chars; limite = 100)")
        score -= 20
    if "#shorts" not in title.lower():
        issues.append("título sem #Shorts")
        score -= 10
    if len(description) < 200:
        issues.append(f"descrição curta ({len(description)} chars; ideal ≥ 200)")
        score -= 15
    if "pronto-socorro" not in description.lower() and "emergência" not in description.lower():
        issues.append("descrição sem menção a pronto-socorro/emergência (CFM)")
        score -= 10
    if "CRM-SP" not in description:
        issues.append("descrição sem assinatura CRM-SP (CFM)")
        score -= 20
    if len(tags_list) < 10:
        issues.append(f"poucas tags ({len(tags_list)}; ideal ≥ 10)")
        score -= 10
    return max(0, score), issues


def gerar(episode, foco, hook, pontos, hashtags="", fontes=None, idx=None):
    """Conveniência: retorna dict {title, title_alt, description, tags, search_intent} pronto p/ o upload."""
    kids = _is_kids(episode["id"])
    eid = episode["id"]
    t = titulo(episode, foco, idx)
    t_alt = titulo_alt(episode, foco, avoid=t)
    desc = descricao(hook, pontos, hashtags, fontes)
    tgs = tags(foco, kids, eid)
    sc, title_score, desc_score = t, score_seo(t, desc, tgs)[0], score_seo(t, desc, tgs)[1]
    return {
        "title": t,
        "title_alt": t_alt,
        "description": desc,
        "tags": tgs,
        "search_intent": search_intent(eid),
    }


if __name__ == "__main__":
    demo = {"id": "fixador_externo"}
    out = gerar(demo, "Fixador externo",
                "Saiu da cirurgia com fixador externo? Cuidar dos pinos evita a complicação mais comum — a infecção.",
                ["Lave os pinos no banho com sabonete neutro — um a um, sem cruzar a limpeza.",
                 "Seque bem; aplique álcool 70% só no metal, nunca na pele.",
                 "Vermelhidão, calor, secreção ou pino frouxo: pronto-socorro."],
                "#Shorts #fixadorexterno #ilizarov #ortopedia #drrafaelvargas",
                ["https://orthoinfo.aaos.org", "https://sbot.org.br"])
    s, issues = score_seo(out["title"], out["description"], out["tags"])
    print("TÍTULO:", out["title"])
    print("TÍTULO ALT:", out["title_alt"])
    print(f"TAGS ({len(out['tags'])}):", out["tags"])
    print(f"SCORE SEO: {s}/100", f"| issues: {issues or 'nenhum'}")
    print("\nINTENÇÕES DE BUSCA:", out["search_intent"])
    print("\nDESCRIÇÃO:\n", out["description"])
