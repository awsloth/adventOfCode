import LeanSoln.data
import Std

inductive Op where
  | AND | OR | XOR | N

def Op.fromString : String → Op
  | "AND" => Op.AND
  | "OR" => Op.OR
  | "XOR" => Op.XOR
  | _ => Op.N

def Op.toString : Op → String
  | Op.AND => "AND"
  | Op.OR => "OR"
  | Op.XOR => "XOR"
  | Op.N => ""

def Op.do : Op → Bool → Bool → Bool
  | Op.AND => Bool.and
  | Op.OR => Bool.or
  | Op.XOR => Bool.xor
  | Op.N => (λ _ ↦ id)

instance : ToString Op where
  toString o := o.toString

deriving instance BEq for Op

def Gate : Type := ((String × Op × String) × String)

deriving instance ToString for Gate
deriving instance BEq for Gate

def inputs (str : String) : Std.HashMap String Bool := let inp := (str.splitOn "\n\n").head!.splitOn "\n";
                                                       let listmap := List.map (λ s ↦ let n := s.splitOn ": ";
                                                                                      match n.getLast! with
                                                                                      | "0" => (n.head!, false)
                                                                                      | _ => (n.head!, true)) inp;
                                                        Std.HashMap.ofList listmap

def gates (str : String) : List Gate := let lines := (str.splitOn "\n\n").getLast!.splitOn "\n";
                                        List.map (λ l ↦ let s := l.splitOn " -> ";
                                                        let (inp, out) := (s.head!.splitOn " ", s.getLast!);
                                                        let (a, op, b) := (inp.head!, Op.fromString inp.tail!.head!, inp.getLast!)
                                                        ((a, op, b), out)
                                                        ) lines

def orderGates (inputs : List String) (gates : List Gate) : List Gate :=
  let ok := List.filter (λ ((a, _, b), _) ↦ Bool.and (inputs.contains a) (inputs.contains b)) gates;
  let rest := List.filter (λ ((a, _, b), _) ↦ Bool.not $ Bool.and (inputs.contains a) (inputs.contains b)) gates;
  let newinp := (inputs ++ (List.map Prod.snd ok));
  if rest == [] then ok
  else ok ++ (orderGates newinp rest)
termination_by gates.length
decreasing_by
  sorry

def evalGates : Std.HashMap String Bool → List Gate → Std.HashMap String Bool
  | hs, [] => hs
  | hs, (((a, op, b), out) :: gs) => let ans := op.do (hs.get! a) (hs.get! b);
                                     evalGates (hs.insert out ans) gs

def comp : String × Bool → String × Bool → Bool
  | (a, _), (b, _) => a < b

def natFromBin : List Bool → Nat
  | [] => 0
  | (x :: xs) => (if x then (Nat.pow 2 xs.length) else 0) + natFromBin xs

def answer (str : String) := let inputVals := inputs str
                             let gateVals := evalGates (inputVals) (orderGates (inputVals).keys (gates str));
                             let remStart := List.filter (λ (y, _) ↦ y.data.head! = 'z') gateVals.toList;
                             let nums := (Array.qsort remStart.toArray comp).toList.reverse;
                             nums

def toBin (xs : List (String × Bool)) : String := List.asString (List.map (λ (_, b) ↦ if b then '1' else '0') xs)

#eval! toBin (answer data)

-- did the rest by hand by editing the input
