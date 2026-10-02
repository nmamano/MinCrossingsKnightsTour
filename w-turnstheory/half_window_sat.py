"""Finite local test: can a long-normal edge leave a forced A input row?"""
from check_corridor_sat import MOVES,cross
from pysat.formula import CNF,IDPool
from pysat.card import CardEnc
from pysat.solvers import Glucose3
from collections import defaultdict
import json,time

def run(R,phase=False):
    start=time.monotonic();pool=IDPool();cnf=CNF();es=[];ids=[];inc=defaultdict(list)
    for u in (0,1):
        for v in range(-R-4,R+5):
            p=(u+v,v)
            for dx,dy in MOVES:
                if dx-dy<=0:continue
                q=(p[0]+dx,p[1]+dy)
                i=pool.id(('e',p,q));es.append((p,q));ids.append(i)
                inc[p].append(i);inc[q].append(i)
    fixed=[((v-1,v),(v+1,v+1)) for v in range(-R-8,R+9)]
    for p,ls in inc.items():
        u,v=p[0]-p[1],p[1]
        if u in (0,1) and -R<=v<=R:
            cnf.extend(CardEnc.equals(ls,1 if u==0 else 2,vpool=pool).clauses)
        else:cnf.extend(CardEnc.atmost(ls,1 if u==0 else 2,vpool=pool).clauses)
    if phase:
        cnf.append([i for (a,b),i in zip(es,ids) if a==(-1,-1) and b==(-2,-3)])
        cnf.append([i for (a,b),i in zip(es,ids) if a==(0,0) and b==(2,1)])
    else:
        cnf.append([i for (a,b),i in zip(es,ids) if a==(0,0) and b[0]-b[1]==3])
    allE=es+fixed
    for i,e in enumerate(allE):
        for j in range(i+1,len(allE)):
            if cross(e,allE[j]):
                assert i<len(es)
                cnf.append([-ids[i]] if j>=len(es) else [-ids[i],-ids[j]])
    with Glucose3(bootstrap_with=cnf.clauses,with_proof=True) as s:
        sat=s.solve();mod=set(s.get_model() or [])
        proof=s.get_proof() if not sat else []
    if R==2 and not phase:
        from pathlib import Path
        here=Path(__file__).parent
        cnf.to_file(str(here/'local_long_edge.cnf'))
        (here/'local_long_edge.drup').write_text('\n'.join(proof)+'\n')
    print(json.dumps(dict(R=R,phase=phase,satisfiable=sat,seconds=time.monotonic()-start)),flush=True)
    return dict(R=R,satisfiable=sat,chosen=[e for e,i in zip(es,ids) if i in mod] if sat else [])
if __name__=='__main__':
    from pathlib import Path
    res=[run(R) for R in (1,2,3,4,6,10)]
    Path(__file__).with_name('half_window_results.json').write_text(json.dumps(res,indent=2))
