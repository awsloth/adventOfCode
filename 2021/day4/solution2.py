from aocd import submit
import bs4
import copier

root = r"C:\Users\Adam\PythonProjects\adventOfCode\2021"

COMPLETE = True
year, day = [2021, 4]

with open(r"C:\Users\Adam\PythonProjects\adventOfCode\2021\day4\input.txt", 'r') as f:
    inp = [line.strip() for line in f.readlines()]

class Board:
    def __init__(self, board):
        self.board = [[*map(int, line.strip().split())] for line in board]
        self.hit = [[0 for _ in range(len(board[0].split()))] for __ in range(len(board))]

    def getNum(self, num):
        for (i, row) in enumerate(self.board):
            if num in row:
                self.hit[i][row.index(num)] = 1

    def won(self):
        for row in self.hit:
            if all(row):
                return True
        
        for i in range(len(self.board[0])):
            if all([row[i] for row in self.hit]):
                return True

        return False

    def nonCalled(self):
        nums = []
        for i in range(len(self.hit)):
            for j in range(len(self.hit[0])):
                if not self.hit[i][j]:
                    nums.append(self.board[i][j])

        return sum(nums)      

inp += ['']  

calls = [*map(int, inp[0].split(","))]
boards = []
for (r1, r2, r3, r4, r5, _) in zip(inp[2::6], inp[3::6], inp[4::6], inp[5::6], inp[6::6], inp[7::6]):
    boards.append(Board([r1, r2, r3, r4, r5]))

complete = [0 for _ in range(len(boards))]
i = -1
while (complete.count(0) > 0):
    i += 1
    for (j, board) in enumerate(boards):
        if not complete[j]:
            board.getNum(calls[i])
            if board.won():
                complete[j] = 1
                last = j


answer = boards[last].nonCalled()*calls[i]

if COMPLETE:
    submit(answer, year=year, day=day)
else:
    print(answer)
