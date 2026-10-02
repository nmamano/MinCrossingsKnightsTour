from fractions import Fraction
import json
exec(open('kappa2_star.py').read().split('lo, hi = Fraction(1, 5), Fraction(2)')[0])
good,h=ok3(Fraction(2,7),20000)
assert good and (int(h.min()),int(h.max()))==(-167,0)
print('PRIMARY PASS',int(h.min()),int(h.max()),flush=True)
doc=json.load(open('../claim14.json'))['runs']['witness'];lookup={s:i for i,s in enumerate(states)}
walk=[]
for (col,pend),f,pb in doc['states']:
 st=(col,tuple((a[0],a[1],b[0],b[1],label) for a,b,label in pend),0)
 walk.append((lookup[st],f,pb))
assert walk[0]==walk[-1]
W=L=0
for (u,f,pb),(v,g,qb),w in zip(walk,walk[1:],doc['arc_weights']):
 assert dict(adj[u])[v]==w
 dirty=int(f or (u,v) not in cyc);end=states[v][0]==0
 assert (g,qb)==((0,dirty) if end else (dirty,pb))
 L+=dirty+3*dirty*(1-pb) if end else 0;W+=w
S=len(walk)-1
assert (S,W,L)==(20,7,7)
assert Fraction(4*W-S,4*L)==Fraction(2,7)
assert 5000*(4*W-S)-4*1431*L==-68
print('ORIGINAL GRAPH WITNESS PASS: 20 steps, weight 7, run mass 7; exact 2/7; negative -68/20000 at 1431/5000.',flush=True)
