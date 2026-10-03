# Claim 53: crossings blog, short-proof update — 2026-10-03

**Mathematical verdict: PASS.** Appendix B faithfully assembles the audited 5n-597 proof and includes both Claim 52E corrections. The closed-tour and spanning simple 2-factor statements are correct. The body describes the new keep/discard proof correctly, subject to the board-domain convention made explicit in B.2. All eight distinct appendix commands exist and passed.

**Change-scope verdict: FAIL against the Claim 46 snapshot.** That comparison contains additional URL/link and image-block changes outside CHANGES_5N597.md. This does not identify who made them or whether they predate the short-proof update. In particular it is not evidence that Turns Theory changed Nil's work. Do not revert these differences on the strength of this audit.

The post was not edited. Audit object: `gap/verifier/claim53_post_snapshot.mdx`, captured at 2026-10-03T20:05:45.662945+00:00, SHA-256 `70806a8f91843e8dcdba262c3f9cb7d2b68544472e5b193409b4d49fe46537ae`. All post line numbers below refer to this snapshot. Later live edits are outside this verdict.

## 53A. Appendix B — PASS

Lines 494 and 496 give the correct even-n>=32 tour range and the spanning simple 2-factor extension. Line 496 explicitly includes crossing pairs from different cycles; line 638 repeats that requirement. The graph remains a knight graph on all board cells, with degree two at every cell.

The comparison with the Claim 52 proof gives:

| Snapshot lines | Checked content | Result |
| --- | --- | --- |
| 502–528 | n^2 edges, finite board-quarter domain, D polynomial including holes, D+X1=2E, union S, usable-quarter bound | PASS |
| 533–543 | Full infinite unit lattice, board-contained vertex set A, linear flux, zero circulation, two bad quarters per bad square | PASS |
| 547–572 | Eight endpoint coefficients, absent exception, strong-row OR predicate, reflected DOWN square row r-1, passing-case charge | PASS |
| 576–593 | Radii and N, disjoint squares/endpoint rows, KEEP rule, z<=b, exclusion of forbidden strip pairs, 2M usable quarters | PASS |
| 598–617 | Degree-only cut states, reachability from empty boundary, full row masks, correct crossing ownership, both potentials and join | PASS |
| 620–636 | Corner union correction, C=1130, scalar elimination and 597 | PASS |
| 638 | Degree-only 2-factor scope, with all cross-component pairs included | PASS |

No mathematical step was lost in shortening the proof. In particular the stronger initial filter is what removes the need for deficient paths and private allocations. It does not remove the charge, alternating-square or exception/VIS arguments.

Both Claim 52E corrections are present: the infinite lattice and A contained in the board at lines 533/541, and the separate exception check versus Claim 50's VIS derivation at lines 588/655. No attribution repair remains there.

The constants recompute as

    per physical side: b_sigma <= X_sigma-n+28/4,
    four sides: b <= sum X_sigma-4n+28,
    union correction: sum X_sigma-s <= 1104,
    b <= s-4n+1132 = T+1130,
    C=1130,
    X >= 5n-(32+C/2) = 5n-597.

The four-side error is 28 after rescaling; it is not 112. The use of a union for s is retained. There is one global constant, with no hidden per-path or per-run error. The smaller positive even sizes mentioned at line 636 are trivial because the numerical lower bound is negative there.

## 53B. Body and stale-claim checks — PASS, with one precision suggestion

Lines 198–199, 267, 279, 281, 285 and 289 correctly summarize the revised proof. Every discarded candidate has a strong end, and distinct discarded candidates choose distinct counted rows. Kept candidates supply distinct usable quarters. The side term and quarter term combine through |Q|<=4E-2T; the summary's half-crossing description does not require the removed private-allocation proof.

The phrase “visible two-quarter strip overlap” is correctly separated from ordinary endpoint-test failure: the endpoint exception is included in test failure. The source does not keep paths with a forbidden overlap or count a strong row twice for two discarded candidates. The finite side statement at line 287 has the fixed end allowance the certificate needs.

The frontmatter, Callout, conclusion, gap and details link all use 597. The leading coefficient ratio 19/15 and the upper construction's separate size range n>=96 remain consistent. The appendix-A construction still needs to form one cycle; that is unrelated to the lower theorem's new degree-only scope.

There is no `612` left in the snapshot, and no `forest` text. No surviving lower-proof text says connectivity is required. The remaining discussion of connections and a single cycle concerns the upper construction and is appropriate.

**Optional mathematical-domain clarification, line 241.** The sentence “Around a closed loop the sum is zero” is intended in the board-contained sense now explicit in B.2. It would be overbroad if read as a statement about arbitrary loops in the infinite lattice outside the board. To make the body accurate without consulting the appendix, replace that sentence only with:

> Around a closed loop enclosing only board vertices, the sum is zero modulo 3.

No other mathematical replacement is needed in the body or appendix. This is a domain clarification, not a change to the proof.

## 53C. Appendix commands — PASS

I extracted every distinct shell command from the snapshot, including appendix A, and ran them from an isolated directory named `bounds-2026` with the same relative sources and required saved fixtures. It used the research virtual environment, at most two jobs, and one numerical thread per job. Outputs stayed in the verifier copy.

| Command | Exit | Seconds, 2026-10-03 |
| --- | ---: | ---: |
| `python3 w-turnstheory/check_fold_proof.py` | 0 | 28.66 |
| `python3 w-turnstheory/check_fold_margins.py` | 0 | 0.33 |
| `python3 w-turnstheory/check_knight_tiles.py` | 0 | 0.36 |
| `python3 w-turnstheory/check_corner_box.py` | 0 | 0.07 |
| `python3 w-turnstheory/check_square_defects.py` | 0 | 0.37 |
| `.venv/bin/python gap/lowerbounds/simple_strip/check_cut_certificate.py` | 0 | 4.44 |
| `python3 gap/verifier/claim50_check.py` | 0 | 8.00 |
| `python3 gap/verifier/claim52_check.py` | 0 | 3.97 |

The two strip implementations reproduce 3,136 states, 48,510 arcs, ranges [-24,0]/[-28,0], eight passes and interface [0,4]. The added Claim 52 command checks the outer-column exception and the disconnected 2-factor example. The post's 5.38/8.51-second values are correctly attributed to the earlier dated audit run; a different rerun time is not an error.

The standard-library/NumPy statements at lines 653–655 are correct. This checks the local repository and installed environment, not a clean installation or remote public checkout. No Lean command remains in these appendices, so the earlier Lean timeout is not an outstanding reproduction failure for this snapshot.

Evidence: `claim53_command_list.json`, `claim53_commands.json`, `claim53_command_0.log` through `_7.log`. This is a math audit; no new MDX compilation or browser check was needed or claimed.

## 53D. Changes outside the supplied list

`claim53_vs46.diff` compares this snapshot with `claim46_crossings_snapshot.mdx`. Besides the listed short-proof edits, it shows:

| New snapshot lines | Additional change relative to Claim 46 |
| --- | --- |
| 51–52 and 56 | Demo URLs changed from the `bounds-2026/demo/` location to the repository-site root, retaining the crossings selector |
| 62 | The word “paper” gained an arXiv link |
| 72–77 | Added BlogImage block for `formation_moves.png` |
| 79–84 | Added BlogImage block for `heel_original.png` |

Appendix A is byte-for-byte identical to Claim 46. All 16 old BlogImage blocks are also byte-for-byte preserved; the new post has 18 blocks. Part 1 as a whole is not byte-for-byte identical to Claim 46 because of the paper link and two inserted blocks. No other unlisted post differences were found. The change-list baseline already has the 14 added image-block lines, as shown by its old line numbers, so an intermediate pre-update version is plausible; it is not established by this comparison.

**Exact change-list correction if Claim 46 is the intended comparison baseline:** replace CHANGES_5N597.md line 85 with:

> Appendix A is byte-for-byte unchanged from the Claim 46 snapshot. Relative to that snapshot, Part 1 also has the paper link and two added image blocks listed below.

Replace its line 86 with:

> All 16 BlogImage blocks present in the Claim 46 snapshot are unchanged; two additional blocks appear in the current post. The post-source diff does not establish whether image asset files changed.

Add the four rows of the table above to that change list, or identify and supply the immediate pre-update baseline and explicitly state that these earlier differences are outside this update. This audit cannot establish authorship or timing from the post diff. It also cannot verify assertions about the turns post or other file writes from two snapshots of this one file.

No post rollback is requested. The only failed checklist item is “nothing outside the change list changed” when the specified comparison is the older Claim 46 snapshot.

## Evidence and proof size

Snapshot metadata: `claim53_snapshot.json`. Full diff: `claim53_vs46.diff`. Image-block/appendix-A and stale-text checks: `claim53_diff_checks.json`. Reproduction evidence is listed above.

The mathematical input remains the short scalar hand proof plus the 3,136-state/48,510-arc certificate and the small exact geometry checks. The blog adds no new lemma or finite assumption beyond Claims 50–52. Both stated lower-bound theorems pass this assembly audit.
