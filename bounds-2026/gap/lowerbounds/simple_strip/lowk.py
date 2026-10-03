import sys, pickle, numpy as np
from collections import Counter
sys.path.insert(0, 'gap/lowerbounds/simple_strip')
from nocyc_common import *
K = pickle.load(open('gap/lowerbounds/simple_strip/kappa.pkl', 'rb'))
k2 = np.array([int(2*K[v][0]) for v in range(len(bstates))])
print('2kappa distribution over states', sorted(Counter(k2).items())[:12])
low = [v for v in range(len(bstates)) if k2[v] <= 3]
print('states with kappa<=3/2:', len(low))
for v in low: print(k2[v], dict(K[v][1]), bstates[v][1])
