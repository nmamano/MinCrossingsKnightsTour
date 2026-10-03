# KT Structures, 2026-10-03. BEYOND5 12: evaluate candidate strip / connectivity splits on raw per-side data
# (b5raw.log from b5plus_check.py). Strip form per side: J >= a g + c Nf(d0) + b (N_re - Nf(d0)), J = (X3 - rows) + Q3'/2.
# Connectivity form: 2a g + 2c Nf + 2b Nnear + BQx - 2K >= 4n - C. K, BQx from beyond5_ledger / claim45_K_check.
import json, sys
KB = {'claim36_FOLD_n192.json': (7, 420), 'claim45_U_patched_n192.json': (16, 438), 'claim36_FOLD_n288.json': (7, 548),
      'claim45_U_patched_n288.json': (25, 584), 'LF1_n96.json': (132, 0), 'LF4_n96.json': (132, 0), 'LF5_n104.json': (148, 0),
      'TT16_n72.json': (84, 0), 'H16a_VerticalEdge_off0_n96.json': (132, 0), 'p5_LF1v0_n72.json': (84, 0),
      'p5_LF1v0_n96.json': (132, 0), 'p5_LF1v0_n120.json': (180, 0), 'FOLD24_n96.json': (7, 292), 'FOLDB1_n144.json': (13, 304),
      'FOLDX_n100.json': (11, 268), 'FJOG_n132.json': (17, 1336)}
R = [json.loads(l[4:]) for l in open('b5raw.log') if l.startswith('RAW')]
def ev(a, c, b, d0):
    worst = 1e9; rows = []
    for r in R:
        K, BQx = KB[r['tour']]; n = r['n']; lhs = BQx - 2*K; sl = []
        for s in r['sides']:
            Nf = s[f'Nf{d0}']; Nn = s['Nre'] - Nf
            sl.append(s['J'] - a*s['g'] - c*Nf - b*Nn)
            lhs += 2*a*s['g'] + 2*c*Nf + 2*b*Nn
        rows.append((r['tour'], n, round(min(sl), 1), round(lhs/n, 2), round(lhs - 4*n)))
    return rows
if __name__ == "__main__":
  for a, c, b, d0 in [(2, 1, 0, 2), (2, 1, 1/3, 2), (1, 1, 0, 1), (2, 1, 0, 1), (2, 1, 1/2, 1), ]:
      print(f'a={a} c={c} b={b:.2f} d0={d0}:  tour n min-side-strip-slack C5/n C5-4n')
      for row in ev(a, c, b, d0): print('   ', *row)
  print('--- b limits: per tour, strip b_max = min over sides (slack at b=0 / Nnear), b_need = deficit / (2 Nnear)')
  for a, d0 in [(2, 2), (2, 1), (3, 1), (3, 2)]:
      print(f'a={a} d0={d0}')
      for r in R:
          K, BQx = KB[r['tour']]; n = r['n']; lhs = BQx - 2*K; Nn_t = 0; bm = []
          for s in r['sides']:
              Nf = s[f'Nf{d0}']; Nn = s['Nre'] - Nf; Nn_t += Nn
              sl = s['J'] - a*s['g'] - Nf
              if Nn: bm.append(round(sl/Nn, 3))
              lhs += 2*a*s['g'] + 2*Nf
          print('   ', r['tour'], n, 'C5(b=0)-4n', round(lhs-4*n), 'Nnear', Nn_t, 'b_need', round(max(0, 4*n-lhs)/(2*Nn_t), 3) if Nn_t else '-', 'strip b_max by side', bm, 'min side slack(b=0)', min(s['J'] - a*s['g'] - s[f'Nf{d0}'] for s in r['sides']))
