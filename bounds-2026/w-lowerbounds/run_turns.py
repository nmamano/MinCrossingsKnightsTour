import sys, time
from strip_dp import build
from mmc import prune, howard, certify
k=int(sys.argv[1])
t=time.time()
states, adj, W = build(k, mode='turns')
alive=prune(adj)
mu,pol,eta=howard(adj,alive)
print('turns k',k,'states',len(states),'per row',mu*W,'(%.0fs)'%(time.time()-t), flush=True)
md,it=certify(adj,mu)
print('certificate mind',md,'iters',it)
