# -*- coding: utf-8 -*-
"""Geração nova de reels (18/10/2026): animação sem rosto comandada pelo tempo das palavras.

Por que existe: o Rafael disse, com os números a favor dele, que os reels tinham virado
"murais informativos levemente cansativos" — lâminas de texto lidas em voz alta, 36 peças em
30 dias e ZERO envios. Depois de ver dois pilotos, aprovou ("pode seguir com tudo") dois
formatos novos:

  * CONVERSA       (`conversa.py`)        — "Se o seu ___ pudesse responder": o paciente reclama,
                                            o objeto responde em 1ª pessoa com o cuidado certo.
                                            Totalmente guiado por dados: cada episódio é um dict.
  * COMO FUNCIONA  (`cf_<tema>.py`)       — o mecanismo animado (o que acontece dentro do corpo).
                                            Cada tema tem a sua cena desenhada à mão.

Peças comuns: `voz.py` (edge-tts com WordBoundary — o tempo de cada palavra comanda legenda e
animação), `som.py` (trilha e efeitos sintetizados, sem licença de terceiro), `fontes.py`
(Segoe no Windows, Roboto no runner Linux). Entrada única: `python -m animado.render <id>`.
Episódios: `episodios_entretenimento.py` (lido também pelo portão de aprovação).
"""
