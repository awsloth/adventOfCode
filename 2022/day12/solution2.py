from aocd import submit
import bs4
import copier

COMPLETE = False 
year, day = [2022, 12]

with open(r"2022\day12\input.txt", 'r') as f:
    inp = [line.strip() for line in f.readlines()]

# inp="""Sabqponm
# abcryxxl
# accszExk
# acctuvwj
# abdefghi""".split('\n')

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

i = 1
while not total:
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

    for node in nodes:
        if node.num != -1 and inp[node.y][node.x] == "a":
            total += 1

def printRoute(node):
    if node.notes[-1][1] == "start":
        print(node.x, node.y)
        return
    
    print(node.x, node.y)
    printRoute(node.notes[-1][1])

min_node = float("inf")
for node in nodes:
    if inp[node.y][node.x] == "a" and min_node > node.weight:
        min_node = node.weight

answer = min_node

if COMPLETE:
    submit(answer, year=year, day=day)
else:
    print(answer)
