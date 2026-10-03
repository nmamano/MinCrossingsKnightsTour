"""Small gentle-seam replay, one solver worker, five seconds per solve."""
import sys,json
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'w-structures'))
from seam import Seam,build_model
from run_seam import KIND
from seam_flux import cur_terms
from ortools.sat.python import cp_model
k=KIND['gentle'];st=Seam(T=k['T'](3),hv=k['hv'],w1=3,w2=3,f1=k['f1'],form1=k['form1'],f2=k['f2'],form2=k['form2'],s=1)
res=[]
for target in [None,-1,0,1]:
 m,x=build_model(st,lanes=False)
 if target is not None:
  terms,const=cur_terms(st,x);m.Add(sum(terms)+const==target)
 sol=cp_model.CpSolver();sol.parameters.num_workers=1;sol.parameters.max_time_in_seconds=5
 z=sol.Solve(m);r={'target':target,'status':sol.StatusName(z),'bound':sol.BestObjectiveBound()}
 if z in (cp_model.OPTIMAL,cp_model.FEASIBLE):
  chosen=[i for i,v in enumerate(x) if sol.Value(v)];a,b=cur_terms(st,[int(i in chosen) for i in range(len(x))]);r.update(X=sol.ObjectiveValue(),current=sum(a)+b,chosen=chosen)
 res.append(r);print(r,flush=True)
Path('gap/verifier/claim44_seam.json').write_text(json.dumps(res,indent=1))
