"""Extra geometric hypotheses sufficient for the audited three-gap insertion proof."""
from pathlib import Path
import json
R=Path('gap/verifier/claim55_run')
for tag in ('selftest_TT16','selftest_L106b','selftest_swap','period16'):
 p=R/tag;rep=json.loads((p/'allsize_checks.json').read_text());ds={d['residue']:d for d in (json.loads(f.read_text()) for f in p.glob('res*.json'))}
 w,s=rep['line_period'],rep['step'];assert w>=5 and s%w==0
 for tr in rep['transfers']:
  N=tr['N'];a=tr['cut'];k=tr['gap'];d=ds[N%rep['period']]
  DB,DT=len(d['bottom']),len(d['top']);WL,WR=len(d['left'][0].split()),len(d['right'][0].split())
  local={c:set() for c in ('BL','BR','TL','TR')}
  for name in d['zones']:
   c,xy=name.split(':');x,y=map(int,xy.split(','));i=x if c[1]=='L' else -1-x;j=y if c[0]=='B' else -1-y
   assert min(i,j)>=0;local[c].add((i,j))
  radius=max(max(i,j)+1 for vs in local.values() for i,j in vs)
  assert N>=2*max(radius,DB,DT,WL,WR)+6
  for c,vs in local.items():
   width=WL if c[1]=='L' else WR;depth=DB if c[0]=='B' else DT
   assert {(i,j) for i in range(width) for j in range(depth)}<=vs
  overlap_ranges=[(0,WL-1+2*(DB-1)),(N-WR,N-1+2*(DB-1)),(2*(N-DT),WL-1+2*(N-1)),(N-WR+2*(N-DT),3*N-3)]
  assert a>=overlap_ranges[k][1]+6
  assert a+w<=overlap_ranges[k+1][0]-6
 print(tag,': extra geometry PASS; w =',w,'s =',s,'; all zones inward, separated, cover band overlaps; cuts in correct band-pair regimes')
