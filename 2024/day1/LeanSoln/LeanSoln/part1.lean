import LeanSoln.data

namespace part1
def splitToProd (x : String) : Nat × Nat := let strs := x.splitOn "   " ;
                                            (strs.head!.toNat!, (strs.get! 1).toNat!)

def listPairToPairList {α : Type} : List (α × α) → List α × List α
  | [] => ([], [])
  | ((a, b) :: xs) => let rest := listPairToPairList xs ; (a :: rest.fst, b :: rest.snd)

def pairListToListPair {α : Type} : List α × List α → List (α × α)
  | ([] , []) => []
  | ((_ :: _), []) => []
  | ([], (_ :: _)) => []
  | ((x :: xs), (y :: ys)) => (x , y) :: pairListToListPair (xs, ys)

def pairLists (str : String) : List Nat × List Nat := listPairToPairList $ List.map splitToProd (str.splitOn "\n")

def sortListPair (xs : List Nat × List Nat) : List Nat × List Nat := ((Array.qsort xs.fst.toArray (.<.)).toList, (Array.qsort xs.snd.toArray (.<.)).toList)

def sumDiffs : List (Prod Nat Nat) → Nat
  | [] => 0
  | ((x , y) :: xs) => if y > x then (y - x) + sumDiffs xs
                       else (x - y) + sumDiffs xs

def answer : Nat := sumDiffs $ pairListToListPair $ sortListPair $ pairLists data
end part1
