COMPLETE = False
year, day = [2022, 8]

def main(enabled_print=True, test=False):
    if test:
        with open(r"2022\day8\test.txt", 'r') as f:
            inp = [line.strip() for line in f.readlines()]
    else:
        with open(r"2022\day8\input.txt", 'r') as f:
            inp = [line.strip() for line in f.readlines()]
    
    row_valid = [[False for _ in range(len(inp[0]))] for __ in range(len(inp))]
    column_valid = [[False for _ in range(len(inp))] for __ in range(len(inp[0]))]
    for j in range(len(inp)):
        row = [int(x) for x in inp[j]]
        for i in range(len(row)):
            valid = True
            if i == 0 or i == len(row)-1:
                valid = False
            elif max(row[:i]) < row[i]:
                valid = False
            elif max(row[i+1:]) < row[i]:
                valid = False
            row_valid[j][i] = valid
    
    for j in range(len(inp[0])):
        column = [int(x[j]) for x in inp]
        for i in range(len(column)):
            valid = True
            if i == 0 or i == len(column)-1:
                valid = False
            elif max(column[:i]) < column[i]:
                valid = False
            elif max(column[i+1:]) < column[i]:
                valid = False
    
            column_valid[i][j] = valid
    
    valids = [[(column_valid[i][j] and row_valid[i][j]) for i in range(len(row_valid[j]))] for j in range(len(row_valid))]
    
    end = []
    for valid in valids:
        end += valid
    
    return len(inp)*len(inp[0]) - sum(end)

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
