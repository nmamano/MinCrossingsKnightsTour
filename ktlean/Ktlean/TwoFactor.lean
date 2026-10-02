import Ktlean.Basic
import Ktlean.Strip

/-!
# Turns of 2-factors

The strip lemma at the four sides of the board, and the bound `8 * n - 64` for 2-factors.
-/

open Finset

namespace KT

variable {n : ℕ}

lemma IsKnightVec.bounds {d : ℤ × ℤ} (h : IsKnightVec d) :
    (-2 ≤ d.1 ∧ d.1 ≤ 2 ∧ d.1 ≠ 0) ∧ (-2 ≤ d.2 ∧ d.2 ≤ 2 ∧ d.2 ≠ 0) := by
  unfold IsKnightVec at h
  rcases h with ⟨h1, h2⟩ | ⟨h1, h2⟩ <;>
  · rw [abs_eq (by norm_num)] at h1 h2
    omega

lemma card_filter_comp_proj (p : Cell n → Fin n) (hp : p = Prod.fst ∨ p = Prod.snd)
    (g : Fin n → Prop) [DecidablePred g] :
    (univ.filter fun v : Cell n => g (p v)).card = n * (univ.filter g).card := by
  rcases hp with rfl | rfl
  · rw [show (univ.filter fun v : Cell n => g v.1) = (univ.filter g) ×ˢ univ by
      ext v; simp, card_product, card_univ, Fintype.card_fin, mul_comm]
  · rw [show (univ.filter fun v : Cell n => g v.2) = univ ×ˢ (univ.filter g) by
      ext v; simp, card_product, card_univ, Fintype.card_fin]

open Classical in
/-- The strip lemma for one side of the board. The function `v ↦ s * p v + b` is the distance
from one of the four sides (`p` is a coordinate, `s = ±1`). -/
theorem TwoFactor.two_mul_le_strip (F : TwoFactor n) (hn : 4 ≤ n) (p : Cell n → Fin n)
    (hp : p = Prod.fst ∨ p = Prod.snd) (s b : ℤ) (hsb : (s = 1 ∧ b = 0) ∨ (s = -1 ∧ b = n - 1)) :
    2 * n ≤ (univ.filter fun v => F.IsTurn v ∧ s * (p v : ℤ) + b < 4).card := by
  apply strip_lemma F.nbrs F.card_nbrs F.symm (fun v => s * (p v : ℤ) + b)
  · intro v
    have := (p v).isLt
    rcases hsb with ⟨rfl, rfl⟩ | ⟨rfl, rfl⟩ <;> omega
  · intro v u hu
    have hk := (F.isKnightMove v u hu).bounds
    simp only [disp] at hk
    rcases hp with rfl | rfl <;> rcases hsb with ⟨rfl, rfl⟩ | ⟨rfl, rfl⟩ <;> omega
  · intro v hv
    simp only [TwoFactor.IsTurn, not_not] at hv
    obtain ⟨u, hu, w, hw, h⟩ := hv
    refine ⟨u, hu, w, hw, ?_⟩
    simp only [disp, Prod.ext_iff, Prod.fst_neg, Prod.snd_neg] at h
    rcases hp with rfl | rfl <;> rcases hsb with ⟨rfl, rfl⟩ | ⟨rfl, rfl⟩ <;> omega
  · intro k hk0 hk4
    rw [card_filter_comp_proj p hp (fun x => s * (x : ℤ) + b = k)]
    suffices (univ.filter fun x : Fin n => s * (x : ℤ) + b = k).card = 1 by rw [this, mul_one]
    rw [card_eq_one]
    rcases hsb with ⟨rfl, rfl⟩ | ⟨rfl, rfl⟩
    · refine ⟨⟨k.toNat, by omega⟩, ?_⟩
      ext x; simp only [mem_filter, mem_univ, true_and, mem_singleton, Fin.ext_iff]; omega
    · refine ⟨⟨(n - 1 - k).toNat, by omega⟩, ?_⟩
      ext x; simp only [mem_filter, mem_univ, true_and, mem_singleton, Fin.ext_iff]; omega

/-- At most 8 values of a coordinate lie within distance 4 of one of the two sides. -/
lemma card_near_side_le (n : ℕ) :
    (univ.filter fun x : Fin n => 1 * (x : ℤ) + 0 < 4 ∨ -1 * (x : ℤ) + (n - 1) < 4).card ≤ 8 := by
  rw [filter_or]
  refine (card_union_le _ _).trans ?_
  have h1 : (univ.filter fun x : Fin n => 1 * (x : ℤ) + 0 < 4).card ≤ (range 4).card :=
    card_le_card_of_injOn (fun x => (x : ℕ)) (by intro a ha; simp at ha ⊢; omega)
      (by intro a _ b _ h; exact Fin.ext h)
  have h2 : (univ.filter fun x : Fin n => -1 * (x : ℤ) + (n - 1) < 4).card ≤ (range 4).card :=
    card_le_card_of_injOn (fun x => n - 1 - (x : ℕ))
      (by intro a ha; simp at ha ⊢; have := a.isLt; omega)
      (by intro a _ b _ h; have := a.isLt; have := b.isLt; simp at h; exact Fin.ext (by omega))
  simp only [card_range] at h1 h2
  omega

open Classical in
/-- **Main theorem for 2-factors.** Every 2-factor of the knight's graph on the `n × n` board,
`n ≥ 8`, has at least `8 * n - 64` turns. -/
theorem TwoFactor.eight_mul_le_numTurns_add (F : TwoFactor n) (hn : 8 ≤ n) :
    8 * n ≤ F.numTurns + 64 := by
  have hL := F.two_mul_le_strip (by omega) Prod.fst (Or.inl rfl) 1 0 (Or.inl ⟨rfl, rfl⟩)
  have hR := F.two_mul_le_strip (by omega) Prod.fst (Or.inl rfl) (-1) (n - 1) (Or.inr ⟨rfl, rfl⟩)
  have hB := F.two_mul_le_strip (by omega) Prod.snd (Or.inr rfl) 1 0 (Or.inl ⟨rfl, rfl⟩)
  have hT := F.two_mul_le_strip (by omega) Prod.snd (Or.inr rfl) (-1) (n - 1) (Or.inr ⟨rfl, rfl⟩)
  simp only [filter_and] at hL hR hB hT
  set S := univ.filter F.IsTurn
  set E := univ.filter fun x : Fin n => 1 * (x : ℤ) + 0 < 4 ∨ -1 * (x : ℤ) + (n - 1) < 4
  -- two disjoint opposite strips
  have pair : ∀ p : Cell n → Fin n,
      (S ∩ univ.filter fun v => 1 * (p v : ℤ) + 0 < 4).card +
        (S ∩ univ.filter fun v => -1 * (p v : ℤ) + (n - 1) < 4).card =
      (S ∩ univ.filter fun v => p v ∈ E).card := by
    intro p
    rw [← card_union_of_disjoint, ← inter_union_distrib_left, ← filter_or]
    · congr 2; ext v; simp [E]
    · refine disjoint_of_subset_left inter_subset_right
        (disjoint_of_subset_right inter_subset_right
          (disjoint_filter.2 fun v _ h h' => by omega))
  have hV := pair Prod.fst
  have hH := pair Prod.snd
  -- the overlap of the two unions of strips is the four corner squares
  have hcorner : ((univ.filter fun v : Cell n => v.1 ∈ E) ∩
      (univ.filter fun v : Cell n => v.2 ∈ E)).card ≤ 64 := by
    rw [← filter_and, show (univ.filter fun v : Cell n => v.1 ∈ E ∧ v.2 ∈ E) = E ×ˢ E by
      ext v; simp, card_product]
    have := card_near_side_le n
    nlinarith
  have hincl := card_union_add_card_inter (S ∩ univ.filter fun v => v.1 ∈ E)
    (S ∩ univ.filter fun v => v.2 ∈ E)
  have hu : (S ∩ (univ.filter fun v => v.1 ∈ E) ∪ S ∩ univ.filter fun v => v.2 ∈ E).card ≤
      S.card := card_le_card (union_subset inter_subset_left inter_subset_left)
  have hi : ((S ∩ univ.filter fun v => v.1 ∈ E) ∩ S ∩ univ.filter fun v => v.2 ∈ E).card ≤ 64 :=
    (card_le_card (by
      intro v hv; simp only [mem_inter] at hv ⊢; exact ⟨hv.1.1.2, hv.2⟩)).trans hcorner
  have hS : F.numTurns = S.card := by
    unfold TwoFactor.numTurns; congr 1
  rw [← inter_assoc] at hincl
  omega

end KT
