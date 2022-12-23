COMPLETE = True
year, day = [2022, 10]

def main(enabled_print=True, test=False):
    if test:
        with open(r"2022\day10\test.txt", 'r') as f:
            inp = [line.strip() for line in f.readlines()]
    else:
        with open(r"2022\day10\input.txt", 'r') as f:
            inp = [line.strip() for line in f.readlines()]
    
    instructions = [1]
    for line in inp:
        if line.split(" ")[0] == "addx":
            instructions.append("addS")
            instructions.append(int(line.split(" ")[1]))
        else:
            instructions.append("noop")
    
    up_to_vals = [*range(20, len(instructions), 40)]
    answer = 0
    for val in up_to_vals:
        answer += val * (sum([i for i in instructions[:val] if type(i) is int]))
    
    return answer

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
