import Leansoln.data

def sum : List Int → Int
  | [] => 0
  | (x :: xs) => x + sum xs

def sumToN (xs : List Int) (n : Nat) : Int :=
  match xs with
  | [] => 0
  | (x :: xs) => if (n==0) then 0 else (if (n == 1) then x else x + sumToN xs (n-1))

def signedToInt (s : String) : Int :=
  match String.data s with
  | [] => 0
  | (x :: xs) => if (x == '+') then String.toInt! (String.mk xs) else -String.toInt! (String.mk xs)

def listToInt : List String → List Int
  | [] => []
  | (x :: xs) => (signedToInt x) :: listToInt xs 

def range : Nat → List Nat
  | 0 => []
  | (Nat.succ n) => (range n) ++ [n]

def map {α β : Type} : (α → β) → List α → List β
  | _, [] => []
  | f, (x :: xs) => f x :: map f xs

def zip {α β : Type} : List α → List β → List (α × β)
  | (x :: xs), (y :: ys) => (x, y) :: zip xs ys 
  | _, _ => []

def intList : List Int := (listToInt (String.splitOn data "\n"))

def sumList : List Int := map (sumToN intList) (range (List.length intList))

def hasDiff : Int → Int → List Int → List Int
  | _, _, [] => []
  | n, d, (x :: xs) => if ((Int.tmod (n - x) d) == 0) then x :: hasDiff n d xs else hasDiff n d xs

def allDiffs : Int → List Int → List (Int × Int)
  | _, [] => []
  | d, (x :: xs) => (map (λ y => (x, y)) (hasDiff x d xs)) ++ (allDiffs d xs)

structure Triple where
  fst : Int
  snd : Int
  thd : Int

def α : Type := Triple

def sortHelper : List α → (α × α) → List α → List α → (α → Int) → List α
  | [], xy, [], sorted, f => (if (f xy.fst ≤ f xy.snd) then [xy.fst, xy.snd] else [xy.snd, xy.fst]) ++ sorted
  | (x :: []), xy, [], sorted, f => let ans :=(if (f xy.fst ≤ f xy.snd) then xy else (xy.snd, xy.fst)); sortHelper [] (x, ans.fst) [] (ans.snd :: sorted) f
  | (x :: (y :: xs)), xy, [], sorted, f => let ans :=(if (f xy.fst ≤ f xy.snd) then xy else (xy.snd, xy.fst)); sortHelper [] (x, y) (xs ++ [ans.fst]) (ans.snd :: sorted) f
  | s, xy, (e :: es), sorted, f => let ans := (if (f xy.fst ≤ f xy.snd) then xy else (xy.snd, xy.fst)); sortHelper (s ++ [ans.fst]) (ans.snd, e) es sorted f

-- if (f x < f x1) then x :: (sort (x1 :: xs) f) else x1 :: (sort (x :: xs) f)

def sort : List α → (α → Int) → List α
  | [], _ => []
  | (x :: []), _ => [x]
  | (x :: (x1 :: [])), f => if (f x ≤ f x1) then [x, x1] else [x1, x]
  | (x :: (y :: xs)), f => sortHelper [] (x, y) xs [] f

def abs (n : Int) : Int :=
  if (n < 0) then -n else n

-- Close but can't be bothered with the last bit, involves rephrasing all functions :(

