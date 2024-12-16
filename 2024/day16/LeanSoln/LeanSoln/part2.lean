import LeanSoln.data

def Node : Type := (Nat × Nat)
def Graph : Type := List (Node × (List (Node × Nat)))

def Node.x : Node → Nat
  | (x, _) => x

def Node.y : Node → Nat
  | (_, y) => y

deriving instance BEq, Inhabited for Node

def Node.adjacent : Node → Graph → List (Node × Nat)
  | _, [] => []
  | node, ((x, adj) :: xs) => if x == node then adj else node.adjacent xs

def coordAdjacent : Nat × Nat → List (Nat × Nat) → List (Nat × Nat)
  | (x, y), xs => List.filter (λ ab ↦ Bool.or (Bool.or ((x - 1, y) == ab) ((x + 1, y) == ab)) (Bool.or ((x, y -1)== ab) ((x, y + 1) == ab))) xs

def grid (str : String) : List (Nat × Nat × Char) := List.join $ List.map (λ (y, line) ↦ List.map (λ (x, c) ↦ (x, y, c)) (List.enum line)) (List.enum (List.map (λ s ↦ s.data) (str.splitOn "\n")))

def stripLast {α β δ : Type} : α × β × δ → α × β
  | (a, b, _) => (a, b)

def clearSpaces (str : String) : List (Nat × Nat) := List.map stripLast $ List.filter (λ (_, _, c) ↦ c == '.') $ grid str

def startPos (str : String) : (Nat × Nat) := stripLast $ (List.filter (λ (_, _, c) ↦ c == 'S') $ grid str).head!

def endPos (str : String) : (Nat × Nat) := stripLast $ (List.filter (λ (_, _, c) ↦ c == 'E') $ grid str).head!

def formGraph (points : List (Nat × Nat)) : Graph := List.map
                                            (λ p ↦ let adj := (coordAdjacent p points);
                                                  (p, List.zip adj (List.replicate adj.length 1))) points


def findAligned : List (Node × Nat) → List (Node × Nat)
  | [] => []
  | (((x, y), w) :: xs) => let aligned := List.filter (λ ((a, b), _) ↦ Bool.or (x==a) (b==y)) xs;
                           if aligned.length == 1
                           then ((x, y), w) :: aligned
                           else xs

def dummy : Nat := 100000

def changeIntersections : Graph → Graph → Graph
  | [], inter => inter
  | ((x, cons) :: xs), inter =>
  match cons.length with
  | 0 => (changeIntersections xs inter)
  | 1 => (changeIntersections xs inter)
  | 2 => if Bool.or (cons.head!.fst.x == cons.getLast!.fst.x)
                    (cons.head!.fst.y == cons.getLast!.fst.y)
         then (changeIntersections xs inter)
         else let changedWeight := List.map (λ (npos, ncons) ↦
              if npos == cons.head!.fst
              then (npos,
                    List.map (λ (con, weight) ↦ if (con == x)
                                                then (con, 1001)
                                                else (con, weight)) ncons)
              else if npos == x
              then (npos, [(cons.head!.fst, 1001), cons.getLast!])
              else (npos, ncons)) inter;
              (changeIntersections xs changedWeight)
  | _ => let newpoint := (x.fst+dummy, x.snd+dummy)
         let aligned := findAligned cons;
         let notaligned := List.filter (λ x ↦ Bool.not (aligned.contains x)) cons;
         let changedPoints := List.map (λ (node, ncons) ↦ 
                                        if Bool.or (notaligned.contains (node, 1))
                                                   (notaligned.contains (node, 1001))
                                        then (node, List.map (λ (nx, nw) ↦
                                                                if nx == x then (newpoint, nw)
                                                                           else (nx, nw)) ncons)
                                        else if Bool.or (aligned.contains (node, 1))
                                                        (aligned.contains (node, 1001))
                                        then (node, (newpoint, 1001) :: ncons)
                                        else if node == x
                                        then (node, aligned)
                                        else (node, ncons)) inter;
         (changeIntersections xs ((newpoint, (notaligned ++ (List.map (λ (xy, _) ↦ (xy, 1001)) aligned))) :: changedPoints))

def graphModel (str : String) : Graph := let startGraph := (formGraph (clearSpaces str));
                                        changeIntersections startGraph startGraph

def fstItem {α β : Type} : α × β → α
  | (a, _) => a

def addEnd (g : Graph) (e : Node) := (e, [((e.fst - 1, e.snd), 1), ((e.fst, e.snd+1), 1)]) :: 
                                     List.map (λ (n, cons) ↦ if Bool.or (n == (e.fst - 1, e.snd))
                                                                        (n == (e.fst, e.snd + 1))
                                                             then (n, (e, 1) :: cons)
                                                             else (n, cons)) g

def findConnections : Graph → (Node × Nat) → List (Node × Nat)
  | [], _ => []
  | ((y, cons) :: ys), (x, _) => if (x == y) then cons else findConnections ys (x, 0)

def uniqueIze : List (Node × Nat) → List (Node × Nat)
  | [] => []
  | ((n, cost) :: xs) => if (List.filter (λ (m, _) ↦ m == n) xs).length > 0
                         then (List.map (λ (m, mcost) ↦ if m == n then (m, (Nat.min cost mcost)) else (m, mcost)) xs)
                         else (n, cost) :: (uniqueIze xs)

-- Graph, visited and cost, currentWeights
def stepDijkstras : Graph → List (Node × Nat) × List (Node × Nat) → List (Node × Nat) × List (Node × Nat)
  | _, (visited, []) => (visited, [])
  | g, (visited, current) => let smallest := List.foldl (λ smallest ↦ (λ next ↦ if smallest.snd < next.snd then smallest else next)) current.head! current.tail!;
                             let new := List.map (λ (n, cost) ↦ (n, smallest.snd+cost)) $ List.filter (λ y ↦ Bool.not $ (List.map fstItem visited).contains y.fst) (findConnections g smallest);
                             let updatedCurrent := uniqueIze (new ++ List.filter (λ y ↦ Bool.not (smallest == y)) current);
                             (smallest :: visited, updatedCurrent)

def doNSteps : Nat → Graph → List (Node × Nat) × List (Node × Nat) → List (Node × Nat) × List (Node × Nat)
  | 0, _, ls => ls
  | (n+1), g, ls => doNSteps n g (stepDijkstras g ls)

def finishedGraph (str : String) : Graph := addEnd (graphModel str) (endPos str)

def ansAfterN (n : Nat) (str : String) : List (Node × Nat) × List (Node × Nat) :=
  let start := startPos str;
  doNSteps n (finishedGraph str) ([(start, 0)], [((start.fst, start.snd - 1), 1001), ((start.fst+1, start.snd), 1)])

def solvedDijkstras (str : String) : List (Node × Nat) := (ansAfterN 11500 str).fst

def lookup : Node → List (Node × Nat) → Nat
  | _, [] => dummy
  | x, ((y, cost) :: ys) => if x == y then cost else (lookup x ys)

def getNext : Graph → List (Node × Nat) → Node → List (Nat × Nat)
  | g, xs, start => List.map (fstItem) $ List.filter (λ (next, dist) ↦ ((lookup start xs) - dist) == (lookup next xs)) (findConnections g (start, 0))

def paths : Nat → Node → Graph → List (Node × Nat) → List (List Node) → List (List Node)
  | 0, _, _, _, routes => routes
  | (n + 1), start, g, xs, routes => paths n start g xs
                              (List.map (λ route ↦ if Bool.or ((List.getLast! route) == (start.x + 1, start.y))
                                                              ((List.getLast! route) == (start.x, start.y-1))
                                                   then [route]
                                                   else List.map (route ++ [.]) $
                                                        getNext g xs (List.getLast! route)) routes).join

def nodeUnique : List Node → List Node
  | [] => []
  | (x :: xs) => if Bool.or (xs.contains x) (
                    Bool.or (xs.contains (x.fst+dummy, x.snd+dummy))
                            (xs.contains (x.fst-dummy, x.snd-dummy)))
                 then nodeUnique xs
                 else x :: (nodeUnique xs)

def answer (str : String) : Nat := (nodeUnique (paths 12000 (startPos str) (finishedGraph str) (solvedDijkstras str) [[endPos str]]).join).length + 1
