#!/usr/bin/env python
"""All-n pipeline for corner sets (KT Integrator, 2026-10-04). Generalises periodic.py.

Input: one or more base tours from gap/searcher/turns/csolve.py --mode tour --out (keys n, tour, A, B, combo
or inline bottom/left/top/right/phases, optional region). All bases must use the same side gadgets and phases.
Steps:
 1. Skeleton = kt.board.build_general(gadgets, phases). Free shape = the corner regions (A x B + B x A, or the
    explicit region), stored as offsets from the corner anchors BL (0,0), BR (n,0), TL (0,n), TR (n,n).
    Every base tour must equal the skeleton outside the shape; differing cells are added to the shape.
 2. Outside matching (ends of all fixed paths, as anchored offsets) for every even n; smallest period p in n
    and the first n (n_s) from which it is periodic.
 3. Per residue class mod p: corner content from a base in that class (n >= n_s), else a CP-SAT solve
    (turns first, crossings tie-break) at the smallest n0 >= max(n_s, 56) in the class.
 4. Every even n in [nmin, nmax]: transplant the class content; if the tour is not valid, solve directly.
 5. Write pipeline/<tag>/res<r>.json (input of allsize_check.py), tours/<tag>_n<n>.json, SUMMARY.md.
Usage: allpipe.py --tag X gap/searcher/turns/base_n56.json [...] [--nmin 48 --nmax 110 --time 300 --workers 2]
"""
import argparse, json, os, sys, time
from math import gcd
def lcm(a, b): return a * b // gcd(a, b)
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE); sys.path.insert(0, ROOT)
from kt.board import build_general, complete, to_grid, fixed_paths, tpl_moves
from kt.core import validate, num_crossings, num_turns, MI, MJ
from assemble import walk_check

CORNERS = ('BL', 'BR', 'TL', 'TR')
def anchor(k, n): return ((n if k[1] == 'R' else 0), (n if k[0] == 'T' else 0))
def local(k, i, j):  # i = distance from the vertical side, j = from the horizontal side
    return ((-1 - i) if k[1] == 'R' else i, (-1 - j) if k[0] == 'T' else j)

def grid_to_full(g):
    n = len(g); full = {}
    for r, row in enumerate(g):
        for x, code in enumerate(row):
            y = n - 1 - r
            full[(x, y)] = {(x + MJ[int(m)], y - MI[int(m)]) for m in code}
    return full

class Spec:
    def __init__(self, d):
        if 'bottom' not in d and 'combo' in d:
            c = json.load(open(os.path.join(ROOT, d['combo']) if not os.path.isabs(d['combo']) else d['combo']))
            d = {**c, **d}
        menu = {e['name']: e['tpl'] for e in json.load(open(os.path.join(HERE, 'menu_turns.json')))}
        g = lambda v: menu[v] if isinstance(v, str) else v       # a gadget may be a menu_turns.json name
        self.B, self.L = g(d['bottom']), g(d['left'])
        self.T, self.R = g(d.get('top') or d['bottom']), g(d.get('right') or d['left'])
        self.ph = tuple(d['phases'])
        dep = [tpl_moves(t)[2] for t in (self.B, self.T)] + [tpl_moves(t)[1] for t in (self.L, self.R)]
        self.zmin = max(dep) + 1
        self.depths = dict(B=dep[0], T=dep[1], L=dep[2], R=dep[3])
        self.per = dict(B=tpl_moves(self.B)[1], T=tpl_moves(self.T)[1], L=tpl_moves(self.L)[2], R=tpl_moves(self.R)[2])
    def key(self): return json.dumps([self.B, self.T, self.L, self.R, self.ph])
    def skeleton(self, n): return build_general(n, self.B, self.L, self.T, self.R, phases=self.ph, Z=self.zmin)[0]

def extract(n, full, Db, Dl, P, Q):
    """Read the four periodic side bands from a tour (sample near the middle of each side); phases (0,0,0,0).
    The skeleton-vs-tour comparison in main() then checks that the bands really are periodic."""
    inv = {(MJ[m], -MI[m]): m for m in range(8)}
    def code(c, sgn): return ''.join(sorted(str(inv[(sgn * (v[0] - c[0]), sgn * (v[1] - c[1]))]) for v in full[c]))
    mid = lambda L, i: i % L + L * ((n // 2) // L)
    bottom = [' '.join(code((mid(P, l), y), 1) for l in range(P)) for y in range(Db - 1, -1, -1)]
    top = [' '.join(code((mid(P, -l), n - 1 - y), -1) for l in range(P)) for y in range(Db - 1, -1, -1)]
    left = [' '.join(code((x, mid(Q, ly)), 1) for x in range(Dl)) for ly in range(Q - 1, -1, -1)]
    right = [' '.join(code((n - 1 - x, mid(Q, -ly)), -1) for x in range(Dl)) for ly in range(Q - 1, -1, -1)]
    return dict(bottom=bottom, top=top, left=left, right=right, phases=[0, 0, 0, 0])

def shape_of(d):
    sh = {k: set() for k in CORNERS}
    if 'region' in d:
        for k in CORNERS:
            for i, j in d['region'][k]: sh[k].add(local(k, i, j))
    else:
        A, B = d['A'], d['B']
        for k in CORNERS:
            for (w, h) in ((A, B), (B, A)):
                for i in range(w):
                    for j in range(h): sh[k].add(local(k, i, j))
    return sh

def cells(sh, n):
    out = {}
    for k in CORNERS:
        ax, ay = anchor(k, n)
        for (dx, dy) in sh[k]: out[(ax + dx, ay + dy)] = (k, (dx, dy))
    return out

def outside(spec, sh, n):
    cm = cells(sh, n)
    if len(cm) != sum(len(v) for v in sh.values()): return None          # corner regions overlap
    nb = spec.skeleton(n)
    paths, closed = fixed_paths(n, nb, set(cm))
    if closed: return None
    m = set()
    for (u, v, cs) in paths:
        a = cm[u] + ((cs[0][0] - u[0], cs[0][1] - u[1]),)
        b = cm[v] + ((cs[-1][0] - v[0], cs[-1][1] - v[1]),)
        m.add(tuple(sorted([a, b])))
    return frozenset(m)

def content(sh, n, full):
    out = {}
    for c, (k, off) in cells(sh, n).items():
        out[f'{k}:{off[0]},{off[1]}'] = sorted([v[0] - c[0], v[1] - c[1]] for v in full[c])
    return out

def apply(spec, n, cont):
    full = {c: set(v) for c, v in spec.skeleton(n).items()}
    for key, ds in cont.items():
        k, xy = key.split(':'); dx, dy = map(int, xy.split(',')); ax, ay = anchor(k, n)
        c = (ax + dx, ay + dy)
        if not (0 <= c[0] < n and 0 <= c[1] < n): return None
        full[c] = {(c[0] + a, c[1] + b) for a, b in ds}
    return full

def check(n, full):
    if full is None: return None
    try: g = to_grid(n, full)
    except Exception: return None
    if not (validate(g) and walk_check(g)): return None
    return g

def solve(spec, sh, n, a, hint=None, fixed=None):
    nb = spec.skeleton(n); free = set(cells(sh, n))
    if fixed:
        fx = apply(spec, n, fixed)
        for key in fixed:
            k, xy = key.split(':'); dx, dy = map(int, xy.split(',')); ax, ay = anchor(k, n)
            c = (ax + dx, ay + dy); nb[c] = fx[c]; free.discard(c)
    w = dict(turn_weight=1000, crossing_weight=0 if a.pure_turns else 1)
    full, info = complete(n, nb, free, time_limit=a.time, workers=a.workers, hint=hint if hint else True, **w)
    return full, info

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('bases', nargs='*'); ap.add_argument('--tag', required=True)
    ap.add_argument('--combo', help='no bases: JSON with bottom/left/top/right/phases (gadget names allowed); needs --A --B')
    ap.add_argument('--A', type=int); ap.add_argument('--B', type=int)
    ap.add_argument('--nmin', type=int, default=48); ap.add_argument('--nmax', type=int, default=110)
    ap.add_argument('--time', type=float, default=300); ap.add_argument('--workers', type=int, default=2)
    ap.add_argument('--pure-turns', action='store_true', help='no crossing tie-break (faster solves)')
    ap.add_argument('--max-corner', type=int, default=16, help='reject base tours that differ from the skeleton farther in')
    ap.add_argument('--extract', help='Db,Dl,P,Q: read the side bands from each base tour (bases without gadget keys)')
    ap.add_argument('--period', type=int, help='use this period in n (needed with --residues if other classes are bad)')
    ap.add_argument('--residues', help='only these even residues mod p (comma list); the claim covers only them')
    a = ap.parse_args()
    out = os.path.join(HERE, 'pipeline', a.tag); os.makedirs(os.path.join(out, 'tours'), exist_ok=True)
    log = open(os.path.join(out, 'run.log'), 'a')
    def say(*s):
        msg = ' '.join(str(x) for x in s); print(msg, flush=True); log.write(msg + '\n'); log.flush()
    say(f'== allpipe {a.tag} {time.strftime("%Y-%m-%d %H:%M:%S")} bases={a.bases}')
    raw = [json.load(open(p)) for p in a.bases]
    for d in raw:
        if a.A and 'A' not in d and 'region' not in d: d['A'], d['B'] = a.A, a.B or a.A
        if a.extract and 'bottom' not in d and 'combo' not in d:
            Db, Dl, P_, Q_ = map(int, a.extract.split(','))
            d.update(extract(d['n'], grid_to_full(d['tour']), Db, Dl, P_, Q_))
    if not raw:
        assert a.combo and a.A and a.B, 'give base files, or --combo with --A and --B'
        specs = [Spec(json.load(open(a.combo)))]
    else:
        specs = [Spec(d) for d in raw]
    assert all(s.key() == specs[0].key() for s in specs), 'bases use different gadgets or phases'
    spec = specs[0]
    sh = {k: set() for k in CORNERS}
    if not raw: sh = shape_of(dict(A=a.A, B=a.B))
    for d in raw:
        for k, v in shape_of(d).items(): sh[k] |= v
    bases = {}
    for p, d in zip(a.bases, raw):
        n = d['n']; full = grid_to_full(d['tour']); g = check(n, full)
        assert g is not None, f'{p}: base tour is not one valid closed tour'
        nb = spec.skeleton(n); cm = cells(sh, n); extra = []
        for c in nb:
            if c not in cm and full[c] != nb[c]: extra.append(c)
        def inward(c):  # corner distance: max(i, j) in the nearest corner's inward coordinates
            return min(max(c[0] if k[1] == 'L' else n - 1 - c[0], c[1] if k[0] == 'B' else n - 1 - c[1]) for k in CORNERS)
        far = [c for c in extra if inward(c) >= a.max_corner]
        if far:
            codes = {}
            for c in far:
                g_ = {(v[0] - c[0], v[1] - c[1]) for v in full[c]}
                key = 'straight (2,1) [15]' if g_ == {(2, 1), (-2, -1)} else 'straight (1,-2) [37]' if g_ == {(1, -2), (-1, 2)} \
                    else 'straight (2,-1) [26]' if g_ == {(2, -1), (-2, 1)} else 'other'
                codes[key] = codes.get(key, 0) + 1
            sys.exit(f'REJECT {p}: {len(far)} cells at corner distance >= {a.max_corner} differ from the TT16-type skeleton '
                     f'(single x+2y straight interior + 4 periodic side bands). Their moves: {codes}. Mixed interior fields '
                     f'(e.g. move pairs 15/37, period 5) and side gadgets that change along a side are not supported: '
                     f'the all-size insertion argument of allsize_check.py does not apply to them.')
        for c in extra:  # add to the nearest corner's shape
            k = min(CORNERS, key=lambda k: max(abs(c[0] - anchor(k, n)[0]), abs(c[1] - anchor(k, n)[1])))
            ax, ay = anchor(k, n); sh[k].add((c[0] - ax, c[1] - ay))
        if extra: say(f'{p}: {len(extra)} cells outside the stated region differ from the skeleton; added to the shape')
        bases[n] = (p, full, num_turns(g), num_crossings(g))
        say(f'base n={n}: T={num_turns(g)} (T-8n={num_turns(g) - 8 * n}) X={num_crossings(g)} file={p}')
    for k in CORNERS:
        ow, oh = spec.depths['L' if k[1] == 'L' else 'R'], spec.depths['B' if k[0] == 'B' else 'T']
        need = {local(k, i, j) for i in range(ow) for j in range(oh)}
        assert need <= sh[k], f'shape at {k} must cover the band overlap {ow}x{oh}'
    say('shape cells per corner:', {k: len(v) for k, v in sh.items()},
        'bounding boxes:', {k: (max(abs(x) for x, _ in v) + (k[1] == 'L'), max(abs(y) for _, y in v) + (k[0] == 'B')) for k, v in sh.items()})
    # 2. period of the outside matching
    hi = max(a.nmax, 200) + 100
    M = {n: outside(spec, sh, n) for n in range(a.nmin, hi + 1, 2)}
    best = None
    if a.period:  # periodicity required only inside the wanted classes
        p = a.period; wr = [int(r) for r in a.residues.split(',')] if a.residues else list(range(0, p, 2))
        for ns in range(a.nmin, 101, 2):
            if all(M[n] is not None and M[n] == M[n + p] for n in range(ns, hi - p + 1, 2) if n % p in wr):
                best = (p, ns); break
        say(f'bad n (overlap/closed fixed cycles) in the wanted classes: {[n for n in M if M[n] is None and n % p in wr]}')
    for p in ([] if a.period else range(2, 97, 2)):
        for ns in range(a.nmin, 101, 2):
            if all(M[n] is not None and M[n] == M[n + p] for n in range(ns, hi - p + 1, 2)):
                best = (p, ns); break
        if best: break
    assert best, 'outside matching has no period <= 96 from any n <= 100'
    p, ns = best
    say(f'outside matching: EMPIRICAL period p={p} in n from n_s={ns} (finite check to n={hi}, not a proof); '
        f'n with overlap/closed fixed cycles: {[n for n in M if M[n] is None]}')
    # 3. content per residue class
    cont = {}
    want = sorted(int(r) for r in a.residues.split(',')) if a.residues else list(range(0, p, 2))
    assert all(r % 2 == 0 and 0 <= r < p for r in want), ('residues must be even and < p', want, p)
    for r in want:
        src = sorted(n for n in bases if n % p == r and n >= ns)
        if src:
            n0 = src[0]; cont[r] = (n0, content(sh, n0, bases[n0][1]), dict(source=bases[n0][0]))
            continue
        n0 = next(n for n in range(max(ns, 56), 1000, 2) if n % p == r)
        if not bases:
            say(f'res {r}: no base; solving at n0={n0} from the skeleton hint (time {a.time}s) ...')
            full, info = solve(spec, sh, n0, a)
            if full is None: say(f'res {r}: solve FAILED: {info}'); continue
            say(f'res {r}: solved n0={n0}: {info}'); g = check(n0, full)
            if g is None: say(f'res {r}: solution is not one tour'); continue
            bases[n0] = ('allpipe CP-SAT', full, num_turns(g), num_crossings(g))
            cont[r] = (n0, content(sh, n0, full), dict(source='allpipe CP-SAT', info=info)); continue
        nb_ = min(bases, key=lambda m: abs(m - n0))
        bc = content(sh, nb_, bases[nb_][1]); hint = apply(spec, n0, bc)
        # a corner keeps its exact band surroundings when n changes by a multiple of the band periods there
        same = {'BL': True, 'BR': (n0 - nb_) % spec.per['B'] == 0, 'TL': (n0 - nb_) % spec.per['L'] == 0,
                'TR': (n0 - nb_) % lcm(spec.per['T'], spec.per['R']) == 0}
        keep = [k for k in CORNERS if same[k]]
        say(f'res {r}: no base; solving at n0={n0} with corners {keep} copied from base n={nb_} '
            f'(time {a.time}s, workers {a.workers}) ...')
        full, info = solve(spec, sh, n0, a, hint=hint, fixed={key: v for key, v in bc.items() if key.split(':')[0] in keep})
        if full is None and keep:
            say(f'res {r}: with copied corners: {info}; retrying with all corners free')
            full, info = solve(spec, sh, n0, a, hint=hint)
        if full is None: say(f'res {r}: solve FAILED: {info}'); continue
        say(f'res {r}: solved n0={n0}: {info}')
        cont[r] = (n0, content(sh, n0, full), dict(source='allpipe CP-SAT', info=info))
    # 4. all n
    rows = []
    for n in range(a.nmin, a.nmax + 1, 2):
        r = n % p; how = None; g = None
        if r not in want: continue
        if r in cont:
            g = check(n, apply(spec, n, cont[r][1])); how = f'transplant res{r:02d} (n0={cont[r][0]})' if g else None
        if g is None:
            hint = apply(spec, n, cont[r][1]) if r in cont else None
            full, info = solve(spec, sh, n, a, hint=hint)
            g = check(n, full); how = f'direct solve {info.get("status") if isinstance(info, dict) else info}'
        if g is None:
            say(f'n={n}: FAILED ({how})'); rows.append((n, None, None, 'FAILED')); continue
        T, X = num_turns(g), num_crossings(g)
        rows.append((n, T, X, how))
        json.dump(dict(n=n, tag=a.tag, turns=T, crossings=X, method=how, bottom=spec.B, top=spec.T, left=spec.L,
                       right=spec.R, phases=list(spec.ph), tour=g), open(os.path.join(out, 'tours', f'{a.tag}_n{n}.json'), 'w'))
        say(f'n={n}: T={T} T-8n={T - 8 * n} X={X} {how}')
    # 5. residue files
    for r, (n0, c, src) in cont.items():
        json.dump(dict(format='anchored-v2', tag=a.tag, n0=n0, period=p, n_stable=ns, residue=r, phases=list(spec.ph),
                       bottom=spec.B, top=spec.T, left=spec.L, right=spec.R, source=src, zones=c,
                       note='zones: key "<corner>:dx,dy" = cell anchor + (dx, dy), anchors BL (0,0), BR (n,0), TL (0,n), '
                            'TR (n,n); value = the two moves (mx, my); x right, y up; apply to build_general(gadgets, phases)'),
                  open(os.path.join(out, f'res{r:02d}.json'), 'w'))
    ok = [x for x in rows if x[1] is not None]
    worst = max((T - 8 * n for n, T, X, h in ok), default=None)
    per = {}
    for n, T, X, h in ok: per.setdefault(n % p, set()).add(T - 8 * n)
    with open(os.path.join(out, 'SUMMARY.md'), 'w') as f:
        f.write(f'# {a.tag}: all-n pipeline ({time.strftime("%Y-%m-%d %H:%M")} UTC+2 box clock)\n\n')
        f.write('Candidate data, not a theorem: the all-n statement needs a PASS of allsize_check.py and its audit.\n\n')
        f.write(f'Bases: {a.bases}\nEmpirical period p = {p} from n_s = {ns} (finite check to n = {hi}). Residue sources: '
                f'{ {r: (v[0], v[2].get("source")) for r, v in cont.items()} }\n\n')
        f.write(f'T - 8n per residue class mod {p} (n = {a.nmin}..{a.nmax}): {dict(sorted((k, sorted(v)) for k, v in per.items()))}\n')
        f.write(f'Worst T - 8n over the n that succeeded: {worst}  (TT16: -14). FAILED n: {[x[0] for x in rows if x[1] is None]}\n\n')
        f.write('| n | T | T-8n | X | method |\n|---|---|---|---|---|\n')
        for n, T, X, h in rows: f.write(f'| {n} | {T} | {"" if T is None else T - 8 * n} | {X} | {h} |\n')
    say(f'DONE (candidate; failed n: {[x[0] for x in rows if x[1] is None]}): T-8n per residue {dict(sorted((k, sorted(v)) for k, v in per.items()))}; worst {worst}; '
        f'next: python3 w-integrator/allsize_check.py w-integrator/pipeline/{a.tag}')

if __name__ == '__main__':
    main()
