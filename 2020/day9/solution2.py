import os
year, day = [2020, 9]
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

    inp = [int(x) for x in inp]

    if test:
        preamble = 5
    else:
        preamble = 25

    cur_pos = preamble
    invalid_nums = []
    for i in range(cur_pos, len(inp)):
        found_sol = False
        for j in range(i-preamble, i):
            for k in range(i-preamble, j):
                if j == k:
                    continue

                if inp[j] + inp[k] == inp[i]:
                    found_sol = True
                    break
            if found_sol:
                break

        if not found_sol:
            invalid_nums.append(inp[i])
    
    found = False
    size = 1
    while not found:
        size += 1
        for i in range(len(inp)-size+1):
            if sum([inp[i+a] for a in range(size)]) == invalid_nums[0]:
                contig = inp[i:i+size]
                return max(contig) + min(contig)


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