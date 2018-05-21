from enum import Enum
import random


class KnowledgeState(Enum):
    HIDDEN = 1
    FLAGGED = 2
    STEPPED = 3

    def __str__(self):
        if self == self.HIDDEN:
            return '#'
        elif self == KnowledgeState.FLAGGED:
            return '*'
        elif self == KnowledgeState.STEPPED:
            return '_'
        else:
            return 'E'


class TruthState(object):
    def __init__(self, has_mine):
        self.has_mine = has_mine
        self.mine_neighbors = None  # to be set when we know our neighbors

    def __str__(self):
        if self.has_mine:
            return '*'
        elif self.mine_neighbors is not None:
            return str(self.mine_neighbors)
        else:
            return 'E'


class MinesweeperBoard(object):

    def __init__(self, width, height, num_mines):
        if num_mines >= width * height:
            # this many mines could cause a naive mine-placement algorithm to loop indefinitely
            raise ValueError("too many mines")
        self.num_mines = num_mines
        self.width = width
        self.height = height

        self.knowledge = [[KnowledgeState.HIDDEN for x in range(width)] for y in range(height)]

        self.truth = None  # lazy-initialize this on first click to prevent first-click death

    def _truth_neighbors(self, x, y):
        return [
            self.truth[ny][nx]
            for ny in range(max(y - 1, 0), min(y + 2, self.height))
            for nx in range(max(x - 1, 0), min(x + 2, self.width))
            if not (nx == x and ny == y)
        ]

    def _setup_mines(self, safe_x, safe_y):
        self.truth = [[TruthState(False) for x in range(self.width)] for y in range(self.height)]

        # place a temporary mine in the safe space so we can remove it after
        x = safe_x
        y = safe_y
        # place num_mines more mines
        for __ in range(self.num_mines):
            self.truth[y][x].has_mine = True
            while self.truth[y][x].has_mine:
                x = random.randint(0, self.width - 1)  # randint range is inclusive for some reason
                y = random.randint(0, self.height - 1)
        self.truth[y][x].has_mine = True
        # remove our placeholder mine
        self.truth[safe_y][safe_x].has_mine = False

        # compute dangerous neighbors
        for y in range(self.height):
            for x in range(self.width):
                self.truth[y][x].mine_neighbors = sum(neighbor.has_mine for neighbor in self._truth_neighbors(x, y))

    def step(self, x, y):
        if not self.truth:
            self._setup_mines(x, y)

        if self.knowledge[y][x] == KnowledgeState.HIDDEN:
            self.knowledge[y][x] = KnowledgeState.STEPPED
            return self.truth[y][x].has_mine

    def _cell_str(self, x, y):
        return str(
            self.truth[y][x]
            if self.knowledge[y][x] == KnowledgeState.STEPPED
            else self.knowledge[y][x]
        )

    def _truth_str(self):
        return '\n'.join([''.join(str(cell) for cell in row) for row in self.truth])

    def __str__(self):
        return '\n'.join([''.join(self._cell_str(x, y) for x in range(self.width)) for y in range(self.height)])
