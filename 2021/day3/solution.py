from aocd import submit
import bs4
import copier

root = r"C:\Users\Adam\PythonProjects\adventOfCode\2021"

COMPLETE = True
year, day = [2021, 3]

with open(r"C:\Users\Adam\PythonProjects\adventOfCode\2021\day3\input.txt", 'r') as f:
    inp = [line.strip() for line in f.readlines()]

end_num = ""
for i in range(len(inp[0])):
    tally = 0
    for line in inp:
        if line[i] == "1":
            tally += 1

    if tally > len(inp)//2:
        end_num += "1"
    else:
        end_num += "0"

op_end = ""
for c in end_num:
    op_end += "10"[int(c)]

answer = int(end_num, 2) * int(op_end, 2)

if COMPLETE:
    r = submit(answer, year=year, day=day)
    soup = bs4.BeautifulSoup(r.text, "html.parser")
    message = soup.article.text
    if "That's the right answer" in message:
        copier.make_next()
else:
    print(answer)
