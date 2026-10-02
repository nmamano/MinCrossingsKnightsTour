#!/usr/bin/env python3
"""TT16 tours for the turns note: build from the corner files, check, count, draw, make tables.

Standard library for the checks; matplotlib only for the drawings.
usage (from the project root): .venv/bin/python writeup/turns/figures/tt16.py
"""
import json
from pathlib import Path

ROOT = Path('/home/nil/nil/knight-formation-research')
OUT = Path(__file__).resolve().parent
DIRS = ((1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1), (-2, 1), (-1, 2))
CODE = {d: k for k, d in enumerate(DIRS)}


def template(rows):
    rows = [r.split() for r in rows]
    return {(x, len(rows) - 1 - r): tuple(DIRS[int(k)] for k in s)
            for r, row in enumerate(rows) for x, s in enumerate(row)}, len(rows[0]), len(rows)


def corner_data(residue):
    return json.loads((ROOT / f'w-integrator/corners/TT16_res{residue:02d}.json').read_text())


def build(n):
    """Graph of the TT16 tour for even n >= 48: cell -> its two neighbours."""
    d = corner_data(n % 8)
    B, P, D = template(d['bottom']); T, PT, DT = template(d['top'])
    L, W, Q = template(d['left']); R, WR, QR = template(d['right'])
    xb, xt, yl, yr = d['phases']
    g = {}
    for x in range(n):
        for y in range(n):
            ds = ((2, -1), (-2, 1))
            if y < D: ds = B[((x - xb) % P, y)]
            if y >= n - DT: ds = tuple((-a, -b) for a, b in T[((xt - x) % PT, n - 1 - y)])
            if x < W: ds = L[(x, (y - yl) % Q)]
            if x >= n - WR: ds = tuple((-a, -b) for a, b in R[(n - 1 - x, (yr - y) % QR)])
            g[x, y] = tuple((x + a, y + b) for a, b in ds)
    z = d['Z']; anchors = {'BL': (0, 0), 'BR': (n - z, 0), 'TL': (0, n - z), 'TR': (n - z, n - z)}
    for name, ds in d['zones'].items():
        corner, uv = name.split(':'); u, v = map(int, uv.split(',')); a, b = anchors[corner]
        x, y = a + u, b + v
        g[x, y] = tuple((x + dx, y + dy) for dx, dy in ds)
    return g


def check_tour(g):
    for u, vs in g.items():
        assert len(set(vs)) == 2
        for v in vs:
            assert v in g and u in g[v], (u, v)
            assert sorted(map(abs, (v[0] - u[0], v[1] - u[1]))) == [1, 2]
    start = next(iter(g)); prev = None; u = start; seen = set()
    while u not in seen:
        seen.add(u); v = next(v for v in g[u] if v != prev); prev, u = u, v
    assert u == start and len(seen) == len(g), 'not one cycle'


def is_turn(g, u):
    (a, b) = g[u]
    return (a[0] - u[0], a[1] - u[1]) != (u[0] - b[0], u[1] - b[1])


def turns(g):
    return sum(is_turn(g, u) for u in g)


def counts():
    rows = []
    for n in range(48, 104, 2):
        g = build(n); check_tour(g); t = turns(g)
        zone = sum(is_turn(g, (x, y)) for x in range(n) for y in range(n)
                   if (x < 6 or x >= n - 6) and (y < 6 or y >= n - 6))
        assert t == 8 * n - 14, (n, t)
        rows.append((n, t, zone))
    return rows


def corner_tables():
    """LaTeX: the four 6x6 corner squares per residue, as move-code grids (rows top first)."""
    out = []
    for r in (0, 2, 4, 6):
        d = corner_data(r)
        cells = []
        for corner in ('TL', 'TR', 'BL', 'BR'):
            grid = []
            for v in range(5, -1, -1):
                grid.append(' & '.join(''.join(sorted(str(CODE[tuple(m)]) for m in d['zones'][f'{corner}:{u},{v}']))
                                       for u in range(6)))
            cells.append((corner, grid))
        out.append(f'\\paragraph{{Residue $n\\equiv {r}\\pmod 8$.}}\n\\begin{{center}}\\scriptsize\\ttfamily')
        for i, (corner, grid) in enumerate(cells):
            out.append(f'\\begin{{tabular}}[t]{{@{{}}c@{{\\,}}c@{{\\,}}c@{{\\,}}c@{{\\,}}c@{{\\,}}c@{{}}}}'
                       f'\\multicolumn{{6}}{{c}}{{\\normalfont\\scriptsize {corner}}}\\\\')
            out.append('\\\\\n'.join(grid) + '\\end{tabular}' + ('\\qquad' if i < 3 else ''))
        out.append('\\end{center}\n')
    (OUT / 'corner_tables.tex').write_text('\n'.join(out))


# ---------------------------------------------------------------- drawings
def save(fig, name):
    fig.savefig(OUT / f'{name}.pdf', bbox_inches='tight')
    fig.savefig(OUT / f'turns_{name}.png', bbox_inches='tight', dpi=110)

def draw_window(ax, g, n, x0, x1, y0, y1, period_lines=None, shade_zone=True, dot=6):
    import matplotlib.patches as mp
    ax.set_xlim(x0 - 0.6, x1 + 0.6); ax.set_ylim(y0 - 0.6, y1 + 0.6)
    ax.set_aspect('equal'); ax.axis('off')
    for x in range(x0, x1 + 1):
        for y in range(y0, y1 + 1):
            if (x + y) % 2 == 0:
                ax.add_patch(mp.Rectangle((x - .5, y - .5), 1, 1, color='#eef1f4', lw=0, zorder=0))
    if shade_zone:
        for cx, cy in [(0, 0), (n - 6, 0), (0, n - 6), (n - 6, n - 6)]:
            ax.add_patch(mp.Rectangle((cx - .5, cy - .5), 6, 6, fill=False, ec='#7a5195', lw=1.2,
                                      ls='--', zorder=1))
    drawn = set()
    for u, vs in g.items():
        for v in vs:
            e = tuple(sorted((u, v)))
            if e in drawn: continue
            drawn.add(e)
            inside = [x0 - 2 <= p[0] <= x1 + 2 and y0 - 2 <= p[1] <= y1 + 2 for p in e]
            if any(inside):
                ax.plot([e[0][0], e[1][0]], [e[0][1], e[1][1]], color='#4a5a6a', lw=0.8, zorder=2,
                        solid_capstyle='round')
    for x in range(x0, x1 + 1):
        for y in range(y0, y1 + 1):
            if (x, y) in g:
                if is_turn(g, (x, y)):
                    ax.plot(x, y, 'o', color='#c0392b', ms=dot * 0.8, zorder=3)
                else:
                    ax.plot(x, y, 'o', color='#9aa5b1', ms=dot * 0.35, zorder=3)
    for xp in (period_lines or []):
        ax.plot([xp - .5, xp - .5], [y0 - .6, y1 + .6], color='#2c7fb8', lw=1, ls=':', zorder=1)


def figures():
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    plt.rcParams['font.size'] = 9
    n = 48; g = build(n)
    # whole tour
    fig, ax = plt.subplots(figsize=(5.2, 5.2))
    draw_window(ax, g, n, 0, n - 1, 0, n - 1, dot=2.2)
    save(fig, 'tour48'); plt.close(fig)
    # bottom-left corner and bottom band, with period boundaries
    fig, ax = plt.subplots(figsize=(6.4, 2.8))
    draw_window(ax, g, n, 0, 25, 0, 8, period_lines=[8, 16, 24])
    save(fig, 'band_bottom'); plt.close(fig)
    # left band
    fig, ax = plt.subplots(figsize=(2.6, 4.2))
    draw_window(ax, g, n, 0, 9, 14, 29)
    save(fig, 'band_left'); plt.close(fig)


def lemma_figure():
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import matplotlib.patches as mp
    fig, axes = plt.subplots(1, 3, figsize=(6.6, 2.9))
    titles = ['column 0: always a turn', 'columns 1, 2: two outward\nmoves give a turn',
              'column 3: no move back\ngives a turn']
    cases = [((0, 3), [(1, 2), (2, 1), (2, -1), (1, -2)], [(1, 2), (2, -1)], 0),
             ((1, 3), [(-1, 2), (-1, -2), (2, 1), (2, -1)], [(-1, 2), (2, -1)], 1),
             ((3, 3), [(-1, 2), (-2, 1), (-2, -1), (-1, -2), (1, 2), (2, -1)],
              [(1, 2), (2, -1)], 3)]
    shade = ['#d6ecea', '#f3e6d4', '#e2def0']
    for ax, title, (c, allowed, used, col), sh in zip(axes, titles, cases, shade):
        ax.set_xlim(-0.6, 5.6); ax.set_ylim(-0.6, 6.6); ax.set_aspect('equal'); ax.axis('off')
        cols = [0] if col == 0 else ([1, 2] if col == 1 else [3])
        for x in range(6):
            for y in range(7):
                color = sh if x in cols else ('#f4f6f8' if (x + y) % 2 == 0 else 'white')
                ax.add_patch(mp.Rectangle((x - .5, y - .5), 1, 1, fc=color, ec='#d0d5da', lw=0.5))
        ax.plot([-.5, -.5], [-.5, 6.5], color='black', lw=2.5)
        for d in allowed:
            if d in used: continue
            outward = col in (1,) and (c[0] + d[0]) in (0, 3)
            ax.annotate('', xy=(c[0] + d[0], c[1] + d[1]), xytext=c,
                        arrowprops=dict(arrowstyle='->', color='#b0b6bc', lw=0.8, ls='--'))
        for d in used:
            ax.annotate('', xy=(c[0] + d[0], c[1] + d[1]), xytext=c,
                        arrowprops=dict(arrowstyle='->', color='#c0392b', lw=1.6))
        ax.plot(*c, 'o', color='#c0392b', ms=6)
        for x in range(6):
            ax.text(x, -0.95, str(x), ha='center', va='top', fontsize=7, color='#666')
        ax.set_title(title, fontsize=8.5)
    save(fig, 'lemma'); plt.close(fig)


if __name__ == '__main__':
    rows = counts()
    print('PASS: TT16 one closed tour with 8n-14 turns for n =', rows[0][0], '..', rows[-1][0])
    for n, t, zone in rows:
        print(f'  n={n:3d} turns={t} (= 8n-14) turns in the four 6x6 corner squares={zone}')
    for n, _, _ in rows:
        (OUT / f'tour{n}.json').write_text(json.dumps([[list(u),list(vs)] for u,vs in build(n).items()]))
    corner_tables(); lemma_figure(); figures()
    print('wrote corner_tables.tex, lemma.pdf, tour48.pdf, band_bottom.pdf, band_left.pdf')
