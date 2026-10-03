"""Pure non-B Hall tests on the same snapshot as the mixed v3 tests.
One process. Preserves all original mixed results. p=2/3 and 1/2, strict R=10.
"""
import sys
sys.dont_write_bytecode=True
import json,hashlib,time
from pathlib import Path
from fractions import Fraction
from check_hall_v3 import geometry,near,flow,selftest
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'gap/turnstheory'

def main():
 selftest(); old=json.loads((OUT/'hall_v3_results.json').read_text())
 assert len(old)==193 and all(r['valid'] for r in old)
 results=[];started=time.monotonic()
 for i,r in enumerate(old):
  tour=json.loads((ROOT/r['sources'][0]).read_text())['tour']
  h=hashlib.sha256(json.dumps(tour,separators=(',',':')).encode()).hexdigest()
  assert h==r['sha256']
  info,C,atoms=geometry(tour,pair_exclusion='B')
  for k in ('n','X','E','G','X1','W3','retained','S_union'):assert info[k]==r[k]
  pairs=[a for a in atoms if a[0]=='pair'];assert len(pairs)==info['X']-info['B_union']
  adj=[[j for j,a in enumerate(pairs) if near(a[1],c,info['n'],10)] for c in C]
  trials=[]
  for p,scale,demand in [('2/3',3,2),('1/2',2,1)]:
   value,J,N=flow(adj,[scale]*len(pairs),demand)
   deficit=Fraction(demand*len(C)-value,scale)
   trials.append(dict(p=p,radius=10,currency='unit crossing pairs outside B union',scale=scale,
      flow=value,demand=demand*len(C),Delta=str(deficit),J=[C[j] for j in J],
      neighbour_count=len(N),neighbour_pairs=[pairs[j][3] for j in N]))
  results.append(dict(**info,sources=r['sources'],sha256=h,mixed_trials=[{k:v for k,v in t.items() if k!='neighbour_atoms'} for t in r['trials']],pure_trials=trials))
  (OUT/'hall_currency_results.json').write_text(json.dumps(results,indent=2)+'\n')
  print(f"{i+1}/{len(old)} n={info['n']} "+' '.join(f"pure p={t['p']} Delta={t['Delta']}" for t in trials)+f" {r['sources'][0]} elapsed={time.monotonic()-started:.1f}s",flush=True)
 assert len(results)==len(old)
 lines=['# Hall currency comparison — 2026-10-03','',
        'Same 193 validated tours, 345 saved records, strict radius 10. Mixed means nu_p, lambda=p.',
        'Pure means unit capacity per proper crossing pair outside the union B of the four outer-column pair sets.',
        'Each row gives the exact maximum Hall deficit over all retained-path subsets.','',
        '| Source | n | Retained | Mixed 2/3 | Pure 2/3 | Mixed 1/2 | Pure 1/2 |',
        '| --- | ---: | ---: | ---: | ---: | ---: | ---: |']
 with (OUT/'hall_currency_results.tsv').open('w') as f:
  f.write('source\tn\tretained\tmixed_2_3\tpure_2_3\tmixed_1_2\tpure_1_2\tsha256\n')
  for r in results:
   vals=[r['mixed_trials'][0]['Delta'],r['pure_trials'][0]['Delta'],r['mixed_trials'][1]['Delta'],r['pure_trials'][1]['Delta']]
   name=next((s for s in r['sources'] if s.startswith('w-integrator/tours/') and '/certificates/' not in s),r['sources'][0])
   lines.append('| `'+name+'` | '+' | '.join(map(str,[r['n'],r['retained']]+vals))+' |')
   for s in r['sources']:f.write('\t'.join(map(str,[s,r['n'],r['retained']]+vals+[r['sha256']]))+'\n')
 (OUT/'HALL_CURRENCY_RESULTS.md').write_text('\n'.join(lines)+'\n')
 for pi in (0,1):
  worst=max(results,key=lambda r:(Fraction(r['pure_trials'][pi]['Delta']),r['n']))
  (OUT/f"hall_pure_worst_{worst['pure_trials'][pi]['p'].replace('/','_')}.json").write_text(json.dumps(worst,indent=2)+'\n')
  print('PURE MAX',worst['pure_trials'][pi]['p'],worst['pure_trials'][pi]['Delta'],worst['sources'],flush=True)
 print('DONE',len(results),'boards',time.monotonic()-started,'seconds',flush=True)
if __name__=='__main__':main()
