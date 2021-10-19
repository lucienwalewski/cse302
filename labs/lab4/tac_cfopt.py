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
from typing import List


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

        self._destinations = []
        self.update_dest()
        self._prev = []
        self._succ = []
        self.cfg = False

    @property
    def prev(self):
        return self._prev

    @property
    def succ(self):
        return self._succ

    @property
    def label(self):
        return self._label

    @property
    def destinations(self):
        return self._destinations

    def update_dest(self):

        for instr in self.instructions[1:]:
            if instr['opcode'] in conditional_jumps:
                self._destinations.append(instr['args'][1])
            elif instr['opcode'] == 'jmp':
                self._destinations.append(instr['args'][0])
        

    def add_prev(self, prev):
        '''Add BasisBlock to list of predecessors'''
        assert isinstance(prev, BasicBlock)
        self._prev.append(prev)

    def add_succ(self, succ):
        '''Add BasicBlock to list of successors'''
        assert isinstance(succ, BasicBlock)
        self._succ.append(succ)


def _fresh_label() -> int:
    '''Obtain fresh label'''
    global __last_label
    __last_label += 1
    t = f'%.Lb{__last_label}'
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

    if body[0]['opcode'] != 'label':
        body[:0] = [{"opcode": "label", "args": [
            _fresh_label()], "result": []}]

    body_labelled = []
    for i, instr in enumerate(body):
        if instr['opcode'] in conditional_jumps + ['jmp']:
            body_labelled.append(instr)
            if body[i + 1]['opcode'] != 'label':
                body_labelled.append({'opcode': 'label', 'args': [
                    _fresh_label()], 'result': []})
        else:
            body_labelled.append(instr)

    block_start, block_end = 0, 1
    block_list = []
    while block_end < len(body_labelled):
        while body_labelled[block_end]['opcode'] not in ['jmp', 'ret', 'label'] + conditional_jumps:
            block_end += 1
        if body_labelled[block_end]['opcode'] in ['jmp', 'ret'] + conditional_jumps:
            block_list.append(BasicBlock(body_labelled[block_start:block_end+1]))
            block_start = block_end + 1
            block_end += 2
        else:  # Label
            block_list.append(BasicBlock(body_labelled[block_start:block_end]))
            block_start = block_end
            block_end += 1

    for i, block in enumerate(block_list):
        if block.instructions[-1]['opcode'] not in ['jmp', 'ret']:
            block.instructions.append({'opcode': 'jmp', 'args':
                                        block_list[i+1].instructions[0]['args'], 'result': []})
            block.update_dest()
    return block_list


def build_cfg(current_block, basic_blocks):
    '''Given a list of basic blocks construct the 
    cfg of the procedure.'''
    
    current_block.cfg = True

  
    for dest_block in [basic_block for basic_block in basic_blocks if basic_block.label in current_block.destinations] :
    
        dest_block = dest_block if dest_block.cfg else build_cfg(dest_block, basic_blocks) 
        dest_block.add_prev(current_block)
        current_block.add_succ(dest_block)

    print([ba.cfg for ba in basic_blocks])
    

    return current_block


def apply_control_flow_simplification(cfg):
    pass


def serialize(cfg):
    pass


def optimize(json_tac):
    body = json_tac["body"]
    basic_blocks = build_basic_blocks(body)
    entry_blocks = basic_blocks[0]
    cfg = build_cfg(entry_blocks,basic_blocks)

    # cfg_optimized = apply_control_flow_simplification(cfg)
    # serialized_tac = serialize(cfg_optimized)


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
    json_tac = json.load(json_tac_file)[0]
    optimized_tac = optimize(json_tac)

    if opts.o:
        json_tac_file = open(opts.fname_dest[0], "w")
        json.dump(optimized_tac, json_tac_file)

    else:
        print(optimized_tac)
