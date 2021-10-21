import argparse
import sys
from ast2tac import Prog
from lexer import lexer
from parser import parser




if __name__ == '__main__':

    ap = argparse.ArgumentParser(
        description="Runs the parser and type-checker alone")
    ap.add_argument('fname', metavar='FILE', type=str, nargs=1,
                    help='The TAC(JSON) file to process')
    opts = ap.parse_args()
    assert(opts.fname[0].endswith(".bx"))
    

    ## parse bx 

    with open(opts.fname[0], 'r') as bx_file:
        try:
            prog = parser.parse(bx_file.read(), lexer=lexer)
        except SyntaxError as serr:
            print(serr)
            exit(1)

    ## type_check
    prog.syntax_check(filename) 



    


    