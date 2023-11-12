import os
import logging
year, day = [2019, 10]
root: str = os.path.join(os.getcwd(), str(year), f"day{day}")

class Run:
    TEST = 0
    REAL = 1

def factors(num):    
    facts = []

    for i in range(1, abs(num)+1):
        if num % i == 0:
            facts.append(i)
    
    return facts

def hcf(num1, num2):
    if (num1 == 0 and abs(num2) != 1):
        return abs(num2)
    elif (num2 == 0 and abs(num1) != 1):
        return abs(num1)
    elif num1 == 0 or num2 == 0:
        return 1
    
    num1_factors = factors(num1)
    num2_factors = factors(num2)

    return max(set(num1_factors).intersection(set(num2_factors)))

def main(root: str, run_type: Run = Run.TEST) -> int:
    if run_type == Run.TEST:
        with open(os.path.join(root, "test.txt"), 'r') as f:
            inp: list[str] = [line.strip() for line in f.readlines()]
    elif run_type == Run.REAL:
        with open(os.path.join(root, "input.txt"), 'r') as f:
            inp: list[str] = [line.strip() for line in f.readlines()]
    else:
        raise Exception("Error in getting run type")

    undone_list: list[list[tuple[int, int]]] = [[(x, y) for x in range(len(inp[y])) if inp[y][x] == '#'] for y in range(len(inp))]
    
    ast_locs: list[tuple[int, int]] = []
    for elem in undone_list:
        ast_locs += elem
    
    best = None
    max_seen = 0
    for cur_ast in ast_locs:
        ratios: list[tuple[int, int]] = []

        for asteroid in ast_locs:
            if asteroid == cur_ast:
                continue

            x_ratio = asteroid[0]-cur_ast[0]
            y_ratio = asteroid[1]-cur_ast[1]

            while hcf(x_ratio, y_ratio) != 1:
                divisor = hcf(x_ratio, y_ratio)
                x_ratio //= divisor
                y_ratio //= divisor

            if (x_ratio, y_ratio) not in ratios:
                ratios.append((x_ratio, y_ratio))

        if len(ratios) > max_seen:
            max_seen = len(ratios)
            best = cur_ast

    ratios: list[tuple[int, int]] = []

    for asteroid in ast_locs:
        if asteroid == best:
            continue

        x_ratio = asteroid[0]-best[0]
        y_ratio = asteroid[1]-best[1]

        ratios.append((x_ratio, y_ratio))

    ratio_planet_dict: dict[str, list[tuple[int, int]]] = {}
    base_ratios = []
    for ratio in ratios:
        x_ratio = ratio[0]
        y_ratio = ratio[1]

        while hcf(x_ratio, y_ratio) != 1:
            divisor = hcf(x_ratio, y_ratio)
            x_ratio //= divisor
            y_ratio //= divisor

        key = f"{x_ratio},{y_ratio}"
        if key not in ratio_planet_dict:
            ratio_planet_dict[key] = [ratio]
            base_ratios.append((x_ratio, y_ratio))
        else:
            ratio_planet_dict[key].append(ratio)

    for key in ratio_planet_dict:
        ratio_planet_dict[key] = [*sorted(ratio_planet_dict[key], key=lambda x: x[0])]

    U = [x for x in base_ratios if x[0]==0 and x[1]<0]
    UR = [x for x in base_ratios if x[0]>0 and x[1]<0]
    R = [x for x in base_ratios if x[0]>0 and x[1]==0]
    LR = [x for x in base_ratios if x[0]>0 and x[1]>0]
    D = [x for x in base_ratios if x[0]==0 and x[1]>0]
    LL = [x for x in base_ratios if x[0]<0 and x[1]>0]
    L = [x for x in base_ratios if x[0]<0 and x[1]==0]
    UL = [x for x in base_ratios if x[0]<0 and x[1]<0]

    UR.sort(key=lambda x: -x[0]/x[1])
    LR.sort(key=lambda x: x[1]/x[0])
    LL.sort(key=lambda x: -x[0]/x[1])
    UL.sort(key=lambda x: x[1]/x[0])

    sorted_keys = [f"{x},{y}" for x,y in U+UR+R+LR+D+LL+L+UL]

    dict_lists = [ratio_planet_dict[x] for x in sorted_keys]

    first_x_planets = list(zip(*dict_lists))[0]

    planets = [(x[0]+best[0], x[1]+best[1]) for x in first_x_planets]

    return planets[199][0]*100 + planets[199][1]

if __name__ == "__main__":
    # Import libraries
    from aocd import submit

    import bs4
    import sys

    # Get command line arguments
    arg_list: list[str] = [x.upper() for x in sys.argv]

    # Detect logging level wanted
    loglevel = None
    for arg in arg_list:
        if "--log" in arg.lower():
            loglevel = arg.removeprefix("--LOG=")

    # If none specified, assume base
    if loglevel is None:
        loglevel = "WARNING"

    # Get logging level
    numeric_level = getattr(logging, loglevel.upper(), None)

    # Check value is ccorrect
    if not isinstance(numeric_level, int):
        raise ValueError(f"Invalid log level: {loglevel}")

    # Set logging config
    logging.basicConfig(format='[%(levelname)s]: %(message)s', level=numeric_level)

    # Take first two character to detect for -T
    first_two_chars: list[str] = [x[:2] for x in arg_list]

    # Check whether user has input both
    if "-T" in first_two_chars and "-R" in arg_list:
        raise Exception("Input either -T or -R, not both")
    
    # Check which (if any user has input)
    test_ans = None
    if "-R" in arg_list:
        # Set run type to real
        run_type = Run.REAL

    elif "-T" in first_two_chars:
        # Test that user has put in a numeric value for the test answer
        valid = False
        for elem in arg_list:
            if "-T" in elem and "=" in elem:
                try:
                    test_ans = int(elem.split("=")[1])
                    valid = True
                except ValueError:
                    raise Exception("Enter a numeric value for test answer")
        
        # Raise exception if user input wrong value
        if not valid:
            raise Exception("Argument -T takes input -T=<test_answer>")
        
        # Set run type to test
        run_type = Run.TEST
    else:
        # If user has input neither raise exception
        raise Exception("You need to input either -T or -R")
    
    # Run solution
    answer = main(root, run_type)

    # Test answer
    if run_type == Run.REAL:
        r = submit(answer, year=year, day=day)
        if r is not None:
            soup = bs4.BeautifulSoup(r.data, "html.parser")
            message = soup.article.text
            if "That's the right answer" in message:
                print("Yippee!")
    
    elif run_type == Run.TEST:
        print(f"The answer is {test_ans}, you got {answer}.")

        if (test_ans == answer):
            print(f"You got it right! Time to submit!")
        else:
            print("Time to change ur code :(")
        
    else:
        raise Exception("Somehow run_type was not test or real")
