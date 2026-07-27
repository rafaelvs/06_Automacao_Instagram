# -*- coding: utf-8 -*-
"""
SÉRIE "Respondendo" (temporada "Você Perguntou") — 10 reels curtos de PERGUNTA & RESPOSTA.
Formato enxuto p/ retenção (<=5 cenas; vo total 60-78 palavras): a cena 0 é a PRÓPRIA PERGUNTA
como hook (kicker fixo "Você perguntou"; 1a frase do vo = a pergunta, já com a keyword leiga),
e a última cena (cta=True) fecha com send-first específico do tema + "salva".

TRIPLA KEYWORD NATIVA (casa com checar_v6.py): quando o item tem jargão canônico (GLOSSARIO de
checar_termo_popular), a MESMA keyword aparece nas 3 camadas da cena 0 — vo, on-screen (k/sc/sub) e
1a frase da caption. Itens sem jargão canônico (pino/fixador, pé torto, displasia, ponta dos pés)
reforçam a keyword LEIGA nativa nas 3 camadas e ficam fora do denominador do lint (sem gap).

CONTEÚDO: cada resposta usa SÓ o núcleo aprovado do material (subconjunto fiel; sem afirmação clínica
nova). Enquadramento honesto — "pergunta que sempre chega", NUNCA "paciente meu".
CFM (Res. 2.336/2023): educativo, sem prometer/insinuar resultado, sem sensacionalismo, sem estética/
altura no alongamento, sem conduta individual (avaliação/acompanhamento ok). Terminologia: sempre
"discrepância de membro"/"anisomelia" (nunca o termo vetado — ver PROIBIDOS em checar_termo_popular).
Rodapé CRM-SP 226103 · RQE 137901 + disclaimer entram pelo render.
"""
SIG = "Dr. Rafael Vargas · CRM-SP 226103 · RQE 137901"
DISCLAIMER = "Conteúdo educativo; não substitui avaliação individual."


def _cap(corpo, cta_linha, extra_tags):
    # espelha cap_ped/cap_rec de episodios_novos_2026: corpo + send-ask + salvar + hashtags + SIG + disclaimer
    return (corpo + "\n\n" + cta_linha
            + "\n📌 Salva pra lembrar. 💬 Dúvida? Comenta ou chama no direct.\n\n"
            + extra_tags + "\n\n" + SIG + "\n" + DISCLAIMER)


def cap_rec(corpo, extra_tags=""):
    # série "Osso Novo"/reconstrução: público adulto — send-ask por condição (SEND_OK no lint)
    return _cap(corpo, "📤 Manda pra quem tem essa mesma dúvida — ou vive isso agora.", extra_tags)


def cap_ped(corpo, extra_tags=""):
    # ortopedia pediátrica: send-ask por condição a um pai/mãe (SEND_OK no lint)
    return _cap(corpo, "📤 Manda pra quem tem essa mesma dúvida — um pai, uma mãe.", extra_tags)


QA_EPISODES = [

 # ───────────── ep1 · reconstrução · discrepância ─────────────
 {"id":"qa_perna_encurtou_acidente","ep":1,"serie":"Respondendo","temporada":"Você Perguntou","motif_family":"bone",
  "scenes":[
   {"k":"Você perguntou","sc":["A perna pode ficar","mais curta após um acidente?"],"e":None,
    "sub":"Discrepância de membro: quando o trauma encurta o osso.",
    "vo":"A perna pode ficar mais curta depois de um acidente grave? Pode — é a discrepância de membro."},
   {"k":"Por quê","sc":["O osso consolida","encurtado."],"e":None,"sub":"Traumas de alta energia podem consolidar o osso mais curto.",
    "vo":"Traumas de alta energia às vezes consolidam o osso já encurtado."},
   {"k":"Na criança","sc":["Cartilagem de","crescimento."],"e":None,"sub":"Em quem ainda cresce, lesão na cartilagem pede acompanhamento até o fim do crescimento.",
    "vo":"Em quem ainda cresce, a lesão da cartilagem de crescimento pede acompanhamento."},
   {"k":"A boa notícia","sc":["Tem avaliação","e tratamento."],"e":None,"sub":"A discrepância de membro tem avaliação e caminhos de tratamento.",
    "vo":"E fica a boa notícia: a discrepância de membro tem avaliação e caminhos de tratamento."},
   {"k":"Passa adiante","sc":["Manda pra quem","passou por isso."],"e":None,"sub":"Salva pra levar numa avaliação.","cta":True,
    "vo":"Manda pra quem tem essa mesma dúvida ou passou por um acidente assim, e salva pra lembrar."},
  ],
  "caption":cap_rec("A discrepância de membro (perna mais curta) pode, sim, surgir após um acidente grave. Traumas de alta energia às vezes fazem o osso consolidar encurtado, ou lesam a cartilagem de crescimento em quem ainda cresce — por isso fraturas importantes pedem acompanhamento até o fim do crescimento. E ela tem avaliação e caminhos de tratamento.","#discrepancia #reconstrucaoossea #fratura")},

 # ───────────── ep2 · reconstrução · Ilizarov (fixador) ─────────────
 {"id":"qa_gaiola_perna","ep":2,"serie":"Respondendo","temporada":"Você Perguntou","motif_family":"bone",
  "scenes":[
   {"k":"Você perguntou","sc":["Pra que serve a","'gaiola' de metal na perna?"],"e":None,
    "sub":"O fixador circular (Ilizarov) trata fratura, deformidade e discrepância de membro.",
    "vo":"Pra que serve aquela 'gaiola' de metal na perna? É o fixador circular, que trata fratura e discrepância de membro."},
   {"k":"Ilizarov","sc":["Corrige e","reconstrói o osso."],"e":None,"sub":"Trata fraturas complexas e corrige deformidades.",
    "vo":"É o método Ilizarov: corrige e reconstrói o osso."},
   {"k":"Como","sc":["Gradual e","controlado."],"e":None,"sub":"Ajustes ao longo de semanas, de forma gradual.",
    "vo":"Faz isso aos poucos, de forma gradual e controlada, com ajustes ao longo de semanas."},
   {"k":"Pra quê","sc":["Fratura, deformidade,","perna mais curta."],"e":None,"sub":"Serve para fraturas complexas, deformidades e discrepância.",
    "vo":"Serve pra fratura complexa, deformidade e pra corrigir uma perna mais curta."},
   {"k":"Passa adiante","sc":["Manda pra quem","vai usar fixador."],"e":None,"sub":"Salva pra lembrar.","cta":True,
    "vo":"Manda pra quem vive isso ou vai usar um fixador, e salva pra lembrar."},
  ],
  "caption":cap_rec("A discrepância de membro (uma perna mais curta) é um dos alvos daquela 'gaiola' de metal na perna — o fixador circular tipo Ilizarov. Ele trata fraturas complexas, corrige deformidades e reconstrói o osso de forma gradual e controlada, com ajustes ao longo de semanas.","#ilizarov #fixadorexterno #reconstrucaoossea")},

 # ───────────── ep3 · reconstrução · pseudoartrose ─────────────
 {"id":"qa_osso_nao_cola","ep":3,"serie":"Respondendo","temporada":"Você Perguntou","motif_family":"bone",
  "scenes":[
   {"k":"Você perguntou","sc":["Minha fratura","não colou. E agora?"],"e":None,
    "sub":"Quando o osso não cola no tempo esperado, chama-se pseudoartrose.",
    "vo":"Minha fratura não colou no tempo esperado — o que é pseudoartrose? É a falha de cicatrização do osso."},
   {"k":"O que é","sc":["O osso não","cicatriza no prazo."],"e":None,"sub":"A cicatrização não acontece no tempo esperado.",
    "vo":"É quando o osso não cicatriza no tempo esperado."},
   {"k":"Por quê","sc":["Instabilidade +","fatores do corpo."],"e":None,"sub":"Causas comuns: instabilidade no foco da fratura e fatores biológicos.",
    "vo":"As causas comuns são instabilidade no foco da fratura somada a fatores biológicos."},
   {"k":"Tem caminho","sc":["Tratamento:","caso a caso."],"e":None,"sub":"A avaliação especializada define o caminho caso a caso.",
    "vo":"Tem tratamento, e a avaliação especializada define o caminho por caso."},
   {"k":"Passa adiante","sc":["Manda pra quem","está há meses assim."],"e":None,"sub":"Salva pra levar numa reavaliação.","cta":True,
    "vo":"Manda pra quem tem essa mesma dúvida ou está há meses sem colar, e salva."},
  ],
  "caption":cap_rec("Pseudoartrose é a falha de consolidação: o osso não cola no tempo esperado. As causas comuns são instabilidade no foco da fratura somada a fatores biológicos. Tem tratamento — e a avaliação especializada define o caminho caso a caso.","#pseudoartrose #consolidacaoossea #fratura")},

 # ───────────── ep4 · reconstrução · consolidação (tempo) ─────────────
 {"id":"qa_tempo_osso_colar","ep":4,"serie":"Respondendo","temporada":"Você Perguntou","motif_family":"bone",
  "scenes":[
   {"k":"Você perguntou","sc":["Quanto tempo o osso","demora pra 'colar'?"],"e":None,
    "sub":"O tempo de consolidação varia — não há prazo único.",
    "vo":"Quanto tempo o osso demora pra 'colar' depois de uma fratura? O tempo de consolidação varia."},
   {"k":"Depende","sc":["Do osso e do","tipo de fratura."],"e":None,"sub":"Varia com o osso, o tipo de fratura, idade e saúde.",
    "vo":"Depende do osso, do tipo de fratura, da idade e da saúde da pessoa."},
   {"k":"Quanto","sc":["De semanas","a meses."],"e":"semanas","sub":"Vai de semanas a meses; não existe prazo fixo.",
    "vo":"Na prática, vai de semanas a meses — não existe um prazo único."},
   {"k":"Como saber","sc":["Clínica +","imagem."],"e":None,"sub":"O acompanhamento clínico e de imagem confirma a evolução.",
    "vo":"Quem confirma é o acompanhamento clínico e de imagem, ao longo do tempo."},
   {"k":"Passa adiante","sc":["Manda pra quem","está esperando colar."],"e":None,"sub":"Salva pra acompanhar com calma.","cta":True,
    "vo":"Manda pra quem vive essa espera pra colar, e salva pra lembrar."},
  ],
  "caption":cap_rec("O tempo de consolidação (o osso 'colar') varia com o osso, o tipo de fratura, a idade e o estado de saúde — de semanas a meses, sem prazo único. O acompanhamento clínico e de imagem confirma a evolução.","#consolidacaoossea #fratura #ortopedia")},

 # ───────────── ep5 · reconstrução · fixador externo (pino) ─────────────
 {"id":"qa_pino_frouxo","ep":5,"serie":"Respondendo","temporada":"Você Perguntou","motif_family":"bone",
  "scenes":[
   {"k":"Você perguntou","sc":["Um pino do fixador","parece frouxo. E agora?"],"e":None,
    "sub":"Pino do fixador externo frouxo: fale logo com a equipe.",
    "vo":"Um pino do meu fixador parece frouxo, o que eu faço? Comunique logo a equipe."},
   {"k":"Não faça","sc":["Não aperte por","conta própria."],"e":"Não","sub":"Ajustes fazem parte do método — não mexa sozinho.","motif":"no",
    "vo":"Ajustes fazem parte do método; não tente apertar por conta própria."},
   {"k":"Fique de olho","sc":["Sinais nos","trajetos dos pinos."],"e":None,"sub":"Secreção persistente, vermelhidão e dor local crescente.",
    "vo":"Fique de olho nos trajetos dos pinos: secreção persistente, vermelhidão e dor local crescente."},
   {"k":"O que fazer","sc":["Contato","precoce."],"e":None,"sub":"Avisar cedo evita complicação.",
    "vo":"O contato precoce com a equipe evita uma complicação."},
   {"k":"Passa adiante","sc":["Manda pra quem","usa fixador."],"e":None,"sub":"Salva pra ter à mão.","cta":True,
    "vo":"Manda pra quem vive isso ou usa um fixador, e salva pra ter à mão."},
  ],
  "caption":cap_rec("Um pino do fixador externo frouxo pede uma atitude simples: comunicar logo a equipe — ajustes fazem parte do método, e não se deve apertar por conta própria. Fique de olho nos trajetos dos pinos: secreção persistente, vermelhidão ou dor local crescente pedem contato precoce, que evita complicação.","#fixadorexterno #reconstrucaoossea #posoperatorio")},

 # ───────────── ep6 · reconstrução · consolidação (carga) ─────────────
 {"id":"qa_quando_pisar","ep":6,"serie":"Respondendo","temporada":"Você Perguntou","motif_family":"bone",
  "scenes":[
   {"k":"Você perguntou","sc":["Quando posso voltar","a pisar após a cirurgia?"],"e":None,
    "sub":"A carga depende da fixação e do estágio de consolidação.",
    "vo":"Quando posso voltar a pisar depois da cirurgia de fratura? Depende do estágio de consolidação."},
   {"k":"Não é data","sc":["Não é dia","fixo no calendário."],"e":None,"sub":"A liberação de carga não segue data fixa.",
    "vo":"Não é uma data fixa no calendário: a liberação de carga é individual."},
   {"k":"Depende de","sc":["Estabilidade e","estágio do osso."],"e":None,"sub":"Da estabilidade da fixação e do estágio de consolidação.",
    "vo":"Depende da estabilidade da fixação e de como o osso está evoluindo."},
   {"k":"Como voltar","sc":["Retorno","progressivo."],"e":None,"sub":"Guiado por quem conhece a fixação usada.","motif":"no",
    "vo":"O retorno é progressivo, guiado por quem conhece a fixação; antecipar carga por conta própria compromete o resultado."},
   {"k":"Passa adiante","sc":["Manda pra quem","vai voltar a pisar."],"e":None,"sub":"Salva pra lembrar.","cta":True,
    "vo":"Manda pra quem vive isso ou vai voltar a pisar, e salva pra lembrar."},
  ],
  "caption":cap_rec("A volta a pisar depende da estabilidade da fixação e do estágio de consolidação (o quanto o osso já colou) — não de uma data fixa. O retorno é progressivo, guiado por quem conhece a fixação usada; antecipar carga por conta própria pode comprometer o resultado.","#consolidacaoossea #posoperatorio #reabilitacao")},

 # ───────────── ep7 · pediátrica · pé torto (Ponseti) ─────────────
 {"id":"qa_pe_torto_bebe","ep":7,"serie":"Respondendo","temporada":"Você Perguntou","motif_family":"feet",
  "scenes":[
   {"k":"Você perguntou","sc":["Descobri na gravidez:","meu bebê tem pé torto."],"e":None,
    "sub":"Pé torto: o tratamento começa após o nascimento.",
    "vo":"Descobri na gravidez que meu bebê tem pé torto, e agora? Na gestação não há tratamento."},
   {"k":"Quando começa","sc":["Nas primeiras","semanas de vida."],"e":None,"sub":"Começa após o nascimento, cedo.",
    "vo":"Ele começa nas primeiras semanas de vida, logo após o nascimento."},
   {"k":"Como","sc":["Manipulação e","gessos seriados."],"e":None,"sub":"Método de Ponseti: manipulação suave e gessos em etapas.",
    "vo":"Com manipulação suave e gessos seriados, o método de Ponseti."},
   {"k":"A boa notícia","sc":["Boa correção descrita","quando cedo."],"e":None,"sub":"Boa taxa de correção descrita quando conduzido cedo.",
    "vo":"É o padrão de tratamento, com boa correção descrita quando conduzido cedo."},
   {"k":"Passa adiante","sc":["Manda pra quem","recebeu esse diagnóstico."],"e":None,"sub":"O diagnóstico na gravidez serve pra planejar.","cta":True,
    "vo":"Manda pra quem vive isso ou recebeu esse diagnóstico na gravidez, e salva."},
  ],
  "caption":cap_ped("Descobrir na gravidez que o bebê tem pé torto assusta, mas há caminho: na gestação não há tratamento — ele começa nas primeiras semanas de vida, com manipulação suave e gessos seriados (método de Ponseti), com boa taxa de correção descrita quando conduzido cedo. O diagnóstico na gravidez serve para planejar.","#petorto #ponseti #ortopediapediatrica")},

 # ───────────── ep8 · pediátrica · displasia (ultrassom) ─────────────
 {"id":"qa_ultrassom_quadril","ep":8,"serie":"Respondendo","temporada":"Você Perguntou","motif_family":"feet",
  "scenes":[
   {"k":"Você perguntou","sc":["Ultrassom do quadril","veio 'tipo 2a'. É grave?"],"e":None,
    "sub":"O ultrassom é a triagem da displasia do quadril.",
    "vo":"O ultrassom do quadril do meu bebê veio 'tipo 2a', é grave? É a triagem da displasia do quadril."},
   {"k":"Calma","sc":["Costuma ser","imaturidade."],"e":None,"sub":"Em bebê novinho, 'tipo 2a' costuma indicar imaturidade, não doença estabelecida.",
    "vo":"Em bebê novinho, esse laudo costuma indicar imaturidade, não doença estabelecida."},
   {"k":"O caminho","sc":["Acompanhamento","seriado."],"e":None,"sub":"Muitos evoluem bem com acompanhamento seriado, que confirma a evolução.",
    "vo":"Muitos evoluem bem com acompanhamento seriado — e é ele que confirma a evolução."},
   {"k":"Quem define","sc":["Ortopedista pediátrico,","com exame e imagem."],"e":None,"sub":"Quem interpreta a escala do laudo é o ortopedista pediátrico.",
    "vo":"Quem interpreta a escala do laudo é o ortopedista pediátrico, com exame e imagem."},
   {"k":"Passa adiante","sc":["Manda pra quem","recebeu esse laudo."],"e":None,"sub":"Salva pra levar na consulta.","cta":True,
    "vo":"Manda pra quem recebeu esse laudo e vive essa dúvida, e salva pra lembrar."},
  ],
  "caption":cap_ped("Na triagem da displasia do quadril, um ultrassom 'tipo 2a' assusta — mas, em bebê novinho, esse laudo costuma indicar imaturidade, não doença estabelecida. Muitos evoluem bem com acompanhamento seriado, e quem interpreta a escala é o ortopedista pediátrico, com exame e imagem.","#displasiadoquadril #ddq #ortopediapediatrica")},

 # ───────────── ep9 · pediátrica · pé plano (palmilha) ─────────────
 {"id":"qa_pe_chato_palmilha","ep":9,"serie":"Respondendo","temporada":"Você Perguntou","motif_family":"feet",
  "scenes":[
   {"k":"Você perguntou","sc":["Meu filho tem pé","chato. Precisa de palmilha?"],"e":None,
    "sub":"Pé chato (pé plano) flexível e indolor é muito comum.",
    "vo":"Meu filho tem pé chato, precisa de palmilha, botinha ou cirurgia? O pé plano flexível é muito comum."},
   {"k":"A regra","sc":["Flexível e sem dor:","costuma melhorar sozinho."],"e":None,"sub":"A maioria melhora com o crescimento, sem tratamento.",
    "vo":"Sendo flexível e indolor, a maioria melhora com o crescimento, sem tratamento."},
   {"k":"O que importa","sc":["É a função,","não a foto."],"e":"função","sub":"Dor, rigidez ou limitação é que pedem avaliação.",
    "vo":"O que importa é a função: dor, rigidez ou limitação é que pedem avaliação."},
   {"k":"Mitos","sc":["Palmilha não","molda o pé."],"e":"não","sub":"Palmilha e botinha não 'moldam' o pé; cirurgia é caso específico.","motif":"no",
    "vo":"Palmilha e botinha não moldam o pé, e cirurgia é para casos específicos."},
   {"k":"Passa adiante","sc":["Manda pra quem","vai comprar palmilha."],"e":None,"sub":"Salva antes da próxima compra.","cta":True,
    "vo":"Manda pra quem vive essa dúvida ou vai comprar palmilha, e salva."},
  ],
  "caption":cap_ped("O pé chato (pé plano) flexível e indolor é muito comum e, na maioria, melhora com o crescimento, sem tratamento. O que importa é a função: dor, rigidez ou limitação é que pedem avaliação. Palmilha e botinha não 'moldam' o pé; cirurgia é para casos específicos.","#pechato #peplano #ortopediapediatrica")},

 # ───────────── ep10 · pediátrica · ponta dos pés ─────────────
 {"id":"qa_ponta_dos_pes","ep":10,"serie":"Respondendo","temporada":"Você Perguntou","motif_family":"feet",
  "scenes":[
   {"k":"Você perguntou","sc":["Meu filho anda na","ponta dos pés. Tem tratamento?"],"e":None,
    "sub":"Andar na ponta dos pés: causas vão de hábito a encurtamento na panturrilha.",
    "vo":"Meu filho sempre anda na ponta dos pés, tem tratamento? Depende da causa."},
   {"k":"Muitas vezes","sc":["Hábito que passa","sozinho."],"e":None,"sub":"Costuma ser hábito da infância que desaparece sozinho.",
    "vo":"Muitas vezes é um hábito da infância que desaparece sozinho."},
   {"k":"Às vezes","sc":["Encurtamento real","na panturrilha."],"e":None,"sub":"Pode haver um encurtamento real na panturrilha, ou outras causas.",
    "vo":"Às vezes há um encurtamento real na panturrilha, ou outras causas que merecem investigação."},
   {"k":"Quando avaliar","sc":["Persistente ou","só de um lado."],"e":None,"sub":"Persistente, limitante ou só de um lado pede avaliação.","motif":"no",
    "vo":"Se é persistente, limitante ou só de um lado, a avaliação ortopédica define a causa."},
   {"k":"Passa adiante","sc":["Manda pra quem","vê o filho na pontinha."],"e":None,"sub":"Salva pra observar com calma.","cta":True,
    "vo":"Manda pra quem vive isso ou vê o filho na pontinha, e salva pra lembrar."},
  ],
  "caption":cap_ped("Andar na ponta dos pés o tempo todo pode ir de um hábito da infância, que desaparece sozinho, até um encurtamento real na panturrilha, ou outras causas que merecem investigação. Persistente, limitante ou só de um lado pede avaliação ortopédica para definir a causa e as opções.","#andarnapontadope #marcha #ortopediapediatrica")},

]

# ── ROLLOUT anti-templatização (espelha episodios_lote_julho_2026 / pós-op): layout + paleta por id. ──
# setdefault → opt-in explícito por episódio ainda vence; toca SÓ os QA_EPISODES (não afeta as outras
# séries). layout="auto" deixa o render resolver via ganchos_layout; palette determinística por id.
import ganchos_layout as _gl
for _e in QA_EPISODES:
    _e.setdefault("layout", "auto")
    _e.setdefault("palette", _gl.palette_para(_e["id"]))
