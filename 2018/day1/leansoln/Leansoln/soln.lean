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

def any : List Bool → Bool
  | [] => false
  | (x :: xs) => if x then true else any xs

def map {α β : Type} : (α → β) → List α → List β
  | _, [] => []
  | f, (x :: xs) => f x :: map f xs

def range1 (n : Nat) : List Nat := map (λ x => x + 1) (range n)

def sumList : List Int := map (sumToN (listToInt (String.splitOn data "\n"))) (range 977)

def posHelper : Nat → Int → List Int → Int
  | _, _, [] => -1
  | z, y, (x :: xs) => if (x == y) then z else posHelper (Nat.succ z) y xs

def pos : Int → List Int → Int := posHelper 0 

def repeats : List Int → List Int
  | [] => []
  | (x :: xs) => if ((pos x xs) ≠ -1) then x :: repeats xs else repeats xs

def repeatList : Nat → List Int → List Int
  | 0, _ => []
  | (Nat.succ n), xs => xs ++ (repeatList n xs)

def intList : List Int := (listToInt (String.splitOn data "\n"))

