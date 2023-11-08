COMPLETE = False
year, day = [2022, 21]

def recurFind(cur_monkey, monkeys, ops):
    if type(monkeys[cur_monkey]) is int:
        return monkeys[cur_monkey]
    
    m1, symb, m2 = monkeys[cur_monkey].split(" ")

    return ops[symb](recurFind(m1, monkeys, ops), recurFind(m2, monkeys, ops))

def main(enabled_print=True, test=False):
    if test:
        with open(r"2022\day21\test.txt", 'r') as f:
            inp = [line.strip() for line in f.readlines()]
    else:
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
    
    return recurFind("root", monkeys, ops)

if __name__ == "__main__":
    from aocd import submit

    import bs4
    import copier

    answer = main(not COMPLETE)
    
    if COMPLETE:
        r = submit(answer, year=year, day=day)
        soup = bs4.BeautifulSoup(r.text, "html.parser")
        message = soup.article.text
        if "That's the right answer" in message:
            copier.make_next(year, day)
    else:
        print(answer)
