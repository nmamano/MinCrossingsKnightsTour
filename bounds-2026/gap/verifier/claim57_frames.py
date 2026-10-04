"""Exact coefficient/frame checks for Claim 57; no graph solutions or worker imports."""
from pathlib import Path
from collections import defaultdict,Counter
import json
D=[(a,b) for a in [-2,-1,1,2] for b in [-2,-1,1,2] if abs(a*b)==2]
S=[tuple(map(int,l.split())) for l in Path('gap/verifier/claim57_run/source_z6_slots.txt').read_text().splitlines()]
expected={(x,y,x+a,y+b) for x in range(6) for y in [-2,-1] for a,b in D if 0<=x+a<6 and y+b>=0}
assert len(S)==28 and set(S)==expected
w={s:((1 if s[2]<s[0] else -1) if min(s[0],s[2])>=3 else 0) for s in S}
sigma=lambda s:(s[2],-1-s[3],s[0],-1-s[1])
assert all(sigma(s) in w and sigma(sigma(s))==s and w[sigma(s)]==-w[s] for s in S)
edge=lambda u,v:tuple(sorted((u,v)))
def cut(c):return {edge((x,c+y),(X,c+Y)):w[x,y,X,Y] for x,y,X,Y in S}
def cleaned(d):return {k:v for k,v in d.items() if v}
actual=defaultdict(int)
for e,v in cut(0).items():actual[e]+=v
for e,v in cut(1).items():actual[e]-=v
want=defaultdict(int)
for x in range(3,6):
 for dx,dy in D:
  if 3<=x+dx<6:want[edge((x,0),(x+dx,dy))]+=1 if dx>0 else -1
assert cleaned(actual)==cleaned(want)
records=[]
for A in [10,14,20]:
 for n in list(range(2*A,2*A+12))+[2*A+31,2*A+100]:
  def rot(p,k):
   x,y=p
   for _ in range(k):x,y=y,n-1-x
   return x,y
  def cross(k,c,horizontal=False):
   ans={}
   for slot in S:
    x,y,X,Y=slot
    u,v=((c+y,x),(c+Y,X)) if horizontal else ((x,c+y),(X,c+Y))
    ans[slot]=edge(rot(u,k),rot(v,k))
   return ans
  cover=Counter();allcoeff=defaultdict(int)
  for k in range(4):
   for x in range(A):
    for y in range(A):
     if min(x,y)<6:cover[rot((x,y),k)]+=1
   for x in range(6):
    for y in range(A,n-A):cover[rot((x,y),k)]+=1
   vs=cross(k,A);hs=cross(k,A,True);end=cross(k,n-A);next_h=cross((k+1)%4,A,True)
   assert all(end[sigma(slot)]==next_h[slot] for slot in S)
   for slot in S:
    # corner reduced cost + side reduced cost
    allcoeff[vs[slot]]-=w[slot]
    allcoeff[hs[slot]]+=w[sigma(slot)]
    allcoeff[vs[slot]]+=w[slot]
    allcoeff[end[slot]]-=w[slot]
  ring={(x,y) for x in range(n) for y in range(n) if min(x,y,n-1-x,n-1-y)<6}
  assert set(cover)==ring and set(cover.values())=={1}
  assert not cleaned(allcoeff)
  records.append(dict(A=A,n=n,ring_cells=len(ring),frame_identity=True,partition=True,boundary_cancellation=True))
Path('gap/verifier/claim57_run/frames.json').write_text(json.dumps(dict(slots=28,row_divergence_identity=True,cases=records),indent=2)+'\n')
print('PASS: slot enumeration, mirror, row divergence; exact partition/frame/cancellation for',len(records),'(A,n) pairs')
