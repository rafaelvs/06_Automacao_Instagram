# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════════════════════╗
║  APROVADO PELO DR. RAFAEL EM 30/08/2026 (decisão D3, chat auditoria-instagram-v1) ║
║  Registro: aprovacoes.json · lote qa_lote2 (hash por episódio).                   ║
║  Notas de consenso (ep11 gesso / ep16 dor do crescimento) apresentadas no pacote  ║
║  de decisões e mantidas sinalizadas abaixo.                                       ║
╚══════════════════════════════════════════════════════════════════════════════════╝

SÉRIE "Respondendo" (temporada "Você Perguntou") — LOTE 2 · 12 rascunhos de episódio (ep11–ep22).
Seleção = itens #1 a #12 do ranking de PAUTA_QA_LOTE2.md (17 titulares + 2 reservas; os itens
#13–#17 e as reservas ficam na pauta aguardando o corte/reordenação do Rafael — meta D3: >=12).
Mix deste lote: 8 reconstrução/nicho + 4 pediátrica (espelha a proporção 6+4 do lote 1).

FORMATO: idêntico ao lote 1 (episodios_qa_respondendo.py) — <=5 cenas; vo total 60–78 palavras;
cena 0 = a PRÓPRIA PERGUNTA como hook (kicker fixo "Você perguntou"; 1ª frase do vo = a pergunta,
já com a keyword leiga); última cena (cta=True) fecha com send-first específico do tema + "salva".
TRIPLA KEYWORD NATIVA: a keyword de SEO da pauta aparece nas 3 camadas da cena 0 — vo, on-screen
(k/sc/sub) e 1ª frase da caption. motif_family segue a convenção do lote 1 (bone=reconstrução,
feet=pediátrica).

CONTEÚDO: cada resposta usa SÓ o núcleo aprovado de answer_bank.py (CORE + ALERT; subconjunto
fiel — nenhuma afirmação clínica nova, nenhum número sem fonte). Resposta em tese, nunca conduta
individual. Enquadramento honesto — "pergunta que sempre chega", NUNCA "paciente meu".
CFM (Res. 2.336/2023 e 2.454): educativo, sem prometer/insinuar resultado, sem sensacionalismo,
sem estética/altura no alongamento (tabu — nenhum item deste lote toca o tema), sem conduta
individual. Terminologia: sempre "discrepância de membro"/"anisomelia" (nunca o termo vetado).
Rodapé CRM-SP 226103 · RQE 137901 + disclaimer entram pelo render.

⚠️ PONTOS A CONFERIR NO AVAL CLÍNICO (sinalização honesta — únicos trechos que vão além do texto
literal do answer_bank.py; ambos são consenso leigo de cuidado, sem número e sem conduta nova):
  · ep11 (gesso): "o gesso comum não é feito para molhar" e "não introduza objetos para coçar —
    podem ferir a pele". Sinais de alerta e "não retirar por conta própria" vêm do banco.
  · ep16 (dor do crescimento): a existência do quadro benigno é consenso (ângulo aprovado na
    pauta); os sinais que descartam "do crescimento" vêm do ALERT pediatria do banco.

⚠️ NOTA DE FORMATO: o _cap do lote 1 traz a linha fixa "💬 Dúvida? Comenta ou chama no direct."
— pedido de comentário é sinal REFUTADO pela análise (top-3 = send/save), e o guardrail da S1
veta CTA de comentário. Neste rascunho a linha foi ajustada para "💬 Dúvida? Chama no direct."
(sem o "Comenta ou"). [⚠ REVISAR: se o Rafael mantiver o _cap antigo do lote 1 em produção,
alinhar lá também — a mudança vale para as duas temporadas, não por episódio.]

DROP-IN: quando aprovado, este arquivo vive ao lado de ganchos_layout.py (mesma pasta do motor);
os episódios podem ser anexados a QA_EPISODES do lote 1 (a numeração ep11–ep22 já continua a
sequência) ou consumidos como módulo próprio. cap_rec/cap_ped/_cap são cópias fiéis do lote 1.
"""
SIG = "Dr. Rafael Vargas · CRM-SP 226103 · RQE 137901"
DISCLAIMER = "Conteúdo educativo; não substitui avaliação individual."
IA_DISCLOSURE = "Narração com voz digital (IA)."  # CFM 2.454/2026 (D6, aprovado 30/08/2026)


def _cap(corpo, cta_linha, extra_tags):
    # espelha cap_ped/cap_rec de episodios_novos_2026: corpo + send-ask + salvar + hashtags + SIG + disclaimer
    return (corpo + "\n\n" + cta_linha
            + "\n📌 Salva pra lembrar. 💬 Dúvida? Chama no direct.\n\n"
            + extra_tags + "\n\n" + IA_DISCLOSURE + "\n" + SIG + "\n" + DISCLAIMER)


def cap_rec(corpo, extra_tags=""):
    # série "Osso Novo"/reconstrução: público adulto — send-ask por condição (SEND_OK no lint)
    return _cap(corpo, "📤 Manda pra quem tem essa mesma dúvida — ou vive isso agora.", extra_tags)


def cap_ped(corpo, extra_tags=""):
    # ortopedia pediátrica: send-ask por condição a um pai/mãe (SEND_OK no lint)
    return _cap(corpo, "📤 Manda pra quem tem essa mesma dúvida — um pai, uma mãe.", extra_tags)


QA_EPISODES_LOTE2 = [

 # ───────────── ep11 · pediátrica · gesso (pauta #1 · fratura_consolidacao, n=46) ─────────────
 {"id":"qa_gesso_molhar","ep":11,"serie":"Respondendo","temporada":"Você Perguntou","motif_family":"feet",
  "scenes":[
   {"k":"Você perguntou","sc":["O gesso do meu filho","pode molhar? E se coçar?"],"e":None,
    "sub":"Cuidados com o gesso: o que fazer e o que observar.",
    "vo":"O gesso do meu filho pode molhar? E se coçar lá dentro? Siga a orientação da equipe."},
   {"k":"Regra geral","sc":["Gesso comum não","é feito pra molhar."],"e":None,"sub":"O gesso comum não é feito para molhar; a equipe orienta como proteger no banho.",
    "vo":"O gesso comum não é feito para molhar — a equipe orienta como proteger no banho."},
   {"k":"Coceira","sc":["Nada de objetos","dentro do gesso."],"e":"Não","sub":"Não introduza objetos para coçar: podem ferir a pele lá dentro.","motif":"no",
    "vo":"Coçou? Não introduza objetos dentro do gesso — podem ferir a pele."},
   {"k":"Sinais de alerta","sc":["Dedos frios, pálidos","ou muito inchados."],"e":None,"sub":"Dedos frios, pálidos, formigando ou muito inchados dentro do gesso: retorno imediato.",
    "vo":"Fique de olho: dedos frios, pálidos, formigando ou muito inchados pedem retorno imediato."},
   {"k":"Passa adiante","sc":["Manda pra quem tem","criança engessada."],"e":None,"sub":"Salva pra ter à mão.","cta":True,
    "vo":"Manda pra quem tem uma criança engessada em casa, e salva pra ter à mão."},
  ],
  "caption":cap_ped("Cuidados com o gesso: ele não é feito para molhar (a equipe orienta como proteger no banho) e nada de introduzir objetos para coçar — podem ferir a pele lá dentro. O mais importante são os sinais de alerta: dedos frios, pálidos, formigando ou muito inchados dentro do gesso pedem retorno imediato. E imobilização não se retira por conta própria.","#gesso #fratura #ortopediapediatrica")},

 # ───────────── ep12 · reconstrução · retirada de material (pauta #2 · pos_op_fixacao, n=28) ─────────────
 {"id":"qa_tirar_placa","ep":12,"serie":"Respondendo","temporada":"Você Perguntou","motif_family":"bone",
  "scenes":[
   {"k":"Você perguntou","sc":["O osso colou. Preciso","tirar a placa e os parafusos?"],"e":None,
    "sub":"Retirada de placa e parafusos: nem sempre é necessária.",
    "vo":"O osso colou — preciso tirar a placa e os parafusos? Nem sempre."},
   {"k":"A regra","sc":["Retirada nem sempre","é necessária."],"e":None,"sub":"A retirada do material de síntese nem sempre é necessária.",
    "vo":"A retirada do material de síntese nem sempre é necessária."},
   {"k":"Quando sim","sc":["Tem indicação e","tempo próprios."],"e":None,"sub":"Quando indicada, a retirada tem um tempo próprio.",
    "vo":"Quando indicada, ela tem um tempo próprio, definido caso a caso."},
   {"k":"Quem decide","sc":["O cirurgião, com","apoio das radiografias."],"e":None,"sub":"A decisão é do cirurgião que acompanha o caso, com apoio das radiografias.",
    "vo":"Quem decide é o cirurgião que acompanha o caso, com apoio das radiografias."},
   {"k":"Passa adiante","sc":["Manda pra quem","convive com a placa."],"e":None,"sub":"Salva pra levar na consulta.","cta":True,
    "vo":"Manda pra quem tem essa mesma dúvida ou convive com a placa, e salva pra levar na consulta."},
  ],
  "caption":cap_rec("Retirada de placa e parafusos: nem sempre é necessária. Quando indicada, a retirada do material de síntese tem um tempo próprio — a decisão é do cirurgião que acompanha o caso, com apoio das radiografias, sempre caso a caso.","#retiradadeplaca #osteossintese #posoperatorio")},

 # ───────────── ep13 · reconstrução · consolidação × tabagismo (pauta #3 · fratura_consolidacao, n=46) ─────────────
 {"id":"qa_cigarro_osso","ep":13,"serie":"Respondendo","temporada":"Você Perguntou","motif_family":"bone",
  "scenes":[
   {"k":"Você perguntou","sc":["Fumar atrasa o","osso a colar?"],"e":None,
    "sub":"Tabagismo está entre os fatores que retardam a consolidação óssea.",
    "vo":"Fumar atrasa o osso a colar? Atrasa — o tabagismo está entre os fatores que retardam a consolidação óssea."},
   {"k":"Não está só","sc":["Diabetes e nutrição","também pesam."],"e":None,"sub":"Diabetes e nutrição inadequada também podem retardar a cicatrização.",
    "vo":"E não está sozinho: diabetes e nutrição inadequada também podem retardar a cicatrização."},
   {"k":"A boa notícia","sc":["São fatores que dá","pra controlar."],"e":None,"sub":"Controlar esses fatores ajuda bastante a consolidação.",
    "vo":"A boa notícia: são fatores que dá pra controlar — e controlar ajuda bastante."},
   {"k":"Junto disso","sc":["Siga a orientação de","carga e imobilização."],"e":None,"sub":"Seguir a orientação de carga e imobilização favorece a melhor consolidação.",
    "vo":"Junto disso, seguir a orientação de carga e imobilização favorece a melhor consolidação."},
   {"k":"Passa adiante","sc":["Manda pra quem","fuma e fraturou."],"e":None,"sub":"Salva pra lembrar.","cta":True,
    "vo":"Manda pra quem fuma e está esperando o osso colar, e salva pra lembrar."},
  ],
  "caption":cap_rec("Consolidação óssea e cigarro: o tabagismo está entre os fatores que retardam a cicatrização do osso, junto de diabetes e nutrição inadequada. A boa notícia é que são fatores que dá para controlar — e controlar ajuda bastante, junto de seguir a orientação de carga e imobilização do seu ortopedista.","#consolidacaoossea #fratura #tabagismo")},

 # ───────────── ep14 · reconstrução/NICHO · tempo de fixador (pauta #4 · fixador_ilizarov, n=24) ─────────────
 {"id":"qa_tempo_fixador","ep":14,"serie":"Respondendo","temporada":"Você Perguntou","motif_family":"bone",
  "scenes":[
   {"k":"Você perguntou","sc":["Quanto tempo vou ficar","com o fixador na perna?"],"e":None,
    "sub":"Fixador externo: o tempo de tratamento não tem prazo único.",
    "vo":"Quanto tempo vou ficar com o fixador externo na perna? Não existe prazo único."},
   {"k":"Depende","sc":["Do objetivo do","tratamento."],"e":None,"sub":"Fratura complexa, correção de deformidade ou reconstrução: cada objetivo tem seu ritmo.",
    "vo":"Depende do objetivo: fratura complexa, correção de deformidade ou reconstrução do osso."},
   {"k":"Quem mostra","sc":["A evolução nas","radiografias."],"e":None,"sub":"O acompanhamento com radiografias seriadas mostra a evolução.",
    "vo":"Quem mostra o caminho é a evolução do osso nas radiografias seriadas."},
   {"k":"Enquanto isso","sc":["Cuidados diários e","fisioterapia."],"e":None,"sub":"Higiene dos pinos, ritmo de ajuste e fisioterapia fazem parte do método.",
    "vo":"Enquanto isso, higiene dos pinos, ritmo de ajuste e fisioterapia fazem parte do método."},
   {"k":"Passa adiante","sc":["Manda pra quem","usa fixador."],"e":None,"sub":"Salva pra lembrar.","cta":True,
    "vo":"Manda pra quem usa fixador ou vai começar essa jornada, e salva pra lembrar."},
  ],
  "caption":cap_rec("Fixador externo: quanto tempo de tratamento? Não existe prazo único — depende do objetivo (fratura complexa, correção de deformidade, reconstrução) e da evolução do osso, acompanhada por radiografias seriadas. Enquanto o aparelho está em uso, higiene diária dos pinos, ritmo de ajuste orientado pela equipe e fisioterapia fazem parte do método.","#fixadorexterno #ilizarov #reconstrucaoossea")},

 # ───────────── ep15 · reconstrução/NICHO · higiene dos pinos (pauta #5 · fixador_ilizarov, n=24) ─────────────
 {"id":"qa_banho_fixador","ep":15,"serie":"Respondendo","temporada":"Você Perguntou","motif_family":"bone",
  "scenes":[
   {"k":"Você perguntou","sc":["Posso tomar banho com","o fixador? E os pinos?"],"e":None,
    "sub":"Cuidados com o fixador externo: higiene diária dos trajetos dos pinos.",
    "vo":"Posso tomar banho com o fixador externo? Como limpo os pinos? A equipe ensina a rotina."},
   {"k":"Por quê","sc":["Higiene diária","previne infecção."],"e":None,"sub":"A higiene diária dos trajetos dos pinos previne infecção.",
    "vo":"A higiene diária dos trajetos dos pinos é parte do tratamento: previne infecção."},
   {"k":"Normal","sc":["Pequenas reações locais","costumam ocorrer."],"e":None,"sub":"Pequenas reações na pele ao redor dos pinos nem sempre indicam problema.",
    "vo":"Pequenas reações na pele ao redor dos pinos costumam ocorrer e nem sempre indicam problema."},
   {"k":"Alerta","sc":["Secreção, mau cheiro,","vermelhidão que aumenta."],"e":None,"sub":"Secreção purulenta ou com mau cheiro, vermelhidão que aumenta ou febre: contato precoce.","motif":"no",
    "vo":"Já secreção com mau cheiro, vermelhidão que aumenta ou febre pedem contato precoce."},
   {"k":"Passa adiante","sc":["Manda pra quem","usa fixador."],"e":None,"sub":"Salva pra ter à mão.","cta":True,
    "vo":"Manda pra quem usa fixador e vive essa rotina, e salva pra ter à mão."},
  ],
  "caption":cap_rec("Cuidados com o fixador externo: a higiene diária dos trajetos dos pinos é parte do tratamento e previne infecção — a equipe ensina a rotina, inclusive como fazer no banho. Pequenas reações na pele ao redor dos pinos costumam ocorrer e nem sempre indicam problema; já secreção purulenta ou com mau cheiro, vermelhidão que aumenta ou febre pedem contato precoce com a equipe.","#fixadorexterno #ilizarov #posoperatorio")},

 # ───────────── ep16 · pediátrica · dor do crescimento (pauta #6 · pediatria, n=6) ─────────────
 {"id":"qa_dor_crescimento","ep":16,"serie":"Respondendo","temporada":"Você Perguntou","motif_family":"feet",
  "scenes":[
   {"k":"Você perguntou","sc":["Dor do crescimento existe","ou é desculpa?"],"e":None,
    "sub":"Dor do crescimento: existe — e tem sinais que descartam o quadro benigno.",
    "vo":"Dor do crescimento existe mesmo ou é desculpa? Existe — e é comum na infância."},
   {"k":"Como costuma ser","sc":["Vai e vem, sem","outros sinais."],"e":None,"sub":"O quadro benigno vai e vem, sem outros sinais associados.",
    "vo":"O quadro benigno é o que vai e vem, sem nenhum outro sinal."},
   {"k":"Não é do crescimento","sc":["Dor persistente, que","acorda a criança."],"e":None,"sub":"Dor persistente, que acorda a criança à noite, com mancar ou febre, pede avaliação.","motif":"no",
    "vo":"Já dor persistente, que acorda a criança à noite, com mancar ou febre, não é."},
   {"k":"O caminho","sc":["Avaliação com ortopedista","pediátrico."],"e":None,"sub":"A avaliação separa o que é fisiológico do que precisa de tratamento.",
    "vo":"Esses sinais pedem avaliação com ortopedista pediátrico, pra separar o benigno do que precisa de cuidado."},
   {"k":"Passa adiante","sc":["Manda pra quem ouve","'é do crescimento'."],"e":None,"sub":"Salva pra observar com calma.","cta":True,
    "vo":"Manda pra quem sempre ouve que 'é do crescimento', e salva pra observar com calma."},
  ],
  "caption":cap_ped("Dor do crescimento existe — é um quadro benigno e comum da infância, que vai e vem sem outros sinais. O que não é 'do crescimento': dor persistente, que acorda a criança à noite, com mancar, febre ou inchaço — esses sinais pedem avaliação com ortopedista pediátrico, para separar o que é fisiológico do que precisa de tratamento.","#dordocrescimento #ortopediapediatrica #saudeinfantil")},

 # ───────────── ep17 · pediátrica · claudicação (pauta #7 · pediatria, n=6) ─────────────
 {"id":"qa_crianca_mancando","ep":17,"serie":"Respondendo","temporada":"Você Perguntou","motif_family":"feet",
  "scenes":[
   {"k":"Você perguntou","sc":["Meu filho está mancando","sem ter batido. E agora?"],"e":None,
    "sub":"Criança mancando sem trauma: sinal que merece atenção.",
    "vo":"Meu filho está mancando e não bateu em lugar nenhum — o que pode ser? Merece atenção."},
   {"k":"Não é frescura","sc":["Mancar sem trauma","não é 'manha'."],"e":None,"sub":"Claudicação (mancar) persistente na criança não deve ser ignorada.",
    "vo":"Mancar sem trauma não é manha: a claudicação persistente não deve ser ignorada."},
   {"k":"Fique de olho","sc":["Dor à noite, febre,","inchaço."],"e":None,"sub":"Mancar que não melhora, dor que acorda à noite, febre ou inchaço apressam a consulta.","motif":"no",
    "vo":"Mancar que não melhora, dor que acorda à noite, febre ou inchaço apressam a consulta."},
   {"k":"O caminho","sc":["Avaliação com ortopedista","pediátrico."],"e":None,"sub":"A avaliação separa o que é passageiro do que precisa de tratamento.",
    "vo":"A avaliação com ortopedista pediátrico separa o que é passageiro do que precisa de tratamento."},
   {"k":"Passa adiante","sc":["Manda pra quem viu","o filho mancar."],"e":None,"sub":"Salva pra agir cedo.","cta":True,
    "vo":"Manda pra quem já viu o filho mancar do nada, e salva pra agir cedo."},
  ],
  "caption":cap_ped("Criança mancando sem trauma não é 'manha': claudicação persistente merece avaliação com ortopedista pediátrico, para separar o que é passageiro do que precisa de tratamento. Apressam a consulta: mancar que não melhora, dor que acorda a criança à noite, febre, inchaço ou perda de movimento.","#claudicacao #ortopediapediatrica #saudeinfantil")},

 # ───────────── ep18 · pediátrica · lesão óssea benigna (pauta #8 · tumor_osseo, n=3) ─────────────
 {"id":"qa_caroco_no_osso","ep":18,"serie":"Respondendo","temporada":"Você Perguntou","motif_family":"feet",
  "scenes":[
   {"k":"Você perguntou","sc":["Apareceu um caroço duro","no osso do meu filho."],"e":None,
    "sub":"Caroço no osso da criança: pode ser o osteocondroma, lesão benigna comum.",
    "vo":"Apareceu um caroço duro no osso do meu filho — é grave? Pode ser um osteocondroma, lesão benigna comum."},
   {"k":"Calma","sc":["Na criança, a maioria","é benigna."],"e":None,"sub":"A maioria das lesões ósseas na criança é benigna.",
    "vo":"Respira: na criança, a maioria das lesões ósseas é benigna."},
   {"k":"Quem define","sc":["Exame clínico +","imagem."],"e":None,"sub":"Somente a avaliação com exame clínico e imagem define a natureza da lesão.",
    "vo":"Mas quem define é a avaliação: exame clínico e exames de imagem, como a radiografia."},
   {"k":"Apressam a consulta","sc":["Crescimento rápido ou","dor à noite."],"e":None,"sub":"Aumento rápido da lesão, dor que acorda à noite ou febre apressam a consulta.","motif":"no",
    "vo":"Aumento rápido da lesão, dor que acorda à noite ou febre apressam a consulta."},
   {"k":"Passa adiante","sc":["Manda pra quem notou","um caroço assim."],"e":None,"sub":"Salva pra levar na consulta.","cta":True,
    "vo":"Manda pra quem notou um caroço assim no filho, e salva pra levar na consulta."},
  ],
  "caption":cap_ped("Osteocondroma (exostose) é uma das lesões benignas e comuns que aparecem como um 'caroço duro' no osso da criança. A maioria das lesões ósseas na infância é benigna — mas somente a avaliação especializada, com exame clínico e exames de imagem, define a natureza da lesão e a conduta. Apressam a consulta: aumento rápido da lesão, dor que acorda à noite ou febre.","#osteocondroma #exostose #ortopediapediatrica")},

 # ───────────── ep19 · reconstrução/NICHO · discrepância: conduta (pauta #9 · discrepância, >=4 reais) ─────────────
 {"id":"qa_perna_curta_operar","ep":19,"serie":"Respondendo","temporada":"Você Perguntou","motif_family":"bone",
  "scenes":[
   {"k":"Você perguntou","sc":["Uma perna mais curta:","sempre precisa operar?"],"e":None,
    "sub":"Discrepância de membro: a conduta depende da magnitude, da idade e da causa.",
    "vo":"Uma perna mais curta que a outra sempre precisa operar? Não — é a discrepância de membro."},
   {"k":"Primeiro: medir","sc":["Exame clínico +","escanometria."],"e":None,"sub":"A diferença é medida com precisão por exame clínico e escanometria.",
    "vo":"Primeiro se mede com precisão, com exame clínico e radiografias como a escanometria."},
   {"k":"Diferenças pequenas","sc":["Compensação e","observação."],"e":None,"sub":"Diferenças pequenas: palmilha de compensação e acompanhamento.",
    "vo":"Diferenças pequenas costumam ser conduzidas com palmilha de compensação e observação."},
   {"k":"Casos selecionados","sc":["Correção em casos","selecionados."],"e":None,"sub":"Diferenças maiores podem ter indicação de correção — magnitude, idade e causa orientam.",
    "vo":"Já diferenças maiores podem ter indicação de correção — depende da magnitude, da idade e da causa."},
   {"k":"Passa adiante","sc":["Manda pra quem convive","com essa diferença."],"e":None,"sub":"Salva pra levar numa avaliação.","cta":True,
    "vo":"Manda pra quem convive com essa diferença, e salva pra levar numa avaliação."},
  ],
  "caption":cap_rec("Discrepância de membro (uma perna mais curta): nem sempre precisa operar. A diferença é medida com precisão por exame clínico e radiografias como a escanometria; diferenças pequenas costumam ser conduzidas com palmilha de compensação e observação, e as maiores podem ter indicação de correção — a conduta depende da magnitude, da idade e da causa, sempre de forma individualizada.","#discrepancia #anisomelia #reconstrucaoossea")},

 # ───────────── ep20 · reconstrução/NICHO · ajuste do fixador (pauta #10 · fixador_ilizarov, n=24) ─────────────
 {"id":"qa_ajustar_fixador","ep":20,"serie":"Respondendo","temporada":"Você Perguntou","motif_family":"bone",
  "scenes":[
   {"k":"Você perguntou","sc":["Ajustar o fixador dói?","O que vou sentir?"],"e":None,
    "sub":"Método Ilizarov: desconfortos leves são comuns durante a correção.",
    "vo":"Ajustar o fixador dói? No método Ilizarov, desconfortos leves são comuns ao longo do tratamento."},
   {"k":"O que é normal","sc":["Desconforto leve e","reações discretas na pele."],"e":None,"sub":"Desconfortos leves e reações discretas na pele ao redor dos pinos são comuns.",
    "vo":"É esperado sentir desconforto leve, e reações discretas na pele dos pinos acontecem."},
   {"k":"O ritmo importa","sc":["Ajuste no ritmo","orientado pela equipe."],"e":None,"sub":"O ritmo de ajuste é programado e orientado pela equipe.",
    "vo":"O ajuste segue um ritmo programado, orientado pela equipe — cumprir esse ritmo é fundamental."},
   {"k":"Não é normal","sc":["Dor intensa e","progressiva."],"e":"Não","sub":"Dor intensa e progressiva não é esperada: contato com a equipe.","motif":"no",
    "vo":"Já dor intensa e progressiva não é esperada — é caso de contato com a equipe."},
   {"k":"Passa adiante","sc":["Manda pra quem vai","começar a correção."],"e":None,"sub":"Salva pra lembrar.","cta":True,
    "vo":"Manda pra quem vai começar a correção, e salva pra lembrar."},
  ],
  "caption":cap_rec("Método Ilizarov: ajustar o fixador dói? Desconfortos leves e reações discretas na pele ao redor dos pinos são comuns ao longo do tratamento, e o ajuste segue um ritmo programado, orientado pela equipe. Dor intensa e progressiva, porém, não é esperada — é caso de contato precoce com a equipe.","#ilizarov #fixadorexterno #reconstrucaoossea")},

 # ───────────── ep21 · reconstrução · calo ósseo (pauta #11 · fratura_consolidacao, n=46) ─────────────
 {"id":"qa_calo_osseo","ep":21,"serie":"Respondendo","temporada":"Você Perguntou","motif_family":"bone",
  "scenes":[
   {"k":"Você perguntou","sc":["O que é o 'calo ósseo'","do meu raio-X?"],"e":None,
    "sub":"Calo ósseo: o osso cicatrizando.",
    "vo":"O que é esse 'calo ósseo' que apareceu no meu raio-X? É o osso cicatrizando."},
   {"k":"O que é","sc":["Tecido novo no","lugar da fratura."],"e":None,"sub":"Na cicatrização, o corpo forma um calo no lugar da fratura.",
    "vo":"Na cicatrização óssea, o corpo forma tecido novo no lugar da fratura."},
   {"k":"Com o tempo","sc":["Vai ganhando","resistência."],"e":None,"sub":"O calo vai ganhando resistência com o tempo — consolidação em andamento.",
    "vo":"Esse calo vai ganhando resistência com o tempo — é sinal de consolidação em andamento."},
   {"k":"Quem acompanha","sc":["Radiografias","seriadas."],"e":None,"sub":"Radiografias seriadas mostram a evolução e guiam a liberação de carga.",
    "vo":"Radiografias seriadas mostram a evolução e indicam a hora de liberar carga e movimento."},
   {"k":"Passa adiante","sc":["Manda pra quem leu","isso no laudo."],"e":None,"sub":"Salva pra lembrar.","cta":True,
    "vo":"Manda pra quem leu isso no laudo e ficou na dúvida, e salva."},
  ],
  "caption":cap_rec("Calo ósseo é o osso cicatrizando: na consolidação, o corpo forma tecido novo no lugar da fratura, e esse calo vai ganhando resistência com o tempo. As radiografias seriadas mostram a evolução e indicam quando liberar carga e movimento — por isso o acompanhamento faz diferença.","#caloosseo #consolidacaoossea #fratura")},

 # ───────────── ep22 · reconstrução/NICHO · refratura (pauta #12 · pseudartrose, n=2) ─────────────
 {"id":"qa_refratura","ep":22,"serie":"Respondendo","temporada":"Você Perguntou","motif_family":"bone",
  "scenes":[
   {"k":"Você perguntou","sc":["Quebrei o mesmo osso","de novo. Por quê?"],"e":None,
    "sub":"Refratura: quebrar de novo pede investigação da causa.",
    "vo":"Quebrei o mesmo osso de novo — por que refraturou? Isso pede investigação da causa."},
   {"k":"Possíveis causas","sc":["Fixação, biologia,","carga antes da hora."],"e":None,"sub":"Instabilidade da fixação, fatores do paciente e esforço precoce entram na conta.",
    "vo":"Instabilidade da fixação, fatores do paciente e esforço antes da hora entram na conta."},
   {"k":"Por isso","sc":["Investigar antes de","tratar igual."],"e":None,"sub":"Investigar a causa evita tratar de novo do mesmo jeito.",
    "vo":"Por isso se investiga antes de simplesmente tratar de novo do mesmo jeito."},
   {"k":"Tem caminho","sc":["Tratamento","individualizado."],"e":None,"sub":"O tratamento é individualizado: pode envolver revisão da fixação e enxerto ósseo.",
    "vo":"O tratamento é individualizado — pode envolver revisão da fixação e enxerto ósseo."},
   {"k":"Passa adiante","sc":["Manda pra quem passou","por uma refratura."],"e":None,"sub":"Salva pra levar na consulta.","cta":True,
    "vo":"Manda pra quem passou por uma refratura, e salva pra levar na consulta."},
  ],
  "caption":cap_rec("Refratura — quebrar o mesmo osso de novo — pede investigação da causa: estabilidade da fixação, fatores do paciente (como tabagismo e diabetes) e o momento do retorno à carga entram na conta. O tratamento é individualizado e pode envolver revisão da fixação, enxerto ósseo e, em casos selecionados, reconstrução com fixador externo.","#refratura #pseudoartrose #reconstrucaoossea")},

]

# ── ROLLOUT anti-templatização (idêntico ao lote 1): layout + paleta por id. ──
# setdefault → opt-in explícito por episódio ainda vence; toca SÓ os QA_EPISODES_LOTE2.
# layout="auto" deixa o render resolver via ganchos_layout; palette determinística por id.
# NOTA DE RASCUNHO: este import exige que o arquivo viva na pasta do motor (ao lado de
# ganchos_layout.py), como o lote 1 — no scratchpad ele falha de propósito (fail-closed).
import ganchos_layout as _gl
for _e in QA_EPISODES_LOTE2:
    _e.setdefault("layout", "auto")
    _e.setdefault("palette", _gl.palette_para(_e["id"]))


QA_LOTE2 = QA_EPISODES_LOTE2  # alias p/ o agregador
