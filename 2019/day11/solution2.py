"""Module to solve part 2 of advent of code 2019-11"""
from enum import Enum
import os
import logging
year, day = [2019, 11]
ROOT_DIR: str = os.path.join(os.getcwd(), str(year), f"day{day}")


class Run(Enum):
    """Enum for program run type"""
    TEST = 0
    REAL = 1

class IntCom:
    """Class to handle running the intcode computer"""

    def __init__(self, memory: dict[int, int]):
        self.pointer: int = 0
        self.rel_base: int = 0
        self.mem: dict[int, int] = memory
        self.halted: bool = False

    def find_pos(self, mode: int, pointer: int) -> int:
        """Find value of variable based on pointer and mode"""
        match (mode):
            case 2:
                if self.mem[pointer]+self.rel_base not in self.mem:
                    self.mem[self.mem[pointer]+self.rel_base] = 0

                return self.mem[self.mem[pointer]+self.rel_base]
            case 1:
                if pointer not in self.mem:
                    self.mem[pointer] = 0

                return self.mem[pointer]
            case _:
                if self.mem[pointer] not in self.mem:
                    self.mem[self.mem[pointer]] = 0

                return self.mem[self.mem[pointer]]

    def find_pointer(self, mode: int, pointer: int) -> int:
        """Find pointer to output data to"""
        match (mode):
            case 2:
                if self.mem[pointer]+self.rel_base not in self.mem:
                    self.mem[self.mem[pointer]+self.rel_base] = 0

                return self.mem[pointer]+self.rel_base
            case _:
                if self.mem[pointer] not in self.mem:
                    self.mem[self.mem[pointer]] = 0

                return self.mem[pointer]

    def run_step(self, pot_input: int) -> int | None:
        """Runs a step of the code, with pot_input being potential input"""
        cur_instruction = str(self.mem[self.pointer])[-2:]
        modes = [int(x) for x in str(self.mem[self.pointer])[:-2].rjust(3, "0")]

        match (int(cur_instruction)):
            case 1:
                var1 = self.find_pos(modes[-1], self.pointer+1)
                var2 = self.find_pos(modes[-2], self.pointer+2)

                pointer_val = self.find_pointer(modes[-3], self.pointer+3)

                self.mem[pointer_val] = var1 + var2
                self.pointer+= 4
            case 2:
                var1 = self.find_pos(modes[-1], self.pointer+1)
                var2 = self.find_pos(modes[-2], self.pointer+2)

                pointer_val = self.find_pointer(modes[-3], self.pointer+3)

                self.mem[pointer_val] = var1 * var2
                self.pointer+= 4
            case 3:
                pointer_val = self.find_pointer(modes[-1], self.pointer+1)

                self.mem[pointer_val] = pot_input

                self.pointer+= 2
            case 4:
                self.pointer+= 2

                if modes[-1] == 2:
                    return self.mem[self.mem[self.pointer-1]+self.rel_base]
                if modes[-1]:
                    return self.mem[self.pointer-1]

                return self.mem[self.mem[self.pointer-1]]
            case 5:
                var1 = self.find_pos(modes[-1], self.pointer+1)
                var2 = self.find_pos(modes[-2], self.pointer+2)

                if var1:
                    self.pointer= var2
                else:
                    self.pointer+= 3
            case 6:
                var1 = self.find_pos(modes[-1], self.pointer+1)
                var2 = self.find_pos(modes[-2], self.pointer+2)

                if not var1:
                    self.pointer= var2
                else:
                    self.pointer+= 3
            case 7:
                var1 = self.find_pos(modes[-1], self.pointer+1)
                var2 = self.find_pos(modes[-2], self.pointer+2)

                pointer_val = self.find_pointer(modes[-3], self.pointer+3)

                self.mem[pointer_val] = int(var1 < var2)

                self.pointer+= 4
            case 8:
                var1 = self.find_pos(modes[-1], self.pointer+1)
                var2 = self.find_pos(modes[-2], self.pointer+2)

                pointer_val = self.find_pointer(modes[-3], self.pointer+3)

                self.mem[pointer_val] = int(var1 == var2)

                self.pointer+= 4
            case 9:
                var1 = self.find_pos(modes[-1], self.pointer+1)

                self.rel_base += var1
                self.pointer+= 2
            case 99:
                self.halted = True
            case _:
                raise ValueError("Came across unexpected instruction")

        return None

def read_input(root: str, run_type: Run = Run.TEST) -> list[str]:
    """Function to read in input from test or input text file"""
    if run_type == Run.TEST:
        with open(os.path.join(root, "test.txt"), 'r', encoding="utf8") as f:
            out: list[str] = [line.strip() for line in f.readlines()]
    elif run_type == Run.REAL:
        with open(os.path.join(root, "input.txt"), 'r', encoding="utf8") as f:
            out: list[str] = [line.strip() for line in f.readlines()]

    return out

def main(root: str, run_type: Run = Run.TEST) -> int:
    """Function to run the solution"""
    inp = read_input(root, run_type)

    intcode_com: IntCom = IntCom({i: int(val) for (i, val) in enumerate(inp[0].split(","))})

    grid: dict[int, dict[int, bool]] = {}

    grid[0] = {}
    grid[0][0] = True

    cur_pos = [0, 0]
    cur_dir = (0, -1)
    dir_order = [(0, -1), (1, 0), (0, 1), (-1, 0)]

    coloured: list[list[int]] = []

    while not intcode_com.halted:
        next_instruction = intcode_com.run_step(grid[cur_pos[1]][cur_pos[0]])
        while next_instruction is None and not intcode_com.halted:
            next_instruction = intcode_com.run_step(grid[cur_pos[1]][cur_pos[0]])

        colour = next_instruction

        next_instruction = intcode_com.run_step(grid[cur_pos[1]][cur_pos[0]])
        while next_instruction is None and not intcode_com.halted:
            next_instruction = intcode_com.run_step(grid[cur_pos[1]][cur_pos[0]])

        if intcode_com.halted:
            continue

        turn = next_instruction

        if turn:
            cur_dir = dir_order[(dir_order.index(cur_dir)+1)%4]
        else:
            cur_dir = dir_order[(dir_order.index(cur_dir)-1)%4]

        grid[cur_pos[1]][cur_pos[0]] = bool(colour)

        cur_pos[0] += cur_dir[0]
        cur_pos[1] += cur_dir[1]

        if cur_pos[1] not in grid:
            grid[cur_pos[1]] = {}

        if cur_pos[0] not in grid[cur_pos[1]]:
            grid[cur_pos[1]][cur_pos[0]] = False

        if cur_pos not in coloured:
            coloured.append(cur_pos.copy())

    y_span = [min(grid), max(grid)]
    x_span = [min(min(x) for x in grid.values()), max(max(x) for x in grid.values())]

    vis_grid = [["." for _ in range(x_span[1]-x_span[0]+1)] for __ in range(y_span[1]-y_span[0]+1)]

    for (y, x_vals) in grid.items():
        for (x, colour) in x_vals.items():
            vis_grid[y-y_span[0]][x-y_span[0]] = ".#"[colour]

    logging.info('\n'.join([""]+["".join(line) for line in vis_grid]))

    return -1

if __name__ == "__main__":
    # Import libraries
    from aocd import submit

    import sys

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
        r = submit(ANSWER, year=year, day=day)
        if r is not None:
            if "That's the right answer" in str(r.data):
                print("Yippee!")

    elif prog_run_type == Run.TEST:
        print(f"The answer is {test_ans}, you got {ANSWER}.")

        if test_ans == ANSWER:
            print("You got it right! Time to submit!")
        else:
            print("Time to change ur code :(")
