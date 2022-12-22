COMPLETE = True
year, day = [2022, 3]

def main(enabled_print=True):
    with open(r"2022\day3\input.txt", 'r') as f:
        inp = [line.strip() for line in f.readlines()]

    answer = 0
    for line in inp:
        h1, h2 = line[:len(line)//2], line[len(line)//2:]
        c = list(set(h1).intersection(set(h2)))[0]
        prior = ord(c.upper()) - 64
        if c.upper() == c:
            prior += 26
        answer += prior

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
