import sys
import json
from lexer import lexer
from parser import parser_yacc
from syntax_checker import check_syntax
from ast2tac import Prog

if __name__ == '__main__':
    filename = sys.argv[1]
    with open(filename, 'r') as fp:
        try:
            parse_output = parser_yacc.parse(fp.read(), lexer=lexer)
        except SyntaxError as serr:
            exit(1)

        if check_syntax(parse_output, filename):
            sys.exit(1)

        tac = Prog(parse_output, 'tmm')

        tacname = filename[:-3] + '.tac.json'
        with open(tacname, 'w') as fp:
            json.dump(tac.js_obj, fp)
        print(f'{filename} -> {tacname}')
