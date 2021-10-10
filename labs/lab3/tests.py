import os
import subprocess

from parser import parser
from ast2tac import Prog
from bx2tac import bx2tac
from bx_ast import reset
from lexer import lexer
from tac2x64 import compile_tac

good_path = 'examples/'
good_files = [os.path.join(dp, f) for dp, _, fn in os.walk(good_path) for f in fn]

bad_path = 'regression/'
bad_files = [os.path.join(dp, f) for dp, _, fn in os.walk(good_path) for f in fn]

def test_lex():
    for file in good_files:
        with open(file, 'r') as fp:
            lexer.input(fp.read())
            for tok in lexer:
                pass

def test_parse():
    for file in good_files:
        with open(file, 'r') as fp:
            reset()
            res = parser.parse(fp.read())
            res.syntax_check(file)

def test_ast2tac():
    for file in good_files:
        with open(file, 'r') as fp:
            reset()
            res = parser.parse(fp.read())
            res.syntax_check(file)
            prog = Prog(res)
            prog.get_instructions()

def test_asm():
    for file in good_files:
        with open(file, 'r') as fp:
            reset()
            res = parser.parse(fp.read())
            res.syntax_check(file)
            prog = Prog(res)

            tac = [{'proc': '@main',
                    'body': prog.get_instructions()}]

            compile_tac(tac, file)
            # cmd = ['gcc', '-o', file[:-3], 'bx_runtime.c', file[:-3] + '.s']
            # p = subprocess.Popen(cmd)
            # p.wait()
            # cmd = ['rm', file[:-3] + '.s']
            # p = subprocess.Popen(cmd)
            # p.wait()
            # cmd = ['rm', file[:-3]]
            # p = subprocess.Popen(cmd)
            # p.wait()
        
# if __name__ == '__main__':
#     test_parse()
