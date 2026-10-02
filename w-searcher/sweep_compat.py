import sys, json
from menu_run import go
from classes import compat_classes
kind = sys.argv[1]; Ps = json.loads(sys.argv[2]); Ds = json.loads(sys.argv[3]); tl = float(sys.argv[4])
for name, M, al in compat_classes():
    for D in Ds:
        for P in Ps:
            go(kind, P, D, rule=(M, al), rname=name, tl=tl)
