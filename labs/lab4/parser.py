"""
Parser that takes file produced by lexer and produces
an ast.

Usage: 

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
    ('right', 'BOOLNEG'),
    ('right', 'BITCOMPL')
)


def p_program(p):
    '''program : decl_star'''
    p[0] = Program(p.lineno(1), p[1])


def p_decl_star(p):
    '''decl_star : 
                 | decl_star decl'''
    if len(p) == 1:
        p[0] = []
    else:
        p[0] = p[1]
        p[0].append(p[2])


def p_decl(p):
    '''decl : vardecl
            | procdecl'''
    p[0] = p[1]


def p_ty(p):
    '''ty : INT
          | BOOL'''
    p[0] = Ty(p.lineno(1), p[1])


def p_procdecl(p):
    '''procdecl : DEF IDENT LPAREN params RPAREN return_type block'''
    p[0] = Procdecl(p.lineno(1), p[2], p[4], p[6], p[7])


def p_params(p):
    '''params : 
              | param params_star'''
    if len(p) == 1:
        p[0] = None
    else:
        p[0] = [p[1]] + p[2]


def p_params_star(p):
    '''params_star : 
                   | params_star COMMA param'''
    if len(p) == 1:
        p[0] = []
    else:
        p[0] = p[1]
        p[0].append(p[3])


def p_return_type(p):
    '''return_type : 
                   | COLON ty'''
    if len(p) == 1:
        p[0] = Ty(p.lineno(0), 'void')
    else:
        p[0] = p[2]


def p_param(p):
    '''param : IDENT ident_star COLON ty'''
    p[0] = Param(p.lineno(1), [p[1]] + p[2], p[4])


def p_ident_star(p):
    '''ident_star : 
                  | ident_star COMMA IDENT'''
    if len(p) == 1:
        p[0] = []
    else:
        p[0] = p[1]
        p[0].append(p[3])


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
    p[0] = Vardecl(p.lineno(1), p[2], p[4])


def p_varinits(p):
    '''varinits : IDENT EQUAL expr varinits_star'''
    p[0] = [Varinit(p.lineno(1), Variable(p.lineno(1), p[1]), p[3])] + p[4]


def p_varinits_star(p):
    '''varinits_star : 
                     | varinits_star COMMA IDENT EQUAL expr'''
    if len(p) == 1:
        p[0] = []
    else:
        p[0] = p[1] + [Varinit(p.lineno(1), Variable(p.lineno(3), p[3]), p[5])]


def p_assign(p):
    '''assign : IDENT EQUAL expr SEMICOLON'''
    p[0] = Assign(p.lineno(1), Variable(p.lineno(1), p[1], 'int'), p[3])


def p_eval(p):
    '''eval : expr SEMICOLON'''
    p[0] = Eval(p.lineno(1), p[1])


def p_ifelse(p):
    '''ifelse : IF LPAREN expr RPAREN block ifrest'''
    p[0] = IfElse(p.lineno(1), p[3], p[5], p[6])


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
    if len(p) == 4:
        p[0] = Return(p.lineno(1), p[2])
    else:
        p[0] = Return(p.lineno(1), None)


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
            | BOOLNEG expr
            | MINUS expr'''
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
        elif p[1] == '-':
            p[0] = OpApp(p.lineno(2), 'MINUS', [p[2]])


def p_expr_parens(p):
    '''expr : LPAREN expr RPAREN'''
    p[0] = p[2]


def p_expr_procedure_calls(p):
    '''expr : IDENT LPAREN exprs RPAREN'''
    p[0] = Call(p.lineno(1), p[1], p[3])


def p_exprs(p):
    '''exprs :
             | expr exprs_star'''
    if len(p) == 1:
        p[0] = []
    else:
        p[0] = [p[1]] + p[2]


def p_exprs_star(p):
    '''exprs_star : 
                  | exprs_star COMMA expr'''
    if len(p) == 1:
        p[0] = []
    else:
        p[0] = p[1]
        p[1].append(p[2])


# Error rule for syntax errors


def p_error(p):
    if p is None:
        raise SyntaxError('Syntax error')

    raise SyntaxError(f'Syntax error at line {p.lineno}')


parser = yacc.yacc()
