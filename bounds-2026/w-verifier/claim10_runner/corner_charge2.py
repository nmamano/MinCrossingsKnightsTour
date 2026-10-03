"""Independent re-implementation of the corner charge (no shared code with corner_charge.py or
strip_dp.py). Exact rational arithmetic. For each corner option, Q = sum over the directed dual
segments of the path  (1/2,R+1/2) -> (1/2,1/2) -> (R+1/2,1/2) -> (R+1/2,3/2)  plus the segment
(3/2,R+1/2) -> (1/2,R+1/2)  of  phi(s) - chi(right cell of s)."""
from fractions import Fraction as Fr
import itertools

H = Fr(1, 2)


def col(c):
    return 1 if (c[0] + c[1]) % 2 == 0 else -1


def crossing_side(A, B, e):
    """If segment e properly crosses segment AB, return the endpoint of e on the left of A->B, else None."""
    (p, q) = e
    def cr(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    d1, d2 = cr(A, B, p), cr(A, B, q)
    d3, d4 = cr(p, q, A), cr(p, q, B)
    if d1 * d2 < 0 and d3 * d4 < 0:
        return p if d1 > 0 else q
    return None


def path_value(E, segs):
    tot = 0
    for A, B in segs:
        ph = 0
        for e in E:
            if abs(e[0][0] - A[0]) > 3 or abs(e[0][1] - A[1]) > 3:
                continue
            l = crossing_side(A, B, e)
            if l is not None:
                ph += col(l)
        dx, dy = B[0] - A[0], B[1] - A[1]
        mx, my = (A[0] + B[0]) / 2, (A[1] + B[1]) / 2
        rc = (int(mx + dy / 2), int(my - dx / 2))     # cell on the right of the midpoint
        assert mx + dy / 2 == rc[0] and my - dx / 2 == rc[1]
        tot += ph - col(rc)
    return tot


def left_edges(kind, y):
    s = 1 if kind == 'P' else -1
    return [((0, y), (2, y + s)), ((0, y), (1, y + 2 * s)), ((1, y), (3, y + s))]


def main():
    moves = [(a, b) for a in (-2, -1, 1, 2) for b in (-2, -1, 1, 2) if abs(a) != abs(b)]
    corner = [(0, 0), (0, 1), (0, 2), (0, 3), (1, 0), (2, 0), (3, 0)]
    for L, Bk in itertools.product('PQ', 'PQ'):
        for R in (12, 13):
            E0 = set()
            for y in range(4, R + 10):
                for a, b in left_edges(L, y):
                    if a[1] >= 0 and b[1] >= 0:
                        E0.add(frozenset((a, b)))
                for a, b in left_edges(Bk, y):
                    a2, b2 = (a[1], a[0]), (b[1], b[0])
                    if a2[0] >= 0 and b2[0] >= 0:
                        E0.add(frozenset((a2, b2)))
            pts = [(H, R + H - k) for k in range(R + 1)] + [(H + k, H) for k in range(1, R + 1)] + [(R + H, 1 + H)]
            segs = list(zip(pts, pts[1:])) + [((1 + H, R + H), (H, R + H))]
            segs = [((Fr(a[0]), Fr(a[1])), (Fr(b[0]), Fr(b[1]))) for a, b in segs]
            have = {c: sum(1 for e in E0 if c in e) for c in corner}
            choices = []
            for c in corner:
                nb = [(c[0] + dx, c[1] + dy) for dx, dy in moves if c[0] + dx >= 0 and c[1] + dy >= 0]
                k = 2 - have[c]
                choices.append([frozenset(frozenset((c, q)) for q in sub) for sub in itertools.combinations(nb, k)] if k >= 0 else [])
            values = set(); count = 0
            for pick in itertools.product(*choices):
                E = set(E0)
                for s in pick:
                    E |= s
                if any(sum(1 for e in E if c in e) != 2 for c in corner):
                    continue
                count += 1
                Ef = [tuple((Fr(p[0]), Fr(p[1])) for p in e) for e in E]
                values.add(path_value(Ef, segs) % 3)
            print(f'left={L} bottom={Bk} R={R}: {count} corner options, Q mod 3 in {sorted(values)}', flush=True)


if __name__ == '__main__':
    main()
