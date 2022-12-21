from aocd import submit
import bs4
import copier

COMPLETE = True
year, day = [2022, 21]

with open(r"2022\day21\input.txt", 'r') as f:
    inp = [line.strip() for line in f.readlines()]

monkeys = {}
ops = {'*': lambda x, y: x*y, '/': lambda x, y: x // y, '-': lambda x, y: x - y, '+':lambda x, y: x + y}

for line in inp:
    name, operation = line.split(":")
    operation = operation[1:]
    just_num = True
    for op in ops.keys():
        if op in operation:
            just_num = False
            break

    if just_num:
        monkeys[name] = int(operation)
    else:
        monkeys[name] = operation
        
def recurFind(cur_monkey):
    if type(monkeys[cur_monkey]) is int:
        return monkeys[cur_monkey]
    
    m1, symb, m2 = monkeys[cur_monkey].split(" ")

    return ops[symb](recurFind(m1), recurFind(m2))

answer = recurFind("root")

if COMPLETE:
    r = submit(answer, year=year, day=day)
    soup = bs4.BeautifulSoup(r.text, "html.parser")
    message = soup.article.text
    if "That's the right answer" in message:
        copier.make_next()
else:
    print(answer)
