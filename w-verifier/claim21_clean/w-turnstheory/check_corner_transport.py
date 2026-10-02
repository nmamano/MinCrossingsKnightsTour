"""Check reference charges and the difference-flow identity on one valid tour."""
import sys,json
from pathlib import Path
from collections import Counter
root=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(root),str(root/'w-lowerbounds')]
from fold_complete2 import base
from kt.gentour import gen_tour
from kt.core import validate,edges
n=48
F,deg=base(n)
q={(x,y):(1 if (x+y)%2==0 else -1)*(2-deg[x,y]) for x in range(n) for y in range(n)}
t=gen_tour(n,n);assert validate(t)
# core coordinates are (row,column); swap them for Cartesian (x,y).
H={tuple(sorted(((a[1],a[0]),(b[1],b[0])))) for a,b in edges(t)}
changed=(H-F)|(F-H)
def charge(R):return sum(q[p] for p in R)
def flux(E,R):
    z=0
    for a,b in E:
        if (a in R)==(b in R):continue
        p=a if a in R else b
        z+=1 if sum(p)%2==0 else -1
    return z
rows=[]
for r in range(4,n//2-3):
    R={(x,y) for x in range(r) for y in range(r)}
    delta=flux(H,R)-flux(F,R)
    assert charge(R)==delta==2
    assert flux(H,R)==(2 if r%2 else 0)
    rows.append(dict(r=r,reference_charge=charge(R),tour_flux=flux(H,R),reference_flux=flux(F,R),difference_flux=delta))
print('PASS: n=48, radii',rows[0]['r'],'through',rows[-1]['r'],'all have difference flux 2.')
print('PASS: raw tour flux is 0 on even square windows and 2 on odd square windows.')
# General moment identity: each signed changed edge contributes a potential difference.
phi=lambda p:abs(p[0]+p[1]-(n-1))
moment=sum(q[p]*phi(p) for p in q)
edge_moment=0
for a,b in changed:
    black,white=(a,b) if sum(a)%2==0 else (b,a)
    edge_moment+=(1 if (a,b) in H else -1)*(phi(black)-phi(white))
assert moment==edge_moment
assert abs(moment)<=3*len(changed)
print('PASS: charge moment',moment,'equals edge moment; symmetric difference size',len(changed))
Path(__file__).with_name('corner_transport_check.json').write_text(json.dumps(dict(n=n,moment=moment,changed_edges=len(changed),cuts=rows),indent=2))
