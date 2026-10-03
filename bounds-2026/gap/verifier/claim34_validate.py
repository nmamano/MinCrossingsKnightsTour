"""Solver-free validation and both Hall tests for the saved closed tour."""
from pathlib import Path
from collections import defaultdict
import json,sys
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'w-verifier'))
from claim9_tiles import quarters,proper
from check import check, MOVES
p=json.loads((ROOT/'gap/verifier/claim34_closed_tour.json').read_text());N=p['n']
edges={tuple(map(tuple,e)) for e in p['edges']};adj=defaultdict(list);own=defaultdict(list)
for a,b in edges:
    assert all(0<=z<N for v in (a,b) for z in v)
    assert sorted((abs(a[0]-b[0]),abs(a[1]-b[1])))==[1,2]
    adj[a].append(b);adj[b].append(a)
    for x,y,k in quarters(((0,0),(b[0]-a[0],b[1]-a[1]))):own[x+a[0],y+a[1],k].append((a,b))
assert len(adj)==N*N and len(edges)==N*N and all(len(ns)==2 for ns in adj.values())
seen={(0,0)};queue=[(0,0)]
for v in queue:
    for u in adj[v]:
        if u not in seen:seen.add(u);queue.append(u)
assert len(seen)==N*N
HQ={'BR':(0,1),'TL':(2,3),'RT':(1,2),'LB':(3,0)}
def good(x,y):return all(len(own[x,y,k])==1 for k in range(4))
def state(t):
    x,y,h=t
    if not good(x,y):return 'B'
    qs=HQ[h]
    if own[x,y,qs[0]]!=own[x,y,qs[1]]:return 'W'
    e=own[x,y,qs[0]][0]
    return 'H' if abs(e[0][0]-e[1][0])==2 else 'V'
chains=defaultdict(list)
for x in range(N-1):
    for y in range(N-1):
        for h,k,pos in [('BR',y-x,2*x),('TL',y-x+1,2*x-1),('RT',x+y,2*x),('LB',x+y-1,2*x-1)]:
            chains[('/' if h in ('BR','TL') else '\\',k)].append((pos,(x,y,h)))
cuts=[]
for items in chains.values():
    seq=[t for i,t in sorted(items)];left=None
    for j,t in enumerate(seq):
        s=state(t)
        if s=='W':left=None
        elif s in ('H','V'):
            if left is not None and j>left+1 and state(seq[left])!=s:cuts.append(seq[left:j+1])
            left=j
target=list(map(tuple,p['cut']));assert target in cuts
def candidates(cut,mode):
    return {(x,y,k) for x,y,h in cut[1:-1] for k in (HQ[h] if mode=='half' else range(4)) if len(own[x,y,k])!=1}
def hall(mode):
    opts=[candidates(c,mode) for c in cuts];matched={};got=0
    def augment(slot,seen):
        for q in opts[slot//2]:
            if q in seen:continue
            seen.add(q)
            if q not in matched or augment(matched[q],seen):matched[q]=slot;return True
        return False
    for slot in range(2*len(cuts)):got+=augment(slot,set())
    return dict(cuts=len(cuts),demand=2*len(cuts),matched=got)
half=candidates(target,'half');square=candidates(target,'square');assert len(half)==1
es=sorted(edges);X=sum(proper(e,f) for i,e in enumerate(es) for f in es[:i])
grid=[['' for x in range(N)] for row in range(N)]
for (x,y),ns in adj.items():
    grid[N-1-y][x]=''.join(sorted(str(MOVES.index((y-v,u-x))) for u,v in ns))
cx,turns=check(grid);assert cx==X
(ROOT/'gap/verifier/claim34_tour_n16.json').write_text(json.dumps(dict(n=N,tour=grid,crossings=X,turns=turns),indent=2))
out=dict(date='2026-10-03',n=N,vertices=N*N,edges=len(edges),connected=True,degree_two=True,
         knight_moves=True,X=X,cut=target,endpoint_bits=[state(target[0]),state(target[-1])],
         gap_half_bad_quarters=sorted(half),gap_square_bad_quarters=sorted(square),
         gap_min_side_distance=min(min(x,y,N-2-x,N-2-y) for x,y,h in target[1:-1]),
         endpoint_tiles=[own[t[0],t[1],HQ[t[2]][0]][0] for t in (target[0],target[-1])],
         gap_multiplicities=[dict(half=t,m=[len(own[t[0],t[1],k]) for k in range(4)]) for t in target[1:-1]],
         square_hall=hall('square'),half_hall=hall('half'))
print(json.dumps(out,indent=2));(ROOT/'gap/verifier/claim34_validation.json').write_text(json.dumps(out,indent=2))
