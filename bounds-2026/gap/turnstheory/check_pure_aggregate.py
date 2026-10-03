"""Read saved audited-tour counts; no geometry or Hall-flow rerun."""
import json
from fractions import Fraction
from pathlib import Path
HERE=Path(__file__).resolve().parent
rows=json.loads((HERE/'hall_v3_results.json').read_text())
assert len(rows)==193 and all(r['valid'] for r in rows)
out=[]
for r in rows:
 xout=r['X']-r['S_union']
 out.append(dict(n=r['n'],L=r['retained'],X_out=xout,T=r['S_union']-4*r['n']+2,
  deficit_half=str(Fraction(r['retained'],2)-xout),
  deficit_two_thirds=str(Fraction(2*r['retained'],3)-xout),sources=r['sources']))
(HERE/'pure_aggregate_check.json').write_text(json.dumps(out,indent=2)+'\n')
for key in ('deficit_half','deficit_two_thirds'):
 print(key)
 for r in sorted(out,key=lambda r:Fraction(r[key]),reverse=True)[:5]:
  print(r['n'],r['L'],r['X_out'],r[key],r['sources'][0])
