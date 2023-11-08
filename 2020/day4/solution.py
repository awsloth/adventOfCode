import os
year, day = [2020, 4]
root = os.path.join(os.getcwd(), str(year), f"day{day}")

def valid(passport: dict):
    fields = set(["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"])
    return (fields.intersection(set(passport.keys())) == fields)

def main(enabled_print=True, test=False):
    if test:
        with open(os.path.join(root, "test.txt"), 'r') as f:
            inp = [line.strip() for line in f.readlines()]
    else:
        with open(os.path.join(root, "input.txt"), 'r') as f:
            inp = [line.strip() for line in f.readlines()]

    passports = []
    cur_pass = {}
    for line in inp:
        if line == "":
            passports.append(cur_pass)
            cur_pass = {}
            continue

        for attr in line.split(" "):
            at, val = attr.split(":")
            cur_pass[at] = val

    passports.append(cur_pass)

    total = 0
    for passport in passports:
        total += valid(passport)
        if enabled_print and not valid(passport):
            print(f"{passport.keys()=}")

    return total

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
        r = submit(answer, year=year, day=day, quiet=False)
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