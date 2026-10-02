import sys, ast
from fold_complete2 import base
n=int(sys.argv[1]); ts=ast.literal_eval(sys.argv[2]); ms=ast.literal_eval(sys.argv[3])
E,deg=base(n,ts=ts,ms=ms)
for Y in [5,8,11,14,17,20, 30, 40]:
    # cut between rows Y-1 and Y ; edges with min y < Y <= max y
    contrib={}
    for e in E:
        (a,b),(c,d)=e
        lo=(a,b) if b<d else (c,d); hi=(c,d) if b<d else (a,b)
        if lo[1] < Y <= hi[1]:
            s = 1 if (lo[0]+lo[1])%2==0 else -1
            x=min(lo[0],hi[0])
            contrib[x]=contrib.get(x,0)+s
    tot=sum(contrib.values())
    # group into segments
    xs=sorted(contrib)
    run=[]; cur=0; start=0
    line=''.join({1:'+',-1:'-',0:'0',2:'P',-2:'M'}.get(contrib.get(x,0),'?') for x in range(n))
    print(Y, 'total', tot, line)
