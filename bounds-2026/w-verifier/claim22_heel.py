"""Read PDF vector paths and compare them with periodic templates. No worker imports."""
from pathlib import Path
from pypdf import PdfReader
from pypdf.generic import ContentStream
from collections import defaultdict
import ast,json
from check import MOVES
from periodic import count
from strand_audit import pairing
root=Path.cwd();tree=ast.parse(Path('kt/templates.py').read_text());templates={}
for st in tree.body:
 if isinstance(st,ast.Assign) and isinstance(st.targets[0],ast.Name) and st.targets[0].id in ('Sequence1Default','Sequence1Opt','SequenceP40','VerticalEdge'):
  templates[st.targets[0].id]=ast.literal_eval(st.value)
templates['heel21']=json.loads(Path('w-integrator/gadgets/heel21.json').read_text())['template']
res={}
for name,tpl in templates.items():
 tpl=[s.replace('xx','26') for s in tpl];cells=[s.split() for s in tpl];T=sum(abs(int(s[0])-int(s[1]))!=4 for row in cells for s in row)
 res[name]={'X':count(tpl,'left' if name=='VerticalEdge' else 'bottom'),'T':T}
 if name!='VerticalEdge' and name!='SequenceP40':res[name]['pairing']=pairing(tpl,'B')
 print(name,res[name],flush=True)
r=PdfReader('paper.pdf');form=r.pages[19]['/Resources']['/XObject']['/Im11'].get_object();ops=ContentStream(form,r).operations
paths=[];path=[];color=(0,0,0);width=1;stack=[]
for vals,op in ops:
 vals=list(vals)
 if op==b'q':stack.append((color,width))
 elif op==b'Q':color,width=stack.pop()
 elif op==b'RG':color=tuple(map(float,vals))
 elif op==b'w':width=float(vals[0])
 elif op==b'm':path=[tuple(map(float,vals))]
 elif op==b'l':path.append(tuple(map(float,vals)))
 elif op in (b'S',b's'):
  if width==1.2 and color!=(0,0,0):paths.append((color,path[:]))
  path=[]
 elif op in (b'f',b'f*',b'n',b'B',b'B*'):path=[]
# Each panel is translated by 144 PDF units. Grid pitch is 16.
results={}
for name,x0 in [('Sequence1Default',928),('heel21',1072),('Sequence1Opt',1216)]:
 edges=set()
 for col,pts in paths:
  if not pts or not all(x0-40<=x<=x0+120 for x,y in pts):continue
  for (x,y),(u,v) in zip(pts,pts[1:]):
   a=((x-x0)/16,(y-2856)/16);b=((u-x0)/16,(v-2856)/16)
   dx,dy=b[0]-a[0],b[1]-a[1];length=min(abs(dx),abs(dy))
   if not length or abs(max(abs(dx),abs(dy))-2*length)>1e-5 or abs(length-round(length))>1e-5:continue
   for k in range(round(length)):
    p=(round(a[0]+k*dx/length),round(a[1]+k*dy/length));q=(round(a[0]+(k+1)*dx/length),round(a[1]+(k+1)*dy/length));edges.add(tuple(sorted((p,q))))
 tpl=[s.replace('xx','26').split() for s in templates[name]];scores=[]
 for offset in range(8):
  bad=[];total=0
  for e in edges:
   for p,q in (e,e[::-1]):
    x,y=p
    if not 0<=y<4:continue
    s=tpl[3-y][(x+offset)%8];allowed={(x+MOVES[int(k)][1],y-MOVES[int(k)][0]) for k in s};total+=1
    if q not in allowed:bad.append((p,q,s))
  scores.append((len(bad),offset,total,bad))
 best=min(scores);results[name]={'edges':len(edges),'best_mismatches':best[0],'phase':best[1],'directed_tests':best[2],'examples':best[3][:8]}
 print('PDF',name,results[name],flush=True)
res['pdf']=results;Path('w-verifier/claim22_heel.json').write_text(json.dumps(res,indent=2))
# Recover the printed centre panel in board.js row order, retaining straight unused cells.
x0=1072; nb=defaultdict(set)
for col,pts in paths:
 if not pts or not all(x0-40<=x<=x0+120 for x,y in pts):continue
 for (x,y),(u,v) in zip(pts,pts[1:]):
  a=((x-x0)/16,(y-2856)/16);b=((u-x0)/16,(v-2856)/16);dx,dy=b[0]-a[0],b[1]-a[1];length=min(abs(dx),abs(dy))
  if not length or abs(max(abs(dx),abs(dy))-2*length)>1e-5 or abs(length-round(length))>1e-5:continue
  for k in range(round(length)):
   p=(round(a[0]+k*dx/length),round(a[1]+k*dy/length));q=(round(a[0]+(k+1)*dx/length),round(a[1]+(k+1)*dy/length));nb[p].add(q);nb[q].add(p)
printed=[];loads=[]
for y in range(3,-1,-1):
 row=[]
 for x in range(8):
  ns=nb[x,y];loads.append(len(ns))
  if len(ns)==2:row.append(''.join(sorted(str(MOVES.index((y-v,u-x))) for u,v in ns)))
  elif not ns:row.append('26')
  else:row.append('??')
 printed.append(' '.join(row))
print('PRINTED CENTER',printed,'degrees',dict(__import__('collections').Counter(loads)))
if '??' not in ' '.join(printed):
 print('PRINTED CENTER COUNTS',count(printed,'bottom'),sum(abs(int(s[0])-int(s[1]))!=4 for row in printed for s in row.split()))
 res['printed_centre_template']=printed
 Path('w-verifier/claim22_heel.json').write_text(json.dumps(res,indent=2))
