from pathlib import Path
import sys
from collections import Counter
sys.path[:0]=[str(Path(__file__).resolve().parents[1]),str(Path(__file__).resolve().parents[1]/'w-lowerbounds')]
from fold_complete2 import base
for n in (48,96):
    E,deg=base(n)
    print(n,'degrees',dict(sorted(Counter(deg[x,y] for x in range(n) for y in range(n)).items())))
    print('isolated',[(x,y) for x in range(n) for y in range(n) if deg[x,y]==0])
