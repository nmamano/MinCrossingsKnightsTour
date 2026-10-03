# KT Structures 2026-10-04: residual map of a solution: r(v) = t(v) - side lower terms; corner sums and r>0 cells.
import sys, json
from tmin import lower, MI, MJ
rec = json.load(open(sys.argv[1])); g = rec['grid']; n = len(g)
R = {}
for i in range(n):
    for j in range(n):
        p = [int(c) for c in g[i][j]]; t = int(abs(p[0]-p[1]) != 4)
        di = [MI[k] for k in p]; dj = [MJ[k] for k in p]
        R[i, j] = t - lower(j, dj) - lower(n-1-j, [-d for d in dj]) - lower(i, di) - lower(n-1-i, [-d for d in di])
cs = []
for ci in (0, n-4):
    for cj in (0, n-4):
        cs.append(sum(R[i, j] for i in range(ci, ci+4) for j in range(cj, cj+4)))
inc = lambda i, j: (i < 4 or i >= n-4) and (j < 4 or j >= n-4)
out = [(i, j, R[i, j]) for (i, j) in R if not inc(i, j) and R[i, j]]
print('n', n, 'T-8n', sum(R.values()), 'corners (TL,TR,BL,BR)', cs, 'outside r>0:', len(out), 'sum', sum(r for *_, r in out))
print('outside cells (i,j,r):', sorted(out))
