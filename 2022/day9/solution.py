from aocd import submit
import bs4
import copier

COMPLETE = True
year, day = [2022, 9]

with open(r"2022\day9\input.txt", 'r') as f:
    inp = [line.strip() for line in f.readlines()]

G_SIZE = 500
t_count = [[0 for _ in range(G_SIZE)] for __ in range(G_SIZE)]
h_pos = [0, 0]
t_pos = [0, 0]
for line in inp:
    op, num = line.split(" ")
    num = int(num)
    for i in range(num):
        match op:
            case 'R':
                h_pos[0] += 1
            case 'L':
                h_pos[0] -= 1
            case 'U':
                h_pos[1] += 1
            case 'D':
                h_pos[1] -= 1

        match [h_pos[0]-t_pos[0], h_pos[1]-t_pos[1]]:
            case [0, y]:
                if (y % 2) == 0:
                    t_pos[1] = int(h_pos[1] - y/2)
            case [x, 0]:
                if (x % 2) == 0:
                    t_pos[0] = int(h_pos[0] - x/2)
            case [1, 2] | [-1, 2]:
                t_pos[0] = h_pos[0]
                t_pos[1] = h_pos[1] - 1
            case [1, -2] | [-1, -2]:
                t_pos[0] = h_pos[0]
                t_pos[1] = h_pos[1] + 1
            case [2, 1] | [2, -1]:
                t_pos[0] = h_pos[0] - 1
                t_pos[1] = h_pos[1]
            case [-2, 1] | [-2, -1]:
                t_pos[0] = h_pos[0] + 1
                t_pos[1] = h_pos[1]

        t_count[t_pos[0]][t_pos[1]] += 1


answer = sum([len(row)-row.count(0) for row in t_count])

if COMPLETE:
    r = submit(answer, year=year, day=day)
    soup = bs4.BeautifulSoup(r.text, "html.parser")
    message = soup.article.text
    if "That's the right answer" in message:
        copier.make_next()
else:
    print(answer)
