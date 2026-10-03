from pathlib import Path
import os,shutil,subprocess,time,json,hashlib
root=Path.cwd();dest=root/'w-verifier/claim23a_closeout_clean';dest.mkdir(exist_ok=True)
files=[root/p for p in ('writeup/turns/post.mdx','writeup/turns/check_corner.py','writeup/turns/figures/tt16.py','w-turnstheory/check_proof.py','w-turnstheory/check_corner_certificate.py','w-turnstheory/corner_witness.txt','w-turnstheory/check_upper_proofs.py')]
files+=list((root/'kt').glob('*.py'))+list((root/'w-integrator/corners').glob('TT16_res*.json'))+list((root/'w-integrator/corners').glob('H16a_VE_res*.json'))+list((root/'w-integrator/tours').glob('TT16_n*.json'))
manifest={}
for p in files:
 q=dest/p.relative_to(root);q.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,q);manifest[str(p.relative_to(root))]=hashlib.sha256(p.read_bytes()).hexdigest()
(dest/'sources.json').write_text(json.dumps(manifest,indent=2))
(dest/'.venv').symlink_to(root/'.venv',target_is_directory=True) if not (dest/'.venv').exists() else None
cpu=min(os.sched_getaffinity(0));env={'PATH':os.environ['PATH'],'HOME':os.environ['HOME'],'LANG':'C.UTF-8','PYTHONDONTWRITEBYTECODE':'1','OMP_NUM_THREADS':'1','OPENBLAS_NUM_THREADS':'1','LEAN_NUM_THREADS':'1','MPLCONFIGDIR':str(dest/'mpl_cache')}
commands=[(dest,['python3','w-turnstheory/check_proof.py']),(dest,['python3','writeup/turns/check_corner.py']),(dest,['python3','w-turnstheory/check_corner_certificate.py']),(dest,['.venv/bin/python','writeup/turns/figures/tt16.py']),(dest,['python3','w-turnstheory/check_upper_proofs.py']),(root/'ktlean',['lake','build']),(root/'ktlean',['lake','env','lean','Axioms.lean'])]
results=[]
for i,(cwd,cmd) in enumerate(commands,1):
 start=time.monotonic()
 with (dest/f'command_{i}.log').open('w') as f:r=subprocess.run(cmd,cwd=cwd,env=env,stdout=f,stderr=subprocess.STDOUT,preexec_fn=lambda:os.sched_setaffinity(0,{cpu}))
 results.append({'command':cmd,'cwd':str(cwd.relative_to(root)),'exit':r.returncode,'seconds':round(time.monotonic()-start,2)});(dest/'commands.json').write_text(json.dumps(results,indent=2));print(results[-1],flush=True)
