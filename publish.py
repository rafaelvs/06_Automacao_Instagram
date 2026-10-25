#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Publicador automatico para Instagram (API oficial da Meta / Instagram Login).

Modelo BIBLIOTECA CURADA, sem repetir:
- posts.json e reels.json sao listas (bibliotecas) — 1 item por janela.
- sequences.json e a nova STORY SERIALIZADA: cada item e 1 DIA = sequencia de 5 frames,
  publicados EM BLOCO (um story atras do outro) na janela diaria.
- Nada se repete. Quando a biblioteca acaba, o robo nao publica (hora de reabastecer).

Agenda (horario de Brasilia, BRT = UTC-3):
- POSTS (feed):  Ter/Qui/Sab, a partir das 15:00.  (pico de audiencia 12h-15h; ver auditoria jun/2026)
- STORIES (seq): TODOS OS DIAS, a partir das 12:30  -> 1 sequencia (5 frames) por dia.
- REELS:         Seg/Qua/Sex/Dom, a partir das 15:00.  (pico de audiencia; antes era 19:00, na descida)

Env: IG_USER_ID, IG_ACCESS_TOKEN, GITHUB_REPOSITORY, GRAPH_VERSION (opc),
     FORCE_ID (opc: publica esse id imediatamente - post, story, reel ou sequencia).

NOTA — falha de AUTENTICACAO e' BARULHENTA (nao silenciosa):
    O token da Meta (renovado a cada ~60 dias) e' o ponto unico de falha do motor.
    Ate 07/2026 um `except Exception` engolia o erro, o main() retornava normal e o
    job do Actions terminava VERDE — a fila pararia sem ninguem perceber. Agora um
    erro de auth vira `AuthError`, o robo para de tentar (o token vale para todos os
    itens), grava o que ja' saiu e sai com exit != 0, deixando o job VERMELHO — que
    e' o que dispara a notificacao do GitHub.

    CUIDADO ao mexer aqui: a Meta devolve HTTP **400** (nao 401) com
    type=OAuthException / code=190 quando o token expira, entao NAO da' para decidir
    so' pelo status HTTP. E os codigos de rate limit (4, 17, 32...) tambem vem como
    OAuthException — esses sao transitorios e NAO podem derrubar o job.

NOTA — por que NAO existe um limite de itens por execucao aqui:
    O robo do LinkedIn tem LINKEDIN_MAX_PER_RUN porque la' os posts tem horario
    marcado e se acumulam como "vencidos" enquanto a publicacao esta travada. Aqui a
    fila e' uma BIBLIOTECA e cada bloco publica no maximo 1 item por dia-calendario
    (guarda `last_*_date != today`). Se o token ficar morto 10 dias, a volta publica
    1 post, nao 10 — a recuperacao ja' e' gradual por construcao. Um limite global
    de 1/execucao seria ate' NOCIVO: no domingo saem legitimamente carrossel + reel.
"""
import os, re, sys, json, time, subprocess, datetime as dt
import requests

POST_WEEKDAYS  = {1, 3, 5}
POST_MIN       = 15*60                   # 15:00 BRT (pico de audiencia; era 19:00)
POST2_WEEKDAYS = {6}                     # 4o carrossel/sem (feed 8/sem) — dia-duplo c/ Reel no domingo
POST2_MIN      = 11*60                   # 11:00 BRT — escalonado p/ nao colidir com o Reel das 15h
# Saida da estagnacao (12/09/2026, plano §4 item 1): stories caem de ~35/semana para ~15/semana.
# Era sequencia DIARIA (5 frames x 7 dias); os sinais de ranking de Stories sao de relacionamento
# por espectador ("com que frequencia voce ve os stories desta conta") — cada seguidor que pula a
# sequencia diaria gera exatamente o sinal negativo. Mediana de mercado: 8,39 stories/semana. A
# sequencia continua um bloco de 5 frames (e' uma historia); o que muda e' a FREQUENCIA:
# 3 dias/semana = 15 frames/semana (~2,1/dia). Decisao do Rafael em 12/09 ("vamos fazer tudo");
# dias escolhidos em 13/09 pelos views/dia MEDIDOS (relatorio_stories.md): SAB 102,0 > SEG 100,7 >
# TER 91,3 ... QUI 69,0 (pior). Seg/ter/sab; a sequencia de ter antecipa o carrossel das 15h.
SEQ_WEEKDAYS   = {1, 3, 5}               # sequencia ter/qui/sab — dias do CARROSSEL (a de 12:30 antecipa
                                         # o post das 15h). Era DIARIA ate 12/09/2026.
# REVERTIDO em 19/09/2026 (auditoria v2, achado D3). Em 13/09 troquei para seg/ter/sab
# citando "SAB 102,0 · SEG 100,7 · TER 91,3 vs QUI 69,0 views/dia". Estava errado por dois
# motivos, os dois provados na v2:
#   1. EIXO DESLOCADO UM DIA. stories_pulse.py grava `dia = agora UTC` e stories.yml roda
#      `0 2 * * *` (23:00 BRT do dia anterior), entao a medicao do dia D e' da sequencia
#      publicada em D-1. relatorio_stories.md agregou por `dia` como se fosse o dia do tema.
#      Prova independente: dias SEM sequencia = 13, 16, 17, 18/09; dias com stories_ativos=0
#      = 14, 17, 18, 19/09 — exatamente +1. Reatribuindo pelo D-1 sobre os 32 dias limpos
#      disponiveis na decisao: DOM 102,2 · SEX 100,7 · SEG 96,3 · QUI 92,0 · SAB 90,5 ·
#      QUA 80,0 · TER 77,8. Os tres dias que escolhi eram o 3o, o 7o e o 5o.
#   2. "TER 91,3" nao se reproduz em janela nenhuma (93,0 ate 29/08; 96,3 ate 12/09) e a
#      serie diaria tem n=23 dias limpos (2 a 4 por dia da semana), nao os "83 dias" que
#      escrevi no PLANO_EXPERIMENTOS. Com esse n, a diferenca entre o melhor e o pior dia
#      cabe no ruido: NAO da' para escolher dia por este dado.
# Entao volta o criterio que nao dependia dessa medicao e que foi decidido em 12/09: casar a
# sequencia com o dia do carrossel. E7 (PLANO_EXPERIMENTOS) decide em 15/10, com amostra.
SEQ_MIN        = 12*60 + 30              # 12:30
REEL_WEEKDAYS  = {0, 2, 4, 6}
REEL_MIN       = 15*60                   # 15:00 BRT (pico de audiencia; era 19:00)
BRT = dt.timezone(dt.timedelta(hours=-3))

ROOT = os.path.dirname(os.path.abspath(__file__))
POSTS_FILE   = os.path.join(ROOT, "posts.json")
STORIES_FILE = os.path.join(ROOT, "stories.json")
SEQ_FILE     = os.path.join(ROOT, "sequences.json")
REELS_FILE   = os.path.join(ROOT, "reels.json")
DESTAQUES_FILE = os.path.join(ROOT, "destaques.json")
STATE_FILE   = os.path.join(ROOT, "state", "published.json")
TOKEN_STATE_FILE = os.path.join(ROOT, "state", "token_refresh.json")  # escrito por refresh_token.py
AVISO_EXPIRACAO_DIAS = 14   # a renovacao roda toda segunda: 14 dias = ~2 tentativas de folga

IG_USER_ID = os.environ.get("IG_USER_ID", "").strip()
TOKEN      = os.environ.get("IG_ACCESS_TOKEN", "").strip()
REPO       = os.environ.get("GITHUB_REPOSITORY", "").strip()

def _commit_do_checkout():
    """SHA do commit do checkout (git rev-parse HEAD), ou None fora de um clone deste repo.

    A raw URL das MIDIAS (story, reel, post) vai com este SHA, nao com o nome do branch (auditoria
    24/10/2026, publicacao#6 / render_ci#0): os portoes do publish.yml conferem os bytes DESTE checkout
    (sha256 do video da story contra o irmao, video do reel contra o aprovado). Com `main` na URL a Meta
    baixava o que estivesse no main na HORA DA BUSCA — um re-render empurrado entre o checkout e o
    POST /media saia sem ter passado por portao nenhum, e o cache de 5 min do raw.githubusercontent.com
    podia servir o render anterior. URL por commit e' imutavel. So' vale se o repo do git for ESTE
    diretorio (teste em pasta temporaria dentro de outro repo nao pode herdar um SHA alheio)."""
    try:
        top = subprocess.run(["git", "-C", ROOT, "rev-parse", "--show-toplevel"], capture_output=True, text=True, timeout=20)
        sha = subprocess.run(["git", "-C", ROOT, "rev-parse", "HEAD"], capture_output=True, text=True, timeout=20)
    except (OSError, subprocess.SubprocessError):
        return None
    if top.returncode != 0 or sha.returncode != 0:
        return None
    if os.path.normcase(os.path.realpath(top.stdout.strip())) != os.path.normcase(os.path.realpath(ROOT)):
        return None
    s_ = sha.stdout.strip()
    return s_ if re.fullmatch(r"[0-9a-f]{40}", s_) else None

COMMIT     = _commit_do_checkout()
# reserva: o nome do branch (sem git no ambiente). No Actions isso e' sinal de defeito: avisa ALTO.
REF        = COMMIT or (os.environ.get("GITHUB_REF_NAME", "main").strip() or "main")
# Só avisa quando ESTE diretório é um checkout (tem .git) e mesmo assim o git falhou. Os testes copiam o
# publish.py para uma pasta temporária sem .git, também dentro do Actions (GITHUB_ACTIONS=true herdado):
# ali o branch é a reserva certa, e o aviso quebrava o teste de "silêncio" do teste_publish_exit (CI 25/10).
if COMMIT is None and os.environ.get("GITHUB_ACTIONS", "").lower() == "true" and os.path.exists(os.path.join(ROOT, ".git")):
    print(f"::warning::git rev-parse HEAD falhou: a raw URL das midias vai pelo branch '{REF}' — a Meta pode "
          "baixar bytes diferentes dos que os portoes conferiram (checkout sem .git?).")
VER        = os.environ.get("GRAPH_VERSION", "v21.0").strip()
FORCE_ID   = os.environ.get("FORCE_ID", "").strip()
LOCATION_ID = os.environ.get("LOCATION_ID", "").strip()   # SEO local: place id (SP). Inerte se vazio.
# Trial Reels: publica o reel so' para NAO-seguidores (alcance de descoberta); graduacao
# SS_PERFORMANCE promove sozinho aos seguidores se performar (sem passo manual). Default OFF.
TRIAL_REELS = os.environ.get("TRIAL_REELS", "false").strip().lower() in ("1", "true", "yes", "sim")
TRIAL_GRADUATION = os.environ.get("TRIAL_GRADUATION", "").strip() or "SS_PERFORMANCE"  # vazio -> default; SS_PERFORMANCE | MANUAL
# Alarme fail-loud (plano de saida da estagnacao, B6-iii, 12/09/2026): se as N ultimas pecas do
# feed (reels + carrosseis, o que entra em /media) somam ZERO curtidas, o motor esta publicando
# no vazio e continuar so' treina o algoritmo no nao-engajamento. Nesse caso o run NAO publica,
# grava o alarme no state e sai VERMELHO. Desliga-se por variavel de repositorio
# ALARME_CURTIDAS=off (decisao humana declarada, nunca default). Falha de LEITURA da API nao
# bloqueia (fail-open com ::warning::) — medidor quebrado nao pode parar a fila.
ALARME_CURTIDAS = os.environ.get("ALARME_CURTIDAS", "on").strip().lower() not in ("off", "0", "false", "nao", "no")
ALARME_N_PECAS  = int(os.environ.get("ALARME_N_PECAS", "6") or 6)
# ROTULO DE IA (decisao do Rafael, 18/10/2026). A Central de Ajuda do Instagram exige rotulo em
# "um reel narrado com uma sobreposicao de voz realista gerada por IA" e avisa que pode haver
# penalidade sem ele. A API aceita `is_ai_generated` na criacao do conteiner desde 22/06/2026
# (changelog oficial, Instagram Login incluido). PROVADO antes de ligar: canario_rotulo_ia.py
# (run 39189956255) — `true` aceito e `banana` recusado com "Param is_ai_generated must be a
# boolean", ou seja, a API LE o campo (aceitar `true` sozinho nao provaria nada). Vale so' para
# REEL com voz sintetica: imagem e carrossel sao isentos pela propria Meta. Desliga-se por
# variavel de repositorio ROTULO_IA=off (decisao humana declarada, nunca default).
ROTULO_IA = os.environ.get("ROTULO_IA", "on").strip().lower() not in ("off", "0", "false", "nao", "no")
MARCAS_VOZ_IA = ("voz digital (ia)",)          # declaracao da legenda (CFM 2.454); o portao exige voz_ia explicito
# COTA DE LAMINAS (decisao do Rafael, 18/10/2026: "desacelerar as laminas antigas"). O reel em
# lamina de texto lida em voz alta virou "mural informativo": 36 pecas em 30 dias, ZERO envios.
# Os formatos novos (item["formato"] = "conversa" | "como_funciona") entram sem cota; lamina
# (item sem "formato") sai no maximo LAMINAS_POR_SEMANA vezes por semana (segunda a domingo,
# horario de Brasilia). Dia de reel sem peca permitida = sem reel nesse dia (o motor NAO para:
# regra de 27/09 — nunca desligar, sempre reativar). -1 = sem cota. A REGRA mora em regra_reels.py
# (fonte unica com a agenda do PROGRAMACAO.md — auditoria 19/10); aqui so' o nome de sempre.
import regra_reels
LAMINAS_POR_SEMANA = regra_reels.cota_laminas()
# Conversa ("Se o seu ___ pudesse responder") so' depois de N dias da ultima (Rafael, 19/10/2026:
# "tem que ser mais espacada [...] vez ou outra somente, pq e' um modelo mais cansativo"). Mesma regra unica.
DIAS_ENTRE_CONVERSAS = regra_reels.dias_entre_conversas()
# All-in COMO FUNCIONA (Rafael, 24/10/2026): conversa suspensa por padrao (regra_reels.py).
CONVERSAS_ATIVAS = regra_reels.conversas_ativas()
# All-in em TODO o conteudo (Rafael, 24/10/2026): carrossel estatico e sequencia de stories antigos
# suspensos por padrao ate existir a versao no formato novo (regra_reels.py). Religar = mudar o padrao.
POSTS_ATIVOS = regra_reels.posts_ativos()
SEQUENCIAS_ATIVAS = regra_reels.sequencias_ativas()
# STORIES DA GERAÇÃO NOVA (Rafael, 24/10/2026: "story com roteiro próprio"; formato "COMO FUNCIONA EM
# 3 TOQUES" escolhido pelo mesmo processo do reel). 3 vídeos curtos por story, ter/qui/sáb 12:30, só
# APROVADO e só com o reel de origem no ar há 2+ dias (checar_stories.py). Publicação em partes sem
# duplicar (publicar_stories.py: espera conjunta com prazo, estado gravado parte a parte, erro da
# Meta conferido pelo status do contêiner).
STORIES_NOVOS_ATIVOS = regra_reels.stories_novos_ativos()
STORY_NOVO_WEEKDAYS = {1, 3, 5}           # ter/qui/sab — dias SEM reel
STORY_NOVO_MIN = 12*60 + 30
STORIES_NOVOS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "stories_cf.json")
APROVACOES_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "aprovacoes.json")
HOST       = f"https://graph.instagram.com/{VER}"

if not IG_USER_ID or not TOKEN:
    print("ERRO: defina os secrets IG_USER_ID e IG_ACCESS_TOKEN."); sys.exit(1)

class AuthError(RuntimeError):
    """Token invalido/expirado ou permissao negada. Aborta o run e faz o job ficar
    VERMELHO, em vez de sair verde com a fila parada."""

# Quase TUDO na Meta chega com type=OAuthException — inclusive rate limit e erro de
# midia. Por isso a classificacao e' por CODIGO, nao pelo type.
# 1) Token/permissao: nao adianta tentar de novo, precisa de humano.
AUTH_CODES     = {10, 102, 190, 2500}
AUTH_SUBCODES  = {458, 459, 460, 463, 464, 467, 492}
# 2) Throttling: transitorio, o proximo disparo do cron resolve sozinho.
RATE_CODES     = {4, 17, 32, 341, 613}
# 3) Parametro/midia invalida: problema DAQUELE item, nao do token. O robo loga e
#    segue para os outros blocos (um reel corrompido nao pode travar a sequencia do dia).
CONTEUDO_CODES = {100, 352, 2207001, 2207003, 2207004, 2207005, 2207006, 2207020,
                  2207026, 2207027, 2207032, 2207052, 2207053}

def _e_falha_de_auth(status, payload):
    # corpo pode vir vazio/HTML/lista (erro de gateway): nunca confiar no formato
    err = payload.get("error") if isinstance(payload, dict) else None
    if not isinstance(err, dict): err = {}
    code = err.get("code"); sub = err.get("error_subcode")
    if sub in AUTH_SUBCODES: return True
    if code in AUTH_CODES: return True
    if isinstance(code, int) and 200 <= code <= 299: return True    # familia de permissao
    if code in RATE_CODES or code in CONTEUDO_CODES: return False
    if isinstance(code, int) and code >= 2207000: return False      # erros de container/midia
    # v1.6 (11/09/2026): a familia 2207xxx chega no error_subcode, com `code` GENERICO
    # (24 "Media Not Found", 9007 "media is not ready", 9004 "could not be fetched").
    # Lendo so' o `code`, os 3 casos caiam no catch-all de OAuthException abaixo e viravam
    # AuthError: 6 runs vermelhos na janela 16/08-08/09 abortaram a fila inteira e
    # imprimiram "renove o token" com token vivo. As duas linhas abaixo vem DEPOIS de
    # AUTH_CODES/AUTH_SUBCODES de proposito: token morto (190) com subcode de midia junto
    # continua sendo tratado como token morto.
    if sub in CONTEUDO_CODES: return False
    if isinstance(sub, int) and sub >= 2207000: return False        # idem, pelo subcode
    # 24/10/2026 (auditoria, publicacao#0): o HTTP 500 TRANSITORIO da Graph API chega como
    # {"type": "OAuthException", "code": 2, "is_transient": true, "message": "An unexpected error has
    # occurred. Please retry your request later."} (e o "unknown error" como code 1). Caia no catch-all
    # abaixo e virava AuthError: a story pulava a consulta ao conteiner, a parte que a Meta tinha posto
    # no ar ficava sem registro e o run seguinte a republicava ("AUTENTICACAO FALHOU" com o token vivo);
    # no reel, o mesmo republicava o reel. Vem DEPOIS de AUTH_CODES/AUTH_SUBCODES de proposito: 190 com
    # HTTP 500 (ou com is_transient) continua token morto.
    if (isinstance(status, int) and status >= 500) or str(err.get("is_transient", "")).lower() == "true" \
            or code in (1, 2):
        return False
    if str(err.get("type", "")) == "OAuthException": return True
    return status in (401, 403)

def _erro_api(r, onde):
    """Resposta >=400 vira excecao: AuthError se for token/permissao (aborta tudo),
    RuntimeError no resto (o robo tolera e tenta o proximo bloco)."""
    try: payload = r.json()
    except Exception: payload = {}
    detalhe = f"{onde} -> {r.status_code}: {r.text[:300]}"
    exc = AuthError(detalhe) if _e_falha_de_auth(r.status_code, payload) else RuntimeError(detalhe)
    exc.status, exc.payload = r.status_code, payload      # quem decide "saiu ou nao" le o codigo, nao o texto
    raise exc

class PublicacaoIncerta(RuntimeError):
    """media_publish respondeu erro e o conteiner nao diz nem 'saiu' (PUBLISHED) nem 'nao saiu' (FINISHED),
    ou a propria consulta falhou: a peca PODE estar no ar. O item e' registrado como `<kind>_incerto`
    (nao volta a fila sozinho: republicar seria duplicar) e todo run fica VERMELHO ate a conferencia
    humana (docs/02_RUNBOOK.md §12). `auth` = havia erro de token no caminho (o run para)."""
    def __init__(self, msg, container=None, auth=False):
        super().__init__(msg)
        self.container = container
        self.auth = auth

KINDS_INCERTOS = ("post_incerto", "reel_incerto", "seq_incerto", "story_incerto")

# WRITE-AHEAD de REEL e POST (auditoria de fechamento, 25/10/2026). So' a story tinha: o reel com HTTP 500 no
# media_publish, conteiner FINISHED na consulta logo depois e a Meta ENTREGANDO depois (licao da casa: 500 da Meta
# ENTREGA — e entrega tarde) ficava fora do estado; o run seguinte criava OUTRO conteiner e o reel saia 2x,
# permanente no feed. Agora o conteiner vai ao estado e ao disco ANTES do media_publish (state['reel_publicando'] /
# state['post_publicando']) e fica la' enquanto o conteiner disser FINISHED depois de erro (ou o job morrer dentro
# da chamada). O run seguinte pergunta a ESTE conteiner antes de qualquer decisao (_resolver_write_ahead_feed):
# PUBLISHED = saiu (registra); FINISHED = o bloco publica o MESMO conteiner (conteiner so' publica uma vez: a
# entrega tardia nunca duplica); EXPIRED/ERROR = nunca saiu (descarta; a peca segue na fila); outro status = INCERTO.
KINDS_WRITE_AHEAD = ("reel", "post")


def _chave_wa(kind):
    return f"{kind}_publicando"


def _wa(state, kind, item, entrada=None):
    """Contexto do write-ahead de uma peca: `entrada` = o write-ahead FINISHED de um run anterior (reaproveitar)."""
    return {"state": state, "kind": kind, "id": item["id"], "entrada": entrada}


def _wa_gravar(wa, cont, extras=None):
    reg = {"id": wa["id"], "container": cont, "at": dt.datetime.now(dt.timezone.utc).isoformat(), "commit": REF}
    reg.update({k: v for k, v in (extras or {}).items() if v is not None})
    wa["state"][_chave_wa(wa["kind"])] = reg
    save_state(wa["state"])                       # no disco ANTES do media_publish


def _wa_tirar(state, kind, item_id):
    ent = state.get(_chave_wa(kind))
    if isinstance(ent, dict) and ent.get("id") == item_id:
        state.pop(_chave_wa(kind), None)
        return True
    return False

def _avisar_token_parado(auth_error):
    """Mensagem unica de encerramento quando o token morre. Sai com exit 1 para o
    job ficar vermelho (o estado ja' foi gravado pelo chamador)."""
    print(f"::error::AUTENTICACAO FALHOU — token do Instagram invalido ou expirado. {auth_error}")
    print("::error::A fila esta PARADA: nada mais sera publicado ate' renovar. Gere um novo "
          "token e atualize o secret IG_ACCESS_TOKEN em rafaelvs/06_Automacao_Instagram.")
    sys.exit(1)

def _falhou(falhas, rotulo, erro):
    """Registra falha NAO-auth de um item, de forma BARULHENTA.

    Ate 07/2026 estas falhas saiam por `print` puro: o main() retornava normal e o job
    ficava VERDE. Como o item que falha NAO entra em `done` nem avanca `last_*_date`, o
    cron (*/30) repetia o MESMO item para sempre — inclusive o `RuntimeError` do
    guardrail CFM (`BLOQUEADO CFM`), que e' permanente por definicao e NUNCA se resolve
    sozinho. Resultado: fila parada em silencio, com o painel todo verde.

    Agora cada falha sai como `::error::` (anotacao visivel no Actions) e o main()
    devolve a lista para o processo sair com exit 1 — espelhando o caminho do AuthError.
    O passo "Salvar estado" do publish.yml tem `if: always()`, entao o que JA' foi ao ar
    continua sendo commitado normalmente: ficar vermelho nao faz republicar."""
    print(f"::error::FALHA {rotulo}: {erro}")
    falhas.append(f"{rotulo} ({type(erro).__name__})")

def _avisar_validade_do_token():
    """Aviso preventivo de expiracao DENTRO do motor.

    Ate 07/2026 o unico alarme de expiracao vivia fora do repo (uma tarefa agendada no
    PC do Rafael). Se o refresh-token.yml falha — como falhou desde sempre, por falta do
    secret GH_SECRETS_PAT — nada aqui dentro reclamava ate' o token simplesmente morrer.
    Isto le' o rastro deixado por refresh_token.py e avisa ANTES. Nunca bloqueia: e' so'
    um ::warning:: (o job segue verde), porque publicar ainda funciona ate' a expiracao."""
    # Leitura propria (nao load_json): um JSON corrompido aqui levantaria ValueError e
    # derrubaria a publicacao inteira por causa de um aviso COSMETICO. Fail-open sempre.
    try:
        with open(TOKEN_STATE_FILE, encoding="utf-8") as fh:
            estado = json.load(fh)
    except (OSError, ValueError):
        estado = None
    if not isinstance(estado, dict) or not estado.get("expira_em"):
        print("::warning::Sem registro de renovacao do token (state/token_refresh.json ausente). "
              "A renovacao automatica pode nunca ter rodado — confira o workflow refresh-token.yml.")
        return
    try:
        expira = dt.date.fromisoformat(estado["expira_em"])
    except (TypeError, ValueError):
        print("::warning::state/token_refresh.json tem 'expira_em' ilegivel — nao da' para conferir a validade.")
        return
    dias = (expira - dt.datetime.now(BRT).date()).days
    if dias <= AVISO_EXPIRACAO_DIAS:
        print(f"::warning::Token do Instagram expira em {dias} dia(s) ({expira:%d/%m/%Y}). "
              "Se o refresh-token.yml nao voltar a rodar verde, a fila para nessa data.")

def raw_url(path):
    if not REPO: raise RuntimeError("GITHUB_REPOSITORY nao definido (rode no GitHub Actions).")
    return f"https://raw.githubusercontent.com/{REPO}/{REF}/{path}"
def load_json(p, d):
    try:
        with open(p, encoding="utf-8") as f: return json.load(f)
    except FileNotFoundError: return d
def save_state(s):
    os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
    with open(STATE_FILE, "w", encoding="utf-8") as f: json.dump(s, f, ensure_ascii=False, indent=2)
def api_post(path, data):
    data = dict(data); data["access_token"] = TOKEN
    r = requests.post(f"{HOST}/{path}", data=data, timeout=120)
    if r.status_code >= 400: _erro_api(r, f"POST {path}")
    return r.json()
def api_get(path, params):
    params = dict(params); params["access_token"] = TOKEN
    r = requests.get(f"{HOST}/{path}", params=params, timeout=60)
    if r.status_code >= 400: _erro_api(r, f"GET {path}")
    return r.json()
_CONFIRMACAO = None   # publicacao confirmada pelo conteiner depois de erro (vai para o registro, ver log())

def _recusa_de_nao_pronto(e):
    """A Meta recusou o media_publish porque o conteiner ainda nao estava pronto (code 9007 / subcode 2207027,
    o caso real de 16/08-08/09): ela diz que NAO publicou — falha comum do item (o cron retenta), nunca incerto."""
    p = getattr(e, "payload", None)
    err = p.get("error") if isinstance(p, dict) else None
    return isinstance(err, dict) and (err.get("code") == 9007 or err.get("error_subcode") == 2207027)

def _publicar_conteiner(cont, wa=None, extras=None):
    """media_publish que NAO confunde resposta de erro com 'nao saiu' (licao da casa: HTTP 500 da Meta
    ENTREGA). Qualquer excecao — inclusive AuthError, que ja' foi classificacao errada de um 500
    transitorio — so' sobe depois de perguntar ao conteiner: PUBLISHED = saiu (devolve None: sem
    media_id, registro com `confirmado_por`); FINISHED = nao saiu AINDA (a excecao sobe, mas o write-ahead
    FICA: o proximo run pergunta de novo a este conteiner e publica o MESMO — a Meta entrega depois do 500);
    ERROR ou EXPIRED, ou a recusa 'conteiner nao pronto' (9007/2207027) = nao saiu (write-ahead descartado;
    o cron retenta com conteiner novo); qualquer outro status (IN_PROGRESS depois de 500...), ou a consulta
    falhando = PublicacaoIncerta. `wa` (reel/post): o conteiner vai ao estado e ao disco ANTES do
    media_publish (job morto DENTRO da chamada deixa o rastro); o log() / _registrar_incerto o tiram."""
    global _CONFIRMACAO
    _CONFIRMACAO = None
    if wa is not None:
        _wa_gravar(wa, cont, extras)
    try:
        mid = (api_post(f"{IG_USER_ID}/media_publish", {"creation_id": cont}) or {}).get("id")
        if mid:
            return mid
        erro = RuntimeError(f"media_publish do conteiner {cont} sem id na resposta")
    except Exception as e:                           # noqa: BLE001 — decide pelo conteiner
        erro = e
    try:
        st = (api_get(cont, {"fields": "status_code"}) or {}).get("status_code")
    except Exception as e2:                          # noqa: BLE001
        raise PublicacaoIncerta(f"media_publish falhou ({str(erro)[:200]}) e a consulta ao conteiner {cont} "
                                f"tambem ({str(e2)[:120]}) — pode ter ido ao ar", cont,
                                auth=isinstance(erro, AuthError) or isinstance(e2, AuthError)) from erro
    if st == "PUBLISHED":
        _CONFIRMACAO = {"container": cont, "confirmado_por": "status_code PUBLISHED depois de erro"}
        print(f"::warning::media_publish respondeu erro ({str(erro)[:200]}), mas o conteiner {cont} esta "
              "PUBLISHED: a peca SAIU (registrada sem media_id, nao sera republicada).", flush=True)
        return None
    if st == "FINISHED":
        # pronto e nao publicado NESTE INSTANTE — o que nao prova que nao saiu: a Meta entrega depois do 500. Com
        # write-ahead, ele fica: o proximo run pergunta de novo e, se ainda FINISHED, publica o MESMO conteiner.
        if wa is not None:
            print(f"::warning::media_publish do conteiner {cont} respondeu erro e ele esta FINISHED: isso NAO prova "
                  "que nao saiu (a Meta entrega depois do 500). Write-ahead mantido: o proximo run pergunta de novo a "
                  "ESTE conteiner e, se ainda FINISHED, publica o MESMO — nunca cria outro.", flush=True)
        raise erro
    if st in ("ERROR", "EXPIRED") or _recusa_de_nao_pronto(erro):
        # nao saiu: ERROR/EXPIRED = conteiner que nunca vira midia; 'nao pronto' = a Meta recusou dizendo por
        # que. Token morto segue AuthError; o resto e' falha do item.
        if wa is not None and _wa_tirar(wa["state"], wa["kind"], wa["id"]):
            save_state(wa["state"])
        raise erro
    raise PublicacaoIncerta(f"media_publish falhou ({str(erro)[:200]}) e o conteiner {cont} esta {st!r} — "
                            "pode ter ido ao ar", cont, auth=isinstance(erro, AuthError)) from erro

def _registrar_incerto(state, falhas, item_id, kind, erro, now):
    """Peca que PODE estar no ar: registro `<kind>_incerto` (o id entra em `done`: nao republica sozinho),
    estado salvo na hora e falha registrada. -> o erro, se havia token morto no caminho (para tudo)."""
    state["published"].append({"id": item_id, "kind": f"{kind}_incerto", "media_id": None, "at": now.isoformat(),
                               "container": getattr(erro, "container", None), "erro": str(erro)[:300]})
    _wa_tirar(state, kind, item_id)              # o registro incerto guarda o conteiner
    save_state(state)
    print(f"::error::{kind} {item_id}: publicacao INCERTA — {erro}. Registrado como '{kind}_incerto' (nao volta a "
          "fila sozinho). Confira no app e resolva no state/published.json (docs/02_RUNBOOK.md §12).")
    falhas.append(f"{kind} {item_id} (publicacao INCERTA)")
    return erro if getattr(erro, "auth", False) else None

def wait_finished(cid, tries=10, delay=6):
    for _ in range(tries):
        st = api_get(cid, {"fields": "status_code"}).get("status_code")
        if st == "FINISHED": return True
        if st in ("ERROR", "EXPIRED"): raise RuntimeError(f"Container {cid} status {st}")
        time.sleep(delay)
    return True
def _alt(item):
    """Alt-text (acessibilidade + SEO de imagem): usa item['alt'] ou a 1a linha da legenda
    (que e' keyword-forward). API suporta alt_text em imagens desde mar/2025."""
    a = (item.get("alt") or "").strip()
    if not a:
        a = (item.get("caption", "") or "").strip().split("\n", 1)[0].strip()
    return a[:100]

def _loc(d):
    """Adiciona location_id (SEO local) ao payload se LOCATION_ID estiver definido. No-op se vazio."""
    if LOCATION_ID:
        d = dict(d); d["location_id"] = LOCATION_ID
    return d

def _collab(d, item):
    """AUDIENCIA EMPRESTADA (plano de saida da estagnacao, B3, 12/09/2026): item["collaborators"]
    = lista de ate 3 usernames (sem @) vira o parametro `collaborators` do container — a doc da
    Graph API autoriza em imagem, carrossel e reel (NAO em story). Em 91 pecas publicadas ate
    11/09 o motor NUNCA enviou este parametro. O parceiro precisa ACEITAR o convite no app para
    a peca aparecer no perfil dele; ate la' ela sai normal no nosso. Username invalido faz a Meta
    recusar o container (erro de CONTEUDO, item falha ALTO e nao trava o token) — e' exatamente o
    que o canario `canario-collab.yml` prova antes de qualquer peca real levar o parametro."""
    cols = item.get("collaborators") or []
    if not isinstance(cols, list):
        raise RuntimeError(f"collaborators do item {item.get('id')} deve ser lista, veio {type(cols).__name__}")
    cols = [str(c).strip().lstrip("@") for c in cols if str(c).strip()]
    if not cols:
        return d
    if len(cols) > 3:
        raise RuntimeError(f"item {item.get('id')}: a API aceita no maximo 3 collaborators, vieram {len(cols)}")
    d = dict(d); d["collaborators"] = json.dumps(cols)
    print(f"  collaborators: {cols}", flush=True)
    return d

def _ultimas_pecas_sem_curtida():
    """Le as N ultimas pecas do feed em /media e devolve (soma_de_curtidas, ids) — ou None se a
    leitura falhar (fail-open: medidor quebrado nao para a fila). So' leitura, nunca publica."""
    try:
        r = api_get(f"{IG_USER_ID}/media", {"fields": "id,like_count,timestamp,media_product_type",
                                            "limit": ALARME_N_PECAS})
        pecas = [m for m in r.get("data", []) if m.get("media_product_type") != "STORY"][:ALARME_N_PECAS]
        if len(pecas) < ALARME_N_PECAS:
            return None
        return sum(int(m.get("like_count") or 0) for m in pecas), [m["id"] for m in pecas]
    except AuthError:
        raise
    except Exception as e:                       # leitura e' cosmetica para a publicacao: fail-open
        print(f"::warning::alarme de curtidas: leitura de /media falhou ({type(e).__name__}) — alarme nao avaliado neste run.")
        return None

def _texto_auditavel(item):
    """Junta TODA superficie de texto do item, nao so a legenda.

    A auditoria v1 mediu que o gate cobria ~13% do que e publicado: auditava apenas
    `item['caption']`, entao rotulo de sequencia, texto de cena de reel e slide de
    carrossel passavam batido. Varre tambem colecoes aninhadas para que qualquer campo
    de texto que venha a ser adicionado aos JSONs ja nasca coberto."""
    partes = []
    # "alt" entrou em 19/09 (achado D5 da v2): o alt text PUBLICO vai para a API em
    # item["alt"] (20 pecas, 1 ja' no ar) e o guard so' procurava "alt_text" — texto
    # publicado que nenhuma regua lia.
    for chave in ("caption", "label", "theme", "titulo", "title", "alt", "alt_text"):
        v = item.get(chave)
        if isinstance(v, str) and v.strip():
            partes.append(v)
    for colecao in ("scenes", "slides", "frames"):
        for el in (item.get(colecao) or []):
            if isinstance(el, dict):
                partes += [v for v in el.values() if isinstance(v, str) and v.strip()]
            elif isinstance(el, str) and el.strip():
                partes.append(el)
    return "\n".join(partes)


def _cfm_guard(item):
    """Backstop CFM antes de publicar. Se o MODULO estiver ausente: avisa ALTO e nao bloqueia
    (fail-open RUIDOSO — nao quebra o robo). Se o modulo existir mas tiver bug (SyntaxError/re.error):
    a excecao propaga -> o try/except do chamador trata como FALHA (fail-CLOSED: nao publica, nao marca
    done). Se houver VIOLACAO de CFM: loga marcador distinto 'BLOQUEADO CFM' e levanta RuntimeError
    (o chamador pula o item e NAO avanca, forcando revisao humana). Conteudo limpo passa direto."""
    try:
        from cfm_guardrails import auditar
    except (ImportError, ModuleNotFoundError):
        print("!!! ALERTA: cfm_guardrails ausente — guardrail CFM DESLIGADO neste run.", file=sys.stderr)
        return
    # Assinatura em texto so' e' exigivel onde a legenda e' o que o usuario le (post/reel
    # tem "caption"). Sequencia/story so' tem rotulo estrutural curto (theme/label) e a
    # identificacao CFM vive no RODAPE DO RENDER, nunca no JSON -- exigir texto ali travaria
    # a fila inteira (0 das 150 sequencias reais tem CRM em campo de texto).
    tem_legenda_visivel = bool(item.get("caption"))
    viol = [p for p in auditar(_texto_auditavel(item), "publico",
                               exigir_assinatura_texto=tem_legenda_visivel) if p[0] == "VIOLACAO"]
    if viol:
        msg = "BLOQUEADO CFM: " + "; ".join(f"{r}:{d}" for _, r, d in viol)
        print(f"!!! {msg} (item={item.get('id', '?')}) — NAO publicado, revisar.", file=sys.stderr)
        raise RuntimeError(msg)

def publish_post(item, wa=None):
    _cfm_guard(item)
    reuso = (wa or {}).get("entrada")
    if reuso:
        print(f"  reaproveitando o conteiner {reuso['container']} do write-ahead de {reuso.get('at')} (FINISHED: "
              "nao se cria outro)", flush=True)
        return _publicar_conteiner(reuso["container"], wa)
    imgs = item["images"]; cap = item.get("caption", ""); alt = _alt(item)
    if len(imgs) == 1:
        cont = api_post(f"{IG_USER_ID}/media", _collab(_loc({"image_url": raw_url(imgs[0]), "caption": cap, "alt_text": alt}), item))["id"]
    else:
        # alt_text por filho do carrossel (verificar no 1o publish real; se a API recusar, remover dos filhos).
        kids = [api_post(f"{IG_USER_ID}/media", {"image_url": raw_url(p), "is_carousel_item": "true", "alt_text": alt})["id"] for p in imgs]
        cont = api_post(f"{IG_USER_ID}/media", _collab(_loc({"media_type": "CAROUSEL", "children": ",".join(kids), "caption": cap}), item))["id"]
    wait_finished(cont)
    return _publicar_conteiner(cont, wa)
def publish_story_img(image_path):
    cont = api_post(f"{IG_USER_ID}/media", {"image_url": raw_url(image_path), "media_type": "STORIES"})["id"]
    wait_finished(cont)
    return _publicar_conteiner(cont)
def publish_story(item):
    _cfm_guard(item)
    return publish_story_img(item["image"])
def publish_sequence(seq):
    # publica os 5 frames em ordem, um atras do outro (story serializado)
    # Guard aqui tambem: sequencia e o MAIOR volume publicado (5 telas por peca) e ate
    # 02/08/2026 era a unica rota que subia sem nenhum backstop de CFM.
    _cfm_guard(seq)
    ids = []
    for i, img in enumerate(seq["images"], 1):
        mid = publish_story_img(img); ids.append(mid)
        print(f"  frame {i}/{len(seq['images'])} -> {mid}", flush=True)
        time.sleep(2)
    return ids
# Ramo que a ultima publicacao de reel tomou. Vai para o state (ver log()).
# Sem isto ninguem consegue provar POR DADO se um reel saiu em modo trial: o fallback
# abaixo e' silencioso e a Graph API nao expoe o status de trial na leitura da midia.
# Foi essa cegueira que deixou 19 reels publicados fora do grid de 22/06 a 24/07/2026
# sem que nenhuma auditoria conseguisse confirmar a causa. Ver docs/06_TRIAL_REELS.md.
_MODO_REEL = None   # "trial" | "fallback_normal" | "normal"


def _voz_ia(item):
    """Reel com voz sintetica? Basta UM sinal: `voz_ia` verdadeiro OU a declaracao na legenda.
    Antes um `voz_ia: false` explicito vencia a marca da legenda e o reel saia sem rotulo; o
    portao (checar_entretenimento) agora exige os dois coerentes em todo reel pendente."""
    cap = (item.get("caption") or "").lower()
    return bool(item.get("voz_ia")) or any(m in cap for m in MARCAS_VOZ_IA)

_ROTULO_REEL = None
def _rotulo_ia(d, item):
    global _ROTULO_REEL
    _ROTULO_REEL = bool(ROTULO_IA and _voz_ia(item))
    if _ROTULO_REEL:
        d["is_ai_generated"] = "true"
        print("  rotulo de IA: is_ai_generated=true (reel com voz sintetica)", flush=True)
    return d

_formato = regra_reels.formato


def _laminas_na_semana(state, reels, agora_brt):
    return regra_reels.laminas_na_semana(state, reels, agora_brt)


def proximo_reel(reels, done, state, agora_brt):
    return regra_reels.proximo_reel(reels, done, state, agora_brt, cota=LAMINAS_POR_SEMANA,
                                    dias_conversa=DIAS_ENTRE_CONVERSAS, conversa_ativa=CONVERSAS_ATIVAS)

def _erro_transitorio(e):
    """A Meta NAO respondeu sobre o pedido (HTTP 5xx, is_transient, code 1/2, throttling): nao e' recusa de parametro."""
    st, p = getattr(e, "status", None), getattr(e, "payload", None)
    err = p.get("error") if isinstance(p, dict) else None
    if not isinstance(err, dict):
        err = {}
    return (isinstance(st, int) and st >= 500) or str(err.get("is_transient", "")).lower() == "true" \
        or err.get("code") in (1, 2) or err.get("code") in RATE_CODES


_FORMATO_REEL = None
def publish_reel(item, wa=None):
    global _MODO_REEL, _FORMATO_REEL, _ROTULO_REEL
    _FORMATO_REEL = _formato(item)
    _cfm_guard(item)
    reuso = (wa or {}).get("entrada")
    if reuso:
        # write-ahead de um run anterior com o conteiner FINISHED: publica o MESMO (o ramo/rotulo vem do registro)
        _MODO_REEL = reuso.get("modo_reel") or "normal"
        _ROTULO_REEL = reuso.get("rotulo_ia")
        print(f"  reaproveitando o conteiner {reuso['container']} do write-ahead de {reuso.get('at')} (FINISHED: "
              "nao se cria outro)", flush=True)
        return _publicar_conteiner(reuso["container"], wa,
                                   {"modo_reel": _MODO_REEL, "rotulo_ia": _ROTULO_REEL, "formato": _FORMATO_REEL})
    # alt_text NAO e' suportado em reels (so imagens); location_id e collaborators sao suportados.
    base = _rotulo_ia(_collab(_loc({"media_type": "REELS", "video_url": raw_url(item["video"]),
                                    "caption": item.get("caption", "")}), item), item)
    cont = None
    _MODO_REEL = "normal"
    # Trial por PECA (plano B5, 12/09/2026): item["trial"] = true publica SO' esta peca em modo
    # trial (instrumento de diagnostico — 4 pecas, sorteio congelado em PLANO_EXPERIMENTOS.md),
    # sem religar o modo global (TRIAL_REELS segue false desde 25/07). Trial tira a peca do grid.
    if TRIAL_REELS or bool(item.get("trial")):
        # Trial Reel: so' para nao-seguidores; graduacao automatica (SS_PERFORMANCE) se performar.
        try:
            p = dict(base); p["trial_params"] = json.dumps({"graduation_strategy": TRIAL_GRADUATION})
            cont = api_post(f"{IG_USER_ID}/media", p)["id"]
            _MODO_REEL = "trial"
        except AuthError:
            # Token morto nao e' "trial_params recusado": propaga, senao este except
            # engoliria a falha de auth e o robo tentaria de novo a' toa.
            raise
        except RuntimeError as e:
            if _erro_transitorio(e):
                # 25/10/2026 (auditoria de fechamento): desde que o 500 transitorio deixou de ser AuthError, ele caia
                # aqui e virava 'trial_params recusado' — a peca do experimento (sorteio congelado) saia no GRID como
                # reel normal. 500/is_transient/throttling NAO e' recusa do parametro: falha do item, o cron tenta o
                # trial de novo.
                raise
            # Fallback robusto: se a API recusar trial_params, publica reel normal (nao trava o robo).
            print(f"  ! trial_params recusado ({e}); publicando como reel normal.", file=sys.stderr)
            cont = None
            _MODO_REEL = "fallback_normal"
    if cont is None:
        p = dict(base); p["share_to_feed"] = "true"
        cont = api_post(f"{IG_USER_ID}/media", p)["id"]
    wait_finished(cont, tries=30, delay=10)
    return _publicar_conteiner(cont, wa, {"modo_reel": _MODO_REEL, "rotulo_ia": _ROTULO_REEL, "formato": _FORMATO_REEL})
def log(state, item_id, kind, mid, now):
    reg = {"id": item_id, "kind": kind, "media_id": mid, "at": now.isoformat()}
    if mid is None and _CONFIRMACAO:
        reg.update(_CONFIRMACAO)            # saiu apesar do erro: o conteiner confirmou (sem media_id)
    if kind == "reel" and _MODO_REEL:
        # Prova por dado de qual ramo publicou (trial / fallback / normal). A auditoria v1
        # nao conseguiu confirmar isso em 18 reels de julho porque nada era gravado.
        reg["modo_reel"] = _MODO_REEL
        print(f"  modo do reel: {_MODO_REEL}", flush=True)
    if kind == "reel" and _ROTULO_REEL is not None:
        reg["rotulo_ia"] = _ROTULO_REEL
    if kind == "reel" and _FORMATO_REEL:
        # o formato vai no registro: a cota de laminas conta pelo que SAIU, nao pelo reels.json de
        # hoje (peca nova retirada da fila depois de publicada passava a contar como lamina)
        reg["formato"] = _FORMATO_REEL
    state["published"].append(reg)
    _wa_tirar(state, kind, item_id)          # a peca esta no registro: o write-ahead dela acabou
def next_item(items, done): return next((x for x in items if x["id"] not in done), None)


def _resolver_write_ahead_feed(state, falhas):
    """Write-ahead de reel/post que um run anterior deixou (erro no media_publish com o conteiner FINISHED, ou job
    morto DENTRO da chamada): pergunta a ESTE conteiner antes de qualquer decisao.
      PUBLISHED      -> a peca SAIU (entrega tardia ou job morto): registra sem media_id (`confirmado_por`) e marca o dia;
      FINISHED       -> nao saiu ainda: o bloco do tipo publica o MESMO conteiner, antes da fila (nunca cria outro);
      EXPIRED/ERROR  -> nunca saiu (a Meta so' expira conteiner NAO publicado): descarta, a peca segue na fila;
      outro status   -> `<kind>_incerto` (fora da fila, run vermelho ate a conferencia — RUNBOOK §12);
      consulta falha -> nada daquele tipo sai neste run (vermelho); o proximo pergunta de novo.
    -> ({kind: write-ahead FINISHED}, {kind: (id, motivo do bloqueio)})."""
    reuso, bloqueio = {}, {}
    for kind in KINDS_WRITE_AHEAD:
        ent = state.get(_chave_wa(kind))
        if not ent:
            continue
        if not isinstance(ent, dict) or not ent.get("id") or not ent.get("container"):
            bloqueio[kind] = (None, f"write-ahead de {kind} ilegivel ({str(ent)[:150]}): nada deste tipo sai ate a "
                                    "conferencia no app (docs/02_RUNBOOK.md §12)")
            continue
        iid, c = ent["id"], ent["container"]
        rot = f"{kind} {iid} (conteiner {c}, write-ahead de {ent.get('at')})"
        if any(e.get("id") == iid and e.get("kind") in (kind, f"{kind}_incerto") for e in state["published"]):
            print(f"{rot}: a peca ja esta no registro — write-ahead descartado.")
            state.pop(_chave_wa(kind), None); save_state(state)
            continue
        try:
            stc = (api_get(c, {"fields": "status_code"}) or {}).get("status_code")
        except AuthError:
            raise
        except Exception as e:                       # noqa: BLE001 — sem resposta nao se decide (nem se publica)
            bloqueio[kind] = (iid, f"{rot}: a consulta ao conteiner falhou ({str(e)[:200]}) — nada deste tipo sai "
                                   "neste run; o proximo pergunta de novo")
            continue
        if stc == "PUBLISHED":
            reg = {"id": iid, "kind": kind, "media_id": None, "at": ent.get("at"), "container": c,
                   "confirmado_por": "status_code PUBLISHED (write-ahead de run anterior)"}
            reg.update({k: ent[k] for k in ("modo_reel", "rotulo_ia", "formato") if ent.get(k) is not None})
            state["published"].append(reg)
            campo = "last_reel_date" if kind == "reel" else "last_post_date"
            d = _data_brt(ent.get("at"))
            if d is not None and (state.get(campo) or "") < d.isoformat():
                state[campo] = d.isoformat()
            state.pop(_chave_wa(kind), None); save_state(state)
            print(f"::warning::{rot}: o conteiner esta PUBLISHED — a peca SAIU (a Meta entregou depois do erro, ou o "
                  "job morreu no media_publish). Registrada sem media_id; NAO sera republicada.")
        elif stc == "FINISHED":
            reuso[kind] = ent
            print(f"{rot}: FINISHED — nao saiu ainda; este run publica o MESMO conteiner (nunca outro).")
        elif stc in ("EXPIRED", "ERROR"):
            state.pop(_chave_wa(kind), None); save_state(state)
            print(f"{rot}: conteiner {stc} — nunca saiu; write-ahead descartado (a peca segue na fila).")
        else:
            state["published"].append({"id": iid, "kind": f"{kind}_incerto", "media_id": None, "at": ent.get("at"),
                                       "container": c, "status": stc, "erro": f"write-ahead: conteiner {stc!r}"})
            state.pop(_chave_wa(kind), None); save_state(state)
            _falhou(falhas, f"{kind} {iid}", RuntimeError(
                f"publicacao INCERTA: o conteiner do write-ahead esta {stc!r} — pode ter ido ao ar. Registrado como "
                f"'{kind}_incerto' (nao volta a fila sozinho); confira no app (docs/02_RUNBOOK.md §12)"))
    return reuso, bloqueio


def _escolher_com_write_ahead(kind, biblioteca, reuso, bloqueio, falhas, escolher):
    """(item, write-ahead a reaproveitar). O conteiner FINISHED de um run anterior vem ANTES da fila: publicar
    outra peca deixaria aquele conteiner solto (a Meta ainda pode entrega-lo). Bloqueio = falha, nada sai."""
    if kind in bloqueio:
        _falhou(falhas, f"{kind} (write-ahead)", RuntimeError(bloqueio[kind][1]))
        return None, None
    ent = reuso.get(kind)
    if ent:
        it = next((x for x in biblioteca if x.get("id") == ent.get("id")), None)
        if it is None:
            _falhou(falhas, f"{kind} {ent.get('id')} (write-ahead)", RuntimeError(
                f"o conteiner {ent.get('container')} preparado para {ent.get('id')} esta FINISHED, mas a peca saiu da "
                "biblioteca: nada deste tipo sai ate o conteiner expirar (24 h) ou a conferencia (docs/02_RUNBOOK.md §12)"))
            return None, None
        return it, ent
    return escolher(), None


def _temas_agendados(reels, pub, brt):
    """{tema: [datas]} dos reels que a fila ainda vai publicar (mesma projeção do PROGRAMACAO.md)."""
    import publish_agenda, temas_conteudo
    out = {}
    hoje = brt.date()
    for d, i in publish_agenda.projeta_reels(reels, pub, hoje, any(
            e.get("kind") == "reel" and e.get("at", "")[:10] and
            dt.datetime.fromisoformat(e["at"]).astimezone(BRT).date() == hoje for e in pub), horizonte_dias=120):
        t = temas_conteudo.tema_de(i)
        if t:
            out.setdefault(t, []).append(d)
    return out


STATE_PUBLICANDO = "story_nova_publicando"   # write-ahead da parte em media_publish (publicar_stories.py)


def _data_brt(iso):
    try:
        return dt.datetime.fromisoformat(iso).astimezone(BRT).date()
    except (TypeError, ValueError):
        return None


def _resolver_write_ahead(state, hoje):
    """Write-ahead que um run anterior deixou (job morto DENTRO do media_publish, ou erro com o conteiner
    FINISHED): pergunta ao conteiner ANTES de qualquer decisao (publicar_stories.resolver_publicando).
    PUBLISHED = a parte saiu (registra); FINISHED do mesmo dia = reaproveita o MESMO conteiner; EXPIRED,
    ou FINISHED de outro dia = nunca saiu (descarta); o resto = parte INCERTA.
    -> ({story: {parte: conteiner}} para reaproveitar, story que esta conferencia completou ou None)."""
    import checar_stories as CS, publicar_stories as PS
    ent = state.get(STATE_PUBLICANDO)
    if not ent:
        return {}, None
    sid, i, c = ent.get("story"), ent.get("parte"), ent.get("container")
    rot = f"story {sid} parte {i + 1 if isinstance(i, int) else i} (conteiner {c}, write-ahead de {ent.get('at')})"
    try:
        decisao, st = PS.resolver_publicando(ent, api_get)
    except AuthError:
        raise
    except Exception as e:                       # noqa: BLE001 — sem resposta nao se decide (nem se publica)
        raise RuntimeError(f"{rot}: a consulta ao conteiner falhou ({e}) — nada publicado; o proximo run "
                           "pergunta de novo") from e
    if decisao == "reusar" and _data_brt(ent.get("at")) == hoje:
        print(f"{rot}: FINISHED — nao saiu; o MESMO conteiner sera reaproveitado (nao se cria outro).")
        return {sid: {i: c}}, None
    base = {"id": f"{sid}#{i}", "story": sid, "parte": i, "media_id": None, "at": ent.get("at"), "container": c,
            "temas": ent.get("temas") or [], "sha256": ent.get("sha256"), "commit": ent.get("commit")}
    state.pop(STATE_PUBLICANDO, None)
    if decisao == "publicada":
        state["published"].append(dict(base, kind="story_nova",
                                        confirmado_por="status_code PUBLISHED (write-ahead de run anterior)"))
        print(f"::warning::{rot}: o conteiner esta PUBLISHED — a parte SAIU (o run anterior morreu ou errou "
              "no media_publish). Registrada sem media_id; nao sera republicada.")
        completa = len(CS.partes_publicadas(state["published"]).get(sid, {})) == len(CS.PAPEIS)
        d = _data_brt(ent.get("at"))
        if completa and d is not None and (state.get("last_story_nova_date") or "") < d.isoformat():
            state["last_story_nova_date"] = d.isoformat()
        save_state(state)
        return {}, (sid if completa else None)
    if decisao in ("reusar", "descartar"):
        print(f"{rot}: conteiner {st} — nunca saiu; registro descartado.")
        save_state(state)
        return {}, None
    state["published"].append(dict(base, kind="story_nova_incerta", status=st, erro=f"write-ahead: conteiner {st!r}"))
    save_state(state)
    print(f"::error::{rot}: conteiner {st!r} — a parte pode ter ido ao ar. Registrada como INCERTA.")
    return {}, None


def _conferir_conta_antes_da_story(state, brt):
    """GET {IG_USER_ID}/stories ANTES de criar conteiner (auditoria 24/10, publicacao#1): story de HOJE, a
    partir das 12:30, que o estado nao conhece = outro run publicou com o estado velho (checkout de SHA
    antigo, push perdido) ou houve story postada a mao. Nada sai: falha ALTO. Leitura que falha tambem
    nao libera (guarda cega nao e' guarda). Parte registrada sem media_id (confirmada pelo conteiner)
    desconta uma story desconhecida."""
    import publicar_stories as PS
    desde = dt.datetime(brt.year, brt.month, brt.day, STORY_NOVO_MIN // 60, STORY_NOVO_MIN % 60, tzinfo=BRT)
    conhecidos, sem_id = set(), 0
    for e in state["published"]:
        if e.get("media_id"):
            conhecidos.add(e["media_id"])
        conhecidos.update(m for m in (e.get("media_ids") or []) if m)
        if e.get("kind") == "story_nova" and not e.get("media_id"):
            t = PS.instante(e.get("at"))
            if t is not None and t >= desde:
                sem_id += 1
    try:
        novas = PS.stories_desconhecidas(api_get, IG_USER_ID, conhecidos, desde)
    except AuthError:
        raise
    except Exception as e:                       # noqa: BLE001
        raise RuntimeError(f"nao deu para conferir a conta antes da story (GET {IG_USER_ID}/stories: {e}) — "
                           "nada publicado; o proximo run tenta de novo") from e
    if len(novas) > sem_id:
        ids = ", ".join(f"{x.get('id')} ({x.get('timestamp')})" for x in novas)
        raise RuntimeError(f"a conta tem {len(novas)} story(ies) de hoje depois das 12:30 que o estado NAO conhece "
                           f"[{ids}]" + (f" ({sem_id} parte(s) sem media_id descontada(s))" if sem_id else "") +
                           ": outro run publicou com o estado velho, ou houve story manual. NADA publicado — confira "
                           "no app e registre no state/published.json (docs/02_RUNBOOK.md §12).")


def publicar_story_nova(state, reels, brt, now, forcar=None, falhas=None):
    """Publica a story da geração nova do dia (ou a `forcar`). Devolve True se algo saiu (ou se a conferência
    do write-ahead completou a story de hoje). A MESMA régua da página (checar_stories, topo do módulo):
    write-ahead -> incertas -> retomada -> candidatas -> escolher -> veredito -> conta -> publicar.
      - pendente de aprovação: ::warning:: e FORA da escolha (nunca trava a aprovada);
      - pendente com formato/conteúdo quebrado: a escolhida sai e o job fica vermelho (`falhas`);
      - incompleta de outro dia, parte incerta, aprovada barrada pelo portão, conta com story de hoje que
        o estado não conhece: exceção (job vermelho, nada publicado);
      - FORCE (decisão humana): story não aprovada, já completa ou barrada = exceção;
      - last_story_nova_date só quando ESTE run completou a story."""
    import checar_stories as CS, publicar_stories as PS, temas_conteudo
    fila = load_json(STORIES_NOVOS_FILE, [])
    aprov = load_json(APROVACOES_FILE, {"lotes": []})
    reels_por_id = {r["id"]: r for r in reels}
    hoje = brt.date()
    erros_fila = []
    reuso, concluida = _resolver_write_ahead(state, hoje)
    pub = state["published"]
    inc = CS.incertas(pub)
    if inc:
        raise RuntimeError(f"story(ies) com parte INCERTA {inc}: pode estar no ar. Confira no app e resolva no "
                           "state/published.json antes de publicar outra (docs/02_RUNBOOK.md §12, story_nova_incerta).")
    if concluida and forcar in (None, concluida) and state.get("last_story_nova_date") == hoje.isoformat():
        print(f"Story {concluida} completada pela conferência do contêiner (write-ahead do run anterior).")
        return True
    st_ret, situ, det = CS.retomada(fila, pub, hoje)
    if forcar:
        st = next((x for x in fila if x.get("id") == forcar), None)
        if st is None:
            raise RuntimeError(f"story {forcar} não está em stories_cf.json")
        feitas = CS.partes_publicadas(pub).get(forcar, {})
        if len(feitas) >= len(CS.PAPEIS):
            quando = sorted({str(e.get("at", ""))[:10] for e in pub if e.get("story") == forcar and e.get("kind") == "story_nova"})
            raise RuntimeError(f"FORCE story:{forcar}: já publicada inteira ({', '.join(quando)}) — nada a publicar "
                               "(pedido humano que não publica não fica verde; o dia NÃO foi marcado)")
        if CS.data_do_reel(st.get("reel_ref"), pub) is None:
            raise RuntimeError(f"story {forcar}: o reel {st.get('reel_ref')} ainda não saiu no grid — a tela 3 diria "
                               "'Vídeo completo no perfil' sem o vídeo no perfil")
        if st_ret is not None and st_ret.get("id") != forcar:
            raise RuntimeError(f"FORCE story:{forcar}: a story {st_ret['id']} está incompleta ({det}) — resolva-a antes "
                               "de forçar outra")
        if situ == "incompleta_expirada":
            raise RuntimeError(det)
        outro = [x for x in reuso if x != forcar]
        if outro:
            raise RuntimeError(f"FORCE story:{forcar}: a story {outro[0]} tem contêiner preparado hoje (write-ahead) — "
                               "complete-a antes de forçar outra")
        motivo = "FORCE" + (" (as partes que faltam)" if feitas else "")
    else:
        if situ == "incompleta_expirada":
            raise RuntimeError(det)
        if situ == "retomada":
            st, motivo = st_ret, "retomada (as partes que faltam)"
            outro = [x for x in reuso if x != st.get("id")]
            if outro:
                raise RuntimeError(f"story {outro[0]} tem contêiner preparado (write-ahead) e {st.get('id')} está "
                                   "incompleta no mesmo dia — confira no app (docs/02_RUNBOOK.md §12)")
        elif reuso:
            sid_r = next(iter(reuso))
            st = next((x for x in fila if x.get("id") == sid_r), None)
            if st is None:
                raise RuntimeError(f"story {sid_r} tem contêiner preparado hoje (write-ahead), mas saiu do "
                                   "stories_cf.json — confira no app (docs/02_RUNBOOK.md §12)")
            motivo = "retomada (contêiner preparado pelo run anterior)"
        else:
            cands, fora = CS.candidatas(fila, pub, aprov, hoje, reels_por_id)
            for sid_f, nivel, msg in fora:
                if nivel == "aviso":
                    print(f"::warning::{msg}")
                else:
                    erros_fila.append(msg)
                    if falhas is not None:
                        _falhou(falhas, f"story {sid_f} (fila, portão)", RuntimeError(msg))
                    else:
                        print(f"::error::{msg}")
            st, motivo = CS.escolher(cands, pub, hoje, futuras=_temas_agendados(reels, pub, brt), fila=fila)
            if st is None:
                print(f"Stories novos: nenhuma story liberada hoje ({motivo}).")
                if erros_fila and falhas is None:
                    raise RuntimeError("stories da fila com erro de portão: " + "; ".join(erros_fila))
                return False
    sid = st["id"]
    v = CS.veredito(st, aprov, reels_por_id)
    k = len(CS.partes_publicadas(pub).get(sid, {}))
    if not v["pode_sair"]:
        if v["situacao"] != "aprovada":
            if k:
                raise RuntimeError(f"story {sid} com {k}/{len(CS.PAPEIS)} parte(s) no ar e SEM aprovação válida "
                                   f"({v['situacao']}: {v['detalhe']}): nada sai — decida (docs/02_RUNBOOK.md §12)")
            if forcar:
                raise RuntimeError(f"FORCE story:{sid}: aguardando aprovação do Rafael ({v['situacao']}: {v['detalhe']}) "
                                   "— story só sai APROVADA")
            raise RuntimeError(f"story {sid} não pode sair ({v['situacao']}: {v['detalhe']})")
        raise RuntimeError(f"story {sid} BLOQUEADA pelo portão: " + "; ".join(m for _, m in v["erros"]))
    meta = CS.carregar(CS.irmao_de(st), {})
    partes = [{"arquivo": p["arquivo"], "tipo": "video"} for p in meta["partes"]]
    shas = [p.get("sha256") for p in meta["partes"]]
    ja = CS.partes_publicadas(pub).get(sid, {})
    prev = {}
    ent = state.get(STATE_PUBLICANDO) or {}
    for i, c in (reuso.get(sid) or {}).items():
        if ent.get("sha256") and isinstance(i, int) and i < len(shas) and ent["sha256"] != shas[i]:
            # FINISHED = nunca saiu: largar o contêiner velho é seguro; publicá-lo seria sair o render antigo
            print(f"write-ahead da parte {i + 1}: o render mudou desde então — o contêiner velho NÃO é reaproveitado.")
            state.pop(STATE_PUBLICANDO, None)
            save_state(state)
        else:
            prev[i] = c
    _conferir_conta_antes_da_story(state, brt)
    temas = sorted(temas_conteudo.temas_do_item(st))
    print(f"Story {sid} (reel {st['reel_ref']}) [{motivo}] — publicando partes "
          f"{[i + 1 for i in range(len(partes)) if i not in ja]}...")

    def antes(i, c):
        # write-ahead: o contêiner vai ao estado e ao disco ANTES do media_publish (job morto no meio da
        # chamada deixa o rastro; o próximo run pergunta ao contêiner antes de criar outro)
        state[STATE_PUBLICANDO] = {"story": sid, "parte": i, "container": c, "at": now.isoformat(),
                                   "sha256": shas[i] if i < len(shas) else None, "commit": REF, "temas": temas}
        save_state(state)

    def registrar(i, mid, info):
        reg = {"id": f"{sid}#{i}", "kind": "story_nova_incerta" if info.get("incerto") else "story_nova",
               "story": sid, "parte": i, "media_id": mid, "at": now.isoformat(),
               "temas": temas,                         # regra de distância entre temas
               "sha256": shas[i] if i < len(shas) else None,   # a retomada confere que o render não mudou
               "commit": REF}
        reg.update({k_: v_ for k_, v_ in info.items() if k_ != "incerto"})
        state["published"].append(reg)
        state.pop(STATE_PUBLICANDO, None)
        save_state(state)                      # a parte que saiu não volta para a fila
        print(f"  parte {i + 1}/{len(partes)} -> {mid or reg.get('confirmado_por') or 'INCERTA'}", flush=True)

    saiu = PS.publicar_partes(sid, partes, ja, ig_user=IG_USER_ID, api_post=api_post, api_get=api_get,
                              raw_url=raw_url, registrar=registrar, antes_de_publicar=antes, conteineres=prev,
                              erros_fatais=(AuthError,))
    completa = len(CS.partes_publicadas(state["published"]).get(sid, {})) == len(partes)
    if saiu and completa:
        state["last_story_nova_date"] = hoje.isoformat()
        save_state(state)
    prob = PS.conferir_no_ar(saiu, api_get, erros_fatais=(AuthError,))
    if prob:
        raise RuntimeError(f"story {sid} publicada, mas a conferência no ar falhou: " + "; ".join(prob))
    print(f"Story {sid} OK -> {len(saiu)} parte(s) neste run" + ("" if completa else " (story INCOMPLETA)"))
    if erros_fila and falhas is None:
        raise RuntimeError("stories da fila com erro de portão: " + "; ".join(erros_fila))
    return bool(saiu)

def main():
    posts   = load_json(POSTS_FILE, [])
    stories = load_json(STORIES_FILE, [])
    seqs    = load_json(SEQ_FILE, [])
    reels   = load_json(REELS_FILE, [])
    state = load_json(STATE_FILE, {"published": [], "last_post_date": "", "last_seq_date": "", "last_reel_date": ""})
    state.setdefault("published", []); state.setdefault("last_post_date", ""); state.setdefault("last_seq_date", ""); state.setdefault("last_reel_date", "")
    done = {e["id"] for e in state["published"]}
    now = dt.datetime.now(dt.timezone.utc); brt = now.astimezone(BRT); today = brt.date().isoformat()
    mod = brt.hour*60 + brt.minute; changed = False
    auth_error = None   # token morto: para tudo, grava o que saiu e sai com exit 1
    falhas = []         # falhas NAO-auth: o run termina VERMELHO (ver _falhou)

    _avisar_validade_do_token()

    # Peca com publicacao INCERTA (media_publish errou e o conteiner nao confirmou): fica fora da fila
    # (republicar seria duplicar) e TODO run fica vermelho ate a conferencia humana (RUNBOOK §12).
    for e in state["published"]:
        if e.get("kind") in KINDS_INCERTOS:
            _falhou(falhas, f"{e['kind']} {e.get('id')}", RuntimeError(
                f"publicacao INCERTA desde {e.get('at')} (conteiner {e.get('container')}) — confira no app e "
                "resolva no state/published.json (docs/02_RUNBOOK.md §12)"))

    # Write-ahead de reel/post que um run anterior deixou: pergunta ao conteiner ANTES de qualquer decisao
    # (entrega tardia depois do 500, job morto no media_publish). Ver _resolver_write_ahead_feed.
    try:
        wa_reuso, wa_bloq = _resolver_write_ahead_feed(state, falhas)
    except AuthError as e:                       # token morto ja' na consulta: nada decidido, nada publicado
        _avisar_token_parado(e)
    done = {e["id"] for e in state["published"]}

    # ALARME FAIL-LOUD (B6-iii): N ultimas pecas do feed com ZERO curtidas = publicar no vazio.
    # Avaliado antes de qualquer publicacao agendada (FORCE_ID e' decisao humana e passa direto).
    if ALARME_CURTIDAS and not FORCE_ID:
        try:
            leitura = _ultimas_pecas_sem_curtida()
        except AuthError as e:                   # token morto ja' na leitura: mesmo caminho de sempre
            _avisar_token_parado(e)
        if leitura is not None:
            soma, ids_lidos = leitura
            if soma == 0:
                state["alarme_curtidas"] = {"quando": now.isoformat(), "pecas": ids_lidos, "curtidas": 0}
                save_state(state)
                print(f"::error::ALARME: as {len(ids_lidos)} ultimas pecas do feed somam ZERO curtidas "
                      f"({', '.join(ids_lidos)}). O motor NAO vai publicar no vazio: fila PAUSADA ate' "
                      "decisao humana (var ALARME_CURTIDAS=off no repo, ou FORCE_ID). Ver docs/02_RUNBOOK.md.")
                falhas.append("alarme_zero_curtidas")
                # exit explicito AQUI (como _avisar_token_parado): o estado ja' foi gravado e
                # nada foi publicado — o job tem de ficar VERMELHO em qualquer chamador.
                sys.exit(1)
            elif "alarme_curtidas" in state:
                del state["alarme_curtidas"]; changed = True

    if FORCE_ID == "destaques":
        for it in load_json(DESTAQUES_FILE, []):
            try:
                mid = publish_story(it); log(state, it["id"], "story", mid, now); changed = True
                print(f"Destaque {it['id']} OK -> {mid}")
            except PublicacaoIncerta as e:
                changed = True
                if _registrar_incerto(state, falhas, it["id"], "story", e, now): auth_error = e; break
            except AuthError as e: auth_error = e; break
            except Exception as e: _falhou(falhas, f"destaque {it['id']}", e)
        if changed: save_state(state)
        if auth_error: _avisar_token_parado(auth_error)
        return falhas

    if FORCE_ID.startswith("story:"):
        # decisão humana: publica AGORA a story da geração nova (portão e aprovação continuam valendo)
        try:
            if not publicar_story_nova(state, reels, brt, now, forcar=FORCE_ID.split(":", 1)[1], falhas=falhas):
                _falhou(falhas, f"FORCE {FORCE_ID}", RuntimeError("nada publicado neste run"))
        except AuthError as e: _avisar_token_parado(e)
        except Exception as e: _falhou(falhas, f"FORCE {FORCE_ID}", e)
        return falhas

    if FORCE_ID:
        it = next((x for x in posts if x["id"] == FORCE_ID), None); kind = "post"
        if it is None:
            it = next((x for x in seqs if x["id"] == FORCE_ID), None); kind = "seq"
        if it is None:
            it = next((x for x in stories if x["id"] == FORCE_ID), None); kind = "story"
        if it is None:
            it = next((x for x in reels if x["id"] == FORCE_ID), None); kind = "reel"
        if it is None:
            # FORCE_ID digitado errado tambem e' falha: antes saia verde sem publicar nada.
            _falhou(falhas, f"FORCE_ID={FORCE_ID}", ValueError("id nao encontrado em nenhuma biblioteca"))
            return falhas
        wa_f = None
        if kind in KINDS_WRITE_AHEAD:
            ent_f = wa_reuso.get(kind)
            if kind in wa_bloq:                  # sem saber se o conteiner preparado saiu, nada deste tipo sai (nem
                _falhou(falhas, f"FORCE {FORCE_ID}", RuntimeError(wa_bloq[kind][1]))   # gravar outro write-ahead por cima)
                return falhas
            if ent_f and ent_f.get("id") != it["id"]:
                # gravar o write-ahead desta peca apagaria o do conteiner FINISHED da outra (que a Meta ainda pode entregar)
                _falhou(falhas, f"FORCE {FORCE_ID}", RuntimeError(
                    f"o {kind} {ent_f.get('id')} tem conteiner preparado (write-ahead FINISHED, {ent_f.get('container')}): "
                    "o proximo run agendado do tipo o publica primeiro — FORCE de outra peca espera (docs/02_RUNBOOK.md §12)"))
                return falhas
            wa_f = _wa(state, kind, it, ent_f)
        try:
            if kind == "post": mid = publish_post(it, wa=wa_f)
            elif kind == "seq": mid = publish_sequence(it)[0]
            elif kind == "story": mid = publish_story(it)
            else: mid = publish_reel(it, wa=wa_f)
            log(state, it["id"], kind, mid, now); save_state(state); print(f"FORCE {FORCE_ID} OK -> {mid}")
        except PublicacaoIncerta as e:
            if _registrar_incerto(state, falhas, it["id"], kind, e, now): _avisar_token_parado(e)
        except AuthError as e: _avisar_token_parado(e)
        except Exception as e: _falhou(falhas, f"FORCE {FORCE_ID}", e)
        return falhas

    if not POSTS_ATIVOS:
        print("Posts (carrosseis estaticos): SUSPENSOS — all-in no formato novo (24/10/2026, regra_reels.py).")
    if not SEQUENCIAS_ATIVAS:
        print("Sequencias de stories antigas: SUSPENSAS — all-in no formato novo (24/10/2026, regra_reels.py).")

    # POSTS (feed)
    if POSTS_ATIVOS and brt.weekday() in POST_WEEKDAYS and mod >= POST_MIN and state["last_post_date"] != today:
        it, ent_wa = _escolher_com_write_ahead("post", posts, wa_reuso, wa_bloq, falhas, lambda: next_item(posts, done))
        if it:
            try:
                mid = publish_post(it, wa=_wa(state, "post", it, ent_wa)); log(state, it["id"], "post", mid, now)
                done.add(it["id"]); state["last_post_date"] = today; changed = True; wa_reuso.pop("post", None)
                print(f"Post {it['id']} OK -> {mid or 'confirmado pelo conteiner'}")
            except PublicacaoIncerta as e:
                done.add(it["id"]); state["last_post_date"] = today; changed = True; wa_reuso.pop("post", None)
                auth_error = _registrar_incerto(state, falhas, it["id"], "post", e, now) or auth_error
            except AuthError as e: auth_error = e
            except Exception as e: _falhou(falhas, f"post {it['id']}", e)
        elif "post" not in wa_bloq and "post" not in wa_reuso:
            print("Biblioteca de POSTS esgotada — hora de reabastecer.")

    # CARROSSEL EXTRA (4o/sem) — dia-duplo com o Reel; horario escalonado (11h) p/ nao colidir
    if POSTS_ATIVOS and not auth_error and brt.weekday() in POST2_WEEKDAYS and mod >= POST2_MIN and state["last_post_date"] != today:
        it, ent_wa = _escolher_com_write_ahead("post", posts, wa_reuso, wa_bloq, falhas, lambda: next_item(posts, done))
        if it:
            try:
                mid = publish_post(it, wa=_wa(state, "post", it, ent_wa)); log(state, it["id"], "post", mid, now)
                done.add(it["id"]); state["last_post_date"] = today; changed = True; wa_reuso.pop("post", None)
                print(f"Post extra {it['id']} OK -> {mid or 'confirmado pelo conteiner'}")
            except PublicacaoIncerta as e:
                done.add(it["id"]); state["last_post_date"] = today; changed = True; wa_reuso.pop("post", None)
                auth_error = _registrar_incerto(state, falhas, it["id"], "post", e, now) or auth_error
            except AuthError as e: auth_error = e
            except Exception as e: _falhou(falhas, f"post extra {it['id']}", e)
        elif "post" not in wa_bloq and "post" not in wa_reuso:
            print("Biblioteca de POSTS esgotada (extra) — hora de reabastecer.")

    # SEQUENCIA DIARIA (story serializado, 5 frames)
    if SEQUENCIAS_ATIVAS and not auth_error and brt.weekday() in SEQ_WEEKDAYS and mod >= SEQ_MIN and state["last_seq_date"] != today:
        it = next_item(seqs, done)
        if it:
            try:
                print(f"Sequencia {it['id']} ({it.get('theme','')}) — publicando {len(it['images'])} frames...")
                ids = publish_sequence(it); log(state, it["id"], "seq", ids[0], now)
                state["published"][-1]["media_ids"] = ids    # TODOS os frames: a conferencia da conta (stories) os reconhece
                done.add(it["id"]); state["last_seq_date"] = today; changed = True
                print(f"Sequencia {it['id']} OK -> {len(ids)} frames")
            except PublicacaoIncerta as e:
                done.add(it["id"]); state["last_seq_date"] = today; changed = True
                auth_error = _registrar_incerto(state, falhas, it["id"], "seq", e, now) or auth_error
            except AuthError as e: auth_error = e
            except Exception as e: _falhou(falhas, f"sequencia {it['id']}", e)
        else:
            print("Biblioteca de SEQUENCIAS esgotada — hora de reabastecer.")

    # STORIES DA GERAÇÃO NOVA (3 toques, roteiro próprio)
    if STORIES_NOVOS_ATIVOS and not auth_error and brt.weekday() in STORY_NOVO_WEEKDAYS and mod >= STORY_NOVO_MIN \
            and state.get("last_story_nova_date") != today:
        try:
            if publicar_story_nova(state, reels, brt, now, falhas=falhas):
                changed = True
        except AuthError as e: auth_error = e
        except Exception as e: _falhou(falhas, "story da geração nova", e)

    # REELS
    if not auth_error and brt.weekday() in REEL_WEEKDAYS and mod >= REEL_MIN and state["last_reel_date"] != today:
        it, ent_wa = _escolher_com_write_ahead("reel", reels, wa_reuso, wa_bloq, falhas,
                                               lambda: proximo_reel(reels, done, state, brt))
        if it:
            try:
                mid = publish_reel(it, wa=_wa(state, "reel", it, ent_wa)); log(state, it["id"], "reel", mid, now)
                done.add(it["id"]); state["last_reel_date"] = today; changed = True
                print(f"Reel {it['id']} ({_formato(it)}) OK -> {mid or 'confirmado pelo conteiner'}")
            except PublicacaoIncerta as e:
                done.add(it["id"]); state["last_reel_date"] = today; changed = True
                auth_error = _registrar_incerto(state, falhas, it["id"], "reel", e, now) or auth_error
            except AuthError as e: auth_error = e
            except Exception as e: _falhou(falhas, f"reel {it['id']}", e)
        elif "reel" in wa_bloq or "reel" in wa_reuso:
            pass                                 # write-ahead bloqueando: a falha ja' foi registrada
        elif any(x["id"] not in done for x in reels):
            # Nao e' falha nem biblioteca vazia: as cotas da semana (lamina, conversa) ja' sairam e
            # nao ha' COMO FUNCIONA pronto. Dia sem reel, por decisao (18 e 19/10/2026).
            print(f"Reels: nenhum COMO FUNCIONA pronto na fila — sem reel hoje (lamina: cota {LAMINAS_POR_SEMANA}/semana; "
                  f"conversa: {'so a cada ' + str(DIAS_ENTRE_CONVERSAS) + ' dias' if CONVERSAS_ATIVAS else 'suspensa'}). "
                  "Produza COMO FUNCIONA para a fila nao parar.")
        else:
            print("Biblioteca de REELS esgotada — hora de reabastecer.")

    # Grava o estado ANTES de sair com erro, para nao reperder o que ja' foi publicado
    # quando o token morre no meio da execucao.
    if changed: save_state(state); print("Estado atualizado.")
    elif not auth_error and not falhas: print("Nada a publicar agora.")

    if auth_error: _avisar_token_parado(auth_error)
    return falhas

if __name__ == "__main__":
    # O exit code vive AQUI, nao dentro do main(), para que todo caminho de saida
    # (inclusive os `return` antecipados do FORCE_ID) passe pelo mesmo veredito.
    _falhas = main() or []
    if _falhas:
        print(f"::error::{len(_falhas)} item(ns) falharam SEM publicar: {'; '.join(_falhas)}")
        print("::error::Item que falha nao entra em `done`: o cron (*/30) vai RETENTAR o mesmo "
              "item indefinidamente. Se for 'BLOQUEADO CFM', a fila NAO anda sozinha — "
              "corrija ou remova o item (docs/02_RUNBOOK.md).")
        sys.exit(1)
