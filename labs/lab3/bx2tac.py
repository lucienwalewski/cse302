import json
import sys

from ast2tac import Prog
from lexer import lexer
from syntax_checker import check_syntax
from parser import parser_yacc


def make_Prog(filename: str) -> Prog:
    with open(filename, 'r') as fp:
        try:
            parse_output = parser_yacc.parse(fp.read(), lexer=lexer)
        except SyntaxError as serr:
            print(serr)
            exit(1)
    
    # if check_syntax(parse_output, filename):
    #     sys.exit(1)

    return Prog(parse_output)


def bx2tac(filename: str) -> list:
    return [{'proc': '@main',
        'body': make_Prog(filename).get_instructions()}]

def bx2tacjson(filename: str) -> list:
    bod = [instr.js_obj for instr in make_Prog(filename).get_instructions()]
    tac = [{'proc': '@main',
        'body': bod}]
    print(tac)
    tacname = filename[:-3] + '.tac.json'
    with open(tacname, 'w') as fp:
        json.dump(tac, fp)
    print(f'{filename} -> {tacname}')
    return tac
