import LeanSoln.data

def lines : List String := data.splitOn "\n"

def relRules : List String → List String := List.takeWhile (λ x ↦ x.data.contains '|')

def printRules (xs : List String) : List String := (List.dropWhile (λ x ↦ x.data.contains '|') xs).tail!

def intRelRules : List String → List (Nat × Nat) := List.map (λ x ↦ let xs := x.splitOn "|" ; (xs.head!.toNat!, xs.tail!.head!.toNat!))
def intPrintRules : List String → List (List Nat) := List.map (λ x ↦ List.map (λ y ↦ y.toNat!) (x.splitOn ","))

def rel (x y : Nat) (xs : List (Nat × Nat)) : Bool := if (xs.contains (x, y)) then true else Bool.not $ xs.contains (y, x)

def validLine : List (Nat × Nat) → List Nat → Bool
  | _, [] => true
  | _, (_ :: []) => true
  | relations, (x :: xs) => Bool.and (List.all (List.map (rel x . relations) xs) id) (validLine relations xs)

def countTrue : List Bool → Nat
  | [] => 0
  | (x :: xs) => (if x then 1 else 0) + countTrue xs

def validRules (xs : List String) : List (List Nat) := List.filter (λ x ↦ validLine (intRelRules $ relRules xs) x) (intPrintRules $ printRules xs)

def middle (xs : List Nat) : Nat := xs.get! (xs.length / 2)

def sum : List Nat → Nat
  | [] => 0
  | (x :: xs) => x + (sum xs)



#eval sum (List.map middle (validRules lines))
