import os
year, day = [2019, 1]
root = f"C:\\Users\\Adam\\PythonProjects\\adventOfCode\\{year}\\day{day}"

def fuel_cost(mass):
    total = 0
    while mass//3 - 2 > 0:
        total += mass//3 - 2
        mass = mass//3 - 2

    return total

def main(enabled_print=True, test=False):
    if test:
        with open(os.path.join(root, "test.txt"), 'r') as f:
            inp = [line.strip() for line in f.readlines()]
    else:
        with open(os.path.join(root, "input.txt"), 'r') as f:
            inp = [line.strip() for line in f.readlines()]

    return sum([fuel_cost(int(line)) for line in inp])

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
        soup = bs4.BeautifulSoup(r.text, "html.parser")
        message = soup.article.text
        if "That's the right answer" in message:
            print("YIPPEE!!!!")
    elif run_test:
        print(f"The answer is {test_ans}, you got {answer}.")
        if (test_ans == answer):
            print(f"You got it right! Time to submit!")
        else:
            print("Time to change ur code :(")
    else:
        print(f"You got {answer}")