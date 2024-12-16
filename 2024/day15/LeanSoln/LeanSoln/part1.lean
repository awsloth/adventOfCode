import LeanSoln.data

def Grid : Type := List (List Char)

inductive Dir where
  | U | D | L | R

def Wall : Type := Nat × Nat
def Box : Type := Nat × Nat
def Robot : Type := Nat × Nat
def GameState : Type := (List Box) × Robot

def Robot.move : Robot → Dir → Robot
  | (x, y), Dir.U => (x, y - 1)
  | (x, y), Dir.D => (x, y + 1)
  | (x, y), Dir.L => (x - 1, y)
  | (x, y), Dir.R => (x + 1, y)

def Box.shift : Box → Dir → Box
  | (x, y), Dir.U => (x, y - 1)
  | (x, y), Dir.D => (x, y + 1)
  | (x, y), Dir.L => (x - 1, y)
  | (x, y), Dir.R => (x + 1, y)

def Dir.fromChar : Char → Dir
  | '^' => Dir.U
  | 'v' => Dir.D
  | '<' => Dir.L
  | '>' => Dir.R
  | _ => Dir.D

def Dir.toString : Dir → String
  | Dir.U => "^"
  | Dir.D => "v"
  | Dir.L => "<"
  | Dir.R => ">"

deriving instance BEq for Dir
deriving instance Inhabited, BEq, ToString for Box
deriving instance BEq for Wall
deriving instance ToString for Robot

instance : ToString (List Box) where
  toString bxs := String.join (List.map (λ (a, b) ↦ s!"({a}, {b}) ") bxs)

instance : ToString Dir where
  toString d := Dir.toString d

def GameState.toString : GameState → String
  | (xs, (x, y)) => (s!"[{x}, {y}] : ").append $ String.join (List.map (λ (a, b) ↦ s!"({a}, {b}) ") xs)

instance : ToString GameState where
  toString gs := GameState.toString gs

def grid (s : String) : Grid := List.map (λ line ↦ line.data) $ (s.splitOn "\n\n").head!.splitOn "\n"

def moves (s : String) : List Dir := List.map (Dir.fromChar) (List.filter (.≠'\n') ((s.splitOn "\n\n").tail!.head!.data))

def List.enumGrid {α : Type} (xs : List (List α)) : List (Nat × Nat × α) := (List.map (λ (y, ys) ↦ List.enum (List.zip (List.replicate ys.length y) ys)) (List.enum xs)).join

def stripLast {α β δ : Type} : α × β × δ → α × β
  | (a, b, _) => (a, b)

def items (g : Grid) : (List Wall) × GameState :=
  let gridCoords := (List.enumGrid g);
  let walls := List.filter (λ (_, _, c) ↦ c == '#') gridCoords;
  let boxes := List.filter (λ (_, _, c) ↦ c == 'O') gridCoords;
  let player := List.filter (λ (_, _, c) ↦ c == '@') gridCoords;
  (List.map stripLast walls, List.map stripLast boxes, stripLast player.head!)

def comp : Dir → Box → Box → Bool
  | Dir.U, (_, y1), (_, y2) => y2 < y1
  | Dir.D, (_, y1), (_, y2) => y1 < y2
  | Dir.L, (x1, _), (x2, _) => x2 < x1
  | Dir.R, (x1, _), (x2, _) => x1 < x2

def findBoxLine : Dir → GameState → List Box
  | Dir.U, (boxes, (px, py)) => (Array.qsort (List.filter (λ (x, y) ↦ Bool.and (x == px) (y < py)) boxes).toArray (comp Dir.U)).toList
  | Dir.D, (boxes, (px, py)) => (Array.qsort (List.filter (λ (x, y) ↦ Bool.and (x == px) (y > py)) boxes).toArray (comp Dir.D)).toList
  | Dir.L, (boxes, (px, py)) => (Array.qsort (List.filter (λ (x, y) ↦ Bool.and (x < px) (y == py)) boxes).toArray (comp Dir.L)).toList
  | Dir.R, (boxes, (px, py)) => (Array.qsort (List.filter (λ (x, y) ↦ Bool.and (x > px) (y == py)) boxes).toArray (comp Dir.R)).toList

def findContinuous : Dir → List Box → List Box
  | _, [] => []
  | _, (x :: []) => [x]
  | Dir.U, boxes => boxes.head! :: (List.map (λ x ↦ x.snd) $ List.takeWhile (λ ((_, y1), (_, y2)) ↦ y1 - 1 == y2) (List.zip boxes boxes.tail!))
  | Dir.D, boxes => boxes.head! :: (List.map (λ x ↦ x.snd) $ List.takeWhile (λ ((_, y1), (_, y2)) ↦ y1 + 1 == y2) (List.zip boxes boxes.tail!))
  | Dir.L, boxes => boxes.head! :: (List.map (λ x ↦ x.snd) $ List.takeWhile (λ ((x1, _), (x2, _)) ↦ x1 - 1 == x2) (List.zip boxes boxes.tail!))
  | Dir.R, boxes => boxes.head! :: (List.map (λ x ↦ x.snd) $ List.takeWhile (λ ((x1, _), (x2, _)) ↦ x1 + 1 == x2) (List.zip boxes boxes.tail!))

def nextContBoxes : Dir → GameState → List Box
  | d, gs => findContinuous d $ findBoxLine d gs

def adjacent : Dir → Robot → Box → Bool
  | Dir.U, (x, y), (a, b) => Bool.and (x == a) (y-1 == b)
  | Dir.D, (x, y), (a, b) => Bool.and (x == a) (y+1 == b)
  | Dir.L, (x, y), (a, b) => Bool.and (y == b) (x-1 == a)
  | Dir.R, (x, y), (a, b) => Bool.and (y == b) (x+1 == a)

def defaultMap : List Wall → List Char := List.foldl (λ grid ↦ (λ (a, b) ↦ grid.set (b*11 + a) '#')) (List.map (λ y ↦ y.data) (List.replicate 10 "..........\n")).join

def genMap : Dir → List Wall → GameState → List Char
  | d, walls, (boxes, (x, y)) => List.foldl (λ grid ↦ (λ (a, b) ↦ grid.set (b*11 + a) 'O')) ((defaultMap walls).set (y*11 + x) d.toString.data.head!) boxes

def doMoves : List Dir → GameState → List Wall → GameState
  | [], gamestate, _ => gamestate
  | (d :: xs), (boxes, robot), walls =>
                           let line := nextContBoxes d (boxes, robot)
                           if Bool.and (line.length > 0) (adjacent d robot line.head!) then
                                if walls.contains (line.getLast!.shift d)
                                then doMoves xs (boxes, robot) walls
                                else let newBoxes := boxes.replace (line.head!) (line.getLast!.shift d);
                                     doMoves xs (newBoxes, robot.move d) walls
                           else if walls.contains (robot.move d)
                                then doMoves xs (boxes, robot) walls
                                else doMoves xs (boxes, robot.move d) walls

def finalState (str : String) : GameState := doMoves (moves $ str) (items $ grid $ str).snd (items $ grid str).fst 

def List.sum : List Nat → Nat := List.foldl (.+.) 0

def calcGPS (boxes : List Box) : Nat := List.sum $ List.map (λ (x, y) ↦ 100*y + x) boxes

def answer (str : String) : Nat := calcGPS (finalState str).fst 
