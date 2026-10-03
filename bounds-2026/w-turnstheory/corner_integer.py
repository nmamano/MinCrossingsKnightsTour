from itertools import combinations
from ortools.sat.python import cp_model
from check_corner_certificate import M,lower
for K in [4,5,6]:
    C={(x,y) for x in range(K) for y in range(K)}
    m=cp_model.CpModel();pv={};inc={};cost=[]
    for p in sorted(C):
        opts=[]
        for a,b in combinations([d for d in M if p[0]+d[0]>=0 and p[1]+d[1]>=0],2):
            z=m.NewBoolVar('');pv[p,a,b]=z;opts.append(z)
            for d in (a,b):
                q=(p[0]+d[0],p[1]+d[1]);inc.setdefault((p,q),[]).append(z)
            t=int(a[0]+b[0]!=0 or a[1]+b[1]!=0)
            cost.append((t-lower(p[0],[a[0],b[0]])-lower(p[1],[a[1],b[1]]))*z)
        m.Add(sum(opts)==1)
    for p,q in inc:
        if q in C and p<q:m.Add(sum(inc[p,q])==sum(inc[q,p]))
    m.Minimize(sum(cost))
    for trial in range(10):
        s=cp_model.CpSolver();s.parameters.num_workers=1;s.parameters.max_time_in_seconds=3
        st=s.Solve(m)
        print('K',K,'trial',trial,s.StatusName(st),'objective',s.ObjectiveValue(),'bound',s.BestObjectiveBound(),flush=True)
        if st not in (cp_model.FEASIBLE,cp_model.OPTIMAL):break
        chosen=[(p,a,b) for (p,a,b),v in pv.items() if s.Value(v)]
        adj={p:[] for p in C}
        for p,a,b in chosen:
            for d in (a,b):
                q=(p[0]+d[0],p[1]+d[1])
                if q in C:adj[p].append(q)
        seen=set();cycles=[]
        for p in C:
            if p in seen:continue
            stack=[p];comp=set()
            while stack:
                v=stack.pop()
                if v in comp:continue
                comp.add(v);stack.extend(adj[v])
            seen|=comp
            if all(len(adj[v])==2 for v in comp):cycles.append(comp)
        if not cycles:
            print('No internal cycle.',flush=True)
            if K==4:
                for p,a,b in chosen:print(p,a,b)
            break
        for comp in cycles:
            es=[sum(inc[p,q]) for p in comp for q in adj[p] if p<q]
            m.Add(sum(es)<=len(comp)-1)
