import LeanSoln.data

def lines : List String := String.splitOn data "\n"

structure Claim where
  tag : String
  x : Nat
  y : Nat
  width : Nat
  height : Nat
deriving Repr

structure Line where
  y : Nat
  startx : Nat
  endx : Nat
deriving Repr

def map {α β : Type} : (α → β) → List α → List β
  | _, [] => []
  | f, (x :: xs) => (f x) :: (map f xs)

def dummyClaim : Claim := { tag := "oops", x := 0, y := 0, width := 0, height := 0}

def tagToNat (s : String) : Nat :=
  match (String.data s) with
  | [] => 0
  | (_ :: xs) => (xs.toString).toNat!

def splitInfo (s : String) : Claim :=
  match (String.splitOn s " @ ") with
  | (x :: (y :: [])) => match (String.splitOn y ": ") with
                        | (a :: (b :: [])) => match (String.splitOn a ",") with
                                              | (a1 :: (a2 :: [])) => match (String.splitOn b "x") with
                                                                      | (b1 :: (b2 :: [])) => { tag := x, x := a1.toNat!, y := a2.toNat!, width := b1.toNat!, height := b2.toNat!}
                                                                      | _ => dummyClaim
                                              | _ => dummyClaim
                        | _ => dummyClaim
  | _ => dummyClaim

-- Idea
-- list of lines
-- each block converted into strips of x lines
-- add intersection of lines, then morph to form one line
-- running total

def range : Nat → Nat → List Nat
  | s, 0 => [s]
  | s, (Nat.succ e) => (range s e) ++ [e]

def claimToLines : Claim → List Line
  | { tag := _, x := x, y := y, width := wid, height := hi } => map (λ yp => { y := yp, startx := x, endx := x + wid - 1 }) (range y (y + hi))
  -- Worth noting that startx and endx is inclusive, i.e. the line sits in these positions.

#eval map claimToLines (map splitInfo lines)

