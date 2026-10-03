"""Verify the independent beta witness against the original strip model."""
from fractions import Fraction
import json
exec(open('alpha_star.py').read().split('lo, hi = Fraction(0), Fraction(2)')[0])
doc=json.load(open('../claim13_rows.json'))['sharp_cycle'];lookup={s:i for i,s in enumerate(states)}
walk=[]
for (col,pend),flag in doc['states']:
 st=(col,tuple((a[0],a[1],b[0],b[1],label) for a,b,label in pend),0)
 walk.append((lookup[st],flag))
assert walk[0]==walk[-1] and states[walk[0][0]][0]==0 and walk[0][1]==0
W=B=0
for (u,f),(v,g),w,bad in zip(walk,walk[1:],doc['arc_weights'],doc['row_charges']):
 assert dict(adj[u])[v]==w
 nf=bool(f or (u,v) not in cyc);last=states[v][0]==0
 assert g==(0 if last else int(nf))
 assert bad==int(last and nf)
 W+=w;B+=bad
L=len(walk)-1
assert (L,W,B)==(16,6,4)
assert Fraction(4*W-L,4*B)==Fraction(1,2)
assert 1000*(4*W-L)-2004*B==-16
print('PASS original graph: 16 steps, weight 6, 4 bad rows; exact beta=1/2; cost at 501/1000 is -16/4000.')
