"""Run a list of configs sequentially; append one JSON line per run to results.jsonl.
usage: python driver.py '<json list of run() kwargs>' """
import sys, json, time
from lib import *
from verify import check
cfgs = json.loads(sys.argv[1])
for c in cfgs:
    h = c.pop('hint', None)
    if h == 'H16a':
        c['hint_tpl'] = tile_bottom(H16a, c['P'], c['D'])
    elif h == 'VE':
        c['hint_tpl'] = tile_left(VE, c['P'], c['D'])
    elif h:
        c['hint_tpl'] = h
    t0 = time.time()
    r = run(**c)
    if 'tpl' in r:
        r['check'] = check(r['kind'], r['tpl'], s=r['s'], off=r['off'])
    r['stamp'] = time.strftime('%Y-%m-%d %H:%M')
    print(json.dumps(r), flush=True)
    with open('results.jsonl', 'a') as f:
        f.write(json.dumps(r) + '\n')
