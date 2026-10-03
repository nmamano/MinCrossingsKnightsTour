import Ktlean.Boundary

/-!
# Tile overlaps of the edges at column 0 (FINDINGS.md 9.6, 10.2)

Two distinct knight edges with an endpoint in column 0 (and the other endpoints in `x ≥ 0`) have
tile overlaps only in squares with left coordinate `0`, except for the pair
`(0, j)--(2, j+1)`, `(0, j+1)--(2, j)`, whose overlap can reach the square `[1, 2] × [j, j+1]`.
A critical row `j` (the hypothesis of `corner_charge_row`) excludes this pair, since `P` and `P'`
contain only one edge of it each.
-/

open Finset

namespace KT

lemma tri0_neg : ∀ d ∈ knightVecs, tri0 (-d) = (tri0 d).image (shift (-d)) := by decide

lemma tri_symm {p d : Pt} (hd : d ∈ knightVecs) : tri (p + d) (-d) = tri p d := by
  ext t
  rw [mem_tri_iff, mem_tri_iff, tri0_neg d hd, mem_image]
  constructor
  · rintro ⟨⟨x, y, q⟩, hs, h⟩
    simp only [shift, Prod.mk.injEq, Prod.fst_add, Prod.snd_add, Prod.fst_neg,
      Prod.snd_neg] at h
    have e : ((t.1 - p.1, t.2.1 - p.2, t.2.2) : QTri) = (x, y, q) := by
      simp only [Prod.mk.injEq]; exact ⟨by omega, by omega, h.2.2.symm⟩
    rwa [e]
  · intro h
    refine ⟨_, h, ?_⟩
    simp only [shift, Prod.mk.injEq, Prod.fst_add, Prod.snd_add, Prod.fst_neg, Prod.snd_neg]
    exact ⟨by ring, by ring, trivial⟩

lemma canon_symm {k : Pt → ℤ} {d : Pt} (hk : k (-d) = -k d) (hk0 : k d ≠ 0) (p : Pt) :
    canon k (p + d) (-d) = canon k p d := by
  unfold canon
  rw [hk]
  split_ifs with h1 h2 h2
  · omega
  · simp
  · simp
  · omega

lemma col0_overlap_rel : ∀ w ∈ C0, ∀ r ∈ Icc (-3 : ℤ) 3, ∀ w' ∈ C0, (r ≠ 0 ∨ w' ≠ w) →
    ∀ t ∈ tri 0 w ∩ tri (0, r) w', t.1 = 0 ∨ (t.1 = 1 ∧
      ((w = (2, 1) ∧ r = 1 ∧ w' = (2, -1) ∧ t.2.1 = 0) ∨
        (w = (2, -1) ∧ r = -1 ∧ w' = (2, 1) ∧ t.2.1 = -1))) := by
  decide +kernel

lemma excl_cert : ∀ s ∈ ({1, -1} : Finset ℤ),
    ¬ ((((0, 0), (2, 1)) : Pt × Pt) ∈ PL s ∧ (((2, 0), (-2, 1)) : Pt × Pt) ∈ PL s) := by
  decide +kernel

section Family

variable {ι : Type*} [Fintype ι] {a d : ι → Pt}

lemma tri_eq_oth (hd : ∀ i, d i ∈ knightVecs) {v : Pt} {i : ι} (hi : i ∈ atCell a d v) :
    tri (a i) (d i) = tri v (oth a d v i - v) := by
  rw [mem_atCell] at hi
  unfold oth
  split_ifs with h
  · rw [h, add_sub_cancel_left]
  · have h2 := hi.resolve_left h
    rw [← tri_symm (hd i), h2]
    congr 1
    rw [← h2]; abel

lemma canon_eq_oth (hd : ∀ i, d i ∈ knightVecs) {v : Pt} {i : ι} (hi : i ∈ atCell a d v) :
    canon Prod.snd (a i - v) (d i) = canon Prod.snd 0 (oth a d v i - v) := by
  rw [mem_atCell] at hi
  unfold oth
  split_ifs with h
  · rw [h, sub_self, add_sub_cancel_left]
  · have h2 := hi.resolve_left h
    have hk : (d i).2 ≠ 0 := by
      have := hd i; simp only [knightVecs, mem_insert, mem_singleton] at this
      rcases this with h | h | h | h | h | h | h | h <;> rw [h] <;> decide
    rw [← canon_symm (k := Prod.snd) (d := d i) (by simp) hk (a i - v)]
    congr 1
    · rw [← h2]; abel
    · rw [← h2]; abel

/-- Overlaps of two edges at column 0 lie in `x ≤ 1`; at `x = 1` only the exceptional pair. -/
lemma col0_overlap (hd : ∀ i, d i ∈ knightVecs) (hdist : DistinctEdges a d)
    (hpos : ∀ i, 0 ≤ (a i).1 ∧ 0 ≤ (a i + d i).1) {i j : ι} {y y' : ℤ}
    (hi : i ∈ atCell a d (0, y)) (hj : j ∈ atCell a d (0, y')) (hij : i ≠ j) {t : QTri}
    (ht : t ∈ tri (a i) (d i)) (ht' : t ∈ tri (a j) (d j)) :
    t.1 = 0 ∨ (t.1 = 1 ∧ ∃ j0 : ℤ, t.2.1 = j0 ∧
      ((oth a d (0, y) i = (2, j0 + 1) ∧ y = j0 ∧ oth a d (0, y') j = (2, j0) ∧ y' = j0 + 1) ∨
       (oth a d (0, y) i = (2, j0) ∧ y = j0 + 1 ∧ oth a d (0, y') j = (2, j0 + 1) ∧
        y' = j0))) := by
  have hC : ∀ {k : ι} {z : ℤ}, k ∈ atCell a d (0, z) → oth a d (0, z) k - (0, z) ∈ C0 := by
    intro k z hk
    apply knight_mem_C0 _ (oth_sub_mem hd hk)
    have := hpos k
    unfold oth
    split_ifs <;> simp only [Prod.fst_sub] <;> omega
  rw [tri_eq_oth hd hi, mem_tri_iff] at ht
  rw [tri_eq_oth hd hj, mem_tri_iff] at ht'
  set w := oth a d (0, y) i - (0, y) with hw
  set w' := oth a d (0, y') j - (0, y') with hw'
  have hb := mem_tri0_bounds (oth_sub_mem hd hi) ht
  have hb' := mem_tri0_bounds (oth_sub_mem hd hj) ht'
  simp only at hb hb'
  have hr : y' - y ∈ Icc (-3 : ℤ) 3 := by rw [mem_Icc]; omega
  have hne : y' - y ≠ 0 ∨ w' ≠ w := by
    by_contra hc
    push Not at hc
    have hyy : y' = y := by omega
    subst hyy
    exact hij (oth_injOn hdist _ hi hj (sub_left_injective hc.2).symm)
  have key := col0_overlap_rel w (hC hi) (y' - y) hr w' (hC hj) hne (t.1, t.2.1 - y, t.2.2)
    (by
      rw [mem_inter, mem_tri_iff, mem_tri_iff]
      constructor
      · convert ht using 2; simp
      · convert ht' using 2; simp)
  simp only at key
  rcases key with h | ⟨h1, h⟩
  · exact Or.inl h
  · right
    refine ⟨h1, t.2.1, rfl, ?_⟩
    rcases h with ⟨e1, e2, e3, e4⟩ | ⟨e1, e2, e3, e4⟩
    · left
      refine ⟨?_, by omega, ?_, by omega⟩
      · have : oth a d (0, y) i = (2, 1) + (0, y) := by rw [← e1, hw, sub_add_cancel]
        rw [this]; ext <;> simp; omega
      · have : oth a d (0, y') j = (2, -1) + (0, y') := by rw [← e3, hw', sub_add_cancel]
        rw [this]; ext <;> simp; omega
    · right
      refine ⟨?_, by omega, ?_, by omega⟩
      · have : oth a d (0, y) i = (2, -1) + (0, y) := by rw [← e1, hw, sub_add_cancel]
        rw [this]; ext <;> simp; omega
      · have : oth a d (0, y') j = (2, 1) + (0, y') := by rw [← e3, hw', sub_add_cancel]
        rw [this]; ext <;> simp; omega

/-- The canonical forms of the exceptional pair at row `j0`. -/
lemma canon_exc (hd : ∀ i, d i ∈ knightVecs) {j0 : ℤ}
    {i j : ι} (hi : i ∈ atCell a d (0, j0)) (hj : j ∈ atCell a d (0, j0 + 1))
    (hoi : oth a d (0, j0) i = (2, j0 + 1)) (hoj : oth a d (0, j0 + 1) j = (2, j0)) :
    canon Prod.snd (a i - (0, j0)) (d i) = ((0, 0), (2, 1)) ∧
      canon Prod.snd (a j - (0, j0)) (d j) = ((2, 0), (-2, 1)) := by
  refine ⟨?_, ?_⟩
  · rw [canon_eq_oth hd hi, hoi]
    simp [canon]
    rfl
  · rw [mem_atCell] at hj
    unfold canon
    rcases hj with h | h
    · have hdj : d j = (2, -1) := by
        have := hoj; unfold oth at this; simp only [h, ↓reduceIte] at this
        ext <;> simp [Prod.ext_iff] at this ⊢ <;> omega
      rw [h, hdj]; ext <;> simp
    · have h' : ¬ a j = (0, j0 + 1) := by
        intro h'; rw [h'] at h
        exact d_ne_zero hd j (by simpa using h)
      have haj : a j = (2, j0) := by
        have := hoj; unfold oth at this; simpa only [h', ↓reduceIte] using this
      have hdj : d j = (-2, 1) := by
        rw [haj] at h; ext <;> simp [Prod.ext_iff] at h ⊢ <;> omega
      rw [haj, hdj]; ext <;> simp

/-- A critical row `j0` excludes the exceptional pair. -/
lemma not_both_of_row (hd : ∀ i, d i ∈ knightVecs) (j0 : ℤ) (s : ℤ)
    (hs : s ∈ ({1, -1} : Finset ℤ))
    (hrow : (univ.filter fun i => StradL (canon Prod.snd (a i - (0, j0)) (d i))).image
      (fun i => canon Prod.snd (a i - (0, j0)) (d i)) = PL s)
    {i j : ι} (hi : i ∈ atCell a d (0, j0)) (hj : j ∈ atCell a d (0, j0 + 1))
    (hoi : oth a d (0, j0) i = (2, j0 + 1)) (hoj : oth a d (0, j0 + 1) j = (2, j0)) : False := by
  apply excl_cert s hs
  obtain ⟨hci, hcj⟩ := canon_exc hd hi hj hoi hoj
  have hmem : ∀ k : ι, StradL (canon Prod.snd (a k - (0, j0)) (d k)) →
      canon Prod.snd (a k - (0, j0)) (d k) ∈ PL s := by
    intro k hk
    rw [← hrow]
    exact mem_image.2 ⟨k, by simp [hk], rfl⟩
  refine ⟨?_, ?_⟩
  · rw [← hci]; exact hmem i (by rw [hci]; decide)
  · rw [← hcj]; exact hmem j (by rw [hcj]; decide)

end Family

end KT
