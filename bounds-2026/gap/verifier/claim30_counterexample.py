"""A completed-tour counterexample to one H/V word per connected good domain."""
import json,sys,hashlib
from collections import defaultdict,deque
from pathlib import Path
sys.path.insert(0,'w-verifier')
from check import check as validate,MOVES
from claim29_window import tile,edge
f=Path('w-integrator/tours/FOLD24_n96.json');data=json.loads(f.read_text());tour=data['tour'];n=len(tour)
X,turns=validate(tour);assert X==data['crossings']
es=set()
for row,line in enumerate(tour):
 for col,code in enumerate(line):
  for v in code:
   dy,dx=MOVES[int(v)];es.add(edge((col,n-1-row),(col+dx,n-1-row-dy)))
own=defaultdict(list)
for e in es:
 for q in tile(e):own[q].append(e)
good={}
for x in range(n-1):
 for y in range(n-1):
  if all(len(own[x,y,k])==1 for k in range(4)):
   good[x,y]=own[x,y,0][0]==own[x,y,1][0]
source=(2,2);target=(5,6);parent={source:None};todo=deque([source])
while todo:
 a=todo.popleft()
 if a==target:break
 for b in ((a[0]+1,a[1]),(a[0]-1,a[1]),(a[0],a[1]+1),(a[0],a[1]-1)):
  if b not in parent and good.get(b)==True:parent[b]=a;todo.append(b)
assert target in parent
path=[];a=target
while a is not None:path.append(a);a=parent[a]
path.reverse()
assert own[2,2,2]==[edge((1,2),(3,3))]
assert own[5,6,0]==[edge((5,5),(6,7))]
# TL(2,2) and BR(5,6) belong to the same ribbon k=1.
# The intervening ribbon vertices are not an uninterrupted good run.
ribbon=[(2,2,2),(2,3,0),(3,3,2),(3,4,0),(4,4,2),(4,5,0),(5,5,2),(5,6,0)]
records=[dict(half=q,quarter_multiplicities=[len(own[q[0],q[1],k]) for k in range(4)],good_slash=good.get(q[:2])==True) for q in ribbon]
assert any(not r['good_slash'] for r in records)
out=dict(date='2026-10-03',file=str(f),sha256=hashlib.sha256(f.read_bytes()).hexdigest(),tour_valid=True,n=n,X=X,first_half='TL(2,2)',first_tile=[[1,2],[3,3]],first_bit='H',second_half='BR(5,6)',second_tile=[[5,5],[6,7]],second_bit='V',ribbon=1,good_slash_square_path=path,ribbon_run=records)
Path('gap/verifier/claim30_counterexample.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
