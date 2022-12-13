from aocd import submit
import bs4
import copier

COMPLETE = False
year, day = [2022, 12]

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

i = 1
while 1:
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

    if inp[saved[0].y][saved[0].x] == "E":
        break

def printRoute(node):
    if node.notes[-1][1] == "start":
        print(node.x, node.y)
        return
    
    print(node.x, node.y)
    printRoute(node.notes[-1][1])

answer = saved[0].weight

# printRoute(saved[0])

if COMPLETE:
    r = submit(answer, year=year, day=day)
    soup = bs4.BeautifulSoup(r.text, "html.parser")
    message = soup.article.text
    if "That's the right answer" in message:
        copier.make_next()
else:
    copier.make_next() # print(answer)