"""Parity-lifted version of potlp.py: for EVEN side length L (n = 2A + L even) the side is a path in G x Z_2.
Two linear potentials h0, h1 with  S*c + h0(u) - h1(v) >= 0  and  S*c + h1(u) - h0(v) >= 0  on every arc of G.
A side of even length from s to e then costs >= (h0(e) - h0(s))/S, so for even n >= 2A:
    R_W(n) >= 4 * min over corners of [cost - h0(s)/S + h0(sigma t)/S].
usage: potlp2.py W A prefix [tl_corner] [B]   (REMOTE=user@host:dir as in potlp.py)"""
import sys, subprocess, json, os, time
from fractions import Fraction
from math import lcm
import numpy as np
from scipy.optimize import linprog
import corner_pot as cp
W, A, pre = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
TL = float(sys.argv[4]) if len(sys.argv) > 4 else 600; B = float(sys.argv[5]) if len(sys.argv) > 5 else 6
HERE = os.path.dirname(os.path.abspath(__file__))
S = cp.slots_of(W); K = len(S)
chi = lambda m: np.array([(m >> k) & 1 for k in range(K)], dtype=float)
arcs = []  # rows over (w0, w1): coefficient vector, rhs
def add_arc(u, v, c, p):
    row = np.zeros(2 * K)
    if p == 0: row[K:] += chi(v); row[:K] -= chi(u)     # c + h0(u) - h1(v) >= 0
    else: row[:K] += chi(v); row[K:] -= chi(u)          # c + h1(u) - h0(v) >= 0
    arcs.append((row, c))
seen = set()
for line in open(pre + '_zarcs.txt'):
    u, v = (int(t, 16) for t in line.split())
    if (u, v) not in seen: seen.add((u, v)); add_arc(u, v, 0, 0); add_arc(u, v, 0, 1)
sols = []; log = open(pre + f'_potlp2_A{A}.log', 'a')
def say(*a):
    s = ' '.join(str(x) for x in a); print(s, flush=True); log.write(s + '\n'); log.flush()
say('start', time.strftime('%F %T'), 'W', W, 'A', A, 'K', K, 'zero-arc rows', len(arcs))
def lp():
    Aub, bub = [], []
    for phi, c in sols: Aub.append(list(-np.array(phi, dtype=float)) + [0.0] * K + [1.0]); bub.append(c)
    for row, c in arcs: Aub.append(list(row) + [0.0]); bub.append(c)
    res = linprog(np.r_[np.zeros(2 * K), -1.0], A_ub=np.array(Aub), b_ub=np.array(bub),
                  bounds=[(-B, B)] * (2 * K) + [(-50, 50)], method='highs')
    return res.x[:2 * K], res.x[2 * K]
def to_int(w):
    fr = [Fraction(x).limit_denominator(24) for x in w]; sc = 1
    for f in fr: sc = lcm(sc, f.denominator)
    return [int(f * sc) for f in fr], sc
w_int, sc = [0] * (2 * K), 1; best = None
for it in range(400):
    if sols: w, z = lp(); w_int, sc = to_int(w)
    else: z = 50
    st, val, bd, new = cp.solve(W, A, w_int[:K], sc, TL)
    for c, phi in new: sols.append((phi, c))
    say(f'it {it} LP z {z:.4f} scale {sc} corner {st} value {val/sc:.4f} bound {bd/sc:.4f} sols {len(sols)} arcs {len(arcs)}')
    if st != 'OPTIMAL': say('corner not optimal; stop'); break
    if val / sc < z - 1e-6: continue
    wf = pre + f'_pot2_A{A}_w.txt'; open(wf, 'w').write(f'{sc} ' + ' '.join(map(str, w_int)) + '\n')
    if os.environ.get('REMOTE'):
        host, rdir = os.environ['REMOTE'].split(':')
        subprocess.run(['scp', '-q', wf, f'{host}:{rdir}/potw2.txt'], check=True)
        cmd = (f'cd {rdir} && ulimit -v 8000000 && WFILE=potw2.txt STATES=z{W}/z{W}_states.bin OMP_NUM_THREADS=4 '
               f'nice -n 19 ./stripzi_par {W} z{W}/chk2 && echo VIOLFILE && cat z{W}/chk2_viol.txt')
        out = subprocess.run(['ssh', host, cmd], capture_output=True, text=True).stdout
        head, _, vtxt = out.partition('VIOLFILE\n'); open(pre + '_chk2_viol.txt', 'w').write(vtxt); out = head
    else:
        env = dict(os.environ, WFILE=wf, STATES=pre + '_states.bin')
        out = subprocess.run([os.path.join(HERE, 'stripzi_par'), str(W), pre + '_chk2'], env=env, capture_output=True, text=True).stdout
    line = [l for l in out.splitlines() if l.startswith('scale')][0]; say('  strip check:', line)
    if int(line.split()[5]) >= 0:
        say(f'VALID parity potentials, corner OPTIMAL {val/sc}: R_W(n) >= {4*val/sc} for EVEN n >= {2*A}; w = {sc} {w_int}')
        best = (val / sc, sc, w_int); break
    nv = 0
    for l in open(pre + '_chk2_viol.txt'):
        u, v, c, _ = l.split(); u, v, c = int(u, 16), int(v, 16), int(c); add_arc(u, v, c % 1000, c // 1000); nv += 1
    say('  added violated arcs', nv)
json.dump({'best': best, 'nsols': len(sols), 'narcs': len(arcs)}, open(pre + f'_potlp2_A{A}.json', 'w'))
