from pathlib import Path
import subprocess,time,json,os
root=Path(__file__).resolve().parents[2];cwd=root/'gap/verifier/claim52_run/bounds-2026'
cmds=['python3 w-turnstheory/check_knight_tiles.py','python3 w-turnstheory/check_corner_box.py','python3 w-turnstheory/check_square_defects.py','.venv/bin/python gap/lowerbounds/simple_strip/check_cut_certificate.py','python3 gap/verifier/claim50_check.py']
results=[]
for i,cmd in enumerate(cmds):
 start=time.monotonic();log=root/f'gap/verifier/claim52_command_{i}.log'
 with log.open('w') as f:r=subprocess.run(cmd.split(),cwd=cwd,stdout=f,stderr=subprocess.STDOUT,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1','OPENBLAS_NUM_THREADS':'1','OMP_NUM_THREADS':'1'},timeout=90)
 results.append(dict(command=cmd,exit=r.returncode,seconds=time.monotonic()-start,log=str(log.relative_to(root))));print(results[-1],flush=True)
 (root/'gap/verifier/claim52_commands.json').write_text(json.dumps(results,indent=2))
 assert r.returncode==0
