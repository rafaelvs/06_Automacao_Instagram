# -*- coding: utf-8 -*-
"""Regenera PROGRAMACAO.md a partir da FILA (reels.json / posts.json − state/published.json),
projetando as datas pela agenda do publish.py (reels TODO dia às 15h: seg/qua/sex/dom COMO FUNCIONA, ter/qui/sáb
os 4 formatos novos em rodízio a partir de 03/11/2026 — regra_reels.py; posts ter/qui/sáb 15h + dom 11h, suspensos).
Uso: python _gen_programacao.py [AAAA-MM-DD]   (data-base = hoje BRT por padrão)"""
import datetime as dt
import io
import json
import os
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)
import publish_agenda as PA  # noqa: E402

RAW = "https://raw.githubusercontent.com/rafaelvs/06_Automacao_Instagram/main/"
DOW = ["seg", "ter", "qua", "qui", "sex", "sáb", "dom"]


def carrega(n):
    with open(os.path.join(ROOT, n), encoding="utf-8-sig") as f:
        return json.load(f)


def serie_de(iid):
    try:
        from episodios_pe_no_chao import get
        return get(iid).get("serie") or get(iid).get("temporada") or ""
    except Exception:
        return "legado (mudo)" if iid.startswith("reel") else ""


def projeta(ids, weekdays, base, ja_hoje):
    """datas FIFO: 1 item por dia-calendário nos weekdays dados, a partir de base (exclusiva se ja_hoje)."""
    out = []; d = base + dt.timedelta(days=1 if ja_hoje else 0)
    for iid in ids:
        while d.weekday() not in weekdays:
            d += dt.timedelta(days=1)
        out.append((d, iid)); d += dt.timedelta(days=1)
    return out


def secao_stories(st, rp, hoje):
    """Linhas da seção de stories: a agenda do robô (só APROVADAS, com o portão), o bloqueio (parte
    incerta, story incompleta de outro dia, portão barrando a escolhida) e, à parte, as que aguardam
    aprovação (fora da conta), com a data em que sairiam se aprovadas hoje."""
    import checar_stories as CS
    stn = carrega("stories_cf.json") if os.path.exists(os.path.join(ROOT, "stories_cf.json")) else []
    aprov = carrega("aprovacoes.json")
    reels = {r["id"]: r for r in carrega("reels.json")}
    ja = st.get("last_story_nova_date") == hoje.isoformat()
    det = PA.projeta_stories_detalhe(stn, st["published"], rp, hoje, ja, aprovacoes=aprov, reels_por_id=reels)
    nd = PA.regra_reels.dias_entre_mesmo_tema()
    feitas = CS.partes_publicadas(st["published"])
    L = ["\n## Stories da geração nova (ter · qui · sáb 12:30)\n",
         f"*3 vídeos curtos sem voz por story, roteiro próprio. **Regra de temas (Rafael, 24/10):** nada sai sobre um tema que "
         f"apareceu ou vai aparecer em qualquer superfície há menos de {nd} dias; entre os liberados, sai o tema mais antigo. "
         f"Só sai APROVADA pelo Rafael, com o reel de origem no grid há {CS.DIAS_DEPOIS_DO_REEL}+ dias e com o portão limpo "
         "(render do CI coerente com o texto). Story que aguarda aprovação fica FORA da conta: não sai e não segura as outras. "
         "Esta tabela usa a mesma régua do robô (checar_stories.py).*\n",
         "| Data | Story | Reel de origem | Situação |", "|---|---|---|---|"]
    for d, iid, motivo in det["agenda"]:
        it = next(x for x in stn if x["id"] == iid)
        situ = "aprovada" + (" — **retomada** (só as partes que faltam)" if str(motivo).startswith("retomada") else "")
        L.append(f"| {DOW[d.weekday()]} {d:%d/%m} | `{iid}` | `{it.get('reel_ref')}` | {situ} |")
    pend = [x for x in stn if len(feitas.get(x.get("id"), {})) != len(CS.PAPEIS) and CS.aprovacao_de(x, aprov)[0] != "aprovada"]
    if det["bloqueio"]:
        L.append(f"| — | **BLOQUEADO** — {det['bloqueio']} | | |")
    elif not det["agenda"]:
        L.append(f"| — | **nenhum story projetado** ({len(stn)} na fila; {len(pend)} aguardando aprovação) | | |")
    if pend:
        L.append("\n**Aguardando aprovação do Rafael** (fora da conta: não saem e não travam as aprovadas):\n")
        for x in pend:
            v = CS.veredito(x, aprov, reels)
            render = [m for t, m in v["avisos"] if t == "render"]
            hip = PA.projeta_stories_detalhe(stn, st["published"], rp, hoje, ja, aprovacoes=aprov, reels_por_id=reels,
                                            aprovadas_extra=(x["id"],))
            quando = next((f"{DOW[d.weekday()]} {d:%d/%m}" for d, i, _ in hip["agenda"] if i == x["id"]), None)
            if quando is None:
                quando = f"não sai no horizonte ({hip['bloqueio']})" if hip["bloqueio"] else "fora do horizonte de 120 dias"
            L.append(f"- `{x['id']}` (reel `{x.get('reel_ref')}`): {v['situacao']} — {v['detalhe']}. "
                     f"Render: {render[0] if render else 'em dia'}. Se aprovada hoje (com o render do CI): {quando}."
                     + "".join(f" **ERRO no portão (CI vermelho):** {m}" for _, m in v["erros"]))
    return L


def secao_rodizio(fila, published, rp, hoje, ja_hoje=False):
    """Explicação do rodízio dos formatos novos + uma linha por formato (na fila, último publicado, próximas vagas) e
    as vagas de ter/qui/sáb que a projeção deixa SEM reel (falta de peça pronta)."""
    R = PA.regra_reels
    done = {e["id"] for e in published}
    ult = R.ultimas_por_formato({"published": published}, fila)
    fmt = {x["id"]: PA.formato(x) for x in fila}
    ini = R.INICIO_FORMATOS_NOVOS
    L = [f"*Regra (Rafael, 24-26/10/2026, regra_reels.py — a mesma do robô): **seg · qua · sex · dom = COMO FUNCIONA**; "
         f"**ter · qui · sáb = os 4 FORMATOS NOVOS em rodízio**, a partir de {ini:%d/%m/%Y} (antes disso, ter/qui/sáb sem reel). "
         "**Rodízio COM PESO (Rafael, 31/10, depois dos números: câmera lenta 25.612 de alcance em 1,8 dia):** "
         f"pesos {', '.join(f'{f} {w}' for f, w in R.pesos_formatos_novos().items())} — câmera lenta em 2 de cada 3 vagas, "
         "Chama o VAR na outra; Qual dos dois e Mito na prova são RESERVA (saem só quando os de peso > 0 estão sem peça). "
         "Todo formato faz a estreia antes de valer o peso; dentro do formato sai o 1º da fila. Formato sem peça pronta sai do rodízio até ganhar "
         "peça; vaga sem nenhuma peça pronta = sem reel nesse dia (o robô avisa, não é erro). Formato novo nunca ocupa "
         "seg/qua/sex/dom, e COMO FUNCIONA nunca ocupa ter/qui/sáb. 1 reel por dia.*\n",
         "| Formato novo | Na fila (pendentes) | Último publicado | Próximas vagas projetadas |", "|---|---|---|---|"]
    for f in R.FORMATOS_NOVOS:
        pend = sum(1 for x in fila if x["id"] not in done and fmt[x["id"]] == f)
        prox = [d for d, i in rp if fmt.get(i) == f][:3]
        L.append(f"| **{R.NOMES_FORMATOS[f]}** (`{f}`) | {pend} | "
                 f"{ult[f].strftime('%d/%m/%Y') if ult.get(f) else 'nunca'} | "
                 f"{', '.join(f'{DOW[d.weekday()]} {d:%d/%m}' for d in prox) or '— (sem peça pronta)'} |")
    projetados = {d for d, _ in rp}
    fim = max([d for d, _ in rp] + [hoje + dt.timedelta(days=14)])
    vazias, d = [], max(hoje + dt.timedelta(days=1 if ja_hoje else 0), ini)    # hoje já com reel: não é vaga
    while d <= fim:
        if R.grupo_do_dia(d) == R.GRUPO_NOVOS and d not in projetados:
            vazias.append(d)
        d += dt.timedelta(days=1)
    if vazias:
        L.append(f"\n**Vagas de formato novo SEM peça pronta (sem reel nesses dias) até {fim:%d/%m}: {len(vazias)}** — "
                 + ", ".join(f"{DOW[x.weekday()]} {x:%d/%m}" for x in vazias[:12])
                 + (f" e mais {len(vazias) - 12}" if len(vazias) > 12 else "")
                 + ". Cada peça pronta de formato novo anexada à fila ocupa a próxima vaga.\n")
    return L


def main():
    if any(os.environ.get(v) for v in ("LAMINAS_POR_SEMANA", "DIAS_ENTRE_CONVERSAS", "CONVERSAS_ATIVAS",
                                         "POSTS_ATIVOS", "SEQUENCIAS_ATIVAS", "STORIES_NOVOS_ATIVOS",
                                         "DIAS_ENTRE_MESMO_TEMA")):
        # a produção não lê variável (regra_reels.py é a fonte única); página gerada com outra cota mentiria
        raise SystemExit("ERRO: LAMINAS_POR_SEMANA está definida no ambiente local — a produção usa "
                         "regra_reels.LAMINAS_POR_SEMANA_PADRAO. Tire a variável e rode de novo.")
    hoje = dt.date.fromisoformat(sys.argv[1]) if len(sys.argv) > 1 else dt.datetime.now(PA.BRT).date()
    st = carrega("state/published.json"); done = {e["id"] for e in st["published"]}
    reels = [x for x in carrega("reels.json") if x["id"] not in done]
    posts = [x for x in carrega("posts.json") if x["id"] not in done]
    seqs = [x for x in carrega("sequences.json") if x["id"] not in done]
    fmt_de = {x["id"]: PA.formato(x) for x in carrega("reels.json")}
    cota = PA.cota_vigente()
    rp = PA.projeta_reels(carrega("reels.json"), st["published"], hoje, st.get("last_reel_date") == hoje.isoformat())
    projetados = {i for _, i in rp}
    # COMO FUNCIONA e formatos novos sempre saem: os que a projeção não alcança estão FORA do horizonte; lâmina e
    # conversa não projetadas estão PARADAS (suspensas ou na cota)
    sempre = ("como_funciona",) + tuple(PA.regra_reels.FORMATOS_NOVOS)
    fora = [x["id"] for x in reels if x["id"] not in projetados and PA.formato(x) in sempre]
    parados = [x for x in reels if x["id"] not in projetados and PA.formato(x) not in sempre]
    txt_cota = ("sem limite" if cota < 0 else "SUSPENSA (all-in COMO FUNCIONA, 24/10)" if cota == 0
                else f"no máximo {cota} vez(es) por semana")
    cc = PA.regra_reels.dias_entre_conversas()
    txt_conv = ("SUSPENSA (all-in COMO FUNCIONA, 24/10)" if not PA.regra_reels.conversas_ativas()
                else "sem intervalo mínimo" if cc <= 0 else f"no máximo 1 a cada {cc} dias")
    posts_on = PA.regra_reels.posts_ativos(); seqs_on = PA.regra_reels.sequencias_ativas()
    pp = projeta([x["id"] for x in posts], PA.POST_WEEKDAYS | PA.POST2_WEEKDAYS, hoje,
                 st.get("last_post_date") == hoje.isoformat()) if posts_on else []
    trial = {x["id"] for x in reels if x.get("trial")}
    L = [f"# PROGRAMAÇÃO — o que vai ao ar e quando\n",
         f"Regenerado em {hoje:%d/%m/%Y} por `_gen_programacao.py`. **Datas são projeção da fila FIFO** a partir do último publicado — job vermelho, alarme de curtidas ou mudança na fila desloca tudo; a fonte de verdade é a fila.\n",
         "**Como revisar/suspender (regra de 30/08):** os itens ficam dias na fila antes de publicar — confira por aqui; para suspender ou editar, avise o chat da auditoria (ou remova a entrada do JSON, com lock `motor-instagram`). Piloto ativo só para formato/estratégia NOVA ou mudança de voz.\n",
         "**Marcações:** `[TRIAL]` = publica só para não-seguidores e fora do grid (B5, 4 peças sorteadas); `[A]`/`[B]` = braço do teste de gancho (B4); `← capa v2` = primeiro reel com o template novo.\n",
         f"**Formatos (18/10/2026; formatos novos 26/10/2026):** COMO FUNCIONA, CONVERSA e os 4 formatos novos "
         f"({', '.join(PA.regra_reels.NOMES_FORMATOS[f] for f in PA.regra_reels.FORMATOS_NOVOS)}) são a geração nova (animação, sem rosto). "
         f"COMO FUNCIONA sai sem limite em seg/qua/sex/dom; os formatos novos revezam em ter/qui/sáb; a CONVERSA: {txt_conv}; "
         f"a lâmina antiga: {txt_cota} (regra_reels.py). Dia de reel sem peça permitida fica sem reel.\n",
         "\n## Reels (todos os dias, ~15h BRT)\n"]
    L += secao_rodizio(carrega("reels.json"), st["published"], rp, hoje, st.get("last_reel_date") == hoje.isoformat())
    L += ["\n| Data | Formato | Peça | Série | Vídeo |", "|---|---|---|---|---|"]
    braco = {"fx_sentar_levantar": "A", "fx_roupa": "A", "fx_pino_inflamado": "A", "fx_retirada": "A",
             "fx_kit_casa": "B", "fx_viagem": "B", "fx_curativo_pinos": "B", "fx_dormir": "B"}
    primeiro_v2 = True
    for d, iid in rp:
        tags = []
        if iid in trial: tags.append("**[TRIAL]**")
        if iid in braco: tags.append(f"[{braco[iid]}]")
        f = next((PA.formato(x) for x in reels if x["id"] == iid), "lamina")
        nome_f = PA.regra_reels.NOMES_FORMATOS.get(f, f.replace("_", " ").upper())
        v = next(x["video"] for x in reels if x["id"] == iid)
        serie = next((x.get("serie") for x in reels if x["id"] == iid and x.get("serie")), None) or serie_de(iid)
        L.append(f"| {DOW[d.weekday()]} {d:%d/%m} | **{nome_f}** | `{iid}` {' '.join(tags)} | {serie} | [▶ assistir]({RAW}{v}) |")
    if not rp:
        L.append("| — | | **nenhum reel projetado** | | |")
    if fora:
        L.append(f"\n*{len(fora)} COMO FUNCIONA / formato novo da fila FORA desta projeção (horizonte de 2 anos): "
                 f"{', '.join('`' + i + '`' for i in fora[:12])}{' …' if len(fora) > 12 else ''}*")
    if parados:
        nconv = sum(1 for x in parados if x.get("formato") == "conversa")
        L.append(f"\n*Parados na fila (all-in no formato novo, 24/10 — nada apagado, religar em regra_reels.py): "
                 f"{nconv} conversa(s) e {len(parados) - nconv} lâmina(s).*")
    L += ["\n## Posts de feed (ter · qui · sáb 15h · dom 11h)\n", "| Data | Peça | Nº imagens |", "|---|---|---|"]
    if not posts_on:
        L.append(f"| — | **SUSPENSOS** — all-in no formato novo (24/10); {len(posts)} carrossel(éis) estático(s) parado(s) na fila | |")
    for d, iid in pp:
        n = len(next(x["images"] for x in posts if x["id"] == iid))
        rot = " (verbete)" if iid.startswith("v_") else ""
        L.append(f"| {DOW[d.weekday()]} {d:%d/%m} | `{iid}`{rot} | {n} |")
    # stories da geração nova ("COMO FUNCIONA em 3 toques", roteiro próprio): a MESMA régua do robô
    # (checar_stories: incertas -> retomada do mesmo dia -> só aprovadas -> distância de tema -> portão)
    L += secao_stories(st, rp, hoje)
    if not seqs_on:
        L += [f"\n*Sequências de stories antigas: SUSPENSAS — all-in no formato novo (24/10); {len(seqs)} parada(s) na fila "
              "(os temas voltam como stories da geração nova).*\n"]
    else:
      L += [f"\n*Sequências de stories: {len(seqs)} restantes, publicadas ter/qui/sáb às 12:30, nos dias do carrossel (cadência reduzida em 12/09; a troca de dias de 13/09 foi revertida em 19/09 — o eixo de dia da semana estava deslocado um dia, ver E7). Quem edita a fila, regenera esta página.*\n"]
    with open(os.path.join(ROOT, "PROGRAMACAO.md"), "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(L))
    novos = sum(1 for _, i in rp if fmt_de.get(i, "lamina") != "lamina")
    rodizio = sum(1 for _, i in rp if fmt_de.get(i) in PA.regra_reels.FORMATOS_NOVOS)
    ate_r = f"até {rp[-1][0]:%d/%m}" if rp else "(nenhum projetado)"
    ate_p = f"até {pp[-1][0]:%d/%m}" if pp else "(nenhum)"
    print(f"PROGRAMACAO.md: {len(rp)} reels ({novos} da geração nova, {rodizio} dos 4 formatos novos em ter/qui/sáb) "
          f"{ate_r}, {len(fora)} fora da projeção | {len(pp)} posts {ate_p}")


if __name__ == "__main__":
    main()
