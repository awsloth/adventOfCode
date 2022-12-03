from aocd import submit
import bs4
import copier

COMPLETE = True 
year, day = [2022, 3]

with open(r"2022\day3\input.txt", 'r') as f:
    inp = [line.strip() for line in f.readlines()]

answer = 0
for (l1, l2, l3) in zip(inp[::3], inp[1::3], inp[2::3]):
    c = list((set(l1).intersection(set(l2))).intersection(set(l3)))[0]
    prior = ord(c.upper()) - 64
    if c.upper() == c:
        prior += 26
    answer += prior

if COMPLETE:
    submit(answer, year=year, day=day)
else:
    print(answer)
