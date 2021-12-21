import numpy as np


class Player():
    """ A class to represent a bingo player.

    Attributes:
        card -- 2d array representing the current state of the player's bingo card.

        score -- the sum of the non-marked squares on the player's board multiplied
        by the last called number.

        complete -- Boolean indicating whether the player has marked a winning line
        on their card.

        position -- The number of calls it took the player to complete their card.

    Methods:
        mark -- mark the called number if it is on the player's card.
    """

    def __init__(self, card):
        self._number = 0
        self.position = 0
        self.card = card
        self.card.extend(np.transpose(self.card))

    def mark(self, number):
        self._number = number
        self.card = [[square for square in row if square != self._number] for row in self.card]

    def get_score(self):
        return(self._number * sum(map(sum, self.card)) / 2)

    def get_complete(self):
        for row in self.card:
            if len(row) == 0:
                return(True)
        return(False)

    def set_position(self, position):
        self._position = position

    def get_position(self):
        return self._position

    score = property(get_score)
    complete = property(get_complete)
    position = property(get_position, set_position)


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


lines = []
with open('raw.txt', 'r') as input:
    for line in input:
        if line.strip():
            lines.append(line.split())

calls = list(map(int, "".join(lines.pop(0)).split(",")))
lines = [list(map(int, line)) for line in lines]
cards = list(chunks(lines, len(lines[0])))
players = [Player(card) for card in cards]
results = []

for player in players:
    for call in calls:
        player.mark(call)
        if player.complete:
            player.position = calls.index(call)
            results.append([player.position, player.score])
            break

results_sorted = sorted(results,key=lambda X: X[0])

print(f"First board wins with score: {results_sorted[0][1]}")
print(f"Last board completes with score: {results_sorted[-1][1]}")