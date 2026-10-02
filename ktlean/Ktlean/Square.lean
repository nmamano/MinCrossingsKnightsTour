import Ktlean.TileBudget

/-!
# Square defects (KT Turns Theory, FINDINGS.md sections 9.1 and 9.2)

* `mult_alt`: in every unit square, the multiplicities of the four quarter triangles satisfy
  `m₀ + m₂ = m₁ + m₃` (9.1). A knight tile meets two unit squares, in two adjacent quarters each.
* `two_bad`: so a square with one quarter of multiplicity `≠ 1` has a second one.
* `charged_squares_budget` (9.2): `L` charged steps whose beside-squares lie in pairwise disjoint
  sets of squares, with all quarters of these squares in `U`, give `2L + 8n + #Bo ≤ 2Y + 4`.
  (With `Y = 2X`, `#Bo = 2|B|`: `2L ≤ 4X - 8n + 4 - 2|B|`.)
-/

open Finset

namespace KT

/-- The unit square (lower-left corner) of a quarter triangle. -/
def sqOf (t : QTri) : Pt := (t.1, t.2.1)

lemma tri0_alt_rel : ∀ d ∈ knightVecs, ∀ x ∈ Icc (-2 : ℤ) 1, ∀ y ∈ Icc (-2 : ℤ) 1,
    (if (x, y, 0) ∈ tri0 d then 1 else 0) + (if (x, y, 2) ∈ tri0 d then 1 else 0) =
      (if (x, y, 1) ∈ tri0 d then 1 else 0) + (if (x, y, 3) ∈ tri0 d then (1 : ℕ) else 0) := by
  decide +kernel

lemma tri_alt {p d : Pt} (hd : d ∈ knightVecs) (x y : ℤ) :
    (if (x, y, 0) ∈ tri p d then 1 else 0) + (if (x, y, 2) ∈ tri p d then 1 else 0) =
      (if (x, y, 1) ∈ tri p d then 1 else 0) + (if (x, y, 3) ∈ tri p d then (1 : ℕ) else 0) := by
  simp only [mem_tri_iff]
  by_cases h : x - p.1 ∈ Icc (-2 : ℤ) 1 ∧ y - p.2 ∈ Icc (-2 : ℤ) 1
  · exact tri0_alt_rel d hd _ h.1 _ h.2
  · have hn : ∀ k : Fin 4, (x - p.1, y - p.2, k) ∉ tri0 d := by
      intro k hk
      have := mem_tri0_bounds hd hk
      simp only at this
      simp only [mem_Icc] at h
      omega
    simp [hn]

variable {ι : Type*} [Fintype ι] (a d : ι → Pt)

lemma mult_eq_sum (t : QTri) : mult a d t = ∑ i, if t ∈ tri (a i) (d i) then 1 else 0 := by
  rw [mult, card_filter]

/-- **(9.1)** The alternating sum of the multiplicities in a unit square is zero. -/
theorem mult_alt (hd : ∀ i, d i ∈ knightVecs) (x y : ℤ) :
    mult a d (x, y, 0) + mult a d (x, y, 2) = mult a d (x, y, 1) + mult a d (x, y, 3) := by
  simp only [mult_eq_sum, ← sum_add_distrib]
  exact sum_congr rfl fun i _ => tri_alt (hd i) x y

/-- A square with one bad quarter has a second bad quarter. -/
theorem two_bad (hd : ∀ i, d i ∈ knightVecs) {t : QTri} (ht : mult a d t ≠ 1) :
    ∃ t', t' ≠ t ∧ sqOf t' = sqOf t ∧ mult a d t' ≠ 1 := by
  obtain ⟨x, y, k⟩ := t
  have h := mult_alt a d hd x y
  by_contra hc
  push Not at hc
  have hk : ∀ j : Fin 4, j ≠ k → mult a d (x, y, j) = 1 := fun j hj =>
    hc (x, y, j) (by simp [hj]) (by simp [sqOf])
  fin_cases k
  · rw [hk 1 (by decide), hk 2 (by decide), hk 3 (by decide)] at h
    simp only [Fin.zero_eta, Fin.isValue] at ht h; omega
  · rw [hk 0 (by decide), hk 2 (by decide), hk 3 (by decide)] at h
    simp only [Fin.mk_one, Fin.isValue] at ht h; omega
  · rw [hk 0 (by decide), hk 1 (by decide), hk 3 (by decide)] at h
    simp only [Fin.reduceFinMk, Fin.isValue] at ht h; omega
  · rw [hk 0 (by decide), hk 1 (by decide), hk 2 (by decide)] at h
    simp only [Fin.reduceFinMk, Fin.isValue] at ht h; omega

variable [DecidableEq ι]

/-- **Charged squares cost crossings (9.2).** Let `sq k` (`k < L`) be pairwise disjoint sets of
unit squares, all of whose quarter triangles lie in `U`. If each `sq k` contains both squares
beside a step `q` where `ω(q) = flux(q) + χ(q)` is not `0` mod 3, then
`2L + 8n + #Bo ≤ 2Y + 4`. -/
theorem charged_squares_budget (n : ℕ) (hd : ∀ i, d i ∈ knightVecs)
    (ha : ∀ i, 0 ≤ (a i).1 ∧ (a i).1 < n ∧ 0 ≤ (a i).2 ∧ (a i).2 < n)
    (hb : ∀ i, 0 ≤ (a i + d i).1 ∧ (a i + d i).1 < n ∧ 0 ≤ (a i + d i).2 ∧ (a i + d i).2 < n)
    (hdist : ∀ i j, i ≠ j →
      ¬ ((a i = a j ∧ a i + d i = a j + d j) ∨ (a i = a j + d j ∧ a i + d i = a j)))
    (hcard : Fintype.card ι = n * n)
    (U : Finset QTri) (hU : U ⊆ boardTris n) (Bo : Finset (ι × ι)) (hBo : Bo ⊆ crossPairs a d)
    (hBoU : ∀ p ∈ Bo, ∀ t ∈ U, ¬ (t ∈ tri (a p.1) (d p.1) ∧ t ∈ tri (a p.2) (d p.2)))
    (L : ℕ) (sq : Fin L → Finset Pt)
    (hdisj : ∀ k l, k ≠ l → Disjoint (sq k) (sq l))
    (hsqU : ∀ k, ∀ s ∈ sq k, ∀ j : Fin 4, (s.1, s.2, j) ∈ U)
    (hcharged : ∀ k, ∃ q, sqOf (nearLo q) ∈ sq k ∧ sqOf (nearHi q) ∈ sq k ∧
      ¬ (3 : ℤ) ∣ flux a d q + chi q.1) :
    2 * L + 8 * n + Bo.card ≤ 2 * (crossPairs a d).card + 4 := by
  set D := U.filter fun t => mult a d t ≠ 1
  have hU' : ∀ k, ∀ t, sqOf t ∈ sq k → t ∈ U := by
    intro k t ht
    obtain ⟨x, y, j⟩ := t
    exact hsqU k _ ht j
  have hbad : ∀ k, 2 ≤ (D.filter fun t => sqOf t ∈ sq k).card := by
    intro k
    obtain ⟨q, hlo, hhi, hnd⟩ := hcharged k
    obtain ⟨t, hts, htb⟩ : ∃ t, sqOf t ∈ sq k ∧ mult a d t ≠ 1 := by
      by_cases h1 : mult a d (nearLo q) = 1
      · by_cases h2 : mult a d (nearHi q) = 1
        · exact absurd (three_dvd_flux_add_chi a d hd q h1 h2) hnd
        · exact ⟨_, hhi, h2⟩
      · exact ⟨_, hlo, h1⟩
    obtain ⟨t', hne, hsq, htb'⟩ := two_bad a d hd htb
    have hsub : ({t, t'} : Finset QTri) ⊆ D.filter fun t => sqOf t ∈ sq k := by
      intro s hs
      simp only [mem_insert, mem_singleton] at hs
      simp only [D, mem_filter]
      rcases hs with rfl | rfl
      · exact ⟨⟨hU' k _ hts, htb⟩, hts⟩
      · exact ⟨⟨hU' k _ (hsq ▸ hts), htb'⟩, hsq ▸ hts⟩
    have := card_le_card hsub
    rwa [card_pair hne.symm] at this
  have hsum : ∑ k, (D.filter fun t => sqOf t ∈ sq k).card ≤ D.card := by
    rw [← card_biUnion]
    · exact card_le_card (biUnion_subset.2 fun k _ => filter_subset _ _)
    · intro k _ l _ hkl
      rw [Function.onFun, disjoint_left]
      intro t h1 h2
      exact disjoint_left.1 (hdisj k l hkl) (mem_filter.1 h1).2 (mem_filter.1 h2).2
  have h2L : 2 * L ≤ D.card := by
    calc 2 * L = ∑ _k : Fin L, 2 := by simp [mul_comm]
      _ ≤ ∑ k, (D.filter fun t => sqOf t ∈ sq k).card := sum_le_sum fun k _ => hbad k
      _ ≤ D.card := hsum
  have hB : D.card + 8 * n + Bo.card ≤ 2 * (crossPairs a d).card + 4 :=
    bad_budget a d n hd ha hb hdist hcard U hU Bo hBo hBoU
  omega

end KT
