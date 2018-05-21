from __future__ import print_function, division, unicode_literals, absolute_import

from cmd import Cmd

from MinesweeperBoard import MinesweeperBoard

NEW_GAME_ADVICE = 'Start a new game with "new WIDTH HEIGHT NUM_MINES".'


class MinesweeperCmd(Cmd):
    """Handle commands for a game of Minesweeper."""

    def __init__(self):
        Cmd.__init__(self)
        self.board = None
        print(NEW_GAME_ADVICE)

    # ----- game control -----

    def do_new(self, arg_string):
        """new WIDTH HEIGHT NUM_MINES
        Start a new game with the specified dimensions and number of mines."""
        try:
            width, height, num_mines = (int(arg) for arg in arg_string.split())
        except ValueError:
            return self.onecmd("help new")

        self.board = MinesweeperBoard(width, height, num_mines)

    def do_end(self, __):
        """End the game, but don't exit the program."""
        self.board = None

    # ----- game play -----

    def do_step(self, arg_string):
        """step X Y
        Play a step at space X, Y."""
        if not self.board:
            return self.onecmd("help new")

        try:
            x, y = (int(arg) for arg in arg_string.split())
        except ValueError:
            return self.onecmd("help step")

        try:
            game_end = self.board.step(x, y)
        except IndexError:
            print('out of range')
            return False

        # TODO: if the game is done, print something interesting and discard it

    # ----- parser handling -----

    def do_exit(self, __):
        """Exit the game."""
        print('Goodbye')
        return True

    def do_quit(self, arg_string):
        """Exit the game. (Synonym for exit.)"""
        return self.do_exit(arg_string)

    def do_EOF(self, arg_string):
        """Exit the game. (Synonym for exit.)"""
        return self.do_exit(arg_string)

    # ----- meta -----

    def precmd(self, line):
        line = line.lower()
        return line

    def postcmd(self, stop, line):
        print()
        if self.board:
            print(self.board)
        else:
            print(NEW_GAME_ADVICE)
        return stop


def main():
    interpreter = MinesweeperCmd()
    interpreter.cmdloop()


if __name__ == '__main__':
    main()
