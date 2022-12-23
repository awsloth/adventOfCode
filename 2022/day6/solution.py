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
    while len(list(set(inp[0][i:i+4]))) < 4:
        i += 1
    
    return i + 4

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
