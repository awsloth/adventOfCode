COMPLETE = False
year, day = [2021, 8]

def main(enabled_print=True, test=False):
    if test:
        with open(r"2021\day8\test.txt", 'r') as f:
            inp = [line.strip() for line in f.readlines()]
    else:
        with open(r"2021\day8\input.txt", 'r') as f:
            inp = [line.strip() for line in f.readlines()]
    
    a = [2, 3, 6, 7, 8]
    b = [4, 8]
    c = [1, 3, 4, 7, 8]
    d = [2, 3, 4, 8]
    e = [8]
    f = [1, 3, 4, 6, 7, 8, 9, 0]
    g = [2, 3, 5, 6, 8, 9, 0]
    containing = [a, b, c, d, e, f, g]
    
    vals = {
        1:set('cf'), 2:set('acdeg'), 3:set('acdfg'), 4:set('bcdf'), 5:set('abdfg'),
        6:set('abdefg'), 7:set('acf'), 8:set('abcdefg'), 9:set('abcdfg'), 0:set('abcefg')}
    
    answer = 0
    for line in inp:
        num_dict = {}
        nums = []
        for set_n in line.split("|"):
            nums += set_n.split(" ")
        for num in nums:
            if len(num) == 2:
                num_dict[1] = num
            elif len(num) == 3:
                num_dict[7] = num
            elif len(num) == 4:
                num_dict[4] = num
            elif len(num) == 7:
                num_dict[8] = num
            elif len(num) == 5:
                for dig in [2, 3, 5]:
                    if dig not in num_dict:
                        num_dict[dig] = []
                    if set(num) not in [*map(set, num_dict[dig])]:
                        num_dict[dig].append(num)
            elif len(num) == 6:
                for dig in [0, 6, 9]:
                    if dig not in num_dict:
                        num_dict[dig] = []
                    if set(num) not in [*map(set, num_dict[dig])]:
                        num_dict[dig].append(num)
    
        if len(set(num_dict[2][0]).intersection(set(num_dict[2][1]))) == 3:
            num_dict[3] = num_dict[2][2]
            num_dict[2] = [num_dict[2][0], num_dict[2][1]]
            num_dict[5] = [num_dict[2][0], num_dict[2][1]]
        elif len(set(num_dict[2][0]).intersection(set(num_dict[2][2]))) == 3:
            num_dict[3] = num_dict[2][1]
            num_dict[2] = [num_dict[2][0], num_dict[2][2]]
            num_dict[5] = [num_dict[2][0], num_dict[2][1]]
        else:
            num_dict[3] = num_dict[2][0]
            num_dict[2] = [num_dict[2][1], num_dict[2][2]]
            num_dict[5] = [num_dict[2][0], num_dict[2][1]]
    
        pos = ['' for _ in range(len(containing))]
        for (i, p) in enumerate(containing):
            if type(num_dict[p[0]]) == list:
                c_set = set(num_dict[p[0]][0])
                for _set in num_dict[p[0]][1:]:
                    c_set = c_set.intersection(set(_set))
            else:
                c_set = set(num_dict[p[0]])
            for num in p[1:]:
                if type(num_dict[num]) == list:
                    for val in num_dict[num]:
                        c_set = c_set.intersection(set(val))
                else:
                    c_set = c_set.intersection(set(num_dict[num]))
                
    
            pos[i] = c_set
            
        actual = ['' for _ in range(7)]
        while len([c for c in actual if c == '']) >= 1:
            for (i, p) in enumerate(pos):
                if len(p) == 1:
                    actual[i] = list(p)[0]
            
            for item in actual:
                for _set in pos:
                    _set.discard(item)
    
        actual = dict(zip(actual, 'abcdefg'))
    
        end_nums = ""
        for num in line.split("|")[1].split(" "):
            num = "".join([actual[c] for c in num])
            for (key, item) in vals.items():
                if len(item.difference(set(num))) == 0 and len(set(num).difference(item)) == 0:
                    end_nums += str(key)
    
        answer += int(end_nums)

    return answer
    
if __name__ == "__main__":
    from aocd import submit

    answer = main(not COMPLETE)
    
    if COMPLETE:
        r = submit(answer, year=year, day=day)
    else:
        print(answer)

