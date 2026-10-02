"""usage: run_seam.py kind p w s tl [off2...]; kind in gentle, sharp, vert, horiz2"""
import sys, json
from seam import Seam, solve
from unroll import check
KIND = {
  'vfreeB':  dict(T=lambda p: (0, p), hv=(1, 0), f1=(1, 2), form1=(2, -1), f2=(1, -2), form2=(-2, -1)),
  'gentle': dict(T=lambda p: (p, p), hv=(-1, 1), f1=(2, -1), form1=(1, 2), f2=(1, -2), form2=(2, 1)),
  'sharp':  dict(T=lambda p: (p, -p), hv=(1, 1), f1=(2, -1), form1=(1, 2), f2=(1, -2), form2=(-2, -1)),
  'vert':   dict(T=lambda p: (0, p), hv=(1, 0), f1=(2, -1), form1=(1, 2), f2=(2, 1), form2=(-1, 2)),
  'horizAA':dict(T=lambda p: (p, 0), hv=(0, 1), f1=(2, -1), form1=(1, 2), f2=(2, 1), form2=(1, -2)),
}
def make(kind, p, w, s, off2, w2=None):
    k = KIND[kind]
    return Seam(T=k['T'](p), hv=k['hv'], w1=w, w2=w if w2 is None else w2, f1=k['f1'], form1=k['form1'],
                f2=k['f2'], form2=k['form2'], s=s, off1=0, off2=off2)
if __name__ == '__main__':
    kind, p, w, s, tl = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), float(sys.argv[5])
    offs = [int(a) for a in sys.argv[6:]] or list(range(s))
    for off2 in offs:
        lanes = s > 0
        st = make(kind, p, w, max(s, 1), off2)
        r = solve(st, time_limit=tl, workers=1, lanes=lanes)
        line = f'{kind} p={p} w={w} s={s} off2={off2} cells={len(st.base)} {r["status"]} {r["time"]}s'
        if 'X' in r:
            c = check(st, r['chosen'])
            line += f' X={r["X"]} T={r["T"]} bound={r["bound"]} X/p={r["X"]/p:.3f} T/p={r["T"]/p:.3f} chk(strands_ok={c["strands_ok"]},X={c["X_per_period"]},T={c["T_per_period"]},bad={len(c["bad"])})'
            line += ' chosen=' + json.dumps(r['chosen'])
        print(line, flush=True)
