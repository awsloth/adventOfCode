from aocd import submit
import bs4
import copier

COMPLETE = True
year, day = [2022, 6]

with open(r"2022\day6\input.txt", 'r') as f:
    inp = [line.strip() for line in f.readlines()]

i = 0
while len(list(set(inp[0][i:i+4]))) < 4:
    i += 1

answer = i + 4

if COMPLETE:
    r = submit(answer, year=year, day=day)
    soup = bs4.BeautifulSoup(r.text, "html.parser")
    message = soup.article.text
    if "That's the right answer" in message:
        copier.make_next()
else:
    print(answer)
