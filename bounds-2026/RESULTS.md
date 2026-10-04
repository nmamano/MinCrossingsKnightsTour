# Knight's tours: proved results

2026-10-02. This is the entry point to the proofs and their checks.
All boards below are n by n. X counts unordered pairs of properly crossing
move segments; shared endpoints do not count. T counts turns in a closed
tour. A 2-factor is a spanning simple degree-two subgraph and can contain
several cycles. Upper bounds give one Hamiltonian cycle.

| Result | Status | How checked |
| --- | --- | --- |
| X <= 19n/3+142 | Proved, even n>=96 | All-size insertion proof; complete path matchings and local counts |
| X <= 9n+7 | Proved, even n>=48 | All-size insertion proof; finite base tours and band counts |
| X <= 343n/48+671/24 | Proved, even n>=96 | All-size insertion proof; all 24 residue classes |
| X >= 5n-597 | Proved, closed tours and 2-factors, even n>=32 | Tile count; 3,136-state cut-state certificate |
| X >= 5n-612 | Proved, closed tours, even n>=32 (older proof) | Quarter payments; strip stability certificate |
| X >= 14n/3-407 | Proved, closed tours, even n>=32 | Tile and path count; exact strip potentials |
| X >= 4n-2 | Proved, every tour and 2-factor | Tile-area proof; exact geometry; unconditional Lean theorem |
| T = 8n-17 (n = 2 mod 8), T = 8n-16 (n = 6 mod 8) | Constructed, even n>=48 in these classes | All-size insertion proof, period 16; exact turn count |
| T = 8n-14 | Constructed, even n>=48 | All-size insertion proof; exact turn count |
| T >= 8n-28 | Proved, tours and 2-factors, n>=8 | Four-column count; exact corner certificate; unconditional Lean theorem |
| T >= 8n-64 | Proved, tours and 2-factors, n>=8 | Four-column count; unconditional Lean theorem |

Finite checks support the stated all-size arguments; sampling board sizes
alone is not the proof. The commands below run from the project root,
use Python 3, and need no solver. Lean status is stated separately; these
commands do not rebuild Lean.

## Crossing upper bound: 19n/3+O(1)

For every even n>=96 there is a closed tour with X<=19n/3+142.
The fold construction has X(n+24)-X(n)=152. Its path matching alternates
between two valid states, so this recurrence holds for all such sizes.

Proof: [PROOF_fold.md](w-turnstheory/PROOF_fold.md).
Audit: Claims 12 and 21(B) in [FINDINGS.md](w-verifier/FINDINGS.md).
Lean: no formal construction theorem is claimed.

```sh
python3 w-turnstheory/check_fold_proof.py
```

## Crossing upper bound: 9n+O(1)

For every even n>=48, the H16a construction gives a closed tour with
X<=9n+7. Its crossing count increases by 216 when n increases by 24.

Proof: [PROOFS.md, Sections 1-4](w-turnstheory/PROOFS.md).
Audit: Claims 1, 4, and 7 in [FINDINGS.md](w-verifier/FINDINGS.md);
Claim 7 checks the complete all-size insertion argument.
Lean: no formal construction theorem is claimed.

```sh
python3 w-turnstheory/check_upper_proofs.py
```

## Crossing upper bound: 343n/48+O(1)

For every even n>=96, the LF4 construction gives a closed tour with
X=343n/48+b[n mod 48]. The exact 24 constants are in the proof;
their maximum is 671/24. Thus X<=343n/48+671/24.

Proof: [PROOFS.md, Section 5](w-turnstheory/PROOFS.md).
Audit: Claim 8 in [FINDINGS.md](w-verifier/FINDINGS.md).
Lean: no formal construction theorem is claimed.

```sh
python3 w-turnstheory/check_lf_proof.py
```

## Crossing lower bound: 5n-597

Every closed tour on an even board n>=32 has X>=5n-597. The same bound
holds for every spanning simple knight 2-factor, where crossing pairs
from different cycles count as well as pairs from the same cycle.

Proof: [PROOF_5N_V2.md](gap/turnstheory/PROOF_5N_V2.md).
Audit: Claims 50, 51 and 52 in [FINDINGS.md](w-verifier/FINDINGS.md).
The two text corrections from Claim 52 have been applied.
The computer input is the cut-state strip certificate with 3,136 states
(about 4 s; it needs NumPy). Claim 50 checks it again with the Python
standard library only.

An older proof of X>=5n-612 for closed tours,
[PROOF_5N.md](gap/turnstheory/PROOF_5N.md) (Claim 42), stays in the repository.

```sh
python3 w-turnstheory/check_knight_tiles.py
python3 w-turnstheory/check_corner_box.py
python3 w-turnstheory/check_square_defects.py
.venv/bin/python gap/lowerbounds/simple_strip/check_cut_certificate.py
python3 gap/verifier/claim50_check.py
python3 gap/verifier/claim52_check.py
```

## Crossing lower bound: 14n/3-O(1)

Every closed tour on an even board n>=32 has X>=14n/3-407.
The theorem is unconditional: its strip stability input has an exact
finite certificate. This statement is not asserted for arbitrary
2-factors.

Proof: [PROOF_crossings_lower.md](w-turnstheory/PROOF_crossings_lower.md).
Audit: Claims 19, 20, and 21(B) in [FINDINGS.md](w-verifier/FINDINGS.md).
The four final document corrections from Claim 21 have been applied.

Lean: [KT.ClosedTour.fourteen_mul_le_of_stability](ktlean/Ktlean/TourMain.lean)
is conditional on strip stability. With the certified stability constant
1131 it gives X>=14n/3-421. The strip certificate and its connection to
the strip walk are not formalized in Lean. This is distinct from the
unconditional, independently audited proof with constant 407. See the
[Lean theorem statement and scope](ktlean/README.md).

```sh
python3 w-turnstheory/check_crossings_lower.py
```

## Crossing lower bound: 4n-2

Every closed tour, and every spanning 2-factor of the knight graph, has
X>=4n-2. No size threshold or separate evenness hypothesis is needed.
The statement is conditional only on the existence of the tour or
2-factor.

Proof: [PROOF_crossings_lower.md, Section 1](w-turnstheory/PROOF_crossings_lower.md).
Audit: Claim 9 and the tile-area part of Claim 20 in
[FINDINGS.md](w-verifier/FINDINGS.md).
Lean: [KT.ClosedTour.four_mul_sub_two_le_numCrossings and
KT.TwoFactor.four_mul_sub_two_le_numCrossings](ktlean/Ktlean/Crossings.lean)
are unconditional, with only the standard axioms listed in the
[Lean README](ktlean/README.md). The command checks the finite geometry
used by the area proof.

```sh
python3 w-turnstheory/check_knight_tiles.py
```

## Turn upper bound: 8n-17 and 8n-16 for n = 2, 6 mod 8

For every even n>=48 with n = 2 mod 8 there is a closed tour with exactly
T=8n-17, and for every even n>=48 with n = 6 mod 8 one with exactly T=8n-16.
For n = 0, 4 mod 8 the best known value is still 8n-14 (next section).

Proof: [TURNS_IMPROVED.md](TURNS_IMPROVED.md) (construction; the block insertion of
[TURNS_PROOFS.md, part F](TURNS_PROOFS.md#f-one-closed-tour-for-every-n-block-insertion)
with period 16, done by a general checker).
Audit: Claim 55b ([report](gap/verifier/claim55b_report.md), the checker) and
Claim 56 ([report](gap/verifier/claim56_report.md), both bounds).
Lean: no formal construction theorem is claimed.

```sh
python3 w-integrator/allsize_check.py w-integrator/pipeline/ES_res2 --partial
python3 w-integrator/allsize_check.py w-integrator/pipeline/ES_res6 --partial
```

## Turn upper bound: 8n-14

For every even n>=48, the TT16 construction gives a closed tour with
exactly T=8n-14. This is an upper bound on the minimum, not a claim that
the construction is optimal. With the lower bound 8n-28, this proves the
paper's conjecture (a leading factor of 8) and shows that it is tight.

Proof: [turns paper, Theorem 1(b) and construction](writeup/turns/main.pdf),
or [TURNS_PROOFS.md, parts D-F](TURNS_PROOFS.md#d-the-tours-complete-construction)
(construction, turn count, [block insertion](TURNS_PROOFS.md#f-one-closed-tour-for-every-n-block-insertion)),
with the all-size connectivity argument in
[PROOFS.md, Sections 1-4](w-turnstheory/PROOFS.md).
Audit: Claims 6, 7, and 16 in [FINDINGS.md](w-verifier/FINDINGS.md).
Lean: no formal construction theorem is claimed.

```sh
python3 w-turnstheory/check_upper_proofs.py
```

## Turn lower bound: 8n-28

For every n>=8, every closed tour and every spanning 2-factor has
T>=8n-28. Therefore, for every even n>=48,

    8n-28 <= T_min(n) <= 8n-14.

In particular T_min(n)/n tends to 8 through even n.

Proof: [turns paper, lower bound and corner certificate](writeup/turns/main.pdf),
or [TURNS_PROOFS.md, part C](TURNS_PROOFS.md#c-the-corner-certificate-and-8n---28).
Audit: Claim 16 in [FINDINGS.md](w-verifier/FINDINGS.md); the Lean proof: Claim 54.
Lean: [KT.ClosedTour.eight_mul_sub_28_le_numTurns](ktlean/Ktlean/Turns28.lean)
and `KT.TwoFactor.eight_mul_le_numTurns_add_28` are unconditional, with only
the standard axioms; see [Lean scope and axioms](ktlean/README.md). The command
checks all 209 local inequalities in the printed corner certificate.

```sh
python3 writeup/turns/check_corner.py
```

## Turn lower bound: 8n-64

For every n>=8, every closed tour and every spanning 2-factor has
T>=8n-64. Each four-column side strip has at least 2n turns; subtracting
the four corner overlaps proves the bound.

Proof: [turns paper, four-column lemma and its first theorem](writeup/turns/main.pdf),
[TURNS_PROOFS.md, part B](TURNS_PROOFS.md#b-the-four-column-lemma-and-8n---64),
or the [one-page argument in FINDINGS, Section 1](w-turnstheory/FINDINGS.md).
Audit: Claim 2 in [FINDINGS.md](w-verifier/FINDINGS.md).
Lean: [KT.ClosedTour.eight_mul_sub_64_le_numTurns](ktlean/Ktlean/Tour.lean)
and `KT.TwoFactor.eight_mul_le_numTurns_add` are unconditional;
see [Lean scope and axioms](ktlean/README.md). The command checks all
77 allowed local pairs and supporting finite tour examples.

```sh
python3 w-turnstheory/check_proof.py
```

## What is not proved

- The exact minimum turn count: the sharp constant c in T_min(n) = 8n - c lies between
  17 and 28 for n = 2 mod 8, 16 and 28 for n = 6 mod 8, and 14 and 28 for n = 0, 4 mod 8.
- The exact minimum crossing coefficient between 5 and 19/3.
- A lower bound of 19n/3 for every construction in the fold family.
- The general carrier lower bound and its fold-family consequence in
  [Claim 17](w-verifier/FINDINGS.md). The audited conditional counting
  argument does not supply its missing transport and boundary hypotheses.
- An all-size jog-band construction with 16n/3+O(log n) crossings.
- An unconditional Lean proof of the full 14n/3 lower bound: strip
  stability remains an explicit hypothesis of that formal theorem.

## Reproduction record

Command runs for this entry point are recorded in
[results_checks.json](w-turnstheory/results_checks.json), with a separate
text log per command. The shared TT16/H16a command is listed under both
results and needs only one run. **All seven distinct commands passed on
2026-10-02**, run sequentially with one process at a time. Every recorded
exit code is zero. No new Lean build was run for this entry point.
