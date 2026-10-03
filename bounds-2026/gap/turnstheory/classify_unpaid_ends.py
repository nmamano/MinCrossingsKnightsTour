"""Exact geometric types of S-minus-B double-quarter pairs at end squares."""
import sys,json
sys.dont_write_bytecode=True
from pathlib import Path
from itertools import combinations
from collections import Counter
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'w-turnstheory'))
from check_knight_tiles import microtiles,cross
moves=[(dx,dy) for dx in (-2,-1,1,2) for dy in (-2,-1,1,2) if abs(dx)+abs(dy)==3]
es=sorted({tuple(sorted(((x,y),(x+dx,y+dy)))) for x in (0,1) for y in range(-4,5) for dx,dy in moves if x+dx>=0})
tiles={e:microtiles(e) for e in es};types=[]
for e,f in combinations(es,2):
 if any(p[0]==0 for p in e) and any(p[0]==0 for p in f):continue
 qs=tiles[e]&tiles[f]
 if len(qs)!=2:continue
 if not any(y==0 and x>=1 for x,y,k in qs):continue
 assert cross(e,f)
 types.append(dict(edges=[e,f],overlap=sorted(qs)))
print('types:',len(types))
for t in types:print(json.dumps(t))
(ROOT/'gap/turnstheory/unpaid_end_types.json').write_text(json.dumps(types,indent=2)+'\n')
