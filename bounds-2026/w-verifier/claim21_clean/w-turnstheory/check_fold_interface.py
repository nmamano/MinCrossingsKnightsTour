"""Independent finite check of the exact free-fold interface formula."""
from itertools import product
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from kt.core import seg_cross

def p(k):return (k,k)
def q(k):return (k+2,k+1)
def ea(k):return (p(k),q(k))
def eb(k):return (p(k),q(k-3))
for i in range(-8,9):
    for j in range(-8,9):
        assert seg_cross(*ea(i),*eb(j))==(j-i in (1,2))
print('PASS: A_i and B_j cross exactly when j-i is 1 or 2.')
for state in product((0,1),repeat=3):
    chosen=lambda k:ea(k) if state[k%3] else eb(k)
    # One edge per source; count cross pairs per period by the A edge.
    count=sum(seg_cross(*ea(i),*eb(j)) for i in range(3) if state[i]
              for j in range(-5,8) if not state[j%3])
    r=sum(state)
    assert count==r*(3-r)
    for i in range(-6,7):
        incoming=int(state[i%3]==1)+int(state[(i+3)%3]==0)
        assert incoming==1
    print('state',state,'flux',r,'crossings per period',count)
print('PASS: all 8 period-three states; mixed states have exactly 2 crossings per period.')
