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
REEL_WEEKDAYS = {0, 2, 4, 6}
REEL_MIN = 15 * 60
BRT = regra_reels.BRT
formato = regra_reels.formato


def cota_vigente():
    return regra_reels.cota_laminas()


def projeta_reels(fila, published, base, ja_hoje, cota=None, horizonte_dias=730, dias_conversa=None,
                  conversa_ativa=None):
    """[(data, id)] dos reels que vão sair, simulando o publish em cada dia de reel às 15h:
    `fila` = reels.json INTEIRO (na ordem), `published` = state['published'] real. Cada peça
    projetada entra no estado simulado com o formato — exatamente o que o log() do publish grava."""
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
                                           conversa_ativa=conversa_ativa)
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
    teste_stories()
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
