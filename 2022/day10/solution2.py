with open(r"2022\day10\input.txt", 'r') as f:
    inp = [line.strip() for line in f.readlines()]

instructions = []
for line in inp:
    if line.split(" ")[0] == "addx":
        instructions.append("addS")
        instructions.append(int(line.split(" ")[1]))
    else:
        instructions.append("noop")

pixels = (len(instructions)//40)*40
screen = [["_" for _ in range(40)] for __ in range(pixels//40)]
register = 1
for i in range(pixels):
    y, x = divmod(i, 40)
    if register - 1 <= x <= register + 1:
        screen[y][x] = "#"
    else:
        screen[y][x] = " "

    if type(instructions[i]) is int:
        register += instructions[i]
    

print(*map(''.join, screen), sep='\n')