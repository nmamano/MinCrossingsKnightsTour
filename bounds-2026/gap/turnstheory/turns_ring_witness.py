"""Join the sampled -7 corner to its reflection using zero-cost width-4 rows.
Checks a free-interior boundary ring; makes no full-board completion claim.
"""
import collections,json,pickle
from pathlib import Path
from turns_gap_scan import lower,turn
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).parent
states,arcs=pickle.load(open(ROOT/'gap/lowerbounds/turns_ring/strip_W4.pkl','rb'));ids={s:i for i,s in enumerate(states)}
Z=collections.defaultdict(dict)
for u,v,c,ch in arcs:
 if c==0:Z[u][v]=ch

def reflect(s):return frozenset((x+dx,-1-y-dy,-dx,dy) for x,y,dx,dy in s)

def path(u,v,length):
 levels=[{u:None}]
 for t in range(length):
  nxt={}
  for a in levels[-1]:
   for b in Z[a]:nxt.setdefault(b,a)
  levels.append(nxt)
 if v not in levels[-1]:return None
 out=[v]
 for d in reversed(levels[1:]):out.append(d[out[-1]])
 return out[::-1]

sample=json.load(open(OUT/'turns_gap_extend.json'))['corner_runs'][0]['samples'][0]
K=8;corner={tuple(p):(tuple(a),tuple(b)) for p,a,b in sample['chosen']}
uv=[s['cuts'][-1]['state'] for s in sample['sides']]
r_uv=[ids[reflect(states[u])] for u in uv]
results=[]
for n in (32,40,48,64,96):
 paths=[path(u,v,n-2*K) for u,v in zip(uv,r_uv)]
 if any(p is None for p in paths):results.append(dict(n=n,joined=False));continue
 chosen={}
 def put(p,ds,sx,sy):
  x,y=p;px=x if sx==1 else n-1-x;py=y if sy==1 else n-1-y
  assert (px,py) not in chosen
  chosen[px,py]=tuple((sx*dx,sy*dy) for dx,dy in ds)
 for sx in (1,-1):
  for sy in (1,-1):
   for p,ds in corner.items():
    if min(p)<4:put(p,ds,sx,sy)
 for d,pa in enumerate(paths):
  for j,(u,v) in enumerate(zip(pa,pa[1:])):
   for x,ds in Z[u][v]:
    if d==0:
     for sx in (1,-1):put((x,K+j),ds,sx,1)
    else:
     for sy in (1,-1):put((K+j,x),tuple((dy,dx) for dx,dy in ds),1,sy)
 assert len(chosen)==n*n-(n-8)**2
 ghosts=collections.Counter();adj={p:[] for p in chosen};cost=0
 for (x,y),ds in chosen.items():
  p=x,y
  cost+=turn(ds)-lower(x,[dx for dx,dy in ds])-lower(n-1-x,[-dx for dx,dy in ds])-lower(y,[dy for dx,dy in ds])-lower(n-1-y,[-dy for dx,dy in ds])
  for dx,dy in ds:
   q=x+dx,y+dy;assert 0<=q[0]<n and 0<=q[1]<n
   if q in chosen:
    assert (-dx,-dy) in chosen[q],(n,p,q)
    adj[p].append(q)
   else:ghosts[q]+=1
 assert cost==-28
 seen=set();cycles=[]
 for p in chosen:
  if p in seen:continue
  cc=set();stack=[p]
  while stack:
   v=stack.pop()
   if v in cc:continue
   cc.add(v);stack.extend(adj[v])
  seen|=cc
  if all(len(adj[v])==2 for v in cc):cycles.append(len(cc))
 ghost_sources=collections.defaultdict(list)
 for p,ds in chosen.items():
  for dx,dy in ds:
   q=p[0]+dx,p[1]+dy
   if q not in chosen:ghost_sources[q].append(p)
 forced_turns=[q for q,ps in ghost_sources.items() if len(ps)==2 and (ps[0][0]+ps[1][0],ps[0][1]+ps[1][1])!=(2*q[0],2*q[1])]
 overloaded=[[q,ps] for q,ps in sorted(ghost_sources.items()) if len(ps)>2]
 r=dict(n=n,joined=True,residual=cost,internal_cycles=cycles,ghost_degree_hist=dict(collections.Counter(ghosts.values())),forced_ghost_turns=len(forced_turns),overloaded=overloaded,paths=paths)
 results.append(r)
 if n==48:
  (OUT/'turns_ring_n48.json').write_text(json.dumps(dict(n=n,chosen=[[p,*ds] for p,ds in sorted(chosen.items())],result=r),indent=2))
 print({k:v for k,v in r.items() if k!='paths'},flush=True)
(OUT/'turns_ring_witness.json').write_text(json.dumps(dict(date='2026-10-04',K=K,corner_sample=0,terminal=uv,reflected_terminal=r_uv,results=results),indent=2))
