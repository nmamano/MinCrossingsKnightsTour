"""menu_results.jsonl -> menuN.json (cheapest gadget per (kind, rule)) + gadgets/*.json"""
import json, sys
rows = [json.loads(l) for l in open('../w-searcher/menu_results.jsonl')]
best = {}
for r in rows:
    if r.get('status') not in ('OPTIMAL', 'FEASIBLE') or not r.get('check', {}).get('paths_ok', True): continue
    if r['rule'].startswith('lane s=4 o=') and r['rule'][-1] in '246': continue   # shifts of o=0
    per = len(r['tpl'][0].split()) if r['kind'] == 'bottom' else len(r['tpl'])
    name = f"{r['kind'][0]}_{r['rule'].replace(' ', '').replace('=', '').replace('%', 'm')}"
    k = (r['kind'], r['rule'])
    if k not in best or r['X'] / per < best[k]['X'] / best[k]['per'] - 1e-9:
        best[k] = dict(name=name, kind=r['kind'], tpl=r['tpl'], X=r['X'], T=r.get('T'), status=r['status'], per=per)
menu = list(best.values())
json.dump(menu, open(sys.argv[1], 'w'), indent=0)
for g in menu:
    json.dump(g['tpl'], open(f"gadgets/{g['name']}.json", 'w'))
    print(f"{g['name']:32} {g['X'] / g['per']:.3f} {g['status']}")
