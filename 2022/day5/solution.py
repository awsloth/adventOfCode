COMPLETE = False
year, day = [2022, 5]

def main(enabled_print=True, test=False):
    if test:
        with open(r"2022\day5\test.txt", 'r') as f:
            inp = f.read()
    else:
        with open(r"2022\day5\input.txt", 'r') as f:
            inp = f.read()
    
    crates, ops = inp.split("\n\n")
    num_stacks = int(crates.split("\n")[-1].split("   ")[-1].strip())
    stacks = [[] for _ in range(num_stacks)]
    
    for line in crates.split("\n")[:-1]:
        crateList = [*map("".join, [*zip(line[::4], line[1::4], line[2::4])])]
        for i in range(len(crateList)):
            if crateList[i] != "   ":
                stacks[i].insert(0, crateList[i][1:-1])

    for line in ops.split("\n"):
        nums = [[a.strip() for a in l.split("to")] for l in line.split("from")]
        quant = int(nums[0][0][5:])
        _from, to = map(int, nums[1])
        for i in range(quant):
            el = stacks[_from-1].pop()
            stacks[to-1].append(el)

    answer = ""
    for stack in stacks:
        if stack != []:
            answer += stack[-1]
    
    return answer

if __name__ == "__main__":
    from aocd import submit

    import bs4
    import copier

    answer = main(False)
    
    if COMPLETE:
        r = submit(answer, year=year, day=day)
        soup = bs4.BeautifulSoup(r.text, "html.parser")
        message = soup.article.text
        if "That's the right answer" in message:
            copier.make_next(year, day)
    else:
        print(answer)
