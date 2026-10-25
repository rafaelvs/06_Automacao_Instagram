# -*- coding: utf-8 -*-
"""Reordena a CAUDA da fila de reels COMO FUNCIONA pela regra de temas (Rafael, 24/10/2026).

"não colocar coisas que foram postadas muito recentemente sobrepondo [...] usar temas mais anteriores
nas próximas postagens, para não ficar repetitivo demais". O publish.py continua FIFO (a ordem da fila
é a programação que o Rafael revisa); esta ferramenta reescreve a ORDEM uma vez, simulando dia a dia:
em cada dia de reel, sai o 1º da fila cujo tema não apareceu (em nenhuma superfície) nos últimos N dias;
se todos conflitam, o do tema que apareceu há mais tempo — nunca deixa dia sem reel por causa do tema.

Os reels até --fixar-ate (inclusive) ficam onde estão: são o M1 (02/11) e decisões já tomadas.

Uso:  python ordenar_fila_temas.py --fixar-ate 2026-10-30            (mostra a proposta)
      python ordenar_fila_temas.py --fixar-ate 2026-10-30 --gravar    (reescreve reels.json)
"""
import argparse
import datetime as dt
import json
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)
import publish_agenda as PA          # noqa: E402
import regra_reels                   # noqa: E402
import temas_conteudo as T           # noqa: E402


def main():
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
    antes = PA.projeta_reels(reels, st["published"], hoje, ja_hoje)
    fixos = [i for d, i in antes if d <= fixar]
    cauda = [i for d, i in antes if d > fixar]                 # ordem atual da cauda projetada
    por_id = {r["id"]: r for r in reels}
    # simula: o estado recebe os fixos nas suas datas e a cauda escolhida dia a dia
    sim = list(st["published"]) + [{"id": i, "kind": "reel", "at": dt.datetime(d.year, d.month, d.day, 15, 5,
                                    tzinfo=PA.BRT).isoformat()} for d, i in antes if d <= fixar]
    dias = [d for d, _ in antes if d > fixar]
    restante = list(cauda); nova = []
    d = dias[0] if dias else None
    while restante and d is not None:
        if d.weekday() in PA.REEL_WEEKDAYS:
            pas = T.aparicoes([e for e in sim if e.get("at", "")[:10] <= d.isoformat()], PA.BRT)
            esc = next((i for i in restante if not T.conflito({T.tema_de(i)} - {None}, d, pas, {}, n)), None)
            if esc is None:
                esc = min(restante, key=lambda i: (T.ultima({T.tema_de(i)} - {None}, pas), restante.index(i)))
            nova.append((d, esc)); restante.remove(esc)
            sim.append({"id": esc, "kind": "reel", "at": dt.datetime(d.year, d.month, d.day, 15, 5, tzinfo=PA.BRT).isoformat()})
        d += dt.timedelta(days=1)
    print(f"Regra: {n} dias entre o mesmo tema | fixos até {fixar:%d/%m}: {fixos}")
    for (d0, i0), (d1, i1) in zip([(d, i) for d, i in antes if d > fixar], nova):
        marca = "" if i0 == i1 else "   <- muda"
        print(f"{d1:%a %d/%m}  {i1:26s} {str(T.tema_de(i1)):18s} (antes: {i0}){marca}")
    if a.gravar:
        ordem = fixos + [i for _, i in nova]
        pos = {i: k for k, i in enumerate(ordem)}
        idx = [k for k, r in enumerate(reels) if r["id"] in pos]           # posições ocupadas pelos projetados
        novos = sorted((r for r in reels if r["id"] in pos), key=lambda r: pos[r["id"]])
        for k, r in zip(idx, novos):
            reels[k] = r
        with open(os.path.join(ROOT, "reels.json"), "w", encoding="utf-8", newline="\n") as f:
            json.dump(reels, f, ensure_ascii=False, indent=2)
            f.write("\n")
        depois = PA.projeta_reels(reels, st["published"], hoje, ja_hoje)
        assert [i for _, i in depois] == ordem, "a projeção depois de gravar não bate com a ordem proposta"
        print("reels.json reescrito; projeção conferida.")


if __name__ == "__main__":
    main()
