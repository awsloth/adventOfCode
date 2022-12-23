COMPLETE = False
year, day = [2022, 13]

def strToList(string):
    c_list = []
    depth = 0
    cur_nums = ""
    for c in string:
        n_list = c_list
        for _ in range(depth):
            n_list = n_list[-1]
        
        if c == "[":
            if cur_nums not in ['', ',']:
                n_list += [*map(int, [num for num in cur_nums.split(",") if num != ""])]

            cur_nums = ""

            n_list.append([])
            depth += 1
        elif c != "]":
            cur_nums += c
        else:
            if cur_nums not in ['', ',']:
                n_list += [*map(int, [num for num in cur_nums.split(",") if num != ""])]

            cur_nums = ""

            depth -= 1

    return c_list[0]

def recurSum(left, right):
    if type(left) != type(right):
        if type(left) is not list:
            left = [left]
        else:
            right = [right]

    if type(left) is int:
        if left < right:
            return 1
        elif right < left:
            return -1
    else:        
        for (l, r) in zip(left, right):
            s = recurSum(l, r)
            if s != 0:
                return s

        if len(right) > len(left):
            return 1
        
        elif len(left) > len(right):
            return -1

    return 0

def main(enabled_print=True, test=False):
    import functools

    if test:
        with open(r"2022\day13\test.txt", 'r') as f:
            inp = f.read()
    else:
        with open(r"2022\day13\input.txt", 'r') as f:
            inp = f.read()
    
    answer = 0
    codes = [[[2]],[[6]]]
    for pair in inp.split("\n\n"):
        codes += [*map(strToList, pair.split("\n"))]
    
    codes = sorted(codes, key=functools.cmp_to_key(recurSum), reverse=True)
    
    index1 = codes.index([[2]]) + 1
    index2 = codes.index([[6]]) + 1
    
    return index1*index2
    
if __name__ == "__main__":
    from aocd import submit

    answer = main(not COMPLETE)
    
    if COMPLETE:
        r = submit(answer, year=year, day=day)
    else:
        print(answer)

