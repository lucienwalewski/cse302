"""
Author: Lucien Walewski
Class: CSE302

Use case: 'python3 ast2tac.py <astfilename>

Remarks:
    Retrospectivally would have been better to use class
    hierarchies as would make for more readable, cleaner and 
    scalable code.
"""

import json
import sys
from os import stat

TEMPORARIES = -1  # Global counter on temporaries

BINARY_MAPPINGS = {'PLUS': 'add', 'MINUS': 'sub', 'TIMES': 'mul', 'DIV': 'div', 'MODULUS': 'mod',
                   'BITAND': 'and', 'BITOR': 'or', 'BITXOR': 'xor', 'BITSHL': 'shl', 'BITSHR': 'shr'}
UNARY_MAPPINGS = {'UMINUS': 'neg', 'BITCOMPL': 'not'}


def generate_code(expr, write, mappings):
    """Returns a list of instructions, equivalent to 'code(e, x) from
    lecture slides"""
    global TEMPORARIES, BINARY_MAPPINGS, UNARY_MAPPINGS
    expr = expr[0]  # Ignore location component
    if expr[0] == '<number>':
        instruction = [{'opcode': 'const', 'args': [
            expr[1]], 'result': f'%{write}'}]
        return instruction, mappings

    elif expr[0] == '<var>':
        instruction = [{'opcode': 'copy', 'args': [
            f'%{mappings[expr[1]]}'], 'result': f'%{write}'}]
        return instruction, mappings

    elif expr[0] == '<unop>':
        op, arg = expr[1][0][0], expr[2]
        new_temp = get_new_temporary()
        instructions, mappings = generate_code(arg, new_temp, mappings)
        TEMPORARIES -= 1
        instructions += [{'opcode': UNARY_MAPPINGS[op],
                          'args': [f'%{new_temp}'], 'result': f'%{write}'}]
        return instructions, mappings

    elif expr[0] == '<binop>':
        arg1, op, arg2 = expr[1], expr[2][0][0], expr[3]
        new_temp1 = get_new_temporary()
        instructions1, mappings = generate_code(arg1, new_temp1, mappings)
        new_temp2 = get_new_temporary()
        instructions2, mappings = generate_code(arg2, new_temp2, mappings)
        TEMPORARIES -= 2
        instructions = instructions1 + instructions2 + \
            [{'opcode': BINARY_MAPPINGS[op], 'args': [
                f'%{new_temp1}', f'%{new_temp2}'], 'result': f'%{write}'}]
        return instructions, mappings


def handle_statement(statement, mappings):
    """Given a statement and the current mappings, determine
    the type of the statement and generate the appropriate instructions
    as a list while also updating the mappings"""
    global TEMPORARIES
    if statement[0][0] == '<vardecl>':
        write = statement[0][1][0]
        number = statement[0][2][0][1]  # Always 0
        new_temporary = get_new_temporary()
        mappings[write] = new_temporary
        instruction = [{'opcode': 'const', 'args': [
            number], 'result': f'%{new_temporary}'}]
        return instruction, mappings
    elif statement[0][0] == '<assign>':
        write = statement[0][1][0][1]
        expr = statement[0][-1]
        temporary = mappings[write]
        instruction, mappings = generate_code(expr, temporary, mappings)
        return instruction, mappings
    elif statement[0][0] == '<eval>':
        expr = statement[0][1][0][2][0]
        new_temporary = get_new_temporary()
        instruction, mappings = generate_code(expr, new_temporary, mappings)
        TEMPORARIES -= 1
        instruction = instruction + \
            [{'opcode': 'print', 'args': [f'%{new_temporary}'], 'result': None}]
        return instruction, mappings


def top_down_maximal_munch(body):
    res = [{'proc': '@main', 'body': []}]
    mappings, instructions = {}, []
    for statement in body:  # Generate instructions for each line in the body
        # Get new intructions and updated mappings
        new_instructions, mappings = handle_statement(statement, mappings)
        instructions += new_instructions
    return instructions


def get_new_temporary():
    global TEMPORARIES
    TEMPORARIES += 1
    return TEMPORARIES


def main():
    if len(sys.argv) != 2:
        print("Must only provide ast json file name as argument")
        return
    ast_file = sys.argv[1]
    if not ast_file.endswith('.json'):
        print("File must be json file")
        return
    with open(ast_file, 'r') as fp:
        js_obj = json.load(fp)
        # Directly fetch body of procedure
        body = js_obj['ast'][0][0][0][-1][0][1]
        instructions = top_down_maximal_munch(body)
    out = [{'proc': '@main', 'body': instructions}]
    with open(ast_file[:-5] + '.tac.json', 'w') as outfile:
        json.dump(out, outfile)


if __name__ == "__main__":
    main()
