"""Produce the readable inventory and cross-check the three Claim 29 inputs."""
import json
from pathlib import Path
from collections import defaultdict
from fractions import Fraction
root=Path(__file__).resolve().parents[2]
folder=root/'gap/turnstheory'
rows=json.loads((folder/'hall_v3_results.json').read_text())
by_source={s:r for r in rows for s in r['sources']}
expected=json.loads((folder/'hall_inventory.json').read_text())
assert set(by_source)=={s for s,n in expected}, 'run incomplete'
assert all(r['valid'] for r in rows), [(r['sources'],r.get('error')) for r in rows if not r['valid']]
for old in json.loads((root/'gap/verifier/claim29_tours.json').read_text()):
    new=by_source[old['source']]
    for key in ('n','X','E','G','X1','W3','retained'):assert new[key]==old[key], (old['source'],key)
assert sum(s.startswith('w-integrator/tours/FOLD24_n') for s in by_source)==36
print('PASS: full inventory covered; all valid; all three Claim 29 geometries agree; 36 primary FOLD24 tours covered.')
lines=['# Strict mixed-capacity Hall screening — 2026-10-03','',
       f'{len(rows)} distinct validated tours; {len(by_source)} saved JSON records. R=10 throughout.',
       'At each price, lambda=p. Delta is exact, not rounded. n<128 is additional screening outside the stated v3 size range.','',
       '| Primary file | n | X | Retained | Delta, p=2/3 | Delta, p=1/2 | Saved copies |',
       '| --- | ---: | ---: | ---: | ---: | ---: | ---: |']
for r in rows:
    primary=next((s for s in r['sources'] if s.startswith('w-integrator/tours/') and '/certificates/' not in s),r['sources'][0])
    trials={t['p']:t for t in r['trials']}
    lines.append(f"| `{primary}` | {r['n']} | {r['X']} | {r['retained']} | {trials['2/3']['Delta']} | {trials['1/2']['Delta']} | {len(r['sources'])} |")
lines += ['', 'Every saved file and its board hash is listed in `hall_v3_results.tsv`.',
          'Full details and source aliases are in `hall_v3_results.json`.']
(folder/'HALL_V3_RESULTS.md').write_text('\n'.join(lines)+'\n')
for family in ('FOLD24','H16a','LF4','TT16','FIELD'):
    selected=[r for r in rows if any(Path(s).name.startswith(family+'_') for s in r['sources'])]
    print(family, 'unique',len(selected),'n',sorted({r['n'] for r in selected}),
          'maxDelta',{p:str(max(Fraction(next(t for t in r['trials'] if t['p']==p)['Delta']) for r in selected)) for p in ('2/3','1/2')})
print('n>=128',sum(r['n']>=128 for r in rows))
