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
  3. AUTOPROMOÇÃO COMPARATIVA — posicionar-se contra outros profissionais ("o que outros
     não resolveram", "não há mais o que fazer").
  4. ESTÉTICA/ALTURA no ALONGAMENTO — tabu da área: alongamento ósseo nunca sob ângulo estético/altura.
  5. RAIO-X / EXAME DE IMAGEM — só ilustração/esquema didático; nunca exame real nem falso/realista.
  6. ASSINATURA — material público deve ter CRM + RQE ("Médico").

A bateria adversarial vive em testes_guardrails.py. Alterou regra aqui? Rode lá:
GAP tem que cair e FALSO_POSITIVO tem que continuar zero.
"""
import re
import unicodedata


def _norm(s):
    return unicodedata.normalize("NFKD", str(s)).encode("ascii", "ignore").decode().lower()


def _sem_hashtags(s):
    """Mantido para compatibilidade com quem importa. NÃO usar como pré-processamento de
    auditoria: apagar a hashtag cria ponto cego — hashtag é texto público e indexável."""
    return re.sub(r"#\S+", " ", str(s))


def _texto_auditavel(s):
    """Texto que vai para as regras de palavra. O '#' vira espaço em vez de apagar a
    hashtag inteira: '#dismetria' precisa ser auditado como 'dismetria'."""
    return str(s).replace("#", " ")


def _corpos_hashtag(s):
    r"""Corpos das hashtags, normalizados e SEM separador. Hashtag costuma vir concatenada
    ('#resultadogarantido'), forma em que \b nunca casa — por isso estes corpos são
    testados por SUBSTRING (ver HASHTAG_SUSPEITA), não por limite de palavra."""
    return [_norm(h) for h in re.findall(r"#(\w+)", str(s))]


# 1) Termos vetados (terminologia) -> correto
VETADOS = {
    "dismetria": 'discrepância de membro / anisomelia',
}

# 2) Promessa / sensacionalismo. Cada item: (regex_normalizado, detalhe)
PROMESSAS = [
    # Stem aberto. A versão anterior listava flexão por flexão e deixava passar
    # 'garantidos', 'garantidas', 'garantiu', 'garantiram', 'garantindo'.
    (r"\bgarant[a-z]*\b", "promessa de resultado ('garantir')"),
    (r"\bcura (garantida|definitiva|certa|total)\b", "promessa de cura"),
    # Antes só casava '100% de (sucesso|cura|resultado)'; '100% dos casos',
    # '100% de eficácia' e '100% segura' passavam.
    (r"\b100% (?:d[eoa]s? )?(sucesso|cura|curas|resultado|resultados|casos|pacientes|"
     r"eficacia|eficaz|seguro|segura|seguranca|garantido|garantida|indolor)\b",
     "promessa absoluta ('100%')"),
    # Antes só '\bsem risco\b' (singular exato). Cobre plural e as inversões.
    (r"\b(sem|nenhum|zero) riscos?\b", "minimiza risco (sensacionalismo)"),
    (r"\brisco zero\b", "minimiza risco (sensacionalismo)"),
    (r"\bmilagr(e|es|oso|osa|osos|osas)\b", "sensacionalismo ('milagre')"),
    (r"\bo (melhor|maior|unico|mais experiente) (medico|cirurgiao|ortopedista|"
     r"profissional|especialista)\b", "autopromoção (superlativo)"),
    (r"\bnumero 1\b", "autopromoção ('número 1')"),
    (r"\bconsulta gratis\b", "'consulta grátis' (vedado)"),
    # Variantes: 'antes e depois', 'antes x depois', 'antes/depois', 'antes vs depois'.
    (r"\bantes\s*(?:e|x|/|vs\.?|versus)\s*depois\b",
     "'antes e depois' (sensacionalismo/identificável)"),
]

# 2b) Fragmentos suspeitos DENTRO de hashtag concatenada. Testados por substring porque
# em '#resultadogarantido' não existe limite de palavra para \b encontrar.
HASHTAG_SUSPEITA = [
    ("garant", "promessa de resultado"),
    ("milagr", "sensacionalismo ('milagre')"),
    ("semrisco", "minimiza risco"),
    ("riscozero", "minimiza risco"),
    ("curadefinitiva", "promessa de cura"),
    ("antesedepois", "'antes e depois'"),
    ("melhormedico", "autopromoção"),
    ("numero1", "autopromoção"),
]

# 2c) Negações que ANULAM uma "promessa" (ex.: "não prometo milagre" é honestidade).
# A versão anterior continha "nao e " — seis caracteres genéricos que anulavam QUALQUER
# promessa num raio de 45 chars, mesmo sem relação semântica: "não é caro: garanto o
# resultado" passava limpo. Trocado por negações ancoradas no que está sendo negado.
NEG_PROMESSA = ["nao promet", "nao garant", "nao existe", "nada de", "longe de",
                "jamais", "nao oferec", "nao vendo", "nao faco", "sem promessa",
                "nunca promet", "nao fazem", "nao faz sentido", "sem ser",
                "nao significa", "nao quer dizer", "nao e milagr", "nao e garantia",
                "nao e cura", "nao e promessa", "nao e sobre", "nao e por",
                "nao ha garantia", "nenhuma garantia"]

# 3) Autopromoção comparativa — REGRA NOVA. Não existia: a transcrição das imagens
# revelou dest04 ("O que outros não resolveram") e story07 ("Já ouviu 'não há mais o
# que fazer'?"), que passavam limpos por TODAS as 10 regex de PROMESSAS.
#
# Duas famílias, com tratamento DIFERENTE — a primeira versão desta regra tratava as
# duas igual e errou feio: sinalizou 13 itens, dos quais 12 eram o material que educa
# CONTRA o enquadramento (episódios do tipo "manda pra quem acha que não tem jeito" e
# a temporada "Mito x Verdade"). Ruído desse tamanho enterra o achado real.
#
# FORTE: posicionamento em 1ª pessoa contra outros profissionais. Não tem leitura
# inocente — sem filtro de contexto.
AUTOPROMOCAO_FORTE = [
    (r"\b(o que|que) (outros|os outros|ninguem|outro medico|outros medicos) "
     r"nao (resolveu|resolveram|resolve|resolvem|conseguiu|conseguiram|fez|fizeram|quis|quiseram)\b",
     "comparação com outros profissionais"),
    (r"\bonde (outros|os outros|todos) (falharam|falhou|desistiram|desistiu)\b",
     "comparação com outros profissionais"),
    (r"\boutros (medicos|profissionais|colegas|ortopedistas) (nao|recusaram|desistiram|erraram)\b",
     "comparação com outros profissionais"),
]

# CASO PERDIDO: aqui a FRASE não revela a POSTURA. Medida no conteúdo real, ela aparece
# majoritariamente sendo contrariada. Por isso tem filtro de contexto.
AUTOPROMOCAO_CASO_PERDIDO = [
    (r"\bnao ha mais (o que fazer|nada a fazer)\b", "apelo ao 'caso perdido'"),
    (r"\bnao ha o que fazer\b", "apelo ao 'caso perdido'"),
    (r"\bnao tem (mais )?(solucao|jeito|conserto)\b", "apelo ao 'caso perdido'"),
    (r"\b(disseram|falaram|te disseram) que nao (tinha|havia|tem|ha)\b", "apelo ao 'caso perdido'"),
]
# Marcadores de que a frase está sendo ATRIBUÍDA a terceiros para ser contrariada
# ("quem acha que não tem jeito") ou explicitamente rotulada como mito — e não usada
# como gancho promocional. NÃO incluir marcadores de esperança ("existe caminho"):
# story07 usa exatamente isso e o Rafael quer continuar vendo story07.
CASO_PERDIDO_CTX_OK = ["acha que", "acham que", "achando que", "quem acha", "mito"]

# 4) Estética/altura no alongamento (precisa co-ocorrer alongamento + estética)
ALONG_GATILHO = ["alongament", "alongar o osso", "osso novo", "estatura", "transporte osseo"]
ESTETICA_TERMOS = ["estetic", "cosmetic", "ficar mais alto", "ganhar altura", "aumentar a altura",
                   "ficar mais alta", "questao de altura", "por beleza", "embelez", "vaidade"]
# negações/guardrail que tornam OK ("NÃO é sobre ficar mais alto", "nunca por estética")
NEGACAO = ["nao e sobre", "nao e por", "nunca ", "nao e estetic", "nao e questao de altura",
           "nada de estetic", "longe de estetic", "nao por vaidade", "nao e vaidade", "sem ser estetic"]

# 5) Exame de imagem
EXAME_TERMOS = ["raio-x", "raio x", "raiox", "radiografia", "tomografia", "ressonancia", "exame de imagem"]
# "na imagem" foi REMOVIDO desta lista: é expressão banal ("como se vê na imagem") que
# aparece em qualquer legenda apontando para a própria arte, e liberava exame REAL.
EXAME_OK_CTX = ["ilustr", "esquem", "didatic", "desenho", "simbol", "no olhometro"]


def auditar(texto, contexto="publico"):
    """contexto: 'publico' (post/legenda — exige assinatura) ou 'mensagem' (DM/bot — não exige)."""
    issues = []
    n = _norm(_texto_auditavel(texto))
    hashtags = _corpos_hashtag(texto)

    # 1) termos vetados — no corpo E dentro de hashtag concatenada
    for termo, correto in VETADOS.items():
        t = _norm(termo)
        if (t in n) or any(t in h for h in hashtags):
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

    # 2b) promessa escondida em hashtag concatenada, onde \b nunca casa.
    #     Sem janela de negação: hashtag não carrega contexto que possa negar.
    for h in hashtags:
        for frag, detalhe in HASHTAG_SUSPEITA:
            if frag in h:
                issues.append(("VIOLACAO", "promessa", f"{detalhe} — em hashtag '#{h}'"))
                break

    # 3) autopromoção comparativa — família FORTE sem filtro; família 'caso perdido'
    #    anulada por marcador de crença alheia / desmistificação.
    for rgx, detalhe in AUTOPROMOCAO_FORTE:
        if re.search(rgx, n):
            issues.append(("VIOLACAO", "autopromocao", detalhe))
    for rgx, detalhe in AUTOPROMOCAO_CASO_PERDIDO:
        for m in re.finditer(rgx, n):
            janela = n[max(0, m.start() - 60): m.end() + 60]
            if any(ok in janela for ok in CASO_PERDIDO_CTX_OK):
                continue  # frase citada para ser contrariada — é o oposto do achado
            issues.append(("VIOLACAO", "autopromocao", detalhe))
            break

    # 4) estética/altura no alongamento (co-ocorrência, exceto se houver negação/guardrail).
    #    Antes usava n.find(): só a PRIMEIRA ocorrência era avaliada, então um primeiro uso
    #    negado ("não é sobre estética") blindava todos os usos reais seguintes.
    if any(g in n for g in ALONG_GATILHO):
        for est in ESTETICA_TERMOS:
            for m in re.finditer(re.escape(est), n):
                janela = n[max(0, m.start() - 60): m.start() + 40]
                if any(neg in janela for neg in NEGACAO):
                    continue  # é o próprio guardrail afirmando o tabu — ok
                issues.append(("REVISAR", "estetica_alongamento",
                               f"'{est}' perto de alongamento — confirmar que NÃO é ângulo estético/altura"))
                break

    # 5) exame de imagem sem contexto de ilustração. Mesma correção do find(): todas as
    #    ocorrências do termo, não só a primeira.
    for termo in EXAME_TERMOS:
        for m in re.finditer(re.escape(termo), n):
            janela = n[max(0, m.start() - 80): m.start() + 80]
            if any(ok in janela for ok in EXAME_OK_CTX):
                continue
            issues.append(("REVISAR", "exame_imagem",
                           f"'{termo}' sem contexto de ilustração/esquema — garantir que é só didático (nunca exame real/falso)"))
            break

    # 6) assinatura CFM (só material público)
    if contexto == "publico":
        if not (("crm" in n) and ("rqe" in n)):
            issues.append(("REVISAR", "assinatura", "material público sem CRM+RQE visível no texto (pode estar no rodapé do render)"))

    return issues


if __name__ == "__main__":
    print("Os casos de teste vivem em testes_guardrails.py (bateria adversarial).")
    print("Rode: python testes_guardrails.py\n")
    for t, ctx in [("Garanto a cura da sua dismetria!", "publico"),
                   ("Alongamento NÃO é sobre ficar mais alto — é função.", "publico")]:
        print(repr(t[:45]), "->", auditar(t, ctx))
