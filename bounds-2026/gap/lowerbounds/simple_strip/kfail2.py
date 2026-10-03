import sys, pickle, numpy as np
from collections import Counter, defaultdict
sys.path.insert(0, 'gap/lowerbounds/simple_strip')
from nocyc_common import *
K = pickle.load(open('gap/lowerbounds/simple_strip/kappa.pkl', 'rb'))
k = int(sys.argv[1]) if len(sys.argv) > 1 else 0
d = np.load(f'gap/lowerbounds/simple_strip/kpot_{k}_0.npy')
neg = defaultdict(list)
for j, (u, v, W, m) in enumerate(rows):
    c = int(2*K[v][0]) - 4*g_of(m, k)
    if c < 0: neg[v].append((j, c))
print('distinct end states with negative arcs', len(neg))
nz = [s for s in range(len(bstates)) if d[s] != 0]
print('nonzero-potential states', len(nz))
# sizes of pending sets
print('pending sizes of neg end states', Counter(len(bstates[v][1]) for v in neg))
ends = Counter(); 
for v in neg: ends[bstates[v][1]] += 1
# find edges common to all neg end states
from functools import reduce
common = reduce(lambda a, b: a & b, [set(bstates[v][1]) for v in neg])
print('edges common to all neg end states', common)
cnt = Counter(e for v in neg for e in bstates[v][1]); print(cnt.most_common())
for v in list(neg)[:40]:
    print(int(2*K[v][0]), min(c for j, c in neg[v]), bstates[v][1])
