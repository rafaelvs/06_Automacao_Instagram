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
    (r"\bantes e depois\b", "'antes e depois' (sensacionalismo/identificável)"),
]

# 2b) Negações que ANULAM uma "promessa" (ex.: "não prometo milagre" é honestidade, não violação)
NEG_PROMESSA = ["nao promet", "nao garant", "nao e ", "nao existe", "nada de", "longe de",
                "jamais", "nao oferec", "nao vendo", "nao faco", "sem promessa", "nunca promet",
                "nao fazem", "nao faz sentido", "sem ser", "nao significa", "nao quer dizer"]

# 3) Estética/altura no alongamento (precisa co-ocorrer alongamento + estética)
ALONG_GATILHO = ["alongament", "alongar o osso", "osso novo", "estatura", "transporte osseo"]
ESTETICA_TERMOS = ["estetic", "cosmetic", "ficar mais alto", "ganhar altura", "aumentar a altura",
                   "ficar mais alta", "questao de altura", "por beleza", "embelez", "vaidade"]
# negações/guardrail que tornam OK ("NÃO é sobre ficar mais alto", "nunca por estética")
NEGACAO = ["nao e sobre", "nao e por", "nunca ", "nao e estetic", "nao e questao de altura",
           "nada de estetic", "longe de estetic", "nao por vaidade", "nao e vaidade", "sem ser estetic"]

# 4) Exame de imagem
EXAME_TERMOS = ["raio-x", "raio x", "raiox", "radiografia", "tomografia", "ressonancia", "exame de imagem"]
EXAME_OK_CTX = ["ilustr", "esquem", "didatic", "desenho", "simbol", "no olhometro", "na imagem"]


def auditar(texto, contexto="publico"):
    """contexto: 'publico' (post/legenda — exige assinatura) ou 'mensagem' (DM/bot — não exige)."""
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

    # 3) estética/altura no alongamento (co-ocorrência, exceto se houver negação/guardrail)
    if any(g in n for g in ALONG_GATILHO):
        for est in ESTETICA_TERMOS:
            if est in n:
                # acha a janela ao redor do termo estético; se houver negação perto, é guardrail (ok)
                idx = n.find(est)
                janela = n[max(0, idx - 60): idx + 40]
                if any(neg in janela for neg in NEGACAO):
                    continue  # é o próprio guardrail afirmando o tabu — ok
                issues.append(("REVISAR", "estetica_alongamento",
                               f"'{est}' perto de alongamento — confirmar que NÃO é ângulo estético/altura"))

    # 4) exame de imagem sem contexto de ilustração
    for termo in EXAME_TERMOS:
        if termo in n:
            idx = n.find(termo)
            janela = n[max(0, idx - 80): idx + 80]
            if not any(ok in janela for ok in EXAME_OK_CTX):
                issues.append(("REVISAR", "exame_imagem",
                               f"'{termo}' sem contexto de ilustração/esquema — garantir que é só didático (nunca exame real/falso)"))

    # 5) assinatura CFM (só material público)
    if contexto == "publico":
        if not (("crm" in n) and ("rqe" in n)):
            issues.append(("REVISAR", "assinatura", "material público sem CRM+RQE visível no texto (pode estar no rodapé do render)"))

    return issues


if __name__ == "__main__":
    # smoke test
    casos = [
        ("Garanto a cura da sua dismetria!", "publico"),
        ("Alongamento ósseo pra ficar mais alto", "publico"),
        ("Alongamento NÃO é sobre ficar mais alto — é função.", "publico"),
        ("Vou pedir um raio-x", "publico"),
        ("o esquema do raio-x didático mostra...", "publico"),
        ("Discrepância de membro: medir antes. CRM-SP 226103 RQE 137901", "publico"),
    ]
    for t, ctx in casos:
        print(repr(t[:45]), "->", auditar(t, ctx))
