COMPLETE = True
year, day = [2022, 4]

def cRange(str):
    a1, a2 = map(int, str.split("-"))
    return [*range(a1, a2+1)]


def main(enabled_print=True, test=False):
    if test:
        with open(r"2022\day4\test.txt", 'r') as f:
            inp = [line.strip() for line in f.readlines()]
    else:
        with open(r"2022\day4\input.txt", 'r') as f:
            inp = [line.strip() for line in f.readlines()]

    answer = 0
    for line in inp:
        r1, r2 = map(cRange, line.split(","))
        if set(r1).issubset(set(r2)) or set(r2).issubset(set(r1)):
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