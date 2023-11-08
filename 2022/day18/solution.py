COMPLETE = False
year, day = [2022, 18]

def touching(cub1, cub2):
    if cub1[0] == cub2[0] and cub1[1] == cub2[1] and abs(cub1[2]-cub2[2]) == 1:
        return True
    if cub1[0] == cub2[0] and cub1[2] == cub2[2] and abs(cub1[1]-cub2[1]) == 1:
        return True
    if cub1[1] == cub2[1] and cub1[2] == cub2[2] and abs(cub1[0]-cub2[0]) == 1:
        return True
    return False

def main(enabled_print=True, test=False):
    if test:
        with open(r"2022\day18\test.txt", 'r') as f:
            inp = [line.strip() for line in f.readlines()]
    else:
        with open(r"2022\day18\input.txt", 'r') as f:
            inp = [line.strip() for line in f.readlines()]
    
    cubes = [[*map(int, line.split(","))] for line in inp]
    answer = len(cubes)*6
    for i in range(len(cubes)):
        for j in range(i+1, len(cubes)):
            answer -= 2*touching(cubes[i], cubes[j])
    
    return answer

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
