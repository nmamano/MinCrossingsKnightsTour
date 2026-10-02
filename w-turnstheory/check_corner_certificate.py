"""Exact certificate for T >= 8n-28. No solver imports."""
from itertools import combinations
from fractions import Fraction
M=[(dx,dy) for dx in (-2,-1,1,2) for dy in (-2,-1,1,2) if abs(dx)+abs(dy)==3]
def lower(x,ds):
    if x==0:return 1
    if x in (1,2):return sum(x+d in (0,3) for d in ds)-1
    if x==3:return 1-sum(x+d in (1,2) for d in ds)
    return 0
# Coordinates are (x,y), with 0 <= x,y <= 3.
ALPHA={(0,0):-1,(0,3):-1,(1,1):1,(1,3):-1,(2,3):-1,
       (3,0):-1,(3,1):-1,(3,2):-1,(3,3):-1}
BETA={((0,1),(1,3)):-1,((0,2),(2,3)):-1,((0,3),(1,1)):1,
      ((1,0),(3,1)):-1,((1,1),(3,0)):-1,((1,2),(3,3)):-1,
      ((2,0),(3,2)):-1,((2,1),(3,3)):-1,((2,2),(3,0)):-1}
def cert_at(p,ds):
    c=ALPHA.get(p,0)
    for d in ds:
        q=(p[0]+d[0],p[1]+d[1]);e=tuple(sorted((p,q)))
        c+=BETA.get(e,0)*(1 if p<q else -1)
    return c
count=0
mins=[]
for y in range(4):
    row=[]
    for x in range(4):
        p=(x,y);vals=[]
        for a,b in combinations([d for d in M if x+d[0]>=0 and y+d[1]>=0],2):
            t=int(a[0]+b[0]!=0 or a[1]+b[1]!=0)
            r=t-lower(x,[a[0],b[0]])-lower(y,[a[1],b[1]])
            gap=r-cert_at(p,(a,b))
            assert gap>=0,(p,a,b,r,cert_at(p,(a,b)))
            vals.append(gap);count+=1
        row.append(min(vals))
    mins.append(row)
assert sum(ALPHA.values())==-7
print('PASS:',count,'local pairs; all certificate gaps >=0.')
print('Minimum gap by y row:',mins)
print('Sum of vertex constants:',sum(ALPHA.values()),'; four-corner constant: -28.')

# Check global formula independently on known valid tours.
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from kt.gentour import gen_tour
from kt.core import validate,neighbors,num_turns
for n in (16,24,40,80):
    tour=gen_tour(n,n);assert validate(tour)
    side_sum=0;corner_res=[0]*4;full_res=0
    for y in range(n):
        for x in range(n):
            ds=[(xx-x,yy-y) for yy,xx in neighbors(tour,y,x)]
            t=int(tuple(map(sum,zip(*ds)))!=(0,0))
            ls=(lower(x,[d[0] for d in ds])+lower(n-1-x,[-d[0] for d in ds])+
                lower(y,[d[1] for d in ds])+lower(n-1-y,[-d[1] for d in ds]))
            side_sum+=ls;full_res+=t-ls
            for k,(xx,yy) in enumerate(((x,y),(n-1-x,y),(x,n-1-y),(n-1-x,n-1-y))):
                if xx<4 and yy<4:corner_res[k]+=t-ls
    assert side_sum==8*n
    assert min(corner_res)>=-7
    assert full_res==num_turns(tour)-8*n>=-28
    print('PASS: n=',n,'corner residuals=',corner_res,'T-8n=',full_res)

witness={}
for line in (Path(__file__).parent/'corner_witness.txt').read_text().splitlines():
    if not line or line.startswith('#'):continue
    x,y,ax,ay,bx,by=map(int,line.split())
    witness[x,y]=((ax,ay),(bx,by))
assert len(witness)==16
residual=0;adj={v:[] for v in witness}
for p,(a,b) in witness.items():
    assert a in M and b in M and a!=b
    for d in (a,b):
        q=(p[0]+d[0],p[1]+d[1]);assert min(q)>=0
        if q in witness:
            assert (-d[0],-d[1]) in witness[q]
            adj[p].append(q)
    t=int(tuple(map(sum,zip(a,b)))!=(0,0))
    residual+=t-lower(p[0],[a[0],b[0]])-lower(p[1],[a[1],b[1]])
assert residual==-7
seen=set()
for v in witness:
    if v in seen:continue
    comp=set();stack=[v]
    while stack:
        p=stack.pop()
        if p in comp:continue
        comp.add(p);stack.extend(adj[p])
    assert any(len(adj[p])<2 for p in comp)
    seen|=comp
print('PASS: local witness has residual -7, consistent edges, and no internal cycle.')
