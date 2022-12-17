from aocd import submit
import bs4
import copier
from functools import cache

COMPLETE = False
year, day = [2022, 16]

with open(r"2022\day16\input.txt", 'r') as f:
    inp = [line.strip() for line in f.readlines()]

name_dict = {}
valves = []
for (i, line) in enumerate(inp):
    name, rest = line.split(" has flow rate=")
    flow_rate, tunnels = rest.split("valve")
    name = name[-2:]
    flow_rate = int(flow_rate.split(";")[0])
    tunnels = [t.replace(",", "") for t in tunnels.split(" ")[1:]]
    valves.append([name, flow_rate, tunnels, False, i])
    name_dict.update({name: i})

for i in range(len(valves)):
    for (j, valve) in enumerate(valves[i][2]):
        valves[i][2][j] = name_dict[valve]

def dijkstras(num):
    nodes = []
    for v in valves:
        nodes.append([v[0], v[2], float('inf'), -1])

    last_node = nodes[num]
    nodes[num][2] = 0
    nodes[num][3] = 1
    while [node for node in nodes if node[3] == -1] != []:
        for node in last_node[1]:
            if nodes[node][3] == -1:
                nodes[node][2] = last_node[2] + 1
        
        last_node = sorted([node for node in nodes if node[3] == -1], key=lambda x: x[2])[0]
        last_node[3] = 1

    return [node[2] for node in nodes]

dist_matrix = [dijkstras(i) for i in range(len(valves))]

def recurFind(time, cur_node, nodes, score):
    choices = [node for node in nodes if time - dist_matrix[cur_node][node[4]] - 1 > 0 and not node[3] and node[1] > 0]

    scores = []
    for choice in choices:
        l = [n.copy() for n in nodes]
        l[choice[4]][3] = True
        r_time = time - dist_matrix[cur_node][choice[4]] - 1
        _score = recurFind(r_time, choice[4], l, score + choice[1]*r_time)
        for s in _score:
            scores.append([s, choice])

        scores.append([[score + choice[1]*r_time], choice])

    if choices == []:
        return [[score]]

    pos = []
    for (s, choice) in scores:
        if len(s) == 1:
            pos.append([s[0], [choice[4]]])
        else:
            pos.append([s[0], s[1] + [choice[4]]])

    return pos

solns = recurFind(26, 20, valves.copy(), 0)

total = len(solns)**2

answer = 0
for i in range(len(solns)):
    for j in range(len(solns)):
        if solns[i][0] + solns[j][0] > answer and set(solns[i][1]).intersection(set(solns[j][1])) == set():
            answer = solns[i][0] + solns[j][0]

if COMPLETE:
    r = submit(answer, year=year, day=day)
else:
    print(answer)
