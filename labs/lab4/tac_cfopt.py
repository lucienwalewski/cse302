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

conditional_jumps = ["je","jne","jl","jle","jg","jge"] # list of cond jump instructions

class BasicBlock():
    def __init__(self, instructions) -> None:
        '''
        instructions -- list of tac instructions
        prev -- predecessor(s) of the block
        succ -- successor(s) of the block'''
        assert isinstance(instructions, list)
        self.instructions = instructions
        label = instructions[0]
        assert label["opcode"] == 'label', 'Incorrect beginning of basic block'
        self._label = label["args"][0]

        self._destinations = []
        for instr in self.instructions[1:]:
            if instr['opcode'] in conditional_jumps:
                self._destinations.append(instr['args'][1])
            elif instr['opcode'] == 'jmp':
                self._destinations.append(instr['args'][0])

        self._prev = []
        self._succ = []
    
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
    def end(self):
        return self._end

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


def build_basic_blocks(body):
    """
    1. Add an entry label before first instruction if needed.
    2. For jumps, add a label after the instruction if one doesn’t already exist.
    3. Start a new block at each label; accumulate instructions in the block until encountering a jump
    (inclusive), a ret (inclusive), or another label (exclusive).
    4. Add explicit jmps for fall-throughs. All blocks must end with a ret or a jmp.
    """
    list_of_blocks = []
    block = []

    
        ## add entry label to block
    
    

    
    while body : 

        

        if body[0]["opcode"] != "label" : ## add label to beginning of the block
            body[:0] = [{"opcode":"label","args":[_fresh_label()], "result":[]}]

        i = 0
        
        while True :
            ## go through instructions until we reach a jump or a conditionnal jump followed by a non jump instruction.
            if  (i == len(body)-1 or body[i]["opcode"] in ["jmp","ret"]) or  (  body[i]["opcode"] in conditional_jumps and (body[i+1]["opcode"] not in conditional_jumps+["jmp","ret"] or i+1 >= len(body))  ) :
                break
        
              
            i +=1 

        block = body[:i+1]

        if i == len(body)-1 :
            block.append({"opcode":"ret","args":["this will be changed"], "result":[]})


        if block[-1]["opcode"] in conditional_jumps :
            ## last instruction is a conditionnal jump. we add an unc. jump
            if body[0]["opcode"] == "label" :
                ## there is already a label for the next block. we jump to this label
                block.append({"opcode":"jmp","args":[body[0]["args"]], "result":[]})
            else :
                ## otherwise, we create the label and the jump to it 
                body[:0] = [{"opcode":"label","args":[_fresh_label()], "result":[]}]
                block.append({"opcode":"jmp","args":[f'%.Lb{__last_label}'], "result":[]})


        list_of_blocks.append(BasicBlock(block))
        body = body[i+1:]




    return list_of_blocks



            

            


def build_cfg(basic_blocks: List[BasicBlock]) -> BasicBlock:
    '''Given a list of basic blocks construct the 
    cfg of the procedure. Assume that the first block in the
    list is the entry block'''
    entry_block = basic_blocks[0] 
    current_block = entry_block
    while True:
        next_label = current_block.end
        next_block = next(block for block in basic_blocks if block.label == next_label)
        current_block.add_succ(next_block)
        next_block.add_prev(current_block)



    return entry_block


def apply_control_flow_simplification(cfg):
    pass


def serialize(cfg) :
    pass


def optimize(json_tac) :
    body = json_tac["body"]
    basic_blocks = build_basic_blocks(body)
    cfg = build_cfg(basic_blocks)
    cfg_optimized = apply_control_flow_simplification(cfg)
    serialized_tac = serialize(cfg_optimized)


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description='Codegen: Tac (JSON) to Tac optimized (JSON)')
    ap.add_argument('-o', dest='o', action='store_true', default=False,
                    help="stores resulting json in a file")
    ap.add_argument('fname', metavar='FILE', type=str, nargs=1,
                    help='The TAC(JSON) file to process')
    opts, rem_args = ap.parse_known_args(sys.argv[1:])
    if opts.o : 
        ap.add_argument('fname_dest', metavar='FILE_DEST', type=str, nargs=1,
                    help='The TAC(JSON) file to create')
        opts = ap.parse_args(sys.argv[1:])



    json_tac_file = open(opts.fname[0])
    json_tac = json.load(json_tac_file)[0]
    optimized_tac = optimize(json_tac)

    if opts.o :
        json_tac_file = open(opts.fname_dest[0],"w")
        json.dump(optimized_tac,json_tac_file)

    else :
        print(optimized_tac)


    

