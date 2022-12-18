import pygame
import time

pygame.init()

with open(r"2022\day14\input.txt", 'r') as f:
    inp = [line.strip() for line in f.readlines()]

sand_start = (300, 0)
x_offset = 200
WIDTH, HEIGHT = 600, 200
rock_pattern = [['.' for _ in range(WIDTH)] for __ in range(HEIGHT)]

SCALE = 2
screen = pygame.display.set_mode((WIDTH*SCALE, HEIGHT*SCALE))

rock_pattern[sand_start[1]][sand_start[0]] = '+'

rock_points = []
for line in inp:
    points = [[*map(int, point.split(","))] for point in line.split(" -> ")]
    points = [[p[0]-x_offset, p[1]] for p in points]
    rock_points.append(points)
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

rock_points.append([[0, y_pos+2], [WIDTH, y_pos+2]])

rock_pattern[y_pos+2] = ['#' for _ in range(1000)]

for rock in rock_points:
    rock = rock + [*reversed(rock)]
    if len(rock) > 2:
        pygame.draw.polygon(screen, (0, 0, 255), [[*map(lambda x: SCALE*x, point)] for point in rock], width=SCALE)
    else:
        pygame.draw.line(screen, (0, 0, 255), *[[*map(lambda x: SCALE*x, point)] for point in rock], width=SCALE)

pygame.display.update()

# Simulate sand
answer = 0
complete = False
while not complete:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    grain_pos = [sand_start[0], sand_start[1]+1]
    while 1:

        column = [row[grain_pos[0]] for row in rock_pattern][grain_pos[1]:]

        if '#' not in column and '*' not in column:
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

    pygame.draw.rect(screen, (255, 255, 0), (grain_pos[0]*SCALE, grain_pos[1]*SCALE, SCALE, SCALE))

    pygame.display.update((grain_pos[0]*SCALE, grain_pos[1]*SCALE, SCALE, SCALE))
