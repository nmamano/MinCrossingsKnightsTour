"""Standard-library coordinate and forced-ray check of saved integer corners."""
import collections,json,sys
from fractions import Fraction
from pathlib import Path
M={(dx,dy) for dx in (-2,-1,1,2) for dy in (-2,-1,1,2) if abs(dx)+abs(dy)==3}
def L(x,ds):
 if x==0:return 1
 if x in (1,2):return sum(x+d in (0,3) for d in ds)-1
 if x==3:return 1-sum(x+d in (1,2) for d in ds)
 return 0
alpha={(0,0):-1,(0,3):-1,(1,1):1,(1,3):-1,(2,3):-1,(3,0):-1,(3,1):-1,(3,2):-1,(3,3):-1}
beta={((0,1),(1,3)):-1,((0,2),(2,3)):-1,((0,3),(1,1)):1,((1,0),(3,1)):-1,((1,1),(3,0)):-1,((1,2),(3,3)):-1,((2,0),(3,2)):-1,((2,1),(3,3)):-1,((2,2),(3,0)):-1}
def cross(a,b):return a[0]*b[1]-a[1]*b[0]
for name in sys.argv[1:]:
 f=Path(name);j=json.loads(f.read_text());K=j['K'];D={tuple(p):(tuple(a),tuple(b)) for p,a,b in j['chosen']};C={(x,y) for x in range(K) for y in range(K)}
 assert set(D)==C and len(D)==len(j['chosen'])
 adj={p:[] for p in C};ports=[];rvals={};costs=collections.Counter();directions=collections.Counter()
 for p,ds in D.items():
  assert len(set(ds))==2 and all(d in M for d in ds)
  t=int(tuple(map(sum,zip(*ds)))!=(0,0));r=t-L(p[0],[d[0] for d in ds])-L(p[1],[d[1] for d in ds]);rvals[p]=r
  if min(p)>=4:
   costs['interior_turns']+=t;directions[str(min(ds))]+=1
  elif max(p)>=4:costs['side_slack']+=r
  else:
   costs['corner_residual']+=r
   cert=alpha.get(p,0)
   for d in ds:
    q=p[0]+d[0],p[1]+d[1];e=tuple(sorted((p,q)));cert+=beta.get(e,0)*(1 if p<q else -1)
   assert r>=cert
  for d in ds:
   q=p[0]+d[0],p[1]+d[1];assert min(q)>=0
   if q in C:
    assert (-d[0],-d[1]) in D[q];adj[p].append(q)
   else:ports.append((p,d,q))
 assert sum(rvals.values())==j['residual']
 seen=set();comps=[]
 for p in sorted(C):
  if p in seen:continue
  cc=set();stack=[p]
  while stack:
   v=stack.pop()
   if v in cc:continue
   cc.add(v);stack.extend(adj[v])
  seen|=cc;assert any(len(adj[v])<2 for v in cc)
  assert sum(2-len(adj[v]) for v in cc)==2
  comps.append(len(cc))
 ghosts=collections.defaultdict(list)
 for p,d,q in ports:ghosts[q].append(p)
 forced_bad=[dict(cell=q,from_cells=ps) for q,ps in ghosts.items() if len(ps)>2 or (min(q)>=4 and len(ps)==2 and (ps[0][0]+ps[1][0],ps[0][1]+ps[1][1])!=(2*q[0],2*q[1]))]
 rays=[(p,d,q) for p,d,q in ports if min(q)>=4];conflicts=[]
 for i,(p,d,q) in enumerate(rays):
  for p2,d2,q2 in rays[i+1:]:
   den=cross(d,d2)
   if not den:continue
   diff=p2[0]-p[0],p2[1]-p[1]
   a=Fraction(cross(diff,d2),den);b=Fraction(cross(diff,d),den)
   if a.denominator!=1 or b.denominator!=1 or min(a,b)<1:continue
   v=p[0]+int(a)*d[0],p[1]+int(a)*d[1]
   if min(v)<4:continue
   assert v not in C
   conflicts.append(dict(cell=v,first_port=[p,d,q],second_port=[p2,d2,q2],steps=[int(a),int(b)],required_window=max(v)+1))
 conflicts.sort(key=lambda c:(c['required_window'],c['cell']))
 mod3=collections.defaultdict(collections.Counter)
 for (x,y),ds in D.items():
  if min(x,y)>=4:mod3[(x+y)%3][str(min(ds))]+=1
 bulk_mismatch=None
 if all(len(v)==1 for v in mod3.values()) and len(mod3)==3:
  representative={r:next(ds for p,ds in D.items() if min(p)>=4 and sum(p)%3==r) for r in mod3}
  bulk_mismatch=[]
  for p,ds in D.items():
   for d in M:
    q=p[0]+d[0],p[1]+d[1]
    if q not in D and min(q)>=4 and ((d in ds)!=((-d[0],-d[1]) in representative[sum(q)%3])):
     bulk_mismatch.append([p,d,q])
 report=dict(period3_bulk_interface_mismatches=bulk_mismatch,mod3_interior={k:dict(v) for k,v in mod3.items()},K=K,residual=sum(rvals.values()),costs=dict(costs),components=len(comps),path_length_hist=dict(collections.Counter(comps)),ports=len(ports),port_sides=dict(collections.Counter('both' if q[0]>=K and q[1]>=K else 'right' if q[0]>=K else 'top' for p,d,q in ports)),ghost_load_hist=dict(collections.Counter(map(len,ghosts.values()))),immediate_bad_ghosts=forced_bad,interior_pair_counts=dict(directions),forced_ray_conflicts=len(conflicts),first_conflicts=conflicts[:12],all_ports=ports)
 f.with_name(f.stem+'_check.json').write_text(json.dumps(report,indent=2))
 print(json.dumps({k:v for k,v in report.items() if k not in ('all_ports','first_conflicts')}),flush=True)
 if conflicts:print('FIRST_CONFLICT',json.dumps(conflicts[0]),flush=True)
