from aocd import submit
import bs4
import copier

COMPLETE = True
year, day = [2022, 14]

with open(r"2022\day14\input.txt", 'r') as f:
    inp = [line.strip() for line in f.readlines()]

sand_start = (500, 0)
rock_pattern = [['.' for _ in range(1000)] for __ in range(200)]

rock_pattern[sand_start[1]][sand_start[0]] = '+'

for line in inp:
    points = [[*map(int, point.split(","))] for point in line.split(" -> ")]
    for ((s_x, s_y), (e_x, e_y)) in zip(points, points[1:]):
        if s_x == e_x:
            for i in range(min(s_y, e_y), max(s_y, e_y)+1):
                rock_pattern[i][s_x] = '#'
        else:
            for i in range(min(s_x, e_x), max(s_x, e_x)+1):
                rock_pattern[s_y][i] = '#'

y_pos = 0
for (i, row) in enumerate(rock_pattern):
    if '#' in row:
        y_pos = i

rock_pattern[y_pos+2] = ['#' for _ in range(1000)]

# Simulate sand
answer = 0
complete = False
while not complete:
    grain_pos = [sand_start[0], sand_start[1]]
    while 1:
        column = [row[grain_pos[0]] for row in rock_pattern][grain_pos[1]:]

        if '#' not in column and '*' not in column:
            complete = True
            break

        g_pos = float('inf')
        drop_pos = float('inf')

        if '*' in column:
            g_pos = column.index("*") - 1
        
        if '#' in column:
            drop_pos = column.index("#") - 1
        
        grain_pos = [grain_pos[0], grain_pos[1]+min(drop_pos, g_pos)]

        if rock_pattern[grain_pos[1]+1][grain_pos[0]-1] == ".":
            grain_pos = [grain_pos[0]-1, grain_pos[1]+1]
        elif rock_pattern[grain_pos[1]+1][grain_pos[0]+1] == ".":
            grain_pos = [grain_pos[0]+1, grain_pos[1]+1]
        else:
            rock_pattern[grain_pos[1]][grain_pos[0]] = "*"
            answer += 1
            break
    
    if grain_pos == [sand_start[0], sand_start[1]]:
        complete = True

if COMPLETE:
    submit(answer, year=year, day=day)
else:
    print(answer)
