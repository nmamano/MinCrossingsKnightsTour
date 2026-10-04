from pathlib import Path
import json,sys,importlib.util,shutil
root=Path.cwd();out=root/'gap/verifier/claim55b_run'
sys.path[:0]=[str(root),str(root/'w-integrator')]
spec=importlib.util.spec_from_file_location('pipe',out/'later_allpipe.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
m.ROOT=str(root);m.HERE=str(out);shutil.copy2(root/'w-integrator/menu_turns.json',out/'menu_turns.json')
d=json.loads((root/'gap/verifier/claim55_run/selftest_TT16/tours/selftest_TT16_n56.json').read_text());d.update(A=6,B=6)
g=m.grid_to_full(d['tour']);seq=[];prev=None;u=(0,0)
while u not in seq:
 seq.append(u);v=next(v for v in g[u] if v!=prev);prev,u=u,v
N=len(seq);pos={u:i for i,u in enumerate(seq)}
knight=lambda u,v:sorted([abs(u[0]-v[0]),abs(u[1]-v[1])])==[1,2]
found=False
for i,a in enumerate(seq):
 if not(20<=a[0]<36 and 20<=a[1]<36):continue
 b=seq[(i+1)%N]
 for dx,dy in [(x,y) for x in [-2,-1,1,2] for y in [-2,-1,1,2] if abs(x*y)==2]:
  c=(a[0]+dx,a[1]+dy);j=pos.get(c,-1)
  if j<=i+1 or (i==0 and j==N-1):continue
  e=seq[(j+1)%N]
  if knight(b,e):seq[i+1:j+1]=seq[i+1:j+1][::-1];found=True;break
 if found:break
assert found
new={u:{seq[(i-1)%N],seq[(i+1)%N]} for i,u in enumerate(seq)}
tour=m.check(56,new);assert tour is not None
d['tour']=tour;p=out/'far_change_base.json';p.write_text(json.dumps(d))
sys.argv=['allpipe.py','--tag','far_guard_probe',str(p)]
try:m.main()
except SystemExit as e:
 assert 'REJECT' in str(e) and 'corner distance >= 16' in str(e),str(e)
 print('EXPECTED REJECTION:',e)
else:raise AssertionError('far-change guard did not reject')
