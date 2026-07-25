# -*- coding: utf-8 -*-
"""
Auditoria de qualidade SEO de seo_episodios.json.
Uso: python _lint_seo.py [--strict] [eid1 eid2 ...]
  --strict   : falha com exit 1 se qualquer episódio < 90 pts.
  eid1 eid2  : filtrar episódios específicos.

Critérios verificados:
  1. Título ≥ 45 chars e ≤ 100 chars
  2. Título contém #Shorts
  3. Descrição ≥ 200 chars
  4. Descrição contém "pronto-socorro" ou "emergência" (CFM: sinal de alarme)
  5. Descrição contém "CRM-SP" (assinatura obrigatória)
  6. ≥ 10 tags únicas
  7. title_alt presente e diferente do title
  8. search_intent presente (≥ 1 item)
  9. title_alt entre 45 e 100 chars
 10. title_alt íntegro (sem corte no meio da palavra/parêntese)
 11. title_alt sem expressão duplicada

Isenção: os 28 episódios EP07-28 já publicados no canal não são cobrados no
critério 1 (comprimento mínimo do título) — ver TITULO_DO_CANAL abaixo. A isenção
aparece marcada na saída, nunca some em silêncio.
"""
import json, sys, os

sys.path.insert(0, os.path.dirname(__file__))
import seo_youtube as seo

JSON_PATH = os.path.join(os.path.dirname(__file__), "seo_episodios.json")


# ─── Sanidade do title_alt ──────────────────────────────────────────────────────
# title_alt é só sugestão de A/B — não vai para o ar sem o Rafael escolher. Mas se
# for escolhido, vai como está. Estas checagens pegam os dois defeitos que o motor
# já teve e que passaram batido enquanto o lint só olhava presença/diferença:
# corte cru no char 92 ("...(guia para os pai #Shorts") e expressão duplicada
# ("...no pós-operatório no pós-operatório — o que fazer").

def _corpo_alt(alt):
    """title_alt sem o sufixo ' #Shorts' — o texto que o motor de fato montou."""
    return alt[:-len(seo.SHORTS)] if alt.endswith(seo.SHORTS) else alt


def _alt_integro(alt):
    """False quando o texto tem cara de corte cru: parêntese aberto sem fechar
    (foi assim que '(guia para os pais)' virou '(guia para os pai') ou separador
    solto no fim."""
    corpo = _corpo_alt(alt)
    if corpo.count("(") != corpo.count(")"):
        return False
    return corpo == corpo.rstrip(seo._SEPARADORES)


def _alt_sem_duplicata(alt):
    """False quando alguma expressão de 2+ palavras aparece duas vezes no título."""
    palavras = seo._norm(_corpo_alt(alt)).split()
    bigramas = [" ".join(palavras[i:i + 2]) for i in range(len(palavras) - 1)]
    return len(bigramas) == len(set(bigramas))


RULES = [
    ("TITLE_LEN_MIN",  lambda e: len(e["title"]) >= seo.TITLE_MIN,
     f"título muito curto (< {seo.TITLE_MIN} chars; atual={{len_title}})"),
    ("TITLE_LEN_MAX",  lambda e: len(e["title"]) <= seo.TITLE_MAX,
     f"título muito longo (> {seo.TITLE_MAX} chars; atual={{len_title}})"),
    ("TITLE_SHORTS",   lambda e: "#shorts" in e["title"].lower(),
     "título sem #Shorts"),
    ("DESC_LEN",       lambda e: len(e["description"]) >= 200,
     "descrição curta (< 200 chars; atual={len_desc})"),
    ("DESC_ALARME",    lambda e: any(w in e["description"].lower()
                                     for w in ["pronto-socorro", "emergência", "emergencia"]),
     "descrição sem menção a pronto-socorro/emergência (CFM)"),
    ("DESC_CRM",       lambda e: "CRM-SP" in e["description"],
     "descrição sem assinatura CRM-SP (CFM)"),
    ("TAGS_COUNT",     lambda e: len(e.get("tags", [])) >= 10,
     "poucas tags (< 10; atual={n_tags})"),
    ("TITLE_ALT",      lambda e: e.get("title_alt") and e["title_alt"] != e["title"],
     "title_alt ausente ou igual ao title"),
    ("SEARCH_INTENT",  lambda e: bool(e.get("search_intent")),
     "search_intent ausente"),
    ("ALT_LEN_MIN",    lambda e: len(e.get("title_alt") or "") >= seo.TITLE_MIN,
     f"title_alt muito curto (< {seo.TITLE_MIN} chars; atual={{len_alt}})"),
    ("ALT_LEN_MAX",    lambda e: len(e.get("title_alt") or "") <= seo.TITLE_MAX,
     f"title_alt muito longo (> {seo.TITLE_MAX} chars; atual={{len_alt}})"),
    ("ALT_INTEGRO",    lambda e: _alt_integro(e.get("title_alt") or ""),
     "title_alt truncado (parêntese aberto ou separador solto no fim)"),
    ("ALT_SEM_DUP",    lambda e: _alt_sem_duplicata(e.get("title_alt") or ""),
     "title_alt com expressão duplicada"),
]

WEIGHTS = {
    "TITLE_LEN_MIN": 10, "TITLE_LEN_MAX": 15, "TITLE_SHORTS": 10,
    "DESC_LEN": 10, "DESC_ALARME": 15, "DESC_CRM": 20,
    "TAGS_COUNT": 10, "TITLE_ALT": 5, "SEARCH_INTENT": 5,
    "ALT_LEN_MIN": 5, "ALT_LEN_MAX": 5, "ALT_INTEGRO": 5, "ALT_SEM_DUP": 5,
}

# ─── Títulos preservados do canal (EP07-28) ─────────────────────────────────────
# Estes 28 vídeos já estão publicados no YouTube e o gerador preserva o `title`
# deles de propósito — ver _gen_seo_json.py: "não mudamos os títulos dos EP07-28
# existentes", e build_entry(), que copia o title da entrada existente.
# Alongá-los para bater os 45 chars significaria RENOMEAR vídeo no ar, perdendo o
# histórico de SEO. Então TITLE_LEN_MIN não se aplica a eles.
# Lista CONGELADA de propósito: episódio novo continua sendo cobrado normalmente.
TITULO_DO_CANAL = frozenset({
    "artrorrise",            "artrorrise_kids",
    "growth_guided",         "growth_guided_kids",
    "ferida_cirurgica",      "ferida_cirurgica_kids",
    "dor_posop",             "dor_posop_kids",
    "edema",                 "edema_kids",
    "infeccao_ferida",       "infeccao_ferida_kids",
    "tvp",                   "tvp_kids",
    "fisioterapia",          "fisioterapia_kids",
    "retorno_atividades",    "retorno_atividades_kids",
    "ortese_bota",           "ortese_bota_kids",
    "distracao_alongamento", "distracao_alongamento_kids",
    "consolidacao",          "consolidacao_kids",
    "retirada_fixador",      "retirada_fixador_kids",
    "banho_posop",           "banho_posop_kids",
})

# Só o comprimento mínimo é dispensado. Tudo que é CFM (DESC_ALARME, DESC_CRM) e
# o teto de 100 chars continuam valendo para todo mundo.
ISENCOES = frozenset({"TITLE_LEN_MIN"})


def _fmt(msg, e):
    return msg.format(
        len_title=len(e["title"]),
        len_desc=len(e["description"]),
        n_tags=len(e.get("tags", [])),
        len_alt=len(e.get("title_alt") or ""),
    )


def lint_entry(eid, e):
    issues = []
    isentos = []
    score = 100
    for name, check_fn, msg_tpl in RULES:
        if check_fn(e):
            continue
        if eid in TITULO_DO_CANAL and name in ISENCOES:
            isentos.append(name)
            continue
        issues.append((name, _fmt(msg_tpl, e)))
        score -= WEIGHTS.get(name, 10)
    return max(0, score), issues, isentos


def main():
    strict   = "--strict" in sys.argv
    filter_ids = [a for a in sys.argv[1:] if not a.startswith("--")]

    with open(JSON_PATH, encoding="utf-8") as f:
        data = json.load(f)

    if filter_ids:
        data = {k: v for k, v in data.items() if k in filter_ids}

    total = 0
    failed = 0
    all_issues = {}

    n_isentos = 0

    for eid, e in data.items():
        s, issues, isentos = lint_entry(eid, e)
        total += s
        flag = "OK " if not issues else ("WRN" if s >= 80 else "ERR")
        line = f"{flag}  {eid:<36} {s:3}/100  tags={len(e.get('tags',[])):2}"
        if isentos:
            n_isentos += 1
            line += f"  [isento: {', '.join(isentos)} — titulo publicado no canal]"
        print(line)
        if issues:
            for name, msg in issues:
                print(f"     [{name}] {msg}")
            all_issues[eid] = issues
            if s < 80:
                failed += 1

    n = len(data)
    print(f"\nMedia: {total // n}/100  ({n} episodios, {len(all_issues)} com issues, {n-len(all_issues)} perfeitos)")
    if n_isentos:
        print(f"Isentos de TITLE_LEN_MIN: {n_isentos} (titulo ja publicado no canal — nao penalizado)")

    if strict and failed > 0:
        print(f"[STRICT] {failed} episodios com score < 80 — EXIT 1", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
