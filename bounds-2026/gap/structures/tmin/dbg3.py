import sys; sys.argv=['x']
from tmin import *
n=8
m,P,T=build(n,'2f',0)
m.Add(T<=35)
s=cp_model.CpSolver(); s.parameters.num_workers=2; s.parameters.max_time_in_seconds=20
st=s.Solve(m); print(s.StatusName(st))
m,P,T=build(n,'2f',0)
s=cp_model.CpSolver(); s.parameters.num_workers=2; s.parameters.max_time_in_seconds=10;s.parameters.cp_model_presolve=False
st=s.Solve(m); print(s.StatusName(st), s.ObjectiveValue(), s.BestObjectiveBound())
