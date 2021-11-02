import argparse
import sys
from ast2tac import Prog
from lexer import lexer
from parser import parser



def bxfront(filename: str) -> Prog:
    '''Parse and type check bx and return a prog'''
    with open(filename, 'r') as bx_file:
        try:
            prog = parser.parse(bx_file.read(), lexer=lexer)
            return prog
        except SyntaxError as serr:
            print(serr)
            exit(1)
        # else:
        #     print('Successfully lexed and parsed and type checked')

    
if __name__ == '__main__':
    ap = argparse.ArgumentParser(
        description="Runs the parser and type-checker alone")
    ap.add_argument('fname', metavar='FILE', type=str, nargs=1,
                    help='The TAC(JSON) file to process')
    opts = ap.parse_args()
    assert(opts.fname[0].endswith(".bx"))
    filename = opts.fname[0]
    bxfront(filename)

