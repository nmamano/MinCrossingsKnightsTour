import Ktlean.Flux

/-!
# The excess-crossing budget (KT Turns Theory, FINDINGS.md sections 6.4 and 6.5)

For `n * n` distinct knight edges in the board `[0, n-1]²`, let `Y` be the number of ordered
pairs of distinct edges that cross properly (`Y = 2X` for `X` unordered pairs).

* `bad_budget`: let `U` be a set of quarter triangles of the board, and `Bo` a set of ordered
  properly crossing pairs whose tile overlaps avoid `U`. The number of quarter triangles in `U`
  whose multiplicity is not one satisfies `#bad + 8n + #Bo ≤ 2Y + 4`.
  (With `Y = 2X` and `#Bo = 2|B|`: `#bad ≤ 4X - 8n + 4 - 2|B|`.)
* `charged_paths_budget`: `L` pairwise disjoint sets of grid edges ("dual paths"), each with a
  step `q` where `ω = flux + χ` is not `0` mod 3, and with all their beside-triangles in `U`,
  satisfy `L + 8n + #Bo ≤ 2Y + 4`.
-/

open Finset

namespace KT

variable {ι : Type*} [Fintype ι] (a d : ι → Pt)

lemma sum_mult (S : Finset QTri) :
    ∑ t ∈ S, mult a d t = ∑ i, (tri (a i) (d i) ∩ S).card := by
  simp only [mult, card_filter]
  rw [sum_comm]
  refine sum_congr rfl fun i _ => ?_
  rw [← card_filter, filter_mem_eq_inter, inter_comm]

lemma sum_mult_sq (S : Finset QTri) :
    ∑ t ∈ S, mult a d t ^ 2 = ∑ i, ∑ j, (tri (a i) (d i) ∩ tri (a j) (d j) ∩ S).card := by
  simp only [mult, card_filter, sq, sum_mul_sum]
  rw [sum_comm]
  refine sum_congr rfl fun i _ => ?_
  rw [sum_comm]
  refine sum_congr rfl fun j _ => ?_
  have : ∀ t, (if t ∈ tri (a i) (d i) then 1 else 0) * (if t ∈ tri (a j) (d j) then 1 else 0) =
      if t ∈ tri (a i) (d i) ∩ tri (a j) (d j) then 1 else 0 := by
    intro t
    by_cases h1 : t ∈ tri (a i) (d i) <;> by_cases h2 : t ∈ tri (a j) (d j) <;> simp [h1, h2]
  rw [sum_congr rfl fun t _ => this t, ← card_filter, filter_mem_eq_inter, inter_comm]

/-- The quarter triangles of the board `[0, n-1]²`. -/
def boardTris (n : ℕ) : Finset QTri :=
  Icc 0 ((n : ℤ) - 2) ×ˢ (Icc 0 ((n : ℤ) - 2) ×ˢ (univ : Finset (Fin 4)))

variable [DecidableEq ι]

lemma tri_subset_boardTris (n : ℕ) {p e : Pt} (he : e ∈ knightVecs)
    (hp : 0 ≤ p.1 ∧ p.1 < n ∧ 0 ≤ p.2 ∧ p.2 < n)
    (hq : 0 ≤ (p + e).1 ∧ (p + e).1 < n ∧ 0 ≤ (p + e).2 ∧ (p + e).2 < n) :
    tri p e ⊆ boardTris n := by
  intro t ht
  have h1 := mem_tri_bounds he ht
  simp only [Prod.fst_add, Prod.snd_add] at hq
  simp only [boardTris, mem_product, mem_Icc, mem_univ, and_true]
  have hm1 : min 0 e.1 = 0 ∨ min 0 e.1 = e.1 := min_choice _ _
  have hm2 : min 0 e.2 = 0 ∨ min 0 e.2 = e.2 := min_choice _ _
  have hM1 : max 0 e.1 = 0 ∨ max 0 e.1 = e.1 := max_choice _ _
  have hM2 : max 0 e.2 = 0 ∨ max 0 e.2 = e.2 := max_choice _ _
  have := min_le_left 0 e.1; have := min_le_right 0 e.1
  have := le_max_left 0 e.1; have := le_max_right 0 e.1
  have := min_le_left 0 e.2; have := min_le_right 0 e.2
  have := le_max_left 0 e.2; have := le_max_right 0 e.2
  omega

lemma card_eq_sum_sum (S : Finset (ι × ι)) :
    S.card = ∑ i, ∑ j, if (i, j) ∈ S then 1 else 0 := by
  rw [← Fintype.sum_prod_type' (fun i j => if (i, j) ∈ S then 1 else 0), sum_boole]
  simp

/-- The ordered pairs of distinct edges of the family that cross properly. -/
def crossPairs : Finset (ι × ι) :=
  univ.filter fun p => p.1 ≠ p.2 ∧ ProperCross (a p.1) (a p.1 + d p.1) (a p.2) (a p.2 + d p.2)

/-- **The excess-crossing budget.** -/
theorem bad_budget (n : ℕ) (hd : ∀ i, d i ∈ knightVecs)
    (ha : ∀ i, 0 ≤ (a i).1 ∧ (a i).1 < n ∧ 0 ≤ (a i).2 ∧ (a i).2 < n)
    (hb : ∀ i, 0 ≤ (a i + d i).1 ∧ (a i + d i).1 < n ∧ 0 ≤ (a i + d i).2 ∧ (a i + d i).2 < n)
    (hdist : ∀ i j, i ≠ j →
      ¬ ((a i = a j ∧ a i + d i = a j + d j) ∨ (a i = a j + d j ∧ a i + d i = a j)))
    (hcard : Fintype.card ι = n * n)
    (U : Finset QTri) (hU : U ⊆ boardTris n) (Bo : Finset (ι × ι)) (hBo : Bo ⊆ crossPairs a d)
    (hBoU : ∀ p ∈ Bo, ∀ t ∈ U, ¬ (t ∈ tri (a p.1) (d p.1) ∧ t ∈ tri (a p.2) (d p.2))) :
    (U.filter fun t => mult a d t ≠ 1).card + 8 * n + Bo.card ≤
      2 * (crossPairs a d).card + 4 := by
  rcases Nat.eq_zero_or_pos n with rfl | hn
  · have hU0 : U = ∅ := by
      refine subset_empty.1 (hU.trans ?_)
      intro t ht
      simp only [boardTris, mem_product, mem_Icc] at ht
      omega
    have := card_le_card hBo
    simp [hU0]
    omega
  obtain ⟨k, rfl⟩ : ∃ k, n = k + 1 := ⟨n - 1, by omega⟩
  set T := boardTris (k + 1)
  set tile : ι → Finset QTri := fun i => tri (a i) (d i)
  set Y := (crossPairs a d).card
  have hT : T.card = k * (k * 4) := by
    simp only [T, boardTris, card_product, Int.card_Icc, card_univ, Fintype.card_fin]
    rw [show ((k + 1 : ℕ) - 2 + 1 - 0 : ℤ) = k by push_cast; ring, Int.toNat_natCast]
  have hsub : ∀ i, tile i ⊆ T := fun i => tri_subset_boardTris _ (hd i) (ha i) (hb i)
  have hcardt : ∀ i, (tile i).card = 4 := fun i => tri_card (hd i)
  -- pair estimate
  have P2 : ∀ i j, (tile i ∩ tile j).card ≤ (if i = j then 4 else 0) +
      2 * (if (i, j) ∈ crossPairs a d then 1 else 0) := by
    intro i j
    by_cases hij : i = j
    · subst hij; simp [hcardt]
    · have := tri_inter_card_le (hd i) (hd j) (hdist i j hij)
      simp only [crossPairs, mem_filter, mem_univ, true_and]
      simp only [hij, ite_false, zero_add, ne_eq, not_false_eq_true, true_and]
      exact this
  -- (1) and (2)
  have S1 : ∑ t ∈ T, mult a d t = 4 * ((k + 1) * (k + 1)) := by
    rw [sum_mult, ← hcard]
    simp [tile, inter_eq_left.2 (hsub _), hcardt, mul_comm]
  have S2 : ∑ t ∈ T, mult a d t ^ 2 ≤ 4 * ((k + 1) * (k + 1)) + 2 * Y := by
    rw [sum_mult_sq]
    have : ∀ i j, (tri (a i) (d i) ∩ tri (a j) (d j) ∩ T).card ≤ (if i = j then 4 else 0) +
        2 * (if (i, j) ∈ crossPairs a d then 1 else 0) := fun i j =>
      (card_le_card inter_subset_left).trans (P2 i j)
    refine (sum_le_sum fun i _ => sum_le_sum fun j _ => this i j).trans (le_of_eq ?_)
    rw [show Y = _ from card_eq_sum_sum (crossPairs a d)]
    simp only [sum_add_distrib, sum_ite_eq, mem_univ, ite_true, ← mul_sum, sum_const,
      card_univ, smul_eq_mul, hcard]
    ring
  -- (3) gaps
  set G := (T.filter fun t => mult a d t = 0).card
  have S3 : 3 * ∑ t ∈ T, mult a d t + 2 * G ≤ 2 * T.card + ∑ t ∈ T, mult a d t ^ 2 := by
    have pt : ∀ m : ℕ, 3 * m + 2 * (if m = 0 then 1 else 0) ≤ 2 * 1 + m ^ 2 := by
      intro m
      rcases Nat.lt_or_ge m 3 with h | h
      · interval_cases m <;> simp
      · simp only [show m ≠ 0 by omega, ite_false]; nlinarith
    have := sum_le_sum fun t (_ : t ∈ T) => pt (mult a d t)
    rw [sum_add_distrib, sum_add_distrib, ← mul_sum, ← mul_sum, ← mul_sum, sum_boole,
      sum_const, smul_eq_mul, mul_one] at this
    simpa [G, mul_comm] using this
  -- (4) multiply covered triangles in U
  set M := (U.filter fun t => 2 ≤ mult a d t).card
  have S4 : M + Bo.card ≤ Y := by
    have pt : ∀ m : ℕ, m + 2 * (if 2 ≤ m then 1 else 0) ≤ m ^ 2 := by
      intro m
      rcases Nat.lt_or_ge m 2 with h | h
      · interval_cases m <;> simp
      · simp only [h, ite_true]; nlinarith
    have h1 := sum_le_sum fun t (_ : t ∈ U) => pt (mult a d t)
    rw [sum_add_distrib, ← mul_sum, sum_boole, sum_mult, sum_mult_sq] at h1
    have h2 : ∀ i j, (tri (a i) (d i) ∩ tri (a j) (d j) ∩ U).card ≤
        (if i = j then (tri (a i) (d i) ∩ U).card else 0) +
        2 * (if (i, j) ∈ crossPairs a d \ Bo then 1 else 0) := by
      intro i j
      by_cases hij : i = j
      · subst hij; simp
      · simp only [hij, ite_false, zero_add]
        by_cases hB : (i, j) ∈ Bo
        · have : tri (a i) (d i) ∩ tri (a j) (d j) ∩ U = ∅ := by
            refine eq_empty_of_forall_notMem fun t ht => ?_
            simp only [mem_inter] at ht
            exact hBoU _ hB t ht.2 ⟨ht.1.1, ht.1.2⟩
          simp [this]
        · have := (card_le_card (inter_subset_left (s₁ := tile i ∩ tile j) (s₂ := U))).trans
            (P2 i j)
          simp only [hij, ite_false, zero_add] at this
          simpa [mem_sdiff, hB] using this
    have h3 := sum_le_sum fun i (_ : i ∈ univ) => sum_le_sum fun j (_ : j ∈ univ) => h2 i j
    have hdiff := card_eq_sum_sum (crossPairs a d \ Bo)
    simp only [sum_add_distrib, sum_ite_eq, mem_univ, ite_true, ← mul_sum] at h3
    simp only [Nat.cast_id] at h1
    have h4 := card_sdiff_add_card_eq_card hBo
    simp only [M, Y]
    omega
  -- (5) bad triangles are gaps or multiply covered
  have S5 : (U.filter fun t => mult a d t ≠ 1).card ≤ G + M := by
    refine (card_le_card ?_).trans (card_union_le (T.filter fun t => mult a d t = 0)
      (U.filter fun t => 2 ≤ mult a d t))
    intro t ht
    simp only [mem_filter] at ht
    simp only [mem_union, mem_filter]
    rcases Nat.lt_or_ge (mult a d t) 2 with h | h
    · left; exact ⟨hU ht.1, by omega⟩
    · right; exact ⟨ht.1, h⟩
  rw [S1, hT] at S3
  nlinarith

/-- The grid edge beside a quarter triangle (each quarter triangle has exactly one unit grid
side). -/
def edgeOf (t : QTri) : GridEdge :=
  match t.2.2 with
  | 0 => ((t.1, t.2.1), false)
  | 1 => ((t.1 + 1, t.2.1), true)
  | 2 => ((t.1, t.2.1 + 1), false)
  | 3 => ((t.1, t.2.1), true)

lemma edgeOf_nearLo (q : GridEdge) : edgeOf (nearLo q) = q := by
  obtain ⟨⟨x, y⟩, v⟩ := q
  cases v <;> simp [edgeOf, nearLo]

lemma edgeOf_nearHi (q : GridEdge) : edgeOf (nearHi q) = q := by
  obtain ⟨⟨x, y⟩, v⟩ := q
  cases v <;> simp [edgeOf, nearHi]

/-- **Charged paths cost crossings (6.5).** `L` pairwise disjoint sets of grid edges, each with
a step `q` where `ω(q) = flux(q) + χ(q)` is not `0` mod 3, and with all their beside-triangles
in `U`, satisfy `L + 8n + #Bo ≤ 2Y + 4`. -/
theorem charged_paths_budget (n : ℕ) (hd : ∀ i, d i ∈ knightVecs)
    (ha : ∀ i, 0 ≤ (a i).1 ∧ (a i).1 < n ∧ 0 ≤ (a i).2 ∧ (a i).2 < n)
    (hb : ∀ i, 0 ≤ (a i + d i).1 ∧ (a i + d i).1 < n ∧ 0 ≤ (a i + d i).2 ∧ (a i + d i).2 < n)
    (hdist : ∀ i j, i ≠ j →
      ¬ ((a i = a j ∧ a i + d i = a j + d j) ∨ (a i = a j + d j ∧ a i + d i = a j)))
    (hcard : Fintype.card ι = n * n)
    (U : Finset QTri) (hU : U ⊆ boardTris n) (Bo : Finset (ι × ι)) (hBo : Bo ⊆ crossPairs a d)
    (hBoU : ∀ p ∈ Bo, ∀ t ∈ U, ¬ (t ∈ tri (a p.1) (d p.1) ∧ t ∈ tri (a p.2) (d p.2)))
    (L : ℕ) (path : Fin L → Finset GridEdge)
    (hdisj : ∀ k l, k ≠ l → Disjoint (path k) (path l))
    (hpathU : ∀ k, ∀ q ∈ path k, nearLo q ∈ U ∧ nearHi q ∈ U)
    (hcharged : ∀ k, ∃ q ∈ path k, ¬ (3 : ℤ) ∣ flux a d q + chi q.1) :
    L + 8 * n + Bo.card ≤ 2 * (crossPairs a d).card + 4 := by
  have hbad : ∀ k, ∃ t, t ∈ U ∧ mult a d t ≠ 1 ∧ edgeOf t ∈ path k := by
    intro k
    obtain ⟨q, hq, hnd⟩ := hcharged k
    by_cases hlo : mult a d (nearLo q) = 1
    · by_cases hhi : mult a d (nearHi q) = 1
      · exact absurd (three_dvd_flux_add_chi a d hd q hlo hhi) hnd
      · exact ⟨_, (hpathU k q hq).2, hhi, by rw [edgeOf_nearHi]; exact hq⟩
    · exact ⟨_, (hpathU k q hq).1, hlo, by rw [edgeOf_nearLo]; exact hq⟩
  choose t ht using hbad
  have hL : L ≤ (U.filter fun t => mult a d t ≠ 1).card := by
    have := card_le_card_of_injOn t (s := (univ : Finset (Fin L)))
      (t := U.filter fun t => mult a d t ≠ 1)
      (by intro k _; simp only [coe_filter, Set.mem_ofPred_eq]; exact ⟨(ht k).1, (ht k).2.1⟩)
      (by
        intro k _ l _ hkl
        by_contra hne
        exact disjoint_left.1 (hdisj k l hne) (ht k).2.2 (hkl ▸ (ht l).2.2))
    simpa using this
  have := bad_budget a d n hd ha hb hdist hcard U hU Bo hBo hBoU
  omega

/-- **The counting chain of section 7.4 / 7.6** (pure arithmetic). With `E = X - (4n - 2)`,
the inputs `d ≤ 5E + 5659` (strip stability), `2n ≤ L + 60 + 4d` (charged corner paths),
`4n ≤ |B| + 48 + d` (boundary crossings) and `L + 8n + 2|B| ≤ 4X + 4` (tile budget) give
`X ≥ (4 + 1/17) n - 17087/17`. -/
theorem counting_chain (n X E d L B : ℤ) (hE : X = 4 * n - 2 + E) (hd : d ≤ 5 * E + 5659)
    (hL1 : 2 * n ≤ L + 60 + 4 * d) (hB : 4 * n ≤ B + 48 + d)
    (hL2 : L + 8 * n + 2 * B ≤ 4 * X + 4) : 69 * n ≤ 17 * X + 17087 := by
  linarith

end KT
