"""Standalone DRUP proof checker (standard Python only). usage: check_drup.py file.cnf file.drup
Checks every added clause by reverse unit propagation against the current clause database
(deletions 'd ...' are ignored, which is always sound), and requires the empty clause."""
import sys


def main(cnf_path, proof_path):
    clauses = []
    for line in open(cnf_path):
        line = line.strip()
        if not line or line[0] in 'cp':
            continue
        lits = list(map(int, line.split()))
        assert lits[-1] == 0
        clauses.append(lits[:-1])
    nvars = max((abs(l) for c in clauses for l in c), default=0)
    # clause store with watches
    store = []          # list of lists (None if deleted)
    watches = {}        # lit -> list of clause ids
    units = []          # ids of unit clauses (active)
    key_index = {}      # sorted tuple -> list of ids (for deletion)

    def add(c):
        cid = len(store)
        store.append(list(c))
        key_index.setdefault(tuple(sorted(c)), []).append(cid)
        if len(c) >= 2:
            watches.setdefault(c[0], []).append(cid)
            watches.setdefault(c[1], []).append(cid)
        else:
            units.append(cid)
        return cid

    def delete(c):
        ids = key_index.get(tuple(sorted(c)))
        if ids:
            cid = ids.pop()
            store[cid] = None

    def propagate_conflict(assume):
        val = {}
        trail = []

        def assign(l):
            v = val.get(abs(l))
            if v is None:
                val[abs(l)] = l > 0
                trail.append(l)
                return True
            return v == (l > 0)

        for l in assume:
            if not assign(l):
                return True
        for cid in units:
            c = store[cid]
            if c is None:
                continue
            if len(c) == 0:
                return True
            if not assign(c[0]):
                return True
        i = 0
        while i < len(trail):
            l = trail[i]; i += 1
            falselit = -l
            wl = watches.get(falselit, [])
            j = 0
            while j < len(wl):
                cid = wl[j]
                c = store[cid]
                if c is None:
                    wl[j] = wl[-1]; wl.pop(); continue
                if c[0] == falselit:
                    c[0], c[1] = c[1], c[0]
                if c[1] != falselit:      # stale watch
                    wl[j] = wl[-1]; wl.pop(); continue
                other = c[0]
                ov = val.get(abs(other))
                if ov is not None and ov == (other > 0):
                    j += 1; continue
                found = False
                for k in range(2, len(c)):
                    lk = c[k]; vk = val.get(abs(lk))
                    if vk is None or vk == (lk > 0):
                        c[1], c[k] = c[k], c[1]
                        watches.setdefault(c[1], []).append(cid)
                        wl[j] = wl[-1]; wl.pop()
                        found = True
                        break
                if found:
                    continue
                if ov is None:
                    assign(other); j += 1
                else:
                    return True
        return False

    for c in clauses:
        add(c)
    checked = 0; empty = False
    for line in open(proof_path):
        line = line.strip()
        if not line:
            continue
        if line.startswith('d '):
            lits = list(map(int, line[2:].split()))
            assert lits[-1] == 0
            # deletions are ignored (always sound; solvers may delete reason clauses of top-level units)
            continue
        lits = list(map(int, line.split()))
        assert lits[-1] == 0
        c = lits[:-1]
        if not propagate_conflict([-l for l in c]):
            print('FAIL: clause is not RUP:', c)
            return False
        checked += 1
        if not c:
            empty = True
            break
        add(c)
    if not empty:
        # the proof may end without an explicit empty clause; then the database itself must be RUP-empty
        empty = propagate_conflict([])
    if empty:
        print(f'PASS {cnf_path}: {checked} RUP additions verified, empty clause derived (UNSAT).')
        return True
    print('FAIL: no empty clause')
    return False


if __name__ == '__main__':
    ok = main(sys.argv[1], sys.argv[2])
    sys.exit(0 if ok else 1)
