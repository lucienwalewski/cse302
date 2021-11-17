import sys
import argparse
from typing import List, Union

from cfg import *
from ssagen import *
from tac import *

def DSE(cfg: CFG) -> None:
    """
    Global Dead Store Elimination
    """
    modified = True
    while modified:
        modified = False
        livein, liveout = dict(), dict()
        recompute_liveness(cfg, livein, liveout)

        new_instrs = []
        for ins in cfg.instrs():
            if ins.opcode not in ('div', 'mod', 'call'):
                # Check if dead store
                if ins.dest and ins.dest not in liveout[ins]:
                    modified = True
                    continue
            new_instrs.append(ins)
        if modified:
            cfg = infer(new_instrs)

def GCP(tlv, cfg: CFG) -> None:
    """
    Global Copy Propagation. This is a one-shot procedure.
    """
    crude_ssagen(tlv, cfg)


def optimize_decl(tac_proc: Union[Gvar, Proc]) -> Union[Gvar, Proc]:
    """
    Optimize a declaration. First perform DSE as many times as necessary,
    then GCP. 
    """
    cfg = infer(tac_proc)
    DSE(cfg)
    GCP(tac_proc, cfg)
    linearize(tac_proc, cfg)
    return tac_proc


def execute(tac_list: List):
    """Execute a TAC program"""
    gvars, procs = dict(), dict()
    for decl in tac_list:
        if isinstance(decl, Gvar):
            gvars[decl.name] = decl
        elif isinstance(decl, Proc):
            procs[decl.name] = decl
    tac.execute(gvars, procs, '@main', [])


if __name__ == "__main__":
    # Parse the command line arguments
    ap = argparse.ArgumentParser(
        description='Control flow optimization. TAC->TAC')
    ap.add_argument('fname', metavar='FILE', type=str, nargs=1,
                    help='The BX(JSON) file to process')
    ap.add_argument('-o', '--output', dest='output', type=str)
    opts = ap.parse_args(sys.argv[1:])
    fname = opts.fname[0]

    # Read the input file into tac
    try:
        tac_list = load_tac(fname)
    except ValueError as e:
        print(e)
        sys.exit(1)
    # Optimize the declarations
    new_tac_list = []
    for decl in tac_list:
        if isinstance(decl, Proc):
            new_tac_list.append(optimize_decl(decl))
        else: new_tac_list.append(decl)

    # Write the output file if requested
    if opts.output:
        with open(ap.output, 'w') as f:
            json.dump(new_tac_list, f)
    # Execute the program
    else:
        execute(new_tac_list)

    #     # cfg.write_dot(fname + '.dot')
    #     # os.system(f'dot -Tpdf -O {fname}.dot.{tac_unit.name[1:]}.dot')