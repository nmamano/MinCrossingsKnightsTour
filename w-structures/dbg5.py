from seam import Seam, solve, build_model
from unroll import check
from ortools.sat.python import cp_model
st = Seam(T=(4,4), hv=(-1,1), w1=3, w2=3, f1=(2,-1), form1=(1,2), f2=(1,-2), form2=(2,1), s=1)
m, x = build_model(st, lanes=False)
# enumerate several solutions with X<=6
s = cp_model.CpSolver(); s.parameters.num_workers=1; s.parameters.max_time_in_seconds=5
seen=set()
for it in range(12):
    r = s.Solve(m)
    if r not in (cp_model.OPTIMAL, cp_model.FEASIBLE): break
    ch = [i for i in range(len(x)) if s.Value(x[i])]
    c = check(st, ch)
    mp = sorted(set(((a[3]) % 12, a[4]-a[3]) for a in c['sample']))
    full = check(st, ch)
    print(st.evaluate(ch), sorted(set((a[3]%12, a[4]-a[3]) for a in full['sample'])))
    m.AddBoolOr([x[i].Not() for i in ch])
