from seam import Seam, solve
from unroll import check
for w in (2,3):
    st = Seam(T=(4,4), hv=(-1,1), w1=w, w2=w, f1=(2,-1), form1=(1,2), f2=(1,-2), form2=(2,1), s=1)
    r = solve(st, time_limit=20, lanes=False)
    c = check(st, r['chosen'])
    print(w, r['status'], r['X'], r['T'], [(a[3],a[4]) for a in c['sample']], c['bad'][:2])
    for off2 in range(-6, 7):
        st = Seam(T=(4,4), hv=(-1,1), w1=w, w2=w, f1=(2,-1), form1=(1,2), f2=(1,-2), form2=(2,1), s=1, off2=off2)
        r = solve(st, time_limit=20)
        print('  s=1 off2', off2, r['status'], r.get('X'), r.get('T'))
