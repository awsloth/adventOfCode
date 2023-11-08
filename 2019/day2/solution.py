import os
year, day = [2019, 2]
root = os.path.join(os.getcwd(), str(year), f"day{day}")

def main(enabled_print=True, test=False):
    if test:
        with open(os.path.join(root, "test.txt"), 'r') as f:
            inp = [line.strip() for line in f.readlines()]
    else:
        with open(os.path.join(root, "input.txt"), 'r') as f:
            inp = [line.strip() for line in f.readlines()]

    inp = inp[0]
    memory = [int(val) for val in inp.split(",")]

    pointer = 0
    running = True

    # Start Program
    memory[1] = 12
    memory[2] = 2

    while running:
        match (memory[pointer]):
            case 1:
                memory[memory[pointer+3]] = memory[memory[pointer+1]] + memory[memory[pointer+2]]
                pointer += 4
                pass
            case 2:
                memory[memory[pointer+3]] = memory[memory[pointer+1]] * memory[memory[pointer+2]]
                pointer += 4
                pass
            case 99:
                running = False
                pass
            case _:
                return -1

    return memory[0]

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

    answer = main(not complete, run_test)
    
    if complete:
        r = submit(answer, year=year, day=day)
        if r is not None:
            soup = bs4.BeautifulSoup(r.data, "html.parser")
            message = soup.article.text
            if "That's the right answer" in message:
                copier.make_next(year, day)
    elif run_test:
        print(f"The answer is {test_ans}, you got {answer}.")
        if (test_ans == answer):
            print(f"You got it right! Time to submit!")
        else:
            print("Time to change ur code :(")
    else:
        print(f"You got {answer}")