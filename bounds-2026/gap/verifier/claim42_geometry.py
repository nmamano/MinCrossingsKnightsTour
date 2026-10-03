"""Exact geometry and Claim V support, no author imports."""
from itertools import combinations,product
from pathlib import Path
import json,hashlib
from claim26_certificate import edge,cross
from claim37_check import tile
qs=lambda e:{(x,y,q) for (x,y),h in tile(e) for q in h}
es=set()
for x,y in product((0,1),range(-3,4)):
 for dx,dy in ((1,2),(1,-2),(-1,2),(-1,-2),(2,1),(2,-1),(-2,1),(-2,-1)):
  if x+dx>=0:es.add(edge((x,y),(x+dx,y+dy)))
exc={edge((0,0),(2,1)),edge((0,1),(2,0))};B=[];vis=[]
for a,b in combinations(sorted(es),2):
 ov=qs(a)&qs(b)
 if not ov:continue
 assert cross(a,b) and len(ov) in (1,2)
 assert max(x for x,y,q in ov)<=2
 if any(x>=1 and y==0 for x,y,q in ov):
  if all(any(x==0 for x,y in e) for e in (a,b)):
   assert {a,b}==exc;B.append((a,b,sorted(ov)))
  elif len(ov)==2:
   vis.append((a,b,sorted(ov)))
   # At the end of row 0 both edges are pending.
   assert all(min(y for x,y in e)<=0<max(y for x,y in e) for e in (a,b))
assert len(B)==1 and len(vis)==7
# A quarter away from its own side cannot belong to another physical side's S*.
# Every strip tile has inward coordinate <=3, so its open quarters have square depth <=2.
assert all(max(x for x,y,q in qs(e))<=2 for e in es)
out={'date':'2026-10-03','B_pairs_touching_path_row':B,'VIS_pairs':vis,'max_strip_quarter_square_depth':2}
Path('gap/verifier/claim42_geometry.json').write_text(json.dumps(out,indent=1))
files=['gap/lowerbounds/FINDINGS.md','gap/lowerbounds/f1v_stab.py','gap/lowerbounds/frac_stab.py','gap/lowerbounds/strip_dp.py','gap/turnstheory/PROOF_5N_PLAN.md','gap/turnstheory/PROOF_52_11.md','w-turnstheory/PROOF_crossings_lower.md']
Path('gap/verifier/claim42_sources.json').write_text(json.dumps({f:hashlib.sha256(Path(f).read_bytes()).hexdigest() for f in files},indent=1))
print('PASS: one B exception pair, seven VIS pairs, all VIS edges pending; depth <=2.')
