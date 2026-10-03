import random, subprocess, sys, gen
random.seed(int(sys.argv[1]) if len(sys.argv) > 1 else 1)
bad = 0
PR = float(sys.argv[2]) if len(sys.argv) > 2 else 0.2
for it in range(40):
    w, h = random.randint(3, 6), random.randint(3, 6)
    cells = [(x, y) for x in range(w) for y in range(h)]
    req = {c: (2 if random.random() < PR else 1) for c in cells}
    E = gen.knight_edges(cells, lambda p, q: True)
    edges = []
    for p, q in E:
        r = random.random()
        fl = 1 if r < 0.03 else 2 if r < 0.08 else 4 if r < 0.12 else 0
        edges.append((p, q, fl, random.choice([0, 0, 1, -1])))
    gen.write('/tmp/rt.txt', cells, req, edges)
    a = subprocess.run(['python3', 'brute.py', '/tmp/rt.txt'], capture_output=True, text=True, timeout=600).stdout.strip()
    b = subprocess.run([sys.argv[3] if len(sys.argv) > 3 else './certify', '/tmp/rt.txt'], capture_output=True, text=True).stdout
    import json
    bs = sorted(int(k) for k in json.loads(b)['feasible'])
    ok = str(bs) == a
    bad += not ok
    print(it, w, h, len(edges), a, bs, 'OK' if ok else 'MISMATCH', flush=True)
print('mismatches', bad)
