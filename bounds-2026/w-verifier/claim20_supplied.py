#!/usr/bin/env python3
"""Run all finite inputs to PROOF_crossings_lower.md, sequentially, without a solver."""
import json
from pathlib import Path
import subprocess
import sys
import time
HERE=Path('/home/nil/nil/knight-formation-research/w-turnstheory')
ROOT=HERE.parent
CHECKS=(
    ('Tile geometry and flux','check_knight_tiles.py'),
    ('Critical scan rows and their full edge data','check_one_row_strip.py'),
    ('One-row corner charge','check_corner_box.py'),
    ('Boundary count and full-square exclusion','check_col0_squares.py'),
    ('Two bad quarters per defective square','check_square_defects.py'),
    ('Joint endpoint strip stability','check_lower_stability.py'),
)
def main():
    results=[]
    for name,file in CHECKS:
        print('\nCHECK:',name,flush=True)
        start=time.monotonic()
        r=subprocess.run([sys.executable,str(HERE/file)],cwd=ROOT,text=True,
                         stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        print(r.stdout,end='',flush=True)
        results.append({'lemma':name,'checker':file,'exit_code':r.returncode,
                        'seconds':round(time.monotonic()-start,3),'output':r.stdout})
        if r.returncode:
            raise SystemExit(f'FAIL: {name}')
    assert 1104-2+29==1131
    assert 164+2*1131==2426
    assert 2426+12<=6*407
    (ROOT/'w-verifier/claim20_supplied_checks.json').write_text(json.dumps(results,indent=2)+'\n')
    print('\nPASS: all finite inputs and arithmetic for X >= 14n/3 - 407.')
if __name__=='__main__':main()
