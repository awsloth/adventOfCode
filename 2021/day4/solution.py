COMPLETE = False
year, day = [2021, 4]

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

def main(enabled_print=True, test=False):
    if test:
        with open(r"2021\day4\test.txt", 'r') as f:
            inp = [line.strip() for line in f.readlines()]
    else:
        with open(r"2021\day4\input.txt", 'r') as f:
            inp = [line.strip() for line in f.readlines()]       
    
    calls = [*map(int, inp[0].split(","))]
    boards = []
    for (r1, r2, r3, r4, r5, _) in zip(inp[2::6], inp[3::6], inp[4::6], inp[5::6], inp[6::6], inp[7::6]):
        boards.append(Board([r1, r2, r3, r4, r5]))
    
    complete = False
    i = 0
    while not complete:
        for board in boards:
            board.getNum(calls[i])
            if board.won():
                complete = True
                return board.nonCalled() * calls[i]
    
        i += 1

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
