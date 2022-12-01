from aocd import submit
import bs4
import copier
import math

COMPLETE = False
year, day = [2021, 7]

with open(r"2021\day7\input.txt", 'r') as f:
    inp = [line.strip() for line in f.readlines()]

inp = ["16,1,2,0,4,2,7,1,2,14"]

nums = [*map(int, inp[0].split(","))]
num_tots = {}
for num in nums:
    num_tots[num] = nums.count(num)

mean = sum(nums)/len(nums)

answer = 0
for num in num_tots.keys():
    ...

if COMPLETE:
    r = submit(answer, year=year, day=day)
    soup = bs4.BeautifulSoup(r.text, "html.parser")
    message = soup.article.text
    if "That's the right answer" in message:
        copier.make_next()
else:
    print(answer)
