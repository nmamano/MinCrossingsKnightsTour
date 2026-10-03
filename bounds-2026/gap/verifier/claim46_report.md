# Claim 46: crossings post 5n snapshot audit — 2026-10-03

**PASS for the mathematics and the stated 5n-612 bound. Corrections required for dependencies and check attribution. GAP for the Lean command rerun: it timed out.** No mathematical replacement to the theorem or proof is needed. Neither blog post was edited.

## Object and scope

The object is `gap/verifier/claim46_crossings_snapshot.mdx`, captured at 2026-10-03T14:45:56.786291+00:00, SHA-256 `6e940f2a4dfbcf2751718909076f81aa3dcc7f48309cd1532f2bddb521739ed3`. Line numbers below refer only to this snapshot. Later changes by Nil are outside this verdict. Snapshot metadata is in `claim46_snapshot.json`.

The update list in `gap/turnstheory/FINDINGS.md`, the consolidated `PROOF_5N.md`, Claims 39, 40 and 42, and the actual check implementations were the audit sources. Appendix A's complete first details block is byte-identical to `gap/turnstheory/post_before_5n.mdx`. Both figures were copied and inspected separately after the text snapshot; their hashes are in `claim46_extra_checks.json`. They show lower coefficient 5 and upper coefficient 19/3 (rounded 6.33 in the progress chart). This figure finding applies to the copied assets, not a guarantee about their bytes at the earlier text capture time.

## Mathematics: PASS

B.1 gives the exact tile identity, including the uncovered-quarter contribution and the definition of W3. B.2's flux argument supplies the mod-3 charge; the degree-two closed-tour assumption is present. B.3 uses radii 12 through n/2-4, so there are N=2n-60 candidates. The endpoint table, exceptional pair, retention rule and passing residue agree with the audited construction. Candidate squares are distinct, including after corner rotations; the excluded pair accounts for the only B overlap which could reach an end square. Thus retained squares avoid B.

B.4 uses the correct capacity nu: one half per crossing outside S*, one quarter per hole, and the X1/W3 quarter terms. Multiplicity-two quarters covered by an S* pair with a two-quarter overlap are excluded. The quarter payments are private because each candidate uses distinct squares and the atom budgets were checked in Claim 39. Its simplification to a full half-unit for every nondeficient retained path is valid; it does not need the partial-demand notation of Claim 40. The exact identity is E+580=nu+(T+1160)/2. This uses the strip reserve once, in addition to the quarter payments; it does not add the 4n baseline a second time.

B.5 correctly sends each lost candidate to a failed test and each deficient retained candidate to a visible end. A deficient charged path has an unpayable quarter; the pair covering it lies in S* minus B and its overlap has square depth at most two. The candidate geometry forces that side to be an endpoint side. The up test uses square row r and the down test uses r-1. Radius 12 suffices, so no 42-path allowance is needed. The near/far row intervals are disjoint, and a physical side row owns at most one candidate. Hence G_strong >= D_loss+L_def without reuse of a row.

B.6 uses the forest relaxation of each proper strip subgraph of a connected tour, with the correct degree and crossing ownership rules. The common full-row-mask graph has 82,516 base states/144,674 arcs and 184,006 augmented states/343,631 arcs. The rebuilt up/down potentials have ranges [-29,0] and [-33,0], and both settle in 41 passes. Every arc inequality passes. Their row-boundary difference is [-4,4]. The split therefore costs at most 37/4 per physical side, rather than the sum of two unrelated ranges. The corner estimate gives G_strong <= T+1139 <= T+1160. The post correctly distinguishes this certificate from the author's separate-orientation calculation, which alone gives constant 614.

B.7 then gives

    E+580 >= (L-L_def)/2 + (D_loss+L_def)/2
          = (L+D_loss)/2 = N/2 = n-30,
    X = 4n-2+E >= 5n-612.

This holds for every closed tour on an even n by n board with n>=32. For smaller positive even n the same numerical lower bound is trivial. The Callout, body steps, asymptotic ratio 19/15 and gap interval agree. The existence range n>=96 for the 19n/3+142 upper bound is kept separate from the lower-bound range. The proof makes no claim that 5n is a Lean theorem.

## Exact technical replacements

These are factual corrections, not prose-style edits.

1. **Dependency paragraph, line 488.** Replace the sentence `The independent strip checker needs NumPy.` with:

> The independent strip checker needs NumPy, NetworkX and python-sat. The geometry checker `claim42_geometry.py` also needs python-sat, through its imported `claim37_check` module.

Keep the author's NumPy/OR-Tools requirement. The actual independent checker imports NetworkX for its tight-cycle check, and both verifier programs import a module with top-level PySAT imports. Those imports execute even though these two commands do not solve a SAT instance.

2. **Candidate-geometry attribution, line 607.** Replace `The same check verifies the side-depth argument and candidate geometry for every even n from 32 through 258.` (with the original inline code formatting) by:

> This check verifies the side-depth argument. The independent strip checker in B.6 also checks candidate geometry for every even `n` from 32 through 258.

The following sentence about the coordinate proof for all even n>=32 can stay.

3. **Visibility-check attribution, line 658.** Replace the last sentence of the paragraph beginning `This works for every candidate radius` with:

> The geometry check in B.3 finds seven up-oriented visible pairs and checks their depth and pending-edge support. The independent checker in B.6 enumerates seven pairs in each orientation and verifies their exact reflection, including the square-row shift.

The B.3 script does not enumerate the down orientation. The B.6 script does.

4. **Output files, line 718.** Replace the sentence beginning `The potential arrays, hashes and report are saved` with:

> This command saves `claim42_potential_up.npy`, `claim42_potential_down.npy` and `claim42_check.json` under `gap/verifier/`; the JSON report includes the potential hashes. The geometry command in B.3 saves `claim42_sources.json`. Save the terminal output separately to retain a log.

The displayed command has no output redirection and does not create `claim42_check.log`. Existing saved log files are not generated by that command.

## Command and rendering checks

All eleven distinct Python commands displayed in the appendices were run successfully from an isolated folder named `bounds-2026`, with the repository-relative sources and required tour data copied there. It used the existing research virtual environment and at most two jobs. Reports and generated files went to the isolated copy. This is a local reproduction check, not a clean installation or an audit of the remote public checkout.

The independent certificate took 15.7 seconds in this rerun; the author up/down certificates took 29.7/44.8 seconds. These do not invalidate the post's dated prior measurements. The tile, defect, corner, quarter-support, Claim 39, geometry, FOLD proof and FOLD margin checks also passed. Exact commands, exit status, times and log paths are in `claim46_commands.json` and `claim46_command_00.log` through `_11.log`.

The remaining distinct command, `(cd ktlean && lake env lean Axioms.lean)`, produced no output and timed out at 180 seconds. Its path and source file exist. This audit therefore cannot certify that every displayed command finishes in the present environment. The post already conditions that command on the installed Lean toolchain and dependencies. No cause for the timeout is established here, and it is not evidence of a false theorem. Repair for full reproduction closeout: rerun this exact command in the intended configured Lean environment and retain its completed output.

A copy of the existing MDX check was pointed at the snapshot, with the site's actual compiler and options. It passed compilation and the two collapsed proof-block checks. The live post was not read by that compiler check and was not changed.

## Proof size and finite inputs

The 5n appendix is a hand proof plus exact local tile/quarter/end geometry and one finite strip potential certificate, with a second implementation. The critical new finite graph has 184,006 states and 343,631 arcs. No periodic SAT optimum, new connectivity conjecture, above-5n argument or large R3 graph is needed. The unresolved items are the four factual documentation corrections and the Lean rerun, not a gap in the 5n proof.
