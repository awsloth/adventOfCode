import LeanSoln.data

def Path : Type := Nat × Nat

inductive Dir where
  | U | D | L | R

deriving instance BEq for Path
deriving instance Inhabited for Path
deriving instance ToString for Path
deriving instance BEq for Dir

def Path.neighbours : Path → Dir → List Path → List Path
  | (x, y), d, points => (if (points.contains (x-1, y)) ∧ (Bool.not (d == Dir.R)) then [(x-1, y)] else []) ++
                         (if (points.contains (x+1, y)) ∧ (Bool.not (d == Dir.L)) then [(x+1, y)] else []) ++
                         (if (points.contains (x, y-1)) ∧ (Bool.not (d == Dir.D)) then [(x, y-1)] else []) ++
                         (if (points.contains (x, y+1)) ∧ (Bool.not (d == Dir.U)) then [(x, y+1)] else [])

def Path.doubleNeighbours : Path → Dir → List Path → List Path
  | (x, y), d, points => (if (points.contains (x-2, y)) ∧ (Bool.not (d == Dir.L)) then [(x-2, y)] else []) ++
                         (if (points.contains (x+2, y)) ∧ (Bool.not (d == Dir.R)) then [(x+2, y)] else []) ++
                         (if (points.contains (x, y-2)) ∧ (Bool.not (d == Dir.U)) then [(x, y-2)] else []) ++
                         (if (points.contains (x, y+2)) ∧ (Bool.not (d == Dir.D)) then [(x, y+2)] else [])

def Path.dirBetween : Path → Path → Dir
  | (x, y), (a, b) => if a < x then Dir.L
                      else if a > x then Dir.R
                      else if y < b then Dir.D
                      else Dir.U

def newDir : Dir → Path → Path → Dir
  | Dir.U, (sx, _), (nx, _) => if nx < sx then Dir.L
                                 else if nx > sx then Dir.R
                                 else Dir.U
  | Dir.D, (sx, _), (nx, _) => if nx < sx then Dir.L
                                 else if nx > sx then Dir.R
                                 else Dir.D
  | Dir.L, (_, sy), (_, ny) => if ny < sy then Dir.U
                                 else if ny > sy then Dir.D
                                 else Dir.L
  | Dir.R, (_, sy), (_, ny) => if ny < sy then Dir.U
                                 else if ny > sy then Dir.D
                                 else Dir.R

def gridToSpaces (str : String) : Path × List Path :=
  let grid := List.map String.data $ str.splitOn "\n";
  let coords := List.map (λ (y, line) ↦ List.map (λ (x, c) ↦ (x, y, c)) (List.enum line)) (List.enum grid)
  let spaces := List.filter (λ (_, _, c) ↦ ".ES".contains c) coords.join
  let start := List.filter (λ (_, _, c) ↦ c = 'S') coords.join
  ((start.head!.fst, start.head!.snd.fst), List.map (λ (x, y, _) ↦ (x, y)) spaces)

def corePath (steps : List Path) : Path → Dir → List Path
  | curp, d => let moves := curp.neighbours d steps;
               if moves.length == 0 then []
               else if moves.length > 1 then [(9999999, 9999999)]
               else let new_dir := newDir d curp moves.head!;
               moves.head! :: (corePath (steps.erase moves.head!) moves.head! new_dir)
termination_by steps.length
decreasing_by
  sorry

def pathForStr (str : String) : List Path := let (start, grid) := gridToSpaces str;
                                             start :: (corePath grid start Dir.D)

def determineCheats : List Path → List (Path × Path)
  | (x :: (y :: xs)) => let poss := x.doubleNeighbours (x.dirBetween y) xs;
                        (List.zip (List.replicate poss.length x) poss) ++ determineCheats (y :: xs)
  | _ => []

def cheatSaves (corepath : List Path) : List (Path × Path) → List Nat := List.map (λ (x, y) ↦ (corepath.findIdx (.==y)) - (corepath.findIdx (.==x)))

def timeSavesOverN (core : List Path) (n : Nat) : Nat := (List.filter (n+2≤.) $ cheatSaves core (determineCheats core)).length

-- #eval! timeSavesOverN (pathForStr testData) 100
