import Ktlean.Frames

/-!
# Helper facts for the combined theorem

Explicit formulas for the frames `k < 4`, invariance of proper crossings under the quarter turn,
and the unit squares of the corner paths `γ_R`.
-/

open Finset

namespace KT

lemma rotPt_iter_mod (n : ℤ) (k : ℕ) (p : Pt) : (rotPt n)^[k % 4] p = (rotPt n)^[k] p := by
  conv_rhs => rw [← Nat.mod_add_div k 4]
  rw [Function.iterate_add_apply, Function.iterate_mul]
  have : (rotPt n)^[4] = id := funext (rotPt_iter_four n)
  rw [this, Function.iterate_id, id]

lemma rotL_iter_mod (k : ℕ) (d : Pt) : rotL^[k % 4] d = rotL^[k] d := by
  conv_rhs => rw [← Nat.mod_add_div k 4]
  rw [Function.iterate_add_apply, Function.iterate_mul]
  have : rotL^[4] = id := funext rotL_iter_four
  rw [this, Function.iterate_id, id]

lemma rotPt_iter_cases (n : ℤ) {k : ℕ} (hk : k < 4) (p : Pt) :
    (k = 0 ∧ (rotPt n)^[k] p = p) ∨ (k = 1 ∧ (rotPt n)^[k] p = (n - 1 - p.2, p.1)) ∨
    (k = 2 ∧ (rotPt n)^[k] p = (n - 1 - p.1, n - 1 - p.2)) ∨
    (k = 3 ∧ (rotPt n)^[k] p = (p.2, n - 1 - p.1)) := by
  interval_cases k <;> simp [rotPt]

lemma rotSq_iter_cases (n : ℤ) {k : ℕ} (hk : k < 4) (s : Pt) :
    (k = 0 ∧ (rotSq n)^[k] s = s) ∨ (k = 1 ∧ (rotSq n)^[k] s = (n - 2 - s.2, s.1)) ∨
    (k = 2 ∧ (rotSq n)^[k] s = (n - 2 - s.1, n - 2 - s.2)) ∨
    (k = 3 ∧ (rotSq n)^[k] s = (s.2, n - 2 - s.1)) := by
  interval_cases k <;> simp [rotSq]

lemma det_rot (n : ℤ) (a b c : Pt) : det (rotPt n a) (rotPt n b) (rotPt n c) = det a b c := by
  simp only [det, rotPt]; ring

lemma properCross_rot (n : ℤ) (a b c d : Pt) :
    ProperCross (rotPt n a) (rotPt n b) (rotPt n c) (rotPt n d) ↔ ProperCross a b c d := by
  simp only [ProperCross, det_rot]

lemma properCross_rot_iter (n : ℤ) (k : ℕ) (a b c d : Pt) :
    ProperCross ((rotPt n)^[k] a) ((rotPt n)^[k] b) ((rotPt n)^[k] c) ((rotPt n)^[k] d) ↔
      ProperCross a b c d := by
  induction k with
  | zero => rfl
  | succ k ih => simp only [Function.iterate_succ_apply', properCross_rot, ih]

lemma crossPairs_iter {ι : Type*} [Fintype ι] [DecidableEq ι] (a d : ι → Pt) (n : ℤ) (k : ℕ) :
    crossPairs (fun i => (rotPt n)^[k] (a i)) (fun i => rotL^[k] (d i)) = crossPairs a d := by
  unfold crossPairs
  congr 1
  funext p
  simp only [← rotPt_iter_add, properCross_rot_iter]

/-! ### The unit squares of `γ_R` -/

/-- The unit squares whose centres are the vertices of `γ_R`. -/
def gammaSq (R : ℤ) : Finset Pt :=
  ((Icc 1 R).image fun x => (x, R)) ∪ ((Icc 1 R).image fun y => (R, y))

lemma mem_gammaSq {R : ℤ} {s : Pt} :
    s ∈ gammaSq R ↔ (1 ≤ s.1 ∧ s.1 ≤ R ∧ s.2 = R) ∨ (s.1 = R ∧ 1 ≤ s.2 ∧ s.2 ≤ R) := by
  obtain ⟨x, y⟩ := s
  simp only [gammaSq, mem_union, mem_image, mem_Icc, Prod.mk.injEq]
  constructor
  · rintro (⟨x', h, rfl, rfl⟩ | ⟨y', h, rfl, rfl⟩)
    · exact Or.inl ⟨h.1, h.2, rfl⟩
    · exact Or.inr ⟨rfl, h.1, h.2⟩
  · rintro (⟨h1, h2, rfl⟩ | ⟨rfl, h1, h2⟩)
    · exact Or.inl ⟨x, ⟨h1, h2⟩, rfl, rfl⟩
    · exact Or.inr ⟨y, ⟨h1, h2⟩, rfl, rfl⟩

lemma besideSq_subset_gammaSq {R : ℤ} {q : GridEdge} (hq : q ∈ gammaSteps R) :
    besideSq q ⊆ gammaSq R := by
  intro s hs
  rw [mem_gammaSq]
  simp only [gammaSteps, mem_union, mem_image, mem_Icc] at hq
  simp only [besideSq, mem_insert, mem_singleton] at hs
  rcases hq with ⟨x, hx, rfl⟩ | ⟨y, hy, rfl⟩ <;>
    rcases hs with rfl | rfl <;> simp [nearLo, nearHi, sqOf] <;> omega

/-- The unit squares of the board `[0, n-1]²`. -/
def boardSq (n : ℤ) : Finset Pt := Icc 0 (n - 2) ×ˢ Icc 0 (n - 2)

lemma rotSq_mem_boardSq {n : ℤ} {s : Pt} : rotSq n s ∈ boardSq n ↔ s ∈ boardSq n := by
  simp only [boardSq, rotSq, mem_product, mem_Icc]; omega

lemma rotSq_iter_mem_boardSq {n : ℤ} (k : ℕ) {s : Pt} :
    (rotSq n)^[k] s ∈ boardSq n ↔ s ∈ boardSq n := by
  induction k with
  | zero => rfl
  | succ k ih => rw [Function.iterate_succ_apply', rotSq_mem_boardSq, ih]

end KT
