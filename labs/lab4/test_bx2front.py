from tac_cfopt import optimize
import subprocess
import json
import bx2front
import os
from tac2x64 import compile_tac_from_json
import sys



tac_path = 'examples/'
tac_files = [os.path.join(dp, f)
             for dp, _, fn in os.walk(tac_path) for f in fn if f.endswith(".bx")]





class HiddenPrints:
    def __enter__(self):
        self._original_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stdout = self._original_stdout

def run_tests() :
    for tac_file in tac_files : 
        if "regression" in tac_file :
            try :
                with HiddenPrints():
                    bx2front.bxfront(tac_file)
                print(f'ERROR {tac_file} regression file should not be parsed correctly')
            except : 
                print("PASS")
        else :
            try :
                with HiddenPrints():
                    bx2front.bxfront(tac_file)
                print("PASS")
            except : print(f'ERROR {tac_file} error during parsing of correct file')

        
    
        

if __name__ == '__main__':

    run_tests()

    
