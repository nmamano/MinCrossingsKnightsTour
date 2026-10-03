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

from fractions import Fraction
from pathlib import Path
K=6
w=[3,-1,-1,1]
bounds=[(None,None)]*len(rows)
for p in C:
    x,y=p;dx=min(x,n-1-x);dy=min(y,n-1-y)
    if dx>=4 and dy>=4:
        a=(w[dx] if dx<4 else 0)+(w[dy] if dy<4 else 0)
        bounds[rows['v',p]]=(a,a)
res=linprog([-z for z in rhs],A_ub=A.T,b_ub=cost,bounds=bounds,method='highs',options={'threads':1,'time_limit':15})
print('dual',n,res.message,None if res.fun is None else -res.fun,flush=True)
if res.success:
    ds=[Fraction(float(z)).limit_denominator(10000) for z in res.x]
    Ac=A.tocsc()
    for j in range(len(pairs)):
        assert sum(ds[int(i)]*int(z) for i,z in zip(Ac.indices[Ac.indptr[j]:Ac.indptr[j+1]],Ac.data[Ac.indptr[j]:Ac.indptr[j+1]]))<=cost[j]
    obj=sum(ds[i]*rhs[i] for i in range(len(rows)))
    print('EXACT',obj, 'constant',obj-8*n,flush=True)
    Path(__file__).with_name(f'bulkzero-dual-n{n}.json').write_text(json.dumps(dict(n=n,bound=str(obj),dual=[(r,str(ds[i])) for r,i in rows.items() if ds[i]])))
