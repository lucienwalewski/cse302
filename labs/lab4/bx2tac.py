import json
import sys
import argparse

from ast2tac import Prog
from lexer import lexer
from parser import parser


def make_Prog(filename: str) -> Prog:
    with open(filename, 'r') as fp:
        try:
            prog = parser.parse(fp.read(), lexer=lexer)
        except SyntaxError as serr:
            print(serr)
            exit(1)

    return Prog(prog)


def bx2tac(filename: str) -> list:
    return make_Prog(filename).js_obj


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


if __name__ == '__main__':
    ap = argparse.ArgumentParser(
        description="Runs the parser and type-checker alone")
    ap.add_argument('fname', metavar='FILE', type=str, nargs=1,
                    help='The TAC(JSON) file to process')
    opts = ap.parse_args()
    assert(opts.fname[0].endswith(".bx"))
    filename = opts.fname[0]
    tac = bx2tac(filename)
    with open('output_tac.tac.json', 'w') as fp:
        json.dump(tac, fp)
