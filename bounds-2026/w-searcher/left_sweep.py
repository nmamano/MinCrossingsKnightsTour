import json, time, sys
from lib import *
from verify import check
Qs = json.loads(sys.argv[1]); Ds = json.loads(sys.argv[2]); TL = float(sys.argv[3])
for Q in Qs:
  for off in (0, 1):
    for D in Ds:
        r = run('left', Q, D, off=off, time_limit=TL, workers=1)
        if 'tpl' in r: r['check'] = check('left', r['tpl'], off=off)
        r['stamp'] = time.strftime('%Y-%m-%d %H:%M')
        with open('results_left.jsonl', 'a') as f: f.write(json.dumps(r) + '\n')
        print(Q, off, D, {k: r.get(k) for k in ('status', 'time', 'obj', 'bound', 'X', 'T')},
              'rate/row', r.get('X') and round(r['X'] / Q, 3), 'check', r.get('check') and (r['check']['ok'], r['check']['X_per_period']), flush=True)
