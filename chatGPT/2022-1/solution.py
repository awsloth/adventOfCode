calories = []

# read in the input and parse it into a list of integers
with open('chatGPT/2022-1/input.txt', 'r') as f:
    for line in f:
        if line.strip():  # ignore blank lines
            calories.append(int(line.strip()))

# group the calories by elf
elf_calories = {}
current_elf = 0
for calorie in calories:
    if calorie == 0:  # a blank line indicates the start of a new elf's inventory
        current_elf += 1
    if current_elf not in elf_calories:
        elf_calories[current_elf] = 0
    elf_calories[current_elf] += calorie

# sort the elves by the number of calories they're carrying in descending order
sorted_elf_calories = sorted(elf_calories.items(), key=lambda x: x[1], reverse=True)

# print out the total number of calories for the top three elves
top_three_calories = 0
for elf, calories in sorted_elf_calories[:3]:
    top_three_calories += calories
print(top_three_calories)
