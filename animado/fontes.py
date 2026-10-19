# -*- coding: utf-8 -*-
"""Fontes por PAPEL (preta, negrito, semi, regular), resolvidas no Windows (Segoe UI, onde o
piloto foi feito) e no runner Linux do GitHub (Roboto, pacote `fonts-roboto`), com reserva em
Liberation/DejaVu. `FONTES=<pasta>` força uma pasta. Falha ALTO se nenhuma fonte servir — vídeo
com a fonte errada não pode sair em silêncio."""
import glob
import os
import sys

import skia

CANDIDATOS = {
    "black": ["seguibl.ttf", "Roboto-Black.ttf", "Roboto-ExtraBold.ttf", "Roboto-Bold.ttf",
              "LiberationSans-Bold.ttf", "DejaVuSans-Bold.ttf"],
    "bold": ["segoeuib.ttf", "Roboto-Bold.ttf", "LiberationSans-Bold.ttf", "DejaVuSans-Bold.ttf"],
    "semi": ["seguisb.ttf", "Roboto-Medium.ttf", "LiberationSans-Bold.ttf", "DejaVuSans-Bold.ttf"],
    "reg": ["segoeui.ttf", "Roboto-Regular.ttf", "LiberationSans-Regular.ttf", "DejaVuSans.ttf"],
}
PASTAS = [os.environ.get("FONTES", ""), os.path.join(os.environ.get("WINDIR", r"C:\Windows"), "Fonts"),
          "/usr/share/fonts", "/usr/local/share/fonts", os.path.expanduser("~/.fonts")]

_cache = {}


def _achar(nome):
    for pasta in PASTAS:
        if not pasta or not os.path.isdir(pasta):
            continue
        direto = os.path.join(pasta, nome)
        if os.path.exists(direto):
            return direto
        achados = glob.glob(os.path.join(pasta, "**", nome), recursive=True)
        if achados:
            return sorted(achados)[0]
    return None


def fonte(papel):
    if papel in _cache:
        return _cache[papel]
    for nome in CANDIDATOS[papel]:
        caminho = _achar(nome)
        if caminho:
            tf = skia.Typeface.MakeFromFile(caminho)
            if tf is not None:
                _cache[papel] = tf
                print(f"  fonte {papel}: {caminho}", file=sys.stderr)
                return tf
    raise SystemExit(f"ERRO: nenhuma fonte para o papel '{papel}' (procurei {CANDIDATOS[papel]} em {PASTAS}).")
