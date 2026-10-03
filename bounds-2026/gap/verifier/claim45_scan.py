"""Exact C5-4 census on saved closed tours, 2026-10-03.
Uses audited retention/atom builder and author's R-b counts; separately computes BQx.
"""
from pathlib import Path
import sys,json,time
from collections import defaultdict
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'gap/lowerbounds/beyond5'))
import r_b
from claim38_switch import edge,qs
from check import MOVES,check
basegeom=r_b.geometry
cache={}
def geom(g):
 info,cs,atoms=basegeom(g);cache.update(info=info,cs=cs,atoms=atoms);return info,cs,atoms
r_b.geometry=geom
out=[]
for file in sys.argv[1:]:
 start=time.monotonic();res=r_b.run(file);grid=json.loads(Path(file).read_text())['tour'];n=len(grid)
 X,_=check(grid);assert X==cache['info']['X'];assert not res['no_g_end']
 es={edge((x,n-1-y),(x+MOVES[int(v)][1],n-1-y-MOVES[int(v)][0])) for y,row in enumerate(grid) for x,code in enumerate(row) for v in code}
 own=defaultdict(list)
 for e in es:
  for q in qs(e):own[q].append(e)
 dep=lambda x,y:min(x,y,n-2-x,n-2-y)
 deepbad={(x,y,k) for x in range(5,n-6) for y in range(5,n-6) for k in range(4) if len(own[x,y,k])!=1}
 selected=0
 for fx,fy,r in cache['cs']:
  pp=[(n-2-x if fx else x,n-2-y if fy else y) for x,y in [(r,j) for j in range(1,r+1)]+[(i,r) for i in range(r-1,0,-1)]]
  selected+=min(2,sum((x,y,k) in deepbad for x,y in pp for k in range(4)))
 bqx=len(deepbad)-selected;t=res['total'];c5=2*(t['G_free']+t['N_free2'])+bqx
 z={'file':file,'n':n,'X':X,'G_free':t['G_free'],'N_free':t['N_free2'],'BQdeep':len(deepbad),'selected_deep':selected,'BQx':bqx,'C5':c5,'C5_minus_4n':c5-4*n,'ratio':c5/n,'lost':res['lost'],'deficient':res['deficient'],'sides':res['sides'],'seconds':time.monotonic()-start}
 out.append(z);Path('gap/verifier/claim45_scan.json').write_text(json.dumps(out,indent=1));print(z,flush=True)
