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
    # ERA: r"\bgarant(o|e|em|ia|ido|ida|imos|ir|ira|irao|iremos)\b" — o \b apos 'ido'/'ida'
    # impedia o plural e 'iu'/'indo'/'iram' nem estavam na alternancia.
    # AGORA: r"\bgarant[a-z]*\b" (stem aberto).
    (f"Resultados garantidos para todos os pacientes. {SIG}", "publico", True, "promessa", False, False,
     "'garantidos' (plural)"),
    (f"Correções garantidas em qualquer idade. {SIG}", "publico", True, "promessa", False, False,
     "'garantidas' (plural feminino)"),
    (f"A técnica garantiu o alinhamento em todos. {SIG}", "publico", True, "promessa", False, False,
     "'garantiu' (preterito)"),
    (f"Estamos garantindo o resultado do tratamento. {SIG}", "publico", True, "promessa", False, False,
     "'garantindo' (gerundio)"),
    (f"Os médicos garantiram a recuperação total. {SIG}", "publico", True, "promessa", False, False,
     "'garantiram' (3a pessoa plural preterito)"),

    # ------------------------------------------------------ furo #8: minimizar risco
    # ERA: r"\bsem risco\b" (singular exato). AGORA: r"\b(sem|nenhum|zero) riscos?\b"
    # mais r"\brisco zero\b".
    (f"Procedimento sem riscos para a criança. {SIG}", "publico", True, "promessa", False, False,
     "'sem riscos' (plural)"),
    (f"Cirurgia com risco zero de complicação. {SIG}", "publico", True, "promessa", False, False,
     "'risco zero' (ordem invertida)"),
    (f"Tratamento com zero risco de infecção. {SIG}", "publico", True, "promessa", False, False,
     "'zero risco'"),
    (f"Não há nenhum risco no alongamento ósseo. {SIG}", "publico", True, "promessa", False, False,
     "'nenhum risco'"),

    # --------------------------------------------------- furo #8: absoluto numerico
    # ERA: r"\b100% de (sucesso|cura|resultado)\b" — so 3 substantivos e 'de' obrigatorio.
    (f"Funciona em 100% dos casos que atendo. {SIG}", "publico", True, "promessa", False, False,
     "'100% dos casos'"),
    (f"Método com 100% de eficácia comprovada. {SIG}", "publico", True, "promessa", False, False,
     "'100% de eficacia'"),
    (f"Abordagem 100% segura para o paciente. {SIG}", "publico", True, "promessa", False, False,
     "'100% segura' (sem 'de')"),

    # ------------------------------------------ furo #8: negacao larga demais (NEG_PROMESSA)
    # ERA: NEG_PROMESSA continha "nao e " — 6 caracteres genericos que anulavam QUALQUER
    # promessa num raio de 45 chars. Removido em favor de negacoes ancoradas.
    (f"Não é caro: garanto o resultado do tratamento. {SIG}", "publico", True, "promessa", False, False,
     "'nao e' sobre PRECO nao pode mais anular 'garanto'"),
    (f"Isso não é raro. Garanto a cura definitiva. {SIG}", "publico", True, "promessa", False, False,
     "'nao e' sobre frequencia nao pode mais anular 'garanto a cura'"),

    # -------------------------------------------------- furo #8: hashtag some antes da auditoria
    # ERA: _sem_hashtags() apagava #\S+ ANTES de normalizar. Hashtag e texto publico e
    # indexavel. AGORA: '#' vira espaco, e o corpo concatenado e testado por substring.
    (f"Discrepância de membro. #dismetria #ortopedia {SIG}", "publico", True, "termo_vetado", False, False,
     "termo VETADO dentro de hashtag"),
    (f"Veja o caso. #resultadogarantido {SIG}", "publico", True, "promessa", False, False,
     "promessa dentro de hashtag CONCATENADA (onde \\b nunca casa)"),

    # ------------------------------------------- furo #8: n.find() so olhava a 1a ocorrencia
    # ERA: n.find(termo) avaliava a janela da PRIMEIRA ocorrencia; se ela fosse negada,
    # todas as seguintes ficavam impunes. AGORA: re.finditer sobre todas.
    # O enchimento entre as duas ocorrencias e proposital: afasta a 2a da janela de
    # negacao de -60 chars, isolando o defeito do find() do defeito de janela.
    (f"Alongamento não é sobre estética, isso é importante deixar claro para todo mundo "
     f"que me pergunta sobre o tema. Faço alongamento por estética quando o paciente quer. {SIG}",
     "publico", True, "estetica_alongamento", False, False,
     "1a ocorrencia de 'estetic' negada NAO pode mais blindar a 2a (real)"),

    # GAP QUE PERMANECE: aqui as duas ocorrencias estao a menos de 80 chars, entao a
    # janela de contexto do exame ainda engole o 'ilustracao/didatica' da primeira.
    # E defeito de LARGURA DE JANELA, nao de find(). Estreitar a janela sem medir o
    # impacto nos 18 exame_imagem ja existentes trocaria falso negativo por falso
    # positivo — fica documentado ate haver decisao sobre a severidade (item 3).
    (f"A ilustração do raio-x é didática. Depois peço a radiografia real do paciente "
     f"e publico aqui. {SIG}", "publico", True, "exame_imagem", True, False,
     "janela de +/-80 chars ainda alcanca o contexto de ilustracao da frase anterior"),

    # ----------------------------------------------- furo #8: 'na imagem' liberava exame real
    # ERA: EXAME_OK_CTX incluia "na imagem", expressao banalissima. Removido.
    (f"Ressonância do meu paciente, como se vê na imagem. {SIG}", "publico", True, "exame_imagem", False, False,
     "'na imagem' nao pode mais liberar exame REAL de paciente"),

    # ------------------------------------------- regra NOVA: autopromocao comparativa
    # Nao era furo de regex — era regra INEXISTENTE. Criada a pedido do Rafael depois de
    # a transcricao revelar dest04 e story07, ambos ja publicados.
    (f"CASOS COMPLEXOS · O que outros não resolveram. {SIG}", "publico", True, "autopromocao", False, False,
     "dest04 — posicionamento comparativo frente a outros profissionais"),
    (f"Já ouviu 'não há mais o que fazer'? Em muitos casos existe um caminho. {SIG}",
     "publico", True, "autopromocao", False, False,
     "story07 — apelo ao 'caso perdido'"),
    (f"Sou o maior especialista em alongamento do país. {SIG}", "publico", True, "promessa", False, False,
     "superlativo alem de 'o melhor <profissao>'"),

    # ------------------------------------------------- variantes de 'antes e depois'
    (f"Antes x depois do tratamento. {SIG}", "publico", True, "promessa", False, False,
     "'antes x depois'"),
    (f"Antes/depois do alongamento. {SIG}", "publico", True, "promessa", False, False,
     "'antes/depois'"),

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


def _pegou(texto, contexto, regra):
    """True se auditar() sinalizou a regra alvo, em QUALQUER severidade.

    Checar so 'VIOLACAO' era um bug desta bateria: estetica_alongamento e exame_imagem
    emitem REVISAR por desenho, entao esses casos apareceriam como GAP eternamente,
    mesmo depois de corrigidos. O que se testa aqui e DETECCAO; a severidade correta
    de cada regra e assunto separado (item 3).
    """
    return any(r == regra for _sev, r, _det in auditar(texto, contexto))


def _limpo(texto, contexto):
    """True se auditar() nao sinalizou NADA substantivo. 'assinatura' e ignorada: e
    ruido estrutural de cena/frame, nao achado de conteudo."""
    return not any(r != "assinatura" for _sev, r, _det in auditar(texto, contexto))


def relatorio(verbose=True):
    ok = gaps = falsos = regressoes = 0
    linhas = []
    for texto, ctx, deve, regra, gap_conhecido, critico, nota in CASOS:
        bloqueou = _pegou(texto, ctx, regra) if deve else (not _limpo(texto, ctx))
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
