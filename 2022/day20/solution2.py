COMPLETE = False
year, day = [2022, 20]

def main(enabled_print=True, test=False):
    if test:
        with open(r"2022\day20\test.txt", 'r') as f:
            inp = [line.strip() for line in f.readlines()]
    else:
        with open(r"2022\day20\input.txt", 'r') as f:
            inp = [line.strip() for line in f.readlines()]
    
    decrypt_key = 811589153
    
    orig = [int(l) for l in inp]
    order = [[int(line)*decrypt_key, i] for (i, line) in enumerate(inp)]
    for k in range(10):
        pos = 0
        while pos < len(order):
            for (i, number) in enumerate(order):
                if number[1] == pos:
                    next_num = i
                    break
    
            if order[next_num][0] == 0:
                pos += 1
                continue
    
            new_index = (next_num + order[next_num][0]) % (len(order) - 1)
            
            temp = order.pop(next_num)
            
            order.insert(new_index, temp)
    
            pos += 1
        
        if enabled_print:
            print(k)
    
    order = [o[0] for o in order]
    zero = order.index(0)
    
    if enabled_print:
        print(order[(1000+zero)%len(order)])
        print(order[(2000+zero)%len(order)])
        print(order[(3000+zero)%len(order)])
    
    return order[(1000+zero)%len(order)] + order[(2000+zero)%len(order)] + order[(3000+zero)%len(order)]
    
if __name__ == "__main__":
    from aocd import submit

    answer = main(not COMPLETE)
    
    if COMPLETE:
        r = submit(answer, year=year, day=day)
    else:
        print(answer)

