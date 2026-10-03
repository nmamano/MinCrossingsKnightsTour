"""Left-edge turns menu. All solves are serial, with one CP-SAT worker."""
import importlib.util
import json
import sys
import time
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from kt.strip import Strip
from kt.search import build_model, to_template
from kt.core import MI, MJ
from ortools.sat.python import cp_model

ROOT=Path(__file__).resolve().parents[1]
OUT=Path(__file__).parent
spec=importlib.util.spec_from_file_location('edge_check',ROOT/'w-searcher/verify.py')
edge_check=importlib.util.module_from_spec(spec)
spec.loader.exec_module(edge_check)

def verify(tpl,d=None,par=None):
    rows=[r.split() for r in tpl]; Q,D=len(rows),len(rows[0])
    def nb(u):
        x,y=u
        return [(x+MJ[int(k)],y-MI[int(k)]) for k in rows[Q-1-y%Q][x]]
    covered=set(); pairs=set(); signed=set(); turns=0
    for y in range(Q):
        for x in range(D):
            u=(x,y); a,b=nb(u)
            assert min(a[0],b[0])>=0
            turns += (a[0]+b[0],a[1]+b[1]) != (2*x,2*y)
            for v in (a,b):
                if v[0]<D: assert u in nb(v)
                else: assert (v[0]-x,v[1]-y)==(2,-1)
    for x in (D-2,D-1):
        for y in range(Q):
            u=(x,y); prev,cur=(x+2,y-1),u
            assert prev in nb(u)
            seen=set()
            for _ in range(Q*D+1):
                canon=(cur[0],cur[1]%Q)
                assert canon not in seen, 'finite cycle or winding path'
                seen.add(canon);covered.add(canon)
                nxt=[v for v in nb(cur) if v!=prev]
                assert len(nxt)==1
                prev,cur=cur,nxt[0]
                if cur[0]>=D:
                    a=x+2*y; b=prev[0]+2*prev[1]
                    lo,hi=sorted((a,b))
                    assert a!=b
                    if d is not None: assert hi-lo==d and lo%2==par
                    pairs.add((lo%(2*Q),hi-lo))
                    signed.add((a%(2*Q),b-a))
                    break
            else: raise AssertionError('path did not end')
    assert len(covered)==Q*D
    check=edge_check.check('left',tpl,K=8)
    assert not [e for e in check['bad'] if e[0]!='trace']
    assert check['T_per_period']==turns
    return dict(T=int(turns),X=check['X_per_period'],pairing=sorted(pairs),
        signed_offsets=sorted(signed),all_cells_on_finite_paths=True,
        unrolled=check,cper=2*Q)

def exact_turns(m,x,st):
    straight=[]
    for u in st.base:
        dirs={d:x[i] for i,d in st.inc[u]}
        dirs.update({d:1 for d in st.fixed_inc[u]})
        local=[]
        for d,a in dirs.items():
            nd=(-d[0],-d[1])
            if nd in dirs and d>nd:
                b=dirs[nd];z=m.NewBoolVar('exact_straight')
                m.Add(z<=a);m.Add(z<=b);m.Add(z>=a+b-1)
                local.append(z)
        m.Add(sum(local)<=1)
        straight.extend(local)
    return len(st.base)-sum(straight)

def seed(st,rule):
    rows=[json.loads(l) for l in (ROOT/'w-searcher/menu_results.jsonl').read_text().splitlines()]
    candidates=[r for r in rows if r['kind']=='left' and r['rule']==rule and 'tpl' in r
                and r['D']<=st.D and st.P%r['P']==0]
    if not candidates:return None
    r=min(candidates,key=lambda r:(r['T']/r['P'],r['X']/r['P']))
    rr=[row.split()+['26']*(st.D-r['D']) for row in r['tpl']]*(st.P//r['P'])
    chosen=[]
    for i,(u,v) in enumerate(st.var_edges):
        code=rr[st.P-1-u[1]][u[0]]
        if (v[0]-u[0],v[1]-u[1]) in [(MJ[int(k)],-MI[int(k)]) for k in code]:chosen.append(i)
    st.evaluate(chosen)
    return chosen

def run_case(Q,D,d=None,par=None,seconds=12):
    name='free' if d is None else f'd={d} low%2={par}'
    st=Strip('left',Q,D)
    hint=seed(st,name)
    m,x,X,_=build_model(st,wX=0,wT=1,lanes=False,hint=hint)
    T=exact_turns(m,x,st)
    m.Minimize(T)
    if d is not None:
        # Fixed class determines a unique partner for each terminal.
        # The label is the smaller line number of that pair.
        n=Q*D; cs=[st.line_of(u) for u in st.terminals]
        labels={u:m.NewIntVar(min(cs)-4*n-d,max(cs)+4*n+d,'pair_root') for u in st.base}
        for u in st.terminals:
            c=st.line_of(u)
            m.Add(labels[u] == (c if c%2==par else c-d))
        for i,(u,v) in enumerate(st.var_edges):
            vb,k=st.canon(v)
            m.Add(labels[u]==labels[vb]+k*2*Q).OnlyEnforceIf(x[i])
    sol=cp_model.CpSolver();sol.parameters.num_workers=1
    sol.parameters.max_time_in_seconds=seconds
    start=time.monotonic(); status=sol.Solve(m)
    r=dict(date='2026-10-02',kind='left',Q=Q,P=Q,D=D,rule=name,d=d,parity=par,
           turn_status=sol.StatusName(status),turn_bound=sol.BestObjectiveBound(),
           turn_seconds=round(time.monotonic()-start,3),workers=1)
    if status in (cp_model.OPTIMAL,cp_model.FEASIBLE):
        chosen=[i for i,v in enumerate(x) if sol.Value(v)]
        a,b=st.evaluate(chosen)
        assert sol.Value(T)==b
        r.update(T=b,X=a,chosen=chosen,tpl=to_template(st,chosen))
        m.Add(T==b);m.Minimize(X)
        m.ClearHints()
        for i in range(len(m.Proto().variables)):
            v=m.GetIntVarFromProtoIndex(i);m.AddHint(v,sol.Value(v))
        start=time.monotonic();status=sol.Solve(m)
        r.update(cross_status=sol.StatusName(status),cross_bound=sol.BestObjectiveBound(),
                 cross_seconds=round(time.monotonic()-start,3))
        if status in (cp_model.OPTIMAL,cp_model.FEASIBLE):
            chosen=[i for i,v in enumerate(x) if sol.Value(v)]
            a,b2=st.evaluate(chosen);assert b2==b
            r.update(X=a,chosen=chosen,tpl=to_template(st,chosen))
        r['check']=verify(r['tpl'],d,par)
        assert (r['check']['X'],r['check']['T'])==(r['X'],r['T'])
        r.update(T_rate=b/Q,X_rate=r['X']/Q)
        tag='free' if d is None else f'd{d}-p{par}'
        (OUT/f'left-{tag}-Q{Q}-D{D}-template.json').write_text(json.dumps(r['tpl'],indent=2)+'\n')
    with (OUT/'left_results.jsonl').open('a') as f:f.write(json.dumps(r)+'\n')
    print(json.dumps({k:v for k,v in r.items() if k not in ('chosen','tpl','check')}),flush=True)
    render()
    return r

def render():
    rows=[json.loads(l) for l in (OUT/'left_results.jsonl').read_text().splitlines()]
    groups={}
    for r in rows:groups.setdefault(r['rule'],[]).append(r)
    out=['# Minimum-turn LEFT gadget menu','', 'Date: 2026-10-02. One CP-SAT worker; all solves ran in sequence.',
         'Model: `kt/strip.py`, kind `left`, with the lane rule disabled. Q is rows per period; D is strip depth.',
         'Each fixed class joins {c,c+d}, where c is the smaller line number and has the stated parity. The line is x+2y=c.',
         'First minimize turns. Then fix that turn count and minimize crossings. Status T/X refers to these two solves for the selected size.',
         'OPTIMAL proves the optimum for that size. A best menu entry is not a proof across other sizes whose runs remain incomplete.',
         'Each template passes degree, symmetry, turn, crossing, and complete finite-path checks. Signed offsets and all run bounds are in `left_results.jsonl`.',
         'Pairing `a+d` means {c,c+d} for c mod (2Q)=a, with c the smaller line number. Rows in each template are top-first.', '',
         '| class | turns/row | crossings/row | status T / X | Q | D | pairing | template |',
         '| --- | ---: | ---: | --- | ---: | ---: | --- | --- |']
    missing=[]
    for name,rs in sorted(groups.items()):
        feasible=[r for r in rs if 'check' in r]
        if not feasible:
            missing.append((name,rs));continue
        r=min(feasible,key=lambda r:(r['T_rate'],r['X_rate'],r['turn_status']!='OPTIMAL',r['cross_status']!='OPTIMAL',r['D'],r['Q']))
        pair=' '.join(f'{a}+{d}' for a,d in r['check']['pairing'])
        out.append(f"| {name} | {r['T_rate']:g} | {r['X_rate']:g} | {r['turn_status']} / {r['cross_status']} | {r['Q']} | {r['D']} | {pair} | `{' / '.join(r['tpl'])}` |")
    out+=['','## Classes with no gadget found','']
    for name,rs in missing:
        out.append(name+': '+', '.join(f"Q{r['Q']} D{r['D']} {r['turn_status']}" for r in rs)+'.')
    out+=['','## All size results','', '| class | Q | D | T | X | turn status | turn bound | cross status | cross bound |', '| --- | ---: | ---: | ---: | ---: | --- | ---: | --- | ---: |']
    for r in rows:
        out.append(f"| {r['rule']} | {r['Q']} | {r['D']} | {r.get('T','—')} | {r.get('X','—')} | {r['turn_status']} | {r['turn_bound']} | {r.get('cross_status','—')} | {r.get('cross_bound','—')} |")
    (OUT/'LEFT_MENU.md').write_text('\n'.join(out)+'\n')

if __name__=='__main__':
    rules=[(None,None)]+[(d,p) for d in (1,3,5,7,9) for p in (0,1)]
    for d,p in rules:
        for Q in (4,8):
            for D in (2,3,4):run_case(Q,D,d,p)
