"""Small exact width-six pairing and label checks. No solver or tour claims."""
from pathlib import Path
import json

def P(c): return c-3 if c%2==0 else c+3
def U(c): return c+5 if c%2==0 else c-5
def knight(a,b):return sorted(abs(a[i]-b[i]) for i in (0,1))==[1,2]
def neigh(v,kind):
 x,y=v
 if x==0:return {(2,y+1),(1,y+(2 if kind=='P' else -2))}
 if x==1:return {(3,y+1),(0,y+(-2 if kind=='P' else 2))}
 return {(x-2,y-1),(x+2,y+1)}
records=[]
for r in range(-6,7):
 for kind,path in [('P',[(4,r),(2,r-1),(0,r-2),(1,r),(3,r+1),(5,r+2)]),
                   ('U',[(5,r),(3,r-1),(1,r-2),(0,r),(2,r+1),(4,r+2)])]:
  assert all(knight(a,b) and b in neigh(a,kind) and a in neigh(b,kind) for a,b in zip(path,path[1:]))
  outside=[(x+2,y+1) for x,y in (path[0],path[-1])]
  labels=[x-2*y for x,y in outside]
  assert (P if kind=='P' else U)(labels[0])==labels[1]
  if r==0:records.append(dict(kind=kind,path=path,outside=outside,labels=labels))
for eps in (-1,1):
 for s in range(-12,13):
  for c in range(-12,13):
   commute=P(eps*c+s)==eps*P(c)+s
   assert commute==((eps==1 and s%2==0) or (eps==-1 and s%2==1))
# A pairing-only four-return shape: all shifts even, but no four-piece trap.
f={0:100,-3:101,2:104,-1:97}
assert all((v-k)%2==0 for k,v in f.items())
assert all(P(f[c])!=f[P(c)] for c in f)
out=dict(date='2026-10-03',pairing_examples=records,affine_commutation='epsilon=+1,s even OR epsilon=-1,s odd',
         unequal_shift_matching_shape=f,scope='pairing and label algebra only; no degree-two geometric completion claimed for the shape')
Path('gap/turnstheory/c5j_width6_check.json').write_text(json.dumps(out,indent=2)+'\n')
print('PASS: P/U width-six paths, distinct labelled pairings, affine commutation, unequal-shift matching shape.')
