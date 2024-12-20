COMPLETE = False
year, day = [2022, 7]

def find_totals(dir: dict, path: str, totals):
    total = 0
    for (key, value) in dir.items():
        if type(value) == int:
            total += value
        else:
            _, val = find_totals(value, path+f"/{key}", totals)
            total += val
    
    totals[path] = total

    return (totals, total)

def main(enabled_print=True, test=False):
    if test:
        with open(r"2022\day7\test.txt", 'r') as f:
            inp = f.read()
    else:
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
            
    
    totals, _ = find_totals(directory, "/", {})
    
    return min([num for num in totals.values() if num > 30000000+totals["/"]-70000000])
    
if __name__ == "__main__":
    from aocd import submit

    answer = main(not COMPLETE)
    
    if COMPLETE:
        r = submit(answer, year=year, day=day)
    else:
        print(answer)

