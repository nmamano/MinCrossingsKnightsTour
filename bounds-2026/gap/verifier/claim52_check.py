"""Assembly support: exact exception enumeration and a disconnected 2-factor test.
Standard library; imports only independent verifier checkers from Claims 50/51.
"""
from pathlib import Path
from itertools import product,combinations
from collections import defaultdict,Counter
import json
import claim50_check as A
from claim51_check import run as scalar_check,MOVES
edge=A.edge
# Exhaustive strip geometry near square row zero. Span two proves this box sufficient.
es={edge((x,y),(x+dx,y+dy)) for x,y in product((0,1),range(-3,4)) for dx,dy in ((1,2),(2,1),(-1,2),(-2,1),(1,-2),(2,-1),(-1,-2),(-2,-1)) if 0<=x+dx<=3}
qq={e:A.quarters(e) for e in es};exception=[]
for a,b in combinations(sorted(es),2):
 common=qq[a]&qq[b]
 if common:assert A.cross(a,b) and max(x for x,y,k in common)<=2
 if all(any(x==0 for x,y in e) for e in (a,b)) and any(x>=1 and y==0 for x,y,k in common):exception.append((a,b,sorted(common)))
expected={edge((0,0),(2,1)),edge((0,1),(2,0))}
assert len(exception)==1 and set(exception[0][:2])==expected and max(q[0] for q in exception[0][2])==1
# Reflect directly, checking the DOWN row -1 and the corresponding pair.
ref=lambda e:edge(*[(x,-y) for x,y in e]);eres={ref(e) for e in es};qr={e:A.quarters(e) for e in eres};down=[]
for a,b in combinations(sorted(eres),2):
 if all(any(x==0 for x,y in e) for e in (a,b)) and any(x>=1 and y==-1 for x,y,k in qr[a]&qr[b]):down.append((a,b))
assert len(down)==1 and set(down[0])=={ref(e) for e in expected}

file='gap/verifier/claim36_FOLD_n144.json';grid=json.loads(Path(file).read_text())['tour'];n=len(grid)
E={edge((x,n-1-y),(x+MOVES[int(v)][1],n-1-y-MOVES[int(v)][0])) for y,row in enumerate(grid) for x,code in enumerate(row) for v in code};adj=defaultdict(set)
for a,b in E:adj[a].add(b);adj[b].add(a)
seq=[(0,0)];prev=None;cur=(0,0)
while True:
 z=next(v for v in sorted(adj[cur]) if v!=prev)
 if z==(0,0):break
 seq.append(z);prev,cur=cur,z
assert len(seq)==n*n
nex=dict(zip(seq,seq[1:]+seq[:1]));pre={b:a for a,b in nex.items()}
knight=lambda a,b:sorted((abs(a[0]-b[0]),abs(a[1]-b[1])))==[1,2]
patch=None
for a in sorted(nex):
 b=nex[a]
 for dy,dx in MOVES:
  d=(a[0]+dx,a[1]+dy)
  if d not in pre:continue
  c=pre[d]
  if len({a,b,c,d})!=4 or not knight(b,c):continue
  rem={edge(a,b),edge(c,d)};add={edge(a,d),edge(b,c)}
  if add&E:continue
  patch=dict(remove=sorted(rem),add=sorted(add));break
 if patch:break
assert patch
F=E-rem|add;adj=defaultdict(set)
for a,b in F:adj[a].add(b);adj[b].add(a)
assert len(F)==n*n and all(len(nb)==2 for nb in adj.values())
comp={};sizes=[]
for v in sorted(adj):
 if v in comp:continue
 ci=len(sizes);todo=[v];comp[v]=ci;size=0
 while todo:
  p=todo.pop();size+=1
  for q in adj[p]:
   if q not in comp:comp[q]=ci;todo.append(q)
 sizes.append(size)
assert len(sizes)==2
og=[['' for _ in range(n)] for _ in range(n)]
for (x,y),nb in adj.items():og[n-1-y][x]=''.join(str(MOVES.index((y-v,u-x))) for u,v in sorted(nb))
f='gap/verifier/claim52_twofactor_n144.json';Path(f).write_text(json.dumps(dict(tour=og,component_sizes=sizes,patch=patch,source=file)))
scalar=scalar_check(f)
own=defaultdict(list)
for e in F:
 for q in A.quarters(e):own[q].append(e)
pairs={tuple(sorted((a,b))) for ls in own.values() for a,b in combinations(ls,2)}
between=sum(comp[a[0]]!=comp[b[0]] for a,b in pairs)
# Walk the actual disconnected strip, retaining only the cut edges, with no component labels.
walks=[]
for T in (lambda v:v,lambda v:(n-1-v[0],v[1]),lambda v:(v[1],v[0]),lambda v:(n-1-v[1],v[0])):
 loc={edge(T(a),T(b)) for a,b in F};strip={e for e in loc if min(e[0][0],e[1][0])<2};s=0;sw=0
 for r in range(n):
  mask={edge((a[0],a[1]-r),(b[0],b[1]-r)) for a,b in strip if min(a[1],b[1])<=r<=max(a[1],b[1])}
  target=sum(A.C[edge((a[0],a[1]-1),(b[0],b[1]-1))] for a,b in mask if max(a[1],b[1])>0)
  gu,gd=A.flags(sum(A.U[e] for e in mask));found=[w for t,w,u,d in A.arcs_from(s) if (t,u,d)==(target,gu,gd)]
  assert len(found)==1;sw+=found[0];s=target
 assert s==0 and sw==sum(A.cross(a,b) for a,b in combinations(strip,2));walks.append(sw)
gf=[]
for T in (lambda v:v,lambda v:(n-1-v[0],v[1]),lambda v:(v[1],v[0]),lambda v:(n-1-v[1],v[0])):
 loc={edge(T(a),T(b)) for a,b in F};strip={e for e in loc if min(e[0][0],e[1][0])<2};gg=[]
 for r in range(n):
  mask=sum(A.U[edge((a[0],a[1]-r),(b[0],b[1]-r))] for a,b in strip if min(a[1],b[1])<=r<=max(a[1],b[1]))
  gg.append(A.flags(mask)[0 if r<n//2 else 1])
 gf.append(gg)
multi=[]
for fx,fy in product((0,1),repeat=2):
 for r in range(12,n//2-3):
  if gf[fx][n-1-r if fy else r] or gf[2+fy][n-1-r if fx else r]:continue
  pp=[(n-2-x if fx else x,n-2-y if fy else y) for x,y in [(r,j) for j in range(1,r+1)]+[(j,r) for j in range(r-1,0,-1)]]
  touched={comp[e[0]] for x,y in pp for k in range(4) for e in own[x,y,k]}
  if len(touched)>1:multi.append((fx,fy,r))
assert multi
out=dict(date='2026-10-03',outer_exception_up=exception,outer_exception_down=down,twofactor_components=sizes,cross_component_pairs=between,kept_paths_meeting_both_cycles=len(multi),example_kept_path=multi[0],scalar_check=scalar,side_crossings=walks,all_row_walks_pass=True)
Path('gap/verifier/claim52_check.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
