# KT Structures, 2026-10-03. (C5-4) inside chambers (BEYOND5 section 8): per maximal chamber, need = L - 2 C_in,
# 2 U_in, and BQx(REGION) = bad quarters in region squares at depth >= 5 minus route (i)'s deep-first selections there.
import sys, json
from pathlib import Path
from collections import defaultdict, Counter
import sys as _s; from pathlib import Path as _P; _R = _P(__file__).resolve().parents[2]
_s.path.insert(0, str(_R/"gap/turnstheory")); _s.path.insert(0, str(_R/"gap/verifier"))
import chamber_ledger as CL, chamber_scan as C, fold_exact_scan as F
import beyond5_ledger as B
from check_hall_v3 import geometry
from claim38_switch import edge, qs
from check import MOVES

def selections(f):
    grid = json.loads(Path(f).read_text())['tour']; info, cs, atoms = geometry(grid); n = info['n']
    es = {edge((x, n-1-y), (x+MOVES[int(v)][1], n-1-y-MOVES[int(v)][0])) for y, row in enumerate(grid) for x, code in enumerate(row) for v in code}
    own = defaultdict(list)
    for e in es:
        for q in qs(e): own[q].append(e)
    dep = lambda x, y: min(x, y, n-2-x, n-2-y)
    def squares(c):
        fx, fy, r = c
        return [(n-2-x if fx else x, n-2-y if fy else y) for x, y in [(r, j) for j in range(1, r+1)] + [(i, r) for i in range(r-1, 0, -1)]]
    sel = Counter()   # square -> number of selected deep quarters
    for c in cs:
        deep = sorted(((-dep(x, y), (x, y, k)) for x, y in squares(c) for k in range(4) if dep(x, y) >= 5 and len(own[x, y, k]) != 1))
        for _, q in deep[:2]: sel[q[0], q[1]] += 1
    badsq = Counter({(x, y): sum(1 for k in range(4) if len(own[x, y, k]) != 1) for x in range(n-1) for y in range(n-1)})
    return n, sel, badsq, dep

if __name__ == '__main__':
    for f in sys.argv[1:]:
        n, rep, *_ = C.analyse(f)
        _, rows, g = CL.ledger(f)
        n, sel, badsq, dep = selections(f)
        # regions again (ledger does not return them): rebuild from chamber_ledger internals
        tot = Counter()
        for r, rr in zip(rep, rows):
            reg = CL.last_regions[(r['side'], r['lo'], r['hi'])]
            deepbad = sum(badsq[q] for q in reg if dep(*q) >= 5); s = sum(sel[q] for q in reg if dep(*q) >= 5)
            line = dict(side=r['side'], L=rr['L'], need=rr['need'], twoUin=2*rr['Uin'], BQx_reg=deepbad - s, sel_reg=s, BQreg=rr['BQreg'])
            tot.update({k: v for k, v in line.items() if k != 'side'}); print('   ', line)
        print(Path(f).name, 'n', n, 'total', dict(tot), flush=True)
