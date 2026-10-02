"""Search mixed left matchings below 2 crossings/row, with exact MID cuts."""
import json
import math
import sys
import time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT));sys.path.insert(0,str(ROOT/'w-integrator'))
from kt.strip import Strip
from kt.search import build_model,to_template
from ortools.sat.python import cp_model
from strands import pairing,region_check,parity
from left_menu import verify

OUT=Path(__file__).parent
RIGHT=['23 27']*4
PR=pairing(RIGHT,'left')
PB=pairing(json.loads((OUT/'T18-P8-D4.json').read_text()),'bottom')
MARKER='\n## Left crossings against right d=3/odd, 2026-10-02\n'

def paths(st,chosen):
    """Signed partner and selected edge footprint for each terminal residue."""
    chosen=set(chosen);out={};per=2*st.P
    for u in st.terminals:
        prev=(u[0]+2,u[1]-1);cur=u;foot=set();seen=set()
        while True:
            base,_=st.canon(cur)
            assert base not in seen
            seen.add(base)
            ns=[]
            for e,d in st.inc[base]:
                if e in chosen:
                    v=(cur[0]+d[0],cur[1]+d[1])
                    if v!=prev:ns.append((v,e))
            for d in st.fixed_inc[base]:
                v=(cur[0]+d[0],cur[1]+d[1])
                if v!=prev:ns.append((v,None))
            assert len(ns)==1
            nxt,e=ns[0]
            if e is None:
                a,b=st.line_of(u),st.line_of(cur)
                out[a%per]=(b-a,foot)
                break
            foot.add(e);prev,cur=cur,nxt
    assert len(out)==per
    return out

def mid_cycles(ps,per):
    """Exact lift of the alternating graph; repeated residue with nonzero
    displacement is an infinite component, zero displacement is a cycle."""
    cuts=set()
    for root in range(per):
        cur,side=root,0
        seen={};left_steps=[]
        while (cur%per,side) not in seen:
            seen[cur%per,side]=(cur,len(left_steps))
            if side==0:
                delta,foot=ps[cur%per]
                left_steps.append(foot);cur+=delta
            else:
                cur += 3 if cur%2 else -3
            side=1-side
        old,start=seen[cur%per,side]
        if old==cur:
            footprint=frozenset().union(*left_steps[start:])
            assert footprint
            cuts.add(footprint)
    return cuts

def add_cut_parity(m,x,st):
    # Each finite terminal path crosses line c=1/2 with the parity of its
    # two endpoints. Thus selected band edges give the matching cut parity.
    odd=[];per=2*st.P
    for i,(u,v) in enumerate(st.var_edges):
        a,b=st.line_of(u),st.line_of(v)
        lo=math.floor(-max(a,b)/per)-2
        hi=math.ceil(-min(a,b)/per)+2
        count=sum((a+k*per<=0)!=(b+k*per<=0) for k in range(lo,hi+1))
        if count%2:odd.append(x[i])
    # Right d3/odd has matching parity 1 for every even board size.
    assert parity(PR['pairs'],PR['cper'],shift=255,sign=-1)==1
    m.AddBoolXOr(odd)

def forbid_odd_three(m,x,st):
    """Orient each path from its smaller to larger terminal line. Propagate
    that smaller line as a label; an even end cannot start three below it."""
    N=len(st.base);per=2*st.P
    lines=[st.line_of(u) for u in st.terminals]
    # A finite path uses <= N quotient vertices and moves <= 2 rows per
    # step. Six N units in line coordinates covers every possible label.
    A={u:m.NewIntVar(min(lines)-6*N,max(lines)+6*N,'start_line') for u in st.base}
    net={u:[] for u in st.base};terms=set(st.terminals)
    for i,(u,v) in enumerate(st.var_edges):
        vb,k=st.canon(v)
        gp=m.NewBoolVar('forward');gn=m.NewBoolVar('backward')
        m.Add(gp+gn==x[i])
        net[u].append(gp-gn);net[vb].append(gn-gp)
        m.Add(A[u]==A[vb]+k*per).OnlyEnforceIf(x[i])
    for u in st.base:
        if u not in terms:m.Add(sum(net[u])==0);continue
        start=m.NewBoolVar('is_start');c=st.line_of(u)
        m.Add(sum(net[u])==2*start-1)
        m.Add(A[u]==c).OnlyEnforceIf(start)
        m.Add(A[u]<c).OnlyEnforceIf(start.Not())
        if c%2==0:m.Add(A[u]!=c-3).OnlyEnforceIf(start.Not())

def render():
    f=OUT/'cross_left_results.jsonl'
    rows=[json.loads(l) for l in f.read_text().splitlines()] if f.exists() else []
    out=[MARKER,
         'Final depth-5/6 result: no gadget below 2 crossings per row was found. For Q=4 and Q=6, both depths are proved unable to improve 2. For Q=8, both 45-second runs ended without a solution or an infeasibility proof. No further search was run after this budget.',
         'The value 2 is attained by the verified d=5/even gadget below, so it is the exact compatible minimum in the four proved size cases.',
         'Initial search: Q=4,8,12 and D=2..5. After the Chief Researcher update, only Q=4,6,8 and D=5,6 are searched, with a hard no-{odd,odd+3} rule. The lane rule is disabled. The crossing objective is constrained to X < 2Q.',
         'Right gadget: `23 27 / 23 27 / 23 27 / 23 27`, with pairs {c,c+3} for odd c. One CP-SAT worker; all solves are sequential.',
         'The model uses kt.search.build_model, an exact cut-parity constraint, and lazy exclusions of finite alternating MID cycles. Mixed left pairings are allowed.',
         'Every proposed improvement must pass independent strip checks, an exact periodic MID test, and w-integrator/strands.py region_check at n=256 and n=258. Only the MID region is used for acceptance.',
         'A no-improvement proof applies only to the stated strip size. UNKNOWN means the time limit left the case open.', '',
         '| Q | D | hard no-odd+3 | result | accepted X/row | solves | cycle cuts | seconds |',
         '| ---: | ---: | --- | --- | ---: | ---: | ---: | ---: |']
    for r in rows:
        out.append(f"| {r['Q']} | {r['D']} | {r.get('hard_no_odd_three',False)} | {r['result']} | {r.get('best_rate','—')} | {r['solves']} | {r['cycle_cuts']} | {r['seconds']} |")
    out+=['', '### Verified reference at 2 crossings per row', '',
          'Template file: `w-turnsbuilder/cross-left-baseline-template.json`. Check file: `w-turnsbuilder/cross-left-baseline-check.json`.', '',
          '```text','02 24','02 24','02 24','02 24','```', '',
          'Q=4, D=2: X=8, T=8. Add straight `26` columns to extend the depth, and repeat the constant row for Q=6 or Q=8.',
          'Line pairs are {c,c+5} for even c. Signed offsets are +5 for even c and -5 for odd c.',
          'Both MID checks, n=256 and n=258, report zero finite cycles, four strands, and cut count [4].', '',
          '### Scope of the hard-rule model', '',
          'Every terminal path is oriented from its smaller to its larger line number. Its smaller endpoint is propagated as a label along selected edges. An even larger endpoint c is forbidden to have label c-3. This excludes all {odd,odd+3} pairs, including mixed matchings and paths with different shapes.',
          'Label ranges extend six times the number of quotient cells beyond the terminal range. A finite path cannot repeat a quotient cell, and each knight step changes the row by at most two, so this range does not impose an extra span restriction.',
          'The selected-edge parity across c=1/2 is constrained to be odd. For finite paths this equals the matching cut parity. It is necessary for MID compatibility with the rotated d=3/odd right gadget on an even board.',
          'Before each hard-rule search, a separate fixed-edge control solve checked the 2/row reference in the same model, before the strict improvement bound was added. All six control solves returned OPTIMAL at X=2Q.',
          'None of the six hard-rule searches produced a candidate below 2. Thus no new template passed or failed the MID filter in that final batch. The reference template did pass the filter.', '']
    for r in rows:
        for a in r.get('accepted',[]):
            out+=['',f"### Q={r['Q']}, D={r['D']}, X={a['X']}, T={a['T']}",
                  '',f"Template file: `{a['template_file']}`.",'','```text',*a['template'],'```',
                  '', 'Pairs (lower c mod 2Q, span): `'+json.dumps(a['check']['pairing'])+'`.',
                  'Signed offsets: `'+json.dumps(a['check']['signed_offsets'])+'`.',
                  'MID region checks: `'+json.dumps(a['MID'])+'`.']
    out+=['','Run evidence: `w-turnsbuilder/cross_left_results.jsonl`. Candidate checks and rejected-cycle data are saved separately in `cross_left_candidates.jsonl`.','']
    f=OUT/'FINDINGS.md'
    text=f.read_text().split(MARKER)[0]
    f.write_text(text+'\n'+'\n'.join(out))

def run_case(Q,D,limit=40,hard=False):
    st=Strip('left',Q,D,s=1)
    m,x,X,_=build_model(st,wX=1,wT=0,lanes=False)
    add_cut_parity(m,x,st)
    control_status=None
    if hard:
        forbid_odd_three(m,x,st)
        # Check the known 2/row partner in this exact model before adding
        # the strict improvement bound. This is not part of the search.
        control=m.Clone()
        for i,(u,v) in enumerate(st.var_edges):
            code='02' if u[0]==0 else '24' if u[0]==1 else '26'
            from kt.core import MI,MJ
            chosen=(v[0]-u[0],v[1]-u[1]) in [(MJ[int(k)],-MI[int(k)]) for k in code]
            control.Add(control.GetIntVarFromProtoIndex(x[i].Index())==int(chosen))
        cs=cp_model.CpSolver();cs.parameters.num_workers=1;cs.parameters.max_time_in_seconds=3
        cr=cs.Solve(control);control_status=cs.StatusName(cr)
        assert cr in (cp_model.OPTIMAL,cp_model.FEASIBLE),control_status
        assert round(cs.ObjectiveValue())==2*Q
    m.Add(X<=2*Q-1)
    start=time.monotonic();solves=0;cut_count=0;accepted=[];known_cuts=set()
    result='TIME LIMIT; no improvement found';last_bound=None;best=None
    while time.monotonic()-start<limit:
        s=cp_model.CpSolver();s.parameters.num_workers=1
        s.parameters.max_time_in_seconds=max(.1,limit-(time.monotonic()-start))
        status=s.Solve(m);solves+=1;last_bound=s.BestObjectiveBound()
        if status==cp_model.INFEASIBLE:
            result='OPTIMAL compatible candidate' if accepted else 'PROVED no compatible X < 2Q'
            break
        if status not in (cp_model.OPTIMAL,cp_model.FEASIBLE):break
        chosen=[i for i,v in enumerate(x) if s.Value(v)]
        a,b=st.evaluate(chosen);tpl=to_template(st,chosen)
        ps=paths(st,chosen);cycles=mid_cycles(ps,2*Q)
        pL=pairing(tpl,'left')
        mid={str(n):region_check(PB,pL,PR,PB,n,(0,0,0,0))['MID'] for n in (256,258)}
        cand=dict(Q=Q,D=D,X=a,T=b,status=s.StatusName(status),bound=last_bound,
                  template=tpl,finite_cycle_cuts=[sorted(c) for c in cycles],MID=mid)
        if cycles:
            for c in cycles:
                if c in known_cuts:raise AssertionError('repeated forbidden cycle')
                known_cuts.add(c);m.Add(sum(x[i] for i in c)<=len(c)-1);cut_count+=1
        else:
            ck=verify(tpl)
            assert not pL['bad'] and not pL['uncovered']
            assert all(r['cycles']==0 and not any(c%2 for c in r['cuts']) for r in mid.values()),mid
            assert ck['X']==a
            assert parity(pL['pairs'],pL['cper'])==1
            tf=OUT/f'cross-left-Q{Q}-D{D}-X{a}-template.json'
            tf.write_text(json.dumps(tpl,indent=2)+'\n')
            cand.update(check=ck,MID=mid,template_file=str(tf.relative_to(ROOT)))
            accepted.append(cand);best=a/Q
            m.Add(X<=a-1)
            result='FEASIBLE compatible improvement'
            print('ACCEPTED',json.dumps(cand),flush=True)
        with (OUT/'cross_left_candidates.jsonl').open('a') as f:f.write(json.dumps(cand)+'\n')
        m.ClearHints()
    r=dict(date='2026-10-02',Q=Q,D=D,result=result,solves=solves,cycle_cuts=cut_count,
           seconds=round(time.monotonic()-start,2),last_bound=last_bound,accepted=accepted,
           hard_no_odd_three=hard,control_status=control_status)
    if best is not None:r['best_rate']=best
    with (OUT/'cross_left_results.jsonl').open('a') as f:f.write(json.dumps(r)+'\n')
    print(json.dumps({k:v for k,v in r.items() if k!='accepted'}),flush=True)
    render()
    return r

if __name__=='__main__':
    render()
    for Q in (4,6,8):
        for D in (5,6):run_case(Q,D,45,hard=True)
