COMPLETE = False
year, day = [2021, 3]

def main(enabled_print=True, test=False):
    if test:
        with open(r"2021\day3\test.txt", 'r') as f:
            inp = [line.strip() for line in f.readlines()]
    else:
        with open(r"2021\day3\input.txt", 'r') as f:
            inp = [line.strip() for line in f.readlines()]
    
    end_num = ""
    for i in range(len(inp[0])):
        tally = 0
        for line in inp:
            if line[i] == "1":
                tally += 1
    
        if tally > len(inp)//2:
            end_num += "1"
        else:
            end_num += "0"
    
    op_end = ""
    for c in end_num:
        op_end += "10"[int(c)]
    
    answer = int(end_num, 2) * int(op_end, 2)
    
    return 1

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
