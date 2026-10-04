#!/usr/bin/env python3
"""Regression tests for allsize_check.py (KT Integrator, 2026-10-04), from the Claim 55 adversarial cases
(gap/verifier/claim55_adversarial.py), run on copies in a temporary directory.
Expected: every bad input is rejected (nonzero exit); TT16 and its period-16 relabelling pass with -14."""
import json, shutil, subprocess, sys, tempfile, importlib.util
from pathlib import Path

HERE = Path(__file__).resolve().parent; ROOT = HERE.parent
CHK = HERE / 'allsize_check.py'
spec = importlib.util.spec_from_file_location('chk', CHK); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
tmp = Path(tempfile.mkdtemp(prefix='allsize_regress_'))

def copy(name):
    dst = tmp / name
    shutil.copytree(HERE / 'pipeline' / 'selftest_TT16', dst); return dst

def run(d):
    r = subprocess.run([sys.executable, str(CHK), str(d)], capture_output=True, text=True)
    return r.returncode, ('PASS: T(n)' in r.stdout), (r.stdout + r.stderr).strip().splitlines()[-1][:150]

cases = []
# 1. wrong-size fallback (Claim 55 blocking defect): off-board override at n=48 plus a 16x16 tour labelled n=48
d1 = copy('bad_fallback_size'); f = d1 / 'res00.json'; d = json.loads(f.read_text())
g = m.graph(d, 56); d['zones']['BL:48,0'] = [[v[0] - 48, v[1]] for v in g[48, 0]]; f.write_text(json.dumps(d))
small = json.loads((ROOT / 'gap/verifier/claim34_tour_n16.json').read_text()); small['n'] = 48
(d1 / 'tours' / 'selftest_TT16_n48.json').write_text(json.dumps(small))
cases.append(('bad_fallback_size', d1, False))
d2 = copy('bad_no_fallback'); (d2 / 'res00.json').write_text(f.read_text())
(d2 / 'tours' / 'selftest_TT16_n48.json').unlink(); cases.append(('bad_no_fallback', d2, False))
d2b = copy('good_genuine_fallback'); (d2b / 'res00.json').write_text(f.read_text())   # real 48x48 tour file covers n=48
cases.append(('good_genuine_fallback', d2b, True))
d3 = copy('bad_missing_residue'); (d3 / 'res06.json').unlink(); cases.append(('bad_missing_residue', d3, False))
d4 = copy('bad_phase'); f4 = d4 / 'res00.json'; d = json.loads(f4.read_text()); d['phases'][0] += 1; f4.write_text(json.dumps(d))
cases.append(('bad_phase', d4, False))
d5 = copy('bad_move'); f5 = d5 / 'res00.json'; d = json.loads(f5.read_text()); d['zones']['BL:0,0'] = [[0, 0], [1, 2]]
f5.write_text(json.dumps(d)); cases.append(('bad_move', d5, False))
# 6. zone shape that misses its band overlap cell (BL:0,0 removed from every residue file)
d6 = copy('bad_overlap')
for f6 in d6.glob('res*.json'):
    d = json.loads(f6.read_text()); d['zones'].pop('BL:0,0'); f6.write_text(json.dumps(d))
cases.append(('bad_overlap', d6, False))
d9 = copy('bad_interior')
for f9 in d9.glob('res*.json'):
    d = json.loads(f9.read_text()); d['interior'] = 'mixed 15/37 period 5'; f9.write_text(json.dumps(d))
cases.append(('bad_interior', d9, False))
d7 = copy('good_TT16'); cases.append(('good_TT16', d7, True))
d8 = copy('good_period16')
for f8 in d8.glob('res*.json'):
    d = json.loads(f8.read_text())
    for side in ('bottom', 'top'): d[side] = [row + ' ' + row for row in d[side]]
    f8.write_text(json.dumps(d))
cases.append(('good_period16', d8, True))
ok = True
for name, path, want in cases:
    code, passed, last = run(path)
    good = (passed and code == 0) if want else (code != 0 and not passed)
    ok &= good
    print(f'{"OK  " if good else "BAD "} {name}: exit {code}, {"PASS" if passed else "REJECT"} | {last}', flush=True)
shutil.rmtree(tmp)
print('ALL REGRESSION TESTS OK' if ok else 'REGRESSION FAILURE'); sys.exit(0 if ok else 1)
