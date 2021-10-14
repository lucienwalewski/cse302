"""
CFG inference from linearized TAC
• Coalescing of linear chains of blocks
• Unreachable code elimination (UCE)
• Jump threading for unconditional jump sequences
• Jump threading to turn conditional jumps into unconditional jumps
• Serialization of the CFG back to ordinary TAC
"""


import sys
import json


def build_basic_blocks(body):
    pass

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
    if sys.argv[1]=="o" :
        assert argc==4 
        assert argv[3].endswith(".tac.json")
        json_tac_file = open(argv[2])
        json_tac = json.load(json_tac_file)
        optimized_tac = optimize(json_tac)
        json_tac_file = open(argv[3],"w")
        json.dump(optimized_tac,json_tac_file)
    else :
        assert argc==2 
        assert argv[2].endswith(".tac.json")
        json_tac_file = open(argv[2])
        json_tac = json.load(json_tac_file)
        optimized_tac = optimize(json_tac)
        print(optimized_tac)

        

        


    
    
1
