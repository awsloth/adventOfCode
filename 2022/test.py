import os
import importlib
import json

root = os.getcwd()
year = "2022"

root = os.path.join(root, year)

with open(os.path.join(root, "answers.json"), 'r') as f:
    content = f.read()

answers = json.loads(content)

days = [day for day in os.listdir(root) if day not in ["answers.json", "test.py"]]
for day in sorted(days, key=lambda x: int(x[3:])):
    num = int(day[3:]) - 1

    cur_part = 'part1'
    s1 = importlib.import_module(f"{day}.solution")
    test_val = s1.main(False, test=True)
    assert test_val == answers['test'][cur_part][num], f"Failed test p1 for day {num+1}, got {test_val} should have {answers['test'][cur_part][num]}"
    real_val = s1.main(False)
    assert real_val == answers['real'][cur_part][num], f"Failed real p1 for day {num+1}, got {real_val} should have {answers['real'][cur_part][num]}"

    cur_part = 'part2'
    s2 = importlib.import_module(f"{day}.solution2")
    test_val = s2.main(False, test=True)
    assert test_val == answers['test'][cur_part][num], f"Failed test p2 for day {num+1}, got {test_val} should have {answers['test'][cur_part][num]}"
    real_val = s2.main(False)
    assert real_val == answers['real'][cur_part][num], f"Failed real p2 for day {num+1}, got {real_val} should have {answers['real'][cur_part][num]}"

    print(f"Passed {day}")