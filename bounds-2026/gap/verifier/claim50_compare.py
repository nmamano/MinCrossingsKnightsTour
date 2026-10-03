"""Cross-check the two implementations after independent reconstruction."""
import importlib.util,json
from pathlib import Path
from collections import Counter
import numpy as np
import claim50_check as I
p=Path('gap/lowerbounds/simple_strip/check_cut_certificate.py')
spec=importlib.util.spec_from_file_location('author_cut',p);A=importlib.util.module_from_spec(spec);spec.loader.exec_module(A)
assert set(A.TERMS.items())=={(I.edge(a,b),v) for a,b,v in I.raw}
vis={I.U[a]|I.U[b] for a,b in A.VIS};assert vis==set(I.vis[0])
assert {I.U[A.refl(a)]|I.U[A.refl(b)] for a,b in A.VIS}==set(I.vis[1])
encode=lambda ss:sum(I.C[e] for e in ss)
states=[frozenset()];ids={states[0]:0};count=0
for s in states:
 aa=[]
 for t,w,mask in A.row_arcs(s):
  if t not in ids:ids[t]=len(states);states.append(t)
  aa.append((encode(t),w,A.g_value(mask,1),A.g_value(mask,-1)))
 assert Counter(aa)==Counter(I.arcs_from(encode(s)));count+=len(aa)
pots=json.loads(Path('gap/verifier/claim50_potentials.json').read_text())
base=Path('gap/verifier/claim50_author_run/gap/lowerbounds/simple_strip')
for k,name in enumerate(('up','down')):
 pp=np.load(base/f'cut_potential_{name}.npy')
 assert all(int(pp[i])==pots[str(encode(s))][k] for i,s in enumerate(states))
result=dict(states=len(states),arcs=count,all_arcs_equal=True,all_potentials_equal=True,coefficients_equal=True,VIS_geometry_equal=True)
Path('gap/verifier/claim50_compare.json').write_text(json.dumps(result,indent=2));print(result)
