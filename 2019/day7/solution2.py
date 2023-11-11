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

        inputs = [x+5 for x in inputs]

        list_mem: list[list[str]] = [[int(val) for val in inp.split(",")].copy() for _ in range(amplifiers)]
        pointers = [0, 0, 0, 0, 0]
        inputted = [0, 0, 0, 0, 0]
        end_val = 0
        cur_amp = 0
        running = True

        while running:
            pointer = pointers[cur_amp]
            cur_instruction = str(list_mem[cur_amp][pointer])[-2:]

            if enabled_print and inputs == [9, 7, 8, 5, 6]:
                print(f"{pointers=}, {cur_amp=}, {cur_instruction=}, {end_val=}, {inputted=}")
                print(list_mem[cur_amp])
                print()
        
            modes = [int(x) for x in str(list_mem[cur_amp][pointer])[:-2].rjust(3, "0")]
            match (int(cur_instruction)):
                case 1:
                    if modes[-1]:
                        var1 = list_mem[cur_amp][pointer+1]
                    else:
                        var1 = list_mem[cur_amp][list_mem[cur_amp][pointer+1]]
                    
                    if modes[-2]:
                        var2 = list_mem[cur_amp][pointer+2]
                    else:
                        var2 = list_mem[cur_amp][list_mem[cur_amp][pointer+2]]

                    list_mem[cur_amp][list_mem[cur_amp][pointer+3]] = var1 + var2
                    pointers[cur_amp] += 4
                    pass
                case 2:
                    if modes[-1]:
                        var1 = list_mem[cur_amp][pointer+1]
                    else:
                        var1 = list_mem[cur_amp][list_mem[cur_amp][pointer+1]]
                    
                    if modes[-2]:
                        var2 = list_mem[cur_amp][pointer+2]
                    else:
                        var2 = list_mem[cur_amp][list_mem[cur_amp][pointer+2]]

                    list_mem[cur_amp][list_mem[cur_amp][pointer+3]] = var1 * var2
                    pointers[cur_amp] += 4
                    pass
                case 3:
                    if not inputted[cur_amp]:
                        list_mem[cur_amp][list_mem[cur_amp][pointer+1]] = inputs[cur_amp]
                        inputted[cur_amp] += 1
                    else:
                        list_mem[cur_amp][list_mem[cur_amp][pointer+1]] = end_val
                    
                    pointers[cur_amp] += 2
                    pass
                case 4:
                    if modes[-1]:
                        end_val = list_mem[cur_amp][pointer+1]
                    else:
                        end_val = list_mem[cur_amp][list_mem[cur_amp][pointer+1]]
                    pointers[cur_amp] += 2

                    cur_amp += 1
                    cur_amp %= 5
                    pass
                case 5:
                    if modes[-1]:
                        var1 = list_mem[cur_amp][pointer+1]
                    else:
                        var1 = list_mem[cur_amp][list_mem[cur_amp][pointer+1]]

                    if modes[-2]:
                        var2 = list_mem[cur_amp][pointer+2]
                    else:
                        var2 = list_mem[cur_amp][list_mem[cur_amp][pointer+2]]
                    
                    if var1:
                        pointers[cur_amp] = var2
                    else:
                        pointers[cur_amp] += 3
                case 6:
                    if modes[-1]:
                        var1 = list_mem[cur_amp][pointer+1]
                    else:
                        var1 = list_mem[cur_amp][list_mem[cur_amp][pointer+1]]

                    if modes[-2]:
                        var2 = list_mem[cur_amp][pointer+2]
                    else:
                        var2 = list_mem[cur_amp][list_mem[cur_amp][pointer+2]]
                    
                    if not var1:
                        pointers[cur_amp] = var2
                    else:
                        pointers[cur_amp] += 3
                case 7:
                    if modes[-1]:
                        var1 = list_mem[cur_amp][pointer+1]
                    else:
                        var1 = list_mem[cur_amp][list_mem[cur_amp][pointer+1]]

                    if modes[-2]:
                        var2 = list_mem[cur_amp][pointer+2]
                    else:
                        var2 = list_mem[cur_amp][list_mem[cur_amp][pointer+2]]
                    
                    list_mem[cur_amp][list_mem[cur_amp][pointer+3]] = int(var1 < var2)

                    pointers[cur_amp] += 4
                case 8:
                    if modes[-1]:
                        var1 = list_mem[cur_amp][pointer+1]
                    else:
                        var1 = list_mem[cur_amp][list_mem[cur_amp][pointer+1]]

                    if modes[-2]:
                        var2 = list_mem[cur_amp][pointer+2]
                    else:
                        var2 = list_mem[cur_amp][list_mem[cur_amp][pointer+2]]
                    
                    list_mem[cur_amp][list_mem[cur_amp][pointer+3]] = int(var1 == var2)

                    pointers[cur_amp] += 4
                case 99:
                    if cur_amp == 4:
                        running = False
                    else:
                        cur_amp += 1
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