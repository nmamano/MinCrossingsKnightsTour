"""Independent exhaustive check of the local inequalities; no solver required."""
from itertools import combinations
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))

moves=[(dx,dy) for dx in (-2,-1,1,2) for dy in (-2,-1,1,2) if abs(dx)+abs(dy)==3]
count=0
for x in range(4):
    for a,b in combinations([d for d in moves if x+d[0]>=0],2):
        turn=int(a[0]+b[0]!=0 or a[1]+b[1]!=0)
        if x==0:
            lower=1
        elif x in (1,2):
            p=sum(x+d[0] in (0,3) for d in (a,b))
            lower=p-1
        else:
            q=sum(x+d[0] in (1,2) for d in (a,b))
            lower=1-q
        assert turn>=lower,(x,a,b,turn,lower)
        count+=1
print(f'PASS: all {count} allowed pairs satisfy the local inequalities.')

from kt.gentour import gen_tour
from kt.core import validate, neighbors, num_turns
for n in (16,24,40,80):
    t=gen_tour(n,n)
    assert validate(t)
    turning={(i,j) for i in range(n) for j in range(n)
             if tuple(map(sum,zip(*[(a-i,b-j) for a,b in neighbors(t,i,j)])))!=(0,0)}
    strips=[sum(j<4 for i,j in turning),sum(j>=n-4 for i,j in turning),
            sum(i<4 for i,j in turning),sum(i>=n-4 for i,j in turning)]
    assert min(strips)>=2*n
    assert len(turning)==num_turns(t)
    assert len(turning)>=8*n-64
    print(f'PASS: n={n}, turns={len(turning)}, side-strip counts={strips}.')
