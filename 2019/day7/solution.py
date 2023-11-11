import os
year, day = [2019, 7]
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

    amplifiers = 5
    max_input = 4

    max_output = 0
    for j in range((max_input+1)**amplifiers):
        inputs = [0 for _ in range(amplifiers)]
        rest = j
        for k in range(amplifiers):
            inputs[k], rest = divmod(rest, (max_input+1)**(amplifiers-k-1))
        
        if any([x==y for (x, y) in zip(sorted(inputs), sorted(inputs)[1:])]):
            continue

        end_val = 0
        for i in range(amplifiers):
            inputted = False
            # Reset memory
            memory: list[str] = [int(val) for val in inp.split(",")]
            pointer = 0
            running = True

            while running:
                cur_instruction = str(memory[pointer])[-2:]
                modes = [int(x) for x in str(memory[pointer])[:-2].rjust(3, "0")]
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
                        if inputted:
                            memory[memory[pointer+1]] = end_val
                        else:
                            inputted = True
                            memory[memory[pointer+1]] = inputs[i]
                        pointer += 2
                        pass
                    case 4:
                        if modes[-1]:
                            end_val = memory[pointer+1]
                        else:
                            end_val = memory[memory[pointer+1]]
                        pointer += 2
                        pass
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
                        if enabled_print:
                            print(f"{inputs=}")
                            print(f"{cur_instruction}")
                        return -1
        
        if end_val > max_output:
            max_output = end_val

    return max_output

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