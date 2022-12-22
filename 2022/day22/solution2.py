from aocd import submit
import bs4
import copier
import regex as re

COMPLETE = False 
year, day = [2022, 22]

with open(r"2022\day22\input.txt", 'r') as f:
    inp = f.read()

# inp = """        ...#
#         .#..
#         #...
#         ....
# ...#.......#
# ........#...
# ..#....#....
# ..........#.
#         ...#....
#         .....#..
#         .#......
#         ......#.

# 10R5L5R10L4R5L5"""

grid, move_pattern = inp.split("\n\n")

grid = [line.replace(" ", "x") for line in grid.split('\n')]

max_len = max([len(l) for l in grid])
grid = ['x'*(max_len+2)]+['x'+line.ljust(max_len, "x")+'x' for line in grid]+['x'*(max_len+2)]

moves = []
for move in re.split("([0-9]+[A-Z])", move_pattern):
    if move != '':
        if 'L' in move or 'R' in move:
            moves.append(int(move[:-1]))
            moves.append(move[-1])
        else:
            moves.append(int(move))

"""
#   #  |   0
# ###  | 123
#   ## |   45

edges = [
    [[2, 0], [3, 0], 'u'],
    [[1, 1], [0, 1], 'u'],
    [[1, 1], [2, 1], 'u'],
    [[2, 0], [2, 1], 'l'],
    [[0, 2], [1, 2], 'd'],
    [[3, 3], [2, 3], 'd'],
    [[1, 2], [2, 2], 'd'],
    [[2, 2], [2, 3], 'l'],
    [[3, 2], [4, 2], 'u'],
    [[3, 2], [3, 1], 'r'],
    [[3, 3], [4, 3], 'd'],
    [[0, 1], [0, 2], 'l'],
    [[3, 0], [3, 1], 'r'],
    [[4, 3], [4, 2], 'r']
]

"""

#"""
#  ## |  01
#  #  |  2
# ##  | 34
# #   | 5

# (0, 2)-(1, 2) <-> (1, 1)-(1, 2)
# (0, 2)-(0, 3) <-> (1, 1)-(1, 0)
# (1, 0)-(2, 0) <-> (0, 3)-(0, 4)
# (1, 3)-(2, 3) <-> (1, 3)-(1, 4)
# (2, 0)-(3, 0) <-> (0, 4)-(1, 4)
# (2, 1)-(3, 1) <-> (2, 1)-(2, 2)
# (2, 2)-(2, 3) <-> (3, 1)-(3, 0)

edges = [
    [[0, 2], [1, 2], 'u'],
    [[1, 1], [1, 2], 'l'],
    [[0, 2], [0, 3], 'l'],
    [[1, 1], [1, 0], 'l'],
    [[1, 0], [2, 0], 'u'],
    [[0, 3], [0, 4], 'l'],
    [[1, 3], [2, 3], 'd'],
    [[1, 3], [1, 4], 'r'],
    [[2, 0], [3, 0], 'u'],
    [[0, 4], [1, 4], 'd'],
    [[2, 1], [3, 1], 'd'],
    [[2, 1], [2, 2], 'r'],
    [[2, 2], [2, 3], 'r'],
    [[3, 1], [3, 0], 'r']
]
# """

SIZE = 50

edges = [[[*map(lambda x: x*SIZE+1, edge[0])], [*map(lambda x: x*SIZE+1, edge[1])], edge[2]] for edge in edges]

def findWrap(x, y, dir):
    # Find matching edge
    wrap_edge = -1
    for (i, (e1, e2, d)) in enumerate(edges):
        if e1[0] > e2[0] or e1[1] > e2[1]:
            comp2 = e1
            comp1 = e2
        else:
            comp1 = e1
            comp2 = e2

        match [d, dir]:
            case ['r', 0]:
                if comp1[1] <= y < comp2[1] and comp1[0] == x + 1:
                    wrap_edge = i
                    break
            case ['d', 1]:
                if comp1[0] <= x < comp2[0] and comp1[1] == y + 1:
                    wrap_edge = i
                    break
            case ['l', 2]:
                if comp1[1] <= y < comp2[1] and comp1[0] == x:
                    wrap_edge = i
                    break
            case ['u', 3]:
                if comp1[0] <= x < comp2[0] and comp1[1] == y:
                    wrap_edge = i
                    break

    if wrap_edge == -1:
        print(x, y)
        raise BaseException("Error!")

    # Find matching pair from edge
    if wrap_edge % 2 == 0:
        pair = wrap_edge + 1
    else:
        pair = wrap_edge - 1

    match edges[wrap_edge][2]:
        case 'r':
            x_points = [edges[wrap_edge][0][0] - 1]*SIZE
            if edges[wrap_edge][0][1] < edges[wrap_edge][1][1]:
                y_points = [*range(edges[wrap_edge][0][1], edges[wrap_edge][1][1])]
            else:
                y_points = [*reversed(range(edges[wrap_edge][1][1], edges[wrap_edge][0][1]))]
            point_list = [*zip(x_points, y_points)]
        case 'l':
            x_points = [edges[wrap_edge][0][0]]*SIZE
            if edges[wrap_edge][0][1] < edges[wrap_edge][1][1]:
                y_points = [*range(edges[wrap_edge][0][1], edges[wrap_edge][1][1])]
            else:
                y_points = [*reversed(range(edges[wrap_edge][1][1], edges[wrap_edge][0][1]))]
            point_list = [*zip(x_points, y_points)]
        case 'd':
            y_points = [edges[wrap_edge][0][1] - 1]*SIZE
            if edges[wrap_edge][0][0] < edges[wrap_edge][1][0]:
                x_points = [*range(edges[wrap_edge][0][0], edges[wrap_edge][1][0])]
            else:
                x_points = [*reversed(range(edges[wrap_edge][1][0], edges[wrap_edge][0][0]))]
            point_list = [*zip(x_points, y_points)]
        case 'u':
            y_points = [edges[wrap_edge][0][1]]*SIZE
            if edges[wrap_edge][0][0] < edges[wrap_edge][1][0]:
                x_points = [*range(edges[wrap_edge][0][0], edges[wrap_edge][1][0])]
            else:
                x_points = [*reversed(range(edges[wrap_edge][1][0], edges[wrap_edge][0][0]))]
            point_list = [*zip(x_points, y_points)]

    index = -1
    for (i, (x1, y1)) in enumerate(point_list):
        if x == x1 and y == y1:
            index = i
            break

    if index == -1:
        print(x, y)
        print(edges[wrap_edge])
        raise BaseException("Error2!")

    match edges[pair][2]:
        case 'r':
            x_points = [edges[pair][0][0] - 1]*SIZE
            if edges[pair][0][1] < edges[pair][1][1]:
                y_points = [*range(edges[pair][0][1], edges[pair][1][1])]
            else:
                y_points = [*reversed(range(edges[pair][1][1], edges[pair][0][1]))]
            point_list = [*zip(x_points, y_points)]
        case 'l':
            x_points = [edges[pair][0][0]]*SIZE
            if edges[pair][0][1] < edges[pair][1][1]:
                y_points = [*range(edges[pair][0][1], edges[pair][1][1])]
            else:
                y_points = [*reversed(range(edges[pair][1][1], edges[pair][0][1]))]
            point_list = [*zip(x_points, y_points)]
        case 'd':
            y_points = [edges[pair][0][1] - 1]*SIZE
            if edges[pair][0][0] < edges[pair][1][0]:
                x_points = [*range(edges[pair][0][0], edges[pair][1][0])]
            else:
                x_points = [*reversed(range(edges[pair][1][0], edges[pair][0][0]))]
            point_list = [*zip(x_points, y_points)]
        case 'u':
            y_points = [edges[pair][0][1]]*SIZE
            if edges[pair][0][0] < edges[pair][1][0]:
                x_points = [*range(edges[pair][0][0], edges[pair][1][0])]
            else:
                x_points = [*reversed(range(edges[pair][1][0], edges[pair][0][0]))]
            point_list = [*zip(x_points, y_points)]

    point_list = point_list
    new_pos = [point_list[index][0],point_list[index][1]]

    dir2 = 'rdlu'.index(edges[pair][2])

    new_dir = dir2 + 2
    new_dir %= 4

    return new_pos, new_dir

dirs = [[1, 0], [0, 1], [-1, 0], [0, -1]]
cur_pos = [grid[1].index("."), 1]
direction = 0

for move in moves:
    if type(move) is int:

        for _ in range(move):
            next_pos = [x+y for (x, y) in zip(cur_pos, dirs[direction])]

            if grid[next_pos[1]][next_pos[0]] == "x":
                # Find wrap around point
                saved_dir = direction

                next_pos, direction = findWrap(*cur_pos, direction)
            
                if grid[next_pos[1]][next_pos[0]] == "#":
                    # Hit a wall
                    # print("hit wall wrap")
                    direction = saved_dir
                    break
                else:
                    # Wrap around
                    cur_pos = next_pos
            elif grid[next_pos[1]][next_pos[0]] == "#":
                # Finished moving this go
                # print("hit wall directly")
                break
            else:
                # Move as normal
                cur_pos = next_pos
    else:
        if move == "R":
            direction += 1
            direction %= 4
        elif move == "L":
            direction -= 1
            direction %= 4
        else:
            print(f"Error: {move}")

    print(cur_pos, move, direction)

answer = 1000 * cur_pos[1] + 4 * cur_pos[0] + direction

# 103031 - small

if COMPLETE:
    submit(answer, year=year, day=day)
else:
    print(answer)
