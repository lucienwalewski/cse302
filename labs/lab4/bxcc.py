'''Chains bx->ast, ast->tac, tac->64
to produce an executable from a bx file.
Optimizes the intermediate tac. 

Usage:
    python3 bxcc.py filename.bx
    
Returns:
    filename.s'''

import argparse
import json
import subprocess
import sys

from bx2front import bxfront
from bx_ast import Program
from bx2tac import bx2tac, bx2tacjson
from tac2x64 import compile_tac
from ast2tac import Prog
from tac_cfopt import optimize

if __name__ == '__main__':
    ap = argparse.ArgumentParser(description='Codegen: BX (JSON) to ASM (x64)')
    ap.add_argument('--keep-tac', dest='keep_tac', action='store_true', default=False,
                    help='Produce intermediate tac.json file')
    ap.add_argument('--optimize', dest='optim', action='store_true', default=True,
                    help='Optimize intermediate tac.json file')
    ap.add_argument('fname', metavar='FILE', type=str, nargs=1,
                    help='The BX(JSON) file to process')
    opts = ap.parse_args(sys.argv[1:])
    fname = opts.fname[0]

    program: Program = bxfront(fname)  # Parse + type-check
    prog: Prog = Prog(program)  # Create ast + tac
    tac = prog.js_obj  # Create json for tac
    if opts.optim:
        tac = optimize(tac) # Optimize tac
    if opts.keep_tac:
        with open(fname + '.tac.json', 'w') as fp:
            json.dump(tac, fp, indent=2)
    compile_tac(tac, fname[:-3] + '.s')  # Compile tac to x64

    # Linking and running
    cmd = ['gcc', '-o', fname[:-3], 'bx_runtime.c', fname[:-3] + '.s']
    p = subprocess.Popen(cmd)
    p.wait()
    cmd = ['rm', fname[:-3] + '.s']
    p = subprocess.Popen(cmd)
    p.wait()
    print(f'{fname[:-3] + ".bx"} -> {fname[:-3]}')
