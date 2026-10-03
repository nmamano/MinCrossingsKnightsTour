"""Zero-crossing half-strip: incoming A edges fixed, other exit edges free."""
from check_corridor_sat import MOVES,cross
from pysat.formula import CNF,IDPool
from pysat.card import CardEnc
from pysat.solvers import Glucose3
import time,json

def run(K,P):
    start=time.monotonic();pool=IDPool();cnf=CNF()
    es=[];ids=[]
    for u in range(K):
        for v in range(P):
            p=(u+v,v)
            for dx,dy in MOVES:
                if dx-dy<=0:continue
                q=(p[0]+dx,p[1]+dy)
                es.append((p,q));ids.append(pool.id(('e',p,q)))
    fixed=[((v-1,v),(v+1,v+1)) for v in range(P)]
    inc={(u,v):[] for u in range(K+3) for v in range(P)}
    for e,i in zip(es,ids):
        for x,y in e:inc[x-y,y%P].append(i)
    for (u,v),ls in inc.items():
        c=CardEnc.equals(ls,1 if u==0 else 2,vpool=pool) if u<K else CardEnc.atmost(ls,2,vpool=pool)
        cnf.extend(c.clauses)
    cnf.append([i for (a,b),i in zip(es,ids) if a[0]-a[1]==0 and b[0]-b[1]==3])
    allE=es+fixed
    for i,e in enumerate(allE):
        for j in range(i,len(allE)):
            f=allE[j]
            for k in range(-2,3):
                if i==j and k==0:continue
                if cross(e,tuple((x+k*P,y+k*P) for x,y in f)):
                    assert i<len(es)
                    cnf.append([-ids[i]] if j>=len(es) or i==j else [-ids[i],-ids[j]])
    with Glucose3(bootstrap_with=cnf.clauses) as s:
        sat=s.solve()
        model=set(s.get_model() or [])
    out=dict(K=K,P=P,satisfiable=sat,seconds=time.monotonic()-start,
             chosen=[e for e,i in zip(es,ids) if i in model] if sat else [])
    print(json.dumps({k:v for k,v in out.items() if k!='chosen'}),flush=True)
    return out
if __name__=='__main__':
    from pathlib import Path
    res=[run(K,6) for K in (1,2,3,4,6)]
    Path(__file__).with_name('half_corridor_results.json').write_text(json.dumps(res,indent=2))
