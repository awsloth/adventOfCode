COMPLETE = False
year, day = [2022, 21]

def recurFind(cur_monkey, monkeys, _ops):
    if type(monkeys[cur_monkey]) is int:
        if cur_monkey == "humn":
            return 'x'
        return monkeys[cur_monkey]
    
    m1, symb, m2 = monkeys[cur_monkey].split(" ")

    m1_num = recurFind(m1, monkeys, _ops)
    m2_num = recurFind(m2, monkeys, _ops)

    if type(m1_num) in [int, float] and type(m2_num) in [int, float]:
        return _ops[symb](m1_num, m2_num)

    return [m1_num, symb, m2_num]


def main(enabled_print=True, test=False):
    if test:
        with open(r"2022\day21\test.txt", 'r') as f:
            inp = [line.strip() for line in f.readlines()]
    else:
        with open(r"2022\day21\input.txt", 'r') as f:
            inp = [line.strip() for line in f.readlines()]
    
    monkeys = {}
    _ops = {'*': lambda x, y: x * y, '/': lambda x, y: x // y, '-': lambda x, y: x - y, '+':lambda x, y: x + y}
    reverse = {'/': lambda x, y: x * y, '*': lambda x, y: x // y, '+': lambda x, y: x - y, '-':lambda x, y: x + y}
    
    for line in inp:
        name, operation = line.split(":")
        operation = operation[1:]
        just_num = True
        for op in _ops.keys():
            if op in operation:
                just_num = False
                break
    
        if just_num:
            monkeys[name] = int(operation)
        else:
            monkeys[name] = operation
    
    m1, symb, m2 = monkeys["root"].split(" ")
    
    m1_ans = recurFind(m1, monkeys, _ops)
    m2_ans = recurFind(m2, monkeys, _ops)
    
    if enabled_print:
        print(m1_ans)
        print(m2_ans)
    
    if type(m1_ans) in [int, float]:
        answer = m1_ans
        ops = m2_ans
    elif type(m2_ans) in [int, float]:
        answer = m2_ans
        ops = m1_ans
    
    while ops != 'x':
    
        cur_op = ops[1]
        if type(ops[0]) in [int, float]:
            pos = 'l'
            num = ops[0]
            ops = ops[2]
        elif type(ops[2]) in [int, float]:
            pos = 'r'
            num = ops[2]
            ops = ops[0]
    
        if enabled_print:
            print(num, cur_op, answer)
    
        if cur_op in ['*', '+']:
            answer = reverse[cur_op](answer, num)
    
        else:
            if pos == 'l':
                answer = _ops[cur_op](num, answer)
            elif pos == 'r':
                answer = reverse[cur_op](answer, num)

    return answer
    
if __name__ == "__main__":
    from aocd import submit

    answer = main(not COMPLETE)
    
    if COMPLETE:
        r = submit(answer, year=year, day=day)
    else:
        print(answer)

