from __future__ import print_function, division, unicode_literals, absolute_import

import sys


def main(argv=None):
    print('nothing in particular')
    words = str(raw_input('type something > '))
    print('you typed {}'.format(words))


if __name__ == '__main__':
    main(sys.argv)
