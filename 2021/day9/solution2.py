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

def expand(coords):
    x, y = coords
    row = rows[y]
    column = columns[x]
    pos = []
    
    if x > 0 and row[x-1] != 9:
        pos.append([x - 1, y])
    if x < len(row) - 1 and row[x+1] != 9:
        pos.append([x + 1, y])
    if y > 0 and column[y-1] != 9:
        pos.append([x, y - 1])
    if y < len(column) - 1 and column[y+1] != 9:
        pos.append([x, y + 1])

    return pos

grid = [[*map(int, line)] for line in inp]

rows = grid
columns = [[row[i] for row in rows] for i in range(len(grid[0]))]

basins = []
for i in range(len(columns)):
    for j in range(len(rows)):
        v = valid(i, j, rows[j], columns[i])
        if v:
            basin = [[i, j]]

            expands = []
            change = 0
            for result in map(expand, basin):
                expands += result
            
            for item in expands:
                if item not in basin:
                    basin.append(item)
                    change += 1
        
            while change > 0:
                expands = []
                change = 0
                for result in map(expand, basin):
                    expands += result
                    
                for item in expands:
                    if item not in basin:
                        basin.append(item)
                        change += 1
            
            basins.append(len(basin))

basins = sorted(basins)
answer = basins[-1] * basins[-2] * basins[-3]

if COMPLETE:
    submit(answer, year=year, day=day)
else:
    print(answer)
