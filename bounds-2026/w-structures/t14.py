from seam import Seam, solve
for P in (2, 3, 4, 6, 8):
    for D in (3, 4):
        st = Seam(T=(P, 0), hv=(0, -1), w1=D - 1, w2=0, f1=(2, -1), form1=(1, 2), s=1)
        r = solve(st, time_limit=60, workers=2, lanes=False)
        print('shallow bottom no lanes P', P, 'D', D, r['status'], r.get('X'), r.get('T'), 'per col', r['X'] / P if 'X' in r else None, flush=True)
