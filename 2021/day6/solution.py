from aocd import submit
import bs4
import copier

COMPLETE = False
year, day = [2021, 6]

with open(r"2021\day6\input.txt", 'r') as f:
    inp = [line.strip() for line in f.readlines()]

nums = [*map(int, inp[0].split(","))]
for i in range(80):
    end_val = len(nums)
    for j in range(end_val):
        if nums[j] == 0:
            nums[j] = 6
            nums.append(8)
        else:
            nums[j] -= 1

answer = len(nums)

if COMPLETE:
    r = submit(answer, year=year, day=day)
    soup = bs4.BeautifulSoup(r.text, "html.parser")
    message = soup.article.text
    if "That's the right answer" in message:
        copier.make_next()
else:
    print(answer)
