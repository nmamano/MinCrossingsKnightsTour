"""Independent one-row endpoint audit. No worker imports."""
from itertools import product
from pathlib import Path
import json
import networkx as nx
from claim11_forest import transitions,potentials
from claim11_corner import options,coefficient,chi,canon,M,K

def rows():
 states=[(0,())];idx={states[0]:0};arcs=[]
 for u,s in enumerate(states):
  best={}
  for t,w in transitions(s):
   if t not in idx:idx[t]=len(states);states.append(t)
   v=idx[t];best[v]=min(best.get(v,w),w)
  arcs.extend((u,v,w) for v,w in best.items())
 N=len(states);assert (N,len(arcs))==(82516,144674)
 d=potentials(N,arcs,[4*w-1 for u,v,w in arcs],0)
 G=nx.DiGraph();G.add_nodes_from(range(N));G.add_edges_from((u,v) for u,v,w in arcs if 4*w-1+d[u]-d[v]==0)
 comps=[c for c in nx.strongly_connected_components(G) if len(c)>1]
 assert len(comps)==2 and all(len(c)==4 for c in comps)
 patterns={};out=[]
 for c in comps:
  root=next(u for u in c if states[u][0]==0);path=[root]
  for _ in range(4):
   ns=[v for v in G[path[-1]] if v in c];assert len(ns)==1;path.append(ns[0])
  assert path[-1]==root
  front=set()
  for step,u in enumerate(path):
   assert states[u][0]==step%4
   shift=int(step==4)
   front|={canon((a[0],a[1]+shift),(b[0],b[1]+shift)) for a,b,l in states[u][1]}
  fits=[]
  for sign in (-1,1):
   expected=set()
   for y in range(-4,5):
    for a,b in [((0,y),(2,y+sign)),((0,y),(1,y+2*sign)),((1,y),(3,y+sign))]:
     if min(a[1],b[1])<=0<=max(a[1],b[1]):expected.add(canon(a,b))
   if expected==front:fits.append(sign)
  assert len(fits)==1;sg=fits[0];patterns[sg]=front
  # All legal strip edges that straddle row 0 are either present in the union or absent.
  universe=set()
  for x,y in product(range(4),range(-2,3)):
   for dx,dy in M:
    b=(x+dx,y+dy)
    if 0<=b[0]<4 and min(x,b[0])<2 and min(y,b[1])<=0<=max(y,b[1]):universe.add(canon((x,y),b))
  assert front<=universe
  reflected={canon((a[0],-a[1]),(b[0],-b[1])) for a,b in front}
  # Both squares above and below this row can be an endpoint square after reflection.
  for j in (-1,0):
   pair={canon((0,j),(2,j+1)),canon((0,j+1),(2,j))}
   assert not pair<=front and not pair<=reflected
  out.append({'sign':sg,'phases':[states[u][0] for u in path],'present_edges':len(front),'absent_edges':len(universe-front)})
 assert {canon((a[0],-a[1]),(b[0],-b[1])) for a,b in patterns[1]}==patterns[-1]
 print('row recovery',out,flush=True);return patterns,{'states':N,'arcs':len(arcs),'rows':out}

def corner(patterns):
 opts=options();reports=[];signatures={}
 for R in (12,13,14,15,24,25,60,61):
  edges=set()
  # Include all edges in a large positive box, not only edges presumed to meet an endpoint.
  for x,y in product(range(R+5),repeat=2):
   for dx,dy in M:
    q=(x+dx,y+dy)
    if min(q)>=0:edges.add(canon((x,y),q))
  middle={(0,y) for y in range(4,R)}|{(y,0) for y in range(4,R)}
  residual={e:coefficient(e,R)+sum(chi(v) for v in e if v in middle) for e in edges}
  residual={e:c for e,c in residual.items() if c}
  base=-chi((1,R+1))-chi((R+1,1))-2*sum(chi((0,j)) for j in range(1,R+1))-2*sum(chi(v) for v in middle)
  left={e:c for e,c in residual.items() if not any(v in K for v in e) and max(p[0] for p in e)<=3}
  bottom={e:c for e,c in residual.items() if not any(v in K for v in e) and max(p[1] for p in e)<=3}
  assert len(left)==len(bottom)==8
  norm=sorted((canon((a[0],a[1]-R),(b[0],b[1]-R)),v*chi((0,R))) for (a,b),v in left.items())
  assert all(min(a[1],b[1])<=R<=max(a[1],b[1]) and min(a[0],b[0])<2 for a,b in left)
  assert {canon((a[1],a[0]),(b[1],b[0])):v for (a,b),v in left.items()}==bottom
  for sign in (-1,1):
   selected={canon((a[0],a[1]+R),(b[0],b[1]+R)) for a,b in patterns[sign]}
   assert sum(v for e,v in left.items() if e in selected)==-chi((0,R))
  cv=[sum(residual.get(e,0) for e in es) for es in opts]
  for ls,bs in product((-1,1),repeat=2):
   known={canon((a[0],a[1]+R),(b[0],b[1]+R)) for a,b in patterns[ls]}
   known|={canon((a[1]+R,a[0]),(b[1]+R,b[0])) for a,b in patterns[bs]}
   assert all(any(v in K for v in e) or e in left or e in bottom for e in residual)
   fixed=sum(residual.get(e,0) for e in known)
   assert {(base+fixed+c)%3 for c in cv}=={1}
  signature=(base,tuple(norm),tuple(sorted((e,v) for e,v in residual.items() if any(p in K for p in e))))
  if R%2 in signatures:assert signature==signatures[R%2]
  else:signatures[R%2]=signature
  reports.append({'R':R,'corner_options':len(opts),'pattern_pairs':4,'left_terms':norm})
 print('corner PASS',len(reports),'radii',flush=True);return reports

def intervals():
 out=[]
 for n in (32,34,48,64,96,128,256):
  # Each physical side uses ONE scan direction for both of its corner tests.
  A=list(range(12,n//2-3));B=[n-1-R for R in A]
  assert not set(A)&set(B) and len(set(A+B))==len(A)+len(B)
  assert min(B)==n//2+3 and max(B)==n-13
  out.append({'n':n,'near':[min(A),max(A)],'far':[min(B),max(B)],'max_paths_removed_per_bad_side_row':1})
 return out
if __name__=='__main__':
 p,r=rows();out={'date':'2026-10-02','strip':r,'corner':corner(p),'intervals':intervals()}
 Path('w-verifier/claim18.json').write_text(json.dumps(out,indent=1));print('ALL PASS',flush=True)
