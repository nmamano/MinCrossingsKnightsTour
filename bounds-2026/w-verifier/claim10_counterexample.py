from itertools import combinations
from pysat.solvers import Solver
import json
cycle=[(0,0),(1,2),(0,4),(2,3),(0,2),(2,1)]
forced={tuple(sorted([cycle[i-1],v])) for i,v in enumerate(cycle)}
for n in (6,8,10):
 cells=[(x,y) for x in range(n) for y in range(n)]
 edges=[(v,w) for v,w in combinations(cells,2) if sorted((abs(v[0]-w[0]),abs(v[1]-w[1])))==[1,2]]
 ids={e:i+1 for i,e in enumerate(edges)}
 clauses=[[ids[e]] for e in forced]
 for v in cells:
  inc=[ids[e] for e in edges if v in e]
  clauses.extend([-a,-b,-c] for a,b,c in combinations(inc,3))
  clauses.extend(list(c) for c in combinations(inc,len(inc)-1))
 with Solver(name='glucose4',bootstrap_with=clauses) as solver:
  sat=solver.solve()
  print('n',n,'2-factor containing forbidden strip cycle',sat)
  if not sat:continue
  positive=set(k for k in solver.get_model() if k>0)
  chosen=[e for e in edges if ids[e] in positive]
  assert all(sum(v in e for e in chosen)==2 for v in cells)
  assert forced<=set(chosen)
  json.dump({'n':n,'cycle':cycle,'edges':chosen},open('w-verifier/claim10_cycle_counterexample.json','w'),indent=1)
  break
