import json
from collections import deque
from os import name

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
    '''Class taking AST in the form of the class Program
    and converts it to TAC'''

    def __init__(self, prog: Program) -> None:
        self.prog = prog
        self.localtemps = []
        # self.__tempmap = dict()
        self.__last = -1
        self.__last_label = -1
        self._break_stack = deque()
        self._continue_stack = deque()
        self.compilation_units = []  # Made into a list at the end
        self.scopes = []
        self.create_scope()
        self.create_compilation_units()

    @property
    def js_obj(self):
        '''Return json file for Prog'''
        compilation_units_js = []
        for unit in self.compilation_units:
            if 'proc' in unit:
                body = unit['body']
                compilation_units_js.append(
                    {'proc': unit['proc'], 'args': unit['args'], 'body': []})
                for instr in body:
                    compilation_units_js[-1]['body'].append(instr.js_obj)
            else:
                compilation_units_js.append(unit)
        return compilation_units_js

    # @property
    # def instructions(self):
    #     return
    #     return [instr.js_obj for instr in self.instrs]

    def create_scope(self) -> None:
        '''Create the initial global scope'''
        global_scope = {}
        for decl in self.prog.decls:
            if isinstance(decl, Vardecl):
                for varinit in decl.varinits:
                    global_scope[varinit.var.name] = f'@{varinit.var.name}'
            if isinstance(decl, Procdecl):
                global_scope[decl.name] = f'@{decl.name}'
        self.scopes = [global_scope]

    def create_compilation_units(self) -> None:
        '''Create a list of compilation units'''
        for decl in self.prog.decls:
            if isinstance(decl, Vardecl):
                for varinit in decl.varinits:
                    if varinit.expr.ty.ty_str == 'bool':
                        compilation_unit = {
                            'var': f'@{varinit.var.name}', 'init': 1 if varinit.expr.value else 0}
                    else:
                        compilation_unit = {
                            'var': f'@{varinit.var.name}', 'init': varinit.expr.value}
                    self.compilation_units.append(compilation_unit)
            elif isinstance(decl, Procdecl):  # Procdecl
                compilation_unit = {'proc': f'@{decl.name}', 'args': self.get_procdecl_args(
                                    decl), 'body': []}
                self.compilation_units.append(compilation_unit)
                self.get_procdecl_tac(decl)

    def get_procdecl_args(self, decl: Procdecl) -> list:
        '''Create a list of params for a given procedure
        declaration'''
        if decl.params is None:
            return []
        return [f'%{arg}' for param in decl.params for arg in param.names]

    def get_procdecl_tac(self, decl: Procdecl) -> list:
        '''Given a procedure declaration, munch the body'''
        new_scope = dict()
        if decl.params is not None:
            for param in decl.params:
                for arg in param.names:
                    new_scope[arg] = f'%{arg}'
        self.scopes.append(new_scope)
        instructions = [self.tmm_stmt(stmt) for stmt in decl.block.stmts]
        self.scopes.pop()
        return instructions

    def _fresh(self) -> int:
        '''Obtain fresh temporary'''
        self.__last += 1
        t = f'%{self.__last}'
        # self.localtemps.append(t)
        return t

    def _fresh_label(self) -> int:
        '''Obtain fresh label'''
        self.__last_label += 1
        t = f'%.L{self.__last_label}'
        return t

    def _lookup(self, var: str) -> int:
        '''Lookup temporary assigned to variable'''
        for scope in reversed(self.scopes):
            if var in scope:
                return scope[var]
        temporary = self._fresh()
        self.scopes[-1][var] = temporary
        return temporary

    def _emit(self, opcode, args, result) -> None:
        '''Append instruction to list of instructions'''
        self.compilation_units[-1]['body'].append(Instr(opcode, args, result))

    def tmm_expr(self, expr: Expr, target: str) -> None:
        '''Emit code to evaluate 'expr', 
        storing the result in target'''
        if expr.ty.ty_str == 'bool':
            ti = self._fresh()
            Lt, Lf = [self._fresh_label() for _ in range(2)]
            self._emit('const', [0], ti)
            self.tmm_bool_expr(expr, Lt, Lf)
            self._emit('label', [Lt], None)
            self._emit('const', [1], ti)
            self._emit('label', [Lf], None)
            self._emit('copy', [ti], target)
        elif isinstance(expr, Number):
            self._emit('const', [expr.value], target)
        elif isinstance(expr, Variable):
            src = self._lookup(expr.name)
            self._emit('copy', [src], target)
        elif isinstance(expr, OpApp):
            self.tmm_opapp(expr, target)
        elif isinstance(expr, Call):
            self.tmm_call(expr, target)
        elif isinstance(expr, Bool):
            self._emit('const', [1 if expr.value else 0], target)
        else:
            raise ValueError(
                f'tmm_expr: unknown expr kind {expr.__class__}')

    def tmm_opapp(self, opapp: OpApp, target: str) -> None:
        '''Munch an opapp'''
        args = []
        for arg in opapp.args:
            arg_target = self._fresh()
            self.tmm_expr(arg, arg_target)
            args.append(arg_target)
        self._emit(opcode_map[opapp.op], args, target)

    def tmm_bool_expr(self, bexpr: Expr, Lt, Lf) -> None:
        '''Emit code to evaluate 'bexpr', 
        jumping to 'Lt' if true and 'Lf'
        if false.'''
        if isinstance(bexpr, Bool):
            if bexpr.value:
                self._emit('jmp', [Lt], None)
            elif bexpr.value == False:
                self._emit('jmp', [Lf], None)
        elif isinstance(bexpr, Variable):
            src = self._lookup(bexpr.name)
            self._emit('jz', [src, Lf], None)
            self._emit('jmp', [Lt], None)
        elif isinstance(bexpr, OpApp):
            if bexpr.op in {'EQUALITY', 'DISEQUALITY',
                            'LT', 'LEQ', 'GT', 'GEQ'}:
                args = []
                for arg in bexpr.args:
                    arg_target = self._fresh()
                    self.tmm_expr(arg, arg_target)
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
        elif isinstance(bexpr, Call):
            target = self._fresh()
            self.tmm_call(bexpr, target)
            self._emit('jz', [target, Lf], None)
            self._emit('jmp', [Lt], None)
        else:
            print(bexpr)
            raise ValueError(
                f'tmm_expr: unknown expr kind: {bexpr.__class__}')

    def tmm_stmt(self, stmt: Stmt) -> None:
        '''Emit code to evaluate a statement'''
        if isinstance(stmt, Assign):
            self.tmm_assign(stmt)
        elif isinstance(stmt, Vardecl):
            self.tmm_vardecl(stmt)
        elif isinstance(stmt, IfElse):
            self.tmm_ifelse(stmt)
        elif isinstance(stmt, Block):
            self.tmm_block(stmt)
        elif isinstance(stmt, While):
            self.tmm_while(stmt)
        elif isinstance(stmt, Jump):
            self.tmm_jump(stmt)
        elif isinstance(stmt, Eval):
            self.tmm_eval(stmt)
        elif isinstance(stmt, Return):
            self.tmm_return(stmt)
        else:
            print(stmt)
            raise ValueError(f'tmm_stmt: unknown stmt kind: {stmt.__class__}')

    def tmm_assign(self, stmt: Assign) -> None:
        '''Munch an assignment'''
        target = self._lookup(stmt.var.name)
        self.tmm_expr(stmt.expr, target)

    def tmm_vardecl(self, vardecl: Vardecl) -> None:
        '''Given a vardecl, munch the varinits'''
        for varinit in vardecl.varinits:
            target = self._fresh()
            self.tmm_expr(varinit.expr, target)
            self.scopes[-1][varinit.var.name] = target

    def tmm_ifelse(self, ifelse: IfElse) -> None:
        '''Munch an ifelse'''
        Lt, Lf, Lo = [self._fresh_label() for _ in range(3)]
        self.tmm_bool_expr(ifelse.condition, Lt, Lf)
        self._emit('label', [Lt], None)
        self.tmm_stmt(ifelse.block)
        self._emit('jmp', [Lo], None)
        # if (isinstance(ifelse.ifrest, Block) and ifelse.ifrest.stmts) or (isinstance(ifelse.ifrest, IfElse) and ifelse.ifrest.block.stmts):
        self._emit('label', [Lf], None)
        self.tmm_stmt(ifelse.ifrest)
        self._emit('label', [Lo], None)

    def tmm_block(self, block: Block) -> None:
        '''Munch a block'''
        self.scopes.append(dict())
        for stmt in block.stmts:
            self.tmm_stmt(stmt)
        self.scopes.pop()

    def tmm_while(self, while_stmt: While) -> None:
        '''Munch a while block'''
        Lhead, Lbod, Lend = [self._fresh_label() for _ in range(3)]
        self._break_stack.append(Lend)
        self._continue_stack.append(Lhead)
        self._emit('label', [Lhead], None)
        self.tmm_bool_expr(while_stmt.condition, Lbod, Lend)
        self._emit('label', [Lbod], None)
        self.tmm_stmt(while_stmt.block)
        self._emit('jmp', [Lhead], None)
        self._emit('label', [Lend], None)
        self._break_stack.pop()
        self._continue_stack.pop()

    def tmm_jump(self, jmp: Jump) -> None:
        '''Munch a jump'''
        if jmp.op == 'break':
            if len(self._break_stack) < 1:
                raise ValueError(f'Bad break at line {jmp.sloc}')
            self._emit('jmp', [self._break_stack[-1]], None)
        elif jmp.op == 'continue':
            if len(self._continue_stack) < 1:
                raise ValueError(f'Bad continue at line {jmp.sloc}')
            self._emit('jmp', [self._continue_stack[-1]], None)

    def tmm_eval(self, eval: Eval) -> None:
        '''Munch an evaluation. This is like munching any
        expression except without storing the result in a
        temporary'''
        self.tmm_expr(eval.expr, target=None)

    def tmm_return(self, ret: Return) -> None:
        '''Munch a return'''
        if ret.expr:
            target = self._fresh()
            self.tmm_expr(ret.expr, target)
            self._emit('ret', [target], None)
        else:
            self._emit('ret', [], None)

    def tmm_call(self, call: Call, target: str = None) -> None:
        '''Munch a procedure call. If the target is None
        then it is a subroutine and we do not store the result.'''
        targets = []
        for position, expr in enumerate(call.exprs):
            new_target = self._fresh()
            self.tmm_expr(expr, new_target)
            targets.append((position, new_target))
            # self._emit('param', [position + 1, new_target], None)
        for position, targ in targets:
            self._emit('param', [position + 1, targ], None)
        self._emit('call', [f'@{call.func}', position + 1], target)


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
