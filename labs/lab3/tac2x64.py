import sys
from lab2 import bx2tac

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Single argument must be tac filename')
        exit(1)
    filename = sys.argv[1]