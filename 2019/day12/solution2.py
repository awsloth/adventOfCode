"""Module to solve part 2 of advent of code 2019-12"""
from enum import Enum
from typing import Generator
import os
import logging
year, day = [2019, 12]
ROOT_DIR: str = os.path.join(os.getcwd(), str(year), f"day{day}")

class Run(Enum):
    """Enum for program run type"""
    TEST = 0
    REAL = 1

def read_input(root: str, run_type: Run = Run.TEST) -> list[str]:
    """Function to read in input from test or input text file"""
    if run_type == Run.TEST:
        with open(os.path.join(root, "test.txt"), 'r', encoding="utf8") as f:
            out: list[str] = [line.strip() for line in f.readlines()]
    elif run_type == Run.REAL:
        with open(os.path.join(root, "input.txt"), 'r', encoding="utf8") as f:
            out: list[str] = [line.strip() for line in f.readlines()]

    return out

def run_step(
        planets: list[list[int]], planet_vel: list[list[int]]
        ) -> tuple[list[list[int]],list[list[int]]]:
    """Runs a step in the simulation"""
    for (i, planet1) in enumerate(planets):
        for (j, planet2) in enumerate(planets[i:]):
            for k in range(3):
                if planet1[k] > planet2[k]:
                    planet_vel[i][k] += -1
                    planet_vel[j+i][k] -= -1
                elif planet1[k] < planet2[k]:
                    planet_vel[i][k] += 1
                    planet_vel[j+i][k] -= 1

    planets = [[x+y for (x, y) in zip(vel, planet)] for vel, planet in zip(planet_vel, planets)]

    return planets, planet_vel

def calc_energy(planets: list[list[int]], planet_vel: list[list[int]]) -> int:
    """Calculates the total energy in the system"""
    total_energy: int = 0
    for (planet, velocity) in zip(planets, planet_vel):
        pot_energy = sum(abs(x) for x in planet)
        kin_energy = sum(abs(x) for x in velocity)
        total_energy += pot_energy * kin_energy

    return total_energy

def frmt_planet(planet: list[int]) -> str:
    """Formats a planet as a string"""
    return f"<x={planet[0]}, y={planet[1]}, z={planet[2]}>"

def frmt_velo(velo: list[int]) -> str:
    """Formats a velocity as a string"""
    return f"<x={velo[0]}, y={velo[1]}, z={velo[2]}>"

def state(planets: list[list[int]], planet_vel: list[list[int]]) -> list[str]:
    """Return the current states as an strings"""
    states = [[planet[i] for planet in planets] for i in range(3)]
    vel_states = [[vel[i] for vel in planet_vel] for i in range(3)]

    combined = [
        ",".join(str(x) for x in states[i])+"|"+",".join(str(x) for x in vel_states[i])
        for i in range(3)
    ]

    return combined

def primes_up_to_n(n: int) -> Generator[int, None, None]:
    """Gets all primes up to n"""
    for i in range(2, n+1):
        if not any(i%x==0 for x in range(2, i)):
            yield i

def prime_factorisation(num: int) -> dict[int, int]:
    """Gets prime factorisation of a number"""
    cur_num = num
    pos_factors = primes_up_to_n(num)
    cur_pos_factor = next(pos_factors)

    factors: dict[int, int] = {}
    while cur_num != 1:
        while cur_num % cur_pos_factor == 0:
            if cur_pos_factor not in factors:
                factors[cur_pos_factor] = 1
            else:
                factors[cur_pos_factor] += 1

            cur_num //= cur_pos_factor

        cur_pos_factor = next(pos_factors)

    return factors

def hcm(nums: list[int]) -> int:
    """Find highest common multiple"""
    factors = [prime_factorisation(num) for num in nums]

    total_set: set[int] = set()
    for factor in factors:
        total_set = total_set.union(set(factor.keys()))

    end_num = 1
    for num in total_set:
        end_num *= num ** max(factors[i][num] for i in range(len(factors)) if num in factors[i])

    return end_num


def main(root: str, run_type: Run = Run.TEST) -> int:
    """Function to run the solution"""
    inp = read_input(root, run_type)
    all_coords = [line.removeprefix("<").removesuffix(">").split(",") for line in inp]
    planets = [[int(x.strip()[2:]) for x in coord] for coord in all_coords]
    planet_vel = [[0 for _ in range(3)] for __ in range(len(all_coords))]

    state_sets: list[set[str]] = [set(), set(), set()]
    found_dup = [0, 0, 0]
    step = 0
    while not all(found_dup):
        if (step+1) % 10000 == 0:
            logging.info("Running step: %s", step+1)

        cur_states = state(planets, planet_vel)

        for i in range(3):
            if cur_states[i] in state_sets[i]:
                if not found_dup[i]:
                    found_dup[i] = step
                    logging.info("Found repeat on %s after %i steps", "xyz"[i], step)

            state_sets[i].add(cur_states[i])

        step += 1

        planets, planet_vel = run_step(planets, planet_vel)

        for (planet, velocity) in zip(planets, planet_vel):
            logging.debug("%s %s", frmt_planet(planet), frmt_velo(velocity))

    return hcm([found_dup[0],found_dup[1], found_dup[2]])

if __name__ == "__main__":
    # Import libraries
    from aocd import submit
    from urllib3 import BaseHTTPResponse

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
        r: BaseHTTPResponse | None = submit(ANSWER, year=year, day=day)
        if r is not None:
            if "That\\'s the right answer" in str(r.data):
                print("Yippee!")

    elif prog_run_type == Run.TEST:
        print(f"The answer is {test_ans}, you got {ANSWER}.")

        if test_ans == ANSWER:
            print("You got it right! Time to submit!")
        else:
            print("Time to change ur code :(")
