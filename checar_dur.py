#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
checar_dur.py — o campo `dur` das filas de reel tem de ser a duração REAL do MP4.

POR QUE EXISTE (auditoria v2, 19/09/2026, achado D4): `dur` era escrito pelos geradores
como a SOMA das durações das cenas do storyboard (`gerar_reels.py:86-88`, cenas de 3,0 s),
não como a duração do arquivo que vai ao ar. Com narração, o MP4 renderizado fica muito
mais longo que o storyboard: 54 dos 57 itens que declaravam `dur` erravam mais de 10%
(−58,6% a +243,1%) e outros 47 não declaravam nada. Como `dur` é o DENOMINADOR da retenção
(watch time ÷ duração), a auditoria v1 publicou 9,5% de retenção onde o real era 3,5% —
o erro de medição chegou a ser quase o dobro do número relatado.

Duração é lida do átomo `mvhd` do próprio arquivo (sem depender de ffprobe estar instalado).
Validação cruzada feita na v2: as 4 durações medíveis batem com as curvas lidas no app em
13/09 (`LEITURA_2026-09-13.md`): 31,1/36,7/30,4/40,6 s contra 31/36/30/40 s.

Uso:
  python checar_dur.py                 # CONFERE (exit 1 se algum dur diverge >10% ou falta)
  python checar_dur.py --corrigir      # reescreve `dur` com o valor medido
  python checar_dur.py --auto-teste    # prova que o checador reprova de verdade
"""
import argparse
import io
import json
import os
import struct
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
ROOT = os.path.dirname(os.path.abspath(__file__))
FILAS = ["reels.json", "reels_legado_mudos.json"]
TOLERANCIA = 0.10


def duracao_mp4(caminho):
    """Segundos pelo átomo mvhd. None se o arquivo não tiver um mvhd legível."""
    try:
        with open(caminho, "rb") as f:
            dados = f.read(4 * 1024 * 1024)               # mvhd vive no início do moov
    except OSError:
        return None
    i = dados.find(b"mvhd")
    if i < 0:
        return None
    off = i + 4
    try:
        versao = dados[off]
        if versao == 0:
            escala, unidades = struct.unpack(">II", dados[off + 12:off + 20])
        else:
            escala, unidades = struct.unpack(">IQ", dados[off + 20:off + 32])
    except (struct.error, IndexError):
        return None
    return unidades / escala if escala else None


def varrer():
    """[(fila, item, dur_declarado, dur_real)] só dos itens cujo MP4 existe no repo."""
    out = []
    for fila in FILAS:
        p = os.path.join(ROOT, fila)
        if not os.path.exists(p):
            continue
        itens = json.load(open(p, encoding="utf-8"))
        for it in itens:
            video = it.get("video") or ""
            if not video:
                continue
            caminho = os.path.join(ROOT, video.replace("/", os.sep))
            if not os.path.exists(caminho):
                continue                                   # mp4 renderizado sob demanda: não é dívida daqui
            out.append((fila, it, it.get("dur"), duracao_mp4(caminho)))
    return out


def conferir(universo=None, verbose=True):
    """`universo` permite conferir uma lista JA CARREGADA. Sem isso o auto-teste seria um
    controle negativo contaminado: `varrer()` relê do disco e descartaria a semente em
    memória, então o checador pareceria aprovar/reprovar por conta de outro item — o
    defeito que este próprio auto-teste pegou na primeira execução (19/09/2026)."""
    faltando, errados, ok = [], [], 0
    for fila, it, declarado, real in (varrer() if universo is None else universo):
        if real is None:
            continue
        if declarado is None:
            faltando.append((fila, it["id"], round(real, 1)))
        elif abs(declarado - real) / real > TOLERANCIA:
            errados.append((fila, it["id"], declarado, round(real, 1)))
        else:
            ok += 1
    if verbose:
        for f, i, r in faltando[:40]:
            print(f"  FALTA    {i:30} ({f}) — real {r}s")
        for f, i, d, r in errados[:40]:
            erro = (d - r) / r * 100
            print(f"  DIVERGE  {i:30} ({f}) — declarado {d}s, real {r}s ({erro:+.0f}%)")
        total = ok + len(faltando) + len(errados)
        print(f"\n{total} item(ns) com MP4 no repo | OK {ok} | sem dur {len(faltando)} | "
              f"divergente >{int(TOLERANCIA*100)}% {len(errados)}")
        if total == 0:
            print("ERRO: universo VAZIO — nenhum MP4 conferido. Universo vazio nao e' aprovacao.")
    return faltando, errados, ok


def corrigir():
    mudou_total = 0
    for fila in FILAS:
        p = os.path.join(ROOT, fila)
        if not os.path.exists(p):
            continue
        itens = json.load(open(p, encoding="utf-8"))
        mudou = 0
        for it in itens:
            video = it.get("video") or ""
            if not video:
                continue
            caminho = os.path.join(ROOT, video.replace("/", os.sep))
            if not os.path.exists(caminho):
                continue
            real = duracao_mp4(caminho)
            if real is None:
                continue
            novo = round(real, 1)
            if it.get("dur") != novo:
                print(f"  {it['id']:30} {it.get('dur')} -> {novo}")
                it["dur"] = novo
                mudou += 1
        if mudou:
            with open(p, "w", encoding="utf-8", newline="\n") as f:
                json.dump(itens, f, ensure_ascii=False, indent=1)
                f.write("\n")
            print(f"{fila}: {mudou} dur corrigido(s)")
            mudou_total += mudou
    print(f"TOTAL corrigido: {mudou_total}")
    return mudou_total


def auto_teste():
    """Controle positivo: semeia um dur absurdo em memória e exige que o checador acuse.
    Checador que nunca reprova não é checador (lição da casa)."""
    universo = varrer()
    alvo = next(((f, it, d, r) for f, it, d, r in universo if r), None)
    if not alvo:
        sys.exit("auto-teste: nenhum MP4 no repo para testar.")
    _f, it, _d, real = alvo
    original = it.get("dur")
    # O universo tem de ser o MESMO objeto em memória nas duas checagens, e reduzido ao
    # item semeado: senão os outros itens divergentes do disco respondem no lugar dele.
    so_o_alvo = [(f, i, d, r) for (f, i, d, r) in universo if i is it]
    try:
        it["dur"] = round(real * 3, 1)                     # +200%: tem de ser acusado
        _falta, errados, _ok = conferir([(f, i, i.get("dur"), r) for f, i, _d, r in so_o_alvo],
                                        verbose=False)
        if not any(e[1] == it["id"] for e in errados):
            sys.exit("FALHA no auto-teste: dur 3x errado passou — o checador esta cego.")
        print("auto-teste: dur 3x errado foi ACUSADO, como esperado.")
        it["dur"] = round(real, 1)                         # controle negativo: valor certo passa
        falta, errados, ok = conferir([(f, i, i.get("dur"), r) for f, i, _d, r in so_o_alvo],
                                      verbose=False)
        if any(e[1] == it["id"] for e in errados) or falta:
            sys.exit("FALHA no auto-teste: dur CERTO foi acusado — o checador reprova tudo.")
        if ok != 1:
            sys.exit("FALHA no auto-teste: o item correto nao foi contado como OK.")
        print("auto-teste: dur correto passou, como esperado. OK")
    finally:
        it["dur"] = original                               # só memória; nada foi gravado
    return 0


def main():
    ap = argparse.ArgumentParser(description="Confere/corrige o campo dur das filas de reel.")
    ap.add_argument("--corrigir", action="store_true", help="reescreve dur com a duracao medida")
    ap.add_argument("--auto-teste", action="store_true")
    a = ap.parse_args()
    if a.auto_teste:
        return auto_teste()
    if a.corrigir:
        corrigir()
        print("\nconferindo depois de corrigir:")
    faltando, errados, ok = conferir()
    if ok + len(faltando) + len(errados) == 0:
        return 1
    return 1 if (faltando or errados) else 0


if __name__ == "__main__":
    sys.exit(main())
