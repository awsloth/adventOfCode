from aocd import submit
import bs4
import copier

COMPLETE = True 
year, day = [2022, 6]

with open(r"2022\day6\input.txt", 'r') as f:
    inp = [line.strip() for line in f.readlines()]

i = 0
while len(list(set(inp[0][i:i+14]))) < 14:
    i += 1

print(inp[0][i:i+14])
answer = i + 14

if COMPLETE:
    submit(answer, year=year, day=day)
else:
    print(answer)
