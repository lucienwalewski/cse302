import json
from collections import deque

from bx_ast import *

opcode_map = {
    'PLUS': 'add', 'MINUS': 'sub', 'TIMES': 'mul', 'DIV': 'div',
    'MODULUS': 'mod', 'BITAND': 'and', 'BITOR': 'or', 'BITXOR': 'xor',
    'BITSHL': 'shl', 'BITSHR': 'shr', 'BITCOMPL': 'not',
    'UMINUS': 'neg',

    'EQUALITY': 'je', 'DISEQUALITY': 'jne', 'LT': 'jl', 'LEQ': 'jle',
    'GT': 'jg', 'GEQ': 'jge'
}

####################
# Instructions


class Instr:
    # reduce memory pressure by eliding the dynamic dictionary
    __slots__ = ['opcode', 'args', 'result']

    def __init__(self, opcode, args, result):
        self.opcode = opcode
        self.args = args
        self.result = result

    @property
    def js_obj(self):
        return {'opcode': self.opcode,
                'args': self.args,
                'result': self.result}


class Prog():
    def __init__(self, ast_prog: Program, alg = 'tmm'):
        self.localtemps = []
        self.instrs = []
        self.__tempmap = dict()
        self.__last = -1
        self.__last_label = -1
        self._break_stack = deque()
        self._continue_stack = deque()
        for v in ast_prog.lvars:
            self._emit('const', [0], self._lookup(v))
        self.tmm_stmt(ast_prog.block)

    @property
    def js_obj(self):
        '''Return json file for Prog'''
        return [{'proc': '@main',
                 'body': [i.js_obj for i in self.instrs]}]

    def _fresh(self) -> int:
        '''Obtain fresh temporary'''
        self.__last += 1
        t = f'%{self.__last}'
        self.localtemps.append(t)
        return t

    def _fresh_label(self) -> int:
        '''Obtain fresh label'''
        self.__last_label += 1
        t = f'%.L{self.__last_label}'
        return t

    def _lookup(self, var: str) -> int:
        '''Lookup temporary assigned to variable'''
        t = self.__tempmap.get(var)
        if t is None:
            t = self._fresh()
            self.__tempmap[var] = t
        return t

    def _emit(self, opcode, args, result) -> None:
        '''Append instruction to list of instructions'''
        self.instrs.append(Instr(opcode, args, result))

    def tmm_int_expr(self, expr: Expr, target) -> None:
        '''Emit code to evaluate 'expr', 
        storing the result in target'''
        if isinstance(expr, Number):
            self._emit('const', [expr.value], target)
        elif isinstance(expr, Variable):
            src = self._lookup(expr.name)
            self._emit('copy', [src], target)
        elif isinstance(expr, OpApp):
            args = []
            for arg in expr.args:
                arg_target = self._fresh()
                self.tmm_int_expr(arg, arg_target)
                args.append(arg_target)
            self._emit(opcode_map[expr.op], args, target)
        else:
            raise ValueError(
                f'tmm_expr: unknown expr kind {expr.__class__}')

    def tmm_bool_expr(self, bexpr: Expr, Lt, Lf) -> None:
        '''Emit code to evaluate 'bexpr', 
        jumping to 'Lt' if true and 'Lf'
        if false.'''
        if isinstance(bexpr, Bool):
            if bexpr.value == True:
                self._emit('jmp', [Lt], None)
            elif bexpr.value == False:
                self._emit('jmp', [Lf], None)
        elif isinstance(bexpr, OpApp):
            if bexpr.op in {'EQUALITY', 'DISEQUALITY',
                            'LT', 'LEQ', 'GT', 'GEQ'}:
                args = []
                for arg in bexpr.args:
                    arg_target = self._fresh()
                    self.tmm_int_expr(arg, arg_target)
                    args.append(arg_target)
                self._emit('sub', args, args[0])
                self._emit(opcode_map[bexpr.op], [args[0], Lt], None)
                self._emit('jmp', [Lf], None)
            elif bexpr.op == 'BOOLAND':
                Li = self._fresh_label()
                self.tmm_bool_expr(bexpr.args[0], Li, Lf)
                self._emit('label', [Li], None)
                self.tmm_bool_expr(bexpr.args[1], Lt, Lf)
            elif bexpr.op == 'BOOLOR':
                Li = self._fresh_label()
                self.tmm_bool_expr(bexpr.args[0], Lt, Li)
                self._emit('label', [Li], None)
                self.tmm_bool_expr(bexpr.args[1], Lt, Lf)
            elif bexpr.op == 'BOOLNEG':
                self.tmm_bool_expr(bexpr.args[0], Lf, Lt)
        else:
            print(bexpr)
            raise ValueError(
                f'tmm_expr: unknown expr kind: {bexpr.__class__}')

    def tmm_stmt(self, stmt: Stmt) -> None:
        '''Emit code to evaluate a statement'''
        if isinstance(stmt, Assign) or isinstance(stmt, Vardecl):
            target = self._lookup(stmt.var.name)
            self.tmm_int_expr(stmt.expr, target)
        elif isinstance(stmt, Print):
            target = self._fresh()
            self.tmm_int_expr(stmt.expr, target)
            self._emit('print', [target], None)
        elif isinstance(stmt, IfElse):
            Lt, Lf, Lo = [self._fresh_label() for _ in range(3)]
            self.tmm_bool_expr(stmt.condition, Lt, Lf)
            self._emit('label', [Lt], None)
            self.tmm_stmt(stmt.block)
            self._emit('jmp', [Lo], None)
            self._emit('label', [Lf], None)
            self.tmm_stmt(stmt.ifrest)
            self._emit('label', [Lo], None)
        elif isinstance(stmt, Block):
            for stmt in stmt.stmts:
                self.tmm_stmt(stmt)
        elif isinstance(stmt, While):
            Lhead, Lbod, Lend = [self._fresh_label() for _ in range(3)]
            self._break_stack.append(Lend)
            self._continue_stack.append(Lhead)
            self._emit('label', [Lhead], None)
            self.tmm_bool_expr(stmt.condition, Lbod, Lend)
            self._emit('label', [Lbod], None)
            self.tmm_stmt(stmt.block)
            self._emit('jmp', [Lhead], None)
            self._emit('label', [Lend], None)
            self._break_stack.pop()
            self._continue_stack.pop()
        elif isinstance(stmt, Jump):
            if stmt.op == 'break':
                if len(self._break_stack) < 1:
                    raise ValueError(f'Bad break at line {stmt.sloc}')
                self._emit('jmp', [self._break_stack[-1]], None)
            elif stmt.op == 'continue':
                if len(self._continue_stack) < 1:
                    raise ValueError(f'Bad continue at line {stmt.sloc}')
                self._emit('jmp', [self._continue_stack[-1]], None)
        else:
            print(stmt)
            raise ValueError(f'tmm_stmt: unknown stmt kind: {stmt.__class__}')

    def get_instructions(self):
        return self.instrs


def ast_to_tac_json(fname, alg):
    assert fname.endswith('.json')
    with open(fname, 'rb') as fp:
        js_obj = json.load(fp)
        ast_prog = Program.load(js_obj['ast'])
    tac_prog = Prog(ast_prog, alg)
    tacname = fname[:-4] + 'tac.json'
    with open(tacname, 'w') as fp:
        json.dump(tac_prog.js_obj, fp)
    print(f'{fname} -> {tacname}')
    return tacname
