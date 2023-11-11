import os
import logging
year, day = [2019, 8]
root: str = os.path.join(os.getcwd(), str(year), f"day{day}")

class Run:
    TEST = 0
    REAL = 1

def main(root: str, run_type: Run = Run.TEST) -> int:
    if run_type == Run.TEST:
        with open(os.path.join(root, "test.txt"), 'r') as f:
            inp: list[str] = [line.strip() for line in f.readlines()]
    elif run_type == Run.REAL:
        with open(os.path.join(root, "input.txt"), 'r') as f:
            inp: list[str] = [line.strip() for line in f.readlines()]
    else:
        raise Exception("Error in getting run type")
    
    width, height = (25, 6)
    screen_size = width*height

    inp: list[int] = [int(x) for x in inp[0]]

    screen_count = len(inp)//screen_size

    screens: list[list[int]] = [inp[screen_size*i:screen_size*(i+1)] for i in range(screen_count)]

    pixel_val = [" ", "█"]

    end_screen: list[str] = [None for _ in range(screen_size)]

    for screen in screens:
        for (i, pixel) in enumerate(screen):
            if end_screen[i] is None and pixel != 2:
                end_screen[i] = pixel_val[pixel]
    
    for i in range(height):
        print(*end_screen[width*i:width*(i+1)])

    return 0

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
