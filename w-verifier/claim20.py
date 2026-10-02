"""Independent checks of the standalone proof's new loop and larger-box argument."""
from pathlib import Path
from itertools import product
import json
from claim9_tiles import proper,det
from claim11_corner import M,chi,canon

def raw(e,s):
 E=tuple((2*x,2*y) for x,y in e)
 if not proper(E,s):return 0
 return 1 if det(s[0],s[1],E[0])>0 else -1

def main():
 dual=[]
 for x,y in product(range(-4,6),repeat=2):
  a=(2*x+1,2*y+1)
  dual.extend([(a,(a[0]+2,a[1])),(a,(a[0],a[1]+2))])
 checked=0
 for p in product(range(2),repeat=2):
  for dx,dy in M:
   q=(p[0]+dx,p[1]+dy)
   sx=1 if dx>0 else -1;sy=1 if dy>0 else -1
   ds=[(sx,0),(0,sy),(sx,0)] if abs(dx)==2 else [(0,sy),(sx,0),(0,sy)]
   route=[p]
   for x,y in ds:route.append((route[-1][0]+x,route[-1][1]+y))
   assert route[-1]==q
   count=0
   for s in dual:
    v=raw((p,q),s);assert v==sum(raw(e,s) for e in zip(route,route[1:]));count+=abs(v)
   assert count==3;checked+=1
 # Larger box top end at R=0, with all possible nearby nonnegative-x edges.
 top=[((3,1),(1,1)),((1,1),(-1,1))]
 edges=set()
 for x,y in product(range(7),range(-4,5)):
  for dx,dy in M:
   q=(x+dx,y+dy)
   if q[0]>=0:edges.add(canon((x,y),q))
 coeff={e:chi(e[0])*sum(raw(e,s) for s in top) for e in edges}
 coeff={e:c for e,c in coeff.items() if c}
 old=json.loads(Path('w-verifier/claim18.json').read_text())['corner'][0]['left_terms']
 F={canon(tuple(a),tuple(b)):c for (a,b),c in old}
 assert len(coeff)==8
 for e in edges|set(F):assert coeff.get(e,0)-F.get(e,0)==int((0,0) in e)
 assert all(min(a[1],b[1])<=0<max(a[1],b[1]) for a,b in coeff)
 tr=lambda p:(p[1],p[0])
 right=[(tr(b),tr(a)) for a,b in top]
 for e,c in coeff.items():assert chi(e[0])*sum(raw(tuple(map(tr,e)),s) for s in right)==c
 # Unit-grid flux across the actual Q_R, including outside-left and outside-bottom steps.
 cases=[]
 for R in (12,13,14,15,24,25,100,101):
  pts=[(3,2*R+1),(1,2*R+1),(-1,2*R+1)]
  pts += [(-1,y) for y in range(2*R-1,-2,-2)]
  pts += [(x,-1) for x in range(1,2*R+2,2)]
  pts += [(2*R+1,1),(2*R+1,3)]
  outside=ends=0
  for i,(a,b) in enumerate(zip(pts,pts[1:])):
   # Grid-edge endpoint on the left of this directed dual step.
   dx,dy=b[0]-a[0],b[1]-a[1]
   p=((a[0]+b[0]-dy)//4,(a[1]+b[1]+dx)//4)
   c=chi(p)
   if i<2 or i>=len(pts)-3:ends+=c
   else:outside+=c
  assert ends==0 and outside==1+(-1)**R
  assert (outside+2*(-1)**R)%3==1
  cases.append({'R':R,'outside_grid_flux':outside,'end_grid_flux':ends,'Q_charge_mod3':1})
 assert 4*1131+0==4524
 assert 164+2*1131==2426 and 2426+12==2438<=6*407
 out={'date':'2026-10-02','knight_routes_checked':checked,'dual_steps_per_route':len(dual),'top_end_coefficients':[(e,c) for e,c in sorted(coeff.items())],'coefficient_identity':'end flux = F + degree(0,0)','larger_boxes':cases,'exact_bound':'14n/3 - 1219/3'}
 Path('w-verifier/claim20.json').write_text(json.dumps(out,indent=1));print('ALL INDEPENDENT NEW-INPUT CHECKS PASS')
if __name__=='__main__':main()
