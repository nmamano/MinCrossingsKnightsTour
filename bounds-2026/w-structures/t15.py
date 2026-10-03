from seam import Seam, solve
# same family B' (dir (1,2), form 2x-y) on both sides; seam along T; shift by k lines (off2 = k, s = 1)
cases = {'horiz': ((2, 0), (0, 1)), 'vert': ((0, 2), (1, 0)), 'diag': ((2, 2), (-1, 1)), 'anti': ((2, -2), (1, 1)), 'dirB': ((1, 2), (2, -1))}
for name, (T, hv) in cases.items():
    if T == (1, 2):
        continue
    for k in (1, 3):
        best = None
        for w in (2, 3):
            st = Seam(T=T, hv=hv, w1=w, w2=w, f1=(1, 2), form1=(2, -1), f2=(1, 2), form2=(2, -1), s=1, off2=k)
            r = solve(st, time_limit=60, workers=2)
            lines = abs(st.delta)
            if 'X' in r:
                print(name, 'shift', k, 'w', w, r['status'], 'X/period', r['X'], 'lines/period', lines, 'X per line %.3f' % (r['X'] / lines), flush=True)
            else:
                print(name, 'shift', k, 'w', w, r['status'], flush=True)
