from aocd import submit
import bs4
import copier

COMPLETE = True
year, day = [2021, 1]

with open(r"2021\day1\input.txt", 'r') as f:
    inp = [line.strip() for line in f.readlines()]

answer = 0
for ((s1, s2, s3), (e1, e2, e3)) in zip(zip(inp, inp[1:], inp[2:]), zip(inp[1:], inp[2:], inp[3:])):
    if sum(map(int, [s1, s2, s3])) < sum(map(int, [e1, e2, e3])):
        answer += 1


if COMPLETE:
    submit(answer, year=year, day=day)
else:
    print(answer)
