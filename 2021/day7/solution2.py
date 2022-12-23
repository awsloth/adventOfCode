COMPLETE = False
year, day = [2021, 7]

def get_dist(num, nums):
    total = 0
    for (key, val) in nums.items():
        n = abs(key-num)
        total += (n * (n + 1) // 2) * val
    
    return total

def main(enabled_print=True, test=False):
    if test:
        with open(r"2021\day7\test.txt", 'r') as f:
            inp = [line.strip() for line in f.readlines()]
    else:
        with open(r"2021\day7\input.txt", 'r') as f:
            inp = [line.strip() for line in f.readlines()]
    
    nums = [*map(int, inp[0].split(","))]
    num_tots = {}
    for num in nums:
        num_tots[num] = nums.count(num)
    
    best = float('inf')
    for num in range(min(nums), max(nums)+1):
        cur_dist = get_dist(num, num_tots)
        if cur_dist < best:
            best = cur_dist
    
    return best
    
if __name__ == "__main__":
    from aocd import submit

    answer = main(not COMPLETE)
    
    if COMPLETE:
        r = submit(answer, year=year, day=day)
    else:
        print(answer)

