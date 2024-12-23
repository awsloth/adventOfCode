import LeanSoln.data
import Std

def Vertex : Type := String

def Vertex.satCond : Vertex → Bool
  | s => s.data.head! == 't'

deriving instance BEq for Vertex
deriving instance Hashable for Vertex
deriving instance Inhabited for Vertex
deriving instance ToString for Vertex

def Vertex.LT : Vertex → Vertex → Bool
  | u, v => u.data < v.data

instance : LT Vertex where
  lt u v := u.LT v

def Graph : Type := Std.HashMap Vertex (List Vertex)

def Graph.empty : Graph := Std.HashMap.empty

def Graph.fromString (str : String) : Graph := let pairs := List.map (λ x ↦ let vs := x.splitOn "-";
                                                               (vs.head!, vs.tail!.head!)) (str.splitOn "\n");
                                               List.foldl (λ g ↦
                                                          (λ (u, v) ↦ let g2 := (if g.contains u
                                                                      then let t := (g.get! u);
                                                                           (g.erase u).insert u (v :: t)
                                                                      else g.insert u [v]);

                                                                      if g2.contains v
                                                                      then let t := (g2.get! v);
                                                                           (g2.erase v).insert v (u :: t)
                                                                      else g2.insert v [u])
                                                          ) Graph.empty pairs

def Graph.vertices (g : Graph) : List Vertex := g.keys

def List.choose : List α → Nat → List (List α)
  | [], _ => []
  | (_ :: _), 0 => []
  | (x :: xs), 1 => [x] :: xs.choose 1
  | (x :: xs), (n+1) => (List.map (λ y ↦ (x :: y)) (xs.choose n)) ++ xs.choose (n + 1)

def connected : Graph → List Vertex → Bool
  | _, [] => true
  | g, (x :: xs) => Bool.and (List.all xs (λ y ↦ (g.get! y).contains x)) (connected g xs)

def hasKN : Graph → Vertex → Nat → Bool
  | g, v, n => List.any ((g.get! v).choose n) (λ xs ↦ connected g xs)

def findKN : Graph → Vertex → Nat → List Vertex
  | g, v, n => (List.filter (λ xs ↦ connected g xs) ((g.get! v).choose n)).head!

def findBiggestK : Graph → Nat → List Vertex
  | _, 0 => []
  | g, (n + 1) => if List.any g.vertices (hasKN g . (n + 1))
                  then let v := (List.filter (hasKN g . (n + 1)) g.vertices).head!;
                       v :: findKN g v (n + 1)
                  else findBiggestK g n

def answer (str : String) : List Vertex := let g := Graph.fromString str; (Array.qsort (findBiggestK g 20).toArray (Vertex.LT . .)).toList
