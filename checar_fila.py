# -*- coding: utf-8 -*-
"""Alarme de ESTOQUE da fila (auditoria v4, 27/11/2026 — P0 nº 2 do backlog).

A v4 achou que o risco mais imediato do perfil não era o algoritmo, era o estoque: o último roteiro
novo aprovado era de 08/11 e a primeira vaga vazia de reel caía em 10/12 — e nada avisava. Este
checador SÓ LÊ (não toca no publish.py, no reels.json nem nas regras de cota) e projeta a fila dia a
dia com a MESMA regra do robô (publish_agenda.projeta_reels -> regra_reels.proximo_reel), separada
nos dois grupos de dias (formatos novos ter/qui/sáb; COMO FUNCIONA seg/qua/sex/dom), e os stories
com publish_agenda.projeta_stories_detalhe.

  VERMELHO (exit 1): menos de DIAS_VERMELHO dias até a 1ª vaga de reel vazia em QUALQUER grupo.
  AMARELO (exit 0, vai para o resumo do job): menos de DIAS_AMARELO dias num grupo; menos de
    MIN_PECAS_PESO peças pendentes de CÂMERA LENTA ou de CHAMA O VAR (os formatos com peso > 0);
    próxima story a mais de MAX_DIAS_STORY dias (ou nenhuma no horizonte); PROGRAMACAO.md
    regenerado há mais de MAX_DIAS_PROGRAMACAO dias.

"Dias de reel" = dias corridos de `hoje` até a 1ª vaga do grupo que fica sem peça. A projeção parte
do dia do último registro do estado (com o que já saiu nesse dia), então `--hoje` no futuro consome
a fila entre o estado real e a data pedida — é assim que `--hoje 2026-12-06` mostra o buraco de 10/12.

Uso: python checar_fila.py [--hoje AAAA-MM-DD] | --auto-teste
"""
import argparse
import datetime as dt
import json
import os
import re
import sys

RAIZ = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, RAIZ)
import regra_reels as R  # noqa: E402
import publish_agenda as PA  # noqa: E402

DIAS_VERMELHO = 5
DIAS_AMARELO = 10
MIN_PECAS_PESO = 2
FORMATOS_COM_PESO = ("camera_lenta", "chama_o_var")
MAX_DIAS_STORY = 7
MAX_DIAS_PROGRAMACAO = 7
HORIZONTE = 60
GRUPOS = (R.GRUPO_NOVOS, R.GRUPO_COMO_FUNCIONA)
NOME_GRUPO = {R.GRUPO_NOVOS: "formatos novos (ter/qui/sáb)", R.GRUPO_COMO_FUNCIONA: "COMO FUNCIONA (seg/qua/sex/dom)"}
RE_PROG = re.compile(r"Regenerado em (\d{2})/(\d{2})/(\d{4})")


def _data_brt(at):
    try:
        return dt.datetime.fromisoformat(at).astimezone(R.BRT).date()
    except (TypeError, ValueError):
        return None


def base_do_estado(published, hoje):
    """(base, reel_ja_saiu_na_base, story_ja_saiu_na_base): o dia do último registro do estado.
    Sem registro, ou estado à frente de `hoje`, a base é `hoje`."""
    datas = [d for d in (_data_brt(e.get("at")) for e in published) if d]
    base = max(datas) if datas else hoje
    if base > hoje:
        base = hoje
    no_dia = [e for e in published if _data_brt(e.get("at")) == base]
    reel = any(e.get("kind") in ("reel", "reel_incerto") for e in no_dia)
    story = any(e.get("kind") == "story_nova" for e in no_dia)
    return base, reel, story


def cobertura_reels(reels, published, hoje, horizonte=HORIZONTE):
    """-> ({grupo: dias até a 1ª vaga vazia (horizonte se nenhuma)}, {grupo: data da 1ª vaga vazia | None}, proj)."""
    base, ja, _ = base_do_estado(published, hoje)
    fim = hoje + dt.timedelta(days=horizonte)
    proj = PA.projeta_reels(reels, published, base, ja, horizonte_dias=(fim - base).days)
    ocupado = {d for d, _ in proj}
    vazio = {g: None for g in GRUPOS}
    d = hoje
    while d <= fim:
        g = R.grupo_do_dia(d)
        ja_hoje = (d == base and ja)
        if g in vazio and vazio[g] is None and d not in ocupado and not ja_hoje:
            vazio[g] = d
        d += dt.timedelta(days=1)
    dias = {g: (vazio[g] - hoje).days if vazio[g] else horizonte for g in GRUPOS}
    return dias, vazio, proj


def pendentes_por_formato(reels, published, consumidos=()):
    """Peças de CÂMERA LENTA / CHAMA O VAR ainda na fila: fora do estado e fora do que a projeção já
    publicou antes de `hoje` (`consumidos`)."""
    done = {e.get("id") for e in published} | set(consumidos)
    out = {f: 0 for f in FORMATOS_COM_PESO}
    for x in reels:
        f = R.formato(x)
        if f in out and x.get("id") not in done:
            out[f] += 1
    return out


def proxima_story(stories, published, reels_proj, hoje, aprovacoes=None, reels_por_id=None):
    """-> (data da próxima story >= hoje | None, bloqueio | None, pendentes)."""
    base, _, story_ja = base_do_estado(published, hoje)
    fim = hoje + dt.timedelta(days=HORIZONTE)
    r = PA.projeta_stories_detalhe(stories, published, reels_proj, base, story_ja, horizonte_dias=(fim - base).days,
                                   aprovacoes=aprovacoes, reels_por_id=reels_por_id)
    datas = [d for d, _, _ in r["agenda"] if d >= hoje]
    return (min(datas) if datas else None), r.get("bloqueio"), r.get("pendentes", [])


def data_programacao(texto):
    m = RE_PROG.search(texto or "")
    if not m:
        return None
    dd, mm, aa = map(int, m.groups())
    return dt.date(aa, mm, dd)


def classificar(dias, vazio, pend, story, bloqueio, prog, hoje):
    """-> (exit, [(nível, mensagem)]). Pura: o auto-teste exercita as fronteiras aqui."""
    msgs = []
    for g in GRUPOS:
        quando = f"1ª vaga vazia em {vazio[g]:%d/%m}" if vazio.get(g) else f"sem vaga vazia em {HORIZONTE} dias"
        txt = f"{NOME_GRUPO[g]}: {dias[g]} dia(s) de reel ({quando})"
        if dias[g] < DIAS_VERMELHO:
            msgs.append(("VERMELHO", txt + f" < {DIAS_VERMELHO} — falta roteiro aprovado AGORA"))
        elif dias[g] < DIAS_AMARELO:
            msgs.append(("AMARELO", txt + f" < {DIAS_AMARELO}"))
        else:
            msgs.append(("ok", txt))
    for f in FORMATOS_COM_PESO:
        txt = f"{R.NOMES_FORMATOS[f]}: {pend[f]} peça(s) pendente(s) na fila"
        msgs.append(("AMARELO", txt + f" < {MIN_PECAS_PESO} (formato com peso no rodízio)") if pend[f] < MIN_PECAS_PESO
                    else ("ok", txt))
    if bloqueio:
        msgs.append(("AMARELO", f"stories: BLOQUEIO na projeção — {bloqueio}"))
    if story is None:
        msgs.append(("AMARELO", f"stories: nenhuma story projetada nos próximos {HORIZONTE} dias"))
    elif (story - hoje).days > MAX_DIAS_STORY:
        msgs.append(("AMARELO", f"stories: próxima só em {story:%d/%m} ({(story - hoje).days} dias > {MAX_DIAS_STORY})"))
    else:
        msgs.append(("ok", f"stories: próxima em {story:%d/%m}"))
    if prog is None:
        msgs.append(("AMARELO", "PROGRAMACAO.md sem a linha 'Regenerado em DD/MM/AAAA' (ou ausente)"))
    elif (hoje - prog).days > MAX_DIAS_PROGRAMACAO:
        msgs.append(("AMARELO", f"PROGRAMACAO.md regenerado em {prog:%d/%m/%Y} ({(hoje - prog).days} dias > "
                                f"{MAX_DIAS_PROGRAMACAO}) — a página que o Rafael revisa está velha"))
    else:
        msgs.append(("ok", f"PROGRAMACAO.md regenerado em {prog:%d/%m/%Y}"))
    rc = 1 if any(n == "VERMELHO" for n, _ in msgs) else 0
    return rc, msgs


def avaliar(reels, published, stories, prog_texto, hoje, aprovacoes=None, reels_por_id=None):
    dias, vazio, proj = cobertura_reels(reels, published, hoje)
    pend = pendentes_por_formato(reels, published, [rid for d, rid in proj if d < hoje])
    story, bloq, _ = proxima_story(stories, published, proj, hoje, aprovacoes, reels_por_id)
    return classificar(dias, vazio, pend, story, bloq, data_programacao(prog_texto), hoje)


def _ler(nome, padrao):
    try:
        with open(os.path.join(RAIZ, nome), encoding="utf-8-sig") as f:
            return f.read() if padrao is None else json.load(f)
    except FileNotFoundError:
        return "" if padrao is None else padrao


def auto_teste():
    os.environ["TROCAS_DE_DIA"] = "off"     # a mecânica não depende do calendário de testes de 11/2026
    os.environ["REEL_DO_DIA"] = "off"
    seg = dt.date(2027, 3, 1)               # segunda
    assert seg.weekday() == 0
    ontem = (dt.datetime(2027, 2, 28, 15, 5, tzinfo=R.BRT)).isoformat()
    pub = [{"id": "velho", "kind": "reel", "at": ontem, "formato": "como_funciona"}]

    def fila(n_cf, n_cl, n_var):
        return ([{"id": f"cf{i}", "formato": "como_funciona"} for i in range(n_cf)]
                + [{"id": f"cl{i}", "formato": "camera_lenta"} for i in range(n_cl)]
                + [{"id": f"var{i}", "formato": "chama_o_var"} for i in range(n_var)])
    prog_ok = "Regenerado em 28/02/2027 por `_gen_programacao.py`."
    falhas = 0

    def caso(nome, cond):
        nonlocal falhas
        falhas += not cond
        print(f"[{'ok' if cond else 'FALHOU'}] {nome}")

    # positivo: fila vazia reprova (exit 1) — sem stories também, que é amarelo
    rc, msgs = avaliar([], pub, [], prog_ok, seg, aprovacoes={"lotes": []}, reels_por_id={})
    caso("positivo: fila vazia = VERMELHO (exit 1)", rc == 1 and sum(n == "VERMELHO" for n, _ in msgs) == 2)
    # negativo: fila de 30+ dias nos dois grupos passa sem vermelho e sem amarelo de reel
    rc, msgs = avaliar(fila(20, 12, 8), pub, [], prog_ok, seg, aprovacoes={"lotes": []}, reels_por_id={})
    reel_msgs = [n for n, m in msgs if "dia(s) de reel" in m or "pendente" in m]
    caso("negativo: fila de 30 dias = exit 0, reels todos ok", rc == 0 and reel_msgs == ["ok"] * 4)
    # cobertura medida certo: seg com 2 COMO FUNCIONA -> saem seg e qua, sexta (dia 4) fica vazia
    dias, vazio, _ = cobertura_reels(fila(2, 12, 8), pub, seg)
    caso("cobertura: 2 COMO FUNCIONA a partir de seg = 4 dias (1ª vaga vazia na sex)",
         dias[R.GRUPO_COMO_FUNCIONA] == 4 and vazio[R.GRUPO_COMO_FUNCIONA] == dt.date(2027, 3, 5))
    # reel de hoje já saiu: não conta hoje como vaga vazia
    pub_hoje = pub + [{"id": "hoje", "kind": "reel", "at": dt.datetime(2027, 3, 1, 15, 5, tzinfo=R.BRT).isoformat(),
                       "formato": "como_funciona"}]
    dias, vazio, _ = cobertura_reels(fila(0, 12, 8), pub_hoje, seg)
    caso("cobertura: reel de hoje publicado e fila CF vazia = 1ª vaga vazia na qua (2 dias)",
         vazio[R.GRUPO_COMO_FUNCIONA] == dt.date(2027, 3, 3) and dias[R.GRUPO_COMO_FUNCIONA] == 2)
    # fronteiras 5/10 na classificação
    vz = {g: None for g in GRUPOS}
    sem = dict(pend={"camera_lenta": 5, "chama_o_var": 5}, story=seg, bloqueio=None, prog=seg, hoje=seg)
    for d_cf, esperado_rc, esperado_nivel in ((4, 1, "VERMELHO"), (5, 0, "AMARELO"), (9, 0, "AMARELO"), (10, 0, "ok")):
        rc, msgs = classificar({R.GRUPO_NOVOS: 30, R.GRUPO_COMO_FUNCIONA: d_cf}, vz, **sem)
        nivel = next(n for n, m in msgs if m.startswith("COMO FUNCIONA"))
        caso(f"fronteira: {d_cf} dias = {esperado_nivel} (exit {esperado_rc})", rc == esperado_rc and nivel == esperado_nivel)
    # peças com peso: 1 de CÂMERA LENTA = amarelo; 2 = ok
    for n, esperado in ((1, "AMARELO"), (2, "ok")):
        rc, msgs = classificar({g: 30 for g in GRUPOS}, vz, {"camera_lenta": n, "chama_o_var": 5}, seg, None, seg, seg)
        nivel = next(nv for nv, m in msgs if m.startswith("CÂMERA LENTA"))
        caso(f"peso: {n} CÂMERA LENTA pendente = {esperado}", nivel == esperado and rc == 0)
    # story: 8 dias = amarelo, 7 = ok, nenhuma = amarelo
    for st, esperado in ((seg + dt.timedelta(8), "AMARELO"), (seg + dt.timedelta(7), "ok"), (None, "AMARELO")):
        _, msgs = classificar({g: 30 for g in GRUPOS}, vz, sem["pend"], st, None, seg, seg)
        nivel = next(nv for nv, m in msgs if m.startswith("stories"))
        caso(f"story: {st} = {esperado}", nivel == esperado)
    # PROGRAMACAO.md: 8 dias = amarelo, 7 = ok, sem linha = amarelo
    for txt, esperado in (("Regenerado em 21/02/2027", "AMARELO"), ("Regenerado em 22/02/2027", "ok"), ("nada", "AMARELO")):
        _, msgs = classificar({g: 30 for g in GRUPOS}, vz, sem["pend"], seg, None, data_programacao(txt), seg)
        nivel = next(nv for nv, m in msgs if m.startswith("PROGRAMACAO"))
        caso(f"programação: '{txt}' = {esperado}", nivel == esperado)
    # --hoje no futuro com estado de ontem: a projeção parte do ESTADO e consome a fila até hoje (verificador 27/11:
    # com `base = hoje` este controle positivo virava amarelo e nada acusava)
    seg8 = seg + dt.timedelta(days=7)
    fila8 = fila(4, 12, 8)
    rc, msgs = avaliar(fila8, pub, [], prog_ok, seg8, aprovacoes={"lotes": []}, reels_por_id={})
    caso("futuro: estado de ontem + 7 dias consome os 4 COMO FUNCIONA = VERMELHO", rc == 1)
    _, _, proj = cobertura_reels(fila8, pub, seg8)
    pend = pendentes_por_formato(fila8, pub, [rid for d, rid in proj if d < seg8])
    caso("futuro: peças com peso descontam as que a projeção já publicou (20 - 3 = 17)",
         pend["camera_lenta"] + pend["chama_o_var"] == 17)
    # estado à frente de hoje: base volta para hoje
    pub_fut = pub + [{"id": "fut", "kind": "reel", "at": dt.datetime(2027, 3, 5, 15, 5, tzinfo=R.BRT).isoformat()}]
    caso("estado à frente de hoje: base = hoje", base_do_estado(pub_fut, seg)[0] == seg)
    # bloqueio de story na projeção = amarelo
    _, msgs = classificar({g: 30 for g in GRUPOS}, vz, sem["pend"], seg, "story X sem aprovação", seg, seg)
    caso("story: bloqueio na projeção = AMARELO", any(n == "AMARELO" and "BLOQUEIO" in m for n, m in msgs))
    os.environ.pop("TROCAS_DE_DIA"); os.environ.pop("REEL_DO_DIA")
    total = 4 + 4 + 2 + 3 + 3 + 4
    print(f"AUTO-TESTE: {total - falhas}/{total} —", "PASSOU" if not falhas else "REPROVOU")
    return 1 if falhas else 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--hoje"); ap.add_argument("--auto-teste", action="store_true")
    a = ap.parse_args()
    if a.auto_teste:
        return auto_teste()
    hoje = dt.date.fromisoformat(a.hoje) if a.hoje else dt.datetime.now(R.BRT).date()
    reels = _ler("reels.json", [])
    published = _ler(os.path.join("state", "published.json"), {"published": []}).get("published", [])
    stories = _ler("stories_cf.json", [])
    rc, msgs = avaliar(reels, published, stories, _ler("PROGRAMACAO.md", None), hoje)
    resumo = [f"### Estoque da fila ({hoje:%d/%m/%Y})", ""]
    for nivel, m in msgs:
        print(f"[{nivel}] {m}")
        if nivel == "VERMELHO":
            print(f"::error::{m}")
        elif nivel == "AMARELO":
            print(f"::warning::{m}")
        resumo.append(f"- **{nivel}** {m}")
    print("VEREDITO:", "VERMELHO" if rc else ("AMARELO" if any(n == "AMARELO" for n, _ in msgs) else "ok"))
    caminho = os.environ.get("GITHUB_STEP_SUMMARY")
    if caminho:
        with open(caminho, "a", encoding="utf-8") as f:
            f.write("\n".join(resumo) + "\n")
    return rc


if __name__ == "__main__":
    sys.exit(main())
