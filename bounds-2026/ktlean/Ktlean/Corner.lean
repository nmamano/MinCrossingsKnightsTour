import Ktlean.Loop

/-!
# The corner charge (KT Turns Theory, FINDINGS.md section 7.3, in a simpler form)

We use the box `B_R = [0, R]²` of lattice points at the bottom-left corner of the board. Its
boundary steps are: the outer steps (left of column 0 and below row 0, which no board edge
crosses), four steps `T4` at the two ends (top steps at `x = 0, 1`, right steps at `y = 0, 1`),
and the interior path `γ_R` (top steps at `x = 2..R`, right steps at `y = 2..R`).
-/

open Finset

namespace KT

lemma mem_bdry (B : Finset Pt) (q : GridEdge) :
    q ∈ bdry B ↔ ¬ (q.1 ∈ B ↔ q.1 + dirOf q.2 ∈ B) := by
  unfold bdry
  rw [mem_filter]
  refine ⟨fun h => h.2, fun h => ⟨?_, h⟩⟩
  obtain ⟨u, v⟩ := q
  by_cases hu : u ∈ B
  · refine mem_image.2 ⟨(u, dirOf v), mem_product.2 ⟨hu, ?_⟩, ?_⟩ <;>
      cases v <;> simp [dirs4, dirOf, stepEdge]
  · have hw : u + dirOf v ∈ B := by tauto
    refine mem_image.2 ⟨(u + dirOf v, -dirOf v), mem_product.2 ⟨hw, ?_⟩, ?_⟩ <;>
      cases v <;> simp [dirs4, dirOf, stepEdge, Prod.ext_iff]

/-- The box `[0, R]²`. -/
def box (R : ℤ) : Finset Pt := Icc 0 R ×ˢ Icc 0 R

/-- The interior path `γ_R`: top steps at `x = 2..R` and right steps at `y = 2..R`. -/
def gammaSteps (R : ℤ) : Finset GridEdge :=
  ((Icc 2 R).image fun x => ((x, R), true)) ∪ ((Icc 2 R).image fun y => ((R, y), false))

/-- The four end steps. -/
def T4 (R : ℤ) : Finset GridEdge :=
  {((0, R), true), ((1, R), true), ((R, 0), false), ((R, 1), false)}

/-- The outer steps, left of column 0 and below row 0. -/
def outerSteps (R : ℤ) : Finset GridEdge :=
  ((Icc 0 R).image fun y => ((-1, y), false)) ∪ ((Icc 0 R).image fun x => ((x, -1), true))

lemma bdry_box {R : ℤ} (hR : 2 ≤ R) :
    bdry (box R) = outerSteps R ∪ T4 R ∪ gammaSteps R := by
  ext ⟨⟨x, y⟩, v⟩
  rw [mem_bdry]
  cases v <;> simp [box, outerSteps, T4, gammaSteps, dirOf, Prod.ext_iff] <;> omega

lemma disjoint_parts {R : ℤ} (hR : 2 ≤ R) :
    Disjoint (outerSteps R ∪ T4 R) (gammaSteps R) ∧ Disjoint (outerSteps R) (T4 R) := by
  constructor <;> rw [disjoint_left] <;> rintro ⟨⟨x, y⟩, v⟩ h1 h2 <;> cases v <;>
    simp [outerSteps, T4, gammaSteps, Prod.ext_iff] at h1 h2 <;> omega

lemma mid_range : ∀ d ∈ knightVecs, (0 ≤ (mid1 d).1 ∨ d.1 ≤ (mid1 d).1) ∧
    (0 ≤ (mid1 d).2 ∨ d.2 ≤ (mid1 d).2) ∧ (0 ≤ (mid2 d).1 ∨ d.1 ≤ (mid2 d).1) ∧
    (0 ≤ (mid2 d).2 ∨ d.2 ≤ (mid2 d).2) := by decide

lemma stepSign_ne_zero' {u w : Pt} {q : GridEdge} (h : stepSign u w q ≠ 0) :
    u = q.1 ∨ w = q.1 := by
  unfold stepSign at h
  split_ifs at h with h1 h2
  · exact Or.inl h1.1
  · exact Or.inr h2.1
  · exact absurd rfl h

/-- No board edge crosses an outer step. -/
lemma flux1_outer {p d : Pt} (hd : d ∈ knightVecs) (hp : 0 ≤ p.1 ∧ 0 ≤ p.2)
    (hq : 0 ≤ (p + d).1 ∧ 0 ≤ (p + d).2) {R : ℤ} {q : GridEdge} (h : q ∈ outerSteps R) :
    flux1 p d q = 0 := by
  have hneg : q.1.1 = -1 ∨ q.1.2 = -1 := by
    obtain ⟨⟨x, y⟩, v⟩ := q
    simp only [outerSteps, mem_union, mem_image, mem_Icc] at h
    rcases h with ⟨y', -, h1⟩ | ⟨x', -, h1⟩ <;> rw [← h1] <;> simp
  have hm := mid_range d hd
  simp only [Prod.fst_add, Prod.snd_add] at hq
  have z : ∀ u w : Pt, 0 ≤ u.1 → 0 ≤ u.2 → 0 ≤ w.1 → 0 ≤ w.2 → stepSign u w q = 0 := by
    intro u w h1 h2 h3 h4
    by_contra hne
    rcases stepSign_ne_zero' hne with rfl | rfl <;> omega
  rw [flux1_eq_path hd, pathSign, z, z, z] <;> (try simp only [Prod.fst_add, Prod.snd_add]) <;>
    omega

lemma flux1_add (p d t : Pt) (a : Pt) (v : Bool) (hd : d ∈ knightVecs) :
    flux1 (p + t) d (a + t, v) = chi t * flux1 p d (a, v) := by
  rw [flux1_eq_path hd, flux1_eq_path hd, pathSign_sub, pathSign_sub p d a,
    show p + t - (a + t) = p - a by abel, chi_add]
  ring

lemma flux1_far {p d : Pt} {a : Pt} {v : Bool} (hd : d ∈ knightVecs)
    (h : flux1 p d (a, v) ≠ 0) : |p.1 - a.1| ≤ 2 ∧ |p.2 - a.2| ≤ 2 := by
  by_cases hc : CrossesDual p d (a, v)
  · rw [crossesDual_sub] at hc
    have := hc.bounds hd
    simp only [Prod.fst_sub, Prod.snd_sub] at this
    constructor <;> rw [abs_le] <;> omega
  · simp [flux1, hc] at h

lemma properCross_swap (a b c d : Pt) : ProperCross b a c d ↔ ProperCross a b c d := by
  unfold ProperCross det
  constructor <;> rintro ⟨h1, h2⟩ <;> constructor <;> nlinarith [h1, h2]

lemma flux1_symm {p d : Pt} (hd : d ∈ knightVecs) (q : GridEdge) :
    flux1 (p + d) (-d) q = flux1 p d q := by
  have hc : chi (p + d) = - chi p := by rw [chi_add, chi_knight hd]; ring
  have hx : CrossesDual (p + d) (-d) q ↔ CrossesDual p d q := by
    unfold CrossesDual
    simp only [Prod.fst_add, Prod.snd_add, Prod.fst_neg, Prod.snd_neg, add_neg_cancel_right]
    exact properCross_swap _ _ _ _
  unfold flux1
  rw [if_congr hx rfl rfl, hc]
  split_ifs <;> simp [Int.sign_neg]

/-! ### The two ends, in local coordinates -/

/-- The strip cells of the four endpoint rows at the top end of the left side, relative to
`(0, R)`: columns `0, 1` and rows `-1..2`. -/
def FL : Finset Pt := ({0, 1} : Finset ℤ) ×ˢ Icc (-1) 2

/-- The pattern `P` (`s = 1`) or `P'` (`s = -1`) at a left strip cell `v` (column 0 or 1). -/
def patL (s : ℤ) (v : Pt) : Finset Pt :=
  if v.1 = 0 then {(2, v.2 + s), (1, v.2 + 2 * s)} else {(3, v.2 + s), (0, v.2 - 2 * s)}

/-- Flux of a knight edge through the two top end steps, in local coordinates. -/
def gL (p d : Pt) : ℤ := flux1 p d ((0, 0), true) + flux1 p d ((1, 0), true)

/-- The weighted end value (each edge counted twice in total). -/
def CL (s : ℤ) : ℤ :=
  ∑ v ∈ FL, ∑ w ∈ patL s v, gL v (w - v) * (1 + if w ∈ FL then 0 else 1)

/-- The bottom side, transposed: rows `0, 1` and columns `-1..2`, relative to `(R, 0)`. -/
def FB : Finset Pt := Icc (-1) 2 ×ˢ ({0, 1} : Finset ℤ)

def patB (s : ℤ) (v : Pt) : Finset Pt :=
  if v.2 = 0 then {(v.1 + s, 2), (v.1 + 2 * s, 1)} else {(v.1 + s, 3), (v.1 - 2 * s, 0)}

def gB (p d : Pt) : ℤ := flux1 p d ((0, 0), false) + flux1 p d ((0, 1), false)

def CB (s : ℤ) : ℤ :=
  ∑ v ∈ FB, ∑ w ∈ patB s v, gB v (w - v) * (1 + if w ∈ FB then 0 else 1)

lemma CL_eq : ∀ s ∈ ({1, -1} : Finset ℤ), CL s = 2 := by decide +kernel
lemma CB_eq : ∀ s ∈ ({1, -1} : Finset ℤ), CB s = 2 := by decide +kernel

lemma gL_support_rel : ∀ x ∈ Icc (-4 : ℤ) 4, ∀ y ∈ Icc (-4 : ℤ) 4, ∀ d ∈ knightVecs,
    0 ≤ x → 0 ≤ x + d.1 → gL (x, y) d ≠ 0 → (x, y) ∈ FL ∨ (x, y) + d ∈ FL := by
  decide +kernel

lemma gB_support_rel : ∀ x ∈ Icc (-4 : ℤ) 4, ∀ y ∈ Icc (-4 : ℤ) 4, ∀ d ∈ knightVecs,
    0 ≤ y → 0 ≤ y + d.2 → gB (x, y) d ≠ 0 → (x, y) ∈ FB ∨ (x, y) + d ∈ FB := by
  decide +kernel

lemma gL_support {p d : Pt} (hd : d ∈ knightVecs) (hx : 0 ≤ p.1) (hx' : 0 ≤ p.1 + d.1)
    (h : gL p d ≠ 0) : p ∈ FL ∨ p + d ∈ FL := by
  have hn : |p.1| ≤ 4 ∧ |p.2| ≤ 4 := by
    by_contra hc
    apply h
    have h1 : flux1 p d ((0, 0), true) = 0 := by
      by_contra h1; have := flux1_far hd h1; dsimp only at this; rw [abs_le, abs_le] at *; omega
    have h2 : flux1 p d ((1, 0), true) = 0 := by
      by_contra h2; have := flux1_far hd h2; dsimp only at this; rw [abs_le, abs_le] at *; omega
    simp [gL, h1, h2]
  rw [abs_le, abs_le] at hn
  have := gL_support_rel p.1 (mem_Icc.2 hn.1) p.2 (mem_Icc.2 hn.2) d hd hx hx'
  simpa using this h

lemma gB_support {p d : Pt} (hd : d ∈ knightVecs) (hy : 0 ≤ p.2) (hy' : 0 ≤ p.2 + d.2)
    (h : gB p d ≠ 0) : p ∈ FB ∨ p + d ∈ FB := by
  have hn : |p.1| ≤ 4 ∧ |p.2| ≤ 4 := by
    by_contra hc
    apply h
    have h1 : flux1 p d ((0, 0), false) = 0 := by
      by_contra h1; have := flux1_far hd h1; dsimp only at this; rw [abs_le, abs_le] at *; omega
    have h2 : flux1 p d ((0, 1), false) = 0 := by
      by_contra h2; have := flux1_far hd h2; dsimp only at this; rw [abs_le, abs_le] at *; omega
    simp [gB, h1, h2]
  rw [abs_le, abs_le] at hn
  have := gB_support_rel p.1 (mem_Icc.2 hn.1) p.2 (mem_Icc.2 hn.2) d hd hy hy'
  simpa using this h

section Family

variable {ι : Type*} [Fintype ι] (a d : ι → Pt)

/-- The edges at `v` go exactly to the two points of `N`. -/
def NbrsAre (v : Pt) (N : Finset Pt) : Prop :=
  N.card = 2 ∧ deg a d v = 2 ∧ (∀ i, a i = v → a i + d i ∈ N) ∧ (∀ i, a i + d i = v → a i ∈ N)

/-- Distinct edges (as unordered pairs). -/
def DistinctEdges : Prop :=
  ∀ i j, i ≠ j → ¬ ((a i = a j ∧ a i + d i = a j + d j) ∨ (a i = a j + d j ∧ a i + d i = a j))

lemma dart_sum (hd : ∀ i, d i ∈ knightVecs) (hdist : DistinctEdges a d) {v : Pt}
    {N : Finset Pt} (hN : NbrsAre a d v N) (f : Pt → ℤ) :
    ∑ i, ((if a i = v then f (a i + d i) else 0) + (if a i + d i = v then f (a i) else 0)) =
      ∑ w ∈ N, f w := by
  obtain ⟨hN2, hdeg, h1, h2⟩ := hN
  have hd0 : ∀ i, d i ≠ 0 := fun i h => by
    have := hd i; rw [h] at this; simp [knightVecs, Prod.ext_iff] at this
  set S1 := univ.filter fun i => a i = v
  set S2 := univ.filter fun i => a i + d i = v
  have inj1 : Set.InjOn (fun i => a i + d i) S1 := by
    intro i hi j hj hij
    simp only [S1, coe_filter, Set.mem_ofPred_eq, mem_univ, true_and] at hi hj
    by_contra hne
    exact hdist i j hne (Or.inl ⟨hi.trans hj.symm, hij⟩)
  have inj2 : Set.InjOn (fun i => a i) S2 := by
    intro i hi j hj hij
    simp only [S2, coe_filter, Set.mem_ofPred_eq, mem_univ, true_and] at hi hj
    by_contra hne
    exact hdist i j hne (Or.inl ⟨hij, hi.trans hj.symm⟩)
  have hdisj : Disjoint (S1.image fun i => a i + d i) (S2.image fun i => a i) := by
    rw [disjoint_left]
    intro w hw1 hw2
    obtain ⟨i, hi, rfl⟩ := mem_image.1 hw1
    obtain ⟨j, hj, hji⟩ := mem_image.1 hw2
    simp only [S1, S2, mem_filter, mem_univ, true_and] at hi hj
    by_cases hij : i = j
    · subst hij
      exact hd0 i (by
        have : a i + d i = a i + 0 := by rw [add_zero]; exact hj.trans hi.symm
        exact add_left_cancel this)
    · exact hdist i j hij (Or.inr ⟨hi.trans hj.symm, hji.symm⟩)
  have hsub : (S1.image fun i => a i + d i) ∪ (S2.image fun i => a i) ⊆ N := by
    intro w hw
    rcases mem_union.1 hw with hw | hw
    · obtain ⟨i, hi, rfl⟩ := mem_image.1 hw
      exact h1 i (mem_filter.1 hi).2
    · obtain ⟨i, hi, rfl⟩ := mem_image.1 hw
      exact h2 i (mem_filter.1 hi).2
  have hcard : ((S1.image fun i => a i + d i) ∪ (S2.image fun i => a i)).card = 2 := by
    rw [card_union_of_disjoint hdisj, card_image_of_injOn inj1, card_image_of_injOn inj2]
    exact hdeg
  have heq := eq_of_subset_of_card_le hsub (by rw [hcard, hN2])
  rw [sum_add_distrib, ← sum_filter, ← sum_filter, ← sum_image inj1, ← sum_image inj2,
    ← sum_union hdisj, heq]

lemma gL_symm {p d : Pt} (hd : d ∈ knightVecs) : gL (p + d) (-d) = gL p d := by
  simp only [gL, flux1_symm hd]

lemma gB_symm {p d : Pt} (hd : d ∈ knightVecs) : gB (p + d) (-d) = gB p d := by
  simp only [gB, flux1_symm hd]

/-- Double counting with weights, for a function `g` on edges supported near a set `F`. -/
lemma two_mul_sum_eq (hd : ∀ i, d i ∈ knightVecs) (hdist : DistinctEdges a d)
    (F : Finset Pt) (g : Pt → Pt → ℤ) (hsymm : ∀ i, g (a i + d i) (-d i) = g (a i) (d i))
    (hsupp : ∀ i, g (a i) (d i) ≠ 0 → a i ∈ F ∨ a i + d i ∈ F)
    (pat : Pt → Finset Pt) (hpat : ∀ v ∈ F, NbrsAre a d v (pat v)) :
    2 * ∑ i, g (a i) (d i) =
      ∑ v ∈ F, ∑ w ∈ pat v, g v (w - v) * (1 + if w ∈ F then 0 else 1) := by
  set G : Pt → Pt → ℤ := fun v w =>
    if v ∈ F then g v (w - v) * (1 + if w ∈ F then 0 else 1) else 0
  have step1 : ∀ i, 2 * g (a i) (d i) = G (a i) (a i + d i) + G (a i + d i) (a i) := by
    intro i
    have e1 : a i + d i - a i = d i := by abel
    have e2 : a i - (a i + d i) = -d i := by abel
    simp only [G, e1, e2, hsymm i]
    by_cases ha : a i ∈ F <;> by_cases hb : a i + d i ∈ F <;> simp only [ha, hb, ite_true,
      ite_false]
    · ring
    · ring
    · ring
    · have : g (a i) (d i) = 0 := by
        by_contra h; rcases hsupp i h with h | h <;> contradiction
      simp [this]
  have step2 : ∀ i, G (a i) (a i + d i) + G (a i + d i) (a i) = ∑ v ∈ F,
      ((if a i = v then G v (a i + d i) else 0) + (if a i + d i = v then G v (a i) else 0)) := by
    intro i
    rw [sum_add_distrib, sum_ite_eq, sum_ite_eq]
    simp only [G]
    split_ifs <;> simp_all
  rw [mul_sum, sum_congr rfl fun i _ => (step1 i).trans (step2 i), sum_comm]
  refine sum_congr rfl fun v hv => ?_
  rw [dart_sum a d hd hdist (hpat v hv) (G v)]
  refine sum_congr rfl fun w _ => ?_
  simp [G, hv]

lemma two_mul_sum_chi_col (R : ℕ) :
    2 * ∑ y ∈ Icc (0 : ℤ) R, chi (0, y) = 1 + chi (0, R) := by
  induction R with
  | zero => simp [chi]
  | succ k ih =>
    rw [show (Icc (0 : ℤ) ((k + 1 : ℕ) : ℤ)) = insert ((k : ℤ) + 1) (Icc 0 (k : ℤ)) by
      ext y; simp only [mem_insert, mem_Icc]; push_cast; omega]
    rw [sum_insert (by simp), mul_add, ih]
    have : chi (0, (k : ℤ) + 1) = - chi (0, (k : ℤ)) := by
      unfold chi; simp only [zero_add]; split_ifs <;> omega
    push_cast; rw [this]; ring

lemma two_mul_sum_chi_row (R : ℕ) :
    2 * ∑ x ∈ Icc (0 : ℤ) R, chi (x, 0) = 1 + chi (0, R) := by
  rw [← two_mul_sum_chi_col]
  congr 1
  refine sum_congr rfl fun x _ => ?_
  simp [chi]

/-- **Corner charge.** For a family of distinct knight edges inside the board, with degree two
on the box `[0, R]²` and with the pattern `P/P'` (signs `sL`, `sB`) on the four endpoint rows of
the left side (rows `R-1..R+2`) and the bottom side (columns `R-1..R+2`, transposed), some step
of the interior path `γ_R` has `ω = flux + χ` not divisible by 3. The pattern hypotheses are
stated for the family shifted by `(0, R)` and by `(R, 0)`. -/
theorem corner_charge (hd : ∀ i, d i ∈ knightVecs)
    (hpos : ∀ i, 0 ≤ (a i).1 ∧ 0 ≤ (a i).2 ∧ 0 ≤ (a i + d i).1 ∧ 0 ≤ (a i + d i).2)
    (R : ℕ) (hR : 12 ≤ R) (hdeg : ∀ v ∈ box R, deg a d v = 2)
    (sL sB : ℤ) (hsL : sL ∈ ({1, -1} : Finset ℤ)) (hsB : sB ∈ ({1, -1} : Finset ℤ))
    (hpatL : ∀ v ∈ FL, NbrsAre (fun i => a i - (0, (R : ℤ))) d v (patL sL v))
    (hpatB : ∀ v ∈ FB, NbrsAre (fun i => a i - ((R : ℤ), 0)) d v (patB sB v))
    (hdistL : DistinctEdges (fun i => a i - (0, (R : ℤ))) d)
    (hdistB : DistinctEdges (fun i => a i - ((R : ℤ), 0)) d) :
    ∃ q ∈ gammaSteps R, ¬ (3 : ℤ) ∣ flux a d q + chi q.1 := by
  by_contra hall
  push Not at hall
  have hR2 : (2 : ℤ) ≤ R := by omega
  have h0 := three_dvd_sum_bdry a d hd (box R) hdeg
  obtain ⟨dj1, dj2⟩ := disjoint_parts hR2
  rw [bdry_box hR2, sum_union dj1, sum_union dj2] at h0
  -- the interior path
  have hΓ : (3 : ℤ) ∣ ∑ q ∈ gammaSteps R, eps (box R) q * (flux a d q + chi q.1) :=
    dvd_sum fun q hq => dvd_mul_of_dvd_right (hall q hq) _
  -- the outer steps
  have hO : 2 * ∑ q ∈ outerSteps R, eps (box R) q * (flux a d q + chi q.1) =
      2 * (1 + chi (0, R)) := by
    have hflux : ∀ q ∈ outerSteps R, flux a d q = 0 := fun q hq =>
      sum_eq_zero fun i _ => flux1_outer (hd i) ⟨(hpos i).1, (hpos i).2.1⟩
        ⟨(hpos i).2.2.1, (hpos i).2.2.2⟩ hq
    rw [sum_congr rfl fun q hq => by rw [hflux q hq, zero_add]]
    unfold outerSteps
    rw [sum_union]
    · rw [sum_image (by intro x _ y _ h; simpa using h),
        sum_image (by intro x _ y _ h; simpa using h)]
      have e1 : ∀ y ∈ Icc (0 : ℤ) R, eps (box R) ((-1, y), false) * chi ((-1, y), false).1 =
          chi (0, y) := by
        intro y _; simp [eps, box, chi]; split_ifs <;> omega
      have e2 : ∀ x ∈ Icc (0 : ℤ) R, eps (box R) ((x, -1), true) * chi ((x, -1), true).1 =
          chi (x, 0) := by
        intro x _; simp [eps, box, chi]; split_ifs <;> omega
      rw [sum_congr rfl e1, sum_congr rfl e2, mul_add, two_mul_sum_chi_col, two_mul_sum_chi_row]
      ring
    · rw [disjoint_left]; intro q h1 h2
      simp only [mem_image] at h1 h2
      obtain ⟨y, -, rfl⟩ := h1; obtain ⟨x, -, h⟩ := h2; simp [Prod.ext_iff] at h
  -- the four end steps
  have hT : 2 * ∑ q ∈ T4 R, eps (box R) q * (flux a d q + chi q.1) = 4 * chi (0, R) := by
    have he : ∀ q ∈ T4 R, eps (box R) q = 1 := by
      intro q hq; simp only [T4, mem_insert, mem_singleton] at hq
      rcases hq with rfl | rfl | rfl | rfl <;> simp [eps, box] <;> omega
    rw [sum_congr rfl fun q hq => by rw [he q hq, one_mul], sum_add_distrib]
    have hchi : ∑ q ∈ T4 R, chi q.1 = 0 := by
      unfold T4
      rw [sum_insert (by simp [Prod.ext_iff]; try omega),
        sum_insert (by simp [Prod.ext_iff]; try omega),
        sum_insert (by simp [Prod.ext_iff]; try omega), sum_singleton]
      simp only [chi]; split_ifs <;> omega
    have hfl : ∑ q ∈ T4 R, flux a d q = ∑ i, (chi (0, (R : ℤ)) * gL (a i - (0, (R : ℤ))) (d i) +
        chi ((R : ℤ), 0) * gB (a i - ((R : ℤ), 0)) (d i)) := by
      simp only [flux]
      rw [sum_comm]
      refine sum_congr rfl fun i _ => ?_
      unfold T4
      rw [sum_insert (by simp [Prod.ext_iff]; try omega),
        sum_insert (by simp [Prod.ext_iff]; try omega),
        sum_insert (by simp [Prod.ext_iff]; try omega), sum_singleton]
      have t : ∀ (t : Pt) (c : Pt) (v : Bool), flux1 (a i) (d i) (c + t, v) =
          chi t * flux1 (a i - t) (d i) (c, v) := by
        intro t c v
        rw [← flux1_add _ _ t c v (hd i), sub_add_cancel]
      rw [show (((0 : ℤ), (R : ℤ)), true) = ((0, 0) + (0, (R : ℤ)), true) by simp,
        show (((1 : ℤ), (R : ℤ)), true) = ((1, 0) + (0, (R : ℤ)), true) by simp,
        show (((R : ℤ), (0 : ℤ)), false) = ((0, 0) + ((R : ℤ), 0), false) by simp,
        show (((R : ℤ), (1 : ℤ)), false) = ((0, 1) + ((R : ℤ), 0), false) by simp, t, t, t, t]
      simp only [gL, gB]; ring
    have hL := two_mul_sum_eq (fun i => a i - (0, (R : ℤ))) d hd hdistL FL gL
      (fun i => by simp only [sub_add_eq_add_sub]; rw [show a i + d i - (0, (R : ℤ)) =
        a i - (0, (R : ℤ)) + d i by abel]; exact gL_symm (hd i))
      (fun i h => by
        have := gL_support (hd i) (by simpa using (hpos i).1)
          (by have := (hpos i).2.2.1; simp only [Prod.fst_add, Prod.fst_sub] at this ⊢; omega) h
        simpa [sub_add_eq_add_sub] using this)
      (patL sL) hpatL
    have hB := two_mul_sum_eq (fun i => a i - ((R : ℤ), 0)) d hd hdistB FB gB
      (fun i => by simp only [sub_add_eq_add_sub]; rw [show a i + d i - ((R : ℤ), 0) =
        a i - ((R : ℤ), 0) + d i by abel]; exact gB_symm (hd i))
      (fun i h => by
        have := gB_support (hd i) (by simpa using (hpos i).2.1)
          (by have := (hpos i).2.2.2; simp only [Prod.snd_add, Prod.snd_sub] at this ⊢; omega) h
        simpa [sub_add_eq_add_sub] using this)
      (patB sB) hpatB
    rw [← CL, CL_eq sL hsL] at hL
    rw [← CB, CB_eq sB hsB] at hB
    have hc : chi ((R : ℤ), 0) = chi (0, (R : ℤ)) := by simp [chi]
    rw [hchi, add_zero, hfl, sum_add_distrib, ← mul_sum, ← mul_sum, hc]
    linear_combination chi (0, (R : ℤ)) * hL + chi (0, (R : ℤ)) * hB
  -- conclusion
  set O := ∑ q ∈ outerSteps R, eps (box R) q * (flux a d q + chi q.1)
  set T := ∑ q ∈ T4 R, eps (box R) q * (flux a d q + chi q.1)
  set Γ := ∑ q ∈ gammaSteps R, eps (box R) q * (flux a d q + chi q.1)
  obtain ⟨k, hk⟩ := h0
  obtain ⟨m, hm⟩ := hΓ
  have hchi1 : chi (0, (R : ℤ)) = 1 ∨ chi (0, (R : ℤ)) = -1 := by
    unfold chi; split_ifs <;> simp
  rcases hchi1 with h | h <;> rw [h] at hO hT <;> omega

end Family

end KT
