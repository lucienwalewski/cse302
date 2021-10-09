import json
import sys
from parser import parser_yacc

from ast2tac import Prog
from lexer import lexer
from syntax_checker import check_syntax


def make_Prog(filename: str) -> Prog:
    with open(filename, 'r') as fp:
        try:
            parse_output = parser_yacc.parse(fp.read(), lexer=lexer)
        except SyntaxError as serr:
            print(f'Syntax error:{serr}')
            exit(1)
    
    # if check_syntax(parse_output, filename):
    #     sys.exit(1)

    return Prog(parse_output)


def bx2tac(filename: str) -> list:
    return [{'proc': '@main',
        'body': make_Prog(filename).get_instructions()}]

def bx2tacjson(filename: str) -> list:
    tac = make_Prog(filename)
    tacname = filename[:3] + '.tac.json'
    with open(tacname, 'w') as fp:
        json.dump(tac.js_obj, fp)
    print(f'{filename} -> {tacname}')
    return tac.get_instructions()
