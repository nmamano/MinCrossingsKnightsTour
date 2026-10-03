"""Check the boundary matching graph for all free trees through size 10."""
from claim37_check import shapes,tile
from collections import defaultdict
from pathlib import Path
import json
D=((1,0),(-1,0),(0,1),(0,-1));HS=('BR','TL','RT','LB')
# Build half adjacency from exact tile geometry.
adj=defaultdict(set)
for x in range(-3,14):
 for y in range(-3,14):
  for dx,dy in ((1,2),(2,1),(1,-2),(2,-1)):
   a,b=tile(((x,y),(x+dx,y+dy)));adj[a].add(b);adj[b].add(a)
out=[]
for s,level in enumerate(shapes(10)[1:],1):
 for U0 in level:
  U=set(U0);seen=set();graph=defaultdict(list)
  for q in U:
   for h in HS:
    z=(q,h)
    if z in seen:continue
    stack=[z];seen.add(z);ends=[]
    while stack:
     v=stack.pop();assert len(adj[v])==2
     for w in adj[v]:
      if w[0] not in U:ends.append((v[0],w[0]))
      elif w not in seen:seen.add(w);stack.append(w)
    assert len(ends)==2
    a,b=ends;graph[a].append(b);graph[b].append(a)
  assert len(graph)==2*s+2 and all(len(v)==2 for v in graph.values())
  seen={next(iter(graph))};todo=list(seen)
  for v in todo:
   for w in graph[v]:
    if w not in seen:seen.add(w);todo.append(w)
  assert len(seen)==len(graph)
 out.append(dict(size=s,shapes=len(level),one_boundary_cycle=True))
Path('gap/verifier/claim41_uniform.json').write_text(json.dumps(out,indent=2));print(out)
