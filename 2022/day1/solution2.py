COMPLETE = True
year, day = [2022, 1]

def main(enabled_print=True, test=False):
    if test:
        with open(r"2022\day1\test.txt", 'r') as f:
            inp = [line.strip() for line in f.readlines()]
    else:
        with open(r"2022\day1\input.txt", 'r') as f:
            inp = [line.strip() for line in f.readlines()]
    
    runningTotal = 0
    totals = []
    for line in inp:
        if line == '':
            totals.append(runningTotal)
            runningTotal = 0
        else:
            runningTotal += int(line)

    totals.append(runningTotal)

    top, second, third, *_ = sorted(totals, reverse=True)
    return top + second + third

if __name__ == "__main__":
    from aocd import submit

    answer = main(not COMPLETE)
    
    if COMPLETE:
        r = submit(answer, year=year, day=day)
    else:
        print(answer)
