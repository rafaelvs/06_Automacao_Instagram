# -*- coding: utf-8 -*-
"""Reordena a CAUDA da fila de reels pela regra de temas (Rafael, 24/10/2026).

"não colocar coisas que foram postadas muito recentemente sobrepondo [...] usar temas mais anteriores
nas próximas postagens, para não ficar repetitivo demais". O publish.py continua FIFO (a ordem da fila
é a programação que o Rafael revisa); esta ferramenta reescreve a ORDEM uma vez, simulando dia a dia
com a MESMA regra do robô (regra_reels.proximo_reel):
  * em cada dia, o GRUPO do dia decide quem pode sair (regra_reels.grupo_do_dia): seg/qua/sex/dom = COMO
    FUNCIONA (e lâmina/conversa, se religadas e dentro da cota); ter/qui/sáb a partir de 03/11 = o formato
    novo da vez no RODÍZIO (o publicado há mais tempo; a ferramenta não mexe no rodízio, só em QUAL peça
    daquele formato sai);
  * entre as peças que podem sair, sai a 1ª da fila cujo tema não apareceu nos últimos N dias em NENHUMA
    superfície — todos os reels (dos dois grupos), stories e sequências do estado, mais o que a própria
    simulação já pôs no ar; se todas conflitam, a do tema que apareceu há mais tempo — nunca deixa dia sem
    reel por causa do tema.
Só reordena DENTRO do mesmo grupo de dias (formatos novos 26/10/2026): as posições que COMO FUNCIONA ocupa na fila
continuam com COMO FUNCIONA. Nos formatos novos, dentro do mesmo FORMATO: cada formato novo fica com as posições que já
tinha na fila e as peças dele saem delas na ordem em que serão publicadas. Assim o 1º pendente de cada formato está, em
toda vaga, na mesma posição da fila original, e o desempate do rodízio (posição do 1º pendente) dá a MESMA sequência de
formatos — a ferramenta só escolhe QUAL peça do formato sai (verificação de 26/10/2026: com as vagas do GRUPO inteiro,
uma peça de outro formato caía antes de um fixo e trocava o formato de uma data FIXADA).

Os reels até --fixar-ate (inclusive) ficam nas MESMAS DATAS: são o M1 (02/11) e decisões já tomadas. Na fila, vão à
FRENTE das posições da classe deles (o grupo COMO FUNCIONA, ou o formato novo), na ordem das datas; a cauda vem depois.

--gravar só escreve o reels.json depois de conferir que a fila nova projeta EXATAMENTE os fixos + a proposta (mesma
regra do robô, dia a dia). Divergiu = aborta sem tocar no arquivo (antes gravava e só depois conferia).

Uso:  python ordenar_fila_temas.py --fixar-ate 2026-10-30            (mostra a proposta)
      python ordenar_fila_temas.py --fixar-ate 2026-10-30 --gravar    (reescreve reels.json)
"""
import argparse
import datetime as dt
import json
import os
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)
import publish_agenda as PA          # noqa: E402
import regra_reels                   # noqa: E402
import temas_conteudo as T           # noqa: E402


def _grupo_do_item(item):
    return regra_reels.grupo_do_formato(regra_reels.formato(item))


def _classe_do_item(item):
    """Classe de vagas da fila: o grupo COMO FUNCIONA inteiro (COMO FUNCIONA, e lâmina/conversa se religadas: o 1º
    liberado da fila sai) ou o PRÓPRIO formato novo (o rodízio decide o formato; a posição do 1º pendente desempata)."""
    f = regra_reels.formato(item)
    return f if f in regra_reels.FORMATOS_NOVOS else regra_reels.GRUPO_COMO_FUNCIONA


def _as_15h(d):
    return dt.datetime(d.year, d.month, d.day, PA.REEL_MIN // 60, PA.REEL_MIN % 60 + 5, tzinfo=PA.BRT)


def reordenar(reels, published, hoje, ja_hoje, fixar, n, horizonte_dias=800, **regra):
    """Proposta de nova ordem da cauda (sem gravar nada).
    -> {"antes": [(data, id)], "fixos": [id], "nova": [(data, id)], "fila": reels.json reordenado (lista nova),
        "depois": [(data, id)] que a fila nova projeta, "confere": depois == fixos (nas datas deles) + nova}.
    `regra` = argumentos da regra do robô (cota, dias_conversa, conversa_ativa, inicio_novos) — os testes os fixam."""
    antes = PA.projeta_reels(reels, published, hoje, ja_hoje, **regra)
    fixos = [i for d, i in antes if d <= fixar]                # na ordem das datas
    cauda = [i for d, i in antes if d > fixar]                 # ordem atual da cauda projetada
    por_id = {}
    primeira_pos = {}
    for k, r in enumerate(reels):
        por_id.setdefault(r["id"], r)
        primeira_pos.setdefault(r["id"], k)
    grupo_de = {i: _grupo_do_item(por_id[i]) for i in fixos + cauda}
    classe_de = {i: _classe_do_item(por_id[i]) for i in fixos + cauda}
    classes = sorted(set(classe_de.values()))
    # as posições da fila que os projetados (fixos + cauda) de cada CLASSE ocupam (o grupo COMO FUNCIONA; cada formato
    # novo): continuam da mesma classe depois de reordenar. Em cada classe, os FIXOS na frente (ordem das datas), depois
    # o que a simulação escolhe, na ordem de saída: nenhuma peça da cauda fica antes de um fixo, e o 1º pendente de cada
    # formato novo fica, a cada vaga, na posição em que estava na fila original (o rodízio desempata por ela)
    vagas = {c: sorted(primeira_pos[i] for i in fixos + cauda if classe_de[i] == c) for c in classes}
    fixos_de = {c: [i for i in fixos if classe_de[i] == c] for c in classes}
    escolhidos = {c: [] for c in classes}
    restante = list(cauda)

    def fila_com_escolhas():
        """A fila como o robô a veria agora: em cada classe, os fixos na frente (ordem das datas), depois o já
        escolhido e o resto na ordem atual."""
        v = list(reels)
        for c in classes:
            for k, i in zip(vagas[c], fixos_de[c] + escolhidos[c] + [x for x in restante if classe_de[x] == c]):
                v[k] = por_id[i]
        return v

    def tema(i):
        return T.tema_de(por_id.get(i) or i)

    sim = list(published) + [{"id": i, "kind": "reel", "at": _as_15h(d).isoformat(), "formato": regra_reels.formato(por_id[i]),
                              "temas": [t for t in (tema(i),) if t]} for d, i in antes if d <= fixar]
    done = {e["id"] for e in sim}
    nova = []
    dias = [d for d, _ in antes if d > fixar]
    d = dias[0] if dias else None
    while restante and d is not None:
        if (d - dias[0]).days > horizonte_dias:
            raise SystemExit(f"ERRO: a simulação não fecha em {horizonte_dias} dias — sobraram {restante[:6]} (a regra "
                             "mudou no meio? nada gravado)")
        agora = _as_15h(d)
        estado = {"published": sim}
        grupo = regra_reels.grupo_do_dia(d, regra.get("inicio_novos"))
        esc0 = regra_reels.proximo_reel(fila_com_escolhas(), done, estado, agora, **regra) if grupo is not None else None
        if esc0 is not None:
            if grupo == regra_reels.GRUPO_NOVOS:
                # o rodízio decide o FORMATO do dia; aqui só se escolhe QUAL peça dele
                cands = [i for i in restante if regra_reels.formato(por_id[i]) == regra_reels.formato(esc0)]
            else:
                # COMO FUNCIONA (e lâmina/conversa liberadas hoje pelas cotas): a peça sozinha passaria na regra
                cands = [i for i in restante if grupo_de[i] == grupo
                         and regra_reels.proximo_reel([por_id[i]], done, estado, agora, **regra) is not None]
            if cands:
                pas = T.aparicoes([e for e in sim if str(e.get("at", ""))[:10] <= d.isoformat()], PA.BRT)
                esc = next((i for i in cands if not T.conflito({tema(i)} - {None}, d, pas, {}, n)), None)
                if esc is None:
                    esc = min(cands, key=lambda i: (T.ultima({tema(i)} - {None}, pas), cands.index(i)))
                nova.append((d, esc)); restante.remove(esc); escolhidos[classe_de[esc]].append(esc); done.add(esc)
                sim.append({"id": esc, "kind": "reel", "at": agora.isoformat(), "formato": regra_reels.formato(por_id[esc]),
                            "temas": [t for t in (tema(esc),) if t]})
        d += dt.timedelta(days=1)
    fila = fila_com_escolhas()
    # a prova: a fila nova, projetada pela MESMA regra do robô, dá os fixos nas datas deles e a proposta
    depois = PA.projeta_reels(fila, published, hoje, ja_hoje, **regra)
    esperado = [(d1, i) for d1, i in antes if d1 <= fixar] + nova
    return {"antes": antes, "fixos": fixos, "nova": nova, "fila": fila, "depois": depois, "confere": depois == esperado}


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--fixar-ate", required=True, help="AAAA-MM-DD: reels projetados até esta data não mudam")
    ap.add_argument("--hoje", default=None)
    ap.add_argument("--gravar", action="store_true")
    a = ap.parse_args()
    fixar = dt.date.fromisoformat(a.fixar_ate)
    hoje = dt.date.fromisoformat(a.hoje) if a.hoje else dt.datetime.now(PA.BRT).date()
    n = regra_reels.dias_entre_mesmo_tema()
    reels = json.load(open(os.path.join(ROOT, "reels.json"), encoding="utf-8"))
    st = json.load(open(os.path.join(ROOT, "state", "published.json"), encoding="utf-8"))
    ja_hoje = st.get("last_reel_date") == hoje.isoformat()
    r = reordenar(reels, st["published"], hoje, ja_hoje, fixar, n)
    por_id = {x["id"]: x for x in reels}
    antes_por_dia = {d: i for d, i in r["antes"]}
    print(f"Regra: {n} dias entre o mesmo tema (todos os reels e stories) | só reordena dentro do grupo de dias | "
          f"fixos até {fixar:%d/%m}: {r['fixos']}")
    for d1, i1 in r["nova"]:
        i0 = antes_por_dia.get(d1)
        marca = "" if i0 == i1 else "   <- muda"
        f = regra_reels.NOMES_FORMATOS.get(regra_reels.formato(por_id[i1]), regra_reels.formato(por_id[i1]))
        print(f"{d1:%a %d/%m}  {f:15s} {i1:30s} {str(T.tema_de(por_id[i1])):18s} (antes: {i0}){marca}")
    if [i for _, i in r["nova"]] != [i for d, i in r["antes"] if d > fixar] or \
            [d for d, _ in r["nova"]] != [d for d, _ in r["antes"] if d > fixar]:
        print("(a ordem muda; as datas de cada grupo seguem as mesmas vagas)")
    if not r["confere"]:
        # conferido ANTES de abrir o reels.json: a fila nova não projeta os fixos + a proposta -> nada é gravado
        esperado = [(d1, i1) for d1, i1 in r["antes"] if d1 <= fixar] + r["nova"]
        dif = [(e, g) for e, g in zip(esperado, r["depois"]) if e != g] or [(esperado[len(r["depois"]):][:3],
                                                                             r["depois"][len(esperado):][:3])]
        print(f"ERRO: a fila reordenada NÃO projeta a proposta (1ª diferença, esperado x projetado: {dif[:3]}) — "
              "reels.json INTOCADO.")
        raise SystemExit(1)
    if a.gravar:
        ordem = r["fixos"] + [i for _, i in r["nova"]]
        with open(os.path.join(ROOT, "reels.json"), "w", encoding="utf-8", newline="\n") as f:
            json.dump(r["fila"], f, ensure_ascii=False, indent=2)
            f.write("\n")
        # 2ª conferência, sobre o arquivo gravado (lido de volta do disco)
        gravada = json.load(open(os.path.join(ROOT, "reels.json"), encoding="utf-8"))
        depois = PA.projeta_reels(gravada, st["published"], hoje, ja_hoje)
        assert [i for _, i in depois] == ordem, "a projeção depois de gravar não bate com a ordem proposta"
        print("reels.json reescrito; projeção conferida (antes e depois de gravar).")


if __name__ == "__main__":
    main()
