import time
import pygame

with open(r"2022\day9\input.txt", 'r') as f:
    inp = [line.strip() for line in f.readlines()]

scale = 2
G_SIZE = 300
t_count = [[0 for _ in range(G_SIZE)] for __ in range(G_SIZE)]

screen = pygame.display.set_mode((G_SIZE*scale, G_SIZE*scale))
clock = pygame.time.Clock()

def hsvToRGB(h, s, v):
    c = v * s
    x = c * (1 - abs((h/60)%2 - 1))
    m = v - c
    h %= 360
    if 0 <= h < 60:
        r_, g_, b_ = c, x, 0
    elif 60 <= h < 120:
        r_, g_, b_ = x, c, 0
    elif 120 <= h < 180:
        r_, g_, b_ = 0, c, x
    elif 180 <= h < 240:
        r_, g_, b_ = 0, x, c
    elif 240 <= h < 300:
        r_, g_, b_ = x, 0, c
    elif 300 <= h < 360:
        r_, g_, b_ = c, 0, x
    r, g, b = map(lambda x: (x+m)*255, [r_, g_, b_])
    return (r, g, b)

list_pos = [[0, 0] for _ in range(10)]

for line in inp:
    # clock.tick(90)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
    
    op, num = line.split(" ")
    num = int(num)
    for i in range(num):
        match op:
            case 'R':
                list_pos[0][0] += 1
            case 'L':
                list_pos[0][0] -= 1
            case 'U':
                list_pos[0][1] += 1
            case 'D':
                list_pos[0][1] -= 1

        for (p1, p2) in zip(range(9), range(1, 10)):
            match [list_pos[p1][0]-list_pos[p2][0], list_pos[p1][1]-list_pos[p2][1]]:
                case [0, y] if y % 2 == 0:
                    list_pos[p2][1] = int(list_pos[p1][1] - y/2)
                case [x, 0] if x % 2 == 0:
                    list_pos[p2][0] = int(list_pos[p1][0] - x/2)
                case [1, y] | [-1, y] if abs(y) == 2:
                    list_pos[p2][0] = list_pos[p1][0]
                    list_pos[p2][1] = list_pos[p1][1] - y // 2
                case [x, 1] | [x, -1] if abs(x) == 2:
                    list_pos[p2][0] = list_pos[p1][0] - x//2
                    list_pos[p2][1] = list_pos[p1][1]
                case [x, y] if abs(x) == 2 and abs(y) == 2:
                    list_pos[p2][0] = list_pos[p1][0] - x//2
                    list_pos[p2][1] = list_pos[p1][1] - y//2

        for i in range(10):
            t_count[list_pos[i][0]+G_SIZE//2][list_pos[i][1]+G_SIZE//2] += 1

    screen.fill((0, 0, 0))
    t_pixels = [[[x, y] for x in range(len(t_count[y])) if t_count[y][x]] for y in range(len(t_count))]

    pixels = []
    for row in t_pixels:
        for pos in row:
            if pos != []:
                pixels.append(pos)

    for (x, y) in pixels:
        pixel = t_count[y][x]
        pygame.draw.rect(screen, hsvToRGB(1.3*pixel, 0.7, 0.8), (x*scale, y*scale, scale, scale))
    
    for point in list_pos:
        pygame.draw.rect(screen, (255,255, 255), (*map(lambda x: (G_SIZE*scale)//2 + x*scale, [*reversed(point)]), scale, scale))

    pygame.display.update()

time.sleep(5)