#!/usr/bin/env python3
"""Reproduce finite inputs for PROOF_52_11.md, one process at a time.

--reuse-stability-logs uses the two logs from this work session rather
than repeating the two largest checks. Default mode reruns every check.
"""
import argparse
from fractions import Fraction
import json
import os
from pathlib import Path
import re
import subprocess
import sys

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--reuse-stability-logs',action='store_true')
    args=parser.parse_args()
    env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1')
    results=[]
    small=[
        ('tile_geometry','w-turnstheory/check_knight_tiles.py'),
        ('endpoint_flux','w-turnstheory/check_corner_box.py'),
        ('boundary_overlap','w-turnstheory/check_col0_squares.py'),
        ('square_defects','w-turnstheory/check_square_defects.py'),
        ('endpoint_loss','w-turnstheory/check_endpoint_loss.py'),
        ('boundary_credit','gap/turnstheory/check_boundary_credit.py'),
    ]
    for name,path in small:
        result=subprocess.run([sys.executable,str(ROOT/path)],cwd=ROOT,
                              env=env,text=True,capture_output=True,check=True)
        assert 'PASS:' in result.stdout,(name,result.stdout)
        (HERE/f'check_52_11_{name}.log').write_text(result.stdout+result.stderr)
        results.append(dict(check=name,status='passed',reused=False))
        print('PASS:',name,flush=True)
    for orient,lower,nodes,arcs in [('up',-155,188112,338200),('down',-159,335564,630778)]:
        path=HERE/f'r1_{orient}_check.log'
        if args.reuse_stability_logs:
            output=path.read_text()
        else:
            result=subprocess.run([sys.executable,str(ROOT/'gap/lowerbounds/r1_independent.py'),
                                   orient,'4','3'],cwd=ROOT,env=env,text=True,
                                  capture_output=True,check=True)
            output=result.stdout+result.stderr
            path.write_text(output)
        assert 'base states 82516 arcs 144674 (w recomputed and matched)' in output
        assert f'augmented nodes {nodes} arcs {arcs}' in output
        assert re.search(rf'{orient} beta=4/3: converged after \d+ passes, no negative cycle; '
                         rf'potential range {lower}\.\.0 \(units 1/\(4q\)\)',output),output
        results.append(dict(check=f'stability_{orient}',status='passed',
                            reused=args.reuse_stability_logs,potential_range=[lower,0],
                            potential_denominator=12))
        print('PASS: stability',orient,'(existing log)' if args.reuse_stability_logs else '',flush=True)
    cells={(x,y) for x in range(4) for y in range(4)}
    edges={(a,b) for a in cells for b in cells if a<b
           and sorted((abs(a[0]-b[0]),abs(a[1]-b[1])))==[1,2]}
    assert len(edges)==24
    strip_overlap=4*(24*23//2)
    assert strip_overlap==1104
    boundary_overlap=20
    area_error=2*(boundary_overlap-2)
    path_error=2*60+area_error
    certificate_error=8*Fraction(159,12)
    stability_error=strip_overlap-2+certificate_error
    coefficient_E=4+2/Fraction(4,3)
    total_error=path_error+2*stability_error/Fraction(4,3)
    coefficient_X=4+4/coefficient_E
    constant_X=2+total_error/coefficient_E
    assert (path_error,certificate_error,stability_error)==(156,106,1208)
    assert coefficient_E==Fraction(11,2) and total_error==1968
    assert coefficient_X==Fraction(52,11) and constant_X==Fraction(3958,11)<360
    assert coefficient_X-Fraction(14,3)==Fraction(2,33)
    report=dict(date='2026-10-03',status='finite checks passed; all-size proof audited PASS in Claim 26',
                checks=results,coefficient=str(coefficient_X),exact_subtracted_constant=str(constant_X),
                rounded_subtracted_constant=360)
    (HERE/'check_52_11_report.json').write_text(json.dumps(report,indent=2)+'\n')
    print('PASS: exact constants; audited X >= 52n/11 - 360 (Claim 26).')

if __name__=='__main__':
    main()
