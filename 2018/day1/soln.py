with open("data.txt", "r") as f:
    contents = [l.strip() for l in f.readlines()]

nums = [int(x) for x in contents]

def gen_ops(ops):
    pos = 0
    while 1:
        yield ops[pos]
        pos += 1
        pos %= len(ops)

operators = gen_ops(nums)

total = 0
covered = []

#while (total not in covered):
#    covered.append(total)
#
#   total += next(operators)

# print(len(covered))

# Alternate solution

sum_nums = [sum(nums[:n]) for n in range(len(nums))]

poss = []
for (i, num1) in enumerate(sum_nums):
    for (j, num2) in enumerate(sum_nums[i+1:]):
        if (num2-num1) % 500 == 0:
            poss.append((num1, num2, abs((num2-num1)//500), i+j+1))

poss.sort(key=lambda x: x[2])
poss.sort(key=lambda x: x[3])

print(poss[0])


