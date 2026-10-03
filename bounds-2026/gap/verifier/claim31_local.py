"""Independent R3 budget, exact algebra, and critical-field checks."""
import json,re
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
from itertools import combinations,product
from claim26_certificate import edge,cross,TERMS,EXC
out={'date':'2026-10-03'}
verts=list(product(range(6),repeat=2))
es=[edge(a,b) for a,b in combinations(verts,2) if sorted((abs(a[0]-b[0]),abs(a[1]-b[1])))==[1,2]]
assert len(es)==80
pairs={tuple(sorted((a[0],b[0]))) for a,b in es if a[0] in (0,1,3) or b[0] in (0,1,3)}
assert pairs=={(0,1),(0,2),(1,2),(1,3),(2,3),(3,4),(3,5)}
overcount=4*(80*79//2);assert overcount==12640
C=F(104,4);R5=overcount-2+8*C
assert R5==12846
constant=F(156+R5,5)+2
assert constant==F(13012,5) and constant<=2603
out['theorem']={'coefficient':'24/5','constant':str(constant),'rounded':2603,'even_n_at_least':32,'overcount':overcount}
fields={}
for orient in ('up','down'):
 log=Path(f'gap/searcher/lower/joint_{orient}.log').read_text()
 segment=log.rsplit('  cycle:',1)[1].split(' try beta')[0]
 rows=int(re.search(r'\d+ arcs, (\d+) rows',segment).group(1))
 template=[]
 for line in segment.splitlines():
  if 'row ' not in line or ' x ' not in line:continue
  for x,y,X,Y in re.findall(r'\((-?\d+),(-?\d+)\)-\((-?\d+),(-?\d+)\)',line):
   template.append(edge((int(x),int(y)),(int(X),int(Y))))
 E={edge((a[0],a[1]+k*rows),(b[0],b[1]+k*rows)) for a,b in template for k in range(-12,13)}
 deg=Counter(v for e in E for v in e)
 assert all(deg[x,y]==2 if x in (0,1,3) else deg[x,y]<=2 for x in range(6) for y in range(-8*rows,8*rows))
 assert all(tuple(sorted((a[0],b[0]))) in pairs for a,b in E)
 S={e for e in E if min(p[0] for p in e)<2}
 par={}
 def find(a):
  while a in par:a=par[a]
  return a
 for a,b in S:
  a,b=find(a),find(b);assert a!=b;par[a]=b
 hits=[(e,f) for e,f in combinations(E,2) if cross(e,f) and 0<=max(min(p[1] for p in e),min(p[1] for p in f))<rows]
 W=sum(e in S and f in S for e,f in hits)
 B=sum(any(x==0 for x,y in e) and any(x==0 for x,y in f) for e,f in hits)
 WX=len(hits)-W;penalties=[]
 sign=1 if orient=='up' else -1
 for phase in (0,1):
  t=0
  for y in range(rows):
   tr=lambda p:(p[0],y+sign*p[1])
   f=sum(c for a,b,c in TERMS if edge(tr(a),tr(b)) in E)
   exception=all(edge(tr(a),tr(b)) in E for a,b in EXC)
   c=1-2*((y+phase)%2);h=((1+c)//2+c*(f+2))%3
   t+=2 if exception else (1,2,0)[h]
  penalties.append(F(t,2))
 ratio=F(len(hits)-rows,1)/(max(penalties)-(B-rows))
 assert ratio==2
 fields[orient]={'period':rows,'Y':len(hits),'S_crossings':W,'boundary_pairs':B,'mixed_or_J_crossings':WX,'penalties':list(map(str,penalties)),'beta_limit':str(ratio),'template':template}
out['critical_fields']=fields
out['status']='PASS'
Path('gap/verifier/claim31_local.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
