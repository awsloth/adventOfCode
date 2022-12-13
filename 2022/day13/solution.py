from aocd import submit
import bs4
import copier

COMPLETE = True
year, day = [2022, 13]

with open(r"2022\day13\input.txt", 'r') as f:
    inp = f.read()

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
        
answer = 0
for (i, pair) in enumerate(inp.split("\n\n")):
    added = False
    left, right = map(strToList, pair.split("\n"))
    for (l, r) in zip(left, right):
        s = recurSum(l, r)
        if s == 1:
            if not added:
                answer += i + 1
                added = True
        elif s == -1:
            added = True
            break

    if len(right) > len(left):
        if not added:
            answer += i + 1
    elif len(right) < len(left):
        continue
    

if COMPLETE:
    r = submit(answer, year=year, day=day)
    soup = bs4.BeautifulSoup(r.text, "html.parser")
    message = soup.article.text
    if "That's the right answer" in message:
        copier.make_next()
else:
    print(answer)
