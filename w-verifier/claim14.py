"""Independent Claim 14 certificates. One process. No worker imports."""
from pathlib import Path
from itertools import combinations,product
from collections import deque,Counter
from fractions import Fraction
import json
import networkx as nx
from claim11_forest import transitions,potentials
from claim9_tiles import proper,quarters

def width1_transitions(s):
 x,pend=s;p=(x,0)
 inc=[e for e in pend if e[1]==p];keep=[e for e in pend if e[1]!=p]
 if len(inc)>2 or len(inc)==2 and inc[0][2]==inc[1][2]:return
 possible=[(p,(xx,dy)) for xx in range(3) for dy in (1,2) if sorted((abs(xx-x),dy))==[1,2] and min(x,xx)<1]
 need=[2-len(inc)] if x<1 else range(3-len(inc))
 for k in need:
  for chosen in combinations(possible,k):
   if any(sum(e[1]==q for e in keep)+sum(e[1]==q for e in chosen)>2 for a,q in chosen):continue
   labels={e[2] for e in inc};merged=min(labels) if labels else -1
   result=[(a,b,merged if c in labels else c) for a,b,c in keep]+[(a,b,merged) for a,b in chosen]
   weight=sum(proper(e,(a,b)) for e in chosen for a,b,c in keep)+sum(proper(e,f) for e,f in combinations(chosen,2))
   shift=int(x==2);ren={};canon=[]
   for a,b,c in sorted(result):
    if c not in ren:ren[c]=len(ren)
    canon.append(((a[0],a[1]-shift),(b[0],b[1]-shift),ren[c]))
   yield ((x+1)%3,tuple(canon)),weight

def boundary():
 opts=list(combinations([(1,-2),(1,2),(2,-1),(2,1)],2))
 def edges(c,y):return [((0,y),(x,y+d)) for x,d in opts[c]]
 states=[()];ids={():0};arcs=[]
 for u,s in enumerate(states):
  for c in range(6):
   t=(s+(c,))[-3:]
   if t not in ids:ids[t]=len(states);states.append(t)
   w=sum(proper(e,f) for e in edges(c,0) for j,p in enumerate(reversed(s),1) for f in edges(p,-j))
   arcs.append((u,ids[t],w))
 h=potentials(len(states),arcs,[w-1 for u,v,w in arcs],0)
 unrestricted_min=min(h)
 states1=[(0,())];idx1={states1[0]:0};arcs1=[]
 for u,s1 in enumerate(states1):
  for t,w in width1_transitions(s1):
   if t not in idx1:idx1[t]=len(states1);states1.append(t)
   arcs1.append((u,idx1[t],w))
 h1=potentials(len(states1),arcs1,[3*w-1 for u,v,w in arcs1],0)
 assert len(states1)==330 and min(h1)==-3
 assert all(c+h1[u]-h1[v]>=0 for (u,v,w),c in zip(arcs1,[3*w-1 for u,v,w in arcs1]))
 # Pairs with source rows separated by >=4 cannot cross (vertical spans at most 4).
 assert all(not proper(e,f) for a,b in product(range(6),repeat=2) for e in edges(a,0) for f in edges(b,4))
 es={e for c in range(6) for y in range(-6,7) for e in edges(c,y)}
 pairs=[(e,f) for e,f in combinations(sorted(es),2) if proper(e,f)]
 assert len(pairs)==115
 overlap=set().union(*(quarters(e)&quarters(f) for e,f in pairs))
 assert all(i<2 and (i!=1 or k==3) for i,j,k in overlap)
 # Claim 15 correction: an edge at the origin also meets both side classes.
 corneredges={((0,0),(1,2)),((0,0),(2,1)),((0,1),(2,0)),((0,2),(1,0))}
 assert len(corneredges)==4
 assert sum(proper(e,f) for e,f in combinations(corneredges,2))==5
 out={'states':len(states),'arcs':len(arcs),'unrestricted_minimum':unrestricted_min,'forest_states':len(states1),'forest_arcs':len(arcs1),'forest_start_potential_scaled3':min(h1),'crossing_pairs':len(pairs),'right_square_overlap_quarters':sorted({k for i,j,k in overlap if i==1}),'max_duplicate_pair_per_corner':5}
 print('boundary',out,flush=True)
 return out

def geometry():
 out=[]
 for n in (32,48,64,96,120):
  U=set();seen=set();rowsets=[[],[]]
  for fx,fy in product((0,1),repeat=2):
   tr=lambda p:((2*(n-1)-p[0]) if fx else p[0],(2*(n-1)-p[1]) if fy else p[1])
   for R in range(12,n//2-3):
    pts=[(2*R+1,y) for y in range(3,2*R+2,2)]+[(x,2*R+1) for x in range(2*R-1,2,-2)]
    for a,b in zip(pts,pts[1:]):
     a,b=tr(a),tr(b);key=tuple(sorted((a,b)));assert key not in seen;seen.add(key)
     if a[1]==b[1]:
      k=(a[0]+b[0])//4;j=(a[1]-1)//2;ts=[(k-1,j,1),(k,j,3)]
     else:
      i=(a[0]-1)//2;k=(a[1]+b[1])//4;ts=[(i,k-1,2),(i,k,0)]
     for t in ts:assert t not in U;U.add(t);assert 1<=t[0]<n-2 and 1<=t[1]<n-2
  for axis,flip in product((0,1),repeat=2):
   def tr(p):
    x,y=p
    if flip:x=n-1-x
    return (y,x) if axis else (x,y)
   es=[(tr((0,y)),tr((x,y+d))) for y in range(n) for x,d in ((1,-2),(1,2),(2,-1),(2,1)) if 0<=y+d<n]
   for e,f in combinations(es,2):
    if proper(e,f):assert not ((quarters(e)&quarters(f))&U)
  # Every interval of bad rows, including one crossing the middle.
  windows=[set(range(R-1,R+3)) for R in range(12,n//2-3)]
  windows+= [{n-1-y for y in s} for s in windows]
  slack=0
  for a in range(n):
   for b in range(a,n):
    lost=sum(any(a<=y<=b for y in s) for s in windows)
    assert lost<=b-a+4
    slack=max(slack,lost-(b-a+1))
  out.append({'n':n,'dual_edges':len(seen),'quarters':len(U),'maximum_run_overhead':slack})
 print('geometry',out,flush=True);return out

def runs():
 states=[(0,())];index={states[0]:0};arcs=[]
 for u,s in enumerate(states):
  outgoing={}
  for t,w in transitions(s):
   if t not in index:index[t]=len(states);states.append(t)
   v=index[t];outgoing[v]=min(outgoing.get(v,w),w)
  arcs.extend((u,v,w) for v,w in outgoing.items())
 N=len(states);assert (N,len(arcs))==(82516,144674)
 d=potentials(N,arcs,[4*w-1 for u,v,w in arcs],0)
 G=nx.DiGraph();G.add_nodes_from(range(N));G.add_edges_from((u,v) for u,v,w in arcs if 4*w-1+d[u]-d[v]==0)
 comps=[c for c in nx.strongly_connected_components(G) if len(c)>1 or any(G.has_edge(u,u) for u in c)]
 critical={(u,v) for c in comps for u in c for v in G[u] if v in c};assert len(critical)==8
 augmented=[];costs=[];losses=[]
 for u,v,w in arcs:
  for flag,previous in product((0,1),repeat=2):
   dirty=int(flag or (u,v) not in critical);end=states[v][0]==0
   loss=(dirty+3*dirty*(1-previous)) if end else 0
   nf,np=(0,dirty) if end else (dirty,previous)
   a,b=4*u+2*flag+previous,4*v+2*nf+np
   augmented.append((a,b,w));losses.append(loss);costs.append(7*(4*w-1)-8*loss)
 print('run graph',4*N,len(augmented),flush=True)
 h=potentials(4*N,augmented,costs)
 assert (min(h),max(h))==(-167,0)
 assert all(c+h[a]-h[b]>=0 for (a,b,w),c in zip(augmented,costs))
 full=nx.DiGraph();full.add_edges_from((a,b) for a,b,w in augmented)
 reach=nx.descendants(full,0)|{0};del full
 Z=nx.DiGraph();Z.add_nodes_from(reach)
 Z.add_edges_from((a,b) for (a,b,w),c in zip(augmented,costs) if a in reach and c+h[a]-h[b]==0)
 belong={u:i for i,c in enumerate(nx.strongly_connected_components(Z)) for u in c}
 a,b=next((a,b) for (a,b,w),c,l in zip(augmented,costs,losses) if l and a in reach and c+h[a]-h[b]==0 and belong[a]==belong[b])
 nodes=[a]+nx.shortest_path(Z,b,a)
 lookup={(a,b):(w,l) for (a,b,w),l in zip(augmented,losses)}
 offset=next(i for i,a in enumerate(nodes[:-1]) if states[a//4][0]==0)
 nodes=nodes[:-1];nodes=nodes[offset:]+nodes[:offset];nodes.append(nodes[0])
 W=sum(lookup[a,b][0] for a,b in zip(nodes,nodes[1:]));L=sum(lookup[a,b][1] for a,b in zip(nodes,nodes[1:]));S=len(nodes)-1
 bad=[int(any((nodes[j+k]//4,nodes[j+k+1]//4) not in critical for k in range(4))) for j in range(0,S,4)]
 assert L==sum(bad)+3*sum(b and not bad[i-1] for i,b in enumerate(bad))
 assert Fraction(4*W-S,4*L)==Fraction(2,7)
 neg=5000*(4*W-S)-4*1431*L;assert neg<0
 out={'base_states':N,'base_arcs':len(arcs),'augmented_states':4*N,'augmented_arcs':len(augmented),'reachable_states':len(reach),'potential_scaled28':[min(h),max(h)],'witness':{'steps':S,'weight':W,'loss':L,'bad_rows':bad,'ratio':'2/7','negative_at_1431_5000_scaled20000':neg,'states':[[states[a//4],(a%4)//2,a%2] for a in nodes],'arc_weights':[lookup[a,b][0] for a,b in zip(nodes,nodes[1:])]}}
 print('potential',min(h),max(h),'witness',S,W,L,bad,'negative',neg,flush=True);return out
if __name__=='__main__':
 out={'date':'2026-10-02','boundary':boundary(),'geometry':geometry(),'runs':runs()}
 Path('w-verifier/claim14.json').write_text(json.dumps(out,indent=1))
