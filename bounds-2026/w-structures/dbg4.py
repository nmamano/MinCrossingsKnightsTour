from seam import Seam, solve
from unroll import check
for s in (1,2,3,4,6,12):
  for off2 in range(-s, s+1):
    st = Seam(T=(4,4), hv=(-1,1), w1=3, w2=3, f1=(2,-1), form1=(1,2), f2=(1,-2), form2=(2,1), s=s, off2=off2)
    r = solve(st, time_limit=10)
    if r['status'] != 'INFEASIBLE': print(s, off2, r['status'], r['X'], r['T'])
st = Seam(T=(4,4), hv=(-1,1), w1=3, w2=3, f1=(2,-1), form1=(1,2), f2=(1,-2), form2=(2,1), s=1)
r = solve(st, time_limit=10, lanes=False)
c = check(st, r['chosen'])
print(sorted((a[3], a[4]) for a in c['sample']))
import unroll
