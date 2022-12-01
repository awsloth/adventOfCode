from aocd import get_data
import datetime
import os
import webbrowser

now = datetime.datetime.now()

if now.hour >= 5:
    cur_day = now.day
else:
    cur_day = now.day - 1

year = now.year

root = os.getcwd()

base_file = f'''from aocd import submit
import bs4
import copier

root = r"{os.path.join(root, str(year))}"

COMPLETE = False
year, day = [{year}, {cur_day}]

with open(r"{os.path.join(root, str(year), f'day{cur_day}', 'input.txt')}", 'r') as f:
    inp = [line.strip() for line in f.readlines()]

answer = inp

if COMPLETE:
    r = submit(answer, year=year, day=day)
    soup = bs4.BeautifulSoup(r.text, "html.parser")
    message = soup.article.text
    if "That's the right answer" in message:
        copier.make_next()
else:
    print(answer)
'''

copier_content=f'''import os

def make_next():
    root = '{root}'

    year, day = {year}, {cur_day}

    if not os.path.exists(os.path.join(root, str(year), f"day{cur_day}", "solution2.py")):
        with open(os.path.join(root, str(year), f"day{cur_day}", "solution.py"), "r") as f:
            with open(os.path.join(root, str(year), f"day{cur_day}", "solution2.py"), "w") as f1:
                for line in f.readlines():
                    f1.write(line)
'''

if not os.path.exists(os.path.join(root, str(year), f"day{cur_day}")):
    os.makedirs(f"{year}/day{cur_day}")
    with open(f"{year}/day{cur_day}/input.txt", 'w') as f:
        content = get_data(year=year, day=cur_day)
        f.write(content)
    
    with open(f"{year}/day{cur_day}/solution.py", 'w') as f:
        f.write(base_file)

    phrase_replace = {"$year$":str(year), "$day$":str(cur_day), "$root$":root}
    with open("base_copier.txt", "r") as s:
        with open(f"{year}/day{cur_day}/copier.py", 'w') as f:
            for line in s.readlines():
                new_line = line
                for (key, value) in phrase_replace.items():
                    if key in new_line:
                        x = new_line.find(key)
                        new_line = new_line[:x] + value + new_line[x+len(key):]
                
                f.write(new_line)