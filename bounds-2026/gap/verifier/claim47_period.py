"""Exact infinite periodic collar count, via bounded lifted traces."""
from claim47_check import *
w=json.loads(Path('gap/verifier/claim47_U_gadget_24.json').read_text());out=[]
for period in (24,28,32):
 es={edge((x,y),q) for x in range(16) for y in range(-8*period,9*period) for q in nn((x,y))}
 for j in range(-6,7):
  for e in w['remove']:es.remove(edge(*[(x,y+j*period) for x,y in e]))
  for e in w['add']:es.add(edge(*[(x,y+j*period) for x,y in e]))
 adj=graph(es);g=[]
 for r in range(-2*period,3*period):
  tr=lambda p:(p[0],p[1]+r)
  F=sum(c for a,b,c in TERMS if edge(tr(a),tr(b)) in es)
  if F%3!=2 or all(edge(tr(a),tr(b)) in es for a,b in EXC) or any(all(edge(tr(a),tr(b)) in es for a,b in z[:2]) for z in vp):g.append(r)
 assert [r for r in g if 0<=r<period]==[r-period for r in g if period<=r<2*period]
 def desc(o,q):
  dx,dy=q[0]-o[0],q[1]-o[1];sg=1 if dx*dy>0 else -1
  return dx,sg,q[0]-2*sg*q[1]
 P=Counter();traces=[]
 for a,b in sorted(es):
  if (a[0]<3)==(b[0]<3):continue
  o,q=(a,b) if a[0]<3 else (b,a)
  if not 0<=o[1]<period:continue
  prev,cur=q,o;seen=set();trace=[]
  while cur[0]<3:
   assert cur not in seen;seen.add(cur);trace.append(cur)
   assert len(adj[cur])==2
   prev,cur=cur,next(z for z in adj[cur] if z!=prev)
  p,pp=desc(o,q),desc(prev,cur)
  good=p[:2]==pp[:2] and p[0]==2 and pp[2]==p[2]+(-3 if p[2]%2==0 else 3)
  if not good:P[min(3,min(abs(o[1]-r) for r in g))]+=1
  traces.append({'port':[o,q],'exit':[prev,cur],'good':good,'trace':trace})
 ys=[v[1] for t in traces for v in t['trace']]
 assert min(ys)>-2*period and max(ys)<3*period
 ng=sum(0<=r<period for r in g)
 costs={str(c):str(4*ng+2*c*P[1]+2*(P[2]+P[3])) for c in (Fraction(1,2),Fraction(2,3))}
 out.append(dict(period=period,g=[r for r in g if 0<=r<period],P=dict(P),costs=costs,trace_y_range=[min(ys),max(ys)],traces=traces))
 print({k:v for k,v in out[-1].items() if k!='traces'})
Path('gap/verifier/claim47_period.json').write_text(json.dumps(out,indent=2))
