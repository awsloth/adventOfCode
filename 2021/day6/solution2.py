COMPLETE = False
year, day = [2021, 6]

def main(enabled_print=True, test=False):
    if test:
        with open(r"2021\day6\test.txt", 'r') as f:
            inp = [line.strip() for line in f.readlines()]
    else:
        with open(r"2021\day6\input.txt", 'r') as f:
            inp = [line.strip() for line in f.readlines()]
    
    fishes = {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0}
    
    for num in [*map(int, inp[0].split(","))]:
        fishes[num] += 1
    
    for _ in range(256):
        prev_state = fishes.copy()
        for (key, value) in prev_state.items():
            if key != 0:
                fishes[key - 1] = value
        
        fishes[8] = 0
        fishes[6] += prev_state[0]
        fishes[8] += prev_state[0]
    
    return sum(fishes.values())
    
if __name__ == "__main__":
    from aocd import submit

    answer = main(not COMPLETE)
    
    if COMPLETE:
        r = submit(answer, year=year, day=day)
    else:
        print(answer)

