# -*- coding: utf-8 -*-
"""Stories SERIALIZADOS (temporada semanal + lente diaria). Piloto: Semana do Joelho, Dia 1."""
import os, json
from PIL import Image, ImageDraw
from gerar_conteudo import F, wrap, trk, arcs, INK, PAPER, CREAM, GOLD, TXT_L, TXT_D, MUT_L, MUT_D, SB, NR, NB, IMG, ROOT, SIG

DISC = "Conteúdo educativo · não substitui avaliação médica."

def seq_story(fn, v, theme, idx, n, segment, title, sub, cue):
    W, H = 1080, 1920; M = 130
    img = Image.new("RGBA", (W, H), (INK if v == "dark" else PAPER) + (255,))
    img = arcs(img, v, W, H); d = ImageDraw.Draw(img)
    tcol = CREAM if v == "dark" else INK
    scol = TXT_L if v == "dark" else TXT_D
    mcol = MUT_L if v == "dark" else MUT_D
    faint = (90, 86, 80) if v == "dark" else (214, 208, 196)
    d.text((M, 150), "RV", font=F(SB, 60), fill=tcol); wf = d.textlength("RV", font=F(SB, 60))
    d.line([(M+wf+24, 162), (M+wf+24, 212)], fill=GOLD, width=2)
    d.text((M+wf+44, 160), "Dr. Rafael Vargas", font=F(NR, 26), fill=tcol)
    d.text((M+wf+44, 194), "Ortopedia · São Paulo", font=F(NR, 22), fill=GOLD)
    trk(d, (W-M, 168), f"{idx}/{n}", F(NB, 34), GOLD, 4, left=False)
    trk(d, (M, 300), theme.upper(), F(NB, 26), GOLD, 5)
    by = 350; bx0 = M; bx1 = W-M; gap = 12; segw = (bx1-bx0-(n-1)*gap)/n
    for i in range(n):
        x = bx0 + i*(segw+gap)
        d.rounded_rectangle([x, by, x+segw, by+10], radius=5, fill=(GOLD if i < idx else faint))
    ky = 640; trk(d, (M, ky), segment.upper(), F(NB, 30), GOLD, 6); d.line([(M, ky+50), (M+70, ky+50)], fill=GOLD, width=3)
    ty = ky+98; tf = F(SB, 88); tl = wrap(d, title, tf, W-2*M)
    if len(tl) > 3: tf = F(SB, 70); tl = wrap(d, title, tf, W-2*M)
    for ln in tl: d.text((M, ty), ln, font=tf, fill=tcol); ty += int(tf.size*1.1)
    by2 = ty+46
    for ln in wrap(d, sub, F(NR, 40), W-2*M): d.text((M, by2), ln, font=F(NR, 40), fill=scol); by2 += 58
    cy = H-360
    for ln in wrap(d, cue, F(NB, 34), W-2*M): d.text((M, cy), ln, font=F(NB, 34), fill=GOLD); cy += 46
    d.text((M, H-210), "@rafaelvargasmd", font=F(NR, 30), fill=mcol)
    d.text((M, H-162), SIG, font=F(NR, 23), fill=mcol)
    d.text((M, H-120), DISC, font=F(NR, 22), fill=mcol)
    img.save(os.path.join(IMG, fn), "JPEG", quality=92)

THEME = "Semana do Joelho"
DIA1 = [
 ("dark", "SEG · O que observar", "Joelho da criança: 4 sinais que pedem avaliação",
  "E um que assusta os pais, mas sozinho costuma ser normal. Vem comigo nos próximos cards.", "deslize →"),
 ("dark", "Sinais 1 e 2", "Incha ou trava",
  "Joelho que incha depois do esforço, ou que “trava” e não estende direito, merece avaliação — não é só pancada boba.", "continua →"),
 ("dark", "Sinais 3 e 4", "Dói à noite ou faz mancar",
  "Dor que acorda a criança, sempre no mesmo ponto, ou que faz mancar por mais de um ou dois dias: vale avaliar.", "continua →"),
 ("dark", "O que costuma ser normal", "O estalo sem dor",
  "Joelho que estala ao agachar, sem dor, inchaço ou falseio, quase sempre não preocupa. O que muda tudo é vir com dor.", "quase lá →"),
 ("dark", "Guarde isso", "Na dúvida, observe e avalie",
  "Salve para lembrar dos sinais e mande para um pai ou mãe. Avaliar cedo costuma simplificar tudo.", "Amanhã: perna em X ou arqueada — é só fase do crescimento? Fale comigo no WhatsApp da bio. →"),
]

def render_dia(prefix, theme, dia):
    n = len(dia); out = []
    for i, (v, seg, title, sub, cue) in enumerate(dia, 1):
        fn = f"{prefix}_{i}.jpg"; seq_story(fn, v, theme, i, n, seg, title, sub, cue)
        out.append("images/"+fn); print("ok", fn, flush=True)
    return out

if __name__ == "__main__":
    render_dia("seq_joelho_seg", THEME, DIA1)
    print("Dia 1 OK")
