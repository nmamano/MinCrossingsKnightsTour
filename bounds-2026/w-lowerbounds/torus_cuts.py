import sys
from collections import Counter
from ortools.sat.python import cp_model
from strip_dp import cross
exec(open('torus_flux_mod3.py').read().split("class CB")[0].replace("p=int(sys.argv[1]); q=int(sys.argv[2]); tl=int(sys.argv[3]) if len(sys.argv)>3 else 600","p=int(sys.argv[1]); q=int(sys.argv[2]); tl=600"))
rows=Counter()
class CB(cp_model.CpSolverSolutionCallback):
    def __init__(s): super().__init__()
    def on_solution_callback(s):
        ch=[e for e in E if s.Value(xv[e])]
        cnt=Counter()
        for (x,y,dx,dy) in ch:
            if dy>0 and y+dy>=q: cnt[((dx,dy), chi(x,y), y+dy-q)]+=1   # (type, colour of lower end, row offset)
        h,v=flux(ch)
        key=(h,tuple(sorted(cnt.items())))
        rows[key]+=1
s=cp_model.CpSolver(); s.parameters.enumerate_all_solutions=True; s.parameters.num_workers=1; s.parameters.max_time_in_seconds=tl
s.Solve(m,CB())
for k,v in sorted(rows.items(), key=lambda t:-t[1])[:25]: print(v, 'flux',k[0], k[1])
print('distinct',len(rows))
