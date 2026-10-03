"""Independent exact checks of the period-(2,4) wall and perfect-field attachments."""
from collections import defaultdict
from itertools import combinations,product
from pathlib import Path
import json,sys
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'w-verifier'))
from claim9_tiles import quarters,proper
W=[((-1,0),(1,1)),((1,0),(3,1)),((1,0),(2,2)),((2,0),(3,2)),((3,0),(5,1)),((3,0),(4,2)),
   ((0,1),(2,2)),((2,1),(4,2)),((2,1),(3,3)),((4,1),(6,2)),((4,1),(5,3)),
   ((1,2),(3,3)),((1,2),(2,4)),((3,2),(5,3)),
   ((0,3),(2,4)),((2,3),(4,4)),((2,3),(3,5)),((4,3),(6,4)),((4,3),(5,5))]
MOV=[(x,y) for x,y in product(range(-2,3),repeat=2) if sorted((abs(x),abs(y)))==[1,2]]
def edge(a,b):return tuple(sorted((a,b)))
def tr(v,k):return v[0]+2*k,v[1]+4*k
def u(v):return v[0]-(v[1]+1)//2
def modeled(v):return 0<=u(v)<4
def tile(e):
    a,b=e
    return {(x+a[0],y+a[1],q) for x,y,q in quarters(((0,0),(b[0]-a[0],b[1]-a[1])))}
E={edge(tr(a,k),tr(b,k)) for a,b in W for k in range(-10,11)}
assert len(E)==21*19 and all(any(modeled(v) for v in e) for e in E)
adj=defaultdict(set);own=defaultdict(list)
for a,b in E:
    adj[a].add(b);adj[b].add(a)
    for q in tile((a,b)):own[q].append((a,b))
assert max(map(len,adj.values()))<=2
assert all(len(adj[x,y])==2 for y in range(-8,9) for x in range(-10,15) if modeled((x,y)))
crossings=[(e,f) for e,f in combinations(sorted(E),2) if 0<=max(min(v[1] for v in e),min(v[1] for v in f))<4 and proper(e,f)]
assert len(crossings)==2
# Exact voltage graph. A quotient cycle with nonzero translation lifts to a line,
# not a finite cycle. Paths in a degree<=2 quotient cannot lift to finite cycles.
def canon(v):
    k=v[1]//4;return tr(v,-k),k
Q=defaultdict(list)
for ei,(a,b) in enumerate(W):
    ca,ka=canon(a);cb,kb=canon(b)
    Q[ca].append((cb,kb-ka,ei));Q[cb].append((ca,ka-kb,ei))
components=[];seen=set()
for start in Q:
    if start in seen:continue
    comp={start};todo=[start]
    for v in todo:
        for z,vol,i in Q[v]:
            if z not in comp:comp.add(z);todo.append(z)
    seen|=comp;is_cycle=all(len(Q[v])==2 for v in comp);voltage=None
    if is_cycle:
        cur=start;last=-1;voltage=0
        while True:
            z,vol,i=next(a for a in Q[cur] if a[2]!=last)
            voltage+=vol;last=i;cur=z
            if cur==start:break
        assert voltage!=0
    components.append(dict(vertices=len(comp),quotient_cycle=is_cycle,voltage=voltage))
rows=[];holes=doubles=0
for y in range(4):
    potential=defaultdict(set)
    for x0,y0 in product(range(-6,12),range(y-2,y+4)):
        for dx,dy in MOV:
            e=edge((x0,y0),(x0+dx,y0+dy))
            for x,j,q in tile(e):
                if j==y:potential[x].add(e)
    complete=sorted(x for x,es in potential.items() if es and all(any(modeled(v) for v in e) for e in es))
    assert complete==list(range(min(complete),max(complete)+1))
    counts={x:[len(own[x,y,q]) for q in range(4)] for x in complete}
    assert counts[complete[0]]==counts[complete[-1]]==[1]*4
    holes+=sum(m==0 for ms in counts.values() for m in ms)
    doubles+=sum(m==2 for ms in counts.values() for m in ms)
    psi=sum((-1)**(x+y+1)*(counts[x-1][1]+counts[x][3]+1) for x in complete[1:])
    assert psi%3!=0
    rows.append(dict(y=y,complete_columns=complete,multiplicities=counts,omega_integer=psi,psi_mod3=psi%3))
assert holes==doubles==4

# Test all (2,4)-periodic full-plane fold stacks as direct exterior fields.
attachments={}
for side in ('left','right'):
    fits=[]
    vertices=[(x,y) for y in range(4) for x in range(-6,12) if (-3<=u((x,y))<0 if side=='left' else 4<=u((x,y))<7)]
    for a,b in ((1,0),(0,1),(1,1),(1,-1)):
        steps=[d for d in MOV if a*d[0]+b*d[1]==1];period=abs(2*a+4*b)
        for seq in product(steps,repeat=period):
            def neigh(v):
                t=a*v[0]+b*v[1];f=seq[t%period];g=seq[(t-1)%period]
                return {(v[0]+f[0],v[1]+f[1]),(v[0]-g[0],v[1]-g[1])}
            if all({z for z in neigh(v) if modeled(z)}==adj[v] for v in vertices):
                fits.append(dict(functional=[a,b],word=seq))
    attachments[side]=fits
assert all(len(attachments[side])==1 for side in attachments)
assert attachments['left']==attachments['right']
# Explicit perfect full-plane exterior: f=x-y, c_even=(-1,-2), c_odd=(2,1).
extended=set(E)
for y in range(-16,20):
    for s in range(-14,18):
        v=(s+(y+1)//2,y);d=(-1,-2) if (v[0]-v[1])%2==0 else (2,1)
        z=(v[0]+d[0],v[1]+d[1])
        if not modeled(v) and not modeled(z):extended.add(edge(v,z))
eadj=defaultdict(set);em=defaultdict(int)
for a,b in extended:
    eadj[a].add(b);eadj[b].add(a)
    for q in tile((a,b)):em[q]+=1
for y in range(4):
    for s in range(-10,14):
        x=s+(y+1)//2;assert len(eadj[x,y])==2
        counts=[em[x,y,k] for k in range(4)]
        if x not in rows[y]['complete_columns']:assert counts==[1]*4
        else:assert counts==rows[y]['multiplicities'][x]
ex=[(e,f) for e,f in combinations(sorted(extended),2)
    if 0<=max(min(v[1] for v in e),min(v[1] for v in f))<4 and proper(e,f)]
assert len(ex)==2
assert all(len(tile(e)&tile(f))==2 for e,f in ex)
full=dict(functional='x-y',even_step=[-1,-2],odd_step=[2,1],
          crossings_per_period=len(ex),extra_crossings=0,checked_vertices=96,
          checked_quarters=384,holes_per_period=4,X1_per_period=0,W3_per_period=0)
def multiplicity(x,y,q):
    k=y//4;x-=2*k;y-=4*k
    return em[x,y,q] if -10<=x-(y+1)//2<14 else 1
gamma=[]
for r in range(12,81):
    flux=sum((-1)**(r+j+1)*(multiplicity(r,j,2)+multiplicity(r,j+1,0)+1) for j in range(1,r))
    flux-=sum((-1)**(x+r+1)*(multiplicity(x-1,r,1)+multiplicity(x,r,3)+1) for x in range(2,r+1))
    assert flux%3!=0
    gamma.append((r,flux%3))
out=dict(date='2026-10-03',period=[2,4],edge_orbits=19,modeled_degrees_two=True,max_degree=2,
         quotient_components=components,no_finite_cycle=True,crossing_pairs=crossings,
         crossings_per_period=2,holes_in_complete_squares=holes,doubles_in_complete_squares=doubles,
         rows=rows,direct_foldstack_attachments=attachments,explicit_plane_extension=full,
         open_gamma_residues=gamma)
print(json.dumps(out,indent=2));(ROOT/'gap/verifier/claim35_wall.json').write_text(json.dumps(out,indent=2))
