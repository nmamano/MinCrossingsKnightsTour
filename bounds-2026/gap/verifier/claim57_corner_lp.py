"""Build an independent local-marginal LP and extract an exact rational dual certificate."""
import os
os.sched_setaffinity(0,sorted(os.sched_getaffinity(0))[:2])
from pathlib import Path
from itertools import combinations
from fractions import Fraction
import json,sys
import numpy as np
from scipy.sparse import coo_matrix
from scipy.optimize import linprog
from claim57_local import MOVES,lower
A=int(sys.argv[1]);scale=int(sys.argv[2]);W=6
cells=[(x,y) for y in range(A) for x in range(A) if min(x,y)<W];cs=set(cells);edges=set()
for p in cells:
 for dx,dy in MOVES:
  q=(p[0]+dx,p[1]+dy)
  if q in cs:edges.add(tuple(sorted((p,q))))
edges=sorted(edges);index={p:i for i,p in enumerate(cells)};ei={e:len(cells)+i for i,e in enumerate(edges)}
columns=[];costs=[];options=[]
for p in cells:
 x,y=p
 for a,b in combinations([d for d in MOVES if x+d[0]>=0 and y+d[1]>=0],2):
  r=int(a!=(-b[0],-b[1]))-lower(x,[a[0],b[0]])-lower(y,[a[1],b[1]])
  cost=scale*r;col=[(index[p],1)]
  for dx,dy in [a,b]:
   q=(x+dx,y+dy)
   if q in cs:
    e=tuple(sorted((p,q)));col.append((ei[e],1 if p==e[0] else -1))
   # -h(vertical state) + h(sigma(horizontal state)); sigma negates these weights.
   if y<A<=q[1] and 3<=x<6 and 3<=q[0]<6:cost+=1 if dx>0 else -1
   if x<A<=q[0] and 3<=y<6 and 3<=q[1]<6:cost+=1 if dy>0 else -1
  columns.append(col);costs.append(cost);options.append([p,a,b])
rr=[];cc=[];vv=[]
for j,col in enumerate(columns):
 for i,v in col:rr.append(i);cc.append(j);vv.append(v)
B=coo_matrix((vv,(rr,cc)),shape=(len(cells)+len(edges),len(columns))).tocsr();rhs=np.r_[np.ones(len(cells)),np.zeros(len(edges))]
res=linprog(costs,A_eq=B,b_eq=rhs,bounds=(0,None),method='highs')
print('A',A,'scale',scale,'variables',len(columns),'rows',len(rhs),'status',res.message,'opt',res.fun,flush=True)
assert res.success
ys=[Fraction(float(v)).limit_denominator(1000000) for v in res.eqlin.marginals]
viol=[]
for j,col in enumerate(columns):
 z=sum((ys[i]*v for i,v in col),Fraction())
 if z>costs[j]:viol.append((j,str(z-costs[j])))
value=sum(ys[:len(cells)],Fraction())
print('Exact candidate dual:',value,'/',scale,'violations',len(viol),'denominators',sorted(set(y.denominator for y in ys)),flush=True)
out=dict(A=A,W=W,scale=scale,float_opt=res.fun,exact_dual=str(value),violations=viol,cells=cells,edges=edges,dual=[str(v) for v in ys])
Path(f'gap/verifier/claim57_run/corner_A{A}_S{scale}_dual.json').write_text(json.dumps(out,indent=1)+'\n')
