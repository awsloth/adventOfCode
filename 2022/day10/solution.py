from aocd import submit
import bs4
import copier

COMPLETE = True
year, day = [2022, 10]

with open(r"2022\day10\input.txt", 'r') as f:
    inp = [line.strip() for line in f.readlines()]

instructions = [1]
for line in inp:
    if line.split(" ")[0] == "addx":
        instructions.append("addS")
        instructions.append(int(line.split(" ")[1]))
    else:
        instructions.append("noop")

up_to_vals = [*range(20, len(instructions), 40)]
answer = 0
for val in up_to_vals:
    answer += val * (sum([i for i in instructions[:val] if type(i) is int]))

if COMPLETE:
    r = submit(answer, year=year, day=day)
    soup = bs4.BeautifulSoup(r.text, "html.parser")
    message = soup.article.text
    if "That's the right answer" in message:
        copier.make_next()
else:
    print(answer)
