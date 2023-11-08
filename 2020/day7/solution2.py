import os
year, day = [2020, 7]
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

    bags = {}
    for bag in inp:
        name, content = bag.split(" contain ")
        name = name[:-5]
        content = content[:-1].split(", ")
        contents = [(name[0], name[2:-4].strip()) for name in content]
        for i in range(len(contents)):
            count, val = contents[i]
            if count == "n":
                contents[i] = (1, val)
            else:
                contents[i] = (int(contents[i][0]), val)
        
        bags[name] = contents

    total = 0
    if enabled_print:
        print(total)
        print(bags["shiny gold"])

    while set([val[1] for val in bags["shiny gold"]]) != set():
        # do operations on each bag
        new_content = []
        for (count, bag) in bags["shiny gold"]:
            if bag == "other":
                continue
            else:
                total += count
                for (new_count, new_bag) in bags[bag]:
                    if new_bag in [val[1] for val in new_content]:
                        for i in range(len(new_content)):
                            if new_content[i][1] == new_bag:
                                break
                        
                        new_content[i] = (new_content[i][0]+count*new_count, new_content[i][1])
                    else:
                        new_content.append((count*new_count, new_bag))
        
        bags["shiny gold"] = new_content

        if enabled_print:
            print(total)
            print(bags["shiny gold"])

    return total

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