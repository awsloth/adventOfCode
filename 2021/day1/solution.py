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
    for (prev, line) in zip(inp, inp[1:]):
        if int(prev) < int(line):
            answer += 1
    
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
