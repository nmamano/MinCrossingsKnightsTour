import sys, json
from verify import unroll, check
from collections import Counter
def strands(kind, tpl, K=10):
    adj, band, P, D = unroll(kind, tpl, K)
    along = (lambda u: u[0]) if kind == 'bottom' else (lambda u: u[1])
    depth = (lambda u: u[1]) if kind == 'bottom' else (lambda u: u[0])
    out = []
    for t in sorted(u for u in band if 3 * P <= along(u) < 4 * P and any(depth(v) >= D for v in adj[u])):
        prev = next(v for v in adj[t] if depth(v) >= D); cur = t; n = 0
        while True:
            nx = [v for v in adj[cur] if v != prev]
            prev, cur = cur, nx[0]; n += 1
            if depth(cur) >= D or n > 1000: break
        e = prev
        out.append((t[0] + 2 * t[1], e[0] + 2 * e[1], n))
    return out
if __name__ == '__main__':
    tpl = json.loads(sys.argv[2]); kind = sys.argv[1]
    st = strands(kind, tpl)
    print('line pairs (c_start, c_end, len):', st)
    print('offsets c_end - c_start:', Counter(b - a for a, b, n in st))
