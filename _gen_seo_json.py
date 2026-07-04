# -*- coding: utf-8 -*-
"""
Gera / atualiza seo_episodios.json a partir dos dados canônicos deste arquivo.
Uso: python _gen_seo_json.py [--dry]
  --dry  : imprime o JSON sem salvar.

Cada entrada define: foco, hook, pontos, hashtags, fontes.
O script usa seo_youtube.gerar() para produzir title/title_alt/description/tags/search_intent.
Entradas já existentes: descrição PRESERVADA do JSON original (não regera hook/pontos para não
sobrescrever edições manuais anteriores). Só tags e title_alt são regenerados via motor.

Para EP01-06 (novos): conteúdo escrito aqui com base nos roteiros de episodios_pos_op.py.
"""
import json, sys, os
sys.path.insert(0, os.path.dirname(__file__))
import seo_youtube as seo

JSON_PATH = os.path.join(os.path.dirname(__file__), "seo_episodios.json")

# ─── MAPA foco por episódio (usado para tags + title_alt) ────────────────────────────────────
# Derivado dos títulos já publicados no canal (não mudamos os títulos dos EP07-28 existentes).
FOCO = {
    # EP01-06 (novos)
    "gesso_pos_op":               "Gesso no pós-operatório",
    "gesso_pos_op_kids":          "Gesso em criança",
    "fixador_externo":            "Fixador externo",
    "fixador_externo_kids":       "Fixador externo em criança",
    "carga_fisio":                "Mobilização e fisioterapia precoce",
    "carga_fisio_kids":           "Mobilização e fisioterapia na criança",
    # EP07-28 (preservam título original — só atualizamos tags/title_alt)
    "artrorrise":                 "Artrorrise",
    "artrorrise_kids":            "Artrorrise em criança",
    "growth_guided":              "Guia de crescimento ósseo",
    "growth_guided_kids":         "Guia de crescimento em criança",
    "ferida_cirurgica":           "Cuidado com a ferida cirúrgica",
    "ferida_cirurgica_kids":      "Ferida cirúrgica em criança",
    "dor_posop":                  "Dor no pós-operatório",
    "dor_posop_kids":             "Dor pós-cirurgia em criança",
    "edema":                      "Edema após cirurgia",
    "edema_kids":                 "Edema após cirurgia em criança",
    "infeccao_ferida":            "Infecção de ferida cirúrgica",
    "infeccao_ferida_kids":       "Infecção de ferida em criança",
    "tvp":                        "TVP após cirurgia ortopédica",
    "tvp_kids":                   "TVP em criança após cirurgia",
    "fisioterapia":               "Fisioterapia no pós-operatório",
    "fisioterapia_kids":          "Fisioterapia em criança operada no pós-operatório",
    "retorno_atividades":         "Retorno às atividades após cirurgia",
    "retorno_atividades_kids":    "Retorno às atividades da criança",
    "ortese_bota":                "Bota ortopédica no pós-operatório",
    "ortese_bota_kids":           "Bota ortopédica em criança no pós-operatório",
    "distracao_alongamento":      "Distração e alongamento ósseo no pós-operatório",
    "distracao_alongamento_kids": "Alongamento ósseo em criança",
    "consolidacao":               "Consolidação óssea",
    "consolidacao_kids":          "Consolidação óssea em criança",
    "retirada_fixador":           "Retirada do fixador externo",
    "retirada_fixador_kids":      "Retirada do fixador em criança",
    "banho_posop":                "Banho após cirurgia ortopédica",
    "banho_posop_kids":           "Banho de criança após cirurgia",
}

# ─── ENTRADAS NOVAS: EP01-06 ─────────────────────────────────────────────────────────────────
# Conteúdo extraído dos roteiros de episodios_pos_op.py + adaptado para descrição YouTube.
_NEW_ENTRIES_DATA = {
    "gesso_pos_op": dict(
        hook="Saiu de gesso depois da cirurgia? Os cuidados que protegem o resultado — e os sinais que mandam você ao pronto-socorro.",
        pontos=[
            "Em repouso, eleve o membro acima do coração durante toda a recuperação.",
            "Gesso não pode molhar: capa impermeável é a opção mais segura.",
            "Dedos roxos, frios, com formigamento, ou gesso apertando cada vez mais: pronto-socorro.",
        ],
        hashtags="#Shorts #gesso #posoperatorio #ortopedia #drrafaelvargas",
        fontes=["https://orthoinfo.aaos.org", "https://sbot.org.br"],
    ),
    "gesso_pos_op_kids": dict(
        hook="Seu filho saiu de gesso depois da cirurgia? Veja os cuidados específicos da criança — e os sinais de alarme que pedem o pronto-socorro.",
        pontos=[
            "Eleve o membro da criança em repouso — acima do coração, em toda a recuperação.",
            "Evite que a criança enfie objetos no gesso; cubra a abertura da extremidade.",
            "Criança mais agitada que antes, ou com dedos roxos e frios: pronto-socorro imediato.",
        ],
        hashtags="#Shorts #gesso #ortopediapediatrica #criancaoperada #drrafaelvargas",
        fontes=["https://orthoinfo.aaos.org", "https://sbot.org.br", "https://sbcp.org.br"],
    ),
    "fixador_externo": dict(
        hook="Saiu da cirurgia com fixador externo? Cuidar dos pinos evita a complicação mais comum — a infecção.",
        pontos=[
            "Lave os pinos no banho com sabonete neutro — um material por pino, nunca cruzando a limpeza.",
            "Seque bem cada pino; aplique álcool 70% só no metal, nunca na pele.",
            "Vermelhidão, calor, secreção, pino frouxo ou febre: pronto-socorro.",
        ],
        hashtags="#Shorts #fixadorexterno #ilizarov #ortopedia #drrafaelvargas",
        fontes=["https://orthoinfo.aaos.org", "https://sbot.org.br"],
    ),
    "fixador_externo_kids": dict(
        hook="Seu filho está com fixador externo? O cuidado com os pinos evita a complicação mais comum na criança — a infecção.",
        pontos=[
            "Lave os pinos no banho com sabonete neutro; mãos lavadas e luva limpa antes de tocar.",
            "Um material por pino — o que secou um pino não toca o outro.",
            "Criança prostrada, com febre, ou pino com secreção: pronto-socorro.",
        ],
        hashtags="#Shorts #fixadorexterno #ortopediapediatrica #ilizarovinfantil #drrafaelvargas",
        fontes=["https://orthoinfo.aaos.org", "https://sbot.org.br", "https://sbcp.org.br"],
    ),
    "carga_fisio": dict(
        hook="Operou e tem medo de mexer? No ritmo que a sua equipe liberar, o movimento é parte do tratamento — não o inimigo.",
        pontos=[
            "Imobilidade excessiva perde força e enrijece a articulação — o oposto do que você precisa.",
            "Fisioterapia não é opcional: é parte do tratamento; começar no momento certo define a amplitude.",
            "Dor crescente ou inchaço que piora ao se mover: não force — e pronto-socorro se for sinal de alarme.",
        ],
        hashtags="#Shorts #fisioterapia #posoperatorio #mobilizacaoprecoce #drrafaelvargas",
        fontes=["https://orthoinfo.aaos.org", "https://sbot.org.br"],
    ),
    "carga_fisio_kids": dict(
        hook="Seu filho operou e você tem medo de deixar mexer? No ritmo da equipe, o movimento é parte do tratamento da criança.",
        pontos=[
            "Criança parada demais perde força e amplitude — o corpo dela responde rápido ao movimento.",
            "Fisioterapia em criança vira brincadeira guiada: aumenta a adesão e o resultado.",
            "Dor que aumenta muito ou criança prostrada: não force o movimento — pronto-socorro se necessário.",
        ],
        hashtags="#Shorts #fisioterapia #ortopediapediatrica #reabilitacaopediatrica #drrafaelvargas",
        fontes=["https://orthoinfo.aaos.org", "https://sbot.org.br", "https://sbcp.org.br"],
    ),
}

# ─── LÓGICA PRINCIPAL ────────────────────────────────────────────────────────────────────────
def build_entry(eid, existing_entry=None, new_data=None):
    """Constrói uma entrada do JSON para o episódio eid.
    Se existing_entry: preserva title e description originais; atualiza tags + adiciona campos.
    Se new_data: cria entry completa via seo_youtube.gerar()."""
    ep = {"id": eid}
    kids = seo._is_kids(eid)
    foco = FOCO[eid]

    if existing_entry and new_data is None:
        # Episódio já existente: preservar title e description; regenerar tags + adicionar title_alt
        title = existing_entry["title"]
        desc  = existing_entry["description"]
        new_tags = seo.tags(foco, kids, eid)
        title_alt = seo.titulo_alt(ep, foco, avoid=title)
        si = seo.search_intent(eid)
        entry = {
            "title":          title,
            "title_alt":      title_alt,
            "description":    desc,
            "tags":           new_tags,
            "search_intent":  si,
        }
    else:
        # Episódio novo: gerar via motor
        d = new_data
        out = seo.gerar(ep, foco, d["hook"], d["pontos"], d["hashtags"], d.get("fontes"))
        entry = {
            "title":         out["title"],
            "title_alt":     out["title_alt"],
            "description":   out["description"],
            "tags":          out["tags"],
            "search_intent": out["search_intent"],
        }
    return entry


def main():
    dry = "--dry" in sys.argv

    # Carregar JSON existente
    with open(JSON_PATH, encoding="utf-8") as f:
        existing = json.load(f)

    # Ordem canônica dos episódios (EP01-34)
    ORDER = [
        "gesso_pos_op", "gesso_pos_op_kids",
        "fixador_externo", "fixador_externo_kids",
        "carga_fisio", "carga_fisio_kids",
        "artrorrise", "artrorrise_kids",
        "growth_guided", "growth_guided_kids",
        "ferida_cirurgica", "ferida_cirurgica_kids",
        "dor_posop", "dor_posop_kids",
        "edema", "edema_kids",
        "infeccao_ferida", "infeccao_ferida_kids",
        "tvp", "tvp_kids",
        "fisioterapia", "fisioterapia_kids",
        "retorno_atividades", "retorno_atividades_kids",
        "ortese_bota", "ortese_bota_kids",
        "distracao_alongamento", "distracao_alongamento_kids",
        "consolidacao", "consolidacao_kids",
        "retirada_fixador", "retirada_fixador_kids",
        "banho_posop", "banho_posop_kids",
    ]

    result = {}
    for eid in ORDER:
        if eid in existing:
            result[eid] = build_entry(eid, existing_entry=existing[eid])
        elif eid in _NEW_ENTRIES_DATA:
            result[eid] = build_entry(eid, new_data=_NEW_ENTRIES_DATA[eid])
        else:
            print(f"[AVISO] {eid} não encontrado em JSON nem em _NEW_ENTRIES_DATA — pulando.", file=sys.stderr)

    out_json = json.dumps(result, ensure_ascii=False, indent=2)

    if dry:
        print(out_json)
    else:
        with open(JSON_PATH, "w", encoding="utf-8") as f:
            f.write(out_json + "\n")
        print(f"[OK] seo_episodios.json atualizado — {len(result)} entradas.")

    # Relatório de qualidade
    print("\n── SCORE SEO (todos os episódios) ──")
    total = 0
    for eid, e in result.items():
        s, issues = seo.score_seo(e["title"], e["description"], e["tags"])
        total += s
        flag = "✅" if s >= 80 else ("⚠️ " if s >= 60 else "❌")
        prefix = f"{flag} {eid:<32} {s:3}/100"
        if issues:
            print(prefix, " | issues:", "; ".join(issues))
        else:
            print(prefix)
    print(f"\nMédia: {total//len(result)}/100  ({len(result)} eps)")


if __name__ == "__main__":
    main()
