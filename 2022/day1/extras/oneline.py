with open(r"C:\Users\Adam\PythonProjects\adventOfCode\2022\day1\input.txt", 'r') as f:print([*sorted([sum(map(int, nums[:-1].split("/"))) for nums in "".join([[line.strip()+"/","."][line == '\n'] for line in f.readlines()]).split(".")], reverse=True)][0])