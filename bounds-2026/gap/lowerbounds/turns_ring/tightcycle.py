"""From cornopt pairs (s t sigma_t) and tight.cpp output, find closed walks of 4 corners with tight sides of
length L (all four sides equal): then R_W(2A + L) == 4 * corner value.  usage: tightcycle.py pairs tightout A"""
import sys, re
import numpy as np
pairs = [l.split() for l in open(sys.argv[1])]; A = int(sys.argv[3])
reach = {}
for l in open(sys.argv[2]):
    if not l.startswith('source'): continue
    src = l.split()[1]; d = {}
    for part in l.split('|')[1:]:
        t, ls = part.split(':'); d[t.strip()] = set(int(x) for x in ls.split())
    reach[src] = d
P = len(pairs)
for L in range(0, 31):
    M = np.zeros((P, P), dtype=np.int64)
    for i, (s, t, st) in enumerate(pairs):
        d = reach.get(s, {})
        for j, (s2, t2, st2) in enumerate(pairs):
            if L in d.get(st2, ()): M[i, j] = 1
    M2 = M @ M; tr = int(np.trace(M2 @ M2))
    if tr:
        # extract one closed walk
        M2b = (M2 > 0).astype(np.int64)
        for i in range(P):
            if (M2b @ M2b)[i, i]:
                for j in range(P):
                    if M2b[i, j] and M2b[j, i]:
                        a = next(k for k in range(P) if M[i, k] and M[k, j]); b = next(k for k in range(P) if M[j, k] and M[k, i])
                        print(f'L {L} n {2*A+L}: closed walks {tr}; e.g. corner pairs {i} {a} {j} {b}'); break
                break
    else: print(f'L {L} n {2*A+L}: none')
