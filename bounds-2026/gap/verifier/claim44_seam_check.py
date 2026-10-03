"""Replay saved gentle seams; count bad quarters independently by exact tiles."""
import sys,json
from pathlib import Path
from collections import Counter
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'w-structures'))
from seam import Seam
from run_seam import KIND
from unroll import unroll,check
from claim26_certificate import edge
from claim37_check import tile
k=KIND['gentle'];st=Seam(T=(3,3),hv=k['hv'],w1=3,w2=3,f1=k['f1'],form1=k['form1'],f2=k['f2'],form2=k['form2'],s=1)
out=[]
for r in json.loads(Path('gap/verifier/claim44_seam.json').read_text()):
 if r['target'] not in (-1,0):continue
 z=check(st,r['chosen']);assert not z['bad'];assert z['X_per_period']==3
 adj,band=unroll(st,r['chosen'],K=12,margin=12)
 es={edge(p,q) for p,nn in adj.items() for q in nn}
 cov=Counter((x,y,q) for e in es for (x,y),h in tile(e) for q in h)
 bq=[(x,y,q,cov[x,y,q]) for x in range(12,15) for y in range(x-8,x+9) for q in 'BRTL' if cov[x,y,q]!=1]
 assert all(abs(y-x)<=5 for x,y,q,m in bq)
 rr={'current':r['current'],'X_per_period':z['X_per_period'],'bad_quarters_per_period':len(bq),'multiplicities':dict(Counter(q[3] for q in bq))};out.append(rr);print(rr)
Path('gap/verifier/claim44_seam_check.json').write_text(json.dumps(out,indent=1))
