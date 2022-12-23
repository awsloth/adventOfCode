COMPLETE = False
year, day = [2021, 1]
    
def main(enabled_print=True, test=False):
    if test:
        with open(r"2021\day1\test.txt", 'r') as f:
            inp = [line.strip() for line in f.readlines()]
    else:
        with open(r"2021\day1\input.txt", 'r') as f:
            inp = [line.strip() for line in f.readlines()]
    
    answer = 0
    for ((s1, s2, s3), (e1, e2, e3)) in zip(zip(inp, inp[1:], inp[2:]), zip(inp[1:], inp[2:], inp[3:])):
        if sum(map(int, [s1, s2, s3])) < sum(map(int, [e1, e2, e3])):
            answer += 1

    return answer
    
if __name__ == "__main__":
    from aocd import submit

    answer = main(not COMPLETE)
    
    if COMPLETE:
        r = submit(answer, year=year, day=day)
    else:
        print(answer)
