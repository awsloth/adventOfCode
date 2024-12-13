import LeanSoln.data

def List.sum : List Nat → Nat := foldl (λ s ↦ (λ n ↦ s + n)) 0

-- inclusive range
def Range : Type := (Nat × Nat)

deriving instance BEq for Range

def Range.width : Range → Nat
  | (1, 0) => 0
  | (x, y) => (y - x + 1)

def Range.intersect : Range → Range → Range
  | (sp, ep), (sq, eq) => if Bool.and (sq ≤ sp) (ep ≤ eq) then (sp, ep)
                          else if Bool.and (sp ≤ sq) (eq ≤ ep) then (sq,eq)
                          else if Bool.and (Bool.and (sq ≤ ep) (sp ≤ eq)) (eq ≤ ep) then (sp, eq)
                          else if (Bool.and (sq ≤ ep) (sp ≤ eq)) then (sq, ep)
                          else (1, 0)

-- patch, connected plants
def Patch : Type := Char × List (List Range)

def Patch.ranges : Patch → List (List Range)
  | (_, ranges) => ranges

def Patch.area : Patch → Nat
  | (_, lines) => List.sum $ List.map (λ blocks ↦ List.sum $ List.map Range.width blocks) lines

def Patch.perimeter : Patch → Nat
  | (_, lines) => List.sum $
                  List.map (λ (above, line) ↦ (line.length +
                                              (List.sum $ List.map Range.width line) -
                                              (List.sum $ List.map (λ block ↦
                                                                    List.sum $ List.map (λ a ↦
                                                                    (block.intersect a).width) above) line)
                                              )*2
                           )
                  (List.zip ([[]] ++ lines) lines)

def Patch.insertRange : Patch → Nat → Range → Patch
  | (c, patches), d, r => if d == patches.length then (c, patches ++ [[r]]) else (c, patches.set d ((patches.get! d) ++ [r]))

def Patch.merge : Patch → List Patch → Patch
  | p, [] => p
  | p, xs => List.foldl (λ (c, sp) ↦ (λ (_, np) ↦ (c, List.zipWith (.++.) (sp ++ [[]]) (np ++ [[]])))) p xs

deriving instance Inhabited, BEq for Patch

def splitHelper : List Char → List Char → List (List Char)
  | [], curblock => [curblock]
  | (x :: []), _ => [[x]]
  | (x :: (y :: [])), curblock => if x == y then [curblock ++ [x, y]] else [curblock ++ [x], [y]]
  | (x :: (y :: xs)), curblock => if x == y then splitHelper (y :: xs) (curblock ++ [x]) else (curblock ++ [x]) :: splitHelper (y :: xs) []

def String.splitOnChange (s : String) : List String := List.map (λ block ↦ block.asString) (splitHelper s.data [])

def lines : String → List String := (String.splitOn . "\n")

-- Includes the sum of no elements
def List.cumlSum : List Nat → List Nat := List.foldl (λ xs ↦ (λ y ↦ xs ++ [xs.getLast! + y])) [0]

-- Inclusive range, so the last is _in_ the range
def lineToRange (blocks : List String) : List (Char × Range) :=
  List.map (λ (block, x) ↦ (block.data.head!, (x, x + block.length - 1)))
           (List.zip blocks
                     (List.map (λ x ↦ x.length) blocks).cumlSum)

-- Turn string into grid of blocks
def gridToBlocks (str : String) : List (List (Char × Range)) :=
  List.map lineToRange $
  List.map (λ s ↦ s.splitOnChange) (lines str)

-- Form the intial patches from blocks
def initialPatches : List (Char × Range) → List Patch
  | [] => []
  | ((c, r) :: xs) => (c, [[r]]) :: (initialPatches xs)

def intersectAbove (r : Range) (above : List Range) : Bool := (List.any above (λ t ↦ Bool.not $ (r.intersect t) == (1, 0)))

def emptyN : Nat → List (List Range)
  | 0 => []
  | (n+1) => [[]] ++ emptyN n

-- Merge a line of blocks into the above connected patches
def mergeAbove : Nat × List Patch → List (Char × Range) → (Nat × List Patch)
  | (d, patches), [] => (d+1, patches)
  | (d, patches), ((x, r) :: xs) =>
    let aboveIntersection := List.filter (λ (c, p) ↦ Bool.and (Bool.and (c == x) (p.length ≥ d)) (intersectAbove r (p.get! (d-1)))) patches;
    let leftOver := List.filter (λ x ↦ Bool.not (aboveIntersection.contains x)) patches;
    match (aboveIntersection).length with
    | 0 => mergeAbove (d, ((x, (emptyN d) ++ [[r]]) :: leftOver)) xs
    | 1 => mergeAbove (d, ((aboveIntersection.head!.insertRange d r) :: leftOver)) xs
    | _ => mergeAbove (d, (((aboveIntersection.head!.merge aboveIntersection.tail!).insertRange d r) :: leftOver)) xs

def blocksToPatches (blocks : List (List (Char × Range))) : List Patch :=
  (List.foldl mergeAbove (1, initialPatches blocks.head!) blocks.tail!).snd

def calcCost (patches : List Patch) : Nat := List.sum (List.map (λ p ↦ p.area * p.perimeter) patches)

def calcCostDebug (patches : List Patch) : List (Nat × Nat × Patch) := (List.map (λ p ↦ (p.area, p.perimeter, p)) patches)

def answer : String → Nat := calcCost ∘ blocksToPatches ∘ gridToBlocks

