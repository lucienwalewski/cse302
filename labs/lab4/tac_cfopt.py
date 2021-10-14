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

conditional_jumps = [] ## list of cond jump instructions

class BasicBlock():
    def __init__(self, instructions, prev, succ) -> None:
        assert isinstance(instructions, list)
        assert isinstance(prev, BasicBlock)
        assert isinstance(succ, BasicBlock)
        self.instructions = instructions
        self.prev = prev
        self.succ = succ
    
    @property
    def prev(self):
        return self.prev

    @property
    def succ(self):
        return self.succ


def build_basic_blocks(body):
    '''
    1. Add an entry label before first instruction if needed.
    2. For jumps, add a label after the instruction if one doesn’t already exist.
    3. Start a new block at each label; accumulate instructions in the block until encountering a jump
    (inclusive), a ret (inclusive), or another label (exclusive).
    4. Add explicit jmps for fall-throughs. All blocks must end with a ret or a jmp.
    '''

    list_of_blocks = []
    block = []

    
        ## add entry label to block

    if body[0]["opcode"] != label : ## add label to beginning of the block
        pass

    
    while body : 

        i = 0
        
        while True :
            ## go through instructions until we reach a jump or a conditionnal jump followed by a non jump instruction.
            if  (body[i]["opcode"] == ["jmp","ret"]) or  (  body[i]["opcode"] in conditional_jumps and (body[i+1]["opcode"] not in conditional_jumps+["jmp","ret"] or i+1 >= len(body))  ) :
                break
            i +=1 


        block = body[:i+1]

        if block[-1]["opcode"] in conditional_jumps :
            pass
            ## add an unconditionnal jump after the sequence of tac 




        list_of_blocks.append(block)
        body = body[i+1:]

            


            




def build_cfg(basic_blocks: List):
    pass

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


    

