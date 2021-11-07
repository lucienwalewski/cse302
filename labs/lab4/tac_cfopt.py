"""
CFG inference from linearized TAC
• Coalescing of linear chains of blocks
• Unreachable code elimination (UCE)
• Jump threading for unconditional jump sequences
• Jump threading to turn conditional jumps into unconditional jumps
• Serialization of the CFG back to ordinary TAC
"""


import sys
import argparse
import json
from typing import List, Tuple, Union


__last_label = 0

_conditional_jumps = ["je", "jne", "jl", "jle",
                      "jg", "jge"]  # list of cond jump instructions

_conditional_jumps_pars = {'je': ['je', 'jle', 'jge'], 'jne': ['jne'],
                           'jl': ['jl', 'jne', 'jle'], 'jle': ['jle'],
                           'jg': ['jg', 'jne', 'jge'], 'jge': ['jge']}


class BasicBlock():
    def __init__(self, instructions) -> None:
        '''
        instructions -- list of tac instructions
        '''
        assert isinstance(instructions, list)
        self.instructions = instructions
        label = instructions[0]
        assert label["opcode"] == 'label', 'Incorrect beginning of basic block'
        self._label = label["args"][0]
        self._prev = set()
        self.update_succ()
        # self._empty_body = True if len(self.instructions) == 2 else False

    # @property
    # def prev(self):
    #     return self._prev

    @property
    def succ(self):
        return self._succ

    @property
    def label(self):
        return self._label

    def update_succ(self):
        '''Iterates over instructions and adds labels
        and jumps to list of destinations'''
        self._succ = set()
        for instr in self.instructions[1:]:
            if instr['opcode'] in _conditional_jumps:
                self._succ.add(instr['args'][1])
            elif instr['opcode'] == 'jmp':
                self._succ.add(instr['args'][0])

    # def add_prev(self, prev: str):
    #     '''Add BasisBlock to list of predecessors'''
    #     self._prev.add(prev)

    def add_succ(self, succ: str):
        '''Add BasicBlock to list of successors'''
        self._succ.add(succ)


class CFG():
    def __init__(self, entry_block: str, blocks: List[BasicBlock]) -> None:
        self._construct_cfg(entry_block, blocks)

    def __getitem__(self, label: str) -> BasicBlock:
        '''Return the block with input label "label"'''
        return self._block_map[label]

    def successors(self, label: str):
        return iter(self._fwd[label])

    def predecessors(self, label: str):
        return iter(self._bwd[label])

    def add_node(self, block):
        pass

    def add_edge(self, label_from, label_to):
        pass

    def _construct_cfg(self, entry_block: str, blocks: List[BasicBlock]) -> None:
        '''Constructs the cfg'''
        for block in blocks:
            block.update_succ()
        self._entry_block = entry_block
        self._block_map = dict({block.label: block for block in blocks})
        self._fwd = dict({label: set() for label in self._block_map})
        self._bwd = dict({label: set() for label in self._block_map})
        for block in self._block_map:
            for succ in self._block_map[block].succ:
                self._fwd[block].add(succ)

        # self._check_validity()
        for origin, dests in self._fwd.items():
            for dest in dests:
                self._bwd[dest].add(origin)

    def _can_merge(self, b1: str, b2: str) -> bool:
        '''Check if two block can be merged'''
        return self._fwd[b1] == {b2} and self._bwd[b2] == {b1}

    def _is_empty(self, block: str) -> bool:
        '''Check if a block is empty'''
        instrs = self._block_map[block].instructions
        return len(instrs) == 2 and instrs[1]['opcode'] == 'jmp'

    def _coalesce(self) -> bool:
        '''Coalesce all linear blocks'''
        modified = False
        while True:
            recently_modified = False
            for b1 in self._block_map:
                if len(self._fwd[b1]) == 1:
                    b2 = next(iter(self._fwd[b1]))
                    if self._can_merge(b1, b2) and b2 != self._entry_block:
                        self._block_map[b1].instructions = self._block_map[b1].instructions[:-1] \
                            + self._block_map[b2].instructions
                        self._uce()
                        modified = True
                        recently_modified = True
                        break  # Repeat process
            if recently_modified:
                continue
            else:
                break  # No more blocks that can be merged
        return modified

    def _uce(self) -> None:
        '''Perform Unreachable Code Elimination'''
        self._construct_cfg(self._entry_block, self._block_map.values())
        visited_blocks = self._uce_traversal(self._entry_block, set())
        self._construct_cfg(self._entry_block, [
                            basic_block for block_key, basic_block in self._block_map.items() if block_key in visited_blocks])

    def _uce_traversal(self, block: str, visited_blocks: set) -> set:
        '''Perform DFS on the cfg and return all the visited blocks'''
        visited_blocks.add(block)
        for block in self._fwd[block]:
            if block not in visited_blocks:
                visited_blocks.add(block)
                visited_blocks = self._uce_traversal(block, visited_blocks)
        return visited_blocks

    def _unconditional_jump_threading_sequencing(self) -> bool:
        '''Sequence a linear sequence of blocks'''
        modified = False
        while True:
            recently_modified = False
            for b1 in self._block_map:
                if len(self._fwd[b1]) == 1:
                    block_sequence = [b1]
                    bi = b1
                    while True:
                        bj = next(iter(self._fwd[bi]))
                        if self._can_merge(bi, bj) and self._is_empty(bj):
                            block_sequence.append(bj)
                            bi = bj
                        else:
                            block_sequence.append(bj)
                            bi = bj
                            break  # End of sequence
                    if len(block_sequence) > 2:
                        self._block_map[b1].instructions[-1]['args'] = [bi]
                        self._uce()
                        modified = True
                        recently_modified = True
                        break  # Repeat process
            if recently_modified:
                continue
            else:
                break  # No more blocks to merge
        return modified

    def _fetch_condition(self, block: str) -> str:
        pass

    def _check_writes(self, block: str, temporary: str) -> bool:
        '''Check if there are any writes to a temporary in a given block'''
        return any((True if temporary in instr['result'] else False for instr in self._block_map[block].instructions))

    def _update_jmp(self, block: str, label: str) -> None:
        '''Given a new label update the jmp at the end of a block'''
        self._block_map[block].instructions[-1]['args'] = [label]

    def _conditional_jump_threading_sequencing(self) -> bool:
        '''Turn a sequence of conditional jumps into uncoditional
        jumps with jump threading'''
        modified = False
        while True:
            for b1 in self._block_map:
                for b2 in self._fwd[b1]:
                    jmp_instr_b1 = next(
                        (instr for instr in self._block_map[b1].instructions if instr['opcode']
                         in _conditional_jumps if instr['args'][-1] == b2), None)
                    if jmp_instr_b1:
                        temporary = jmp_instr_b1['args'][0]
                        jmp_instr_b2 = next(
                            ((i, instr) for i, instr in enumerate(self._block_map[b2].instructions) if instr['opcode']
                             in _conditional_jumps if instr['args'][0] == temporary), None)
                        if jmp_instr_b2:
                            if not self._check_writes(b2, temporary) and jmp_instr_b2[1]['opcode'] in _conditional_jumps_pars[jmp_instr_b1['opcode']]:
                                deleted_instr = self._block_map[b2].instructions.pop(
                                    jmp_instr_b2[0])
                                self._update_jmp(b2, deleted_instr['args'][1])
                                self._uce()
                                modified = True
                                break  # Repeat process
            break  # No more blocks to perform conditional jmp threading on
        return modified

    def _remove_redundant_jumps(self, instrs: list) -> list:
        '''Remove redundant jumps at the end of blocks
        once serialized'''
        new_instrs = []
        for i, instr in enumerate(instrs[:-1]):
            if instr['opcode'] == 'jmp':
                if instr['args'][0] == instrs[i + 1]['args'][0]:
                    continue
            else:
                new_instrs.append(instr)
        new_instrs.append(instrs[-1])
        return new_instrs

    def optimize(self) -> None:
        '''Apply the available optimization routines'''
        modified = True
        while modified:
            modified = False
            modified |= self._unconditional_jump_threading_sequencing()
            modified |= self._coalesce()
            modified |= self._conditional_jump_threading_sequencing()

    def serialize(self) -> list:
        '''Serialize the cfg and return the tac'''
        remaining_blocks = set(self._block_map.keys())
        remaining_blocks.remove(self._entry_block)
        schedule: List[str] = []
        current_block: str = self._entry_block
        while True:
            while True:
                schedule.append(current_block)
                potential_successors = [
                    block for block in self._fwd[current_block] if block not in schedule]
                if not potential_successors:
                    break
                current_block = potential_successors[0]
                remaining_blocks.remove(current_block)
            if not remaining_blocks:
                break
            current_block = remaining_blocks.pop()
        tac = []
        for block in schedule:
            tac += self._block_map[block].instructions
        return tac

    def _check_validity(self) -> bool:
        '''Verify that the current state of the cfg is valid'''
        print(self._block_map.keys())
        print(self._fwd.keys())
        print(self._bwd.keys())
        return True


def _fresh_label() -> int:
    '''Obtain fresh label'''
    global __last_label
    __last_label += 1
    t = f'%.L{__last_label}'
    return t


def find_largest_label(body: list) -> int:
    return max([int(instr['args'][0][3:]) for instr in body if instr['opcode'] == 'label'], default=0)


def build_basic_blocks(body: list) -> List[BasicBlock]:
    """
    1. Add an entry label before first instruction if needed.
    2. For jumps, add a label after the instruction if one doesn’t already exist.
    3. Start a new block at each label; accumulate instructions in the block until encountering a jump
    (inclusive), a ret (inclusive), or another label (exclusive).
    4. Add explicit jmps for fall-throughs. All blocks must end with a ret or a jmp.
    """
    global __last_label
    __last_label = max(__last_label, find_largest_label(body))

    # Add entry label if not present
    if body[0]['opcode'] != 'label':
        body[: 0] = [{"opcode": "label", "args": [
            _fresh_label()], "result": None}]

    # Add labels after jumps if necessary
    body_labelled = []
    for i, instr in enumerate(body):
        if instr['opcode'] in _conditional_jumps + ['jmp']:
            body_labelled.append(instr)
            if body[i + 1]['opcode'] != 'label':
                body_labelled.append({'opcode': 'label', 'args': [
                    _fresh_label()], 'result': None})
        else:
            body_labelled.append(instr)

    # Create list of BasicBlocksblock_labellei
    block_start, block_end = 0, 1
    block_list: List[BasicBlock] = []
    while block_end < len(body_labelled):
        while body_labelled[block_end]['opcode'] not in ['jmp', 'ret', 'label'] + _conditional_jumps:
            block_end += 1
        if body_labelled[block_end]['opcode'] in ['jmp', 'ret'] + _conditional_jumps:
            block_list.append(BasicBlock(
                body_labelled[block_start: block_end+1]))
            block_start = block_end + 1
            block_end += 2
        else:  # Label
            block_list.append(BasicBlock(
                body_labelled[block_start: block_end]))
            block_start = block_end
            block_end += 1

    # Edge case for tac ending with label
    if block_start == len(body_labelled) - 1 and body_labelled[block_start]['opcode'] == 'label':
        body_labelled.append({'opcode': 'ret', 'args': [], 'result': None})
        block_list.append(BasicBlock(body_labelled[block_start:]))

    # Add explicit jumps for fall-through
    for i, block in enumerate(block_list[:-1]):
        if block.instructions[-1]['opcode'] not in ['jmp', 'ret']:
            block.instructions.append({'opcode': 'jmp', 'args':
                                       [block_list[i+1].label], 'result': None})
            block.add_succ(block_list[i+1].label)

    return block_list


def optimize(tac: list) -> list:
    '''Given an input list of TAC declarations, 
    optimize the tac for bodies of procedure declarations'''
    optimized_decls = []
    for decl in tac:
        if 'proc' in decl:
            optimized_decls.append(
                {'proc': decl['proc'], 'args': decl['args'], 'body': optimize_body(decl['body'])})
        else:
            optimized_decls.append(decl)
    return optimized_decls


def optimize_body(body: list) -> list:
    '''Given an input list of TAC instructions, 
    optimize the TAC and output a new list of TAC
    instructions'''
    basic_blocks = build_basic_blocks(body)
    entry_block = basic_blocks[0].label
    cfg = CFG(entry_block, basic_blocks)
    cfg.optimize()
    serialized_tac = cfg.serialize()
    # serialized_tac = cfg._remove_redundant_jumps(serialized_tac)
    return serialized_tac


if __name__ == '__main__':
    ap = argparse.ArgumentParser(
        description='Codegen: Tac (JSON) to Tac optimized (JSON)')
    ap.add_argument('-o', dest='o', action='store_true', default=False,
                    help="stores resulting json in a file")
    ap.add_argument('fname', metavar='FILE', type=str, nargs=1,
                    help='The TAC(JSON) file to process')
    opts, rem_args = ap.parse_known_args(sys.argv[1:])
    if opts.o:
        ap.add_argument('fname_dest', metavar='FILE_DEST', type=str, nargs=1,
                        help='The TAC(JSON) file to create')
        opts = ap.parse_args(sys.argv[1:])

    json_tac_file = open(opts.fname[0])
    json_tac = json.load(json_tac_file)
    optimized_tac = optimize(json_tac)

    if opts.o:
        json_tac_file = open(opts.fname_dest[0], "w")
        json.dump(optimized_tac, json_tac_file)

    else:
        print(optimized_tac)
