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
"""
import json, sys, os

sys.path.insert(0, os.path.dirname(__file__))
import seo_youtube as seo

JSON_PATH = os.path.join(os.path.dirname(__file__), "seo_episodios.json")

RULES = [
    ("TITLE_LEN_MIN",  lambda e: len(e["title"]) >= 45,
     "título muito curto (< 45 chars; atual={len_title})"),
    ("TITLE_LEN_MAX",  lambda e: len(e["title"]) <= 100,
     "título muito longo (> 100 chars; atual={len_title})"),
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
]

WEIGHTS = {
    "TITLE_LEN_MIN": 10, "TITLE_LEN_MAX": 15, "TITLE_SHORTS": 10,
    "DESC_LEN": 10, "DESC_ALARME": 15, "DESC_CRM": 20,
    "TAGS_COUNT": 10, "TITLE_ALT": 5, "SEARCH_INTENT": 5,
}


def _fmt(msg, e):
    return msg.format(
        len_title=len(e["title"]),
        len_desc=len(e["description"]),
        n_tags=len(e.get("tags", [])),
    )


def lint_entry(eid, e):
    issues = []
    score = 100
    for name, check_fn, msg_tpl in RULES:
        if not check_fn(e):
            issues.append((name, _fmt(msg_tpl, e)))
            score -= WEIGHTS.get(name, 10)
    return max(0, score), issues


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

    for eid, e in data.items():
        s, issues = lint_entry(eid, e)
        total += s
        flag = "OK " if not issues else ("WRN" if s >= 80 else "ERR")
        line = f"{flag}  {eid:<36} {s:3}/100  tags={len(e.get('tags',[])):2}"
        if issues:
            print(line)
            for name, msg in issues:
                print(f"     [{name}] {msg}")
            all_issues[eid] = issues
            if s < 80:
                failed += 1
        else:
            print(line)

    n = len(data)
    print(f"\nMedia: {total // n}/100  ({n} episodios, {len(all_issues)} com issues, {n-len(all_issues)} perfeitos)")

    if strict and failed > 0:
        print(f"[STRICT] {failed} episodios com score < 80 — EXIT 1", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
