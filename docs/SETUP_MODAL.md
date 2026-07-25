# 🎙️ SETUP MODAL — treino da voz pt-BR

> ⚠️ **Documento RECONSTRUÍDO em 25/07/2026.** O original foi perdido na troca de máquina
> (vivia fora do Git). Este texto foi remontado a partir do que está **codificado** em
> [`voz/modal_voz.py`](../voz/modal_voz.py), que o cita como fonte para o bootstrap.
> Se o original reaparecer, prevalece o original.

Fine-tune **VITS** de uma voz pt-BR no [Modal](https://modal.com), desenhado para ser
**auto-curável**: dispara e esquece. Se cair, religa sozinho e retoma do checkpoint.

> 🔒 **O repositório é público.** Nunca commite tokens, nem o valor do `HF_TOKEN`, nem
> credenciais do Modal. Segredos vivem em `modal secret`. Ver `02_RUNBOOK §5`.

---

## 1. Bootstrap (uma vez)

```bash
pip install modal && modal setup
```
```bash
modal secret create huggingface HF_TOKEN=<seu_token_hf>
```
```bash
modal deploy voz/modal_voz.py
```
```bash
modal run voz/modal_voz.py
```

| Comando | O que faz |
|---|---|
| `modal setup` | autentica a CLI na sua conta |
| `modal secret create huggingface` | cria o secret com o token do Hugging Face |
| `modal deploy` | liga o **cron de segurança** (a cada 8 h) |
| `modal run` | dispara o **primeiro treino agora** (bloqueia até o ciclo retornar status) |

O `deploy` e o `run` são independentes: `deploy` só agenda; `run` executa já.

---

## 2. Por que Modal

Cron nativo + retries + Volume persistente. A combinação é o que torna o treino "dispara e esquece":

- **Fine-tune** a partir de `tts_models/pt/cv/vits` → termina em ~5-10 h de GPU, não semanas.
- **Checkpoints no Volume** (durável entre execuções) → retoma com `continue_path`, que restaura
  otimizador, scheduler e passo — resume real, não só os pesos.
- Se a sessão cair, o **retry do Modal** e o **`modal.Cron` de segurança** religam sozinhos.
- Ao atingir o alvo, grava `DONE` e **tudo vira no-op** — o cron continua rodando sem fazer nada.
- **Heartbeat** (`progress.txt`) espelhado no Hugging Face, para acompanhar de fora.
- **Lease anti-concorrência**: nunca dois treinos escrevendo no mesmo Volume.

---

## 3. Parâmetros

| Constante | Valor | Significado |
|---|---|---|
| `app` | `voz-ptbr` | nome da app no Modal |
| `vol` | `voz-ckpt` | Volume persistente (criado se faltar) |
| `BASE_MODEL` | `tts_models/pt/cv/vits` | base portuguesa para fine-tune |
| `TARGET_STEP` | `35000` | alvo de qualidade (~5-10 h em A10G) |
| `LEASE_TTL` | `1200` (20 min) | lease sem refresh nesse prazo = treino morto |
| `HF_DS` | `rafaelvargassilva/tts-ptbr-dados` | dataset (Hugging Face) |
| `HF_CK` | `rafaelvargassilva/voz-ptbr-ckpt` | destino dos checkpoints |
| GPU | `A10G` | |
| `timeout` | `12 * 3600` | 12 h por execução |
| `retries` | `2` | |
| `schedule` | `modal.Cron("0 */8 * * *")` | religa a cada 8 h |

### Layout do Volume (`/ckpt`)

```
/ckpt
├── run/           RUNROOT  — config + checkpoints do Coqui
├── data/          DATADIR  — dataset cacheado (metadata.csv)
├── DONE           alvo atingido → tudo vira no-op
├── RUNNING        LEASE — timestamp do treino ativo
└── progress.txt   PROG — heartbeat, espelhado no HF
```

---

## 4. Como um ciclo decide o que fazer

`_train_once()` é **idempotente**. Na ordem:

1. **`DONE` existe?** → retorna `DONE`, não faz nada.
2. **`RUNNING` fresco?** (idade < 20 min) → retorna `BUSY`, outro treino está ativo.
3. Grava o próprio lease.
4. **Dataset em cache?** Se não, `snapshot_download` do HF para `/ckpt/data`.
5. **Decide o modo:**
   - existe subpasta de run com `.pth` → **`continue_path`** (resume real)
   - senão → baixa a base e usa **`restore_path`** (fine-tune, run nova)
   - base indisponível → treino do zero (fallback)
6. Treina em subprocesso, com uma thread de monitor a cada 180 s: atualiza o lease, faz
   `vol.commit()` e publica o heartbeat.
7. **No fim**, remove o lease, sobe o melhor checkpoint + `config.json` para o HF, e retorna:

| Status | Condição |
|---|---|
| `DONE` | `rc == 0` **e** passo ≥ 35000 → grava `DONE` |
| `PAUSED` | `rc == 0`, alvo não atingido → o próximo ciclo retoma |
| `FAILED` | `rc != 0` |
| `BUSY` | outro treino com lease vivo |

---

## 5. Config de treino (a `RECIPE`)

Se for fine-tune, **herda a config da base** — chars e áudio precisam bater com os pesos. Só cai
para a config char pt-BR manual (22050 Hz) se a herança falhar.

Overrides fixos:

```
batch_size=16 · eval_batch_size=8 · epochs=1000
use_phonemes=False · text_cleaner="multilingual_cleaners"
save_step=1000 · save_n_checkpoints=3 · save_best_after=1000
print_step=25 · plot_step=200
mixed_precision=False
```

> ⚠️ **`mixed_precision=False` é intencional.** Fix confirmado: fp16 derrubava o `kl_loss` já no
> passo 0. Não reative sem reproduzir o problema — está anotado em
> [`voz/modal_voz.py:227`](../voz/modal_voz.py#L227).

---

## 6. Operação

**Acompanhar de fora:** `progress.txt` no repo `rafaelvargassilva/voz-ptbr-ckpt` no Hugging Face.
Traz `STATUS`, `STEP`, `TS`, `TARGET` e as últimas métricas do log.

**Nos logs do Modal:** linhas `[MON] passo~N | Xmin` a cada 3 min.

| Sintoma | Causa provável | Ação |
|---|---|---|
| Todo ciclo retorna `BUSY` | lease preso de um processo morto | apagar `/ckpt/RUNNING` no Volume |
| Retorna `DONE` sem treinar | `DONE` já existe | apagar `/ckpt/DONE` para retomar |
| `FAILED` repetido | erro no treino | ver `train.log` no fim do heartbeat |
| Não retoma, recomeça do zero | sem `.pth` em `/ckpt/run/*` | conferir se o `vol.commit()` rodou |
| Push ao HF falha | token sem permissão de escrita | recriar o secret `huggingface` |

**Parar de vez:** `modal app stop voz-ptbr` (ou gravar `DONE` no Volume, que zera o custo do cron
sem removê-lo).

---

## 7. Estado

Ver [`03_AUDITORIA.md §1`](03_AUDITORIA.md) — há uma **decisão pendente** sobre manter ou pausar o
treino de voz própria. Este documento descreve a infra; não afirma que o treino esteja ativo.

---

## Referências cruzadas

- [`00_ARQUITETURA.md`](00_ARQUITETURA.md) — pipeline ponta a ponta
- [`GUIA_PRODUCAO_RECUPERACAO.md`](GUIA_PRODUCAO_RECUPERACAO.md) — a voz Antonio é a de produção hoje (rate -8%, pitch -4Hz)
- [`03_AUDITORIA.md`](03_AUDITORIA.md) — decisão pendente sobre o treino
