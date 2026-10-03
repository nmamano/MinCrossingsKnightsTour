import sys,time,json,hashlib
from pathlib import Path
sys.path.insert(0,'gap/lowerbounds/gaplemma')
import tree_automaton as A
out=[];start=time.time()
for ty in A.block_types():
 rows=[]
 for v in A.side_link_solutions(ty):
  rows.append((tuple(v[d,s] for d in 'BRTL' for s in '/\\'),tuple(v['ex'][d] for d in 'BRTL')))
 rows.sort(key=repr)
 out.append(dict(types=tuple(ty[q] for q in A.BLOCK),count=len(rows),sha256=hashlib.sha256(repr(rows).encode()).hexdigest()))
 print(len(out),len(rows),round(time.time()-start,2),flush=True)
Path('gap/verifier/claim41_author_patches.json').write_text(json.dumps(out,indent=2))
print('TOTAL',sum(v['count'] for v in out),flush=True)
