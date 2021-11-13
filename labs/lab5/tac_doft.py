import sys
import argparse

from cfg import *
from ssagen import *
from tac import *


def DSE():
    """
    Main function for the TAC-DOF translator.
    """

def GCP():
    pass


if __name__ == "__main__":
    # Parse the command line arguments
    ap = argparse.ArgumentParser(
        description='Control flow optimization. TAC->TAC')
    ap.add_argument('fname', metavar='FILE', type=str, nargs=1,
                    help='The BX(JSON) file to process')
    opts = ap.parse_args(sys.argv[1:])
    ap.add_argument('-o', '--output', dest='output', type=str)
    fname = opts.fname[0]

    tac_list = load_tac(fname)
    for tac_unit in tac_list:
        if isinstance(tac_unit, Proc):
            cfg = infer(tac_unit)
            crude_ssagen(tac_unit, cfg)
            # cfg.write_dot(fname + '.dot')
            # os.system(f'dot -Tpdf -O {fname}.dot.{tac_unit.name[1:]}.dot')
            livein, liveout = dict(), dict()
            recompute_liveness(cfg, livein, liveout)
            # print(liveout)
            for ins in cfg.instrs():
                if ins.opcode in ('div', 'mod', 'call'):
                    continue
                if ins.dest:
                    print(ins.dest)
                    print(liveout[ins])
                    if ins.dest not in liveout[ins]:
                        print(ins)

