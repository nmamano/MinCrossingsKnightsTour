"""Independent evidence checks for the blog addendum."""
from pathlib import Path
from collections import Counter
import json,hashlib
W={}
for s in Path('w-turnstheory/corner_witness.txt').read_text().splitlines():
 if not s or s.startswith('#'):continue
 x,y,a,b,c,d=map(int,s.split());W[x,y]=((a,b),(c,d))
def lower(i,vals):
 return 1 if i==0 else sum(v in (0,3) for v in vals)-1 if i in (1,2) else 1-sum(v in (1,2) for v in vals)
r=0;adj={};edges=set()
for (x,y),ds in W.items():
 assert len(set(ds))==2 and all(sorted(map(abs,d))==[1,2] for d in ds)
 ns=[(x+a,y+b) for a,b in ds];assert all(min(q)>=0 for q in ns)
 r+=int(tuple(sum(z) for z in zip(*ds))!=(0,0))-lower(x,[q[0] for q in ns])-lower(y,[q[1] for q in ns])
 adj[x,y]=[q for q in ns if q in W]
 for q in ns:
  edges.add(tuple(sorted(((x,y),q))))
  if q in W:assert (x-q[0],y-q[1]) in W[q]
seen=set();sizes=[]
for p in W:
 if p in seen:continue
 todo=[p];comp=set()
 while todo:
  q=todo.pop()
  if q in comp:continue
  comp.add(q);todo.extend(adj[q])
 assert sum(len(adj[q]) for q in comp)//2==len(comp)-1
 seen|=comp;sizes.append(len(comp))
assert len(W)==16 and r==-7
old=json.loads(Path('w-verifier/tt16_results.json').read_text());sizes_old=[v['n'] for v in old['rebuilt']]
assert sizes_old==list(range(48,136,2))+[312,314,316,318]
assert all(v['T']==8*v['n']-14 for v in old['rebuilt'])
for v in old['corners']:assert hashlib.sha256(Path(v['file']).read_bytes()).hexdigest()==v['sha256']
raw=json.loads(Path('w-verifier/claim16_runner/tour48.json').read_text());g={tuple(p):list(map(tuple,ns)) for p,ns in raw}
def turn(p):
 a,b=g[p];return (a[0]-p[0])*(b[1]-p[1])!=(a[1]-p[1])*(b[0]-p[0])
bottom=[sum(turn((x,y)) for y in range(4)) for x in range(8,24)]
top=[sum(turn((x,y)) for y in range(44,48)) for x in range(8,24)]
assert bottom==[3,1,2,2,1,3,2,2]*2 and top==[1,3,2,2,3,1,2,2]*2
assert all(a+b==4 for a,b in zip(bottom,top))
assert sum(map(turn,g))==370
out={'date':'2026-10-02','corner_residual':r,'corner_internal_component_sizes':sizes,'old_rebuild_sizes':sizes_old,'corner_hashes_unchanged':True,'count_bottom':bottom,'count_top':top,'n48_turns':370,'n56_turns':next(v['T'] for v in old['rebuilt'] if v['n']==56)}
Path('w-verifier/claim16_blog.json').write_text(json.dumps(out,indent=1));print(out)
