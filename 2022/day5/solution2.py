from aocd import submit
import bs4
import copier

COMPLETE = True
year, day = [2022, 5]

with open(r"2022\day5\input.txt", 'r') as f:
    inp = [line for line in f.readlines()]

crates = inp[:8]
ops = inp[10:]
stacks = [[] for _ in range(9)]
for line in crates:
    crateList = [*map("".join, [*zip(line[::4], line[1::4], line[2::4])])]
    for i in range(len(crateList)):
        if crateList[i] != "   ":
            stacks[i].insert(0, crateList[i][1:-1])

for line in ops:
    nums = [[a.strip() for a in l.split("to")] for l in line.split("from")]
    quant = int(nums[0][0][5:])
    _from, to = map(int, nums[1])
    temp = []
    for i in range(quant):
        temp.append(stacks[_from-1].pop())
    
    stacks[to-1] += [*reversed(temp)]

answer = ""
for stack in stacks:
    if stack != []:
        answer += stack[-1]

if COMPLETE:
    submit(answer, year=year, day=day)
else:
    print(answer)
