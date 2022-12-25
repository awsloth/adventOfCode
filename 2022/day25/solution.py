COMPLETE = True
year, day = [2022, 25]

def getSNAFU(num):
    symbs = '012=-'

    highest = 0
    while not (sum([2*(5**i) for i in range(highest+1)]) >= num >= sum([-2*(5**i) for i in range(highest)])+5**highest):
        highest += 1

    end_num = [0 for _ in range(highest+1)]

    if num >= 2*(5**highest) + sum([-2*(5**i) for i in range(highest)]):
        end_num[0] = 2
    else:
        end_num[0] = 1

    for i in range(1, highest+1):
        r_len = highest - i
        remainder = num - fromSNAFU("".join([symbs[c] for c in end_num]))
        if remainder == 0:
            break

        elif remainder > 0:
            if remainder >= 2*(5**r_len) + sum([-2*(5**j) for j in range(r_len)]):
                end_num[i] = 2
            elif remainder >= (5**r_len) + sum([-2*(5**j) for j in range(r_len)]):
                end_num[i] = 1
            else:
                end_num[i] = 0
        elif remainder < 0:
            if remainder >= sum([-2*(5**j) for j in range(r_len)]):
                end_num[i] = 0
            elif remainder >= -(5**r_len) + sum([-2*(5**j) for j in range(r_len)]):
                end_num[i] = -1
            else:
                end_num[i] = -2

    return "".join([symbs[c] for c in end_num])

def fromSNAFU(text):
    val = {"=":-2, "-":-1, "0":0, "1":1, "2":2}
    num = 0
    for (i, c) in enumerate(reversed(text)):
        num += val[c]*(5**i)

    return num

def main(enabled_print=True, test=False):
    if test:
        with open(r"2022\day25\test.txt", 'r') as f:
            inp = [line.strip() for line in f.readlines()]
    else:
        with open(r"2022\day25\input.txt", 'r') as f:
            inp = [line.strip() for line in f.readlines()]

    num_sum = 0
    for line in inp:
        num_sum += fromSNAFU(line)

    num = getSNAFU(num_sum)
    
    assert fromSNAFU(num) == num_sum

    return num

if __name__ == "__main__":
    from aocd import submit

    import bs4
    import copier

    answer = main(not COMPLETE, False)
    
    if COMPLETE:
        r = submit(answer, year=year, day=day)
        soup = bs4.BeautifulSoup(r.text, "html.parser")
        message = soup.article.text
        if "That's the right answer" in message:
            copier.make_next(year, day)
    else:
        print(answer)
