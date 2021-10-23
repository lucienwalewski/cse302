#!/usr/bin/env python3

from typing import Union, List

"""
A class hierarchy for the AST of the BX language.
"""

####################
# Nodes


from typing import Type

declarations = []
declarations_line = {}

def reset():
    global declarations, declarations_line
    declarations = []
    declarations_line = {}

class Node:
    """Superclass of all AST nodes"""
    vardecls = {}
    fname = ''

    def __init__(self, sloc):
        """
        sloc -- source location linenumber
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
        raise ValueError(f'Variable {var} not in scope at line {self.sloc}')


####################
# Declarations




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

    def syntax_check(self, fname):
        for stmt in self.stmts:
            stmt.syntax_check(fname)

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

    def expr_check(self, fname):
        if self.name not in declarations:
            raise ValueError(f'{fname}:line {self.sloc}:Error:Undeclared variable "{self.name}"')

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

    def expr_check(self, fname):
        if self.value < 0 or (self.value >> 63):
            raise ValueError(
                f'{fname}:line {self.sloc}:Error:Number "{self.value}" out of range [0, 2<<63)')

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

    def expr_check(self, fname):
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
                       'BITSHL', 'BITSHR', 'UMINUS', 'NEG', 'BITCOMPL'
                       } and all([arg.ty == 'int' for arg in self.args]):
            self.ty = 'int'
        elif self.op in {'EQUALITY', 'DISEQUALITY',
                         'LT', 'LEQ', 'GT', 'GEQ' 
                         } and all([arg.ty == 'int' for arg in self.args]):
            self.ty = 'bool'
        elif self.op in {'BOOLAND', 'BOOLOR', 'BOOLNEG'
                         } and all([arg.ty == 'bool' for arg in self.args]):
            self.ty = 'bool'
        else:
            raise TypeError(
                f'Operation {self.op} not defined for arguments {self.args} with types {tuple([arg.ty for arg in self.args])} at line {self.sloc}')

    def expr_check(self, fname):
        for arg in self.args:
            arg.expr_check(fname)

    @property
    def js_obj(self):
        return {'tag': 'OpApp',
                'op': self.op,
                'args': [arg.js_obj for arg in self.args]}

####################
# Statements




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
                f'IfElse condition must be of type bool (cannot be of type {self.condition.ty} at line {self.sloc}')
        self.block.type_check(var_tys)
        self.ifrest.type_check(var_tys)

    def syntax_check(self, fname):
        self.condition.expr_check(fname)
        self.block.syntax_check(fname)
        self.ifrest.syntax_check(fname)

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
                f'While condition must be of type bool (cannot be of type {self.condition.ty} at line {self.sloc}')
        self.block.type_check(var_tys)

    def syntax_check(self, fname):
        self.condition.expr_check(fname)
        self.block.syntax_check(fname)


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

    def syntax_check(self, fname):
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
                f"Assignment of variable '{self.var.name}' of type '{var_type}' to expr of type '{self.expr.ty}' at line {self.sloc}")

    def syntax_check(self, fname):
        self.expr.expr_check(fname)
        self.var.expr_check(fname)

    @property
    def js_obj(self):
        return {'tag': 'Assign',
                'lhs': self.lhs.js_obj,
                'rhs': self.rhs.js_obj}

class Eval(Stmt):
    '''Evaluations'''
    def __init__(self, sloc, expr: Expr):
        super().__init__(sloc)
        self.expr = expr

    def type_check(self, var_tys):
        # FIXME
        return super().type_check(var_tys)

    def syntax_check(self, fname):
        # FIXMe
        pass

    @property
    def js_obj(self):
        # FIXME
        pass

class Return(Stmt):
    def __init__(self, sloc, expr: Union[Expr, None]):
        super().__init__(sloc)
        self.expr = expr

    def type_check(self, var_tys):
        # FIXME
        return super().type_check(var_tys)

    def syntax_check(self, fname):
        # FIXMe
        pass

    @property
    def js_obj(self):
        # FIXME
        pass

# class Print(Stmt):
#     def __init__(self, sloc, expr: Expr):
#         """
#         expr -- an Expr instance
#         """
#         super().__init__(sloc)
#         self.expr = expr

#     def type_check(self, var_tys):
#         self.expr.type_check(var_tys)
#         if self.expr.ty != 'int':
#             raise TypeError(f'Cannot print expr of type {self.expr.ty} at line {self.sloc}')

#     def syntax_check(self, fname):
#         self.expr.expr_check(fname)

#     @property
#     def js_obj(self):
#         return {'tag': 'Print',
#                 'arg': self.arg.js_obj}



class Decl(Node):
    '''Superclass of declarations'''
    def __init__(self, sloc):
        super().__init__(sloc)



class Varinit(Decl):
    '''Variable init'''

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
                f'Variable {self.var.name} already declared in same scope at line {self.sloc}')
        self.expr.type_check(var_tys)
        self.var.ty = self.expr.ty
        var_tys[-1][self.var.name] = self.var.ty

    def syntax_check(self, fname):
        global declarations
        self.expr.expr_check(fname)
        if self.var.name in declarations:
            raise ValueError(f'{fname}:line {self.sloc}:Error:Duplicate declaration of variable "{self.var.name}"\n'f'{fname}:line {declarations_line[self.var.name]}:Info:Earlier declaration of "{self.var.name}"')

        declarations.append(self.var.name)
        declarations_line[self.var.name] = self.sloc
        
    @property
    def js_obj(self):
        return {'tag': 'Varinit',
                'lhs': self.var.js_obj,
                'rhs': self.expr.js_obj}

class Ty(Node):
    def __init__(self, sloc, ty: str):
        super().__init__(sloc)
        assert type in ['int', 'bool']
        self.ty = ty

    @property
    def js_obj(self):
        # FIXME
        pass

class Vardecl(Decl):
    '''Variable decarations'''

    def __init__(self, sloc, vars: List[Varinit], ty: Ty) -> None:
        super().__init__()
        assert len(vars) > 0
        self.vars = vars
        self.ty = ty






class Param(Node):
    def __init__(self, sloc, names: List[str], ty: Ty):
        super().__init__(sloc)
        assert len(names) > 0
        self.names = names
        self.ty = ty

class Procdecl(Decl):
    def __init__(self, sloc, name: str, params: list[Param], return_type: Union[Ty, None], block: Block) -> None:
        super().__init__()
        self.params = params
        self.return_type = return_type
        self.block = block




####################
# Programs

class Program(Node):
    def __init__(self, sloc, decls: list[Decl]):
        super().__init__(sloc)
        self.decls = decls
        self.type_check([])

    def type_check(self, var_tys):
        self.block.type_check(var_tys)
        # FIXME

    def syntax_check(self, fname):
        fname = fname
        self.block.syntax_check(fname)
        # FIXME

    @property
    def js_obj(self):
        # FIXME
        return {'tag': 'Program',
                'vars': self.lvars,
                'decls': self.decls.js_obj}

