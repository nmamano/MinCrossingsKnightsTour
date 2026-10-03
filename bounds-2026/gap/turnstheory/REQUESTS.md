# R1 complete — 2026-10-03

KT Lower Bounds certified beta=4/3 in both orientations and both initial
parities; see its FINDINGS.md L3. Turns Theory reran the independent
checks and wrote `PROOF_52_11.md`, for Chief Researcher to send to KT
Verifier. No further finite task is requested until that audit is done.

The original request follows for the record.

# Request R1 to KT Lower Bounds — 2026-10-03

**Priority: test actual boundary-crossing credit before the blocked-run
augmentation.** The new period-4 obstruction kills the blocked-run-only
proposal: its ghost degrees are one, so it has no blocked rows. Do not
spend time on that proposal by itself.

There is a simpler new finite task. The old area inequality uses the
actual outer-column crossing set `B`, then replaces its size by `4n-O(1)`.
Keep its surplus. On side sigma, let `B_sigma` count crossing pairs BOTH
of whose edges have an endpoint in column 0. This is a count of pairs,
not the number of edges. Put

```
D = sum_sigma X_sigma - 4n,
R = sum_sigma B_sigma - 4n.
```

The same path proof gives `4n <= 4E + 2A - 2R + O(1)`, where
`E=X-4n+2`. Thus a strip certificate

```
X_sigma - length + beta*(B_sigma - length)
    >= beta*sum_rows a - C                              (R1)
```

gives `A-R <= E/beta+O(1)` and hence the same coefficient formula
`4+2beta/(2beta+1)`. Beta above one now improves 14/3 through a different
inequality. Test 4/3 first; if it fails, seek any beta>1 or give a cycle.

Use your existing fractional endpoint graph, separate up/down
orientations, both initial parities, and `t=2a`. For each arc, count
`w0`: the crossings introduced on that arc whose TWO edges both touch
column 0. Then for beta=`p/q`, use integer weight

```
q*(4w-1) + p*(4w0-1) - 2p*t.                           (R2)
```

The baseline `-p` applies to EVERY cell transition, just like `-q`.
The endpoint charge `t` still applies only at row end. No extra row
history, tile count, or wider strip is needed. Build `w0` directly from
the new edges and the pending edges used to compute `w`.

Checks against the two known obstructions:

* Your period-4 field has `X_sigma=8`, `B_sigma=8`, and `sum a=4` per
  period in the bad phase. The left side of (R1) is `4+4beta`, which
  exceeds `4beta`. It no longer blocks any beta.
* The old saturated period-one field has crossing rate two, boundary
  crossing rate one, and penalty rate 3/4. It still imposes beta<=4/3.
* Cheap fields have both crossing rates one and penalty zero.

These counts pass `python3 gap/turnstheory/check_boundary_credit.py`.
The proof of the budget reduction is at the top of FINDINGS.md.

If R1 is blocked at beta=1, the next available credit is area slack:
the new period-4 field has four one-quarter overlaps per period, two
triple-covered quarters, and two empty quarters in square column 0.
Do not add that state yet; first extract and inspect the new blocking
cycle. It may have none of that slack.
