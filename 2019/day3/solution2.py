import os
year, day = [2019, 3]
root = f"C:\\Users\\Adam\\PythonProjects\\adventOfCode\\{year}\\day{day}"

def main(enabled_print=True, test=False, debug=False):
    if debug:
        with open(os.path.join(root, "input.txt"), 'r') as f:
            inp = [line.strip() for line in f.readlines()]
    elif test:
        with open(os.path.join(root, "test.txt"), 'r') as f:
            inp = [line.strip() for line in f.readlines()]
    else:
        with open(os.path.join(root, "input.txt"), 'r') as f:
            inp = [line.strip() for line in f.readlines()]

    first_wire = []
    cur_pos = [0, 0]
    for op in inp[0].split(","):
        dist = int(op[1:])
        match op[0]:
            case 'R':
                for i in range(1, dist):
                    first_wire.append((cur_pos[0]+i, cur_pos[1]))
                cur_pos[0] += dist
                pass
            case 'L':
                for i in range(1, dist):
                    first_wire.append((cur_pos[0]-i, cur_pos[1]))
                cur_pos[0] -= dist
                pass
            case 'U':
                for i in range(1, dist):
                    first_wire.append((cur_pos[0], cur_pos[1]-i))
                cur_pos[1] -= dist
                pass
            case 'D':
                for i in range(1, dist):
                    first_wire.append((cur_pos[0], cur_pos[1]+i))
                cur_pos[1] += dist
                pass

        first_wire.append((cur_pos[0], cur_pos[1]))

    second_wire = []
    cur_pos = [0, 0]
    for op in inp[1].split(","):
        dist = int(op[1:])
        match op[0]:
            case 'R':
                for i in range(1, dist):
                    second_wire.append((cur_pos[0]+i, cur_pos[1]))
                cur_pos[0] += dist
                pass
            case 'L':
                for i in range(1, dist):
                    second_wire.append((cur_pos[0]-i, cur_pos[1]))
                cur_pos[0] -= dist
                pass
            case 'U':
                for i in range(1, dist):
                    second_wire.append((cur_pos[0], cur_pos[1]-i))
                cur_pos[1] -= dist
                pass
            case 'D':
                for i in range(1, dist):
                    second_wire.append((cur_pos[0], cur_pos[1]+i))
                cur_pos[1] += dist
                pass

        second_wire.append((cur_pos[0], cur_pos[1]))
    
    intersections = list(set(first_wire).intersection(set(second_wire)))
    
    scores = []
    for inter in intersections:
        for (i, pos) in enumerate(first_wire):
            if pos == inter:
                break
        for (j, pos) in enumerate(second_wire):
            if pos == inter:
                break
        
        scores.append(i+j+2)

    return min(scores)

if __name__ == "__main__":
    from aocd import submit

    import bs4
    import sys

    if (len(sys.argv) < 3):
        print("Enter command line arguments")
        exit(-1)
    
    arg_list = sys.argv[1:]
    complete = arg_list[0].lower() == "true"
    run_test = arg_list[1].lower() == "true"

    if (len(sys.argv) == 4):
        test_ans = int(sys.argv[3])
    elif (run_test):
        print("Provide answer to test")
        exit(-1)

    if (run_test and not os.path.exists(os.path.join(root, "test.txt"))):
        print("Test file does not exist")
        exit(-1)

    answer = main(not complete, run_test, complete)
    
    if run_test:
        print(f"The answer is {test_ans}, you got {answer}.")
        if (test_ans == answer):
            print(f"You got it right! Time to submit!")
        else:
            print("Time to change ur code :(")
    elif complete:
        r = submit(answer, year=year, day=day)
        if r is not None:
            soup = bs4.BeautifulSoup(r.data, "html.parser")
            message = soup.article.text
            if "That's the right answer" in message:
                print("Yippee!")
    else:
        print(f"You got {answer}")