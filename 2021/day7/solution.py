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
        total += abs(key-num) * val
    
    return total

nums = [*map(int, inp[0].split(","))]
num_tots = {}
for num in nums:
    num_tots[num] = nums.count(num)

best = float('inf')
for num in num_tots.keys():
    cur_dist = get_dist(num, num_tots)
    if cur_dist < best:
        best = cur_dist

answer = best

if COMPLETE:
    r = submit(answer, year=year, day=day)
    soup = bs4.BeautifulSoup(r.text, "html.parser")
    message = soup.article.text
    if "That's the right answer" in message:
        copier.make_next()
else:
    print(answer)
