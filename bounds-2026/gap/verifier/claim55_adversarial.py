from pathlib import Path
import json,shutil,subprocess,sys,importlib.util
ROOT=Path('gap/verifier/claim55_run')
spec=importlib.util.spec_from_file_location('checker',ROOT/'allsize_check.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
def copy(name):
 dst=ROOT/name;shutil.copytree(ROOT/'selftest_TT16',dst);return dst

def run(d):
 r=subprocess.run([sys.executable,str(ROOT/'allsize_check.py'),str(d)],capture_output=True,text=True)
 (ROOT/(d.name+'.log')).write_text(r.stdout+r.stderr)
 print(d.name,'exit',r.returncode,'PASS' if 'PASS: T(n)' in r.stdout else 'REJECT',flush=True)
 return r

# A redundant bottom-band override that is off-board only at n=48 in its class.
bad=copy('bad_fallback_size');f=bad/'res00.json';d=json.loads(f.read_text())
g=m.graph(d,56);d['zones']['BL:48,0']=[[v[0]-48,v[1]] for v in g[48,0]];f.write_text(json.dumps(d))
# Supply a genuine 16x16 tour under the expected 48x48 filename.
small=json.loads(Path('gap/verifier/claim34_tour_n16.json').read_text());sg=m.tour_grid(small['tour']);m.validate(sg)
small['n']=48;(bad/'tours'/'selftest_TT16_n48.json').write_text(json.dumps(small))
r=run(bad);assert r.returncode==0 and 'PASS: T(n)' in r.stdout
rep=json.loads((bad/'allsize_checks.json').read_text());print('wrong-size direct record:',next(x for x in rep['direct'] if x[0]==48),'actual cells',len(sg),flush=True)

# Without a fallback the same bad transplant must fail.
no=copy('bad_no_fallback');(no/'res00.json').write_text(f.read_text());(no/'tours'/'selftest_TT16_n48.json').unlink();assert run(no).returncode!=0
# Missing residue, inconsistent phase, illegal zone moves must fail.
no=copy('bad_missing_residue');(no/'res06.json').unlink();assert run(no).returncode!=0
no=copy('bad_phase');f=no/'res00.json';d=json.loads(f.read_text());d['phases'][0]+=1;f.write_text(json.dumps(d));assert run(no).returncode!=0
no=copy('bad_move');f=no/'res00.json';d=json.loads(f.read_text());d['zones']['BL:0,0']=[[0,0],[1,2]];f.write_text(json.dumps(d));assert run(no).returncode!=0
# Same mathematical templates, declared period 16: exercises s > p.
no=copy('period16');
for f in no.glob('res*.json'):
 d=json.loads(f.read_text())
 for side in ['bottom','top']:d[side]=[row+' '+row for row in d[side]]
 f.write_text(json.dumps(d))
assert run(no).returncode==0
