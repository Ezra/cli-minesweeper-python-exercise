from enum import Enum


class MinesweeperKnowledgeState(Enum):
    HIDDEN = 1
    FLAGGED = 2
    STEPPED = 3


class MinesweeperCellState(object):
    def __init__(self, has_mine):
        self.has_mine = has_mine
        self.mine_neighbors = None


class MinesweeperBoard(object):

    def __init__(self, width, height, num_mines):

        if num_mines > width * height:
            # this many mines could cause a naive mine-placement algorithm to loop indefinitely
            raise ValueError("too many mines")

        self.knowledge = [[MinesweeperKnowledgeState.HIDDEN for x in range(width)] for y in range(height)]

        self.truth = None  # lazy-initialize this on first click to prevent first-click death
        self.num_mines = num_mines
        self.width = width
        self.height = height

    def _setup_mines(self):
        self.truth = [[MinesweeperCellState(False) for x in range(self.width)] for y in range(self.height)]

        for __ in range(self.num_mines):
            pass  # TODO place a mine
