"""Enumerate single-cycle two-edge switches inside fixed depth-6 chambers.
Only changed tiles wholly inside one region are admitted, preserving its barrier.
"""
from claim49_census6 import *
from claim38_switch import knight
f='gap/verifier/claim36_FOLD_n144.json'
n,rows,_=CL.ledger(f);_,ports,changed,other,es,adj=CL.port_data(f)
inside=lambda v:all(6<=z<=n-7 for z in v)
region={};regions=[]
for r in rows:
 reg=CL.last_regions[r['side'],r['lo'],r['hi']];regions.append(reg)
 for q in reg:region[q]=len(regions)-1
# Orient the closed tour. Reconnecting a-c and b-d reverses a segment and retains one cycle.
seq=[(0,0)];prev=None;cur=(0,0)
while True:
 nxt=next(z for z in sorted(adj[cur]) if z!=prev)
 if nxt==(0,0):break
 seq.append(nxt);prev,cur=cur,nxt
assert len(seq)==n*n
nex=dict(zip(seq,seq[1:]+seq[:1]));own=defaultdict(set)
for e in es:
 for q in qs(e):own[q].add(e)
# Label each oriented interior edge with its two exterior ports in tour order.
ends={};seen=set()
for p in ports:
 o,q=p
 if nex[o]!=q:continue
 prev,cur=o,q;path=[]
 while inside(cur):
  z=nex[cur];path.append((cur,z));prev,cur=cur,z
 exitp=(cur,prev)
 for a,b in path:
  if inside(b):ends[a,b]=(p,exitp)
checks=0;improvements=[];best=None
for a,b in nex.items():
 if (a,b) not in ends:continue
 for dx,dy in ((1,2),(2,1),(-1,2),(-2,1),(1,-2),(2,-1),(-1,-2),(-2,-1)):
  c=(a[0]+dx,a[1]+dy)
  if c not in nex or a>=c:continue
  d=nex[c]
  if (c,d) not in ends or len({a,b,c,d})!=4 or not knight(b,d):continue
  rem=[edge(a,b),edge(c,d)];add=[edge(a,c),edge(b,d)]
  if any(e in es for e in add):continue
  A,B=ends[a,b];C,D=ends[c,d]
  if {A,B}=={C,D}:continue
  keys={q for e in rem+add for q in qs(e)};rs={region.get(q[:2]) for q in keys}
  if len(rs)!=1 or None in rs or any(min(q[0],q[1],n-2-q[0],n-2-q[1])<5 for q in keys):continue
  ri=next(iter(rs));reg=regions[ri];r=rows[ri]
  def inret(pair):
   return all(ports.get(k) is not None and ports[k]['side']==r['side'] and r['lo']<=ports[k]['row']<=r['hi']+1 for k in pair)
  # Both entire source chords must be inside the fixed region, as tested by the source's precise vertex convention.
  rb=reg # Allowing only vertices incident to region is stricter than region plus barrier.
  def source_inside(k):
   return all(any((v[0]+dx,v[1]+dy) in rb for dx in (-1,0) for dy in (-1,0)) for v in CL.chord_path(k,adj,inside))
  if not all(inret(pair) and source_inside(pair[0]) for pair in ((A,B),(C,D))):continue
  u=lambda pair:int(not any(k in changed for k in pair))
  du=u((A,C))+u((B,D))-u((A,B))-u((C,D))
  before=sum(len(own[q])!=1 for q in keys)
  after=sum(len((own[q]-set(rem))|{e for e in add if q in qs(e)})!=1 for q in keys)
  db=after-before;checks+=1
  z=dict(delta_Uin=du,delta_BQ=db,score=2*du-db,remove=rem,add=add,region=ri)
  if best is None or z['score']>best['score']:best=z
  if du>0:improvements.append(z)
out=dict(file=f,n=n,admissible_switches=checks,best=best,positive_U_switches=improvements)
Path('gap/verifier/claim49_switch_search.json').write_text(json.dumps(out,indent=2));print(json.dumps(out),flush=True)
