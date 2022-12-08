from aocd import submit
import bs4
import copier

COMPLETE = True
year, day = [2022, 7]

with open(r"2022\day7\input.txt", 'r') as f:
    inp = f.read()

dir_stack = []
directory = {"/": {}}
for command in inp.split("\n$"):
    if len(command.split("\n")) == 1:
        change = command.split(" ")[-1]
        if change == "..":
            dir_stack.pop()
        elif change == "/":
            dir_stack = ["/"]
        else:
            dir_stack.append(change)
    else:
        result = command.split("\n")[1:]
        for line in result:
            if "dir" in line:
                end_dir = line.split(" ")[-1]
                cur_dir = directory
                for dir in dir_stack:
                    cur_dir = cur_dir[dir]
                if end_dir not in cur_dir:
                    cur_dir[end_dir] = {}
            else:
                size, name  = line.split(" ")
                cur_dir = directory
                for dir in dir_stack:
                    cur_dir = cur_dir[dir]
                cur_dir[name] = int(size)
        

totals = {}
def find_totals(dir: dict, path: str):
    total = 0
    for (key, value) in dir.items():
        if type(value) == int:
            total += value
        else:
            total += find_totals(value, path+f"/{key}")
    
    totals[path] = total

    return total

find_totals(directory, "/")

answer = sum([num for num in totals.values() if num <= 100000])

if COMPLETE:
    r = submit(answer, year=year, day=day)
    soup = bs4.BeautifulSoup(r.text, "html.parser")
    message = soup.article.text
    if "That's the right answer" in message:
        copier.make_next()
else:
    print(answer)