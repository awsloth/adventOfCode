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
        bags[name] = contents

    if enabled_print:
        print(f"{bags=}")

    done_bags = ["shiny gold"]
    while set(done_bags) != set([key for key in bags.keys() if bags[key] != []]):
        # do operations on each bag
        for (key, values) in bags.items():
            if key in done_bags:
                continue
            
            if "shiny gold" in [val[1] for val in values]:
                done_bags.append(key)
                continue

            new_contents = []
            for i in range(len(values)):
                if bags[key][i][1] == "other":
                    continue
                new_content = bags[bags[key][i][1]]
                for val in new_content:
                    if val[1] != "other" and val[1] not in [va[1] for va in new_contents]:
                        new_contents.append(val)
                    else:
                        # identify and sum it
                        ...
            
            if "shiny gold" in [item[1] for item in new_contents]:
                done_bags.append(key)

            bags[key] = new_contents
        
        if enabled_print:
            print(f"{bags=}")
    
    return len(done_bags) - 1

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