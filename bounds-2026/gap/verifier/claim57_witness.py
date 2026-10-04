"""Use an optimizer only to find witnesses; the lower bounds are checked separately in exact arithmetic."""
import os,sys,runpy,json
from pathlib import Path
os.sched_setaffinity(0,sorted(os.sched_getaffinity(0))[:2])
A=int(sys.argv[1]);scale=int(sys.argv[2]);ctx=runpy.run_path('gap/verifier/claim57_corner_lp.py')
from scipy.optimize import milp,Bounds,LinearConstraint
import numpy as np
r=milp(ctx['costs'],integrality=np.ones(len(ctx['costs'])),bounds=Bounds(0,1),constraints=LinearConstraint(ctx['B'],ctx['rhs'],ctx['rhs']),options={'time_limit':90,'mip_rel_gap':0})
assert r.x is not None,r.message
selected=[ctx['options'][j] for j,x in enumerate(r.x) if x>.5]
assert len(selected)==len(ctx['cells'])
Path(f'gap/verifier/claim57_run/corner_A{A}_witness.json').write_text(json.dumps(dict(A=A,scale=scale,reported_cost=r.fun,choices=selected),indent=1)+'\n')
print('WITNESS',A,scale,r.message,r.fun,flush=True)
