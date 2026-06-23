# -*- coding: utf-8 -*-
"""Auditoria de saude do motor (nao-destrutiva, so leitura). Gera relatorio no stdout."""
import os, json, ast, glob, re

ROOT = os.path.dirname(os.path.abspath(__file__))
def J(p):
    try:
        with open(os.path.join(ROOT,p), encoding="utf-8") as f: return json.load(f)
    except Exception as e: return None

def exists(rel): return os.path.isfile(os.path.join(ROOT, rel))

print("="*70); print("1) RUNWAY (quanto falta publicar antes de reabastecer)"); print("="*70)
state = J("state/published.json") or {"published":[]}
done = {e["id"] for e in state.get("published",[])}
libs = {"posts":"posts.json","reels":"reels.json","sequences":"sequences.json","stories":"stories.json"}
for name,fn in libs.items():
    d = J(fn) or []
    ids = [x.get("id") for x in d]
    pub = sum(1 for x in d if x.get("id") in done)
    rem = len(d)-pub
    dups = len(ids)-len(set(ids))
    print(f"  {name:10} total={len(d):4}  publicados={pub:4}  restam={rem:4}  ids_duplicados={dups}")
print(f"  (state.published registros={len(state.get('published',[]))})")

print(); print("="*70); print("2) REFERENCIAS DE MIDIA QUEBRADAS (item aponta p/ arquivo inexistente)"); print("="*70)
def check(lib, field, multi):
    d = J(lib) or []; broken=[]
    for it in d:
        paths = it.get(field) if multi else ([it.get(field)] if it.get(field) else [])
        for p in (paths or []):
            if p and not exists(p): broken.append((it.get("id"), p))
    return d, broken
total_broken=0
for lib,field,multi in [("posts.json","images",True),("reels.json","video",False),
                        ("sequences.json","images",True),("stories.json","image",False),
                        ("destaques.json","image",False)]:
    d,broken = check(lib,field,multi)
    total_broken += len(broken)
    flag = "OK" if not broken else f"** {len(broken)} QUEBRADAS **"
    print(f"  {lib:18} itens={len(d):4}  {flag}")
    for i,(iid,p) in enumerate(broken[:8]): print(f"      - {iid}: {p}")
    if len(broken)>8: print(f"      ... +{len(broken)-8}")
print(f"  TOTAL refs quebradas: {total_broken}")

print(); print("="*70); print("3) INVENTARIO DE SCRIPTS (.py) — docstring + imports internos"); print("="*70)
pys = sorted(glob.glob(os.path.join(ROOT,"*.py")) + glob.glob(os.path.join(ROOT,"voz","*.py")))
local_mods = {os.path.splitext(os.path.basename(p))[0] for p in pys}
for p in pys:
    rel = os.path.relpath(p, ROOT)
    if os.path.basename(p).startswith("_auditoria"): continue
    src = open(p,encoding="utf-8").read()
    try:
        tree = ast.parse(src); doc = (ast.get_docstring(tree) or "").strip().split("\n")[0][:90]
    except Exception: doc=""
    imps=set()
    for m in re.finditer(r'^\s*(?:from|import)\s+([a-zA-Z0-9_]+)', src, re.M):
        if m.group(1) in local_mods: imps.add(m.group(1))
    print(f"  {rel:32} <- {doc}")
    if imps: print(f"      usa: {', '.join(sorted(imps))}")

print(); print("="*70); print("4) WORKFLOWS -> script que disparam"); print("="*70)
for wf in sorted(glob.glob(os.path.join(ROOT,".github","workflows","*.yml"))):
    src=open(wf,encoding="utf-8").read()
    runs = re.findall(r'python\s+([A-Za-z0-9_./]+\.py)', src)
    name = os.path.basename(wf)
    cron = re.findall(r'cron:\s*[\'"]([^\'"]+)', src)
    disp = "workflow_dispatch" in src
    trg = ("cron="+",".join(cron) if cron else "") + (" +manual" if disp else "")
    miss = [r for r in set(runs) if not exists(r)]
    print(f"  {name:30} -> {', '.join(sorted(set(runs))) or '(sem python direto)'}  [{trg.strip()}]")
    if miss: print(f"      ** referencia script inexistente: {miss}")

print(); print("="*70); print("5) ARQUIVOS DE MIDIA orfaos vs referenciados (amostra)"); print("="*70)
ref_imgs=set()
for lib,field,multi in [("posts.json","images",True),("sequences.json","images",True),
                        ("stories.json","image",False),("destaques.json","image",False)]:
    for it in (J(lib) or []):
        ps = it.get(field) if multi else [it.get(field)]
        for p in (ps or []):
            if p: ref_imgs.add(p.replace("\\","/"))
all_imgs = {os.path.relpath(p,ROOT).replace("\\","/") for p in glob.glob(os.path.join(ROOT,"images","*.jpg"))}
orf = sorted(all_imgs - ref_imgs)
print(f"  images/*.jpg no disco={len(all_imgs)}  referenciadas={len(all_imgs & ref_imgs)}  orfas={len(orf)}")
ref_vids=set(it.get("video","") for it in (J("reels.json") or []))
all_vids={os.path.relpath(p,ROOT).replace("\\","/") for p in glob.glob(os.path.join(ROOT,"reels","*.mp4"))}
print(f"  reels/*.mp4 no disco={len(all_vids)}  referenciados(em reels.json)={len(all_vids & ref_vids)}")
print(f"  (mp4 com prefixo _ = previews fora do publish: {sum(1 for v in all_vids if os.path.basename(v).startswith('_'))})")
print("\nFIM.")
