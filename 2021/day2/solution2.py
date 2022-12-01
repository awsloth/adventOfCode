from aocd import submit
import bs4
import copier

root = r"C:\Users\Adam\PythonProjects\adventOfCode\2021"

COMPLETE = True
year, day = [2021, 2]

with open(r"C:\Users\Adam\PythonProjects\adventOfCode\2021\day2\input.txt", 'r') as f:
    inp = [line.strip() for line in f.readlines()]

h_pos = 0
depth = 0
aim = 0

for line in inp:
    if "forward" in line:
        h_pos += int(line[7:])
        depth += aim * int(line[7:])
    elif "up" in line:
        aim -= int(line[2:])
    else:
        aim += int(line[4:])

answer = h_pos * depth

if COMPLETE:
    submit(answer, year=year, day=day)
else:
    print(answer)
