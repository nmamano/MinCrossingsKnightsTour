from pathlib import Path
import os,subprocess,json,time,sys
root=Path.cwd(); dest=root/'w-verifier/claim23b_clean'
os.sched_setaffinity(0,{min(os.sched_getaffinity(0))})
checks=[]
for old,new in [('claim20','claim23b_geometry'),('claim19','claim23b_stability'),('claim12_affine_margins','claim23b_margins'),('claim12_full','claim23b_fold')]:
 s=(root/f'w-verifier/{old}.py').read_text()
 s=s.replace(f'w-verifier/{old}.json',f'w-verifier/{new}.json').replace('w-verifier/claim12_full_results.json','w-verifier/claim23b_fold_results.json')
 if new=='claim23b_margins': s=s.replace('from claim12_full import SHIFT','SHIFT=((0,6),(6,24),(18,0),(24,18),(0,0),(0,24),(24,0),(24,24),(0,12),(12,0),(12,24),(24,12),(12,12))')
 p=root/f'w-verifier/{new}.py';p.write_text(s)
 checks.append((root,['.venv/bin/python',str(p.relative_to(root))]))
checks.append((root/'ktlean',['lake','env','lean','Axioms.lean']))
results=[]
for i,(cwd,cmd) in enumerate(checks,1):
 t=time.monotonic()
 with (dest/f'extra_{i}.log').open('w') as f:r=subprocess.run(cmd,cwd=cwd,env={'PATH':os.environ['PATH'],'HOME':os.environ['HOME'],'LANG':'C.UTF-8','PYTHONDONTWRITEBYTECODE':'1','OMP_NUM_THREADS':'1','LEAN_NUM_THREADS':'1'},stdout=f,stderr=subprocess.STDOUT)
 results.append({'command':cmd,'exit':r.returncode,'seconds':round(time.monotonic()-t,2)})
 (dest/'extra_commands.json').write_text(json.dumps(results,indent=2));print(results[-1],flush=True)
 if r.returncode:break
