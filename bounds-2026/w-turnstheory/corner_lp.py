from itertools import combinations
from fractions import Fraction
from scipy.optimize import linprog
from scipy.sparse import lil_matrix
from corner_check import M,lower
for K in [4,5,6,8,10]:
    pairs=[((x,y),a,b) for x in range(K) for y in range(K) for a,b in combinations([d for d in M if x+d[0]>=0 and y+d[1]>=0],2)]
    cells=[(x,y) for x in range(K) for y in range(K)]
    edges=set()
    for p,a,b in pairs:
        for d in (a,b):
            q=(p[0]+d[0],p[1]+d[1])
            if q in cells: edges.add(tuple(sorted((p,q))))
    rows=[('c',p) for p in cells]+[('e',e) for e in sorted(edges)]
    ri={r:i for i,r in enumerate(rows)}
    A=lil_matrix((len(rows),len(pairs)))
    c=[]
    for j,(p,a,b) in enumerate(pairs):
        A[ri['c',p],j]=1
        for d in (a,b):
            q=(p[0]+d[0],p[1]+d[1]);e=tuple(sorted((p,q)))
            if e in edges:A[ri['e',e],j]+=1 if p<q else -1
        t=int(a[0]+b[0]!=0 or a[1]+b[1]!=0)
        c.append(t-lower(p[0],[a[0],b[0]])-lower(p[1],[a[1],b[1]]))
    rhs=[int(r[0]=='c') for r in rows]
    res=linprog(c,A_eq=A.tocsr(),b_eq=rhs,bounds=(0,None),method='highs',options={'threads':1})
    print('K',K,'loss',-res.fun,flush=True)
    if K==4:
        dual=[Fraction(float(z)).limit_denominator(1000) for z in res.eqlin.marginals]
        print('NONZERO DUAL',[(r,str(z)) for r,z in zip(rows,dual) if z])
        for j,v in enumerate(pairs):assert sum(dual[i]*int(A[i,j]) for i in range(len(rows)))<=c[j],v
        print('Exact bound',sum(dual[i]*rhs[i] for i in range(len(rows))))
