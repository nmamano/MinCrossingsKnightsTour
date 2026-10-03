"""Exact minimum crossings on small n x n boards: 2-factors vs closed tours (lazy subtour cuts)."""
import sys, itertools, time
from ortools.sat.python import cp_model
import networkx as nx
from strip_dp import cross
MOV=[(1,2),(2,1),(2,-1),(1,-2)]
def solve(n, tour, tlimit=600, threads=2):
    on=lambda p:0<=p[0]<n and 0<=p[1]<n
    E=[]
    for x in range(n):
        for y in range(n):
            for d in MOV:
                q=(x+d[0],y+d[1])
                if on(q): E.append(((x,y),q))
    m=cp_model.CpModel(); xv={e:m.NewBoolVar('') for e in E}
    inc={(x,y):[] for x in range(n) for y in range(n)}
    for e in E: inc[e[0]].append(e); inc[e[1]].append(e)
    for c in inc: m.Add(sum(xv[e] for e in inc[c])==2)
    Z=[]
    for e,f in itertools.combinations(E,2):
        if abs(e[0][0]-f[0][0])<=3 and abs(e[0][1]-f[0][1])<=3 and cross((*e[0],*e[1]),(*f[0],*f[1])):
            z=m.NewBoolVar(''); m.AddBoolOr([xv[e].Not(),xv[f].Not(),z]); Z.append(z)
    m.Minimize(sum(Z))
    t0=time.time()
    while True:
        s=cp_model.CpSolver(); s.parameters.num_workers=threads; s.parameters.max_time_in_seconds=tlimit
        st=s.Solve(m)
        ch=[e for e in E if s.Value(xv[e])]
        G=nx.Graph(); G.add_edges_from(ch); comps=list(nx.connected_components(G))
        if not tour or len(comps)==1:
            return s.ObjectiveValue(), s.BestObjectiveBound(), s.StatusName(st), len(comps), time.time()-t0
        for c in comps:
            m.Add(sum(xv[e] for e in E if (e[0] in c)!=(e[1] in c))>=2)
for n in map(int, sys.argv[2:]):
    r=solve(n, sys.argv[1]=='tour')
    print(sys.argv[1], 'n',n,'obj',r[0],'bound',r[1],r[2],'components',r[3],'time %.0f'%r[4], flush=True)
