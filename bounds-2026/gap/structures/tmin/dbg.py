import sys; sys.argv=['x']
from tmin import *
n=8
m,P,T=build(n,'2f',0)
s=cp_model.CpSolver(); s.parameters.num_workers=2; s.parameters.max_time_in_seconds=20; s.parameters.log_search_progress=True
st=s.Solve(m); print(s.StatusName(st), s.ObjectiveValue(), s.BestObjectiveBound())
