"""Exact small locality check for the quarter-payment hand lemma."""
import sys
from pathlib import Path
sys.dont_write_bytecode=True
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'w-turnstheory'))
from check_knight_tiles import microtiles
maximum=0
count=0
for dx,dy in ((1,2),(1,-2),(2,1),(2,-1)):
    e=((0,0),(dx,dy))
    for x,y,k in microtiles(e):
        for u,v in e:
            dist=max(abs(2*u-(2*x+1)),abs(2*v-(2*y+1)))
            assert dist<=3
            maximum=max(maximum,dist)
        count+=1
assert count==16 and maximum==3
print('PASS: four undirected move types, 16 covered quarters; all endpoints within 3/2 of each square centre.')
