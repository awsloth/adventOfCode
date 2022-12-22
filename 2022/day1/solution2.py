COMPLETE = True
year, day = [2022, 1]

def main(enabled_print=True):
    with open(r"day1\input.txt", 'r') as f:
        inp = [line.strip() for line in f.readlines()]

    runningTotal = 0
    totals = []
    for line in inp:
        if line == '':
            totals.append(runningTotal)
            runningTotal = 0
        else:
            runningTotal += int(line)

    top = max(totals)
    totals.remove(top)
    second = max(totals)
    totals.remove(second)
    third = max(totals)

    return top + second + third

if __name__ == "__main__":
    from aocd import submit

    answer = main(not COMPLETE)
    
    if COMPLETE:
        r = submit(answer, year=year, day=day)
    else:
        print(answer)
