# -*- coding: utf-8 -*-
"""
SÉRIE "FIXADOR EXTERNO POR DENTRO" — 8 episódios (12/09/2026, plano de saída da estagnação, B2 + B4).

POR QUE ESTA SÉRIE: é a maior lacuna medida do levantamento de 11/09 — 178 sugestões de busca para
"fixador externo", 93% de paciente/família ("como higienizar", "como dormir", "como sentar",
"inflamado o que fazer"); índice de busca 5,29 na escala escoliose=100 (~1.300× "discrepância de
membros"); mediana de 13.252 views no YouTube PT-BR e 0 de 12 resultados com ≤60s; o conteúdo que
rankeia tem 6 a 14 anos. É o nicho exato do perfil, 100% compatível com faceless, e está vago.

FORMATO: ≤5 cenas, vo total 60–78 palavras (~2,2 palavras/s → 30–35 s), cena 0 = gancho na fala
do paciente, última cena cta=True (envio). Capa v2 do render (render_reel A3): a cena 0 mostra só
o gancho + o herói visual; kicker/sub/CTA entram a partir de 3,5 s.

TESTE CONTROLADO DE GANCHO (B4) — sorteio CONGELADO antes de escrever, seed
"saida-estagnacao-2026-09-12-gancho" (ver PLANO_EXPERIMENTOS.md):
  BRAÇO A — fragmento nominal com número/risco e a resolução já no gancho:
            fx_sentar_levantar, fx_roupa, fx_pino_inflamado, fx_retirada
  BRAÇO B — pergunta do paciente + kicker de série (o gancho atual):
            fx_kit_casa, fx_viagem, fx_curativo_pinos, fx_dormir
  Os "números" do braço A são CONTAGENS DE ITENS DO PRÓPRIO VÍDEO (3 sinais, 2 movimentos, 1 regra),
  nunca estatística clínica — regra da casa: nenhum número sem fonte.

CONTEÚDO: orientação GERAL de convivência com o aparelho — subconjunto do que a casa já publicou e
aprovou (qa_banho_fixador, vida_cotidiana_fixador, c_on_cuidado_pinos, fim_tratamento): nenhuma
afirmação clínica nova, nenhuma conduta individual, nenhum número sem fonte. Sempre "quem decide é a
sua equipe/o seu cirurgião". Sinais de alerta = os mesmos do acervo (secreção purulenta/mau cheiro,
vermelhidão que aumenta, dor nova, febre → contato precoce; pronto-socorro se febre).
CFM 2.336/2023 e 2.454/2026: educativo, sem promessa, sem paciente real, rodapé CRM/RQE pelo render,
"Narração com voz digital (IA)" na legenda. Terminologia: fixador externo / método Ilizarov;
"discrepância de membro" quando aparecer (NUNCA o termo vetado). Alongamento sempre funcional.

APROVAÇÃO: lote FIXADOR-POR-DENTRO-2026-09-12 em aprovacoes.json — decisão "vamos fazer tudo,
prossiga" (12/09) sobre o plano, item B2; revisão passiva do Rafael na fila antes da data de cada
peça (PROGRAMACAO.md).
"""
import ganchos_layout as _gl

SIG = "Dr. Rafael Vargas · Médico · CRM-SP 226103 · RQE 137901 — Reconstrução e Alongamento Ósseo · Ortopedia Pediátrica."
DISC = "Conteúdo educativo; não substitui avaliação individual."
IA = "Narração com voz digital (IA)."
MENCAO = "Sociedade da área: @asami.brasil"


def _cap(corpo, cta="Envia para quem está com o fixador — ou cuida de quem está."):
    return corpo + "\n\n" + cta + "\n\n" + MENCAO + "\n\n" + IA + "\n" + SIG + "\n" + DISC


SERIE = "Fixador por dentro"

FIXADOR = [

 # ───────────── ep401 · BRAÇO B · curativo dos pinos ─────────────
 {"id":"fx_curativo_pinos","ep":401,"serie":SERIE,"temporada":"fixador","motif_family":"bone",
  "scenes":[
   {"k":"Fixador por dentro","sc":["Como limpar os pinos","do fixador em casa?"],"e":None,
    "sub":"A rotina que a equipe ensina — e os sinais que pedem contato.",
    "vo":"Como limpar os pinos do fixador em casa? A rotina é a que a sua equipe ensinou."},
   {"k":"Antes de tudo","sc":["Mãos limpas.","Um material por pino."],"e":"Um",
    "sub":"Lave as mãos; não passe o mesmo material de um pino para o outro.",
    "vo":"Mãos lavadas. E cada pino com o seu material: nunca a mesma gaze de um pino para o outro."},
   {"k":"O que não fazer","sc":["Não arranque","as crostas."],"e":"Não","motif":"no",
    "sub":"Nem pomadas ou produtos por conta própria — só o que a equipe orientou.",
    "vo":"Não arranque crostas, nem pomada por conta própria. Só o que a equipe orientou."},
   {"k":"Fique de olho","sc":["Pus, mau cheiro,","vermelhidão que cresce."],"e":None,
    "sub":"Reações leves na pele são comuns; esses sinais pedem contato precoce. Febre: pronto-socorro.",
    "vo":"Reação leve na pele é comum. Pus, mau cheiro, vermelhidão que cresce ou dor nova: avise cedo. Febre: pronto-socorro."},
   {"k":"Passa adiante","sc":["Envia para quem","está com o fixador."],"e":None,"cta":True,
    "sub":"Ou para quem cuida de alguém que está.",
    "vo":"Envia para quem cuida de um fixador."},
  ],
  "caption":_cap("Como limpar os pinos do fixador externo em casa? A rotina é a que a sua equipe ensinou; o que vale para todo mundo: mãos lavadas, um material para cada pino (nunca o mesmo de um pino para o outro), sem arrancar crostas e sem pomada ou produto por conta própria. Reações leves na pele são comuns — já secreção com pus ou mau cheiro, vermelhidão que aumenta, dor nova ou febre pedem contato precoce com a equipe (febre: pronto-socorro).")},

 # ───────────── ep402 · BRAÇO B · dormir ─────────────
 {"id":"fx_dormir","ep":402,"serie":SERIE,"temporada":"fixador","motif_family":"bone",
  "scenes":[
   {"k":"Fixador por dentro","sc":["Como dormir com","o fixador externo?"],"e":None,
    "sub":"Apoio, proteção e a posição que a equipe liberou.",
    "vo":"Como dormir com o fixador externo? Dá para dormir bem, com três ajustes."},
   {"k":"Apoio","sc":["A perna descansa","apoiada, não pendurada."],"e":"apoiada",
    "sub":"Travesseiro ou apoio sob a perna: o peso do aparelho não deve puxar nem girar a perna.",
    "vo":"Apoio: um travesseiro sob a perna, para o aparelho não puxar nem girar a perna à noite."},
   {"k":"Proteção","sc":["Uma capa de tecido","sobre o aparelho."],"e":None,
    "sub":"Evita enroscar no lençol e protege quem dorme ao lado.",
    "vo":"Proteção: uma capa de tecido sobre o aparelho, que não enrosca no lençol e protege quem dorme ao lado."},
   {"k":"Posição","sc":["A que a equipe","liberou para você."],"e":None,
    "sub":"Cada fase do tratamento pode ter uma orientação diferente.",
    "vo":"Posição: a que a equipe liberou; cada fase tem a sua. Dor forte e nova ao acordar: avise."},
   {"k":"Passa adiante","sc":["Envia para quem","vai dormir com ele."],"e":None,"cta":True,
    "sub":"Salva para a primeira noite.",
    "vo":"Envia para quem vai passar a primeira noite com o fixador."},
  ],
  "caption":_cap("Como dormir com o fixador externo? Três ajustes: apoio (travesseiro sob a perna, para o peso do aparelho não puxar nem girar a perna à noite), proteção (uma capa de tecido sobre o aparelho, que evita enroscar no lençol e protege quem dorme ao lado) e a posição que a sua equipe liberou — cada fase do tratamento pode ter uma orientação diferente. Dor forte e nova ao acordar: avise a equipe.")},

 # ───────────── ep403 · BRAÇO A · sentar e levantar ─────────────
 {"id":"fx_sentar_levantar","ep":403,"serie":SERIE,"temporada":"fixador","motif_family":"bone",
  "scenes":[
   {"k":"Fixador por dentro","sc":["2 movimentos para","sentar e levantar."],"e":"2",
    "sub":"Com fixador externo, a cadeira certa e a ordem certa poupam a perna.",
    "vo":"Dois movimentos para sentar e levantar com o fixador, sem forçar a perna. Antes, a cadeira certa."},
   {"k":"A cadeira","sc":["Firme, com braços,","não muito baixa."],"e":None,
    "sub":"Cadeira baixa ou macia demais obriga a forçar o joelho e o aparelho.",
    "vo":"Cadeira firme, com braços e não muito baixa. Baixa ou macia demais obriga a forçar o joelho e o aparelho."},
   {"k":"Movimento 1","sc":["Chega à borda.","Apoia nos braços."],"e":None,
    "sub":"A perna do aparelho vai à frente, apoiada, antes de subir.",
    "vo":"Um: chega à borda do assento, mãos nos braços da cadeira, perna do aparelho à frente, apoiada."},
   {"k":"Movimento 2","sc":["Sobe pela perna","que está livre."],"e":None,
    "sub":"O aparelho não é alça: use-o só do jeito que a equipe mostrou.",
    "vo":"Movimento dois: sobe pela perna livre. O aparelho não é alça: use-o só do jeito que a equipe mostrou."},
   {"k":"Passa adiante","sc":["Envia para quem","está reaprendendo."],"e":None,"cta":True,
    "sub":"Sentar, levantar, um dia de cada vez.",
    "vo":"Envia para quem está reaprendendo."},
  ],
  "caption":_cap("Sentar e levantar com o fixador externo: dois movimentos e a cadeira certa. A cadeira: firme, com braços e não muito baixa — cadeira baixa ou macia demais obriga a forçar o joelho e o aparelho. Movimento 1: chegue à borda do assento e apoie as mãos nos braços, com a perna do aparelho à frente e apoiada. Movimento 2: suba pela perna que está livre. O aparelho não é alça: use-o para apoiar a perna só do jeito que a sua equipe mostrou.")},

 # ───────────── ep404 · BRAÇO A · roupa ─────────────
 {"id":"fx_roupa","ep":404,"serie":SERIE,"temporada":"fixador","motif_family":"bone",
  "scenes":[
   {"k":"Fixador por dentro","sc":["Roupa e fixador:","1 regra resolve."],"e":"1",
    "sub":"A peça abre antes de entrar — nunca passa forçada por cima dos pinos.",
    "vo":"Roupa e fixador: uma regra resolve quase tudo. A peça abre antes de entrar, nunca passa forçada sobre os pinos."},
   {"k":"Calça","sc":["Larga, com abertura","lateral ou shorts."],"e":None,
    "sub":"Velcro ou botões na lateral da perna facilitam; a perna do aparelho veste primeiro.",
    "vo":"Calça larga com abertura lateral, de velcro ou botões, ou shorts. A perna do aparelho veste primeiro."},
   {"k":"Pé e meia","sc":["Calçado aberto","do lado do aparelho."],"e":None,
    "sub":"O pé pode inchar mais nesse lado; calçado com ajuste facilita.",
    "vo":"No pé desse lado, calçado mais aberto ou com ajuste: ele pode inchar mais."},
   {"k":"Capa","sc":["Uma capa de tecido","protege o aparelho."],"e":None,
    "sub":"Não enrosca, não expõe, e fica mais confortável na rua.",
    "vo":"E uma capa de tecido no aparelho: não enrosca, não expõe os pinos. Detalhes, com a equipe."},
   {"k":"Passa adiante","sc":["Envia para quem","vai sair de casa."],"e":None,"cta":True,
    "sub":"Salva para o dia de se vestir.",
    "vo":"Envia para quem vai sair de casa com o fixador."},
  ],
  "caption":_cap("Roupa e fixador externo: uma regra resolve quase tudo — a peça abre antes de entrar, nunca passa forçada por cima dos pinos. Calça larga com abertura lateral (velcro ou botões) ou shorts, com a perna do aparelho vestindo primeiro; no pé desse lado, calçado mais aberto ou com ajuste, porque ele pode inchar mais; e uma capa de tecido sobre o aparelho, que não enrosca, não expõe os pinos e fica mais confortável na rua. Detalhes do seu caso: com a sua equipe.")},

 # ───────────── ep405 · BRAÇO B · viagem e deslocamento ─────────────
 {"id":"fx_viagem","ep":405,"serie":SERIE,"temporada":"fixador","motif_family":"bone",
  "scenes":[
   {"k":"Fixador por dentro","sc":["Posso viajar com","o fixador externo?"],"e":None,
    "sub":"Depende da fase — e do planejamento com a equipe.",
    "vo":"Posso viajar com o fixador externo? Depende da fase do tratamento, e de combinar antes com a equipe."},
   {"k":"No carro","sc":["Perna apoiada,","paradas para mover."],"e":None,
    "sub":"Banco que permita esticar a perna; pare para se movimentar no trajeto.",
    "vo":"No carro, a perna vai apoiada, num banco que permita esticar. Em trajetos longos, pare para se movimentar."},
   {"k":"Na bagagem","sc":["O kit de curativo","vai junto."],"e":None,
    "sub":"E um relatório da equipe: o aparelho é de metal e chama o detector.",
    "vo":"Na bagagem, o kit de curativo e um relatório da equipe: o aparelho é de metal e chama o detector."},
   {"k":"O calendário","sc":["Ajustes e consultas","não podem ficar para trás."],"e":None,
    "sub":"Na fase de alongamento, os ajustes têm dia certo — planeje a viagem em volta deles.",
    "vo":"E o calendário: ajustes e consultas têm dia certo. A viagem se planeja em volta deles."},
   {"k":"Passa adiante","sc":["Envia para quem","está planejando."],"e":None,"cta":True,
    "sub":"Salva para conversar com a equipe.",
    "vo":"Envia para quem está planejando viajar."},
  ],
  "caption":_cap("Posso viajar com o fixador externo? Depende da fase do tratamento — e de combinar antes com a equipe. No carro: perna apoiada, banco que permita esticar e paradas para se movimentar. Na bagagem: o kit de curativo e um relatório da equipe (o aparelho é de metal e chama o detector do aeroporto). E o calendário: na fase de alongamento os ajustes têm dia certo, e as consultas também — a viagem se planeja em volta deles.")},

 # ───────────── ep406 · BRAÇO A · pino inflamado ─────────────
 {"id":"fx_pino_inflamado","ep":406,"serie":SERIE,"temporada":"fixador","motif_family":"bone",
  "scenes":[
   {"k":"Fixador por dentro","sc":["3 sinais no pino que","não esperam o retorno."],"e":"3",
    "sub":"Pus ou mau cheiro, vermelhidão que cresce, dor nova. Com febre: pronto-socorro.",
    "vo":"Três sinais no pino do fixador que não esperam o retorno: pus ou mau cheiro, vermelhidão que cresce, dor nova. Febre: pronto-socorro."},
   {"k":"O que é comum","sc":["Reação leve na pele","costuma acontecer."],"e":None,
    "sub":"Um pouco de vermelhidão ou secreção clara nem sempre indica problema.",
    "vo":"O comum: reação leve na pele ao redor do pino, pouca vermelhidão ou secreção clara. Nem sempre é problema."},
   {"k":"O que muda","sc":["Piora, cresce,","passa a doer."],"e":"Piora","motif":"no",
    "sub":"É a evolução que importa: o que piora em vez de melhorar pede avaliação.",
    "vo":"O que muda a leitura é a evolução: o que piora, cresce ou dói pede avaliação."},
   {"k":"O que não fazer","sc":["Antibiótico ou pomada","por conta própria."],"e":None,
    "sub":"Quem decide o tratamento do trajeto do pino é a equipe que acompanha.",
    "vo":"E nada de antibiótico ou pomada por conta própria. Quem decide é a equipe."},
   {"k":"Passa adiante","sc":["Envia para quem","cuida dos pinos."],"e":None,"cta":True,
    "sub":"Salva para o dia da dúvida.",
    "vo":"Envia para quem cuida dos pinos."},
  ],
  "caption":_cap("Três sinais no pino do fixador externo que não esperam a próxima consulta: secreção com pus ou mau cheiro, vermelhidão que aumenta e dor nova — com febre, pronto-socorro. O que é comum: uma reação leve na pele ao redor do pino, com pouca vermelhidão ou secreção clara, nem sempre indica problema. O que muda a leitura é a evolução: o que piora, cresce ou passa a doer pede avaliação. Nada de antibiótico ou pomada por conta própria — quem decide é a equipe que acompanha o caso.")},

 # ───────────── ep407 · BRAÇO A · retirada ─────────────
 {"id":"fx_retirada","ep":407,"serie":SERIE,"temporada":"fixador","motif_family":"bone",
  "scenes":[
   {"k":"Fixador por dentro","sc":["O dia de tirar o fixador:","o que acontece depois."],"e":None,
    "sub":"O aparelho sai; o osso novo ainda está ganhando resistência.",
    "vo":"O dia de tirar o fixador: o que acontece, e o que vem depois."},
   {"k":"A retirada","sc":["É um procedimento,","com hora marcada."],"e":None,
    "sub":"Feita pela equipe, em ambiente adequado, conforme o caso.",
    "vo":"A retirada é procedimento da equipe, em ambiente adequado, conforme o caso. Não se faz em casa."},
   {"k":"Os trajetos","sc":["Os furos dos pinos","cicatrizam com o tempo."],"e":None,
    "sub":"Curativo simples, do jeito que a equipe orientar, até fechar.",
    "vo":"Os trajetos dos pinos cicatrizam nas semanas seguintes, com curativo simples, do jeito que a equipe orientar."},
   {"k":"O osso","sc":["Carga e atividade","voltam aos poucos."],"e":"aos poucos",
    "sub":"O osso novo segue ganhando resistência por meses; a fisioterapia continua.",
    "vo":"E o osso novo, ainda mais frágil, ganha resistência por meses. Carga volta aos poucos; a fisioterapia continua."},
   {"k":"Passa adiante","sc":["Envia para quem","está contando os dias."],"e":None,"cta":True,
    "sub":"Salva para o dia da retirada.",
    "vo":"Envia para quem está contando os dias."},
  ],
  "caption":_cap("O dia de tirar o fixador externo: a retirada é um procedimento feito pela equipe, em ambiente adequado e conforme o caso. Depois, os trajetos dos pinos cicatrizam ao longo das semanas seguintes, com curativo simples, do jeito que a equipe orientar. E o osso novo, ainda mais frágil que o osso maduro, segue ganhando resistência por meses: carga e atividade voltam aos poucos, e a fisioterapia continua.")},

 # ───────────── ep408 · BRAÇO B · kit de casa ─────────────
 {"id":"fx_kit_casa","ep":408,"serie":SERIE,"temporada":"fixador","motif_family":"bone",
  "scenes":[
   {"k":"Fixador por dentro","sc":["O que ter em casa","para cuidar do fixador?"],"e":None,
    "sub":"O kit que facilita a rotina — montado com a equipe.",
    "vo":"O que ter em casa para cuidar do fixador? Um kit simples, montado com a equipe."},
   {"k":"Curativo","sc":["O material que","a equipe indicou."],"e":None,
    "sub":"Gaze, solução e o resto da lista dela — e nada além disso.",
    "vo":"Curativo: gaze, solução e o que estiver na lista da equipe. Pomada por conta própria fica fora."},
   {"k":"Conforto","sc":["Capa para o aparelho,","apoio para a perna."],"e":None,
    "sub":"Roupa larga com abertura lateral e um travesseiro firme resolvem muito.",
    "vo":"Conforto: capa para o aparelho, travesseiro firme para a perna, roupa larga com abertura lateral."},
   {"k":"Organização","sc":["Contato da equipe","e o calendário à vista."],"e":None,
    "sub":"Ajustes, curativos e consultas anotados onde toda a casa veja.",
    "vo":"Organização: contato da equipe anotado, e o calendário de ajustes e consultas onde toda a casa veja."},
   {"k":"Passa adiante","sc":["Envia para quem","vai receber o aparelho."],"e":None,"cta":True,
    "sub":"Salva antes de montar o kit.",
    "vo":"Envia para quem vai receber o fixador."},
  ],
  "caption":_cap("O que ter em casa para cuidar do fixador externo? Um kit simples, montado com a orientação da equipe: para o curativo, gaze, solução e o que mais estiver na lista dela (pomada e produto por conta própria ficam fora); para o conforto, uma capa de tecido para o aparelho, um travesseiro firme para apoiar a perna e roupa larga com abertura lateral; para a organização, o contato da equipe anotado e o calendário de ajustes, curativos e consultas onde toda a casa veja.")},
]

# Variação anti-templatização: layout balanceado no lote + paleta por id (padrão dos lotes anteriores).
for _e, _lay in zip(FIXADOR, _gl.layout_para_sequencia([e["id"] for e in FIXADOR])):
    _e.setdefault("layout", _lay)
    _e.setdefault("palette", _gl.palette_para(_e["id"]))
