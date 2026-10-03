"""Count bad quarters in one (6,6) period of each FOLD corridor."""
import json
from pathlib import Path
from collections import Counter
from claim38_switch import edge,qs
D=json.loads(Path('w-integrator/corners/FOLD24_base_n96.json').read_text())
out=[]
for r in range(4):
 es=set()
 for x in range(-12,25):
  for y in range(-20,35):
   delta=y-x
   moves=D['template'][f'{r}:{(x-8)%6},{delta}'] if 0<=delta<=2 else ((2,1),(-2,-1)) if delta>2 else ((1,2),(-1,-2))
   for dx,dy in moves:
    b=(x+dx,y+dy)
    if not 0<=delta<=2 and 0<=b[1]-b[0]<=2:continue
    es.add(edge((x,y),b))
 cov=Counter(q for e in es for q in qs(e))
 bad=[(x,y,k) for x in range(6) for y in range(x-8,x+11) for k in range(4) if cov[x,y,k]!=1]
 assert len(bad)==16
 out.append(dict(frame=r,bad_per_period=len(bad),bad=bad))
Path('gap/verifier/claim38_corridor_bq.json').write_text(json.dumps(out,indent=2))
print('All four corridors have 16 bad quarters per (6,6) period.')
