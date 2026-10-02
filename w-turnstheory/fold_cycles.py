import sys
from pathlib import Path
sys.path[:0]=[str(Path(__file__).resolve().parents[1]),str(Path(__file__).resolve().parents[1]/'w-lowerbounds')]
from fold_complete2 import base
from collections import defaultdict
n=48;E,deg=base(n);adj=defaultdict(list)
for a,b in E:adj[a].append(b);adj[b].append(a)
for y in range(2,12):
    start=(0,y);p=None;q=start;walk=[];closed=False
    for _ in range(n*n):
        walk.append(q)
        if len(adj[q])!=2:break
        nxt=adj[q][0] if adj[q][0]!=p else adj[q][1]
        p,q=q,nxt
        if q==start:closed=True;break
    print(y,'closed',closed,'length',len(walk),'max',max(max(p) for p in walk),'sample',walk[:12])
