from aocd import submit
import bs4
import copier

COMPLETE = True
year, day = [2021, 5]

with open(r"2021\day5\input.txt", 'r') as f:
    inp = [line.strip() for line in f.readlines()]

GRID_SIZE = 1000
grid = [['.'for _ in range(GRID_SIZE)] for __ in range(GRID_SIZE)]

for line in inp:
    c1, c2 = line.split(" -> ")
    x1, y1 = [*map(int, c1.split(","))]
    x2, y2 = [*map(int, c2.split(","))]
    if x1 == x2:
        for i in range(min(y1, y2), max(y1, y2)+1):
            if grid[i][x1] == ".":
                grid[i][x1] = 1
            else:
                grid[i][x1] += 1
    elif y1 == y2:
        for i in range(min(x1, x2), max(x1, x2)+1):
            if grid[y1][i] == ".":
                grid[y1][i] = 1
            else:
                grid[y1][i] += 1

answer = 0
for row in grid:
    for el in row:
        if type(el) == int and el >= 2:
            answer += 1

if COMPLETE:
    r = submit(answer, year=year, day=day)
    soup = bs4.BeautifulSoup(r.text, "html.parser")
    message = soup.article.text
    if "That's the right answer" in message:
        copier.make_next()
else:
    print(answer)
