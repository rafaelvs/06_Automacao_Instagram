# -*- coding: utf-8 -*-
"""
GUARDRAILS CFM 2.336/2023 — módulo COMPARTILHADO (IG, WhatsApp, qualquer canal público).
Unifica num só lugar as regras que estavam espalhadas/divergentes. Importável:

    from cfm_guardrails import auditar
    problemas = auditar(texto, contexto="publico")   # lista de (severidade, regra, detalhe)

Severidades: "VIOLACAO" (proibido — corrigir) e "REVISAR" (provável ok, mas conferir contexto).

Regras (Res. CFM 2.336/2023 + decisões do projeto):
  1. TERMO VETADO — "dismetria" (usar "discrepância de membro"/anisomelia). [memória terminologia-ortopedica]
  2. PROMESSA / SENSACIONALISMO — proibido prometer/insinuar resultado, "o melhor", "grátis".
  3. ESTÉTICA/ALTURA no ALONGAMENTO — tabu da área: alongamento ósseo nunca sob ângulo estético/altura.
  4. RAIO-X / EXAME DE IMAGEM — só ilustração/esquema didático; nunca exame real nem falso/realista.
  5. ASSINATURA — material público deve ter CRM + RQE ("Médico").
"""
import re
import unicodedata


def _norm(s):
    return unicodedata.normalize("NFKD", str(s)).encode("ascii", "ignore").decode().lower()


def _sem_hashtags(s):
    return re.sub(r"#\S+", " ", str(s))


# 1) Termos vetados (terminologia) -> correto
VETADOS = {
    "dismetria": 'discrepância de membro / anisomelia',
}

# 2) Promessa / sensacionalismo. Cada item: (regex_normalizado, detalhe)
PROMESSAS = [
    (r"\bgarant(o|e|em|ia|ido|ida|imos|ir|ira|irao|iremos)\b", "promessa de resultado ('garantir')"),
    (r"\bresultado garantido\b", "promessa de resultado"),
    (r"\bcura (garantida|definitiva|certa)\b", "promessa de cura"),
    (r"\b100% de (sucesso|cura|resultado)\b", "promessa absoluta"),
    (r"\bsem risco\b", "minimiza risco (sensacionalismo)"),
    (r"\bmilagr(e|oso|osa)\b", "sensacionalismo ('milagre')"),
    (r"\bo melhor (medico|cirurgiao|ortopedista|profissional)\b", "autopromoção ('o melhor')"),
    (r"\bnumero 1\b", "autopromoção ('número 1')"),
    (r"\bconsulta gratis\b", "'consulta grátis' (vedado)"),
]

# "antes e depois" NAO e VIOLACAO por si so: o Art. 14, II, b da Res. CFM 2.336/2023
# PERMITE antes-e-depois quando exibido como CONJUNTO (par de imagens, mesmo contexto,
# sem sensacionalizar). Rebaixado de VIOLACAO para REVISAR em 16/08/2026 (auditoria v1) —
# antes disso a regra travava a fila por engano em conteudo licito.
ANTES_DEPOIS_RGX = r"\bantes e depois\b"

# 2b) Negações que ANULAM uma "promessa" (ex.: "não prometo milagre" é honestidade, não violação)
NEG_PROMESSA = ["nao promet", "nao garant", "nao e ", "nao existe", "nada de", "longe de",
                "jamais", "nao oferec", "nao vendo", "nao faco", "sem promessa", "nunca promet",
                "nao fazem", "nao faz sentido", "sem ser", "nao significa", "nao quer dizer"]

# 3) Estética/altura no alongamento (precisa co-ocorrer alongamento + estética)
ALONG_GATILHO = ["alongament", "alongar o osso", "osso novo", "estatura", "transporte osseo"]
ESTETICA_TERMOS = ["estetic", "cosmetic", "ficar mais alto", "ganhar altura", "aumentar a altura",
                   "ficar mais alta", "questao de altura", "por beleza", "embelez", "vaidade",
                   # D17 (30/08/2026): o furo achado pela fábrica de verbetes — "estatura" era só
                   # GATILHO, então "alongamento para ganhar estatura" passava sem nenhum issue.
                   "ganhar estatura", "aumentar a estatura", "aumento de estatura",
                   "ficar alto", "ser mais alto", "questao de estatura"]
# negações/guardrail que tornam OK ("NÃO é sobre ficar mais alto", "nunca por estética")
NEGACAO = ["nao e sobre", "nao e por", "nunca ", "nao e estetic", "nao e questao de altura",
           "nada de estetic", "longe de estetic", "nao por vaidade", "nao e vaidade", "sem ser estetic",
           # D17: formas defensivas reais do acervo que a lista não conhecia (on_consolidacao_viciosa)
           "nao e questao de", "nao embelez", "nao a aparencia", "nao e aparencia", "nao e estetica"]

# 4) Exame de imagem
EXAME_TERMOS = ["raio-x", "raio x", "raiox", "radiografia", "tomografia", "ressonancia", "exame de imagem"]
EXAME_OK_CTX = ["ilustr", "esquem", "didatic", "desenho", "simbol", "no olhometro", "na imagem"]


def auditar(texto, contexto="publico", exigir_assinatura_texto=True):
    """contexto: 'publico' (post/legenda — exige assinatura) ou 'mensagem' (DM/bot — não exige).

    exigir_assinatura_texto: default True (post/reel — a legenda É o que o usuário lê, a
    assinatura ausente no texto é VIOLACAO). Passar False para conteúdo cuja legenda é só
    um rótulo estrutural curto e a identificação vive no RENDER (sequência/story — nenhuma
    das 150 sequências reais tem CRM em texto, é assim que o formato funciona): nesse caso
    a checagem vira REVISAR (advisório), não bloqueio. Sem essa distinção, promover a regra
    de REVISAR para VIOLACAO travaria toda sequência para sempre — achado do teste
    `test_publicacao.py` ao rodar com a promoção aplicada indiscriminadamente."""
    issues = []
    bruto = _sem_hashtags(texto)
    n = _norm(bruto)

    # 1) termos vetados
    for termo, correto in VETADOS.items():
        if _norm(termo) in n:
            issues.append(("VIOLACAO", "termo_vetado", f"'{termo}' -> usar '{correto}'"))

    # 2) promessas/sensacionalismo (pula casos NEGADOS — negação pode vir ANTES ou DEPOIS do gatilho:
    #    "não prometo milagre" / "milagre não existe" / "antes e depois não fazem sentido")
    for rgx, detalhe in PROMESSAS:
        for m in re.finditer(rgx, n):
            janela = n[max(0, m.start() - 35): m.end() + 45]
            if any(neg in janela for neg in NEG_PROMESSA):
                continue
            issues.append(("VIOLACAO", "promessa", detalhe))
            break

    # 2b) "antes e depois" isolado: REVISAR, nao VIOLACAO (ver ANTES_DEPOIS_RGX acima)
    for m in re.finditer(ANTES_DEPOIS_RGX, n):
        janela = n[max(0, m.start() - 35): m.end() + 45]
        if any(neg in janela for neg in NEG_PROMESSA):
            continue
        issues.append(("REVISAR", "antes_depois",
                       "'antes e depois' — confirmar que aparece como CONJUNTO (par de imagens, Art. 14 II b), não isolado/sensacionalizado"))
        break

    # 3) estética/altura no alongamento (co-ocorrência, exceto se houver negação/guardrail)
    if any(g in n for g in ALONG_GATILHO):
        for est in ESTETICA_TERMOS:
            if est in n:
                # acha a janela ao redor do termo estético; se houver negação perto, é guardrail (ok)
                idx = n.find(est)
                janela = n[max(0, idx - 60): idx + 40]
                if any(neg in janela for neg in NEGACAO):
                    continue  # é o próprio guardrail afirmando o tabu — ok
                # D17 (30/08/2026, decisão do Rafael): promovido de REVISAR para VIOLACAO —
                # o tabu estético/estatura é ABSOLUTO no projeto (regra transversal do
                # CLAUDE.md), e a lista NEGACAO já protege a menção defensiva. Espelha a
                # promoção da assinatura em 16/08: requisito objetivo não fica em advisório.
                issues.append(("VIOLACAO", "estetica_alongamento",
                               f"'{est}' perto de alongamento SEM negação — ângulo estético/altura é tabu absoluto"))

    # 4) exame de imagem sem contexto de ilustração
    for termo in EXAME_TERMOS:
        if termo in n:
            idx = n.find(termo)
            janela = n[max(0, idx - 80): idx + 80]
            if not any(ok in janela for ok in EXAME_OK_CTX):
                issues.append(("REVISAR", "exame_imagem",
                               f"'{termo}' sem contexto de ilustração/esquema — garantir que é só didático (nunca exame real/falso)"))

    # 5) assinatura CFM (só material público) — promovido de REVISAR para VIOLACAO em
    # 16/08/2026 (auditoria v1): e requisito OBJETIVAMENTE checavel (Arts. 4o/6o), nao
    # uma suspeita a confirmar. 91/183 legendas nao traziam a palavra "Médico" ate a
    # correção de 02/08; manter em REVISAR deixava passar sem alarme.
    if contexto == "publico":
        if not (("crm" in n) and ("rqe" in n)):
            sev = "VIOLACAO" if exigir_assinatura_texto else "REVISAR"
            issues.append((sev, "assinatura", "material público sem CRM+RQE visível no texto (pode estar no rodapé do render)"))

    return issues


if __name__ == "__main__":
    # smoke test
    casos = [
        ("Garanto a cura da sua dismetria!", "publico"),
        ("Alongamento ósseo pra ficar mais alto", "publico"),               # D17: tem de dar VIOLACAO
        ("Alongamento estético para ganhar estatura", "publico"),           # D17: o furo original — VIOLACAO
        ("Alongamento NÃO é sobre ficar mais alto — é função.", "publico"),  # negação: sem issue de estética
        ("Vou pedir um raio-x", "publico"),
        ("o esquema do raio-x didático mostra...", "publico"),
        ("Discrepância de membro: medir antes. CRM-SP 226103 RQE 137901", "publico"),
    ]
    for t, ctx in casos:
        print(repr(t[:45]), "->", auditar(t, ctx))
