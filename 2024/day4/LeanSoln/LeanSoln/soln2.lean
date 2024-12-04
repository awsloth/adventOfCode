import LeanSoln.data

def lines : List String := data.splitOn "\n"

def Grid : Type := (Char × Char × Char) × (Char × Char × Char) × (Char × Char × Char)

def lines3 (xs : List String) : List (String × String × String) := List.zip xs (List.zip xs.tail! xs.tail!.tail!)

def cutIntoThrees : List Char × List Char × List Char → List Grid
  | (x, y, z) => let xs := List.zip x (List.zip y z) ; List.zip xs (List.zip xs.tail! xs.tail!.tail!)

def cut3 : List (List Char × List Char × List Char) →  List Grid
  | [] => []
  | (x :: xs) => (cutIntoThrees x) ++ (cut3 xs)

def to3x3 : List String → List Grid := cut3 ∘ (List.map (λ (x, y, z) ↦ (x.data, y.data, z.data)) .) ∘ lines3

def crossValid : Grid → Bool
  | (('M', _, 'M'), (_, 'A', _), ('S', _, 'S')) => true
  | (('S', _, 'M'), (_, 'A', _), ('S', _, 'M')) => true
  | (('M', _, 'S'), (_, 'A', _), ('M', _, 'S')) => true
  | (('S', _, 'S'), (_, 'A', _), ('M', _, 'M')) => true
  | _ => false

def countTrue : List Bool → Nat
  | [] => 0
  | (true :: xs) => Nat.succ (countTrue xs)
  | (false :: xs) => countTrue xs

#eval countTrue $ List.map crossValid (to3x3 lines)
