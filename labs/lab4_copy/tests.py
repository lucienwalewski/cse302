from tac_cfopt import optimize
import subprocess
import json
import os
from tac2x64 import compile_tac_from_json
import sys
sys.path.append('../lab3')
# sys.path.append('..')


tac_path = 'tac_examples'
tac_files = [os.path.join(dp, f)
             for dp, _, fn in os.walk(tac_path) for f in fn if f.endswith("tac.json")]
    


def test_tac_optimization():

    for file in tac_files:

        with open(file, 'r') as fp:
            tac = json.load(fp)
        tac = tac[0]['body']

        ## get optimized tac
        optimized_tac = optimize(tac)
        with open("optim/"+file, 'w') as file_write:
            json.dump([{'proc': '@main', 'body': optimized_tac}], file_write)
        
        ## compile optimized tac
        compile_tac_from_json("optim/"+file)
        cmd = ['gcc', '-o', "optim/"+file[:-4] + "exe", 'bx_runtime.c',  "optim/"+file[:-4]+"s"]
        p = subprocess.Popen(cmd)
        print(f'{"optim/"+file[:-4]+"s"} -> {"optim/"+file[:-4] + "exe"}')
        

        ## compile original tac
        compile_tac_from_json(file)
        cmd = ['gcc', '-o', file[:-4]+"exe", 'bx_runtime.c', file[:-4] + "s"]
        p = subprocess.Popen(cmd)
        print(f'{file[:-4]+"s"} -> {file[:-4]+"exe"}')

       
        ## run and display the output of optimized tac
        cmd = ["optim/"+file[:-4]+"exe"]
        output1 = subprocess.Popen( cmd, stdout=subprocess.PIPE ).communicate()[0]
        print()
        print("output for optimized procedure : ")
        print(output1)

        ## run and display the output of original tac
        cmd = ["./" +file[:-4]+"exe"]
        output2 = subprocess.Popen( cmd, stdout=subprocess.PIPE ).communicate()[0]
        print()
        print("output for original procedure : ")
        print(output2)

        ## compare 
        print()
        print("Optimized tac incorrect." if output1!=output2 else "Optimized tac correct")



        

            
            
    #cmd = ["rm", "optim/"+file[:-4]+"s", "optim/"+file[:-4]+"exe",file[:-4]+"s",file[:-4]+"exe" ]
    #p = subprocess.Popen(cmd)


            

    






if __name__ == '__main__':

    test_tac_optimization()
