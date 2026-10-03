"""Coverage checks and a direct resource comparison on the old worst Hall set."""
import sys
sys.dont_write_bytecode=True
import json
from pathlib import Path
from fractions import Fraction
from collections import Counter
from check_hall_v3 import geometry,near
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'gap/turnstheory'
rows=json.loads((OUT/'hall_currency_results.json').read_text())
old=json.loads((OUT/'hall_v3_results.json').read_text())
assert len(rows)==len(old)==193
assert {s for r in rows for s in r['sources']}=={s for s,n in json.loads((OUT/'hall_inventory.json').read_text())}
assert sum(len(r['sources']) for r in rows)==345
for r,oldr in zip(rows,old):
 assert r['sha256']==oldr['sha256']
 for t,oldt in zip(r['mixed_trials'],oldr['trials']):
  assert t['Delta']==oldt['Delta'] and t['flow']==oldt['flow']
 for t in r['pure_trials']:assert t['Delta']=='0' and t['flow']==t['demand'] and not t['J']
for prev in json.loads((ROOT/'gap/verifier/claim29_tours.json').read_text()):
 r=next(r for r in rows if prev['source'] in r['sources'])
 assert r['B_union']==prev['B']
 print('PASS B union matches Claim 29:',prev['source'],prev['B'])
worst=json.loads((OUT/'hall_v3_worst_2_3.json').read_text())
J=worst['trials'][0]['J'];n=worst['n']
tour=json.loads((ROOT/worst['sources'][0]).read_text())['tour']
info,C,atoms=geometry(tour,pair_exclusion='B')
counts=Counter();newpairs=[]
for kind,box,units,geo in atoms:
 if kind!='pair' or not any(near(box,c,n,10) for c in J):continue
 def in_s(e,f):
  return any((any(p[k]<=1 for p in e) and any(p[k]<=1 for p in f)) or
             (any(p[k]>=n-2 for p in e) and any(p[k]>=n-2 for p in f)) for k in (0,1))
 counts['S_minus_B' if in_s(*geo) else 'outside_S']+=units;newpairs.append(geo)
assert counts['outside_S']==21
out=dict(source=worst['sources'][0],n=n,J=J,counts=dict(counts),
         pure_capacity=len(newpairs),demand=str(Fraction(2*len(J),3)),
         pure_signed_deficit=str(Fraction(2*len(J),3)-len(newpairs)),
         mixed_capacity='301/6',mixed_deficit='25/2',pure_neighbour_pairs=newpairs)
(OUT/'hall_currency_old_cut.json').write_text(json.dumps(out,indent=2)+'\n')
print('PASS full inventory and all exact flows; original mixed values unchanged.')
print('OLD J:',len(J),'paths; pure capacities',dict(counts),'total',len(newpairs))
print('OLD J pure signed deficit:',out['pure_signed_deficit'],'versus mixed deficit 25/2')
