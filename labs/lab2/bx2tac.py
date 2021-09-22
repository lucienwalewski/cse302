import sys
from lexer import lexer
from parser import parser_yacc

if __name__ == '__main__':
    file = sys.argv[1]
    with open(file, 'r') as fp:
        res = parser_yacc.parse(fp.read(), lexer=lexer)
        print(res)
