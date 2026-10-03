"""Count edge pairs per period in an infinite strip with straight continuations."""
import json
from pathlib import Path
from check import MOVES,proper

def count(template,kind):
    cells=[r.split() for r in template];h=len(cells);w=len(cells[0]);edges=set()
    if kind=='bottom':
        domain=((r,c) for r in range(-8,h) for c in range(-8,w+8));axis=1;period=w
    else:
        domain=((r,c) for r in range(-8,h+8) for c in range(0,w+8));axis=0;period=h
    for r,c in domain:
        s=(cells[r][c%w] if r>=0 else '26') if kind=='bottom' else (cells[r%h][c] if c<w else '26')
        for k in s:
            di,dj=MOVES[int(k)];q=(r+di,c+dj)
            assert q[0]<h if kind=='bottom' else q[1]>=0
            edges.add(tuple(sorted(((r,c),q))))
    edges=sorted(edges);x=0
    for i,e in enumerate(edges):
        for f in edges[:i]:
            # Assign each pair to the period of its smallest longitudinal endpoint.
            if 0<=min(p[axis] for p in e+f)<period and proper(e,f): x+=1
    return x

if __name__=='__main__':
    for fam in ['H16a','H16b']:
        d=json.loads(next(Path('w-integrator/tours').glob(fam+'*.json')).read_text())
        print(fam,'bottom crossings per 8 columns:',count(d['bottom'],'bottom'))
        print(fam,'left crossings per 4 rows:',count(d['left'],'left'))
