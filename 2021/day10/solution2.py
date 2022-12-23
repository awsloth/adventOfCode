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
    scores = {"(":1, "[":2, "{":3, "<":4}
    opens = '{([<'
    line_scores = []
    answer = 0
    for (j, line) in enumerate(inp):
        b_stack = []
        for (i, symb) in enumerate(line):
            if symb in opens:
                b_stack.append(symb)
            elif co[symb] == b_stack[-1]:
                b_stack.pop()
            else:
                break
        else:
            score = 0
            while len(b_stack) > 0:
                item = b_stack.pop()
                score *= 5
                score += scores[item]
            line_scores.append(score)
        
    return sorted(line_scores)[len(line_scores)//2]
    
if __name__ == "__main__":
    from aocd import submit

    answer = main(not COMPLETE)
    
    if COMPLETE:
        r = submit(answer, year=year, day=day)
    else:
        print(answer)

