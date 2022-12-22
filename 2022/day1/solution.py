COMPLETE = True
year, day = [2022, 1]

def main(enabled_print=True):
    with open(r"2022\day1\input.txt", 'r') as f:
        inp = [line.strip() for line in f.readlines()]

    runningTotal = 0
    totals = []
    for line in inp:
        if line == '':
            totals.append(runningTotal)
            runningTotal = 0
        else:
            runningTotal += int(line)

    return max(totals)

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
