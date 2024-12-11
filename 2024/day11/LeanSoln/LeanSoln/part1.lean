import LeanSoln.data

def testData : String := "125 17"

def line (str : String) : List Nat := List.map (λ s ↦ s.toNat!) (str.splitOn " ")

def split (n : Nat) := let len := n.repr.length; ((List.take (len/2) n.repr.data).asString.toNat!, (List.drop (len/2) n.repr.data).asString.toNat!)

def flatten : List (Sum (Nat × Nat) Nat) → List Nat :=
  List.foldl
  (λ fst ↦ (λ snd ↦ match snd with
          | (Sum.inl (x, y)) => fst ++ [x, y] 
          | (Sum.inr x) => fst ++ [x]
  )) []

def applyRule : Nat → Sum (Nat × Nat) Nat
  | 0 => Sum.inr 1
  | n => if Nat.mod (n.repr.length) 2 == 0 then Sum.inl (split n)
         else Sum.inr (n * 2024)

def applyN : Nat → List Nat → List Nat
  | 0, xs => xs
  | (n+1), xs => applyN n (flatten (List.map applyRule xs))

#eval (applyN 25 (line data)).length
