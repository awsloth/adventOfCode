from aocd import submit
import bs4
import copier

COMPLETE = True
year, day = [2022, 4]

with open(r"2022\day4\input.txt", 'r') as f:
    inp = [line.strip() for line in f.readlines()]

def cRange(str):
    a1, a2 = map(int, str.split("-"))
    return [*range(a1, a2+1)]

answer = 0
for line in inp:
    r1, r2 = map(cRange, line.split(","))
    if set(r1).issubset(set(r2)) or set(r2).issubset(set(r1)):
        answer += 1
    

if COMPLETE:
    r = submit(answer, year=year, day=day)
    soup = bs4.BeautifulSoup(r.text, "html.parser")
    message = soup.article.text
    if "That's the right answer" in message:
        copier.make_next()
else:
    print(answer)
