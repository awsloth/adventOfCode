import LeanSoln.data

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

def abs (x : Int) : Int := if x < 0 then -x else x

def sumDiffs : List (Prod Int Int) → Int
  | [] => 0
  | ((x , y) :: xs) => abs (y - x) + sumDiffs xs

#eval sumDiffs (pairListToListPair sortedLists)
