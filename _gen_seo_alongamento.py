# -*- coding: utf-8 -*-
"""Gera seo_alongamento.json (6 episodios do lote 1 da serie "Alongamento Osseo").

Titulos <=60 chars de proposito: a auditoria v2 apontou 25/34 titulos da serie antiga acima
disso (resíduo D2). A serie nova nasce dentro do limite.
"""
import json, os

ASSINATURA = ("Dr. Rafael Vargas · CRM-SP 226103 · RQE 137901 — Reconstrução e Alongamento Ósseo · "
              "Ortopedia Pediátrica.\nConteúdo educativo, não substitui a avaliação do seu médico.")
REF_AD   = "Referências: https://orthoinfo.aaos.org · https://sbot.org.br"
REF_KIDS = "Referências: https://orthoinfo.aaos.org · https://sbot.org.br · https://sbcp.org.br"

def desc(gancho, bullets, refs, hashtags):
    return (f"{gancho}\n\n" + "\n".join("• " + b for b in bullets) +
            "\n\nDúvidas de rotina: WhatsApp (11) 3280-1413.\n\n" +
            ASSINATURA + "\n\n" + refs + "\n\n" + hashtags)

BASE = ["ortopedia", "alongamento ósseo", "reconstrução óssea", "Dr. Rafael Vargas",
        "ortopedia São Paulo", "discrepância de membro", "fixador externo"]

SEO = {
 "discrepancia_membro": {
  "title": "Uma perna mais curta: quando tratar? #Shorts",
  "description": desc(
    # sem "estetica": dispara o guardrail CFM e, pior, "nem sempre e SO estetica" sugere que as vezes e
    "Uma perna mais curta que a outra nem sempre precisa de cirurgia. O que decide é o quanto ela afeta a função.",
    ["Diferenças pequenas são comuns e muita gente não tem sintoma; acompanhar costuma bastar.",
     "O que pesa: tamanho da diferença, causa e o quanto afeta a marcha.",
     "Mancar que apareceu, dor no quadril ou na coluna: procure avaliação com ortopedista."],
    REF_AD, "#Shorts #discrepanciademembro #alongamentoosseo #ortopedia #drrafaelvargas"),
  "tags": BASE + ["uma perna maior que a outra", "diferença de comprimento das pernas",
    "anisomelia", "perna mais curta que a outra", "quando operar diferença de perna",
    "palmilha compensadora", "claudicação", "discrepância de comprimento dos membros"]},

 "discrepancia_membro_kids": {
  "title": "Perna mais curta na criança: quando tratar (pais) #Shorts",
  "description": desc(
    "Uma perna do seu filho mais curta que a outra? Nem sempre é caso de cirurgia.",
    ["Diferenças pequenas são comuns na infância e muitas vezes não dão sintoma.",
     "Na criança o crescimento muda a conta — por isso o acompanhamento é o tratamento.",
     "Começou a mancar, dor no quadril ou diferença que aumentou rápido: leve para avaliação."],
    REF_KIDS, "#Shorts #ortopediapediatrica #discrepanciademembro #criança #drrafaelvargas"),
  "tags": BASE + ["ortopedia pediátrica", "ortopedia infantil", "pais",
    "perna mais curta criança", "filho manca", "criança mancando",
    "diferença de perna em criança", "crescimento ósseo criança", "anisomelia infantil"]},

 "fixador_ou_haste": {
  "title": "Fixador externo ou haste interna? Como se escolhe #Shorts",
  "description": desc(
    "Fixador por fora ou haste por dentro? Essa escolha não é preferência do paciente nem do médico.",
    ["O fixador externo corrige o ângulo junto com o alongamento e permite ajuste — exige cuidado diário com os pinos.",
     "A haste interna não deixa nada para fora, mas depende do osso comportar o implante.",
     "Quem decide é o caso: deformidade, idade, qualidade do osso e infecção prévia."],
    REF_AD, "#Shorts #fixadorexterno #alongamentoosseo #ilizarov #drrafaelvargas"),
  "tags": BASE + ["fixador ou haste", "alongamento sem fixador", "haste intramedular alongamento",
    "ilizarov", "fixador externo circular", "alongamento ósseo método",
    "haste motorizada alongamento", "tipos de alongamento ósseo"]},

 "fixador_ou_haste_kids": {
  "title": "Fixador ou haste na criança: como se escolhe (pais) #Shorts",
  "description": desc(
    "Fixador por fora ou haste por dentro no seu filho? A escolha depende do osso dele.",
    ["O fixador externo permite ajuste — e o cuidado diário com os pinos vira rotina da família.",
     "Na criança pesa um fator a mais: as placas de crescimento, que não podem ser danificadas.",
     "Leve à consulta a rotina real do seu filho: escola, esporte, quem cuida dele."],
    REF_KIDS, "#Shorts #ortopediapediatrica #fixadorexterno #criança #drrafaelvargas"),
  "tags": BASE + ["ortopedia pediátrica", "ortopedia infantil", "pais",
    "fixador externo criança", "alongamento ósseo criança", "placa de crescimento",
    "cirurgia ortopédica infantil", "fixador em criança rotina"]},

 "tempo_tratamento": {
  "title": "Alongamento ósseo: quanto tempo dura o tratamento #Shorts",
  "description": desc(
    "Alongar o osso leva bem mais tempo do que a conta de um milímetro por dia sugere.",
    ["A fase de alongamento é a mais rápida: cerca de 1 mm por dia, em pequenos ajustes.",
     "A consolidação leva bem mais tempo — é quando o osso novo endurece para aguentar carga.",
     "Dor intensa em repouso, dormência que avança ou infecção nos pinos: pronto-socorro."],
    REF_AD, "#Shorts #alongamentoosseo #fixadorexterno #consolidacaoossea #drrafaelvargas"),
  "tags": BASE + ["quanto tempo fixador externo", "tempo de alongamento ósseo",
    "consolidação óssea", "quanto tempo dura alongamento", "distração osteogênica",
    "fases do alongamento ósseo", "retirada do fixador quando"]},

 "tempo_tratamento_kids": {
  "title": "Fixador na criança: quanto tempo dura (pais) #Shorts",
  "description": desc(
    "Quanto tempo seu filho vai ficar com o fixador? Mais do que a conta sugere.",
    ["São duas fases: o alongamento, mais rápido, e a consolidação, mais longa.",
     "Criança costuma consolidar mais rápido que adulto — mas fisioterapia e consultas seguem iguais.",
     "Dor intensa em repouso, criança prostrada ou secreção nos pinos com febre: pronto-socorro."],
    REF_KIDS, "#Shorts #ortopediapediatrica #fixadorexterno #criança #drrafaelvargas"),
  "tags": BASE + ["ortopedia pediátrica", "ortopedia infantil", "pais",
    "fixador externo criança tempo", "alongamento ósseo criança", "consolidação óssea criança",
    "escola com fixador", "rotina criança fixador externo"]},
}


# ─────────────────── LOTE 2 (01/08/2026) ───────────────────
SEO.update({
 "pseudartrose": {
  "title": "O osso não colou? Isso se chama pseudartrose #Shorts",
  "description": desc(
    "Fraturou, operou, e meses depois o osso ainda não colou? Isso tem nome: pseudartrose.",
    ["A consolidação não acontece no tempo esperado e o foco da fratura continua se mexendo.",
     "Pesa a estabilidade do osso, a circulação no local, infecção — e o cigarro.",
     "Dor que persiste meses depois: procure avaliação com quem trata reconstrução óssea."],
    REF_AD, "#Shorts #pseudartrose #reconstrucaoossea #fratura #drrafaelvargas"),
  "tags": BASE + ["pseudartrose", "osso que não cola", "fratura que não consolida",
    "falha de consolidação óssea", "osso não colou depois da cirurgia",
    "tratamento pseudartrose", "enxerto ósseo", "não consolidação de fratura"]},

 "pseudartrose_kids": {
  "title": "O osso do seu filho não colou? (guia para os pais) #Shorts",
  "description": desc(
    "O osso do seu filho fraturou, tratou, e não colou? Isso tem nome e tem tratamento.",
    ["Criança costuma consolidar bem — quando não cola, vale investigar a causa.",
     "Existe uma forma que aparece nos primeiros anos, às vezes ligada a manchas na pele.",
     "Dor que não passa, deformidade nova ou a criança evitando apoiar: leve para avaliação."],
    REF_KIDS, "#Shorts #ortopediapediatrica #pseudartrose #criança #drrafaelvargas"),
  "tags": BASE + ["ortopedia pediátrica", "ortopedia infantil", "pais",
    "osso que não cola criança", "pseudartrose congênita", "fratura criança não consolidou",
    "perna arqueada bebê", "manchas na pele e osso"]},

 "sequela_fratura": {
  "title": "Fratura que colou torta: ainda dá para tratar #Shorts",
  "description": desc(
    "Fratura que colou em posição ruim, encurtada, ou que infeccionou: ainda dá para tratar.",
    ["A sequela muda a marcha e sobrecarrega o resto do corpo.",
     "Havendo infecção no osso, ela é resolvida junto com a reconstrução, em etapas.",
     "Se convive com dor ou manca: vale uma segunda opinião com quem trata reconstrução óssea."],
    REF_AD, "#Shorts #sequeladefratura #reconstrucaoossea #osteomielite #drrafaelvargas"),
  "tags": BASE + ["sequela de fratura", "fratura consolidada torta", "osso torto depois da fratura",
    "infecção no osso", "osteomielite", "perna encurtada após fratura",
    "correção de deformidade óssea", "reconstrução após fratura"]},

 "sequela_fratura_kids": {
  "title": "Fratura que colou torta na criança (para os pais) #Shorts",
  "description": desc(
    "A fratura do seu filho colou torta ou deixou a perna mais curta? Em criança, a conta é diferente.",
    ["A criança remodela o osso — parte dos desalinhamentos melhora com o crescimento.",
     "Mas tem limite: depende da idade, do osso e do tipo de desvio.",
     "Se a placa de crescimento se machucou, a diferença pode aumentar: acompanhe de perto."],
    REF_KIDS, "#Shorts #ortopediapediatrica #fratura #criança #drrafaelvargas"),
  "tags": BASE + ["ortopedia pediátrica", "ortopedia infantil", "pais",
    "fratura criança colou torta", "remodelação óssea criança", "placa de crescimento fratura",
    "perna torta após fratura criança", "sequela fratura infantil"]},

 "primeira_consulta": {
  "title": "Alongamento ósseo: o que perguntar na consulta #Shorts",
  "description": desc(
    "Vai na primeira consulta sobre alongamento ósseo? Anote estas perguntas antes de ir.",
    ["Qual o objetivo funcional do tratamento e o que exatamente será corrigido.",
     "Qual método, quanto tempo no total, e como fica sua rotina de trabalho.",
     "Quais os riscos e o que se faz se algo não sair como esperado."],
    REF_AD, "#Shorts #alongamentoosseo #primeiraconsulta #ortopedia #drrafaelvargas"),
  "tags": BASE + ["primeira consulta alongamento ósseo", "o que perguntar ao ortopedista",
    "consulta ortopedia o que levar", "segunda opinião ortopedia",
    "avaliação alongamento ósseo", "como escolher ortopedista"]},

 "primeira_consulta_kids": {
  "title": "Levar seu filho ao ortopedista: o que perguntar #Shorts",
  "description": desc(
    "Vai levar seu filho na primeira consulta de ortopedia? Anote o que perguntar.",
    ["Leve os exames anteriores e, se tiver, vídeo de como ele anda.",
     "Pergunte o que dá para observar, o que tratar agora, e de quanto em quanto tempo voltar.",
     "Pergunte como fica a escola, a educação física e o esporte durante o acompanhamento."],
    REF_KIDS, "#Shorts #ortopediapediatrica #consulta #criança #drrafaelvargas"),
  "tags": BASE + ["ortopedia pediátrica", "ortopedia infantil", "pais",
    "primeira consulta ortopedista criança", "o que perguntar ortopedista infantil",
    "levar filho ao ortopedista", "criança mancando consulta"]},
})


# ─────────────────── LOTE 3 (16/08/2026) ───────────────────
SEO.update({
 "fim_tratamento": {
  "title": "Tirou o fixador? O tratamento não acaba aí #Shorts",
  "description": desc(
    "O fixador saiu, o raio-X está bom — mas o tratamento não termina nesse dia.",
    ["O osso novo ainda está mais frágil que o osso maduro por meses após a retirada.",
     "Carga e atividade voltam aos poucos, no ritmo que a equipe orienta.",
     "Dor nova ou insegurança para apoiar o peso: volte para reavaliação antes de forçar."],
    REF_AD, "#Shorts #alongamentoosseo #fixadorexterno #reconstrucaoossea #drrafaelvargas"),
  "tags": BASE + ["depois de tirar o fixador externo", "pos retirada fixador",
    "reabilitacao pos alongamento osseo", "quando volto a andar normal",
    "osso fragil apos fixador", "retirada do fixador externo cuidados", "alta do tratamento ortopedico"]},

 "fim_tratamento_kids": {
  "title": "Tiraram o fixador do seu filho? Cuidado continua #Shorts",
  "description": desc(
    "O fixador do seu filho saiu — mas o cuidado com aquele osso continua.",
    ["O osso novo segue ganhando resistência por meses; quedas merecem mais atenção.",
     "Esporte e educação física voltam aos poucos, no ritmo que a equipe orientar.",
     "Dor nova ou ele evitando apoiar o membro depois da retirada: leve para reavaliação."],
    REF_KIDS, "#Shorts #ortopediapediatrica #fixadorexterno #crianca #drrafaelvargas"),
  "tags": BASE + ["ortopedia pediátrica", "ortopedia infantil", "pais",
    "retirada fixador externo crianca", "crianca depois do fixador", "volta ao esporte crianca fixador",
    "cuidados pos fixador infantil", "osso fragil crianca"]},
})


# ─────────────── LOTE 4 (16/08/2026) ───────────────
SEO.update({
 "deformidade_angular": {
  "title": "Perna torta ou perna curta? Não é o mesmo #Shorts",
  "description": desc(
    "Perna torta e perna curta são problemas diferentes — e o tratamento também.",
    ["Na deformidade angular, o eixo do osso está desviado.",
     "No encurtamento, o osso é mais curto, sem desvio de eixo. Muitas vezes vêm juntos.",
     "Perna que muda de forma, ou desconforto ao apoiar que não melhora: procure avaliação."],
    REF_AD, "#Shorts #deformidadeangular #alongamentoosseo #ortopedia #drrafaelvargas"),
  "tags": BASE + ["deformidade angular perna", "perna torta tratamento", "genu varo genu valgo",
    "correção de eixo do osso", "encurtamento x deformidade", "osteotomia corretiva",
    "perna arqueada adulto"]},

 "deformidade_angular_kids": {
  "title": "Perna torta ou curta na criança? São diferentes #Shorts",
  "description": desc(
    "No seu filho, perna torta e perna curta são coisas diferentes — cada uma tem seu tratamento.",
    ["A deformidade angular costuma chamar atenção pela forma do joelho ou tornozelo.",
     "Na criança, alguns desvios pequenos melhoram sozinhos com o crescimento.",
     "Perna que mudou de forma, ou ele começou a mancar: leve para avaliação."],
    REF_KIDS, "#Shorts #ortopediapediatrica #deformidadeangular #criança #drrafaelvargas"),
  "tags": BASE + ["ortopedia pediátrica", "ortopedia infantil", "pais",
    "perna torta criança", "genu valgo infantil", "joelho torto criança",
    "perna arqueada bebê tratamento", "deformidade angular infantil"]},

 "quanto_alongar": {
  "title": "Quanto dá para alongar o osso? O que decide #Shorts",
  "description": desc(
    "Quantos centímetros dá para alongar? Não existe um número fixo — depende do seu caso.",
    ["Pele, nervo e vaso esticam junto com o osso e ditam o limite seguro por etapa.",
     "Passar do limite de uma vez aumenta o risco de lesão — por isso casos maiores são feitos em fases.",
     "Leve essa pergunta para o planejamento com seu cirurgião."],
    REF_AD, "#Shorts #alongamentoosseo #ilizarov #distracaoossea #drrafaelvargas"),
  "tags": BASE + ["quanto dá para alongar a perna", "limite alongamento ósseo",
    "quantos centímetros alongamento", "alongamento em etapas", "distração osteogênica limite",
    "risco alongamento ósseo nervo"]},

 "quanto_alongar_kids": {
  "title": "Quanto dá para alongar na criança? O que pesa #Shorts",
  "description": desc(
    "Quanto dá para alongar na perna do seu filho? Não é um número fixo — depende do caso dele.",
    ["Pele, nervo e vaso ditam o limite seguro em cada etapa, junto com o osso.",
     "Na criança, o plano também considera quanto ainda falta crescer.",
     "Leve essa pergunta ao planejamento com o cirurgião."],
    REF_KIDS, "#Shorts #ortopediapediatrica #alongamentoosseo #criança #drrafaelvargas"),
  "tags": BASE + ["ortopedia pediátrica", "ortopedia infantil", "pais",
    "quanto alongar perna criança", "alongamento ósseo infantil limite",
    "crescimento e alongamento ósseo", "planejamento cirúrgico infantil"]},

 "trabalho_escola": {
  "title": "Fixador externo: quando volto ao trabalho? #Shorts",
  "description": desc(
    "Voltar ao trabalho com fixador depende mais da função do cargo do que de uma data no calendário.",
    ["Trabalho sentado costuma liberar mais cedo; esforço físico intenso demora mais.",
     "Organize o deslocamento e reserve um momento para cuidar dos pinos.",
     "Dor que piora no fim do dia ou sinais de infecção nos pinos: avise a equipe."],
    REF_AD, "#Shorts #fixadorexterno #voltaraotrabalho #alongamentoosseo #drrafaelvargas"),
  "tags": BASE + ["voltar ao trabalho com fixador externo", "afastamento fixador externo",
    "trabalhar com fixador externo", "rotina fixador externo trabalho",
    "quando volto a trabalhar cirurgia perna"]},

 "trabalho_escola_kids": {
  "title": "Fixador externo: quando volta à escola? #Shorts",
  "description": desc(
    "Seu filho pode voltar à escola bem antes do que os pais costumam imaginar.",
    ["A sala de aula costuma ser liberada logo; recreio livre e educação física esperam.",
     "Converse com os professores sobre o fixador antes da volta.",
     "Dor após o dia de aula, ou sinais de infecção nos pinos: avise a equipe."],
    REF_KIDS, "#Shorts #ortopediapediatrica #fixadorexterno #criança #drrafaelvargas"),
  "tags": BASE + ["ortopedia pediátrica", "ortopedia infantil", "pais",
    "volta à escola com fixador externo", "criança fixador externo escola",
    "educação física com fixador", "rotina escolar cirurgia ortopédica"]},

 "vida_cotidiana_fixador": {
  "title": "Banho, roupa e sono com fixador externo #Shorts",
  "description": desc(
    "Banho, roupa e sono com fixador têm truques simples que facilitam o dia a dia.",
    ["O banho normal costuma ser liberado — aproveite para lavar os pinos com sabonete neutro.",
     "Roupas largas com zíper lateral ajudam a vestir; um travesseiro de apoio protege ao dormir.",
     "Secreção com mau cheiro, vermelhidão que avança ou febre: pronto-socorro."],
    REF_AD, "#Shorts #fixadorexterno #rotina #alongamentoosseo #drrafaelvargas"),
  "tags": BASE + ["como tomar banho com fixador externo", "como dormir com fixador externo",
    "roupa para fixador externo", "cuidados diários fixador externo",
    "rotina com fixador externo", "higiene dos pinos fixador"]},

 "vida_cotidiana_fixador_kids": {
  "title": "Banho, roupa e sono do seu filho com fixador #Shorts",
  "description": desc(
    "Banho, roupa e sono do seu filho com o fixador ficam mais fáceis com alguns ajustes.",
    ["O banho normal costuma ser liberado — supervisione sempre e lave os pinos.",
     "Roupas largas facilitam vestir; um travesseiro de apoio protege ao dormir.",
     "Secreção, vermelhidão que avança ao redor dos pinos, ou febre: pronto-socorro."],
    REF_KIDS, "#Shorts #ortopediapediatrica #fixadorexterno #criança #drrafaelvargas"),
  "tags": BASE + ["ortopedia pediátrica", "ortopedia infantil", "pais",
    "banho criança com fixador externo", "dormir com fixador externo criança",
    "cuidados fixador externo infantil", "rotina criança fixador"]},
})

if __name__ == "__main__":
    p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "seo_alongamento.json")
    json.dump(SEO, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print("gerado:", p)
    for k, v in SEO.items():
        t = ", ".join(v["tags"])
        flag = ""
        if len(v["title"]) > 60: flag += "  !! TITULO>60"
        if len(v["title"]) > 100: flag += "  !! ESTOURA YT"
        if len(t) > 500: flag += "  !! TAGS>500"
        if len(v["description"]) > 5000: flag += "  !! DESC>5000"
        print(f"{k:26s} tit={len(v['title']):3d} desc={len(v['description']):4d} "
              f"tags={len(v['tags']):2d}/{len(t):3d}{flag}")
