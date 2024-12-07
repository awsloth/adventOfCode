import LeanSoln.data

def lines (xs : String) : List (Nat × List Nat) := List.map (λ y ↦ let sr := y.splitOn ": " ; (sr.head!.toNat!, (List.map (λ z ↦ z.toNat!) (sr.tail!.head!.splitOn " ")))) (xs.splitOn "\n")

def List.prod : List Nat → Nat
  | [] => 1
  | (x :: xs) => x * List.prod xs

def List.sum : List Nat → Nat
  | [] => 0
  | (x :: xs) => x + List.sum xs

def maxLineValueHelp : List Nat → Nat
  | [] => 0
  | (x :: []) => x
  | (n :: (1 :: [])) => 1 + n
  | (1 :: xs) => 1 + (maxLineValueHelp xs)
  | (n :: xs) => n * (maxLineValueHelp xs)

def maxLineValue (xs : List Nat) : Nat := maxLineValueHelp xs.reverse

def minLineValueHelp : List Nat → Nat
  | [] => 0
  | (x :: []) => x
  | (n :: (1 :: [])) => n
  | (1 :: xs) => 1 * (minLineValueHelp xs)
  | (n :: xs) => n + (minLineValueHelp xs)


def minLineValue (xs : List Nat) : Nat := minLineValueHelp xs.reverse

def linePossible : Nat × List Nat → Bool
  | (x, xs) => Bool.and (x ≤ maxLineValue xs) (x ≥ minLineValue xs)

def rejectImposs : List (Nat × List Nat) → List (Nat × List Nat) := List.filter linePossible

def genSumsHelp : List Nat → List Nat
  | [] => []
  | (x :: []) => [x]
  | (x :: xs) => let prev := (genSumsHelp xs); (List.map (.+x) prev) ++ (List.map (.*x) prev)

def genSums (xs : List Nat) : List Nat := genSumsHelp xs.reverse

def satLine : (Nat × List Nat) → Bool
  | (x, xs) => (genSums xs).contains x

def answer := List.sum (List.map (λ y ↦ y.fst) (List.filter satLine (rejectImposs $ lines data)))
