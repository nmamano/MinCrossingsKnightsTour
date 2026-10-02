import json,ast
from pathlib import Path
from check import MOVES
from claim12_full import build
from strand_audit import pairing
D=json.loads(Path('w-verifier/claim22_heel.json').read_text());p=D['printed_centre_template'];print('PDF printed heel pairing',pairing(p,'B'))
# Trace the complete 40-column matching, independently of worker code.
def trace(tpl):
 a=[s.split() for s in tpl];W=len(a[0]);H=len(a)
 def adj(p):
  x,y=p;return [(x+MOVES[int(k)][1],y-MOVES[int(k)][0]) for k in a[H-1-y][x%W]]
 result={};covered=set()
 for x in range(-2*W,3*W):
  for y in range(H):
   p=(x,y)
   for q in adj(p):
    lab=q[0]+2*q[1]
    if q[1]<H or not 0<=lab<W:continue
    prev=q;cur=p;seen=set()
    while cur[1]<H:
     assert cur not in seen;seen.add(cur);covered.add((cur[0]%W,cur[1]));ns=adj(cur);assert prev in ns;prev,cur=cur,next(v for v in ns if v!=prev)
    result[lab]=cur[0]+2*cur[1]
 assert len(result)==W and len(covered)==W*H
 return result
raw={}
for st in ast.parse(Path('kt/templates.py').read_text()).body:
 if isinstance(st,ast.Assign) and isinstance(st.targets[0],ast.Name) and st.targets[0].id in ('Sequence1Opt','SequenceP40'):raw[st.targets[0].id]=ast.literal_eval(st.value)
a=trace(raw['SequenceP40']);b=trace([' '.join([row]*5) for row in raw['Sequence1Opt']]);assert a==b;print('P40 complete 40-terminal pairing matches five paper heels')
ALPHA='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_';fold=[]
for n in (96,98,114,120,144,192,198,200):
 d=json.loads(Path(f'w-integrator/corners/FOLD24_base_n{96+(n-96)%24}.json').read_text());g,_,_,sizes=build(d,n);r=json.loads(Path(f'demo/data/FOLD_n{n}.json').read_text())
 for i in range(n):
  for j in range(n):
   v=ALPHA.index(r['cells'][i*n+j]);p=(j,n-1-i);ns={(j+MOVES[k][1],n-1-i-MOVES[k][0]) for k in (v//8,v%8)};assert g[p]==ns
 assert sizes==[n*n];fold.append(n)
print('Demo FOLD equals audited explicit assembler at',fold)
Path('w-verifier/claim22_extra.json').write_text(json.dumps({'printed_pairing':pairing(p if False else D['printed_centre_template'],'B'),'P40_matching':a,'fold_equal_sizes':fold},indent=2))
