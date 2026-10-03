from seam import Seam, solve
# trivial A|A seam along diagonal: should be 0 crossings, identity
for s in (1,4):
    st = Seam(T=(4,4), hv=(-1,1), w1=2, w2=2, f1=(2,-1), form1=(1,2), f2=(2,-1), form2=(1,2), s=s)
    print('AA', s, solve(st, time_limit=10)['status'])
# A|B gentle, bigger
for p in (8,):
  for w in (2,3,4,5):
    for off2 in range(4):
        st = Seam(T=(p,p), hv=(-1,1), w1=w, w2=w, f1=(2,-1), form1=(1,2), f2=(1,-2), form2=(2,1), s=4, off2=off2)
        r = solve(st, time_limit=30)
        print(p, w, off2, r['status'], r.get('X'), r.get('T'), r.get('bound'))
