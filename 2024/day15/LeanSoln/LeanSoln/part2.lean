import LeanSoln.data

set_option debug.skipKernelTC true

def Grid : Type := List (List Char)

inductive Dir where
  | U | D | L | R

def Wall : Type := Nat × Nat
def Box : Type := (Nat × Nat) × (Nat × Nat)
def Robot : Type := Nat × Nat
def GameState : Type := (List Box) × Robot

def Robot.move : Robot → Dir → Robot
  | (x, y), Dir.U => (x, y - 1)
  | (x, y), Dir.D => (x, y + 1)
  | (x, y), Dir.L => (x - 1, y)
  | (x, y), Dir.R => (x + 1, y)

def Box.shift : Box → Dir → Box
  | ((x, y), (a, b)), Dir.U => ((x, y - 1), (a, b - 1))
  | ((x, y), (a, b)), Dir.D => ((x, y + 1), (a, b + 1))
  | ((x, y), (a, b)), Dir.L => ((x - 1, y), (a - 1, b))
  | ((x, y), (a, b)), Dir.R => ((x + 1, y), (a + 1, b))

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
  | (xs, (x, y)) => (s!"[{x}, {y}] : ").append $ String.join (List.map (λ ((a, b), (x, y)) ↦ s!"({a}, {b} ↔ {x}, {y}) ") xs)

instance : ToString GameState where
  toString gs := GameState.toString gs

def grid (s : String) : Grid := List.map (λ line ↦ line.data) $ (s.splitOn "\n\n").head!.splitOn "\n"

def moves (s : String) : List Dir := List.map (Dir.fromChar) (List.filter (.≠'\n') ((s.splitOn "\n\n").tail!.head!.data))

def List.enumGrid {α : Type} (xs : List (List α)) : List (Nat × Nat × α) := (List.map (λ (y, ys) ↦ List.enum (List.zip (List.replicate ys.length y) ys)) (List.enum xs)).join

def stripLast {α β δ : Type} : α × β × δ → α × β
  | (a, b, _) => (a, b)

def mapToWide : Nat × Nat → List (Nat × Nat)
  | (x, y) => [(x*2, y), (x*2 + 1, y)]

def mapToWidePair : Nat × Nat → (Nat × Nat) × (Nat × Nat)
  | (x, y) => ((x*2, y), (x*2 + 1, y))

def List.unpair {α : Type} : List (α × α) → List α := List.foldl (λ xs ↦ (λ (a, b) ↦ xs ++ [a, b])) []

def items (g : Grid) : (List Wall) × GameState :=
  let gridCoords := (List.enumGrid g);
  let walls := List.filter (λ (_, _, c) ↦ c == '#') gridCoords;
  let boxes := List.filter (λ (_, _, c) ↦ c == 'O') gridCoords;
  let player := List.filter (λ (_, _, c) ↦ c == '@') gridCoords;
  ((List.map (mapToWide ∘ stripLast) walls).join, List.map (mapToWidePair ∘ stripLast) boxes, (mapToWide $ stripLast player.head!).head!)

def comp : Dir → Box → Box → Bool
  | Dir.U, ((_, y1), _), ((_, y2), _) => y2 < y1
  | Dir.D, ((_, y1), _), ((_, y2), _) => y1 < y2
  | Dir.L, ((x1, _), _), ((x2, _), _) => x2 < x1
  | Dir.R, ((x1, _), _), ((x2, _), _) => x1 < x2

def findBoxLine : Dir → GameState → List Box
  | Dir.U, (boxes, (px, py)) => (Array.qsort (List.filter (λ ((x, y), (a, b)) ↦ Bool.or (Bool.and (x == px) (y < py)) (Bool.and (a == px) (b < py))) boxes).toArray (comp Dir.U)).toList
  | Dir.D, (boxes, (px, py)) => (Array.qsort (List.filter (λ ((x, y), (a, b)) ↦ Bool.or (Bool.and (x == px) (y > py)) (Bool.and (a == px) (b > py))) boxes).toArray (comp Dir.D)).toList
  | Dir.L, (boxes, (px, py)) => (Array.qsort (List.filter (λ ((x, y), (a, b)) ↦ Bool.or (Bool.and (y == py) (x < px)) (Bool.and (b == py) (a < px))) boxes).toArray (comp Dir.L)).toList
  | Dir.R, (boxes, (px, py)) => (Array.qsort (List.filter (λ ((x, y), (a, b)) ↦ Bool.or (Bool.and (y == py) (x > px)) (Bool.and (b == py) (a > px))) boxes).toArray (comp Dir.R)).toList

def isNext : Dir → Box × Box → Bool
  | Dir.U, (((px1, py1), (px2, _)), ((nx1, _), (nx2, ny2))) => Bool.and (py1 - 1 == ny2) (Bool.or (px1 == nx2) (Bool.or (px1 == nx1) (px2 == nx1)))
  | Dir.D, (((px1, py1), (px2, _)), ((nx1, _), (nx2, ny2))) => Bool.and (py1 + 1 == ny2) (Bool.or (px1 == nx2) (Bool.or (px1 == nx1) (px2 == nx1)))
  | Dir.L, (((px1, py1), (_, _)), ((_, _), (nx2, ny2))) => Bool.and (px1 - 1 == nx2) (py1 == ny2) 
  | Dir.R, (((_, py1), (px2, _)), ((nx1, _), (_, ny2))) => Bool.and (px2 + 1 == nx1) (py1 == ny2)


def findContinuous : Dir → List Box → List Box
  | _, [] => []
  | _, (x :: []) => [x]
  | d, boxes => boxes.head! :: (List.map (λ x ↦ x.snd) $ List.takeWhile (isNext d) (List.zip boxes boxes.tail!))

def nextContBoxes : Dir → GameState → List Box
  | d, gs => findContinuous d $ findBoxLine d gs

def adjacent : Dir → Robot → Box → Bool
  | Dir.U, (x, y), ((a1, b1), (a2, b2)) => Bool.or (Bool.and (x == a1) (y-1 == b1)) (Bool.and (x == a2) (y-1 == b2))
  | Dir.D, (x, y), ((a1, b1), (a2, b2)) => Bool.or (Bool.and (x == a1) (y+1 == b1)) (Bool.and (x == a2) (y+1 == b2))
  | Dir.L, (x, y), ((a1, b1), (a2, b2)) => Bool.or (Bool.and (y == b1) (x-1 == a1)) (Bool.and (y == b2) (x-1 == a2))
  | Dir.R, (x, y), ((a1, b1), (a2, b2)) => Bool.or (Bool.and (y == b1) (x+1 == a1)) (Bool.and (y == b2) (x+1 == a2))


def defaultMap : List Wall → List Char := List.foldl (λ grid ↦ (λ (a, b) ↦ grid.set (b*21 + a) '#')) (List.map (λ y ↦ y.data) (List.replicate 10 "....................\n")).join

def genMap : Dir → List Wall → GameState → String
  | d, walls, (boxes, (x, y)) => (List.foldl (λ grid ↦ (λ ((a, b), (x, y)) ↦ (grid.set (b*21 + a) '[').set (y*21 + x) ']')) ((defaultMap walls).set (y*21 + x) d.toString.data.head!) boxes).asString

def remapChunk : Dir → List Box → List Box → List Box
  | _, [], inter => inter
  | d, (x :: xs), inter => remapChunk d xs (inter.replace x (x.shift d))

-- direction, to search, boxes, pushedboxes
def findAllBlocks : Dir → List Box → List Box → List Box → List Box
  | d, [], _, _ => []
  | d, (x :: xs), tested, boxes => if (tested.contains x) then (findAllBlocks d xs tested boxes)
                                   else
                                   let nextl := nextContBoxes d (boxes, x.fst);
                                   let nextr := nextContBoxes d (boxes, x.snd);
                                   if Bool.and (nextl.length > 0) (adjacent d x.fst nextl.head!)
                                   then if Bool.and (nextr.length > 0) (adjacent d x.snd nextr.head!)
                                    then x :: findAllBlocks d (nextr.head! :: (nextl.head! :: xs)) (x :: tested) boxes
                                    else x :: findAllBlocks d (nextl.head! :: xs) (x :: tested) boxes
                                   else if Bool.and (nextr.length > 0) (adjacent d x.snd nextr.head!)
                                    then x :: findAllBlocks d (nextr.head! :: xs) (x :: tested) boxes
                                    else x :: findAllBlocks d xs (x :: tested) boxes

def doMoves : List Dir → GameState → List Wall → GameState
  | [], gamestate, _ => gamestate
  | (d :: xs), (boxes, robot), walls =>
                           let line := nextContBoxes d (boxes, robot)
                           if Bool.and (line.length > 0) (adjacent d robot line.head!) then
                                let pushedBlocks := findAllBlocks d line [] boxes; -- TO DO
                                if List.any (List.map (λ b ↦ b.shift d) pushedBlocks) (λ (l, r) ↦ Bool.or (walls.contains l) (walls.contains r))
                                then doMoves xs (boxes, robot) walls
                                else let newBoxes := remapChunk d pushedBlocks boxes;
                                     doMoves xs (newBoxes, robot.move d) walls
                           else if walls.contains (robot.move d)
                                then doMoves xs (boxes, robot) walls
                                else doMoves xs (boxes, robot.move d) walls

def finalState (str : String) : GameState := doMoves (moves $ str) (items $ grid $ str).snd (items $ grid str).fst 

def List.sum : List Nat → Nat := List.foldl (.+.) 0

def calcGPS (boxes : List Box) : Nat := List.sum $ List.map (λ ((x, y), _) ↦ 100*y + x) boxes

def answer (str : String) : Nat := calcGPS (finalState str).fst

#eval! answer data
