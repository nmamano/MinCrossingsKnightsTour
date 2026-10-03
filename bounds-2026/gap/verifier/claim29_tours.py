"""Independent identity and generous-collar Hall tests on saved closed tours."""
import sys,json
from pathlib import Path
from collections import defaultdict,Counter,deque
from itertools import combinations
sys.path.insert(0,'w-verifier')
from check import check as validate, MOVES
from claim29_window import tile
from claim26_certificate import edge,cross,TERMS,EXC
# claim29_window is imported only for tile(); its executable driver is guarded.

def flow(adj,nresources):
 # capacities scaled by three: every path demands 2 and every pair supplies 3.
 count=len(adj);sink=1+count+nresources; graph=[{} for _ in range(sink+1)]
 def arc(a,b,c):graph[a][b]=c;graph[b][a]=0
 for i,rs in enumerate(adj):
  arc(0,1+i,2)
  for j in rs:arc(1+i,1+count+j,2*count+1)
 for j in range(nresources):arc(1+count+j,sink,3)
 result=0
 while True:
  parent={0:None};q=deque([0])
  while q and sink not in parent:
   u=q.popleft()
   for v,c in graph[u].items():
    if c and v not in parent:parent[v]=u;q.append(v)
  if sink not in parent:break
  v=sink;gain=10**9
  while v:gain=min(gain,graph[parent[v]][v]);v=parent[v]
  v=sink
  while v:u=parent[v];graph[u][v]-=gain;graph[v][u]+=gain;v=u
  result+=gain
 # Source-side cut gives a Hall set if there is a deficit.
 subset=[i for i in range(count) if 1+i in parent]
 return result,subset

def run(file):
 d=json.loads(Path(file).read_text());tour=d['tour'];n=len(tour)
 X,turns=validate(tour)
 es=set()
 for y,row in enumerate(tour):
  for x,code in enumerate(row):
   for v in code:
    dy,dx=MOVES[int(v)]
    es.add(edge((x,n-1-y),(x+dx,n-1-y-dy)))
 assert len(es)==n*n
 es=sorted(es);buckets=defaultdict(list)
 for i,e in enumerate(es):
  for q in tile(e):buckets[q].append(i)
 mult=Counter(len(ids) for ids in buckets.values())
 pairs=Counter()
 for ids in buckets.values():
  for a,b in combinations(ids,2):pairs[a,b]+=1
 assert len(pairs)==X and all(v in (1,2) for v in pairs.values())
 assert all(cross(es[a],es[b]) for a,b in pairs)
 G=4*(n-1)**2-len(buckets);X1=sum(v==1 for v in pairs.values())
 W3=sum((m-1)*(m-2)//2*ct for m,ct in mult.items())
 assert 2*(X-4*n+2)==G+X1+W3
 B=set()
 for a,b in pairs:
  for axis in (0,1):
   for border in (0,n-1):
    if any(v[axis]==border for v in es[a]) and any(v[axis]==border for v in es[b]):B.add((a,b))
 resources=[z for z in pairs if z not in B]
 candidates=[]
 for fx in (0,1):
  for fy in (0,1):
   trans=lambda a:((n-1-a[0]) if fx else a[0],(n-1-a[1]) if fy else a[1])
   local={edge(trans(a),trans(b)) for a,b in es}
   for r in range(12,n//2-3):
    hs=[];bad=False
    for transpose in (False,True):
     def at(p):
      p=(p[0],p[1]+r)
      return (p[1],p[0]) if transpose else p
     F=sum(c for a,b,c in TERMS if edge(at(a),at(b)) in local)
     bad|=all(edge(at(a),at(b)) in local for a,b in EXC)
     c=1-2*(r%2);hs.append(((1+c)//2+c*(F+2))%3)
    if not bad and sum(hs)%3:
     candidates.append((fx,fy,r))
 def near(candidate,z,radius):
  fx,fy,r=candidate
  points=[((n-1-x) if fx else x,(n-1-y) if fy else y) for i in z for x,y in es[i]]
  # Whole support bounding box is a generous superset of the support.
  lx=min(x for x,y in points);hx=max(x for x,y in points)
  ly=min(y for x,y in points);hy=max(y for x,y in points)
  # distance of the box from either closed arm, L-infinity, doubled units.
  def dist(ax,bx,ay,by):
   return max(0,2*lx-bx,ax-2*hx,2*ly-by,ay-2*hy)
  return min(dist(2*r+1,2*r+1,3,2*r+1),dist(3,2*r+1,2*r+1,2*r+1))<=2*radius
 trials=[]
 for radius in (0,1,2,4,8):
  adj=[[j for j,z in enumerate(resources) if near(c,z,radius)] for c in candidates]
  value,subset=flow(adj,len(resources))
  union=set(j for rs in adj for j in rs)
  trials.append(dict(radius=radius,retained=len(candidates),available_union=len(union),scaled_flow=value,scaled_demand=2*len(candidates),hall_subset=[candidates[i] for i in subset] if value<2*len(candidates) else []))
 return dict(source=file,n=n,X=X,E=X-4*n+2,G=G,X1=X1,W3=W3,B=len(B),retained=len(candidates),hall=trials)
if __name__=='__main__':
 files=['w-integrator/tours/FOLD24_n96.json','w-integrator/tours/FOLD24_n98.json','gap/lowerbounds/conn/FIELD_n166_92_155.json']
 out=[]
 for file in files:
  r=run(file);out.append(r);print(json.dumps(r),flush=True)
 Path('gap/verifier/claim29_tours.json').write_text(json.dumps(out,indent=2))
