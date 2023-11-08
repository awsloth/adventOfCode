COMPLETE = False
year, day = [2022, 17]

def piece1(top_left, _grid, move):
    if move == "<":
        if top_left[0] == 0:
            return False
        if _grid[top_left[1]][top_left[0]-1] == '#':
            return False
        return True
    elif move == ">":
        if top_left[0]+3 == 6:
            return False
        if _grid[top_left[1]][top_left[0]+4] == '#':
            return False
        return True
    elif move == "v":
        if any([_grid[top_left[1]-1][x] == '#' for x in range(top_left[0], top_left[0]+4)]):
            return False
        elif top_left[1] == 0:
            return False
        return True
    
    print("Error!")

def piece2(top_left, _grid, move):
    if move == "<":
        if top_left[0]-1 == 0:
            return False
        if _grid[top_left[1]][top_left[0]-1] == '#':
            return False
        if _grid[top_left[1]-1][top_left[0]-2] == '#':
            return False
        if _grid[top_left[1]-2][top_left[0]-1] == '#':
            return False
        return True
    elif move == ">":
        if top_left[0] + 1 == 6:
            return False
        if _grid[top_left[1]][top_left[0]+1] == '#':
            return False
        if _grid[top_left[1]-1][top_left[0]+2] == '#':
            return False
        if _grid[top_left[1]-2][top_left[0]+1] == '#':
            return False
        return True
    elif move == "v":
        if top_left[1] - 2 == 0:
            return False
        if _grid[top_left[1]-2][top_left[0]+1] == '#':
            return False
        if _grid[top_left[1]-2][top_left[0]-1] == '#':
            return False
        if _grid[top_left[1]-3][top_left[0]] == '#':
            return False
        return True

    print("Error!")

def piece3(top_left, _grid, move):
    # ..#
    # ..#
    # ###
    if move == "<":
        if top_left[0]-2 == 0:
            return False
        if _grid[top_left[1]][top_left[0]-1] == '#':
            return False
        if _grid[top_left[1]-1][top_left[0]-1] == '#':
            return False
        if _grid[top_left[1]-2][top_left[0]-3] == '#':
            return False
        return True
    elif move == ">":
        if top_left[0] == 6:
            return False
        if _grid[top_left[1]][top_left[0]+1] == '#':
            return False
        if _grid[top_left[1]-1][top_left[0]+1] == '#':
            return False
        if _grid[top_left[1]-2][top_left[0]+1] == '#':
            return False
        return True
    elif move == "v":
        if top_left[1] - 2 == 0:
            return False
        if _grid[top_left[1]-3][top_left[0]-2] == '#':
            return False
        if _grid[top_left[1]-3][top_left[0]-1] == '#':
            return False
        if _grid[top_left[1]-3][top_left[0]] == '#':
            return False
        return True
    print("Error!")
    
def piece4(top_left, _grid, move):
    if move == "<":
        if top_left[0] == 0:
            return False
        if _grid[top_left[1]][top_left[0]-1] == '#':
            return False
        if _grid[top_left[1]-1][top_left[0]-1] == '#':
            return False
        if _grid[top_left[1]-2][top_left[0]-1] == '#':
            return False
        if _grid[top_left[1]-3][top_left[0]-1] == '#':
            return False
        return True
    elif move == ">":
        if top_left[0] == 6:
            return False
        if _grid[top_left[1]][top_left[0]+1] == '#':
            return False
        if _grid[top_left[1]-1][top_left[0]+1] == '#':
            return False
        if _grid[top_left[1]-2][top_left[0]+1] == '#':
            return False
        if _grid[top_left[1]-3][top_left[0]+1] == '#':
            return False
        return True
    elif move == "v":
        if top_left[1]-3 == 0:
            return False
        if _grid[top_left[1]-4][top_left[0]] == '#':
            return False
        return True
    print("Error!")

def piece5(top_left, _grid, move):
    # ##
    # ##
    if move == "<":
        if top_left[0] == 0:
            return False
        if _grid[top_left[1]][top_left[0] - 1] == '#':
            return False
        if _grid[top_left[1] - 1][top_left[0] - 1] == '#':
            return False
        return True
    elif move == ">":
        if top_left[0] + 1 == 6:
            return False
        if _grid[top_left[1]][top_left[0] + 2] == '#':
            return False
        if _grid[top_left[1] - 1][top_left[0] + 2] == '#':
            return False
        return True
    elif move == "v":
        if top_left[1] - 1 == 0:
            return False
        if _grid[top_left[1]-2][top_left[0]] == '#':
            return False
        if _grid[top_left[1]-2][top_left[0]+1] == '#':
            return False
        return True
    print("Error!")

def draw(top_left, shape, _grid):
    for (i, (width, offset)) in enumerate(shape):
        left = top_left[0]+offset
        right = top_left[0]+width+offset
        _grid[top_left[1]-i] = _grid[top_left[1]-i][:left] + '#'*width + _grid[top_left[1]-i][right:]


def main(enabled_print=True, test=False):
    if test:
        with open(r"2022\day17\test.txt", 'r') as f:
            inp = [line.strip() for line in f.readlines()]
    else:
        with open(r"2022\day17\input.txt", 'r') as f:
            inp = [line.strip() for line in f.readlines()]
    
    bounding = [
        piece1,
        piece2,
        piece3,
        piece4,
        piece5
    ]
    
    top_lefts = [
        lambda y: [2, y+4],
        lambda y: [3, y+6],
        lambda y: [4, y+6],
        lambda y: [2, y+7],
        lambda y: [2, y+5]
        
    ]
    
    shapes = [
        [
            [4, 0]
        ],
        [
            [1, 0],
            [3, -1],
            [1, 0]
        ],
        [
            [1, 0],
            [1, 0],
            [3, -2]
        ],
        [
            [1, 0],
            [1, 0],
            [1, 0],
            [1, 0]
        ],
        [
            [2, 0],
            [2, 0]
        ]
    ]
    
    grid = []
    moves = inp[0]
    step = 5
    
    points = []
    scores = []
    pointer = 0
    max_height = -1
    overlap = False
    start = 0
    end = 0
    i = 0
    while not overlap:
        cur_pos = top_lefts[i%5](max_height).copy()
        for j in range(cur_pos[1]-max_height+1):
            grid.append('.......')
        
        landed = False
        while not landed:
            # Attempt move side to side
            if bounding[i%5](cur_pos, grid, moves[pointer]):
                if moves[pointer] == "<":
                    cur_pos[0] -= 1
                else:
                    cur_pos[0] += 1
    
            # Attempt move down if not able turn on landed flag
            if bounding[i%5](cur_pos, grid, 'v'):
                cur_pos[1] -= 1
            else:
                landed = True
    
            # Increase pointer
            pointer += 1
            pointer %= len(moves)
    
        draw(cur_pos, shapes[i%5], grid)
        max_height = max([i for i in range(len(grid)) if '#' in grid[i]])
    
        grid = [row for row in grid if row != '.......']
    
        points.append(cur_pos)
        scores.append(max_height)
    
        pos = []
        for p1 in range(0, len(points) - step, step):
            for p2 in range(p1, len(points) - step, step):
                if p1 != p2 and points[p1][0] == points[p2][0] and points[p1+1][0] == points[p2+1][0]:
                    pos.append([p1, p2])
    
        for (p1, p2) in pos:
            dif = points[p2][1] - points[p1][1]
            if len(points) > 2 * p2 - p1:
                for k in range(p2-p1):
                    if points[p1+k][0] != points[p2+k][0] or points[p1+k][1] + dif != points[p2+k][1]:
                        break
                else:
                    start = p1
                    end = p2
                    overlap = True
                    break
    
        if enabled_print:
            if i % 1000 == 0:
                print(i)
        
        i += 1
    
    s_score = scores[start]
    repeat_score = scores[end] - scores[start]
    repeat_dist = end - start
    total_gos = 1_000_000_000_000
    total_repeats = (total_gos - start) // repeat_dist
    remaining_gos = total_gos  - (start + 1) - (total_repeats * repeat_dist)
    remaining_score = scores[remaining_gos+start] - scores[start]
    total_score = total_repeats * repeat_score + s_score + remaining_score
    
    return total_score + 1
    
if __name__ == "__main__":
    from aocd import submit

    answer = main(not COMPLETE)
    
    if COMPLETE:
        r = submit(answer, year=year, day=day)
    else:
        print(answer)

