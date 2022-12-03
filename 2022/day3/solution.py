from aocd import submit
import bs4
import copier

COMPLETE = True
year, day = [2022, 3]

with open(r"2022\day3\input.txt", 'r') as f:
    inp = [line.strip() for line in f.readlines()]

answer = 0
for line in inp:
    h1, h2 = line[:len(line)//2], line[len(line)//2:]
    c = list(set(h1).intersection(set(h2)))[0]
    prior = ord(c.upper()) - 64
    if c.upper() == c:
        prior += 26
    answer += prior

if COMPLETE:
    r = submit(answer, year=year, day=day)
    soup = bs4.BeautifulSoup(r.text, "html.parser")
    message = soup.article.text
    if "That's the right answer" in message:
        copier.make_next()
else:
    print(answer)
