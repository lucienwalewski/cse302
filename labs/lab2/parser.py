"""
Parser that takes file produced by lexer and produces
an ast.

Usage:

Returns:
"""

from py.ply import yacc
from lexer import tokens, lexer
import bx_ast

precedence = (
    ('left', 'BITOR'),
    ('left', 'BITXOR'),
    ('left', 'BITAND'),
    ('left', 'BITSHL', 'BITSHR'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIV', 'MODULUS'),
    ('right', 'UMINUS'),
    ('right', 'BITCOMPL')
)


def p_program(p):
    '''program : DEF MAIN LPAREN RPAREN LBRACE stmts_star RBRACE'''
    p[0] = bx_ast.Program([], [], p[6])


def p_statements_star(p):
    '''stmts_star : 
                  | stmts_star stmt'''
    if len(p) == 1:
        p[0] = []
    else:
        p[0] = p[1]
        p[0].append(p[2])


def p_statement(p):
    '''stmt : vardecl 
            | assign
            | print'''
    p[0] = p[1]


def p_vardecl(p):
    '''vardecl : VAR IDENT EQUAL expr COLON INT SEMICOLON'''
    p[0] = bx_ast.Assign([0] * 6, p[2], p[4])


def p_assign(p):
    '''assign : IDENT EQUAL expr SEMICOLON'''
    p[0] = bx_ast.Assign([0]*6, p[1], p[3])


def p_print(p):
    '''print : PRINT LPAREN expr RPAREN SEMICOLON'''
    p[0] = bx_ast.Print([0] * 6, p[3])


def p_expr_ident(p):
    '''expr : IDENT'''
    p[0] = bx_ast.Variable([0]*6, p[1])


def p_expr_number(p):
    '''expr : NUMBER'''
    p[0] = bx_ast.Number([0] * 6, p[1])


def p_operators(p):
    '''expr : expr PLUS expr
            | expr MINUS expr
            | expr DIV expr
            | expr TIMES expr
            | expr MODULUS expr
            | expr BITOR expr
            | expr BITAND expr
            | expr BITXOR expr
            | expr BITSHL expr
            | expr BITSHR expr
            | BITCOMPL expr'''
    if len(p) == 4:
        if p[2] == '+':
            p[0] = bx_ast.OpApp([0], 'PLUS', (p[1], p[3]))
        elif p[2] == '-':
            p[0] = bx_ast.OpApp([0] * 6, 'MINUS', (p[1], p[3]))
        elif p[2] == '/':
            p[0] = bx_ast.OpApp([0] * 6, 'DIV', (p[1], p[3]))
        elif p[2] == '*':
            p[0] = bx_ast.OpApp([0] * 6, 'TIMES', (p[1], p[3]))
        elif p[2] == '%':
            p[0] = bx_ast.OpApp([0] * 6, 'MODULUS', (p[1], p[3]))
        elif p[2] == '|':
            p[0] = bx_ast.OpApp([0] * 6, 'BITOR', [p[1], p[3]])
        elif p[2] == '&':
            p[0] = bx_ast.OpApp([0] * 6, 'BITAND', [p[1], p[3]])
        elif p[2] == '^':
            p[0] = bx_ast.OpApp([0] * 6, 'BITXOR', [p[1], p[3]])
        elif p[2] == '<<':
            p[0] = bx_ast.OpApp([0] * 6, 'BITSHL', [p[1], p[3]])
        elif p[2] == '>>':
            p[0] = bx_ast.OpApp([0] * 6, 'BITSHR', [p[1], p[3]])
    elif len(p) == 3:
        p[0] = bx_ast.OpApp([], 'BITCOMPL', [p[2]])


def p_expr_parens(p):
    '''expr : LPAREN expr RPAREN
            | LBRACE expr RBRACE'''
    p[0] = p[2]


def p_expr_uminus(p):
    '''expr : MINUS expr %prec UMINUS'''
    p[0] = bx_ast.OpApp([], 'UMINUS', [p[2]])


# Error rule for syntax errors
def p_error(p):
    print("Syntax error in input!")


parser_yacc = yacc.yacc()

# while True:
#     try:
#         s = input('calc > ')
#     except EOFError:
#         break
#     if not s:
#         continue
#     result = parser.parse(s, lexer=lexer)
#     print(result)
