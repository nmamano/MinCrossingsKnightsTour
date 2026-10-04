# Claim 55: generalized all-size upper-bound checker

Audit date: 2026-10-04. Reviewer: KT Verifier (Astra).

## Verdict

**FAIL as an unconditional certificate checker for every input it accepts.** There is a reproduced wrong-size fallback bug. Also, the generalized insertion argument needs explicit geometric preconditions that the checker does not fully enforce.

**PASS for the three supplied test families under the additional geometric checks in this audit:** TT16 gives `8n - 14`; `selftest_L106b` and `selftest_swap` give at most `8n - 13`, for every even n ≥ 48. This audit does not invalidate the earlier TT16 proof. The new generalized tool needs changes before its PASS alone can certify an arbitrary new corner set.

## Audited versions

Source snapshots are in `gap/verifier/claim55_run/`:

- `allsize_check.py`: SHA-256 `8624765d287f640d7780aec2f603b5510d414b981c5d9f5c4b8cf954beeb8f2c`.
- `allpipe.py`: SHA-256 `949646fb63f54a0e747c161b4954efbce879571c427bf808980bc08a8e925628`.

The worker's source files and existing pipeline outputs were not edited. Tests use copied data and separate output directories. All computations use at most two cores.

## Blocking defect: a fallback need not be an n by n tour

At `allsize_check.py:198`, the fallback is decoded using `len(td['tour'])`, then checked as a graph. Neither `td['n']`, the row count, the row lengths, nor the graph's vertex set is checked against the requested n. `validate(g)` verifies one cycle on the supplied graph, not that it covers the requested board.

Reproduction in `claim55_adversarial.py`:

1. Copy the valid TT16 residue files.
2. In residue 0, add the redundant bottom-band override `BL:48,0`, using its normal moves at n=56. It is harmless at n=56,64,... but off-board at n=48. This forces the fallback for n=48.
3. Put an independently available, valid 16 by 16 knight tour under `tours/selftest_TT16_n48.json`, with metadata `n=48`.
4. Run the unchanged checker.

Observed result: exit 0 and `PASS: T(n) <= 8n + (-14) for every even n >= 48`. Its report includes `[48, 234, "tour file"]`, although that witness contains only 256 cells. A true 48 by 48 tour has at least 356 turns by the established lower bound, so 234 cannot be a valid count for that board.

This does **not** refute the numerical TT16 upper bound, which is already proved. It shows that this checker can certify a base case without a witness for that case.

Evidence: `claim55_run/bad_fallback_size.log`, its `allsize_checks.json`, and `adversarial_summary.log`. The same transplant with no fallback is correctly rejected. Missing residue files, inconsistent phases, and an illegal corner move are also correctly rejected.

Required fix: before decoding a fallback, require `td['n'] == n`, exactly n rows, exactly n cells per row, and exactly two distinct valid move codes per cell. After decoding, require the vertex set to be exactly `{0,...,n-1}²`. A regression test must reject this copied 16 by 16 witness, even when its metadata says 48.

## What the matching argument proves

The `slab` walk correctly obtains the pairing of its boundary ports and rejects a cycle wholly inside the slab through the `seen == vertices` check. Its port names record the side band, both endpoint depths, and both line offsets. In a valid periodic gap, these are sufficient to identify a physical seam edge uniquely.

`compose` treats the seam as degree-two internal vertices and retains the induced outer pairing. It rejects a component with no outer port. I independently checked all 11,025 pairs of perfect matchings on four left and four right ports with a separate connected-component implementation. Results agree: 9,648 valid compositions and 1,377 rejections for internal cycles. See `claim55_compose.py` and `claim55_run/compose.log`.

Let `q=s/w`. The actual condition is `M^(1+q)=M`, with every intermediate composition checked for a new cycle. For q=1 this is `M²=M`. Associativity and repetition of the same verified q-step composition give `M^(1+kq)=M` for every k≥0, without introducing a closed component. Thus adding s lines to a *uniform periodic gap* preserves its connection pattern and introduces no new cycle.

What is not sufficient on its own is checking the slab at just N and N+s. One must also know that the slab can be repeated at every later size, and that the rest of the graph, after suppressing straight interior paths, has the same connections. This follows from the geometric hypotheses below. The source checks clearance from the supplied zones, but does not independently check all those hypotheses: in particular, it does not enforce coverage of band overlaps, a stable corner radius, the correct three band-pair regimes, or a slab width that prevents skipped edges.

I found no error in `compose` or its no-new-cycle test. The failure is in the scope of accepted certificates, not that finite gluing computation.

## Exact sufficient preconditions for an all-n proof

These are conservative, explicit sufficient conditions, not a claim that every condition is necessary. Under them, the successful checks yield the stated theorem.

1. **Execution and input semantics.** Run Python with assertions enabled. Period p is a positive even integer; there is exactly one residue file for each even residue modulo p. All templates are nonempty rectangular arrays of two distinct legal knight moves, with the stated fixed phases. All residue files use the same templates and phases. The family outside its fixed anchored zones is exactly the straight field plus these four periodic bands, as implemented by `graph`.

2. **Stable corners.** Decode inward coordinates as `i=dx` on the left, `i=-1-dx` on the right, `j=dy` on the bottom, and `j=-1-dy` on the top. Every zone cell has nonnegative i,j and lies in a fixed R by R corner box. Take R at least the four band depths too. Zone cells do not alias. Each corner shape contains the full overlap rectangle of its two incident bands. For each induction class, choose N≥2R+6. This keeps all corner corrections, band overlaps, and their adjacent knight edges separated from the opposite sides for every later size. Corner vectors and shapes stay fixed in their own residue file.

3. **Correct, sufficiently wide gaps.** Let `ell=x+2y`, `w=lcm(PB,PT,2QL,2QR)`, and `s=lcm(p,w)`. Require w≥5 (or explicitly handle every edge that skips a slab). A knight edge changes ell by at most 5; width at least 5 prevents a jump from below the slab to above it with neither endpoint inside. The source's slab routine does not record such bypass edges when the width is smaller.

   In each gap k=0,1,2, both slab boundaries have the source's six-line clearance from the neighboring zone spans. They must also lie beyond/before the corresponding band-overlap spans. At board size N, these four overlap spans are:

   ```text
   BL: [0,                    WL-1 + 2(DB-1)]
   BR: [N-WR,                 N-1 + 2(DB-1)]
   TL: [2(N-DT),              WL-1 + 2(N-1)]
   TR: [N-WR + 2(N-DT),       3N-3]
   ```

   Require `a >= max_overlap[k] + 6` and `a+w <= min_overlap[k+1] - 6`, in addition to the zone-span bounds. These put the three slabs in the bottom/left, left/right, and right/top regimes, respectively. The growing cuts `a+k*s` remain in those regimes; the intervening gaps expand and the exceptional pieces stay anchored.

4. **Local periodicity and consistency.** The infinite-band checks must pass, including reciprocal incidences with the straight field. Translating ell by w advances horizontal band coordinates by w and vertical band coordinates by w/2; the divisibility in w preserves all phases. Changing n by s preserves the residue, corner environments, and band phases. Interior paths have zero turns; lengthening them changes neither their endpoint pairing nor their turn contribution.

5. **Finite bases on the right boards.** For every even class modulo s, check every required even n from 48 through N+s as an actual n by n Hamiltonian knight cycle. A separate directly solved tour may cover an exceptional n<N, but its dimensions and vertex set must be checked. Both N and N+s must use the anchored family, as the source requires. These cases cover all finite exceptions and start every induction class.

6. **Transfer and no-cycle checks.** In each of the three gaps, check equal port alphabets, full vertex coverage, the identity `M^(1+s/w)=M`, and equality with both the width-w and width-(w+s) slabs at N+s. Together with conditions 2–4, these are repeatable gap replacements, and the unchanged contracted remainder connects the replacement paths into the same single cycle.

7. **Exact cost.** Each band's added length is s, a multiple of its period. Its added turns are `(s/period) * turns_per_period`. The separated corner and overlap corrections are unchanged, so the total increment is exactly dT at every induction step, not just the checked first step. Require the integer equality `dT == 8*s`; retain the finite `T(N+s)-T(N)==dT` check as a consistency test. Then every class keeps its value of `T-8n`. Taking the maximum over all checked finite cases gives the announced c.

`claim55_geometry.py` checks the extra geometric conditions for all three supplied families and the period-16 test below. All pass. Their minimum induction base is 96; all have ample room for their corner radius. Thus their existing slab checks can be used with the geometric argument above.

## Period found by allpipe

`allpipe.py:169–180` compares outside matchings only through `max(nmax,200)+100`, normally 300. This is evidence for a period and a useful way to select residue data. It is **not** a proof of that period for unbounded n.

The all-size proof does not need to assume this empirical period: it checks every even class modulo s and uses the fixed residue file along steps of s. If s>p, the induction proves repetition under s, not necessarily the stronger assertion that the outside matching has period p. The pipeline's period and `n_stable` labels should retain their finite-check qualification unless a separate proof establishes them.

`allpipe` is a candidate generator. Its `DONE`/`SUMMARY.md` is not a theorem: it can record failed sizes, and its displayed worst constant excludes those failures. Require the independent checker and the preconditions above before publishing an all-n result.

## Reproduction and independent recounts

The unmodified checker was run on copied test folders. It reports:

| Family | constants by residues 0,2,4,6 modulo 8 | worst constant |
|---|---|---:|
| selftest_TT16 | -14, -14, -14, -14 | -14 |
| selftest_L106b | -14, -13, -14, -13 | -13 |
| selftest_swap | -14, -14, -13, -14 | -13 |

The earlier folder `selftest_L106` is not the improved L-shape self-test: its summary has worst constant -4. This audit uses `selftest_L106b`, which is the -13 family identified by the worker's result.

`claim55_tests.py` separately reconstructs the band and corner graphs, checks exact board coverage, distinct degree two, knight edges, reciprocity, and one cycle, and counts turns with an integer determinant. For each family it checks all 32 even sizes 48..110, plus 192,194,196,198 and 312,314,316,318: 40 sizes per family, 120 independent checks. All counts agree. At stored sizes, the reconstructed edge sets also agree with the stored tours and their count metadata.

I also doubled the declared horizontal template periods without changing the pattern. This gives p=8, w=16, s=16 and exercises s>p. The checker reports TT16's -14 again, and the extra geometric checks pass. This test does not establish correctness for every possible period-16 pattern; it covers the generalized step handling on a controlled input.

The TT16 `allpipe` workflow was also rerun from four supplied bases (56,58,60,62), with only its output/menu directory redirected to the audit folder. It found period 8 from 48 in its finite outside-matching scan, produced all 32 tours for 48..110 without a solve, and the unchanged all-size checker accepted the regenerated residue files. All 32 regenerated tours were independently recounted and validated. See `claim55_pipeline_run.py`, `claim55_run/pipeline_run.log`, and `pipeline_allsize.log`. The two CP-SAT self-tests were audited from their existing output certificates; their solver searches were not rerun.

Logs and count data are in `claim55_run/{selftest_TT16,selftest_L106b,selftest_swap,period16}.log`, `independent_counts.json`, `geometry.log`, and `adversarial_summary.log`.

## Required changes before approval of the general tool

- Fix fallback board validation and add the wrong-size regression test.
- Enforce the geometric/width hypotheses above, or replace them with equally explicit checks of the full reduced-graph insertion map. Do not infer them just from two matching slabs.
- Check slope with integer arithmetic (`dT == 8*s`).
- Keep empirical outside-matching periodicity separate from the proved induction step.

No replacement construction or stronger upper bound is claimed here. The three supplied families pass the independent checks; the general checker remains unapproved until its accepted-input contract is enforced.
