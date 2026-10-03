import sys, time
from strip_dp import build
from mmc import prune, howard, certify
k=int(sys.argv[1]); fam=(int(sys.argv[2]),int(sys.argv[3]))
states, adj, W = build(k, fam=fam)
alive=prune(adj)
mu,pol,eta=howard(adj,alive)
print('k',k,'fam',fam,'states',len(states),'alive',sum(alive),'per row',mu*W)
