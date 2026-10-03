"""Fresh integer proper-crossing recount and witness reconstruction, 2026-10-03.
Standard library only. No imports from previous checkers or worker code.
"""
from pathlib import Path
from collections import defaultdict
import json,hashlib
ROOT=Path(__file__).resolve().parents[2]
def edge(a,b):return tuple(sorted((tuple(a),tuple(b))))
def det(a,b,c):return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
def cross(e,f):
 a,b=e;c,d=f
 return det(a,b,c)*det(a,b,d)<0 and det(c,d,a)*det(c,d,b)<0
moves=((-2,1),(-1,2),(1,2),(2,1),(2,-1),(1,-2),(-1,-2),(-2,-1))
def load(file):
 data=json.loads(Path(file).read_text());g=data['tour'];n=len(g);es=set()
 for row,rr in enumerate(g):
  assert len(rr)==n
  for x,code in enumerate(rr):
   assert len(code)==2 and code[0]!=code[1]
   for z in code:
    dy,dx=moves[int(z)];r,c=row+dy,x+dx
    assert 0<=r<n and 0<=c<n
    assert any((r+moves[int(t)][0],c+moves[int(t)][1])==(row,x) for t in g[r][c])
    es.add(edge((x,n-1-row),(c,n-1-r)))
 assert len(es)==n*n
 return data,n,es

def count(es):
 # Unit-square bounding-box bins. Any proper crossing belongs to a common bin.
 bins=defaultdict(list);answer=0
 for e in sorted(es):
  (x,y),(u,v)=e
  keys=[(a,b) for a in range(min(x,u),max(x,u)+1) for b in range(min(y,v),max(y,v)+1)]
  candidates={f for k in keys for f in bins[k]}
  answer+=sum(cross(e,f) for f in candidates)
  for k in keys:bins[k].append(e)
 return answer

def connected(es,n):
 adj=defaultdict(set)
 for a,b in es:adj[a].add(b);adj[b].add(a)
 assert len(adj)==n*n and all(len(v)==2 for v in adj.values())
 seen={(0,0)};todo=[(0,0)]
 while todo:
  for q in adj[todo.pop()]:
   if q not in seen:seen.add(q);todo.append(q)
 assert len(seen)==n*n

basefile='gap/verifier/claim36_FOLD_n288.json';newfile='gap/verifier/claim47_patched_n288.json'
b,n,es=load(basefile);d,nn,target=load(newfile);assert n==nn==288
connected(es,n);connected(target,n)
xb=count(es);xt=count(target);w=json.loads(Path('gap/verifier/claim47_U_gadget_24.json').read_text());changes=[]
for p in d['patches']:
 side,sign,t=p['side'],p['sign'],p['t']
 def T(v):
  x,y=v;y=t+sign*y
  return (x,y) if side==0 else (n-1-x,y) if side==1 else (y,x) if side==2 else (y,n-1-x)
 rem={edge(T(a),T(b)) for a,b in w['remove']};add={edge(T(a),T(b)) for a,b in w['add']}
 assert rem<=es and not add&es
 # Only pairs containing a changed edge can change. Count each unordered pair once.
 lost={tuple(sorted((e,f))) for e in rem for f in es if e!=f and cross(e,f)}
 nxt=es-rem|add
 gained={tuple(sorted((e,f))) for e in add for f in nxt if e!=f and cross(e,f)}
 change=len(gained)-len(lost);assert change==111
 changes.append(dict(patch=p,lost=len(lost),gained=len(gained),delta=change));es=nxt
assert es==target and len(changes)==4 and xt-xb==sum(p['delta'] for p in changes)==444
assert (xb,xt)==(1936,2380)
# Recount the reported d0=0 slack from the separately saved Claim 47 full-tour census.
census=json.loads(Path('gap/verifier/claim47_scan.json').read_text());slacks=[]
for r in census:
 sides=r['sides'];xx=sum(s['X3_minus_rows'] for s in sides);q=sum(s['Q3'] for s in sides);g=sum(s['g'] for s in sides);nf=sum(s['N_free0'] for s in sides)
 slack=xx+q//2-2*g-nf;assert q%2==0
 slacks.append(dict(file=r['file'],X3_minus_rows=xx,Q3=q,g=g,Nfree0=nf,slack_d0=slack,min_side_slack=min(s['X3_minus_rows']+s['Q3']/2-2*s['g']-s['N_free0'] for s in sides)))
assert [r['slack_d0'] for r in slacks]==[116,892]
assert slacks[1]['min_side_slack']==220
files=[basefile,newfile,'gap/verifier/claim47_U_gadget_24.json','gap/verifier/claim47_scan.json']
out=dict(date='2026-10-03',X_base=xb,X_patched=xt,patches=changes,slacks=slacks,slack_scope='Arithmetic from prior independent Claim 47 census; no fresh quarter census',sha256={f:hashlib.sha256(Path(f).read_bytes()).hexdigest() for f in files})
Path('gap/verifier/claim48_check.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
