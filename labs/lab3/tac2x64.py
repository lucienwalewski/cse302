import sys
import json


def tac_to_x64(tac_instrs):
    for instruc in tac_instrs:
        pass  # Do something


def compile_tac(fname):
    if fname.endswith('.tac.json'):
        rname = fname[:-9]
    elif fname.endswith('.json'):
        rname = fname[:-5]
    else:
        raise ValueError(f'{fname} does not end in .tac.json or .json')
    tjs = None
    with open(fname, 'rb') as fp:
        tjs = json.load(fp)
    assert isinstance(tjs, list) and len(tjs) == 1, tjs
    tjs = tjs[0]
    assert 'proc' in tjs and tjs['proc'] == '@main', tjs
    asm = ['\t' + line for line in tac_to_x64(tjs['body'])]
    asm[:0] = [f'\t.globl main',
               f'\t.text',
               'main:',
               r'\tpushq \%rbp',
               r'\tmovq \%rsp, \%rbp',
               r'\tsubq $64, \%rsp', # To be modified (currently for 8 temporaries)
               r'\tmovq \%rbp, \%rsp',
               r'\tpopq \%rbp',
               r'\tmovq \$0, \%rax',
               r'\tretq']


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(f'Usage: {sys.argv[0]} tacfile.tac.json')
        sys.exit(1)
    compile_tac(sys.argv[1])
