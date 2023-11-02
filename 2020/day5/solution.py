import os
year, day = [2020, 5]
root = f"C:\\Users\\Adam\\PythonProjects\\adventOfCode\\{year}\\day{day}"

def main(enabled_print=True, test=False):
    import math
    if test:
        with open(os.path.join(root, "test.txt"), 'r') as f:
            inp = [line.strip() for line in f.readlines()]
    else:
        with open(os.path.join(root, "input.txt"), 'r') as f:
            inp = [line.strip() for line in f.readlines()]

    seat_ids = []
    for line in inp:
        column = [0, 7]
        row = [0, 127]
        for char in line[:-3]:
            match char:
                case 'B':
                    row[0] += math.ceil((row[1]-row[0])/2)
                    pass
                case 'F':
                    row[1] -= math.ceil((row[1]-row[0])/2)
        
        for char in line[-3:]:
            match char:
                case 'R':
                    column[0] += math.ceil((column[1]-column[0])/2)
                    pass
                case 'L':
                    column[1] -= math.ceil((column[1]-column[0])/2)

        if (enabled_print):
            print(f"{column=}, {row=}, ")

        seat_ids.append(row[0]*8 + column[0])
    
    
    return max(seat_ids)

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