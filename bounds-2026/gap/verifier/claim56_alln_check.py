"""Independent counts, geometry, and path matchings for Claim 56 Part 2 (2026-10-04)."""
from pathlib import Path
import importlib.util,json,hashlib
ROOT=Path('gap/verifier/claim56_alln')
s=importlib.util.spec_from_file_location('own','gap/verifier/claim55_tests.py');own=importlib.util.module_from_spec(s);s.loader.exec_module(own)
ell=lambda u:u[0]+2*u[1]
def slab(g,n,a,w,dep):
 DB,DT,WL,WR=dep
 V={u for u in g if a<=ell(u)<a+w};seen=set();pairs=[];alph=[set(),set()]
 def label(u,v):
  external=v;side=0 if ell(external)<a else 1;cut=a+side*w
  lo,hi=sorted([u,v],key=ell);sides=[]
  if max(lo[1],hi[1])<DB:sides.append(('B',lo[1],hi[1]))
  if min(lo[1],hi[1])>=n-DT:sides.append(('T',n-1-lo[1],n-1-hi[1]))
  if max(lo[0],hi[0])<WL:sides.append(('L',lo[0],hi[0]))
  if min(lo[0],hi[0])>=n-WR:sides.append(('R',n-1-lo[0],n-1-hi[0]))
  assert len(sides)==1
  key=sides[0]+(ell(lo)-cut,ell(hi)-cut);assert key not in alph[side];alph[side].add(key)
  return side,key
 for start in V:
  if start in seen:continue
  seen.add(start);stack=[start];ends=[]
  while stack:
   u=stack.pop()
   for v in g[u]:
    if v not in V:ends.append(label(u,v))
    elif v not in seen:seen.add(v);stack.append(v)
  assert len(ends)==2,('internal cycle or non-path component',n,a,w,len(ends))
  pairs.append(ends)
 assert seen==V and alph[0]==alph[1]
 keys=sorted(alph[0]);idx={k:i for i,k in enumerate(keys)};M={}
 for a,b in pairs:
  u=(a[0],idx[a[1]]);v=(b[0],idx[b[1]]);assert u!=v and u not in M and v not in M
  M[u]=v;M[v]=u
 return keys,M

def glue(A,B):
 adj={}
 for M,k in [(A,0),(B,1)]:
  for a,b in M.items():
   if a>b:continue
   u=(a[0]+k,a[1]);v=(b[0]+k,b[1]);adj.setdefault(u,[]).append(v);adj.setdefault(v,[]).append(u)
 seen=set();out={}
 for start in adj:
  if start in seen:continue
  stack=[start];seen.add(start);ends=[]
  while stack:
   u=stack.pop()
   if u[0]!=1:ends.append((u[0]//2,u[1]))
   for v in adj[u]:
    if v not in seen:seen.add(v);stack.append(v)
  assert len(ends)==2,('cycle on gluing',ends)
  a,b=ends;out[a]=b;out[b]=a
 return out

report={}
for tag,wanted,constant in [('ES_res2',[2,10],-17),('ES_res6',[6,14],-16)]:
 folder=ROOT/tag;rep=json.loads((folder/'allsize_checks.json').read_text());ds={d['residue']:d for d in (json.loads(p.read_text()) for p in folder.glob('res*.json'))}
 assert sorted(ds)==wanted and rep['period']==16 and rep['step']==16 and rep['line_period']==8 and rep['dT_per_step']==128
 expected=list(range(50 if tag=='ES_res2' else 54,127,8));stored=[];manif=[]
 for f in sorted((folder/'tours').glob('*.json')):
  raw=f.read_bytes();d=json.loads(raw);n=d['n'];g=own.from_grid(d['tour']);t=own.audit(g,n)
  assert t==d['turns']==8*n+constant
  model=own.rebuild(ds[n%16],n);assert all(set(g[u])==set(model[u]) for u in g)
  stored.append(n);manif.append(dict(file=str(f),n=n,turns=t,sha256=hashlib.sha256(raw).hexdigest()))
 assert sorted(stored)==expected
 graphs={};counts=[]
 for n in sorted(set(expected+[tr['N']+16 for tr in rep['transfers']])):
  g=own.rebuild(ds[n%16],n);t=own.audit(g,n);assert t==8*n+constant;graphs[n]=g;counts.append([n,t])
 transfers=[]
 for tr in rep['transfers']:
  n=tr['N'];d=ds[n%16];k=tr['gap'];a=tr['cut'];w=8
  DB,DT=len(d['bottom']),len(d['top']);WL,WR=len(d['left'][0].split()),len(d['right'][0].split());dep=(DB,DT,WL,WR)
  shapes={c:set() for c in ['BL','BR','TL','TR']};spans={c:[] for c in shapes}
  for name in d['zones']:
   c,xy=name.split(':');dx,dy=map(int,xy.split(','));i=dx if c[1]=='L' else -1-dx;j=dy if c[0]=='B' else -1-dy
   assert i>=0 and j>=0;shapes[c].add((i,j));spans[c].append(dx+(n if c[1]=='R' else 0)+2*(dy+(n if c[0]=='T' else 0)))
  R=max(*dep,max(max(i,j)+1 for vs in shapes.values() for i,j in vs));assert R==8 and n>=max(96,2*R+6)
  for c,vs in shapes.items():
   W=WL if c[1]=='L' else WR;H=DB if c[0]=='B' else DT
   assert {(i,j) for i in range(W) for j in range(H)}<=vs
  order=['BL','BR','TL','TR'];ov=[(0,WL-1+2*(DB-1)),(n-WR,n-1+2*(DB-1)),(2*(n-DT),WL-1+2*(n-1)),(n-WR+2*(n-DT),3*n-3)]
  assert a>=max(max(spans[order[k]]),ov[k][1])+6
  assert a+w<=min(min(spans[order[k+1]]),ov[k+1][0])-6
  K,M=slab(graphs[n],n,a,8,dep)
  assert M==glue(glue(M,M),M)
  assert slab(graphs[n+16],n+16,a+k*16,8,dep)==(K,M)
  assert slab(graphs[n+16],n+16,a+k*16,24,dep)==(K,M)
  assert K==[tuple(x) for x in tr['ports']]
  claimed={tuple(u):tuple(v) for pair in tr['matching'] for u,v in [pair,pair[::-1]]};assert claimed==M
  transfers.append(dict(N=n,gap=k,cut=a,ports=len(K),M_cubed_equals_M=True,no_new_cycle=True))
 # Independent template-cell turn sum, without band_turns().
 d=next(iter(ds.values()));cost=0;band=[]
 for side in ['bottom','top','left','right']:
  rows=[r.split() for r in d[side]];period=len(rows[0]) if side in ['bottom','top'] else len(rows)
  t=sum((int(z[0])-int(z[1]))%8!=4 for row in rows for z in row)
  assert 16%period==0;cost+=16//period*t;band.append([side,period,t])
  horizontal=side in ['bottom','top'];depth=len(rows) if horizontal else len(rows[0])
  def vectors(u):
   along,deep=u if horizontal else (u[1],u[0])
   assert deep>=0
   if deep>=depth:return [(2,-1),(-2,1)]
   x,y=(along%period,deep) if horizontal else (deep,along%period)
   return [own.MOVES[int(k)] for k in rows[-1-y][x]]
  for along in range(period):
   for deep in range(depth+3):
    u=(along,deep) if horizontal else (deep,along)
    for dx,dy in vectors(u):
     v=(u[0]+dx,u[1]+dy)
     assert (-dx,-dy) in vectors(v)
 assert cost==128
 report[tag]=dict(supplied=manif,counts=counts,bands=band,transfers=transfers,classes=wanted,step=16,dT=128,constant=constant)
 print(tag,':',len(stored),'supplied tours;',len(transfers),'transfers;',len(transfers)*3,'independent slab checks; constant',constant,flush=True)
(ROOT/'independent_proof_checks.json').write_text(json.dumps(report,indent=2)+'\n')
print('ALL INDEPENDENT PROOF CHECKS PASS')
