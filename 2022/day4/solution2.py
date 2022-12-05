from aocd import submit
import bs4
import copier

COMPLETE = True
year, day = [2022, 4]

with open(r"2022\day4\input.txt", 'r') as f:
    inp = [line.strip() for line in f.readlines()]

def cRange(str):
    a1, a2 = map(int, str.split("-"))
    return [*range(a1, a2+1)]

answer = 0
for line in inp:
    r1, r2 = map(cRange, line.split(","))
    if list(set(r1).intersection(set(r2))) != []:
        answer += 1
    

if COMPLETE:
    submit(answer, year=year, day=day)
else:
    print(answer)
