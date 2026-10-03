"""Independent periodic W=4 strip model with exact lifted port pairings.

Run with the project venv. Optional arguments: maximum period, seconds.
No worker code imports. Cyclic components without ports are allowed when
they lift to infinite paths; at W=4 such components lie in columns 0,1.
"""
from collections import Counter, defaultdict
from itertools import combinations
from pathlib import Path
import json
import sys
import time
from ortools.sat.python import cp_model

def cross(e,f):
    def det(a,b,c):
        return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
    a,b=e; c,d=f
    return det(a,b,c)*det(a,b,d)<0 and det(c,d,a)*det(c,d,b)<0

def translate(e,t):
    return tuple((x,y+t) for x,y in e)

def run(period,seconds,repair_count=None):
    p=period
    cells=[(x,y) for x in range(4) for y in range(p)]
    ports=[(x,y) for x in (2,3) for y in range(p)]
    es=[((x,y),(xx,y+dy)) for x,y in cells for xx in range(x+1,4)
        for dy in (-2,-1,1,2) if sorted((xx-x,abs(dy)))==[1,2]]
    forced=[((x,y),(x+2,y+1)) for x,y in ports]
    wrap=lambda v:(v[0],v[1]%p)
    m=cp_model.CpModel()
    selected=[m.new_bool_var('e'+str(i)) for i in range(len(es))]
    incident=defaultdict(list)
    for v,e in zip(selected,es):
        for a in e:
            incident[wrap(a)].append(v)
    for a in cells:
        m.add(sum(incident[a])==(1 if a[0]>=2 else 2))

    # A finite quotient component with ports has exactly two degree-one
    # port vertices. Their common label identifies the matched pair.
    # Label 2p permits components with no ports.
    lab={a:m.new_int_var(0,2*p,'lab'+str(a)) for a in cells}
    active={a:m.new_bool_var('active'+str(a)) for a in cells}
    lift={a:m.new_int_var(-10,10,'lift'+str(a)) for a in cells}
    for a in cells:
        m.add(lab[a]<2*p).only_enforce_if(active[a])
        m.add(lab[a]==2*p).only_enforce_if(active[a].Not())
    for v,(a,b) in zip(selected,es):
        aa,bb=wrap(a),wrap(b)
        m.add(lab[aa]==lab[bb]).only_enforce_if(v)
        m.add(bb[1]+p*lift[bb]-aa[1]-p*lift[aa]==b[1]-a[1]).only_enforce_if([v,active[aa]])
    matching={}; bad={}
    for i,j in combinations(range(2*p),2):
        v=m.new_bool_var('pair'+str((i,j)))
        matching[i,j]=v
        a,b=ports[i],ports[j]
        m.add(lab[a]==i).only_enforce_if(v)
        m.add(lab[b]==i).only_enforce_if(v)
        m.add(lift[a]==0).only_enforce_if(v)
        wrong=m.new_bool_var('bad'+str((i,j)))
        bad[i,j]=wrong
        m.add(wrong<=v)
        # True line label c=x-2y, without reduction modulo the period.
        delta=(3 if a[0]%2 else -3)
        diff=b[0]-2*(b[1]+p*lift[b])-a[0]+2*(a[1]+p*lift[a])
        m.add(diff==delta).only_enforce_if([v,wrong.Not()])
        m.add(diff!=delta).only_enforce_if(wrong)
    for i in range(2*p):
        m.add(sum(v for (a,b),v in matching.items() if i in (a,b))==1)

    # The lifted simple path has at most 4p vertices, hence displacement
    # <8p. With its root normalized, lift in [-10,10] excludes no pairing.
    # Count pair orbits by the later lower-end row in [0,p).
    copies=[]
    all_es=es+forced
    for i,e in enumerate(all_es):
        for k in range(-3,4):
            f=translate(e,k*p)
            lo=min(y for x,y in f)
            if -2<=lo<p:
                copies.append((i,f))
    crossing_coeff=Counter()
    for (i,e),(j,f) in combinations(copies,2):
        if 0<=max(min(y for x,y in e),min(y for x,y in f))<p and cross(e,f):
            assert i!=j
            crossing_coeff[tuple(sorted((i,j)))]+=1
    terms=[]
    for (i,j),co in crossing_coeff.items():
        if i>=len(es):
            terms.append(co)
        elif j>=len(es):
            terms.append(co*selected[i])
        else:
            z=m.new_bool_var('cross'+str((i,j)))
            m.add(z<=selected[i]); m.add(z<=selected[j])
            m.add(z>=selected[i]+selected[j]-1)
            terms.append(co*z)
    x=sum(terms)
    nre=2*sum(bad.values())
    if repair_count is not None:
        m.add(nre==repair_count)

    # Base-current class at the cut below row zero. For odd periods,
    # geometry repeats but colour changes sign; the zero class is valid.
    current_terms=[]; fixed_current=0
    for i,e in enumerate(all_es):
        co=0
        for k in range(-3,4):
            f=translate(e,k*p)
            a,b=sorted(f,key=lambda v:(v[1],v[0]))
            if a[1]<0<=b[1]:
                co+=-1 if (a[0]+a[1])%2 else 1
        if i<len(es):
            current_terms.append(co*selected[i])
        else:
            fixed_current+=co
    m.add(sum(current_terms)+fixed_current==0)
    m.minimize(2*x-nre)
    for v,(a,b) in zip(selected,es):
        is_p=(b[0]-a[0]==2 and b[1]-a[1]==1) or (a[0]==0 and b[0]==1 and b[1]-a[1]==2)
        m.add_hint(v,int(is_p))
    for (i,j),v in matching.items():
        a,b=ports[i],ports[j]
        m.add_hint(v,int(a[0]==2 and b==(3,(a[1]+2)%p)))
        m.add_hint(bad[i,j],0)
    solver=cp_model.CpSolver()
    solver.parameters.num_workers=2
    solver.parameters.max_time_in_seconds=seconds
    solver.parameters.random_seed=2803
    start=time.monotonic()
    st=solver.solve(m)
    out={'period':p,'width':4,'status':solver.status_name(st),
         'seconds':round(time.monotonic()-start,3),
         'best_bound':solver.best_objective_bound,'workers':2,
         'objective':'2X-N_re','current':0,'required_repaired_ends':repair_count}
    if st not in (cp_model.OPTIMAL,cp_model.FEASIBLE):
        return out
    chosen=[e for i,e in enumerate(es) if solver.value(selected[i])]
    gotx=solver.value(x); gotre=solver.value(nre)
    out.update(X=gotx,N_re=gotre,objective_value=solver.objective_value,edges=chosen)

    # Trace actual endpoints in the infinite cover, independently of labels.
    def neighbors(a):
        result=[]
        for u,v in chosen:
            if wrap(a)==wrap(u):
                result.append((v[0],a[1]+v[1]-u[1]))
            if wrap(a)==wrap(v):
                result.append((u[0],a[1]+u[1]-v[1]))
        return result
    repaired=0; visited=set()
    for root in ports:
        previous=None; a=root; path=[]
        while True:
            path.append(a); visited.add(wrap(a))
            assert len(path)<=4*p+1
            if previous is not None and a[0]>=2:
                break
            nxt=[v for v in neighbors(a) if v!=previous]
            assert len(nxt)==1
            previous,a=a,nxt[0]
        c=root[0]-2*root[1]
        want=c+(3 if c%2 else -3)
        repaired+=a[0]-2*a[1]!=want
    assert repaired==gotre
    for root in cells:
        if root in visited:
            continue
        previous=None; a=root; seen={}
        while wrap(a) not in seen:
            seen[wrap(a)]=a; visited.add(wrap(a))
            assert a[0]<2
            ns=neighbors(a)
            assert len(ns)==2
            nxt=next(v for v in ns if v!=previous)
            previous,a=a,nxt
        assert a[1]!=seen[wrap(a)][1], 'finite cycle'
    # Recount using the earlier lower row as owner, instead of the later.
    unrolled=[]
    for e in chosen+forced:
        for k in range(-3,4):
            f=translate(e,k*p)
            if -2<=min(y for x,y in f)<p+2:
                unrolled.append(f)
    direct=sum(cross(e,f) for e,f in combinations(unrolled,2)
               if 0<=min(min(y for x,y in e),min(y for x,y in f))<p)
    assert direct==gotx
    assert 2*gotx-gotre==solver.objective_value
    out['independent_cover_check']='PASS'
    return out

if __name__=='__main__':
    maximum=int(sys.argv[1]) if len(sys.argv)>1 else 8
    seconds=float(sys.argv[2]) if len(sys.argv)>2 else 90
    results=[]
    for p in range(1,maximum+1):
        r=run(p,seconds); results.append(r)
        Path('gap/verifier/claim28_pairing.json').write_text(json.dumps({'date':'2026-10-03','results':results},indent=2))
        print({k:v for k,v in r.items() if k!='edges'},flush=True)
