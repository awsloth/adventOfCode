import os

def make_next(year, day):
    # Set root directory
    root = os.getcwd()

    # If file exists, do not run
    if os.path.exists(os.path.join(str(year), f"day{day}", "solution2.py")):
        print("File already exists!")
        exit(-1)
    
    # Get content of solution
    with open(os.path.join(str(year), f"day{day}", "solution.py"), "r") as f:
        lines = f.readlines()

    start_index = lines.index("root: str = os.path.join(os.getcwd(), str(year), f\"day{day}\")")
    end_index = lines.index('if __name__ == "__main__":\n')

    functions = lines[start_index+1:end_index]

    # Phrases to replace
    phrase_replace = {"$year$":str(year), "$day$":str(day), "$root$":root}

    # Open base solution
    with open("base_solution2.txt", "r") as s:

        # Open solution program
        with open(f"{year}/day{day}/solution2.py", 'w') as f:

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
    import sys
    if (len(sys.argv) != 3):
        print("Badly specified arguments")
        exit(-1)

    year = int(sys.argv[1]) 
    day = int(sys.argv[2])
    make_next(year, day)