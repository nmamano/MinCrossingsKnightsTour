from rate import *
from collections import Counter
loops = Counter((M[j], int(Wt[j])) for j in range(len(rows)) if S[j] == D[j])
print('self-loop masks (mask, W): count', sorted(loops.items(), key=lambda t: t[0][1])[:10])
PQ = {m for (m, W) in loops if W == 1}
print('W=1 loops', len(PQ), [[es[i] for i in range(20) if m >> i & 1] for m in PQ])
ng = [int(m not in PQ) for m in M]
print('ng critical', critical(ng))
gg = [g_of(m) for m in M]
print('g on PQ rows:', Counter(g for g, m in zip(gg, M) if m in PQ))
