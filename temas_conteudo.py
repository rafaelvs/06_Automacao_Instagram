# -*- coding: utf-8 -*-
"""TEMA de cada peça e a regra de DISTÂNCIA ENTRE TEMAS (Rafael, 24/10/2026).

O pedido, nas palavras dele: "não colocar coisas que foram postadas muito recentemente
sobrepondo [...] como a gente vai fazer a partir das postagens anteriores, a gente tem que usar
temas mais anteriores nas próximas postagens, para não ficar repetitivo demais".

Vira duas regras, aplicadas às peças DERIVADAS (story e carrossel da geração nova, que nascem de
um reel COMO FUNCIONA ou de uma peça antiga):
  1. DISTÂNCIA: a peça não sai se o MESMO TEMA apareceu, em qualquer superfície (reel, carrossel,
     story, sequência antiga), há menos de N dias — nem se ele vai aparecer (reel já na fila) em
     menos de N dias. N = regra_reels.DIAS_ENTRE_MESMO_TEMA_PADRAO.
  2. ANTIGUIDADE: entre as peças liberadas, sai primeiro a do tema que apareceu há MAIS tempo.

O tema é uma chave curta (ex.: "alongamento", "pe_virado"). Ordem de resolução: campo "tema" do
item → mapa explícito por id → tema do reel de origem (reel_ref) → palavras do id → None.

Sem tema a peça não bloqueia nada e passa À FRENTE das outras (ultima = date.min). Por isso a peça
DERIVADA (story) sem tema classificável, ou com campo "tema" fora de NOMES (erro de digitação, que
tema_de descartaria calado), é REPROVADA no portão (problemas_de_tema, chamado por checar_stories).
As palavras do id casam por TOKEN separado por '_' (prefixo do token: 'manca' casa 'mancando'), nunca
por substring solta: 'cola' dentro de 'escola' classificava 'trabalho_escola' como consolidação.
`python temas_conteudo.py --relatorio` lista os ids da fila e do estado cujo tema veio por palavra
(último recurso: alguém revisa) ou ficou sem tema.
"""
import datetime as dt

# Temas (nome legível) — base: o ranking de temas de sucesso (lab/ranking/temas.py, 19/10).
NOMES = {
    "pinos": "pinos, curativo e banho com fixador",
    "rotina_fixador": "rotina com fixador (dormir, sentar, roupa, viajar, escola)",
    "fixador_haste": "que aparelho é esse? fixador x haste",
    "tempo_tratamento": "quanto tempo dura, dói?, quando volto a pisar, retirada",
    "alongamento": "como o osso cresce no alongamento (1 mm por dia)",
    "discrepancia": "uma perna mais curta que a outra",
    "consolidacao": "como o osso cola / osso que não cola / refratura",
    "osteomielite": "infecção no osso (osteomielite)",
    "trauma_transporte": "acidente que levou osso / transporte ósseo",
    "gesso_placa": "gesso e placa depois da fratura",
    "pernas_crianca": "perna torta ou em X na criança",
    "eixo": "corrigir o eixo da perna",
    "pe_torto": "pé torto do bebê",
    "pe_virado": "pé virado para dentro ou para fora",
    "pe_chato": "pé chato, palmilha e sapato",
    "dor_crescimento": "dor de crescimento",
    "quadril_bebe": "quadril do bebê (displasia)",
    "ponta_pes": "andar na ponta dos pés",
    "mancando": "criança mancando / dor no quadril ou joelho sem trauma",
    "escoliose": "costas da criança (escoliose, mochila)",
    "andar": "quando a criança anda / cai muito / andador",
    "esporte": "dor no esporte / fratura por estresse",
    "joelho": "joelho que estala / joelho da criança",
    "fratura_crianca": "osso da criança, placa de crescimento, fratura na criança",
    "cotovelo_baba": "cotovelo de babá",
    "nao_estetica": "o que é reconstrução (e não é estética)",
    "consulta": "como é a consulta e o acompanhamento",
    "socorros": "primeiros socorros",
    "outros": "outros",
}

POR_ID = {
    # geração nova — reels COMO FUNCIONA
    "cf_alongamento": "alongamento", "cf_regra_milimetro": "alongamento",
    "cf_fratura_cola": "consolidacao", "cf_pseudartrose": "consolidacao", "cf_refratura": "consolidacao",
    "cf_transporte_osseo": "trauma_transporte", "cf_osteomielite": "osteomielite",
    "cf_pe_virado": "pe_virado", "cf_eixo_perna": "eixo", "cf_corrigir_e_alongar": "eixo",
    "cf_fixador_circular": "fixador_haste", "cf_gesso_placa": "gesso_placa", "cf_pe_torto": "pe_torto",
    "cf_escoliose": "escoliose", "cf_quadril_bebe": "quadril_bebe", "cf_placa_crescimento": "fratura_crianca",
    "cf_discrepancia_causas": "discrepancia", "cf_cotovelo_baba": "cotovelo_baba",
    "cf_quando_pisar": "tempo_tratamento", "cf_fisioterapia": "tempo_tratamento", "cf_quanto_tempo": "tempo_tratamento",
    "cf_retirada_fixador": "tempo_tratamento", "cf_dor_alongamento": "tempo_tratamento",
    "cf_crianca_mancando": "mancando", "cf_joelho_quadril": "mancando", "cf_pernas_x_o": "pernas_crianca",
    "cf_osgood_sever": "esporte", "cf_fratura_estresse": "esporte", "cf_andador": "andar",
    # geração nova — conversas
    "cv_fixador": "fixador_haste", "cv_gesso_filho": "gesso_placa", "cv_osso": "consolidacao",
    "cv_muleta": "tempo_tratamento", "cv_pinos": "pinos", "cv_pe_chato": "pe_chato",
    "cv_dor_crescimento": "dor_crescimento", "cv_perna_curta": "discrepancia",
    # peças antigas (ranking de 19/10)
    "post37": "pinos", "on_cuidado_pinos": "pinos", "qa_banho_fixador": "pinos", "c_on_cuidado_pinos": "pinos",
    "v_reconstrucao_sex": "pinos", "fx_kit_casa": "pinos", "fx_pino_inflamado": "pinos", "qa_pino_frouxo": "pinos",
    "v_reconstrucao_sab": "pinos",
    "post21": "rotina_fixador", "v_reconstrucao_qui": "rotina_fixador", "fx_dormir": "rotina_fixador",
    "fx_sentar_levantar": "rotina_fixador", "fx_roupa": "rotina_fixador", "fx_viagem": "rotina_fixador",
    "post03": "fixador_haste", "qa_gaiola_perna": "fixador_haste", "v_reconstrucao_qua": "fixador_haste",
    "fixador_ou_haste": "fixador_haste", "on_fixador_vs_haste": "fixador_haste", "c_on_fixador_vs_haste": "fixador_haste",
    "s_on_fixador_vs_haste": "fixador_haste",
    "post12": "tempo_tratamento", "post38": "tempo_tratamento", "on_quanto_tempo": "tempo_tratamento",
    "c_on_quanto_tempo": "tempo_tratamento", "qa_tempo_fixador": "tempo_tratamento", "tempo_tratamento": "tempo_tratamento",
    "qa_quando_pisar": "tempo_tratamento", "fim_tratamento": "tempo_tratamento", "on_fisioterapia": "tempo_tratamento",
    "fx_retirada": "tempo_tratamento", "s_on_quanto_tempo": "tempo_tratamento", "s_on_pisar_ou_nao": "tempo_tratamento",
    "s_on_dia_da_retirada": "tempo_tratamento", "s_on_dor_no_alongamento": "tempo_tratamento",
    "reel03": "alongamento", "on_osso_cresce": "alongamento", "on_regra_milimetro": "alongamento",
    "on_tres_fases": "alongamento", "c_on_tres_fases": "alongamento", "post22": "alongamento",
    "v_reconstrucao_dom": "alongamento", "c_on_osso_cresce": "alongamento", "c_on_regra_milimetro": "alongamento",
    "post04": "discrepancia", "on_discrepancia": "discrepancia", "on_medir_antes": "discrepancia",
    "c_on_medir_antes": "discrepancia", "c_on_discrepancia": "discrepancia", "qa_perna_encurtou_acidente": "discrepancia",
    "post36": "discrepancia", "discrepancia_membro": "discrepancia", "v_reconstrucao_ter": "discrepancia",
    "qa_perna_curta_operar": "discrepancia", "pnc_perna_curta_crianca": "discrepancia", "post50": "discrepancia",
    "s_on_discrepancia": "discrepancia", "s_on_medir_antes": "discrepancia",
    "post05": "consolidacao", "on_pseudartrose": "consolidacao", "on_tres_razoes": "consolidacao",
    "qa_osso_nao_cola": "consolidacao", "post39": "consolidacao", "pseudartrose": "consolidacao",
    "c_on_pseudartrose": "consolidacao", "c_on_tres_razoes": "consolidacao", "qa_tempo_osso_colar": "consolidacao",
    "on_cigarro": "consolidacao", "qa_cigarro_osso": "consolidacao", "qa_calo_osseo": "consolidacao",
    "qa_refratura": "consolidacao",
    "post14": "osteomielite", "on_osteomielite": "osteomielite", "post40": "osteomielite",
    "caso_osteomielite_0cm": "osteomielite", "c_on_osteomielite": "osteomielite",
    "post13": "trauma_transporte", "on_pos_trauma": "trauma_transporte", "on_transporte_osseo": "trauma_transporte",
    "caso_transporte_tibia": "trauma_transporte", "sequela_fratura": "trauma_transporte",
    "s_on_transporte_osseo": "trauma_transporte", "c_on_transporte_osseo": "trauma_transporte",
    "qa_gesso_molhar": "gesso_placa", "qa_tirar_placa": "gesso_placa",
    "pnc_pernas_tortas": "pernas_crianca", "post15": "pernas_crianca", "post25": "pernas_crianca",
    "v_pernas_ter": "pernas_crianca", "v_pernas_qua": "pernas_crianca", "v_pernas_sab": "pernas_crianca",
    "post60": "pernas_crianca", "v_pernas_dom": "pernas_crianca", "v_pernas_seg": "pernas_crianca",
    "v_pernas_qui": "pernas_crianca", "v_pernas_sex": "pernas_crianca",
    "on_perna_torta_adulto": "eixo", "post41": "eixo", "post48": "eixo", "deformidade_angular": "eixo",
    "on_osteotomia": "eixo", "v_reconstrucao_seg": "eixo", "c_on_osteotomia": "eixo", "c_on_perna_torta_adulto": "eixo",
    "reel02": "pe_torto", "pnc_pe_torto": "pe_torto", "post19": "pe_torto", "qa_pe_torto_bebe": "pe_torto",
    "pnc_pe_pra_dentro": "pe_virado", "post42": "pe_virado", "post44": "pe_virado", "s_pnc_pe_pra_dentro": "pe_virado",
    "pnc_pe_chato": "pe_chato", "post26": "pe_chato", "qa_pe_chato_palmilha": "pe_chato", "pnc_tenis_caro": "pe_chato",
    "post33": "pe_chato", "post51": "pe_chato",
    "reel01": "dor_crescimento", "pnc_dor_crescimento": "dor_crescimento", "post24": "dor_crescimento",
    "pnc_nao_dor_crescimento": "dor_crescimento", "qa_dor_crescimento": "dor_crescimento",
    "pnc_displasia_quadril": "quadril_bebe", "post20": "quadril_bebe", "qa_ultrassom_quadril": "quadril_bebe",
    "pnc_ponta_dos_pes": "ponta_pes", "qa_ponta_dos_pes": "ponta_pes",
    "pnc_mancando": "mancando", "pnc_mancar_febre": "mancando", "qa_crianca_mancando": "mancando",
    "post35": "mancando", "post29": "mancando", "pnc_quando_procurar": "mancando",
    "post27": "escoliose", "pnc_escoliose": "escoliose", "esc_teste_adams": "escoliose", "pnc_mochila": "escoliose",
    "post55": "escoliose", "esc_estirao": "escoliose", "esc_nao_doi": "escoliose", "s_pnc_escoliose": "escoliose",
    "pnc_andador": "andar", "pnc_marcos_andar": "andar", "post34": "andar", "pnc_cai_muito": "andar",
    "pnc_sentar_w": "andar", "post06": "andar", "post47": "andar",
    "post28": "esporte", "post52": "esporte", "post56": "esporte", "post57": "esporte", "s_pnc_esporte_apos_fratura": "esporte",
    "pnc_estalo_joelho": "joelho", "post53": "joelho", "post54": "joelho",
    "post16": "fratura_crianca", "post49": "fratura_crianca", "post32": "fratura_crianca", "post43": "fratura_crianca",
    "post30": "outros", "post31": "cotovelo_baba", "post23": "outros", "qa_caroco_no_osso": "outros",
    "caso_silver_russell": "discrepancia",
    "post02": "nao_estetica", "on_nao_estetica": "nao_estetica",
    "post07": "consulta", "post08": "consulta", "post11": "consulta", "post17": "consulta", "post18": "consulta",
    "post45": "consulta", "post46": "consulta", "post58": "consulta", "post61": "consulta",
    "primeira_consulta": "consulta", "s_on_consulta_de_controle": "consulta",
    "s_on_tres_fases": "alongamento", "s_on_tres_razoes": "consolidacao", "s_on_cigarro": "consolidacao",
    "s_on_muletas_sem_erro": "tempo_tratamento", "s_on_dirigir_trabalho": "rotina_fixador",
    "s_pnc_primeira_consulta": "consulta", "s_on_osteotomia": "eixo", "s_on_perna_torta_adulto": "eixo",
    # revisão 24/10 (a palavra do id classificava errado: 'cola' em 'escola', 'fixador' antes de 'rotina',
    # 'joelho' em joelho valgo = perna em X)
    "trabalho_escola": "rotina_fixador", "vida_cotidiana_fixador": "rotina_fixador",
    "s_on_fixador_rotina": "rotina_fixador", "pnc_joelho_valgo": "pernas_crianca",
}

# Sequências diárias das temporadas (ids '<slug>-<dia>')
TEMPORADA = {"joelho": "joelho", "tornozelo": "esporte", "quadril": "mancando", "coluna": "escoliose",
             "pernas": "pernas_crianca", "fraturas": "fratura_crianca", "reconstrucao": "alongamento",
             "crescimento": "dor_crescimento", "esporte": "esporte", "marcha": "andar", "cotovelo": "cotovelo_baba",
             "socorros": "socorros", "complexos": "outros"}

# Palavras do id (último recurso, na ordem). Casam por TOKEN do id separado por '_' (ou '-'): cada
# token da palavra tem de ser um token do id, na sequência, e o ÚLTIMO pode ser prefixo ('alonga' casa
# 'alongamento'). Nunca substring solta ('cola' não casa 'escola').
PALAVRAS = [("pino", "pinos"), ("retirada", "tempo_tratamento"), ("quanto_tempo", "tempo_tratamento"),
            ("pisar", "tempo_tratamento"), ("fisioterapia", "tempo_tratamento"), ("alonga", "alongamento"),
            ("milimetro", "alongamento"), ("osso_cresce", "alongamento"), ("discrepancia", "discrepancia"),
            ("perna_curta", "discrepancia"), ("medir", "discrepancia"), ("pseudartrose", "consolidacao"),
            ("cola", "consolidacao"), ("osteomielite", "osteomielite"), ("transporte", "trauma_transporte"),
            ("gesso", "gesso_placa"), ("valgo", "pernas_crianca"), ("varo", "pernas_crianca"),
            ("pernas", "pernas_crianca"), ("pe_torto", "pe_torto"),
            ("pe_pra_dentro", "pe_virado"), ("pe_virado", "pe_virado"), ("pe_chato", "pe_chato"),
            ("dor_crescimento", "dor_crescimento"), ("quadril_bebe", "quadril_bebe"), ("displasia", "quadril_bebe"),
            ("ponta", "ponta_pes"), ("manca", "mancando"), ("escoliose", "escoliose"), ("coluna", "escoliose"),
            ("andador", "andar"), ("andar", "andar"), ("esporte", "esporte"), ("joelho", "joelho"),
            ("cotovelo", "cotovelo_baba"), ("rotina", "rotina_fixador"), ("cotidian", "rotina_fixador"),
            ("fixador", "fixador_haste"), ("eixo", "eixo")]


def _tokens(s):
    return [t for t in str(s).lower().replace("-", "_").split("_") if t]


def palavra_casa(palavra, id_):
    """A palavra (um ou mais tokens) aparece no id por TOKEN: tokens iguais em sequência, o último
    podendo ser prefixo do token do id."""
    p, t = _tokens(palavra), _tokens(id_)
    if not p:
        return False
    for i in range(len(t) - len(p) + 1):
        if t[i:i + len(p) - 1] == p[:-1] and t[i + len(p) - 1].startswith(p[-1]):
            return True
    return False


def origem_do_tema(item_ou_id, por_id_extra=None):
    """(tema, origem) com origem em 'campo' | 'por_id' | 'reel_ref' | 'temporada' | 'palavra' | None."""
    item = item_ou_id if isinstance(item_ou_id, dict) else {"id": item_ou_id}
    if item.get("tema") in NOMES:
        return item["tema"], "campo"
    i = str(item.get("id") or "")
    base = i.split("#", 1)[0]                     # partes de story ('stn_x#0') herdam o tema da story
    for mapa in (por_id_extra or {}, POR_ID):
        if base in mapa:
            return mapa[base], "por_id"
    if item.get("reel_ref"):
        t = tema_de(item["reel_ref"], por_id_extra)
        if t:
            return t, "reel_ref"
    slug = base.split("-", 1)[0]
    if "-" in base and slug in TEMPORADA:
        return TEMPORADA[slug], "temporada"
    for palavra, tema in PALAVRAS:
        if palavra_casa(palavra, base):
            return tema, "palavra"
    return None, None


def tema_de(item_ou_id, por_id_extra=None):
    """Chave de tema de um item (dict) ou de um id. None = não classificado."""
    return origem_do_tema(item_ou_id, por_id_extra)[0]


def problemas_de_tema(item, por_id_extra=None):
    """Por que a peça DERIVADA (story) não pode entrar na regra de temas: campo 'tema' presente e fora
    de NOMES, reel de origem sem tema classificável, ou nenhum tema. Lista vazia = classificável."""
    p = []
    sid = item.get("id") or "?"
    if "tema" in item and item.get("tema") not in NOMES:
        p.append(f"{sid}: tema {item.get('tema')!r} não é um tema de temas_conteudo.NOMES (erro de digitação "
                 "seria descartado calado e a peça herdaria só o tema do reel)")
    if item.get("reel_ref") and tema_de(item["reel_ref"], por_id_extra) is None:
        p.append(f"{sid}: o reel de origem {item['reel_ref']!r} não tem tema classificável (ponha em "
                 "temas_conteudo.POR_ID): sem tema a peça fura a distância e passa à frente das outras")
    if not temas_do_item(item, por_id_extra):
        p.append(f"{sid}: sem tema classificável (campo 'tema' ou reel de origem com tema)")
    return p


def temas_do_item(item, por_id_extra=None):
    """Um item derivado pesa pelo PRÓPRIO tema e pelo tema do reel de origem (ele mostra o desenho
    daquele reel): os dois precisam estar longe de aparições recentes."""
    out = {tema_de(item, por_id_extra)}
    if isinstance(item, dict) and item.get("reel_ref"):
        out.add(tema_de(item["reel_ref"], por_id_extra))
    out.discard(None)
    return out


def aparicoes(publicados, fuso, por_id_extra=None):
    """{tema: [datas]} das peças publicadas (data no fuso dado). Peça derivada grava no estado os
    `temas` que ocupa (o próprio e o do reel de onde tira o desenho): todos contam como aparição."""
    out = {}
    for e in publicados:
        if isinstance(e.get("temas"), list) and e["temas"]:
            ts = set(e["temas"])
        elif e.get("kind") in ("story_nova", "carrossel_novo"):
            ts = {tema_de(e.get("story") or e.get("id"), por_id_extra)}
        else:
            ts = {tema_de(e.get("id"), por_id_extra)}
        ts.discard(None)
        if not ts:
            continue
        try:
            d = dt.datetime.fromisoformat(e["at"]).astimezone(fuso).date()
        except (KeyError, ValueError, TypeError):
            continue
        for t in ts:
            out.setdefault(t, []).append(d)
    return out


def conflito(temas, dia, passadas, futuras, n):
    """Motivo do bloqueio (str) ou None. Bloqueia se algum dos temas apareceu há menos de n dias ou
    vai aparecer (agendado) em menos de n dias."""
    for t in sorted(temas):
        for d in passadas.get(t, []):
            if d <= dia and (dia - d).days < n:
                return f"tema '{t}' saiu em {d:%d/%m} (menos de {n} dias)"
        for d in futuras.get(t, []):
            if d >= dia and (d - dia).days < n:
                return f"tema '{t}' está agendado para {d:%d/%m} (menos de {n} dias)"
    return None


def ultima(temas, passadas):
    datas = [d for t in temas for d in passadas.get(t, [])]
    return max(datas) if datas else dt.date.min


def escolher(candidatos, dia, passadas, futuras, n, por_id_extra=None):
    """Entre os candidatos liberados pela distância, o do tema que apareceu há MAIS tempo (empate:
    ordem da fila). Devolve (item, bloqueados[(id, motivo)])."""
    livres, bloqueados = [], []
    for k, it in enumerate(candidatos):
        ts = temas_do_item(it, por_id_extra)
        mot = conflito(ts, dia, passadas, futuras, n)
        if mot:
            bloqueados.append((it.get("id"), mot))
        else:
            livres.append((ultima(ts, passadas), k, it))
    livres.sort(key=lambda x: (x[0], x[1]))
    return (livres[0][2] if livres else None), bloqueados


def _autoteste():
    falhas = []

    def checa(nome, ok):
        print(("OK   " if ok else "FALHA"), nome)
        if not ok:
            falhas.append(nome)

    d = dt.date
    checa("cf_alongamento -> alongamento", tema_de("cf_alongamento") == "alongamento")
    checa("parte de story herda o tema", tema_de("stn_x#1", {"stn_x": "pe_virado"}) == "pe_virado")
    checa("story sem tema herda do reel de origem", tema_de({"id": "stn_y", "reel_ref": "cf_escoliose"}) == "escoliose")
    checa("tema explícito vence", tema_de({"id": "stn_y", "reel_ref": "cf_alongamento", "tema": "tempo_tratamento"}) == "tempo_tratamento")
    checa("sequência de temporada", tema_de("fraturas-qui") == "fratura_crianca")
    checa("item derivado pesa pelos dois temas", temas_do_item({"id": "s", "tema": "tempo_tratamento", "reel_ref": "cf_alongamento"}) == {"tempo_tratamento", "alongamento"})
    pas = {"alongamento": [d(2026, 10, 21), d(2026, 10, 24)], "pe_virado": [d(2026, 10, 28)]}
    fut = {"tempo_tratamento": [d(2026, 11, 22)]}
    checa("CONTROLE: tema que saiu há 3 dias bloqueia", conflito({"alongamento"}, d(2026, 10, 27), pas, fut, 14) is not None)
    checa("tema que saiu há 14 dias libera", conflito({"alongamento"}, d(2026, 11, 7), pas, fut, 14) is None)
    checa("CONTROLE: tema agendado daqui a 10 dias bloqueia", conflito({"tempo_tratamento"}, d(2026, 11, 12), pas, fut, 14) is not None)
    a = {"id": "a", "reel_ref": "cf_pe_virado"}; b = {"id": "b", "reel_ref": "cf_alongamento"}
    it, bl = escolher([a, b], d(2026, 11, 20), pas, {}, 14)
    checa("o tema mais antigo sai primeiro", it is b and bl == [])
    it, bl = escolher([a, b], d(2026, 11, 8), pas, {}, 14)
    checa("CONTROLE: o recente fica bloqueado e o antigo sai", it is b and bl and bl[0][0] == "a")
    # palavra do id por TOKEN (achado 24/10: 'cola' dentro de 'escola')
    checa("palavra por token: 'x_osso_cola_rapido' -> consolidacao", tema_de("x_osso_cola_rapido") == "consolidacao")
    checa("palavra prefixo do token: 'x_crianca_mancando' -> mancando", tema_de("x_crianca_mancando") == "mancando")
    checa("palavra de 2 tokens: 'x_pe_torto_bebe' -> pe_torto", tema_de("x_pe_torto_bebe") == "pe_torto")
    checa("CONTROLE: 'cola' dentro de 'escola' não casa", tema_de("x_volta_escola") is None)
    checa("CONTROLE: 'x_tempe_torto' não casa 'pe_torto' (token inteiro)", not palavra_casa("pe_torto", "x_tempe_torto"))
    checa("CONTROLE: 'rotina' vem antes de 'fixador'", tema_de("x_fixador_rotina") == "rotina_fixador")
    checa("CONTROLE: joelho valgo é perna em X", tema_de("x_joelho_valgo") == "pernas_crianca")
    checa("ids revisados em 24/10", [tema_de(i) for i in ("trabalho_escola", "s_on_fixador_rotina", "pnc_joelho_valgo",
                                                        "vida_cotidiana_fixador")]
          == ["rotina_fixador", "rotina_fixador", "pernas_crianca", "rotina_fixador"])
    checa("origem do tema registrada", origem_do_tema("x_osso_cola_rapido") == ("consolidacao", "palavra")
          and origem_do_tema({"id": "s", "tema": "pinos"}) == ("pinos", "campo"))
    # peça derivada sem tema / com tema inválido (achado 24/10: falhava calado)
    ok = {"id": "stn_y", "reel_ref": "cf_alongamento", "tema": "tempo_tratamento"}
    checa("story com tema válido e reel classificado passa", problemas_de_tema(ok) == [])
    checa("CONTROLE: tema com hífen ('tempo-tratamento') reprova", bool(problemas_de_tema(dict(ok, tema="tempo-tratamento"))))
    checa("CONTROLE: reel de origem sem tema reprova", bool(problemas_de_tema({"id": "stn_z", "reel_ref": "cf_zz_novo", "tema": "pinos"})))
    checa("CONTROLE: sem tema nenhum reprova", bool(problemas_de_tema({"id": "stn_z"})))
    print("\n" + ("AUTOTESTE OK" if not falhas else f"AUTOTESTE: {len(falhas)} FALHA(S)"))
    return 1 if falhas else 0


def _relatorio():
    """Ids da fila (reels/stories) e do estado cujo tema veio por PALAVRA do id (último recurso) ou
    que ficaram sem tema: lista para alguém revisar e pôr em POR_ID. Só informa (exit 0)."""
    import io
    import json
    import os
    raiz = os.path.dirname(os.path.abspath(__file__))

    def ler(nome, padrao):
        try:
            with io.open(os.path.join(raiz, nome), encoding="utf-8-sig") as f:
                return json.load(f)
        except FileNotFoundError:
            return padrao
    itens = [("reels.json", x) for x in ler("reels.json", [])] + [("stories_cf.json", x) for x in ler("stories_cf.json", [])]
    itens += [("published.json", {"id": e.get("story") or e.get("id")}) for e in ler(os.path.join("state", "published.json"),
                                                                                     {}).get("published", [])]
    vistos = set()
    for origem, it in itens:
        if it.get("id") in vistos:
            continue
        vistos.add(it.get("id"))
        tema, como = origem_do_tema(it)
        if como in ("palavra", None):
            print(f"{origem:16s} {it.get('id')!s:34s} {tema or '— sem tema —':18s} ({como or 'não classificado'})")
    return 0


if __name__ == "__main__":
    import argparse
    import sys
    ap = argparse.ArgumentParser(description="Regra de temas: autoteste (padrão) ou relatório de classificação.")
    ap.add_argument("--relatorio", action="store_true", help="lista ids com tema por palavra-chave ou sem tema")
    sys.exit(_relatorio() if ap.parse_args().relatorio else _autoteste())
