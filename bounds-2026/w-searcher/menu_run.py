import sys, json, time
from lib import *
import search2
from verify import check
from pairs import pairing
def go(kind, P, D, rule=None, rname='free', tl=60, hint=None):
    st = Strip(kind, P, D, s=1)
    r = search2.solve(st, rule=rule, time_limit=tl, hint=hint)
    out = dict(kind=kind, P=P, D=D, rule=rname, status=r['status'], time=r['time'])
    if 'chosen' in r:
        tpl = search.to_template(st, r['chosen'])
        c = check(kind, tpl, s=10**6)   # s huge: lane check meaningless here; we use ok-ness of paths
        pr, cper = pairing(kind, tpl)
        out.update(X=r['X'], T=r['T'], bound=r['bound'], rate=r['X'] / P, tpl=tpl,
                   check=dict(paths_ok=not c['bad'] and c['uncovered'] == 0, X=c['X_per_period']), pairing=pr, cper=cper)
    out['stamp'] = time.strftime('%Y-%m-%d %H:%M')
    with open('menu_results.jsonl', 'a') as f: f.write(json.dumps(out) + '\n')
    print(json.dumps({k: out.get(k) for k in ('kind', 'P', 'D', 'rule', 'status', 'X', 'bound', 'rate', 'pairing', 'check', 'time')}), flush=True)
    return out
if __name__ == '__main__':
    for c in json.loads(sys.argv[1]):
        rule = c.pop('rule', None)
        if rule: c['rule'] = (rule[0], set(map(tuple, rule[1]))); c.setdefault('rname', 'M%d:%s' % (rule[0], ','.join('%d/%d' % tuple(a) for a in rule[1])))
        go(**c)
