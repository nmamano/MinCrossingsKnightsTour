import sys, json, time
from lib import *
import search2
from verify import check
from pairs import pairing
from filt import bl_pass, mid_pass, L3ODD, L5EVEN
LEFT = {'L3odd': L3ODD, 'L5even': L5EVEN}
cfgs = json.loads(sys.argv[1])
for c in cfgs:
    kind = c.get('kind', 'bottom'); st = Strip(kind, c['P'], c['D'], s=1)
    rule = (c['rule'][0], set(map(tuple, c['rule'][1]))) if c.get('rule') else None
    left = LEFT[c['vs']]
    print('==', c, flush=True)
    hint = None
    if c.get('hint'):
        ht = tile_bottom(c['hint'], c['P'], c['D']) if kind == 'bottom' else tile_left(c['hint'], c['P'], c['D'])
        hint = set(chosen_from_template(st, ht)); print('hint eval', st.evaluate(hint), flush=True)
    r = search2.solve_filtered(st, rule, (lambda t: bl_pass(t, left)) if kind == 'bottom' else (lambda t: mid_pass(t, left)), time_limit=c.get('tl', 60), max_iter=c.get('it', 15), pi=c.get('pi'), hint=hint,
                               log=lambda s: print(s, flush=True))
    out = dict(kind=kind, P=c['P'], D=c['D'], rule=c.get('name', 'filtered') + (' pi=%d' % c['pi'] if 'pi' in c else ''), vs=c['vs'], status=r['status'], stamp=time.strftime('%Y-%m-%d %H:%M'))
    if 'tpl' in r:
        ck = check(kind, r['tpl'], s=10**6); pr, cper = pairing(kind, r['tpl'])
        out.update(X=r['X'], T=r['T'], bound=r['bound'], rate=r['X'] / c['P'], tpl=r['tpl'], pairing=pr, cper=cper,
                   check=dict(paths_ok=not ck['bad'] and ck['uncovered'] == 0, X=ck['X_per_period']),
                   accept={str(k): v for k, v in r['accept'].items()})
    print(json.dumps(out), flush=True)
    with open('menu_results.jsonl', 'a') as f: f.write(json.dumps(out) + '\n')
