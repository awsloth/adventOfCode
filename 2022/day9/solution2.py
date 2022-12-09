from aocd import submit
import bs4
import copier

COMPLETE = True
year, day = [2022, 9]

with open(r"2022\day9\input.txt", 'r') as f:
    inp = [line.strip() for line in f.readlines()]


G_SIZE = 600
t_count = [[0 for _ in range(G_SIZE)] for __ in range(G_SIZE)]
grid = [['.' for _ in range(G_SIZE)] for __ in range(G_SIZE)]
list_pos = [[0, 0] for _ in range(10)]
for line in inp:
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


        t_count[list_pos[9][0]+G_SIZE//2][list_pos[9][1]+G_SIZE//2] += 1


answer = sum([len(row)-row.count(0) for row in t_count])

if COMPLETE:
    r = submit(answer, year=year, day=day)
    soup = bs4.BeautifulSoup(r.text, "html.parser")
    message = soup.article.text
    if "That's the right answer" in message:
        copier.make_next()
else:
    print(answer)
