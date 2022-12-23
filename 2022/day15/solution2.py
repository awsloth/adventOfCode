COMPLETE = False
year, day = [2022, 15]

def main(enabled_print=True, test=False):
    if test:
        with open(r"2022\day15\test.txt", 'r') as f:
            inp = [line.strip() for line in f.readlines()]
    else:
        with open(r"2022\day15\input.txt", 'r') as f:
            inp = [line.strip() for line in f.readlines()]
    
    sensors = []
    for line in inp:
        sensor, beacon = line.split(":")
        index = sensor.index("x=")
        sensor = sensor[index:].split(",")
        s_x = int(sensor[0].split("=")[1])
        s_y = int(sensor[1].split("=")[1])
    
        index = beacon.index("x=")
        beacon = beacon[index:].split(",")
        b_x = int(beacon[0].split("=")[1])
        b_y = int(beacon[1].split("=")[1])
    
        dist = abs(s_x-b_x) + abs(s_y-b_y)
        sensors.append([[s_x, s_y], dist])
    
    for row in range(4_000_000):
        covered = []
        for (s_pos, dist) in sensors:
            y_dist = abs(s_pos[1]-row)
            if dist < y_dist:
                continue
            x_dif = dist-y_dist
            potential = [s_pos[0]-x_dif, s_pos[0]+x_dif]
            covered.append(potential)
    
        covered = sorted(covered, key=lambda x: x[0])
        disjoint_sets = []
        found_solution = False
        while len(covered) > 1:
            n_covered = []
            for (set1, set2) in zip(covered[::2], covered[1::2]):
                if set1[0] <= set2[0] and set1[1] >= set2[1]:
                    n_covered.append(set1)
                elif set1[1] >= set2[0]:
                    n_covered.append([set1[0], set2[1]])
                else:
                    n_covered.append(set1)
                    n_covered.append(set2)
                    if len(n_covered) == 2:
                        disjoint_sets.append(set1)
                        disjoint_sets.append(set2)
                        found_solution = True
                        break
    
            if found_solution:
                break
        
            if len(covered) % 2:
                n_covered.append(covered[-1])
    
            covered = n_covered.copy()
    
        if found_solution:
            answer = (disjoint_sets[0][1] + 1)*4_000_000 + row
            break
    
        if covered[0][0] > 0:
            answer = row
            break
        elif covered[0][1] < 4_000_000:
            answer = 4_000_000*4_000_000 + row
            break
    
        if enabled_print:
            if row % 20000 == 0:
                print(f"{row/40_000:.1f}%")

    return answer
    
if __name__ == "__main__":
    from aocd import submit

    answer = main(not COMPLETE)
    
    if COMPLETE:
        r = submit(answer, year=year, day=day)
    else:
        print(answer)

