#!/usr/bin/env python3

"""
A class hierarchy for the AST of the BX language.
"""

####################
# Nodes


class Node:
    """Superclass of all AST nodes"""

    def __init__(self, sloc):
        """
        sloc -- source location (list of 6 numbers; see handout for meaning)
        """
        self.sloc = sloc


####################
# Blocks


class Block(Node) :
    def __init__(self, sloc, stmts):
        super().__init__(sloc)
        self.stmts = stmts

    @staticmethod
    def load(block):
        """
        blocks -- list of statements 
        returns: a Block instance if json is valid, None otherwise
        """
        stmts = []
        lvars = []

        block = block[0][1]
        
        while len(block) > 0:
            st, block = block[0], block[1:]
            print("statement",st)
            if st[0][0] == "<vardecl>" :
                # store the new variable somewhere
                pass
            stmt = Stmt.load(st)
            assert stmt is not None, st
            stmts.append(stmt)





####################
# Expressions

class Expr(Node):
    """Superclass of all expressions"""

    def __init__(self, sloc):
        super().__init__(sloc)

    @staticmethod
    def load(js_obj):
        """
        js_obj -- data produced by json.load()
        returns: an Expr instance if json is valid, None otherwise
        """
        if not isinstance(js_obj, list):
            return None
        sloc = js_obj[1] if len(js_obj) > 1 else None
        js_obj = js_obj[0]
        if js_obj[0] == '<var>':
            return Variable(sloc, js_obj[1])
        elif js_obj[0] == '<number>':
            return Number(sloc, js_obj[1])
        elif js_obj[0] == '<binop>':
            return OpApp(sloc, js_obj[2][0][0], [Expr.load(js_obj[1]), Expr.load(js_obj[3])])
        elif js_obj[0] == '<unop>':
            return OpApp(sloc, js_obj[1][0][0], [Expr.load(js_obj[2])])
        else:
            return None

    def type_check(self):
        pass


class Variable(Expr):
    """Program variable"""

    def __init__(self, sloc, name: str):
        """
        name -- string representation of the name of the variable
        """
        super().__init__(sloc)
        self.name = name

    def type_check(self):
        pass

    @property
    def js_obj(self):
        return {'tag': 'Variable',
                'name': self.name}


class Number(Expr):
    """Number literal"""

    def __init__(self, sloc, value: int):
        """
        value -- int representing the value of the number
        """
        super().__init__(sloc)
        self.value = value
    
    def type_check(self):
        self.ty = 'int'

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
    
    def type_check(self):
        self.ty = 'bool'


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
        for arg in args:
            assert isinstance(arg, Expr), arg.__class__
        self.args = tuple(args)     # make container class explicitly a tuple

    def type_check(self, _):
        for arg in self.args:
            arg.type_check(_)

        if self.op in {'PLUS', 'MINUS', 'TIMES', 'DIV',
                         'MODULUS', 'BITAND', 'BITOR', 'BITXOR',
                         'BITSHL', 'BITSHR', 'UMINUS', 'NEG'}:
            for arg in self.args:
                assert arg.ty == 'int' 
            self.ty = 'int'
        elif self.op in {'EQUALITY', 'DISEQUALITY',
                         'LT', 'LEQ' 'GT', 'GEQ', 'BITCOMPL'}:
            for arg in self.args:
                assert arg.ty == 'int'
            self.ty = 'bool'
        elif self.op in {'BOOLAND', 'BOOLOR', 'NOT'}:
            for arg in self.args:
                assert arg.ty == 'bool'
            self.ty = 'bool'

    @property
    def js_obj(self):
        return {'tag': 'OpApp',
                'op': self.op,
                'args': [arg.js_obj for arg in self.args]}

####################
# Statements


class Stmt(Node):
    """Superclass of all statements"""

    def __init__(self, sloc):
        super().__init__(sloc)

    @staticmethod
    def load(js_obj):
        """
        js_obj -- data produced by json.load()
        returns: a Stmt instance if json is valid, None otherwise
        """
        if not isinstance(js_obj, list):
            return None
        sloc = js_obj[1] if len(js_obj) > 1 else None
        js_obj = js_obj[0]
        if js_obj[0] == '<while>':
             return While(sloc, Expr.load(js_obj[1]), Block.load(js_obj[2]))
        elif js_obj[0] == '<assign>':
            return Assign(sloc, Expr.load(js_obj[1]), Expr.load(js_obj[2]))
        elif js_obj[0] == '<eval>':
            js_obj = js_obj[1][0]
            return Print(sloc, Expr.load(js_obj[2][0]))
        else:
            return None


class Vardecl(Stmt):
    '''Variable declarations'''

    def __init__(self, sloc, lhs: Variable, rhs: Expr):
        '''
        lhs -- a Variable instance
        rhs -- an Expr instance
        '''
        super().__init__(sloc)
        self.lhs = lhs
        self.rhs = rhs
        self.rhs.type_check()
        self.lhs.ty = self.rhs.ty

    @property
    def js_obj(self):
        return {'tag': 'Vardecl',
                'lhs': self.lhs.js_obj,
                'rhs': self.rhs.js_obj}

class IfRest(Stmt):
    def __init__(self, sloc, args):
        '''
        ifelse -- optional ifelse
        block -- optional Block
        '''
        super().__init__(sloc)
        # FIXME

class IfElse(Stmt):
    def __init__(self, sloc, condition: Expr, block: Block, ifrest: IfRest):
        '''
        condition -- condition to enter the block 
        block -- list of statements to execute
        ifrest -- else blocks
        '''
        super().__init__(sloc)
        self.condition = condition
        self.block = block
        self.ifrest = ifrest



class While(Stmt):
    def __init__(self, sloc, condition: Expr, block: Block):
        '''
        condition -- condition to enter the block
        block -- list of statements
        '''
        super().__init__(sloc)
        self.condition = condition 
        self.block = block

    @property
    def js_obj(self):
        return {'tag': 'While',
                'lhs': self.condition.js_obj,
                'rhs': self.Block.js_obj}




class Assign(Stmt):
    """Assignments"""

    def __init__(self, sloc, lhs: Variable, rhs: Expr):
        """
        lhs -- a Variable instance
        rhs -- an Expr instance
        """
        super().__init__(sloc)
        self.lhs = lhs
        self.rhs = rhs

    @property
    def js_obj(self):
        return {'tag': 'Assign',
                'lhs': self.lhs.js_obj,
                'rhs': self.rhs.js_obj}


class Print(Stmt):
    def __init__(self, sloc, arg: Expr):
        """
        arg -- an Expr instance
        """
        super().__init__(sloc)
        assert isinstance(arg, Expr)
        self.arg = arg

    @property
    def js_obj(self):
        return {'tag': 'Print',
                'arg': self.arg.js_obj}

####################
# Programs


class Program(Node):
    def __init__(self, sloc, lvars, stmts):
        super().__init__(sloc)
        self.lvars = lvars
        self.stmts = stmts

    @staticmethod
    def load(js_obj):
        assert isinstance(js_obj, list)
        sloc = js_obj[1] if len(js_obj) > 1 else None
        js_obj = js_obj[0]
        assert isinstance(js_obj, list)
        assert len(js_obj) == 1
        js_obj = js_obj[0][0]
        assert len(js_obj[2]) == 0  # type of args
        block = js_obj[4][0][1][:]
        # load the variables
        lvars = []
        while len(block) > 0:
            if block[0][0][0] != '<vardecl>':
                break
            var, block = block[0][0], block[1:]
            lvars.append(var[1][0])
        # load the statements
        stmts = []
        while len(block) > 0:
            st, block = block[0], block[1:]
            stmt = Stmt.load(st)
            assert stmt is not None, st
            stmts.append(stmt)
        return Program(sloc, lvars, stmts)

    # @staticmethod
    # def load(fname):
    #   with open(fname, 'rb') as fp:
    #     js_obj = json.load(fp)
    #     assert 'ast' in js_obj, js_obj
    #     return Program(js_obj['ast'])

    @property
    def js_obj(self):
        return {'tag': 'Program',
                'vars': self.lvars,
                'stmts': [stmt.js_obj for stmt in self.stmts]}
