import Ktlean.CornerTurns

/-!
# `8 * n - 28` turns for 2-factors and closed tours

For each side of the board, `t v ≥ Lside d v` at every cell and `Σ_v Lside d v = 2 * n`.
For `n ≥ 8`, a cell outside the four 4 × 4 corners is within distance 4 of at most one side,
and at a corner cell only the two sides of that corner contribute. So
`T - 8 n = Σ_v (t v - Σ_sides Lside) ≥ Σ_corners (corner sum) ≥ -4 c` for any `CornerBound c`.
-/

open Finset

namespace KT

variable {n : ℕ}

/-- The distance `s * x + b` of the coordinate `x` from a side (`s = 1, b = 0` or
`s = -1, b = n - 1`). -/
def sideDist (s b : ℤ) (x : Fin n) : ℤ := s * (x : ℤ) + b

/-- The side condition on `(s, b)`. -/
def SideParam (n : ℕ) (s b : ℤ) : Prop := (s = 1 ∧ b = 0) ∨ (s = -1 ∧ b = n - 1)

lemma IsKnightVec.mul_sign {a b sa sb : ℤ} (h : IsKnightVec (a, b)) (ha : sa = 1 ∨ sa = -1)
    (hb : sb = 1 ∨ sb = -1) : IsKnightVec (sa * a, sb * b) := by
  unfold IsKnightVec at h ⊢
  rcases ha with rfl | rfl <;> rcases hb with rfl | rfl <;> simpa using h

namespace TwoFactor

variable (F : TwoFactor n)

lemma sideDist_step {s b : ℤ} (hsb : SideParam n s b) (p : Cell n → Fin n)
    (hp : p = Prod.fst ∨ p = Prod.snd) (v u : Cell n) (hu : u ∈ F.nbrs v) :
    sideDist s b (p v) - 2 ≤ sideDist s b (p u) ∧ sideDist s b (p u) ≤ sideDist s b (p v) + 2 ∧
      sideDist s b (p u) ≠ sideDist s b (p v) := by
  have hk := (F.isKnightMove v u hu).bounds
  simp only [disp] at hk
  unfold sideDist
  rcases hp with rfl | rfl <;> rcases hsb with ⟨rfl, rfl⟩ | ⟨rfl, rfl⟩ <;> omega

lemma sideDist_nonneg {s b : ℤ} (hsb : SideParam n s b) (x : Fin n) : 0 ≤ sideDist s b x := by
  have := x.isLt
  unfold sideDist
  rcases hsb with ⟨rfl, rfl⟩ | ⟨rfl, rfl⟩ <;> omega

lemma sideDist_turn {s b : ℤ} (hsb : SideParam n s b) (p : Cell n → Fin n)
    (hp : p = Prod.fst ∨ p = Prod.snd) (v : Cell n) (hv : ¬ F.IsTurn v) :
    ∃ u ∈ F.nbrs v, ∃ w ∈ F.nbrs v,
      sideDist s b (p u) - sideDist s b (p v) = -(sideDist s b (p w) - sideDist s b (p v)) := by
  simp only [TwoFactor.IsTurn, not_not] at hv
  obtain ⟨u, hu, w, hw, h⟩ := hv
  refine ⟨u, hu, w, hw, ?_⟩
  simp only [disp, Prod.ext_iff, Prod.fst_neg, Prod.snd_neg] at h
  unfold sideDist
  rcases hp with rfl | rfl <;> rcases hsb with ⟨rfl, rfl⟩ | ⟨rfl, rfl⟩ <;> omega

/-- The sum of the local bounds of one side is exactly `2 * n`. -/
theorem sum_Lside_side (hn : 4 ≤ n) {s b : ℤ} (hsb : SideParam n s b) (p : Cell n → Fin n)
    (hp : p = Prod.fst ∨ p = Prod.snd) :
    ∑ v, Lside F.nbrs (fun v => sideDist s b (p v)) v = 2 * n := by
  apply sum_Lside F.nbrs F.card_nbrs F.symm _ (fun v => sideDist_nonneg hsb (p v))
    (F.sideDist_step hsb p hp)
  intro k hk0 hk4
  rw [card_filter_comp_proj p hp (fun x => sideDist s b x = k)]
  suffices (univ.filter fun x : Fin n => sideDist s b x = k).card = 1 by rw [this, mul_one]
  rw [card_eq_one]
  unfold sideDist
  rcases hsb with ⟨rfl, rfl⟩ | ⟨rfl, rfl⟩
  · refine ⟨⟨k.toNat, by omega⟩, ?_⟩
    ext x; simp only [mem_filter, mem_univ, true_and, mem_singleton, Fin.ext_iff]; omega
  · refine ⟨⟨(n - 1 - k).toNat, by omega⟩, ?_⟩
    ext x; simp only [mem_filter, mem_univ, true_and, mem_singleton, Fin.ext_iff]; omega

open Classical in
lemma Lside_side_le (hsb : SideParam n s b) (p : Cell n → Fin n)
    (hp : p = Prod.fst ∨ p = Prod.snd) (v : Cell n) :
    Lside F.nbrs (fun v => sideDist s b (p v)) v ≤ if F.IsTurn v then 1 else 0 := by
  refine Lside_le_turn F.nbrs F.card_nbrs _ (fun v => sideDist_nonneg hsb (p v))
    (F.sideDist_step hsb p hp) F.IsTurn (fun v hv => ?_) v
  obtain ⟨u, hu, w, hw, h⟩ := F.sideDist_turn hsb p hp v hv
  exact ⟨u, hu, w, hw, by linarith⟩

open Classical in
/-- A corner of the board satisfies the hypotheses of `CornerBound`. -/
theorem corner_sum (hn : 8 ≤ n) {c : ℤ} (hc : CornerBound c) {sx bx sy bY : ℤ}
    (hx : SideParam n sx bx) (hy : SideParam n sy bY) :
    -c ≤ ∑ v ∈ univ.filter (fun v : Cell n => sideDist sx bx v.1 < 4 ∧ sideDist sy bY v.2 < 4),
      ((if F.IsTurn v then 1 else 0) - Lside F.nbrs (fun v => sideDist sx bx v.1) v -
        Lside F.nbrs (fun v => sideDist sy bY v.2) v) := by
  refine hc (Cell n) F.nbrs (fun v => sideDist sx bx v.1) (fun v => sideDist sy bY v.2)
    F.IsTurn F.card_nbrs F.symm ?_ (fun v => sideDist_nonneg hx v.1)
    (fun v => sideDist_nonneg hy v.2) ?_ ?_ ?_
  · intro v u hu
    have hk := F.isKnightMove v u hu
    unfold IsKnightMove disp at hk
    have hsx : sx = 1 ∨ sx = -1 := by rcases hx with ⟨rfl, -⟩ | ⟨rfl, -⟩ <;> simp
    have hsy : sy = 1 ∨ sy = -1 := by rcases hy with ⟨rfl, -⟩ | ⟨rfl, -⟩ <;> simp
    convert hk.mul_sign hsx hsy using 2 <;> unfold sideDist <;> ring
  · intro u w h1 h2
    unfold sideDist at h1 h2
    have e1 : (u.1 : ℕ) = w.1 := by rcases hx with ⟨rfl, rfl⟩ | ⟨rfl, rfl⟩ <;> omega
    have e2 : (u.2 : ℕ) = w.2 := by rcases hy with ⟨rfl, rfl⟩ | ⟨rfl, rfl⟩ <;> omega
    exact Prod.ext (Fin.ext e1) (Fin.ext e2)
  · intro x y hx0 hx4 hy0 hy4
    have hpt : ∀ s b z : ℤ, SideParam n s b → 0 ≤ z → z < 4 → ∃ f : Fin n, sideDist s b f = z := by
      intro s b z hsb hz0 hz4
      unfold sideDist
      rcases hsb with ⟨rfl, rfl⟩ | ⟨rfl, rfl⟩
      · exact ⟨⟨z.toNat, by omega⟩, by simp; omega⟩
      · exact ⟨⟨(n - 1 - z).toNat, by omega⟩, by simp; omega⟩
    obtain ⟨fx, hfx⟩ := hpt sx bx x hx hx0 hx4
    obtain ⟨fy, hfy⟩ := hpt sy bY y hy hy0 hy4
    exact ⟨(fx, fy), hfx, hfy⟩
  · intro v hv
    obtain ⟨u, hu, w, hw, h⟩ := F.sideDist_turn hx Prod.fst (Or.inl rfl) v hv
    obtain ⟨u', hu', w', hw', h'⟩ := F.sideDist_turn hy Prod.snd (Or.inr rfl) v hv
    -- both coordinates come from the same opposite pair
    simp only [TwoFactor.IsTurn, not_not] at hv
    obtain ⟨a, ha, a', ha', hopp⟩ := hv
    refine ⟨a, ha, a', ha', ?_, ?_⟩ <;>
    · simp only [disp, Prod.ext_iff, Prod.fst_neg, Prod.snd_neg] at hopp
      unfold sideDist
      first
        | (rcases hx with ⟨rfl, rfl⟩ | ⟨rfl, rfl⟩ <;> omega)
        | (rcases hy with ⟨rfl, rfl⟩ | ⟨rfl, rfl⟩ <;> omega)

/-- The pointwise inequality: the corner terms are at most `t - Σ_sides L` at every cell. -/
lemma pointwise (hn : 8 ≤ n) (t lL lR lB lT xL xR yB yT : ℤ)
    (hL : lL ≤ t) (hR : lR ≤ t) (hB : lB ≤ t) (hT : lT ≤ t)
    (hL0 : xL < 4 ∨ lL = 0) (hR0 : xR < 4 ∨ lR = 0) (hB0 : yB < 4 ∨ lB = 0)
    (hT0 : yT < 4 ∨ lT = 0) (hx : xL + xR = n - 1) (hy : yB + yT = n - 1) :
    (if xL < 4 ∧ yB < 4 then t - lL - lB else 0) + (if xR < 4 ∧ yB < 4 then t - lR - lB else 0) +
      (if xL < 4 ∧ yT < 4 then t - lL - lT else 0) + (if xR < 4 ∧ yT < 4 then t - lR - lT else 0)
      ≤ t - lL - lR - lB - lT := by
  split_ifs <;> omega

open Classical in
/-- **Turns from a corner bound.** If every corner loses at most `c`, every 2-factor of the
`n × n` knight graph, `n ≥ 8`, has at least `8 n - 4 c` turns. -/
theorem eight_mul_le_numTurns_add_of_cornerBound (hn : 8 ≤ n) {c : ℤ} (hc : CornerBound c) :
    8 * (n : ℤ) ≤ F.numTurns + 4 * c := by
  have side := fun {s b : ℤ} (hsb : SideParam n s b) (p : Cell n → Fin n)
    (hp : p = Prod.fst ∨ p = Prod.snd) => F.sum_Lside_side (by omega) hsb p hp
  have pL : SideParam n 1 0 := Or.inl ⟨rfl, rfl⟩
  have pR : SideParam n (-1) (n - 1) := Or.inr ⟨rfl, rfl⟩
  have sL := side pL Prod.fst (Or.inl rfl)
  have sR := side pR Prod.fst (Or.inl rfl)
  have sB := side pL Prod.snd (Or.inr rfl)
  have sT := side pR Prod.snd (Or.inr rfl)
  have cLB := F.corner_sum hn hc pL pL
  have cRB := F.corner_sum hn hc pR pL
  have cLT := F.corner_sum hn hc pL pR
  have cRT := F.corner_sum hn hc pR pR
  have hT : (F.numTurns : ℤ) = ∑ v, (if F.IsTurn v then 1 else 0 : ℤ) := by
    unfold numTurns; rw [card_filter]; push_cast; rfl
  have zero : ∀ {s b : ℤ} (p : Cell n → Fin n) (v : Cell n),
      sideDist s b (p v) < 4 ∨ Lside F.nbrs (fun v => sideDist s b (p v)) v = 0 := by
    intro s b p v
    by_cases h : sideDist s b (p v) < 4
    · exact Or.inl h
    · exact Or.inr (Lside_eq_zero (by simpa using h))
  have hpt := fun v : Cell n => pointwise hn (if F.IsTurn v then 1 else 0) _ _ _ _ _ _ _ _
    (F.Lside_side_le pL Prod.fst (Or.inl rfl) v) (F.Lside_side_le pR Prod.fst (Or.inl rfl) v)
    (F.Lside_side_le pL Prod.snd (Or.inr rfl) v) (F.Lside_side_le pR Prod.snd (Or.inr rfl) v)
    (zero Prod.fst v) (zero Prod.fst v) (zero Prod.snd v) (zero Prod.snd v)
    (by unfold sideDist; ring) (by unfold sideDist; ring)
  have hsum := sum_le_sum fun v (_ : v ∈ univ) => hpt v
  simp only [sum_add_distrib, sum_sub_distrib] at hsum
  rw [← sum_filter, ← sum_filter, ← sum_filter, ← sum_filter] at hsum
  rw [hT]
  linarith

open Classical in
/-- **Main theorem for 2-factors, constant 28.** Every 2-factor of the knight's graph on the
`n × n` board, `n ≥ 8`, has at least `8 * n - 28` turns. -/
theorem eight_mul_le_numTurns_add_28 (hn : 8 ≤ n) : 8 * n ≤ F.numTurns + 28 := by
  have := F.eight_mul_le_numTurns_add_of_cornerBound hn cornerBound_seven
  omega

end TwoFactor

/-- **Main theorem, constant 28.** Every closed knight's tour of the `n × n` board, `n ≥ 8`,
has at least `8 * n - 28` turns. -/
theorem ClosedTour.eight_mul_sub_28_le_numTurns (T : ClosedTour n) (hn : 8 ≤ n) :
    8 * n - 28 ≤ T.numTurns := by
  have := (T.toTwoFactor (by omega)).eight_mul_le_numTurns_add_28 hn
  rw [T.numTurns_toTwoFactor] at this
  omega

end KT
