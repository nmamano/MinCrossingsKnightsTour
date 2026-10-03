"""Check route-(i) subtraction on every saved deep two-edge switch."""
from claim49_census6 import *
r=json.loads(Path('gap/verifier/claim49_switch_search.json').read_text());f=r['file']
grid=json.loads(Path(f).read_text())['tour'];n=len(grid);info,cs,_=geometry(grid)
es={edge((x,n-1-y),(x+MOVES[int(v)][1],n-1-y-MOVES[int(v)][0])) for y,row in enumerate(grid) for x,code in enumerate(row) for v in code}
own=defaultdict(set)
for e in es:
 for q in qs(e):own[q].add(e)
_,rows,_=CL.ledger(f);regs=[CL.last_regions[z['side'],z['lo'],z['hi']] for z in rows]
dep=lambda q:min(q[0],q[1],n-2-q[0],n-2-q[1])
which={};avail=[]
for i,(fx,fy,rr) in enumerate(cs):
 pp=[(n-2-x if fx else x,n-2-y if fy else y) for x,y in [(rr,j) for j in range(1,rr+1)]+[(x,rr) for x in range(rr-1,0,-1)]]
 aa=set()
 for x,y in pp:
  for k in range(4):
   q=(x,y,k)
   if dep(q)<5:continue
   which[q]=i
   if len(own[q])!=1:aa.add(q)
 avail.append(aa)
pick=lambda aa:sorted(aa,key=lambda q:(-dep(q),q))[:2]
original=[pick(aa) for aa in avail];hist=Counter();best=None
for z in r['positive_U_switches']:
 rem={edge(tuple(a),tuple(b)) for a,b in z['remove']};add={edge(tuple(a),tuple(b)) for a,b in z['add']};keys={q for e in rem|add for q in qs(e)}
 affected={which[q] for q in keys if q in which};mod={i:set(avail[i]) for i in affected}
 for q in keys:
  if q not in which:continue
  aa=mod[which[q]];aa.discard(q)
  if len((own[q]-rem)|{e for e in add if q in qs(e)})!=1:aa.add(q)
 reg=regs[z['region']]
 ds=sum(sum(q[:2] in reg for q in pick(mod[i]))-sum(q[:2] in reg for q in original[i]) for i in affected)
 resid=z['delta_BQ']-ds;score=2*z['delta_Uin']-resid
 hist[z['delta_Uin'],z['delta_BQ'],ds,resid,score]+=1
 if best is None or score>best['score']:best=dict(z,delta_selected_region=ds,delta_BQx=resid,score=score)
# Save an actual one-switch closed tour for a complete census.
b=best;adj=defaultdict(set)
for a,c in es:adj[a].add(c);adj[c].add(a)
for a,c in b['remove']:a,c=tuple(a),tuple(c);adj[a].remove(c);adj[c].remove(a)
for a,c in b['add']:a,c=tuple(a),tuple(c);adj[a].add(c);adj[c].add(a)
og=[['' for _ in range(n)] for _ in range(n)]
for (x,y),nb in adj.items():og[n-1-y][x]=''.join(str(MOVES.index((y-v,u-x))) for u,v in sorted(nb))
X,_=check(og);Path('gap/verifier/claim49_deep_switch_n144.json').write_text(json.dumps(dict(tour=og,source=f,switch=best,X=X)))
out=dict(tested=len(r['positive_U_switches']),histogram=[dict(delta_Uin=k[0],delta_BQ=k[1],delta_selected=k[2],delta_BQx=k[3],score=k[4],count=v) for k,v in hist.items()],best=best,switched_X=X)
Path('gap/verifier/claim49_switch_marks.json').write_text(json.dumps(out,indent=2));print(json.dumps(out))
