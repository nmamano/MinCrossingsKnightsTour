#!/usr/bin/env python3
"""Check the exact per-bad-row potential used in PROOF_crossings_lower.md."""
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
import re
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'w-lowerbounds'))
import endpoint_independent as endpoint

def main():
    out=StringIO()
    sys.argv=['endpoint_independent.py','both','1','1']
    with redirect_stdout(out): endpoint.main()
    log=out.getvalue();print(log,end='')
    assert 'both beta=1/1: converged' in log and 'no negative cycle' in log
    m=re.search(r'range (-?\d+)\.\.(-?\d+) \(units 1/\(4q\)\)',log)
    assert m and tuple(map(int,m.groups()))==(-29,0),log
    print('PASS: exact endpoint error 29/4, coefficient 1 per failed joint endpoint test.')
    cells={(x,y) for x in range(4) for y in range(4)}
    edges={(a,b) for a in cells for b in cells if a<b
           and sorted((abs(a[0]-b[0]),abs(a[1]-b[1])))==[1,2]}
    assert len(edges)==24 and 4*(24*23//2)==1104
    print('PASS: 24 knight edges per 4-by-4 corner; strip overcount at most 1104.')

if __name__=='__main__':main()
