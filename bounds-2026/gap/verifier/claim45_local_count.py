"""Independent, solver-free local C5 change in the pure U collar."""
import json
from pathlib import Path
from collections import defaultdict
from claim26_certificate import edge,TERMS,EXC
from claim37_check import tile
w=json.loads(Path('gap/verifier/claim45_U_gadget.json').read_text())
rem={edge(tuple(a),tuple(b)) for a,b in w['remove']};add={edge(tuple(a),tuple(b)) for a,b in w['add']}
def nn(p):
 x,y=p
 return {(2,y+1),(1,y-2)} if x==0 else {(3,y+1),(0,y+2)} if x==1 else {(x+2,y+1),(x-2,y-1)}
base={edge((x,y),q) for x in range(14) for y in range(-50,67) for q in nn((x,y))}
vp=json.loads(Path('gap/verifier/claim42_geometry.json').read_text())['VIS_pairs']
def counts(es):
 adj=defaultdict(set)
 for a,b in es:adj[a].add(b);adj[b].add(a)
 g=set()
 for r in range(-20,36):
  tr=lambda a:(a[0],a[1]+r)
  F=sum(c for a,b,c in TERMS if edge(tr(a),tr(b)) in es)
  exc=all(edge(tr(a),tr(b)) in es for a,b in EXC)
  vis=any(all(edge(tr(a),tr(b)) in es for a,b in z[:2]) for z in vp)
  if F%3!=2 or exc or vis:g.add(r)
 ports={}
 for a,b in es:
  if (a[0]<3)==(b[0]<3):continue
  o,q=(a,b) if a[0]<3 else (b,a)
  if not -30<=o[1]<=45:continue
  dx,dy=q[0]-o[0],q[1]-o[1];sg=1 if dx*dy>0 else -1
  ports[o,q]=(dx,sg,q[0]-2*sg*q[1])
 changed=[]
 for (o,q),p in ports.items():
  prev,cur=q,o;seen=set()
  while cur[0]<3:
   assert cur not in seen;seen.add(cur)
   prev,cur=cur,next(z for z in adj[cur] if z!=prev)
  pp=ports.get((prev,cur))
  good=pp is not None and p[:2]==pp[:2] and p[0]==2 and pp[2]==p[2]+(-3 if p[2]%2==0 else 3)
  if not good and -10<=o[1]<=26:changed.append((o,q))
 free=[p for p in changed if all(abs(p[0][1]-r)>2 for r in g)]
 return {'g':sorted(g),'changed':len(changed),'N_free':len(free),'changed_rows':[p[0][1] for p in changed],'free_rows':[p[0][1] for p in free]}
a=counts(base);b=counts(base-rem|add)
assert a['g']==[] and b['g']==[0,5,9,14]
assert b['N_free']-a['N_free']==-38
assert all(x<5 for e in rem|add for (x,y),h in tile(e))
out={'before':a,'after':b,'delta_g':4,'delta_N_free':-38,'delta_BQdeep':0,'delta_2g_2Nfree':-68,'required_spacing':24}
Path('gap/verifier/claim45_local_count.json').write_text(json.dumps(out,indent=1));print(out)
