import LeanSoln.data

def lines (xs : String) : List (Nat × List Nat) := List.map (λ y ↦ let sr := y.splitOn ": " ; (sr.head!.toNat!, (List.map (λ z ↦ z.toNat!) (sr.tail!.head!.splitOn " ")))) (xs.splitOn "\n")

def List.prod : List Nat → Nat
  | [] => 1
  | (x :: xs) => x * List.prod xs

def List.sum : List Nat → Nat
  | [] => 0
  | (x :: xs) => x + List.sum xs

def concat : Nat → Nat → Nat
  | x, y => (String.append x.repr y.repr).toNat!

def genSumsHelp : List Nat → List Nat
  | [] => []
  | (x :: []) => [x]
  | (x :: xs) => let prev := (genSumsHelp xs); (List.map (.+x) prev) ++ (List.map (.*x) prev) ++ (List.map (concat . x) prev)

def genSums (xs : List Nat) : List Nat := genSumsHelp xs.reverse

def satLine : (Nat × List Nat) → Bool
  | (x, xs) => (genSums xs).contains x

def answer := List.sum (List.map (λ y ↦ y.fst) (List.filter satLine (lines data)))
