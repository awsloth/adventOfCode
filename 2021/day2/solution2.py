COMPLETE = False
year, day = [2021, 2]

def main(enabled_print=True, test=False):
    if test:
        with open(r"2021\day2\test.txt", 'r') as f:
            inp = [line.strip() for line in f.readlines()]
    else:
        with open(r"2021\day2\input.txt", 'r') as f:
            inp = [line.strip() for line in f.readlines()]
    
    h_pos = 0
    depth = 0
    aim = 0
    
    for line in inp:
        if "forward" in line:
            h_pos += int(line[7:])
            depth += aim * int(line[7:])
        elif "up" in line:
            aim -= int(line[2:])
        else:
            aim += int(line[4:])
    
    return h_pos * depth
    
if __name__ == "__main__":
    from aocd import submit

    answer = main(not COMPLETE)
    
    if COMPLETE:
        r = submit(answer, year=year, day=day)
    else:
        print(answer)

