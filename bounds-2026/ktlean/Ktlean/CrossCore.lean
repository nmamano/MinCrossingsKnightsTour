import Ktlean.Tiles

/-!
# The tile counting argument

For `n * n` distinct knight edges inside the board `[0, n-1]²`, at least `8 * n - 4` ordered
pairs of distinct edges cross properly. Also: a proper crossing makes the two open segments of
the real plane intersect.
-/

open Finset

namespace KT

lemma tri_card {a d : Pt} (hd : d ∈ knightVecs) : (tri a d).card = 4 := by
  rw [tri, card_image_of_injective _ (shift_injective a), tri0_card d hd]

lemma mem_tri_bounds {a d : Pt} (hd : d ∈ knightVecs) {t : QTri} (ht : t ∈ tri a d) :
    a.1 + min 0 d.1 ≤ t.1 ∧ t.1 < a.1 + max 0 d.1 ∧
      a.2 + min 0 d.2 ≤ t.2.1 ∧ t.2.1 < a.2 + max 0 d.2 := by
  obtain ⟨s, hs, rfl⟩ := mem_image.1 ht
  have := tri0_bounds d hd s hs
  simp only [shift]
  omega

lemma tri_eq_image (a b d : Pt) : tri b d = (tri (b - a) d).image (shift a) := by
  rw [tri, tri, image_image]
  congr 1
  funext t
  simp only [shift, Function.comp, Prod.fst_sub, Prod.snd_sub]
  ext <;> simp <;> ring

lemma det_sub (a b c s : Pt) : det (a - s) (b - s) (c - s) = det a b c := by
  simp only [det, Prod.fst_sub, Prod.snd_sub]; ring

lemma properCross_sub (a b c d s : Pt) :
    ProperCross (a - s) (b - s) (c - s) (d - s) ↔ ProperCross a b c d := by
  simp only [ProperCross, det_sub]

lemma properCross_comm (a b c d : Pt) : ProperCross a b c d ↔ ProperCross c d a b := by
  unfold ProperCross; exact And.comm

/-- The finite certificate, for edges in any position. -/
lemma tri_inter_card_le {a b d e : Pt} (hd : d ∈ knightVecs) (he : e ∈ knightVecs)
    (hne : ¬ ((a = b ∧ a + d = b + e) ∨ (a = b + e ∧ a + d = b))) :
    (tri a d ∩ tri b e).card ≤ 2 * (if ProperCross a (a + d) b (b + e) then 1 else 0) := by
  by_cases hnear : |(b - a).1| ≤ 3 ∧ |(b - a).2| ≤ 3
  · have hx := abs_le.1 hnear.1
    have hy := abs_le.1 hnear.2
    have key := tri0_inter_le (b - a).1 (mem_Icc.2 hx) (b - a).2 (mem_Icc.2 hy) d hd e he (by
        intro h
        apply hne
        simp only [Prod.ext_iff, Prod.fst_add, Prod.snd_add, Prod.fst_sub, Prod.snd_sub,
          Prod.fst_zero, Prod.snd_zero] at h ⊢
        omega)
    simp only [Prod.mk.eta] at key
    have hpc : ProperCross a (a + d) b (b + e) ↔ ProperCross 0 d (b - a) (b - a + e) := by
      rw [← properCross_sub a (a + d) b (b + e) a, show a - a = 0 by abel,
        show a + d - a = d by abel, show b + e - a = b - a + e by abel]
    rw [if_congr hpc rfl rfl, tri_eq_image a a d, tri_eq_image a b e,
      ← image_inter _ _ (shift_injective a), card_image_of_injective _ (shift_injective a),
      sub_self, show tri 0 d = tri0 d by ext t; simp [tri, shift]]
    exact key
  · have : tri a d ∩ tri b e = ∅ := by
      rw [eq_empty_iff_forall_notMem]
      intro t ht
      rw [mem_inter] at ht
      have h1 := mem_tri_bounds hd ht.1
      have h2 := mem_tri_bounds he ht.2
      have := tri0_bounds d hd
      simp only [knightVecs, mem_insert, mem_singleton] at hd he
      apply hnear
      simp only [Prod.fst_sub, Prod.snd_sub, abs_le]
      rcases hd with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl <;>
      rcases he with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl <;>
      simp at h1 h2 <;> omega
    rw [this]; simp

lemma three_mul_le_two_add_sq (m : ℕ) : 3 * m ≤ 2 + m ^ 2 := by
  rcases Nat.lt_or_ge m 2 with h | h
  · interval_cases m <;> simp
  · nlinarith

/-- **The tile counting argument.** `n * n` distinct knight edges inside `[0, n-1]²` (edge `i`
goes from `a i` to `a i + d i`) have at least `8 * n - 4` ordered pairs of distinct edges that
cross properly. -/
theorem eight_mul_le_properCross_pairs {ι : Type*} [Fintype ι] [DecidableEq ι] (n : ℕ)
    (a d : ι → Pt) (hd : ∀ i, d i ∈ knightVecs)
    (ha : ∀ i, 0 ≤ (a i).1 ∧ (a i).1 < n ∧ 0 ≤ (a i).2 ∧ (a i).2 < n)
    (hb : ∀ i, 0 ≤ (a i + d i).1 ∧ (a i + d i).1 < n ∧ 0 ≤ (a i + d i).2 ∧ (a i + d i).2 < n)
    (hdist : ∀ i j, i ≠ j →
      ¬ ((a i = a j ∧ a i + d i = a j + d j) ∨ (a i = a j + d j ∧ a i + d i = a j)))
    (hcard : Fintype.card ι = n * n) :
    8 * n ≤ (univ.filter fun p : ι × ι =>
      p.1 ≠ p.2 ∧ ProperCross (a p.1) (a p.1 + d p.1) (a p.2) (a p.2 + d p.2)).card + 4 := by
  rcases Nat.eq_zero_or_pos n with rfl | hn
  · simp
  obtain ⟨k, rfl⟩ : ∃ k, n = k + 1 := ⟨n - 1, by omega⟩
  -- the quarter triangles of the board
  set T : Finset QTri := Icc 0 (k - 1 : ℤ) ×ˢ (Icc 0 (k - 1 : ℤ) ×ˢ (univ : Finset (Fin 4)))
  have hT : T.card = k * (k * 4) := by
    simp only [T, card_product, Int.card_Icc, card_univ, Fintype.card_fin]
    rw [show (k - 1 + 1 - 0 : ℤ) = k by ring, Int.toNat_natCast]
  set tile : ι → Finset QTri := fun i => tri (a i) (d i)
  have htile_card : ∀ i, (tile i).card = 4 := fun i => tri_card (hd i)
  have hsub : ∀ i, tile i ⊆ T := by
    intro i t ht
    have h1 := mem_tri_bounds (hd i) ht
    have h2 := ha i
    have h3 := hb i
    simp only [Prod.fst_add, Prod.snd_add] at h3
    simp only [T, mem_product, mem_Icc, mem_univ, and_true]
    have := min_le_left 0 (d i).1
    have := min_le_right 0 (d i).1
    have := le_max_left 0 (d i).1
    have := le_max_right 0 (d i).1
    have := min_le_left 0 (d i).2
    have := min_le_right 0 (d i).2
    have := le_max_left 0 (d i).2
    have := le_max_right 0 (d i).2
    have hm1 : min 0 (d i).1 = 0 ∨ min 0 (d i).1 = (d i).1 := min_choice _ _
    have hm2 : min 0 (d i).2 = 0 ∨ min 0 (d i).2 = (d i).2 := min_choice _ _
    have hM1 : max 0 (d i).1 = 0 ∨ max 0 (d i).1 = (d i).1 := max_choice _ _
    have hM2 : max 0 (d i).2 = 0 ∨ max 0 (d i).2 = (d i).2 := max_choice _ _
    push_cast at h2 h3 ⊢
    omega
  -- multiplicity of a quarter triangle
  set m : QTri → ℕ := fun t => ∑ i, if t ∈ tile i then 1 else 0
  have S1 : ∑ t ∈ T, m t = 4 * Fintype.card ι := by
    simp only [m]
    rw [sum_comm]
    have : ∀ i, ∑ t ∈ T, (if t ∈ tile i then 1 else 0) = 4 := by
      intro i
      rw [← card_filter, filter_mem_eq_inter, inter_eq_right.2 (hsub i), htile_card]
    simp [this, mul_comm]
  have S2 : ∑ t ∈ T, m t ^ 2 = ∑ i, ∑ j, (tile i ∩ tile j).card := by
    simp only [m, sq, sum_mul_sum]
    rw [sum_comm]
    refine sum_congr rfl fun i _ => ?_
    rw [sum_comm]
    refine sum_congr rfl fun j _ => ?_
    have : ∀ t, (if t ∈ tile i then 1 else 0) * (if t ∈ tile j then 1 else 0) =
        if t ∈ tile i ∩ tile j then 1 else 0 := by
      intro t
      by_cases h1 : t ∈ tile i <;> by_cases h2 : t ∈ tile j <;> simp [h1, h2]
    rw [sum_congr rfl fun t _ => this t, ← card_filter, filter_mem_eq_inter,
      inter_eq_right.2 (inter_subset_left.trans (hsub i))]
  set Y := (univ.filter fun p : ι × ι =>
      p.1 ≠ p.2 ∧ ProperCross (a p.1) (a p.1 + d p.1) (a p.2) (a p.2 + d p.2)).card
  have P1 : 3 * ∑ t ∈ T, m t ≤ 2 * T.card + ∑ t ∈ T, m t ^ 2 := by
    rw [mul_sum, card_eq_sum_ones, mul_sum, ← sum_add_distrib]
    exact sum_le_sum fun t _ => by simpa using three_mul_le_two_add_sq (m t)
  have P2 : ∀ i j, (tile i ∩ tile j).card ≤ (if i = j then 4 else 0) +
      2 * (if i ≠ j ∧ ProperCross (a i) (a i + d i) (a j) (a j + d j) then 1 else 0) := by
    intro i j
    by_cases hij : i = j
    · subst hij; simp [htile_card]
    · simp only [hij, ite_false, ne_eq, not_false_eq_true, true_and, zero_add]
      exact tri_inter_card_le (hd i) (hd j) (hdist i j hij)
  have P3 : ∑ i, ∑ j, (tile i ∩ tile j).card ≤ 4 * Fintype.card ι + 2 * Y := by
    refine (sum_le_sum fun i _ => sum_le_sum fun j _ => P2 i j).trans (le_of_eq ?_)
    simp only [sum_add_distrib, sum_ite_eq, mem_univ, ite_true, ← mul_sum, Y, card_filter,
      Fintype.sum_prod_type]
    simp [mul_comm]
  rw [hcard] at S1 P3
  rw [hT, S1, S2] at P1
  nlinarith

/-- Orientation determinant in the real plane. -/
def detR (a b c : ℝ × ℝ) : ℝ := (b.1 - a.1) * (c.2 - a.2) - (b.2 - a.2) * (c.1 - a.1)

/-- If `C, D` are strictly on opposite sides of the line `AB` and `A, B` are strictly on
opposite sides of the line `CD`, then the open segments `AB` and `CD` intersect. -/
lemma openSegment_inter_nonempty {A B C D : ℝ × ℝ} (h1 : detR A B C * detR A B D < 0)
    (h2 : detR C D A * detR C D B < 0) :
    (openSegment ℝ A B ∩ openSegment ℝ C D).Nonempty := by
  have hD : detR C D A - detR C D B ≠ 0 := by
    intro h
    rw [show detR C D A = detR C D B by linarith] at h2
    nlinarith [mul_self_nonneg (detR C D B)]
  have hE : detR A B C - detR A B D ≠ 0 := by
    intro h
    rw [show detR A B C = detR A B D by linarith] at h1
    nlinarith [mul_self_nonneg (detR A B D)]
  refine ⟨(-detR C D B / (detR C D A - detR C D B)) • A +
      (detR C D A / (detR C D A - detR C D B)) • B,
    ⟨_, _, ?_, ?_, ?_, rfl⟩, ⟨-detR A B D / (detR A B C - detR A B D),
      detR A B C / (detR A B C - detR A B D), ?_, ?_, ?_, ?_⟩⟩
  · rcases mul_neg_iff.1 h2 with ⟨p, q⟩ | ⟨p, q⟩
    · exact div_pos (by linarith) (by linarith)
    · exact div_pos_iff.2 (Or.inr ⟨by linarith, by linarith⟩)
  · rcases mul_neg_iff.1 h2 with ⟨p, q⟩ | ⟨p, q⟩
    · exact div_pos (by linarith) (by linarith)
    · exact div_pos_iff.2 (Or.inr ⟨by linarith, by linarith⟩)
  · rw [← add_div, div_eq_one_iff_eq hD]; ring
  · rcases mul_neg_iff.1 h1 with ⟨p, q⟩ | ⟨p, q⟩
    · exact div_pos (by linarith) (by linarith)
    · exact div_pos_iff.2 (Or.inr ⟨by linarith, by linarith⟩)
  · rcases mul_neg_iff.1 h1 with ⟨p, q⟩ | ⟨p, q⟩
    · exact div_pos (by linarith) (by linarith)
    · exact div_pos_iff.2 (Or.inr ⟨by linarith, by linarith⟩)
  · rw [← add_div, div_eq_one_iff_eq hE]; ring
  · simp only [detR] at hD hE ⊢
    ext <;> simp only [Prod.fst_add, Prod.snd_add, Prod.smul_fst, Prod.smul_snd, smul_eq_mul] <;>
      field_simp <;> ring

end KT
