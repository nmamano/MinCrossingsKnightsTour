"""Independent demo decoder and count audit, no worker imports."""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib
from check import check
ALPHA='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_'
P={'orig':8,'paper':8,'heel21':8,'P40':40,'H16a':24,'LF4':48,'FOLD':24,'T18':24,'TT16':8}
expected={'orig':(F(13),F(19,2)),'paper':(F(12),F(19,2)),'heel21':(F(51,4),F(37,4)),'P40':(F(23,2),F(39,4)),'H16a':(F(9),F(41,4)),'LF4':(F(343,48),F(43,4)),'FOLD':(F(19,3),F(38,3)),'T18':(F(51,4),F(17,2)),'TT16':(F(19,2),F(8))}
summary=json.loads(Path('demo/data/summary.json').read_text());res={'scope':'local serving directory; HTTP unavailable','samples':[],'slopes':{},'all_metadata':{}}
for key,period in P.items():
 ns=sorted(map(int,summary[key]));assert ns==list(range(96 if key in ('LF4','FOLD') else 48,201,2))
 for n in ns:
  d=json.loads(Path(f'demo/data/{key}_n{n}.json').read_text());assert all(d[k]==summary[key][str(n)][k] for k in ('key','n','valid','crossings','turns','brute_crossings'))
 for m,slope in zip(('crossings','turns'),expected[key]):
  slopes={F(summary[key][str(n+period)][m]-summary[key][str(n)][m],period) for n in ns if n+period in ns};assert slopes=={slope},(key,m,slopes)
 res['slopes'][key]=list(map(str,expected[key]));res['all_metadata'][key]=len(ns)
 sample=sorted(set(n for n in (48,50,52,54,56,58,60,62,88,96,98,100,102,114,120,144,192,198,200) if n in ns))
 for n in sample:
  p=Path(f'demo/data/{key}_n{n}.json');d=json.loads(p.read_text());assert len(d['cells'])==n*n and all(c in ALPHA for c in d['cells'])
  codes=[str(ALPHA.index(c)//8)+str(ALPHA.index(c)%8) for c in d['cells']];grid=[codes[i*n:(i+1)*n] for i in range(n)]
  X,T=check(grid);assert (X,T)==(d['crossings'],d['turns']);assert d['valid']
  if d['brute_crossings'] is not None:assert d['brute_crossings']==X
  if key=='TT16':assert T==8*n-14
  if key=='FOLD':assert F(X)-F(19*n,3)<=142
  res['samples'].append({'key':key,'n':n,'X':X,'T':T,'bX':str(X-expected[key][0]*n),'bT':str(T-expected[key][1]*n),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
 print(key,'checked',len(sample),'tours; slopes',res['slopes'][key],flush=True)
Path('w-verifier/claim22_samples.json').write_text(json.dumps(res,indent=2));print('PASS',len(res['samples']),'independent full-tour checks',sum(res['all_metadata'].values()),'metadata checks')
