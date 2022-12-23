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
    
    min_x = min([x[0] for x in cubes])
    max_x = max([x[0] for x in cubes])
    min_y = min([x[1] for x in cubes])
    max_y = max([x[1] for x in cubes])
    min_z = min([x[2] for x in cubes])
    max_z = max([x[2] for x in cubes])
    
    air_cubes = []
    for x in range(min_x, max_x + 1):
        for y in range(min_y, max_y + 1):
            for z in range(min_z, max_z + 1):
                cur_cube = [x, y, z]
                if cur_cube not in cubes:
                    air_cubes.append(cur_cube)
    
    outer_cubes = [cube for cube in air_cubes if cube[0] in [min_x, max_x] or cube[1] in [min_y, max_y] or cube[2] in [min_z, max_z]]
    
    visited_cubes = []
    cube_stack = []
    for cube in outer_cubes:
        if cube not in visited_cubes:
            visited_cubes.append(cube)
        
        cube_stack = [cube]
    
        while 1:
            if cube_stack == []:
                break
    
            pos_moves = [c for c in air_cubes if touching(cube_stack[-1], c) and c not in visited_cubes]
    
            if pos_moves == []:
                cube_stack.pop()
                continue
    
            cube_stack.append(pos_moves[0])
            visited_cubes.append(pos_moves[0])
    
    inner_cubes = [c for c in air_cubes if c not in visited_cubes]
    
    for air in inner_cubes:
        for cube in cubes:
            if touching(air, cube):
                answer -= 1

    return answer
    
if __name__ == "__main__":
    from aocd import submit

    answer = main(not COMPLETE)
    
    if COMPLETE:
        r = submit(answer, year=year, day=day)
    else:
        print(answer)