import subprocess,sys,os
from pathlib import Path
py=sys.executable
os.environ['OPENBLAS_NUM_THREADS']='1';os.environ['OMP_NUM_THREADS']='1';os.environ['MKL_NUM_THREADS']='1'
checks=[('tiles',[py,'check_knight_tiles.py']),('corner_endpoint',[py,'check_corner_endpoint_charge.py']),('strip_rows',[py,'check_strip_row_certificate.py']),('alpha_primary',[py,'-c',"from fractions import Fraction; exec(open('alpha_star.py').read().split('lo, hi = Fraction(0), Fraction(2)')[0]); good,d=ok(Fraction(1,5)); assert good and (d.min(),d.max())==(-149,0); print('PASS alpha=1/5 potential -149..0')"]),('alpha_separate',[py,'-c','from strip2_independent import alpha_check; assert alpha_check(1,5)'])]
for name,cmd in checks:
 print('START',name,flush=True)
 with open(name+'.log','w') as f:subprocess.run(cmd,stdout=f,stderr=subprocess.STDOUT,check=True)
 print('PASS',name,flush=True)
os.chdir('../..')
for name in ['claim11_forest','claim11_corner','claim9_tiles']:
 print('START own',name,flush=True)
 with open('w-verifier/'+name+'_claim11_run.log','w') as f:subprocess.run([py,'w-verifier/'+name+'.py'],stdout=f,stderr=subprocess.STDOUT,check=True)
 print('PASS own',name,flush=True)
