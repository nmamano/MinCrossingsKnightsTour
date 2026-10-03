"""Independent section-8 census using fixed P rule, not learned window rules."""
import json,sys
from pathlib import Path
from collections import Counter,defaultdict
from claim36_scan import run as scan
from claim38_switch import edge,qs
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'w-verifier'))
from check import MOVES

def run(file):
 r=scan(file);grid=json.loads(Path(file).read_text())['tour'];n=len(grid)
 es={edge((x,n-1-y),(x+MOVES[int(v)][1],n-1-y-MOVES[int(v)][0])) for y,row in enumerate(grid) for x,code in enumerate(row) for v in code}
 adj=defaultdict(set);cov=Counter()
 for a,b in es:adj[a].add(b);adj[b].add(a);cov.update(qs((a,b)))
 inside=lambda p:all(3<=z<=n-4 for z in p)
 gp=lambda p:all(cov[p[0]+dx,p[1]+dy,k]==1 for dx in (-1,0) for dy in (-1,0) for k in range(4))
 ts=[lambda p:p,lambda p:(n-1-p[0],p[1]),lambda p:(p[1],p[0]),lambda p:(n-1-p[1],p[0])]
 ports={}
 for a,b in es:
  if inside(a)==inside(b):continue
  o,q=(b,a) if inside(a) else (a,b);sides=[i for i,T in enumerate(ts) if T(o)[0]<3]
  if len(sides)!=1:ports[o,q]=None;continue
  si=sides[0];u,v=ts[si](o),ts[si](q);sg=1 if (v[0]-u[0])*(v[1]-u[1])>0 else -1
  ports[o,q]=(si,v[0]-u[0],sg,v[0]-sg*2*v[1])
 partner={}
 for o,q in ports:
  prev,cur=q,o;seen=set()
  while not inside(cur):
   assert cur not in seen;seen.add(cur)
   prev,cur=cur,next(v for v in adj[cur] if v!=prev)
  partner[o,q]=(prev,cur)
 changed=set()
 for p,z in ports.items():
  zz=ports[partner[p]]
  if z is None or zz is None or z[:3]!=zz[:3] or z[1]!=2 or zz[3]!=z[3]+(-3 if z[3]%2==0 else 3):changed.add(p)
 seen=set();cleanports=set();rets=Counter();exceptions=[]
 for p,z in ports.items():
  if p in seen:continue
  o,q=p;path=[o,q];prev,cur=o,q
  while inside(cur):prev,cur=cur,next(v for v in adj[cur] if v!=prev);path.append(cur)
  p2=(cur,prev);seen.update((p,p2));zz=ports[p2]
  if z is None or zz is None or z[0]!=zz[0] or not all(gp(v) for v in path[1:-1]):continue
  count=(p in changed)+(p2 in changed);rets[count]+=1;cleanports.update((p,p2))
  if not count:exceptions.append(path)
 nr=len(changed);nrp=len(changed-cleanports);ret=sum(rets.values())
 return dict(file=file,n=n,E=r['E'],BQ=r['BQ'],RET_clean=ret,changed_ends=dict(rets),N_re=nr,N_re_prime=nrp,B_left=r['BQ']+2*ret+2*nrp,B_surplus=r['BQ']+2*ret+2*nrp-4*n,D_surplus=r['E']-r['BQ']/4-nr/2,zero_changed_returns=exceptions)
if __name__=='__main__':
 out=[]
 for p in sys.argv[1:]:
  r=run(p);out.append(r);print({k:v for k,v in r.items() if k!='zero_changed_returns'},flush=True)
 Path('gap/verifier/claim38_v3_census.json').write_text(json.dumps(out,indent=2))
