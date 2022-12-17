import pygame
import time

scale = 3
width, height = 173, 41
screen = pygame.display.set_mode((width*scale, height*scale))

with open(r"2022\day12\input.txt", 'r') as f:
    inp = [line.strip() for line in f.readlines()]

class Node:
    def __init__(self, connections, x, y):
        self.connections = connections
        self.node_cons = []
        self.notes = []
        self.num = -1
        self.weight = float("inf")
        self.x = x
        self.y = y
        self.prev = -1

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
    if cur == "S":
        cur = "a"
    moves = []
    if x > 0 and ((ord(inp[y][x-1]) - 1 <= ord(cur) and inp[y][x-1] != "E") or (inp[y][x-1] == "E" and cur in "yz")):
        moves.append([x-1, y])
    if y > 0 and ((ord(inp[y-1][x]) - 1 <= ord(cur) and inp[y-1][x] != "E")  or (inp[y-1][x] == "E" and cur in "yz")):
        moves.append([x, y-1])
    if x < len(inp[0]) - 1 and ((ord(inp[y][x+1]) - 1 <= ord(cur) and inp[y][x+1] != "E")  or (inp[y][x+1] == "E" and cur in "yz")):
        moves.append([x+1, y])
    if y < len(inp) - 1 and ((ord(inp[y+1][x]) - 1 <= ord(cur) and inp[y+1][x] != "E")  or (inp[y+1][x] == "E" and cur in "yz")):
        moves.append([x, y+1])

    return moves

for (i, line) in enumerate(inp):
    if "S" in line:
        start_pos = [line.index("S"), i]

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

pygame.draw.rect(screen, (255, 255, 255), (start_pos[0]*scale, start_pos[1]*scale, scale, scale))
pygame.display.flip()

i = 1
while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
    
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
    saved[0].prev = saved[0].notes[-1][1]

    pygame.draw.rect(screen, (255, 255, 255), (saved[0].x*scale, saved[0].y*scale, scale, scale))
    pygame.display.flip()

    if inp[saved[0].y][saved[0].x] == "E":
        break

answer = saved[0].weight

def findRoute(node):
    if type(node.prev) != Node:
        return [[node.x, node.y]]
    
    l = findRoute(node.prev)
    l.append([node.x, node.y])

    return l

path = findRoute(saved[0])

for (x, y) in path:
    pygame.draw.rect(screen, (255, 0, 0), (x*scale, y*scale, scale, scale))
    pygame.display.flip()

time.sleep(5)