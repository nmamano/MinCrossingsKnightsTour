from pathlib import Path
import shutil, subprocess, os, json, hashlib, time
root=Path.cwd(); dest=root/'w-verifier/claim23b_clean'; dest.mkdir(exist_ok=True)
files=list((root/'w-turnstheory').glob('check_*.py'))
files += [root/'w-lowerbounds'/s for s in ('endpoint_independent.py','strip2_independent.py','strip_dp.py')]
files += list((root/'w-integrator/corners').glob('FOLD24_base_n*.json'))+list((root/'w-integrator/tours').glob('FOLD24_n*.json'))
files += [root/p for p in ('w-turnstheory/PROOF_fold.md','w-turnstheory/PROOF_crossings_lower.md','writeup/crossings/post.mdx','writeup/crossings/figures/cross_figs.py','writeup/crossings/figures/lower_figs.py','writeup/crossings/figures/heel_fig.py')]
manifest={}
for p in files:
 q=dest/p.relative_to(root);q.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,q);manifest[str(p.relative_to(root))]=hashlib.sha256(p.read_bytes()).hexdigest()
(dest/'sources.json').write_text(json.dumps(manifest,indent=2))
old=json.loads((root/'w-verifier/claim20_sources.json').read_text());old.update(json.loads((root/'w-verifier/claim12_full_manifest.json').read_text())['sha256'])
changes={p:{'old':v,'new':manifest.get(p),'changed':manifest.get(p)!=v} for p,v in old.items() if p in manifest}
(dest/'hash_changes.json').write_text(json.dumps(changes,indent=2))
commands=[['python3','w-turnstheory/'+s] for s in ('check_knight_tiles.py','check_corner_box.py','check_col0_squares.py','check_square_defects.py','check_lower_stability.py','check_crossings_lower.py','check_fold_proof.py')]
cpu=min(os.sched_getaffinity(0)); os.sched_setaffinity(0,{cpu})
res=[]
for i,cmd in enumerate(commands,1):
 t=time.monotonic()
 with (dest/f'command_{i}.log').open('w') as f:r=subprocess.run(cmd,cwd=dest,env={'PATH':'/usr/bin:/bin','LANG':'C.UTF-8','PYTHONDONTWRITEBYTECODE':'1','OMP_NUM_THREADS':'1','OPENBLAS_NUM_THREADS':'1'},stdout=f,stderr=subprocess.STDOUT)
 res.append({'command':cmd,'exit':r.returncode,'seconds':round(time.monotonic()-t,2)});(dest/'commands.json').write_text(json.dumps(res,indent=2));print(res[-1],flush=True)
 if r.returncode:break
