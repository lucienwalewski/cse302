'''Chains bx->ast, ast->tac, tac->64
to produce an executable from a bx file

Usage:
    python3 bxcc.py filename.bx
    
Returns:
    filename.s'''

import sys
import json
import argparse

from bx2tac import bx2tac, bx2tacjson
from tac2x64 import compile_tac

if __name__ == '__main__':
    ap = argparse.ArgumentParser(description='Codegen: BX (JSON) to ASM (x64)')
    ap.add_argument('--keep-tac', dest='keep_tac', action='store_true', default=False,
                    help='Produce intermediate tac.json file')
    ap.add_argument('fname', metavar='FILE', type=str, nargs=1,
                    help='The BX(JSON) file to process')
    opts = ap.parse_args(sys.argv[1:])
    if opts.keep_tac:
        tac = bx2tacjson(opts.fname[0])
    tac = bx2tac(opts.fname[0])
    compile_tac(tac, opts.fname[0])

    # print([instr.js_obj for instr in tac])
    # with open(opts.fname[0].removesuffix('.bx') + '.tac.json', 'w') as fp:
    #     json.dump([instr.js_obj for instr in tac], fp)

    # compile_tac()
