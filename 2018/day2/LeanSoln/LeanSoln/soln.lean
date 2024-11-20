import LeanSoln.data

def any : List Bool → Bool
  | [] => false
  | (x :: xs) => if x then true else any xs

def map {α β : Type} : (α → β) → List α → List β
  | _, [] => []
  | f, (x :: xs) => f x :: map f xs

def filter {α : Type} : (α → Bool) → List α → List α
  | _, [] => []
  | f, (x :: xs) => if f x then x :: (filter f xs) else filter f xs

def lines : List String := String.splitOn data "\n"

def testlines : List String := ["abcde","fghij","klmno","pqrst","fguij","axcye","wvxyz"]

def merge : (Char × Nat) → List (Char × Nat) → List (Char × Nat)
  | cn, [] => [cn]
  | cn, (x :: xs) => if (cn.fst == x.fst) then ((x.fst, x.snd + cn.snd) :: xs) else x :: (merge cn xs)

def formCount (m : String) : List (Char × Nat) := 
  match (String.data m) with
  | [] => []
  | (x :: xs) => merge (x, 1) (formCount xs.asString)

def hasDouble (s : String) : Bool := any (map (λ x => x.snd == 2) (formCount s))

def hasTriple (s : String) : Bool := any (map (λ x => x.snd == 3) (formCount s))

def countDoubles : List String → Nat
  | [] => 0
  | (x :: xs) => (if (hasDouble x) then 1 else 0) + countDoubles xs

def countTriples : List String → Nat
  | [] => 0
  | (x :: xs) => (if (hasTriple x) then 1 else 0) + countTriples xs

def answer (l : List String) : Nat := (countDoubles l) * (countTriples l)

def diff (l m : String) : Nat :=
  match String.data l with
  | (x :: xs) => match String.data m with
                 | (y :: ys) => (if (x ≠ y) then 1 else 0) + diff (xs.asString) (ys.asString)
                 | [] => 0
  | [] => 0

def findOneDiff : List String → List (String × String)
  | [] => []
  | (x :: xs) => (map (λ z => (x, z.snd)) (filter (λ y => y.fst == 1) (map (λ z => (diff x z, z)) xs))) ++ (findOneDiff xs)

#eval! findOneDiff lines
