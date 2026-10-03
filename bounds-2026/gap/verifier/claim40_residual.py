"""Light actual-tour test of baseline-plus-residual F1; uses audited atom/retention builder.
Own baseline subtraction and variable-demand max-flow. No new strip solver.
"""
import sys,json
from pathlib import Path
from collections import defaultdict
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'gap/turnstheory'))
from check_hall_v3 import geometry,Dinic,near
from claim38_switch import edge,qs
from check import MOVES

def run(file):
 grid=json.loads(Path(file).read_text())['tour'];info,cs,atoms=geometry(grid);n=info['n']
 es={edge((x,n-1-y),(x+MOVES[int(v)][1],n-1-y-MOVES[int(v)][0])) for y,row in enumerate(grid) for x,code in enumerate(row) for v in code}
 own=defaultdict(list)
 for e in es:
  for q in qs(e):own[q].append(e)
 lookup={(a[0],a[3]):j for j,a in enumerate(atoms)}
 def payable(q):
  ls=own[q];m=len(ls)
  if m==1:return None
  if not m:return lookup['G',q]
  if m>=3:return lookup['W3',q]
  pair=tuple(sorted(ls))
  return lookup.get(('pair',pair),lookup.get(('X1',pair)))
 def squares(c):
  fx,fy,r=c
  return [(n-2-x if fx else x,n-2-y if fy else y) for x,y in [(r,j) for j in range(1,r+1)]+[(i,r) for i in range(r-1,0,-1)]]
 candidates=[c for c in cs if c[2]>32]
 choices=[]
 for c in candidates:
  choices.append([(q,j) for x,y in squares(c) for k in range(4) for q in [(x,y,k)] for j in [payable(q)] if j is not None])
 trials=[]
 for method in ('lex','deep_first','shallow_first'):
  cap=[(2 if a[0]=='pair' else 1)*a[2] for a in atoms];demands=[]
  for opts in choices:
   def depth(q):return min(q[0],q[1],n-2-q[0],n-2-q[1])
   opts=sorted(opts,key=lambda qj:(-depth(qj[0]) if method=='deep_first' else depth(qj[0]) if method=='shallow_first' else 0,qj[0]))
   for q,j in opts[:2]:cap[j]-=1
   demands.append(max(0,2-len(opts)))
  assert min(cap,default=0)>=0
  deficient=[(c,d) for c,d in zip(candidates,demands) if d]
  for mode in ('whole_path','two_anchors','side_strip'):
   adj=[]
   for (fx,fy,r),d in deficient:
    anchors=[(3,2*r+1),(2*r+1,3)]
    anchors=[(2*(n-1)-x if fx else x,2*(n-1)-y if fy else y) for x,y in anchors]
    def eligible(a):
     if mode=='whole_path':return near(a[1],(fx,fy,r),n,10)
     x0,x1,y0,y1=a[1]
     for axis,((x,y),flip) in enumerate(zip(anchors,(fx,fy))):
      if max(abs(x0-x),abs(x1-x),abs(y0-y),abs(y1-y))>20:continue
      if mode=='two_anchors':return True
      # Anchor 0 is on the vertical side (axis 0), anchor 1 on the horizontal side.
      if a[0] in ('pair','X1'):
       if all(min(n-1-v[axis] if flip else v[axis] for v in e)<=5 for e in a[3]):return True
      else:
       dep=n-2-a[3][axis] if flip else a[3][axis]
       if 0<=dep<=5:return True
     return False
    adj.append([j for j,a in enumerate(atoms) if cap[j]>0 and eligible(a)])
   sink=1+len(adj)+len(atoms);D=Dinic(sink+1)
   for i,((c,d),ns) in enumerate(zip(deficient,adj)):
    D.arc(0,1+i,d)
    for j in ns:D.arc(1+i,1+len(adj)+j,10**6)
   for j,v in enumerate(cap):D.arc(1+len(adj)+j,sink,v)
   value,reach=D.solve(0,sink);total=sum(d for c,d in deficient)
   J=[i for i in range(len(adj)) if 1+i in reach];nb={j for i in J for j in adj[i]}
   assert sum(deficient[i][1] for i in J)-sum(cap[j] for j in nb)==total-value
   trials.append(dict(baseline=method,mode=mode,deficient_paths=len(deficient),demand_quarter_units=total,unpaid_quarter_units=total-value,hall_paths=[deficient[i][0] for i in J]))
 return dict(file=file,n=n,retained=len(cs),retained_large=len(candidates),trials=trials)
if __name__=='__main__':
 out=[]
 for f in sys.argv[1:]:
  r=run(f);out.append(r);print(json.dumps(r),flush=True)
 Path('gap/verifier/claim40_residual.json').write_text(json.dumps(out,indent=2))
