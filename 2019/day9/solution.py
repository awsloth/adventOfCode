import os
import logging
year, day = [2019, 9]
root: str = os.path.join(os.getcwd(), str(year), f"day{day}")

class Run:
    TEST = 0
    REAL = 1

def find_pos(mode, pointer, rel_base, memory):
    match (mode):
        case 2:
            if memory[pointer]+rel_base not in memory:
                memory[memory[pointer]+rel_base] = 0
            
            return memory[memory[pointer]+rel_base]
        case 1:
            if pointer not in memory:
                memory[pointer] = 0

            return memory[pointer]
        case 0:
            if memory[pointer] not in memory:
                memory[memory[pointer]] = 0

            return memory[memory[pointer]]
        
def find_pointer(mode, pointer, rel_base, memory):
    match (mode):
        case 2:
            if memory[pointer]+rel_base not in memory:
                memory[memory[pointer]+rel_base] = 0
            
            return memory[pointer]+rel_base
        case 0:
            if memory[pointer] not in memory:
                memory[memory[pointer]] = 0

            return memory[pointer]

def main(root: str, run_type: Run = Run.TEST) -> int:
    if run_type == Run.TEST:
        with open(os.path.join(root, "test.txt"), 'r') as f:
            inp: list[str] = [line.strip() for line in f.readlines()]
    elif run_type == Run.REAL:
        with open(os.path.join(root, "input.txt"), 'r') as f:
            inp: list[str] = [line.strip() for line in f.readlines()]
    else:
        raise Exception("Error in getting run type")


    inp = inp[0]
    memory: dict[int, int] = {i: int(val) for (i, val) in enumerate(inp.split(","))}

    pointer = 0
    rel_base = 0
    running = True

    while running:
        cur_instruction = str(memory[pointer])[-2:]
        modes = [int(x) for x in str(memory[pointer])[:-2].rjust(3, "0")]
        match (int(cur_instruction)):
            case 1:
                var1 = find_pos(modes[-1], pointer+1, rel_base, memory)
                var2 = find_pos(modes[-2], pointer+2, rel_base, memory)

                pointer_val = find_pointer(modes[-3], pointer+3, rel_base, memory)

                if pointer_val < 0:
                    raise Exception("Attempted to write to negative index")

                logging.debug(f"Did {memory[pointer]} on {var1}({memory[pointer+1]}), {var2}({memory[pointer+2]}) to addr{pointer_val}")

                memory[pointer_val] = var1 + var2
                pointer += 4
                pass
            case 2:
                var1 = find_pos(modes[-1], pointer+1, rel_base, memory)
                var2 = find_pos(modes[-2], pointer+2, rel_base, memory)

                pointer_val = find_pointer(modes[-3], pointer+3, rel_base, memory)

                if pointer_val < 0:
                    raise Exception("Attempted to write to negative index")
                
                logging.debug(f"Did {memory[pointer]} on {var1}({memory[pointer+1]}), {var2}({memory[pointer+2]}) to addr{pointer_val}")

                memory[pointer_val] = var1 * var2
                pointer += 4
                pass
            case 3:
                pointer_val = find_pointer(modes[-1], pointer+1, rel_base, memory)

                if pointer_val < 0:
                    raise Exception("Attempted to write to negative index")
                
                memory[pointer_val] = 1 # Initial ID

                logging.debug(f"Did {memory[pointer]} to addr{pointer_val}")
                
                pointer += 2
                pass
            case 4:
                if modes[-1] == 2:
                    logging.info(f"Ouput: {memory[memory[pointer+1]+rel_base]}")
                    return memory[memory[pointer+1]+rel_base]
                elif modes[-1]:
                    logging.info(f"Output: {memory[pointer+1]}")
                    return memory[pointer+1]
                else:
                    logging.info(f"Output: {memory[memory[pointer+1]]}")
                    return memory[memory[pointer+1]]
                
                pointer += 2
            case 5:
                var1 = find_pos(modes[-1], pointer+1, rel_base, memory)
                var2 = find_pos(modes[-2], pointer+2, rel_base, memory)
                
                logging.debug(f"Did {memory[pointer]} on {var1}({memory[pointer+1]}), {var2}({memory[pointer+2]})")

                if var1:
                    pointer = var2
                else:
                    pointer += 3
            case 6:
                var1 = find_pos(modes[-1], pointer+1, rel_base, memory)
                var2 = find_pos(modes[-2], pointer+2, rel_base, memory)

                logging.debug(f"Did {memory[pointer]} on {var1}({memory[pointer+1]}), {var2}({memory[pointer+2]})")
                
                if not var1:
                    pointer = var2
                else:
                    pointer += 3
            case 7:
                var1 = find_pos(modes[-1], pointer+1, rel_base, memory)
                var2 = find_pos(modes[-2], pointer+2, rel_base, memory)
                
                pointer_val = find_pointer(modes[-3], pointer+3, rel_base, memory)

                if pointer_val < 0:
                    raise Exception("Attempted to write to negative index")
                
                logging.debug(f"Did {memory[pointer]} on {var1}({memory[pointer+1]}), {var2}({memory[pointer+2]}) to addr{pointer_val}")

                memory[pointer_val] = int(var1 < var2)

                pointer += 4
                pass
            case 8:
                var1 = find_pos(modes[-1], pointer+1, rel_base, memory)
                var2 = find_pos(modes[-2], pointer+2, rel_base, memory)
                
                pointer_val = find_pointer(modes[-3], pointer+3, rel_base, memory)

                if pointer_val < 0:
                    raise Exception("Attempted to write to negative index")
                
                logging.debug(f"Did {memory[pointer]} on {var1}({memory[pointer+1]}), {var2}({memory[pointer+2]}) to addr{pointer_val}")
                
                memory[pointer_val] = int(var1 == var2)

                pointer += 4
                pass
            case 9:
                var1 = find_pos(modes[-1], pointer+1, rel_base, memory)

                logging.debug(f"Did {memory[pointer]} to rel_base ({rel_base}) with {var1}({memory[pointer+1]})")

                rel_base += var1
                pointer += 2
            case 99:
                running = False
                pass
            case _:
                raise Exception("Attempted to run command that does not exist")


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
