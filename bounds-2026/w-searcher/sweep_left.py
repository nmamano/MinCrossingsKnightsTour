import sys, json
from menu_run import go
from classes import classes
Qs = json.loads(sys.argv[1]); Ds = json.loads(sys.argv[2]); tl = float(sys.argv[3])
for name, M, al in classes():
    for Q in Qs:
        if M and (2 * Q) % M: continue
        for D in Ds:
            go('left', Q, D, rule=(M, al) if M else None, rname=name, tl=tl)
