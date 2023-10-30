import os
import importlib
import json
import time

root = os.getcwd()
year = "2022"

root = os.path.join(root, year)

with open(os.path.join(root, "answers.json"), 'r') as f:
    content = f.read()

answers = json.loads(content)

num_test = 100

days = [day for day in os.listdir(root) if day not in ["answers.json", "test.py", "times", "analyser.py"]]
for day in sorted(days, key=lambda x: int(x[3:])):
    num = int(day[3:]) - 1

    # Import programs
    s1 = importlib.import_module(f"{day}.solution")
    s2 = importlib.import_module(f"{day}.solution2")

    time_dict = {}

    t1 = []
    t2 = []
    t3 = []
    t4 = []

    for i in range(num_test):
        s = time.time()
        test_val = s1.main(False, test=True)
        assert test_val == answers['test']['part1'][num]
        t1.append(time.time() - s)

        s = time.time()
        real_val = s1.main(False)
        assert real_val == answers['real']['part1'][num]
        t2.append(time.time() - s)

        s = time.time()
        test_val = s2.main(False, test=True)
        assert test_val == answers['test']['part2'][num], f"Failed test p2 for day {num+1}, got {test_val} should have {answers['test'][cur_part][num]}"
        t3.append(time.time() - s)

        s = time.time()
        real_val = s2.main(False)
        assert real_val == answers['real']['part2'][num], f"Failed real p2 for day {num+1}, got {real_val} should have {answers['real'][cur_part][num]}"
        t4.append(time.time() - s)

        print(i,end=' ')


    print(f"\ndone {day}")
    time_dict['test'] = {}
    time_dict['test']['part1'] = t1
    time_dict['test']['part2'] = t2
    time_dict['real'] = {}
    time_dict['real']['part1'] = t3
    time_dict['real']['part2'] = t4

    content = json.dumps(time_dict)

    with open(os.path.join(root, "times", f"times_{day}.json"), 'w') as f:
        f.write(content)
