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

    GRID_SIZE = 20000
    grid = [["." for __ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    central_port = [GRID_SIZE//2, GRID_SIZE//2]
    grid[central_port[1]][central_port[0]]  = "o"

    cur_pos = central_port.copy()
    for op in inp[0].split(","):
        dist = int(op[1:])
        match op[0]:
            case 'R':
                for i in range(1, dist):
                    grid[cur_pos[1]][cur_pos[0]+i] = "-"
                cur_pos[0] += dist
                pass
            case 'L':
                for i in range(1, dist):
                    grid[cur_pos[1]][cur_pos[0]-i] = "-"
                cur_pos[0] -= dist
                pass
            case 'U':
                for i in range(1, dist):
                    grid[cur_pos[1]-i][cur_pos[0]] = "|"
                cur_pos[1] -= dist
                pass
            case 'D':
                for i in range(1, dist):
                    grid[cur_pos[1]+i][cur_pos[0]] = "|"
                cur_pos[1] += dist
                pass

        grid[cur_pos[1]][cur_pos[0]] = "+"

    cur_pos = central_port.copy()
    for op in inp[1].split(","):
        dist = int(op[1:])
        match op[0]:
            case 'R':
                for i in range(1, dist):
                    if grid[cur_pos[1]][cur_pos[0]+i] != ".":
                        grid[cur_pos[1]][cur_pos[0]+i] = "X"
                    else:
                        grid[cur_pos[1]][cur_pos[0]+i] = "-"
                cur_pos[0] += dist
                pass
            case 'L':
                for i in range(1, dist):
                    if grid[cur_pos[1]][cur_pos[0]-i] != ".":
                        grid[cur_pos[1]][cur_pos[0]-i] = "X"
                    else:
                        grid[cur_pos[1]][cur_pos[0]-i] = "-"
                cur_pos[0] -= dist
                pass
            case 'U':
                for i in range(1, dist):
                    if grid[cur_pos[1]-i][cur_pos[0]] != ".":
                        grid[cur_pos[1]-i][cur_pos[0]] = "X"
                    else:
                        grid[cur_pos[1]-i][cur_pos[0]] = "|"
                cur_pos[1] -= dist
                pass
            case 'D':
                for i in range(1, dist):
                    if grid[cur_pos[1]+i][cur_pos[0]] != ".":
                        grid[cur_pos[1]+i][cur_pos[0]] = "X"
                    else:
                        grid[cur_pos[1]+i][cur_pos[0]] = "|"
                cur_pos[1] += dist
                pass

        if grid[cur_pos[1]][cur_pos[0]] != ".":
            grid[cur_pos[1]][cur_pos[0]] = "X"
        else:
            grid[cur_pos[1]][cur_pos[0]] = "+"

    cross_pos = sum([[(x, y) for x in range(GRID_SIZE) if grid[y][x] == "X"] for y in range(GRID_SIZE)], [])

    if enabled_print:
        print(cross_pos)
    
    manhattan_dist = [abs(x-central_port[0]) + abs(y - central_port[1]) for (x, y) in cross_pos]

    if enabled_print:
        print(manhattan_dist)
        print(central_port)

    return min(manhattan_dist)

if __name__ == "__main__":
    from aocd import submit

    import bs4
    import copier
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
                copier.make_next(year, day)
    else:
        print(f"You got {answer}")