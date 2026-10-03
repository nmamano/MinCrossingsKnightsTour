import subprocess,sys,pathlib,json
py=sys.executable
for f in sorted(pathlib.Path('certs').glob('*.cnf')):
 subprocess.run([py,'check_drup.py',str(f),str(f.with_suffix('.drup'))],check=True)
import sat_cert as c
from pysat.solvers import Solver
for o in 'hv':
 for ox in (0,1):
  args=list(c.m3_instance(7,o,ox,0)); args[5]=(args[5]+1)%3
  E,cls,_=c.build(*args)
  with Solver(name='glucose4',bootstrap_with=cls) as s:assert s.solve()
  print('wrong-residue SAT','m3',o,ox,flush=True)
for pat in 'PQ':
 args=list(c.nem3_instance(pat,8,4)); args[5]=(args[5]+1)%3
 E,cls,_=c.build(*args)
 with Solver(name='glucose4',bootstrap_with=cls) as s:assert s.solve()
 print('wrong-residue SAT','nem3',pat,flush=True)
pathlib.Path('empty.drup').write_text('')
assert subprocess.run([py,'check_drup.py','certs/m3_W7_h_ox0.cnf','empty.drup']).returncode==1
for f in ['strip_constants.py','strip2_independent.py','corner_charge.py','corner_charge2.py']:
 print('START',f,flush=True)
 with open(f+'.log','w') as out:subprocess.run([py,f],stdout=out,stderr=subprocess.STDOUT,check=True)
 print('DONE',f,flush=True)
