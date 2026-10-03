"""Insert pairing-preserving patches at period 28 into audited closed FOLD tours."""
from claim47_check import *
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'w-verifier'))
from check import check,MOVES
w=json.loads(Path('gap/verifier/claim47_U_gadget_24.json').read_text());W,H=6,24
out=[]
for file in sys.argv[1:]:
 grid=json.loads(Path(file).read_text())['tour'];n=len(grid)
 es={edge((x,n-1-y),(x+MOVES[int(v)][1],n-1-y-MOVES[int(v)][0])) for y,row in enumerate(grid) for x,code in enumerate(row) for v in code};adj=graph(es)
 used=set();patches=[]
 for side in range(4):
  for sign in (1,-1):
   last=-100
   for t in range(15,n-H-15):
    if t-last<28:continue
    def T(v):
     x,y=v;y=t+sign*y
     return (x,y) if side==0 else (n-1-x,y) if side==1 else (y,x) if side==2 else (y,n-1-x)
    V={T((x,y)) for x in range(W) for y in range(H)}
    if V&used:continue
    if not all(adj[T((x,y))]=={T(z) for z in nn((x,y))} for x in range(9) for y in range(-7,H+8)):continue
    used|=V;last=t;patches.append(dict(side=side,sign=sign,t=t))
 # Conditions above use the original graph; patches change disjoint vertex sets.
 for p in patches:
  side,sign,t=p['side'],p['sign'],p['t']
  def T(v):
   x,y=v;y=t+sign*y
   return (x,y) if side==0 else (n-1-x,y) if side==1 else (y,x) if side==2 else (y,n-1-x)
  for a,b in w['remove']:
   a,b=T(a),T(b);adj[a].remove(b);adj[b].remove(a)
  for a,b in w['add']:
   a,b=T(a),T(b);assert b not in adj[a];adj[a].add(b);adj[b].add(a)
 og=[['' for x in range(n)] for y in range(n)]
 for (x,y),nb in adj.items():og[n-1-y][x]=''.join(str(MOVES.index((y-v,u-x))) for u,v in sorted(nb))
 X,_=check(og);dst=f'gap/verifier/claim47_patched_n{n}.json';Path(dst).write_text(json.dumps(dict(tour=og,patches=patches,source=file)))
 out.append(dict(n=n,X=X,patches=patches,file=dst));print(out[-1],flush=True)
Path('gap/verifier/claim47_insert.json').write_text(json.dumps(out,indent=2))
