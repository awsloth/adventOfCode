import os
year, day = [2019, 6]
root = os.path.join(os.getcwd(), str(year), f"day{day}")

def main(enabled_print=True, test=False, debug=False):
    if debug:
        with open(os.path.join(root, "input.txt"), 'r') as f:
            inp = [line.strip() for line in f.readlines()]
    elif test:
        with open(os.path.join(root, "test.txt"), 'r') as f:
            inp = [line.strip() for line in f.readlines()]
    else:
        with open(os.path.join(root, "input.txt"), 'r') as f:
            inp = [line.strip() for line in f.readlines()]

    planets: dict[str, list[str]]= {}

    for line in inp:
        planet1, planet2 = line.split(")")
        if planet1 not in planets.keys():
            planets[planet1] = [planet2]
        else:
            planets[planet1].append(planet2)

    orbiters = set()
    for orbits in [set(x) for x in planets.values()]:
        orbiters = orbiters.union(orbits)

    if enabled_print:
        print(planets)
        print(set([*planets.keys()]))
        print(orbiters)

    base = list(set(planets.keys()).difference(orbiters))[0]
    all_planets = set(planets.keys()).union(orbiters)

    if enabled_print:
        print(base)

    planet_routes = {}
    found = set()
    stack = []
    cur_node = base
    while set(found) != all_planets:
        stack.append(cur_node)
        found.add(cur_node)
        planet_routes[cur_node] = stack.copy()
        if cur_node not in planets.keys():
            pos_routes = []
        
        else:
            pos_routes = set(planets[cur_node]).difference(found)

        if len(pos_routes) == 0:
            if len(stack) == 1:
                continue
            cur_node = stack[-2]
            stack.pop()
            stack.pop()
        
        else:
            cur_node = list(pos_routes)[0]

    if enabled_print:
        print(planet_routes['SAN'], planet_routes['YOU'])

    i = 0
    while planet_routes['SAN'][i] == planet_routes['YOU'][i]:
        i += 1

    return len(planet_routes['SAN']) + len(planet_routes['YOU']) - 2 * (i + 1)

if __name__ == "__main__":
    from aocd import submit

    import bs4
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

    answer = main(not complete, run_test, complete)
    
    if run_test:
        print(f"The answer is {test_ans}, you got {answer}.")
        if (test_ans == answer):
            print(f"You got it right! Time to submit!")
        else:
            print("Time to change ur code :(")
    elif complete:
        r = submit(answer, year=year, day=day)
        if r is not None:
            soup = bs4.BeautifulSoup(r.data, "html.parser")
            message = soup.article.text
            if "That's the right answer" in message:
                print("Yippee!")
    else:
        print(f"You got {answer}")