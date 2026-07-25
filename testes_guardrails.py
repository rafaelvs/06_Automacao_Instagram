# -*- coding: utf-8 -*-
"""
BATERIA ADVERSARIAL dos guardrails CFM.

O __main__ de cfm_guardrails.py (:117-128) tem 6 casos, todos benignos e todos
passando. Isso nao e teste: e demonstracao. Um ruleset de conformidade so vale
o que ele NEGA, e ninguem nunca escreveu um caso pra tentar burlar estas regras.

Este arquivo escreve. Cada caso declara o que DEVERIA acontecer; o relatorio
compara com o que acontece HOJE e classifica:

  OK             — comportamento correto.
  GAP            — deveria bloquear e NAO bloqueia (falso negativo).
  FALSO_POSITIVO — nao deveria bloquear e bloqueia (ruido que treina a ignorar).
  REGRESSAO      — caso marcado critico=True quebrou.

EXIT: 1 apenas se houver REGRESSAO. Os GAPs sao esperados HOJE (furo #8 do
levantamento) e estao aqui justamente para virarem asserçoes de verdade quando
as regex forem corrigidas. Fixar a regex = mudar `gap_conhecido` para False.

NAO alterar cfm_guardrails.py a partir daqui. Este arquivo so observa.

Rodar: python testes_guardrails.py   (use PYTHONIOENCODING=utf-8 no Windows)
"""
import sys

from cfm_guardrails import auditar

SIG = "CRM-SP 226103 RQE 137901"

# (texto, contexto, deve_bloquear, regra_alvo, gap_conhecido, critico, nota)
#   deve_bloquear=True  -> esperamos VIOLACAO da regra_alvo
#   gap_conhecido=True  -> sabemos que HOJE nao funciona; nao conta como regressao
#   critico=True        -> se quebrar, exit 1 (sao os casos que funcionam hoje)
CASOS = [

    # ---------------------------------------------------------------- baseline
    # Os 6 originais de cfm_guardrails.__main__, agora como asserçoes de verdade.
    ("Garanto a cura da sua dismetria!", "publico", True, "termo_vetado", False, True,
     "baseline: termo vetado"),
    ("Garanto a cura da sua dismetria!", "publico", True, "promessa", False, True,
     "baseline: promessa 'garanto'"),
    (f"Discrepância de membro: medir antes. {SIG}", "publico", False, None, False, True,
     "baseline: texto limpo e assinado nao pode disparar nada"),

    # ------------------------------------------------- furo #8: flexao de verbo
    # PROMESSAS[0] = r"\bgarant(o|e|em|ia|ido|ida|imos|ir|ira|irao|iremos)\b"
    # O \b apos 'ido'/'ida' impede o plural; 'iu'/'indo'/'iram' nem estao na lista.
    (f"Resultados garantidos para todos os pacientes. {SIG}", "publico", True, "promessa", True, False,
     "'garantidos' (plural) escapa: \\b depois de 'ido' nao casa com o 's'"),
    (f"Correções garantidas em qualquer idade. {SIG}", "publico", True, "promessa", True, False,
     "'garantidas' (plural feminino) escapa pelo mesmo motivo"),
    (f"A técnica garantiu o alinhamento em todos. {SIG}", "publico", True, "promessa", True, False,
     "'garantiu' (preterito) nao esta na alternancia"),
    (f"Estamos garantindo o resultado do tratamento. {SIG}", "publico", True, "promessa", True, False,
     "'garantindo' (gerundio) nao esta na alternancia"),
    (f"Os médicos garantiram a recuperação total. {SIG}", "publico", True, "promessa", True, False,
     "'garantiram' (3a pessoa plural preterito) nao esta na alternancia"),

    # ------------------------------------------------------ furo #8: minimizar risco
    # PROMESSAS[4] = r"\bsem risco\b" — so o singular exato.
    (f"Procedimento sem riscos para a criança. {SIG}", "publico", True, "promessa", True, False,
     "'sem riscos' (plural) escapa do \\bsem risco\\b"),
    (f"Cirurgia com risco zero de complicação. {SIG}", "publico", True, "promessa", True, False,
     "'risco zero' — ordem invertida, sem regra"),
    (f"Tratamento com zero risco de infecção. {SIG}", "publico", True, "promessa", True, False,
     "'zero risco' — sem regra"),
    (f"Não há nenhum risco no alongamento ósseo. {SIG}", "publico", True, "promessa", True, False,
     "'nenhum risco' — sem regra"),

    # --------------------------------------------------- furo #8: absoluto numerico
    # PROMESSAS[3] = r"\b100% de (sucesso|cura|resultado)\b" — so 3 substantivos.
    (f"Funciona em 100% dos casos que atendo. {SIG}", "publico", True, "promessa", True, False,
     "'100% dos casos' — preposicao e substantivo fora da regra"),
    (f"Método com 100% de eficácia comprovada. {SIG}", "publico", True, "promessa", True, False,
     "'100% de eficacia' — substantivo fora da lista"),
    (f"Abordagem 100% segura para o paciente. {SIG}", "publico", True, "promessa", True, False,
     "'100% segura' — sem 'de', fora da regra"),

    # ------------------------------------------ furo #8: negacao larga demais (NEG_PROMESSA)
    # NEG_PROMESSA contem "nao e " — 6 caracteres genericos. Qualquer "não é" na
    # janela de -35/+45 chars anula a promessa, mesmo sem relacao semantica.
    (f"Não é caro: garanto o resultado do tratamento. {SIG}", "publico", True, "promessa", True, False,
     "'nao e' sobre PRECO anula a promessa de 'garanto' por proximidade cega"),
    (f"Isso não é raro. Garanto a cura definitiva. {SIG}", "publico", True, "promessa", True, False,
     "'nao e' sobre frequencia anula 'garanto a cura'"),

    # -------------------------------------------------- furo #8: hashtag some antes da auditoria
    # _sem_hashtags() (cfm_guardrails.py:71) apaga #\S+ ANTES de normalizar.
    # Hashtag e texto publico: aparece no post e e indexavel.
    (f"Discrepância de membro. #dismetria #ortopedia {SIG}", "publico", True, "termo_vetado", True, False,
     "termo VETADO dentro de hashtag e apagado antes de auditar"),
    (f"Veja o caso. #resultadogarantido {SIG}", "publico", True, "promessa", True, False,
     "promessa dentro de hashtag e apagada antes de auditar"),

    # ------------------------------------------- furo #8: n.find() so olha a 1a ocorrencia
    # Regras 3 e 4 usam n.find(termo) e avaliam a janela da PRIMEIRA ocorrencia.
    # Se a primeira for negada/inocente, todas as seguintes ficam impunes.
    (f"Alongamento não é sobre estética. Faço alongamento por estética quando o paciente "
     f"quer ganhar altura. {SIG}", "publico", True, "estetica_alongamento", True, False,
     "1a ocorrencia de 'estetic' e negada -> find() para ali e a 2a (real) escapa"),
    (f"A ilustração do raio-x é didática. Depois peço a radiografia real do paciente "
     f"e publico aqui. {SIG}", "publico", True, "exame_imagem", True, False,
     "'raio-x' aparece 1o com contexto de ilustracao; 'radiografia' real depois — "
     "mas cada termo tem seu find(), entao o caso real e o 2o termo"),

    # ----------------------------------------------- furo #8: 'na imagem' libera exame real
    # EXAME_OK_CTX (cfm_guardrails.py:64) inclui "na imagem", expressao banalissima
    # que aparece em qualquer legenda que aponte para a propria arte.
    (f"Ressonância do meu paciente, como se vê na imagem. {SIG}", "publico", True, "exame_imagem", True, False,
     "'na imagem' no contexto libera exame REAL de paciente"),

    # ------------------------------------------- lacuna de regra: autopromocao comparativa
    # Nao e furo de regex — e regra INEXISTENTE. Achado da transcricao de dest04/story07.
    (f"CASOS COMPLEXOS · O que outros não resolveram. {SIG}", "publico", True, "autopromocao", True, False,
     "posicionamento comparativo frente a outros profissionais — nenhuma regra cobre"),
    (f"Já ouviu 'não há mais o que fazer'? Em muitos casos existe um caminho. {SIG}",
     "publico", True, "autopromocao", True, False,
     "mesma familia — nenhuma regra cobre"),
    (f"Sou o maior especialista em alongamento do país. {SIG}", "publico", True, "promessa", True, False,
     "'o melhor <profissao>' e coberto, mas 'o maior especialista' nao"),

    # ------------------------------------------------- lacuna: variantes de 'antes e depois'
    (f"Antes x depois do tratamento. {SIG}", "publico", True, "promessa", True, False,
     "'antes x depois' — variante nao coberta por \\bantes e depois\\b"),
    (f"Antes/depois do alongamento. {SIG}", "publico", True, "promessa", True, False,
     "'antes/depois' — variante nao coberta"),

    # ------------------------------------------------------------ nao pode virar ruido
    # Se estes dispararem, o medico aprende a ignorar o lint — pior que nao ter lint.
    (f"Alongamento ósseo NÃO é sobre ficar mais alto — é função. {SIG}", "publico", False, None, False, True,
     "guardrail legitimo afirmando o tabu nao pode virar violacao"),
    (f"Não prometo milagre nenhum. {SIG}", "publico", False, None, False, True,
     "honestidade explicita nao pode virar violacao"),
    (f"O esquema didático do raio-x mostra o eixo. {SIG}", "publico", False, None, False, True,
     "ilustracao didatica declarada nao pode virar violacao"),
    (f"Antes e depois não fazem sentido em ortopedia. {SIG}", "publico", False, None, False, True,
     "critica ao 'antes e depois' nao pode virar violacao"),
]


def _viola(texto, contexto, regra=None):
    """True se auditar() emite VIOLACAO (opcionalmente da regra alvo)."""
    for sev, r, _det in auditar(texto, contexto):
        if sev == "VIOLACAO" and (regra is None or r == regra):
            return True
    return False


def relatorio(verbose=True):
    ok = gaps = falsos = regressoes = 0
    linhas = []
    for texto, ctx, deve, regra, gap_conhecido, critico, nota in CASOS:
        bloqueou = _viola(texto, ctx, regra if deve else None)
        if deve:
            if bloqueou:
                estado = "OK"; ok += 1
            elif gap_conhecido:
                estado = "GAP"; gaps += 1
            else:
                estado = "REGRESSAO"; regressoes += 1
        else:
            if not bloqueou:
                estado = "OK"; ok += 1
            elif critico:
                estado = "REGRESSAO"; regressoes += 1
            else:
                estado = "FALSO_POSITIVO"; falsos += 1
        linhas.append((estado, regra or "-", texto[:62], nota))

    if verbose:
        print("=== BATERIA ADVERSARIAL — cfm_guardrails ===")
        print(f"casos: {len(CASOS)} | OK={ok} GAP={gaps} FALSO_POSITIVO={falsos} REGRESSAO={regressoes}\n")
        for estado in ("REGRESSAO", "FALSO_POSITIVO", "GAP"):
            sel = [l for l in linhas if l[0] == estado]
            if not sel:
                continue
            print(f"--- {estado} ({len(sel)}) ---")
            for _e, regra, txt, nota in sel:
                print(f"  [{regra}] {txt!r}")
                print(f"      -> {nota}")
            print()
        if gaps:
            print(f"Os {gaps} GAPs sao o furo #8 do levantamento, documentados de proposito.")
            print("Corrigir a regex = virar `gap_conhecido` para False e o caso passa a ser asserçao.")

    return {"ok": ok, "gaps": gaps, "falsos": falsos, "regressoes": regressoes, "total": len(CASOS)}


if __name__ == "__main__":
    r = relatorio()
    if r["regressoes"]:
        print(f"\nFALHA: {r['regressoes']} regressao(oes) em caso critico.")
        sys.exit(1)
    print("\nOK: nenhuma regressao em caso critico.")
    sys.exit(0)
