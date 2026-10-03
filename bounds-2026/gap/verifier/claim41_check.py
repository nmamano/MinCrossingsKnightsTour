"""Independent geometric patch enumeration and finite-tree DP, 2026-10-03.
No author imports. Uses exact geometric tile halves from Claim 37.
"""
import itertools as it,json,hashlib,time
from collections import defaultdict,Counter
from pathlib import Path
from pysat.solvers import Glucose4
from claim37_check import tile
DIR='BRTL';DV=((0,-1),(1,0),(0,1),(-1,0));OP=(2,3,0,1)
BLOCK=tuple((x,y) for x in (-1,0,1) for y in (-1,0,1) if (x,y)!=(0,0))
HS=('BR','TL','RT','LB');SIG={'BR':0,'TL':0,'RT':1,'LB':1}
K=[(x,y) for x in range(-2,3) for y in range(-2,3) if sorted((abs(x),abs(y)))==[1,2]]
def plus(a,b):return a[0]+b[0],a[1]+b[1]
def neg(a):return -a[0],-a[1]
def edge(a,b):return tuple(sorted((a,b)))
def vertices(q):return {plus(q,z) for z in ((0,0),(1,0),(0,1),(1,1))}
ALL={edge((x,y),(x+dx,y+dy)) for x in range(-4,5) for y in range(-4,5) for dx,dy in K}
LINK={};HALF=defaultdict(set)
for e in ALL:
 hh=tile(e)
 for (q,h),(r,j) in (hh,hh[::-1]):
  d=DV.index((r[0]-q[0],r[1]-q[1]));LINK[q,d,SIG[h]]=e;HALF[q,h].add(e)
def owner(e,v):
 qq=[q for q,h in tile(e) if v in vertices(q)];assert len(qq)==1
 return qq[0]
def types():
 out=[]
 for bits in it.product((False,True),repeat=4):
  t={(0,0):'U'};t.update({v:('U' if b else 'N\\') for v,b in zip(DV,bits)})
  diagonals=[]
  for x,y in it.product((-1,1),repeat=2):
   cnt=bits[DV.index((x,0))]+bits[DV.index((0,y))]
   opts=('N\\',) if cnt==2 else ('N\\','U') if cnt==1 else ('O',)
   diagonals.append([((x,y),z) for z in opts])
  for choice in it.product(*diagonals):out.append(t|dict(choice))
 return out

def enumerate_patch(t):
 good={q for q,z in t.items() if z=='N\\'}
 used={e for q in good|{(0,0)} for h in HS for e in HALF[q,h]}
 incid={}
 for v in vertices((0,0)):
  incid[v]=[edge(v,plus(v,d)) for d in K if t.get(owner(edge(v,plus(v,d)),v),'O')!='O']
  used.update(incid[v])
 vid={e:i+1 for i,e in enumerate(sorted(used))};cl=[]
 for es in incid.values():cl.extend([-vid[e] for e in z] for z in it.combinations(es,3))
 for q in good:
  for h in HS:
   a,b=sorted(vid[e] for e in HALF[q,h])
   cl.extend(([a,b],[-a,-b]) if SIG[h] else ([-a],[-b]))
 # Exact bad indicator on each quarter, separate truth-table encoding.
 top=len(vid);bads=[]
 for quarter in 'BRTL':
  ls=sorted(vid[e] for h in HS if quarter in h for e in HALF[(0,0),h]);assert len(set(ls))==4
  top+=1;bads.append(top)
  for bits in it.product((0,1),repeat=4):
   cl.append([(-v if b else v) for v,b in zip(ls,bits)]+([top] if sum(bits)!=1 else [-top]))
 cl.append(bads)
 own=[vid[LINK[(0,0),d,s]] for d in range(4) for s in (0,1)]
 proj=set(own);ex={}
 for d,X in enumerate(DV):
  if t[X]!='U':continue
  perp=(1,0) if d in (0,2) else (0,1)
  cross=[vid[LINK[w,d,s]] for w in (perp,neg(perp)) for s in (0,1)]
  parts=[]
  for v in sorted(vertices((0,0))&vertices(X)):
   cp=[];xp=[]
   for e in incid[v]:
    (cp if owner(e,v) in ((0,0),perp,neg(perp)) else xp).append(vid[e])
   parts.append((cp,xp));proj.update(cp+xp)
  ex[d]=(cross,parts);proj.update(cross)
 rows=set()
 with Glucose4(bootstrap_with=cl) as solver:
  while solver.solve():
   model=set(v for v in solver.get_model() if v>0)
   sides=tuple(int(v in model) for v in own)
   ext=tuple(None if d not in ex else (tuple(int(v in model) for v in ex[d][0]),tuple((sum(v in model for v in a),sum(v in model for v in b)) for a,b in ex[d][1])) for d in range(4))
   rows.add((sides,ext));solver.add_clause([-v if v in model else v for v in proj])
 return sorted(rows,key=repr)

def cost(bits):
 val={(d,s):bits[2*d+s] for d in range(4) for s in (0,1)}
 half={h:sum(val[DIR.index(d),SIG[h]] for d in h) for h in HS}
 return sum(sum(half[h] for h in HS if q in h)!=1 for q in 'BRTL')-2

def key(t,bits,ext,d,par,child=False):
 perp=(1,0) if d in (0,2) else (0,1);X=DV[d]
 region=(plus(X,perp),plus(X,neg(perp)),perp,neg(perp))
 e=ext[d]
 if child:
  region=region[2:]+region[:2]
  e=(e[0],tuple((b,a) for a,b in e[1]))
 return (OP[d] if child else d,bits[2*d:2*d+2],tuple(t[q] for q in region),e,par)

def combine(t,bits,parent,states):
 up=None
 for a,b in ((1,2),(3,0)): # active backslash halves RT, LB
  ends=[]
  for d in (a,b):
   ends.append(None if d==parent else states[d] if t[DV[d]]=='U' else bits[2*d+1])
  if None in ends:
   up=1-ends[1-ends.index(None)]
  elif ends[0]!=ends[1]:return False,None
 return True,up

def main():
 start=time.time();patches=[];hashes=[]
 for t in types():
  rows=enumerate_patch(t)
  hashes.append(dict(types=tuple(t[q] for q in BLOCK),count=len(rows),sha256=hashlib.sha256(repr(rows).encode()).hexdigest()))
  for bits,ext in rows:
   c=cost(bits);assert c>=0;patches.append((t,bits,ext,c))
  print('patch type',len(hashes),'count',len(rows),'seconds',round(time.time()-start,2),flush=True)
 Path('gap/verifier/claim41_independent_patches.json').write_text(json.dumps(hashes,indent=2))
 # Independent synchronous height recurrence. Non-cut slash state is omitted.
 values={};history=[];INF=10**8
 for iteration in range(30):
  nxt={}
  for t,bits,ext,cost0 in patches:
   ud=[d for d in range(4) if t[DV[d]]=='U']
   for parent in ud:
    children=[d for d in ud if d!=parent];opts=[]
    for d in children:
     opts.append([(p,values[k]) for p in (0,1) for k in [key(t,bits,ext,d,p,True)] if k in values])
    for selection in it.product(*opts):
     ok,up=combine(t,bits,parent,dict(zip(children,(p for p,v in selection))))
     if not ok:continue
     kk=key(t,bits,ext,parent,up);vv=cost0+sum(v for p,v in selection)
     if vv<nxt.get(kk,INF):nxt[kk]=vv
  assert all(k in nxt and nxt[k]<=v for k,v in values.items())
  row=dict(iteration=iteration,keys=len(nxt),minimum=min(nxt.values(),default=None),fixed=nxt==values)
  history.append(row);print(row,flush=True)
  if nxt==values:break
  values=nxt
 else:raise AssertionError('no fixed point')
 best=INF;root_options=0
 for t,bits,ext,cost0 in patches:
  children=[d for d in range(4) if t[DV[d]]=='U'];opts=[]
  for d in children:opts.append([(p,values[k]) for p in (0,1) for k in [key(t,bits,ext,d,p,True)] if k in values])
  for selection in it.product(*opts):
   ok,up=combine(t,bits,None,dict(zip(children,(p for p,v in selection))))
   if ok:best=min(best,cost0+sum(v for p,v in selection));root_options+=1
 out=dict(block_types=len(hashes),patches=len(patches),history=history,keys=len(values),root_minimum=best,root_options=root_options,seconds=round(time.time()-start,2))
 Path('gap/verifier/claim41_check.json').write_text(json.dumps(out,indent=2));print('FINAL',out,flush=True)
 # Finite closed subsolution table, sufficient to recheck the induction over arbitrary finite trees.
 Path('gap/verifier/claim41_values.json').write_text(json.dumps([(k,v) for k,v in sorted(values.items(),key=repr)]))
if __name__=='__main__':main()
