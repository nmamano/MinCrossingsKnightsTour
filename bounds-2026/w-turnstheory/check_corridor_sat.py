"""Independent SAT check of the finite all-move fold corridor models."""
from pathlib import Path
from itertools import combinations
from pysat.formula import CNF,IDPool
from pysat.card import CardEnc
from pysat.solvers import Glucose3
import json,time

MOVES=((1,2),(2,1),(2,-1),(1,-2),(-1,-2),(-2,-1),(-2,1),(-1,2))
def orient(a,b,c):return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
def cross(e,f):
    a,b=e;c,d=f
    return orient(a,b,c)*orient(a,b,d)<0 and orient(c,d,a)*orient(c,d,b)<0

def verify(D,P,flux,limit,force_long=False):
    started=time.monotonic();pool=IDPool();cnf=CNF()
    # Use actual Cartesian coordinates, periodic translation (P,P).
    cells={(u+v,v):(u,v) for u in range(D) for v in range(P)}
    es=[];ids=[]
    for p,(u,v) in sorted(cells.items()):
        for dx,dy in MOVES:
            un=u+dx-dy
            if not u<un<D:continue
            q=(p[0]+dx,p[1]+dy);es.append((p,q));ids.append(pool.id(('edge',p,q)))
    fixed=[((v-1,v),(v+1,v+1)) for v in range(P)]+[((D-1+v,v),(D+v-2,v-2)) for v in range(P)]
    inc={p:[] for p in cells};fdeg={p:0 for p in cells}
    def canon(p):
        x,y=p;k=y//P;return(x-k*P,y-k*P)
    for e,i in zip(es,ids):
        for p in e:inc[canon(p)].append(i)
    for e in fixed:
        for p in e:
            if canon(p) in fdeg:fdeg[canon(p)]+=1
    for p in cells:cnf.extend(CardEnc.equals(inc[p],2-fdeg[p],vpool=pool).clauses)
    coefficients=[];reference=0
    for (a,b),eid in zip(es,ids):
        u=a[0]-a[1];c=(-1 if u%2 else 1)*(b[1]//P)
        assert c in (-1,0,1)
        if c:coefficients.append((eid,c))
        if (b[0]-a[0],b[1]-a[1])==(-1,-2):reference+=c
    neg=sum(c<0 for _,c in coefficients)
    if flux is not None:
        target=reference+flux+neg
        cnf.extend(CardEnc.equals([i if c>0 else -i for i,c in coefficients],target,vpool=pool).clauses)
    if force_long:cnf.append([i for (a,b),i in zip(es,ids) if (b[0]-b[1])-(a[0]-a[1])==3])
    all_edges=es+fixed;cost=[]
    for i,e in enumerate(all_edges):
        for j in range(i,len(all_edges)):
            f=all_edges[j];mult=0
            for k in range(-3,4):
                if i==j and k==0:continue
                fk=tuple((x+k*P,y+k*P) for x,y in f)
                mult+=int(cross(e,fk))
            if i==j:assert mult%2==0;mult//=2
            if not mult:continue
            assert mult==1,(i,j,mult)
            assert i<len(es),'fixed edges cross'
            if j>=len(es) or i==j:cost.append(ids[i])
            else:
                z=pool.id(('cross',i,j));cnf.append([-ids[i],-ids[j],z]);cost.append(z)
    cnf.extend(CardEnc.atmost(cost,limit,vpool=pool).clauses)
    with Glucose3(bootstrap_with=cnf.clauses) as solver:
        sat=solver.solve()
        witness=set(solver.get_model() or [])
    out=dict(D=D,P=P,flux=flux,max_crossings=limit,force_long=force_long,
             satisfiable=sat,variables=pool.top,clauses=len(cnf.clauses),seconds=time.monotonic()-started)
    print(json.dumps(out),flush=True)
    if sat:out['chosen']=[e for e,i in zip(es,ids) if i in witness]
    return out
if __name__=='__main__':
    results=[]
    for args in [(3,6,1,0),(6,6,1,0),(10,6,1,0),(10,6,0,0,True),(10,6,None,0,True),(4,6,1,3),(6,6,1,3),(4,12,1,7)]:
        results.append(verify(*args))
    Path(__file__).with_name('corridor_sat_results.json').write_text(json.dumps(results,indent=2))
