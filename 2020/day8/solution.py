import os
year, day = [2020, 8]
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

    acc = 0
    pointer = 0
    visited = [False for _ in range(len(inp))]
    while not visited[pointer]:
        if enabled_print:
            print(f"Cur instruction: {inp[pointer]}, {acc=}, {pointer=}")
        
        visited[pointer] = True
        match inp[pointer][:3]:
            case "nop":
                pointer += 1
                pass
            case "acc":
                acc += int(inp[pointer][4:])
                pointer += 1
                pass
            case "jmp":
                pointer += int(inp[pointer][4:])
                pass

    if enabled_print:
        print(f"Cur instruction: {inp[pointer]}, {acc=}, {pointer=}")

    return acc

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