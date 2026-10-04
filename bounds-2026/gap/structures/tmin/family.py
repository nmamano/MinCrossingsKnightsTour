# KT Structures, 2026-10-04. Band-periodic family: copy the PER band t times (rows and columns), then merge cycles.
# usage: family.py base.json t_max   (base must carry "per": [a, k]); writes fam/<base>_t<t>.json for each tour.
import sys, json
from pathlib import Path
from extend import dup_rows, transpose
from merge import adj_from_grid, cycles, best_swap, CODE
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from kt.core import validate, num_turns

def merge_grid(g):
    n = len(g); adj = adj_from_grid(g); lab, c = cycles(adj); cost = 0; c0 = c
    while c > 1:
        b = best_swap(adj, lab)
        if b is None: return None, None, c0
        cost += b[0]; adj.update(b[1]); lab, c = cycles(adj)
    out = [['' for _ in range(n)] for _ in range(n)]
    for (i, j), nb in adj.items():
        out[i][j] = '%d%d' % tuple(sorted(CODE[(q[0] - i, q[1] - j)] for q in nb))
    return out, cost, c0

def main():
    src = sys.argv[1]; tmax = int(sys.argv[2])
    rec = json.loads(Path(src).read_text()); g0 = rec['grid']; a, k = rec['per']
    Path('fam').mkdir(exist_ok=True)
    for t in range(0, tmax + 1):
        g = transpose(dup_rows(transpose(dup_rows(g0, a, k, t)), a, k, t)) if t else g0
        n = len(g); base = num_turns(g) - 8 * n
        out, cost, c0 = merge_grid(g)
        if out is None:
            print(f'{src} t={t} n={n} 2f {base} cycles {c0}: merge stuck', flush=True); continue
        assert validate(out)
        T = num_turns(out) - 8 * n
        Path(f'fam/{Path(src).stem}_t{t}.json').write_text(json.dumps(dict(n=n, T=num_turns(out), T_minus_8n=T, src=src,
            per=[a, k], copies=t, cycles_before=c0, merge_cost=cost, date='2026-10-04', grid=out)))
        print(f'{src} t={t} n={n} 2f {base} cycles {c0} -> tour {T}', flush=True)

if __name__ == '__main__':
    main()
