from enum import Enum
import random


class KnowledgeState(Enum):
    HIDDEN = 1
    FLAGGED = 2
    STEPPED = 3

    def __str__(self):
        if self == self.HIDDEN:
            return '?'
        elif self == KnowledgeState.FLAGGED:
            return '#'
        elif self == KnowledgeState.STEPPED:
            return 'S'
        else:
            return 'E'


class EndState(Enum):
    DEFEAT = 1
    VICTORY = 2


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

        # track progress
        self.num_stepped = 0
        self.end_state = None

    def _neighbor_coordinates(self, x, y):
        return [
            (nx, ny)
            for ny in range(max(y - 1, 0), min(y + 2, self.height))
            for nx in range(max(x - 1, 0), min(x + 2, self.width))
            if not (nx == x and ny == y)
        ]

    def _count_neighboring_mines(self, x, y):
        return sum(self.truth[ny][nx] for nx, ny in self._neighbor_coordinates(x, y))

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
        Returns None if the game is running, or an EndState if it is not.
        """
        if not self.truth:
            self._setup_mines(x, y)

        if self.end_state:
            return self.end_state

        if self.knowledge[y][x] != KnowledgeState.HIDDEN:
            return self.end_state  # None. Can't step on a revealed or flagged space
        self.knowledge[y][x] = KnowledgeState.STEPPED
        self.num_stepped += 1

        if self.truth[y][x]:
            self.end_state = EndState.DEFEAT
            return self.end_state

        # recursively expand if it's a bare patch
        if not self.neighbor_count[y][x]:
            for nx, ny in self._neighbor_coordinates(x, y):
                if self.knowledge[ny][nx] == KnowledgeState.HIDDEN:
                    self.step(nx, ny)

        # check for victory
        if self.num_stepped + self.num_mines >= self.width * self.height:
            self.end_state = EndState.VICTORY
            for ny in range(self.height):
                for nx in range(self.width):
                    if self.truth[y][x]:
                        self.knowledge[y][x] = KnowledgeState.FLAGGED
            return self.end_state

        return self.end_state  # None

    def flag(self, x, y):
        """Place a flag at (x, y)."""

        if self.end_state:
            return
        if self.knowledge[y][x] != KnowledgeState.HIDDEN:
            return

        self.knowledge[y][x] = KnowledgeState.FLAGGED

    def unflag(self, x, y):
        """Remove a flag at (x, y)."""

        if self.end_state:
            return
        if self.knowledge[y][x] != KnowledgeState.FLAGGED:
            return

        self.knowledge[y][x] = KnowledgeState.HIDDEN

    def _cell_str(self, x, y):
        if self.knowledge[y][x] != KnowledgeState.STEPPED:
            return str(self.knowledge[y][x])
        elif self.truth[y][x]:
            return '*'
        elif not self.neighbor_count[y][x]:
            return '.'
        else:
            return str(self.neighbor_count[y][x])

    def _truth_str(self):
        contents = '\n'.join([''.join('!' if has_mine else '.' for has_mine in row) for row in self.truth])
        return self._add_indices(contents)

    def __str__(self):
        contents = '\n'.join([''.join(self._cell_str(x, y) for x in range(self.width)) for y in range(self.height)])
        return self._add_indices(contents)

    def _add_indices(self, contents):
        return '\n'.join(
            ['  ' + ''.join(str(x) for x in range(self.width))] +
            [' ' * (self.width + 2)] +
            [str(y) + ' ' + line for y, line in enumerate(contents.split('\n'))]
        )
