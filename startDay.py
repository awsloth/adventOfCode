# Import libraries
from aocd import get_data
import datetime
import os

# Set date
# now = datetime.datetime.now()
now = datetime.datetime(2021, 12, 11, 5)

# Check what day it is based on hour
if now.hour >= 5:
    cur_day = now.day
else:
    cur_day = now.day - 1

# Set year
year = now.year

# Set root directory
root = "C:\\Users\\Adam\\PythonProjects\\adventOfCode"

# Create files and directory if they do not exist
if not os.path.exists(os.path.join(root, str(year), f"day{cur_day}")):

    # Make directory
    os.makedirs(f"{year}/day{cur_day}")

    # Get input
    with open(f"{year}/day{cur_day}/input.txt", 'w') as f:
        content = get_data(year=year, day=cur_day)
        f.write(content)

    # Phrases to replace
    phrase_replace = {"$year$":str(year), "$day$":str(cur_day), "$root$":root}

    # Open base solution
    with open("base_solution.txt", "r") as s:

        # Open solution program
        with open(f"{year}/day{cur_day}/solution.py", 'w') as f:

            # For line in base solution, copy into solution program
            # replacing keyphrases
            for line in s.readlines():
                new_line = line
                for (key, value) in phrase_replace.items():
                    if key in new_line:
                        x = new_line.find(key)
                        new_line = new_line[:x] + value + new_line[x+len(key):]
                
                f.write(new_line)