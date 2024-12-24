"""Module to solve part 1 of advent of code 2024-24"""
from enum import Enum
import os
import logging
year, day = [2024, 24]
ROOT_DIR: str = os.path.join(os.getcwd(), str(year), f"day{day}")

class Run(Enum):
    """Enum for program run type"""
    TEST = 0
    REAL = 1

def read_input(root: str, run_type: Run = Run.TEST) -> list[str]:
    """Function to read in input from test or input text file"""
    if run_type == Run.TEST:
        with open(os.path.join(root, "test.txt"), 'r', encoding="utf8") as f:
            return [line.strip() for line in f.readlines()]
    elif run_type == Run.REAL:
        with open(os.path.join(root, "input.txt"), 'r', encoding="utf8") as f:
            return [line.strip() for line in f.readlines()]

def main(root: str, run_type: Run = Run.TEST) -> int:
    """Function to run the solution"""
    inp = read_input(root, run_type)

    return -1

if __name__ == "__main__":
    # Import libraries
    from aocd import submit
    from urllib3 import BaseHTTPResponse

    import sys
    import copier

    # Get command line arguments
    arg_list: list[str] = [x.upper() for x in sys.argv]

    # Detect logging level wanted
    log_level = None
    for arg in arg_list:
        if "--log" in arg.lower():
            log_level = arg.removeprefix("--LOG=")

    # If none specified, assume base
    if log_level is None:
        log_level = "WARNING"

    # Get logging level
    numeric_level = getattr(logging, log_level.upper(), None)

    # Check value is ccorrect
    if not isinstance(numeric_level, int):
        raise ValueError(f"Invalid log level: {log_level}")

    # Set logging config
    logging.basicConfig(format='[%(levelname)s]: %(message)s', level=numeric_level)

    # Take first two character to detect for -T
    first_two_chars: list[str] = [x[:2] for x in arg_list]

    # Check whether user has input both
    if "-T" in first_two_chars and "-R" in arg_list:
        raise ValueError("Input either -T or -R, not both")

    # Check which (if any user has input)
    test_ans = None
    if "-R" in arg_list:
        # Set run type to real
        prog_run_type = Run.REAL

    elif "-T" in first_two_chars:
        # Test that user has put in a numeric value for the test answer
        valid = False
        for elem in arg_list:
            if "-T" in elem and "=" in elem:
                try:
                    test_ans = int(elem.split("=")[1])
                    valid = True
                except ValueError as exc:
                    raise ValueError("Enter a numeric value for test answer") from exc

        # Raise exception if user input wrong value
        if not valid:
            raise ValueError("Argument -T takes input -T=<test_answer>")

        # Set run type to test
        prog_run_type = Run.TEST
    else:
        # If user has input neither raise exception
        raise ValueError("You need to input either -T or -R")

    # Run solution
    ANSWER = main(ROOT_DIR, prog_run_type)

    # Test answer
    if prog_run_type == Run.REAL:
        r: BaseHTTPResponse | None = submit(ANSWER, year=year, day=day)
        if r is not None:
            if "That\\'s the right answer" in str(r.data):
                copier.make_next(year, day)

    elif prog_run_type == Run.TEST:
        print(f"The answer is {test_ans}, you got {ANSWER}.")

        if test_ans == ANSWER:
            print("You got it right! Time to submit!")
        else:
            print("Time to change ur code :(")
