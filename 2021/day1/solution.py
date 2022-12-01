from aocd import submit
import bs4
import copier

COMPLETE = True
year, day = [2021, 1]

with open(r"2021\day1\input.txt", 'r') as f:
    inp = [line.strip() for line in f.readlines()]

answer = 0
for (prev, line) in zip(inp, inp[1:]):
    if int(prev) < int(line):
        answer += 1


if COMPLETE:
    r = submit(answer, year=year, day=day)
    soup = bs4.BeautifulSoup(r.text, "html.parser")
    message = soup.article.text
    if "That's the right answer" in message:
        copier.make_next()
else:
    print(answer)
