"""One solver at a time. Preserve every candidate before verification."""
import json
import sys
import time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from kt.strip import Strip
from kt.search import build_model, to_template
from kt.verify_strip import check_bottom, unroll_bottom
from kt.core import MI, MJ
from ortools.sat.python import cp_model
from run import verify

OUT = Path(__file__).parent

def seed_edges(st, tpl):
    rows = [r.split() for r in tpl]
    oldD, oldP = len(rows), len(rows[0])
    def codes(u):
        x,y = u
        return rows[oldD-1-y][x % oldP] if y < oldD else '26'
    chosen=[]
    for i,(u,v) in enumerate(st.var_edges):
        ds = [(MJ[int(k)],-MI[int(k)]) for k in codes(u)]
        if (v[0]-u[0],v[1]-u[1]) in ds:
            chosen.append(i)
    st.evaluate(chosen)
    return chosen

def checks(tpl):
    independent = verify(tpl)
    P,D=len(tpl[0].split()),len(tpl)
    # A finite path visits at most P*D quotient cells. Its x span is at
    # most 2*P*D. This unroll leaves more than that on both sides.
    K=4*D+8
    adj,_,_,_ = unroll_bottom(tpl,K)
    pairs=[]
    for x in range((K//2)*P,(K//2+1)*P):
        prev,cur=(x-2,D),(x,D-1)
        for _ in range(P*D+1):
            ns=[v for v in adj[cur] if v!=prev]
            assert len(ns)==1, (cur,ns)
            prev,cur=cur,ns[0]
            if cur[1]>=D:
                pairs.append((x+2*(D-1),prev[0]+2*prev[1]))
                break
        else: raise AssertionError('center path did not end')
    lane_ok=all(a//8==b//8 and (a//4)%2!=(b//4)%2 for a,b in pairs)
    independent.update(center_periods=K,center_lane_ok=lane_ok,
        pairing_offsets=sorted([[a%P,b-a] for a,b in independent['line_pairing']]))
    legacy=check_bottom(tpl,K=6)
    assert not legacy['bad']
    return dict(independent=independent,unrolled=legacy)

def solve_case(P,D,lanes,seconds=45,seed=True,lex=None,tag=None):
    st=Strip('bottom',P,D)
    tpl=json.loads((OUT/'T18-P8-D4.json').read_text())
    hint=seed_edges(st,tpl) if seed else None
    if lex is not None: hint=lex['chosen']
    m,x,X,T=build_model(st,wX=0,wT=1,lanes=lanes,hint=hint)
    if seed: m.Add(T <= 18*P//8)
    if lex is not None:
        # The shared model's straight indicators have one-way constraints.
        # Make exact indicators for a fixed-turn secondary objective.
        exact_straight=[]
        for u in st.base:
            dirs={d:x[i] for i,d in st.inc[u]}
            dirs.update({d:1 for d in st.fixed_inc[u]})
            for d,a in dirs.items():
                nd=(-d[0],-d[1])
                if nd in dirs and d>nd:
                    b=dirs[nd]
                    z=m.NewBoolVar('exact_straight')
                    m.Add(z<=a); m.Add(z<=b); m.Add(z>=a+b-1)
                    exact_straight.append(z)
        m.Add(len(st.base)-sum(exact_straight) == lex['T'])
        m.Minimize(X)
    solver=cp_model.CpSolver()
    solver.parameters.num_workers=1
    solver.parameters.max_time_in_seconds=seconds
    # Complete the edge-only hint with flow and label values. This is a
    # separate short solve with all hinted edge choices fixed.
    seed_status=None
    if hint:
        seed_solver=cp_model.CpSolver()
        seed_solver.parameters.num_workers=1
        seed_solver.parameters.max_time_in_seconds=5
        seed_solver.parameters.fix_variables_to_their_hinted_value=True
        sr=seed_solver.Solve(m)
        seed_status=seed_solver.StatusName(sr)
        if sr in (cp_model.OPTIMAL,cp_model.FEASIBLE):
            m.ClearHints()
            for i in range(len(m.Proto().variables)):
                v=m.GetIntVarFromProtoIndex(i)
                m.AddHint(v,seed_solver.Value(v))
    start=time.monotonic()
    status=solver.Solve(m)
    result=dict(date='2026-10-02',P=P,D=D,lanes=lanes,status=solver.StatusName(status),
        bound=solver.BestObjectiveBound(),time=round(time.monotonic()-start,2),
        objective='crossings with fixed turns' if lex else 'turns',seeded=seed)
    result['seed_solver_status']=seed_status
    path=OUT/(tag or f"{'lanes' if lanes else 'free'}-P{P}-D{D}.json")
    if status in (cp_model.OPTIMAL,cp_model.FEASIBLE):
        chosen=[i for i,v in enumerate(x) if solver.Value(v)]
        a,b=st.evaluate(chosen)
        result.update(chosen=chosen,X=a,T=b,template=to_template(st,chosen),obj=solver.ObjectiveValue())
    elif hint:
        a,b=st.evaluate(hint)
        result.update(chosen=hint,X=a,T=b,template=to_template(st,hint),
            candidate_source='verified input seed; main solver returned no solution')
    path.write_text(json.dumps(result,indent=2)+'\n')
    if 'chosen' in result:
        result.update(checks(result['template']))
        assert result['independent']['turns']==result['T']
        assert result['unrolled']['crossings_per_period']==result['X']
        if lanes: assert result['independent']['center_lane_ok']
        path.write_text(json.dumps(result,indent=2)+'\n')
        (OUT/(path.stem+'-template.json')).write_text(json.dumps(result['template'],indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('chosen','template','independent','unrolled')}),flush=True)
    return result

if __name__=='__main__':
    mode=sys.argv[1]
    if mode=='diagnose': solve_case(8,5,True,30,False,tag='diagnose-P8-D5.json')
    if mode=='lanes':
        for P,D in ((8,5),(16,4),(16,5),(24,4),(24,5)):
            solve_case(P,D,True,60)
    if mode=='free':
        for P,D in ((8,4),(8,5),(16,4),(16,5),(24,4),(24,5)):
            solve_case(P,D,False,45)
    if mode=='lex':
        for name in sys.argv[2:]:
            r=json.loads((OUT/name).read_text())
            solve_case(r['P'],r['D'],r['lanes'],60,True,lex=r,tag='lex-'+name)
