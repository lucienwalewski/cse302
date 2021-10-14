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

conditional_jumps = [] ## list of cond jump instructions


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
        
    
    while body != []: 

        i = 0
        if body[0]["opcode"] != label : ## add label to beginning of the block
        
        while True :
            if body[i]["opcode"] in conditional_jumps and (body[i+1]["opcode"] not in conditional_jumps or i+1 >= len(body)) :
                break
            i +=1 


        while i<len(body) and body[i]["opcode"] not in ["jmp","ret"] : ## add other jumps to the list for the code to be correct
            i +=1

        if body[i]["opcode"] in conditional_jumps :
            ## go to the end of the conditionnal jump sequence and add an unconditionnal jump
            ## dont forget to increment i when doing this 

        block = body[:i+1]
        list_of_blocks.append(block)
        body = body[i+1:]

            


            




def build_cfg(basic_blocks):
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


    if opts.o :
        json_tac_file = open(opts.fname[0])
        json_tac = json.load(json_tac_file)[0]
        optimized_tac = optimize(json_tac)
        json_tac_file = open(opts.fname_dest[0],"w")
        json.dump(optimized_tac,json_tac_file)

    else :

        json_tac_file = open(opts.fname[0])
        json_tac = json.load(json_tac_file)[0]
        optimized_tac = optimize(json_tac)
        print(optimized_tac)


    # if sys.argv[1]=="o" :
    #     assert argc==4 
    #     assert argv[3].endswith(".tac.json")
    #     json_tac_file = open(argv[2])
    #     json_tac = json.load(json_tac_file)
    #     optimized_tac = optimize(json_tac)
    #     json_tac_file = open(argv[3],"w")
    #     json.dump(optimized_tac,json_tac_file)
    # else :
    #     assert argc==2 
    #     assert argv[2].endswith(".tac.json")
    #     json_tac_file = open(argv[2])
    #     json_tac = json.load(json_tac_file)
    #     optimized_tac = optimize(json_tac)
    #     print(optimized_tac)

        

        


    

