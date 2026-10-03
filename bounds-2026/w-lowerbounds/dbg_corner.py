import os, sys, itertools
os.environ['STRAIGHT']='1'; os.environ['NOX']='1'
sys.argv=['x','12','2','P','P','60']
src=open('corner_neutral.py').read().split("s=cp_model.CpSolver()")[0]
exec(src)
Z=[]
for e,f in itertools.combinations(E,2):
    if (e in forced and f in forced) or box(e) or box(f): continue
    if cross((*e[0],*e[1]),(*f[0],*f[1])):
        z=m.NewBoolVar(''); m.AddBoolOr([xv[e].Not(),xv[f].Not(),z]); Z.append((z,e,f))
m.Minimize(sum(z for z,e,f in Z))
s=cp_model.CpSolver(); s.parameters.num_workers=2; s.parameters.max_time_in_seconds=120
st=s.Solve(m); print(s.StatusName(st), s.ObjectiveValue())
for z,e,f in Z:
    if s.Value(z): print(e,f)
