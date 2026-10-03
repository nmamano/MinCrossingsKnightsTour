"""Corner interface samples and zero-cost side classification. Run from research root.
One solver worker. Sampling is not exhaustive; every saved witness is checked.
"""
import argparse, collections, json, math, pickle, time
from itertools import combinations
from pathlib import Path
import networkx as nx
from ortools.sat.python import cp_model
ROOT=Path(__file__).resolve().parents[2]
OUT=Path(__file__).parent
M=[(dx,dy) for dx in (-2,-1,1,2) for dy in (-2,-1,1,2) if abs(dx)+abs(dy)==3]
def lower(x,ds):
 if x==0:return 1
 if x in (1,2):return sum(x+d in (0,3) for d in ds)-1
 if x==3:return 1-sum(x+d in (1,2) for d in ds)
 return 0
def turn(ds):return int(tuple(map(sum,zip(*ds)))!=(0,0))
def residual(p,ds):return turn(ds)-lower(p[0],[d[0] for d in ds])-lower(p[1],[d[1] for d in ds])
def sidecost(x,ds):return turn(ds)-lower(x,[d[0] for d in ds])
def side_graph():
 states,arcs=pickle.load(open(ROOT/'gap/lowerbounds/turns_ring/strip_W4.pkl','rb'))
 Z=nx.DiGraph();Z.add_nodes_from(range(len(states)))
 Z.add_edges_from((u,v) for u,v,c,ch in arcs if c==0)
 classes=sorted([c for c in nx.strongly_connected_components(Z) if len(c)>1 or Z.has_edge(next(iter(c)),next(iter(c)))],key=lambda c:(len(c),min(c)))
 reach=[0]*len(states); info=[]
 for i,C in enumerate(classes):
  for u in C:reach[u]|=1<<i
  G=Z.subgraph(C); r=min(C); lev={r:0}; q=[r]; period=0
  for u in q:
   for v in G[u]:
    if v not in lev:lev[v]=lev[u]+1;q.append(v)
    period=math.gcd(period,lev[u]+1-lev[v])
  rows=collections.Counter(); examples={}
  for u,v,c,ch in arcs:
   if c==0 and u in C and v in C:
    ts=sum(turn(ds) for x,ds in ch);rows[ts]+=1;examples.setdefault(ts,ch)
  info.append(dict(id=i,states=len(C),arcs=G.number_of_edges(),period=period,row_turn_counts=dict(rows),examples=examples,representative=sorted(states[r])))
 q=collections.deque(u for u,v in enumerate(reach) if v)
 while q:
  v=q.popleft()
  for u in Z.predecessors(v):
   m=reach[u]|reach[v]
   if m!=reach[u]:reach[u]=m;q.append(u)
 return states,{s:i for i,s in enumerate(states)},arcs,reach,info

def inspect(K,chosen,ids,reach):
 C=set(chosen); adj={p:[] for p in C}
 for p,ds in chosen.items():
  assert len(set(ds))==2
  for d in ds:
   assert d in M
   q=(p[0]+d[0],p[1]+d[1]);assert min(q)>=0
   if q in C:
    assert (-d[0],-d[1]) in chosen[q]
    adj[p].append(q)
 seen=set(); cycles=[]
 for p in sorted(C):
  if p in seen:continue
  cc=set();stack=[p]
  while stack:
   v=stack.pop()
   if v in cc:continue
   cc.add(v);stack.extend(adj[v])
  seen|=cc
  if all(len(adj[v])==2 for v in cc):cycles.append(cc)
 traces=[]
 for swap in (False,True):
  data={(y,x) if swap else (x,y):tuple((dy,dx) if swap else (dx,dy) for dx,dy in ds) for (x,y),ds in chosen.items()}
  cuts=[]
  for cut in range(4,K+1):
   st=frozenset((x,y-cut,dx,dy) for (x,y),ds in data.items() if x<4 and y<cut for dx,dy in ds if 0<=x+dx<4 and y+dy>=cut)
   sid=ids.get(st); mask=reach[sid] if sid is not None else 0
   cuts.append(dict(row=cut,state=sid,reachable_zero_classes=[i for i in range(3) if mask>>i&1],pending=sorted(st)))
  traces.append(dict(side='bottom' if swap else 'left',row_turns=[sum(turn(data[x,y]) for x in range(4)) for y in range(4,K)],row_slack=[sum(sidecost(x,data[x,y]) for x in range(4)) for y in range(4,K)],cuts=cuts))
 return sum(residual(p,ds) for p,ds in chosen.items()),cycles,traces

def sample(K,target,count,limit,ids,reach,extend=False):
 m=cp_model.CpModel(); pv={};inc=collections.defaultdict(list);cs=[]
 for p in [(x,y) for x in range(K) for y in range(K)]:
  opts=[]
  for ds in combinations([d for d in M if p[0]+d[0]>=0 and p[1]+d[1]>=0],2):
   z=m.NewBoolVar('');pv[p,ds]=z;opts.append(z);cs.append(residual(p,ds)*z)
   for dx,dy in ds:inc[p,(p[0]+dx,p[1]+dy)].append(z)
  m.AddExactlyOne(opts)
 for p,q in list(inc):
  if q[0]<K and q[1]<K and p<q:m.Add(sum(inc[p,q])==sum(inc[q,p]))
 m.Add(sum(cs)==target)
 if extend:
  edge_types=sorted(set().union(*ids))
  table=[tuple(int(e in st) for e in edge_types) for st,i in ids.items() if reach[i]]
  for swap in (False,True):
   vs=[]
   for x,y,dx,dy in edge_types:
    p=(x,K+y);q=(x+dx,K+y+dy)
    if swap:p=p[::-1];q=q[::-1]
    z=m.NewBoolVar('terminal');m.Add(z==sum(inc[p,q]));vs.append(z)
   m.AddAllowedAssignments(vs,table)
 records=[];cuts=0;start=time.monotonic();status='UNSTARTED'
 for trial in range(count*12):
  s=cp_model.CpSolver();s.parameters.num_workers=1;s.parameters.max_time_in_seconds=limit;s.parameters.random_seed=trial
  st=s.Solve(m);status=s.StatusName(st)
  if st not in (cp_model.OPTIMAL,cp_model.FEASIBLE):break
  chosen={p:ds for (p,ds),z in pv.items() if s.Value(z)}
  val,cycles,traces=inspect(K,chosen,ids,reach);assert val==target
  if cycles:
   for cc in cycles:
    es=[sum(inc[p,q]) for p in cc for q in cc if p<q and (p,q) in inc and any((p[0]+d[0],p[1]+d[1])==q for d in chosen[p])]
    m.Add(sum(es)<=len(cc)-1);cuts+=1
   continue
  projection=[pv[p,ds] for p,ds in chosen.items() if (p[0]<4 and p[1]>=K-2) or (p[1]<4 and p[0]>=K-2)]
  m.Add(sum(projection)<=len(projection)-1)
  records.append(dict(residual=val,chosen=[[p,*ds] for p,ds in sorted(chosen.items())],sides=traces))
  if len(records)>=count:break
 return dict(K=K,target=target,samples=records,last_status=status,exhausted=status=='INFEASIBLE',cycle_cuts=cuts,seconds=round(time.monotonic()-start,3))

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--samples',type=int,default=8);ap.add_argument('--seconds',type=float,default=3);ap.add_argument('--sizes',type=int,nargs='+',default=[8,12]);ap.add_argument('--extend',action='store_true');a=ap.parse_args()
 states,ids,arcs,reach,info=side_graph()
 local={str(x):[ds for ds in combinations([d for d in M if x+d[0]>=0],2) if sidecost(x,ds)==0] for x in range(4)}
 report=dict(date='2026-10-04',graph=dict(states=len(states),arcs=len(arcs),classes=info),local_zero_pairs=local,corner_runs=[])
 path=OUT/('turns_gap_extend.json' if a.extend else 'turns_gap_samples.json');path.write_text(json.dumps(report,indent=2))
 print('SIDE',json.dumps(report['graph']),flush=True)
 for K in a.sizes:
  for target in (-7,-6,-5,-4):
   result=sample(K,target,a.samples,a.seconds,ids,reach,a.extend);report['corner_runs'].append(result);path.write_text(json.dumps(report,indent=2))
   pairs=collections.Counter(tuple(tuple(t['cuts'][-1]['reachable_zero_classes']) for t in r['sides']) for r in result['samples'])
   print('CORNER',K,target,len(result['samples']),result['last_status'],result['seconds'],'classes',dict(pairs),flush=True)
if __name__=='__main__':main()
