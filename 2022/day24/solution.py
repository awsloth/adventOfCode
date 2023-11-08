COMPLETE = True
year, day = [2022, 24]

def moveBlizzard(blizzard, grid_width, grid_height):
    (x, y), dir = blizzard
    match dir:
        case '<':
            if x == 1:
                x = grid_width - 2
            else:
                x -= 1
        case '>':
            if x == grid_width - 2:
                x = 1
            else:
                x += 1
        case '^':
            if y == 1:
                y = grid_height - 2
            else:
                y -= 1
        case 'v':
            if y == grid_height - 2:
                y = 1
            else:
                y += 1

    return [[x, y], dir]

def findMoves(x, y, blizzards, grid_width, grid_height, start, end):
    pos_moves = []
    near_blizzards = []
    hit_self = False
    for blizzard in blizzards:
        if blizzard[0][0] == x and blizzard[0][1] == y:
            hit_self = True
        elif blizzard[0][0] == x and abs(blizzard[0][1] - y) == 1:
            near_blizzards.append(blizzard)
        elif blizzard[0][1] == y and abs(blizzard[0][0] - x) == 1:
            near_blizzards.append(blizzard)

    near_bliz_pos = [n_bliz[0] for n_bliz in near_blizzards]

    if x > 1 and y != 0 and y!= grid_height - 1 and [x-1, y] not in near_bliz_pos:
        pos_moves.append([x-1, y])
    if y > 1 and [x, y-1] not in near_bliz_pos:
        pos_moves.append([x, y-1])
    if x < grid_width - 2 and y != 0 and y!= grid_height - 1 and [x+1, y] not in near_bliz_pos:
        pos_moves.append([x+1, y])
    if y < grid_height - 2 and [x, y+1] not in near_bliz_pos:
        pos_moves.append([x, y+1])
    if x == end[0] and y == end[1]-1:
        pos_moves.append(end)
    if x == start[0] and y == start[1]+1:
        pos_moves.append(start)
    if not hit_self:
        pos_moves.append([x, y])

    return pos_moves

def main(enabled_print=True, test=False):
    if test:
        with open(r"2022\day24\test.txt", 'r') as f:
            inp = [line.strip() for line in f.readlines()]
    else:
        with open(r"2022\day24\input.txt", 'r') as f:
            inp = [line.strip() for line in f.readlines()]

    grid = inp

    blank_grid = [line.replace("<", ".").replace(">", ".").replace("^", ".").replace("v", ".") for line in grid.copy()]

    GRID_WIDTH, GRID_HEIGHT = len(grid[0]), len(grid)

    start = [grid[0].index("."), 0]
    end = [grid[len(grid)-1].index("."), len(grid)-1]

    blizzards = []

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] in ['<', '>', '^', 'v']:
                blizzards.append([[j, i], grid[i][j]])

    cur_states = [start]
    num_moves = 0
    while [state for state in cur_states if state == end] == []:
        if enabled_print:
            print(len(cur_states))
            print(num_moves)
        
        cur_grid = blank_grid.copy()
        for i in range(len(blizzards)):
            blizzards[i] = moveBlizzard(blizzards[i], GRID_WIDTH, GRID_HEIGHT)
            cur_grid[blizzards[i][0][1]] = cur_grid[blizzards[i][0][1]][:blizzards[i][0][0]] + blizzards[i][1] + cur_grid[blizzards[i][0][1]][blizzards[i][0][0]+1:]
        
        new_states = []
        for state in cur_states:
            pos_moves = findMoves(*state, blizzards, GRID_WIDTH, GRID_HEIGHT, start, end)

            for move in pos_moves:
                if move not in new_states:
                    new_states.append(move)

        cur_states = new_states

        num_moves += 1

    return num_moves

if __name__ == "__main__":
    from aocd import submit

    import bs4
    import copier

    answer = main(False)
    
    if COMPLETE:
        r = submit(answer, year=year, day=day)
        soup = bs4.BeautifulSoup(r.text, "html.parser")
        message = soup.article.text
        if "That's the right answer" in message:
            copier.make_next(year, day)
    else:
        print(answer)
