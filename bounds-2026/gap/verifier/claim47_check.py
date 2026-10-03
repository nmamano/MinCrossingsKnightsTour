"""Solver-free Claim 47 pairing and per-distance port count, 2026-10-03."""
import sys,json,hashlib
from pathlib import Path
from collections import defaultdict,Counter
from fractions import Fraction
from claim26_certificate import edge,TERMS,EXC
from claim37_check import tile
vp=json.loads(Path('gap/verifier/claim42_geometry.json').read_text())['VIS_pairs']
def nn(p):
 x,y=p
 return {(2,y+1),(1,y-2)} if x==0 else {(3,y+1),(0,y+2)} if x==1 else {(x+2,y+1),(x-2,y-1)}
def graph(es):
 a=defaultdict(set)
 for p,q in es:a[p].add(q);a[q].add(p)
 return a

def run(file):
 w=json.loads(Path(file).read_text());W,H=w['W'],w['H']
 rem={edge(tuple(a),tuple(b)) for a,b in w['remove']};add={edge(tuple(a),tuple(b)) for a,b in w['add']}
 base={edge((x,y),q) for x in range(W+10) for y in range(-50,H+51) for q in nn((x,y))}
 assert rem<=base and not add&base
 new=base-rem|add;V={(x,y) for x in range(W) for y in range(H)}
 for e in rem|add:
  assert all(v in V for v in e)
  assert sorted((abs(e[0][0]-e[1][0]),abs(e[0][1]-e[1][1])))==[1,2]
 def pairs(es):
  adj=graph(es);assert all(len(adj[v])==2 for v in V)
  seen=set();res=[]
  for p in sorted(V):
   if p in seen:continue
   co={p};todo=[p];seen.add(p)
   while todo:
    for z in adj[todo.pop()]:
     if z in V and z not in seen:seen.add(z);co.add(z);todo.append(z)
   ports=[edge(v,z) for v in co for z in adj[v] if z not in V]
   assert len(ports)==2
   res.append(tuple(sorted(ports)))
  return sorted(res)
 assert pairs(base)==pairs(new)
 def counts(es):
  adj=graph(es);g=set()
  for r in range(-15,H+16):
   tr=lambda a:(a[0],a[1]+r)
   F=sum(c for a,b,c in TERMS if edge(tr(a),tr(b)) in es)
   if F%3!=2 or all(edge(tr(a),tr(b)) in es for a,b in EXC) or any(all(edge(tr(a),tr(b)) in es for a,b in z[:2]) for z in vp):g.add(r)
  ports={}
  for a,b in es:
   if (a[0]<3)==(b[0]<3):continue
   o,q=(a,b) if a[0]<3 else (b,a)
   dx,dy=q[0]-o[0],q[1]-o[1];sg=1 if dx*dy>0 else -1
   ports[o,q]=(dx,sg,q[0]-2*sg*q[1])
  changed=[];allrows=[]
  for (o,q),p in ports.items():
   if not -10<=o[1]<=H+10:continue
   allrows.append(o[1]);prev,cur=q,o;seen=set()
   while cur[0]<3:
    assert cur not in seen;seen.add(cur)
    prev,cur=cur,next(z for z in adj[cur] if z!=prev)
   pp=ports[prev,cur]
   good=p[:2]==pp[:2] and p[0]==2 and pp[2]==p[2]+(-3 if p[2]%2==0 else 3)
   if not good:changed.append(o[1])
  d=Counter(min(3,min((abs(r-z) for z in g),default=100000)) for r in changed)
  return {'g':sorted(g),'changed_rows':sorted(changed),'all_port_rows':sorted(allrows),'P0':d[0],'P1':d[1],'P2':d[2],'P3':d[3]}
 b,a=counts(base),counts(new)
 deep={q for e in rem|add for (x,y),h in tile(e) for q in [(x,y,k) for k in h] if x>=5}
 delta={k:(len(a[k])-len(b[k]) if k=='g' else a[k]-b[k]) for k in ['g','P0','P1','P2','P3']}
 score=lambda c:2*2*delta['g']+2*c*delta['P1']+2*(delta['P2']+delta['P3'])
 out={'file':file,'sha256':hashlib.sha256(Path(file).read_bytes()).hexdigest(),'W':W,'H':H,'unchanged_pairing':True,'pairs':len(pairs(base)),'no_cycles':True,'deep_touched':len(deep),'before':b,'after':a,'delta':delta,'delta_C5_half':str(score(Fraction(1,2))),'delta_C5_twothirds':str(score(Fraction(2,3)))}
 print(json.dumps(out),flush=True);return out
if __name__=='__main__':
 out=[run(f) for f in sys.argv[1:]]
 Path('gap/verifier/claim47_checks.json').write_text(json.dumps(out,indent=2))
