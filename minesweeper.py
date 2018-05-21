from __future__ import print_function, division, unicode_literals, absolute_import

from cmd import Cmd

from MinesweeperBoard import MinesweeperBoard


class MinesweeperCmd(Cmd):
    """Handle commands for a game of Minesweeper."""

    def do_exit(self, __):
        """Exit the game."""
        return True

    def do_quit(self, arg_string):
        """Exit the game. (Synonym for exit.)"""
        return self.do_exit(arg_string)

    def do_EOF(self, arg_string):
        """Exit the game. (Synonym for exit.)"""
        return self.do_exit(arg_string)


def main():
    # interpreter = MinesweeperCmd()
    # interpreter.cmdloop()
    board = MinesweeperBoard(6, 4, 6)
    board.step(1, 1)
    print(board._truth_str())
    print(board)


if __name__ == '__main__':
    main()
