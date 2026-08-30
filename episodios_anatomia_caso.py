# -*- coding: utf-8 -*-
"""
SÉRIE "Anatomia de um Caso" — 3 pilotos (30/08/2026). Caso REAL da literatura, narrado,
com ILUSTRAÇÕES ESQUEMÁTICAS originais (ilustracoes_caso.py) na banda média do frame —
nunca radiografia realista, nunca corpo/rosto identificável, nunca imagem do paciente.

APROVAÇÃO: formato aprovado pelo Rafael em 30/08/2026 ("pode seguir"). Roteiros = os 3
pilotos revisados (piloto_caso_transporte_tibia.md, piloto_caso_osteomielite_0cm.md,
piloto_caso_silver_russell.md). Registro no gate (aprovacoes.json) segue o fluxo padrão
antes de qualquer enfileiramento.

ALTERAÇÃO REGISTRADA (decisão do Rafael, 30/08, via recomendação conservadora do checklist
item 2 do piloto 1): "sem amputação" → "a perna foi preservada" na cena 3 (sub e vo) e na
caption do ep301. O artigo cita amputação como risco geral do tipo de lesão, não como
ameaça afirmada a ESTE paciente — a forma preservadora é a literal.

Campos além do padrão da casa:
  layout: "manchete_regua" EXPLÍCITO (hook no topo, y<820 → banda média y∈[870,1310]
          livre para a ilustração; nenhum layout novo foi criado).
  ilustracao (por cena): {"tipo": <ilustracoes_caso._TIPOS>, ...params} — o motor suprime
          o motivo (_bone) nessa cena e desenha o quadro esquemático na banda média.
Ep 303 RESERVADO (piloto 3 não aprovado nesta leva); ids/eps: 301, 302, 304.
"""

ANATOMIA_CASO = [
 # ═══ ep301 · caso_transporte_tibia · Pentela 2023 (PMC10226645) ═══
 # Perda de 17,2 cm da tíbia (Gustilo IIIB) → transporte ósseo com Ilizarov, 4 meses.
 # Sem ritmo diário no roteiro (o artigo não informa — não inventar).
 {"id":"caso_transporte_tibia","ep":301,"temporada":"anatomia_caso","serie":"Anatomia de um Caso",
  "motif_family":"bone","palette":"carvao_quente","layout":"manchete_regua",
  "scenes":[
   {"k":"ELE PERDEU 17 CM DE OSSO","sc":["E o osso","voltou."],"e":None,
    "sub":"Caso real da literatura médica — ilustração esquemática.",
    "ilustracao":{"tipo":"osso_falha","orientacao":"h","cota":"17,2 cm"},
    "vo":"Ele perdeu dezessete centímetros de osso."},
   {"k":"O acidente","sc":["Faltavam 17,2 cm","de tíbia."],"e":None,
    "sub":"Homem de 29 anos, acidente de trânsito — caso publicado em 2023.",
    "ilustracao":{"tipo":"osso_falha","orientacao":"v","cota":"17,2 cm",
                  "nota":"a pele também sofreu"},
    "vo":"Um homem de vinte e nove anos, um acidente de trânsito: o osso da canela perdeu dezessete vírgula dois centímetros. E a primeira reconstrução da pele falhou."},
   {"k":"O transporte ósseo","sc":["Um pedaço viaja.","O corpo preenche."],"e":"devagarinho",
    "sub":"Fixador circular de Ilizarov: 4 meses de transporte, aos poucos.",
    "ilustracao":{"tipo":"fixador_transporte","rotulo_corte":"corte no osso saudável",
                  "rotulo_novo":"osso novo","rotulo_tempo":"4 meses, aos poucos"},
    "vo":"Com o fixador circular de Ilizarov, a equipe cortou o osso saudável e foi puxando devagarinho, por quatro meses. Atrás dele, o corpo fabricava osso novo: o transporte ósseo."},
   # cena 3: troca registrada — "sem amputação" → "a perna foi preservada" (sub e vo)
   {"k":"O desfecho","sc":["Andando sem apoio.","De volta ao trabalho."],"e":None,
    "sub":"A perna foi preservada — ficou 1,5 cm de encurtamento e rigidez no tornozelo.",
    "ilustracao":{"tipo":"osso_continuo","arco_tornozelo":True,
                  "selos":["de volta ao trabalho","ficou 1,5 cm de encurtamento","rigidez (10°)"]},
    "vo":"No fim: andando sem apoio, de volta ao trabalho — a perna foi preservada. O que ficou: um centímetro e meio de encurtamento e rigidez no tornozelo."},
   {"k":"Caso real da literatura","sc":["Envia. Salva.","Cada caso é único."],"e":None,
    "sub":"Fonte: Pentela et al., 2023 · Dr. Rafael Vargas · CRM-SP 226103 · RQE 137901.",
    "ilustracao":{"tipo":"osso_continuo","esmaecido":True,
                  "citacao":["Pentela HK et al.","Journal of Orthopaedic Case Reports · 2023"]},
    "vo":"Caso real da literatura médica, tratado por outra equipe. Cada caso é único. Envia para quem precisa conhecer o transporte ósseo."},
  ],
  # caption: troca registrada — "sem amputação" → "a perna foi preservada"
  "caption":"Ele perdeu 17,2 cm do osso da canela (tíbia) num acidente de trânsito — e voltou a andar e trabalhar. Caso real publicado na literatura médica, tratado por outra equipe.\n\nDepois de a primeira reconstrução da pele ter falhado, os médicos usaram o fixador circular de Ilizarov: cortaram o osso saudável e foram puxando o segmento aos poucos, por 4 meses — no espaço que abria, o corpo fabricava osso novo. É o transporte ósseo.\n\nO desfecho, com a parte honesta: ele voltou ao trabalho andando sem apoio, a perna foi preservada — e ficou com 1,5 cm de encurtamento e uma contratura de 10° no tornozelo. Cada caso é único: este é o relato de UM paciente, publicado pelos médicos que o trataram. As ilustrações são esquemáticas — não são imagens do paciente.\n\nEnvia para alguém que precisa entender como o transporte ósseo funciona — e salva para rever depois.\n\nNarração com voz digital (IA).\nFonte: Pentela HK, Harshavardhan JKG, Suriyakumar S. Journal of Orthopaedic Case Reports, 2023;13(5):9-13.\n\nDr. Rafael Vargas · CRM-SP 226103 · RQE 137901 — Reconstrução e Alongamento Ósseo · Ortopedia Pediátrica.\nConteúdo educativo; não substitui avaliação individual.\n\n#transporteosseo #ilizarov #fixadorexterno #reconstrucaoossea #perdaossea"},

 # ═══ ep302 · caso_osteomielite_0cm · Hong 2023 (PMC9958936) ═══
 # Sequela de osteomielite: perna arqueada, 14 cm a menos; correção 17 anos depois em 3
 # etapas; diferença final 0,1 cm. Sempre "alongou a perna" (o ganho correu pela fíbula).
 {"id":"caso_osteomielite_0cm","ep":302,"temporada":"anatomia_caso","serie":"Anatomia de um Caso",
  "motif_family":"bone","palette":"noturno_azul","layout":"manchete_regua",
  "scenes":[
   {"k":"17 ANOS DE ESPERA","sc":["A diferença final?","Um milímetro."],"e":None,
    "sub":"Caso real da literatura médica — ilustração esquemática.",
    "ilustracao":{"tipo":"linha_tempo","anos":"17 anos","cota":"14 cm a menos",
                  "nota":"infecção no osso (osteomielite)"},
    "vo":"A correção esperou dezessete anos."},
   {"k":"A sequela","sc":["Perna arqueada,","14 cm a menos."],"e":None,
    "sub":"Osteomielite na infância pode alterar o crescimento do osso.",
    "ilustracao":{"tipo":"linha_tempo","zoom":True,"cota":"14 cm a menos"},
    "vo":"A osteomielite deixou a perna arqueada e catorze centímetros mais curta. Aos vinte e quatro anos, chegou ao hospital mancando."},
   {"k":"A correção em 3 etapas","sc":["Anéis que endireitam.","Placa que segura."],"e":None,
    "sub":"1 mm por dia, por 4 meses; a placa saiu 15 meses depois.",
    "ilustracao":{"tipo":"painel_triplo"},
    "vo":"Foram três etapas: o fixador circular endireitou e alongou a perna, um milímetro por dia, por quatro meses. Depois, uma placa externa discreta segurou o osso até firmar."},
   {"k":"A diferença final","sc":["0,1 cm.","Um milímetro."],"e":"milímetro",
    "sub":"Sem compensação no calçado — e com rigidez no tornozelo.",
    "ilustracao":{"tipo":"regua_resultado","cota":"0,1 cm"},
    "vo":"A diferença final: um milímetro. Voltou ao dia a dia sem mancar. O custo honesto: rigidez no tornozelo. O joelho, quase normal."},
   {"k":"Caso da literatura","sc":["Tratado por outra equipe.","Cada caso é único."],"e":None,
    "sub":"Dr. Rafael Vargas · CRM-SP 226103 · RQE 137901.",
    "ilustracao":{"tipo":"regua_resultado","cota":"0,1 cm","esmaecido":True,
                  "citacao":["Hong P et al.","Medicina (Kaunas) · 2023"]},
    "vo":"Caso real da literatura médica, tratado por outra equipe. Cada caso é único. Envia para quem espera há anos por uma correção."},
  ],
  "caption":"Uma infecção no osso na infância deixou a perna dele arqueada e 14 cm mais curta — a correção veio 17 anos depois, e a diferença final ficou em 0,1 cm.\n\nCaso real publicado na literatura médica e tratado por outra equipe (Hong e colaboradores, 2023, revista Medicina — Kaunas). As ilustrações são esquemáticas: não são imagens do paciente.\n\nAos 24 anos, ele chegou ao hospital mancando. A correção teve 3 etapas: o fixador circular de Ilizarov endireitou e alongou a perna (1 mm por dia, por 4 meses); uma placa externa de perfil baixo substituiu o aparelho volumoso até o osso firmar; e, por fim, a placa foi retirada, 15 meses depois. A parte honesta do desfecho: o tornozelo ficou com rigidez importante — o joelho ficou quase normal — e houve duas infecções no trajeto dos pinos, tratadas com antibiótico.\n\nCada caso é único: este é o relato de UM paciente, publicado pelos médicos que o trataram. Não é promessa de resultado.\n\n📤 Envia para alguém que convive há anos com uma sequela e acha que não tem mais jeito. E salva para rever.\n\nNarração com voz digital (IA).\n\nReferência: Hong P, Ding Y, Xu R, Rai S, Liu R, Li J. Medicina (Kaunas), 2023;59(2):262. doi: 10.3390/medicina59020262\n\nDr. Rafael Vargas · CRM-SP 226103 · RQE 137901 — Reconstrução e Alongamento Ósseo · Ortopedia Pediátrica.\nConteúdo educativo; não substitui avaliação individual.\n\n#osteomielite #alongamentoosseo #fixadorexterno #ilizarov #ortopediapediatrica #reconstrucaoossea"},

 # ═══ ep304 · caso_silver_russell · Al Kaissi 2015 (PMC4955504) — ep 303 RESERVADO ═══
 # Piloto PEDIÁTRICO. GUARDRAILS: zero estética/estatura; "discrepância" (nunca o termo
 # vetado); desfecho literal (órtese abaixo do joelho + calçado 5 cm); sem rosto na arte.
 {"id":"caso_silver_russell","ep":304,"temporada":"anatomia_caso","serie":"Anatomia de um Caso",
  "motif_family":"bone","palette":"verde_clinico","layout":"manchete_regua",
  "scenes":[
   {"k":"15 CENTÍMETROS A MENOS","sc":["Uma menina.","Um plano de 6 anos."],"e":None,
    "sub":"Caso real da literatura médica — ilustração esquemática.",
    "ilustracao":{"tipo":"figura_discrepancia","cota":"diferença: 15 cm"},
    "vo":"Uma perna quinze centímetros mais curta."},
   {"k":"A condição","sc":["Síndrome de","Silver-Russell."],"e":None,
    "sub":"Genética e rara — e não afetava só a perna.",
    "ilustracao":{"tipo":"figura_discrepancia","cota":"diferença: 15 cm"},
    "vo":"Ela tinha síndrome de Silver-Russell, uma condição genética rara — e, além da discrepância, escoliose e luxação do quadril."},
   {"k":"O plano","sc":["7 cirurgias.","Dos 7 aos 13 anos."],"e":"fixador",
    "sub":"Quadril, coluna e o fixador circular no fêmur e na tíbia.",
    "ilustracao":{"tipo":"trilha_cirurgias","ini":"7 anos","fim":"13 anos"},
    "vo":"Dos sete aos treze anos, sete cirurgias: corrigir o quadril, firmar a coluna e, com o fixador circular, alongar fêmur e tíbia — o pé foi junto no aparelho."},
   {"k":"O resultado","sc":["De 15 cm","para 5 cm."],"e":None,
    "sub":"Anda com órtese abaixo do joelho e calçado 5 cm mais alto — e há risco de recidiva.",
    "ilustracao":{"tipo":"ortese_resultado","cota":"diferença: 5 cm — compensada",
                  "cota_calcado":"5 cm","selo":"os autores relatam risco de recidiva"},
    "vo":"A diferença caiu de quinze para cinco centímetros. Ela anda com órtese abaixo do joelho e compensação no calçado — e os autores avisam: pode voltar a aumentar."},
   {"k":"Cada caso é único","sc":["Envia para quem","precisa entender."],"e":None,
    "sub":"Dr. Rafael Vargas · CRM-SP 226103 · RQE 137901.",
    "ilustracao":{"tipo":"ortese_resultado","cota":"diferença: 5 cm — compensada",
                  "cota_calcado":"5 cm","esmaecido":True,
                  "citacao":["Al Kaissi A et al.","Afr J Paediatr Surg · 2015"]},
    "vo":"Caso real da literatura médica, tratado por outra equipe — cada caso é único. Envia para alguém que precisa entender esse caminho. E salva."},
  ],
  "caption":"Uma perna 15 cm mais curta — e o plano de 6 anos de uma menina com síndrome de Silver-Russell. Caso real publicado na literatura médica e tratado por outra equipe — não é paciente meu. As ilustrações são esquemáticas: não são imagens da paciente.\n\nDos 7 aos 13 anos foram 7 cirurgias: corrigir o quadril, firmar a coluna e, com o fixador circular, alongar fêmur e tíbia, com o pé incluído no aparelho. No caminho, o osso novo se mostrou frágil e precisou de hastes internas de proteção. A discrepância caiu de 15 para 5 cm: ela anda com o apoio de uma órtese abaixo do joelho e com calçado 5 cm mais alto. E os próprios autores alertam para o alto risco de recidiva em síndromes assim. Cada caso é único: este é o relato de UMA paciente, publicado pelos médicos que a trataram.\n\nConhece uma família que vive um plano longo desses? Envia este vídeo para ela — e salva para rever.\n\nNarração com voz digital (IA).\n\nFonte: Al Kaissi A, Ganger R, Mindler G, Karner C, Klaushofer K, Grill F. Correction of the axial and appendicular deformities in a patient with Silver-Russel syndrome. Afr J Paediatr Surg. 2015;12(1):36-40. doi: 10.4103/0189-6725.150969 (PMC4955504).\n\nDr. Rafael Vargas · CRM-SP 226103 · RQE 137901 — Reconstrução e Alongamento Ósseo · Ortopedia Pediátrica.\nConteúdo educativo; não substitui avaliação individual.\n\n#alongamentoosseo #ortopediapediatrica #sindromedesilverrussell #fixadorexterno #discrepanciademembros"},
]

if __name__ == "__main__":
    print(len(ANATOMIA_CASO), "episódios 'Anatomia de um Caso':")
    for e in ANATOMIA_CASO:
        n_il = sum(1 for s in e["scenes"] if "ilustracao" in s)
        print(f"  ep{e['ep']} {e['id']:24s} cenas={len(e['scenes'])} ilustradas={n_il} "
              f"palette={e['palette']} layout={e['layout']}")
