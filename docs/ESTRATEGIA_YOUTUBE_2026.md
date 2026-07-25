# 📺 ESTRATÉGIA YOUTUBE 2026 — série "Recuperação"

> ⚠️ **Documento RECONSTRUÍDO em 25/07/2026.** O original foi perdido na troca de máquina
> (vivia fora do Git). Este texto foi remontado **a partir das decisões já codificadas** em
> [`seo_youtube.py`](../seo_youtube.py) e [`ganchos.py`](../ganchos.py) — que o citam como fonte
> normativa. Onde o código não fixa um número, o texto diz "não codificado" em vez de inventar.
> Se o original reaparecer, prevalece o original.

Fonte de verdade para **título, descrição, tags e gancho** dos Shorts do YouTube.
Quem consome este doc: `seo_youtube.py` (metadados) e `ganchos.py` (1ª cena).

---

## 1. Os quatro princípios

Codificados no cabeçalho de [`seo_youtube.py:4-13`](../seo_youtube.py#L4-L13).

### 1.1 CTR importa, mas é *gated* pela retenção
O clique só conta se o vídeo entregar. Título que promete além do conteúdo derruba a retenção
e o alcance junto. **Regra prática:** o título nomeia o que a 1ª cena entrega em ≤10 s.
Sem clickbait vazio.

### 1.2 A busca é semântica
O YouTube casa **tópico e intenção**, não string exata. Título e descrição devem cobrir o
assunto na **linguagem do paciente** — "gesso molhou", não "manejo de imobilização gessada".
Daí `_EPISODE_TAGS` (long-tail real) e `_SEARCH_INTENT` (as 3-5 queries que o paciente digita).

### 1.3 E-E-A-T é o fosso — e isto é YMYL
Conteúdo médico é *Your Money or Your Life*: barra de qualidade mais alta. A autoridade de um
cirurgião com CRM e RQE é o que separa o canal do "AI slop" genérico. Por isso **toda** descrição
carrega a assinatura:

```
Dr. Rafael Vargas · CRM-SP 226103 · RQE 137901 — Reconstrução e Alongamento Ósseo · Ortopedia Pediátrica.
Conteúdo educativo, não substitui a avaliação do seu médico.
```

### 1.4 Variação obrigatória (anti-templatização)
A política **"Inauthentic Content"** do YouTube passou a ser aplicada em **jan/2026**
([`ganchos.py:7-8`](../ganchos.py#L7-L8)). Conteúdo produzido em massa com a mesma cara é
desmonetizável. Contramedida em dois níveis:

| Nível | Mecanismo | Onde |
|---|---|---|
| Abertura | 6 arquétipos de gancho em rotação | `ganchos.py` |
| Título | 8 padrões em rotação | `seo_youtube.py` |

Ambas as rotações são **determinísticas por `episode_id`** — reproduzíveis, sem sorteio.

---

## 2. Ganchos — os 6 arquétipos

A 1ª cena é a maior alavanca de retenção: os primeiros segundos decidem se o paciente ou o
familiar fica. Cada arquétipo abre de um jeito diferente.

| # | Arquétipo | Mecanismo psicológico | Kicker sugerido |
|---|---|---|---|
| 1 | `pergunta` | Abre um loop cognitivo que o espectador quer fechar | VOCÊ SABIA? |
| 2 | `mito_vs_verdade` | Ruptura de expectativa; alta saliência | MITO OU VERDADE? |
| 3 | `dado_estatistica` | Ancoragem por proporção; autoridade imediata | SABIA QUE... |
| 4 | `micro_caso` | Empatia de cenário; põe o paciente no enredo | SAIU DA CIRURGIA |
| 5 | `alerta` | Urgência controlada; retém quem cuida em casa | ATENÇÃO |
| 6 | `boa_noticia` | Empoderamento e alívio; retém familiar ansioso | BOA NOTÍCIA |

**Rotação:** `sum(ord(c) for c in episode_id) % 6`, com **offset +3 para `_kids`**. O offset
garante que o par adulto+infantil do mesmo tema nunca abra com o mesmo estilo.

**Uso ao escrever episódio novo:**
```python
import ganchos
guia = ganchos.info("artrorrise")   # dict com desc + dicas de sc/vo/e + exemplos
```
O guia traz `sc_dica`, `vo_dica`, `e_dica` e um par `exemplo_sc`/`exemplo_vo` por arquétipo.
Siga a dica e adapte ao tema clínico — não copie o exemplo.

---

## 3. Título

**8 padrões** em `TITLE_PATTERNS`, rotação por `sum(ord) % 8`. `{foco}` = tema curto;
`{pais}` = `" (guia para os pais)"` nos `_kids`.

| # | Padrão | Ângulo |
|---|---|---|
| P0 | `{foco}: cuidados e sinais de alarme{pais}` | alarme clássico |
| P1 | `Saiu de cirurgia? {foco}{pais}` | gancho pós-op |
| P2 | `{foco} no pós-operatório — o que fazer{pais}` | how-to |
| P3 | `Pós-operatório: {foco}{pais}` | rótulo (fraco, mas varia) |
| P4 | `{foco}: o essencial e quando ir ao pronto-socorro{pais}` | decisão |
| P5 | `O que é normal com {foco}? Quando é sinal de alarme{pais}` | arco de tranquilização |
| P6 | `{foco}: quando chamar o médico — e quando não precisa{pais}` | árvore de decisão |
| P7 | `Cirurgião explica: {foco}{pais}` | E-E-A-T / autoridade |

- **Limite rígido:** 100 caracteres (corte automático).
- **Ideal:** ≥ 45 caracteres — abaixo disso `score_seo` penaliza.
- **`#Shorts` é anexado automaticamente** se ausente.
- `titulo_alt()` gera a variante do padrão seguinte, para **teste A/B**.

---

## 4. Descrição

Montada por `descricao(hook, pontos, hashtags, fontes)` nesta ordem fixa:

1. **Hook** — 1ª linha forte (não repetir o título literalmente).
2. **Pontos** — bullets `•`, o conteúdo prático.
3. **WhatsApp** — `Dúvidas de rotina: WhatsApp (11) 3280-1413.`
4. **Assinatura + disclaimer** — CRM-SP / RQE (§1.3).
5. **Referências** — opcional, ` · ` entre URLs.
6. **Hashtags** — opcional, última linha.

> ⚠️ O WhatsApp é **canal de dúvida de rotina apenas**. Emergência vai para o pronto-socorro —
> nunca direcionar urgência ao WhatsApp. Ver `GUIA_PRODUCAO_RECUPERACAO.md` §R3.

---

## 5. Tags

`tags(foco, kids, episode_id)` = **base genérica** + **long-tail do episódio** + `foco`, com
deduplicação preservando a ordem.

- **Base (8):** ortopedia, pós-operatório, recuperação, Dr. Rafael Vargas, alongamento ósseo,
  reconstrução óssea, ortopedia São Paulo, cirurgia ortopédica.
- **`kids` acrescenta (4):** ortopedia pediátrica, ortopedia infantil, pais, criança.
- **Long-tail:** `_EPISODE_TAGS[episode_id]` — 4 a 11 termos em linguagem de paciente,
  mapeados para **34 episódios** (17 pares adulto/infantil).

**Mínimo: 10 tags.** Abaixo disso `score_seo` penaliza.

---

## 6. Gate de qualidade — `score_seo()`

Roda antes de publicar. Começa em 100 e desconta:

| Verificação | Penalidade |
|---|---|
| Descrição sem `CRM-SP` | **−20** |
| Título > 100 chars | −20 |
| Título < 45 chars | −15 |
| Descrição < 200 chars | −15 |
| Título sem `#Shorts` | −10 |
| Descrição sem "pronto-socorro"/"emergência" | −10 |
| Menos de 10 tags | −10 |

As duas maiores penalidades são **conformidade CFM**, não SEO — a assinatura CRM-SP e a rota de
emergência. Isso é deliberado: o gate protege o registro profissional antes do alcance.

> **Nota de manutenção:** `score_seo` retorna `(score, issues)`. Em
> [`seo_youtube.py:376`](../seo_youtube.py#L376) há uma linha que chama a função duas vezes e
> atribui a `sc, title_score, desc_score` — variáveis mortas, nunca lidas (`gerar()` não devolve
> score). Não quebra nada, mas é lixo a limpar, e o `gerar()` **não aplica o gate**: quem publica
> precisa chamar `score_seo` explicitamente.

### 6.1 O gate de verdade — `_lint_seo.py`

`score_seo()` pontua **um episódio em memória**. Quem audita o arquivo publicado é
[`_lint_seo.py`](../_lint_seo.py), rodando sobre `seo_episodios.json`:

```bash
python _lint_seo.py                    # audita tudo
python _lint_seo.py --strict           # exit 1 se algum episódio < 90 pts
python _lint_seo.py artrorrise tvp     # filtra episódios
```

Ele repete os 7 critérios do `score_seo` e acrescenta **dois**:

| Regra extra | Peso | Por quê |
|---|---|---|
| `TITLE_ALT` | 5 | `title_alt` presente e diferente do `title` — sem isso não há A/B |
| `SEARCH_INTENT` | 5 | `search_intent` com ao menos 1 item |

> ⚠️ **Os pesos das duas implementações divergem.** Mesma verificação, punição diferente:
>
> | Critério | `score_seo` | `_lint_seo` |
> |---|---|---|
> | Título < 45 | −15 | −10 |
> | Título > 100 | −20 | −15 |
> | Descrição < 200 | −15 | −10 |
> | Sem pronto-socorro/emergência | −10 | −15 |
> | Sem `CRM-SP` | −20 | −20 |
> | Sem `#Shorts` / < 10 tags | −10 | −10 |
>
> Um episódio pode passar em um gate e falhar no outro. **`_lint_seo.py` é o que vale** — é ele
> que roda sobre o arquivo que vai ao ar. Vale unificar os pesos num lugar só.

**Isenção de quem já está no canal.** Episódio já publicado entra em `TITULO_DO_CANAL` e **não é
cobrado** no critério de comprimento mínimo do título. Alongar esses títulos significaria renomear
vídeo no ar e perder o histórico de SEO — `_gen_seo_json.py` preserva o `title` deles de propósito.
A isenção **aparece marcada na saída**, nunca some em silêncio, e episódio inédito é cobrado
normalmente.

> A lista é **derivada de [`state/published_youtube.json`](../state/published_youtube.json)** em
> tempo de execução, não escrita à mão. Já foi um frozenset fixo, montado a partir do comentário
> "EP07-28 já publicados" de `_gen_seo_json.py:30` — que o levantamento do canal desmentiu: isentava
> 6 dos 7 inéditos e deixava de isentar 5 que estavam no ar. Ver
> [`05_YOUTUBE.md`](05_YOUTUBE.md) §1 e §6. Derivar é o que impede a divergência de voltar: publicar
> já é mover o id no ledger, e a isenção acompanha.

---

## 7. Intenções de busca

`_SEARCH_INTENT[episode_id]` lista as 3-5 queries reais do paciente por episódio. **Não é
consumido automaticamente** — é referência para refinamento manual do título/descrição e para
análise de performance futura. Ao escrever um episódio novo, comece por aqui: o título deve
responder a pelo menos uma dessas queries.

---

## 8. Checklist de episódio novo

- [ ] `ganchos.info(id)` → escrever a 1ª cena no arquétipo sorteado
- [ ] `search_intent(id)` → conferir que o título responde a uma query real
- [ ] `titulo()` / `titulo_alt()` → par para A/B
- [ ] `descricao()` com hook, pontos, WhatsApp, assinatura
- [ ] `tags()` com `episode_id` (senão perde o long-tail)
- [ ] `python _lint_seo.py --strict <id>` → **≥ 90 pts**, nenhum issue de CFM
- [ ] `python _lint_recuperacao.py <id>` → 0 erros
- [ ] Aprovação do Rafael (RQE) **antes** do render

---

## Referências cruzadas

- [`GUIA_PRODUCAO_RECUPERACAO.md`](GUIA_PRODUCAO_RECUPERACAO.md) — regras R1-R7 do roteiro e as convenções da série
- [`00_ARQUITETURA.md`](00_ARQUITETURA.md) — pipeline ponta a ponta
- [`SETUP_MODAL.md`](SETUP_MODAL.md) — infra da voz pt-BR
