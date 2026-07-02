# -*- coding: utf-8 -*-
"""
GUARDRAIL DE CONTEÚDO — "termo técnico → nome popular" (lição @drtharikbrandao, auditoria v3).
O pai/paciente busca o SINTOMA (nome popular), não o diagnóstico. Então todo episódio que usa um
JARGÃO clínico deve trazer o nome popular — de preferência no GANCHO (cena 0) ou na legenda.

Este script é um LINT: varre os EPISODES e acusa, por episódio:
  - PROIBIDO: usa um termo VETADO (ex.: "dismetria") — trocar pelo correto ("discrepância de membro").
  - FALTA   : usa o jargão mas o nome popular NÃO aparece em lugar nenhum do episódio (corrigir).
  - SO_CORPO: o nome popular existe, mas não no gancho/legenda (onde capta busca) — melhorar.
  - OK       : jargão + nome popular presentes no gancho/legenda.
Rodar: python checar_termo_popular.py   (use PYTHONIOENCODING=utf-8 no Windows).

GLOSSÁRIO = jargão clínico (que leigo NÃO digita) -> nomes populares aceitos (o que o pai busca).
Termos que o leigo já busca (escoliose, displasia de quadril, pseudartrose) NÃO entram aqui — não
precisam de tradução. Estender este dict a cada lote novo.
"""
import re, unicodedata
from episodios_pe_no_chao import EPISODES

GLOSSARIO = {
    # — pediátrico (jargão que o pai não digita) —
    "geno valgo":        ["perna em x", "joelho em x"],
    "genovalgo":         ["perna em x", "joelho em x"],
    "geno varo":         ["perna arqueada", "pernas tortas", "perna de cowboy"],
    "marcha em equino":  ["ponta do pe", "ponta dos pes"],
    "equino":            ["ponta do pe", "ponta dos pes"],
    "metatarso aduto":   ["pe pra dentro", "pezinho pra dentro"],
    "metatarso varo":    ["pe pra dentro", "pezinho pra dentro"],
    "anteversao femoral":["pe pra dentro", "pes pra dentro"],
    "torcicolo":         ["so olha pra um lado", "so vira pra um lado", "pescoco torto"],
    "apofisite":         ["dor no calcanhar", "dor abaixo do joelho"],
    "osgood":            ["caroco", "abaixo do joelho"],
    "schlatter":         ["caroco", "abaixo do joelho"],
    "sever":             ["dor no calcanhar", "calcanhar"],
    "hipermobilidade":   ["elastica", "frouxa", "dobra demais", "flexivel"],
    "pe plano":          ["pe chato"],
    # — reconstrução (jargão que o paciente não digita) —
    "consolidacao viciosa": ["colou torto", "osso torto", "entortado"],
    "pseudartrose":         ["fratura que nao cola", "osso que nao cola", "nao cola"],
    # grafia canônica com "o" (o match é substring literal: uma grafia NÃO casa a outra)
    "pseudoartrose":        ["fratura que nao cola", "osso que nao cola", "nao cola"],
    "discrepancia":         ["perna mais curta", "uma perna mais curta", "perna curta"],
    "osteomielite":         ["infeccao no osso", "infeccao do osso", "infeccao"],
    "osteotomia":           ["cortar e realinhar", "realinhar", "muda o eixo", "corrige o eixo"],
    # "consolidação" (processo) -> o leigo diz "o osso/a fratura COLAR/colando/colou"
    "consolidacao":         ["colar", "cola ", "colando", "colou", "colam"],
}

# TERMOS PROIBIDOS — o médico NUNCA deve usar (regra de terminologia, memória `terminologia-ortopedica`).
# chave = termo vetado (detectado no conteúdo) -> valor = o termo CORRETO a usar no lugar.
PROIBIDOS = {
    "dismetria": "discrepância de membro (ou anisomelia)",
}

def norm(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()
    return s

def sem_hashtags(s):
    # hashtags (#pseudartrose etc.) são TAGS, não o conteúdo falado/na tela — não contam como jargão usado.
    return re.sub(r"#\S+", " ", s)

def textos(ep):
    s0 = ep["scenes"][0]
    gancho = " ".join([s0.get("k", "")] + s0.get("sc", []) + [s0.get("sub", "")])
    cap = sem_hashtags(ep.get("caption", ""))
    corpo = " ".join(
        " ".join([sc.get("k", "")] + sc.get("sc", []) + [sc.get("sub", ""), sc.get("vo", "")])
        for sc in ep["scenes"]
    )
    return norm(gancho), norm(cap), norm(corpo + " " + cap)

def main():
    faltas, so_corpo, ok, proibidos_uso = [], [], [], []
    for ep in EPISODES:
        ng, ncap, nfull = textos(ep)
        ngc = ng + " " + ncap  # gancho + legenda (onde captura busca)
        for termo, correto in PROIBIDOS.items():
            if norm(termo) in nfull:
                proibidos_uso.append((ep["id"], termo, correto))
        for jarg, pops in GLOSSARIO.items():
            if norm(jarg) not in nfull:
                continue
            no_gancho_legenda = any(p in ngc for p in pops)
            no_corpo = any(p in nfull for p in pops)
            if no_gancho_legenda:
                ok.append((ep["id"], jarg))
            elif no_corpo:
                so_corpo.append((ep["id"], jarg))
            else:
                faltas.append((ep["id"], jarg))
    print("=== LINT termo->popular | %d episodios ===" % len(EPISODES))
    if proibidos_uso:
        print("PROIBIDO (termo vetado usado no conteudo — TROCAR JA):", len(proibidos_uso))
        for i, t, c in proibidos_uso:
            print("   [PROIBIDO] %-26s '%s' -> usar '%s'" % (i, t, c))
    else:
        print("PROIBIDO (termos vetados no conteudo): 0")
    print("OK (jargao + popular no gancho/legenda):", len(ok))
    print("SO_CORPO (popular existe, mas fora do gancho/legenda):", len(so_corpo))
    for i, j in so_corpo:
        print("   [SO_CORPO] %-26s jargao=%s" % (i, j))
    print("FALTA (jargao sem nome popular no episodio):", len(faltas))
    for i, j in faltas:
        print("   [FALTA]    %-26s jargao=%s" % (i, j))
    return faltas, so_corpo

if __name__ == "__main__":
    main()
