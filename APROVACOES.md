# APROVAÇÕES — registro vivo (promovido da minuta em 30/08/2026)

**30/08/2026 — D2:** lote `alongamento_adulto` (11 eps) APROVADO pelo Rafael via chat (auditoria-instagram-v1). **D3:** lote `qa_lote2` (12 eps) APROVADO idem, com as 2 notas de consenso sinalizadas. `legado_pre_gate` documenta a fila pré-existente (ratificação pendente). Fonte de verdade da máquina: `aprovacoes.json` (hash por episódio; conferir com `python checar_aprovacoes.py --hash <id> --fontes .`).

---

**30/08/2026 — piloto de voz do lote 2 APROVADO:** `_preview_qa_gesso_molhar.mp4` enviado ao Rafael antes da intercalação; resposta dele no chat: "está ótimo esse áudio". Motor de voz INALTERADO (edge-tts Antonio, fingerprint 6488eb26…); o piloto valida o formato do lote, conforme a regra de piloto instituída por ele em 30/08.

# MINUTA — APROVACOES.md · Registro de aprovação clínica dos reels narrados

> **STATUS: RASCUNHO LOCAL · AGUARDA AVAL DO RAFAEL.**
> Nada neste arquivo vale como aprovação. Nenhuma linha daqui autoriza enfileiramento.
> Destino proposto após o aval: raiz do repo de produção do motor Instagram, ao lado de
> `reels.json`, com o irmão máquina-legível `aprovacoes.json` (ver `minuta_aprovacoes.json`).
> Redigido em 30/08/2026 na execução S1 preparatória (Aposta 3 do plano de 29/08).

---

## 1. O que é este registro e como ele funciona

Este arquivo é o **registro humano-legível** do gate de aprovação clínica: por lote, **quem
aprovou o quê, quando, em que escopo, e o hash exato dos roteiros no ato da aprovação**. O
irmão `aprovacoes.json` carrega os mesmos fatos em formato que o enforcement
(`checar_aprovacoes.py`) lê: **item sem registro não entra em `reels.json`**.

Regras do registro (deriva das lições da casa):

1. **Aprovação é por roteiro + hash, não por série.** O hash (`sha256` do JSON canônico do
   dicionário do episódio — fórmula na seção 6) congela o texto avalizado. Editou o roteiro
   depois? A aprovação **não cobre** o texto novo (lição: *uma autorização não cobre o script
   editado*) — o check reprova por divergência de hash e o episódio volta para revisão.
2. **Aprovação tem escopo.** `youtube` e `instagram` são gates distintos: quase tudo que está
   aprovado hoje foi aprovado **no contexto do canal YouTube**. O conteúdo clínico é o mesmo,
   mas o registro não presume transferência — a ratificação para Instagram é pedida
   explicitamente no pacote de revisão (`minuta_pacote_revisao.md`).
3. **Quem aprova conteúdo clínico é o Rafael (CRM-SP 226103, RQE 137901).** O registro grava
   data, canal da resposta (ex.: chat de DD/MM, resposta ao doc X) e observações/ressalvas.
4. **Documento de aprovação se TRANSCREVE, não se referencia.** O gatilho desta minuta foi
   exatamente o cabeçalho que referenciava um doc fora do repo (ver seção 2). A guarda que
   existe só no projeto irmão não protege este repo (lição de 4 dias depois: *voltou*).
5. **Ausência de registro ≠ ausência de aprovação — mas para o gate as duas valem o mesmo.**
   Onde a aprovação aconteceu por chat e não foi gravada, este registro marca
   `pendente_ratificacao` e o pacote de revisão pede a ratificação. O gate só lê o registro.

---

## 2. Achado da preparação (30/08/2026) — onde o registro estava

O cabeçalho de `episodios_alongamento.py` remete a `APROVACAO_SERIE_ALONGAMENTO_L1.md`, que
**não existe em nenhum dos 1.592 paths do repo de produção** (verificação da Grande Revisão,
29/08). Em 30/08, esta preparação localizou os documentos — **no projeto irmão**:

| Documento | Onde está | O que registra |
|---|---|---|
| `APROVACAO_SERIE_ALONGAMENTO_L1.md` | `C:/Users/rafae/Claude Code/Projeto_YouTube_Dr_Rafael_Vargas/` | Lote 1 (31/07): pedido + **seção de status com aprovação dos 3 adultos** + kids "aguardando aval" |
| `APROVACAO_SERIE_ALONGAMENTO_L2.md` | idem | Lote 2 (01/08): **só o pedido** — sem seção de resposta |
| `APROVACAO_SERIE_ALONGAMENTO_L3.md` | idem | Lote 3 (16/08): **só o pedido** — sem seção de resposta |
| `APROVACAO_FORMATO_CURTO_2026-07-30.md` | idem | Formato curto (30/07): **"decisão A+B tomada nesta data"** — cobre os 3 `_curto` |
| `APROVACAO_SERIE_VOCE_PERGUNTOU_2026-08-18.md` | idem | Série 3 YouTube (Q&A): pedido de 18/08, decisão pendente (D11 do plano) |

Não existe `APROVACAO_SERIE_ALONGAMENTO_L4.md` em lugar nenhum.

**Consequências:** (a) o estado de aprovação vivia em docstring + docs de outro projeto —
inauditável do repo que publica; (b) parte do que se acreditava "sem nenhum registro" TEM
registro parcial recuperável — este arquivo o transcreve abaixo; (c) parte do que se publica
como "aprovado" NÃO tem resposta registrada em lugar algum — vai a ratificação, não a fé.

---

## 3. Estado documentado hoje (30/08/2026) — os 60 narrados fora da fila

60 reels narrados prontos (render `_preview_*.mp4` existente), **nenhum em `reels.json`**:
22 Alongamento (11 temas × adulto/`_kids`) + 34 pós-op ("Recuperação", 17 temas × 2) + 4
avulsos (3 `_curto` + `apresentacao_rafael`).

| Lote | Eps | O que os documentos dizem | Status honesto no registro |
|---|---|---|---|
| **ALG-L1 adultos** (`discrepancia_membro`, `fixador_ou_haste`, `tempo_tratamento`) | 3 | Doc L1, seção "✅ Status (31/07)": troca de temas, cena 4 proporcional e roteiros **aprovados pelo Rafael em 31/07/2026**; implementado no commit `6eaafc0`. O mesmo doc registra correção PÓS-aprovação no gancho do A1 (gate CFM): "nem sempre é só estética" → "O que decide é o quanto ela afeta a sua função". | **Aprovado (YouTube) com registro** — o mais forte dos 60. Falta: ratificar a correção do A1 + escopo Instagram. |
| **ALG-L1 kids** (3 `_kids` dos mesmos temas) | 3 | Doc L1, Parte 2: "**aguardando seu aval**", com 2 pontos clínicos marcados (placas de crescimento limitam opções internas; "criança costuma consolidar mais rápido"). Docstring do motor repete "AGUARDANDO". **Porém** o doc L3 (16/08) conta "12 Alongamento no ar" no YouTube — conta que só fecha com estes kids publicados. | **Conflito de registro** — docstring diz aguardando; corpus do canal sugere publicados. Não presumir: *achado recorrente pode ser decisão, não bug*. Perguntar e registrar a resposta. |
| **ALG-L2** (`pseudartrose`, `sequela_fratura`, `primeira_consulta` × adulto/kids) | 6 | Doc L2 (01/08): pedido com 3 pontos ⚠️ (cigarro na consolidação; alusão à pseudartrose congênita via "manchas na pele"; convite à segunda opinião). **Nenhuma resposta registrada.** Episódios implementados, renderizados e no ar no YouTube em 16/08. | **Pendente de ratificação** — aprovação provável (foram ao ar sob supervisão), registro inexistente. Os 3 pontos ⚠️ vão no pacote de revisão. |
| **ALG-L3** (`fim_tratamento` × adulto/kids) | 2 | Doc L3 (16/08): pedido; nota do gate CFM sobre "raio-X" apenas falado (precedente aceito). **Nenhuma resposta registrada.** | **Pendente de ratificação.** |
| **ALG-L4** (`deformidade_angular`, `quanto_alongar`, `trabalho_escola`, `vida_cotidiana_fixador` × adulto/kids) | 8 | Sem doc. Comentário no código (16/08): "**Aprovados pelo Rafael em 16/08 após leitura do risco de sobreposição**" — isso aprova os **TEMAS** (11, 3, 10, 9 — consulta feita no fim do doc L3), não os roteiros, que foram escritos depois. | **Temas aprovados; roteiros sem nenhum registro.** É o lote que mais precisa de leitura real. |
| **PÓS-OP "Recuperação"** (17 temas × adulto/kids) | 34 | Docstring, convenção 7: "cada roteiro […] é APROVADO pelo Rafael (RQE) ANTES do render". `CRONOGRAMA_RECUPERACAO.md` marca ①② "aprovado". Todos públicos como Shorts no YouTube desde jun–ago/2026 (o corpus de 18/08 conta 59 no ar = 34+22+3). | **Processo declarado + publicação supervisionada; zero registro por episódio.** Ratificação em lote com releitura das condutas-chave (alarme→PS, carga, banho, TVP, "3 A" pediátricos). |
| **AVULSOS `_curto`** (`infeccao_ferida_curto`, `retorno_atividades_curto`, `edema_curto`) | 3 | Doc FORMATO_CURTO (30/07): "decisão A+B tomada nesta data"; docstring: "Roteiros aprovados pelo Rafael (RQE 137901) em 30/07/2026". | **Aprovado (YouTube) com registro.** Falta: hash + escopo Instagram. |
| **AVULSO `apresentacao_rafael`** | 1 | Docstring registra decisão de enquadramento do Rafael (não declarar "nunca estética" no marketing), mas **nenhum registro de aprovação do texto**. | **Sem registro.** Leitura integral no pacote (é a peça de maior exposição: apresenta o médico). |

**Síntese:** dos 60, apenas **6** têm aprovação com registro recuperável (3 ALG-L1 adultos +
3 `_curto`) — e mesmo esses, no escopo YouTube. **54 dependem de ratificação ou de leitura
nova.** É exatamente por isso que o gate passa a ser mecânico.

---

## 4. Perguntas abertas que o registro precisa que o Rafael responda

1. **ALG-L1 kids**: os 3 foram mesmo liberados (e quando)? Os 2 pontos clínicos da Parte 2
   do doc L1 foram avaliados? (Se a publicação no YouTube foi decisão, registrar a decisão;
   se foi corrida do processo, os 3 voltam para revisão antes do escopo Instagram.)
2. **ALG-L2/L3**: as respostas aos pedidos de 01/08 e 16/08 existiram (chat)? Basta
   confirmar os pontos ⚠️ de cada doc para registrar como ratificação retroativa.
3. **ALG-L4**: leitura real dos 8 roteiros (não houve pedido formal).
4. **Pós-op**: aceita ratificação em lote com releitura de condutas-chave, ou quer releitura
   integral dos 34? (Pacote de revisão traz os dois caminhos com tempos.)
5. **Escopo Instagram**: a legenda dos narrados pós-15/09 ganhará a linha de disclosure
   "Narração com voz digital (IA)" (D6/CFM 2.454) — a ratificação de escopo já considera isso.

---

## 5. Modelo de entrada de lote (preencher a cada aprovação)

```
### <LOTE-ID> — <nome humano do lote>
- Escopo: instagram | youtube
- Episódios (id + hash do roteiro no ato do aval):
  - <id> · sha256:<hash>
- Aprovado por: Rafael Vargas (CRM-SP 226103, RQE 137901)
- Data: AAAA-MM-DD
- Evidência: <onde a resposta existe — doc, chat de DD/MM, este próprio registro>
- Ressalvas/observações: <ex.: "aprovado com a correção X", "kids segurados">
```

Registro máquina-legível equivalente em `aprovacoes.json` (schema em
`minuta_aprovacoes.json`). O hash é recalculado NO ATO do aval com
`python checar_aprovacoes.py --hash <id> --fontes <dir dos episodios_*.py>` — nunca copiado
de snapshot velho (lição: *inventário afirmado nasce vencido*).

## 5.1 Entradas registradas

**NENHUMA.** Esta minuta não cria aprovação; cria o lugar onde ela passa a morar. As oito
entradas candidatas (com hashes do snapshot de 29–30/08 e status `pendente_ratificacao`)
estão pré-preenchidas em `minuta_aprovacoes.json` para o Rafael converter em `aprovado`
lote a lote, nas sessões do pacote de revisão.

---

## 6. Fórmula do hash e snapshot desta minuta

Hash canônico por episódio: `sha256` de
`json.dumps(episodio, ensure_ascii=False, sort_keys=True, separators=(",", ":"))` sobre o
dicionário Python completo do episódio (cenas com `vo`/`k`/`sc`/`sub`, caption, tudo) — cobre
locução, texto de tela e legenda de uma vez. Implementação de referência:
`minuta_checar_aprovacoes.py` (função `hash_canonico`).

Snapshot das fontes usado nos hashes desta minuta (cópias de 29/08 em `prod_repo/`):

| Arquivo | sha256 (16 primeiros) |
|---|---|
| `episodios_alongamento.py` | `700eaeff9def2998` |
| `episodios_pos_op.py` | `85e132f5f6cca218` |
| `episodios_teste_curto.py` | `b08a8b47c2c551a8` |
| `episodio_apresentacao.py` | `bb9eae4cdad6fe6d` |
| `reels.json` (94 itens; 45 ainda não publicados) | `8d39029dc647f823` |
| `state_published.json` | `31fc182a6ed4dd7f` |

⚠️ No ato de cada aprovação, os hashes são recalculados contra o repo de produção real —
este snapshot serve à revisão, não ao registro final.

---

*Minuta preparada em 30/08/2026 · Aposta 3 (gate de aprovação clínica com enforcement) ·*
*AGUARDA AVAL — nada foi gravado no repo, na fila ou no perfil.*

**30/08/2026 — PROCESSO (regra do Rafael):** por padrão, episódio de formato ESTABELECIDO não passa por aval ativo peça a peça — entra na fila com data futura e o Rafael revisa/edita/suspende antes da publicação (janela de revisão passiva; ver PROGRAMACAO.md). Aval ativo/piloto fica reservado a: (a) estreia de formato ou estratégia NOVA (ex.: reel-caso), (b) qualquer mudança no motor de voz (guarda-freio checar_voz.py). O registro em aprovacoes.json continua obrigatório para todo lote novo — muda a FONTE da evidência, não a exigência do registro.

**30/08/2026 — lote REEL-CASO-PILOTOS aprovado** ('pode seguir'): 3 roteiros do Anatomia de um Caso registrados com hash; render do motor implementado (ilustração esquemática opt-in, byte-identidade provada 300/300 frames); enfileiramento aguarda o aval do render do piloto 1.

**30/08/2026 — render do piloto 1 APROVADO** ('o resultado está absurdamente bom, vamos progredir'): os 3 reel-casos entram na fila para 23/09, 30/09 e 07/10 (quartas, pós-janela v2).
