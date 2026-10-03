"""Independent fold assembler, cut matchings, and reduced exterior transport.
No worker imports. Exact integer geometry; one process.
"""
from pathlib import Path
from collections import defaultdict,Counter
import json
from check import MOVES,proper
SHIFT=((0,6),(6,24),(18,0),(24,18),(0,0),(0,24),(24,0),(24,24),(0,12),(12,0),(12,24),(24,12),(12,12))

def rot(p,n,r):
 x,y=p
 for _ in range(r%4):x,y=n-1-y,x
 return x,y

def turn(v,r):
 x,y=v
 for _ in range(r%4):x,y=-y,x
 return x,y

def patches(d,n):
 delta=n-d['n0'];out={}
 for block,(sx,sy) in zip(d['components'],SHIFT):
  ox,oy=block['offset']
  for key,ds in block['cells'].items():
   x,y=map(int,key.split(','));p=(ox+x+sx*delta//24,oy+y+sy*delta//24)
   assert p not in out;out[p]=tuple(map(tuple,ds))
 return out

def build(d,n):
 assert (n-d['n0'])%12==0
 h=n//2;g={(x,y):set() for x in range(n) for y in range(n)}
 for x,y in g:
  if x<h and y<h:v=(2,1) if y>x+1 else (-1,-2)
  elif x>=h and y<h:v=(-1,2) if x+y<n-2 else (2,-1)
  elif x>=h and y>=h:v=(-2,-1) if x-y>1 else (1,2)
  else:v=(1,-2) if x+y>n else (-2,1)
  q=(x+v[0],y+v[1])
  if q in g:g[x,y].add(q);g[q].add((x,y))
 for r in range(4):
  for y in range(n):
   p=rot((0,y),n,r)
   if len(g[p])!=1:continue
   ends={rot((2,y+s),n,r):s for s in (-1,1)}
   q=next(iter(g[p]))
   if q not in ends:continue
   sign=ends[q]*(-1 if h-n//4<=y<h else 1)
   q=rot((1,y+2*sign),n,r)
   if q in g and len(g[q])==1 and q not in g[p]:g[p].add(q);g[q].add(p)
 mid=set()
 for r in range(4):
  for x in range(11,h-11):
   for j in range(3):
    p=rot((x,x+j),n,r);mid.add(p)
    moves=[turn(v,r) for v in d['template'][f'{r}:{(x-8)%6},{j}']]
    g[p]={(p[0]+a,p[1]+b) for a,b in moves}
 patch=patches(d,n)
 for p,ds in patch.items():g[p]={(p[0]+a,p[1]+b) for a,b in ds}
 for p,ns in g.items():
  assert len(ns)==2
  for q in ns:assert q in g and p in g[q] and sorted((abs(q[0]-p[0]),abs(q[1]-p[1])))==[1,2]
 seen=set();sizes=[]
 for p in g:
  if p in seen:continue
  todo=[p];seen.add(p);size=0
  while todo:
   v=todo.pop();size+=1
   for w in g[v]:
    if w not in seen:seen.add(w);todo.append(w)
  sizes.append(size)
 retained=mid|set(patch)|{p for p in g if min(*p,n-1-p[0],n-1-p[1])<=1}
 return g,retained,patch,sorted(sizes)

def label(p,n,kind,r):
 x,y=rot(p,n,-r);h=n//2
 if kind=='corner':return max(2*x-y,2*y-x) if x<h and y<h else None
 return 2*min(y,n-y)-x if x<h else None

def match_region(g,S,stub):
 unseen=set(S);matching={};components=0
 while unseen:
  p=next(iter(unseen));unseen.remove(p);todo=[p];ends=[]
  while todo:
   v=todo.pop()
   for w in g[v]:
    if w not in S:ends.append(stub[v,w])
    elif w in unseen:unseen.remove(w);todo.append(w)
  assert len(ends)==2,('hidden cycle or invalid path',len(ends))
  a,b=ends;assert a not in matching and b not in matching
  matching[a]=b;matching[b]=a;components+=1
 return matching,components

def extract(g,n,kind,r,lo,width):
 lab={p:label(p,n,kind,r) for p in g}
 S={p for p,c in lab.items() if c is not None and lo<=c<lo+width}
 descriptions={};names=[set(),set()]
 for p in S:
  for q in g[p]-S:
   assert lab[q] is not None
   side=int(lab[q]>=lo+width);cut=lo+side*width
   a,b=sorted((p,q),key=lab.get)
   assert lab[a]<cut<=lab[b] and lab[b]-lab[a]<=5
   x,y=rot(a,n,-r);xx,yy=rot(b,n,-r)
   if kind=='corner':
    tag,depth=('L',(x,xx)) if max(x,xx)<=2 else ('B',(y,yy)) if max(y,yy)<=2 else ('D',(y-x,yy-xx))
   else:tag,depth=('lo' if y<n//2 else 'hi'),(x,xx)
   name=(tag,*depth,lab[a]-cut,lab[b]-cut)
   assert name not in names[side];names[side].add(name);descriptions[p,q]=(side,name)
 assert names[0]==names[1]
 ordered=sorted(names[0]);stub={e:(s,ordered.index(k)) for e,(s,k) in descriptions.items()}
 M,_=match_region(g,S,stub)
 return {'cells':S,'ports':stub,'names':ordered,'matching':M}

def union_matching(M,power):
 adj=defaultdict(list)
 def add(a,b):adj[a].append(b);adj[b].append(a)
 width=len(M)//2
 for k in range(power):
  for a,b in M.items():
   if a<b:add((k,*a),(k,*b))
 for k in range(power-1):
  for j in range(width):add((k,1,j),(k+1,0,j))
 ends={(0,0,j):(0,j) for j in range(width)}|{(power-1,1,j):(1,j) for j in range(width)}
 unseen=set(adj);out={}
 while unseen:
  p=unseen.pop();todo=[p];ports=[]
  while todo:
   v=todo.pop()
   if v in ends:ports.append(ends[v])
   for w in adj[v]:
    if w in unseen:unseen.remove(w);todo.append(w)
  assert len(ports)==2,('composition hidden cycle',ports)
  a,b=ports;out[a]=b;out[b]=a
 return out

def exterior(g,blocks):
 inside=set();stub={}
 for key,b in blocks.items():
  assert not inside&b['cells'];inside|=b['cells']
  for (p,q),port in b['ports'].items():stub[q,p]=(key,*port)
 assert all(q not in inside for q,p in stub)
 M,_=match_region(g,set(g)-inside,stub)
 return M,inside,stub

def cycle_count(out,blocks,power):
 adj=defaultdict(list)
 for p,q in out.items():adj[p].append(q)
 for key,b in blocks.items():
  for p,q in union_matching(b['matching'],power).items():adj[key,*p].append((key,*q))
 assert all(len(v)==2 for v in adj.values())
 unseen=set(adj);count=0
 while unseen:
  todo=[unseen.pop()];count+=1
  while todo:
   for q in adj[todo.pop()]:
    if q in unseen:unseen.remove(q);todo.append(q)
 return count

def reduced_exterior(g,R,inside,stub):
 keep=R-inside;edges=Counter();seen=set()
 for p in keep:
  for q in g[p]:
   begin=('v',p)
   if q in inside:end=('p',stub[p,q])
   else:
    prev,cur=p,q
    while cur not in keep:
     seen.add(cur);nxt=next(v for v in g[cur] if v!=prev)
     assert nxt not in inside,'cut port not retained'
     prev,cur=cur,nxt
    end=('v',cur)
   if end[0]=='p' or p<end[1]:edges[tuple(sorted((begin,end),key=repr))]+=1
 assert seen|keep==set(g)-inside,'untraced suppressed piece'
 return edges

def transport(d,n0,n,R0,R1,B0,B1):
 k=(n-n0)//24;mapping={}
 def put(p,q):
  if p in B0:return
  assert q not in B1
  if p in mapping:assert mapping[p]==q,('overlapping placement rules',p,q,mapping[p])
  mapping[p]=q
 # Finite component translations.
 for co,(sx,sy) in zip(d['components'],SHIFT):
  for key in co['cells']:
   x,y=map(int,key.split(','));p=(co['offset'][0]+x,co['offset'][1]+y)
   put(p,(p[0]+k*sx,p[1]+k*sy))
 # Five boundary intervals, separated by the actual eight block cuts.
 for r in range(4):
  for depth in (0,1):
   runs=[];run=[]
   for y in range(n0):
    p=rot((depth,y),n0,r)
    if p in B0:
     if run:runs.append(run);run=[]
    else:run.append(y)
   if run:runs.append(run)
   assert len(runs)==5
   for j,ys in enumerate(runs):
    for y in ys:put(rot((depth,y),n0,r),rot((depth,y+6*k*j),n,r))
 # Diagonal pieces before and after the corner block.
 for r in range(4):
  for x in range(11,n0//2-11):
   for j in range(3):
    p=rot((x,x+j),n0,r)
    if p in B0:continue
    delta=0 if x+2*j<24 else 12*k
    put(p,rot((x+delta,x+j+delta),n,r))
 assert set(mapping)==R0-B0
 assert len(set(mapping.values()))==len(mapping) and set(mapping.values())==R1-B1
 return mapping

def crossings(g):
 buckets=defaultdict(list);edges=[];out=[]
 for p in sorted(g):
  for q in sorted(g[p]):
   if p>q:continue
   e=(p,q);keys=[(x,y) for x in range(min(p[0],q[0])//4,max(p[0],q[0])//4+1) for y in range(min(p[1],q[1])//4,max(p[1],q[1])//4+1)]
   for j in {j for key in keys for j in buckets[key]}:
    if proper(e,edges[j]):out.append((e,edges[j]))
   idx=len(edges);edges.append(e)
   for key in keys:buckets[key].append(idx)
 return out

def count_local(pairs,n,kind,r,lo,width):
 totals=[0,0,0]
 for pair in pairs:
  ps=[rot(p,n,-r) for e in pair for p in e]
  if any(x>=n//2 or kind=='corner' and y>=n//2 for x,y in ps):continue
  cs=[max(2*x-y,2*y-x) if kind=='corner' else 2*min(y,n-y)-x for x,y in ps]
  if lo<=min(cs)<lo+width:
   totals[0]+=1
   boundary=kind=='side' or any(min(x,y)<=2 for x,y in ps)
   totals[1 if boundary else 2]+=1
 return totals

def main():
 report=[]
 for n0 in range(96,120,2):
  d=json.loads(Path(f'w-integrator/corners/FOLD24_base_n{n0}.json').read_text())
  row={'n0':n0,'checks':[]}
  base=None
  for k in (0,1,2,8):
   n=n0+24*k;g,R,patch,sizes=build(d,n);assert sizes==[n*n]
   if k<=2:
    stored=json.loads(Path(f'w-integrator/tours/FOLD24_n{n}.json').read_text())
    assert all(g[x,n-1-y]=={(x+MOVES[int(c)][1],n-1-y-MOVES[int(c)][0]) for c in stored['tour'][y][x]} for x,y in ((x,y) for x in range(n) for y in range(n)))
   blocks={}
   for kind in ('corner','side'):
    for r in range(4):
     a=24 if kind=='corner' else n//2+16
     b=extract(g,n,kind,r,a,6+12*k);assert not b['cells']&set(patch);blocks[kind,r]=b
     if k==0:
      other=extract(g,n,kind,r,a+6,6)
      assert (b['names'],b['matching'])==(other['names'],other['matching'])
      if kind=='corner':assert union_matching(b['matching'],2)==b['matching']
      else:assert all(b['matching'][0,i]==(1,(i+1)%4) for i in range(4))
     else:
      old=base['blocks'][kind,r]
      assert b['names']==old['names'] and b['matching']==union_matching(old['matching'],1+2*k)
   outside,inside,stub=exterior(g,blocks)
   red=reduced_exterior(g,R,inside,stub)
   pairs=crossings(g);cost=0
   for (kind,r),b in blocks.items():
    counts=count_local(pairs,n,kind,r,24 if kind=='corner' else n//2+16,6+12*k)
    expected=(10,6,4) if kind=='corner' else (9,9,0)
    assert counts==[c*(1+2*k) for c in expected];cost+=counts[0]
   turns=sum(sum(q[0]-p[0] for q in ns)!=0 or sum(q[1]-p[1] for q in ns)!=0 for p,ns in g.items())
   if k==0:
    assert cycle_count(outside,blocks,1)==cycle_count(outside,blocks,3)==1
    base={'blocks':blocks,'R':R,'inside':inside,'outside':outside,'red':red,'X':len(pairs),'T':turns,'residual':len(pairs)-cost}
    row['ports']=[{'kind':kind,'rotation':r,'names':b['names'],'matching':[[a,z] for a,z in sorted(b['matching'].items()) if a<z]} for (kind,r),b in blocks.items()]
   else:
    assert outside==base['outside']
    mapping=transport(d,n0,n,base['R'],R,base['inside'],inside)
    def moved(node):return ('v',mapping[node[1]]) if node[0]=='v' else node
    moved_edges=Counter({tuple(sorted((moved(a),moved(b)),key=repr)):v for (a,b),v in base['red'].items()})
    assert red==moved_edges,('outside reduced graph transport',n0,n)
    assert len(pairs)==base['X']+152*k and turns==base['T']+304*k
    assert len(pairs)-cost==base['residual']
   row['checks'].append({'n':n,'k':k,'X':len(pairs),'T':turns,'outside_ports':len(outside),'reduced_exterior_edges':sum(red.values()),'residual_crossings':len(pairs)-cost})
   print('PASS',n0,'k',k,'n',n,'X',len(pairs),'T',turns,flush=True)
  n=n0+12;g,R,patch,sizes=build(d,n)
  blocks={(kind,r):extract(g,n,kind,r,24 if kind=='corner' else n//2+16,12) for kind in ('corner','side') for r in range(4)}
  outside,_,_=exterior(g,blocks);assert outside==base['outside']
  for key,b in blocks.items():assert b['names']==base['blocks'][key]['names'] and b['matching']==union_matching(base['blocks'][key]['matching'],2)
  assert len(sizes)==cycle_count(base['outside'],base['blocks'],2)
  row['step12']={'n':n,'cycle_sizes':sizes};report.append(row)
  Path('w-verifier/claim23b_fold_results.json').write_text(json.dumps(report,indent=1))
 print('PASS 48 independent full reconstructions, 12 step-12 graphs, exterior graph transport and all counts.',flush=True)
if __name__=='__main__':main()
