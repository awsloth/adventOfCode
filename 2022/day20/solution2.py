from aocd import submit

COMPLETE = False 
year, day = [2022, 20]

with open(r"2022\day20\input.txt", 'r') as f:
    inp = [line.strip() for line in f.readlines()]

# inp = """1
# 2
# -3
# 3
# -2
# 0
# 4""".split('\n')

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
    
    print(k)

order = [o[0] for o in order]
zero = order.index(0)

print(order[(1000+zero)%len(order)])
print(order[(2000+zero)%len(order)])
print(order[(3000+zero)%len(order)])

answer = order[(1000+zero)%len(order)] + order[(2000+zero)%len(order)] + order[(3000+zero)%len(order)]

if COMPLETE:
    submit(answer, year=year, day=day)
else:
    print(answer)
