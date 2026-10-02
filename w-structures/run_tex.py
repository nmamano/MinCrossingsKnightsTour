import sys
from texedge import TexEdge, solve
steps_name = sys.argv[1]; D = int(sys.argv[2]); tl = float(sys.argv[3]); lanes = sys.argv[4] == '1' if len(sys.argv) > 4 else True
PAT = {'h1': [2, -2], 'h2': [2, 2, -2, -2], 'h1x2': [2, -2, 2, -2], 'h3': [2,2,2,-2,-2,-2], 'h1x4': [2,-2]*4, 'h2x2': [2,2,-2,-2]*2}
steps = PAT[steps_name]
for off in range(4 if lanes else 1):
    st = TexEdge(steps, D, off=off)
    r = solve(st, tl=tl, lanes=lanes)
    print(steps_name, 'P', st.P, 'D', D, 'off', off, 'lanes', lanes, r['status'], r['time'], 'X', r.get('X'), 'T', r.get('T'), 'bound', r.get('bound'),
          'X/row', (r['X'] / st.P) if 'X' in r else None, flush=True)
