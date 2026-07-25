# YouTube — série "Recuperação": caminho de publicação e decisões

**Escrito em 25/07/2026.** Canal: `UCVxnOwRuauSrn9dJ-tNpSYw` (Dr. Rafael Vargas).
Série: 34 episódios de `episodios_pos_op.py` (17 temas × adulto + `_kids`), todos renderizados em
`reels\_preview_<id>.mp4`.

## TL;DR

- ✅ **27 dos 34 já estão no ar.** Faltam **7**: `carga_fisio_kids`, `consolidacao`,
  `consolidacao_kids`, `retirada_fixador`, `retirada_fixador_kids`, `banho_posop`, `banho_posop_kids`.
- 🆕 Inventário passou a existir: **[`state/published_youtube.json`](../state/published_youtube.json)**.
  Antes desta data **nada** no repositório registrava o que estava publicado.
- 📋 Texto pronto para colar (os 7 inéditos + os 27 no ar): **[`05a_YOUTUBE_COLAR.md`](05a_YOUTUBE_COLAR.md)**.
- 🔒 **DECIDIDO:** o upload segue **manual**. Não construir uploader via API — ver §2.
- 🔒 **DECIDIDO:** CFM dos metadados de YouTube é **bloqueante**, num gate próprio:
  **[`gate_youtube.py`](../gate_youtube.py)** — ver §4.
- 🔒 **DECIDIDO:** os 5 vídeos no ar cujo título divergia do `seo_episodios.json` foram alinhados
  **JSON ← canal** — nenhum vídeo publicado será renomeado. Falta aplicar neles a **descrição e as
  tags** do JSON, que é o que eles realmente ganham — ver §3.

---

## 1. O inventário real (e por que o comentário do código enganava)

`_gen_seo_json.py:21,30` afirma que **EP01–06 são novos** e que **EP07–28 já estavam publicados**.
Conferido vídeo por vídeo no YouTube Studio (28 Shorts, `1–28 de 28`), a realidade é outra:

| Grupo | Situação real | Metadados no ar |
|---|---|---|
| `gesso_pos_op`, `gesso_pos_op_kids`, `fixador_externo`, `fixador_externo_kids`, `carga_fisio` | **no ar desde 24–25/06** | título ad-hoc + **legenda do Instagram** como descrição |
| 22 episódios de `artrorrise` a `distracao_alongamento_kids` | no ar entre 27/06 e 14/07 | **já são os do `seo_episodios.json`** (título e descrição batem) |
| `carga_fisio_kids` (EP06) + EP29–34 | **inéditos** (7) | — |

Ou seja: **5 dos 6 "novos" já estavam no ar** quando o motor SEO v2 rodou (commit `4f838df`, 03/07).
Como esses 5 ainda não existiam no JSON, `_gen_seo_json.build_entry()` caiu no ramo "episódio novo" e
**gerou títulos pelo motor** em vez de preservar o que estava no canal — exatamente o que o ramo
`existing_entry` existe para evitar. E EP29–34, listados sob o rótulo "EP07–28 (já publicados)",
nunca foram publicados.

> Lição registrada: o comentário não era uma fonte de verdade e não havia como cruzá-lo —
> `seo_episodios.json` nasceu inteiro num único commit, sem versão anterior no git.
> É essa lacuna que o `state/published_youtube.json` fecha.

## 2. DECISÃO: o upload segue manual

**Não construir `publish_youtube.py`.** Motivo principal, e não é quota:

- **Projeto de API não auditado → vídeo enviado sai travado em privado.** Todo vídeo enviado por
  `videos.insert` de um projeto criado depois de 28/07/2020 e ainda não auditado é **restrito a
  privado** até o projeto passar pela auditoria de compliance do Google. Para 7 vídeos, submeter um
  projeto a auditoria é desproporcional — e o custo de errar é publicar 7 vídeos que ninguém vê.
- **Quota deixou de ser argumento em qualquer direção.** Em 04/12/2025 o custo de `videos.insert`
  caiu de ~1.600 para ~100 unidades; com os 10.000/dia padrão dá ~100 uploads/dia. Se o gargalo
  fosse quota, automatizar valeria; não é.
- **Volume é baixo e episódico.** 7 uploads agora; o histórico do canal é 27 vídeos em 3 semanas,
  em lotes de 2–3. Ganho de automação não paga OAuth + auditoria + manutenção de token.
- **OAuth em modo "Testing" expira o refresh token em 7 dias** — para um lote pontual, é atrito puro.

**O que MUDA mesmo assim:** o que faltava nunca foi o uploader, era o **registro**. Sem ledger, a
única memória do que estava publicado era um comentário errado. Por isso `state/published_youtube.json`
foi criado agora e é **mantido à mão** (uma linha por upload). Ele espelha o formato de
`state/published.json`, mas sem automação por trás — a diferença está documentada no próprio arquivo.

### Quando reconsiderar (gatilho explícito)

Construir automação **só** se acontecer um destes:
1. Precisar editar metadados dos 34 de uma vez. `videos.update` custa 50 unidades (34 × 50 = 1.700,
   cabe de sobra) e **não é upload**, então a regra de "travado em privado" não deveria se aplicar.
   **Confirmar num vídeo piloto antes de escrever o script** — essa é a parte que não foi verificada aqui.
2. A cadência virar semanal e sustentada.

## 3. DECIDIDO: título dos 5 antigos sincronizado JSON ← canal

Os 5 episódios publicados em 24–25/06 (antes do motor SEO v2) tinham título divergente. Por decisão
do Rafael em 25/07/2026, **o `seo_episodios.json` foi alinhado ao canal** — não o contrário. Nenhum
vídeo publicado será renomeado. O `title_alt` de cada um foi preservado como estava.

| id | `title` agora no JSON (= o que está no ar) | Era no JSON (descartado) |
|---|---|---|
| `gesso_pos_op` | Cuidados com o gesso depois da cirurgia — e os sinais de alarme (71) | Gesso no pós-operatório: cuidados e sinais de alarme (60) |
| `gesso_pos_op_kids` | Gesso na criança: cuidados e sinais de alarme — guia para os pais (73) | Gesso em criança no pós-operatório — o que fazer (guia para os pais) (76) |
| `fixador_externo` | Fixador externo: cuidados com os pinos e sinais de alarme (65) | Saiu de cirurgia? Fixador externo (**41 — reprovava no lint**) |
| `fixador_externo_kids` | Fixador externo na criança: cuidados com os pinos — guia para os pais (77) | Pós-operatório: Fixador externo em criança (guia para os pais) (70) |
| `carga_fisio` | Operou e tem medo de mexer? Mover cedo é parte do tratamento (68) | Cirurgião explica: Mobilização e fisioterapia precoce (61) |

Por que essa direção: os 5 títulos do canal passam no `_lint_seo.py` e, no `fixador_externo`, o do
canal é melhor pela régua do próprio projeto (65 vs 41 chars, que reprovava — a sincronização
**eliminou** esse aviso do lint); renomear vídeo que já acumula exibição não tem ganho claro; e
alinhar o JSON à realidade é a premissa de todo o resto.

### O que ainda falta nesses 5

**Descrição e tags.** A descrição no ar é a legenda do Instagram — sem as `tags`, sem `search_intent`
e sem o bloco de referências. É esse o ganho real que eles ainda não tiveram. Os blocos em
[`05a_YOUTUBE_COLAR.md`](05a_YOUTUBE_COLAR.md) estão marcados com **"NÃO recolar o título"** para
evitar exatamente o acidente que a sincronização preveniu.

## 4. DECISÃO: CFM dos metadados de YouTube é bloqueante — em gate próprio

Resolve o TODO que estava em `checar_cfm.py` e `gate_publicacao.py` ("é decisão do Rafael").

- **Onde bloqueia:** `gate_youtube.py` (novo). Chama a **mesma** `checar_cfm.auditar_seo_youtube()`
  e derruba o exit em VIOLACAO; soma também o lint SEO (score < 80 bloqueia).
- **Onde NÃO bloqueia:** `gate_publicacao.py` segue advisory de propósito. Um título de YouTube não
  pode travar a publicação do Instagram — o desacoplamento era intencional e foi preservado.
- **Custo de ligar:** zero. Na data da decisão os 34 davam **0 VIOLACAO** e 4 REVISAR (todas por
  citarem "radiografia" em contexto clínico legítimo, que nunca bloqueia). Ligar agora não travou
  nada e passa a travar regressão futura.

```bash
python gate_youtube.py
```

## 5. Runbook: publicar um episódio inédito

1. Rodar o gate → tem que dar **PASS**. Lembrando que `python` não está no PATH (§6):
   ```
   $env:PYTHONIOENCODING="utf-8"
   & "C:\Users\rafae\AppData\Local\Programs\Python\Python311\python.exe" gate_youtube.py <id>
   ```
2. Abrir o bloco do episódio em [`05a_YOUTUBE_COLAR.md`](05a_YOUTUBE_COLAR.md).
3. Subir `reels\_preview_<id>.mp4` como Short, público. Colar título, descrição e tags.
   (O campo de tags do YouTube corta em **500 caracteres**; o maior da série tem 484 — pouca folga,
   conferir o número no bloco antes de colar.)
4. Registrar em [`state/published_youtube.json`](../state/published_youtube.json): mover o id de
   `pendentes` para `published` com `video_id` e a data.

## 6. Verificação (tudo rodado de verdade em 25/07/2026)

⚠️ **`python` não resolve no PATH desta máquina** — o `python.exe` no PATH é o stub de 0 byte da
Microsoft Store. O interpretador real está em
`C:\Users\rafae\AppData\Local\Programs\Python\Python311\python.exe` (3.11.9). Use o caminho absoluto
e `PYTHONIOENCODING=utf-8`.

Números **rerodados em 25/07/2026** depois de `TITULO_DO_CANAL` passar a sair do ledger (a tabela
anterior era de antes da tarefa de sanidade do `title_alt`, que acrescentou 4 regras e o aviso de
`consolidacao`):

| Comando | Resultado |
|---|---|
| `_lint_recuperacao.py` | 34 episódios, **0 erros** · exit 0 |
| `_lint_seo.py --strict` | Média **99/100**, **33 perfeitos**, 2 isentos · exit 0 |
| `gate_youtube.py` | **PASS** · 0 bloqueios, 5 avisos · exit 0 |
| `gate_youtube.py <ids>` | filtro funciona; id inexistente é avisado e ignorado |
| `gate_publicacao.py` (Instagram) | **PASS** · 0 bloqueios · exit 0 |

O único aviso do lint SEO é `consolidacao` com `ALT_LEN_MIN` (`title_alt` de 44 chars, 1 a menos que
o mínimo) — vem da tarefa do `title_alt`, é `title_alt` e não `title`, então não é nada que esteja
no ar. Os 5 avisos do gate são esse mais os 4 `REVISAR` de CFM por citarem "radiografia".

Os avisos de título curto de `artrorrise` (36 chars) e `edema` (43) não são cobrados: são os dois
únicos títulos abaixo de 45 chars em **todo** o `seo_episodios.json`, e ambos estão no ar, então a
isenção `TITLE_LEN_MIN` pega os dois — não renomear vídeo publicado. Continuam **marcados na
saída**, nunca somem em silêncio. Nenhum dos 7 inéditos tem título curto hoje; se um tiver, agora é
cobrado, que era a promessa que a lista antiga quebrava.

### ✅ Corrigido: `TITULO_DO_CANAL` agora sai do ledger

**O defeito.** A lista tinha sido montada a partir do comentário de `_gen_seo_json.py:30` ("EP07-28
já publicados"), que **este documento desmente** (§1). Cruzada com o canal, ela errava nas duas pontas:

- **Isentava 6 episódios que NÃO estão publicados** — `consolidacao`, `consolidacao_kids`,
  `retirada_fixador`, `retirada_fixador_kids`, `banho_posop`, `banho_posop_kids`. São 6 dos 7
  inéditos. O comentário na lista prometia "episódio novo continua sendo cobrado normalmente", e era
  exatamente o que deixava de acontecer para esses seis: título curto passaria em silêncio.
- **Não isentava 5 que ESTÃO publicados** — `gesso_pos_op`, `gesso_pos_op_kids`, `fixador_externo`,
  `fixador_externo_kids`, `carga_fisio`. Foi por isso que a `main` "consertou" o `fixador_externo`
  inventando o título `"Fixador externo: cuidados e sinais de alarme"`, que **não é** o que está no
  ar (`dLqjPf9cl7w` = "Fixador externo: cuidados com os pinos e sinais de alarme"). No merge esse
  título foi descartado em favor do real.

**A correção.** O frozenset hardcoded saiu; `TITULO_DO_CANAL` é **derivado em tempo de execução** de
[`state/published_youtube.json`](../state/published_youtube.json) — isenta quem está em `published`
(27), cobra quem está em `pendentes` (7). Derivar em vez de duplicar é o ponto: a lista não tem como
divergir de novo, porque publicar já é mover o id no ledger (passo 4 do runbook em §5) e a isenção
acompanha sozinha. Id ausente do ledger é cobrado normalmente — a direção segura. Se o ledger sumir
ou corromper, o lint **estoura com mensagem explícita** em vez de devolver lista vazia e desligar a
isenção calado.

Conferido depois da troca: os ids isentos passaram a ser exatamente os 27 de `published`; nenhum
`pendente` isento; `published + pendentes` cobre os 34 do `seo_episodios.json`. Com um título de 27
chars injetado em memória, `banho_posop`/`consolidacao`/`retirada_fixador` voltam a ser cobrados em
`TITLE_LEN_MIN` e `gesso_pos_op`/`carga_fisio`/`fixador_externo` são isentos — o inverso do que a
lista antiga fazia. A saída dos gates não mudou, porque nenhum dos 11 ids afetados tem título curto
hoje: o que mudou foi a regra deixar de estar errada.

### O que foi corrigido no `seo_episodios.json` nesta sessão

- **4 descrições sem sinal de alarme** (`retorno_atividades`, `retorno_atividades_kids`,
  `ortese_bota_kids`, `banho_posop`): mandavam "avise o cirurgião" e nunca citavam pronto-socorro,
  contrariando a convenção nº2 da série e o próprio vídeo. A linha de alarme foi trazida da **cena
  de alarme do próprio episódio**, texto já aprovado por você. Em `banho_posop` isso também trocou
  *"seque com papel"* por *"seque com ar frio, cubra com curativo limpo"* — que é o que o vídeo diz.
  **Confira essa troca**, é instrução clínica.
- **`consolidacao`**: `title` e `title_alt` trocados de posição (o `title` tinha 42 chars e reprovava;
  o `title_alt` gerado pelo motor tem 54 e passa). Nenhum texto novo foi escrito e o episódio é
  inédito, então nada no ar mudou.

3 dos 4 episódios com descrição corrigida **já estão no ar** — a descrição publicada deles está
desatualizada em relação ao JSON. Estão marcados com `desc_desatualizada` no ledger.

---

### Fontes das restrições de API citadas em §2

- [Videos: insert — YouTube Data API](https://developers.google.com/youtube/v3/docs/videos/insert)
- [YouTube Data API — Revision History](https://developers.google.com/youtube/v3/revision_history)
- [YouTube Data API Overview (quota)](https://developers.google.com/youtube/v3/getting-started)
- [YouTube API Quota Limits 2026](https://www.getphyllo.com/post/youtube-api-limits-how-to-calculate-api-usage-cost-and-fix-exceeded-api-quota)
