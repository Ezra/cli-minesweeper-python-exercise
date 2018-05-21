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


class MinesweeperBoard(object):

    def __init__(self, width, height, num_mines):
        """Initialize a minesweeper board for play.
        width, height: dimensions
        num_mines: number of mines in the grid (must be less than width * height)"""

        if num_mines >= width * height:
            # this many mines could cause a naive mine-placement algorithm to loop indefinitely
            raise ValueError("too many mines")
        self.num_mines = num_mines
        self.width = width
        self.height = height

        self.knowledge = [[KnowledgeState.HIDDEN for x in range(width)] for y in range(height)]

        self.truth = None  # lazy-initialize these on first click to prevent first-click death
        self.neighbor_count = None

    def _count_neighboring_mines(self, x, y):
        return sum(
            self.truth[ny][nx]
            for ny in range(max(y - 1, 0), min(y + 2, self.height))
            for nx in range(max(x - 1, 0), min(x + 2, self.width))
            if not (nx == x and ny == y)
        )

    def _setup_mines(self, safe_x, safe_y):
        self.truth = [[False for x in range(self.width)] for y in range(self.height)]
        self.neighbor_count = [[0 for x in range(self.width)] for y in range(self.height)]

        # place a temporary mine in the safe space so we can remove it after
        x = safe_x
        y = safe_y
        # place num_mines more mines
        for __ in range(self.num_mines):
            self.truth[y][x] = True
            while self.truth[y][x]:
                x = random.randint(0, self.width - 1)  # randint range is inclusive for some reason
                y = random.randint(0, self.height - 1)
        self.truth[y][x] = True
        # remove our placeholder mine
        self.truth[safe_y][safe_x] = False

        # compute dangerous neighbors
        for y in range(self.height):
            for x in range(self.width):
                self.neighbor_count[y][x] = self._count_neighboring_mines(x, y)

    def step(self, x, y):
        """Try stepping at (x, y).
        If necessary, generate the board first, ensuring (x, y) is safe.
        Returns whether a mine was hit.
        """
        if not self.truth:
            self._setup_mines(x, y)

        if self.knowledge[y][x] == KnowledgeState.HIDDEN:
            self.knowledge[y][x] = KnowledgeState.STEPPED
            return self.truth[y][x]
        else:
            return False

    def _cell_str(self, x, y):
        if self.knowledge[y][x] == KnowledgeState.STEPPED:
            return '*' if self.truth[y][x] else str(self.neighbor_count[y][x])
        else:
            return str(self.knowledge[y][x])

    def _truth_str(self):
        return '\n'.join([''.join('!' if has_mine else '.' for has_mine in row) for row in self.truth])

    def __str__(self):
        return '\n'.join([''.join(self._cell_str(x, y) for x in range(self.width)) for y in range(self.height)])
