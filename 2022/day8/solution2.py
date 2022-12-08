from aocd import submit
import bs4
import copier

COMPLETE = True
year, day = [2022, 8]

with open(r"2022\day8\input.txt", 'r') as f:
    inp = [line.strip() for line in f.readlines()]

row_valid = [[1 for _ in range(len(inp[0]))] for __ in range(len(inp))]
column_valid = [[1 for _ in range(len(inp))] for __ in range(len(inp[0]))]

for j in range(len(inp)):
    row = [int(x) for x in inp[j]]
    for i in range(len(row)):
        score = 1
        # Left side
        if i == 0:
            score = 0
        else:
            left = [*reversed(row[:i])]
            if max(left) < row[i]:
                score *= len(left)
            else:
                pos = 0
                while left[pos] < row[i]:
                    pos += 1

                pos += 1

                score *= pos
        
        # Right side
        if i == len(row) - 1:
            score = 0
        else:
            right = row[i+1:]
            if max(right) < row[i]:
                score *= len(right)
            else:
                pos = 0
                while right[pos] < row[i]:
                    pos += 1

                pos += 1

                score *= pos

        row_valid[j][i] = score

for j in range(len(inp[0])):
    column = [int(x[j]) for x in inp]
    for i in range(len(column)):
        score = 1
        # Left side
        if i == 0:
            score = 0
        else:
            left = [*reversed(column[:i])]
            if max(left) < column[i]:
                score *= len(left)
            else:
                pos = 0
                while left[pos] < column[i]:
                    pos += 1
                
                pos += 1

                score *= pos
        
        # Right side
        if i == len(column) - 1:
            score = 0
        else:
            right = column[i+1:]
            if max(right) < column[i]:
                score *= len(right)
            else:
                pos = 0
                while right[pos] < column[i]:
                    pos += 1

                pos += 1

                score *= pos

        column_valid[i][j] = score

valids = [[(column_valid[j][i] * row_valid[j][i]) for i in range(len(row_valid[j]))] for j in range(len(row_valid))]

end = []
for valid in valids:
    end += valid

answer = max(end)

if COMPLETE:
    submit(answer, year=year, day=day)
else:
    print(answer)
