"""Module to create the files needed to code a solution to an advent of code problem"""
import datetime
import os
import sys

from aocd import get_data

args: list[str] = [x.lower() for x in sys.argv]
first_two_chars = [x[:2] for x in args]

now = datetime.datetime.now()

year = None
day = None

if "-y" in first_two_chars:
    # Year argument
    valid = False
    for arg in args:
        if "-y" in arg and "=" in arg:
            try:
                year = int(arg.removeprefix("-y="))
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
                day = int(arg.removeprefix("-d="))
                valid = True
            except ValueError as err:
                raise ValueError("Invalid input for day, takes integer input") from err

    if not valid:
        raise ValueError("Invalid format for day specifier, takes form -d=<day>")

if year is None:
    year = now.year
if day is None:
    day = now.day

# Set new date
now = datetime.datetime(year, 12, day, 5)

# Check what day it is based on hour
if now.hour >= 5:
    cur_day = now.day
else:
    cur_day = now.day - 1

# Set year
year = now.year
day = now.day

# Set root directory
root = os.getcwd()

# Create files and directory if they do not exist
if not os.path.exists(os.path.join(root, str(year), f"day{cur_day}")):

    # Make directory
    os.makedirs(f"{year}/day{cur_day}")

    # Make directory for 2023 (25 languages challenge)
    if year == 2023:
        os.makedirs(f"{year}/day{cur_day}/varied_solution")

# Get input
with open(f"{year}/day{cur_day}/input.txt", 'w', encoding="utf8") as f:
    content = get_data(year=year, day=cur_day)
    f.write(content)

with open(f"{year}/day{cur_day}/test.txt", 'w', encoding="utf8") as f:
    pass

# Phrases to replace
phrase_replace = {"$year$":str(year), "$day$":str(cur_day)}

# Open base solution
with open("base_solution.txt", "r", encoding="utf8") as s:

    # Open solution program
    with open(f"{year}/day{cur_day}/solution.py", 'w', encoding="utf8") as f:

        # For line in base solution, copy into solution program
        # replacing keyphrases
        for line in s.readlines():
            new_line = line
            for (key, value) in phrase_replace.items():
                if key in new_line:
                    x = new_line.find(key)
                    new_line = new_line[:x] + value + new_line[x+len(key):]

            f.write(new_line)
