import json
import sys
from parser import parser

from ast2tac import Prog
from lexer import lexer
from syntax_checker import check_syntax

if __name__ == '__main__':
    filename = sys.argv[1]
    with open(filename, 'r') as fp:
        try:
            parse_output = parser.parse(fp.read(), lexer=lexer)
        except SyntaxError as serr:
            exit(1)

        if check_syntax(parse_output, filename):
            sys.exit(1)

        tac = Prog(parse_output, 'tmm')

        tacname = filename[:-3] + '.tac.json'
        with open(tacname, 'w') as fp:
            json.dump(tac.js_obj, fp)
        print(f'{filename} -> {tacname}')
