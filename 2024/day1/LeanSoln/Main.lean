import LeanSoln.part1
import LeanSoln.part2

def main : IO Unit := do
  IO.println s!"Part 1: {part1.answer}"
  IO.println s!"Part 2: {part2.soln part2.listCounts}"
