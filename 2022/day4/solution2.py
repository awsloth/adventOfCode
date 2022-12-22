COMPLETE = True
year, day = [2022, 4]

def cRange(str):
    a1, a2 = map(int, str.split("-"))
    return [*range(a1, a2+1)]

def main(enabled_print=True):
    with open(r"2022\day4\input.txt", 'r') as f:
        inp = [line.strip() for line in f.readlines()]

    answer = 0
    for line in inp:
        r1, r2 = map(cRange, line.split(","))
        if list(set(r1).intersection(set(r2))) != []:
            answer += 1
        
    return answer

if __name__ == "__main__":
    from aocd import submit

    answer = main(not COMPLETE)
    
    if COMPLETE:
        r = submit(answer, year=year, day=day)
    else:
        print(answer)
