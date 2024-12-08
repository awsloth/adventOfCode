import LeanSoln.data

def lines : List String := data.splitOn "\n"

def gridDims : (Nat × Nat) := (lines.head!.length, lines.length)

def List.enumerate {α : Type} (xs : List α) : List (Nat × α) := List.zip (List.range xs.length) xs

def List.flatten {α : Type} : List (List α) → List α
  | [] => []
  | (x :: xs) => x ++ xs.flatten

def items (xs : List String) : List (Nat × Nat × Char) := (List.map (λ (y, s) ↦ (List.map (λ (x, c) ↦ (x, y, c)) (List.enumerate s))) (List.enumerate (List.map (λ s ↦ s.data) xs))).flatten

def itemFilter : List (Nat × Nat × Char) → List (Nat × Nat × Char) := List.filter (λ (_, _, c) ↦ c ≠ '.')

def itemOrdering : (Nat × Nat × Char) → (Nat × Nat × Char) → Bool
  | (_, _, c), (_, _, c2) => c < c2

def sortItems (xs : List (Nat × Nat × Char)) : List (Nat × Nat × Char) := (Array.qsort xs.toArray itemOrdering).toList

theorem dropWhileL (c : Char) (xs : List (Nat × Nat × Char)) : sizeOf (List.dropWhile (λ (_, _, c1) ↦ c == c1) xs) < 1 + sizeOf xs := by
  match xs with
  | [] => simp
  | ((x, y, c1) :: ys) => simp[List.dropWhile]
                          match c == c1 with
                          | true => simp
                                    simp[← Nat.add_comm (sizeOf ys)]
                                    simp[← Nat.add_assoc]
                                    simp[Nat.add_assoc (1 + sizeOf ys)]
                                    simp[Nat.lt_add_right (2 + x + 1 + y + c1.toNat + 3) (dropWhileL c ys)]
                          | false => simp

def groupItems : List (Nat × Nat × Char) → List (Char × (List (Nat × Nat)))
  | [] => []
  | ((x, y, c) :: xs) => [(c, (x, y) :: (List.map (λ (x, y, _) ↦ (x, y)) (List.takeWhile (λ (_, _, c1) ↦ c == c1) xs)))] ++ (groupItems (List.dropWhile (λ (_, _, c1) ↦ c == c1) xs))
decreasing_by
  simp
  simp[Nat.add_comm 1]
  simp[Nat.add_assoc (x + 1 + (y + 1 + (c.toNat + 3))) 1]
  simp[Nat.lt_add_left (x + 1 + (y + 1 + (c.toNat + 3))) (dropWhileL c xs)]

def List.pairs {α : Type} : List α → List (α × α)
  | [] => []
  | (_ :: []) => []
  | (x :: xs) => (List.map (λ y ↦ (x, y)) xs) ++ List.pairs xs

def divisorsBelowN : Int → Nat → List Int
  | _, 0 => []
  | _, 1 => [1]
  | a, Nat.succ n => divisorsBelowN a n ++ (if (Int.tmod a (Int.ofNat (Nat.succ n))) == 0 then [Int.ofNat (Nat.succ n)] else []) 
-- does x divide y?
def div (x y : Int) : Bool := if (x == 1) then true else ((Int.tmod y x) == 0) 

def abs : Int → Nat
  | x => if x > 0 then x.toNat else (-x).toNat

def minDiff : Int × Int → Int × Int
  | (0, _) => (0, 1)
  | (_, 0) => (1, 0)
  | (x, y) => let divisors := divisorsBelowN (min x y) (abs (min x y)); let div := (List.filter (λ d ↦ Bool.and (div d x) (div d y)) divisors).getLast! ; (x / div, y / div)

def List.negRange (n : Nat) : List Int := (List.map (Int.negSucc .) (List.range n)).reverse ++ (List.map (Int.ofNat .) (List.range n))

def genCoords : Int × Int → Int × Int → List (Int × Int)
  | (x1, y1), (x2, y2) => let diff := minDiff (x2-x1, y2-y1) ; List.map (λ m ↦ (x1 + m * diff.fst, y1 + m * diff.snd)) (List.negRange gridDims.fst)

def isValid : (Nat × Nat) → (Int × Int) → Bool
  | (maxx, maxy), (x, y) => Bool.not (Bool.or (Bool.or (x < 0) (y < 0)) (Bool.or (x ≥ (Int.ofNat maxx)) (y ≥ (Int.ofNat maxy))))

def pairToInt : Nat × Nat → Int × Int
  | (x, y) => (Int.ofNat x, Int.ofNat y)

def intToPair : Int × Int → Nat × Nat
  | (x, y) => (x.toNat, y.toNat)

def findCoords (xs : List (Nat × Nat)) : List (Nat × Nat) := List.map intToPair (List.map (λ (xy, ab) ↦ let ans := genCoords xy ab; List.filter (isValid gridDims .) ans) (List.pairs (List.map pairToInt xs))).flatten

def allPoints (xss : List (Char × List (Nat × Nat))) : (List (Nat × Nat)) := (List.map (λ (_, xs) ↦ findCoords xs) xss).flatten

def uniquePoints : List (Nat × Nat) → List (Nat × Nat)
  | [] => []
  | (x :: xs) => if xs.contains x then (uniquePoints xs) else x :: uniquePoints xs

def ordering : Nat × Nat → Nat × Nat → Bool
  | (x, _), (y, _) => x < y

def answer := (uniquePoints $ allPoints $ groupItems $ sortItems $ itemFilter $ items lines).length
