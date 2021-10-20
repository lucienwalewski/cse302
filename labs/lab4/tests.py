from tac_cfopt import optimize
import subprocess
import json
import os
import sys
sys.path.append('../lab3')
# sys.path.append('..')


tac_path = 'tac_examples'
tac_files = [os.path.join(dp, f)
             for dp, _, fn in os.walk(tac_path) for f in fn]


def test_tac_optimization():
    for file in tac_files:
        with open(file, 'r') as fp:
            tac = json.load(fp)
            print(tac)
            tac = tac[0]['body']
            optimized_tac = optimize(tac)
            with open('optim.tac.json', 'w') as file_write:
                json.dump([{'proc': '@main', 'body': optimized_tac}], file_write)


if __name__ == '__main__':
    from tac2x64 import compile_tac_from_json
    test_tac_optimization()
