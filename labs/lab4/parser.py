"""
Parser that takes file produced by lexer and produces
an ast.

Usage: Library

Returns:
"""

from bx_ast import *
from lexer import lexer, tokens
from ply import yacc

precedence = (
    ('left', 'BOOLOR'),
    ('left', 'BOOLAND'),
    ('left', 'BITOR'),
    ('left', 'BITXOR'),
    ('left', 'BITAND'),
    ('nonassoc', 'EQUALITY', 'DISEQUALITY'),
    ('nonassoc', 'LT', 'LEQ', 'GT', 'GEQ'),
    ('left', 'BITSHL', 'BITSHR'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIV', 'MODULUS'),
    ('right', 'UMINUS', 'BOOLNEG'),
    ('right', 'BITCOMPL')
)


def p_program(p):
    '''program : decl_star'''
    # p[0] = Program(p.lineno(5), [], p[5])
    p[0] = Program(p.lineno(1), [], p[1])


def p_decl_star(p):
    '''decl_star : 
                  | decl_star decl'''
    if len(p) == 1:
        p[0] = []
    else:
        p[0] = p[1]
        p[0].append(p[2])


def p_decl(p):
    '''stmt : vardecl
            | procdecl'''
    p[0] = p[1]

def p_ty(p):
    '''ty : INT
          | BOOL'''
    p[0] = p[1]

def p_procdecl(p):
    '''procdecl : DEF IDENT LPAREN params RPAREN return_type block'''
    pass

def p_params(p):
    '''params : 
              | param params_star'''
    pass

def p_params_star(p):
    '''params_star : 
                   | params_star COMMA param'''
    pass

def p_return_type(p):
    '''return_type : 
                   | COLON ty'''
    pass

def p_param(p):
    '''IDENT ident_star COLON ty'''
    pass

def p_ident_star(p):
    '''ident_star : 
                  | ident_star COMMA IDENT'''
    pass


def p_stmt(p):
    '''stmt : vardecl
            | block
            | assign
            | eval
            | ifelse
            | while
            | jump
            | return'''
    p[0] = p[1]

def p_vardecl(p):
    '''vardecl : VAR varinits COLON ty SEMICOLON'''
    # p[0] = Vardecl(p.lineno(3), Variable(p.lineno(2), p[2], 'int'), p[4])
    pass

def p_varinits(p):
    '''varinits : IDENT EQUAL expr varinits_star'''
    pass
    
def p_varinits_star(p):
    '''varinits_star : 
                     | varinits_star COMMA IDENT EQUAL expr'''
    pass

def p_assign(p):
    '''assign : IDENT EQUAL expr SEMICOLON'''
    # p[0] = Assign(p.lineno(1), Variable(p.lineno(1), p[1], 'int'), p[3])
    pass

def p_eval(p):
    '''eval : expr SEMICOLON'''
    pass

def p_ifelse(p):
    '''ifelse : IF LPAREN expr RPAREN block ifrest'''
    # p[0] = IfElse(p.lineno(1), p[3], p[5], p[6])
    pass

def p_ifrest(p):
    '''ifrest : 
              | ELSE ifelse
              | ELSE block'''
    if len(p) == 1:
        p[0] = Block(p.lineno(0), [])
    else:
        p[0] = p[2]


def p_while(p):
    '''while : WHILE LPAREN expr RPAREN block'''
    p[0] = While(p.lineno(1), p[3], p[5])


def p_jump(p):
    '''jump : BREAK SEMICOLON
            | CONTINUE SEMICOLON'''
    p[0] = Jump(p.lineno(1), p[1])

def p_return(p):
    '''return : RETURN SEMICOLON
              | RETURN expr SEMICOLON'''
    pass


def p_block(p):
    '''block : LBRACE stmts_star RBRACE'''
    p[0] = Block(p.lineno(2), p[2])

def p_stmts_star(p):
    '''stmts_star : 
                  | stmts_star stmt'''
    if len(p) == 1:
        p[0] = []
    else:
        p[0] = p[1]
        p[0].append(p[2])

def p_expr_ident(p):
    '''expr : IDENT'''
    p[0] = Variable(p.lineno(1), p[1], 'int')


def p_expr_number(p):
    '''expr : NUMBER'''
    p[0] = Number(p.lineno(1), p[1])


def p_expr_true(p):
    '''expr : TRUE'''
    p[0] = Bool(p.lineno(1), True)


def p_expr_false(p):
    '''expr : FALSE'''
    p[0] = Bool(p.lineno(1), False)


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
            | expr BOOLAND expr
            | expr BOOLOR expr
            | expr EQUALITY expr
            | expr DISEQUALITY expr
            | expr GT expr
            | expr GEQ expr
            | expr LT expr
            | expr LEQ expr
            | BITCOMPL expr
            | BOOLNEG expr'''
    if len(p) == 4:
        if p[2] == '+':
            p[0] = OpApp(p.lineno(2), 'PLUS', (p[1], p[3]))
        elif p[2] == '-':
            p[0] = OpApp(p.lineno(2), 'MINUS', (p[1], p[3]))
        elif p[2] == '/':
            p[0] = OpApp(p.lineno(2), 'DIV', (p[1], p[3]))
        elif p[2] == '*':
            p[0] = OpApp(p.lineno(2), 'TIMES', (p[1], p[3]))
        elif p[2] == '%':
            p[0] = OpApp(p.lineno(2), 'MODULUS', (p[1], p[3]))
        elif p[2] == '|':
            p[0] = OpApp(p.lineno(2), 'BITOR', [p[1], p[3]])
        elif p[2] == '&':
            p[0] = OpApp(p.lineno(2), 'BITAND', [p[1], p[3]])
        elif p[2] == '^':
            p[0] = OpApp(p.lineno(2), 'BITXOR', [p[1], p[3]])
        elif p[2] == '<<':
            p[0] = OpApp(p.lineno(2), 'BITSHL', [p[1], p[3]])
        elif p[2] == '>>':
            p[0] = OpApp(p.lineno(2), 'BITSHR', [p[1], p[3]])
        elif p[2] == '&&':
            p[0] = OpApp(p.lineno(2), 'BOOLAND', [p[1], p[3]])
        elif p[2] == '||':
            p[0] = OpApp(p.lineno(2), 'BOOLOR', [p[1], p[3]])
        elif p[2] == '==':
            p[0] = OpApp(p.lineno(2), 'EQUALITY', [p[1], p[3]])
        elif p[2] == '!=':
            p[0] = OpApp(p.lineno(2), 'DISEQUALITY', [p[1], p[3]])
        elif p[2] == '<':
            p[0] = OpApp(p.lineno(2), 'LT', [p[1], p[3]])
        elif p[2] == '<=':
            p[0] = OpApp(p.lineno(2), 'LEQ', [p[1], p[3]])
        elif p[2] == '>':
            p[0] = OpApp(p.lineno(2), 'GT', [p[1], p[3]])
        elif p[2] == '>=':
            p[0] = OpApp(p.lineno(2), 'GEQ', [p[1], p[3]])
    elif len(p) == 3:
        if p[1] == '~':
            p[0] = OpApp(p.lineno(2), 'BITCOMPL', [p[2]])
        elif p[1] == '!':
            p[0] = OpApp(p.lineno(2), 'BOOLNEG', [p[2]])


def p_expr_parens(p):
    '''expr : LPAREN expr RPAREN'''
    p[0] = p[2]


def p_expr_uminus(p):
    '''expr : MINUS expr %prec UMINUS'''
    p[0] = OpApp(p.lineno(2), 'UMINUS', [p[2]])

# Error rule for syntax errors
def p_error(p):
    if p is None:
        raise SyntaxError('Syntax error')

    raise SyntaxError(f'Syntax error at line {p.lineno}')


parser = yacc.yacc()
