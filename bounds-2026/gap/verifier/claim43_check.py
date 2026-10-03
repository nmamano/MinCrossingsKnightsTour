"""Light red-team checks of BEYOND5_FLUX, 2026-10-03. No author imports."""
from pathlib import Path
from collections import Counter
from fractions import Fraction
from itertools import product
import json,hashlib
from claim26_certificate import edge
from claim37_check import tile
H=(2,1);V=(-1,-2)
def neighbours(p,w):
 x,y=p;t=x-y
 a=H if w[t%len(w)]=='H' else V
 b=H if w[(t-1)%len(w)]=='H' else V
 return [(x+a[0],y+a[1]),(x-b[0],y-b[1])]
def current(w):
 P=len(w) if len(w)%2==0 else 2*len(w)
 # Flux across the vertical cut x=1/2, signed at the left endpoint;
 # one complete y-period of left endpoints counts each edge orbit once.
 stubs=[]
 for x,y in product(range(-2,1),range(P)):
  for q in neighbours((x,y),w):
   if q[0]>0:stubs.append(((x,y),q,(1 if (x+y)%2==0 else -1)))
 I=Fraction(sum(e[2] for e in stubs),P)
 a=sum((-1)**t for t in range(P) if w[t%len(w)]=='V')
 assert I==Fraction(-3*a,P)
 return I,P,a,stubs
words=['H','V','HV','HHVV','HHV','HVVVHV','HVHHHV','VVHHVHVV','VHHVVHVH','HVVH']
results=[]
for w in words:
 I,P,a,stubs=current(w)
 es={edge(p,q) for p in product(range(-4,13),repeat=2) for q in neighbours(p,w)}
 counts=Counter((x,y,q) for e in es for (x,y),h in tile(e) for q in h)
 for p in product(range(8),repeat=2):
  nn=neighbours(p,w);assert len(set(nn))==2
  assert all(p in neighbours(q,w) for q in nn)
  assert all(counts[p[0],p[1],q]==1 for q in 'BRTL')
 results.append({'word':w,'vertical_current_per_row':str(I),'period':P,'signed_V_count':a,'alternations':sum(w[t]!=w[(t+1)%len(w)] for t in range(len(w)))})
# Every binary word through length eight: the signed parity formula, not alternation count.
zero_mixed=0;checked=0
for k in range(1,9):
 for w in map(''.join,product('HV',repeat=k)):
  I,*_=current(w);checked+=1
  zero_mixed+=len(set(w))==2 and I==0
# Near-maximal alternation density, but current tends to zero.
dilute=[]
for m in (2,4,8,16):
 w='HV'*(m+1)+'VH'*m;I,P,a,_=current(w)
 assert abs(I)==Fraction(3,len(w))
 dilute.append({'length':len(w),'current':str(I),'alternations':sum(w[t]!=w[(t+1)%len(w)] for t in range(len(w)))})
# A single / ribbon x-y=40 meets three corner candidate families.
n=200;d=40;hits={}
for corner in range(4):
 rr=[]
 for r in range(12,n//2-3):
  pp=[(r,j) for j in range(1,r+1)]+[(i,r) for i in range(r-1,0,-1)]
  for k in range(corner):pp=[(n-2-y,x) for x,y in pp]
  q=[p for p in pp if p[0]-p[1]==d]
  if q:rr.append((r,q))
 hits[corner]=rr
assert [k for k,v in hits.items() if v]==[0,1,2]
# The proposed fraction is correct under its stated hypotheses.
for mu in (1,2,3,4):
 for c in (Fraction(1,3),Fraction(1,2)):
  for j in range(101):
   b=Fraction(j,100);price=(1+b+2*c*(1-b)/mu)/(2+b)
   assert price>=min(Fraction(2,3),Fraction(1,2)+c/mu)
example=json.loads(Path('gap/verifier/claim42_geometry.json').read_text())['VIS_pairs'][0]
report={'date':'2026-10-03','fields':results,'words_checked':checked,'zero_current_mixed_words':zero_mixed,'small_nonzero_current_family':dilute,'three_corner_ribbon':{'n':n,'x_minus_y':d,'hits':hits},'S_minus_B_pair':example,'conditional_fraction_check':'PASS'}
Path('gap/verifier/claim43_check.json').write_text(json.dumps(report,indent=1))
files=['gap/searcher/BEYOND5_FLUX.md','gap/searcher/WALL12.md','gap/searcher/FINDINGS.md','w-integrator/FINDINGS.md','gap/searcher/wall/ribbon_ends.out']
Path('gap/verifier/claim43_sources.json').write_text(json.dumps({f:hashlib.sha256(Path(f).read_bytes()).hexdigest() for f in files},indent=1))
print(json.dumps({**report,'three_corner_ribbon':{k:[len(v),v[0] if v else None,v[-1] if v else None] for k,v in hits.items()}},indent=1))
