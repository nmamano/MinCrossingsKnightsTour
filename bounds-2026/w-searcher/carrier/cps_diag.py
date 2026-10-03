"""CP-SAT templates for the diagonal free-fold carrier, using KT Structures' model (diag_tpl.template)."""
import sys, json, time
sys.path.insert(0, '/home/nil/nil/knight-formation-research/w-structures')
from diag_tpl import template
out = {}
for spec in sys.argv[1:]:
    p, w, tgt, tl = map(int, spec.split(':'))
    st, ev, cells = template(p, w, tgt, tl)
    r = dict(p=p, w=w, current=tgt, status=st, X=ev[0], T=ev[1], rate_per_unit=ev[0] / p, cells=cells, stamp=time.strftime('%Y-%m-%d %H:%M'))
    print(json.dumps({k: v for k, v in r.items() if k != 'cells'}), flush=True)
    with open('diag_cps.jsonl', 'a') as f: f.write(json.dumps(r) + '\n')
