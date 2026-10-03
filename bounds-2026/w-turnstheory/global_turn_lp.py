"""Full-board or boundary-ring pair LP; one HiGHS thread."""
from itertools import combinations
from scipy.optimize import linprog
from scipy.sparse import coo_matrix
import sys,json
M=[(a,b) for a in (-2,-1,1,2) for b in (-2,-1,1,2) if abs(a)+abs(b)==3]
n=int(sys.argv[1]);width=int(sys.argv[2]) if len(sys.argv)>2 else n
C={(x,y) for x in range(n) for y in range(n) if min(x,y,n-1-x,n-1-y)<width or (len(sys.argv)>3 and min(abs(x-y),abs(x+y-n+1))<=int(sys.argv[3]))}
pairs=[];rr=[];cc=[];vv=[];rows={('v',p):i for i,p in enumerate(sorted(C))};cost=[]
for p in sorted(C):
    opts=[d for d in M if 0<=p[0]+d[0]<n and 0<=p[1]+d[1]<n]
    for a,b in combinations(opts,2):
        j=len(pairs);pairs.append((p,a,b));cost.append(int(tuple(map(sum,zip(a,b)))!=(0,0)))
        rr.append(rows['v',p]);cc.append(j);vv.append(1)
        for d in (a,b):
            q=(p[0]+d[0],p[1]+d[1])
            if q not in C:continue
            key=('e',tuple(sorted((p,q))))
            if key not in rows:rows[key]=len(rows)
            rr.append(rows[key]);cc.append(j);vv.append(1 if p<q else -1)
A=coo_matrix((vv,(rr,cc)),shape=(len(rows),len(pairs))).tocsr()
rhs=[0]*len(rows)
for p in C:rhs[rows['v',p]]=1
res=linprog(cost,A_eq=A,b_eq=rhs,bounds=(0,None),method='highs',options={'threads':1,'time_limit':15})
print(json.dumps(dict(n=n,width=width,status=res.message,objective=res.fun,residual=None if res.fun is None else res.fun-8*n)),flush=True)

if res.success:
    from fractions import Fraction
    from pathlib import Path
    ds=[Fraction(float(z)).limit_denominator(100000) for z in res.eqlin.marginals]
    data=dict(n=n,width=width,bound=str(sum(ds[rows['v',p]] for p in C)),dual=[(r,str(ds[i])) for r,i in rows.items() if ds[i]])
    Path(__file__).with_name(f'global-dual-n{n}-w{width}-s{sys.argv[3] if len(sys.argv)>3 else 0}.json').write_text(json.dumps(data))
    if n<=24:
        for y in range(n):print(' '.join(str(ds[rows['v',(x,y)]]) for x in range(n) if (x,y) in C))
