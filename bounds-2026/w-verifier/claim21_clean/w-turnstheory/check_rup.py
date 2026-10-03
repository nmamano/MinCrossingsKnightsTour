"""Check a reverse-unit-propagation UNSAT certificate with standard Python only."""
from pathlib import Path
root=Path(__file__).parent
clauses=[]
for line in (root/'local_long_edge.cnf').read_text().splitlines():
    if not line or line[0] in 'cp':continue
    ls=list(map(int,line.split()));assert ls[-1]==0
    clauses.append(tuple(ls[:-1]))

def contradiction(assumptions):
    truth={}
    def setlit(lit):
        k=abs(lit);v=lit>0
        if k in truth:return truth[k]==v
        truth[k]=v;return True
    for lit in assumptions:
        if not setlit(lit):return True
    while True:
        changed=False
        for clause in clauses:
            remaining=[];satisfied=False
            for lit in clause:
                k=abs(lit)
                if k not in truth:remaining.append(lit)
                elif truth[k]==(lit>0):satisfied=True;break
            if satisfied:continue
            if not remaining:return True
            if len(remaining)==1:
                old=len(truth)
                if not setlit(remaining[0]):return True
                changed|=len(truth)>old
        if not changed:return False

checked=0;empty=False
for line in (root/'local_long_edge.drup').read_text().splitlines():
    if not line or line.startswith('d '):continue
    ls=list(map(int,line.split()));assert ls[-1]==0
    clause=tuple(ls[:-1])
    assert contradiction([-lit for lit in clause]),('not RUP',clause)
    clauses.append(clause);checked+=1
    if not clause:empty=True
assert empty
print(f'PASS: all {checked} proof additions are RUP; the final empty clause proves UNSAT.')
