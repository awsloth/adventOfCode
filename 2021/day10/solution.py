COMPLETE = False
year, day = [2021, 10]

def main(enabled_print=True, test=False):
    if test:
        with open(r"2021\day10\test.txt", 'r') as f:
            inp = [line.strip() for line in f.readlines()]
    else:
        with open(r"2021\day10\input.txt", 'r') as f:
            inp = [line.strip() for line in f.readlines()]
    
    co = {"}":"{", "]":"[", ")":"(", ">":"<"}
    scores = {")":3, "]":57, "}":1197, ">":25137}
    opens = '{([<'
    answer = 0
    for (_, line) in enumerate(inp):
        b_stack = []
        for (__, symb) in enumerate(line):
            if symb in opens:
                b_stack.append(symb)
            elif co[symb] == b_stack[-1]:
                b_stack.pop()
            else:
                answer += scores[symb]
                break

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
