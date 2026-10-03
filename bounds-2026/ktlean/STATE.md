# KT Lean: state for the next session (2026-10-02)

## Role and rules
- You are KT Lean (Research Lab). Manager: Chief Researcher (C.R.), agent id
  agent-1790895858902-etft. Report milestones to C.R. by POST
  localhost:4000/api/agents/agent-1790895858902-etft/messages, in ASD-STE100 Simplified English,
  with theorem names and `#print axioms` output.
- Kernel-only proofs: no `sorry`, no `native_decide`, no new axioms. Axioms must stay
  `[propext, Classical.choice, Quot.sound]`.
- One build at a time (shared, loaded box). `export PATH=$HOME/.elan/bin:$PATH`.
  Iterate one file with `lake env lean Ktlean/X.lean`; `lake build` for the full check
  (Mathlib style linters run only in `lake build`; keep 0 warnings). `lake env lean Axioms.lean`.
- Commit only in this repo (ktlean). Nil allowed commits here. Hand off at about 50% context.

## Proved (all in Ktlean.lean imports; 0 warnings at the last commit)
- Turns, constant 28 (2026-10-04): `KT.ClosedTour.eight_mul_sub_28_le_numTurns`,
  `KT.TwoFactor.eight_mul_le_numTurns_add_28`. CornerTurns.lean (`Lside`, `sum_Lside`,
  `CornerBound c`, `CornerCert` + `Valid` + `cornerBound`, `cert28`, `cornerBound_seven`) and
  Turns28.lean (`eight_mul_le_numTurns_add_of_cornerBound`). For a better certificate of the same
  shape: write a new `CornerCert` value and its two `decide +kernel` checks.
- Turns: `KT.ClosedTour.eight_mul_sub_64_le_numTurns` (8n-64 ≤ turns, n ≥ 8).
- Crossings: `KT.ClosedTour.four_mul_sub_two_le_numCrossings`, `KT.TwoFactor....` (4n-2).
- Flux.lean, TileBudget.lean, LoopCert.lean, Loop.lean, Corner.lean: flux identity, tile budget
  (`bad_budget`, `charged_paths_budget`), loop identity `three_dvd_sum_bdry`, `corner_charge`.
- CornerRow.lean: `corner_charge_row` (one critical row at each end; hypothesis = image of the
  family's straddling strip edges in canonical form equals `PL s` / `PB s`).
- Square.lean: `mult_alt` (9.1), `two_bad`, `charged_squares_budget` (9.2: 2L + 8n + #Bo ≤ 2Y + 4).
- Rotate.lean: `omega_rot`, `corner_charge_rot` (any corner via k quarter turns).
- Boundary.lean: `side_pairs` (NEW: ≥ n+1 crossing pairs among column-0 edges, any degree-two
  family, no forest condition; certificate `c2_cert`: c2 ≥ 1 + down(y+1) - down(y)).
- Overlap.lean: `col0_overlap` (overlaps of column-0 edges lie in x ≤ 1; x = 1 only for the
  exceptional pair), `not_both_of_row` (a critical row excludes that pair).
- Frames.lean: `rowB_of_rowL` (critical row n-2-R of frame k+3 gives the bottom hypothesis at
  column R of frame k, P ↔ P'), tile/square rotation.
- EndTest.lean: `Fcoef` (8 listed edges of FINDINGS 10.2), `gL_eq_Fcoef`, `sum_gL_eq`
  (Σ gL = F + deg), `gB_rot`, `corner_charge_mod_rot`. CornerRow.lean: `corner_charge_mod`
  (end values ≡ 1 mod 3; `corner_charge_row` now follows from it).
- Assembly.lean, Main.lean: `GoodRow` (= 10.4 endpoint test: F ≡ 2 mod 3 and no exceptional pair),
  `ExcPair`, `badRows`, `corners`, `retained`, `cornerSq`, `boundary_card`, `combined_count`
  (10n ≤ Y + b + 130), `fourteen_mul_le_of_stability`.
- TourMain.lean: `ClosedTour.combined_count` (10n ≤ 2X + b + 130, n = 2h ≥ 32) and
  `ClosedTour.fourteen_mul_le_of_stability` (b ≤ X - 4n + 2 + C ⇒ 14n ≤ 3X + C + 132; with
  C = 1131: X ≥ 14n/3 - 421). FINAL per C.R./Nil (2026-10-02): strip stability stays an explicit
  hypothesis; its certificate and soundness proof are NOT to be formalized.

## Conventions
- `Pt = ℤ × ℤ`; `GridEdge = Pt × Bool`: `(a, true)` vertical a → a+(0,1), `(a, false)`
  horizontal a → a+(1,0). Normal points from first to second endpoint.
- Family of edges: index type ι, edge i from `a i` to `a i + d i`, `d i ∈ knightVecs`.
- `ω(q) = flux a d q + chi q.1`. `eps B q = 1` if `q.1 ∈ B` else `-1` (outward orientation).
- `bdry B` = grid edges with exactly one endpoint in B; `mem_bdry` characterizes it.
- Corner lemma variant (sent to C.R.): with B = [0,R]² the outer sides carry no board flux;
  only the 4 end steps `T4` meet tour edges; CL = CB = 2 (kernel check). Python check:
  scratch/corner_box_check.py.

## Open / possible next steps (2026-10-02)
- Constant: corner overlaps are bounded by 6 edges per corner (36 ordered pairs); exact count is
  4 edges. C.R.: constants do not matter, skip.
- Strip stability: SKIPPED by decision of Nil (three independent programs checked it).
  scratch/StripPort.lean has a port of the successor function if this is ever reopened.
- `canon_snd_pos` in Frames.lean is unused (kept as a helper).

## Lean pitfalls seen here
- `if_pos/if_neg/if_true/if_false` are deprecated: use `ite_eq_left/ite_eq_right/ite_true/
  ite_false`. `push_neg` is deprecated: use `push Not`.
- `ring` does not fail inside `first | ring | ...` (it falls back to ring_nf); use `omega` or
  `ring1` first.
- `simp_all` can loop on hypotheses like `q1 = u1`; prefer `split_ifs <;> omega`.
- `Set.mem_setOf_eq` is deprecated: use `Set.mem_ofPred_eq`. `GL` is a Mathlib name.
- `omega` does not see through `set` abbreviations in other hypotheses: ascribe types
  (`have h : A0.card ≤ ... := lemma ...`).
- `rcases h with ⟨rfl, ...⟩` can delete the variable you want to keep; use `rw [e] at ...`.
- Big literals elaborate slowly; encode large data as strings. `decide +kernel` on small
  finite checks (≤ 10^4 cases) takes seconds to a few minutes.
