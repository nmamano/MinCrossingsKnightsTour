"""Exact (reachable-family) band.cpp rates for a kind at width W, seeded with a CP-SAT template of width w
extended by plain field cells (KT Edge Searcher, 2026-10-02).
usage: run_ext.py kind p w rel W  (template from band_cps.jsonl: OPTIMAL row with this kind/p/w1/rel)"""
import json, sys, subprocess, time
from extend import extend
from tpl2edges import convert
from band_gen import KINDS, gen
kind, p, w, rel, W = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])
k = KINDS[kind]
row = None
for l in open('band_cps.jsonl'):
    r = json.loads(l)
    if r['kind'] == kind and r['p'] == p and r['w1'] == w and r.get('rel') == rel and r['status'] == 'OPTIMAL' and 'cells' in r: row = r
assert row, 'no template'
if kind == 'diagfree': T = (p, p)
else: T = (0, p)
cells = extend(row['cells'], T, k['hv'], w, W, k['f1'], k['f2'])
fb = 'xb_%s_p%d_w%d_r%d_W%d.txt' % (kind, p, w, rel, W); fi = 'xi_%s_W%d.txt' % (kind, W)
convert(cells, T, k['sv'], k['hv'], W, fb)
gen(fi, k['hv'], W, 0 if k.get('wall') else W, k['f1'], k['f2'], k['sv'], k['t0'], k.get('u', 1))
t = time.time()
pr = subprocess.run(['./band2', fi, 'none', '30000000'], env={'BASE': fb, 'NOCOREACH': '1', 'CURHIST': '1'}, capture_output=True, text=True)
out = dict(kind=kind, tpl=[p, w, rel, row['X']], W=W, stamp=time.strftime('%Y-%m-%d %H:%M'), secs=round(time.time() - t),
           log=[x for x in pr.stderr.splitlines() if 'q=' not in x])
try:
    j = json.loads(pr.stdout); out.update({a: j[a] for a in ('status', 'states', 'core', 'cycle_len', 'cost', 'rate_per_unit')}); out['edges'] = j['edges']
except Exception: out['stdout'] = pr.stdout[:300]
print(json.dumps({a: b for a, b in out.items() if a != 'edges'}), flush=True)
with open('band_ext.jsonl', 'a') as f: f.write(json.dumps(out) + '\n')
