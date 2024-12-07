import LeanSoln.data
import Mathlib.Order.Defs.PartialOrder

def insert : Int → List Int → List Int
  | x , [] => [x]
  | x , (y :: ys) => if (x < y) then x :: (y :: ys) else y :: (insert x ys)

def listSort : List Int → List Int
  | [] => []
  | (x :: xs) => insert x (listSort xs)

def splitToProd (x : String) : Prod String String := let strs := x.splitOn "   " ; (List.head! strs, List.head! (List.tail! strs))

def dataPairs : List (Prod String String) := List.map (splitToProd) (data.splitOn "\n")

def listPairToPairList : List (Prod String String) → Prod (List String) (List String)
  | [] => ([], [])
  | ((a, b) :: xs) => let rest := listPairToPairList xs ; (a :: rest.fst, b :: rest.snd)

def pairListToListPair : Prod (List Int) (List Int) → List (Prod Int Int)
  | ([] , []) => []
  | ((_ :: _), []) => []
  | ([], (_ :: _)) => []
  | ((x :: xs), (y :: ys)) => (x , y) :: pairListToListPair (xs, ys)

def dataList : Prod (List String) (List String) := listPairToPairList dataPairs

def intLists : Prod (List Int) (List Int) := let xs := dataList ; (List.map (fun s => s.toInt!) xs.fst, List.map (fun s => s.toInt!) xs.snd)

def sortedLists : Prod (List Int) (List Int) := let xs := intLists ; (listSort xs.fst, listSort xs.snd)

-- Fist int is the number being counted, second is count, list int is list, ...
def countHelper : Int → Int → List Int → (Prod Int Int) × (List Int)
  | num, count, [] => ((num, count), [])
  | num, count, (x :: xs) => if (x == num) then (countHelper num (count + 1) xs) else ((num, count), (x :: xs))

theorem countHelp (n : Int) (x : Int) (xs : List Int) : sizeOf (countHelper x n xs).snd <  1 + sizeOf x + sizeOf xs := by
  match xs with
    | [] => simp[countHelper]
            simp[Nat.add_comm 1 (sizeOf x)]
    | (y :: ys) => unfold countHelper
                   split
                   case isTrue => simp[Nat.add_comm 1 (sizeOf y)]
                                  simp[Nat.add_assoc 1]
                                  simp[← Nat.add_assoc (sizeOf x) (sizeOf y + 1) (sizeOf ys)]
                                  simp[Nat.add_comm (sizeOf x)]
                                  simp[Nat.add_assoc]
                                  simp[← Nat.add_assoc]
                                  simp[Nat.add_assoc ((1 + sizeOf y) + 1) (sizeOf x)]
                                  simp[Nat.add_assoc (1 + sizeOf y)]
                                  simp[← Nat.add_assoc 1]
                                  simp[Nat.lt_add_left (1 + sizeOf y) (countHelp (n+1) x ys)]
                   case isFalse => simp[Nat.add_comm 1]

-- Prod Int Int is (number, count)
def toCount : List Int → List (Prod Int Int)
  | [] => []
  | (x :: xs) => let help := (countHelper x 1 xs) ; help.fst :: (toCount help.snd)
decreasing_by
  simp[countHelp]

def listCounts : Prod (List (Prod Int Int)) (List (Prod Int Int)) := let xs := sortedLists ; (toCount xs.fst, toCount xs.snd)

def soln : Prod (List (Prod Int Int)) (List (Prod Int Int)) → Int
  | ([] , []) => 0
  | ([] , _ ) => 0
  | (_  , []) => 0
  | (((x, xcount) :: xs), ((y, ycount) :: ys)) => if (x == y) then (soln (xs, ys)) + (x * xcount * ycount) else (if (x > y) then (soln (((x, xcount) :: xs), ys)) else (soln (xs, ((y, ycount) :: ys))))


#eval soln listCounts
