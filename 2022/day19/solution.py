from aocd import submit
import bs4
import copier
import math

COMPLETE = True
year, day = [2022, 19]

with open(r"2022\day19\input.txt", 'r') as f:
    inp = [line.strip() for line in f.readlines()]

# inp = """Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian.
# Blueprint 2: Each ore robot costs 2 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 8 clay. Each geode robot costs 3 ore and 12 obsidian.""".split("\n")

# Parse Blueprints
blueprints = []
for line in inp:
    b_id, rest = line.split(":")
    ore, clay, obsidian, geode, *_ = rest.split(".")

    b_id = int(b_id.split(" ")[-1])
    ore = int(ore.split(" ")[5])
    clay = int(clay.split(" ")[5])
    o_content = obsidian.split(" ")
    obsidian = [int(o_content[5]), int(o_content[8])]
    g_content = geode.split(" ")
    geode = [int(g_content[5]), int(g_content[8])]

    blueprints.append([b_id, [ore, clay, obsidian, geode]])

# Find possible moves
def findMoves(cur_mats, info):
    choices = []
    if cur_mats[0] >= info[0]:
        choices.append(0)
    if cur_mats[0] >= info[1]:
        choices.append(1)
    if cur_mats[0] >= info[2][0] and cur_mats[1] >= info[2][1]:
        choices.append(2)
    if cur_mats[0] >= info[3][0] and cur_mats[2] >= info[3][1]:
        choices.append(3)

    return choices


# For each blueprint find optimised solution
answer = 0
for (b_id, info) in blueprints:
    cur_materials = [0, 0, 0, 0]
    cur_bots = [1, 0, 0, 0]

    # set initial state
    state = [cur_materials, cur_bots]
    states = [state]

    sub = [
        [info[0], 0, 0, 0],
        [info[1], 0, 0, 0],
        [info[2][0], info[2][1], 0, 0],
        [info[3][0], 0, info[3][1], 0]
    ]

    # Find max if each bot required
    max_ore_bots = max(info[0], info[1], info[2][0], info[3][0])
    max_clay_bots = info[2][1]
    max_obsidian_bots = info[3][1]

    max_clay_ratio = info[2][1] / info[2][0]
    max_obsidian_ratio = info[3][1] / info[3][0]

    # Iterate through each state in the time period
    for time in range(24):
        # Find max of each value at each time (reduces conditions)
        max_ore = max_ore_bots*(24 - time)
        max_clay = max_clay_bots*(24 - time)
        max_obsidian = max_obsidian_bots*(24 - time)
        max_vals = [max_ore, max_clay, max_obsidian, float('inf')]

        # Create new states from old
        new_states = []
        for state in states:
            # Get materials and bots from state
            mats, bots = state

            # Find choices
            choices = findMoves(mats, info)

            # print(choices, mats, info, bots, time, '', sep='\n')

            mats = [mats[i]+bots[i] for i in range(len(mats))]
            mats = [min(x, y) for (x, y) in zip(max_vals, mats)]

            # if bot above max bots or above ratio
            if bots[1] >= max_clay_bots or bots[1]/bots[0] >= max_clay_ratio + 1:
                # do not pick clay bots!!!!
                if 1 in choices:
                    choices = [c for c in choices if c != 1]

            if bots[2] >= max_obsidian_bots or bots[2]/bots[0] >= max_obsidian_ratio + 1:
                # do not pick obsidian bots!!!
                if 2 in choices:
                    choices = [c for c in choices if c != 2]

            if bots[0] >= max_ore_bots:
                # do not pick ore bots!!!
                if 0 in choices:
                    choices = [c for c in choices if c != 0]
            
            if 3 in choices:
                n_bots = bots.copy()
                n_bots[3] += 1
                n_mats = [mats[i]-sub[3][i] for i in range(len(mats))]
                if [n_mats, n_bots] not in new_states:
                    new_states.append([n_mats, n_bots])
            else:
                for choice in choices:
                    n_bots = bots.copy()
                    n_bots[choice] += 1
                    n_mats = [mats[i]-sub[choice][i] for i in range(len(mats))]
                    if [n_mats, n_bots] not in new_states:
                        new_states.append([n_mats, n_bots])

                if [mats.copy(), bots.copy()] not in new_states:
                    new_states.append([mats.copy(), bots.copy()])

        to_remove = []
        for i in range(len(new_states)):
            for j in range(i+1, len(new_states)):
                if new_states[i][1] == new_states[j][1]:
                    if all([c1 <= c2 for (c1, c2) in zip(new_states[i][0], new_states[j][0])]):
                        to_remove.append(i)
                        break
                    elif all([c1 <= c2 for (c1, c2) in zip(new_states[j][0], new_states[i][0])]):
                        if j not in to_remove:
                            to_remove.append(j)
                            continue
                if new_states[i][0] == new_states[j][0]:
                    if all([c1 <= c2 for (c1, c2) in zip(new_states[i][1], new_states[j][1])]):
                        to_remove.append(i)
                        break
                    elif all([c1 <= c2 for (c1, c2) in zip(new_states[j][1], new_states[i][1])]):
                        if j not in to_remove:
                            to_remove.append(j)
                            continue
        
        states = [new_states[i] for i in range(len(new_states)) if i not in to_remove]

    b_state = max(states, key= lambda x: x[0][3])
    print(b_state)
    answer += b_id * b_state[0][3]

if COMPLETE:
    r = submit(answer, year=year, day=day)
    soup = bs4.BeautifulSoup(r.text, "html.parser")
    message = soup.article.text
    if "That's the right answer" in message:
        copier.make_next()
else:
    print(answer)
