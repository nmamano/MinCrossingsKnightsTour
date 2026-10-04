from pathlib import Path
import json,sys,shutil,subprocess
R=Path('gap/verifier/claim56_alln');results=[]
def cp(src,name):
 p=R/name;shutil.copytree(R/src,p);return p
def run(p,partial=True,want=True):
 args=[sys.executable,str(R/'allsize_check.py'),str(p)]+(['--partial'] if partial else [])
 r=subprocess.run(args,capture_output=True,text=True);(R/(p.name+'_probe.log')).write_text(r.stdout+r.stderr)
 ok=r.returncode==0 and 'PASS: T(n)' in r.stdout;assert ok==want
 d=json.loads((p/'allsize_checks.json').read_text()) if ok else None
 results.append(dict(name=p.name,exit=r.returncode,scope=d['scope'] if d else None))
 print(p.name, 'PASS '+d['scope'] if d else 'REJECT',flush=True)
 return d
run(cp('ES_res2','no_partial'),partial=False,want=False)
p=cp('ES_res2','only_res02');(p/'res10.json').unlink();d=run(p)
assert d['scope']=='every even n >= 48 with n mod 16 in [2] (PARTIAL: other classes not covered)'
assert {tr['cls'] for tr in d['transfers']}=={2} and all(n%16==2 for n,t,src in d['direct'])
p=cp('ES_res2','duplicate_residue');shutil.copy2(p/'res02.json',p/'res_duplicate.json');run(p,want=False)
for name,val in [('odd_residue',3),('out_of_range_residue',18)]:
 p=cp('ES_res2',name);f=p/'res02.json';d=json.loads(f.read_text());d['residue']=val;f.write_text(json.dumps(d));run(p,want=False)
p=cp('ES_res2','bad_residue_base');f=p/'res02.json';d=json.loads(f.read_text());d['n0']+=8;f.write_text(json.dumps(d));run(p,want=False)
p=cp('ES_res2','renamed_file');(p/'res02.json').rename(p/'res99.json');d=run(p);assert '[2, 10]' in d['scope']
# w > p: a retained class must lift to every applicable class modulo s.
p=R/'lifted_classes';p.mkdir();src=Path('gap/verifier/claim55b_run/selftest_TT16/res02.json');d=json.loads(src.read_text())
for side in ['bottom','top']:d[side]=[r+' '+r for r in d[side]]
(p/'res02.json').write_text(json.dumps(d));d=run(p)
assert d['period']==8 and d['step']==16
assert {tr['cls'] for tr in d['transfers']}=={2,10}
assert 'n mod 8 in [2]' in d['scope']
(R/'partial_tests.json').write_text(json.dumps(results,indent=2)+'\n')
print('ALL',len(results),'PARTIAL-MODE TESTS PASS')
