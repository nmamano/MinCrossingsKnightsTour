import sys, json
from menu_run import go
from classes import classes
Ps = json.loads(sys.argv[1]); Ds = json.loads(sys.argv[2]); tl = float(sys.argv[3])
only = sys.argv[4].split('|') if len(sys.argv) > 4 else None
for name, M, al in classes():
    if only and not any(name.startswith(o) for o in only): continue
    for P in Ps:
        if M and P % M: continue
        for D in Ds:
            go('bottom', P, D, rule=(M, al) if M else None, rname=name, tl=tl)
