COMPLETE = False
year, day = [2021, 5]

def main(enabled_print=True, test=False):
    if test:
        with open(r"2021\day5\test.txt", 'r') as f:
            inp = [line.strip() for line in f.readlines()]
    else:
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
        elif abs(x1 - x2) == abs(y1 - y2):
            if x1 < x2:
                x_nums = [*range(x1, x2+1)]
            else:
                x_nums = [*reversed([*range(x2, x1+1)])]
    
            if y1 < y2:
                y_nums = [*range(y1, y2+1)]
            else:
                y_nums = [*reversed([*range(y2, y1+1)])]
    
            for (x, y) in zip(x_nums, y_nums):
                if grid[y][x] == ".":
                    grid[y][x] = 1
                else:
                    grid[y][x] += 1
    
    answer = 0
    for row in grid:
        for el in row:
            if type(el) == int and el >= 2:
                answer += 1
    
    return answer
    
if __name__ == "__main__":
    from aocd import submit

    answer = main(not COMPLETE)
    
    if COMPLETE:
        r = submit(answer, year=year, day=day)
    else:
        print(answer)

