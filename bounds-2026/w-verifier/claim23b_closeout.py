from pathlib import Path
import os,shutil,subprocess,time,json,hashlib,re,ast
root=Path.cwd();dest=root/'w-verifier/claim23b_closeout_clean';dest.mkdir(exist_ok=True)
files=[root/p for p in ('writeup/crossings/post.mdx','w-turnstheory/APPENDIX_STATUS.md','w-turnstheory/check_fold_margins.py','w-turnstheory/check_fold_proof.py')]
files+=list((root/'w-integrator/corners').glob('FOLD24_base_n*.json'))+list((root/'w-integrator/tours').glob('FOLD24_n*.json'))
manifest={}
for p in files:
 q=dest/p.relative_to(root);q.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,q);manifest[str(p.relative_to(root))]=hashlib.sha256(p.read_bytes()).hexdigest()
(dest/'sources.json').write_text(json.dumps(manifest,indent=2))
post=(root/'writeup/crossings/post.mdx').read_text();review=(root/'w-verifier/claim23b_review.md').read_text()
sections=re.split(r'\n### (\d+)\.',review.split('## Required replacements')[1].split('## Post body agreement')[0])
checks={}
for i in range(1,len(sections),2):
 n=int(sections[i]);quotes=re.findall(r'^> (.+)$',sections[i+1],re.M)
 checks[n]=[q in post for q in quotes]
assert len(checks)==8 and all(all(v) for v in checks.values()),checks
bodyquotes=re.findall(r'^> (.+)$',review.split('## Post body agreement')[1],re.M)
assert len(bodyquotes)==3 and all(q in post for q in bodyquotes)
url='https://github.com/nmamano/knights-tour-bounds'
assert url in post.split('## Details')[1].split('## Open questions')[0]
assert url in post.split('## Appendix: full proofs')[1]
assert 'w-verifier/' not in post
# Compare every unchanged helper and main body after removing only I/O changes and new assertions.
a=ast.parse((root/'w-verifier/claim23b_margins.py').read_text());b=ast.parse((root/'w-turnstheory/check_fold_margins.py').read_text())
fa={x.name:x for x in a.body if isinstance(x,ast.FunctionDef)};fb={x.name:x for x in b.body if isinstance(x,ast.FunctionDef)}
assert fa.keys()==fb.keys()
for name in fa:
 if name!='main':assert ast.dump(fa[name])==ast.dump(fb[name]),name
oldmain=fa['main'];newmain=fb['main']
loopold=oldmain.body[1];loopnew=newmain.body[1]
assert len(loopnew.body)==len(loopold.body)+2
extra=[x for x in loopnew.body if isinstance(x,ast.Assert)]
assert len(extra)==2
loopnew.body[0]=loopold.body[0]
loopnew.body=[x for x in loopnew.body if not isinstance(x,ast.Assert)]
newmain.body[2]=oldmain.body[2]
assert ast.dump(oldmain)==ast.dump(newmain)
oldman=json.loads((root/'w-verifier/claim23b_clean/sources.json').read_text())
changes=[p for p,h in oldman.items() if hashlib.sha256((root/p).read_bytes()).hexdigest()!=h]
out={'numbered_replacements':checks,'body_replacements':3,'source_links':['Details','Appendix'],'same_margin_helpers':True,'same_margin_main_after_path_changes_and_two_extra_assertions':True,'changes_since_23B':changes}
(dest/'text_and_code_checks.json').write_text(json.dumps(out,indent=2));print(out,flush=True)
os.sched_setaffinity(0,{min(os.sched_getaffinity(0))})
results=[]
for i,name in enumerate(('check_fold_margins.py','check_fold_proof.py'),1):
 cmd=['python3','w-turnstheory/'+name];start=time.monotonic()
 with (dest/f'command_{i}.log').open('w') as f:r=subprocess.run(cmd,cwd=dest,env={'PATH':'/usr/bin:/bin','LANG':'C.UTF-8','PYTHONDONTWRITEBYTECODE':'1','OMP_NUM_THREADS':'1'},stdout=f,stderr=subprocess.STDOUT)
 results.append({'command':cmd,'exit':r.returncode,'seconds':round(time.monotonic()-start,2)});(dest/'commands.json').write_text(json.dumps(results,indent=2));print(results[-1],flush=True)
 assert r.returncode==0
assert json.loads((dest/'w-turnstheory/fold_margin_checks.json').read_text())==json.loads((root/'w-verifier/claim23b_margins.json').read_text())
assert json.loads((dest/'w-turnstheory/fold_proof_checks.json').read_text())==json.loads((root/'w-verifier/claim23b_clean/w-turnstheory/fold_proof_checks.json').read_text())
assert all(hashlib.sha256((root/p).read_bytes()).hexdigest()==h for p,h in manifest.items())
(dest/'final_checks.json').write_text(json.dumps({'margin_report_identical':True,'fold_report_identical':True,'sources_unchanged_during_closeout':True},indent=2));print('ALL CLOSEOUT CHECKS PASS',flush=True)
