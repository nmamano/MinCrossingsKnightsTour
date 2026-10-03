from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import subprocess,time,json,os
root=Path(__file__).resolve().parents[2];cwd=root/'gap/verifier/claim53_run/bounds-2026';cmds=json.loads((root/'gap/verifier/claim53_command_list.json').read_text())
def run(rec):
 i,cmd=rec;start=time.monotonic();log=root/f'gap/verifier/claim53_command_{i}.log'
 with log.open('w') as f:r=subprocess.run(cmd.split(),cwd=cwd,stdout=f,stderr=subprocess.STDOUT,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1','OPENBLAS_NUM_THREADS':'1','OMP_NUM_THREADS':'1'},timeout=120)
 return dict(command=cmd,exit=r.returncode,seconds=time.monotonic()-start,log=str(log.relative_to(root)))
with ThreadPoolExecutor(max_workers=2) as pool:results=list(pool.map(run,enumerate(cmds)))
(root/'gap/verifier/claim53_commands.json').write_text(json.dumps(results,indent=2));print(json.dumps(results,indent=2));assert all(r['exit']==0 for r in results)
