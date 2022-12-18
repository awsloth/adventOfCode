from aocd import submit
import bs4
import copier

COMPLETE = False
year, day = [2022, 18]

with open(r"2022\day18\input.txt", 'r') as f:
    inp = [line.strip() for line in f.readlines()]

# inp = """2,2,2
# 1,2,2
# 3,2,2
# 2,1,2
# 2,3,2
# 2,2,1
# 2,2,3
# 2,2,4
# 2,2,6
# 1,2,5
# 3,2,5
# 2,1,5
# 2,3,5""".split("\n")

def touching(cub1, cub2):
    if cub1[0] == cub2[0] and cub1[1] == cub2[1] and abs(cub1[2]-cub2[2]) == 1:
        return True
    if cub1[0] == cub2[0] and cub1[2] == cub2[2] and abs(cub1[1]-cub2[1]) == 1:
        return True
    if cub1[1] == cub2[1] and cub1[2] == cub2[2] and abs(cub1[0]-cub2[0]) == 1:
        return True
    return False


cubes = [[*map(int, line.split(","))] for line in inp]
answer = len(cubes)*6
for i in range(len(cubes)):
    for j in range(i+1, len(cubes)):
        answer -= 2*touching(cubes[i], cubes[j])

if COMPLETE:
    r = submit(answer, year=year, day=day)
    soup = bs4.BeautifulSoup(r.text, "html.parser")
    message = soup.article.text
    if "That's the right answer" in message:
        copier.make_next()
else:
    print(answer)
