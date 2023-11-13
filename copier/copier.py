"""Module to copy the solution1 code into a solution2 file for quickly starting part 2"""
import os

def make_next(year: int, day: int) -> None:
    """Makes the next file"""

    # If file exists, do not run
    if os.path.exists(os.path.join(str(year), f"day{day}", "solution2.py")):
        raise FileExistsError("File already exists!")

    # Get content of solution
    with open(os.path.join(str(year), f"day{day}", "solution.py"), "r", encoding="utf8") as f:
        lines = f.readlines()

    start_index = lines.index('ROOT_DIR: str = os.path.join(os.getcwd(), str(year), f"day{day}")\n')

    end_index = lines.index('if __name__ == "__main__":\n')

    functions = lines[start_index+1:end_index]

    # Phrases to replace
    phrase_replace = {"$year$":str(year), "$day$":str(day)}

    # Open base solution
    with open("base_solution2.txt", "r", encoding="utf8") as s:

        # Open solution program
        with open(f"{year}/day{day}/solution2.py", 'w', encoding="utf8") as f:

            # For line in base solution, copy into solution program
            # replacing keyphrases
            for line in s.readlines():
                if line == "<-TO REPLACE->\n":
                    for f_line in functions:
                        f.write(f_line)
                    continue

                new_line = line
                for (key, value) in phrase_replace.items():
                    if key in new_line:
                        x = new_line.find(key)
                        new_line = new_line[:x] + value + new_line[x+len(key):]

                f.write(new_line)

if __name__ == "__main__":
    import datetime
    import sys

    args = [x.lower() for x in sys.argv]
    first_two_chars = [x[:2] for x in args]

    now = datetime.datetime.now()

    cur_year = None
    cur_day = None

    if "-y" in first_two_chars:
        # Year argument
        valid = False
        for arg in args:
            if "-y" in arg and "=" in arg:
                try:
                    cur_year = int(arg.removeprefix("-y="))
                    valid = True
                except ValueError as err:
                    raise ValueError("Invalid input for year") from err

        if not valid:
            raise ValueError("Invalid format for year specifier, takes form -y=<year>")

    if "-d" in first_two_chars:
        # Year argument
        valid = False
        for arg in args:
            if "-d" in arg and "=" in arg:
                try:
                    cur_day = int(arg.removeprefix("-d="))
                    valid = True
                except ValueError as err:
                    raise ValueError("Invalid input for day, takes integer input") from err

        if not valid:
            raise ValueError("Invalid format for day specifier, takes form -d=<day>")

    if cur_year is None:
        cur_year = now.year
    if cur_day is None:
        cur_day = now.day

    make_next(cur_year, cur_day)
