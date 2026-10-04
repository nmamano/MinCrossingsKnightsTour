"""Closed walks of 4 optimal corners joined by 4 tight sides of equal length L, for every L >= 0.
Uses tight.cpp output with periodicity (pre, per): hits at L >= pre repeat with period per; pre = -1: walks died out.
If no closed walk exists for even L, then (pairs list complete) every ring with n = 2A + L, n even, has sum r > 4*corner.
usage: tightcycle2.py pairs tightout A Lmax"""
import sys
from collections import defaultdict
import numpy as np, scipy.sparse as sp
pairs = [l.split() for l in open(sys.argv[1]) if not l.startswith('#')]; A, LMAX = int(sys.argv[3]), int(sys.argv[4])
info = {}
for l in open(sys.argv[2]):
    if not l.startswith('source'): continue
    tok = l.split(); src = tok[1]; pre, per = int(tok[5]), int(tok[7]); d = {}
    for part in l.split('|')[1:]:
        t, ls = part.split(':'); d[t.strip()] = set(int(x) for x in ls.split())
    info[src] = (pre, per, d)
def hit(s, tgt, L):
    pre, per, d = info[s]
    if pre >= 0 and L >= pre: L = pre + (L - pre) % per
    return L in d.get(tgt, ())
P = len(pairs); bysrc = defaultdict(list); bytgt = defaultdict(list)
for i, (s, t, st) in enumerate(pairs): bysrc[s].append(i); bytgt[st].append(i)
missing = [s for s in bysrc if s not in info]; print('pairs', P, 'sources', len(bysrc), 'missing tight info', len(missing))
for L in range(LMAX + 1):
    rows, cols = [], []
    for s, I in bysrc.items():
        pre, per, d = info[s]
        for tgt in d:
            if tgt in bytgt and hit(s, tgt, L):
                for i in I:
                    for j in bytgt[tgt]: rows.append(i); cols.append(j)
    M = sp.csr_matrix((np.ones(len(rows), dtype=np.int64), (rows, cols)), shape=(P, P))
    M.data[:] = 1; M2 = M @ M; M2.data[:] = 1; tr = (M2 @ M2).diagonal().sum()
    print(f'L {L} n {2*A+L}: arcs {M.nnz} closed 4-walks {tr}', flush=True)
