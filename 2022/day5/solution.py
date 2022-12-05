from aocd import submit
import bs4
import copier

COMPLETE = False
year, day = [2022, 5]

with open(r"2022\day5\input.txt", 'r') as f:
    inp = [line.strip() for line in f.readlines()]

answer = inp

if COMPLETE:
    r = submit(answer, year=year, day=day)
    soup = bs4.BeautifulSoup(r.text, "html.parser")
    message = soup.article.text
    if "That's the right answer" in message:
        copier.make_next()
else:
    print(answer)
