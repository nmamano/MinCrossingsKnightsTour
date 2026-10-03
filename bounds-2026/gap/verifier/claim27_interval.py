"""Independent interval graph from the verifier's general forest scan.
Uses no author graph code. Checks the saved potential against every own arc.
"""
from collections import Counter
from itertools import combinations
from pathlib import Path
import json
from claim26_certificate import cross

def successors(state):
    x,pending=state;p=(x,0)
    inc=[e for e in pending if e[1]==p]
    keep=[e for e in pending if e[1]!=p]
    if len(inc)>2 or len(inc)==2 and inc[0][2]==inc[1][2]:return
    options=[(p,(xx,dy)) for xx in range(3) for dy in (1,2)
             if sorted((abs(xx-x),dy))==[1,2] and min(x,xx)==0]
    for count in range(3-len(inc)):
      for chosen in combinations(options,count):
        load=Counter(e[1] for e in keep);load.update(b for a,b in chosen)
        if max(load.values(),default=0)>2:continue
        labels={e[2] for e in inc};merged=min(labels) if labels else -1
        result=[(a,b,merged if c in labels else c) for a,b,c in keep]
        result.extend((a,b,merged) for a,b in chosen)
        w=sum(cross(f,(a,b)) for f in chosen for a,b,c in keep)
        w+=sum(cross(e,f) for e,f in combinations(chosen,2))
        shift=int(x==2);labels={};norm=[]
        for a,b,c in sorted(result):
          if c not in labels:labels[c]=len(labels)
          norm.append(((a[0],a[1]-shift),(b[0],b[1]-shift),labels[c]))
        yield ((x+1)%3,tuple(norm)),w,(x!=0 or len(inc)+count==2)

saved=json.loads(Path('gap/verifier/inner_boundary_certificate.json').read_text())
pot={(col,tuple((tuple(a),tuple(b),c) for a,b,c in es)):v for (col,es),v in zip(saved['states'],saved['potential'])}
states=[(0,())];ids={states[0]:0};arcs=[]
for u,s in enumerate(states):
 for t,w,hard in successors(s):
  if t not in ids:ids[t]=len(states);states.append(t)
  arcs.append((u,ids[t],w,hard))
assert len(states)==330 and len(arcs)==700 and set(states)==set(pot)
checked=0
for u,v,w,hard in arcs:
 if hard:
  assert 3*w-1+pot[states[u]]-pot[states[v]]>=0
  checked+=1
assert checked==580
rowpot=[pot[s] for s in states if s[0]==0]
assert min(rowpot)==-12 and max(rowpot)==0
print('PASS independent interval graph: 330 states, 700 arcs, 580 hard inequalities; row error 12/3=4')
