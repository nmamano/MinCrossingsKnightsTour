import Ktlean.TwoFactor

/-!
# From closed tours to 2-factors

A closed tour gives a 2-factor (each cell gets its predecessor and its successor in the tour)
with the same number of turns.
-/

open Finset

namespace KT

variable {n : ℕ}

lemma IsKnightMove.symm {u v : Cell n} (h : IsKnightMove u v) : IsKnightMove v u := by
  unfold IsKnightMove IsKnightVec disp at *
  simp only [abs_sub_comm] at h ⊢
  exact h

lemma IsKnightVec.mem {d : ℤ × ℤ} (h : IsKnightVec d) :
    d ∈ ({(1, 2), (1, -2), (-1, 2), (-1, -2), (2, 1), (2, -1), (-2, 1), (-2, -1)} :
      Finset (ℤ × ℤ)) := by
  obtain ⟨a, b⟩ := d
  unfold IsKnightVec at h
  simp only at h
  rcases h with ⟨h1, h2⟩ | ⟨h1, h2⟩ <;>
  · rw [abs_eq (by norm_num)] at h1 h2
    rcases h1 with rfl | rfl <;> rcases h2 with rfl | rfl <;> decide

/-- Two parallel knight vectors are equal or opposite. -/
lemma IsKnightVec.eq_or_eq_neg_of_cross {d e : ℤ × ℤ} (hd : IsKnightVec d) (he : IsKnightVec e)
    (h : d.1 * e.2 - d.2 * e.1 = 0) : e = d ∨ e = -d := by
  have hd := hd.mem
  have he := he.mem
  simp only [mem_insert, mem_singleton] at hd he
  rcases hd with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl <;>
  rcases he with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl <;>
  simp_all

/-- In a cyclic order of length at least 3, the predecessor and the successor differ. -/
lemma finRotate_symm_ne {m : ℕ} (hm : 3 ≤ m) (i : Fin m) :
    (finRotate m).symm i ≠ finRotate m i := by
  intro h
  have h2 : finRotate m (finRotate m i) = i := by
    rw [← h, Equiv.apply_symm_apply]
  obtain ⟨j, rfl⟩ : ∃ j, m = j + 3 := ⟨m - 3, by omega⟩
  rw [finRotate_apply, finRotate_apply, add_assoc, add_eq_left, Fin.ext_iff,
    Fin.val_add, Fin.val_one, Fin.val_zero, Nat.mod_eq_of_lt (by omega)] at h2
  omega

namespace ClosedTour

/-- The predecessor of position `i` in the cyclic order. -/
abbrev prev {m : ℕ} (i : Fin m) : Fin m := (finRotate m).symm i
/-- The successor of position `i` in the cyclic order. -/
abbrev next {m : ℕ} (i : Fin m) : Fin m := finRotate m i

variable (T : ClosedTour n)

lemma cell_prev_ne_cell_next (hn : 2 ≤ n) (i : Fin (n * n)) :
    T.cell (prev i) ≠ T.cell (next i) :=
  fun h => finRotate_symm_ne (by nlinarith) i (T.cell.injective h)

/-- The 2-factor of a closed tour: the neighbours of a cell are its predecessor and its
successor in the tour. -/
def toTwoFactor (hn : 2 ≤ n) : TwoFactor n where
  nbrs v := {T.cell (prev (T.cell.symm v)), T.cell (next (T.cell.symm v))}
  card_nbrs v := card_pair (T.cell_prev_ne_cell_next hn _)
  isKnightMove v u hu := by
    simp only [mem_insert, mem_singleton] at hu
    rcases hu with rfl | rfl
    · have := T.isKnightMove (prev (T.cell.symm v))
      simp only [prev, Equiv.apply_symm_apply] at this
      exact this.symm
    · have := T.isKnightMove (T.cell.symm v)
      simpa using this
  symm v u hu := by
    simp only [mem_insert, mem_singleton] at hu ⊢
    rcases hu with rfl | rfl
    · right; simp only [next, prev, Equiv.symm_apply_apply, Equiv.apply_symm_apply]
    · left; simp only [next, prev, Equiv.symm_apply_apply, Equiv.apply_symm_apply]

lemma toTwoFactor_isTurn_iff (hn : 2 ≤ n) (i : Fin (n * n)) :
    (T.toTwoFactor hn).IsTurn (T.cell i) ↔ T.IsTurn i := by
  have hab := T.cell_prev_ne_cell_next hn i
  have h1 := (T.isKnightMove (prev i))
  simp only [prev, Equiv.apply_symm_apply] at h1
  have h2 := T.isKnightMove i
  have hd : IsKnightVec (disp (T.cell (prev i)) (T.cell i)) := h1
  have he : IsKnightVec (disp (T.cell i) (T.cell (next i))) := h2
  have hdb := hd.bounds
  have heb := he.bounds
  simp only [TwoFactor.IsTurn, IsTurn, toTwoFactor, Equiv.symm_apply_apply, not_iff_not]
  generalize T.cell (prev i) = a at *
  generalize T.cell i = v at *
  generalize T.cell (next i) = b at *
  simp only [mem_insert, mem_singleton, exists_eq_or_imp, exists_eq_left]
  have hab' : ¬ ((a.1 : ℤ) = b.1 ∧ (a.2 : ℤ) = b.2) := by
    rintro ⟨h1, h2⟩
    exact hab (Prod.ext (Fin.ext (by exact_mod_cast h1)) (Fin.ext (by exact_mod_cast h2)))
  simp only [disp, Collinear3, Prod.ext_iff, Prod.fst_neg, Prod.snd_neg] at *
  constructor
  · rintro (((h | h) | (h | h)))
    · omega
    · linear_combination ((v.1 : ℤ) - a.1) * h.2 - ((v.2 : ℤ) - a.2) * h.1
    · linear_combination ((v.1 : ℤ) - a.1) * h.2 - ((v.2 : ℤ) - a.2) * h.1
    · omega
  · intro h
    have hpar := IsKnightVec.eq_or_eq_neg_of_cross hd he (by
      linear_combination h)
    simp only [Prod.ext_iff, Prod.fst_neg, Prod.snd_neg] at hpar
    omega

/-- A closed tour and its 2-factor have the same number of turns. -/
theorem numTurns_toTwoFactor (hn : 2 ≤ n) : (T.toTwoFactor hn).numTurns = T.numTurns := by
  classical
  unfold TwoFactor.numTurns ClosedTour.numTurns
  symm
  apply card_equiv T.cell
  intro i
  simp [T.toTwoFactor_isTurn_iff hn]

end ClosedTour

/-- **Main theorem.** Every closed knight's tour of the `n × n` board, `n ≥ 8`, has at least
`8 * n - 64` turns. -/
theorem ClosedTour.eight_mul_sub_64_le_numTurns (T : ClosedTour n) (hn : 8 ≤ n) :
    8 * n - 64 ≤ T.numTurns := by
  have := (T.toTwoFactor (by omega)).eight_mul_le_numTurns_add hn
  rw [T.numTurns_toTwoFactor] at this
  omega

end KT
