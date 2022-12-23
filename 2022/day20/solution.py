COMPLETE = False
year, day = [2022, 20]

def main(enabled_print=True, test=False):
    if test:
        with open(r"2022\day20\test.txt", 'r') as f:
            inp = [line.strip() for line in f.readlines()]
    else:
        with open(r"2022\day20\input.txt", 'r') as f:
            inp = [line.strip() for line in f.readlines()]
    
    orig = [int(l) for l in inp]
    order = [[int(line), i] for (i, line) in enumerate(inp)]
    
    pos = 0
    while pos < len(order):
        for (i, number) in enumerate(order):
            if number[1] == pos:
                next_num = i
                break
    
        if order[next_num][0] == 0:
            pos += 1
            continue
    
        new_index = (next_num + order[next_num][0]) % len(order)
        dir = int(abs(order[next_num][0])/order[next_num][0])
        if (next_num + order[next_num][0] + dir) >= len(order) or (next_num + order[next_num][0] + dir) < 0:
            times = abs((next_num + order[next_num][0] + dir) // len(order))
            new_index = (next_num + order[next_num][0] + times*dir) % len(order)
        
        temp = order[next_num]
        order = order[:next_num] + order[next_num+1:]
        
        order.insert(new_index, temp)
        pos += 1
    
    order = [o[0] for o in order]
    zero = order.index(0)
    
    if enabled_print:
        print(order[(1000+zero)%len(order)])
        print(order[(2000+zero)%len(order)])
        print(order[(3000+zero)%len(order)])
    
    return order[(1000+zero)%len(order)] + order[(2000+zero)%len(order)] + order[(3000+zero)%len(order)]

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
