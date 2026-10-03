"""Check the verifier's exact sharp cycle against the original labelled graph."""
import json
from fractions import Fraction
exec(open('alpha_star.py').read().split('lo, hi = Fraction(0), Fraction(2)')[0])
data=json.load(open('../claim11_forest.json'))['sharp_cycle']
index={s:i for i,s in enumerate(states)}
cycle=[]
for col,pend in data['states']:
 st=(col,tuple((a[0],a[1],b[0],b[1],label) for a,b,label in pend),0)
 cycle.append(index[st])
assert cycle[0]==cycle[-1]
total=nc=negative=0
for u,v,w in zip(cycle,cycle[1:],data['arc_weights']):
 assert dict(adj[u])[v]==w
 noncritical=int((u,v) not in cyc)
 total+=w;nc+=noncritical;negative+=1000*(4*w-1)-804*noncritical
steps=len(cycle)-1
assert Fraction(4*total-steps,4*nc)==Fraction(1,5)
assert negative==-40
print('PASS original graph: steps',steps,'crossing weight',total,'non-cycle arcs',nc,'ratio 1/5; 201/1000 weight',negative,'in units 1/4000')
