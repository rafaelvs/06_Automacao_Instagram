# scripts_lote/ — arquivo histórico

Lotes que **já foram cumpridos**. O conteúdo que eles geraram já está nas bibliotecas
(`posts.json`, `reels.json`, `sequences.json`, `stories.json`) e já está sendo publicado.

> **Convenção 4 (`docs/04_ORGANIZACAO_PROPOSTA.md`): lote que já rodou NÃO roda de novo.**
> Rodar de novo **duplica** conteúdo na biblioteca.

## Estes scripts não rodam mais — de propósito

Ao sair da raiz, dois vínculos se romperam. **Isso é intencional**, e funciona como trava
contra reexecução acidental:

**1. `import` local não resolve** (falham na hora, com `ModuleNotFoundError`):

| script | precisa de (ficou na raiz) |
|---|---|
| `posts_batch1.py`, `posts_batch2.py` | `gerar_conteudo` |
| `stories_batch.py`, `stories_batch2.py` | `gerar_conteudo` |
| `gerar_lote_2026.py` | `carrossel`, `episodios_novos_2026`, `gerar_sequencias` |
| `anexar_lote_julho.py` | `episodios_lote_julho_2026` |

**2. `ROOT` derivado de `__file__` aponta para cá, não para a raiz do repo:**
`anexar_lote_julho.py`, `gerar_lote_2026.py`, `gerar_reels.py`, `publish_backup_single.py`.

`reels_batch.py` importa `ROOT` de `gerar_reels`, então herda o mesmo deslocamento.

⚠️ Os do grupo 2 **não falham na hora** — eles rodariam gravando em `scripts_lote/images/`,
`scripts_lote/reels.json` etc. Não rode nada daqui sem ler a seção abaixo.

## Se algum dia for preciso reativar um destes

Não basta mover de volta. Faça, no script:

```python
import os, sys
_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, _REPO)   # resolve os imports da raiz
ROOT = _REPO                # impede gravar dentro de scripts_lote/
```

E antes de rodar, confirme que o lote **não vai reinserir ids que já existem** na biblioteca
de destino (`_auditoria_motor.py` mostra `ids_duplicados`).

## Nota sobre `publish_backup_single.py`

É cópia antiga do `publish.py` e **não tem nenhum guardrail CFM** (`publish.py` tem `_cfm_guard`).
`docs/03_AUDITORIA.md` §2 recomendava remover. Nenhum workflow o chama.
Estando aqui, seu `ROOT` deslocado o deixa inerte (não acha `posts.json`/`state/published.json`),
mas ele continua sendo um publicador funcional se alguém corrigir os caminhos. **Não reative.**

## Validação

O `_auditoria_motor.py` **não** detecta nenhuma das quebras acima — ele valida apenas
referências de mídia dos JSON e os `run: python <path>` dos workflows.
