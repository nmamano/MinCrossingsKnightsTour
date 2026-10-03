"""Small exact checks for the proposed carrier argument; no worker imports."""
from collections import Counter
from fractions import Fraction as F
from pathlib import Path
import json
from claim9_tiles import quarters,proper
# Crossing-free degree-two field: undirected edges p -- p+(2,1).
E=[((x,y),(x+2,y+1)) for x in range(-5,6) for y in range(-5,6)]
C=Counter(t for e in E for t in quarters(e))
assert all(C[x,y,k]==1 for x in range(-2,3) for y in range(-2,3) for k in range(4))
s=((F(1,2),F(1,2)),(F(3,2),F(1,2)))
# Normal points up. Positive black-to-white crossings have positive y direction.
phi=0
for a,b in E:
 if proper((a,b),s):phi+=1 if sum(a)%2==0 else -1
assert phi==1
qphi=-1 # grid edge (1,0)--(1,1), black endpoint (1,1), normal up
assert (phi+qphi)%3==0
# Periodic gentle seam from the audited tile example.
E=[((x,y),(x+1,y-2) if y>=x else (x+2,y-1)) for x in range(-10,11) for y in range(-10,11)]
C=Counter(t for e in E for t in quarters(e))
for x in range(-4,5):
 for y in range(-4,5):assert [C[x,y,k] for k in range(4)]==([0,2,2,0] if y==x-2 else [1,1,1,1])
out={'date':'2026-10-02','uniform_field':{'quarter_multiplicity':1,'raw_H_flux':phi,'Q_flux':qphi,'height_charge_mod3':0},'seam_per_1_1_period':{'gap_quarters':2,'double_quarters':2,'bad_quarters':4,'crossings':1,'net_translation_Manhattan':2},'route_length_counterexample':{'endpoints':[[0,0],[2,0]],'route':[[0,0],[0,2],[2,2],[2,0]],'route_length':6,'shortest_Manhattan_length':2}}
Path('w-verifier/claim17.json').write_text(json.dumps(out,indent=1));print(out)
