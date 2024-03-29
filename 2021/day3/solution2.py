COMPLETE = False
year, day = [2021, 3]

def findSat(condition, inputs):
    end_inp = []
    for input in inputs:
        valid = True
        for (i, bit) in enumerate(condition):
            if input[i] != bit:
                valid = False
        
        if valid:
            end_inp.append(input)

    return end_inp

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
        cur_inp = findSat(end_num, inp)
    
        if len(cur_inp) == 1:
            end_num = cur_inp[0]
            break
    
        for line in cur_inp:
            if line[i] == "1":
                tally += 1
    
        if tally >= len(cur_inp)/2:
            end_num += "1"
        else:
            end_num += "0"
    
    op_end = ""
    for i in range(len(inp[0])):
        tally = 0
        cur_inp = findSat(op_end, inp)
    
        if len(cur_inp) == 1:
            op_end = cur_inp[0]
            break
    
        for line in cur_inp:
            if line[i] == "0":
                tally += 1
    
        if tally > len(cur_inp)/2:
            op_end += "1"
        else:
            op_end += "0"
    
    return int(end_num, 2) * int(op_end, 2)
    
if __name__ == "__main__":
    from aocd import submit

    answer = main(not COMPLETE)
    
    if COMPLETE:
        r = submit(answer, year=year, day=day)
    else:
        print(answer)

