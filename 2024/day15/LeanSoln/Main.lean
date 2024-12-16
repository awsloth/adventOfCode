import LeanSoln.part2

def main : IO Unit := do
  let gs ← finalState smallData
  -- IO.println $ printStart testData
  -- IO.println $ s!"Part 2: {answer data}"
  -- IO.println $ genMap Dir.U (items $ grid $ smallData).fst (finalState smallData)
