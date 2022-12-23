COMPLETE = False
year, day = [2022, 15]

def main(enabled_print=True, test=False):
    if test:
        with open(r"2022\day15\test.txt", 'r') as f:
            inp = [line.strip() for line in f.readlines()]
    else:
        with open(r"2022\day15\input.txt", 'r') as f:
            inp = [line.strip() for line in f.readlines()]

    if test:
        row = 10
    else:
        row = 2_000_000
    
    beacons = []
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
    
        if b_y == row:
            beacons.append(b_x)
    
        dist = abs(s_x-b_x) + abs(s_y-b_y)
        sensors.append([[s_x, s_y], dist])
    
    pos = []
    for (s_pos, dist) in sensors:
        if abs(row - s_pos[1]) > dist:
            continue
    
        pos.append(s_pos[0])
        for i in range(1, dist - abs(row - s_pos[1])+1):
            pos.append(s_pos[0]+i)
            pos.append(s_pos[0]-i)
    
    pos = set(pos).difference(set(beacons))
    
    return len(pos)

if __name__ == "__main__":
    from aocd import submit

    import bs4
    import copier

    answer = main(not COMPLETE)
    
    if COMPLETE:
        r = submit(answer, year=year, day=day)
        soup = bs4.BeautifulSoup(r.text, "html.parser")
        message = soup.article.text
        if "That's the right answer" in message:
            copier.make_next(year, day)
    else:
        print(answer)
