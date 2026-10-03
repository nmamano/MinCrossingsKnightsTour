import Ktlean.LoopCert

/-!
# Flux through the boundary of a lattice point set

Each knight edge from `p` to `p + d` crosses the dual grid along a lattice path of three unit
steps `p = v₀ → v₁ → v₂ → v₃ = p + d` (the Voronoi cells that the segment visits). Its flux
through the dual segment of a grid edge `q` is `χ(p)` times the signed number of steps along `q`
(`flux1_eq_path`). So its flux out of any finite lattice point set `B` telescopes to
`χ(p) ([p ∈ B] - [p+d ∈ B])`.
-/

open Finset

namespace KT

lemma stepSign_sub (u w a : Pt) (v : Bool) :
    stepSign u w (a, v) = stepSign (u - a) (w - a) ((0, 0), v) := by
  unfold stepSign
  simp only [Prod.ext_iff, Prod.fst_sub, Prod.snd_sub, Prod.fst_add, Prod.snd_add]
  split_ifs <;> omega

lemma pathSign_sub (p d a : Pt) (v : Bool) :
    pathSign p d (a, v) = pathSign (p - a) d ((0, 0), v) := by
  have e : ∀ x : Pt, p + x - a = (p - a) + x := fun x => by abel
  unfold pathSign
  rw [stepSign_sub, stepSign_sub _ _ a, stepSign_sub _ _ a, e, e, e]

lemma mid_bounds {d : Pt} (hd : d ∈ knightVecs) :
    -1 ≤ (mid1 d).1 ∧ (mid1 d).1 ≤ 1 ∧ -1 ≤ (mid1 d).2 ∧ (mid1 d).2 ≤ 1 ∧
    -1 ≤ (mid2 d).1 ∧ (mid2 d).1 ≤ 1 ∧ -1 ≤ (mid2 d).2 ∧ (mid2 d).2 ≤ 1 ∧
    -2 ≤ d.1 ∧ d.1 ≤ 2 ∧ -2 ≤ d.2 ∧ d.2 ≤ 2 := by
  simp only [knightVecs, mem_insert, mem_singleton] at hd
  rcases hd with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl <;> decide

lemma stepSign_ne_zero {u w : Pt} {v : Bool} (h : stepSign u w ((0, 0), v) ≠ 0) :
    0 ≤ u.1 ∧ u.1 ≤ 1 ∧ 0 ≤ u.2 ∧ u.2 ≤ 1 := by
  unfold stepSign dirOf at h
  cases v <;> simp only [Prod.ext_iff, Prod.fst_add, Prod.snd_add, ite_true, ite_false,
      Bool.false_eq_true] at h <;> split_ifs at h with h1 h2 <;> omega

/-- **Flux of a knight edge = colour times its lattice path.** -/
theorem flux1_eq_path {d : Pt} (hd : d ∈ knightVecs) (p : Pt) (q : GridEdge) :
    flux1 p d q = chi p * pathSign p d q := by
  obtain ⟨a, v⟩ := q
  have T1 : flux1 p d (a, v) = chi a * flux1 (p - a) d ((0, 0), v) := by
    unfold flux1
    have hc : chi p = chi a * chi (p - a) := by rw [← chi_add]; congr 1; abel
    rw [if_congr (crossesDual_sub p d a v) rfl rfl, hc]
    split_ifs <;> ring
  have hc : chi p = chi a * chi (p - a) := by rw [← chi_add]; congr 1; abel
  rw [T1, pathSign_sub, hc, mul_assoc]
  congr 1
  set r := p - a
  by_cases hnear : r.1 ∈ Icc (-4 : ℤ) 4 ∧ r.2 ∈ Icc (-4 : ℤ) 4
  · have := flux1_eq_path_rel r.1 hnear.1 r.2 hnear.2 d hd v
    rwa [Prod.mk.eta] at this
  · simp only [mem_Icc] at hnear
    have h1 : ¬ CrossesDual r d ((0, 0), v) := fun h => by
      have := h.bounds hd; omega
    have hb := mid_bounds hd
    have z : ∀ u w : Pt, ¬ (0 ≤ u.1 ∧ u.1 ≤ 1 ∧ 0 ≤ u.2 ∧ u.2 ≤ 1) →
        stepSign u w ((0, 0), v) = 0 := fun u w hu => by
      by_contra h; exact hu (stepSign_ne_zero h)
    have h2 : pathSign r d ((0, 0), v) = 0 := by
      unfold pathSign
      rw [z, z, z] <;> (try simp only [Prod.fst_add, Prod.snd_add]) <;> omega
    simp [flux1, h1, h2]

/-- The four unit vectors. -/
def dirs4 : Finset Pt := {(1, 0), (-1, 0), (0, 1), (0, -1)}

/-- The grid edge run along by the unit step `u → u + δ`. -/
def stepEdge (u δ : Pt) : GridEdge :=
  if δ = (1, 0) then (u, false) else if δ = (-1, 0) then (u + δ, false)
  else if δ = (0, 1) then (u, true) else (u + δ, true)

/-- The sign of the unit step `δ` relative to its grid edge. -/
def stepSgn (δ : Pt) : ℤ := if δ = (1, 0) ∨ δ = (0, 1) then 1 else -1

/-- The grid edges with exactly one endpoint in `B`, i.e. the dual steps of the boundary
of `B`. -/
def bdry (B : Finset Pt) : Finset GridEdge :=
  ((B ×ˢ dirs4).image fun x => stepEdge x.1 x.2).filter
    fun q => ¬ (q.1 ∈ B ↔ q.1 + dirOf q.2 ∈ B)

/-- Orientation of a boundary step: `1` if the normal of `q` points out of `B`. -/
def eps (B : Finset Pt) (q : GridEdge) : ℤ := if q.1 ∈ B then 1 else -1

lemma chi_dir {δ : Pt} (h : δ ∈ dirs4) : chi δ = -1 := by
  simp only [dirs4, mem_insert, mem_singleton] at h
  rcases h with rfl | rfl | rfl | rfl <;> decide

lemma chi_knight {δ : Pt} (h : δ ∈ knightVecs) : chi δ = -1 := by
  simp only [knightVecs, mem_insert, mem_singleton] at h
  rcases h with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl <;> decide

lemma stepEdge_spec (u : Pt) {δ : Pt} (hδ : δ ∈ dirs4) :
    ((stepEdge u δ).1 = u ∧ (stepEdge u δ).1 + dirOf (stepEdge u δ).2 = u + δ ∧
      stepSgn δ = 1) ∨
    ((stepEdge u δ).1 = u + δ ∧ (stepEdge u δ).1 + dirOf (stepEdge u δ).2 = u ∧
      stepSgn δ = -1) := by
  simp only [dirs4, mem_insert, mem_singleton] at hδ
  rcases hδ with rfl | rfl | rfl | rfl
  · left; simp [stepEdge, dirOf, stepSgn]
  · right; refine ⟨by simp [stepEdge], ?_, by simp [stepSgn]⟩
    simp only [stepEdge, dirOf]; ext <;> simp
  · left; simp [stepEdge, dirOf, stepSgn]
  · right; refine ⟨by simp [stepEdge], ?_, by simp [stepSgn]⟩
    simp only [stepEdge, dirOf]; ext <;> simp

lemma stepSign_eq (u : Pt) {δ : Pt} (hδ : δ ∈ dirs4) (q : GridEdge) :
    stepSign u (u + δ) q = if q = stepEdge u δ then stepSgn δ else 0 := by
  obtain ⟨⟨q1, q2⟩, v⟩ := q
  obtain ⟨u1, u2⟩ := u
  simp only [dirs4, mem_insert, mem_singleton] at hδ
  rcases hδ with rfl | rfl | rfl | rfl <;> cases v <;>
    simp [stepSign, stepEdge, stepSgn, dirOf, Prod.ext_iff] <;> split_ifs <;> omega

lemma stepEdge_neg (u : Pt) {δ : Pt} (hδ : δ ∈ dirs4) :
    stepEdge (u + δ) (-δ) = stepEdge u δ := by
  simp only [dirs4, mem_insert, mem_singleton] at hδ
  rcases hδ with rfl | rfl | rfl | rfl <;> simp [stepEdge, Prod.ext_iff]

lemma neg_mem_dirs4 {δ : Pt} (hδ : δ ∈ dirs4) : -δ ∈ dirs4 := by
  simp only [dirs4, mem_insert, mem_singleton] at hδ ⊢
  rcases hδ with rfl | rfl | rfl | rfl <;> simp

/-- **Telescoping:** the flux of one unit step `u → u + δ` out of `B`. -/
lemma sum_bdry_stepSign (B : Finset Pt) (u : Pt) {δ : Pt} (hδ : δ ∈ dirs4) :
    ∑ q ∈ bdry B, eps B q * stepSign u (u + δ) q =
      (if u ∈ B then 1 else 0) - (if u + δ ∈ B then 1 else 0) := by
  simp only [stepSign_eq u hδ, mul_ite, mul_zero]
  rw [sum_ite_eq']
  have himg : u ∈ B ∨ u + δ ∈ B →
      stepEdge u δ ∈ (B ×ˢ dirs4).image fun x => stepEdge x.1 x.2 := by
    rintro (h | h)
    · exact mem_image.2 ⟨(u, δ), mem_product.2 ⟨h, hδ⟩, rfl⟩
    · exact mem_image.2 ⟨(u + δ, -δ), mem_product.2 ⟨h, neg_mem_dirs4 hδ⟩,
        stepEdge_neg u hδ⟩
  have hmem : stepEdge u δ ∈ bdry B ↔ ¬ (u ∈ B ↔ u + δ ∈ B) := by
    unfold bdry
    rw [mem_filter]
    rcases stepEdge_spec u hδ with ⟨h1, h2, -⟩ | ⟨h1, h2, -⟩ <;> rw [h2, h1]
    · constructor
      · exact fun h => h.2
      · intro h; refine ⟨himg ?_, h⟩; by_cases hu : u ∈ B <;> tauto
    · constructor
      · exact fun h => fun h' => h.2 h'.symm
      · intro h; refine ⟨himg ?_, fun h' => h h'.symm⟩; by_cases hu : u ∈ B <;> tauto
  by_cases hu : u ∈ B <;> by_cases hw : u + δ ∈ B
  · rw [ite_eq_right (by rw [hmem]; tauto)]; simp [hu, hw]
  · rw [ite_eq_left (by rw [hmem]; tauto)]
    rcases stepEdge_spec u hδ with ⟨h1, -, h3⟩ | ⟨h1, -, h3⟩ <;> simp [eps, h1, h3, hu, hw]
  · rw [ite_eq_left (by rw [hmem]; tauto)]
    rcases stepEdge_spec u hδ with ⟨h1, -, h3⟩ | ⟨h1, -, h3⟩ <;> simp [eps, h1, h3, hu, hw]
  · rw [ite_eq_right (by rw [hmem]; tauto)]; simp [hu, hw]

lemma path_steps {d : Pt} (hd : d ∈ knightVecs) :
    mid1 d ∈ dirs4 ∧ mid2 d - mid1 d ∈ dirs4 ∧ d - mid2 d ∈ dirs4 := by
  simp only [knightVecs, mem_insert, mem_singleton] at hd
  rcases hd with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl <;> decide

/-- The flux of one knight edge out of `B`. -/
lemma sum_bdry_flux1 {d : Pt} (hd : d ∈ knightVecs) (B : Finset Pt) (p : Pt) :
    ∑ q ∈ bdry B, eps B q * flux1 p d q =
      chi p * ((if p ∈ B then 1 else 0) - (if p + d ∈ B then 1 else 0)) := by
  obtain ⟨s1, s2, s3⟩ := path_steps hd
  have h1 := sum_bdry_stepSign B p s1
  have h2 := sum_bdry_stepSign B (p + mid1 d) s2
  have h3 := sum_bdry_stepSign B (p + mid2 d) s3
  rw [show p + mid1 d + (mid2 d - mid1 d) = p + mid2 d by abel] at h2
  rw [show p + mid2 d + (d - mid2 d) = p + d by abel] at h3
  simp only [flux1_eq_path hd, pathSign]
  have : ∀ q, eps B q * (chi p * (stepSign p (p + mid1 d) q +
      stepSign (p + mid1 d) (p + mid2 d) q + stepSign (p + mid2 d) (p + d) q)) =
      chi p * (eps B q * stepSign p (p + mid1 d) q +
        eps B q * stepSign (p + mid1 d) (p + mid2 d) q +
        eps B q * stepSign (p + mid2 d) (p + d) q) := fun q => by ring
  rw [sum_congr rfl fun q _ => this q, ← mul_sum, sum_add_distrib, sum_add_distrib, h1, h2, h3]
  ring

variable {ι : Type*} [Fintype ι] (a d : ι → Pt)

/-- The flux of a family of knight edges out of `B`. -/
lemma sum_bdry_flux (hd : ∀ i, d i ∈ knightVecs) (B : Finset Pt) :
    ∑ q ∈ bdry B, eps B q * flux a d q =
      ∑ i, chi (a i) * ((if a i ∈ B then 1 else 0) - (if a i + d i ∈ B then 1 else 0)) := by
  simp only [flux, mul_sum]
  rw [sum_comm]
  exact sum_congr rfl fun i _ => sum_bdry_flux1 (hd i) B (a i)

/-- The degree of a lattice point in the family. -/
def deg (v : Pt) : ℕ :=
  (univ.filter fun i => a i = v).card + (univ.filter fun i => a i + d i = v).card

lemma sum_flux_eq_deg (hd : ∀ i, d i ∈ knightVecs) (B : Finset Pt) :
    ∑ i, chi (a i) * ((if a i ∈ B then 1 else 0) - (if a i + d i ∈ B then 1 else 0)) =
      ∑ v ∈ B, chi v * (deg a d v : ℤ) := by
  have hc : ∀ i, chi (a i + d i) = - chi (a i) := fun i => by
    rw [chi_add, chi_knight (hd i)]; ring
  have e : ∀ i, chi (a i) * ((if a i ∈ B then 1 else 0) - (if a i + d i ∈ B then 1 else 0)) =
      (∑ v ∈ B, if a i = v then chi v else 0) + (∑ v ∈ B, if a i + d i = v then chi v else 0) := by
    intro i
    rw [sum_ite_eq, sum_ite_eq]
    by_cases h1 : a i ∈ B <;> by_cases h2 : a i + d i ∈ B <;> simp [h1, h2, hc]
  rw [sum_congr rfl fun i _ => e i, sum_add_distrib, sum_comm, sum_comm (s := univ)]
  rw [← sum_add_distrib]
  refine sum_congr rfl fun v _ => ?_
  simp only [deg, Nat.cast_add, mul_add, ← sum_boole, mul_sum]
  congr 1 <;> refine sum_congr rfl fun i _ => ?_ <;> split_ifs <;> simp_all

omit [Fintype ι] in
lemma sum_bdry_chi (B : Finset Pt) :
    ∑ q ∈ bdry B, eps B q * chi q.1 =
      ∑ v ∈ B, ∑ δ ∈ dirs4, chi v * (1 - (if v + δ ∈ B then 1 else 0)) := by
  set S := (B ×ˢ dirs4).filter fun x => x.1 + x.2 ∉ B
  have hbd : bdry B = S.image fun x => stepEdge x.1 x.2 := by
    ext q
    simp only [bdry, S, mem_filter, mem_image, mem_product]
    constructor
    · rintro ⟨⟨⟨v, δ⟩, ⟨hv, hδ⟩, rfl⟩, hx⟩
      refine ⟨(v, δ), ⟨⟨hv, hδ⟩, ?_⟩, rfl⟩
      rcases stepEdge_spec v hδ with ⟨h1, h2, -⟩ | ⟨h1, h2, -⟩ <;> rw [h2, h1] at hx <;> tauto
    · rintro ⟨⟨v, δ⟩, ⟨⟨hv, hδ⟩, hout⟩, rfl⟩
      refine ⟨⟨(v, δ), ⟨hv, hδ⟩, rfl⟩, ?_⟩
      rcases stepEdge_spec v hδ with ⟨h1, h2, -⟩ | ⟨h1, h2, -⟩ <;> rw [h2, h1] <;> tauto
  have hinj : Set.InjOn (fun x : Pt × Pt => stepEdge x.1 x.2) S := by
    rintro ⟨v, δ⟩ hx ⟨w, γ⟩ hy hvw
    simp only [S, coe_filter, mem_product, Set.mem_ofPred_eq] at hx hy
    simp only at hvw
    have sv := stepEdge_spec v hx.1.2
    have sw := stepEdge_spec w hy.1.2
    rw [hvw] at sv
    rcases sv with ⟨a1, a2, -⟩ | ⟨a1, a2, -⟩ <;> rcases sw with ⟨b1, b2, -⟩ | ⟨b1, b2, -⟩
    · have e1 : v = w := a1.symm.trans b1
      subst e1
      exact Prod.ext rfl (add_left_cancel (a2.symm.trans b2))
    · exact absurd ((a2.symm.trans b2) ▸ hy.1.1) hx.2
    · exact absurd ((b2.symm.trans a2) ▸ hx.1.1) hy.2
    · have e2 : v = w := a2.symm.trans b2
      subst e2
      exact Prod.ext rfl (add_left_cancel (a1.symm.trans b1))
  rw [hbd, sum_image hinj]
  have hval : ∀ x ∈ S, eps B (stepEdge x.1 x.2) * chi (stepEdge x.1 x.2).1 = chi x.1 := by
    rintro ⟨v, δ⟩ hx
    simp only [S, mem_filter, mem_product] at hx
    rcases stepEdge_spec v hx.1.2 with ⟨h1, -, -⟩ | ⟨h1, -, -⟩
    · simp [eps, h1, hx.1.1]
    · simp only [eps, h1, hx.2, ite_false, chi_add, chi_dir hx.1.2]; ring
  rw [sum_congr rfl hval, sum_filter, sum_product]
  refine sum_congr rfl fun v _ => sum_congr rfl fun δ _ => ?_
  split_ifs <;> simp_all

omit [Fintype ι] in
lemma sum_chi_inside (B : Finset Pt) :
    ∑ v ∈ B, ∑ δ ∈ dirs4, chi v * (if v + δ ∈ B then 1 else 0) = 0 := by
  rw [← sum_product (f := fun x : Pt × Pt => chi x.1 * (if x.1 + x.2 ∈ B then 1 else 0))]
  rw [← sum_filter_add_sum_filter_not _ (fun x : Pt × Pt => x.1 + x.2 ∈ B)]
  have h0 : ∑ x ∈ (B ×ˢ dirs4).filter (fun x : Pt × Pt => ¬ x.1 + x.2 ∈ B),
      chi x.1 * (if x.1 + x.2 ∈ B then 1 else 0) = 0 :=
    sum_eq_zero fun x hx => by simp only [mem_filter] at hx; simp [hx.2]
  rw [h0, add_zero]
  refine sum_involution (fun x _ => (x.1 + x.2, -x.2)) ?_ ?_ ?_ ?_
  · rintro ⟨v, δ⟩ hx
    simp only [mem_filter, mem_product] at hx
    simp only [hx.2, ite_true, add_neg_cancel_right, hx.1.1, chi_add, chi_dir hx.1.2]
    ring
  · rintro ⟨v, δ⟩ hx _ h
    simp only [mem_filter, mem_product] at hx
    simp only [Prod.mk.injEq] at h
    have h0 : δ = 0 := by simpa using h.1
    subst h0
    simp [dirs4, Prod.ext_iff] at hx
  · rintro ⟨v, δ⟩ hx
    simp only [mem_filter, mem_product] at hx ⊢
    exact ⟨⟨hx.2, neg_mem_dirs4 hx.1.2⟩, by simpa using hx.1.1⟩
  · rintro ⟨v, δ⟩ _
    simp

/-- **The closed-loop identity.** If every lattice point of `B` has degree two in the family,
then the total of `ω = flux + χ` around the boundary of `B` (with outward orientation) is `0`
mod 3. -/
theorem three_dvd_sum_bdry (hd : ∀ i, d i ∈ knightVecs) (B : Finset Pt)
    (hdeg : ∀ v ∈ B, deg a d v = 2) :
    (3 : ℤ) ∣ ∑ q ∈ bdry B, eps B q * (flux a d q + chi q.1) := by
  simp only [mul_add, sum_add_distrib]
  rw [sum_bdry_flux a d hd, sum_flux_eq_deg a d hd, sum_bdry_chi]
  have h4 := sum_chi_inside B
  have : ∑ v ∈ B, ∑ δ ∈ dirs4, chi v * (1 - (if v + δ ∈ B then 1 else 0)) =
      ∑ v ∈ B, 4 * chi v - ∑ v ∈ B, ∑ δ ∈ dirs4, chi v * (if v + δ ∈ B then 1 else 0) := by
    rw [← sum_sub_distrib]
    refine sum_congr rfl fun v _ => ?_
    simp only [mul_sub, mul_one, sum_sub_distrib, sum_const]
    simp [dirs4]
  rw [this, h4, sub_zero, sum_congr rfl fun v hv => by rw [hdeg v hv]]
  refine ⟨∑ v ∈ B, 2 * chi v, ?_⟩
  rw [mul_sum, ← sum_add_distrib]
  refine sum_congr rfl fun v _ => ?_
  push_cast; ring

end KT
