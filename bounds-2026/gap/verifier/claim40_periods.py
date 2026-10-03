"""Small periodic side stop tests, no Hamiltonian-completion claim."""
from pathlib import Path
from collections import defaultdict,Counter
import json
from ortools.sat.python import cp_model
from claim38_switch import edge,qs

def run(p,kind):
 es=[edge((x,y),(xx,y+dy)) for x in range(6) for xx in range(x+1,8) for y in range(p) for dy in (-2,-1,1,2) if sorted((xx-x,abs(dy)))==[1,2]]
 def canon(e):
  a,b=e;t=a[1]//p
  return edge((a[0],a[1]-t*p),(b[0],b[1]-t*p))
 forced=set()
 for y in range(p):
  forced.add(canon(edge((2,y),(0,y+1))))
  if kind=='period4':
   forced.add(canon(edge((3,y),(1,y+1))))
   if y%4!=3:forced.add(canon(edge((1,y),(0,y+2))))
   if y%4==1:forced.add(canon(edge((0,y),(1,y+2))))
  else:
   forced.add(canon(edge((1,y),(0,y+2))))
   forced.add(canon(edge((2,y),(1,y+2)) if y%p!=2 else edge((3,y+1),(1,y+2))))
 m=cp_model.CpModel();v={e:m.NewBoolVar('') for e in es};inc=defaultdict(list);own=defaultdict(list)
 for e,z in v.items():
  for x,y in e:inc[x,y%p].append(z)
  for x,y,k in qs(e):own[x,y%p,k].append(z)
  if e[0][0]<=1:m.Add(z==int(e in forced))
 for (x,y),ls in inc.items():m.Add(sum(ls)==2) if x<=5 else m.Add(sum(ls)<=2)
 # Fully represented square columns 3,4,5, good at every row.
 for x in (3,4,5):
  for y in range(p):
   for k in range(4):m.Add(sum(own[x,y,k])==1)
 # Minimise payable quarters at row zero instead of accepting an arbitrary extension.
 lifted=[]
 for e,z in v.items():
  for t in range(-2,3):
   f=edge((e[0][0],e[0][1]+t*p),(e[1][0],e[1][1]+t*p));lifted.append((f,z))
 pays=[]
 for x in (1,2):
  for k in range(4):
   qq=(x,0,k);cover=[(e,z) for e,z in lifted if qq in qs(e)]
   mult=sum(z for e,z in cover);bad=m.NewBoolVar('bad');m.Add(mult!=1).OnlyEnforceIf(bad);m.Add(mult==1).OnlyEnforceIf(bad.Not())
   doubles=[]
   for ii,(e,z) in enumerate(cover):
    for f,zz in cover[:ii]:
     if min(e[0][0],e[1][0])>1 or min(f[0][0],f[1][0])>1 or len(set(qs(e))&set(qs(f)))!=2:continue
     u=m.NewBoolVar('unpaid_pair');m.AddBoolAnd([z,zz]).OnlyEnforceIf(u);m.Add(mult==2).OnlyEnforceIf(u)
     eq=m.NewBoolVar('two');m.Add(mult==2).OnlyEnforceIf(eq);m.Add(mult!=2).OnlyEnforceIf(eq.Not())
     m.AddBoolOr([z.Not(),zz.Not(),eq.Not(),u]);doubles.append(u)
   unpaid=m.NewBoolVar('unpaid')
   if doubles:m.AddMaxEquality(unpaid,doubles)
   else:m.Add(unpaid==0)
   pay=m.NewBoolVar('pay');m.Add(pay==bad-unpaid);pays.append(pay)
 m.Minimize(sum(pays))
 s=cp_model.CpSolver();s.parameters.num_workers=1;s.parameters.max_time_in_seconds=5
 st=s.Solve(m);out=dict(period=p,kind=kind,status=s.StatusName(st),premise='degree 2 core 0..5; good squares 3..5 at every row')
 if st in (cp_model.OPTIMAL,cp_model.FEASIBLE):
  chosen={e for e,z in v.items() if s.Value(z)};cover=Counter(q for e in chosen for q in [(x,y%p,k) for x,y,k in qs(e)])
  # Count local payable quarters at the two end squares, with actual represented covering tiles.
  lifted={edge((a[0],a[1]+t*p),(b[0],b[1]+t*p)) for a,b in chosen for t in range(-3,4)}
  ls=defaultdict(list)
  for e in lifted:
   for q in qs(e):ls[q].append(e)
  rows=[]
  for y in range(p):
   payable=0;unpaid=0
   for x in (1,2):
    for k in range(4):
     z=ls[x,y,k]
     if len(z)==1:continue
     bad=(len(z)==2 and all(min(a[0],b[0])<=1 for a,b in z) and len(set(qs(z[0]))&set(qs(z[1])))==2)
     unpaid+=bad;payable+=not bad
   rows.append(dict(row=y,payable=payable,unpaid=unpaid,m1=[len(ls[1,y,k]) for k in range(4)],m2=[len(ls[2,y,k]) for k in range(4)]))
  out.update(edges=sorted(chosen),end_rows=rows)
 return out
out=[run(4,'period4'),run(6,'single_shift'),run(8,'single_shift')]
for r in out:print(r,flush=True)
# Explicit false-hole check in the proposed strip's incomplete halo.
def pn(x,y):return [(2,y+1),(1,y+2)] if x==0 else [(3,y+1),(0,y-2)] if x==1 else [(x+2,y+1),(x-2,y-1)]
full={edge((x,y),w) for x in range(12) for y in range(-12,13) for w in pn(x,y)}
restricted={e for e in full if min(e[0][0],e[1][0])<=5}
a=Counter(q for e in full for q in qs(e));b=Counter(q for e in restricted for q in qs(e))
falseholes=[q for q in [(6,0,0),(6,0,1)] if a[q]==1 and b[q]==0]
assert len(falseholes)==2
report=dict(periods=out,false_halo_holes=falseholes)
Path('gap/verifier/claim40_periods.json').write_text(json.dumps(report,indent=2))
print('False halo holes',falseholes)
