from aocd import submit
import bs4
import copier
import pygame

COMPLETE = False
year, day = [2022, 12]

with open(r"2022\day12\input.txt", 'r') as f:
    inp = [line.strip() for line in f.readlines()]

# inp = """Sabqponm
# abcryxxl
# accszExk
# acctuvwj
# abdefghi""".split('\n')

def findMoves(x, y):
    cur = inp[y][x]
    if cur == "S":
        cur = "a"
    moves = []
    if x > 0 and (ord(inp[y][x-1]) - 1 <= ord(cur) or (inp[y][x-1] == "E" and cur in "yz")):
        moves.append([x-1, y])
    if y > 0 and (ord(inp[y-1][x]) - 1 <= ord(cur)  or (inp[y-1][x] == "E" and cur in "yz")):
        moves.append([x, y-1])
    if x < len(inp[0]) - 1 and (ord(inp[y][x+1]) - 1 <= ord(cur)  or (inp[y][x+1] == "E" and cur in "yz")):
        moves.append([x+1, y])
    if y < len(inp) - 1 and (ord(inp[y+1][x]) - 1 <= ord(cur)  or (inp[y+1][x] == "E" and cur in "yz")):
        moves.append([x, y+1])

    return moves

for (i, line) in enumerate(inp):
    if "S" in line:
        start_pos = [line.index("S"), i]

for (i, line) in enumerate(inp):
    if "E" in line:
        end_pos = [line.index("E"), i]

back = False
cur_pos = start_pos

move_stack = []
pos_stack = []

rejected = []


FACTOR = 4
MARGIN = 10
screen = pygame.display.set_mode((len(inp[0])*FACTOR + MARGIN, len(inp)*FACTOR + MARGIN))

while inp[cur_pos[1]][cur_pos[0]] != "E":
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    screen.fill((255, 255, 255))

    for (s, e) in zip(pos_stack, pos_stack[1:]):
        pygame.draw.line(screen, (0, 0, 0), [*map(lambda x: x*FACTOR + MARGIN//2, s)], [*map(lambda x: x*FACTOR + MARGIN//2, e)])

    if pos_stack != []:
        pygame.draw.line(screen, (0, 0, 0), [*map(lambda x: x*FACTOR + MARGIN//2, pos_stack[-1])], [*map(lambda x: x*FACTOR + MARGIN//2, cur_pos)])

    pygame.draw.circle(screen, (0, 255, 0), [*map(lambda x: x*FACTOR + MARGIN//2, start_pos)], 1)
    pygame.draw.circle(screen, (255, 0, 0), [*map(lambda x: x*FACTOR + MARGIN//2, end_pos)], 1)

    pygame.display.update()

    # If backtracked go back to previous position
    if back:
        cur_pos = pos_stack.pop()
    
    # Find possible moves
    pos_moves = sorted(findMoves(*cur_pos), key=lambda x: inp[x[1]][x[0]], reverse=True)

    pos_moves = [move for move in pos_moves if move not in pos_stack and move not in rejected]

    # If there are no moves backtrack
    if pos_moves == []:
        back = True
        rejected.append(cur_pos)
        continue

    # Choose move based on whether just backtracked or arrived
    if back:
        choice = move_stack.pop() + 1
    else:
        choice = 0

    #print(cur_pos)
    #print(pos_moves)
    #print(move_stack)
    #print(pos_stack)
    #print(choice)

    # If the choice does not exist backtrack
    if len(pos_moves) <= choice:
        back = True
        continue

    # Confirm move
    pos_stack.append(cur_pos)
    move_stack.append(choice)
    cur_pos = pos_moves[choice]

    # Reset back on working loop
    back = False

answer = len(move_stack)

if COMPLETE:
    r = submit(answer, year=year, day=day)
    soup = bs4.BeautifulSoup(r.text, "html.parser")
    message = soup.article.text
    if "That's the right answer" in message:
        copier.make_next()
else:
    print(answer)

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    screen.fill((255, 255, 255))

    for (s, e) in zip(pos_stack, pos_stack[1:]):
        pygame.draw.line(screen, (0, 0, 0), [*map(lambda x: x*FACTOR + MARGIN//2, s)], [*map(lambda x: x*FACTOR + MARGIN//2, e)])

    if pos_stack != []:
        pygame.draw.line(screen, (0, 0, 0), [*map(lambda x: x*FACTOR + MARGIN//2, pos_stack[-1])], [*map(lambda x: x*FACTOR + MARGIN//2, cur_pos)])

    pygame.draw.circle(screen, (0, 255, 0), [*map(lambda x: x*FACTOR + MARGIN//2, start_pos)], 1)
    pygame.draw.circle(screen, (255, 0, 0), [*map(lambda x: x*FACTOR + MARGIN//2, end_pos)], 1)

    pygame.display.update()