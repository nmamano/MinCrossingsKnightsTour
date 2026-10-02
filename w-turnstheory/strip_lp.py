from itertools import combinations
from fractions import Fraction
from scipy.optimize import linprog
from scipy.sparse import lil_matrix
M=[(1,2),(2,1),(2,-1),(1,-2),(-1,-2),(-2,-1),(-2,1),(-1,2)]
for D in [2,3,4,6,10,20,40,80]:
    vv=[(x,a,b) for x in range(D) for a,b in combinations(range(8),2) if x+M[a][0]>=0 and x+M[b][0]>=0]
    rows=[('v',x) for x in range(D)]+[('e',x,a) for x in range(D) for a in range(4) if x+M[a][0]<D]
    ri={r:i for i,r in enumerate(rows)}
    A=lil_matrix((len(rows),len(vv)))
    for j,(x,a,b) in enumerate(vv):
        A[ri['v',x],j]=1
        for d in [a,b]:
            key=('e',x,d) if d<4 else ('e',x+M[d][0],d-4)
            if key in ri:A[ri[key],j]+=1 if d<4 else -1
    c=[int(b!=a+4) for x,a,b in vv]
    rhs=[int(r[0]=='v') for r in rows]
    res=linprog(c,A_eq=A.tocsr(),b_eq=rhs,bounds=(0,None),method='highs',options={'threads':1})
    print(D,res.fun,flush=True)
    if D==4:
        dual=[Fraction(float(z)).limit_denominator(1000) for z in res.eqlin.marginals]
        print('DUAL',[(r,str(z)) for r,z in zip(rows,dual) if z])
        for j,v in enumerate(vv):
            assert sum(dual[i]*int(A[i,j]) for i in range(len(rows)))<=c[j],v
        print('EXACT dual checked',sum(dual[i]*rhs[i] for i in range(len(rows))))
