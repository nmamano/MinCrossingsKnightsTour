# rerun the UNKNOWN lines of an interface.py log with a longer time limit (KT Structures, 2026-10-03)
import sys, re
import interface as I
log, a, tl = sys.argv[1], int(sys.argv[2]), float(sys.argv[3])
mults = [int(t) for t in sys.argv[4].split(',')]
for line in open(log):
    if 'per end None' not in line or 'INFEASIBLE' in line: continue
    sl, f1, f2 = line.split()[:3]
    F1, F2 = (f1[0], f1[1:]), (f2[0], f2[1:])
    T0, hv = I.SLOPES[sl]; mm = I.mult_for(T0, F1, F2)
    out = []
    for k in mults:
        T = (k*mm*T0[0], k*mm*T0[1]); ends = I.absorbed(F1, F2, T)
        st, val, bd = I.solve(T, hv, a, F1, F2, tl)
        out.append(f'x{k}:{st}:{val}:{bd}:ends{ends}:' + ('-' if bd is None else f'{bd/ends:.4f}'))
    print(sl, f1, f2, ' '.join(out), flush=True)
