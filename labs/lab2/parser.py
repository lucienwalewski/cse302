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
    p[0] = bx_ast.Program(p.lineno(6), [], p[6])


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
    p[0] = bx_ast.Vardecl(p.lineno(4), bx_ast.Variable(p.lineno(2), p[2]), p[4])


def p_assign(p):
    '''assign : IDENT EQUAL expr SEMICOLON'''
    p[0] = bx_ast.Assign(p.lineno(3), bx_ast.Variable(p.lineno(1), p[1]), p[3])


def p_print(p):
    '''print : PRINT LPAREN expr RPAREN SEMICOLON'''
    p[0] = bx_ast.Print(p.lineno(3), p[3])


def p_expr_ident(p):
    '''expr : IDENT'''
    p[0] = bx_ast.Variable(p.lineno(1), p[1])


def p_expr_number(p):
    '''expr : NUMBER'''
    p[0] = bx_ast.Number(p.lineno(1), p[1])


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
            p[0] = bx_ast.OpApp(p.lineno(2), 'PLUS', (p[1], p[3]))
        elif p[2] == '-':
            p[0] = bx_ast.OpApp(p.lineno(2), 'MINUS', (p[1], p[3]))
        elif p[2] == '/':
            p[0] = bx_ast.OpApp(p.lineno(2), 'DIV', (p[1], p[3]))
        elif p[2] == '*':
            p[0] = bx_ast.OpApp(p.lineno(2), 'TIMES', (p[1], p[3]))
        elif p[2] == '%':
            p[0] = bx_ast.OpApp(p.lineno(2), 'MODULUS', (p[1], p[3]))
        elif p[2] == '|':
            p[0] = bx_ast.OpApp(p.lineno(2), 'BITOR', [p[1], p[3]])
        elif p[2] == '&':
            p[0] = bx_ast.OpApp(p.lineno(2), 'BITAND', [p[1], p[3]])
        elif p[2] == '^':
            p[0] = bx_ast.OpApp(p.lineno(2), 'BITXOR', [p[1], p[3]])
        elif p[2] == '<<':
            p[0] = bx_ast.OpApp(p.lineno(2), 'BITSHL', [p[1], p[3]])
        elif p[2] == '>>':
            p[0] = bx_ast.OpApp(p.lineno(2), 'BITSHR', [p[1], p[3]])
    elif len(p) == 3:
        p[0] = bx_ast.OpApp(p.lineno(2), 'BITCOMPL', [p[2]])


def p_expr_parens(p):
    '''expr : LPAREN expr RPAREN'''
    p[0] = p[2]


def p_expr_uminus(p):
    '''expr : MINUS expr %prec UMINUS'''
    p[0] = bx_ast.OpApp(p.lineno(2), 'UMINUS', [p[2]])


# Error rule for syntax errors
def p_error(p):
    if p is None:
        print(f"Syntax error!")
        raise SyntaxError
    print(f"Syntax error in input at line {p.lineno}")
    raise SyntaxError


parser = yacc.yacc()