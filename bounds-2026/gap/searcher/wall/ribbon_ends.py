#!/usr/bin/env python3
"""Absorbed ribbon ends and integer colour current of wall.cpp witnesses (KT Edge Searcher, 2026-10-03).
For KT Structures (their metric, G11): per witness cycle in a wall.cpp log, read the two margin columns (perfect
squares), their split and the H/V bit of each ribbon run that meets the band, and count absorbed ends per period:
  different splits on the two sides: 1 per ribbon end (each side counted);
  equal splits: 2 per ribbon whose two ends have different bits, else 0; a ribbon that crosses the band as one good
  run has no end.
Also prints the integer colour current along the band: I(Y) = sum over the vertical grid edges between consecutive
complete squares of square row Y of chi(a)(m_+ + m_- - 3g + 1) (audited omega, a = top end, chi(x,y) = (-1)^(x+y)),
and the integer flux through a dual path up each margin column per period (it steps sideways through a cost square
where the margin shifts, so it is not purely exterior flux unless it is a multiple of 3).
usage: ribbon_ends.py LOG [LOG ...]   (uses the LAST cycle printed in each lambda section = the optimal one)"""
import sys, re
from collections import defaultdict
sys.path.insert(0, __file__.rsplit('/', 2)[0])
from check_identity import tile_quarters

MOVES = [(2, 1), (-2, 1), (1, 2), (-1, 2)]
HALF = {'BR': (0, 1), 'TL': (2, 3), 'RT': (1, 2), 'LB': (3, 0)}

def parse(path):
    txt = open(path).read().splitlines()
    m = re.match(r'shear (-?\d+)/(\d+) WM=(\d+) KM=(\d+)', txt[0])
    if m: SA, SB, WM, KM = map(int, m.groups())
    else:   # older header: A=.. WM=.. KM=..
        m = re.match(r'A=(-?\d+) WM=(\d+) KM=(\d+)', txt[0]); SA, WM, KM = map(int, m.groups()); SB = 1
    secs, cur = [], None
    for ln in txt:
        if ln.startswith('== lambda'):
            cur = {'lam': ln.split()[2], 'cyc': None}; secs.append(cur)
        elif ln.startswith('  cycle:') and cur is not None:
            r = re.search(r'(\d+) rows, crossings (\d+), waste (\d+)', ln)
            cur['cyc'] = {'rows': int(r[1]), 'X': int(r[2]), 'waste': int(r[3]), 'lines': []}
        elif ln.startswith('    row ') and cur is not None and cur['cyc'] is not None:
            r = re.match(r'    row (\d+) u (-?\d+) \((\w+)\)', ln)
            es = [tuple(map(int, t)) for t in re.findall(r'\((-?\d+),(-?\d+)\)-\((-?\d+),(-?\d+)\)', ln)]
            cur['cyc']['lines'].append((int(r[1]), int(r[2]), es))
        elif ln.startswith('RESULT') and cur is not None:
            cur['result'] = ln.split('per level (E units) = ')[1].split()[0]
    return SA, SB, WM, KM, [s for s in secs if s['cyc']]

def fdiv(p, q): return p // q

def analyse(SA, SB, WM, KM, cyc, K=10):
    R = cyc['rows']
    # Old logs printed x = u + floor(SA*row/SB) (no row phase). Rebuild every edge from u: x = u + sh(ph0, row),
    # and take the row phase ph0 for which all margin squares are good (the model requires it).
    def sh(ph, y): return fdiv(SA * (ph + y), SB) - fdiv(SA * ph, SB)
    for ph0 in range(SB):
        o = analyse_ph(SA, SB, WM, KM, cyc, K, ph0, sh)
        if o['margin_not_good'] == 0: return o
    return o

def analyse_ph(SA, SB, WM, KM, cyc, K, ph0, sh):
    R = cyc['rows']
    PX = sh(ph0, R); K = max(K, 3 + 30 // R)
    period = [((u + sh(ph0, row), b), (u + sh(ph0, row) + c - a, d)) for row, u, es in cyc['lines'] for (a, b, c, d) in es]
    mod = lambda x, y: 0 <= x - sh(ph0, y) < WM
    E = set()
    for k in range(-K, K + 1):
        for (p, q) in period: E.add(((p[0] + k * PX, p[1] + k * R), (q[0] + k * PX, q[1] + k * R)))
    mult = defaultdict(int); cover = {}   # cover[(X,Y,q)] = edge
    for e in E:
        for t in tile_quarters(*e): mult[t] += 1; cover[t] = e
    ylo, yhi = -3 * R - 12, 3 * R + 12
    cls = {}   # square -> 'L' / 'R' / 'C' (cost); absent = not complete
    for Y in range(ylo, yhi):
        comp = []
        for X in range(sh(ph0, Y) - 12, sh(ph0, Y) + WM + 12):
            ok = True; any_ = False
            for x1 in range(X - 2, X + 4):
                for y1 in range(Y - 2, Y + 2):
                    for (dx, dy) in MOVES:
                        if not (min(x1, x1 + dx) <= X < max(x1, x1 + dx) and y1 <= Y < y1 + dy): continue
                        if not any(t[0] == X and t[1] == Y for t in tile_quarters((x1, y1), (x1 + dx, y1 + dy))): continue
                        any_ = True
                        if not mod(x1, y1) and not mod(x1 + dx, y1 + dy): ok = False
            if ok and any_: comp.append(X)
        assert comp == list(range(comp[0], comp[-1] + 1)), 'complete squares not an interval'
        for X in comp: cls[(X, Y)] = 'C'
        for i in range(KM): cls[(comp[i], Y)] = 'L'; cls[(comp[-1 - i], Y)] = 'R'
    good = lambda X, Y: (X, Y) in cls and all(mult[(X, Y, q)] == 1 for q in range(4))
    def split(X, Y):
        if not good(X, Y): return None
        e = cover[(X, Y, 0)]; dx = e[1][0] - e[0][0]; dy = e[1][1] - e[0][1]
        return '/' if dx * dy > 0 else '\\'
    def bit(X, Y, h):
        e = cover[(X, Y, HALF[h][0])]; return 'H' if abs(e[1][0] - e[0][0]) == 2 else 'V'
    def ribbon(X, Y, h):   # ribbon index (per split) and the two chain neighbours (X, Y, half)
        if h == 'BR': return Y - X, [(X + 1, Y, 'TL'), (X, Y - 1, 'TL')]
        if h == 'TL': return Y - X + 1, [(X - 1, Y, 'BR'), (X, Y + 1, 'BR')]
        if h == 'LB': return Y + X + 1, [(X - 1, Y, 'RT'), (X, Y - 1, 'RT')]
        return Y + X + 2, [(X + 1, Y, 'LB'), (X, Y + 1, 'LB')]
    def goodhalf(X, Y, h, sp): return good(X, Y) and split(X, Y) == sp
    # margin splits per side
    splits = {'L': set(), 'R': set()}; marg_bad = 0
    for (X, Y), c in cls.items():
        if c in 'LR' and -R <= Y < 2 * R:
            sp = split(X, Y)
            if sp is None: marg_bad += 1
            else: splits[c].add(sp)
    ends = {'L': {}, 'R': {}}   # ribbon k -> (row, bit)
    for (X, Y), c in cls.items():
        if c not in 'LR' or not (ylo + 2 <= Y < yhi - 2): continue
        sp = split(X, Y)
        if sp is None: continue
        for h in (('BR', 'TL') if sp == '/' else ('RT', 'LB')):
            k, nb = ribbon(X, Y, h)
            inner = [n for n in nb if cls.get(n[:2], 'O') not in ('O', c)]
            if not inner: continue   # ribbon runs along the margin or leaves to the exterior
            # walk into the band while the halves stay good in this split; reaching the other margin = no end
            n = inner[0]; prev = (X, Y, h); through = False
            for _ in range(200):
                if not goodhalf(*n, sp): break
                if cls[n[:2]] not in ('C', c): through = True; break
                _, nb2 = ribbon(*n); nxt = [m for m in nb2 if m != prev]; prev, n = n, nxt[0]
            if not through: ends[c][k] = (Y, bit(X, Y, h))
    out = {'R': R, 'PX': PX, 'ph0': ph0, 'X': cyc['X'], 'waste': cyc['waste'], 'splitL': ''.join(sorted(splits['L'])),
           'splitR': ''.join(sorted(splits['R'])), 'margin_not_good': marg_bad}
    inper = lambda Y: 0 <= Y < R
    if len(splits['L']) == 1 and splits['L'] != splits['R']:
        out['ends'] = sum(inper(v[0]) for v in ends['L'].values()) + sum(inper(v[0]) for v in ends['R'].values())
    elif len(splits['L']) == 1:
        cnt = 0; unpaired = 0
        for k in set(ends['L']) | set(ends['R']):
            a, b = ends['L'].get(k), ends['R'].get(k)
            row = (a or b)[0]
            if not inper(row): continue
            if a is None or b is None: unpaired += 1; continue
            cnt += 2 if a[1] != b[1] else 0
        out['ends'] = cnt; out['unpaired'] = unpaired
    else:
        out['ends'] = 'mixed margins'
    out['bitsL'] = ''.join(v[1] for k, v in sorted(ends['L'].items()) if inper(v[0]))
    out['bitsR'] = ''.join(v[1] for k, v in sorted(ends['R'].items()) if inper(v[0]))
    # integer colour flux omega(s) = chi(a)(m_+ + m_- - 3g + 1) of a unit dual step s between adjacent squares
    # (a = the end of the crossed grid edge on the left of s; chi(x,y) = (-1)^(x+y)).
    G = defaultdict(int)   # tiles per carried unit edge, keyed by the doubled midpoint
    for e in E: G[(e[0][0] + e[1][0], e[0][1] + e[1][1])] += 1
    chi = lambda x, y: 1 if (x + y) % 2 == 0 else -1
    def omega(s0, s1):
        (X, Y), (X2, Y2) = s0, s1
        if X2 == X + 1: a, mp, mm, mid = (X + 1, Y + 1), mult[(X, Y, 1)], mult[(X2, Y, 3)], (2 * X + 2, 2 * Y + 1)
        elif X2 == X - 1: a, mp, mm, mid = (X, Y), mult[(X, Y, 3)], mult[(X2, Y, 1)], (2 * X, 2 * Y + 1)
        elif Y2 == Y + 1: a, mp, mm, mid = (X, Y + 1), mult[(X, Y, 2)], mult[(X, Y2, 0)], (2 * X + 1, 2 * Y + 2)
        else: a, mp, mm, mid = (X + 1, Y), mult[(X, Y, 0)], mult[(X, Y2, 2)], (2 * X + 1, 2 * Y)
        return chi(*a) * (mp + mm - 3 * G[mid] + 1)
    def path_flux(P): return sum(omega(P[i], P[i + 1]) for i in range(len(P) - 1))
    rowsq = lambda Y: sorted(X for (X, Yy) in cls if Yy == Y)
    def margin_path(side, Y0, Y1):   # up the margin column: vertical step, then sideways inside complete squares
        X = rowsq(Y0)[0 if side == 'L' else -1]; P = [(X, Y0)]
        for Y in range(Y0, Y1):
            Xt = rowsq(Y + 1)[0 if side == 'L' else -1]
            if (X, Y + 1) not in cls:   # sideways first, inside row Y
                while X != Xt: X += 1 if Xt > X else -1; P.append((X, Y))
            P.append((X, Y + 1))
            while X != Xt: X += 1 if Xt > X else -1; P.append((X, Y + 1))
            assert all(q in cls for q in P), 'margin path leaves the complete squares'
        return P
    I = [path_flux([(X, Y) for X in rowsq(Y)]) for Y in range(R)]
    FL = path_flux(margin_path('L', 0, R)); FR = path_flux(margin_path('R', 0, R))
    out['current'] = I; out['FL'] = FL; out['FR'] = FR
    return out

if __name__ == '__main__':
    for path in sys.argv[1:]:
        SA, SB, WM, KM, secs = parse(path)
        print(f'== {path}: shear {SA}/{SB}, WM={WM}, KM={KM}')
        for s in secs:
            o = analyse(SA, SB, WM, KM, s['cyc'])
            r = o['R']
            print(f"  lambda {s['lam']}: result/level {s.get('result', '?')}; witness period {r} rows (shift {o['PX']}): "
                  f"crossings {o['X']} ({o['X']/r:.3f}/row), waste {o['waste']}; splits L '{o['splitL']}' R '{o['splitR']}'"
                  f"{' (non-good margin squares: %d)' % o['margin_not_good'] if o['margin_not_good'] else ''}; "
                  f"absorbed ends/period {o['ends']}{' (unpaired %d)' % o['unpaired'] if o.get('unpaired') else ''}; "
                  f"end bits L {o['bitsL'] or '-'} R {o['bitsR'] or '-'}; "
                  f"{'AXIS WALL (0 crossings); ' if o['X'] == 0 else ''}integer current I(Y) per row {o['current']}; "
                  f"integer flux per period out through the left / right margin {o['FL']} / {o['FR']}")
