import Ktlean.Main
import Ktlean.Crossings

/-!
# The combined count for closed tours

For a closed tour of the `n × n` board, `n = 2h`, `h ≥ 16`, take the family of its `n²` moves.
Then `10 n ≤ 2X + d + 130`, where `X = T.numCrossings` and `d` is the number of non-critical rows
in the scan ranges (`badRows`: rows that fail the endpoint test of FINDINGS 10.4). With the
per-row stability hypothesis `d ≤ X - 4n + 2 + C` this gives `3X ≥ 14n - C - 132`.
-/

open Finset

namespace KT

variable {n : ℕ}

/-- The start points of the moves of a tour. -/
def ClosedTour.ptA (T : ClosedTour n) (i : Fin (n * n)) : Pt := pt (T.cell i)

/-- The vectors of the moves of a tour. -/
def ClosedTour.ptD (T : ClosedTour n) (i : Fin (n * n)) : Pt :=
  pt (T.cell (finRotate _ i)) - pt (T.cell i)

/-- The non-critical rows of a closed tour (`n = 2h`). -/
def ClosedTour.badRows {h : ℕ} (T : ClosedTour (2 * h)) : Finset (ℕ × ℤ) :=
  KT.badRows T.ptA T.ptD h

lemma ClosedTour.ptA_add (T : ClosedTour n) (i : Fin (n * n)) :
    T.ptA i + T.ptD i = pt (T.cell (finRotate _ i)) := by
  simp [ClosedTour.ptA, ClosedTour.ptD]

lemma ClosedTour.distinct (T : ClosedTour n) (hn : 2 ≤ n) : DistinctEdges T.ptA T.ptD := by
  intro i j hij h
  simp only [ClosedTour.ptA_add] at h
  simp only [ClosedTour.ptA] at h
  rcases h with ⟨h1, h2⟩ | ⟨h1, h2⟩
  · exact hij (T.cell.injective (pt_injective h1))
  · have e1 := T.cell.injective (pt_injective h1)
    have e2 := T.cell.injective (pt_injective h2)
    apply finRotate_symm_ne (m := n * n) (by nlinarith) i
    rw [e2, e1, Equiv.symm_apply_apply]

lemma ClosedTour.deg_eq (T : ClosedTour n) {v : Pt} (hv : InBoard n v) :
    deg T.ptA T.ptD v = 2 := by
  obtain ⟨x, y⟩ := v
  unfold InBoard at hv
  simp only at hv
  set c : Cell n := (⟨x.toNat, by omega⟩, ⟨y.toNat, by omega⟩)
  have hc : pt c = (x, y) := by simp [pt, c]; omega
  unfold deg
  have h1 : (univ.filter fun i => T.ptA i = (x, y)) = {T.cell.symm c} := by
    ext i
    simp only [mem_filter, mem_univ, true_and, mem_singleton, ClosedTour.ptA, ← hc]
    constructor
    · intro h; rw [← pt_injective h, Equiv.symm_apply_apply]
    · rintro rfl; rw [Equiv.apply_symm_apply]
  have h2 : (univ.filter fun i => T.ptA i + T.ptD i = (x, y)) =
      {(finRotate _).symm (T.cell.symm c)} := by
    ext i
    simp only [mem_filter, mem_univ, true_and, mem_singleton, ClosedTour.ptA_add, ← hc]
    constructor
    · intro h; rw [← pt_injective h, Equiv.symm_apply_apply, Equiv.symm_apply_apply]
    · rintro rfl; rw [Equiv.apply_symm_apply, Equiv.apply_symm_apply]
  rw [h1, h2, card_singleton, card_singleton]

/-- Ordered properly crossing pairs of moves are at most twice the crossings. -/
lemma ClosedTour.card_crossPairs_le (T : ClosedTour n) :
    (crossPairs T.ptA T.ptD).card ≤ 2 * T.numCrossings := by
  classical
  set X := univ.filter fun p : Fin (n * n) × Fin (n * n) => p.1 < p.2 ∧
    OpenSegmentsMeet (T.cell p.1) (T.cell (finRotate _ p.1))
      (T.cell p.2) (T.cell (finRotate _ p.2))
  have hX : T.numCrossings = X.card := by unfold ClosedTour.numCrossings; congr 1
  have hle := card_le_card (s := crossPairs T.ptA T.ptD) (t := X ∪ X.image Prod.swap) (by
    intro p hp
    have hp' := (mem_filter.1 hp).2
    simp only [ClosedTour.ptA_add] at hp'
    simp only [ClosedTour.ptA] at hp'
    clear hp
    have hp := hp'
    rcases lt_or_gt_of_ne hp.1 with hlt | hlt
    · exact mem_union_left _ (by
        simp only [X, mem_filter, mem_univ, true_and]
        exact ⟨hlt, hp.2.openSegmentsMeet⟩)
    · refine mem_union_right _ (mem_image.2 ⟨p.swap, ?_, Prod.swap_swap p⟩)
      simp only [X, mem_filter, mem_univ, true_and, Prod.fst_swap, Prod.snd_swap]
      exact ⟨hlt, ((properCross_comm _ _ _ _).1 hp.2).openSegmentsMeet⟩)
  have h1 := card_union_le X (X.image Prod.swap)
  have h2 := card_image_le (s := X) (f := Prod.swap)
  omega

/-- **Combined count for closed tours.** `10 n ≤ 2X + d + 130` for `n = 2h ≥ 32`. -/
theorem ClosedTour.combined_count {h : ℕ} (T : ClosedTour (2 * h)) (hh : 16 ≤ h) :
    10 * (2 * h) ≤ 2 * T.numCrossings + T.badRows.card + 130 := by
  have key := KT.combined_count (n := ((2 * h : ℕ) : ℤ)) (a := T.ptA) (d := T.ptD)
    (fun i => (T.isKnightMove i).mem_knightVecs)
    (fun i => ⟨pt_bounds _, by rw [T.ptA_add]; exact pt_bounds _⟩)
    (fun v hv => T.deg_eq hv) (T.distinct (by omega)) (by push_cast; ring) hh (by simp)
  have := T.card_crossPairs_le
  unfold ClosedTour.badRows
  omega

/-- **Conditional main theorem for closed tours.** If the rows that fail the endpoint test
satisfy the per-row strip stability bound `b ≤ E + C` with `E = X - 4n + 2` (FINDINGS 10.4,
TILE_INPUTS section 9: `C = 1131`), then `3X ≥ 14n - C - 132`, that is `X ≥ 14n/3 - 421`. -/
theorem ClosedTour.fourteen_mul_le_of_stability {h : ℕ} (T : ClosedTour (2 * h)) (hh : 16 ≤ h)
    (C : ℤ) (hstab : (T.badRows.card : ℤ) ≤ (T.numCrossings : ℤ) - 4 * (2 * h) + 2 + C) :
    14 * (2 * h : ℤ) ≤ 3 * T.numCrossings + C + 132 := by
  have := T.combined_count hh
  omega

end KT
