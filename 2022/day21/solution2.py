from aocd import submit
import bs4
import copier

COMPLETE = False 
year, day = [2022, 21]

with open(r"2022\day21\input.txt", 'r') as f:
    inp = [line.strip() for line in f.readlines()]

# inp = """root: pppw + sjmn
# dbpl: 5
# cczh: sllz + lgvd
# zczc: 2
# ptdq: humn - dvpt
# dvpt: 3
# lfqf: 4
# humn: 5
# ljgn: 2
# sjmn: drzm * dbpl
# sllz: 4
# pppw: cczh / lfqf
# lgvd: ljgn * ptdq
# drzm: hmdt - zczc
# hmdt: 32""".split('\n')

monkeys = {}
_ops = {'*': lambda x, y: x * y, '/': lambda x, y: x / y, '-': lambda x, y: x - y, '+':lambda x, y: x + y}
reverse = {'/': lambda x, y: x * y, '*': lambda x, y: x / y, '+': lambda x, y: x - y, '-':lambda x, y: x + y}

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
        
def recurFind(cur_monkey):
    if type(monkeys[cur_monkey]) is int:
        if cur_monkey == "humn":
            return 'x'
        return monkeys[cur_monkey]
    
    m1, symb, m2 = monkeys[cur_monkey].split(" ")

    m1_num = recurFind(m1)
    m2_num = recurFind(m2)

    if type(m1_num) in [int, float] and type(m2_num) in [int, float]:
       return _ops[symb](m1_num, m2_num)

    return [m1_num, symb, m2_num]
    

m1, symb, m2 = monkeys["root"].split(" ")

m1_ans = recurFind(m1)
m2_ans = recurFind(m2)

print(m1_ans)
print(m2_ans)

if type(m1_ans) in [int, float]:
    answer = m1_ans
    ops = m2_ans
elif type(m2_ans) in [int, float]:
    answer = m2_ans
    ops = m1_ans

top = answer
bottom = answer

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

    print(num, cur_op, answer)

    if cur_op in ['*', '+']:
        answer = reverse[cur_op](answer, num)

    else:
        if pos == 'l':
            answer = _ops[cur_op](num, answer)
        elif pos == 'r':
            answer = reverse[cur_op](answer, num)

if COMPLETE:
    submit(answer, year=year, day=day)
else:
    print(answer)
