import LeanSoln.data

def numeralData (s : String) : List Nat := List.map (λ c ↦ c.toNat - 48) s.data

def lastID (xs : List Nat) : Nat := if (Nat.mod xs.length 2) == 1 then (xs.length - 1) / 2 else (xs.length / 2) - 1

def List.rangeFrom (s e : Nat) : List Nat := List.map (.+s) (List.range (e - s))

def List.sum : List Nat → Nat
  | [] => 0
  | (x :: xs) => x + xs.sum

-- start-pointer, end-pointer, start-id, end-id, end-memory-pointer, input, output
def answer (spoint epoint sid eid mempointer : Nat) (memory : List Nat) : Nat :=
  if spoint ≥ epoint then List.sum (List.map (eid*.) (List.rangeFrom mempointer (mempointer + (memory.get! spoint))))
  else
  match (Nat.mod spoint 2) with
    | 0 => let space := (mempointer + (memory.get! spoint)); List.sum (List.map (sid*.) (List.rangeFrom mempointer space)) + if (spoint + 1) ≥ epoint then List.sum (List.map (eid*.) (List.rangeFrom mempointer (mempointer + (memory.get! (spoint+1))))) else if (Nat.mod epoint 2) == 1 then answer (spoint + 1) (epoint - 1) (sid + 1) eid mempointer memory else
           let mempointer := space;
           let newspoint := spoint + 1;
           let newsid := sid + 1;
           let space := (memory.get! newspoint);
           let curSpace := (memory.get! epoint);
           if curSpace < space then let start := mempointer + curSpace;
                                    List.sum (List.map (eid*.) (List.rangeFrom mempointer start)) +
                                    answer newspoint (epoint - 2) newsid (eid - 1) start (memory.set newspoint (space - curSpace))
           else if curSpace == space then List.sum (List.map (eid*.) (List.rangeFrom mempointer (mempointer + space)))  +
                                          answer (newspoint + 1) (epoint - 2) newsid (eid - 1) (mempointer + space) (memory.set epoint 0)
           else List.sum (List.map (eid*.) (List.rangeFrom mempointer (mempointer + space)))  + 
                answer (newspoint + 1) epoint newsid eid (mempointer + space) (memory.set epoint (curSpace - space))
    | 1 => if (Nat.mod epoint 2) == 1 then answer spoint (epoint - 1) sid eid mempointer memory else
           let space := (memory.get! spoint);
           let curSpace := (memory.get! epoint);
           if curSpace < space then let start := mempointer + curSpace;
                                    List.sum (List.map (eid*.) (List.rangeFrom mempointer start)) +
                                    answer spoint (epoint - 2) sid (eid - 1) start (memory.set spoint (space - curSpace))
           else if curSpace == space then List.sum (List.map (eid*.) (List.rangeFrom mempointer (mempointer + space)))  +
                                          answer (spoint + 1) (epoint - 2) sid (eid - 1) (mempointer + space) (memory.set epoint 0)
           else List.sum (List.map (eid*.) (List.rangeFrom mempointer (mempointer + space)))  + 
                answer (spoint + 1) epoint sid eid (mempointer + space) (memory.set epoint (curSpace - space))
    | _ => 100000

def findFull (nums : List Nat) : Nat := answer 0 (nums.length - 1) 0 (lastID nums) 0 nums

#eval! findFull $ numeralData $ data
