COMPLETE = False
year, day = [2021, 8]

def main(enabled_print=True, test=False):
    if test:
        with open(r"2021\day8\test.txt", 'r') as f:
            inp = [line.strip() for line in f.readlines()]
    else:
        with open(r"2021\day8\input.txt", 'r') as f:
            inp = [line.strip() for line in f.readlines()]

    answer = 0
    for line in inp:
        for num in line.split("|")[1].split(" "):
            if len(num) in [2, 3, 4, 7]:
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
