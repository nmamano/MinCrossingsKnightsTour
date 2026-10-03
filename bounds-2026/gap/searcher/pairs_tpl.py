"""Line pairing of an edgeB template: which (1,2)-lines (index c = 2x - y) a band strand joins."""
import json, sys
from collections import defaultdict
for d in map(json.loads, open(sys.argv[1])):
    if d.get('rate_per_row') != sys.argv[2]: continue
    R, W = d['rows'], d['W']
    E = set()
    for k in range(-6, 12):
        for a0, b0, a1, b1 in d['edges']:
            E.add(((a0, b0 + k * R), (a1, b1 + k * R)))
    # forced edges: band cell (W-1, y) -> (W, y+2) (field (1,2))
    adj = defaultdict(list)
    for a, b in E: adj[a].append(b); adj[b].append(a)
    res = {}
    for y in range(0, R):
        start = (W - 1, y)   # its forced edge goes out to (W, y+2): line index c = 2(W-1) - y
        # walk inside band from start (the forced edge is the entry)
        prev, cur = None, start
        while True:
            nx = [v for v in adj[cur] if v != prev]
            if cur != start and cur[0] == W - 1 and len(adj[cur]) == 1:
                break
            if not nx: break
            prev, cur = cur, nx[0]
        c1 = 2 * (W - 1) - start[1]; c2 = 2 * (W - 1) - cur[1]
        res[y] = (c1, c2, c2 - c1)
    print(d['current'], R, [res[y][2] for y in range(R)])
