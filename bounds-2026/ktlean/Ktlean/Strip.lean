import Mathlib

/-!
# The four-column strip lemma, in abstract form

We work with a finite set `α` of vertices, a symmetric neighbour function `N` with exactly
two neighbours per vertex (a 2-regular graph), and an integer "column" function `c ≥ 0`
such that every edge changes the column by 1 or 2. A vertex that is not a turn has two
neighbours `u, w` whose columns satisfy `c u + c w = 2 * c v`.
If each of the columns `0, 1, 2, 3` has exactly `m` vertices, then at least `2 * m` turns lie
in these four columns.
-/

open Finset

namespace KT

variable {α : Type*}

/-- Double counting of the edges between two vertex sets. -/
lemma sum_card_inter_comm [DecidableEq α] (N : α → Finset α) (hsymm : ∀ v u, u ∈ N v → v ∈ N u)
    (A B : Finset α) : ∑ v ∈ A, (N v ∩ B).card = ∑ u ∈ B, (N u ∩ A).card := by
  have key : ∀ A B : Finset α,
      ∑ v ∈ A, (N v ∩ B).card = ∑ v ∈ A, ∑ u ∈ B, if u ∈ N v then 1 else 0 := by
    intro A B
    refine sum_congr rfl fun v _ => ?_
    rw [← card_filter, filter_mem_eq_inter, inter_comm]
  rw [key, key, sum_comm]
  refine sum_congr rfl fun u _ => sum_congr rfl fun v _ => ?_
  have : u ∈ N v ↔ v ∈ N u := ⟨hsymm v u, hsymm u v⟩
  simp only [this]

theorem strip_lemma [Fintype α] (N : α → Finset α) (hcard : ∀ v, (N v).card = 2)
    (hsymm : ∀ v u, u ∈ N v → v ∈ N u)
    (c : α → ℤ) (hc0 : ∀ v, 0 ≤ c v)
    (hstep : ∀ v, ∀ u ∈ N v, c v - 2 ≤ c u ∧ c u ≤ c v + 2 ∧ c u ≠ c v)
    (turn : α → Prop) [DecidablePred turn]
    (hturn : ∀ v, ¬ turn v → ∃ u ∈ N v, ∃ w ∈ N v, c u + c w = 2 * c v)
    (m : ℕ) (hcol : ∀ k : ℤ, 0 ≤ k → k < 4 → (univ.filter fun v => c v = k).card = m) :
    2 * m ≤ (univ.filter fun v => turn v ∧ c v < 4).card := by
  classical
  set A0 := univ.filter fun v => c v = 0
  set A3 := univ.filter fun v => c v = 3
  set A12 := univ.filter fun v => c v = 1 ∨ c v = 2
  set A03 := univ.filter fun v => c v = 0 ∨ c v = 3
  let t : α → ℕ := fun v => if turn v then 1 else 0
  have hA0 : A0.card = m := hcol 0 (by norm_num) (by norm_num)
  have hA3 : A3.card = m := hcol 3 (by norm_num) (by norm_num)
  have hA12 : A12.card = 2 * m := by
    have h1 := hcol 1 (by norm_num) (by norm_num)
    have h2 := hcol 2 (by norm_num) (by norm_num)
    rw [show A12 = (univ.filter fun v => c v = 1) ∪ (univ.filter fun v => c v = 2) from
      filter_or _ _ _, card_union_of_disjoint (disjoint_filter.2 fun v _ h h' => by omega)]
    omega
  -- column 0: every vertex is a turn, and all its neighbours are in columns 1, 2
  have F0 : ∀ v ∈ A0, t v = 1 ∧ (N v ∩ A12).card = 2 := by
    intro v hv
    simp only [A0, mem_filter, mem_univ, true_and] at hv
    refine ⟨?_, ?_⟩
    · simp only [t, ite_eq_left_iff]
      intro hnt
      obtain ⟨u, hu, w, hw, h⟩ := hturn v hnt
      have := hstep v u hu; have := hstep v w hw; have := hc0 u; have := hc0 w
      omega
    · rw [← hcard v]
      congr 1
      refine inter_eq_left.2 fun u hu => ?_
      have := hstep v u hu; have := hc0 u
      simp only [A12, mem_filter, mem_univ, true_and]
      omega
  -- columns 1 and 2: at most `1 + t v` neighbours in columns 0, 3
  have F12 : ∀ v ∈ A12, (N v ∩ A0).card + (N v ∩ A3).card ≤ 1 + t v := by
    intro v hv
    simp only [A12, mem_filter, mem_univ, true_and] at hv
    have hu03 : (N v ∩ A0).card + (N v ∩ A3).card = (N v ∩ A03).card := by
      rw [← card_union_of_disjoint, ← inter_union_distrib_left]
      · congr 2
        exact (filter_or _ _ _).symm
      · exact disjoint_of_subset_left inter_subset_right
          (disjoint_of_subset_right inter_subset_right
            (disjoint_filter.2 fun v _ h h' => by omega))
    rw [hu03]
    by_cases ht : turn v
    · simp only [t, ht, ite_true]
      have := card_le_card (inter_subset_left (s₁ := N v) (s₂ := A03))
      rw [hcard v] at this
      omega
    · obtain ⟨u, hu, w, hw, h⟩ := hturn v ht
      have hle : ∀ x ∈ N v, x ∉ A03 → (N v ∩ A03).card ≤ 1 := by
        intro x hx hxA
        have := card_le_card (s := N v ∩ A03) (t := (N v).erase x) (fun y hy => by
          rw [mem_erase]
          exact ⟨fun hxy => hxA (hxy ▸ (mem_inter.1 hy).2), (mem_inter.1 hy).1⟩)
        rw [card_erase_of_mem hx, hcard v] at this
        omega
      by_cases huA : u ∈ A03
      · by_cases hwA : w ∈ A03
        · exfalso
          simp only [A03, mem_filter, mem_univ, true_and] at huA hwA
          omega
        · have := hle w hw hwA; omega
      · have := hle u hu huA; omega
  -- column 3: at least `1 - t v` neighbours in columns 1, 2
  have F3 : ∀ v ∈ A3, 1 ≤ (N v ∩ A12).card + t v := by
    intro v hv
    simp only [A3, mem_filter, mem_univ, true_and] at hv
    by_cases ht : turn v
    · simp only [t, ht, ite_true]; omega
    · obtain ⟨u, hu, w, hw, h⟩ := hturn v ht
      have hmem : ∀ x ∈ N v, x ∈ A12 → 1 ≤ (N v ∩ A12).card := fun x hx hxA =>
        card_pos.2 ⟨x, mem_inter.2 ⟨hx, hxA⟩⟩
      by_cases huA : u ∈ A12
      · have := hmem u hu huA; omega
      · by_cases hwA : w ∈ A12
        · have := hmem w hw hwA; omega
        · exfalso
          simp only [A12, mem_filter, mem_univ, true_and] at huA hwA
          have := hstep v u hu; have := hstep v w hw
          omega
  -- summing up
  set B := ∑ v ∈ A12, (N v ∩ A3).card
  have S0 : ∑ v ∈ A0, t v = m := by
    rw [sum_congr rfl fun v hv => (F0 v hv).1]; simp [hA0]
  have E0 : ∑ v ∈ A12, (N v ∩ A0).card = 2 * m := by
    rw [sum_card_inter_comm N hsymm, sum_congr rfl fun v hv => (F0 v hv).2]; simp [hA0, mul_comm]
  have S12 : B ≤ ∑ v ∈ A12, t v := by
    have := sum_le_sum F12
    rw [sum_add_distrib, sum_add_distrib, E0] at this
    simp only [sum_const, smul_eq_mul, mul_one, hA12] at this
    omega
  have S3 : m ≤ B + ∑ v ∈ A3, t v := by
    have := sum_le_sum F3
    rw [sum_add_distrib, ← sum_card_inter_comm N hsymm] at this
    simpa [hA3] using this
  -- the strip is the disjoint union of A0, A12, A3
  have hstrip : (univ.filter fun v => turn v ∧ c v < 4).card = ∑ v ∈ A0 ∪ A12 ∪ A3, t v := by
    rw [card_filter]
    rw [← sum_filter_add_sum_filter_not univ (fun v => c v < 4)]
    have h1 : ∑ v ∈ univ.filter (fun v => ¬ c v < 4), (if turn v ∧ c v < 4 then 1 else 0) = 0 :=
      sum_eq_zero fun v hv => by
        simp only [mem_filter] at hv; simp [hv.2]
    rw [h1, add_zero]
    have h2 : univ.filter (fun v => c v < 4) = A0 ∪ A12 ∪ A3 := by
      ext v; simp only [A0, A12, A3, mem_union, mem_filter, mem_univ, true_and]
      have := hc0 v; omega
    rw [h2]
    refine sum_congr rfl fun v hv => ?_
    have : c v < 4 := by
      simp only [A0, A12, A3, mem_union, mem_filter, mem_univ, true_and] at hv; omega
    simp [t, this]
  rw [hstrip, sum_union, sum_union]
  · omega
  · exact disjoint_filter.2 fun v _ h h' => by omega
  · rw [disjoint_union_left]
    exact ⟨disjoint_filter.2 fun v _ h h' => by omega, disjoint_filter.2 fun v _ h h' => by omega⟩

end KT
