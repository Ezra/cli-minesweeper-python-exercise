from __future__ import print_function, division, unicode_literals, absolute_import

from cmd import Cmd


class MinesweeperCmd(Cmd):
    """Handle commands for a game of Minesweeper."""

    def do_exit(self, _):
        """Exit the game."""
        return True

    def do_quit(self, text):
        """Exit the game. (Synonym for exit.)"""
        return self.do_exit(text)

    def do_EOF(self, text):
        """Exit the game. (Synonym for exit.)"""
        return self.do_exit(text)


def main():
    interpreter = MinesweeperCmd()
    interpreter.cmdloop()


if __name__ == '__main__':
    main()
