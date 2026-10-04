from pathlib import Path
import importlib.util
p=Path('gap/verifier/claim55_run/allsize_check.py')
s=importlib.util.spec_from_file_location('m',p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
def matchings(xs):
 if not xs:yield {};return
 a=xs[0]
 for b in xs[1:]:
  for sub in matchings([x for x in xs if x not in (a,b)]):yield {**sub,a:b,b:a}
def independent(A,B):
 adj={}
 for M,k in [(A,0),(B,1)]:
  for a,b in M.items():
   if a>b:continue
   u=(a[0]+k,a[1]);v=(b[0]+k,b[1]);adj.setdefault(u,[]).append(v);adj.setdefault(v,[]).append(u)
 seen=set();out={}
 for v in adj:
  if v in seen:continue
  comp={v};stack=[v];seen.add(v)
  while stack:
   for w in adj[stack.pop()]:
    if w not in seen:seen.add(w);comp.add(w);stack.append(w)
  ends=[v for v in comp if v[0]!=1]
  if not ends:return None
  assert len(ends)==2
  a,b=[(v[0]//2,v[1]) for v in ends];out[a]=b;out[b]=a
 return out
mats=list(matchings([(s,i) for s in (0,1) for i in range(4)]));ok=reject=0
for A in mats:
 for B in mats:
  expected=independent(A,B)
  try:got=m.compose(A,B)
  except AssertionError:assert expected is None;reject+=1
  else:assert got==expected;ok+=1
print('PASS:',len(mats)**2,'compositions;',ok,'cycle-free;',reject,'internal-cycle rejections')
