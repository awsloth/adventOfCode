import os
year, day = [2019, 5]
root = os.path.join(os.getcwd(), str(year), f"day{day}")

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

    inp = inp[0]
    memory: list[str] = [int(val) for val in inp.split(",")]

    if enabled_print:
        print(len(memory))

    pointer = 0
    running = True

    while running:
        cur_instruction = str(memory[pointer])[-2:]
        modes = [int(x) for x in str(memory[pointer])[:-2].rjust(3, "0")]
        if enabled_print:
            print(f"{memory[pointer:pointer+4]} {modes=} {pointer=}")
        match (int(cur_instruction)):
            case 1:
                if modes[-1]:
                    var1 = memory[pointer+1]
                else:
                    var1 = memory[memory[pointer+1]]
                
                if modes[-2]:
                    var2 = memory[pointer+2]
                else:
                    var2 = memory[memory[pointer+2]]

                memory[memory[pointer+3]] = var1 + var2
                pointer += 4
                pass
            case 2:
                if modes[-1]:
                    var1 = memory[pointer+1]
                else:
                    var1 = memory[memory[pointer+1]]
                
                if modes[-2]:
                    var2 = memory[pointer+2]
                else:
                    var2 = memory[memory[pointer+2]]

                memory[memory[pointer+3]] = var1 * var2
                pointer += 4
                pass
            case 3:
                memory[memory[pointer+1]] = 5 # ID of thermal regulator
                pointer += 2
                pass
            case 4:
                if modes[-1]:
                    return memory[pointer+1]
                else:
                    return memory[memory[pointer+1]]
            case 5:
                if modes[-1]:
                    var1 = memory[pointer+1]
                else:
                    var1 = memory[memory[pointer+1]]

                if modes[-2]:
                    var2 = memory[pointer+2]
                else:
                    var2 = memory[memory[pointer+2]]
                
                if var1:
                    pointer = var2
                else:
                    pointer += 3
            case 6:
                if modes[-1]:
                    var1 = memory[pointer+1]
                else:
                    var1 = memory[memory[pointer+1]]

                if modes[-2]:
                    var2 = memory[pointer+2]
                else:
                    var2 = memory[memory[pointer+2]]
                
                if not var1:
                    pointer = var2
                else:
                    pointer += 3
            case 7:
                if modes[-1]:
                    var1 = memory[pointer+1]
                else:
                    var1 = memory[memory[pointer+1]]

                if modes[-2]:
                    var2 = memory[pointer+2]
                else:
                    var2 = memory[memory[pointer+2]]
                
                memory[memory[pointer+3]] = (var1 < var2)

                pointer += 4
            case 8:
                if modes[-1]:
                    var1 = memory[pointer+1]
                else:
                    var1 = memory[memory[pointer+1]]

                if modes[-2]:
                    var2 = memory[pointer+2]
                else:
                    var2 = memory[memory[pointer+2]]
                
                memory[memory[pointer+3]] = (var1 == var2)

                pointer += 4
            case 99:
                running = False
                pass
            case _:
                return -1

    return memory[0]

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