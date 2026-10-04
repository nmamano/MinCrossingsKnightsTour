"""New adversarial tests for Claim 55b; data copies only."""
from pathlib import Path
import json,shutil,sys,subprocess,importlib.util
R=Path('gap/verifier/claim55b_run')
s=importlib.util.spec_from_file_location('chk',R/'allsize_check.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
results=[]
def make(name,mut=None):
 d=R/name;shutil.copytree(R/'selftest_TT16',d)
 if mut:
  for f in d.glob('res*.json'):
   x=json.loads(f.read_text());mut(x);f.write_text(json.dumps(x))
 return d

def run(d,want=False,args=(),opt=False):
 cmd=[sys.executable]+(['-O'] if opt else [])+[str(R/'allsize_check.py'),str(d),*args]
 r=subprocess.run(cmd,capture_output=True,text=True)
 (R/(d.name+('_opt' if opt else '')+'.log')).write_text(r.stdout+r.stderr)
 passed=r.returncode==0 and 'PASS: T(n)' in r.stdout
 assert passed==want,(d.name,r.returncode,r.stdout,r.stderr)
 row=dict(name=d.name,exit=r.returncode,pass_message='PASS: T(n)' in r.stdout,last=(r.stdout+r.stderr).strip().splitlines()[-1])
 results.append(row);print(d.name,'PASS' if passed else 'REJECT',row['last'][:130],flush=True)
 return d

run(make('bad_empty_template',lambda d:d.update(bottom=[])))
def ragged(d):d['bottom'][0]+=' 26'
run(make('bad_ragged_template',ragged))
def duplicate(d):d['bottom'][0]='00 '+ ' '.join(d['bottom'][0].split()[1:])
run(make('bad_duplicate_template_move',duplicate))
def invalid(d):d['bottom'][0]='89 '+ ' '.join(d['bottom'][0].split()[1:])
run(make('bad_template_code',invalid))
run(make('bad_outward_zone',lambda d:d['zones'].update({'BR:0,0':[[2,-1],[-2,1]]})))
run(make('bad_zero_period',lambda d:d.update(period=0)))
run(make('bad_odd_period',lambda d:d.update(period=7)))
def narrow(d):
 for k in ['bottom','top']:d[k]=[' '.join(row.split()[:4]) for row in d[k]]
 for k in ['left','right']:d[k]=d[k][:2]
run(make('bad_width4',narrow))
run(make('bad_optimized_python'),opt=True)
# Force early fallback, with a genuine n48 grid but wrong metadata or malformed grid.
def fallback(d):
 if d['residue']==0:
  g=m.graph(d,56);d['zones']['BL:48,0']=[[v[0]-48,v[1]] for v in g[48,0]]
for name,change in [
 ('bad_fallback_metadata',lambda d:d.update(n=50)),
 ('bad_fallback_row_length',lambda d:d['tour'][0].pop()),
 ('bad_fallback_code',lambda d:d['tour'][0].__setitem__(0,'001'))]:
 p=make(name,fallback);f=p/'tours'/'selftest_TT16_n48.json';d=json.loads(f.read_text());change(d);f.write_text(json.dumps(d));run(p)
# A redundant right-band patch destroys diagonal gap clearance, though it leaves each tested board unchanged.
def blocked_gap(d):
 g=m.graph(d,96);u=(95,47);d['zones']['BR:-1,47']=[[v[0]-u[0],v[1]-u[1]] for v in g[u]]
run(make('bad_gap_clearance',blocked_gap))
# Unsupported mixed-field metadata is ignored; PASS still refers to the hard-coded straight field.
run(make('mixed_metadata_ignored',lambda d:d.update(interior={'kind':'mixed','period':5,'directions':[[2,-1],[2,1]]})),True)
# Coordinate aliases are normalized by zone_cells; redundant aliases do not change the graph.
run(make('redundant_coordinate_alias',lambda d:d['zones'].update({'BL:00,0':d['zones']['BL:0,0']})),True)
# A smaller valid induction base is allowed; 96 is a default, not a required mathematical threshold.
run(make('base_override48'),True,args=('--Nmin','48'))
(R/'new_tests.json').write_text(json.dumps(results,indent=2)+'\n')
print('ALL',len(results),'NEW TESTS MATCH EXPECTED OUTCOMES')
