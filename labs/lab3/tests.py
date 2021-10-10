import os

from parser import parser
from bx2tac import bx2tac
from lexer import lexer
from tac2x64 import compile_tac
from bx_ast import reset

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
            res.syntax_check('filename')
        
