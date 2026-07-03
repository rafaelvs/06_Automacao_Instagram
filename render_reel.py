# -*- coding: utf-8 -*-
"""
Motor de craft dos reels narrativos "Pé no Chão" (compartilhado preview/voz).
Craft validado: 30fps, easing com OVERSHOOT na entrada do texto, palavra-chave dourada com
pop de escala, motivo de marca (PEGADAS subindo = primeiros passos) preenchendo o meio,
SAFE ZONE corrigida (rodapé CRM/RQE/disclaimer dentro da área visível; base livre p/ UI do IG),
barra de progresso, fundo com leve parallax.
"""
import os, glob, shutil, subprocess, math
from PIL import Image, ImageDraw, ImageFont

W, H, FPS = 1080, 1920, 30
INK=(18,18,24); CREAM=(243,226,200); GOLD=(176,140,79); TXT_L=(206,198,184); MUT_L=(150,144,132); FAINT=(70,66,60); RED=(196,72,60)

# ── VARIAÇÃO ANTI-TEMPLATIZAÇÃO (política "Inauthentic Content" do YouTube) ──────────────────────────
# Paletas selecionáveis por episódio (episode["palette"]). Default "classico" = cores ORIGINAIS, então
# episódios sem 'palette' (ex.: Instagram/"Pé no Chão") renderizam IDÊNTICOS — mudança 100% aditiva.
PALETTES = {
 "classico":      dict(INK=(18,18,24),  CREAM=(243,226,200), GOLD=(176,140,79), TXT_L=(206,198,184), MUT_L=(150,144,132), FAINT=(70,66,60), RED=(196,72,60)),
 "noturno_azul":  dict(INK=(16,22,34),  CREAM=(232,234,240), GOLD=(214,162,84), TXT_L=(190,198,212), MUT_L=(140,150,168), FAINT=(54,62,80), RED=(210,90,80)),
 "verde_clinico": dict(INK=(18,28,26),  CREAM=(238,236,224), GOLD=(196,156,86), TXT_L=(196,206,198), MUT_L=(140,154,146), FAINT=(58,70,66), RED=(200,84,72)),
 "carvao_quente": dict(INK=(22,20,20),  CREAM=(240,230,214), GOLD=(198,138,86), TXT_L=(208,198,186), MUT_L=(150,142,132), FAINT=(64,60,56), RED=(196,80,64)),
}
def _apply_palette(name):
    g = globals()
    for k, v in PALETTES.get(name or "classico", PALETTES["classico"]).items():
        g[k] = v
FD="/usr/share/fonts/truetype/liberation/"; SB="LiberationSerif-Bold.ttf"; NR="LiberationSans-Regular.ttf"; NB="LiberationSans-Bold.ttf"
M=120
SIG="Dr. Rafael Vargas · CRM-SP 226103 · RQE 137901"
DISC="Conteúdo educativo · não substitui avaliação médica."
SERIE="Pé no Chão"

# ── VARIAÇÃO DE LAYOUT (anti-templatização, camada 2: composição espacial + ritmo tipográfico) ──
# Opt-in por episode["layout"] (espelha episode["palette"]). AUSENTE → "classico" (L0) = código atual
# VERBATIM = byte-idêntico (Instagram "Pé no Chão" e vídeos já renderizados NÃO mudam). "auto" → rotação
# determinística (ganchos_layout). O footer CFM (CRM/RQE + disclaimer) fica SEMPRE fora do dispatch de
# layout e é chamado por último em TODOS os ramos (ver _footer + CLAMP_Y) → presente, legível e na safe
# zone em 100% dos layouts.
CLAMP_Y = 1330   # teto único de qualquer texto de conteúdo (footer começa em fy=1380)
LAYOUTS = {
 "classico":        dict(kind="L0"),
 "editorial_baixo": dict(kind="param", anchor="bottom", base_y=1300, align="L", big=98, small=82,
                         line_h=1.06, kicker=True, header="faixa", motif="wash"),
 "centro_focal":    dict(kind="param", anchor="top", hook_y=812, align="C", big=92, small=78,
                         line_h=1.10, kicker=False, header="minimal", motif="none"),
 "faixa_direita":   dict(kind="param", anchor="top", hook_y=700, align="R", big=92, small=78,
                         line_h=1.06, kicker=False, header="compact_mirror", motif="center"),
 "distico_bicolor": dict(kind="param", anchor="top", hook_y=648, align="L", distico=(60,108),
                         line_h=1.02, kicker=False, header="compact", motif="center"),
 "manchete_regua":  dict(kind="param", anchor="top", hook_y=474, align="L", big=104, small=86,
                         line_h=1.05, kicker=False, header="stacked", motif="none", rule=True),
}
def _resolve_layout(episode):
    name = episode.get("layout")
    if not name:
        name = "classico"
    elif name == "auto":
        import ganchos_layout
        name = ganchos_layout.layout_para(episode["id"])
    return name, LAYOUTS.get(name, LAYOUTS["classico"])
def _clamp_y(y): return min(int(y), CLAMP_Y)
def _hook_x(line, tf, align, dx=0):
    """x0 de UMA linha já montada — centraliza/alinha à direita medindo a largura real (fecha o
    desalinhamento da ênfase dourada em C/R, já que ptxt avança por textlength sem scale)."""
    w = _m.textlength(line, font=tf)
    if align == "C": return int((W - w) / 2)
    if align == "R": return int(W - M - w)
    return int(M + dx)

_FC={}
def F(n,s):
    k=(n,s)
    if k not in _FC: _FC[k]=ImageFont.truetype(FD+n,s)
    return _FC[k]
_m=ImageDraw.Draw(Image.new("RGB",(8,8)))
def eoutc(p): p=0 if p<0 else(1 if p>1 else p); return 1-(1-p)**3
def eback(p):
    p=0 if p<0 else(1 if p>1 else p); c1=1.70158; c3=c1+1; return 1+c3*(p-1)**3+c1*(p-1)**2
def wrap(t,f,mw):
    out=[];cur=""
    for w in t.split():
        s=(cur+" "+w).strip()
        if _m.textlength(s,font=f)<=mw: cur=s
        else:
            if cur: out.append(cur)
            cur=w
    if cur: out.append(cur)
    return out
def trk(d,xy,text,font,fill,tr,left=True):
    x,y=xy
    if not left:
        wt=sum(d.textlength(c,font=font)+tr for c in text)-tr; x=x-wt
    for c in text: d.text((x,y),c,font=font,fill=fill); x+=d.textlength(c,font=font)+tr
def ptxt(base,x,y,text,font,color,alpha,scale=1.0):
    if alpha<=0 or not text: return
    w=int(_m.textlength(text,font=font))+10; h=int(font.size*1.5)+10
    tile=Image.new("RGBA",(max(w,2),max(h,2)),(0,0,0,0)); ImageDraw.Draw(tile).text((5,3),text,font=font,fill=color+(255,))
    if scale!=1.0:
        nw,nh=max(1,int(tile.width*scale)),max(1,int(tile.height*scale)); tile=tile.resize((nw,nh),Image.LANCZOS); x-=(tile.width-w)/2; y-=(tile.height-h)/2
    if alpha<255: tile.putalpha(tile.split()[3].point(lambda v:v*alpha//255))
    base.paste(tile,(int(x-5),int(y-3)),tile)
def _foot(sz,alpha):
    t=Image.new("RGBA",(sz,sz),(0,0,0,0)); d=ImageDraw.Draw(t); c=sz//2; col=GOLD+(alpha,)
    d.ellipse([c-16,int(sz*0.34),c+16,int(sz*0.70)],fill=col); d.ellipse([c-11,int(sz*0.72),c+11,int(sz*0.93)],fill=col)
    for dx in(-15,-6,3,12): d.ellipse([c+dx-4,int(sz*0.26),c+dx+4,int(sz*0.345)],fill=col)
    return t
FPATH=[(M+30,1340,18,-1),(M+170,1300,-10,1),(M+310,1262,16,-1),(W//2,1224,-8,1),
       (W-M-310,1186,16,-1),(W-M-170,1150,-10,1),(W-M-30,1112,14,-1)]
def _feet(img,prog,shift_x=0,shift_y=0,alpha_scale=1.0):
    n=len(FPATH)
    for i,(x,y,ang,side) in enumerate(FPATH):
        a=eoutc((prog-i/(n+1))/0.10)
        if a<=0: continue
        ft=_foot(92,int(60*a*alpha_scale)).rotate(ang+8*side,expand=True,resample=Image.BICUBIC)
        img.paste(ft,(int(x-ft.width/2+side*14+shift_x),int(y-ft.height/2+shift_y)),ft)
def _bone(img,prog,shift_x=0,shift_y=0,alpha_scale=1.0):
    """Motivo da série OSSO NOVO: o osso novo preenchendo o vão (linha que cresce das duas
    pontas pro centro) + uma régua de milímetros por baixo. Identidade INK/CREAM/GOLD.
    shift_x/shift_y deslocam o motivo; alpha_scale (0..1) esmaece (modo 'wash'). Defaults = exato atual."""
    A=alpha_scale
    ov=Image.new("RGBA",(W,H),(0,0,0,0)); d=ImageDraw.Draw(ov)
    y=1230+shift_y; x0,x1=M+30+shift_x,W-M-30+shift_x; cx=(x0+x1)//2; gap=150  # vão central que o osso novo preenche
    a=int(60*A); end=GOLD+(a,)
    # duas pontas de osso (segmentos sólidos), com "cabeças" arredondadas
    d.line([(x0,y),(cx-gap,y)],fill=end,width=10); d.line([(cx+gap,y),(x1,y)],fill=end,width=10)
    for ex in (x0,x1):
        d.ellipse([ex-13,y-16,ex+13,y+16],fill=end)
    # osso novo crescendo das duas pontas pro centro conforme prog
    fill=eoutc(min(1.0,prog/0.85)); half=int(gap*fill)
    nb=GOLD+(int(90*fill*A),)
    if half>0:
        d.line([(cx-gap,y),(cx-gap+half,y)],fill=nb,width=12)
        d.line([(cx+gap,y),(cx+gap-half,y)],fill=nb,width=12)
        # textura de trabéculas (tracinhos diagonais) na zona recém-formada
        for xx in range(cx-gap, cx-gap+half, 18):
            d.line([(xx,y-9),(xx+9,y+9)],fill=GOLD+(int(55*fill*A),),width=2)
        for xx in range(cx+gap, cx+gap-half, -18):
            d.line([(xx,y-9),(xx-9,y+9)],fill=GOLD+(int(55*fill*A),),width=2)
    # régua de milímetros (motivo secundário) logo abaixo
    ry=y+70; d.line([(x0,ry),(x1,ry)],fill=GOLD+(int(34*A),),width=2)
    for i,xx in enumerate(range(x0,x1+1,26)):
        h=14 if i%5==0 else 7
        d.line([(xx,ry),(xx,ry-h)],fill=GOLD+(int(34*A),),width=2)
    img.paste(Image.alpha_composite(img.convert("RGBA"),ov).convert("RGB"),(0,0))
def _bg(drift):
    img=Image.new("RGB",(W,H),INK); ov=Image.new("RGBA",(W,H),(0,0,0,0)); da=ImageDraw.Draw(ov); cy=1720+drift
    for r in(680,580,480,380): da.arc([W//2-r,cy-r,W//2+r,cy+r],204,336,fill=GOLD+(30,),width=2)
    return Image.alpha_composite(img.convert("RGBA"),ov).convert("RGB")
def _no(img,prog,tl):
    a=int(235*eoutc((tl-0.5)/0.6))
    if a<=0: return
    cx,cy,r=W-M-86,470,66; ov=Image.new("RGBA",(W,H),(0,0,0,0)); d=ImageDraw.Draw(ov); col=RED+(a,)
    d.ellipse([cx-r,cy-r,cx+r,cy+r],outline=col,width=13); ang=math.radians(45); dx,dy=math.cos(ang)*r*.74,math.sin(ang)*r*.74
    d.line([(cx-dx,cy+dy),(cx+dx,cy-dy)],fill=col,width=13); img.paste(Image.alpha_composite(img.convert("RGBA"),ov).convert("RGB"),(0,0))
def _header(d,ep,serie=SERIE,style="compact"):
    show_ep = not serie.startswith("Dr.")   # vídeo de apresentação não exibe número de episódio
    if style=="compact":   # ← corpo ORIGINAL verbatim (default; usado por L0 e L4)
        d.text((M,168),"RV",font=F(SB,54),fill=CREAM); wf=d.textlength("RV",font=F(SB,54))
        d.line([(M+wf+22,178),(M+wf+22,222)],fill=GOLD,width=2)
        d.text((M+wf+40,174),"Dr. Rafael Vargas",font=F(NR,25),fill=CREAM); d.text((M+wf+40,206),"Ortopedia · São Paulo",font=F(NR,21),fill=GOLD)
        if show_ep:
            trk(d,(W-M,178),f"EP {ep:02d}",F(NB,30),GOLD,3,left=False)
        trk(d,(M,286),serie.upper(),F(NB,25),GOLD,6); d.line([(M,326),(M+62,326)],fill=GOLD,width=3)
        return
    if style=="faixa":     # régua full-width sob o header (L1)
        d.text((M,168),"RV",font=F(SB,54),fill=CREAM); wf=d.textlength("RV",font=F(SB,54))
        d.line([(M+wf+22,178),(M+wf+22,222)],fill=GOLD,width=2)
        d.text((M+wf+40,174),"Dr. Rafael Vargas",font=F(NR,25),fill=CREAM); d.text((M+wf+40,206),"Ortopedia · São Paulo",font=F(NR,21),fill=GOLD)
        if show_ep: trk(d,(W-M,178),f"EP {ep:02d}",F(NB,30),GOLD,3,left=False)
        trk(d,(M,264),serie.upper(),F(NB,24),GOLD,6)
        d.line([(M,318),(W-M,318)],fill=GOLD,width=2)
        return
    if style=="minimal":   # RV + EP + NOME (centralizado) + kicker da série (L2 pôster). Marca pessoal preservada.
        d.text((M,168),"RV",font=F(SB,54),fill=CREAM)
        if show_ep: trk(d,(W-M,178),f"EP {ep:02d}",F(NB,30),GOLD,3,left=False)
        nm="Dr. Rafael Vargas · Ortopedia · São Paulo"; fn=F(NR,22); nw=_m.textlength(nm,font=fn)
        d.text(((W-nw)/2,214),nm,font=fn,fill=CREAM)
        sk=serie.upper(); fk=F(NB,22); kw=sum(_m.textlength(c,font=fk)+6 for c in sk)-6
        trk(d,((W-kw)/2,258),sk,fk,GOLD,6); cx=W//2; d.line([(cx-30,294),(cx+30,294)],fill=GOLD,width=3)
        return
    if style=="compact_mirror":   # série à DIREITA (espelha hook right-aligned) (L3)
        d.text((M,168),"RV",font=F(SB,54),fill=CREAM); wf=d.textlength("RV",font=F(SB,54))
        d.line([(M+wf+22,178),(M+wf+22,222)],fill=GOLD,width=2)
        d.text((M+wf+40,174),"Dr. Rafael Vargas",font=F(NR,25),fill=CREAM); d.text((M+wf+40,206),"Ortopedia · São Paulo",font=F(NR,21),fill=GOLD)
        if show_ep: trk(d,(W-M,178),f"EP {ep:02d}",F(NB,30),GOLD,3,left=False)
        trk(d,(W-M,286),serie.upper(),F(NB,25),GOLD,6,left=False); d.line([(W-M-62,326),(W-M,326)],fill=GOLD,width=3)
        return
    if style=="stacked":   # masthead vertical (L5 manchete de revista)
        d.text((M,148),"RV",font=F(SB,72),fill=CREAM)
        d.text((M,238),"Dr. Rafael Vargas",font=F(NR,24),fill=CREAM); d.text((M,270),"Ortopedia · São Paulo",font=F(NR,20),fill=GOLD)
        if show_ep: trk(d,(W-M,162),f"EP {ep:02d}",F(NB,30),GOLD,3,left=False)
        trk(d,(W-M,238),serie.upper(),F(NB,22),GOLD,5,left=False)
        return
    _header(d,ep,serie,style="compact")   # fallback defensivo
def _footer(d,prog):
    fy=1380; d.line([(M,fy),(W-M,fy)],fill=FAINT,width=2)
    d.text((M,fy+22),"@rafaelvargasmd",font=F(NR,26),fill=MUT_L); d.text((M,fy+62),SIG,font=F(NR,21),fill=MUT_L); d.text((M,fy+94),DISC,font=F(NR,20),fill=MUT_L)
    by=fy-14; pw=int(prog*(W-2*M)); d.line([(M,by),(W-M,by)],fill=FAINT,width=4); d.line([(M,by),(M+pw,by)],fill=GOLD,width=4)

def _draw_L0(img, d, s, tl):
    """L0 'classico' — miolo de conteúdo ORIGINAL verbatim. NÃO alterar (congelamento byte-idêntico)."""
    BIG=F(SB,98); SUB=F(NR,40); T82=F(SB,82)
    trk(d,(M,560),s["k"].upper(),F(NB,28),GOLD,5); d.line([(M,602),(M+56,602)],fill=GOLD,width=3)
    ln=s["sc"]; emph=s.get("e"); tf=BIG
    if any(_m.textlength(x,font=tf)>W-2*M for x in ln): tf=T82
    ty=680
    for li,L in enumerate(ln):
        pr=(tl-0.08-0.16*li)/0.6; yo=(1-eback(pr))*-46; a=int(255*eoutc((tl-0.08-0.16*li)/0.4))
        if emph and emph in L:
            pre,_,post=L.partition(emph); x=M
            if pre: ptxt(img,x,ty+yo,pre,tf,CREAM,a); x+=_m.textlength(pre,font=tf)
            sc=1.0+0.06*(1-eoutc((tl-0.08-0.16*li)/0.5)); ptxt(img,x,ty+yo,emph,tf,GOLD,a,scale=sc); x+=_m.textlength(emph,font=tf)
            if post: ptxt(img,x,ty+yo,post,tf,CREAM,a)
        else: ptxt(img,M,ty+yo,L,tf,CREAM,a)
        ty+=int(tf.size*1.06)
    if s.get("sub"):
        sy=ty+40; pa=int(255*eoutc((tl-0.5)/0.5))
        for sl in wrap(s["sub"],SUB,W-2*M): ptxt(img,M,sy,sl,SUB,TXT_L,pa); sy+=56
    if s.get("cta"):
        pc=eoutc((tl-0.9)/0.6); ptxt(img,M,1330,"Compartilhar = enviar no direct",F(NB,46),GOLD,int(220*pc))

def _dispatch_motif(img, motif_fam, prog, LP):
    """Motivo (feet/bone) por modo de layout. 'none' pula; 'wash' esmaece; 'center' aceita shift_x."""
    mode=LP.get("motif","center")
    if mode=="none": return
    fn=_bone if motif_fam=="bone" else _feet
    if mode=="wash":
        fn(img,prog,shift_y=-600,alpha_scale=0.30)  # sobe bem p/ o vão vazio do topo + bem faint (não colide c/ o conteúdo bottom-anchored)
    else:
        sx=max(-30,min(30,LP.get("motif_shift_x",0)))  # clamp defensivo: motivo nunca vaza a moldura (x0=M+30+sx fica ≥ M)
        fn(img,prog,shift_x=sx)

def _draw_content(img, d, s, tl, LP):
    """Miolo de conteúdo dos layouts paramétricos (L1-L5): kicker + hook + sub + [régua] + cta.
    TODO y de conteúdo passa por _clamp_y (teto CLAMP_Y=1330) → nunca invade o footer, que é
    desenhado DEPOIS e FORA daqui. A lógica de ênfase dourada (pop de escala) é escrita UMA vez aqui."""
    align=LP["align"]; line_h=LP["line_h"]; distico=LP.get("distico")
    ln=s["sc"]; emph=s.get("e"); no_present = s.get("motif")=="no"
    mw = W-2*M
    if no_present and LP.get("anchor")=="top" and LP.get("hook_y",9999) < 560:
        mw = W-2*M-170   # estreita p/ não colidir com o círculo _no (topo-direita)
    # ── seleção de fontes/cores por linha (uma vez) ──
    if distico and len(ln)>=2:   # contraste de escala inter-linha (só faz sentido com 2+ linhas)
        s0,s1=distico; fonts=[]
        for i,L in enumerate(ln):
            sz = s0 if i==0 else s1; f=F(SB,sz)
            while _m.textlength(L,font=f)>mw and sz>50: sz-=6; f=F(SB,sz)
            fonts.append(f)
        cols=[MUT_L if i==0 else CREAM for i in range(len(ln))]
    else:
        big=LP.get("big", distico[1] if distico else 98); small=LP.get("small", distico[0] if distico else 82)
        tf=F(SB,big)
        if any(_m.textlength(x,font=tf)>mw for x in ln): tf=F(SB,small)
        if any(_m.textlength(x,font=tf)>mw for x in ln): tf=F(SB,70)
        fonts=[tf]*len(ln); cols=[CREAM]*len(ln)
    steps=[int(fonts[i].size*line_h) for i in range(len(ln))]; block_h=sum(steps)
    # ── âncora vertical ──
    if LP.get("anchor")=="bottom":
        # ancora a BASE de todo o conteúdo (hook + sub) em base_y → o sub cabe acima do footer
        sub_lines = wrap(s["sub"], F(NR,40), mw) if s.get("sub") else []
        sub_h = (40 + len(sub_lines)*56) if sub_lines else 0
        top_y = max(384, LP["base_y"] - block_h - sub_h)
    else:
        top_y = LP["hook_y"]
    # ── rótulo/kicker acima do hook, alinhado ──
    k=s["k"].upper(); fk=F(NB,24 if distico else 26); ky=max(352, top_y-52)
    if align=="C":
        kw=sum(_m.textlength(c,font=fk)+5 for c in k)-5; trk(d,((W-kw)/2,ky),k,fk,GOLD,5)
        cx=W//2; d.line([(cx-28,ky+40),(cx+28,ky+40)],fill=GOLD,width=3)
    elif align=="R":
        trk(d,(W-M,ky),k,fk,GOLD,5,left=False); d.line([(W-M-56,ky+40),(W-M,ky+40)],fill=GOLD,width=3)
    else:
        trk(d,(M,ky),k,fk,GOLD,5); d.line([(M,ky+40),(M+56,ky+40)],fill=GOLD,width=3)
    # ── hook (linhas animadas, ênfase dourada com pop) ──
    ty=top_y
    for li,L in enumerate(ln):
        tf=fonts[li]; base=cols[li]
        pr=(tl-0.08-0.16*li)/0.6; yo=(1-eback(pr))*-46; a=int(255*eoutc((tl-0.08-0.16*li)/0.4))
        x0=_hook_x(L,tf,align)
        if emph and emph in L:
            pre,_,post=L.partition(emph); x=x0
            if pre: ptxt(img,x,ty+yo,pre,tf,base,a); x+=_m.textlength(pre,font=tf)
            sc=1.0+0.06*(1-eoutc((tl-0.08-0.16*li)/0.5)); ptxt(img,x,ty+yo,emph,tf,GOLD,a,scale=sc); x+=_m.textlength(emph,font=tf)
            if post: ptxt(img,x,ty+yo,post,tf,base,a)
        else: ptxt(img,x0,ty+yo,L,tf,base,a)
        ty+=steps[li]
    hook_bottom=ty
    # ── régua opcional (L5) + subtítulo ──
    sy=_clamp_y(hook_bottom+40)
    if LP.get("rule"):
        ry=_clamp_y(hook_bottom+26); d.line([(M,ry),(W-M,ry)],fill=GOLD,width=3); sy=_clamp_y(ry+36)
    if s.get("sub"):
        SUB=F(NR,40); pa=int(255*eoutc((tl-0.5)/0.5))
        for sl in wrap(s["sub"],SUB,mw):
            if sy+50>1360: break   # reserva a altura do glifo do sub → base nunca encosta no footer (fy=1380)
            ptxt(img,_hook_x(sl,SUB,align),sy,sl,SUB,TXT_L,pa); sy+=56
    # ── cta (ancorado ACIMA do footer: base do glifo < 1360, contando a própria altura) ──
    if s.get("cta"):
        pc=eoutc((tl-0.9)/0.6); ct="Compartilhar = enviar no direct"; cf=F(NB,46)
        cy=min(sy, 1360-int(cf.size*1.5))
        ptxt(img,_hook_x(ct,cf,align),cy,ct,cf,GOLD,int(220*pc))

def render_frames(episode, durs, frames_dir):
    """Renderiza os JPGs do episódio. durs = lista de durações (s) por cena."""
    _apply_palette(episode.get("palette"))   # variação por episódio (default = cores originais)
    shutil.rmtree(frames_dir,ignore_errors=True); os.makedirs(frames_dir)
    S=episode["scenes"]; ep=episode["ep"]
    serie=episode.get("serie",SERIE); motif_fam=episode.get("motif_family","feet")
    bnd=[]; acc=0.0
    for i,dch in enumerate(durs): bnd.append((acc,acc+dch,i)); acc+=dch
    total=acc; nf=int(total*FPS)
    lay_name, LP = _resolve_layout(episode)        # variação de composição por episódio
    hdr_style = LP.get("header","compact"); is_L0 = LP.get("kind")=="L0"
    for f in range(nf):
        t=f/FPS; cur=bnd[-1]
        for b in bnd:
            if b[0]<=t<b[1]: cur=b; break
        t0,t1,idx=cur; tl=t-t0; s=S[idx]; drift=int(8*math.sin(t*0.5))
        img=_bg(drift)
        # ── MOTIVO: L0 = comportamento exato atual; demais layouts despacham por motif_mode ──
        if is_L0:
            if motif_fam=="bone": _bone(img,t/total)
            else: _feet(img,t/total)
        else:
            _dispatch_motif(img, motif_fam, t/total, LP)
        d=ImageDraw.Draw(img)
        if s.get("motif")=="no": _no(img,t/total,tl); d=ImageDraw.Draw(img)   # SEMPRE (independe do motif_mode)
        _header(d,ep,serie,style=hdr_style)
        # ── CONTEÚDO: dispatch por layout (L0 = miolo verbatim; L1-L5 = paramétrico clampado) ──
        if is_L0: _draw_L0(img,d,s,tl)
        else:     _draw_content(img,d,s,tl,LP)
        _footer(d,t/total)                          # ← IMUTÁVEL, por último, em TODOS os ramos (CFM)
        img.save(f"{frames_dir}/f{f:05d}.jpg","JPEG",quality=92)
    return total, nf

def encode(frames_dir, audio_args, out_mp4):
    cmd=["ffmpeg","-y","-framerate",str(FPS),"-i",f"{frames_dir}/f%05d.jpg"]+audio_args+[
        "-c:v","libx264","-pix_fmt","yuv420p","-profile:v","high","-r","30","-c:a","aac","-b:a","192k",
        "-shortest","-movflags","+faststart",out_mp4]
    subprocess.run(cmd,check=True,capture_output=True)
