"""Periodic edge-gadget model.

Unrolled plane coordinates (x, y): x = column (right), y = row from the board edge.
Interior structure: parallel knight lines  x + 2y = c  (direction (2,-1)), i.e. board.js '26'.
A *gadget region* is a constant-depth strip along one board edge, periodic with translation T:
  kind='bottom': region 0 <= y < depth, board y >= 0, T = (period, 0)
  kind='left'  : region 0 <= x < depth, board x >= 0, T = (0, period)
Every on-board cell outside the region keeps its two line edges (forced). Line edges joining an
outside cell to a region cell are FIXED edges; region cells touching them are terminals (line ends).
Lane of line c: floor((c - off)/s); lane pair p = floor(lane/2), side = lane % 2.
Gadget must: give every region cell degree 2, contain no cycle (incl. winding ones), and join each
terminal to a terminal of the same lane pair on the other side (formation-preserving up to
permutation of the s strands -- Nil's relaxation).
"""
from collections import defaultdict
from .core import seg_cross

MOVES = [(1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1), (-2, 1), (-1, 2)]

class Strip:
    def __init__(self, kind, period, depth, s=4, off=0):
        self.kind, self.P, self.D, self.s, self.off = kind, period, depth, s, off
        if kind == 'bottom':
            self.T = (period, 0)
            self.base = [(x, y) for y in range(depth) for x in range(period)]
            self.pos = [d for d in MOVES if d[0] > 0]
            assert period % (2 * s) == 0
            self.pairs_per_period = period // (2 * s)
        elif kind == 'left':
            self.T = (0, period)
            self.base = [(x, y) for x in range(depth) for y in range(period)]
            self.pos = [d for d in MOVES if d[1] > 0]
            assert (2 * period) % (2 * s) == 0
            self.pairs_per_period = (2 * period) // (2 * s)
        else:
            raise ValueError(kind)
        self.idx = {c: i for i, c in enumerate(self.base)}
        self._build()

    def in_region(self, c):
        return 0 <= (c[1] if self.kind == 'bottom' else c[0]) < self.D

    def on_board(self, c):
        return (c[1] if self.kind == 'bottom' else c[0]) >= 0

    def canon(self, c):
        """(base cell, k) with c = base + k*T."""
        if self.kind == 'bottom':
            k, x = divmod(c[0], self.P); return (x, c[1]), k
        k, y = divmod(c[1], self.P); return (c[0], y), k

    def shift(self, c, k):
        return (c[0] + k * self.T[0], c[1] + k * self.T[1])

    def _build(self):
        # variable edges: (u, v_unrolled) with u base cell
        self.var_edges = []
        self.fixed_edges = []
        for u in self.base:
            for d in MOVES:
                v = (u[0] + d[0], u[1] + d[1])
                if not self.on_board(v):
                    continue
                if self.in_region(v):
                    if d in self.pos:
                        self.var_edges.append((u, v))
                else:
                    # forced line edge iff v's line edge points to u
                    if d in ((-2, 1), (2, -1)):
                        self.fixed_edges.append((u, v))
        self.inc = defaultdict(list)          # base cell -> [(edge id, direction from cell)]
        for eid, (u, v) in enumerate(self.var_edges):
            vb, k = self.canon(v)
            d = (v[0] - u[0], v[1] - u[1])
            self.inc[u].append((eid, d))
            self.inc[vb].append((eid, (-d[0], -d[1])))
        self.fixed_inc = defaultdict(list)
        for (u, v) in self.fixed_edges:
            self.fixed_inc[u].append((v[0] - u[0], v[1] - u[1]))
        self.terminals = sorted(self.fixed_inc)
        for u in self.base:
            assert len(self.fixed_inc[u]) <= 1, u
        # crossing multiplicities: N[(a,b)] for a<=b over var+fixed segments
        segs = [('v', i, e) for i, e in enumerate(self.var_edges)] + [('f', i, e) for i, e in enumerate(self.fixed_edges)]
        self.cross = defaultdict(int)   # key ((kind,i),(kind,j)) -> count of translates crossing
        K = 4 // max(1, min(self.P, 4)) + 2
        for a in range(len(segs)):
            ka, ia, (p1, p2) = segs[a]
            for b in range(a, len(segs)):
                kb, ib, (q1, q2) = segs[b]
                cnt = 0
                for k in range(-K, K + 1):
                    if a == b and k == 0:
                        continue
                    r1, r2 = self.shift(q1, k), self.shift(q2, k)
                    if seg_cross(p1, p2, r1, r2):
                        cnt += 1
                if cnt:
                    if a == b:
                        assert cnt % 2 == 0
                        cnt //= 2
                    self.cross[((ka, ia), (kb, ib))] += cnt

    def line_of(self, u):
        return u[0] + 2 * u[1]

    def lane_info(self, u):
        lane = (self.line_of(u) - self.off) // self.s
        return lane // 2, lane % 2

    # ---------- evaluation of a concrete solution (set of var edge ids) ----------
    def evaluate(self, chosen):
        chosen = set(chosen)
        X = 0
        for ((ka, ia), (kb, ib)), c in self.cross.items():
            pa = ka == 'f' or ia in chosen
            pb = kb == 'f' or ib in chosen
            if pa and pb:
                X += c
        turns = 0
        for u in self.base:
            dirs = [d for (eid, d) in self.inc[u] if eid in chosen] + self.fixed_inc[u]
            assert len(dirs) == 2, (u, dirs)
            if dirs[0] != (-dirs[1][0], -dirs[1][1]):
                turns += 1
        return X, turns
