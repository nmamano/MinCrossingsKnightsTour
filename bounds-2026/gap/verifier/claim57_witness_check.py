"""Exact independent primal corner witness check; no optimizer imports."""
from pathlib import Path
import json
from claim57_corner_exact import MOVES,L
R=Path('gap/verifier/claim57_run');slots=[tuple(map(int,l.split())) for l in (R/'source_z6_slots.txt').read_text().splitlines()];out=[]
for A,scale,target in [(10,6,-37),(14,3,-18),(20,3,-18)]:
 d=json.loads((R/f'corner_A{A}_witness.json').read_text());assert d['A']==A and d['scale']==scale
 ch={tuple(p):(tuple(a),tuple(b)) for p,a,b in d['choices']}
 expected={(x,y) for x in range(A) for y in range(A) if min(x,y)<6}
 assert len(d['choices'])==len(ch)==len(expected) and set(ch)==expected
 raw=list(map(int,(R/f'source_cert_A{10 if A==10 else 14}_w.txt').read_text().split()));assert raw[0]==scale;weights=dict(zip(slots,raw[1:]))
 cost=0
 for p,(a,b) in ch.items():
  assert a in MOVES and b in MOVES and a!=b
  for dx,dy in [a,b]:
   q=(p[0]+dx,p[1]+dy);assert min(q)>=0
   if q in ch:assert (-dx,-dy) in ch[q]
  cost+=int((a[0]+b[0],a[1]+b[1])!=(0,0))-L(p[0],[a[0],b[0]])-L(p[1],[a[1],b[1]])
 hv=hh=0
 for (x,y,X,Y),w in weights.items():
  hv+=w*((X-x,Y-y) in ch[x,A+y])
  hh+=weights[X,-1-Y,x,-1-y]*((Y-y,X-x) in ch[A+y,x])
 reduced=scale*cost-hv+hh;assert reduced==target
 out.append(dict(A=A,scale=scale,cells=len(ch),raw_cost=cost,h_vertical=hv,h_mirrored_horizontal=hh,scaled_reduced_cost=reduced))
print(json.dumps(out,indent=2));(R/'witness_checks.json').write_text(json.dumps(out,indent=2)+'\n')
