import json, sys
mv = {tuple(map(int, k.split(','))): [tuple(d) for d in v] for k, v in json.load(open(sys.argv[1])).items()}
seen = set(); lens = []
for s in mv:
    if s in seen: continue
    L = 0; prev = None; cur = s
    while True:
        seen.add(cur); L += 1
        nxts = [(cur[0]+d[0], cur[1]+d[1]) for d in mv[cur]]
        nx = nxts[0] if nxts[0] != prev else nxts[1]
        if L > 1 and nxts[0] == prev and nxts[1] == prev: nx = nxts[1]
        prev, cur = cur, nx
        if cur == s: break
    lens.append(L)
print('cycles', len(lens), 'lengths', sorted(lens, reverse=True)[:12])
