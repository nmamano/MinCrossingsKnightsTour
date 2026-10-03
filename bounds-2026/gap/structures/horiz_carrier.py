"""Odd-current carrier crossing the strands (SHEET 13.4): horizontal band (T = (p, 0)) in a uniform (2,1) field,
every strand crosses it and is shifted by `shift` lines (S8: odd shift <=> odd current). Min crossings per period,
via w-structures/seam.py. KT Structures, 2026-10-03.  usage: python horiz_carrier.py p w shift [time]"""
import sys
sys.path.insert(0, '/home/nil/nil/knight-formation-research/w-structures')
from seam import Seam, solve
p, w, sh = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]); tl = float(sys.argv[4]) if len(sys.argv) > 4 else 300
st = Seam(T=(p, 0), hv=(0, 1), w1=w, w2=w, f1=(2, 1), form1=(1, -2), f2=(2, 1), form2=(1, -2), s=1, shift=sh)
r = solve(st, time_limit=tl, workers=3)
print(f"horizontal p={p} w={w} shift={sh}: {r['status']} X={r.get('X')} bound={r.get('bound')} per unit x={None if r.get('X') is None else r['X']/p}", flush=True)
