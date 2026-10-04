# Claim 55b: re-audit of the all-size upper-bound checker

Date: 2026-10-04. Reviewer: KT Verifier (Astra).

## Verdict

**PASS for the supported single-straight-field family.** The Claim 55 wrong-size fallback defect is fixed. The checker now enforces the geometric conditions needed for the three-gap insertion proof. A successful default invocation proves the stated bound for every even n ≥ 48 for the family actually reconstructed by the checker.

**NOT APPLICABLE to a mixed interior field, including a period-5 field with two line directions.** Neither a finite period nor a PASS for a different, reconstructed straight-field family proves an all-size result for that mixed field. A new proof and checker are needed for it.

This is a mathematical/code audit, not a Lean formalization of the checker.

## Final-version closeout (queued update received after the first report)

The Chief Researcher confirmed the two later hashes below as the intended Claim 55b versions. I also verified and reran the final `allsize_regress.py`, SHA-256 `a86d08dcd60ac716d0cf04de1d1cb8a2b2f1bebb3458c271faf51af2d57b8708`: **10/10 PASS**, including explicit mixed-interior rejection. Evidence: `regress_final.log` and `later_allsize_regress.py`.

The new `allpipe` far-change guard received a separate execution test. I made a valid TT16-derived 56 by 56 tour with a cycle-preserving switch in the central region, then supplied it with 6 by 6 corner regions. The generator correctly rejected its four changed bulk cells at corner distance at least 16 before running a search. Evidence: `claim55b_pipeline_guard.py` and `pipeline_guard.log`. This test covers the new rejection path; no solver run was needed.

The scoped PASS above applies to the final checker version. Mixed-field generalization remains outside its proof scope.

## Versions and source changes during the audit

The requested versions were snapshotted before testing:

| File | SHA-256 |
|---|---|
| allsize_check.py | `2a792b3a665d43d7195b440dc534c9678b661a284650a03838f767e7aade3058` |
| allpipe.py | `a147c02211e76fc4cdab574ae44e6106155390530762228f0229dd5365a5db05` |

These snapshots and all test output are in `gap/verifier/claim55b_run/`. The original worker files were not edited by the audit. Computation used at most two cores.

The worker changed both files while the audit was running. The later versions are separately snapshotted as `later_allsize_check.py` and `later_allpipe.py`:

| Later file | SHA-256 |
|---|---|
| allsize_check.py | `dcd96d11caef7b818df0688590dd11d5f0cf4cddcab9f5ad434a88e0cca24c44` |
| allpipe.py | `bc5ae0a06ca13c129ee624603884c460caac4ca58a9a7ff22f4c58f168ebfdfd` |

The later checker adds only an assertion that `interior`, when present, equals `"x+2y"`. I inspected the diff and tested this guard: explicit mixed-field metadata is rejected, while all three supplied families still pass. The approval of the straight-field checker applies to this later checker too.

The later generator adds a `--max-corner` limit and a rejection message for base-tour differences far from the declared corner regions. I inspected this restriction; it does not change the proof checker or extend the proof to mixed fields. I did not rerun a full candidate-generation/solver workflow for this later generator.

## Claim 55 conditions: checked

| Condition | Result in the requested checker |
|---|---|
| Assertions enabled | `main` explicitly exits under Python `-O`. |
| Positive even p and complete even residue coverage | Checked. The templates and phases must agree across files. |
| Nonempty rectangular templates, exactly two distinct codes in 0–7 | Checked by `template`/`legal_code`. |
| Exact n by n fallback board | Metadata n, row count, row lengths, and cell codes are checked; `validate(g,n)` checks the exact board vertex set. |
| Valid cycle and turn count | Every direct graph is checked for knight edges, reciprocal degree two and one cycle; turns are recounted. N and N+s cannot use fallback files. |
| Inward anchored corner cells | `corner_radius` requires nonnegative inward coordinates and all four recognized corner labels. |
| Full band-overlap rectangles covered | Checked separately at all four corners, in every residue file. |
| Fixed finite corner radius and separation | R includes all zone coordinates and all four band depths. Each base is at least `2R+6`. |
| No edge skips an entire slab | `w >= 5` is enforced; a knight edge changes `x+2y` by at most 5. |
| Correct gap regimes and clearance | Each search interval uses both the zone spans and band-overlap spans, with six-line clearance at both ends. |
| Infinite-band consistency | The existing reciprocal-incidence checks remain in place, including the straight field next to the bands. |
| Matching, composition and no new cycles | The audited slab and composition checks are unchanged; all intermediate powers, the shifted slab, and the longer slab are checked. |
| Additive cost and slope exactly 8 | The base-step cost must match the band sum. PASS now requires integer `dT == 8*s`; a different slope exits nonzero. |
| Empirical period is not presented as an unbounded proof | `allpipe` now says EMPIRICAL/finite check, labels its output candidate data, and lists failed sizes explicitly. |

Two qualifications to a literal reading of the earlier checklist:

- **96 is the default, not a hard floor.** The code uses `max(--Nmin,2R+6)`. An explicit `--Nmin 48` can succeed, and did for TT16. This is sound: the proof needs the separation bound and all finite bases, not the arbitrary number 96. With the default argument, the claimed `N >= max(96,2R+6)` does hold.
- **Coordinate spellings need not be unique.** For example, `BL:0,0` and `BL:00,0` are accepted. `zone_cells` collapses them to one effective cell assignment, using the last entry. This is a deterministic definition of the reconstructed family, not two physical zone cells. The exact-board checks validate the effective graph; the radius condition separates different corners at induction sizes. A redundant alias test passed without changing the graph. Thus literal rejection of all aliases is not enforced, but uniqueness of the effective graph is sufficient for the proof. Canonical keys would still make certificates easier to review.

No remaining proof defect was found within the supported family.

## Tests

The Integrator's `allsize_regress.py` completed **9/9** checks successfully. In particular, the old 16 by 16 fallback labelled as n=48 is rejected; a genuine 48 by 48 fallback is accepted. Missing residue, inconsistent phases, illegal moves, and a missing band-overlap cell are rejected. TT16 and the period-16 relabelling pass. See `regress.log`.

`gap/verifier/claim55b_tests.py` adds **16 tests**, all with the expected outcome:

- Thirteen rejections: empty template; ragged template; duplicate template move; invalid code; outward corner cell; zero period; odd period; width-4 slab; optimized Python; wrong fallback metadata; wrong fallback row length; malformed fallback code; and a redundant remote zone cell that removes the required diagonal gap.
- Three accepted/scope probes: explicit mixed-field metadata on the **requested** checker version; a redundant coordinate alias; and the valid smaller induction base described above.

The mixed-metadata probe is not evidence for a mixed-field construction. In the requested version, unknown metadata is ignored and `graph` still builds TT16's straight interior. The later checker rejects that same probe explicitly. See `new_tests.log`, `new_tests.json`, and `later_checks.json`.

The new checker reproduces:

| Family | c in T(n) ≤ 8n+c | R |
|---|---:|---:|
| selftest_TT16 | -14 | 6 |
| selftest_L106b | -13 | 10 |
| selftest_swap | -13 | 8 |

I also independently reconstructed and recounted each family at n=48,50,52,54; 104,106,108,110; and 192,194,196,198. All **36** checks pass. This independent code checks the exact vertex set, knight edges, reciprocity and one cycle, and uses a determinant to count turns. See `independent_counts.json`. The larger 120-size recount from Claim 55 remains applicable to the unchanged family data.

The matching routines themselves are unchanged from Claim 55, whose independent 11,025-composition test found complete agreement and correct internal-cycle rejection. No new assumption about an unbounded empirical period is introduced here.

## Exactly what a PASS proves

Use the audited checker with assertions enabled and the default `--nmin 48` (or another successful run whose directly checked range includes all even sizes from 48). Require a successful process exit and its explicit `PASS: T(n) <= 8n + (c)` line. The JSON report alone is not sufficient: it is written before the slope rejection branch.

The proved family is exactly this one:

1. Every non-band, non-zone cell has the two moves `(2,-1)` and `(-2,1)`, so its interior path lies on a line `x+2y = constant` and contributes zero turns.
2. Four fixed periodic side templates override that field, with the code's stated phases and top/right rotations.
3. Fixed corner moves override those templates at the inward anchored cells listed in the residue file for n modulo p. The effective cell assignments are those obtained by `zone_cells`.
4. For finitely many n below a class's induction base, a separately checked n by n closed tour may supply the witness instead of that transplant.

Let `w=lcm(PB,PT,2QL,2QR)` and `s=lcm(p,w)`. The checker supplies a base for every even residue modulo s, not merely modulo p. At each base, the corner radius and clearances put the three slabs in the bottom/left, left/right and right/top regimes. These conditions remain true as n grows by s.

The band phases repeat under the required translations because of the divisibility in w and s. Outside the corner pieces, suppressing straight interior paths leaves the same endpoint connections. The slab identities `M^(1+s/w)=M`, including their no-cycle checks, can therefore be repeated at every step. They preserve the single cycle, not just degree two. This is the same insertion argument audited in Claim 55, now with its geometric conditions enforced.

Each side grows by s, and its added turn count is exactly its per-period cost times the number of added periods. Corner and overlap corrections stay fixed. Thus `T(n+s)=T(n)+dT=T(n)+8s` in each induction class. Taking the largest checked `T(n)-8n`, including every finite fallback case, gives c. Therefore a closed tour with at most `8n+c` turns exists for **every even n≥48**.

A run with `--nmin 50`, for example, proves only the range it prints, unless n=48 is covered separately. The empirical p found by `allpipe` remains a candidate-data period; if s>p, the induction establishes the needed repetition under s, not a separate theorem that the outside matching has minimal period p.

## Mixed interior: not covered

`graph` hard-codes `(2,-1),(-2,1)` for the interior. The band consistency checks use the same field. `line(v)=x+2y`, and `Ports.port` requires every slab-crossing edge to belong to one side band. A second interior line direction can create slab-crossing edges in the bulk, change the path connections of the remainder, and require a different cost analysis. A period of 5 alone resolves none of those issues.

The requested hash accepted an `interior` metadata object but ignored it. The later hash rejects a non-`"x+2y"` value. In either version, a PASS establishes only the reconstructed straight-field family above. If a mixed-field base is absorbed into a large finite corner patch and a subsequent check passes, the result concerns that anchored-patch family with a straight bulk; it is not a proof of the intended mixed field throughout growing boards.

**Next action for mixed-field candidates:** use a separate certificate format and proof that specifies the actual bulk moves, their size/phase dependence, all bulk ports, the remainder correspondence, cycle prevention, and the exact added cost. Keep those candidates outside this tool's approved all-size scope until that proof is audited. No additional change is required to approve the current straight-field theorem checker.

## Superseding partial-mode version (Claim 56 Part 2, 2026-10-04)

The subsequent requested checker hash `f3925853ab20f57416678ee81aa2b4322c7e5074fe4065ff3ef29730353bc5d6` and generator hash `2dfc8f14657e04ef2315d3cafa609d691ae59d7223675a00466a5c7f644316d8` are audited in `claim56_report.md`. **PASS for the same straight-field proof framework, now including explicitly scoped partial residue sets.** The default complete-residue mode retains its previous meaning. A partial PASS covers only its printed residue set, not every even board size.

The new extraction and residue-selection generator features were reviewed, and the resulting graphs were independently reconstructed and checked against all 20 supplied pipeline tours. The partial checker passed eight scope/adversarial tests and the existing ten-case regression suite. Independent geometry, slab matching, cycle-free gluing and cost checks establish the two improved all-size bounds in Claim 56. Mixed fields remain outside scope.
