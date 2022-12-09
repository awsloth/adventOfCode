from aocd import submit
import bs4
import copier

COMPLETE = True
year, day = [2021, 9]

with open(r"2021\day9\input.txt", 'r') as f:
    inp = [line.strip() for line in f.readlines()]

def valid(x, y, row, column):
    r = len(row) - 1
    c = len(column) - 1
    match [x, y]:
        case [0, 0]:
            return (row[x+1] > row[x] and column[y+1] > column[y])
        case [0, y] if y < c:
            return (row[x+1] > row[x] and column[y+1] > column[y] < column[y-1])
        case [x, 0] if x < r:
            return (row[x+1] > row[x] < row[x-1] and column[y+1] > column[y])
        case [x, y] if x < r and y < c:
            return row[x-1] > row[x] < row[x+1] and column[y-1] > column[y] < column[y+1]
        case [x, y] if x < r:
            return row[x-1] > row[x] < row[x+1] and column[y-1] > column[y]
        case [x, y] if y < c:
            return row[x-1] > row[x] and column[y-1] > column[y] < column[y+1]
        case _:
            return (row[x-1] > row[x] and column[y-1] > column[y])

grid = [[*map(int, line)] for line in inp]

rows = grid
columns = [[row[i] for row in rows] for i in range(len(grid[0]))]

answer = 0

for i in range(len(columns)):
    for j in range(len(rows)):
        v = valid(i, j, rows[j], columns[i])
        answer += v*(grid[j][i] + 1)

if COMPLETE:
    r = submit(answer, year=year, day=day)
    soup = bs4.BeautifulSoup(r.text, "html.parser")
    message = soup.article.text
    if "That's the right answer" in message:
        copier.make_next()
else:
    print(answer)
