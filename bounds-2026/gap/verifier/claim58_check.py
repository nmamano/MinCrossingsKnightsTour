#!/usr/bin/env python3
"""Independent Claim 58 check. Python standard library only; run from repo root."""
import hashlib
import json
from pathlib import Path

MANIFEST = Path('gap/structures/tmin/single_tours.json')
EXPECTED = [24, 28, 34, 38, 44, 48, 54, 58, 64, 68, 74, 78, 88, 98]

def require(condition, message):
    if not condition:
        raise ValueError(message)

def check(entry):
    n = entry['n']
    require(type(n) is int and n > 0, 'invalid n')
    raw = Path(entry['file']).read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    require(digest == entry['sha256'], 'SHA-256 mismatch')
    tour = json.loads(raw)
    require(type(tour['n']) is int and tour['n'] == n, 'board metadata mismatch')
    order = tour['order']
    require(type(order) is list and len(order) == n*n, 'incorrect order length')
    for p in order:
        require(type(p) is list and len(p) == 2, 'invalid coordinate shape')
        require(all(type(x) is int and 0 <= x < n for x in p), 'invalid coordinate')
    points = [tuple(p) for p in order]
    require(set(points) == {(r,c) for r in range(n) for c in range(n)}, 'coverage or uniqueness failure')
    moves = []
    for i, (r,c) in enumerate(points):
        rr, cc = points[(i+1) % len(points)]
        move = (rr-r, cc-c)
        require(sorted(map(abs, move)) == [1,2], f'illegal cyclic edge {i}')
        moves.append(move)
    turns = sum(moves[i-1] != moves[i] for i in range(len(moves)))
    cross_turns = sum(moves[i-1][0]*moves[i][1] != moves[i-1][1]*moves[i][0]
                      for i in range(len(moves)))
    require(turns == cross_turns, 'two turn recounts disagree')
    for label, data in [('manifest', entry), ('tour', tour)]:
        require(type(data['T']) is int and data['T'] == turns, label + ' T mismatch')
        require(type(data['T_minus_8n']) is int and data['T_minus_8n'] == turns-8*n,
                label + ' offset mismatch')
    require(Path(entry['file']).read_bytes() == raw, 'tour changed during check')
    return dict(n=n, status='PASS', vertices=len(points), cyclic_knight_edges=len(moves),
                T=turns, T_minus_8n=turns-8*n, sha256=digest, file=entry['file'])

def main():
    raw = MANIFEST.read_bytes()
    manifest = json.loads(raw)
    require(sorted(e['n'] for e in manifest['entries']) == EXPECTED, 'unexpected entry set')
    results = []
    for entry in manifest['entries']:
        try:
            results.append(check(entry))
        except (ValueError, KeyError, TypeError, OSError) as exc:
            results.append(dict(n=entry.get('n'), status='FAIL', reason=str(exc)))
    require(MANIFEST.read_bytes() == raw, 'manifest changed during check')
    output = dict(date='2026-10-04', manifest_sha256=hashlib.sha256(raw).hexdigest(), results=results)
    print(json.dumps(output, indent=2))
    return 0 if all(r['status'] == 'PASS' for r in results) else 1

if __name__ == '__main__':
    raise SystemExit(main())
