# KT Structures, 2026-10-03. All same-side chords: clean (all interior vertices good points), end field signs (+1 '/'-H, -1 '\'-H),
# port steepness (|dx| of the port edge), shift parity s = c'_up - c_low (chevron type only). Usage: python chord_census.py tour.json
import sys, json; sys.path.insert(0,'.')
import fold_exact_scan as F
from collections import defaultdict, Counter
from pathlib import Path
f=sys.argv[1]; r=F.run(f)
grid=json.loads(Path(f).read_text())['tour']; n=len(grid)
E={F.edge((x,n-1-y),(x+F.MOVES[int(v)][1],n-1-y-F.MOVES[int(v)][0])) for y,row in enumerate(grid) for x,code in enumerate(row) for v in code}
adj=defaultdict(set); own=defaultdict(int)
for a,b in E:
    adj[a].add(b); adj[b].add(a)
    for x,y,k in F.templates[b[0]-a[0],b[1]-a[1]]: own[x+a[0],y+a[1],k]+=1
gs=lambda i,j: all(own[i,j,k]==1 for k in range(4))
gp=lambda v: all(gs(v[0]+dx,v[1]+dy) for dx in(-1,0) for dy in(-1,0))
T=[lambda v:v,lambda v:(n-1-v[0],v[1]),lambda v:(v[1],v[0]),lambda v:(n-1-v[1],v[0])]
inside=lambda v: all(3<=z<=n-4 for z in v)
cheap=[set() for _ in range(4)]
# recompute cheap slot sets as in F.run (side frames)
import fold_exact_scan
done=set(); stats=Counter(); rows=[]
for a,b in E:
    if inside(a)==inside(b): continue
    outer,inner=(b,a) if inside(a) else (a,b)
    if (outer,inner) in done: continue
    prev,cur=outer,inner; path=[outer,inner]
    while inside(cur):
        nx=next(v for v in adj[cur] if v!=prev); prev,cur=cur,nx; path.append(cur)
    done.add((outer,inner)); done.add((cur,prev))
    s1=[i for i,t in enumerate(T) if t(outer)[0]<3]; s2=[i for i,t in enumerate(T) if t(cur)[0]<3]
    if len(s1)!=1 or s1!=s2: continue
    si=s1[0]; L=T[si]
    clean=all(gp(v) for v in path[1:-1])
    ends=[]
    for o,q in ((path[0],path[1]),(path[-1],path[-2])):
        o,q=L(o),L(q); d=(q[0]-o[0],q[1]-o[1])
        sgn=1 if d[0]*d[1]>0 else -1
        ends.append((q[1],sgn,abs(d[0]),q))
    ends.sort(); (_,s_lo,w_lo,q_lo),(_,s_up,w_up,q_up)=ends
    sh=None
    if (s_lo,s_up)==(1,-1) and w_lo==w_up==2: sh=(q_up[0]+2*q_up[1])-(q_lo[0]-2*q_lo[1])
    if (s_lo,s_up)==(-1,1) and w_lo==w_up==2: sh=(q_lo[0]+2*q_lo[1])-(q_up[0]-2*q_up[1])
    key=(clean,(s_lo,s_up),(w_lo,w_up), None if sh is None else sh%2)
    stats[key]+=1
    if clean and len(path)>12: rows.append((si,q_lo[1],q_up[1],len(path)-2,sh))
print(Path(f).name,'n',n)
for k,v in sorted(stats.items(),key=lambda kv:-kv[1]): print('  clean=%s ends=%s steep=%s shiftparity=%s : %d'%(k+(v,)))
print('  long clean returns (side, low row, up row, len, shift):',len(rows)); 
for x in sorted(rows)[:6]+sorted(rows)[-3:]: print('   ',x)
