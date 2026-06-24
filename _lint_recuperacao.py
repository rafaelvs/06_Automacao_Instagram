# -*- coding: utf-8 -*-
"""
Linter da série "Recuperação" (vídeos pós-op p/ paciente) — valida cada episódio contra as
convenções aprendidas nos vídeos ① gesso e ② fixador, ANTES de renderizar. Escala com segurança.

Roda: python _lint_recuperacao.py            (valida toda a série)
      python _lint_recuperacao.py <id>       (valida um episódio)
Sai com código 1 se houver ERRO (bloqueia); avisos (WARN) não bloqueiam.

Regras (codificadas dos aprendizados — ver GUIA_PRODUCAO_RECUPERACAO.md):
 R1 serie == "Recuperação".
 R2 6–9 cenas; cada cena: sc=lista de 1–2 linhas; vo não-vazio; ênfase (e) None ou substring de sc.
 R3 ALARME→PS: ao menos uma cena cita "pronto-socorro" (regra de segurança da série).
 R4 CAPTION com bloco CFM: "CRM", "RQE" e "não substitui" (disclaimer educativo).
 R5 ROTINA: caption ou alguma cena cita o canal de dúvida de rotina (WhatsApp).
 R6 PAR adulto+infantil: todo id base tem irmã "<id>_kids" (e vice-versa).
 R7 TERMOS A REVISAR (CFM / clínicos) → WARN: garante/garantia/cura, estética/altura (tabu do
    alongamento), "gelo" sobre gesso, promessas. Não bloqueia, mas sinaliza p/ revisão humana.
"""
import sys, re
import episodios_pe_no_chao as E

SERIE = "Recuperação"
# termos sensíveis (CFM/clínico). "altura do coração/peito" é elevação legítima -> não é tabu;
# o tabu do alongamento é altura/estatura ESTÉTICA (ficar mais alto, ganhar cm).
REVISAR = ["garant", "cura ", " cura.", "estétic", "estatura", "mais alto", "ficar alto",
           "ganhar altura", "aumentar a altura", "milagr", "melhor médico", "sem dor"]
GELO = re.compile(r"\bgelo\b", re.I)

def episodes():
    return [ep for ep in E.EPISODES if ep.get("serie") == SERIE]

def lint_one(ep):
    errs, warns = [], []
    eid = ep.get("id", "?")
    # R1
    if ep.get("serie") != SERIE: errs.append("R1 serie != Recuperação")
    # R2
    sc_n = len(ep.get("scenes", []))
    if not (6 <= sc_n <= 9): warns.append(f"R2 {sc_n} cenas (ideal 8)")
    texto_total = ""
    for i, s in enumerate(ep.get("scenes", []), 1):
        sc = s.get("sc")
        if not isinstance(sc, list) or not (1 <= len(sc) <= 2): errs.append(f"R2 cena{i}: sc deve ser 1–2 linhas")
        e = s.get("e")
        if e is not None and not any(e in L for L in (sc or [])): errs.append(f"R2 cena{i}: ênfase {e!r} não está em sc {sc}")
        vo = (s.get("vo") or "").strip()
        if not vo: errs.append(f"R2 cena{i}: vo vazio")
        texto_total += " " + vo + " " + (s.get("sub") or "")
    # R3
    if "pronto-socorro" not in texto_total.lower() and " ps " not in texto_total.lower():
        errs.append("R3 nenhuma cena cita 'pronto-socorro' (regra de alarme da série)")
    # R4
    cap = (ep.get("caption") or "")
    for token in ("CRM", "RQE", "não substitui"):
        if token not in cap: errs.append(f"R4 caption sem '{token}'")
    # R5
    if "whatsapp" not in (cap + texto_total).lower(): warns.append("R5 sem canal de dúvida de rotina (WhatsApp)")
    # R7
    blob = (texto_total + " " + cap).lower()
    for t in REVISAR:
        if t in blob: warns.append(f"R7 termo a revisar: {t!r}")
    if GELO.search(blob): warns.append("R7 menção a 'gelo' — conferir (não usar gelo sobre o gesso)")
    return errs, warns

def main():
    eps = episodes()
    if len(sys.argv) > 1:
        eps = [E.get(sys.argv[1])]
    ids = {ep["id"] for ep in E.EPISODES}
    total_err = 0
    print(f"== Linter série '{SERIE}' — {len(eps)} episódio(s) ==")
    for ep in eps:
        errs, warns = lint_one(ep)
        # R6 pareamento
        eid = ep["id"]
        if eid.endswith("_kids"):
            base = eid[:-5]
            if base not in ids: errs.append(f"R6 irmã sem o adulto '{base}'")
        else:
            if (eid + "_kids") not in ids: warns.append(f"R6 sem irmã infantil '{eid}_kids'")
        status = "OK" if not errs else f"** {len(errs)} ERRO(S) **"
        print(f"\n[{eid}] {status}" + (f"  ({len(warns)} avisos)" if warns else ""))
        for e in errs: print("   ERRO:", e)
        for w in warns: print("   warn:", w)
        total_err += len(errs)
    print(f"\n== Total de ERROS: {total_err} ==")
    sys.exit(1 if total_err else 0)

if __name__ == "__main__":
    main()
