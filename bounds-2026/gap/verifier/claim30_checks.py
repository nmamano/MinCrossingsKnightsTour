"""Independent exact-cover checks of T1--T3, no worker imports or solver."""
from claim29_window import tile,edge,cross
from itertools import product
from collections import Counter
from pathlib import Path
import json,time
moves=[(1,2),(2,1),(2,-1),(1,-2)]

def covers(mode):
 if mode=='plane':
  squares=[(-1,-1),(0,-1),(-1,0),(0,0)];universe=[(x,y,k) for x,y in squares for k in range(4)]
  es=sorted({edge((x,y),(x+dx,y+dy)) for x in range(-4,5) for y in range(-4,5) for dx,dy in moves if any((a,b) in squares for a,b,k in tile(edge((x,y),(x+dx,y+dy))))})
  qs=[tile(e)&set(universe) for e in es]
 else:
  squares=list(product(range(6),repeat=2));universe=[(x,y,k) for x,y in squares for k in range(4)]
  es=[edge((x,y),(x+dx,y+dy)) for x,y in squares for dx,dy in moves]
  qs=[{(x%6,y%6,k) for x,y,k in tile(e)} for e in es]
 qid={q:i for i,q in enumerate(universe)};masks=[sum(1<<qid[q] for q in cover) for cover in qs]
 choices=[[] for q in universe]
 for i,cover in enumerate(qs):
  for q in cover:choices[qid[q]].append(i)
 vertices=[((a[0]%6,a[1]%6),(b[0]%6,b[1]%6)) if mode=='torus' else (a,b) for a,b in es]
 allmask=(1<<len(universe))-1;found=[];steps=0
 def visit(used,selected,deg):
  nonlocal steps
  steps+=1
  if used==allmask:
   if mode=='plane' and deg.get((0,0),0)!=2:return
   found.append(tuple(selected));return
  best=None;rem=allmask^used
  while rem:
   q=(rem&-rem).bit_length()-1;rem&=rem-1
   options=[]
   for i in choices[q]:
    if masks[i]&used:continue
    a,b=vertices[i]
    if mode=='torus':
     if deg.get(a,0)==2 or deg.get(b,0)==2:continue
    elif (a==(0,0) or b==(0,0)) and deg.get((0,0),0)==2:continue
    options.append(i)
   if not options:return
   if best is None or len(options)<len(best):best=options
   if len(best)==1:break
  for i in best:
   a,b=vertices[i];deg[a]=deg.get(a,0)+1;deg[b]=deg.get(b,0)+1
   visit(used|masks[i],selected+[i],deg)
   deg[a]-=1;deg[b]-=1
 visit(0,[],{})
 stats=Counter();seen_ribbons=set()
 for selected in found:
  own={q:i for i in selected for q in qs[i]};split={}
  for x,y in squares:
   slash=own[x,y,0]==own[x,y,1]
   assert (own[x,y,2]==own[x,y,3]) if slash else (own[x,y,0]==own[x,y,3] and own[x,y,1]==own[x,y,2])
   split[x,y]=slash
  if mode=='plane':
   sw,se,nw,ne=[split[q] for q in squares]
   if sw==se==nw==ne:kind='single'
   elif sw==se and nw==ne:kind='horizontal'
   elif sw==nw and se==ne:kind='vertical'
   else:raise AssertionError('wall turns')
   carried=[]
   for i in selected:
    a,b=es[i];mx=a[0]+b[0];my=a[1]+b[1]
    ends=[(mx,my-1),(mx,my+1)] if abs(a[0]-b[0])==2 else [(mx-1,my),(mx+1,my)]
    if (0,0) in ends:carried.append(i)
   assert len(carried)==2
   if kind=='horizontal':assert all(abs(es[i][1][0]-es[i][0][0])==2 for i in carried)
   if kind=='vertical':assert all(abs(es[i][1][0]-es[i][0][0])==1 for i in carried)
  else:
   assert all(sum(v in vertices[i] for i in selected)==2 for v in squares)
   if len(set(split.values()))==1:
    kind='single';sg=next(iter(split.values()));word={}
    for x,y in squares:
     k=(y-x)%6 if sg else (x+y+1)%6
     for quarter,delta in ((0,0),(2,1)):
      i=own[x,y,quarter];H=abs(es[i][1][0]-es[i][0][0])==2;index=(k+delta)%6
      assert index not in word or word[index]==H;word[index]=H
    seen_ribbons.add((sg,tuple(word[k] for k in range(6))))
   else:
    hz={y for x,y in squares if split[x,y]!=split[x,(y+1)%6]}
    vt={x for x,y in squares if split[x,y]!=split[(x+1)%6,y]}
    assert not(hz and vt)
    assert all(split[x,y]!=split[x,(y+1)%6] for y in hz for x in range(6))
    assert all(split[x,y]!=split[(x+1)%6,y] for x in vt for y in range(6))
    kind='horizontal' if hz else 'vertical'
  stats[kind]+=1
 if mode=='plane':assert len(es)==24 and stats=={'single':32,'horizontal':8,'vertical':8}
 else:assert len(found)==252 and len(seen_ribbons)==128 and stats['single']==128
 return dict(mode=mode,edges=len(es),solutions=len(found),search_nodes=steps,types=dict(stats),ribbon_words=len(seen_ribbons))
if __name__=='__main__':
 t=time.monotonic();r=[]
 for mode in ('plane','torus'):
  a=covers(mode);r.append(a);print(a,flush=True)
 Path('gap/verifier/claim30_checks.json').write_text(json.dumps(dict(date='2026-10-03',results=r,seconds=time.monotonic()-t),indent=2))
