import sys, json
from seam import Seam, solve
from unroll import check
p = int(sys.argv[1]); s = int(sys.argv[2]); tl = float(sys.argv[3])
for w in (2, 3, 4):
    for off2 in range(0, s):
        st = Seam(T=(p,p), hv=(-1,1), w1=w, w2=w, f1=(2,-1), form1=(1,2), f2=(1,-2), form2=(2,1), s=s, off1=0, off2=off2)
        r = solve(st, time_limit=tl, workers=1)
        line = f'p={p} s={s} w={w} off2={off2} n={len(st.base)} {r["status"]} {r["time"]}s'
        if 'X' in r:
            c = check(st, r['chosen'])
            line += f' X={r["X"]} T={r["T"]} bound={r["bound"]} per_x={r["X"]/p:.3f} chk={c["strands_ok"]},{c["X_per_period"]},{c["T_per_period"]},{c["bad"][:1]}'
        print(line, flush=True)
