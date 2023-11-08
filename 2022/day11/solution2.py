COMPLETE = False
year, day = [2022, 11]

class Monkey:
    def __init__(self, _list, op, t_num):
        self.list = _list
        self.op = op
        self.t_num = t_num
        self.inspect_count = 0

    def performGo(self, val):
        for item in self.list:
            item = self.op(item)
            item = item % val

            if (item % self.t_num) == 0:
                self.t_list.get(item)
            else:
                self.f_list.get(item)
            
            self.inspect_count += 1

        self.list = []

    def get(self, item):
        self.list.append(item)

def add(x, y):
    return x + y

def times(x, y):
    return x * y

def main(enabled_print=True, test=False):
    if test:
        with open(r"2022\day11\test.txt", 'r') as f:
            inp = f.read()
    else:
        with open(r"2022\day11\input.txt", 'r') as f:
            inp = f.read()
    
    functions = {"+":add, "*": times} 
    
    monkeys = []
    tests = []
    
    for monkey in inp.split("\n\n"):
        index, items, op, _test, true, false = monkey.split("\n")
        index = index.split("Monkey ")[0]
        items = [*map(int, items.split(":")[-1].split(","))]
        op = op.split("= ")[-1]
        if "+" in op:
            symbol = "+"
        else:
            symbol = "*"
        second = op.split(symbol)[-1]
        if second == " old":
            def func(x, symbol=symbol):
                return functions[symbol](x, x)
        else:
            num = int(second)
            def func(x, symbol=symbol, num=num):
                return functions[symbol](x, num)
        
        _test = int(_test.split("by ")[-1])
        true = int(true.split("monkey ")[-1])
        false = int(false.split("monkey ")[-1])
        monkeys.append([Monkey(items, func, _test), true, false])
        tests.append(_test)
    
    DIV_VAL = 1
    for _test in tests:
        DIV_VAL *= _test
    
    for monkey in monkeys:
        monkey[0].t_list = monkeys[monkey[1]][0]
        monkey[0].f_list = monkeys[monkey[2]][0]
    
    monkeys = [m[0] for m in monkeys]
    
    for i in range(10000):
        for monkey in monkeys:
            monkey.performGo(DIV_VAL)
    
    monkeys = sorted(monkeys, key = lambda x: x.inspect_count, reverse=True)
    return monkeys[0].inspect_count * monkeys[1].inspect_count
    
if __name__ == "__main__":
    from aocd import submit

    answer = main(not COMPLETE)
    
    if COMPLETE:
        r = submit(answer, year=year, day=day)
    else:
        print(answer)

