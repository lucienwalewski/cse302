import argparse
import sys
from bx_ast import Program
from lexer import lexer
from parser import parser


def bxfront(filename: str) -> Program:
    '''Parse and type check bx and return a program'''
    with open(filename, 'r') as bx_file:
        try:
            prog = parser.parse(bx_file.read(), lexer=lexer)
            return prog
        except SyntaxError as serr:
            print(serr)
            exit(1)


if __name__ == '__main__':
    ap = argparse.ArgumentParser(
        description="Runs the parser and type-checker alone")
    ap.add_argument('fname', metavar='FILE', type=str, nargs=1,
                    help='The TAC(JSON) file to process')
    opts = ap.parse_args()
    assert(opts.fname[0].endswith(".bx"))
    filename = opts.fname[0]
    bxfront(filename)
