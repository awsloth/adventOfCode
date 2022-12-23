COMPLETE = True
year, day = [2022, 23]

def getAround(x, y, grid):
    surrounding = ['.' for _ in range(8)]
    if x > 0 and y > 0:
        surrounding[0] = grid[y-1][x-1]
    if y > 0:
        surrounding[1] = grid[y-1][x]
    if y > 0 and x < len(grid[y-1]) - 1:
        surrounding[2] = grid[y-1][x+1]
    if x > 0:
        surrounding[3] = grid[y][x-1]
    if x < len(grid[y]) - 1:
        surrounding[4] = grid[y][x+1]
    if y < len(grid) - 1 and x > 0:
        surrounding[5] = grid[y+1][x-1]
    if y < len(grid) - 1:
        surrounding[6] = grid[y+1][x]
    if y < len(grid) - 1 and x < len(grid[y+1]) - 1:
        surrounding[7] = grid[y+1][x+1]

    return surrounding

def ruleOne(surrounding):
    if surrounding[0] == '.' and surrounding[1] == '.' and surrounding[2] == '.':
        return True
    return False

def ruleTwo(surrounding):
    if surrounding[5] == '.' and surrounding[6] == '.' and surrounding[7] == '.':
        return True
    return False

def ruleThree(surrounding):
    if surrounding[0] == '.' and surrounding[3] == '.' and surrounding[5] == '.':
        return True
    return False

def ruleFour(surrounding):
    if surrounding[2] == '.' and surrounding[4] == '.' and surrounding[7] == '.':
        return True
    return False

def main(enabled_print=True, test=False):
    if test:
        with open(r"2022\day23\test.txt", 'r') as f:
            inp = [line.strip() for line in f.readlines()]
    else:
        with open(r"2022\day23\input.txt", 'r') as f:
            inp = [line.strip() for line in f.readlines()]

    grid = inp

    rules = [[ruleOne, [0, -1]], [ruleTwo, [0, 1]], [ruleThree, [-1, 0]], [ruleFour, [1, 0]]]

    for count in range(10):
        new_grid = [['.' for __ in range(len(grid[0]))] for _ in range(len(grid))]

        elves = []
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                if grid[i][j] == '#':
                    elves.append([i, j])

        to_move = []
        for (y, x) in elves:
            if getAround(x, y, grid).count('#') != 0:
                to_move.append([x, y])
            else:
                new_grid[y][x] = '#'

        prop_moves = []
        for elf in to_move:
            surrounding = getAround(*elf, grid)
            start = count
            index = start
            while not rules[index%4][0](surrounding) and index != start+4:
                index += 1

            if index != start + 4:
                new_pos = [pos+move for (pos, move) in zip(elf, rules[index%4][1])]
                prop_moves.append([elf, new_pos])
            else:
                new_grid[elf[1]][elf[0]] = '#'

        prop_moves = sorted(prop_moves, key=lambda x: x[1][0])

        offset = [0, 0]
        for i in range(len(prop_moves)):
            move_ok = True
            for j in range(len(prop_moves)):
                if prop_moves[i][1] == prop_moves[j][1] and i != j:
                    move_ok = False
                    break
            
            if move_ok:
                if prop_moves[i][1][1] + offset[1] == -1:
                    offset[1] += 1
                    new_grid.insert(0, ['.' for _ in range(len(new_grid))])
                    
                elif prop_moves[i][1][0] + offset[0] == -1:
                    offset[0] += 1
                    new_grid = [['.']+row for row in new_grid]

                elif prop_moves[i][1][1] + offset[1] == len(new_grid):
                    new_grid.append(['.' for _ in range(len(new_grid))])

                elif prop_moves[i][1][0] + offset[0] == len(new_grid[0]):
                    new_grid = [row+['.'] for row in new_grid]
                
                if enabled_print:
                    print(f"elf y={prop_moves[i][1][1]+offset[1]}, elf x={prop_moves[i][1][0]+offset[0]}")
                    print(f"{len(new_grid)=}, {len(new_grid[0])=}")

                new_grid[prop_moves[i][1][1]+offset[1]][prop_moves[i][1][0]+offset[0]] = '#'
            else:
                new_grid[prop_moves[i][0][1]+offset[1]][prop_moves[i][0][0]+offset[0]] = '#'

        grid = new_grid
        
        if enabled_print:
            print(*map(''.join, grid), '', sep='\n')

    return sum([row.count(".") for row in grid])

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
