from aocd import submit
import bs4
import copier

COMPLETE = True
year, day = [2022, 2]

with open(r"2022\day2\input.txt", 'r') as f:
    inp = [line.strip() for line in f.readlines()]

answer = 0
for line in inp:
    p_2 = {"X":"A", "Y":"B", "Z":"C"}
    p_2_score = {"A":1, "B":2, "C":3}
    loss = {"A":"B", "B":"C", "C":"A"}
    p1, p2 = line.split()
    p2 = p_2[p2]
    if p1 == p2:
        answer += 3 + p_2_score[p2]
    elif loss[p1] == p2:
        answer += 6 + p_2_score[p2]
    else:
        answer += p_2_score[p2]

if COMPLETE:
    r = submit(answer, year=year, day=day)
    soup = bs4.BeautifulSoup(r.text, "html.parser")
    message = soup.article.text
    if "That's the right answer" in message:
        copier.make_next()
else:
    print(answer)
