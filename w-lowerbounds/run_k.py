import sys, time
from strip_dp import build
from mmc import prune, howard, certify
from fractions import Fraction
k = int(sys.argv[1])
t=time.time()
states, adj, W = build(k)
alive = prune(adj)
print('k',k,'states',len(states),'alive',sum(alive), 'build %.1fs'%(time.time()-t))
mu, pol, eta = howard(adj, alive)
print('mu per cell', mu, 'per row', mu*W, 'time %.1fs'%(time.time()-t))
md, it = certify(adj, mu)
print('certificate: lam per cell', mu, 'mind', md, 'BF iters', it)
