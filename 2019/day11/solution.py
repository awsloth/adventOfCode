import os
import logging
year, day = [2019, 11]
root: str = os.path.join(os.getcwd(), str(year), f"day{day}")

class Run:
    TEST = 0
    REAL = 1

class Computer:
    def __init__(self, memory):
        self.pointer = 0
        self.rel_base = 0
        self.mem = memory
        self.halted = False

    def find_pos(self, mode, pointer):
        match (mode):
            case 2:
                if self.mem[pointer]+self.rel_base not in self.mem:
                    self.mem[self.mem[pointer]+self.rel_base] = 0
                
                return self.mem[self.mem[pointer]+self.rel_base]
            case 1:
                if pointer not in self.mem:
                    self.mem[pointer] = 0

                return self.mem[pointer]
            case 0:
                if self.mem[pointer] not in self.mem:
                    self.mem[self.mem[pointer]] = 0

                return self.mem[self.mem[pointer]]
    
    def find_pointer(self, mode, pointer):
        match (mode):
            case 2:
                if self.mem[pointer]+self.rel_base not in self.mem:
                    self.mem[self.mem[pointer]+self.rel_base] = 0
                
                return self.mem[pointer]+self.rel_base
            case 0:
                if self.mem[pointer] not in self.mem:
                    self.mem[self.mem[pointer]] = 0

                return self.mem[pointer]
        
    def run_step(self, pot_input):
        cur_instruction = str(self.mem[self.pointer])[-2:]
        modes = [int(x) for x in str(self.mem[self.pointer])[:-2].rjust(3, "0")]

        match (int(cur_instruction)):
            case 1:
                logging.debug("1")
                var1 = self.find_pos(modes[-1], self.pointer+1)
                var2 = self.find_pos(modes[-2], self.pointer+2)

                pointer_val = self.find_pointer(modes[-3], self.pointer+3)

                if pointer_val < 0:
                    raise Exception("Attempted to write to negative index")

                self.mem[pointer_val] = var1 + var2
                self.pointer+= 4
                pass
            case 2:
                logging.debug("2")
                var1 = self.find_pos(modes[-1], self.pointer+1)
                var2 = self.find_pos(modes[-2], self.pointer+2)

                pointer_val = self.find_pointer(modes[-3], self.pointer+3)

                if pointer_val < 0:
                    raise Exception("Attempted to write to negative index")
                
                self.mem[pointer_val] = var1 * var2
                self.pointer+= 4
                pass
            case 3:
                logging.debug("3")
                pointer_val = self.find_pointer(modes[-1], self.pointer+1)

                if pointer_val < 0:
                    raise Exception("Attempted to write to negative index")
                
                self.mem[pointer_val] = pot_input
                
                self.pointer+= 2
                pass
            case 4:
                logging.debug("4")
                self.pointer+= 2
                
                if modes[-1] == 2:
                    return self.mem[self.mem[self.pointer-1]+self.rel_base]
                elif modes[-1]:
                    return self.mem[self.pointer-1]
                else:
                    return self.mem[self.mem[self.pointer-1]]
            case 5:
                logging.debug("5")
                var1 = self.find_pos(modes[-1], self.pointer+1)
                var2 = self.find_pos(modes[-2], self.pointer+2)
                
                if var1:
                    self.pointer= var2
                else:
                    self.pointer+= 3
            case 6:
                logging.debug("6")
                var1 = self.find_pos(modes[-1], self.pointer+1)
                var2 = self.find_pos(modes[-2], self.pointer+2)

                if not var1:
                    self.pointer= var2
                else:
                    self.pointer+= 3
            case 7:
                logging.debug("7")
                var1 = self.find_pos(modes[-1], self.pointer+1)
                var2 = self.find_pos(modes[-2], self.pointer+2)
                
                pointer_val = self.find_pointer(modes[-3], self.pointer+3)

                if pointer_val < 0:
                    raise Exception("Attempted to write to negative index")
                
                self.mem[pointer_val] = int(var1 < var2)

                self.pointer+= 4
                pass
            case 8:
                logging.debug("8")
                var1 = self.find_pos(modes[-1], self.pointer+1)
                var2 = self.find_pos(modes[-2], self.pointer+2)
                
                pointer_val = self.find_pointer(modes[-3], self.pointer+3)

                if pointer_val < 0:
                    raise Exception("Attempted to write to negative index")
                
                self.mem[pointer_val] = int(var1 == var2)

                self.pointer+= 4
                pass
            case 9:
                logging.debug("9")
                var1 = self.find_pos(modes[-1], self.pointer+1)

                self.rel_base += var1
                self.pointer+= 2
            case 99:
                self.halted = True
                pass
            case _:
                raise Exception("Attempted to run command that does not exist")
            
        return None


class Directions:
    UP: tuple[int, int] = (0, -1)
    LEFT: tuple[int, int]  = (-1, 0)
    RIGHT: tuple[int, int]  = (1, 0)
    DOWN: tuple[int, int]  = (0, 1)


def main(root: str, run_type: Run = Run.TEST) -> int:
    if run_type == Run.TEST:
        with open(os.path.join(root, "test.txt"), 'r') as f:
            inp: list[str] = [line.strip() for line in f.readlines()]
    elif run_type == Run.REAL:
        with open(os.path.join(root, "input.txt"), 'r') as f:
            inp: list[str] = [line.strip() for line in f.readlines()]
    else:
        raise Exception("Error in getting run type")

    memory = {i: int(val) for (i, val) in enumerate(inp[0].split(","))}
    IntcodeCom = Computer(memory)

    grid: dict[int, dict[int, bool]] = {}

    start = [0, 0]
    grid[start[1]] = {}
    grid[start[1]][start[0]] = 0

    cur_pos = start
    cur_dir = Directions.UP
    dir_order = [Directions.UP, Directions.RIGHT, Directions.DOWN, Directions.LEFT]

    coloured = []

    while not IntcodeCom.halted:
        next_instruction = IntcodeCom.run_step(grid[cur_pos[1]][cur_pos[0]])
        while next_instruction is None and not IntcodeCom.halted:
            next_instruction = IntcodeCom.run_step(grid[cur_pos[1]][cur_pos[0]])
        
        colour = next_instruction

        next_instruction = IntcodeCom.run_step(grid[cur_pos[1]][cur_pos[0]])
        while next_instruction is None and not IntcodeCom.halted:
            next_instruction = IntcodeCom.run_step(grid[cur_pos[1]][cur_pos[0]])
        
        if IntcodeCom.halted:
            continue
    
        turn = next_instruction

        if turn:
            cur_dir = dir_order[(dir_order.index(cur_dir)+1)%4]
        else:
            cur_dir = dir_order[(dir_order.index(cur_dir)-1)%4]
        
        grid[cur_pos[1]][cur_pos[0]] = colour

        cur_pos[0] += cur_dir[0]
        cur_pos[1] += cur_dir[1]

        if cur_pos[1] not in grid:
            grid[cur_pos[1]] = {}

        if cur_pos[0] not in grid[cur_pos[1]]:
            grid[cur_pos[1]][cur_pos[0]] = 0

        if cur_pos not in coloured:
            coloured.append(cur_pos.copy())
    
    min_y = min(grid)
    max_y = max(grid)
    min_x = min([min(x) for x in grid.values()])
    max_x = max([max(x) for x in grid.values()])

    vis_grid = [["." for _ in range(max_x-min_x+1)] for __ in range(max_y-min_y+1)]

    for (y, x_vals) in grid.items():
        for (x, colour) in x_vals.items():
            vis_grid[y-min_y][x-min_x] = ".#"[colour]

    logging.debug('\n'.join([""]+["".join(line) for line in vis_grid]))

    return len(coloured)

if __name__ == "__main__":
    # Import libraries
    from aocd import submit

    import bs4
    import copier
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
                copier.make_next(year, day)
    
    elif run_type == Run.TEST:
        print(f"The answer is {test_ans}, you got {answer}.")

        if (test_ans == answer):
            print(f"You got it right! Time to submit!")
        else:
            print("Time to change ur code :(")
        
    else:
        raise Exception("Somehow run_type was not test or real")
