# -*- coding: utf-8 -*-
"""Regra de QUAL reel sai em cada dia — fonte ÚNICA, usada pelo publish.py (que publica) e pelo
publish_agenda.py (que projeta o PROGRAMACAO.md). Antes eram duas cópias, e a da agenda lia a cota
do ambiente LOCAL enquanto o publish lia a variável do repositório: bastava mudar a variável para
a página mentir (auditoria 19/10/2026). Não importa nada pesado nem exige secret.

Cotas por formato, por semana (segunda 00:00 a domingo 23:59, BRT). Mudar uma cota = editar o
padrão aqui e commitar (a página e o robô mudam juntos). As variáveis de ambiente só existem para
os testes; o publish.yml NÃO as define.
  * lâmina (item sem `formato`, texto antigo lido em voz alta) — Rafael, 18/10/2026: "desacelerar
    as lâminas" -> no máximo 1 por semana.
  * conversa ("Se o seu ___ pudesse responder") — Rafael, 19/10/2026: "é legal, mas tem que ser mais
    espaçada [...] deixar essa série de responder vez ou outra somente, pq é um modelo mais
    cansativo". A 1ª versão (1 por semana) punha conversa numa segunda e outra na segunda seguinte,
    e ele estranhou ("conversa fixador hoje e já conversa com pinos na segunda?") -> agora é
    INTERVALO: no mínimo DIAS_ENTRE_CONVERSAS_PADRAO dias desde a última conversa publicada.
  * como_funciona — sem cota: é o formato principal.

ALL-IN (Rafael, 24/10/2026), depois dos primeiros números: cf_alongamento alcançou 2.049 contas em
2,8 dias (16 envios) e cf_fratura_cola 1.333 em menos de 1 dia, contra mediana 32 das lâminas em 90
dias; a conversa cv_fixador ficou em 56. "a gente tem que dar all-in agora nesse novo modelo [...] a
gente vai colocar todas as postagens dentro de um modelo parecido". Por padrão a lâmina fica com
cota 0 (suspensa) e a conversa desligada (CONVERSAS_ATIVAS_PADRAO = False): só COMO FUNCIONA sai.
Nada é apagado da fila — religar é mudar um padrão aqui. Dia de reel sem COMO FUNCIONA = dia sem
reel: a produção tem de manter a fila cheia (~4 por semana).

ALL-IN EM TUDO (Rafael, 24/10/2026, minutos depois): "o all-in que eu quero dar não é só do Reels
[...] mas sim de todas as postagens, de todo o conteúdo que produz do Instagram [...] como se a gente
estivesse praticamente começando do zero agora, fazendo esse formato novo". Por padrão, os carrosséis
estáticos (posts.json) e as sequências de stories antigas (sequences.json) também ficam suspensos
(POSTS_ATIVOS_PADRAO / SEQUENCIAS_ATIVAS_PADRAO = False) até existir a versão no formato novo.
Mesma lógica: nada é apagado; religar é mudar o padrão.

FORMATOS NOVOS (Rafael, 24-26/10/2026): 4 formatos novos de VÍDEO nas vagas do antigo carrossel (ter/qui/sáb
15h), revezando, intercalados com o COMO FUNCIONA (seg/qua/sex/dom): "colocar eles, os quatro formatos [...] um
cada dia [...] intercalar um formato novo com como funciona, e aí depois a gente vai ter uma resposta se algum
desses formatos foram melhor". Viu os 4 pilotos e disse "conferido, segue". Vira esta regra (DIA -> GRUPO):
  * seg/qua/sex/dom (DIAS_COMO_FUNCIONA): COMO FUNCIONA (e lâmina/conversa, se religadas, com as cotas acima).
    Formato novo NUNCA sai nesses dias.
  * ter/qui/sáb (DIAS_FORMATOS_NOVOS), a partir de INICIO_FORMATOS_NOVOS (03/11/2026): um dos FORMATOS_NOVOS,
    em RODÍZIO — sai o formato publicado há MAIS tempo (nunca publicado = primeiro; empate = ordem da fila, pela
    posição do 1º pendente de cada formato) e, dentro do formato, o 1º da fila. Formato sem peça pronta sai do
    rodízio até ganhar peça. Antes do início, ter/qui/sáb ficam sem reel.
  * Vaga sem peça pronta = dia sem reel (o publish avisa; não é falha). 1 reel por dia continua (last_reel_date).
A medição do teste entre formatos lê o `formato` gravado no registro de cada reel publicado (publish.log).
"""
import datetime as dt
import os

BRT = dt.timezone(dt.timedelta(hours=-3))
# Formatos novos de vídeo (Rafael, 24-26/10/2026) — o `formato` do item da fila E do episódio. A ordem aqui não
# decide nada (o rodízio decide pela última publicação e pela fila); só fixa os nomes válidos.
FORMATOS_NOVOS = ("qual_dos_dois", "mito_na_prova", "camera_lenta", "chama_o_var")
NOMES_FORMATOS = {"como_funciona": "COMO FUNCIONA", "conversa": "CONVERSA", "lamina": "LÂMINA",
                  "qual_dos_dois": "QUAL DOS DOIS?", "mito_na_prova": "MITO NA PROVA",
                  "camera_lenta": "CÂMERA LENTA", "chama_o_var": "CHAMA O VAR"}
DIAS_COMO_FUNCIONA = frozenset({0, 2, 4, 6})       # seg/qua/sex/dom
DIAS_FORMATOS_NOVOS = frozenset({1, 3, 5})        # ter/qui/sáb — as vagas do carrossel antigo (crons das 15h)
INICIO_FORMATOS_NOVOS = dt.date(2026, 10, 27)      # 1ª terça dos formatos novos (era 03/11; Rafael, 27/10: "eu não queria
                                                   # diminuir o volume [...] a gente adianta as publicações"); antes, sem reel
GRUPO_COMO_FUNCIONA = "como_funciona"
GRUPO_NOVOS = "formatos_novos"
LAMINAS_POR_SEMANA_PADRAO = 0            # 24/10: all-in COMO FUNCIONA (era 1 por semana desde 18/10)
DIAS_ENTRE_CONVERSAS_PADRAO = 10          # Rafael, 19/10: "pode deixar a cada 10 dias" (vale se religar)
CONVERSAS_ATIVAS_PADRAO = False           # 24/10: all-in COMO FUNCIONA — conversa suspensa
POSTS_ATIVOS_PADRAO = False               # 24/10: carrossel estático antigo suspenso (all-in em tudo)
SEQUENCIAS_ATIVAS_PADRAO = False          # 24/10: sequência de stories antiga suspensa (all-in em tudo)
STORIES_NOVOS_ATIVOS_PADRAO = True        # 24/10: story da geração nova (só sai APROVADO, ver checar_stories.py)
# Rafael, 24/10: "não colocar coisas que foram postadas muito recentemente sobrepondo [...] usar temas
# mais anteriores nas próximas postagens, para não ficar repetitivo demais". Peça derivada (story,
# carrossel da geração nova) não sai se o MESMO TEMA apareceu ou vai aparecer em menos de N dias em
# qualquer superfície; entre as liberadas, sai a do tema mais antigo (temas_conteudo.py).
DIAS_ENTRE_MESMO_TEMA_PADRAO = 7    # era 14 (24/10); 27/10: com 14 os stories quase não saíam e o Rafael pediu volume
_SEM_COTA = ("off", "nao", "não", "no", "false", "sem", "-1")


def _cota(var, padrao, valor=None):
    """-1 = sem cota; 0 = suspenso; N = até N por semana. Valor ilegível -> padrão com aviso
    (antes, 'off' derrubava o publish INTEIRO no import, posts e stories junto)."""
    v = os.environ.get(var) if valor is None else valor
    if v is None or str(v).strip() == "":
        return padrao
    v = str(v).strip().lower()
    if v in _SEM_COTA:
        return -1
    try:
        return int(v)
    except ValueError:
        print(f"::warning::{var}={v!r} ilegível — usando o padrão {padrao}", flush=True)
        return padrao


def cota_laminas(valor=None):
    return _cota("LAMINAS_POR_SEMANA", LAMINAS_POR_SEMANA_PADRAO, valor)


def dias_entre_conversas(valor=None):
    """Intervalo mínimo (dias) entre duas conversas publicadas; -1/'off' = sem intervalo."""
    return _cota("DIAS_ENTRE_CONVERSAS", DIAS_ENTRE_CONVERSAS_PADRAO, valor)


def dias_entre_mesmo_tema(valor=None):
    """Distância mínima (dias) entre duas aparições do mesmo tema; -1/'off' = sem distância."""
    return _cota("DIAS_ENTRE_MESMO_TEMA", DIAS_ENTRE_MESMO_TEMA_PADRAO, valor)


def _chave(var, padrao, valor=None):
    v = os.environ.get(var) if valor is None else valor
    if v is None or str(v).strip() == "":
        return padrao
    return str(v).strip().lower() in ("on", "1", "true", "sim", "yes")


def conversas_ativas(valor=None):
    """A série CONVERSA está ligada? Padrão False desde 24/10 (all-in COMO FUNCIONA)."""
    return _chave("CONVERSAS_ATIVAS", CONVERSAS_ATIVAS_PADRAO, valor)


def posts_ativos(valor=None):
    """Os carrosséis do posts.json saem? Padrão False desde 24/10 (all-in em todo o conteúdo)."""
    return _chave("POSTS_ATIVOS", POSTS_ATIVOS_PADRAO, valor)


def stories_novos_ativos(valor=None):
    """Os stories da geração nova (stories_cf.json) saem? Padrão True: o portão só deixa sair story
    aprovado pelo Rafael, com o reel de origem no ar há 2+ dias."""
    return _chave("STORIES_NOVOS_ATIVOS", STORIES_NOVOS_ATIVOS_PADRAO, valor)


def sequencias_ativas(valor=None):
    """As sequências de stories do sequences.json saem? Padrão False desde 24/10 (all-in em tudo)."""
    return _chave("SEQUENCIAS_ATIVAS", SEQUENCIAS_ATIVAS_PADRAO, valor)


def ultima_publicacao(state, reels, fmt_alvo):
    """Data BRT do último reel publicado do formato `fmt_alvo` (None se nunca saiu)."""
    fmt = {r["id"]: formato(r) for r in reels}
    ult = None
    for e in state.get("published", []):
        if e.get("kind") != "reel" or not e.get("at"):
            continue
        if (e.get("formato") or fmt.get(e["id"], "lamina")) != fmt_alvo:
            continue
        try:
            d = dt.datetime.fromisoformat(e["at"]).astimezone(BRT).date()
        except ValueError:
            continue
        ult = d if ult is None or d > ult else ult
    return ult


def formato(item):
    return (item.get("formato") or "lamina").strip().lower()


def publicados_na_semana(state, reels, agora_brt, fmt_alvo):
    """Quantos reels do formato `fmt_alvo` já saíram nesta semana (segunda 00:00 BRT até agora).
    Usa o `formato` gravado no registro do publish; registro antigo (sem o campo) cai no
    reels.json — peça retirada da fila depois de publicada não muda mais de formato."""
    fmt = {r["id"]: formato(r) for r in reels}
    ini = (agora_brt - dt.timedelta(days=agora_brt.weekday())).date()
    n = 0
    for e in state.get("published", []):
        if e.get("kind") != "reel" or not e.get("at"):
            continue
        try:
            quando = dt.datetime.fromisoformat(e["at"]).astimezone(BRT).date()
        except ValueError:
            continue
        f = e.get("formato") or fmt.get(e["id"], "lamina")
        if quando >= ini and f == fmt_alvo:
            n += 1
    return n


def laminas_na_semana(state, reels, agora_brt):
    return publicados_na_semana(state, reels, agora_brt, "lamina")


def _data(dia):
    return dia.date() if isinstance(dia, dt.datetime) else dia


def grupo_do_dia(dia, inicio_novos=None):
    """Que reel o dia comporta: GRUPO_COMO_FUNCIONA (seg/qua/sex/dom), GRUPO_NOVOS (ter/qui/sáb a partir de
    INICIO_FORMATOS_NOVOS) ou None (ter/qui/sáb antes do início: sem reel). `dia` = date ou datetime BRT."""
    d = _data(dia)
    inicio = INICIO_FORMATOS_NOVOS if inicio_novos is None else inicio_novos
    if d.weekday() in DIAS_COMO_FUNCIONA:
        return GRUPO_COMO_FUNCIONA
    if d.weekday() in DIAS_FORMATOS_NOVOS and d >= inicio:
        return GRUPO_NOVOS
    return None


def grupo_do_formato(fmt):
    """O grupo de dias em que um formato pode sair: GRUPO_NOVOS (os 4 formatos novos, ter/qui/sáb) ou
    GRUPO_COMO_FUNCIONA (COMO FUNCIONA, lâmina, conversa: seg/qua/sex/dom). Formato desconhecido cai em
    GRUPO_COMO_FUNCIONA (onde o proximo_reel também não o solta)."""
    return GRUPO_NOVOS if (fmt or "lamina").strip().lower() in FORMATOS_NOVOS else GRUPO_COMO_FUNCIONA


def ultimas_por_formato(state, reels):
    """{formato: data BRT do último reel dele no registro}. O `formato` gravado pelo publish manda; registro antigo
    (sem o campo) cai no reels.json. Conta também o `reel_incerto` (pode estar no ar: o rodízio não repete o
    formato por causa de uma dúvida que a conferência humana ainda vai resolver)."""
    fmt = {r["id"]: formato(r) for r in reels}
    out = {}
    for e in state.get("published", []):
        if e.get("kind") not in ("reel", "reel_incerto") or not e.get("at"):
            continue
        try:
            d = dt.datetime.fromisoformat(e["at"]).astimezone(BRT).date()
        except (TypeError, ValueError):
            continue
        f = (e.get("formato") or fmt.get(e.get("id"), "lamina")).strip().lower()
        if out.get(f) is None or d > out[f]:
            out[f] = d
    return out


# RODÍZIO COM PESO (Rafael, 31/10/2026, vendo os números: câmera lenta 25.612 de alcance em 1,8 dia, 27 envios e
# 22% de pulo nos 3 s; Chama o VAR 3.461 e 22,8 s assistidos — o melhor tempo — contra 1.076 a 2.650 dos COMO
# FUNCIONA; "a gente vai investir nesses formatos novos"; "pode implementar"). Nas vagas de ter/qui/sáb: câmera
# lenta em 2 de cada 3, Chama o VAR na outra; Qual dos dois e Mito na prova viram RESERVA (peso 0): saem só quando
# os de peso > 0 estão sem peça pronta — vaga nunca fica vazia por causa do peso (Rafael, 27/10: volume). Todo
# formato faz a ESTREIA antes de valer o peso (o Mito estreia em 03/11 e mostra os números dele). A contagem do
# peso começa em INICIO_PESOS. Mudar o peso = mudar aqui (fonte única: o PROGRAMACAO.md projeta com a mesma regra).
PESOS_FORMATOS_NOVOS_PADRAO = {"camera_lenta": 2, "chama_o_var": 1, "qual_dos_dois": 0, "mito_na_prova": 0}
INICIO_PESOS = dt.date(2026, 11, 1)


def pesos_formatos_novos(valor=None):
    """{formato: peso}. Variável PESOS_FORMATOS_NOVOS só para os testes ('iguais' = rodízio simples de antes, ou
    'camera_lenta:2,chama_o_var:1,...'); a produção não a define (publish_agenda confere o publish.yml)."""
    v = os.environ.get("PESOS_FORMATOS_NOVOS") if valor is None else valor
    if v is None or str(v).strip() == "":
        return dict(PESOS_FORMATOS_NOVOS_PADRAO)
    v = str(v).strip().lower()
    if v in ("iguais", "off", "-1"):
        return {f: 1 for f in FORMATOS_NOVOS}
    out = {f: 0 for f in FORMATOS_NOVOS}
    try:
        for par in v.split(","):
            f, w = par.split(":")
            if f.strip() in out:
                out[f.strip()] = max(0, int(w))
        return out
    except ValueError:
        print(f"::warning::PESOS_FORMATOS_NOVOS ilegível ({v!r}) — usando o padrão de regra_reels.py.")
        return dict(PESOS_FORMATOS_NOVOS_PADRAO)


def publicados_por_formato_desde(state, reels, desde):
    """{formato: quantos reels dele saíram de `desde` em diante} (mesma leitura de ultimas_por_formato)."""
    fmt = {r["id"]: formato(r) for r in reels}
    out = {}
    for e in state.get("published", []):
        if e.get("kind") not in ("reel", "reel_incerto") or not e.get("at"):
            continue
        try:
            d = dt.datetime.fromisoformat(e["at"]).astimezone(BRT).date()
        except (TypeError, ValueError):
            continue
        if d < desde:
            continue
        f = (e.get("formato") or fmt.get(e.get("id"), "lamina")).strip().lower()
        out[f] = out.get(f, 0) + 1
    return out


def rodizio(reels, done, state, pesos=None):
    """O RODÍZIO dos formatos novos, na ordem em que saem: [(formato, última publicação | None, posição do 1º
    pendente na fila)], só dos formatos com peça pronta. O 1º da lista é o da próxima vaga:
      1. formato NUNCA publicado (estreia), na ordem da fila;
      2. formatos com peso > 0, pela menor razão publicados-desde-INICIO_PESOS / peso (2:1 = câmera lenta duas
         vezes para cada VAR); empate = o publicado há MAIS tempo, depois a fila;
      3. RESERVA (peso 0), o publicado há mais tempo — só quando nenhum de peso > 0 tem peça pronta."""
    pesos = pesos_formatos_novos() if pesos is None else pesos
    ult = ultimas_por_formato(state, reels)
    cont = publicados_por_formato_desde(state, reels, INICIO_PESOS)
    primeiro = {}
    for k, x in enumerate(reels):
        f = formato(x)
        if f in FORMATOS_NOVOS and x["id"] not in done and f not in primeiro:
            primeiro[f] = k

    def chave(f):
        if ult.get(f) is None:
            return (0, 0.0, dt.date.min, primeiro[f])
        w = pesos.get(f, 0)
        if w > 0:
            return (1, cont.get(f, 0) / w, ult[f], primeiro[f])
        return (2, 0.0, ult[f], primeiro[f])
    ordem = sorted(primeiro, key=chave)
    return [(f, ult.get(f), primeiro[f]) for f in ordem]


def proximo_reel(reels, done, state, agora_brt, cota=None, dias_conversa=None, conversa_ativa=None,
                 inicio_novos=None):
    """O reel que sai hoje (ou None = dia sem reel). O DIA decide o grupo (grupo_do_dia):
      * seg/qua/sex/dom: o 1º da fila entre COMO FUNCIONA (sempre), lâmina (só dentro da cota semanal) e conversa
        (só se a série estiver ligada E a última saiu há pelo menos `dias_conversa` dias). Formato novo nunca;
        formato desconhecido também não (o portão checar_entretenimento já o recusa na fila).
      * ter/qui/sáb a partir de INICIO_FORMATOS_NOVOS: o 1º da fila do formato novo da vez no rodízio().
      * ter/qui/sáb antes do início: None.
    `cota` = cota de lâminas (nome histórico)."""
    grupo = grupo_do_dia(agora_brt, inicio_novos)
    if grupo is None:
        return None
    if grupo == GRUPO_NOVOS:
        r = rodizio(reels, done, state)
        if not r:
            return None
        return next(x for x in reels if x["id"] not in done and formato(x) == r[0][0])
    cota = cota_laminas() if cota is None else cota
    dias = dias_entre_conversas() if dias_conversa is None else dias_conversa
    ativa = conversas_ativas() if conversa_ativa is None else conversa_ativa
    ult = ultima_publicacao(state, reels, "conversa")
    livre = {"como_funciona": True,
             "lamina": cota < 0 or publicados_na_semana(state, reels, agora_brt, "lamina") < cota,
             "conversa": ativa and (dias < 0 or ult is None or (_data(agora_brt) - ult).days >= dias)}
    for x in reels:
        if x["id"] in done:
            continue
        if not livre.get(formato(x), False):
            continue
        return x
    return None
