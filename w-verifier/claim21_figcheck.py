"""Independent factual checks of the figure source data. No worker imports."""
import json
from pathlib import Path
from collections import defaultdict,Counter
from fractions import Fraction as F
from check import check,proper,MOVES
from claim9_tiles import quarters
out=Path('w-verifier/claim21_figures');d=json.loads((out/'source_data.json').read_text())
def es(data):return sorted({tuple(sorted(map(tuple,e))) for e in data})
def grid_es(t):
 n=len(t);return es([((j,n-1-i),(j+MOVES[int(c)][1],n-1-i-MOVES[int(c)][0])) for i,row in enumerate(t) for j,s in enumerate(row) for c in s])
def cps(E):
 bins=defaultdict(list);pairs=[]
 for i,e in enumerate(E):
  a,b=e;keys=[(x,y) for x in range(min(a[0],b[0])//4,max(a[0],b[0])//4+1) for y in range(min(a[1],b[1])//4,max(a[1],b[1])//4+1)]
  for j in set(j for k in keys for j in bins[k]):
   f=E[j]
   if proper(e,f):pairs.append((e,f))
  for k in keys:bins[k].append(i)
 return pairs
 defnever=0
def pt(pair):
 (a,b),(c,d)=pair;u=(b[0]-a[0],b[1]-a[1]);v=(d[0]-c[0],d[1]-c[1]);t=F((c[0]-a[0])*v[1]-(c[1]-a[1])*v[0],u[0]*v[1]-u[1]*v[0]);return(a[0]+t*u[0],a[1]+t*u[1])
def components(E):
 adj=defaultdict(set)
 for a,b in E:adj[a].add(b);adj[b].add(a)
 unseen=set(adj);rows=[]
 while unseen:
  p=unseen.pop();q=[p];vs={p}
  while q:
   for t in adj[q.pop()]:
    if t in unseen:unseen.remove(t);vs.add(t);q.append(t)
  rows.append((vs,all(len(adj[v])==2 for v in vs)))
 return rows
res={'date':'2026-10-02','tours':{},'heels':{},'fields':{},'strips':{},'figures':{}}
for name,t in [('paper48',d['paper48']),('H16a64',json.loads(Path('w-integrator/tours/H16a_VerticalEdge_off0_n64.json').read_text())['tour']),('FOLD96',json.loads(Path('w-integrator/tours/FOLD24_n96.json').read_text())['tour'])]:
 X,T=check(t);E=grid_es(t);points=list(map(pt,cps(E)));assert len(points)==X
 res['tours'][name]={'n':len(t),'X':X,'T':T}
 if name!='FOLD96':
  counts=[sum(a<=x<a+8 and 0<=y<=F(15,2) for x,y in points) for a in (6,14,22)]
  res['heels'][name]=counts;assert counts==([28]*3 if name=='paper48' else [16]*3)
 else:res['figures']['flux_crop']={'crossings':sum(F(43,2)<=x<=F(75,2) and F(43,2)<=y<=F(75,2) for x,y in points),'columns':16};assert X==720
for name,ee in d['fields'].items():
 E=es(ee);points=list(map(pt,cps(E)));loops=[vs for vs,closed in components(E) if closed and min(x for x,y in vs)<=1 and all(8<=y<=39 for x,y in vs)]
 res['fields'][name]={'X':len(points),'left_chevrons':len(loops)}
 if name=='48_0':
  assert not any(F(17,2)<=x<=F(43,2) and F(17,2)<=y<=F(43,2) for x,y in points)
  res['figures']['edge_rows']=[sum(F(2*y-1,2)<=b<F(2*y+1,2) and F(-1,2)<=a<=F(19,2) for a,b in points) for y in range(14,22)]
  assert res['figures']['edge_rows']==[1]*8
for name,ee in d['strips'].items():
 E=es(ee);points=list(map(pt,cps(E)));per=sum(3<=y<4 for x,y in points);assert per=={'normal':1,'abnormal':2}[name]
 raw=[((0,-1),(1,1),-1),((0,0),(1,-2),-1),((0,0),(2,-1),-1),((0,1),(1,-1),1),((0,1),(2,0),1),((0,2),(1,0),-1),((1,0),(2,2),-1),((1,1),(2,-1),-1)]
 vals=[]
 for sign in (1,-1):
  canon=lambda p,q:tuple(sorted(((p[0],sign*p[1]),(q[0],sign*q[1]))))
  f=sum(c for p,q,c in raw if canon(p,q) in E);exc=all(canon(p,q) in E for p,q in [((0,0),(2,1)),((0,1),(2,0))]);vals.append({'F':f,'pass':f%3==2 and not exc})
 assert all(v['pass']==(name=='normal') for v in vals)
 res['strips'][name]={'X_per_row':per,'tests':vals}
E=es(d['tt16']);C=Counter(t for e in E for t in quarters(e));hist=Counter(C[i,j,k] for i in range(16) for j in range(10) for k in range(4));res['figures']['tile_crop_multiplicities']=dict(hist)
assert len(components(E))==1 and len(E)==48**2
for k,pair in d['overlaps'].items():
 a,b=es(pair);assert proper(a,b) and len(quarters(a)&quarters(b))==int(k)
res['figures']['overlap_quarters']=[1,2]
(out/'independent_checks.json').write_text(json.dumps(res,indent=2));print(json.dumps(res,indent=2))
