import json
import sys

from ast2tac import Prog
from lexer import lexer
from parser import parser_yacc


def make_Prog(filename: str) -> Prog:
    with open(filename, 'r') as fp:
        try:
            prog = parser_yacc.parse(fp.read(), lexer=lexer)
        except SyntaxError as serr:
            print(serr)
            exit(1)

    prog.syntax_check(filename) 
    
    return Prog(prog)


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
