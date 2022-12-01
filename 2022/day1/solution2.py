from aocd import submit
import bs4
import copier

COMPLETE = False
year, day = [2022, 1]

with open(r"day1\input.txt", 'r') as f:
    inp = [line.strip() for line in f.readlines()]

runningTotal = 0
totals = []
for line in inp:
    if line == '':
        totals.append(runningTotal)
        runningTotal = 0
    else:
        runningTotal += int(line)

top = max(totals)
totals.remove(top)
second = max(totals)
totals.remove(second)
third = max(totals)

answer = top + second + third

if COMPLETE:
    submit(answer, year=year, day=day)
else:
    print(answer)
