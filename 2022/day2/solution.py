COMPLETE = False
year, day = [2022, 2]

def main(enabled_print=True, test=False):
    if test:
        with open(r"2022\day2\test.txt", 'r') as f:
            inp = [line.strip() for line in f.readlines()]
    else:
        with open(r"2022\day2\input.txt", 'r') as f:
            inp = [line.strip() for line in f.readlines()]
    
    answer = 0
    for line in inp:
        p_2 = {"X":"A", "Y":"B", "Z":"C"}
        p_2_score = {"A":1, "B":2, "C":3}
        win = {"B":"A", "C":"B", "A":"C"}

        p1, p2 = line.split()
        p2 = p_2[p2]

        answer += p_2_score[p2]

        if p1 == p2:
            answer += 3
        elif p1 == win[p2]:
            answer += 6

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
