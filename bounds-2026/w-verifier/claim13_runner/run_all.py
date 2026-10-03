import os,sys,subprocess
py=sys.executable
os.environ['OPENBLAS_NUM_THREADS']='1';os.environ['OMP_NUM_THREADS']='1';os.environ['MKL_NUM_THREADS']='1'
for name,cmd in [('beta_primary',[py,'beta_cert.py']),('beta_separate',[py,'-c','from strip2_independent import row_check; assert row_check(1,2)'])]:
 print('START',name,flush=True)
 with open(name+'.log','w') as out:subprocess.run(cmd,stdout=out,stderr=subprocess.STDOUT,check=True)
 print('PASS',name,flush=True)
os.chdir('../..')
with open('w-verifier/claim13_rows.log','w') as out:subprocess.run([py,'w-verifier/claim13_rows.py'],stdout=out,stderr=subprocess.STDOUT,check=True)
print('PASS own augmented graph',flush=True)
