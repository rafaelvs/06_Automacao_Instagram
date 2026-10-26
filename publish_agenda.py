# -*- coding: utf-8 -*-
"""Agenda do publish.py exposta SEM importar o publish (que exige os secrets e aborta sem eles).
Os dias da semana são cópia dos literais do publish.py (teste_agenda confere); a REGRA de qual reel
sai em cada dia NÃO é cópia: é a mesma função do robô (regra_reels.proximo_reel), chamada dia a
dia sobre a fila e o estado reais. Antes havia uma reimplementação aqui, e a cota vinha do
ambiente local enquanto o publish lia a variável do repositório (auditoria 19/10/2026)."""
import datetime as dt
import os
import re

import regra_reels

POST_WEEKDAYS = {1, 3, 5}
POST2_WEEKDAYS = {6}
SEQ_WEEKDAYS = {1, 3, 5}
REEL_WEEKDAYS = {0, 1, 2, 3, 4, 5, 6}    # todo dia abre a janela; o grupo do dia (e se sai reel) é da regra única
REEL_MIN = 15 * 60
BRT = regra_reels.BRT
formato = regra_reels.formato


def cota_vigente():
    return regra_reels.cota_laminas()


def projeta_reels(fila, published, base, ja_hoje, cota=None, horizonte_dias=730, dias_conversa=None,
                  conversa_ativa=None, inicio_novos=None):
    """[(data, id)] dos reels que vão sair, simulando o publish em cada dia de reel às 15h:
    `fila` = reels.json INTEIRO (na ordem), `published` = state['published'] real. Cada peça
    projetada entra no estado simulado com o formato — exatamente o que o log() do publish grava
    (é por ele que o rodízio dos formatos novos sabe qual saiu há mais tempo). O grupo de cada dia
    (COMO FUNCIONA seg/qua/sex/dom, formatos novos ter/qui/sáb a partir de 03/11) é da regra única."""
    cota = cota_vigente() if cota is None else cota
    dias_conversa = regra_reels.dias_entre_conversas() if dias_conversa is None else dias_conversa
    conversa_ativa = regra_reels.conversas_ativas() if conversa_ativa is None else conversa_ativa
    st = {"published": list(published)}
    done = {e["id"] for e in published}
    out = []
    d = base + dt.timedelta(days=1 if ja_hoje else 0)
    fim = base + dt.timedelta(days=horizonte_dias)
    while d <= fim and any(x["id"] not in done for x in fila):
        if d.weekday() in REEL_WEEKDAYS:
            agora = dt.datetime(d.year, d.month, d.day, REEL_MIN // 60, REEL_MIN % 60 + 5, tzinfo=BRT)
            esc = regra_reels.proximo_reel(fila, done, st, agora, cota=cota, dias_conversa=dias_conversa,
                                           conversa_ativa=conversa_ativa, inicio_novos=inicio_novos)
            if esc is not None:
                out.append((d, esc["id"])); done.add(esc["id"])
                st["published"].append({"id": esc["id"], "kind": "reel", "at": agora.isoformat(),
                                        "formato": formato(esc)})
        d += dt.timedelta(days=1)
    return out


STORY_NOVO_WEEKDAYS = {1, 3, 5}           # espelho de publish.STORY_NOVO_WEEKDAYS (teste_agenda confere)
STORY_NOVO_MIN = 12 * 60 + 30


def _aprovacoes_e_reels(aprovacoes, reels_por_id):
    import checar_stories as CS
    raiz = os.path.dirname(os.path.abspath(__file__))
    if aprovacoes is None:
        aprovacoes = CS.carregar(os.path.join(raiz, "aprovacoes.json"), {"lotes": []})
    if reels_por_id is None:
        reels_por_id = {r["id"]: r for r in CS.carregar(os.path.join(raiz, "reels.json"), [])}
    return aprovacoes, reels_por_id


def projeta_stories_detalhe(fila, published, reels_proj, base, ja_hoje, n=None, horizonte_dias=120,
                            aprovacoes=None, reels_por_id=None, portao=None, aprovadas_extra=()):
    """O que o robô vai fazer com os stories da geração nova, dia a dia (ter/qui/sáb às 12:35), com a
    MESMA régua dele (checar_stories: incertas -> retomada -> candidatas -> escolher -> veredito):
      1. parte INCERTA no estado: o robô fica vermelho e nada sai até a conferência -> bloqueio;
      2. story incompleta: retomada só no MESMO dia BRT da 1ª parte (sai o resto); de outro dia =
         'incompleta_expirada': o robô fica vermelho até a decisão humana -> bloqueio;
      3. candidatas: só as APROVADAS com o reel de origem no grid há 2+ dias; as não aprovadas saem
         da conta (listadas em `pendentes`, nunca travam as aprovadas);
      4. escolher: distância entre temas + tema mais antigo;
      5. portão (veredito) da escolhida: aprovada com render/conteúdo quebrado = o robô fica vermelho
         nesse dia e em todo dia seguinte até o conserto -> bloqueio.
    `reels_proj` = saída de projeta_reels (entra como aparição futura e, no dia dela, como reel
    publicado). `portao(st) -> (pode_sair, motivo)` substitui o veredito (testes). `aprovadas_extra`
    = ids tratados como aprovados (hipótese 'se aprovada hoje'; não confere o portão delas).
    -> {'agenda': [(data, id, rótulo)], 'pendentes': [(id, nível, msg)], 'bloqueio': str | None}"""
    import checar_stories as CS
    import temas_conteudo as T
    aprov, reels = _aprovacoes_e_reels(aprovacoes, reels_por_id)
    # hipótese 'se aprovada hoje': a entrada que amarraria o render que está no irmão AGORA (a entrada só de texto
    # não aprova mais — auditoria de fechamento, 25/10) num lote com autor/evidência de mentira, só na memória
    extra_ap = [CS.entrada_hipotetica(s) for s in fila if s.get("id") in set(aprovadas_extra)]
    if extra_ap:
        aprov = {"lotes": list(aprov.get("lotes", [])) + [{"lote": "HIPOTESE", "escopo": [CS.ESCOPO], "status": "aprovado",
                                                          "aprovado_por": "hipótese da página (NÃO é aprovação)",
                                                          "evidencia": "publish_agenda: data em que sairia se aprovada hoje",
                                                          "episodios": extra_ap}]}

    def _portao(st):
        if st.get("id") in set(aprovadas_extra):
            return True, ""
        if portao is not None:
            return portao(st)
        v = CS.veredito(st, aprov, reels)
        return v["pode_sair"], "; ".join(m for _, m in v["erros"][:2])
    extra = {s.get("id"): s.get("tema") for s in fila if s.get("tema")}
    sim = list(published) + [{"id": rid, "kind": "reel", "at": dt.datetime(d.year, d.month, d.day, 15, 5, tzinfo=BRT).isoformat()}
                             for d, rid in reels_proj]
    out = {"agenda": [], "pendentes": [], "bloqueio": None}
    inc = CS.incertas(sim)
    if inc:
        out["bloqueio"] = (f"parte INCERTA de {', '.join(inc)} no estado: o robô fica vermelho e NENHUMA story sai "
                           "até a conferência humana (state/published.json)")
        return out
    vistos_pend = set()
    d = base + dt.timedelta(days=1 if ja_hoje else 0)
    fim = base + dt.timedelta(days=horizonte_dias)
    while d <= fim:
        if d.weekday() in STORY_NOVO_WEEKDAYS:
            at = dt.datetime(d.year, d.month, d.day, 12, 35, tzinfo=BRT).isoformat()
            visto = [e for e in sim if e.get("at", "")[:10] <= d.isoformat()]
            st, situ, det = CS.retomada(fila, visto, d)
            if situ == "incompleta_expirada":
                out["bloqueio"] = f"{d:%d/%m}: {det}. O robô fica vermelho em todo dia de story até a decisão."
                return out
            motivo = "retomada (as partes que faltam)" if situ == "retomada" else None
            if st is None:
                futuras = {}
                for dd, rid in reels_proj:
                    if dd >= d and T.tema_de(rid, extra):
                        futuras.setdefault(T.tema_de(rid, extra), []).append(dd)
                cands, fora = CS.candidatas(fila, visto, aprov, d, reels, detalhar=False)
                for sid, nivel, msg in fora:
                    if (sid, nivel, msg) not in vistos_pend:
                        vistos_pend.add((sid, nivel, msg)); out["pendentes"].append((sid, nivel, msg))
                st, motivo = CS.escolher(cands, visto, d, futuras=futuras, n=n, fila=fila)
            if st is not None:
                pode, porque = _portao(st)
                if not pode:
                    out["bloqueio"] = (f"{d:%d/%m}: `{st['id']}` é a escolhida, mas o portão BARRA ({porque}) — o robô "
                                       "fica vermelho nesse dia e nos seguintes até o conserto (re-render no CI)")
                    return out
                feitas = CS.partes_publicadas(sim).get(st["id"], {})
                out["agenda"].append((d, st["id"], motivo))
                sim += [{"id": f"{st['id']}#{i}", "kind": "story_nova", "story": st["id"], "parte": i, "at": at,
                         "temas": sorted(T.temas_do_item(st, extra))} for i in range(len(CS.PAPEIS)) if i not in feitas]
        d += dt.timedelta(days=1)
    return out


def projeta_stories(fila, published, reels_proj, base, ja_hoje, n=None, horizonte_dias=120, aprovacoes=None,
                    reels_por_id=None):
    """[(data, id)] dos stories que o robô vai publicar (ver projeta_stories_detalhe: pendentes fora
    da conta, retomada só no mesmo dia, incerta/expirada/portão barrando = nada depois)."""
    r = projeta_stories_detalhe(fila, published, reels_proj, base, ja_hoje, n=n, horizonte_dias=horizonte_dias,
                                aprovacoes=aprovacoes, reels_por_id=reels_por_id)
    return [(d, i) for d, i, _ in r["agenda"]]


def teste_agenda():
    """Confere (1) os dias da semana contra os literais do publish.py; (2) que o publish usa a
    regra única e que o publish.yml não sobrescreve a cota por variável; (3) a simulação contra
    um caso calculado à mão, incluindo id repetido e peça nova publicada fora da fila."""
    raiz = os.path.dirname(os.path.abspath(__file__))
    src = open(os.path.join(raiz, "publish.py"), encoding="utf-8").read()
    for nome, val in (("POST_WEEKDAYS", POST_WEEKDAYS), ("POST2_WEEKDAYS", POST2_WEEKDAYS),
                      ("SEQ_WEEKDAYS", SEQ_WEEKDAYS), ("REEL_WEEKDAYS", REEL_WEEKDAYS)):
        m = re.search(nome + r"\s*=\s*\{([^}]*)\}", src)
        assert m, nome
        assert {int(x) for x in m.group(1).split(",")} == val, f"{nome} divergente do publish.py"
    m = re.search(r"REEL_MIN\s*=\s*(\d+)\s*\*\s*60", src)
    assert m and int(m.group(1)) * 60 == REEL_MIN, "REEL_MIN divergente do publish.py"
    assert "STORY_NOVO_WEEKDAYS = {1, 3, 5}" in src and "STORY_NOVO_MIN = 12*60 + 30" in src, \
        "dias/horário de story nova divergem entre publish.py e publish_agenda.py"
    assert "regra_reels.posts_ativos()" in src and "regra_reels.sequencias_ativas()" in src, \
        "publish.py deixou de ler a suspensão de carrossel/sequência da regra única"
    assert "regra_reels.proximo_reel(" in src and "regra_reels.cota_laminas()" in src \
        and "regra_reels.dias_entre_conversas()" in src and "regra_reels.conversas_ativas()" in src, \
        "publish.py deixou de usar a regra única (regra_reels)"
    yml = open(os.path.join(raiz, ".github", "workflows", "publish.yml"), encoding="utf-8").read()
    for var in ("LAMINAS_POR_SEMANA", "DIAS_ENTRE_CONVERSAS", "CONVERSAS_ATIVAS", "POSTS_ATIVOS", "SEQUENCIAS_ATIVAS",
                "STORIES_NOVOS_ATIVOS", "DIAS_ENTRE_MESMO_TEMA"):
        assert not re.search(r"^\s*" + var + r"\s*:", yml, re.M), \
            f"publish.yml voltou a definir {var} — a página leria outra cota que o robô"
    seg = dt.date(2026, 10, 19)
    l1, l2, c1 = {"id": "l1"}, {"id": "l2"}, {"id": "c1", "formato": "conversa"}
    # 2 lâminas + 1 conversa a partir de uma segunda, cota 1: seg l1, qua c1, sex/dom nada, seg seguinte l2
    r = projeta_reels([l1, l2, c1], [], seg, False, cota=1, conversa_ativa=True)
    assert r == [(seg, "l1"), (seg + dt.timedelta(days=2), "c1"), (seg + dt.timedelta(days=7), "l2")], r
    # id repetido na fila: sai uma vez só (o publish só publica uma vez)
    r = projeta_reels([c1, l1, dict(c1)], [], seg, False, cota=1, conversa_ativa=True)
    assert [i for _, i in r] == ["c1", "l1"], r
    # conversa publicada na segunda e JÁ FORA da fila: não conta como lâmina (formato no registro)
    pub = [{"id": "c0", "kind": "reel", "at": "2026-10-19T15:05:00-03:00", "formato": "conversa"}]
    r = projeta_reels([l1], pub, seg, True, cota=1, conversa_ativa=True)
    assert r == [(seg + dt.timedelta(days=2), "l1")], r
    # conversa: só 10 dias depois da anterior (19/10). Fila c1 c2 f1 f2 f3 a partir de segunda:
    # seg c1, qua f1, sex f2, dom f3; seg+7 ainda não pode; c2 no 1º dia de reel a partir de +10 (sex, +11)
    c2 = {"id": "c2", "formato": "conversa"}
    f1, f2, f3 = ({"id": f"f{k}", "formato": "como_funciona"} for k in (1, 2, 3))
    r = projeta_reels([c1, c2, f1, f2, f3], [], seg, False, cota=1, dias_conversa=10, conversa_ativa=True)
    assert [(d - seg).days for d, _ in r] == [0, 2, 4, 6, 11] and [i for _, i in r] == ["c1", "f1", "f2", "f3", "c2"], r
    # ALL-IN (24/10): padrão = lâmina 0 e conversa desligada -> só COMO FUNCIONA sai, um por dia de reel
    r = projeta_reels([l1, c1, f1, c2, f2], [], seg, False, cota=0, conversa_ativa=False)
    assert [i for _, i in r] == ["f1", "f2"] and [(d - seg).days for d, _ in r] == [0, 2], r
    # cota 0 = lâminas suspensas: nada sai, e a projeção fica vazia (o gerador tem de avisar)
    assert projeta_reels([l1], [], seg, False, cota=0, horizonte_dias=30) == []
    teste_formatos_novos(src, yml)
    teste_stories()
    return True


def teste_formatos_novos(src=None, yml=None):
    """FORMATOS NOVOS (Rafael, 24-26/10/2026): ter/qui/sáb a partir de 03/11, em rodízio (o publicado há mais tempo;
    nunca publicado primeiro; empate = ordem da fila; dentro do formato, o 1º da fila); seg/qua/sex/dom só COMO
    FUNCIONA. A página (projeta_reels) e o reordenador (ordenar_fila_temas) usam a mesma regra do robô."""
    raiz = os.path.dirname(os.path.abspath(__file__))
    if src is None:
        src = open(os.path.join(raiz, "publish.py"), encoding="utf-8").read()
    if yml is None:
        yml = open(os.path.join(raiz, ".github", "workflows", "publish.yml"), encoding="utf-8").read()
    assert "regra_reels.grupo_do_dia(" in src, "publish.py deixou de explicar o dia sem reel pelo grupo da regra única"
    assert set(regra_reels.DIAS_COMO_FUNCIONA) | set(regra_reels.DIAS_FORMATOS_NOVOS) == REEL_WEEKDAYS \
        and not set(regra_reels.DIAS_COMO_FUNCIONA) & set(regra_reels.DIAS_FORMATOS_NOVOS), "grupos de dias furados"
    # os crons DEDICADOS das 15h BRT (18 UTC) cobrem os 7 dias: os de ter/qui/sáb são os do antigo carrossel (POSTS).
    # O catch-all (hora '*') não conta: é reserva, não a janela
    dias_18 = set()
    for m in re.finditer(r'cron:\s*"([^"]+)"', yml):
        mi, h, _, _, dow = m.group(1).split()
        if h == "18":
            dias_18 |= set(range(7)) if dow == "*" else {int(x) % 7 for x in dow.split(",")}
    assert dias_18 >= set(range(7)), f"publish.yml sem cron às 15h BRT em algum dia de reel: {sorted(dias_18)}"
    ter27, seg02, ter03 = dt.date(2026, 10, 27), dt.date(2026, 11, 2), dt.date(2026, 11, 3)
    assert regra_reels.INICIO_FORMATOS_NOVOS == ter03 and ter03.weekday() == 1
    novo = lambda i, f: {"id": i, "formato": f}                     # noqa: E731
    q1, q2 = novo("q1", "qual_dos_dois"), novo("q2", "qual_dos_dois")
    m1, m2 = novo("m1", "mito_na_prova"), novo("m2", "mito_na_prova")
    k1, v1 = novo("k1", "camera_lenta"), novo("v1", "chama_o_var")
    f1, f2, f3 = ({"id": f"cf{k}", "formato": "como_funciona"} for k in (1, 2, 3))
    # antes de 03/11 ter/qui/sáb ficam sem reel; o 1º formato novo sai na terça 03/11
    r = projeta_reels([q1], [], ter27, False, horizonte_dias=30)
    assert r == [(ter03, "q1")], ("antes de 03/11 nada de formato novo", r)
    # rodízio sem nada publicado: nunca publicado primeiro, empate pela ordem da fila; depois, o mais antigo
    r = projeta_reels([m1, q1, k1, q2, v1, m2], [], ter03, False, horizonte_dias=30)
    assert [i for _, i in r] == ["m1", "q1", "k1", "v1", "m2", "q2"] \
        and [(d - ter03).days for d, _ in r] == [0, 2, 4, 7, 9, 11], ("rodízio", r)
    # seg/qua/sex/dom NUNCA formato novo, e COMO FUNCIONA nunca ocupa ter/qui/sáb
    assert all(d.weekday() in regra_reels.DIAS_FORMATOS_NOVOS for d, _ in r), r
    r = projeta_reels([f1, f2, f3], [], ter03, False, horizonte_dias=10)
    assert [d.weekday() for d, _ in r] == [2, 4, 6], ("COMO FUNCIONA só seg/qua/sex/dom", r)
    r = projeta_reels([q1, f1, m1, f2], [], seg02, False, horizonte_dias=10)
    assert r == [(seg02, "cf1"), (ter03, "q1"), (seg02 + dt.timedelta(days=2), "cf2"),
                 (seg02 + dt.timedelta(days=3), "m1")], ("intercalado", r)
    # o REGISTRO manda: câmera lenta publicada ontem (FORCE numa segunda) e qual dos dois em 20/10 -> a vaga de
    # terça é do qual dos dois, mesmo atrás na fila; a de quinta, da câmera lenta
    pub = [{"id": "k0", "kind": "reel", "at": "2026-11-02T18:05:00+00:00", "formato": "camera_lenta"},
           {"id": "q0", "kind": "reel", "at": "2026-10-20T18:05:00+00:00", "formato": "qual_dos_dois"}]
    r = projeta_reels([k1, q1], pub, ter03, False, horizonte_dias=3)
    assert r == [(ter03, "q1"), (ter03 + dt.timedelta(days=2), "k1")], ("formato mais antigo primeiro", r)
    # reel incerto do formato conta como aparição (pode estar no ar)
    pub_inc = [{"id": "q0", "kind": "reel_incerto", "at": "2026-11-02T18:05:00+00:00"}]
    r = projeta_reels([novo("q0", "qual_dos_dois"), q1, m1], pub_inc, ter03, False, horizonte_dias=1)
    assert r == [(ter03, "m1")], ("reel_incerto conta no rodízio", r)
    # reordenador: só dentro do grupo de dias, e a distância de tema vale entre TODOS os reels e stories
    import ordenar_fila_temas as O
    fa = {"id": "cf_alongamento", "formato": "como_funciona"}                       # tema alongamento
    fb = {"id": "cf_pe_virado", "formato": "como_funciona"}                         # tema pe_virado
    qa = {"id": "qd_x", "formato": "qual_dos_dois", "tema": "alongamento"}
    qb = {"id": "qd_y", "formato": "qual_dos_dois", "tema": "pe_chato"}
    mb = {"id": "mp_x", "formato": "mito_na_prova", "tema": "pinos"}
    story = [{"id": "stn_z#0", "kind": "story_nova", "story": "stn_z", "at": "2026-10-31T15:35:00+00:00",
              "temas": ["alongamento"]},
             {"id": "stn_w#0", "kind": "story_nova", "story": "stn_w", "at": "2026-10-29T15:35:00+00:00",
              "temas": ["pe_chato"]}]
    fila = [fa, qa, qb, mb, fb]
    regra = dict(cota=0, conversa_ativa=False)
    res = O.reordenar(fila, story, seg02, False, seg02 - dt.timedelta(days=1), 14, **regra)
    # seg 02/11: cf_alongamento conflita com a STORY de 31/10 (alongamento) -> sai cf_pe_virado; o mito (pinos, livre)
    #   está antes na fila mas é de OUTRO grupo de dias: não ocupa segunda;
    # ter 03/11: qual dos dois (nunca publicado, 1º da fila) — qd_x (alongamento, story de 31/10) e qd_y (pe_chato,
    #   story de 29/10) conflitam; sai o tema que apareceu há MAIS tempo (pe_chato);
    # qua 04/11: só sobra cf_alongamento (conflita) -> sai mesmo assim (tema nunca deixa dia sem reel);
    # qui 05/11: mito (nunca publicado) -> mp_x; sáb 07/11: qual -> qd_x
    assert [i for _, i in res["nova"]] == ["cf_pe_virado", "qd_y", "cf_alongamento", "mp_x", "qd_x"], res["nova"]
    # vagas de COMO FUNCIONA continuam de COMO FUNCIONA (0 e 4); cada formato novo, nas posições DELE (qual 1 e 2,
    # mito 3), na ordem de saída
    assert [x["id"] for x in res["fila"]] == ["cf_pe_virado", "qd_y", "qd_x", "mp_x", "cf_alongamento"], \
        ("reordena só dentro do grupo e, nos formatos novos, dentro do formato", res["fila"])
    depois = projeta_reels(res["fila"], story, seg02, False, **regra)
    assert depois == res["nova"], ("a fila reordenada projeta exatamente a proposta", depois, res["nova"])
    assert res["confere"] and res["depois"] == depois, res
    teste_reordenador_fixos(regra)
    return True


def teste_reordenador_fixos(regra):
    """--fixar-ate cobrindo vagas de FORMATO NOVO, com 2+ peças por formato (verificação de 26/10/2026): os fixos ficam
    nas datas deles. Antes, a cauda era escrita nas posições de sempre e uma peça de outro formato caía ANTES de um fixo
    na fila: o desempate do rodízio (posição do 1º pendente) trocava o formato de uma data FIXADA — e o --gravar
    gravava o reels.json antes de conferir. Agora a fila nova é conferida ANTES de gravar; divergiu = nada gravado."""
    import contextlib
    import hashlib
    import io
    import json
    import shutil
    import sys
    import tempfile
    import ordenar_fila_temas as O
    seg26, ter03, qui05, sab07 = dt.date(2026, 10, 26), dt.date(2026, 11, 3), dt.date(2026, 11, 5), dt.date(2026, 11, 7)
    n_ = lambda i, f, t: {"id": i, "formato": f, "tema": t}         # noqa: E731
    # o caso real da verificação: câmera lenta x2, mito x3 e o qual dos dois no FIM da fila (temas todos diferentes)
    fila = [n_("cf_a", "como_funciona", "alongamento"), n_("cam_a", "camera_lenta", "pe_torto"),
            n_("cam_b", "camera_lenta", "joelho"), n_("mito_a", "mito_na_prova", "pinos"),
            n_("mito_b", "mito_na_prova", "escoliose"), n_("mito_c", "mito_na_prova", "fratura"),
            n_("qual_a", "qual_dos_dois", "pe_chato"), n_("cf_b", "como_funciona", "pe_virado")]
    antes = projeta_reels(fila, [], seg26, False, **regra)
    fix = [(d, i) for d, i in antes if d <= qui05]
    assert (ter03, "cam_a") in fix and (qui05, "mito_a") in fix and (sab07, "qual_a") in antes, antes
    res = O.reordenar(fila, [], seg26, False, qui05, 14, **regra)
    assert res["confere"], ("a fila nova tem de projetar os fixos + a proposta", res["depois"], fix + res["nova"])
    assert [x for x in res["depois"] if x[0] <= qui05] == fix, ("fixos mudaram de data", res["depois"], fix)
    assert res["nova"][0] == (sab07, "qual_a"), res["nova"]
    # lâmina religada (cota 1/semana): l2 está ANTES do COMO FUNCIONA fixo de quarta na fila, mas a cota a segura até a
    # segunda seguinte. Escrita nas posições de sempre, a cauda punha cf_y na vaga de l2 — à frente de cf_x — e cf_y
    # roubava a quarta FIXADA. Com os fixos à frente da classe, a quarta continua de cf_x
    qua28 = seg26 + dt.timedelta(days=2)
    fl = [n_("l1", "", "gesso"), n_("l2", "", "pinos"), n_("cf_x", "como_funciona", "pe_torto"),
          n_("cf_y", "como_funciona", "joelho")]
    regra_l = dict(cota=1, conversa_ativa=False)
    a0 = projeta_reels(fl, [], seg26, False, **regra_l)
    assert a0 == [(seg26, "l1"), (qua28, "cf_x"), (seg26 + dt.timedelta(days=4), "cf_y"),
                  (seg26 + dt.timedelta(days=7), "l2")], a0
    r = O.reordenar(fl, [], seg26, False, qua28, 14, **regra_l)
    assert r["confere"] and r["depois"][:2] == a0[:2], ("fixo de COMO FUNCIONA atrás de lâmina presa pela cota", r)
    # fuzz pequeno e determinístico: 2-3 peças por formato, fixar de 02/11 a 12/11, registro com formatos novos já
    # publicados (inclusive DOIS no mesmo dia: empate no rodízio, decidido pela posição na fila). Em todo caso: a fila
    # nova projeta a proposta, os fixos não mudam de data, as datas de cada grupo são as mesmas e a SEQUÊNCIA de
    # formatos novos é a da fila original (o reordenador só escolhe QUAL peça do formato sai)
    import random
    rng = random.Random(26)
    temas = ["alongamento", "pinos", "pe_chato", "pe_torto", "escoliose", "joelho", "fratura", "gesso"]
    for caso in range(150):
        fl = [n_(f"x{k}", rng.choice(["como_funciona"] * 2 + list(regra_reels.FORMATOS_NOVOS)), rng.choice(temas))
              for k in range(rng.randint(6, 14))]
        pub_ = []
        for k in range(rng.randint(0, 4)):
            dia = dt.date(2026, 10, 20) + dt.timedelta(days=rng.choice([0, 0, 2, 4]))     # repete o dia: empates
            pub_.append({"id": f"p{k}", "kind": "reel", "at": f"{dia.isoformat()}T18:05:00+00:00",
                         "formato": rng.choice(list(regra_reels.FORMATOS_NOVOS)), "temas": [rng.choice(temas)]})
        fixar = dt.date(2026, 11, 2) + dt.timedelta(days=rng.randint(0, 10))
        r = O.reordenar(fl, pub_, seg26, False, fixar, 14, **regra)
        a0 = projeta_reels(fl, pub_, seg26, False, **regra)
        fmt_ = {x["id"]: x["formato"] for x in fl}
        fixos_ok = [x for x in r["depois"] if x[0] <= fixar] == [x for x in a0 if x[0] <= fixar]
        datas_ok = sorted(d for d, _ in r["depois"]) == sorted(d for d, _ in a0)
        seq_ok = [(d, fmt_[i]) for d, i in r["depois"] if fmt_[i] in regra_reels.FORMATOS_NOVOS] == \
            [(d, fmt_[i]) for d, i in a0 if fmt_[i] in regra_reels.FORMATOS_NOVOS]
        assert r["confere"] and fixos_ok and datas_ok and seq_ok, \
            ("fuzz do reordenador", caso, fixar, fixos_ok, datas_ok, seq_ok, fl, pub_, a0, r["depois"])
    # --gravar com a projeção divergindo: aborta ANTES de abrir o reels.json (o arquivo fica byte a byte igual)
    tmp = tempfile.mkdtemp(prefix="reordenar_")
    try:
        os.makedirs(os.path.join(tmp, "state"))
        arq = os.path.join(tmp, "reels.json")
        with open(arq, "w", encoding="utf-8") as f:
            json.dump(fila, f)
        with open(os.path.join(tmp, "state", "published.json"), "w", encoding="utf-8") as f:
            json.dump({"published": [], "last_reel_date": ""}, f)
        md5 = hashlib.md5(open(arq, "rb").read()).hexdigest()
        real = O.reordenar
        salvo = (O.ROOT, O.reordenar, sys.argv)
        O.ROOT = tmp
        O.reordenar = lambda *a, **k: dict(real(*a, **k), fila=list(reversed(fila)), confere=False)
        sys.argv = ["ordenar_fila_temas.py", "--fixar-ate", "2026-11-05", "--hoje", "2026-10-26", "--gravar"]
        saida = io.TextIOWrapper(io.BytesIO(), encoding="utf-8")      # o main() faz stdout.reconfigure
        try:
            with contextlib.redirect_stdout(saida):
                O.main()
            abortou = False
        except SystemExit as e:
            abortou = e.code == 1
        except Exception:                                            # noqa: BLE001 — gravou e só depois quebrou
            abortou = False
        finally:
            O.ROOT, O.reordenar, sys.argv = salvo
        saida.flush()
        msg = saida.buffer.getvalue().decode("utf-8")
        assert abortou and "INTOCADO" in msg and hashlib.md5(open(arq, "rb").read()).hexdigest() == md5, \
            ("--gravar com projeção divergente tem de abortar SEM tocar no reels.json", msg[-300:])
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    return True


def teste_stories():
    """A projeção dos stories espelha o robô (achados de 24/10): pendente de tema antigo não trava a
    aprovada; retomada só no mesmo dia; incerta/expirada/portão barrando = bloqueio; reel trial ou de
    ontem não libera a story."""
    import checar_stories as CS

    def story(sid, reel, tema):
        tela = lambda p, tx, t0: {"papel": p, "titulo": ["LINHA UM", "LINHA DOIS"], "texto": tx,  # noqa: E731
                                  "trecho": [t0, t0 + 1.0], "crop": [0, 0, 100, 100]}
        return {"id": sid, "reel_ref": reel, "tema": tema, "angulo": "a", "variante": "A", "cta": "Manda pra quem precisa.",
                "telas": [tela("espanto", "", 1.0), tela("mecanismo", "Texto.", 3.0), tela("significado", "Texto.", 5.0)]}

    def aprova(*sts):
        # a entrada que aprova (hash do texto + vídeos + gerador) num lote com autor/evidência; sem irmão
        # (stories de teste) os vídeos não se conferem e o portão real barra pelo render (ver o último caso)
        return {"lotes": [{"lote": "T", "escopo": [CS.ESCOPO], "status": "aprovado", "aprovado_por": "teste_stories",
                           "evidencia": "teste_stories: aprovação simulada",
                           "episodios": [{"id": s["id"], "hash_roteiro": CS.hash_story(s), "videos": ["sha256:t"] * 3,
                                          "hash_gerador": "sha256:t"} for s in sts]}]}
    livre = lambda st: (True, "")          # noqa: E731  (portão isolado: aqui só a agenda)
    sa = story("stn_ta", "cf_pe_virado", "pe_virado")             # PENDENTE e de tema mais antigo
    sb = story("stn_tb", "cf_alongamento", "tempo_tratamento")    # APROVADA
    pub = [{"id": "cf_pe_virado", "kind": "reel", "at": "2026-09-01T18:00:00+00:00"},
           {"id": "cf_alongamento", "kind": "reel", "at": "2026-10-01T18:00:00+00:00"}]
    ter = dt.date(2026, 11, 17)

    def proj(fila, pub_, aprov, **kw):
        kw.setdefault("portao", livre)
        r = projeta_stories_detalhe(fila, pub_, [], ter, False, n=kw.pop("n", 14), aprovacoes=aprov, reels_por_id={},
                                    horizonte_dias=kw.pop("horizonte_dias", 10), **kw)
        return r, [(d, i) for d, i, _ in r["agenda"]]
    r, ag = proj([sa, sb], pub, aprova(sb))
    assert ag == [(ter, "stn_tb")], ("pendente de tema antigo travou a aprovada", r)
    assert any(i == "stn_ta" and nv == "aviso" for i, nv, _ in r["pendentes"]) and r["bloqueio"] is None, r
    so_texto = {"lotes": [dict(aprova(sb)["lotes"][0], episodios=[{"id": sb["id"], "hash_roteiro": CS.hash_story(sb)}])]}
    r, ag = proj([sa, sb], pub, so_texto)
    assert ag == [] and any(i == "stn_tb" and nv == "aviso" for i, nv, _ in r["pendentes"]), \
        ("entrada só de texto NÃO aprova: a página não projeta (= robô)", r)
    _, ag = proj([sa, sb], pub, aprova(sb), aprovadas_extra=("stn_ta",))
    assert ag == [(ter, "stn_ta"), (ter + dt.timedelta(days=2), "stn_tb")], ("hipótese 'se aprovada hoje'", ag)
    # retomada: só no MESMO dia BRT da 1ª parte
    p0 = {"id": "stn_tb#0", "kind": "story_nova", "story": "stn_tb", "parte": 0, "media_id": "M", "at": "2026-11-17T15:40:00+00:00"}
    r, ag = proj([sa, sb], pub + [p0], aprova(sb))
    assert ag == [(ter, "stn_tb")] and r["agenda"][0][2].startswith("retomada") and r["bloqueio"] is None, r
    r, ag = proj([sa, sb], pub + [dict(p0, at="2026-11-14T15:40:00+00:00")], aprova(sb))
    assert ag == [] and r["bloqueio"] and "expirou" in r["bloqueio"], ("retomada de outro dia tem de bloquear", r)
    inc = {"id": "stn_tb#1", "kind": "story_nova_incerta", "story": "stn_tb", "parte": 1, "media_id": None,
           "at": "2026-11-17T15:40:00+00:00"}
    r, ag = proj([sa, sb], pub + [p0, inc], aprova(sb))
    assert ag == [] and r["bloqueio"] and "INCERTA" in r["bloqueio"], ("parte incerta tem de bloquear", r)
    # calendário: reel de ontem não libera (nem com a distância de tema desligada); trial não conta
    pub_seg = [{"id": "cf_alongamento", "kind": "reel", "at": "2026-11-16T18:05:00+00:00"}]
    _, ag = proj([sb], pub_seg, aprova(sb), n=-1)
    assert ag == [(ter + dt.timedelta(days=2), "stn_tb")], ("2 dias depois do reel", ag)
    _, ag = proj([sb], [dict(pub_seg[0], modo_reel="trial")], aprova(sb), n=-1)
    assert ag == [], ("reel em modo trial não é 'no perfil'", ag)
    # portão de verdade (veredito): aprovada sem render = o robô fica vermelho -> bloqueio, nada depois
    r = projeta_stories_detalhe([sb], pub, [], ter, False, n=14, aprovacoes=aprova(sb), reels_por_id={}, horizonte_dias=10)
    assert r["agenda"] == [] and r["bloqueio"] and "portão BARRA" in r["bloqueio"], ("portão barrando", r)
    assert projeta_stories([sa, sb], pub, [], ter, False, n=14, aprovacoes=aprova(), reels_por_id={}, horizonte_dias=10) == [], \
        "sem aprovação nenhuma, nada é projetado"
    return True


if __name__ == "__main__":
    print("agenda confere com publish.py:", teste_agenda())
