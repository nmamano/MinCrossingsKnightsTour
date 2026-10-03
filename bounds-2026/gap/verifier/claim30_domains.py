"""Look for incompatible ribbon bits in a connected good domain of a saved tour."""
from pathlib import Path
import json,sys
from collections import defaultdict
sys.path.insert(0,'w-verifier')
from check import MOVES
from claim29_window import tile,edge
results=[]
for file in ['w-integrator/tours/FOLD24_n96.json','w-integrator/tours/FOLD24_n98.json','gap/lowerbounds/conn/FIELD_n166_92_155.json']:
 d=json.loads(Path(file).read_text());tour=d['tour'];n=len(tour);es=set()
 for y,row in enumerate(tour):
  for x,code in enumerate(row):
   for v in code:
    dy,dx=MOVES[int(v)];es.add(edge((x,n-1-y),(x+dx,n-1-y-dy)))
 own=defaultdict(list)
 for e in es:
  for q in tile(e):own[q].append(e)
 good={}
 for x in range(n-1):
  for y in range(n-1):
   if all(len(own[x,y,k])==1 for k in range(4)):
    slash=own[x,y,0][0]==own[x,y,1][0]
    good[x,y]=slash
 visited=set();found=[];components=0
 for start in good:
  if start in visited:continue
  todo=[start];cc=[];sg=good[start];visited.add(start)
  while todo:
   a=todo.pop();cc.append(a)
   for b in ((a[0]+1,a[1]),(a[0]-1,a[1]),(a[0],a[1]+1),(a[0],a[1]-1)):
    if b in good and good[b]==sg and b not in visited:visited.add(b);todo.append(b)
  components+=1;bits={}
  for x,y in cc:
   k=y-x if sg else x+y+1
   for half,delta in ((0,0),(2,1)):
    e=own[x,y,half][0];H=abs(e[1][0]-e[0][0])==2;key=(k+delta,H)
    bits[key]=(x,y,half,e)
    if (k+delta,not H) in bits:
     found.append({'split':'/' if sg else '\\','ribbon':k+delta,'component_size':len(cc),'first':bits[k+delta,not H],'second':bits[key]})
     break
   if found:break
  if found:break
 results.append(dict(file=file,good_squares=len(good),components_examined=components,incompatible_domain=found))
 print(json.dumps(results[-1]),flush=True)
Path('gap/verifier/claim30_domains.json').write_text(json.dumps(results,indent=2))
