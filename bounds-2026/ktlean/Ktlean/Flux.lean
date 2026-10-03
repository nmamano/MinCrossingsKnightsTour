import Ktlean.CrossCore

/-!
# The local flux identity (KT Turns Theory, FINDINGS.md section 6.2)

A unit grid edge `q` is given by its first endpoint `q.1` and a flag `q.2`: `true` for the vertical
edge from `q.1` to `q.1 + (0, 1)`, `false` for the horizontal edge from `q.1` to `q.1 + (1, 0)`.
Its dual segment joins the centres of the two unit squares beside it; its normal points from
the first endpoint `a` of `q` to the second endpoint `b`.

The flux of a knight edge `e` through the dual segment of `q` is `0` if `e` does not cross it,
and otherwise `±1`: `+1` if `e`, directed from its black end to its white end, crosses in the
direction of the normal. Here `χ(x, y) = 1` for black cells (`x + y` even), `-1` for white cells.

Identity (6.1) for one edge: `flux = χ(a) * ([t₋ ∈ tile e] + [t₊ ∈ tile e] - 3 [short e = q])`,
where `t₋, t₊` are the two quarter triangles beside `q`, and `short e` is the unit grid edge that
is the short diagonal of the tile of `e`.
-/

open Finset

namespace KT

/-- A unit grid edge: `(a, true)` is the vertical edge `a → a + (0,1)`, `(a, false)` is the
horizontal edge `a → a + (1,0)`. -/
abbrev GridEdge := Pt × Bool

/-- The colour of a lattice point: `1` (black) if `x + y` is even, `-1` (white) if not. -/
def chi (p : Pt) : ℤ := if (p.1 + p.2) % 2 = 0 then 1 else -1

lemma chi_add (p r : Pt) : chi (p + r) = chi p * chi r := by
  simp only [chi, Prod.fst_add, Prod.snd_add]
  split_ifs <;> omega

/-- The two endpoints of the dual segment of `q`, in doubled coordinates. -/
def dualEnds (q : GridEdge) : Pt × Pt :=
  if q.2 then ((2 * q.1.1 - 1, 2 * q.1.2 + 1), (2 * q.1.1 + 1, 2 * q.1.2 + 1))
  else ((2 * q.1.1 + 1, 2 * q.1.2 - 1), (2 * q.1.1 + 1, 2 * q.1.2 + 1))

/-- The knight edge from `p` to `p + d` crosses the dual segment of `q`. -/
def CrossesDual (p d : Pt) (q : GridEdge) : Prop :=
  ProperCross (2 * p.1, 2 * p.2) (2 * (p.1 + d.1), 2 * (p.2 + d.2)) (dualEnds q).1 (dualEnds q).2

instance (p d : Pt) (q : GridEdge) : Decidable (CrossesDual p d q) := by
  unfold CrossesDual; infer_instance

/-- The flux of the knight edge from `p` to `p + d` through the dual segment of `q`. -/
def flux1 (p d : Pt) (q : GridEdge) : ℤ :=
  if CrossesDual p d q then chi p * Int.sign (if q.2 then d.2 else d.1) else 0

/-- The quarter triangle beside `q` on the side of smaller coordinates. -/
def nearLo (q : GridEdge) : QTri := if q.2 then (q.1.1 - 1, q.1.2, 1) else (q.1.1, q.1.2 - 1, 2)

/-- The quarter triangle beside `q` on the side of larger coordinates. -/
def nearHi (q : GridEdge) : QTri := if q.2 then (q.1.1, q.1.2, 3) else (q.1.1, q.1.2, 0)

/-- The short diagonal of the tile of the knight edge from `(0,0)` to `d`. -/
def short0 : Pt → GridEdge
  | (1, 2) => ((0, 1), false)
  | (1, -2) => ((0, -1), false)
  | (-1, 2) => ((-1, 1), false)
  | (-1, -2) => ((-1, -1), false)
  | (2, 1) => ((1, 0), true)
  | (2, -1) => ((1, -1), true)
  | (-2, 1) => ((-1, 0), true)
  | (-2, -1) => ((-1, -1), true)
  | _ => ((0, 0), false)

/-- The short diagonal of the tile of the knight edge from `p` to `p + d`. -/
def short (p d : Pt) : GridEdge := (p + (short0 d).1, (short0 d).2)

/-- The single-edge flux identity, for `q` at the origin and the edge start in `[-4, 4]²`. -/
lemma flux1_rel : ∀ x ∈ Icc (-4 : ℤ) 4, ∀ y ∈ Icc (-4 : ℤ) 4, ∀ d ∈ knightVecs, ∀ v : Bool,
    flux1 (x, y) d ((0, 0), v) =
      ((if nearLo ((0, 0), v) ∈ tri (x, y) d then 1 else 0) +
        (if nearHi ((0, 0), v) ∈ tri (x, y) d then 1 else 0) -
        3 * (if short (x, y) d = ((0, 0), v) then 1 else 0)) := by
  decide +kernel

/-- A lattice point as a point of the real plane. -/
def toR (p : Pt) : ℝ × ℝ := ((p.1 : ℝ), (p.2 : ℝ))

lemma detR_toR (a b c : Pt) : detR (toR a) (toR b) (toR c) = (det a b c : ℝ) := by
  simp only [detR, det, toR]; push_cast; ring

lemma mem_openSegment_bounds {A B z : ℝ × ℝ} (h : z ∈ openSegment ℝ A B) :
    min A.1 B.1 ≤ z.1 ∧ z.1 ≤ max A.1 B.1 ∧ min A.2 B.2 ≤ z.2 ∧ z.2 ≤ max A.2 B.2 := by
  obtain ⟨s, t, hs, ht, hst, rfl⟩ := h
  simp only [Prod.fst_add, Prod.snd_add, Prod.smul_fst, Prod.smul_snd, smul_eq_mul]
  have key : ∀ x y m M : ℝ, m ≤ x → m ≤ y → x ≤ M → y ≤ M →
      m ≤ s * x + t * y ∧ s * x + t * y ≤ M := by
    intro x y m M h1 h2 h3 h4
    have e1 : s * x + t * y - m = s * (x - m) + t * (y - m) := by linear_combination m * hst
    have e2 : M - (s * x + t * y) = s * (M - x) + t * (M - y) := by
      linear_combination (-M) * hst
    have := mul_nonneg hs.le (sub_nonneg.2 h1); have := mul_nonneg ht.le (sub_nonneg.2 h2)
    have := mul_nonneg hs.le (sub_nonneg.2 h3); have := mul_nonneg ht.le (sub_nonneg.2 h4)
    constructor <;> linarith
  have k1 := key A.1 B.1 _ _ (min_le_left _ _) (min_le_right _ _) (le_max_left _ _)
    (le_max_right _ _)
  have k2 := key A.2 B.2 _ _ (min_le_left _ _) (min_le_right _ _) (le_max_left _ _)
    (le_max_right _ _)
  exact ⟨k1.1, k1.2, k2.1, k2.2⟩

/-- Two properly crossing segments have overlapping coordinate ranges. -/
lemma ProperCross.ranges {a b c d : Pt} (h : ProperCross a b c d) :
    min a.1 b.1 ≤ max c.1 d.1 ∧ min c.1 d.1 ≤ max a.1 b.1 ∧
      min a.2 b.2 ≤ max c.2 d.2 ∧ min c.2 d.2 ≤ max a.2 b.2 := by
  obtain ⟨h1, h2⟩ := h
  obtain ⟨z, hz1, hz2⟩ := openSegment_inter_nonempty (A := toR a) (B := toR b) (C := toR c)
    (D := toR d) (by rw [detR_toR, detR_toR]; exact_mod_cast h1)
    (by rw [detR_toR, detR_toR]; exact_mod_cast h2)
  have b1 := mem_openSegment_bounds hz1
  have b2 := mem_openSegment_bounds hz2
  simp only [toR] at b1 b2
  have e1 : ((min a.1 b.1 : ℤ) : ℝ) = min (a.1 : ℝ) b.1 := by push_cast; rfl
  have e2 : ((max c.1 d.1 : ℤ) : ℝ) = max (c.1 : ℝ) d.1 := by push_cast; rfl
  have e3 : ((min c.1 d.1 : ℤ) : ℝ) = min (c.1 : ℝ) d.1 := by push_cast; rfl
  have e4 : ((max a.1 b.1 : ℤ) : ℝ) = max (a.1 : ℝ) b.1 := by push_cast; rfl
  have e5 : ((min a.2 b.2 : ℤ) : ℝ) = min (a.2 : ℝ) b.2 := by push_cast; rfl
  have e6 : ((max c.2 d.2 : ℤ) : ℝ) = max (c.2 : ℝ) d.2 := by push_cast; rfl
  have e7 : ((min c.2 d.2 : ℤ) : ℝ) = min (c.2 : ℝ) d.2 := by push_cast; rfl
  have e8 : ((max a.2 b.2 : ℤ) : ℝ) = max (a.2 : ℝ) b.2 := by push_cast; rfl
  refine ⟨?_, ?_, ?_, ?_⟩
  · have : ((min a.1 b.1 : ℤ) : ℝ) ≤ ((max c.1 d.1 : ℤ) : ℝ) := by
      rw [e1, e2]; linarith [b1.1, b2.2.1]
    exact_mod_cast this
  · have : ((min c.1 d.1 : ℤ) : ℝ) ≤ ((max a.1 b.1 : ℤ) : ℝ) := by
      rw [e3, e4]; linarith [b2.1, b1.2.1]
    exact_mod_cast this
  · have : ((min a.2 b.2 : ℤ) : ℝ) ≤ ((max c.2 d.2 : ℤ) : ℝ) := by
      rw [e5, e6]; linarith [b1.2.2.1, b2.2.2.2]
    exact_mod_cast this
  · have : ((min c.2 d.2 : ℤ) : ℝ) ≤ ((max a.2 b.2 : ℤ) : ℝ) := by
      rw [e7, e8]; linarith [b2.2.2.1, b1.2.2.2]
    exact_mod_cast this

lemma mem_tri_iff (t : QTri) (p d : Pt) :
    t ∈ tri p d ↔ (t.1 - p.1, t.2.1 - p.2, t.2.2) ∈ tri0 d := by
  simp only [tri, mem_image]
  constructor
  · rintro ⟨s, hs, rfl⟩
    simpa [shift] using hs
  · intro h
    exact ⟨_, h, by simp [shift]⟩

lemma crossesDual_sub (p d a : Pt) (v : Bool) :
    CrossesDual p d (a, v) ↔ CrossesDual (p - a) d ((0, 0), v) := by
  unfold CrossesDual
  rw [← properCross_sub _ _ _ _ (2 * a.1, 2 * a.2)]
  cases v <;> simp only [dualEnds, Prod.fst_sub, Prod.snd_sub, Prod.mk_sub_mk, ite_true,
    ite_false, Bool.false_eq_true] <;> ring_nf

lemma CrossesDual.bounds {p d : Pt} {v : Bool} (hd : d ∈ knightVecs)
    (h : CrossesDual p d ((0, 0), v)) : -2 ≤ p.1 ∧ p.1 ≤ 2 ∧ -2 ≤ p.2 ∧ p.2 ≤ 2 := by
  have hr := ProperCross.ranges h
  simp only [knightVecs, mem_insert, mem_singleton] at hd
  cases v <;>
  · simp only [dualEnds, ite_true, ite_false, Bool.false_eq_true] at hr
    rcases hd with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl <;>
    · simp only [min_def, max_def] at hr
      split_ifs at hr <;> omega

lemma mem_tri0_bounds {t : QTri} {d : Pt} (hd : d ∈ knightVecs) (h : t ∈ tri0 d) :
    -2 ≤ t.1 ∧ t.1 ≤ 1 ∧ -2 ≤ t.2.1 ∧ t.2.1 ≤ 1 := by
  have := tri0_bounds d hd t h
  simp only [knightVecs, mem_insert, mem_singleton] at hd
  rcases hd with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl <;> simp at this <;> omega

lemma short0_bounds {d : Pt} (hd : d ∈ knightVecs) :
    -1 ≤ (short0 d).1.1 ∧ (short0 d).1.1 ≤ 1 ∧ -1 ≤ (short0 d).1.2 ∧ (short0 d).1.2 ≤ 1 := by
  simp only [knightVecs, mem_insert, mem_singleton] at hd
  rcases hd with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl <;> decide

/-- **The single-edge flux identity (6.1).** -/
theorem flux1_eq {d : Pt} (hd : d ∈ knightVecs) (p : Pt) (q : GridEdge) :
    flux1 p d q = chi q.1 * ((if nearLo q ∈ tri p d then 1 else 0) +
      (if nearHi q ∈ tri p d then 1 else 0) - 3 * (if short p d = q then 1 else 0)) := by
  obtain ⟨a, v⟩ := q
  set r := p - a with hr
  have hp : p = a + r := by rw [hr]; abel
  have T1 : flux1 p d (a, v) = chi a * flux1 r d ((0, 0), v) := by
    unfold flux1
    have hc : chi p = chi a * chi r := by rw [hp, chi_add]
    rw [if_congr (crossesDual_sub p d a v) rfl rfl, ← hr, hc]
    split_ifs <;> ring
  have T2 : (nearLo (a, v) ∈ tri p d ↔ nearLo ((0, 0), v) ∈ tri r d) ∧
      (nearHi (a, v) ∈ tri p d ↔ nearHi ((0, 0), v) ∈ tri r d) := by
    rw [mem_tri_iff, mem_tri_iff, mem_tri_iff, mem_tri_iff, hp]
    cases v <;> simp only [nearLo, nearHi, ite_true, ite_false, Bool.false_eq_true,
      Prod.fst_add, Prod.snd_add] <;> constructor <;> ring_nf
  have T3 : short p d = (a, v) ↔ short r d = ((0, 0), v) := by
    simp only [short, Prod.ext_iff, hp, Prod.fst_add, Prod.snd_add]
    constructor <;> rintro ⟨⟨h1, h2⟩, h3⟩ <;> exact ⟨⟨by omega, by omega⟩, h3⟩
  rw [T1, if_congr T2.1 rfl rfl, if_congr T2.2 rfl rfl, if_congr T3 rfl rfl]
  congr 1
  by_cases hnear : r.1 ∈ Icc (-4 : ℤ) 4 ∧ r.2 ∈ Icc (-4 : ℤ) 4
  · simpa using flux1_rel r.1 hnear.1 r.2 hnear.2 d hd v
  · simp only [mem_Icc] at hnear
    have h1 : ¬ CrossesDual r d ((0, 0), v) := fun h => by
      have := h.bounds hd; omega
    have h2 : ∀ t : QTri, -1 ≤ t.1 → t.1 ≤ 0 → -1 ≤ t.2.1 → t.2.1 ≤ 0 → t ∉ tri r d := by
      intro t a1 a2 a3 a4 ht
      rw [mem_tri_iff] at ht
      have := mem_tri0_bounds hd ht
      simp only at this
      omega
    have h3 : ¬ short r d = ((0, 0), v) := by
      intro h
      have := short0_bounds hd
      simp only [short, Prod.ext_iff, Prod.fst_add, Prod.snd_add] at h
      omega
    have h4 : nearLo ((0, 0), v) ∉ tri r d := by
      cases v <;> exact h2 _ (by simp [nearLo]) (by simp [nearLo]) (by simp [nearLo])
        (by simp [nearLo])
    have h5 : nearHi ((0, 0), v) ∉ tri r d := by
      cases v <;> exact h2 _ (by simp [nearHi]) (by simp [nearHi]) (by simp [nearHi])
        (by simp [nearHi])
    simp [flux1, h1, h3, h4, h5]

section Family

variable {ι : Type*} [Fintype ι] (a d : ι → Pt)

/-- The flux of a family of knight edges (edge `i` from `a i` to `a i + d i`) through the dual
segment of `q`. -/
def flux (q : GridEdge) : ℤ := ∑ i, flux1 (a i) (d i) q

/-- The multiplicity of a quarter triangle: the number of tiles that contain it. -/
def mult (t : QTri) : ℕ := (univ.filter fun i => t ∈ tri (a i) (d i)).card

/-- The number of tiles whose short diagonal is `q`. -/
def shortCount (q : GridEdge) : ℕ := (univ.filter fun i => short (a i) (d i) = q).card

/-- **Flux identity (6.1)** for a family of knight edges. -/
theorem flux_eq (hd : ∀ i, d i ∈ knightVecs) (q : GridEdge) :
    flux a d q = chi q.1 * ((mult a d (nearLo q) : ℤ) + mult a d (nearHi q) -
      3 * shortCount a d q) := by
  simp only [flux, mult, shortCount, card_filter]
  rw [sum_congr rfl fun i _ => flux1_eq (hd i) (a i) q, ← mul_sum]
  push_cast
  rw [sum_sub_distrib, sum_add_distrib, mul_sum]

/-- The mod-3 form `ω = φ + χ(a)` (6.2): it is `0` mod 3 when both quarter triangles beside
`q` have multiplicity one. -/
theorem three_dvd_flux_add_chi (hd : ∀ i, d i ∈ knightVecs) (q : GridEdge)
    (hlo : mult a d (nearLo q) = 1) (hhi : mult a d (nearHi q) = 1) :
    (3 : ℤ) ∣ flux a d q + chi q.1 := by
  rw [flux_eq a d hd, hlo, hhi]
  exact ⟨chi q.1 * (1 - shortCount a d q), by push_cast; ring⟩

end Family

end KT
