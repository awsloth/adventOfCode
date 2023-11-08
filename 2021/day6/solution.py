COMPLETE = False
year, day = [2021, 6]

def main(enabled_print=True, test=False):
    if test:
        with open(r"2021\day6\test.txt", 'r') as f:
            inp = [line.strip() for line in f.readlines()]
    else:
        with open(r"2021\day6\input.txt", 'r') as f:
            inp = [line.strip() for line in f.readlines()]
    
    nums = [*map(int, inp[0].split(","))]
    for _ in range(80):
        end_val = len(nums)
        for j in range(end_val):
            if nums[j] == 0:
                nums[j] = 6
                nums.append(8)
            else:
                nums[j] -= 1
    
    return len(nums)

if __name__ == "__main__":
    from aocd import submit

    import bs4
    import copier

    answer = main(not COMPLETE)
    
    if COMPLETE:
        r = submit(answer, year=year, day=day)
        soup = bs4.BeautifulSoup(r.text, "html.parser")
        message = soup.article.text
        if "That's the right answer" in message:
            copier.make_next(year, day)
    else:
        print(answer)
