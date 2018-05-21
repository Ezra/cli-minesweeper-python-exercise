from enum import Enum
import random


class MinesweeperKnowledgeState(Enum):
    HIDDEN = 1
    FLAGGED = 2
    STEPPED = 3


class MinesweeperCellState(object):
    def __init__(self, has_mine):
        self.has_mine = has_mine
        self.mine_neighbors = None  # to be set when we know our neighbors


class MinesweeperBoard(object):

    def __init__(self, width, height, num_mines):
        if num_mines >= width * height:
            # this many mines could cause a naive mine-placement algorithm to loop indefinitely
            raise ValueError("too many mines")
        self.num_mines = num_mines
        self.width = width
        self.height = height

        self.knowledge = [[MinesweeperKnowledgeState.HIDDEN for x in range(width)] for y in range(height)]

        self.truth = None  # lazy-initialize this on first click to prevent first-click death

    def _truth_neighbors(self, x, y):
        return [
            self.truth[nx][ny]
            for ny in range(max(y - 1, 0), min(y + 2, self.height))
            for nx in range(max(x - 1, 0), min(x + 2, self.width))
            if nx != x and ny != y
        ]

    def _setup_mines(self, safe_x, safe_y):
        self.truth = [[MinesweeperCellState(False) for x in range(self.width)] for y in range(self.height)]

        # place a temporary mine in the safe space so we can remove it after
        x = safe_x
        y = safe_y
        # place num_mines more mines
        for __ in range(self.num_mines):
            self.truth[x][y].has_mine = True
            while self.truth[x][y].has_mine:
                x = random.randint(0, self.width)
                y = random.randint(0, self.height)
        self.truth[x][y].has_mine = True
        # remove our placeholder mine
        self.truth[safe_x][safe_y].has_mine = False

        # compute dangerous neighbors
        for y in range(self.height):
            for x in range(self.width):
                self.truth[x][y].mine_neighbors = sum(neighbor.has_mine for neighbor in self._truth_neighbors(x, y))

    def step(self, x, y):
        if not self.truth:
            self._setup_mines(x, y)
