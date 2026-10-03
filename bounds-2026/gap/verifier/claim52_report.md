# Claim 52: assembled 5n-597 proof and 2-factor theorem — 2026-10-03

**Closed-tour theorem: PASS.** Every closed knight tour on an even n by n board with n>=32 has X>=5n-597 proper unordered crossing pairs.

**Spanning simple 2-factor theorem: PASS.** The same bound holds for every spanning simple knight 2-factor, with X counting all proper unordered crossing pairs, including pairs whose edges belong to different cycles.

The assembled argument preserves the mathematics audited in Claims 50 and 51. The constant 597 is correct. All five listed reproduction commands passed. Two small text corrections below concern the lattice convention and a checker attribution; neither requires a new mathematical input. No proof or blog source was edited.

## 52A. Audited object and assembly

The object was snapshotted as `gap/verifier/claim52_proof_snapshot.md` at 2026-10-03T18:33:57.157099+00:00. Source hashes are in `claim52_sources.json`. The source is `gap/turnstheory/PROOF_5N_V2.md`.

Section 1 retains the exact full-graph tile count. Its D includes holes through the polynomial value at m=0, and the sum is explicitly over board quarters. S is correctly a union of crossing-pair sets. The usable-quarter inequality is the scalar inequality audited in Claim 51, with no hidden disjoint allocation assumption.

Sections 2 and 3 retain the necessary local flux identity, zero circulation, alternating square identity, eight endpoint coefficients, exception and visibility definitions. The endpoint table agrees with the checked table. DOWN uses square row r-1. The passing-case boundary congruence is written explicitly, so the old residue classification is unnecessary.

Section 4 keeps the correct radii, N=2n-60, disjoint squares and disjoint endpoint rows. A kept path has two non-strong ends, is charged, and supplies two bad quarters. A forbidden two-quarter strip overlap would force the correct endpoint's exception or VIS; all such quarters are therefore usable. No small-radius error, deficient-path argument, or private-payment lemma has been omitted from a place where it is still needed. The new proof genuinely does not require them.

Section 5 matches Claim 50's row graph: twelve possible pending edges, degree two in the first two columns, degree at most two in the next two, all needed edges in the row-arc mask, no cycle restriction, and exact crossing ownership. The actual prefix from an empty board cut establishes reachability of each half-side state. The n arc weights sum to the side's crossing count even across the orientation split. Both strong flags are computed on the same graph. The potentials and their interface have the audited values.

Section 6 uses the same keep/discard elimination as Claim 51. It changes only the numerical black-box constant and the resulting theorem constant.

## 52B. Recompute the new constant

For each physical side, the potentials satisfy

    4w-4-4g+h(u)-h(v) >= 0,
    h_up in [-24,0], h_down in [-28,0],
    h_up-h_down in [0,4].

With start, middle and end cut states a,m,z, telescoping gives

    4(X_sigma-n-b_sigma)
      >= (h_up(m)-h_down(m))-h_up(a)+h_down(z)
      >= 0-0-28 = -28.

Hence b_sigma<=X_sigma-n+7. Four physical sides contribute error 28, not 28 per side after rescaling. Their overlap correction is at most 1104: opposite strips have no common edges in the size range, and a pair common to adjacent strips lies in their 4-by-4 corner square. There are 24 possible knight edges there, giving at most binom(24,2) per corner. This estimate does not depend on which graph components contain the edges.

Therefore

    b <= sum_sigma X_sigma-4n+28
      <= s-4n+1104+28
      = T+1130,
    C = 28+1104-2 = 1130.

Now M=N-z, z<=b and 4E>=2M+2T imply

    4E >= 2(N-z)+2(b-C) >= 2N-2C,
    E >= n-30-C/2,
    X >= 5n-(32+C/2) = 5n-(32+565) = 5n-597.

All quantities and constants have the correct units. There is one global C; no per-run or per-chamber error appears. The new constant uses a valid conservative side estimate, not an unproved sharpness assertion. For smaller positive even n<32, 5n-597 is negative, so the same numerical inequality follows from X>=0.

## 52C. Why the 2-factor theorem is valid

The required hypothesis is a SPANNING SIMPLE degree-two subgraph of the board's knight graph. Counting only crossings within each cycle would be a different statistic and would not satisfy the proof's identities.

1. **Mass and pair counts.** Degree two gives exactly n^2 edges. Each distinct edge contributes four quarters. At a quarter of multiplicity m, binom(m,2) counts every unordered pair of covering edges, regardless of component. Thus D+X1=2E and the usable-quarter bound remain valid with cross-component crossings included.

2. **Flux.** Edges are oriented by the checkerboard sign chi, not by following a tour. The one-edge identity is linear in the selected edge indicators. At any board vertex the graph's signed divergence is chi(v) deg_H(v)=2chi(v). Adding the full unit lattice contributes another 4chi(v), so the combined divergence is 6chi(v), zero modulo three. A finite-set boundary sum telescopes edge by edge; no component needs to be connected to any other component.

3. **Candidate paths meeting several cycles.** A candidate is a path in the grid of square centres, not a path in H. Its flux sums the contributions of every graph edge it crosses. A candidate may cross many cycles, revisit the same cycle, or have quarter multiplicities formed by several cycles. The boundary-divergence identity and local multiplicity formula still apply to their sum. Passing endpoint tests force its total charge to be nonzero. If all its adjacent quarters were good, every local dual step would have zero flux modulo three, a contradiction. Component membership cannot cancel this implication.

4. **Endpoint filtering and overlap exclusion.** The endpoint coefficient identity uses deg_H(0,r)=2, not a traversal of a Hamiltonian cycle. The exception/VIS rules refer to geometric pairs of selected edges and include pairs from different cycles. The square and row disjointness are fixed board geometry.

5. **Finite strip input.** The restriction of a 2-factor has the same exact degrees in columns zero and one and upper degree bounds in columns two and three. It can have a complete component inside the strip, but the cut graph has no labels or cycle rejection. The same induction from the empty bottom cut maps every actual restriction to the graph. New/pending and new/new crossing counts include all components. No connectivity filter is hidden in either the author checker or the independent reconstruction.

6. **Final counts.** The corner union correction, z<=b and scalar elimination are set/cardinality arguments. They impose no additional topological hypothesis.

These points discharge the six re-check items in PROOF_5N_SIMPLE section 7. Claims 50 and 51 provide the finite and hand audits respectively; the assembly does not reintroduce the old forest assumption.

### Additional disconnected example

As an implementation check, `claim52_check.py` makes a degree-preserving two-edge change to the saved FOLD n=144 tour that splits it into two cycles of lengths 19,494 and 1,242. The saved spanning simple 2-factor has X=1030, including 72 crossing pairs between components. Of its 219 kept candidates, 55 have squares meeting tiles from both cycles.

The script checks every actual side row against the cut-state transitions, verifies empty start/end cuts and equality of side arc weights with direct side crossing counts, and rechecks the scalar keep/usable-quarter argument. All pass. This example is supporting evidence; the degree-only argument above proves the theorem for all spanning simple 2-factors.

## 52D. Reproduction — all listed commands PASS

Each displayed command was run from an isolated copy rooted at a folder named `bounds-2026`, containing the same relative sources and the saved fixtures required by the independent checker. The copy uses the research virtual environment. Generated potentials and reports remained inside the verifier's isolated directory, so the shared source outputs were not overwritten.

| Command | Exit | Seconds, 2026-10-03 |
| --- | ---: | ---: |
| `python3 w-turnstheory/check_knight_tiles.py` | 0 | 0.42 |
| `python3 w-turnstheory/check_corner_box.py` | 0 | 0.08 |
| `python3 w-turnstheory/check_square_defects.py` | 0 | 0.44 |
| `.venv/bin/python gap/lowerbounds/simple_strip/check_cut_certificate.py` | 0 | 5.38 |
| `python3 gap/verifier/claim50_check.py` | 0 | 8.51 |

The graph output is 3,136 states and 48,510 arcs; both potentials stabilize in eight passes, with ranges [-24,0]/[-28,0], interface [0,4], and side error 28 in units of one quarter. The independent script also checks twelve actual side strips and the optional identity (K).

This is a reproduction with the local repository sources and installed research environment, not a fresh dependency installation or a check of a remote public checkout. The author command needs NumPy. The independent command needs only the standard library and its three repository fixture files.

Logs are `claim52_command_0.log` through `_4.log`; the command report is `claim52_commands.json`. The added exception/2-factor check is reproducible with

    python3 gap/verifier/claim52_check.py

Its report is `claim52_check.json`, and its fixture is `claim52_twofactor_n144.json`.

## 52E. Two precise text corrections

The numerical theorems pass. These changes make the standalone proof and reproduction claims exact.

**1. State the full-lattice convention and restrict the divergence sum.** Section 2's degree-plus-four identity uses all unit edges of the infinite square lattice, including those leading outside the board. The degree-two condition applies only to board vertices. Replace the opening orientation sentence and the start of the finite-set sentence by:

> Orient the graph edges and all unit edges of the infinite square lattice from chi=1 to chi=-1.

> For a finite vertex set A contained in the board, the total boundary flux is `sum_(v in A) chi(v)*(deg_H(v)+4)=6 sum_(v in A) chi(v)`, hence zero modulo three.

All vertex sets needed for the candidate corner argument are contained in the board. This makes explicit the convention inherited from the audited proof; it does not change the argument.

**2. Correct the outer-column exception check attribution.** Claim 50's standalone checker derives the seven VIS pairs per orientation, but it does not independently enumerate the uniqueness of the outer-column exception. Its exception indicator uses the specified pair. That uniqueness was checked in Claim 42 and was independently rechecked here: the sole up pair touching a depth-one candidate square is `(0,0)--(2,1), (0,1)--(2,0)`, with one overlap quarter in square column zero and one in column one. Its reflection is the sole down pair, at square row -1. Neither reaches square column two.

Replace section 4's sentence “The exact exception/VIS enumeration is part of the independent strip check in Section 7” by:

> The outer-column exception enumeration is audited in Claims 42 and 52. The independent strip checker in Section 7 derives both VIS lists from tile geometry.

In section 7 replace “it checks the strip certificate and exact exception/VIS geometry without author imports” by:

> It checks the strip certificate and derives both VIS lists without author imports.

If the displayed commands are intended to rerun every local enumeration directly, add `python3 gap/verifier/claim52_check.py` to that list. Otherwise the cited prior geometry audits already supply the stated fact. No new package is needed for the added command.

## Proof size and finite inputs

The assembled proof consists of tile incidence counting, a local flux and passing-endpoint lemma, the strong-end filter, one scalar inequality and one cut-state certificate. The only substantial finite graph has 3,136 states and 48,510 arcs. The small tile, endpoint, square, exception and VIS checks are exact geometric checks. There is no forest state, private-payment machinery, higher-width strip certificate, or beyond-5n hypothesis. Both theorem verdicts are PASS with the two presentation corrections above recorded for the author.
