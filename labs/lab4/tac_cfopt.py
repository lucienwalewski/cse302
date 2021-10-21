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

conditional_jumps = ["je", "jne", "jl", "jle",
                     "jg", "jge"]  # list of cond jump instructions


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
        self._succ = set()
        self.update_succ()
        self._empty_body = True if len(self.instructions) == 2 else False

    @property
    def prev(self):
        return self._prev

    @property
    def succ(self):
        return self._succ

    @property
    def label(self):
        return self._label

    def update_succ(self):
        '''Iterates over instructions and adds labels
        and jumps to list of destinations'''
        for instr in self.instructions[1:]:
            if instr['opcode'] in conditional_jumps:
                self._succ.add(instr['args'][1])
            elif instr['opcode'] == 'jmp':
                self._succ.add(instr['args'][0])

    def add_prev(self, prev: str):
        '''Add BasisBlock to list of predecessors'''
        self._prev.add(prev)

    def add_succ(self, succ: str):
        '''Add BasicBlock to list of successors'''
        self._succ.add(succ)


class CFG():
    def __init__(self, entry_block: str, blocks: List[BasicBlock]) -> None:
        self._entry_block = entry_block
        self._block_map = {block.label: block for block in blocks}
        self._fwd = {label: set() for label in self._block_map}
        self._bwd = {label: set() for label in self._block_map}
        self._construct_cfg()
        self._empty_blocks = {
            block for block in self._block_map if self._block_map[block]._empty_body}

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

    def _construct_cfg(self) -> None:
        '''Constructs the cfg'''
        for block in self._block_map:
            for succ in self._block_map[block].succ:
                self._fwd[block].add(succ)

        for origin, dests in self._fwd.items():
            for dest in dests:
                self._bwd[dest].add(origin)

    def _coalesce(self) -> None:
        '''Coalesce all linear blocks'''
        merged_blocks = []
        for b1, dests in self._fwd.items():
            if len(dests) == 1:
                b2 = next(iter(dests))
                if len(self._bwd[b2]) == 1:
                    merged_blocks.append((b1, b2))
        self._merge(merged_blocks)

    def _merge(self, merged_blocks: List[Tuple[str, str]]) -> None:
        '''Given a list of coalescable blocks, updated the cfg'''
        for b1, b2 in merged_blocks:
            instructions = self._block_map[b1].instructions[:-1] \
                + self._block_map[b2].instructions
            self._block_map[b1] = BasicBlock(instructions)
            if b2 in self._empty_blocks:
                self._empty_blocks.remove(b2)
            if self._block_map[b1]._empty_body:
                self._empty_blocks.add(b1)
            for succ in self._fwd[b2]:
                self._bwd[succ].remove(b2)
                self._bwd[succ].add(b1)
            self._fwd[b1] = self._fwd[b2]
            del self._block_map[b2]
            del self._fwd[b2]
            del self._bwd[b2]

    def _uce(self) -> None:
        '''Perform Unreachable Code Elimination'''
        visited_blocks = self._uce_traversal(self._entry_block, set())
        unreachable_blocks = self._block_map.keys() - visited_blocks
        for block in unreachable_blocks:
            del self._block_map[block]
            if block in self._fwd:
                del self._fwd[block]
            if block in self._bwd:
                del self._bwd[block]
            if block in self._empty_blocks:
                self._empty_blocks.remove(block)

    def _uce_traversal(self, block: str, visited_blocks: set) -> set:
        '''Perform DFS on the cfg and return all the visited blocks'''
        visited_blocks.add(block)
        for block in self._fwd[block]:
            if block not in visited_blocks:
                visited_blocks.add(block)
                visited_blocks = self._uce_traversal(block, visited_blocks)
        return visited_blocks

    def _jump_threading_sequencing(self) -> None:
        '''Sequence a linear sequence of blocks'''

        changed = True
        while changed:
            changed = False
            empty_pairs = []
            for bi in self._block_map.keys():
                dests = self._fwd[bi]  # Might have to replace with get
                if len(dests) == 1:
                    bj = next(iter(dests))
                    if len(self._bwd[bj]) == 1 \
                            and len(self._block_map[bj].instructions) == 2 \
                            and self._block_map[bj].instructions[-1]['opcode'] == 'jmp':
                        empty_pairs.append((bi, bj))
            if len(empty_pairs):
                changed = True
                while empty_pairs:
                    bi, bj = empty_pairs.pop()
                    self._fwd[bi] = self._fwd[bj]

    def optimize(self) -> None:
        '''Apply the available optimization routines'''
        self._coalesce()
        self._uce()
        self._jump_threading_sequencing()

    def serialize(self) -> list:
        '''Serialize the cfg and return the tac'''
        tac = self._block_map[self._entry_block].instructions
        entry = self._block_map.pop(self._entry_block)
        for block in self._block_map.values():
            tac += block.instructions
        self._block_map[self._entry_block] = entry
        return tac


def _fresh_label() -> int:
    '''Obtain fresh label'''
    global __last_label
    __last_label += 1
    t = f'%.L{__last_label}'
    return t


def find_largest_label(body: list) -> int:
    return max([int(instr['args'][0][3:]) for instr in body if instr['opcode'] == 'label'])


def build_basic_blocks(body: list) -> List[BasicBlock]:
    """
    1. Add an entry label before first instruction if needed.
    2. For jumps, add a label after the instruction if one doesn’t already exist.
    3. Start a new block at each label; accumulate instructions in the block until encountering a jump
    (inclusive), a ret (inclusive), or another label (exclusive).
    4. Add explicit jmps for fall-throughs. All blocks must end with a ret or a jmp.
    """
    global __last_label
    __last_label = find_largest_label(body)

    # Add entry label if not present
    if body[0]['opcode'] != 'label':
        body[: 0] = [{"opcode": "label", "args": [
            _fresh_label()], "result": []}]

    # Add labels after jumps if necessary
    body_labelled = []
    for i, instr in enumerate(body):
        if instr['opcode'] in conditional_jumps + ['jmp']:
            body_labelled.append(instr)
            if body[i + 1]['opcode'] != 'label':
                body_labelled.append({'opcode': 'label', 'args': [
                    _fresh_label()], 'result': []})
        else:
            body_labelled.append(instr)

    # Create list of BasicBlocks
    block_start, block_end = 0, 1
    block_list = []
    while block_end < len(body_labelled):
        while body_labelled[block_end]['opcode'] not in ['jmp', 'ret', 'label'] + conditional_jumps:
            block_end += 1
        if body_labelled[block_end]['opcode'] in ['jmp', 'ret'] + conditional_jumps:
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
        body_labelled.append({'opcode': 'ret', 'args': [], 'result': []})
        block_list.append(BasicBlock(body_labelled[block_start:]))

    # Add explicit jumps for fall-through
    for i, block in enumerate(block_list[:-1]):
        if block.instructions[-1]['opcode'] not in ['jmp', 'ret']:
            block.instructions.append({'opcode': 'jmp', 'args':
                                       [block_list[i+1].label], 'result': []})
            block.add_succ(block_list[i+1].label)

    return block_list


def optimize(body: list) -> list:
    '''Given an input list of TAC instructions, 
    optimize the TAC and output a new list of TAC
    instructions'''
    basic_blocks = build_basic_blocks(body)
    entry_block = basic_blocks[0].label
    cfg = CFG(entry_block, basic_blocks)
    cfg.optimize()
    # print(cfg._block_map.keys()) # Do not delete - useful for debugging
    # print(cfg._fwd.keys())
    # print(cfg._bwd.keys())
    serialized_tac = cfg.serialize()
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
    json_tac = json.load(json_tac_file)[0]['body']
    optimized_tac = optimize(json_tac)

    if opts.o:
        json_tac_file = open(opts.fname_dest[0], "w")
        json.dump(optimized_tac, json_tac_file)

    else:
        print(optimized_tac)
