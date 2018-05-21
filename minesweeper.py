from __future__ import print_function, division, unicode_literals, absolute_import

from cmd import Cmd

from MinesweeperBoard import MinesweeperBoard, EndState

WELCOME = 'Welcome to Minesweeper!'
NEW_GAME_ADVICE = 'Start a new game with "new WIDTH HEIGHT NUM_MINES".'
PLAY_ADVICE = 'Step, flag, and unflag with "(step|flag|unflag) X Y".'


class MinesweeperCmd(Cmd):
    """Handle commands for a game of Minesweeper."""

    def __init__(self):
        Cmd.__init__(self)
        self.board = None

        self.prompt = '(Minesweeper) '
        self.intro = '\n'.join(['', WELCOME, NEW_GAME_ADVICE, ''])

    # ----- game control -----

    def do_new(self, arg_string):
        """new WIDTH HEIGHT NUM_MINES
        Start a new game with the specified dimensions and number of mines."""
        try:
            width, height, num_mines = (int(arg) for arg in arg_string.split())
        except ValueError:
            return self.onecmd('help new')

        self.board = MinesweeperBoard(width, height, num_mines)

        print()
        print(PLAY_ADVICE)

        return False

    def _cleanup_game(self):
        self.board = None

    def do_end(self, __):
        """End the game, but don't exit the program."""
        self._cleanup_game()

    # ----- game play -----

    def do_step(self, arg_string):
        """step X Y
        Play a step at space X, Y."""
        if not self.board:
            return self.onecmd('help new')

        try:
            x, y = (int(arg) for arg in arg_string.split())
        except ValueError:
            return self.onecmd('help step')

        try:
            game_end = self.board.step(x, y)
        except IndexError:
            print('out of range')
            return False

        if game_end:
            print()
            print(self.board)
            print()
            if game_end == EndState.VICTORY:
                print('You win!!')
            elif game_end == EndState.DEFEAT:
                print('You lose.')

            self._cleanup_game()

        return False

    def do_flag(self, arg_string):
        """flag X Y
        Flag space X, Y as containing a mine."""
        if not self.board:
            return self.onecmd('help new')

        try:
            x, y = (int(arg) for arg in arg_string.split())
        except ValueError:
            return self.onecmd('help flag')

        self.board.flag(x, y)

    def do_mark(self, arg_string):
        """mark X Y
        Flag space X, Y as containing a mine."""
        if not self.board:
            return self.onecmd('help new')

        try:
            x, y = (int(arg) for arg in arg_string.split())
        except ValueError:
            return self.onecmd('help mark')

        self.board.flag(x, y)

    def do_unflag(self, arg_string):
        """flag X Y
        Remove flag from space X, Y."""
        if not self.board:
            return self.onecmd('help new')

        try:
            x, y = (int(arg) for arg in arg_string.split())
        except ValueError:
            return self.onecmd('help unflag')

        self.board.unflag(x, y)

    def do_unmark(self, arg_string):
        """mark X Y
        Remove flag from space X, Y."""
        if not self.board:
            return self.onecmd('help new')

        try:
            x, y = (int(arg) for arg in arg_string.split())
        except ValueError:
            return self.onecmd('help unmark')

        self.board.unflag(x, y)

    # ----- parser handling -----

    def _exit(self):
        print('Goodbye')
        return True

    def do_bye(self, __):
        """Exit the game."""
        return self._exit()

    def do_exit(self, __):
        """Exit the game."""
        return self._exit()

    def do_quit(self, __):
        """Exit the game."""
        return self._exit()

    def do_EOF(self, __):
        """Exit the game."""
        return self._exit()

    # ----- meta -----

    def precmd(self, line):
        if line != 'EOF':
            line = line.lower()
        return line

    def postcmd(self, stop, line):
        if stop:
            return True

        print()
        if self.board:
            print(self.board)
        else:
            print(NEW_GAME_ADVICE)

        return False


def main():
    interpreter = MinesweeperCmd()
    interpreter.cmdloop()


if __name__ == '__main__':
    main()
