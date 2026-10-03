import Ktlean.Flux

/-!
# Lattice paths of knight edges (finite certificate)

Each knight edge from `p` to `p + d` crosses the dual grid along a lattice path of three unit
steps `p = v₀ → v₁ → v₂ → v₃ = p + d` (the Voronoi cells that the segment visits). Its flux
through the dual segment of a grid edge `q` is `χ(p)` times the signed number of steps along `q`.
So its flux out of any finite lattice point set `B` telescopes to `χ(p) ([p ∈ B] - [p+d ∈ B])`.
Summing over a 2-factor gives `Σ_{∂B} ω = Σ_{v ∈ B} χ(v) (deg v + 4) ≡ 0 (mod 3)` if every
`v ∈ B` has degree 2.
-/

open Finset

namespace KT

/-- The unit vector of the grid edge direction. -/
def dirOf (v : Bool) : Pt := if v then (0, 1) else (1, 0)

/-- The signed number of times the unit step `u → w` runs along the grid edge `q`
(`+1` from its first to its second endpoint, `-1` the other way). -/
def stepSign (u w : Pt) (q : GridEdge) : ℤ :=
  if u = q.1 ∧ w = q.1 + dirOf q.2 then 1
  else if w = q.1 ∧ u = q.1 + dirOf q.2 then -1 else 0

/-- The middle points of the lattice path of the knight edge from `(0,0)` to `d`. -/
def mid1 (d : Pt) : Pt := if |d.1| = 2 then (Int.sign d.1, 0) else (0, Int.sign d.2)
def mid2 (d : Pt) : Pt := (Int.sign d.1, Int.sign d.2)

/-- The signed number of steps of the lattice path of the knight edge `p → p + d` along `q`. -/
def pathSign (p d : Pt) (q : GridEdge) : ℤ :=
  stepSign p (p + mid1 d) q + stepSign (p + mid1 d) (p + mid2 d) q +
    stepSign (p + mid2 d) (p + d) q

lemma flux1_eq_path_rel : ∀ x ∈ Icc (-4 : ℤ) 4, ∀ y ∈ Icc (-4 : ℤ) 4, ∀ d ∈ knightVecs,
    ∀ v : Bool, flux1 (x, y) d ((0, 0), v) = chi (x, y) * pathSign (x, y) d ((0, 0), v) := by
  decide +kernel

end KT
