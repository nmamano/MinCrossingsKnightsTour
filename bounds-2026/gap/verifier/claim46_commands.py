"""Run each distinct displayed appendix check without changing source reports."""
from pathlib import Path
import concurrent.futures,subprocess,time,json,os
ROOT=Path(__file__).resolve().parents[2];WD=ROOT/'gap/verifier/claim46_run/bounds-2026'
(WD/'ktlean').symlink_to(ROOT/'ktlean',target_is_directory=True)
commands=['python3 w-turnstheory/check_fold_proof.py','python3 w-turnstheory/check_fold_margins.py','(cd ktlean && lake env lean Axioms.lean)','python3 w-turnstheory/check_knight_tiles.py','python3 w-turnstheory/check_square_defects.py','python3 w-turnstheory/check_corner_box.py','.venv/bin/python gap/verifier/claim42_geometry.py','python3 gap/turnstheory/check_quarter_payment_support.py','python3 gap/verifier/claim39_check.py','OPENBLAS_NUM_THREADS=1 .venv/bin/python gap/verifier/claim42_check.py','(cd gap/lowerbounds && ../../.venv/bin/python f1v_stab.py cert 1 1 up)','(cd gap/lowerbounds && ../../.venv/bin/python f1v_stab.py cert 1 1 down)']
def run(pair):
 i,cmd=pair;t=time.monotonic();path=ROOT/f'gap/verifier/claim46_command_{i:02d}.log'
 env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1','OPENBLAS_NUM_THREADS':'1','OMP_NUM_THREADS':'1'}
 with path.open('w') as f:
  try:r=subprocess.run(cmd,shell=True,cwd=WD,stdout=f,stderr=subprocess.STDOUT,env=env,timeout=180);status=r.returncode
  except subprocess.TimeoutExpired:status='TIMEOUT'
 return {'index':i,'command':cmd,'exit':status,'seconds':time.monotonic()-t,'log':str(path.relative_to(ROOT))}
out=[]
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
 for rec in pool.map(run,enumerate(commands)):
  out.append(rec);print(rec,flush=True);(ROOT/'gap/verifier/claim46_commands.json').write_text(json.dumps(out,indent=1))
