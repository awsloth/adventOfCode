from aocd import submit
import bs4
import copier
import regex as re

COMPLETE = True
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


dirs = [[1, 0], [0, 1], [-1, 0], [0, -1]]
cur_pos = [grid[1].index("."), 1]
direction = 0

for move in moves:
    if type(move) is int:

        for _ in range(move):
            next_pos = [x+y for (x, y) in zip(cur_pos, dirs[direction])]

            if grid[next_pos[1]][next_pos[0]] == "x":
                # Find wrap around point
                op_dir = (direction+2)%4

                next_pos = [x+y for (x, y) in zip(cur_pos, dirs[op_dir])]

                while grid[next_pos[1]][next_pos[0]] != "x":
                    next_pos = [x+y for (x, y) in zip(next_pos, dirs[op_dir])]
                
                next_pos = [x+y for (x, y) in zip(next_pos, dirs[direction])]

                if grid[next_pos[1]][next_pos[0]] == "#":
                    # Hit a wall
                    # print("hit wall wrap")
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

    # print(move, cur_pos, 'rdlu'[direction])

answer = 1000 * cur_pos[1] + 4 * cur_pos[0] + direction

if COMPLETE:
    r = submit(answer, year=year, day=day)
    soup = bs4.BeautifulSoup(r.text, "html.parser")
    message = soup.article.text
    if "That's the right answer" in message:
        copier.make_next()
else:
    print(answer)
