from aocd import submit
import bs4
import copier
import math

COMPLETE = True
year, day = [2021, 7]

with open(r"2021\day7\input.txt", 'r') as f:
    inp = [line.strip() for line in f.readlines()]

def get_dist(num, nums):
    total = 0
    for (key, val) in nums.items():
        n = abs(key-num)
        total += (n * (n + 1) // 2) * val
    
    return total

nums = [*map(int, inp[0].split(","))]
num_tots = {}
for num in nums:
    num_tots[num] = nums.count(num)

best = float('inf')
for num in range(min(nums), max(nums)+1):
    cur_dist = get_dist(num, num_tots)
    if cur_dist < best:
        best = cur_dist

answer = best

if COMPLETE:
    submit(answer, year=year, day=day)
else:
    print(answer)
