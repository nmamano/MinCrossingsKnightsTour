"""Union of two periodic line matchings: count finite cycles in a window (0 = only paths)."""
def expand(pairs, cper, lo, hi):
    m = {}
    for a, d in pairs:
        for k in range((lo - 40) // cper - 1, hi // cper + 2):
            x, y = a + k * cper, a + d + k * cper
            m[x] = y; m[y] = x
    return m
def union_cycles(p1, c1, p2, c2, lo=0, hi=600):
    m1, m2 = expand(p1, c1, lo - 50, hi + 50), expand(p2, c2, lo - 50, hi + 50)
    seen = set(); cyc = []
    for s in range(lo + 50, hi - 50):
        if s in seen: continue
        cur, via, path = s, 1, [s]
        while True:
            nxt = (m1 if via == 1 else m2)[cur]
            via = 3 - via
            if nxt == s: cyc.append(len(path)); break
            if nxt < lo or nxt > hi or len(path) > 400: break
            path.append(nxt); cur = nxt
        seen.update(path)
    return cyc
if __name__ == '__main__':
    L3odd = ([(1, 3)], 2); L1even = ([(0, 1)], 2)
    B6 = ([(3, 3), (4, 3), (5, 3)], 6)
    print('L3odd+L1even', union_cycles(*L3odd, *L1even)[:5])
    print('L1even+B6', union_cycles(*L1even, *B6)[:5])
    print('L3odd+B6', union_cycles(*L3odd, *B6)[:5])
