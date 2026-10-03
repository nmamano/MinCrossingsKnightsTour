"""Independent strong strip audit, 2026-10-03. No author imports.
Full row edge masks, independent forest transitions and polygon tile geometry.
"""
from pathlib import Path
from itertools import combinations,product
import sys,json,time,hashlib,gzip
import numpy as np
from claim26_certificate import transitions,edge,cross,TERMS,EXC
from claim37_check import tile

def qs(e):return {(x,y,q) for (x,y),h in tile(e) for q in h}
def main():
 start=time.monotonic(); states=[(0,())]; ids={states[0]:0}; adj=[]
 for s in states:
  row={}
  for t,w,w0 in transitions(s):
   if t not in ids:ids[t]=len(states);states.append(t)
   v=ids[t]
   if v in row:assert row[v]==w
   row[v]=w
  adj.append(list(row.items()))
 assert (len(states),sum(map(len,adj)))==(82516,144674)
 print('base',len(states),sum(map(len,adj)),flush=True)
 universe=set()
 for x,y,xx,yy in product(range(4),range(-2,3),range(4),range(-2,3)):
  if min(x,xx)<2 and min(y,yy)<=0<=max(y,yy) and sorted((abs(x-xx),abs(y-yy)))==[1,2]:universe.add(edge((x,y),(xx,yy)))
 es=sorted(universe);bits={e:1<<i for i,e in enumerate(es)};assert len(es)==20
 def mask(edges):
  z=0
  for e in edges:z|=bits[e]
  return z
 tests=[];vispairs=[]
 for sign in (1,-1):
  tr=lambda p:(p[0],sign*p[1])
  tests.append(({edge(tr(a),tr(b)):v for a,b,v in TERMS},{edge(tr(a),tr(b)) for a,b in EXC}))
  pairs=[]
  for a,b in combinations(es,2):
   ov=qs(a)&qs(b)
   if len(ov)==2 and any(x in (1,2,3) and y==(0 if sign==1 else -1) for x,y,q in ov) and not (any(x==0 for x,y in a) and any(x==0 for x,y in b)):
    assert cross(a,b);pairs.append((bits[a]|bits[b],a,b,sorted(ov)))
  vispairs.append(pairs)
 # Exact reflection of every visibility pair, including the square-row shift.
 refl=lambda e:edge(*[(x,-y) for x,y in e])
 assert {tuple(sorted((refl(a),refl(b)))) for m,a,b,ov in vispairs[0]}=={tuple(sorted((a,b))) for m,a,b,ov in vispairs[1]}
 pm=[];shifted=[]
 for col,pend in states:
  pm.append(mask(edge(a,b) for a,b,c in pend))
  shifted.append(mask(edge((a[0],a[1]+1),(b[0],b[1]+1)) for a,b,c in pend) if col==0 else 0)
 cache={}
 def flags(m):
  if m not in cache:
   cache[m]=tuple(int(sum(c for e,c in coef.items() if m&bits[e])%3!=2 or all(m&bits[e] for e in exc) or any(m&v==v for v,a,b,ov in vv)) for (coef,exc),vv in zip(tests,vispairs))
  return cache[m]
 nodes=[(u,0) for u,s in enumerate(states) if s[0]==0]; idx={s:i for i,s in enumerate(nodes)};src=[];dst=[];weights=[];gg=[[],[]]
 for i,(u,seen) in enumerate(nodes):
  for v,w in adj[u]:
   final=states[v][0]==0;whole=seen|pm[u]|(shifted[v] if final else pm[v]); key=(v,0 if final else whole)
   if key not in idx:idx[key]=len(nodes);nodes.append(key)
   src.append(i);dst.append(idx[key]);weights.append(4*w-1)
   f=flags(whole) if final else (0,0)
   for k in range(2):gg[k].append(f[k])
 print('mask graph',len(nodes),len(src),'visibility pairs',list(map(len,vispairs)),flush=True)
 src=np.array(src);dst=np.array(dst);weights=np.array(weights);out={}; pots=[]
 for k,name in enumerate(('up','down')):
  cost=weights-4*np.array(gg[k]);d=np.zeros(len(nodes),dtype=np.int64)
  for it in range(1000):
   nd=d.copy();np.minimum.at(nd,dst,d[src]+cost)
   if np.array_equal(nd,d):break
   d=nd
  else:raise AssertionError('no fixed point')
  slack=cost+d[src]-d[dst];assert slack.min()>=0
  boundary=np.array([states[u][0]==0 for u,m in nodes]); print(name,'all range',int(d.min()),int(d.max()),'row boundary range',int(d[boundary].min()),int(d[boundary].max()),flush=True)
  assert (int(d.min()),int(d.max()))==((-29,0) if k==0 else (-33,0))
  np.save('gap/verifier/claim42_potential_'+name+'.npy',d);pots.append(d)
  out[name]={'iterations':it+1,'range':[int(d.min()),int(d.max())],'min_arc_slack':int(slack.min()),'potential_sha256':hashlib.sha256(d.tobytes()).hexdigest()}
  print(name,out[name],flush=True)
 # Sharpness: a zero-cost directed cycle with a positive strong-row count.
 import networkx as nx
 cost=weights-4*np.array(gg[0]);slack=cost+pots[0][src]-pots[0][dst]
 Z=nx.DiGraph();tight=np.nonzero(slack==0)[0]
 Z.add_edges_from((int(src[j]),int(dst[j]),{'arc':int(j)}) for j in tight)
 comp={u:i for i,cc in enumerate(nx.strongly_connected_components(Z)) for u in cc}
 j=next(int(j) for j in tight if gg[0][j] and comp[int(src[j])]==comp[int(dst[j])])
 route=nx.shortest_path(Z,int(dst[j]),int(src[j]));cycle=[j]+[Z[a][b]['arc'] for a,b in zip(route,route[1:])]
 cyc={'arcs':len(cycle),'sum_4w_minus1':int(weights[cycle].sum()),'strong_rows':sum(gg[0][j] for j in cycle)}
 assert cyc['sum_4w_minus1']==4*cyc['strong_rows'] and cyc['strong_rows']>0
 print('critical cycle',cyc,flush=True)
 # Both potentials live on the SAME mask graph, so their interface difference is exact.
 difference=pots[0]-pots[1]; bd=np.array([states[u][0]==0 for u,m in nodes])
 interface={'range':[int(difference[bd].min()),int(difference[bd].max())], 'empty_potentials':[int(p[0]) for p in pots], 'generic_side_error_scaled4':int(-pots[1][bd].min()-difference[bd].min())}
 assert interface['range']==[-4,4] and interface['empty_potentials']==[-17,-17]
 print('interface',interface,flush=True)
 # All candidate squares, including the small radii, are isolated from irrelevant sides.
 from collections import Counter
 geom=[]
 for n in range(32,260,2):
  seen=set()
  for corner in range(4):
   for r in range(12,n//2-3):
    pp=[(r,j) for j in range(1,r+1)]+[(i,r) for i in range(r-1,0,-1)]
    for c in range(corner):pp=[(n-2-y,x) for x,y in pp]
    assert not seen.intersection(pp);seen.update(pp)
    ds=[min(x,y,n-2-x,n-2-y) for x,y in pp]
    assert Counter(d for d in ds if d<4)=={1:2,2:2,3:2}
  geom.append(n)
 report={'date':'2026-10-03','base_states':len(states),'base_arcs':sum(map(len,adj)),'mask_states':len(nodes),'mask_arcs':len(src),'visibility_pairs':vispairs,'potentials':out,'interface':interface,'critical_cycle':cyc,'candidate_geometry_even_n':[min(geom),max(geom)],'seconds':time.monotonic()-start}
 Path('gap/verifier/claim42_check.json').write_text(json.dumps(report,indent=1));print('done',report['seconds'],flush=True)
if __name__=='__main__':main()
