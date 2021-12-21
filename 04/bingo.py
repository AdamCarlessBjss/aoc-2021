#!/usr/bin/env python3

def parse_draws(filename):
    with open(filename, 'r') as fp:
        return(list(map(int, fp.readlines()[0].strip("\n").split(","))))

# split on empty lines, parse each chunk to array of board_data 
# create a bingo board from that data and add it to the list of boards
def parse_boards(filename):
    boards = []
    with open(filename, 'r') as fp:
        board_data = []
        for line in fp.readlines():
            if not line.strip("\n"):
                boards.append(BingoBoard(board_data))
                board_data.clear()
                continue
            line_vals = list(map(int, filter(None,line.strip("\n").split(" ",))))
            board_data.append(line_vals)
    return boards

class BingoBoard:
    def __init__(self, rows):

        # array of counters, one for each row & column of the board
        # each counter starts at number of unmarked values on that line
        # counts backwards to zero as numbers on the line are dibbed.
        self.lines = [0] * 10

        # map of all unmarked values on the board mapped to indexes of 
        # the 2 lines on which each number appears
        self.values = {}

        self.setup_board(rows)

    def dib(self, draw):
        shout_house = False
        if not self.values.get(draw):
            return False

        for index in self.values[draw]:
            self.lines[index] -= 1
            if self.lines[index] == 0:
                shout_house = True

        del self.values[draw]
        return shout_house

    def complete(self):
        for line in self.lines:
            if line == 0:
                return True
        return False

    def unmarked(self):
        return self.values.keys()

    def setup_board(self, rows):
        offset = 5
        for i, row in enumerate(rows):
            for j, col in enumerate(row):
                self.lines[i] += 1
                self.lines[offset+j] += 1
                self.values[col] = (i, offset+j)

def play_bingo(boards, draws):
    results = {}
    for board in boards:
        for i, draw in enumerate(draws):
            if board.dib(draw):
                score = sum(board.unmarked()) * draw
                results[i] = score
                print(f'House! On draw {i} ({draw}), with score {score}, unmarked entries are: {board.unmarked()}')
#                boards.remove(board)
                break
    return sorted(results, reverse=True)

draws = parse_draws("draws.txt")
boards = parse_boards("boards.txt")

results = play_bingo(boards, draws)
print({results})

