COMPLETE = True
year, day = [2022, 2]

def main(enabled_print=True):
    with open(r"2022\day2\input.txt", 'r') as f:
        inp = [line.strip() for line in f.readlines()]

    answer = 0
    for line in inp:
        p_2 = {"X":"A", "Y":"B", "Z":"C"}
        p_2_score = {"A":1, "B":2, "C":3}
        loss = {"A":"B", "B":"C", "C":"A"}
        win = {"B":"A", "C":"B", "A":"C"}
        p1, p2 = line.split()
        if p2 == "X":
            answer += p_2_score[win[p1]]
        elif p2 == "Y":
            answer += 3 + p_2_score[p1]
        else:
            answer += 6 + p_2_score[loss[p1]]

    return answer


if __name__ == "__main__":
    from aocd import submit

    answer = main(not COMPLETE)
    
    if COMPLETE:
        r = submit(answer, year=year, day=day)
    else:
        print(answer)
