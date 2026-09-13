# -*- coding: utf-8 -*-
"""
MINI-SÉRIE "ESCOLIOSE — O SINAL NAS COSTAS" — 3 episódios (12/09/2026, plano de saída da estagnação, D5).

POR QUE: escoliose mede 100 na escala de busca (12,6× o 2º tema pediátrico; ~25.000× "discrepância de
membros"); 177 perguntas de família; 0 de 12 resultados em formato curto. Decisão D5 do Rafael
(12/09): entra SÓ RASTREIO — teste de Adams, quando encaminhar, o que o estirão faz com a curva.
NUNCA tratamento, NUNCA comparação nominal com outra categoria profissional, NUNCA número sem fonte.

CONTEÚDO: consenso de rastreio já publicado pela casa (post27, reel06, c_pnc_escoliose,
s_pnc_escoliose): desvio em curva da coluna vista por trás; costuma ser indolor no início; aparece
mais no estirão da pré-adolescência; sinais = ombros/cintura assimétricos, uma escápula mais saliente,
um lado das costas mais alto ao inclinar o tronco à frente (teste de Adams); quem avalia e decide
exame/conduta é o ortopedista. Nenhuma afirmação nova.

FORMATO: série "Pé no Chão" (motif feet), ≤5 cenas, vo 60–78 palavras, capa v2.
APROVAÇÃO: lote ESCOLIOSE-RASTREIO-2026-09-12 em aprovacoes.json — decisão D5 (12/09); revisão
passiva na fila (PROGRAMACAO.md).
"""
import ganchos_layout as _gl

SIG = "Dr. Rafael Vargas · Médico · CRM-SP 226103 · RQE 137901 — Reconstrução e Alongamento Ósseo · Ortopedia Pediátrica."
DISC = "Conteúdo educativo; não substitui avaliação individual."
IA = "Narração com voz digital (IA)."
MENCAO = "Sociedade da área: @sbortopediapediatrica"


def _cap(corpo, cta="Envia para um pai ou uma mãe de pré-adolescente."):
    return corpo + "\n\n" + cta + "\n\n" + MENCAO + "\n\n" + IA + "\n" + SIG + "\n" + DISC


ESCOLIOSE = [

 # ───────────── ep501 · teste de Adams ─────────────
 {"id":"esc_teste_adams","ep":501,"serie":"Pé no Chão","temporada":"coluna","motif_family":"feet",
  "scenes":[
   {"k":"Escoliose","sc":["O teste das costas","que você faz em casa."],"e":None,
    "sub":"Um movimento simples mostra o sinal que a escoliose costuma dar.",
    "vo":"Um teste das costas que se faz em casa, em um minuto: mostra o sinal que a escoliose dá antes de doer."},
   {"k":"Como fazer","sc":["De pé, pés juntos,","inclina o tronco à frente."],"e":None,
    "sub":"Braços soltos, joelhos esticados. Você olha as costas por trás.",
    "vo":"Criança de pé, pés juntos, tronco inclinado à frente, braços soltos, joelhos esticados. Olhe as costas por trás."},
   {"k":"O que observar","sc":["Um lado das costas","mais alto que o outro."],"e":"mais alto",
    "sub":"É a rotação da coluna aparecendo. É sinal, não diagnóstico.",
    "vo":"Um lado das costas mais alto que o outro é a rotação da coluna aparecendo. Sinal, não diagnóstico."},
   {"k":"O que fazer","sc":["Sinal presente?","Avaliação."],"e":None,
    "sub":"Quem confirma, pede exame e decide a conduta é o ortopedista.",
    "vo":"Sinal presente, ou dúvida? Leve para avaliação. Quem confirma e decide é o ortopedista."},
   {"k":"Passa adiante","sc":["Envia para quem","tem pré-adolescente."],"e":None,"cta":True,
    "sub":"Um minuto de teste, hoje.",
    "vo":"Envia para quem tem pré-adolescente em casa."},
  ],
  "caption":_cap("O teste das costas que você faz em casa: a criança fica de pé, pés juntos, e inclina o tronco para a frente com os braços soltos e os joelhos esticados; você olha as costas por trás. Um lado mais alto que o outro é a rotação da coluna aparecendo — o sinal que a escoliose costuma dar antes de qualquer dor. É sinal, não diagnóstico: quem confirma, decide se pede exame e define a conduta é o ortopedista.")},

 # ───────────── ep502 · não dói ─────────────
 {"id":"esc_nao_doi","ep":502,"serie":"Pé no Chão","temporada":"coluna","motif_family":"feet",
  "scenes":[
   {"k":"Escoliose","sc":["Escoliose costuma","não doer."],"e":"não doer",
    "sub":"Por isso o sinal é visual — e quem vê é quem olha as costas.",
    "vo":"A escoliose costuma não doer no começo. O sinal é visual, e quem vê é quem olha as costas."},
   {"k":"O que é","sc":["Um desvio em curva,","visto por trás."],"e":None,
    "sub":"A coluna, que deveria ser reta de trás, faz uma curva — e gira.",
    "vo":"É um desvio em curva da coluna, visto por trás: a coluna faz uma curva, e gira junto."},
   {"k":"Quando aparece","sc":["Mais no estirão","da pré-adolescência."],"e":None,
    "sub":"É a fase em que vale olhar as costas com atenção.",
    "vo":"Aparece mais no estirão da pré-adolescência. É a fase de olhar as costas com atenção."},
   {"k":"O que observar","sc":["Ombro, cintura, escápula:","um lado diferente."],"e":None,
    "sub":"Um ombro mais alto, a cintura assimétrica, uma escápula mais saliente.",
    "vo":"O que observar: um ombro mais alto, a cintura assimétrica, uma escápula mais saliente. Viu? Leve para avaliação."},
   {"k":"Passa adiante","sc":["Envia para quem","nunca olhou."],"e":None,"cta":True,
    "sub":"As costas contam o que a dor não conta.",
    "vo":"Envia para quem nunca olhou as costas do filho."},
  ],
  "caption":_cap("A escoliose costuma não doer no começo — por isso o sinal é visual, e quem vê é quem olha as costas: os pais, a escola, o pediatra. É um desvio em curva da coluna, visto por trás, que aparece mais no estirão da pré-adolescência. O que observar: um ombro mais alto que o outro, a cintura assimétrica, uma escápula mais saliente. Viu? Leve para avaliação.")},

 # ───────────── ep503 · estirão ─────────────
 {"id":"esc_estirao","ep":503,"serie":"Pé no Chão","temporada":"coluna","motif_family":"feet",
  "scenes":[
   {"k":"Escoliose","sc":["No estirão, a curva","pode mudar mais rápido."],"e":"mais rápido",
    "sub":"É por isso que o acompanhamento tem hora certa.",
    "vo":"No estirão de crescimento, a curva da escoliose pode mudar mais rápido. Por isso o acompanhamento tem hora certa."},
   {"k":"Por quê","sc":["Coluna crescendo","é coluna mudando."],"e":None,
    "sub":"Enquanto o esqueleto amadurece, a curva pode progredir.",
    "vo":"Por quê? Coluna crescendo é coluna mudando: enquanto o esqueleto amadurece, uma curva pode progredir."},
   {"k":"O que isso muda","sc":["O intervalo entre","as reavaliações."],"e":None,
    "sub":"Quem define esse intervalo é o ortopedista, caso a caso.",
    "vo":"O que muda é o intervalo entre as reavaliações, definido caso a caso pelo ortopedista."},
   {"k":"Em casa","sc":["Olhar as costas","de tempos em tempos."],"e":None,
    "sub":"Mudou algo entre uma consulta e outra? Antecipe a reavaliação.",
    "vo":"Em casa, olhe as costas de tempos em tempos. Mudou algo entre uma consulta e outra? Antecipe a reavaliação."},
   {"k":"Passa adiante","sc":["Envia para quem","tem filho no estirão."],"e":None,"cta":True,
    "sub":"Salva para a próxima consulta.",
    "vo":"Envia para quem tem filho no estirão."},
  ],
  "caption":_cap("No estirão de crescimento, a curva da escoliose pode mudar mais rápido — coluna crescendo é coluna mudando, e enquanto o esqueleto amadurece uma curva pode progredir. O que isso muda é o intervalo entre as reavaliações, definido caso a caso pelo ortopedista que acompanha. Em casa: olhe as costas de tempos em tempos; mudou algo entre uma consulta e outra, antecipe a reavaliação.")},
]

for _e, _lay in zip(ESCOLIOSE, _gl.layout_para_sequencia([e["id"] for e in ESCOLIOSE])):
    _e.setdefault("layout", _lay)
    _e.setdefault("palette", _gl.palette_para(_e["id"]))
