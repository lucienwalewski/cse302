'''
Syntax checker that checks syntax on output of parser
that ensures that syntactic constraints are respected

Usage:

Returns:
'''

from bx_ast import *
import sys

declarations = []
declarations_line = {}


def check_variable(expr: Variable, filename: str):
    if expr.name not in declarations:
        print(f'{filename}:line {expr.sloc}:Error:Undeclared variable "{expr.name}"')
        return True


def check_number(expr: Number, filename: str):
    if expr.value < 0 or (expr.value >> 63):
        print(
            f'{filename}:line {expr.sloc}:Error:Number "{expr.value}" out of range [0, 2<<63)')
        return True


def check_opapp(expr: OpApp, filename: str):
    for arg in expr.args:
        if check_expr(arg, filename):
            return True

    return False


def check_expr(expr: Expr, filename: str):
    if isinstance(expr, Variable):
        return check_variable(expr, filename)
    elif isinstance(expr, Number):
        return check_number(expr, filename)
    elif isinstance(expr, OpApp):
        return check_opapp(expr, filename)


def check_vardecl(instruction: Vardecl, filename):
    global declarations
    if check_expr(instruction.rhs, filename):
        return True

    if instruction.lhs in declarations:
        print(f'{filename}:line {instruction.sloc}:Error:Duplicate declaration of variable "{instruction.lhs}"')
        print(
            f'{filename}:line {declarations_line[instruction.lhs]}:Info:Earlier declaration of "{instruction.lhs}"')
        return True

    declarations.append(instruction.lhs.name)
    declarations_line[instruction.lhs.name] = instruction.sloc


def check_assign(instruction: Assign, filename):
    if check_variable(instruction.rhs, filename) or check_expr(instruction.lhs, filename):
        return True


def check_print(instruction: Print, filename):
    if check_expr(instruction.arg, filename):
        return True


def check_syntax(parse_output, filename):
    '''Checks syntax of parse output and raises error'''
    if not isinstance(parse_output, Program):
        print(f'{filename}:Error:Incorrect main function')
        return True
    for instruction in parse_output.stmts:
        if isinstance(instruction, Vardecl):
            if check_vardecl(instruction, filename):
                return True
        elif isinstance(instruction, Assign):
            if check_assign(instruction, filename):
                return True
        elif isinstance(instruction, Print):
            if check_print(instruction, filename):
                return True

    return False
