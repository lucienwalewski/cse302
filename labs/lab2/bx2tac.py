import ply.lex as lex
import re

reserved = {'print': 'PRINT', 'while': 'WHILE'}

# The ‘tokens' tuple must be present and list all the valid tokens
tokens = (
    'PLUS', 'MINUS', 'DIV', 'MODULUS', 'SEMICOLON', 'LPAREN', 'RPAREN', 'IDENT',
    'NUMBER', 'BITOR', 'BITAND', 'BITXOR', 'BITSHL', 'BITSHR', 'BITCOMPL', 'UMINUS'
) + tuple(reserved.values())

# Regexp strings definitions beginning with ‘t_' define simple tokens
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_PLUS = r'\+'
t_MINUS = '-'
t_SEMICOLON = ';'
t_DIV = '/'
t_MODULUS = '%'
t_BITOR = r'\|'
t_BITAND = '&'
t_BITXOR = r'\^'
t_BITSHL = '<<'
t_BITSHR = '>>'
t_BITCOMPL = '~'
t_UMINUS = '-'


# Functions beginning with ‘t_' define complex token processing code.
# The docstrings of the functions contain the regexp that is matched for the token


def t_IDENT(t):
    r'[A-Za-z_][A-Za-z0-9_]*'  # docstring contains the regexp
    t.type = reserved.get(t.value, 'IDENT')
    return t


def t_NUMBER(t):
    r'[1-9][0-9]*'
    t.value = int(t.value)
    return t

# error handling with t_error()


def t_error(t):
    print(f'Illegal character {t.value[0]} on line {t.lexer.lineno}')
    t.lexer.skip(1)  # skip one character


# characters to ignore
# t_ignore = ' \t\f\v'
t_ignore = ' \t\f\v\\'


def t_newline(t):
    r'\n'
    t.lexer.lineno += 1
    # no return, signifying ignore


lexer = lex.lex()
# This will use Python introspection (reflection) to find out all the
# ‘tokens' and ‘t_stuff' in this module and create a suitable lexer from it
