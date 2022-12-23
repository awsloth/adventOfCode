COMPLETE = False
year, day = [2021, 9]

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


def main(enabled_print=True, test=False):
    if test:
        with open(r"2021\day9\test.txt", 'r') as f:
            inp = [line.strip() for line in f.readlines()]
    else:
        with open(r"2021\day9\input.txt", 'r') as f:
            inp = [line.strip() for line in f.readlines()]
    
    grid = [[*map(int, line)] for line in inp]
    
    rows = grid
    columns = [[row[i] for row in rows] for i in range(len(grid[0]))]
    
    answer = 0
    
    for i in range(len(columns)):
        for j in range(len(rows)):
            v = valid(i, j, rows[j], columns[i])
            answer += v*(grid[j][i] + 1)
    
    return answer

if __name__ == "__main__":
    from aocd import submit

    import bs4
    import copier

    answer = main(not COMPLETE)
    
    if COMPLETE:
        r = submit(answer, year=year, day=day)
        soup = bs4.BeautifulSoup(r.text, "html.parser")
        message = soup.article.text
        if "That's the right answer" in message:
            copier.make_next(year, day)
    else:
        print(answer)
