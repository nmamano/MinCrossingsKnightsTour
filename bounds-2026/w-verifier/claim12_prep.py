"""Independent FOLD24 finite-tour audit. No worker code imports."""
from pathlib import Path
from fractions import Fraction
import json,hashlib
from check import check

def main():
 files=sorted(Path('w-integrator/tours').glob('FOLD24_n*.json'),key=lambda p:int(p.stem.split('_n')[-1]))
 rows=[]
 for f in files:
  raw=f.read_bytes();d=json.loads(raw);x,t=check(d['tour']);n=len(d['tour'])
  assert n==d['n']==int(f.stem.split('_n')[-1])
  assert (x,t)==(d['crossings'],d['turns'])
  b=Fraction(3*x-19*n,3);assert b<=142
  row={'file':str(f),'n':n,'crossings':x,'turns':t,'b':str(b),'valid':True,'sha256':hashlib.sha256(raw).hexdigest()}
  rows.append(row);print(n,x,t,'b='+str(b),flush=True)
 assert len(rows)==36 and {r['n'] for r in rows}==set(range(96,168,2))
 residues=[]
 for n0 in range(96,120,2):
  rr=[r for r in rows if r['n']%24==n0%24]
  assert [r['n'] for r in rr]==[n0,n0+24,n0+48]
  assert len({r['b'] for r in rr})==1
  assert all(b['crossings']-a['crossings']==152 for a,b in zip(rr,rr[1:]))
  assert all(b['turns']-a['turns']==304 for a,b in zip(rr,rr[1:]))
  residues.append({'residue':n0%24,'base':n0,'b':rr[0]['b'],'crossings':[r['crossings'] for r in rr],'turns':[r['turns'] for r in rr]})
 copies=[]
 for f in sorted(Path('w-integrator/tours/certificates').glob('FOLD24_n*.json')):
  raw=f.read_bytes();d=json.loads(raw);x,t=check(d['tour']);n=len(d['tour'])
  assert (x,t)==(d['crossings'],d['turns']) and n==d['n']
  base=json.loads(Path(f'w-integrator/tours/FOLD24_n{n}.json').read_text())
  assert d['tour']==base['tour']
  copies.append({'file':str(f),'n':n,'crossings':x,'turns':t,'same_grid':True,'sha256':hashlib.sha256(raw).hexdigest()})
 templates=[]
 for f in sorted(Path('w-integrator/corners').glob('FOLD24_base_n*.json')):
  raw=f.read_bytes();d=json.loads(raw)
  templates.append({'file':str(f),'n0':d['n0'],'p':d['p'],'lo':d['lo'],'band':d['band'],'rad':d['rad'],'template_cells':len(d['template']),'component_sizes':sorted(len(c['cells']) for c in d['components']),'sha256':hashlib.sha256(raw).hexdigest()})
 report={'date':'2026-10-02','tours':rows,'residues':residues,'certificate_copies':copies,'base_data':templates}
 Path('w-verifier/claim12_prep_results.json').write_text(json.dumps(report,indent=1))
 print('PASS: 36 tours,',len(copies),'certificate copies, all crossing increments 152, all turn increments 304.',flush=True)
 print('Base component signatures:',sorted({tuple(r['component_sizes']) for r in templates}),flush=True)
if __name__=='__main__':main()
