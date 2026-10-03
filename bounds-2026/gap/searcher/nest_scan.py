import json, sys
from nest_test import build, components
n = int(sys.argv[1])
for cur in (-1, 0):
    tpl = [d for d in map(json.loads, open('eB4.jsonl')) if d.get('rate_per_row') == '11/6' and d['current'] == cur][0]
    for ph in range(6):
        E = build(n, ph, ph, tpl)
        comps, adj = components(n, E)
        h = n // 2
        cyc = [c for ok, c in comps if ok]
        # classify: TL cycles = all cells x < h and touching the left edge band
        tl = [c for c in cyc if max(p[0] for p in c) < h and min(p[0] for p in c) <= 3]
        bot = [c for c in cyc if min(p[1] for p in c) <= 1 and min(p[0] for p in c) > 3]
        cells_tl = sum(len(c) for c in tl)
        print(f'cur={cur} phase={ph}: cycles {len(cyc)}, TL-nest cycles {len(tl)} ({cells_tl} cells), bottom-nest cycles {len(bot)}')
