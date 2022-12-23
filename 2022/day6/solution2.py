COMPLETE = False
year, day = [2022, 6]

def main(enabled_print=True, test=False):
    if test:
        with open(r"2022\day6\test.txt", 'r') as f:
            inp = [line.strip() for line in f.readlines()]
    else:
        with open(r"2022\day6\input.txt", 'r') as f:
            inp = [line.strip() for line in f.readlines()]
    i = 0
    while len(list(set(inp[0][i:i+14]))) < 14:
        i += 1
    
    if enabled_print:
        print(inp[0][i:i+14])
    
    return i + 14
    
if __name__ == "__main__":
    from aocd import submit

    answer = main(not COMPLETE)
    
    if COMPLETE:
        r = submit(answer, year=year, day=day)
    else:
        print(answer)

