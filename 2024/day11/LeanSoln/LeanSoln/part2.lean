import LeanSoln.data

def testData : String := "125 17"

def line (str : String) : List Nat := List.map (λ s ↦ s.toNat!) (str.splitOn " ")

def split (n : Nat) := let len := n.repr.length; ((List.take (len/2) n.repr.data).asString.toNat!, (List.drop (len/2) n.repr.data).asString.toNat!)

def flatten : List ((Sum (Nat × Nat) Nat) × Nat) → List (Nat × Nat) :=
  List.foldl
  (λ fst ↦ (λ (snd, c) ↦ match snd with
          | (Sum.inl (x, y)) => fst ++ [(x, c), (y, c)] 
          | (Sum.inr x) => fst ++ [(x, c)]
  )) []

def countTotals : List (Nat × Nat) → Nat := List.foldl (λ tot ↦ (λ (_, count) ↦ tot + count)) 0

def applyRule : (Nat × Nat) → (Sum (Nat × Nat) Nat) × Nat
  | (0, c) => (Sum.inr 1, c)
  | (n, c) => if Nat.mod (n.repr.length) 2 == 0 then (Sum.inl (split n), c)
         else (Sum.inr (n * 2024), c)

def unionSums (xs : List (Nat × Nat)) : List (Nat × Nat) := List.map (λ (x, _) ↦ (x, countTotals (List.filter (λ (y, _) ↦ x=y) xs))) xs

def List.unique : List (Nat × Nat) → List (Nat × Nat) := List.foldl (λ xs ↦ (λ xy ↦ if xs.contains xy then xs else xs ++ [xy])) []

def applyN : Nat → List (Nat × Nat) → List (Nat × Nat)
  | 0, xs => xs
  | (n+1), xs => applyN n (unionSums $ flatten (List.map applyRule xs)).unique

def answer : Nat := countTotals $ applyN 75 (List.map (λ n ↦ (n, 1)) (line data))
