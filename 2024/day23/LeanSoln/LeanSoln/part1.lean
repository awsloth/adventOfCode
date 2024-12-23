import LeanSoln.data
import Std

def Vertex : Type := String

def Vertex.satCond : Vertex → Bool
  | s => s.data.head! == 't'

deriving instance BEq for Vertex
deriving instance Hashable for Vertex

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

def List.pairs : List α → List (α × α)
  | [] => []
  | (x :: xs) => (List.map (λ y ↦ (x, y)) xs) ++ xs.pairs

def findTriangles : Graph → Vertex → List (Vertex × Vertex × Vertex)
  | g, v => List.map (λ (x, y) ↦ (v, x, y)) $ List.filter (λ (x, y) ↦ (g.get! x).contains y) (g.get! v).pairs

def vertexComp : Vertex × Vertex × Vertex → Vertex × Vertex × Vertex → Bool
  | (a, b, c), (d, e, f) => if a.LT d then true
                            else if d.LT a then false
                            else if b.LT e then true
                            else if e.LT b then false
                            else if c.LT f then true
                            else false

def sortTri : Vertex × Vertex × Vertex → Vertex × Vertex × Vertex
  | (a, b, c) => if a.LT b then if b.LT c then (a, b, c)
                                else if a.LT c then (a, c, b)
                                else (c, a, b)
                 else if a.LT c then (b, a, c)
                                else if b.LT c then (b, c, a)
                                else (c, b, a)

def sortInner : List (Vertex × Vertex × Vertex) → List (Vertex × Vertex × Vertex) := List.map sortTri

def findAllTriangles : Graph → List (Vertex × Vertex × Vertex)
  | g => List.filter (λ (x, y, z) ↦ Bool.or x.satCond (Bool.or y.satCond z.satCond)) $ (sortInner (List.map (findTriangles g .) $ g.vertices).join).eraseDups

def answer (str : String) : Nat := let g := Graph.fromString str;
                                   (findAllTriangles g).length
