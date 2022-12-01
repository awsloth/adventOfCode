from aocd import submit
import bs4
import copier

root = r"C:\Users\Adam\PythonProjects\adventOfCode\2022"

COMPLETE = False
year, day = [2022, 1]

with open(r"C:\Users\Adam\PythonProjects\adventOfCode\2022\day1\input.txt", 'r') as f:
    inp = [line.strip() for line in f.readlines()]

runningTotal = 0
totals = []
for line in inp:
    if line == '':
        totals.append(runningTotal)
        runningTotal = 0
    else:
        runningTotal += int(line)

answer = max(totals)

if COMPLETE:
    r = submit(answer, year=year, day=day)
    soup = bs4.BeautifulSoup(r.text, "html.parser")
    message = soup.article.text
    if "That's the right answer" in message:
        copier.make_next()
else:
    print(answer)
