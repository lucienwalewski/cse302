#!/usr/bin/env python3

from typing import Union, List

"""
A class hierarchy for the AST of the BX language.
"""

####################
# Nodes


from typing import Type


class Node:
    """Superclass of all AST nodes"""
    vardecls = {}

    def __init__(self, sloc):
        """
        sloc -- source location (list of 6 numbers; see handout for meaning)
        """
        self.sloc = sloc


class Stmt(Node):
    """Superclass of all statements"""

    def __init__(self, sloc):
        super().__init__(sloc)

    def type_check(self, var_tys):
        pass

    def find_variable_type(self, var, var_tys) -> str:
        for scope in reversed(var_tys):
            if var in scope:
                return scope[var]
        return ValueError(f'Variable {var} not in scope')


####################
# Blocks

class Block(Stmt):
    def __init__(self, sloc, stmts: List[Stmt]):
        super().__init__(sloc)
        self.stmts = stmts

    def type_check(self, var_tys):
        var_tys.append(dict())
        for stmt in self.stmts:
            stmt.type_check(var_tys)
        var_tys = var_tys[:-1]

    @property
    def js_obj(self):
        return {'tag': 'Block',
                'stmts': [stmt.js_obj for stmt in self.stmts]}


####################
# Expressions

class Expr(Node):
    """Superclass of all expressions"""

    def __init__(self, sloc):
        super().__init__(sloc)


class Variable(Expr):
    """Program variable"""

    def __init__(self, sloc, name: str, type: str):
        """
        name -- string representation of the name of the variable
        """
        super().__init__(sloc)
        # assert name in self.vardecls
        self.name = name
        self.ty = type

    def type_check(self, var_tys):
        pass

    @property
    def js_obj(self):
        return {'tag': 'Variable',
                'type': self.ty,
                'name': self.name}


class Number(Expr):
    """Number literal"""

    def __init__(self, sloc, value: int):
        """
        value -- int representing the value of the number
        """
        super().__init__(sloc)
        self.value = value
        self.ty = 'int'

    def type_check(self, var_tys):
        pass

    @property
    def js_obj(self):
        return {'tag': 'Number',
                'value': str(self.value)}


class Bool(Expr):
    '''Boolean true or false'''

    def __init__(self, sloc, value: bool):
        super().__init__(sloc)
        '''
        value -- bool representing whether the expression is true or false
        '''
        self.value = value
        self.ty = 'bool'

    def type_check(self, var_tys):
        pass

    @property
    def js_obj(self):
        return {'tag': 'Bool',
                'value': 1 if self.value else 0}


class OpApp(Expr):
    """Operator application"""

    def __init__(self, sloc, op: str, args):
        """
        op -- string representation of the operator
        args -- operands (all Expr instances)
        """
        super().__init__(sloc)
        assert isinstance(op, str), op
        self.op = op
        self.args = tuple(args)     # make container class explicitly a tuple

    def type_check(self, var_tys):
        for arg in self.args:
            arg.type_check(var_tys)

        if self.op in {'PLUS', 'MINUS', 'TIMES', 'DIV',
                       'MODULUS', 'BITAND', 'BITOR', 'BITXOR',
                       'BITSHL', 'BITSHR', 'UMINUS', 'NEG'
                       } and all([arg.ty == 'int' for arg in self.args]):
            self.ty = 'int'
        elif self.op in {'EQUALITY', 'DISEQUALITY',
                         'LT', 'LEQ', 'GT', 'GEQ', 'BITCOMPL'
                         } and all([arg.ty == 'int' for arg in self.args]):
            self.ty = 'bool'
        elif self.op in {'BOOLAND', 'BOOLOR', 'NOT'
                         } and all([arg.ty == 'bool' for arg in self.args]):
            self.ty = 'bool'
        else:
            raise TypeError(
                f'Operation {self.op} not defined for arguments {self.args} with types {tuple([arg.ty for arg in self.args])}')

    @property
    def js_obj(self):
        return {'tag': 'OpApp',
                'op': self.op,
                'args': [arg.js_obj for arg in self.args]}

####################
# Statements


class Vardecl(Stmt):
    '''Variable declarations'''

    def __init__(self, sloc, var: Variable, expr: Expr):
        '''
        var -- a Variable instance
        expr -- an Expr instance
        '''
        super().__init__(sloc)
        self.var = var
        self.expr = expr

    def type_check(self, var_tys):
        if self.var.name in var_tys[-1]:
            raise ValueError(
                f'Variable {self.var.name} already declared in same scope')
        self.expr.type_check(var_tys)
        self.var.ty = self.expr.ty
        var_tys[-1][self.var.name] = self.var.ty

    @property
    def js_obj(self):
        return {'tag': 'Vardecl',
                'lhs': self.var.js_obj,
                'rhs': self.expr.js_obj}


class IfElse(Stmt):
    def __init__(self, sloc, condition: Expr, block: Block, ifrest):
        '''
        condition -- condition to enter the block 
        block -- list of statements to execute
        ifrest -- else blocks of type Block or IfElse
        '''
        super().__init__(sloc)
        assert isinstance(ifrest, (Block, IfElse))
        self.condition = condition
        self.block = block
        self.ifrest = ifrest

    def type_check(self, var_tys):
        self.condition.type_check(var_tys)
        if self.condition.ty != 'bool':
            raise TypeError(
                f'IfElse condition must be of type bool (cannot be of type {self.condition.ty}')
        self.block.type_check(var_tys)
        self.ifrest.type_check(var_tys)

    @property
    def js_obj(self):
        return {'tag': 'IfElse',
                'condition': self.condition.js_obj,
                'block': self.block.js_obj,
                'ifrest': self.ifrest.js_obj}


class While(Stmt):
    def __init__(self, sloc, condition: Expr, block: Block):
        '''
        condition -- condition to enter the block
        block -- list of statements
        '''
        super().__init__(sloc)
        self.condition = condition
        self.block = block

    def type_check(self, var_tys):
        self.condition.type_check(var_tys)
        if self.condition.ty != 'bool':
            raise TypeError(
                f'While condition must be of type bool (cannot be of type {self.condition.ty}')
        self.block.type_check(var_tys)

    @property
    def js_obj(self):
        return {'tag': 'While',
                'condition': self.condition.js_obj,
                'stmts': self.block.js_obj}


class Jump(Stmt):
    def __init__(self, sloc, op: str):
        super().__init__(sloc)
        self.op = op

    def type_check(self, var_tys):
        pass

    @property
    def js_obj(self):
        return {'tag': self.op.capitalize()}


class Assign(Stmt):
    """Assignments"""

    def __init__(self, sloc, var: Variable, expr: Expr):
        """
        var -- a Variable instance
        expr -- an Expr instance
        """
        super().__init__(sloc)
        self.var = var
        self.expr = expr

    def type_check(self, var_tys):
        var_type = self.find_variable_type(self.var.name, var_tys)
        self.expr.type_check(var_tys)
        if var_type != self.expr.ty:
            raise TypeError(
                f"Assignment of variable '{self.var.name}' of type '{var_type}' to expr of type '{self.expr.ty}'")

    @property
    def js_obj(self):
        return {'tag': 'Assign',
                'lhs': self.lhs.js_obj,
                'rhs': self.rhs.js_obj}


class Print(Stmt):
    def __init__(self, sloc, expr: Expr):
        """
        expr -- an Expr instance
        """
        super().__init__(sloc)
        self.expr = expr

    def type_check(self, var_tys):
        self.expr.type_check(var_tys)
        if self.expr.ty != 'int':
            raise TypeError(f'Cannot print expr of type {self.expr.ty}')

    @property
    def js_obj(self):
        return {'tag': 'Print',
                'arg': self.arg.js_obj}

####################
# Programs

class Program(Node):
    def __init__(self, sloc, lvars: list, block: Block):
        super().__init__(sloc)
        self.block = block
        self.lvars = lvars
        self.type_check([])

    def type_check(self, var_tys):
        self.block.type_check(var_tys)

    @property
    def js_obj(self):
        return {'tag': 'Program',
                'vars': self.lvars,
                'block': self.block.js_obj}
