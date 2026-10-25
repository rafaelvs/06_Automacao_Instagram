# -*- coding: utf-8 -*-
"""Publicação de um story em VÁRIAS PARTES sem duplicar (geração nova, 24/10/2026).

Por que existe: a sequência antiga publicava tela por tela com `wait_finished` (que devolve True
mesmo sem o contêiner ficar pronto) e só gravava o estado no FIM. Em 16 de 59 dias isso duplicou
quadros: o job morria no meio (timeout de 15 min, push perdido) e o run seguinte republicava o
bloco inteiro. Aqui:

  1. Todos os contêineres das partes pendentes são criados primeiro e esperados JUNTOS, com prazo
     total. Contêiner em ERROR/EXPIRED ou prazo estourado = falha ALTA sem publicar nada.
  2. WRITE-AHEAD: antes de cada `media_publish`, o contêiner da parte é gravado e salvo em disco
     (`antes_de_publicar`). Job que morre DENTRO da chamada (timeout, cancelamento, runner perdido)
     deixa o rastro: o run seguinte pergunta ao contêiner (`resolver_publicando`) antes de criar
     outro — PUBLISHED = a parte saiu (registra), FINISHED = não saiu (reaproveita o MESMO contêiner:
     contêiner só publica uma vez), EXPIRED = nunca saiu (a Meta só expira contêiner não publicado),
     o resto = INCERTO.
  3. Cada `media_publish` que dá certo é gravado no estado E salvo em disco na hora (`registrar`),
     antes da próxima parte. Job que morre depois disso não republica a parte.
  4. Erro no `media_publish` NÃO é tratado como "não saiu" — NENHUM, nem o "fatal" (token): a Meta
     já entregou post com resposta de erro (lição da casa: HTTP 500 da Meta ENTREGA) e um 500
     transitório já foi classificado como token morto (auditoria 24/10). Pergunta-se ao contêiner
     (`status_code`): PUBLISHED = saiu (registra); FINISHED = não saiu por ora (o write-ahead fica e
     o próximo run pergunta de novo); qualquer outra coisa, ou a consulta falhando = INCERTO: registra
     como incerto e só então levanta — a story fica bloqueada até alguém conferir no app (duplicar no
     ar é pior que faltar uma parte).
  5. Antes de criar contêiner, o publish confere a CONTA (`stories_desconhecidas`, GET /stories): story
     de hoje que o estado não conhece = outro run publicou com o estado velho; nada sai.
  6. Depois de publicar, cada media_id é conferido com GET (job verde ≠ post no ar).

Módulo sem rede própria: recebe `api_post`/`api_get` do publish.py (e dublês nos testes).
"""
import datetime as dt
import re
import time

STATUS_RUINS = ("ERROR", "EXPIRED")


class StoryIncerta(RuntimeError):
    """Uma parte pode ou não ter ido ao ar: a story fica bloqueada até conferência humana."""


def criar_conteiner(parte, ig_user, api_post, raw_url, extra=None):
    dados = {"media_type": "STORIES"}
    if parte.get("tipo", "video") == "video":
        dados["video_url"] = raw_url(parte["arquivo"])
    else:
        dados["image_url"] = raw_url(parte["arquivo"])
    dados.update(extra or {})
    return api_post(f"{ig_user}/media", dados)["id"]


def esperar_todos(conts, api_get, prazo_s, espera_s, rotulo, sleep=time.sleep, relogio=time.monotonic):
    """Espera TODOS os contêineres ficarem FINISHED dentro de um prazo total."""
    fim = relogio() + prazo_s
    prontos = set()
    while True:
        for i, c in conts.items():
            if i in prontos:
                continue
            st = (api_get(c, {"fields": "status_code"}) or {}).get("status_code")
            if st == "FINISHED":
                prontos.add(i)
            elif st in STATUS_RUINS:
                raise RuntimeError(f"{rotulo} parte {i + 1}: contêiner {c} em {st} — nada publicado neste run")
        if len(prontos) == len(conts):
            return
        if relogio() > fim:
            faltam = sorted(i + 1 for i in conts if i not in prontos)
            raise RuntimeError(f"{rotulo}: prazo de {prazo_s}s estourado esperando as partes {faltam} — "
                               "nada publicado neste run")
        sleep(espera_s)


def publicar_partes(story_id, partes, ja_publicadas, *, ig_user, api_post, api_get, raw_url,
                    registrar, antes_de_publicar=None, conteineres=None, erros_fatais=(), prazo_s=480,
                    espera_s=8, extra=None, sleep=time.sleep, relogio=time.monotonic):
    """Publica as partes que faltam de `story_id`, na ordem.

    ja_publicadas: {indice: media_id} do estado (retomada).
    conteineres: {indice: contêiner} de um run anterior, conferido FINISHED (write-ahead): reaproveitado
        em vez de criar outro.
    antes_de_publicar(indice, contêiner): write-ahead — grava e salva em disco ANTES do media_publish.
    registrar(indice, media_id, info): grava no estado e salva em disco ANTES de seguir.
    erros_fatais: exceções que param o run (ex.: AuthError do token morto) — sobem DEPOIS da consulta
        ao contêiner, nunca antes.
    Devolve [(indice, media_id)] do que saiu neste run. Falha = exceção (nunca silêncio)."""
    pend = [i for i in range(len(partes)) if i not in ja_publicadas]
    if not pend:
        return []
    rotulo = f"story {story_id}"
    prev = {i: c for i, c in (conteineres or {}).items() if i in pend and c}
    conts = {i: (prev[i] if i in prev else criar_conteiner(partes[i], ig_user, api_post, raw_url, extra)) for i in pend}
    esperar_todos(conts, api_get, prazo_s, espera_s, rotulo, sleep=sleep, relogio=relogio)
    saiu = []
    for i in pend:
        if antes_de_publicar is not None:
            antes_de_publicar(i, conts[i])
        try:
            mid = (api_post(f"{ig_user}/media_publish", {"creation_id": conts[i]}) or {}).get("id")
            if not mid:
                raise RuntimeError("media_publish sem id na resposta")
        except Exception as e:                                  # noqa: BLE001 — inclusive os fatais: decide pelo contêiner
            fatal = bool(erros_fatais) and isinstance(e, erros_fatais)
            erro_consulta = None
            try:
                st = (api_get(conts[i], {"fields": "status_code"}) or {}).get("status_code")
            except Exception as e2:                             # noqa: BLE001
                st, erro_consulta = None, e2
            if st == "PUBLISHED":
                registrar(i, None, {"container": conts[i], "confirmado_por": "status_code PUBLISHED depois de erro"})
                saiu.append((i, None))
                if fatal:
                    raise e                                     # a parte que saiu está gravada; o resto espera o humano
                continue
            if st == "FINISHED":
                if fatal:
                    raise e
                raise RuntimeError(f"{rotulo} parte {i + 1}: media_publish falhou ({e}); contêiner FINISHED = não "
                                   "saiu (por ora). Partes anteriores registradas; o próximo run pergunta de novo ao "
                                   "contêiner (write-ahead) antes de criar outro.") from e
            info = {"container": conts[i], "incerto": True, "erro": str(e)[:200], "status": st}
            if erro_consulta is not None:
                info["erro_consulta"] = str(erro_consulta)[:200]
            registrar(i, None, info)
            if fatal:
                raise e
            if erro_consulta is not None and erros_fatais and isinstance(erro_consulta, erros_fatais):
                raise erro_consulta from e
            raise StoryIncerta(f"{rotulo} parte {i + 1}: media_publish falhou ({e}) e o contêiner está {st!r}"
                               + (f" (consulta falhou: {erro_consulta})" if erro_consulta is not None else "")
                               + " — pode ter ido ao ar. Story BLOQUEADA até conferir no app.") from e
        registrar(i, mid, {"container": conts[i]})
        saiu.append((i, mid))
        sleep(2)
    return saiu


def resolver_publicando(entrada, api_get):
    """Write-ahead que um run anterior deixou (job morto no meio do media_publish, ou erro com o contêiner
    FINISHED). -> (decisão, status): 'publicada' (PUBLISHED: a parte saiu), 'reusar' (FINISHED: não saiu,
    o contêiner ainda serve), 'descartar' (EXPIRED: a Meta só expira contêiner NÃO publicado em 24 h),
    'incerta' (qualquer outro status ou sem contêiner). Exceção da consulta SOBE: sem resposta, o chamador
    não decide nada (e não publica)."""
    c = (entrada or {}).get("container")
    if not c:
        return "incerta", None
    st = (api_get(c, {"fields": "status_code"}) or {}).get("status_code")
    if st == "PUBLISHED":
        return "publicada", st
    if st == "FINISHED":
        return "reusar", st
    if st == "EXPIRED":
        return "descartar", st
    return "incerta", st


def instante(s):
    """'2026-11-17T15:30:12+0000' (formato da Graph API) ou ISO com ':' -> datetime com fuso, ou None."""
    if not isinstance(s, str) or not s.strip():
        return None
    s = s.strip()
    if s.endswith("Z"):
        s = s[:-1] + "+00:00"
    s = re.sub(r"([+-]\d\d)(\d\d)$", r"\1:\2", s)
    try:
        t = dt.datetime.fromisoformat(s)
    except ValueError:
        return None
    return t if t.tzinfo is not None else None


def stories_desconhecidas(api_get, ig_user, conhecidos, desde):
    """Stories ATIVOS da conta publicados a partir de `desde` (datetime com fuso) cujo id o estado não
    conhece. Story sem hora legível conta como de hoje (cegueira não libera). Resposta sem lista 'data'
    = exceção (não dá para conferir: o chamador não publica)."""
    r = api_get(f"{ig_user}/stories", {"fields": "id,timestamp", "limit": 50}) or {}
    dados = r.get("data") if isinstance(r, dict) else None
    if not isinstance(dados, list):
        raise RuntimeError(f"GET {ig_user}/stories sem lista 'data' ({str(r)[:120]})")
    out = []
    for s in dados:
        if not isinstance(s, dict) or s.get("id") in conhecidos:
            continue
        t = instante(s.get("timestamp"))
        if t is None or t >= desde:
            out.append(s)
    return out


def conferir_no_ar(saiu, api_get, erros_fatais=()):
    """GET de cada media_id publicado. Devolve a lista de problemas (vazia = tudo no ar)."""
    prob = []
    for i, mid in saiu:
        if not mid:
            continue
        try:
            r = api_get(mid, {"fields": "id,timestamp"}) or {}
            if r.get("id") != mid:
                prob.append(f"parte {i + 1}: GET {mid} devolveu {r!r}")
        except erros_fatais:
            raise
        except Exception as e:                                  # noqa: BLE001
            prob.append(f"parte {i + 1}: GET {mid} falhou ({e})")
    return prob


def _autoteste():
    falhas = []

    def checa(nome, ok, det=""):
        print(("OK   " if ok else "FALHA"), nome, "" if ok else det)
        if not ok:
            falhas.append(nome)

    class Auth(Exception):
        pass

    def montar(cen):
        estado = {"n": 0, "pub": [], "status": dict(cen.get("status_extra", {})), "chamadas": []}

        def api_post(path, dados):
            estado["chamadas"].append(("POST", path, dict(dados)))
            if path.endswith("/media"):
                estado["n"] += 1; c = f"C{estado['n']}"
                estado["status"][c] = cen.get("status_inicial", {}).get(estado["n"], "FINISHED")
                return {"id": c}
            c = dados["creation_id"]; k = int(c.lstrip("CX") or 0)
            if cen.get("auth_no_publish") == k:
                estado["falhou"] = True
                if cen.get("auth_mas_saiu"):
                    estado["status"][c] = "PUBLISHED"; estado["pub"].append(c)
                raise Auth("190")
            if k in cen.get("publish_erro", {}):
                estado["falhou"] = True
                efeito = cen["publish_erro"][k]
                if efeito == "saiu":
                    estado["status"][c] = "PUBLISHED"; estado["pub"].append(c)
                elif efeito == "incerto":
                    estado["status"][c] = "IN_PROGRESS"
                raise RuntimeError("HTTP 500")
            estado["status"][c] = "PUBLISHED"; estado["pub"].append(c)
            return {"id": "M" + c[1:]}

        def api_get(path, params):
            estado["chamadas"].append(("GET", path, dict(params)))
            if path.startswith(("C", "X")):
                if cen.get("consulta_falha") and estado.get("falhou"):      # só a consulta DEPOIS do erro
                    raise (Auth("190") if cen["consulta_falha"] == "auth" else RuntimeError("timeout"))
                return {"status_code": estado["status"][path]}
            if path in cen.get("get_falha", ()):
                raise RuntimeError("404")
            return {"id": path}
        return estado, api_post, api_get

    def rodar(cen, ja=None, prazo=480, conteineres=None):
        estado, ap, ag = montar(cen)
        reg, wa = [], []
        t = {"v": 0.0}
        def sleep(s): t["v"] += s
        def relogio(): return t["v"]

        def antes(i, c):
            wa.append((i, c)); estado["chamadas"].append(("WA", i, c))
        try:
            saiu = publicar_partes("st", [{"arquivo": f"p{i}.mp4"} for i in range(3)], ja or {}, ig_user="U",
                                   api_post=ap, api_get=ag, raw_url=lambda p: "https://x/" + p,
                                   registrar=lambda i, m, info: reg.append((i, m, info)), antes_de_publicar=antes,
                                   conteineres=conteineres, erros_fatais=(Auth,), prazo_s=prazo, sleep=sleep,
                                   relogio=relogio)
            return "ok", saiu, reg, estado
        except StoryIncerta as e:
            return "incerta", str(e), reg, estado
        except Auth:
            return "auth", None, reg, estado
        except RuntimeError as e:
            return "erro", str(e), reg, estado
        finally:
            estado["wa"] = wa

    r, saiu, reg, est = rodar({})
    checa("3 partes publicadas e registradas na ordem", r == "ok" and [x[0] for x in reg] == [0, 1, 2] and len(est["pub"]) == 3, (r, reg))
    checa("vídeo vai por video_url com media_type STORIES", all(c[2].get("media_type") == "STORIES" and "video_url" in c[2]
                                                                  for c in est["chamadas"] if c[1] == "U/media"))
    ordem = [c[0] if c[0] == "WA" else c[1] for c in est["chamadas"] if c[0] == "WA" or c[1] == "U/media_publish"]
    checa("write-ahead do contêiner ANTES de cada media_publish", ordem == ["WA", "U/media_publish"] * 3
          and est["wa"] == [(0, "C1"), (1, "C2"), (2, "C3")], ordem)
    r, msg, reg, est = rodar({"status_inicial": {2: "ERROR"}})
    checa("CONTROLE: contêiner em ERROR -> nada publicado", r == "erro" and est["pub"] == [] and reg == [] and est["wa"] == [], (r, msg))
    r, msg, reg, est = rodar({"status_inicial": {3: "IN_PROGRESS"}}, prazo=30)
    checa("CONTROLE: prazo estourado -> nada publicado", r == "erro" and "prazo" in msg and est["pub"] == [], (r, msg))
    r, msg, reg, est = rodar({"publish_erro": {2: "saiu"}})
    checa("erro no publish com contêiner PUBLISHED conta como saiu e segue", r == "ok" and [x[0] for x in reg] == [0, 1, 2]
          and reg[1][2].get("confirmado_por"), (r, reg))
    r, msg, reg, est = rodar({"publish_erro": {2: "nao_saiu"}})
    checa("erro no publish com contêiner FINISHED: parte 1 registrada, para, sem duplicar", r == "erro" and [x[0] for x in reg] == [0]
          and len(est["pub"]) == 1 and est["wa"][-1] == (1, "C2"), (r, reg))
    r2, saiu2, reg2, est2 = rodar({}, ja={0: "M1"})
    checa("retomada publica só as partes 2 e 3", r2 == "ok" and [x[0] for x in reg2] == [1, 2] and len(est2["pub"]) == 2, (r2, reg2))
    r, msg, reg, est = rodar({"publish_erro": {2: "incerto"}})
    checa("CONTROLE: contêiner incerto -> registra incerto e BLOQUEIA", r == "incerta" and reg[-1][2].get("incerto") and len(reg) == 2, (r, reg))
    # fatal (token) no media_publish: sobe só DEPOIS de perguntar ao contêiner
    r, msg, reg, est = rodar({"auth_no_publish": 2, "auth_mas_saiu": True})
    checa("fatal no media_publish com contêiner PUBLISHED: a parte é registrada e o fatal sobe", r == "auth"
          and [x[0] for x in reg] == [0, 1] and reg[1][2].get("confirmado_por") and len(est["pub"]) == 2, (r, reg))
    consultou = any(c[0] == "GET" and c[1] == "C2" for c in est["chamadas"][[k for k, c in enumerate(est["chamadas"])
                                                                              if c[1] == "U/media_publish"][1]:])
    checa("  ...e o contêiner foi consultado depois do erro fatal", consultou, est["chamadas"])
    r, msg, reg, est = rodar({"auth_no_publish": 2})
    checa("fatal no media_publish com contêiner FINISHED: parte 1 registrada, fatal sobe, sem incerta", r == "auth"
          and [x[0] for x in reg] == [0] and len(est["pub"]) == 1, (r, reg))
    r, msg, reg, est = rodar({"auth_no_publish": 2, "consulta_falha": "auth"})
    checa("fatal no media_publish e a consulta falha: registra INCERTO e só então sobe", r == "auth"
          and [x[0] for x in reg] == [0, 1] and reg[1][2].get("incerto") and reg[1][2].get("erro_consulta"), (r, reg))
    r, msg, reg, est = rodar({"publish_erro": {2: "nao_saiu"}, "consulta_falha": "auth"})
    checa("erro comum no media_publish e consulta com token morto: INCERTO registrado e o fatal sobe", r == "auth"
          and reg[-1][0] == 1 and reg[-1][2].get("incerto"), (r, reg))
    r, msg, reg, est = rodar({"publish_erro": {2: "nao_saiu"}, "consulta_falha": "outra"})
    checa("erro comum no media_publish e consulta que falha: INCERTO (nunca 'não saiu')", r == "incerta"
          and reg[-1][2].get("incerto"), (r, reg))
    # reaproveitar o contêiner do write-ahead (FINISHED) em vez de criar outro
    r, saiu, reg, est = rodar({"status_extra": {"X9": "FINISHED"}}, ja={0: "M1"}, conteineres={1: "X9"})
    criados = [c for c in est["chamadas"] if c[1] == "U/media"]
    publ = [c[2]["creation_id"] for c in est["chamadas"] if c[1] == "U/media_publish"]
    checa("contêiner do write-ahead é REAPROVEITADO (não cria outro para a parte)", len(criados) == 1 and publ[0] == "X9", (criados, publ))
    # resolver_publicando
    est, _, ag = montar({})
    est["status"].update({"C7": "PUBLISHED", "C8": "FINISHED", "C9": "IN_PROGRESS", "C6": "EXPIRED", "C5": "ERROR"})
    checa("resolver: PUBLISHED = publicada", resolver_publicando({"container": "C7"}, ag)[0] == "publicada")
    checa("resolver: FINISHED = reusar", resolver_publicando({"container": "C8"}, ag)[0] == "reusar")
    checa("resolver: EXPIRED = descartar (só contêiner não publicado expira)", resolver_publicando({"container": "C6"}, ag)[0] == "descartar")
    checa("CONTROLE resolver: IN_PROGRESS/ERROR/sem contêiner = incerta",
          [resolver_publicando(x, ag)[0] for x in ({"container": "C9"}, {"container": "C5"}, {})] == ["incerta"] * 3)
    est_f, _, ag_f = montar({"consulta_falha": "outra"})
    est_f["falhou"] = True
    try:
        resolver_publicando({"container": "C1"}, ag_f); ok = False
    except RuntimeError:
        ok = True
    checa("CONTROLE resolver: consulta que falha SOBE (não decide no escuro)", ok)
    # stories_desconhecidas (GET /stories antes de publicar)
    desde = dt.datetime(2026, 11, 17, 12, 30, tzinfo=dt.timezone(dt.timedelta(hours=-3)))

    def ag_st(dados):
        return lambda path, params: {"data": dados} if path.endswith("/stories") else {}
    conta = [{"id": "A", "timestamp": "2026-11-17T15:31:00+0000"}, {"id": "B", "timestamp": "2026-11-17T12:00:00+0000"},
             {"id": "C", "timestamp": "2026-11-17T15:40:00+0000"}, {"id": "D"}]
    novas = [s["id"] for s in stories_desconhecidas(ag_st(conta), "U", {"C"}, desde)]
    checa("conta: story de hoje depois das 12:30 que o estado não conhece é acusada; a conhecida e a da manhã não",
          novas == ["A", "D"], novas)
    checa("CONTROLE conta: só stories conhecidas ou de antes das 12:30 = nada acusado",
          stories_desconhecidas(ag_st(conta[:3]), "U", {"A", "C"}, desde) == [])
    try:
        stories_desconhecidas(lambda p, q: {"error": "x"}, "U", set(), desde); ok = False
    except RuntimeError:
        ok = True
    checa("CONTROLE conta: resposta sem 'data' levanta (guarda cega não libera)", ok)
    checa("instante: formato da Graph (+0000) e 'Z'", instante("2026-11-17T15:31:00+0000") == instante("2026-11-17T15:31:00Z")
          == dt.datetime(2026, 11, 17, 15, 31, tzinfo=dt.timezone.utc) and instante("lixo") is None)
    _, ap, ag = montar({"get_falha": ("M2",)})
    checa("conferência: GET que falha vira problema", conferir_no_ar([(0, "M1"), (1, "M2")], ag) != [] and conferir_no_ar([(0, "M1")], ag) == [])
    print("\n" + ("AUTOTESTE OK" if not falhas else f"AUTOTESTE: {len(falhas)} FALHA(S)"))
    return 1 if falhas else 0


if __name__ == "__main__":
    import sys
    sys.exit(_autoteste())
