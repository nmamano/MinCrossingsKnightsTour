"""L5 diagnostic: author's chamber regions, independently counted residual quarters.
Uses audited retained-candidate geometry and the stated deepest-first tie rule.
"""
import sys,json,time
from pathlib import Path
from collections import Counter,defaultdict
from itertools import combinations
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'gap/structures'));sys.path.insert(0,str(ROOT/'gap/turnstheory'))
import claim49_ledger6 as CL
from check_hall_v3 import geometry
from claim38_switch import qs,edge
from check import check,MOVES,proper

def run(file):
 start=time.monotonic();grid=json.loads(Path(file).read_text())['tour'];n=len(grid);X,_=check(grid)
 n,rows,glob=CL.ledger(file)
 es={edge((x,n-1-y),(x+MOVES[int(v)][1],n-1-y-MOVES[int(v)][0])) for y,row in enumerate(grid) for x,code in enumerate(row) for v in code}
 own=defaultdict(list)
 for e in es:
  for q in qs(e):own[q].append(e)
 dep=lambda x,y:min(x,y,n-2-x,n-2-y)
 info,cs,atoms=geometry(grid);assert info['X']==X
 bad={q for x in range(5,n-6) for y in range(5,n-6) for k in range(4) for q in [(x,y,k)] if len(own[q])!=1}
 sel=set();possible=set();full=0
 for fx,fy,r in cs:
  pp=[(n-2-x if fx else x,n-2-y if fy else y) for x,y in [(r,j) for j in range(1,r+1)]+[(i,r) for i in range(r-1,0,-1)]]
  avail=sorted([q for x,y in pp for k in range(4) for q in [(x,y,k)] if q in bad],key=lambda q:(-dep(*q[:2]),q))
  possible.update(avail);chosen=set(avail[:2]);assert not sel&chosen;sel|=chosen;full+=int(len(chosen)==2)
 rr=[]
 for r in rows:
  reg=CL.last_regions[r['side'],r['lo'],r['hi']]
  bb={q for q in bad if q[:2] in reg};ss=sel&bb
  rr.append(dict(side=r['side'],lo=r['lo'],hi=r['hi'],Uin=r['Uin'],raw_deep=len(bb),selected=len(ss),BQx=len(bb-ss),possible_selected_overlap=len(possible&bb),deficit=2*r['Uin']-len(bb-ss)))
 # Own joint J census from exact tile intersections and full halo multiplicities.
 sides=[]
 for T in [lambda v:v,lambda v:(n-1-v[0],v[1]),lambda v:(v[1],v[0]),lambda v:(n-1-v[1],v[0])]:
  loc={edge(T(a),T(b)) for a,b in es};tq={e:set(qs(e)) for e in loc if min(e[0][0],e[1][0])<=4};byq=defaultdict(list)
  for e,qq in tq.items():
   for q in qq:byq[q].append(e)
  pair=set();x1=set();Q=0
  for x in range(5):
   for y in range(8,n-8):
    for k in range(4):
     q=(x,y,k);m=len(byq[q]);Q+=1 if m==0 else (m-1)*(m-2)//2
     for a,b in combinations(byq[q],2):
      ab=tuple(sorted((a,b)))
      if len(tq[a]&tq[b])==1:x1.add(ab)
  Q+=len(x1)
  # All overlaps among S3 edges; ownership uses the later lower endpoint.
  for ls in byq.values():
   for a,b in combinations(ls,2):
    if min(a[0][0],a[1][0])>2 or min(b[0][0],b[1][0])>2:continue
    lo=lambda e:min(e,key=lambda v:(v[1],v[0]))
    later=max((lo(a),lo(b)),key=lambda v:(v[1],v[0]))
    if 8<=later[1]<n-8:pair.add(tuple(sorted((a,b))))
  sides.append(dict(X3_minus_rows=len(pair)-(n-16),Q3=Q,twoJ=2*(len(pair)-(n-16))+Q))
 K=2*n-60-full;BQx=len(bad-sel);twoJ=sum(s['twoJ'] for s in sides)
 out=dict(file=file,n=n,X=X,retained=len(cs),K=K,BQdeep=len(bad),selected=len(sel),BQx=BQx,twoJ=twoJ,C5J=twoJ+BQx-2*K,C5J_minus_4n=twoJ+BQx-2*K-4*n,sides=sides,chambers=rr,total_Uin=sum(r['Uin'] for r in rr),total_region_BQx=sum(r['BQx'] for r in rr),total_region_selected=sum(r['selected'] for r in rr),seconds=time.monotonic()-start)
 return out
if __name__=='__main__':
 for file in sys.argv[1:]:
  out=run(file);p=Path('gap/verifier/claim49_w6_'+Path(file).stem+'_census.json');p.write_text(json.dumps(out,indent=2));print(json.dumps(out),flush=True)
