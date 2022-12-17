import pygame
import time

scale = 3
width, height = 173, 41
screen = pygame.display.set_mode((width*scale, height*scale))

with open(r"2022\day12\input.txt", 'r') as f:
    inp = [line.strip() for line in f.readlines()]

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

class Node:
    def __init__(self, connections, x, y):
        self.connections = connections
        self.node_cons = []
        self.notes = []
        self.num = -1
        self.weight = float("inf")
        self.x = x
        self.y = y

    def update(self):
        for node in self.node_cons:
            if node.num == -1:
                if node.notes != []:
                    if node.notes[-1][0] > self.weight + 1:
                        node.notes.append([self.weight + 1, self])
                else:
                    node.notes.append([self.weight + 1, self])

def findMoves(x, y):
    cur = inp[y][x]
    moves = []
    if x > 0 and ord(inp[y][x-1]) + 1 >= ord(cur):
        moves.append([x-1, y])
    if y > 0 and ord(inp[y-1][x]) + 1 >= ord(cur):
        moves.append([x, y-1])
    if x < len(inp[0]) - 1 and ord(inp[y][x+1]) + 1 >= ord(cur):
        moves.append([x+1, y])
    if y < len(inp) - 1 and ord(inp[y+1][x]) + 1 >= ord(cur):
        moves.append([x, y+1])

    return moves

for (i, line) in enumerate(inp):
    if "E" in line:
        start_pos = [line.index("E"), i]
    if "S" in line:
        s_pos = [line.index("S"), i]

inp[start_pos[1]] = inp[start_pos[1]][:start_pos[0]] + "z" + inp[start_pos[1]][start_pos[0] + 1:]
inp[s_pos[1]] = inp[s_pos[1]][:s_pos[0]] + "a" + inp[s_pos[1]][s_pos[0] + 1:]

grid = [[Node(findMoves(i, j), i, j) for i in range(len(inp[j]))] for j in range(len(inp))]

nodes = []

for row in grid:
    for node in row:
        for pos in node.connections:
            node.node_cons.append(grid[pos[1]][pos[0]])

        nodes.append(node)

grid[start_pos[1]][start_pos[0]].num = 1
grid[start_pos[1]][start_pos[0]].weight = 0
grid[start_pos[1]][start_pos[0]].notes = [[0, "start"]]

total = 0

pygame.draw.rect(screen, hsvToRGB(0, 0.6, 0.7), (start_pos[0]*scale, start_pos[1]*scale, scale, scale))
pygame.display.flip()


i = 1
while not total:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
    
    complete = True
    for node in nodes:
        if node.num == i:
            node.update()

    saved = [nodes[0], float("inf")]
    for node in nodes:
        if node.notes != [] and node.notes[-1][0] < saved[1] and node.num == -1:
            saved = [node, node.notes[-1][0]]
    
    i += 1
    saved[0].num = i
    saved[0].weight = saved[0].notes[-1][0]

    pygame.draw.rect(screen, hsvToRGB(saved[0].weight, 0.6, 0.7), (saved[0].x*scale, saved[0].y*scale, scale, scale))
    pygame.display.flip()

    total = 1
    for node in nodes:
    #    if node.num != -1 and inp[node.y][node.x] == "a":
    #        total += 1
        if node.num == -1:
            total = 0
            break

def getRoute(node):
    if node.notes[-1][1] == "start":
        return [[node.x, node.y]]

    l = getRoute(node.notes[-1][1])
    l.append([node.x, node.y])
    return l

m_node = nodes[0]
min_node = float("inf")
for node in nodes:
    if inp[node.y][node.x] == "a" and min_node > node.weight:
        min_node = node.weight
        m_node = node

# print(m_node)
# path = getRoute(m_node)
# for (x, y) in path:
#     pygame.draw.rect(screen, (255, 255, 255), (x*scale, y*scale, scale, scale))
#     pygame.display.flip()

answer = min_node
time.sleep(3)