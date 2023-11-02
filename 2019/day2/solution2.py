import os
year, day = [2019, 2]
root = f"C:\\Users\\Adam\\PythonProjects\\adventOfCode\\{year}\\day{day}"

def main(enabled_print=True, test=False):
    if test:
        with open(os.path.join(root, "test.txt"), 'r') as f:
            inp = [line.strip() for line in f.readlines()]
    else:
        with open(os.path.join(root, "input.txt"), 'r') as f:
            inp = [line.strip() for line in f.readlines()]

    inp = inp[0]
    done = False
    max_test = 0

    while not done:
        max_test += 1
        for i in range(0, max_test):
            for j in range(0, max_test):
                memory = [int(val) for val in inp.split(",")]

                pointer = 0
                running = True

                # Start Program
                memory[1] = i
                memory[2] = j

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
                        
                if memory[0] == 19690720:
                    done = True
                    break
            
            if done:
                break

    return 100*i + j

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

    answer = main(not complete, run_test)
    
    if complete:
        r = submit(answer, year=year, day=day)
        if r is not None:
            soup = bs4.BeautifulSoup(r.data, "html.parser")
            message = soup.article.text
            if "That's the right answer" in message:
                print("Yippee!")
    elif run_test:
        print(f"The answer is {test_ans}, you got {answer}.")
        if (test_ans == answer):
            print(f"You got it right! Time to submit!")
        else:
            print("Time to change ur code :(")
    else:
        print(f"You got {answer}")