"""
Lexer that takes input file and prints all the tokens
sequentially.

Usage:
    python3 lexer.py <filename>
    
Returns:
    Null"""

from ply import lex

reserved = {'print': 'PRINT',
            'main': 'MAIN',
            'def': 'DEF',
            'var': 'VAR',
            'int': 'INT',
            'if': 'IF',
            'else': 'ELSE',
            'while': 'WHILE',
            'break': 'BREAK',
            'continue': 'CONTINUE',
            'true': 'TRUE',
            'false': 'FALSE'}

# The ‘tokens' tuple must be present and list all the valid tokens
tokens = (
    'IDENT',
    'NUMBER',

    'PLUS',
    'MINUS',
    'DIV',
    'TIMES',
    'MODULUS',
    'BITOR',
    'BITAND',
    'BITXOR',
    'BITSHL',
    'BITSHR',
    'BITCOMPL',
    'EQUAL',

    'SEMICOLON',
    'COLON',
    'LPAREN',
    'RPAREN',
    'LBRACE',
    'RBRACE',

    'LT',
    'LEQ',
    'GT',
    'GEQ',
    'EQUALITY',
    'DISEQUALITY',
    'BOOLAND',
    'BOOLOR',
    'BOOLNEG'
) + tuple(reserved.values())

# Regexp strings definitions beginning with ‘t_' define simple tokens
t_PLUS = r'\+'
t_MINUS = '-'
t_DIV = '/'
t_TIMES = r'\*'
t_MODULUS = '%'
t_BITOR = r'\|'
t_BITAND = '&'
t_BITXOR = r'\^'
t_BITSHL = '<<'
t_BITSHR = '>>'
t_BITCOMPL = '~'

t_SEMICOLON = ';'
t_COLON = ':'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = '{'
t_RBRACE = '}'

t_LT = '<'
t_LEQ = '<='
t_GT = '>'
t_GEQ = '>='
t_EQUALITY = '=='
t_DISEQUALITY = '!='
t_BOOLAND = '&&'
t_BOOLOR = r'\|\|'
t_BOOLNEG = '!'

t_EQUAL = '='

# Functions beginning with ‘t_' define complex token processing code.
# The docstrings of the functions contain the regexp that is matched for the token


def t_IDENT(t):
    r'[A-Za-z_][A-Za-z0-9_]*'  # docstring contains the regexp
    t.type = reserved.get(t.value, 'IDENT')
    return t


def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t


def t_COMMENT(t):
    r'//.*\n?'
    t.lexer.lineno += t.value.count("\n")


def t_error(t):
    print(f'Illegal character "{t.value[0]}" on line {t.lexer.lineno}')
    t.lexer.skip(1)  # skip one character


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


# characters to ignore
t_ignore = ' \t\f\v'


# This will use Python introspection (reflection) to find out all the
# ‘tokens' and ‘t_stuff' in this module and create a suitable lexer from it

lexer = lex.lex()
