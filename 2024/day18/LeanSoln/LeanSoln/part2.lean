import LeanSoln.data

def Wall : Type := Nat × Nat

deriving instance Inhabited for Wall
deriving instance ToString for Wall

def getWalls (str : String) : List Wall := List.map (λ line ↦ let xy := line.splitOn ",";
                                                           (xy.head!.toNat!, xy.tail!.head!.toNat!))
                                                 (str.splitOn "\n")

def heurCost : Nat × Nat → Nat × Nat → Nat
  | (x, y), (a, b) => a-x + b-y

def compLast {α : Type} : α × Nat → α × Nat → Bool
  | (_, x), (_, y) => x < y

def largeValue : Nat := 999999999999999999

def neighbours : Nat × Nat → Nat × Nat → List (Nat × Nat)
  | (0, 0), _ => [(1, 0), (0, 1)]
  | (0, y), (_, my) => if y < my then [(1, y), (0, y-1), (0, y+1)] else [(1, y), (0, y-1)]
  | (x, 0), (mx, _) => if x < mx then [(x+1, 0), (x-1, 0), (x, 1)] else [(x-1, 0), (x, 1)]
  | (x, y), (mx, my) => (if y < my then [(x, y+1)] else []) ++ (if x < mx then [(x+1, y)] else []) ++ [(x-1, y), (x, y-1)]

def setCost : List (List ((Nat × Nat) × Nat × Bool)) → (Nat × Nat) → ((Nat × Nat) × Nat) → List (List ((Nat × Nat) × Nat × Bool))
  | grid, (x, y), ((nx, ny), ncost) => let init_val := (grid.get! y).get! x;
                                                let new_val := ((nx, ny), ncost, init_val.snd.snd);
                                                let new_line := (grid.get! y).set x new_val;
                                                grid.set y new_line



def findEndPath (grid : List (List ((Nat × Nat) × Nat × Bool))) : Nat → Nat × Nat → List (Nat × Nat)
  | 0, (x, y) => [(x, y)]
  | (n + 1), (x, y) => let prev := ((grid.get! y).get! x).fst;
              if prev == (x, y) then [(x, y)]
              else findEndPath grid n prev ++ [(x, y)]

-- for each node, we have a came from, current path cost, isWall
def aStar (grid : List (List ((Nat × Nat) × Nat × Bool))) : Nat → List (Nat × Nat) → Nat × Nat → List (Nat × Nat)
  | _, [], _ => [(largeValue, largeValue)]
  | 0, _, _ => [(largeValue, largeValue)]
  | (n+1), next, endp => let scores := List.map (λ (x, y) ↦ ((grid.get! y).get! x).snd.fst + heurCost (x, y) endp) next;
                         let order := List.map (λ (x, _) ↦ x) (Array.qsort (List.zip next scores).toArray compLast).toList;
                         let lowest := order.head!
                         let lowestcost := ((grid.get! lowest.snd).get! lowest.fst).snd.fst;
                         if lowest == endp then findEndPath grid ((endp.fst + 1)*(endp.snd+1)) lowest
                         else
                         let newNodes := List.filter (λ (x, y) ↦ let (_, cost, wall) := ((grid.get! y).get! x); Bool.and (cost == largeValue) (Bool.not wall)) (neighbours lowest endp);
                         let newGrid := List.foldl (setCost . . (lowest, lowestcost+1)) grid newNodes ;
                         let nodes := List.foldl (λ search ↦ (λ new ↦ if search.contains new then search else new :: search)) order.tail! newNodes;
                         aStar newGrid n nodes endp

def setWall : List (List ((Nat × Nat) × Nat × Bool)) → Wall → List (List ((Nat × Nat) × Nat × Bool))
  | grid, (x, y) => let init_val := (grid.get! y).get! x;
                    let new_val := (init_val.fst, init_val.snd.fst, true);
                    let new_line := (grid.get! y).set x new_val;
                    grid.set y new_line

def startingGrid : Nat × Nat → Nat × Nat → List Wall → List (List ((Nat × Nat) × Nat × Bool))
  | (sx, sy), (ex, ey), walls => let startGrid := List.replicate (ey + 1) (List.replicate (ex + 1) ((sx, sy), largeValue, false));
                                 let wallsGrid := List.foldl setWall startGrid walls;
                                 setCost wallsGrid (sx, sy) ((sx, sy), 0)

def findPath : Nat × Nat → Nat × Nat → List Wall → (List (Nat × Nat))
  | (sx, sy), (ex, ey), walls => aStar (startingGrid (sx, sy) (ex, ey) walls) ((ex + 1) * (ey + 1)) [(sx, sy)] (ex, ey)

def findPathN (n : Nat) (endp : Nat × Nat) : List (Nat × Nat) := (findPath (0, 0) endp $ List.take n (getWalls data))

def recurFind (n : Nat) (walls : List Wall) (endp : Nat × Nat) : Nat :=
  if (n ≤ walls.length)
  then let cur_path := (findPathN n endp);
            if cur_path.getLast! == endp then 
            let nextN := (List.drop n walls).length - (List.dropWhile (λ xy ↦ Bool.not (cur_path.contains xy)) (List.drop n walls)).length;
            recurFind (n + nextN + 1) walls endp
            else n
  else walls.length
termination_by walls.length + 1 - n

def answer : Wall := (getWalls data).get! ((recurFind 1024 (getWalls data) (70, 70)) - 1)
