import os
year, day = [2021, 11]
root = f"C:\\Users\\Adam\\PythonProjects\\adventOfCode\\{year}\\day{day}"
root = f"C:\\Users\\Adam\\PythonProjects\\adventOfCode\\{year}\\day{day}"

def step(grid):
    grid = [[x+1 for x in line] for line in grid]

    return grid

def finished(grid, flashed):
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (grid[i][j] > 9 and not flashed[i][j]):
                return False
            
    return True

def flash(grid, enabled_print):
    flashed = [[0 for _ in line] for line in grid]
    while (not finished(grid, flashed)):
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                if (grid[i][j] > 9 and not flashed[i][j]):
                    # Set to flashed
                    flashed[i][j] = 1

                    # Update surrounding
                    if (i-1 >= 0):
                        if (j-1 >= 0):
                            grid[i-1][j-1] += 1
                        if (j+1 < len(grid[i])):
                            grid[i-1][j+1] += 1
                        grid[i-1][j] += 1

                    if (j-1 >= 0):
                        grid[i][j-1] += 1
                    if (j+1 < len(grid[i])):
                        grid[i][j+1] += 1

                    if (i+1 < len(grid)):
                        if (j-1 >= 0):
                            grid[i+1][j-1] += 1
                        if (j+1 < len(grid[i])):
                            grid[i+1][j+1] += 1
                        grid[i+1][j] += 1

    # Process all > 9 to be 0
    grid = [[[x, 0][x > 9] for x in line] for line in grid]

    return grid, sum([sum(line) for line in flashed])

def main(enabled_print=True, test=False):
    if test:
        with open(os.path.join(root, "test.txt"), 'r') as f:
            inp = [line.strip() for line in f.readlines()]
    else:
        with open(os.path.join(root, "input.txt"), 'r') as f:
            inp = [line.strip() for line in f.readlines()]

    grid = [[int(x) for x in line] for line in inp]

    steps = 0
    total_flash = 0
    while (total_flash != len(grid)*len(grid[0])):
        grid = step(grid)
        grid, count = flash(grid, enabled_print)
        total_flash = count
        steps += 1
    
    return steps

if __name__ == "__main__":
    from aocd import submit
    import bs4
    import copier
    import sys

    if (len(sys.argv) < 3):
        print("Enter command line arguments")
        exit(-1)
    
    arg_list = sys.argv[1:]
    complete = arg_list[0].lower() == "true"
    run_test = arg_list[1].lower() == "true"

    if (len(sys.argv) == 4):
        test_ans = int(sys.argv[3])
    elif (run_test):
        print("Provide answer to test")
        exit(-1)

    if (run_test and not os.path.exists(os.path.join(root, "test.txt"))):
        print("Test file does not exist")
        exit(-1)

    answer = main(not complete, run_test)

    if complete:
        r = submit(answer, year=year, day=day)
        soup = bs4.BeautifulSoup(r.text, "html.parser")
        message = soup.article.text
        if "That's the right answer" in message:
            print("YIPPEE!")
    elif run_test:
        print(f"The answer is {test_ans}, you got {answer}.")
        if (test_ans == answer):
            print(f"You got it right! Time to submit!")
        else:
            print("Time to change ur code :(")
    else:
        print(f"You got {answer}")